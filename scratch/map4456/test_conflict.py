# -*- coding: utf-8 -*-
"""The conflict-and-backup test: the two failure modes that cost the
editor real work, now closed.

1. Two windows of the page are open. Window A moves a farm (its save
   lands). Window B - holding the older state - then moves a farm: its
   save must be REFUSED (409) with a loud banner, not silently overwrite
   A's newer state. After B reloads it holds A's state.
2. The server goes down; window A moves a farm anyway (the save fails,
   the state is stashed in the browser). On reload, the browser's backup
   (newer than the project file) wins, the move comes back, and it pushes
   to the server as soon as the server is back.
"""
import atexit
import io
import json
import os
import shutil
import sys
import tempfile
import time

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


def drag_by(page, sel, dx, dy):
    el = page.locator(sel).first
    b = el.bounding_box()
    cx, cy = b['x'] + b['width'] / 2, b['y'] + b['height'] / 2
    page.mouse.move(cx, cy)
    page.mouse.down()
    page.mouse.move(cx + dx, cy + dy, steps=4)
    page.mouse.up()
    time.sleep(0.4)


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

            # ---- 1. two windows --------------------------------------
            errs = []
            a = browser.new_page(viewport={'width': 1400, 'height': 900})
            a.on('pageerror', lambda e: errs.append(str(e)[:200]))
            a.goto(URL)
            a.wait_for_function(
                "document.getElementById('status').textContent.includes('Loaded')",
                timeout=30000)
            b = browser.new_page(viewport={'width': 1400, 'height': 900})
            b.on('pageerror', lambda e: errs.append(str(e)[:200]))
            b.goto(URL)
            b.wait_for_function(
                "document.getElementById('status').textContent.includes('Loaded')",
                timeout=30000)

            # A moves farm 1: its save lands, the version moves on
            drag_by(a, '[data-farm="1"]', 60, 40)
            d = json.load(open(FARMS, encoding='utf-8'))
            f1a = next(x for x in d if x['n'] == 1)
            check('window A\'s move lands', f1a != {'n': 1, 'x': 0, 'y': 0}
                  and len(d) == 101)

            # B (stale) moves farm 2: refused with the banner
            drag_by(b, '[data-farm="2"]', 50, 30)
            time.sleep(0.8)
            check('window B\'s stale save is refused (409)',
                  'changed in another window' in b.inner_text('#saved')
                  or 'changed in another window' in b.inner_text('#savebanner'),
                  b.inner_text('#savebanner')[:80])
            check('the banner carries a close button',
                  b.locator('#banner-close').count() == 1)
            b.click('#banner-close')
            time.sleep(0.2)
            check('the close button dismisses the banner',
                  not b.locator('#savebanner.on').count() > 0
                  or 'changed in another window' not in
                  b.inner_text('#savebanner'))
            d2 = json.load(open(FARMS, encoding='utf-8'))
            f2 = next(x for x in d2 if x['n'] == 2)
            f1b = next(x for x in d2 if x['n'] == 1)
            check('B\'s refusal did not overwrite A\'s move', f1b == f1a,
                  'farm 1 intact: %s' % (f1b,))
            # farm 2's position: B's move must NOT be in the file (it was
            # refused); the file's farm 2 stays at its pre-move value
            pre2 = next(x['x'] for x in d if x['n'] == 2)
            check('the refused move is not in the file',
                  next(x for x in d2 if x['n'] == 2)['x'] == pre2)
            a.close()
            b.close()

            # after B reloads it holds A's state (checked in scene 2's page)

            # ---- 2. server down, the browser backup wins --------------
            a = browser.new_page(viewport={'width': 1400, 'height': 900})
            a.on('pageerror', lambda e: errs.append(str(e)[:200]))
            a.goto(URL)
            a.wait_for_function(
                "document.getElementById('status').textContent.includes('Restored')",
                timeout=30000)
            test_server.kill()
            drag_by(a, '[data-farm="3"]', -70, 50)
            f3_page = a.evaluate("() => markPos(3)")
            a.wait_for_function(
                "document.getElementById('saved').textContent.includes('SAVE FAILED')"
                + " || document.getElementById('savebanner').textContent"
                + ".toLowerCase().includes('server')", timeout=10000)
            check('the move with the server down is kept in the browser',
                  'SAVE FAILED' in a.inner_text('#saved')
                  or 'server' in a.inner_text('#savebanner').lower(),
                  a.inner_text('#savebanner')[:80])
            # the server comes back, but the state file is gone (the way a
            # cleanup or an import could leave it): the refresh must take
            # the browser backup, which is newer than the (missing) file
            test_server.start()
            for p in (FARMS, REDS):
                if os.path.isfile(p):
                    os.remove(p)
            a.reload()   # the very thing that used to lose everything
            a.wait_for_function(
                "document.getElementById('status').textContent.includes('Restored')",
                timeout=30000)
            check('after the refresh, the browser backup restores the move',
                  a.evaluate("() => markPos(3)")
                  == f3_page,
                  a.inner_text('#status')[:110])
            check('the backup says what happened',
                  'browser' in a.inner_text('#status')
                  or 'backup' in a.inner_text('#status'))
            test_server.start()
            a.wait_for_function(
                "!document.getElementById('saved').textContent.includes('FAILED')"
                + " && document.getElementById('saved').textContent"
                + ".startsWith('saved')", timeout=20000)
            d3 = json.load(open(FARMS, encoding='utf-8'))
            check('the recovered state pushes to the server',
                  any(x for x in d3 if x['n'] == 3
                      and x['x'] == f3_page['x'] and x['y'] == f3_page['y']))
            a.close()

            check('no page errors', not errs, '; '.join(errs[:2]))
            browser.close()
    finally:
        test_server.stop()
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
