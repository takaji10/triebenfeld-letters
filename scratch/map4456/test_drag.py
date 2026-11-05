# -*- coding: utf-8 -*-
"""A real-browser interaction test for the farm-labels working page.

Drives http://127.0.0.1:8780/scratch/map4456/farm_labels.html in headless
Chromium (the system Edge, then Chrome, then a downloaded Chromium) and
tests, in order: the drag of an existing label (tracks the mouse 1:1, the
map does not pan), the three toggles, Hide linked (linked farms' pills AND
their red numbers go; an unmarked farm's red numbers stay), placing a new
farm from the panel, dragging that new label, and Delete.
"""
import io
import re
import sys
import time

from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import atexit
import test_server
test_server.start()
atexit.register(test_server.stop)

URL = 'http://127.0.0.1:8780/scratch/map4456/farm_labels.html'
RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append((name, ok))
    print(('PASS ' if ok else 'FAIL ') + name + ('  -- ' + detail if detail else ''))


def launch(pw):
    for channel in ('msedge', 'chrome'):
        try:
            return pw.chromium.launch(channel=channel, headless=True)
        except Exception as e:
            print(f'channel {channel}: {str(e)[:100]}')
    return pw.chromium.launch(headless=True)


def drag(page, box, dx, dy):
    cx = box['x'] + box['width'] / 2
    cy = box['y'] + box['height'] / 2
    page.mouse.move(cx, cy)
    page.mouse.down()
    for i in range(1, 7):
        page.mouse.move(cx + dx * i / 6, cy + dy * i / 6)
        time.sleep(0.03)
    page.mouse.up()
    time.sleep(0.3)


def main():
    with sync_playwright() as pw:
        browser = launch(pw)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)[:200]))
        page.goto(URL)
        page.wait_for_function(
            "const s = document.getElementById('status').textContent; s.includes('Loaded') || s.includes('Restored')",
            timeout=30000)
        # the autosave file of a previous run would change the starting
        # state: remove it and start from the baked 101
        page.evaluate("() => fetch('/__save/farm_labels', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '[]' })")
        page.reload()
        page.wait_for_function(
            "document.getElementById('status').textContent.includes('Loaded')",
            timeout=30000)

        # farm 78 is marked in the data now (the editor's import run put a
        # label on every farm whose red numbers were identified): remove
        # that one label, so the suite's new-farm flow has the unmarked
        # farm it tests
        row78 = page.locator('#marked .farmrow').filter(has_text='78').first
        row78.locator('.del').click()
        time.sleep(0.3)
        check('setup: farm 78 starts unmarked',
              page.locator('[data-farm="78"]').count() == 0)

        # ---- 1. drag an existing label ---------------------------------
        tag = page.locator('[data-farm="1"]').first
        tag.wait_for(state='visible', timeout=10000)
        b1 = tag.bounding_box()
        nbr = page.locator('[data-farm="2"]').first.bounding_box()
        drag(page, b1, 120, 64)
        a1 = tag.bounding_box()
        an = page.locator('[data-farm="2"]').first.bounding_box()
        dx = (a1['x'] + a1['width'] / 2) - (b1['x'] + b1['width'] / 2)
        dy = (a1['y'] + a1['height'] / 2) - (b1['y'] + b1['height'] / 2)
        check('drag tracks the mouse',
              abs(dx - 120) < 30 and abs(dy - 64) < 24,
              f'pill delta ({dx:.1f}, {dy:.1f})')
        check('the map does not pan under the drag',
              abs(an['x'] - nbr['x']) < 4 and abs(an['y'] - nbr['y']) < 4)
        check('status reports the move', 'moved to' in page.inner_text('#status'))

        # ---- 2. hide linked: linked pills and their reds go -------------
        page.click('#hide-linked')
        time.sleep(0.3)
        check('Hide linked hides a linked farm pill', not tag.is_visible())
        red78 = page.locator('.red-tag').filter(has_text=re.compile('^78$')).first
        check('an unmarked farm\'s red numbers stay', red78.is_visible())
        linked_red = page.locator('.red-tag').filter(has_text=re.compile('^1$')).first
        check('a linked farm\'s red numbers go',
              linked_red.count() == 0 or not linked_red.is_visible())
        page.click('#hide-linked')
        time.sleep(0.3)
        check('Hide linked off restores everything', tag.is_visible())

        # ---- 3. the toggles ---------------------------------------------
        page.click('#reds-toggle')
        time.sleep(0.2)
        check('Red numbers off hides the red tags', not red78.is_visible())
        page.click('#reds-toggle')
        page.click('#names-toggle')
        time.sleep(0.2)
        check('Farm names off hides the pills', not tag.is_visible())
        check('Farm names off keeps the red tags', red78.is_visible())
        page.click('#names-toggle')
        time.sleep(0.2)

        # ---- 4. place a new farm (78), drag it, delete it ----------------
        row = page.locator('#missing .farmrow').filter(has_text='78').first
        row.click()
        time.sleep(0.2)
        # a click on a red pill opens its editor now (the reds are
        # clickable), so place at a spot clear of every pill - probed the
        # way the page's own hit testing works
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
        time.sleep(0.3)
        new_tag = page.locator('[data-farm="78"]').first
        check('placing farm 78 makes its pill',
              new_tag.count() == 1 and new_tag.is_visible(),
              page.inner_text('#status')[:60])
        b78 = new_tag.bounding_box()
        drag(page, b78, -90, 50)
        a78 = new_tag.bounding_box()
        dx = (a78['x'] + a78['width'] / 2) - (b78['x'] + b78['width'] / 2)
        dy = (a78['y'] + a78['height'] / 2) - (b78['y'] + b78['height'] / 2)
        check('the new label drags too', abs(dx + 90) < 30 and abs(dy - 50) < 24,
              f'pill delta ({dx:.1f}, {dy:.1f})')
        # the pill is already selected from its placement (class "sel"), and
        # a click here can be intercepted by the panel when the dragged pill
        # sits under it - Delete works on the selection directly
        page.keyboard.press('Delete')
        time.sleep(0.3)
        check('Delete removes the label', page.locator('[data-farm="78"]').count() == 0)

        check('no page errors', not errors, '; '.join(errors[:2]))
        browser.close()

    failed = [n for n, ok in RESULTS if not ok]
    print()
    print(f'{len(RESULTS) - len(failed)}/{len(RESULTS)} passed'
          + ('' if not failed else ' — FAILED: ' + ', '.join(failed)))
    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
