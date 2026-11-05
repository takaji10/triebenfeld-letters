# -*- coding: utf-8 -*-
"""The red add/delete test.

ADD: the button puts a new pill at the centre of the current view (blue,
reading '· · ·'), the reading editor opens at once; dragging it into
place, typing the number and Enter commits it; it saves with its negative
id, survives a reload, and the import appends it to reds.yml as a real
mark. An Esc before typing withdraws it - nothing saved.

DELETE: clicking a pill opens the editor; a delete in the editor removes
the pill, the deletion is remembered by the mark's baked position, it
survives a reload, and the import drops the mark from reds.yml.
"""
import atexit
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

import test_server
from playwright.sync_api import sync_playwright

test_server.start()
atexit.register(test_server.stop)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

URL = test_server.URL
REDS = test_server.REDS_STATE
RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append((name, ok))
    print(('PASS ' if ok else 'FAIL ') + name + ('  -- ' + detail if detail else ''))


def launch(pw):
    for channel in ('msedge', 'chrome'):
        try:
            return pw.chromium.launch(channel=channel, headless=True)
        except Exception:
            pass
    return pw.chromium.launch(headless=True)


def wait_file(timeout=6.0):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            d = json.load(open(REDS, encoding='utf-8'))
            return d if isinstance(d, list) else d
        except Exception:
            time.sleep(0.1)
    return None


def settle(page):
    page.wait_for_function("""() => {
      const vp = viewer.viewport;
      const k = vp.getZoom() + ',' + vp.getCenter().x + ',' + vp.getCenter().y;
      const st = window.__settle = window.__settle || {};
      if (st.prev === k) { st.n = (st.n || 0) + 1; } else { st.n = 0; }
      st.prev = k;
      return st.n >= 4;
    }""", timeout=10000)


