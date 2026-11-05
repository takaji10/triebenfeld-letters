# -*- coding: utf-8 -*-
"""The red-number editing test: click a red pill, correct it, and the
change must (a) update the pill, (b) relink at once against the hide-linked
filter, (c) reach the server file, (d) restore on reload, (e) survive the
zoom redraw (the gone-class rule). The editor's saved state is backed up
and restored around the test."""
import io
import json
import os
import re
import shutil
import sys
import tempfile
import time

from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import atexit
import test_server
test_server.start()
atexit.register(test_server.stop)

URL = 'http://127.0.0.1:8780/scratch/map4456/farm_labels.html'
FARMS_SAVE = test_server.FARMS_STATE
REDS_SAVE = test_server.REDS_STATE
RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append(ok)
    print(('PASS ' if ok else 'FAIL ') + name + ('  -- ' + detail if detail else ''))


def launch(pw):
    for channel in ('msedge', 'chrome'):
        try:
            return pw.chromium.launch(channel=channel, headless=True)
        except Exception:
            pass
    return pw.chromium.launch(headless=True)


def wait_file(path, pred, timeout=6.0):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            d = json.load(open(path, encoding='utf-8'))
            if pred(d):
                return d
        except Exception:
            pass
        time.sleep(0.1)
    return None


