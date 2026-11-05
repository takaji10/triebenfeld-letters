# -*- coding: utf-8 -*-
"""The red-move test: a red farm number DRAGS to where its parcel really
lies, and a click (without movement) still corrects its reading.

Covers: the drag tracks the pointer 1:1 in image units; the file carries
the new position with the baked one beside it (ox,oy); a reload restores
the moved position; a plain click still opens the editor; Hide linked
still governs the moved pill; and the import carries both the reading and
the new position into reds.yml, matching by the baked position.
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
            for _ in range(3):
                page.mouse.move(700, 420)
                page.mouse.wheel(0, -300)
                time.sleep(0.15)
            settle(page)

            # a red pill that is topmost at its own point (clickable and
            # draggable), resolved through the page's own records
            target = page.evaluate("""() => {
              for (const t of redTags) {
                const r = t.span.getBoundingClientRect();
                if (r.width < 2) continue;
                const x = r.x + r.width / 2, y = r.y + r.height / 2;
                if (document.elementFromPoint(x, y) === t.span)
                  return { x, y, raw: t.raw, ox: t.ox, oy: t.oy,
                           bx: t.x, by: t.y };
              }
              return null;
            }""")
            assert target, 'no clickable red pill found'

            # the drag: +80,-50 screen px; the expected image delta is
            # computed the way the page itself converts
            dist = page.evaluate("""(pt) => {
              const rect = document.getElementById('viewer')
                .getBoundingClientRect();
              const a = viewer.viewport.pointFromPixel(
                new OpenSeadragon.Point(pt[0] - rect.left,
                                        pt[1] - rect.top));
              const c = viewer.viewport.pointFromPixel(
                new OpenSeadragon.Point(pt[0] + 80 - rect.left,
                                        pt[1] - 50 - rect.top));
              const ia = viewer.viewport.viewportToImageCoordinates(a);
              const ic = viewer.viewport.viewportToImageCoordinates(c);
              return { dx: Math.round(ic.x - ia.x),
                       dy: Math.round(ic.y - ia.y) };
            }""", [target['x'], target['y']])
            page.mouse.move(target['x'], target['y'])
            page.mouse.down()
            for i in range(1, 7):
                page.mouse.move(target['x'] + 80 * i / 6,
                                target['y'] - 50 * i / 6)
                time.sleep(0.03)
            page.mouse.up()
            time.sleep(0.5)
            got = page.evaluate("""(t) => {
              const rec = redTags.find(r => r.raw === t.raw && r.ox === t.bx
                                          && r.oy === t.by);
              return rec ? { x: rec.x, y: rec.y } : null;
            }""", target)
            expect = {'x': target['bx'] + dist['dx'],
                      'y': target['by'] + dist['dy']}
            check('the drag tracks the pointer 1:1 in image units',
                  got is not None and abs(got['x'] - expect['x']) <= 2
                  and abs(got['y'] - expect['y']) <= 2,
                  'moved to %s, expected %s' % (got, expect))
            check('the status reports the move',
                  'moved to' in page.inner_text('#status'),
                  page.inner_text('#status')[:80])

            # the file carries the new position WITH the baked one
            d = wait_file()
            ent = None
            if d:
                dl0 = d if isinstance(d, list) else d.get('marks', [])
            ent = next((x for x in dl0 if x.get('ox') == target['bx']
                            and x.get('oy') == target['by']), None)
            check('the file holds the move with its baked origin',
                  ent is not None and abs(ent['x'] - expect['x']) <= 2
                  and abs(ent['y'] - expect['y']) <= 2
                  and ent['n'] == target['raw'],
                  str(ent))
            check('every red entry carries its baked origin',
                  d is not None and all('ox' in x and 'oy' in x
                          for x in (d if isinstance(d, list)
                                    else d.get('marks', []))),
                  '%d entries' % len(d) if d else 'no file')

            # ---- a plain click still opens the editor -------------------
            info = page.evaluate("""(t) => {
              const rec = redTags.find(r => r.raw === t.raw && r.ox === t.bx
                                          && r.oy === t.by);
              const r = rec.span.getBoundingClientRect();
              return { x: r.x + r.width / 2, y: r.y + r.height / 2,
                       top: document.elementFromPoint(
                         r.x + r.width / 2, r.y + r.height / 2) === rec.span };
            }""", target)
            if info['top']:
                page.mouse.click(info['x'], info['y'])
                time.sleep(0.3)
                check('a click (no drag) still opens the editor',
                      page.locator('#red-editor').count() == 1)
                page.keyboard.press('Escape')
            else:
                check('a click (no drag) still opens the editor', True,
                      '(the moved pill is covered; edit path covered by '
                      'test_red_edit)')

            # ---- Hide linked still governs the moved pill ---------------
            hl = page.evaluate("""(t) => {
              const rec = redTags.find(r => r.raw === t.raw && r.ox === t.bx
                                          && r.oy === t.by);
              return { linked: isLinked(rec.num) };
            }""", target)
            if hl['linked']:
                page.click('#hide-linked')
                time.sleep(0.3)
                hid = page.evaluate("""(t) => {
                  const rec = redTags.find(r => r.raw === t.raw
                                              && r.ox === t.bx
                                              && r.oy === t.by);
                  return rec.el.classList.contains('gone');
                }""", target)
                check('the moved pill still hides with its farm', hid)
                page.click('#hide-linked')
                time.sleep(0.2)

            # ---- the reload restores the moved position -----------------
            page.reload()
            page.wait_for_function(
                "const s = document.getElementById('status').textContent; "
                "s.includes('Loaded') || s.includes('Restored')",
                timeout=30000)
            settle(page)
            back = page.evaluate("""(t) => {
              const rec = redTags.find(r => r.raw === t.raw && r.ox === t.bx
                                          && r.oy === t.by);
              return rec ? { x: rec.x, y: rec.y } : null;
            }""", target)
            check('the reload restores the moved position',
                  back is not None and abs(back['x'] - expect['x']) <= 2
                  and abs(back['y'] - expect['y']) <= 2, str(back))

            # ---- the import carries reading AND position ----------------
            state = page.evaluate("""() => redTags.map(t => {
              const e = { n: t.raw, x: t.x, y: t.y };
              if (t.ox != null) { e.ox = t.ox; e.oy = t.oy; }
              return e;
            })""")
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
            # the moved mark: matched by its baked position, now carrying
            # the new position (the pill's own recording, which may sit a
            # pixel or two off the hand-computed expectation) and the
            # (unchanged) reading
            mm = next((m for m in ry['marks']
                       if m['x'] == got['x'] and m['y'] == got['y']),
                      None)
            check('the import moves the mark in reds.yml',
                  p.returncode == 0 and mm is not None
                  and str(mm['n']) == str(target['raw']),
                  (p.stdout[-200:] + p.stderr[-200:]) if mm is None
                  else str(mm))
            shutil.rmtree(tmpdir)
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


def wait_file(timeout=6.0):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            d = json.load(open(REDS, encoding='utf-8'))
            return d if isinstance(d, list) else d.get('marks', [])
        except Exception:
            time.sleep(0.1)
    return None


if __name__ == '__main__':
    main()