def main():
    os.makedirs('scratch/map4456/test-state', exist_ok=True)
    bak = tempfile.mktemp(suffix='.json')
    had = os.path.isfile(REDS)
    if had:
        shutil.copy(REDS, bak)
    yml_bak = tempfile.mktemp(suffix='.yml')
    shutil.copy('maps/pelzucki1896/reds.yml', yml_bak)
    try:
        if had:
            os.remove(REDS)
        with sync_playwright() as pw:
            browser = launch(pw)
            page = browser.new_page(viewport={'width': 1400, 'height': 900})
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)[:200]))
            page.goto(URL)
            page.wait_for_function(
                "const s = document.getElementById('status').textContent; "
                "s.includes('Loaded') || s.includes('Restored')",
                timeout=30000)
            for _ in range(2):
                page.mouse.move(700, 420)
                page.mouse.wheel(0, -300)
                time.sleep(0.15)
            settle(page)
            n_before = page.evaluate("() => redTags.length")
            centre = page.evaluate(
                "() => { const i = viewer.viewport.viewportToImageCoordinates("
                "viewer.viewport.getCenter());"
                " return { x: Math.round(i.x), y: Math.round(i.y) }; }")

            # ---- ADD: the button ----------------------------------------
            page.click('#red-add')
            time.sleep(0.4)
            check('the button adds a new pill at the view centre',
                  page.evaluate("() => redTags.length") == n_before + 1
                  and page.locator('.red-tag.new').count() == 1)
            pos = page.evaluate(
                "() => { const t = redTags.find(t => t.id < 0);"
                " return t ? { x: t.x, y: t.y } : null; }")
            check('the new pill sits at the view centre',
                  pos is not None and abs(pos['x'] - centre['x']) <= 2
                  and abs(pos['y'] - centre['y']) <= 2,
                  '%s vs centre %s' % (pos, centre))
            check('the reading editor opens at once',
                  page.locator('#red-editor').count() == 1)

            # Esc before typing withdraws it
            page.keyboard.press('Escape')
            time.sleep(0.3)
            check('an Esc before typing withdraws the new pill',
                  page.evaluate("() => redTags.length") == n_before
                  and page.locator('.red-tag.new').count() == 0,
                  page.inner_text('#status')[:70])

            # again, this time commit
            page.click('#red-add')
            time.sleep(0.3)
            # drag it a bit, then type the number and Enter
            pill = page.evaluate(
                "() => { const t = redTags.find(t => t.id < 0);"
                " const r = t.span.getBoundingClientRect();"
                " return { x: r.x + r.width / 2, y: r.y + r.height / 2 }; }")
            page.mouse.move(pill['x'], pill['y'])
            page.mouse.down()
            page.mouse.move(pill['x'] + 40, pill['y'] + 30, steps=3)
            page.mouse.up()
            time.sleep(0.3)
            page.locator('#red-num').fill('127')
            page.keyboard.press('Enter')
            time.sleep(0.5)
            got = page.evaluate(
                "() => { const t = redTags.find(t => t.id < 0);"
                " return t ? { raw: t.raw, x: t.x, y: t.y,"
                "              id: t.id } : null; }")
            check('the committed new red reads 127 at its dragged spot',
                  got and got['raw'] == '127' and got['id'] < 0, str(got))

            # the file carries it with its id (and no ox)
            d = wait_file()
            marks = d.get('marks', []) if isinstance(d, dict) else d
            ent = next((x for x in marks if x.get('id') is not None
                        and x['id'] < 0), None)
            check('the new red is in the file with its id',
                  ent is not None and ent['n'] == '127'
                  and 'ox' not in ent, str(ent))

            # the reload restores it
            page.reload()
            page.wait_for_function(
                "const s = document.getElementById('status').textContent; "
                "s.includes('Loaded') || s.includes('Restored')",
                timeout=30000)
            settle(page)
            back = page.evaluate(
                "() => { const t = redTags.find(t => t.id < 0);"
                " return t ? { raw: t.raw, x: t.x, y: t.y } : null; }")
            check('the new red comes back after a reload',
                  back and back['raw'] == '127', str(back))

            # ---- DELETE --------------------------------------------------
            # pick a baked pill that is topmost at its own point
            target = page.evaluate("""() => {
              for (const t of redTags) {
                if (t.id < 0) continue;
                const r = t.span.getBoundingClientRect();
                if (r.width < 2) continue;
                const x = r.x + r.width / 2, y = r.y + r.height / 2;
                if (document.elementFromPoint(x, y) === t.span)
                  return { x, y, raw: t.raw, ox: t.ox, oy: t.oy };
              }
              return null;
            }""")
            assert target, 'no clickable baked pill'
            page.mouse.click(target['x'], target['y'])
            time.sleep(0.3)
            check('the click opens the editor for the delete',
                  page.locator('#red-editor').count() == 1)
            page.locator('#red-del').click()
            time.sleep(0.4)
            gone = page.evaluate("""(t) => {
              return !redTags.some(r => r.ox === t.ox && r.oy === t.oy);
            }""", target)
            check('the Delete button removes the pill',
                  gone, page.inner_text('#status')[:80])
            d = wait_file()
            marks = d.get('marks', []) if isinstance(d, dict) else d
            dels = d.get('deleted', []) if isinstance(d, dict) else []
            check('the deletion is remembered by the baked position',
                  any(x['x'] == target['ox'] and x['y'] == target['oy']
                      for x in dels)
                  and not any(x.get('ox') == target['ox']
                              and x.get('oy') == target['oy']
                              for x in marks),
                  str(dels))

            # the reload keeps it deleted
            page.reload()
            page.wait_for_function(
                "const s = document.getElementById('status').textContent; "
                "s.includes('Loaded') || s.includes('Restored')",
                timeout=30000)
            still = page.evaluate("""(t) => {
              return !redTags.some(r => r.ox === t.ox && r.oy === t.oy);
            }""", target)
            check('the deleted red stays deleted after a reload', still)

            # ---- the import: addition + deletion in reds.yml -------------
            state = page.evaluate("""() => ({
              marks: redTags.map(t => {
                const e = { n: t.raw, x: t.x, y: t.y };
                if (t.id < 0) e.id = t.id;
                else if (t.ox != null) { e.ox = t.ox; e.oy = t.oy; }
                return e;
              }).filter(t => t.n),
              deleted: D.redsDeleted || []
            })""")
            print('STATE: marks=%d, deleted=%s, neg-ids=%s'
                  % (len(state['marks']), state['deleted'],
                     [m.get('id') for m in state['marks']
                      if m.get('id', 1) < 0]))
            tmpdir = tempfile.mkdtemp()
            tmp = os.path.join(tmpdir, 'red_labels_latest.json')
            json.dump(state, open(tmp, 'w', encoding='utf-8'),
                      ensure_ascii=False)
            p = subprocess.run([sys.executable,
                                'pipeline/maps/import_farms.py', tmp],
                               capture_output=True, text=True,
                               encoding='utf-8', errors='replace')
            import yaml
            ry = yaml.safe_load(open('maps/pelzucki1896/reds.yml',
                                     encoding='utf-8'))
            added = next((m for m in ry['marks'] if m['n'] == '127'), None)
            deleted = next((m for m in ry['marks']
                            if m['x'] == target['ox']
                            and m['y'] == target['oy']), None)
            check('the import appends the new mark to reds.yml',
                  p.returncode == 0 and added is not None
                  and added['x'] == back['x'] and added['y'] == back['y'],
                  (p.stdout[-200:] + p.stderr[-160:]) if added is None
                  else str(added))
            check('the import drops the deleted mark from reds.yml',
                  deleted is None,
                  'deleted ledger sent: %s | import said: %s'
                  % (state['deleted'],
                     [ln for ln in p.stdout.splitlines() if 'reds:' in ln]))
            shutil.rmtree(tmpdir)

            # ---- keyboard delete on a selected NEW red -------------------
            # the farm pills stack above the reds, so hide the names layer
            # to make the new pill clickable, as the editor would
            page.click('#names-toggle')
            time.sleep(0.3)
            page.click('#red-add')
            time.sleep(0.3)
            page.locator('#red-num').fill('218')
            page.keyboard.press('Enter')
            time.sleep(0.4)
            np = page.evaluate("""() => {
              const t = redTags.find(t => t.raw === '218');
              const r = t.span.getBoundingClientRect();
              return { x: r.x + r.width / 2, y: r.y + r.height / 2,
                       top: document.elementFromPoint(
                         r.x + r.width / 2, r.y + r.height / 2) === t.span };
            }""")
            check('a second new red is committed and clickable',
                  np is not None and np['top'], str(np))
            page.mouse.click(np['x'], np['y'])
            time.sleep(0.3)
            check('clicking the new red opens its editor',
                  page.locator('#red-editor').count() == 1)
            page.keyboard.press('Escape')
            time.sleep(0.2)
            check('Esc closes the editor but keeps the pill',
                  page.locator('#red-editor').count() == 0
                  and page.evaluate("() => redTags.some(t => t.raw === '218')"))
            page.keyboard.press('Delete')
            time.sleep(0.4)
            check('Delete removes the selected new red',
                  not page.evaluate("() => redTags.some(t => t.raw === '218')"),
                  page.inner_text('#status')[:80])
            page.click('#names-toggle')   # the names layer back on
            time.sleep(0.2)
            d2 = wait_file()
            m2 = (d2.get('marks', []) if isinstance(d2, dict) else d2)
            check('the withdrawn red leaves the saved file',
                  not any(x.get('n') == '218' for x in m2))
            # ---- the editor's Withdraw button on another new red ---------
            page.click('#red-add')
            time.sleep(0.3)
            page.locator('#red-num').fill('219')
            page.keyboard.press('Enter')
            time.sleep(0.4)
            page.evaluate(
                "() => redTags.find(t => t.raw === '219').el.click()")
            time.sleep(0.3)
            check('the editor offers Withdraw for a new red',
                  page.locator('#red-del').count() == 1
                  and page.locator('#red-del').inner_text() == 'Withdraw')
            page.locator('#red-del').click()
            time.sleep(0.4)
            check('Withdraw removes that new red',
                  not page.evaluate("() => redTags.some(t => t.raw === '219')"),
                  page.inner_text('#status')[:80])
            browser.close()
    finally:
        if had:
            shutil.copy(bak, REDS)
        elif os.path.isfile(REDS):
            os.remove(REDS)
        shutil.copy(yml_bak, 'maps/pelzucki1896/reds.yml')
        print('reds file, reds.yml restored / cleaned')
    failed = [n for n, ok in RESULTS if not ok]
    print(f'{len(RESULTS) - len(failed)}/{len(RESULTS)} passed'
          + ('' if not failed else ' — FAILED: ' + ', '.join(failed)))
    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
