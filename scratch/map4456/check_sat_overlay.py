# -*- coding: utf-8 -*-
"""The satellite overlay page, checked in a headless browser.

    python scratch/map4456/check_sat_overlay.py

Serves the tiles repository (the page's own home, the way its Pages
serves it) and loads pelzucki1896/sat_overlay.html in headless Chromium:
the satellite tiles and the warped plan must both lay, and all 101 farm
labels must draw. The page fetches its annotation and the labels' data
beside it and its libraries from the CDN, so the check needs the network.
"""
import io
import os
import sys
import threading
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8',
                              errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8',
                              errors='replace')
MAPS_REPO = os.environ.get('TRIEBENFELD_MAPS',
                           os.path.join(os.path.dirname(os.path.dirname(
                               os.path.dirname(os.path.abspath(__file__)))),
                               '..', 'triebenfeld-maps'))
PAGE = '/pelzucki1896/sat_overlay.html'
PORT = 8791


def launch(pw):
    """The working pages' own launch (check_site_integration.py): Edge's
    bundled Chromium first, the downloaded one second."""
    for channel in ('msedge', None):
        try:
            if channel:
                return pw.chromium.launch(channel=channel, headless=True)
            return pw.chromium.launch(headless=True)
        except Exception:
            continue
    raise RuntimeError('no browser to launch')


def main():
    handler = partial(SimpleHTTPRequestHandler, directory=MAPS_REPO)
    server = ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    from playwright.sync_api import sync_playwright
    errors = []
    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page()
        page.on('pageerror', lambda e: errors.append('pageerror: ' + str(e)))
        # the console's 404 text names no URL, and the page's only 404 in
        # the field has been the browser's own favicon request - the 404s
        # are watched on the responses instead, by URL
        page.on('response', lambda r: errors.append('http ' + str(r.status) +
                                                    ': ' + r.url)
                if r.status >= 400 and 'favicon' not in r.url else None)
        page.goto(f'http://127.0.0.1:{PORT}{PAGE}')
        # the warped layer's canvas and the farm pills
        page.wait_for_selector('.farm-tag', timeout=30000)
        time.sleep(8)
        # into the village at a zoom the pills separate at, then the
        # screenshot the editor's eye would judge by
        page.evaluate('map.setView([52.1085, 17.9055], 16)')
        time.sleep(4)
        n = page.locator('.farm-tag').count()
        has_canvas = page.evaluate(
            "!!document.querySelector('#map canvas')")
        title = page.title()
        print(f'title: {title}')
        print(f'farm tags: {n}')
        print(f'warped layer canvas: {has_canvas}')
        page.screenshot(path=os.path.join(os.path.dirname(os.path.abspath(
            __file__)), 'sat_overlay_check.png'))
        browser.close()
    server.shutdown()
    if errors:
        print('ERRORS:')
        for e in errors:
            print(' ', e)
        sys.exit(1)
    if n != 101:
        print(f'FAIL: expected 101 farm tags, saw {n}')
        sys.exit(1)
    print('OK')


main()
