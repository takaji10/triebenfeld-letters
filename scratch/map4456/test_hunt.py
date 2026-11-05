# -*- coding: utf-8 -*-
"""The hunt test: picking a farm in the "to add" list outlines its red
numbers blue on the map; deselecting or placing clears the outline, and a
placed farm's reds hide at once with Hide linked on."""
import io
import json
import os
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

            # farm 20 is marked in the data now (the editor's import run
            # put a label on every farm whose red numbers were identified):
            # remove that one label, so the suite has the unmarked farm
            # with red numbers it tests
            row20 = page.locator('#marked .farmrow').filter(has_text='20').first
            row20.locator('.del').click()
            time.sleep(0.3)

            # pick farm 20 from the to-add list (unmarked per the data)
            page.click('#missing .farmrow:has-text("20")')
            time.sleep(0.3)
            # how many red numbers read 20, per the page's own records?
            want = page.evaluate("() => redTags.filter(t => t.num === 20).length")
            got = page.evaluate(
                "() => document.querySelectorAll('.red-num.hunt').length")
            check('picking farm 20 outlines its red numbers blue',
                  want > 0 and got == want,
                  '%d outlined of %d reading 20' % (got, want))
            check('the outline is on the matching pills only',
                  page.evaluate("""() => {
                    const bad = [...document.querySelectorAll('.red-num.hunt')]
                      .filter(e => {
                        const pill = e.closest('.red-tag');
                        const rec = redTags.find(r => r.el === pill);
                        return !rec || rec.num !== 20;
                      });
                    return bad.length;
                  }""") == 0)
            check('the status names the hunt',
                  'outlined blue' in page.inner_text('#status'),
                  page.inner_text('#status')[:90])

            # deselect clears the outline (Esc cancels the pending pick)
            page.keyboard.press('Escape')
            time.sleep(0.2)
            check('Esc clears the blue outlines',
                  page.evaluate(
                      "() => document.querySelectorAll('.red-num.hunt').length")
                  == 0)

            # re-pick, then place: the outline clears and the farm links
            page.click('#missing .farmrow:has-text("20")')
            time.sleep(0.2)
            spot = page.evaluate("""() => {
              for (let x = 300; x < 1300; x += 24) {
                for (let y = 200; y < 800; y += 24) {
                  const e = document.elementFromPoint(x, y);
                  if (e && e.closest('#viewer') && !e.closest('.tag')
                      && !e.closest('.red-tag')) return { x, y };
                }
              }
              return null;
            }""")
            page.mouse.click(spot['x'], spot['y'])
            time.sleep(0.4)
            check('placing the farm clears the blue outlines',
                  page.evaluate(
                      "() => document.querySelectorAll('.red-num.hunt').length")
                  == 0)
            check('the placed farm has its pill',
                  page.locator('[data-farm="20"]').count() == 1)

            # the newly linked farm joins the hide-linked set at once
            red20 = page.evaluate(
                "() => redTags.filter(t => t.num === 20).length")
            page.click('#hide-linked')
            time.sleep(0.3)
            hidden = page.evaluate("""() => {
              let hidden = 0;
              redTags.forEach(t => {
                if (t.num === 20 && t.el.classList.contains('gone')) hidden++;
              });
              return hidden;
            }""")
            check('the newly linked farm\'s reds hide with Hide linked',
                  red20 > 0 and hidden == red20,
                  '%d of %d hidden' % (hidden, red20))
            check('its pill hides too',
                  not page.locator('[data-farm="20"]').first.is_visible())
            page.click('#hide-linked')
            time.sleep(0.2)

            # a farm with no red numbers hunts nothing, says so
            # (12 is unmarked; does any red read 12?)
            n12 = page.evaluate("() => redTags.filter(t => t.num === 12).length")
            page.click('#missing .farmrow:has-text("12")')
            time.sleep(0.3)
            st = page.inner_text('#status')
            if n12:
                check('a farm with reds hunts them (12)',
                      page.evaluate(
                          "() => document.querySelectorAll('.red-num.hunt').length")
                      == n12)
            else:
                check('a farm with no reds says so',
                      'No red number of it was found' in st, st[:80])
            page.keyboard.press('Escape')

            check('no page errors', not errors, '; '.join(errors[:2]))
            browser.close()
    finally:
        for p, b in backups.items():
            shutil.copy(b, p)
        for p in (FARMS, REDS):
            if os.path.isfile(p) and p not in backups:
                os.remove(p)
        print('working files restored / cleaned')
    failed = [n for n, ok in RESULTS if not ok]
    print(f'{len(RESULTS) - len(failed)}/{len(RESULTS)} passed'
          + ('' if not failed else ' — FAILED: ' + ', '.join(failed)))
    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
