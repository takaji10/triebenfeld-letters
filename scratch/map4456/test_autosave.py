# -*- coding: utf-8 -*-
"""The autosave test: move, place, delete - each must reach
scratch/map4456/farm_labels_latest.json at once, and a reload must restore
the state. The editor's real saved state is backed up first and restored
after, so the test never touches it."""
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
SAVE = test_server.FARMS_STATE
RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append(ok)
    print(('PASS ' if ok else 'FAIL ') + name + ('  -- ' + detail if detail else ''))


def wait_saved(page, count, timeout=6.0):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            if os.path.isfile(SAVE):
                d = json.load(open(SAVE, encoding='utf-8'))
                if len(d) == count:
                    return d
        except Exception:
            pass
        time.sleep(0.1)
    return None


def launch(pw):
    for channel in ('msedge', 'chrome'):
        try:
            return pw.chromium.launch(channel=channel, headless=True)
        except Exception:
            pass
    return pw.chromium.launch(headless=True)


def main():
    had_state = os.path.isfile(SAVE)
    backup = tempfile.mktemp(suffix='.json')
    if had_state:
        shutil.copy(SAVE, backup)
        print('backed up the editor\'s saved state (%d labels)' %
              len(json.load(open(SAVE, encoding='utf-8'))))
    try:
        # the test starts from the build's baked state, never from a file a
        # previous run (or the test's own probe) left behind
        if os.path.isfile(SAVE):
            os.remove(SAVE)
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
            # the load itself no longer POSTs (a load-time save is what let
            # two windows erase each other): the state file appears with
            # the first real change, so make one - a nudge of farm 1 -
            # before reading the file
            tag0 = page.locator('[data-farm="1"]').first
            tag0.wait_for(state='visible', timeout=10000)
            b0 = tag0.bounding_box()
            page.mouse.move(b0['x'] + b0['width'] / 2,
                            b0['y'] + b0['height'] / 2)
            page.mouse.down()
            page.mouse.move(b0['x'] + b0['width'] / 2 + 3,
                            b0['y'] + b0['height'] / 2, steps=2)
            page.mouse.up()
            t0 = time.time()
            while not os.path.isfile(SAVE) and time.time() - t0 < 10:
                time.sleep(0.2)
            base = json.load(open(SAVE, encoding='utf-8'))
            print('initial state:', len(base), 'labels')
            assert len(base) == 101, 'expected the baked 101 at start'

            # ---- a move saves at once ---------------------------------
            before = json.load(open(SAVE, encoding='utf-8'))
            old1 = next(x for x in before if x['n'] == 1)
            tag = page.locator('[data-farm="1"]').first
            tag.wait_for(state='visible', timeout=10000)
            b = tag.bounding_box()
            cx, cy = b['x'] + b['width'] / 2, b['y'] + b['height'] / 2
            page.mouse.move(cx, cy)
            page.mouse.down()
            for i in range(1, 7):
                page.mouse.move(cx + 40 * i / 6, cy + 24 * i / 6)
                time.sleep(0.03)
            page.mouse.up()
            d = None
            t0 = time.time()
            while time.time() - t0 < 6:
                cur = json.load(open(SAVE, encoding='utf-8'))
                m1 = next((x for x in cur if x['n'] == 1), None)
                if m1 and (m1['x'], m1['y']) != (old1['x'], old1['y']):
                    d = cur
                    break
                time.sleep(0.1)
            check('a move saves at once', d is not None,
                  'farm 1 %s -> %s' % ((old1['x'], old1['y']),
                                       (m1['x'], m1['y']) if m1 else None))

            # ---- a placement saves at once ----------------------------
            spot = page.evaluate("""() => {
              for (let x = 300; x < 1300; x += 24) {
                for (let y = 200; y < 800; y += 24) {
                  const e = document.elementFromPoint(x, y);
                  if (e && e.closest('#viewer') && !e.closest('.tag')) return { x, y };
                }
              }
              return null;
            }""")
            page.click('#missing .farmrow:has-text("12")')
            time.sleep(0.2)
            page.mouse.click(spot['x'], spot['y'])
            time.sleep(0.3)
            d = wait_saved(page, len(base) + 1)
            check('a placement saves at once',
                  d is not None and any(x['n'] == 12 for x in (d or [])))

            # ---- a reload restores the state --------------------------
            page.reload()
            page.wait_for_function(
                "document.getElementById('saved').textContent.startsWith('saved')",
                timeout=30000)
            check('the reload restores the saved state',
                  page.locator('[data-farm="12"]').count() == 1 and
                  page.locator('.tag').count() == len(base) + 1,
                  page.inner_text('#status')[:60])

            # ---- a deletion saves at once -----------------------------
            page.locator('[data-farm="12"]').first.click()
            time.sleep(0.2)
            page.keyboard.press('Delete')
            time.sleep(0.3)
            d = wait_saved(page, len(base))
            check('a deletion saves at once',
                  d is not None and not any(x['n'] == 12 for x in (d or [])))

            # ---- the saved file is import-shaped ----------------------
            check('the saved file is the import\'s shape',
                  all(set(x) == {'n', 'x', 'y'} for x in d))
            check('no page errors', not errors, '; '.join(errors[:2]))
            browser.close()
    finally:
        if had_state:
            shutil.copy(backup, SAVE)
            print('editor\'s saved state restored (%d labels)' %
                  len(json.load(open(SAVE, encoding='utf-8'))))
        elif os.path.isfile(SAVE):
            os.remove(SAVE)
            print('no prior saved state; the test\'s file removed')
    failed = len(RESULTS) - sum(RESULTS)
    print(f'{sum(RESULTS)}/{len(RESULTS)} passed' + ('' if not failed else
          ' — %d FAILED' % failed))
    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
