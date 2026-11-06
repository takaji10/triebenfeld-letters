# -*- coding: utf-8 -*-
"""The zoom-survival test: with Hide linked pressed, zooming and panning
must not bring the linked labels back (the OSD redraw sets inline
display=block every frame; the fix hides by a !important class instead).
Runs the working page and the built site page."""
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

WORK = 'http://127.0.0.1:8780/scratch/map4456/farm_labels.html'
SITE = None   # set in main(): a server rooted at site/_site
SAVE = test_server.FARMS_STATE
RESULTS = []


def start_site_server(port=8781):
    """The built site's own server: site/_site as the document root, so the
    pages' site-root-absolute URLs (/assets/...) resolve as they do live."""
    import functools
    import threading
    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
    handler = functools.partial(SimpleHTTPRequestHandler,
                                directory=os.path.abspath('site/_site'))
    httpd = ThreadingHTTPServer(('127.0.0.1', port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return 'http://127.0.0.1:%d' % port


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


def poke_and_zoom(page):
    """Zoom in and out hard, several rounds, panning between."""
    for _ in range(4):
        page.keyboard.press('Home')
        time.sleep(0.15)
        page.mouse.move(700, 400)
        for _ in range(3):
            page.mouse.wheel(0, -240)   # zoom in
            time.sleep(0.12)
        page.mouse.move(760, 460)
        page.mouse.wheel(0, 120)
        time.sleep(0.2)
        for _ in range(4):
            page.mouse.wheel(0, 240)   # zoom back out
            time.sleep(0.1)
        time.sleep(0.4)


def main():
    had = os.path.isfile(SAVE)
    bak = tempfile.mktemp(suffix='.json')
    if had:
        shutil.copy(SAVE, bak)
    try:
        if os.path.isfile(SAVE):
            os.remove(SAVE)
        with sync_playwright() as pw:
            browser = launch(pw)
            page = browser.new_page(viewport={'width': 1400, 'height': 900})
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)[:160]))

            # ---- the working page --------------------------------------
            page.goto(WORK)
            page.wait_for_function(
                "document.getElementById('status').textContent.includes('Loaded')",
                timeout=30000)
            page.wait_for_function(
                "document.getElementById('saved').textContent.startsWith('saved')",
                timeout=30000)
            # farm 78 is marked in the data now (the editor's import run):
            # remove its label, so the suite keeps an unmarked farm whose
            # red numbers must survive Hide linked
            row78 = page.locator('#marked .farmrow').filter(has_text='78').first
            row78.locator('.del').click()
            time.sleep(0.3)
            tag1 = page.locator('[data-farm="1"]').first
            red1 = page.locator('.red-tag').filter(has_text=re.compile(r'^1$')).first
            check('work: farm pill visible before hiding', tag1.is_visible())
            page.click('#hide-linked')
            time.sleep(0.2)
            check('work: Hide linked hides the linked pill', not tag1.is_visible())
            check('work: Hide linked hides the linked red numbers',
                  red1.count() == 0 or not red1.is_visible())
            poke_and_zoom(page)
            check('work: the pill stays hidden through zooming/panning',
                  not tag1.is_visible())
            check('work: the red numbers stay hidden through zooming/panning',
                  red1.count() == 0 or not red1.is_visible())
            red78 = page.locator('.red-tag').filter(has_text=re.compile(r'^78$')).first
            check('work: the unmarked farm\'s red numbers still show',
                  red78.is_visible())
            unsure_linked = page.evaluate("""() => {
              const t = redTags.find(t => t.unsure && isLinked(t.num));
              return t ? { raw: String(t.raw),
                           gone: t.el.classList.contains('gone') } : null;
            }""")
            check('work: an unsure reading is never hidden, even when its '
                  'number is a linked farm',
                  unsure_linked is not None and not unsure_linked['gone'],
                  str(unsure_linked))
            page.click('#hide-linked')
            time.sleep(0.2)
            check('work: Hide linked off brings them back', tag1.is_visible())
            poke_and_zoom(page)
            check('work: the restored pill survives zooming too', tag1.is_visible())

            # ---- the site page -----------------------------------------
            site_root = start_site_server()
            page.goto(site_root + '/maps/pelzucki1896/')
            page.wait_for_selector('.farm-tag', state='attached', timeout=30000)
            ft = page.locator('.farm-tag[data-farm="1"]').first
            # the names layer is ON by default now; Hide linked is gone
            # (the editor, 2026-11-06)
            check('site: no hide-linked button on the page',
                  page.locator('#reds-linked').count() == 0)
            check('site: the farm pill shows with its layer on', ft.is_visible())
            page.click('#reds-layer')
            time.sleep(0.3)
            sred1 = page.locator('.red-tag').filter(has_text=re.compile(r'^1$')).first
            check('site: the red numbers show with their layer on',
                  sred1.count() == 0 or sred1.is_visible())
            poke_and_zoom(page)
            check('site: the pill survives zooming/panning', ft.is_visible())
            check('site: the red numbers survive zooming',
                  sred1.count() == 0 or sred1.is_visible())
            page.click('#farm-layer')
            time.sleep(0.3)
            check('site: the names layer toggles off', not ft.is_visible())
            page.click('#farm-layer')
            time.sleep(0.3)
            check('site: the names layer toggles back on', ft.is_visible())
            check('no page errors', not errors, '; '.join(errors[:2]))
            browser.close()
    finally:
        if had:
            shutil.copy(bak, SAVE)
        elif os.path.isfile(SAVE):
            os.remove(SAVE)
    print(f'{sum(RESULTS)}/{len(RESULTS)} passed')
    sys.exit(0 if all(RESULTS) else 1)


if __name__ == '__main__':
    main()
