# -*- coding: utf-8 -*-
"""The multiple-farmsteads test: one farm number, several labels.

A farmer can hold more than one farmstead within his plot, so one number
may need labels at several places. Covers: placing the same farm twice
(the farm stays armed after a placement), both pills on the map, both in
the panel with a 1/2 · 2/2 count, both in the save file, both back after a
reload, both hidden by Hide linked with their farm, Delete removing ONE
label while the other stays, and the import accepting the same number at
several positions but refusing one position twice.
"""
import atexit
import io
import json
import os
import shutil
import sys
import tempfile
import time

import requests

import test_server
from playwright.sync_api import sync_playwright

test_server.start()
atexit.register(test_server.stop)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

URL = test_server.URL
FARMS = test_server.FARMS_STATE
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


def main():
    backups = {}
    for p in (FARMS, REDS):
        if os.path.isfile(p):
            backups[p] = tempfile.mktemp(suffix='.json')
            shutil.copy(p, backups[p])
    yml_bak = tempfile.mktemp(suffix='.yml')
    shutil.copy('maps/pelzucki1896/farms.yml', yml_bak)
    try:
        for p in (FARMS, REDS):
            if os.path.isfile(p):
                os.remove(p)
        with sync_playwright() as pw:
            browser = launch(pw)
            page = browser.new_page(viewport={'width': 1400, 'height': 900})
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)[:200]))
            page.goto(URL)
            page.wait_for_function(
                "document.getElementById('status').textContent.includes('Loaded')",
                timeout=30000)

            def clear_spot():
                return page.evaluate("""() => {
                  for (let x = 320; x < 1280; x += 24) {
                    for (let y = 220; y < 780; y += 24) {
                      const e = document.elementFromPoint(x, y);
                      if (e && e.closest('#viewer') && !e.closest('.tag')
                          && !e.closest('.red-tag')) return { x, y };
                    }
                  }
                  return null;
                }""")

            # ---- place farm 12: one placement, then the farm disarms ----
            page.click('#missing .farmrow:has-text("12")')
            time.sleep(0.2)
            s1 = clear_spot()
            page.mouse.click(s1['x'], s1['y'])
            time.sleep(0.4)
            check('the first label of farm 12 is placed',
                  page.locator('[data-farm="12"]').count() == 1)
            check('the farm disarms after one placement',
                  'click its row again' in page.inner_text('#status'),
                  page.inner_text('#status')[:100])
            s2 = clear_spot()
            page.mouse.click(s2['x'], s2['y'])
            time.sleep(0.4)
            check('a stray plain click places nothing',
                  page.locator('[data-farm="12"]').count() == 1)

            s2 = clear_spot()

            # ---- deliberate second farmstead: re-arm, then Shift --------
            page.locator('#marked .farmrow:has-text("12")').first.click()
            time.sleep(0.3)
            check('re-arming a marked farm is one click',
                  'already has' in page.inner_text('#status'),
                  page.inner_text('#status')[:90])
            page.keyboard.down('Shift')
            page.mouse.click(s2['x'], s2['y'])
            page.keyboard.up('Shift')
            time.sleep(0.4)
            check('a Shift-click adds a second label of the same farm',
                  page.locator('[data-farm="12"]').count() == 2
                  and 'still armed' in page.inner_text('#status'),
                  page.inner_text('#status')[:100])
            p1, p2 = page.evaluate("() => [markPos(12), "
                                   "marksFor(12)[1] ? "
                                   "{ x: marksFor(12)[1].x, "
                                   "y: marksFor(12)[1].y } : null]")
            check('the two labels sit at their own places',
                  p1 and p2 and p1 != p2, '%s vs %s' % (p1, p2))

            # ---- the panel: one row per label, with the count ----------
            rows = page.locator('#marked .farmrow:has-text("12")')
            check('the panel lists both labels of farm 12',
                  rows.count() == 2
                  and rows.first.inner_text().replace('\u2116', '').strip()
                      .startswith('12')
                  and '1/2' in rows.first.inner_text()
                  and '2/2' in rows.nth(1).inner_text(),
                  rows.first.inner_text()[:40] + ' | '
                  + rows.nth(1).inner_text()[:40])

            # ---- the file carries both ---------------------------------
            d = json.load(open(FARMS, encoding='utf-8'))
            f12 = [x for x in d if x['n'] == 12]
            check('the save file holds both labels of farm 12',
                  len(f12) == 2 and len(d) == 103,
                  '%d entries for farm 12, %d total' % (len(f12), len(d)))

            # ---- both survive a reload ---------------------------------
            page.reload()
            page.wait_for_function(
                "const s = document.getElementById('status').textContent; "
                "s.includes('Loaded') || s.includes('Restored')",
                timeout=30000)
            check('both labels come back after a reload',
                  page.locator('[data-farm="12"]').count() == 2)

            # ---- Hide linked hides both, with their red numbers ---------
            page.click('#hide-linked')
            time.sleep(0.3)
            gone = page.evaluate("""() => {
              const firm = redTags.filter(t => t.num === 12 && !t.unsure);
              const unsure = redTags.filter(t => t.num === 12 && t.unsure);
              return {
                firmGone: firm.filter(t =>
                  t.el.classList.contains('gone')).length,
                firmAll: firm.length,
                unsureGone: unsure.filter(t =>
                  t.el.classList.contains('gone')).length,
                unsureAll: unsure.length
              };
            }""")
            check('Hide linked hides the farm\'s firm red numbers',
                  gone['firmAll'] > 0 and gone['firmGone'] == gone['firmAll'],
                  str(gone))
            check('Hide linked leaves the farm\'s unsure red numbers showing',
                  gone['unsureGone'] == 0, str(gone))
            page.click('#hide-linked')
            time.sleep(0.2)

            # ---- a marked row arms the farm for another placement -----
            # (the farm's own row in Marked behaves like the to-add rows)
            page.locator('#marked .farmrow:has-text("12")').first.click()
            time.sleep(0.3)
            check('selecting a marked farm arms it for a secondary place',
                  'already has' in page.inner_text('#status')
                  and 'next farmstead' in page.inner_text('#status'),
                  page.inner_text('#status')[:100])
            check('the armed farm\'s red numbers are outlined blue again',
                  page.evaluate(
                      "() => document.querySelectorAll('.red-num.hunt').length")
                  > 0)
            s3 = None
            for attempt in range(8):
                cand = page.evaluate("""(off) => {
                  for (let x = 320 + off; x < 1280; x += 90) {
                    for (let y = 220 + off; y < 780; y += 90) {
                      const e = document.elementFromPoint(x, y);
                      if (e && e.closest('#viewer') && !e.closest('.tag')
                          && !e.closest('.red-tag')) return { x, y };
                    }
                  }
                  return null;
                }""", attempt * 37)
                if cand is None:
                    continue
                page.keyboard.down('Shift')
                page.mouse.click(cand['x'], cand['y'])
                page.keyboard.up('Shift')
                time.sleep(0.4)
                if 'still armed' in page.inner_text('#status'):
                    s3 = cand
                    break
            check('the Shift-click adds a third label of the same farm',
                  s3 is not None
                  and page.locator('[data-farm="12"]').count() == 3
                  and "label " in page.inner_text('#status'),
                  page.inner_text('#status')[:90])
            page.keyboard.press('Escape')   # end the placement run
            time.sleep(0.2)

            # ---- Delete removes ONE label, the others stay -------------
            # the label is selected by clicking its pill (the panel row
            # arms the farm instead)
            page.evaluate(
                "() => document.querySelector('[data-farm=\"12\"]').click()")
            time.sleep(0.2)
            page.keyboard.press('Delete')
            time.sleep(0.4)
            left = page.evaluate("() => markPos(12) ? [markPos(12).x, "
                                 "markPos(12).y] : []")
            check('Delete removes one label, the others stay',
                  page.locator('[data-farm="12"]').count() == 2
                  and len(left) == 2,
                  'remaining at %s' % (left,))
            check('the status says a label of the farm was removed',
                  'labels remain' in page.inner_text('#status'),
                  page.inner_text('#status')[:90])

            # ---- a double-click cannot create a duplicate --------------
            before_dup = page.evaluate("() => marksFor(12).length")
            page.evaluate("""() => {
              const m = marksFor(12)[0];
              makeTag({ n: 12, x: m.x, y: m.y }, true);   // the same pixel
            }""")
            time.sleep(0.3)
            check('a label at an occupied pixel is refused (double-click)',
                  page.evaluate("() => marksFor(12).length") == before_dup
                  and 'nothing added' in page.inner_text('#status'),
                  page.inner_text('#status')[:90])

            # ---- the list's ✕ removes one label directly ---------------
            # hover finds the label first: the row shows its coordinates
            row = page.locator('#marked .farmrow:has-text("12")').first
            row.hover()
            time.sleep(0.2)
            tip = row.get_attribute('title')
            check('hovering a row names its label\'s place',
                  tip and 'at ' in tip, tip or 'no title')
            check('the hovered row highlights its own pill on the map',
                  page.evaluate(
                      "() => marksFor(12).some(m => "
                      "m.el.classList.contains('hovered'))"))
            page.mouse.move(10, 10)
            time.sleep(0.2)
            row.locator('.del').click()
            time.sleep(0.4)
            check('the list\'s ✕ removes that label directly',
                  page.locator('[data-farm="12"]').count() == before_dup - 1
                  and 'removed' in page.inner_text('#status'),
                  page.inner_text('#status')[:90])

            # ---- the server collapses exact duplicates silently --------
            # (a tab holding stacked duplicates once had every save
            # refused with 400, the banner re-appearing on every retry)
            base = test_server.URL.rsplit('/scratch/', 1)[0]
            r = requests.post(base + '/__save/farm_labels', json=[
                {'n': 9, 'x': 1, 'y': 2}, {'n': 9, 'x': 1, 'y': 2},
                {'n': 9, 'x': 3, 'y': 4}], timeout=5)
            check('the server collapses an exact duplicate to one label',
                  r.status_code == 200 and r.json()['saved'] == 2,
                  '%s %s' % (r.status_code, r.text[:60]))

            # ---- import: same number at several places is fine ---------
            dup_pos = tempfile.mktemp(suffix='.json')
            json.dump({'farms': [
                {'n': 5, 'x': 111, 'y': 222}, {'n': 5, 'x': 111, 'y': 222}]},
                open(dup_pos, 'w', encoding='utf-8'))
            page.set_input_files('#importfile', dup_pos)
            time.sleep(0.5)
            check('the import refuses one position twice',
                  'twice at' in page.inner_text('#status'))
            multi = tempfile.mktemp(suffix='.json')
            json.dump({'farms': [
                {'n': 5, 'x': 111, 'y': 222}, {'n': 5, 'x': 333, 'y': 444}]},
                open(multi, 'w', encoding='utf-8'))
            page.set_input_files('#importfile', multi)
            page.wait_for_function(
                "document.getElementById('status').textContent.includes('Imported')",
                timeout=10000)
            check('the import takes the same number at several places',
                  page.locator('[data-farm="5"]').count() == 2,
                  page.inner_text('#status')[:80])

            # ---- the import into farms.yml carries both ----------------
            page.evaluate("""() => {
              farms_list = null;
              const out = marksList.map(m => ({ n: m.n, x: m.x, y: m.y }))
                .sort((a, b) => a.n - b.n || a.x - b.x || a.y - b.y);
              window.__exp = out;
            }""")
            exp = page.evaluate("() => window.__exp")
            tmp = tempfile.mktemp(suffix='.json')
            reds_now = json.load(open(REDS, encoding='utf-8')) \
                if os.path.isfile(REDS) else []
            if isinstance(reds_now, dict):
                reds_now = reds_now.get('marks', [])
            json.dump({'farms': exp, 'reds': reds_now},
                      open(tmp, 'w', encoding='utf-8'))
            import subprocess
            p = subprocess.run([sys.executable,
                                'pipeline/maps/import_farms.py', tmp],
                               capture_output=True, text=True,
                               encoding='utf-8', errors='replace')
            import yaml
            fy = yaml.safe_load(open('maps/pelzucki1896/farms.yml',
                                     encoding='utf-8'))
            y5 = [m for m in fy['marks'] if m['n'] == 5]
            check('the import into farms.yml keeps multiple marks per farm',
                  p.returncode == 0 and len(fy['marks']) == len(exp)
                  and len(y5) == 2,
                  'farm 5: %d of %d total' % (len(y5), len(fy['marks'])))
            os.remove(tmp); os.remove(dup_pos); os.remove(multi)

            check('no page errors', not errors, '; '.join(errors[:2]))
            browser.close()
    finally:
        for p, b in backups.items():
            shutil.copy(b, p)
        for p in (FARMS, REDS):
            if os.path.isfile(p) and p not in backups:
                os.remove(p)
        shutil.copy(yml_bak, 'maps/pelzucki1896/farms.yml')
        print('working files, farms.yml restored / cleaned')
    failed = [n for n, ok in RESULTS if not ok]
    print(f'{len(RESULTS) - len(failed)}/{len(RESULTS)} passed'
          + ('' if not failed else ' — FAILED: ' + ', '.join(failed)))
    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
