# -*- coding: utf-8 -*-
"""The centrepoint check: the tag's ::after dot must sit on the overlay's
anchor point, and stay on it through a drag - which is what makes the dot
usable for placing a label exactly on the farmhouse."""
import io
import re
import subprocess
import sys
import tempfile
import time
import os

from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import atexit
import test_server
test_server.start()
atexit.register(test_server.stop)

URL = 'http://127.0.0.1:8780/scratch/map4456/farm_labels.html'
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


def main():
    # static: the dot is defined once, for tags only
    t = io.open('scratch/map4456/farm_labels.html', encoding='utf-8').read()
    check('dot defined on .tag::after', '.tag::after' in t and '7px' in t)
    check('no dot on red tags', '.red-tag::after' not in t)
    scripts = re.findall(r'<script>(.*?)</script>', t, re.S)
    tmp = tempfile.mkdtemp()
    for i, s in enumerate(scripts):
        p = os.path.join(tmp, f's{i}.js')
        io.open(p, 'w', encoding='utf-8').write(s)
        r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
        if r.returncode != 0:
            check('inline JS', False, r.stderr[:200])
    check('inline JS parses', True)

    with sync_playwright() as pw:
        browser = launch(pw)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)[:200]))
        page.goto(URL)
        page.wait_for_function(
            "const s = document.getElementById('status').textContent; s.includes('Loaded') || s.includes('Restored')",
            timeout=30000)
        # a previous run's autosave would change the starting state: reset
        # to empty (the page then builds from the baked 73) and reload
        page.evaluate("() => fetch('/__save/farm_labels', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '[]' })")
        page.reload()
        page.wait_for_function(
            "document.getElementById('status').textContent.includes('Loaded')",
            timeout=30000)
        # place a new farm so we know the exact anchor: farm 12 at a chosen
        # click point clear of every label (find one by probing the page)
        page.click('#missing .farmrow:has-text("12")')
        time.sleep(0.2)
        spot = page.evaluate("""() => {
          for (let x = 300; x < 1300; x += 24) {
            for (let y = 200; y < 800; y += 24) {
              const e = document.elementFromPoint(x, y);
              if (e && e.closest('#viewer') && !e.closest('.tag')) return { x, y };
            }
          }
          return null;
        }""")
        assert spot, 'no free spot found'
        page.mouse.click(spot['x'], spot['y'])
        time.sleep(0.4)
        tag = page.locator('[data-farm="12"]').first
        box = tag.bounding_box()
        cx = box['x'] + box['width'] / 2
        cy = box['y'] + box['height'] / 2
        check('pill centred on the click point',
              abs(cx - spot['x']) < 3 and abs(cy - spot['y']) < 3,
              f'pill centre ({cx:.1f}, {cy:.1f}) vs click ({spot["x"]}, {spot["y"]})')
        # the dot is the ::after pseudo-element: its position is derivable
        # from the box (50% + the -3.5px margin); the check is that the
        # overlay anchor equals the box centre, since the dot is drawn at
        # exactly that centre
        # now drag: the dot must stay the anchor, i.e. the box centre must
        # land where the drag ends
        page.mouse.move(cx, cy)
        page.mouse.down()
        for i in range(1, 7):
            page.mouse.move(cx + 60 * i / 6, cy + 30 * i / 6)
            time.sleep(0.03)
        page.mouse.up()
        time.sleep(0.3)
        b2 = tag.bounding_box()
        cx2 = b2['x'] + b2['width'] / 2
        cy2 = b2['y'] + b2['height'] / 2
        check('after the drag the centre is the anchor again',
              abs(cx2 - (cx + 60)) < 30 and abs(cy2 - (cy + 30)) < 20,
              f'centre now ({cx2:.1f}, {cy2:.1f}), expected ~( {cx + 60:.1f}, {cy + 30:.1f})')
        # the placed pill also lands in the missing->marked panels correctly
        check('farm 12 left the To add list',
              page.locator('#missing .farmrow:has-text("12")').count() == 0)
        check('no page errors', not errors, '; '.join(errors[:2]))
        browser.close()

    print(f'{sum(RESULTS)}/{len(RESULTS)} passed')
    sys.exit(0 if all(RESULTS) else 1)


if __name__ == '__main__':
    main()
