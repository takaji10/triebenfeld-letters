# -*- coding: utf-8 -*-
"""Browser check of the built site: the Pełzucki 1896 map page (EN + DE)
and document 6's translation table with the proper names.

Serves site/_site statically, drives it in headless Edge, and checks:
  - the map page's layer buttons and their defaults (farm names ON,
    red numbers OFF; the farm-plots layer is GONE - the editor retired
    the drawn polygons, 2026-11-06)
  - the farm pills carry the proper spellings; institutions speak the
    page's language
  - red pills are grey; toggling them on works
  - the settlers' table has the Proper spelling column, conjectural rows
    marked with *
  - document 6: the translation view's table shows the proper names;
    diplomatic view keeps the Cyrillic
"""
import os
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SITE = os.path.abspath('site/_site')
PORT = 8791


def serve():
    os.chdir(SITE)
    srv = ThreadingHTTPServer(('127.0.0.1', PORT), SimpleHTTPRequestHandler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv


serve()
BASE = 'http://127.0.0.1:%d' % PORT
RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append((name, ok))
    print(('PASS ' if ok else 'FAIL ') + name + ('  -- ' + detail
                                                 if detail else ''))


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='msedge', headless=True)
        ctx = browser.new_context(viewport={'width': 1500, 'height': 950})

        # ---- the EN map page -------------------------------------------
        page = ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:200]))
        page.goto(BASE + '/maps/pelzucki1896/')
        page.wait_for_selector('.farm-tag', timeout=60000)
        time.sleep(2)

        def pressed(pid):
            return page.locator('#' + pid).get_attribute('aria-pressed')

        check('farm names layer is ON by default', pressed('farm-layer') == 'true')
        check('the farm-plots layer is gone (retired 2026-11-06)',
              page.locator('#plots-layer').count() == 0
              and page.evaluate(
                  "document.querySelectorAll('.map-plots-svg').length") == 0)
        check('red numbers layer is OFF by default',
              pressed('reds-layer') == 'false')
        n_pills = page.evaluate("document.querySelectorAll('.farm-tag').length")
        check('farm pills render (%d)' % n_pills, n_pills == 101)

        # proper spellings on the pills
        pill2 = page.locator('.farm-tag[data-farm="2"]').first
        check('farm 2’s pill carries the proper spelling',
              'Gibel' in (pill2.inner_text() or ''),
              (pill2.inner_text() or '')[:60])
        pill81 = page.locator('.farm-tag[data-farm="81"]').first
        check('farm 81’s pill reads Schönfisch',
              'Schönfisch' in (pill81.inner_text() or ''),
              (pill81.inner_text() or '')[:60])

        # red pills grey, off by default, come on with the toggle
        page.click('#reds-layer')
        time.sleep(1)
        n_reds = page.evaluate(
            "document.querySelectorAll('.red-tag:not(.gone)').length")
        check('red numbers come on with the toggle (%d showing)' % n_reds,
              n_reds > 300, '%d showing' % n_reds)
        bg = page.evaluate("""() => {
          const e = document.querySelector('.red-tag:not(.gone)');
          return e ? getComputedStyle(e).backgroundColor : null;
        }""")
        check('the red pills are grey now', bg in
              ('rgba(96, 96, 100, 0.88)', 'rgb(96, 96, 100)'), str(bg))

        # the settlers' table: the Proper spelling column
        heads = page.eval_on_selector_all(
            '.farm-table th', 'els => els.map(e => e.textContent.trim())')
        check('the table has the Proper spelling column',
              any('Proper spelling' in h for h in heads), str(heads))
        row2 = page.locator('#farm-2').inner_text()
        check('row 2 shows Gibel in the proper-spelling column',
              'Gibel' in row2, row2[:80])
        conj = page.evaluate(
            "document.querySelectorAll('.farm-conj').length")
        check('conjectural rows carry the asterisk mark (%d)' % conj,
              conj > 10, '%d marked' % conj)

        check('EN map page: no page errors', not errs, '; '.join(errs[:2]))
        page.close()

        # ---- the DE map page --------------------------------------------
        page = ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:200]))
        page.goto(BASE + '/de/karten/pelzucki1896/')
        try:
            page.wait_for_selector('.farm-tag', timeout=60000)
        except Exception:
            print('DE page: farm-tag never appeared - url:', page.url)
            raise
        time.sleep(2)
        inst = page.locator('.farm-tag[data-farm="92"]').first
        t92 = inst.inner_text() or ''
        check('DE page: the school’s pill speaks German (Dorfschule)',
              'Dorfschule' in t92, t92[:60])
        heads = page.eval_on_selector_all(
            '.farm-table th', 'els => els.map(e => e.textContent.trim())')
        check('DE page: the proper-spelling column reads '
              'Richtige Schreibweise',
              any('Richtige Schreibweise' in h for h in heads), str(heads))
        check('DE map page: no page errors', not errs, '; '.join(errs[:2]))
        page.close()

        # ---- document 6: the translation table --------------------------
        page = ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:200]))
        page.goto(BASE + '/documents/apl399806603/6/')
        page.wait_for_selector('.ledger', timeout=30000)
        # switch to the translation view
        page.click('[data-show="translation"]')
        time.sleep(1.5)
        body = page.inner_text('body')
        check('doc 6 translation: the proper name is there (Kończyński)',
              'Kończyński' in body)
        check('doc 6 translation: no transliteration left (Konchinskii gone)',
              'Konchinskii' not in body)
        check('doc 6 translation: Gibel (row 2)',
              'Gibel' in body)
        check('doc 6 translation: heirs reordered (heirs of Wojciech Runge)',
              'heirs of Wojciech Runge' in body)
        check('doc 6 translation: the institutions keep their labels',
              'Village school' in body and 'Common cemetery' in body)
        # diplomatic view keeps the Cyrillic
        page.click('[data-show="diplomatic"]')
        time.sleep(0.8)
        body = page.inner_text('body')
        check('doc 6 diplomatic: the Cyrillic ledger is untouched',
              'Кончинскій Яковъ' in body)
        check('doc 6 page: no page errors', not errs, '; '.join(errs[:2]))
        page.close()

        browser.close()

    failed = [n for n, ok in RESULTS if not ok]
    print('%d/%d passed' % (len(RESULTS) - len(failed), len(RESULTS))
          + ('' if not failed else ' — FAILED: ' + ', '.join(failed)))
    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