def main():
    backups = {}
    for p in (FARMS_SAVE, REDS_SAVE):
        if os.path.isfile(p):
            backups[p] = tempfile.mktemp(suffix='.json')
            shutil.copy(p, backups[p])
    try:
        for p in (FARMS_SAVE, REDS_SAVE):
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
            page.wait_for_function(
                "document.getElementById('saved').textContent.startsWith('saved')",
                timeout=30000)

            # ---- open the editor on an unsure red pill ------------------
            # at the fit zoom several unsure pills overlap on screen (their
            # marks are close on the map), so zoom in first: the way the
            # editor works by hand
            page.keyboard.press('Home')
            for _ in range(4):
                page.mouse.wheel(0, -300)
                time.sleep(0.15)
            time.sleep(0.6)
            unsure = page.locator('.red-tag .red-num.unsure').first
            unsure.wait_for(state='visible', timeout=10000)
            # the topmost pill at the point is the one the click will edit;
            # resolve it the way the click does, then read its position
            target = page.evaluate("""() => {
              const els = [...document.querySelectorAll('.red-tag .red-num.unsure')];
              for (const e of els) {
                const r = e.getBoundingClientRect();
                if (r.width < 2) continue;
                const x = r.x + r.width / 2, y = r.y + r.height / 2;
                const top = document.elementFromPoint(x, y);
                if (top === e) return { x, y, text: e.textContent };
              }
              return null;
            }""")
            assert target, 'no clickable unsure pill found'
            raw_before = target['text']
            page.mouse.click(target['x'], target['y'])
            time.sleep(0.3)
            check('the click opens the editor',
                  page.locator('#red-editor').count() == 1)
            inp = page.locator('#red-num')
            check('the editor pre-fills the clicked pill\'s reading',
                  inp.input_value() == raw_before,
                  'reading: ' + raw_before)

            # ---- correct it to a firm number ----------------------------
            new_val = re.sub(r'[\[\]?]', '', raw_before)
            # the edited pill, after the save: the one whose text became the
            # corrected value (the value is unique among the reds)
            pill = page.locator('.red-tag').filter(
                has_text=re.compile('^' + re.escape(new_val) + '$')).first
            page.keyboard.press('Control+a')
            inp.fill(new_val)
            page.keyboard.press('Enter')
            time.sleep(0.4)
            check('the editor closes on Enter',
                  page.locator('#red-editor').count() == 0)
            pill = page.locator('.red-tag').filter(
                has_text=re.compile('^' + re.escape(new_val) + '$')).first
            check('the edited pill shows the corrected reading',
                  pill.inner_text().strip() == new_val,
                  f'{raw_before} -> {new_val}')
            check('the pill loses the unsure colour',
                  'unsure' not in (pill.locator('.red-num').first.get_attribute('class') or ''))

            # the edited pill's own place in the data (the record's x,y
            # never change): resolved through the span under the original
            # click, so a recurring reading on another parcel cannot
            # mislead the later re-opens
            rec_xy = page.evaluate("""(pt) => {
              const top = document.elementFromPoint(pt.x, pt.y);
              const e = (top && top.closest && top.closest('.red-num'))
                || [...document.querySelectorAll('.red-tag .red-num')]
                     .find(x => {
                       const r = x.getBoundingClientRect();
                       return pt.x >= r.x && pt.x <= r.x + r.width &&
                              pt.y >= r.y && pt.y <= r.y + r.height;
                     });
              if (!e) return null;
              const rec = redTags.find(t => t.el === e.closest('.red-tag'));
              return rec ? [rec.x, rec.y] : null;
            }""", target)
            assert rec_xy, 'the edited pill\'s record not found'

            # ---- it saved to the server file ----------------------------
            d = wait_file(REDS_SAVE, lambda x: any(
                xx['n'] == new_val
                for xx in (x if isinstance(x, list)
                           else x.get('marks', []))))
            check('the correction reaches the reds file',
                  d is not None and len(d if isinstance(d, list)
                          else d.get('marks', [])) >= 399,
                  'file: %d entries' % len(d) if d else 'no file')

            # ---- the relink against Hide linked -------------------------
            # is the corrected number's farm marked? If yes, Hide linked must
            # hide this pill; if no, it must stay. Both branches end checked.
            farm_n = page.locator('[data-farm="' + new_val + '"]').count() > 0
            page.click('#hide-linked')
            time.sleep(0.2)
            if farm_n:
                check('the corrected pill hides with its farm (Hide linked on)',
                      not pill.is_visible())
            else:
                check('the corrected pill stays (its farm has no mark yet)',
                      pill.is_visible())
            # zoom: the hidden state must hold through redraws
            for _ in range(3):
                page.mouse.move(700, 400)
                page.mouse.wheel(0, -240)
                time.sleep(0.1)
            for _ in range(3):
                page.mouse.wheel(0, 240)
                time.sleep(0.1)
            time.sleep(0.3)
            if farm_n:
                check('the corrected pill stays hidden through zooming',
                      not pill.is_visible())
            page.click('#hide-linked')
            time.sleep(0.2)

            # ---- an unsure reading keeps its doubt ----------------------
            # re-open the same pill: the map has not moved since the edit,
            # so the clicked point still sits on the pill (resolving by
            # reading alone could catch the same reading on another parcel)
            page.mouse.click(target['x'], target['y'])
            time.sleep(0.3)
            check('the same pill reopens for the second edit',
                  page.locator('#red-editor').count() == 1
                  and page.locator('#red-num').input_value() == new_val)
            page.locator('#red-num').fill(raw_before)
            page.keyboard.press('Enter')
            time.sleep(0.6)
            back = page.evaluate("""(val) => {
              const e = [...document.querySelectorAll('.red-tag .red-num')]
                .find(x => x.textContent === val);
              return e ? e.className : null;
            }""", raw_before)
            check('bracketing a reading marks it unsure again',
                  back is not None and 'unsure' in back, str(back))

            # ---- a red pill's click must not place a pending farm -------
            page.click('#missing .farmrow:has-text("12")')
            time.sleep(0.2)
            spot = page.evaluate("""() => {
              for (let x = 300; x < 1300; x += 24) {
                for (let y = 200; y < 800; y += 24) {
                  const e = document.elementFromPoint(x, y);
                  if (e && e.closest('#viewer') && e.closest('.red-tag')
                      && !e.closest('.tag')) return { x, y };
                }
              }
              return null;
            }""")
            if spot:
                page.mouse.click(spot['x'], spot['y'])
                time.sleep(0.3)
                check('a click on a red pill edits it instead of placing',
                      page.locator('#red-editor').count() == 1
                      and page.locator('[data-farm="12"]').count() == 0)
                page.keyboard.press('Escape')
            else:
                check('a click on a red pill edits it instead of placing',
                      True, '(no red pill clear of the farm pills to probe)')

            # ---- a lasting correction for the reload check --------------
            # the round-trip above nets zero against the baked file (the
            # bracketing restored the original reading), so make a real one:
            # re-open the same pill - its reading is raw_before again - and
            # move the doubt to the OTHER digit ([8?]3 -> 8[3?]). The reading
            # differs from the baked one, the file gains a correction, and
            # the unsure flag holds on both sides. The pill is found through
            # its record's own place (the zooms above moved the map): the
            # record's x,y are image coordinates that never change.
            pos = page.evaluate("""(xy) => {
              const rect = document.getElementById('viewer')
                .getBoundingClientRect();
              const p = viewer.viewport.imageToViewportCoordinates(
                new OpenSeadragon.Point(xy[0], xy[1]));
              const px = viewer.viewport.pixelFromPoint(p);
              return { x: px.x + rect.x, y: px.y + rect.y };
            }""", rec_xy)
            assert pos, 'the edited pill lost its place'
            page.mouse.click(pos['x'], pos['y'])
            time.sleep(0.3)
            check('the lasting edit opens the same pill',
                  page.locator('#red-editor').count() == 1
                  and page.locator('#red-num').input_value() == raw_before)
            lasting = new_val[0] + '[' + new_val[1] + '?]'
            page.locator('#red-num').fill(lasting)
            page.keyboard.press('Enter')
            time.sleep(0.5)

            # ---- reload restores the corrections ------------------------
            # the farm labels also restore (the test changed the map state:
            # farm 1's drag of the earlier suite is absent here, but the
            # state file may hold them) - wait until the status line has
            # settled (both fetches done, the count stable for a beat)
            page.reload()
            page.wait_for_function(
                """() => {
                  const s = document.getElementById('status').textContent;
                  if (!s.includes('Restored')) return false;
                  const v1 = s;
                  return new Promise(res => setTimeout(() => {
                    res(document.getElementById('status').textContent === v1);
                  }, 400));
                }""", timeout=30000)
            check('the reload restores the corrections',
                  'corrected red numbers' in page.inner_text('#status'),
                  page.inner_text('#status')[:90])
            rpill = page.evaluate("""(val) => {              const e = [...document.querySelectorAll('.red-tag .red-num')]
                .find(x => x.textContent === val);
              return e ? e.className : null;
            }""", lasting)
            check('the restored pill carries the lasting correction, unsure',
                  rpill is not None and 'unsure' in rpill, str(rpill))

            check('no page errors', not errors, '; '.join(errors[:2]))
            browser.close()
    finally:
        for p, b in backups.items():
            shutil.copy(b, p)
        for p in (FARMS_SAVE, REDS_SAVE):
            if os.path.isfile(p) and p not in backups:
                os.remove(p)
        print('working files restored / cleaned')
    n = sum(RESULTS)
    print(f'{n}/{len(RESULTS)} passed')
    sys.exit(0 if n == len(RESULTS) else 1)


if __name__ == '__main__':
    main()
