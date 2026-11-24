# -*- coding: utf-8 -*-
"""
Check that no page runs its text across the whole screen.

The editor, 2026-11-24: two works' pages (Seidel 2018, Słowiński & Połom
2024) had their text spanning the entire screen, unlike every other page. This
serves the built site (site/_site, the baseurl of site/_config.yml) with a
small static server, opens every built page of the literature, the
newspapers, the places, the people and the holdings (and a sample of the
documents) at a 1440px viewport in a headless Chromium (Node + Playwright, run
from an inline script), and measures the width of each line of text in every
paragraph and list item. A page with a line wider than LIMIT px is reported
(the widest few offenders, with their class names), and the script exits 1.

Needs the site built (cd site && bundle exec jekyll build) and `playwright`
for Node (require('playwright') must resolve).

Usage: python pipeline/review/check_text_width.py [--limit 760] [--docs 40]
                                                   [--width 1440] [--only substring]
"""
import argparse, os, random, re, subprocess, sys, tempfile, threading, http.server, functools, socketserver
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.join(ROOT, 'site')
OUT = os.path.join(SITE, '_site')

# The list pages (cards in a grid, not running text) are not measured here.
LIST_PAGES = {'documents/', 'de/dokumente/', 'literature/', 'newspapers/', 'places/', 'people/', 'sources/', 'sources/archive/',
              'de/literatur/', 'de/zeitungen/', 'de/orte/', 'de/personen/', 'de/quellen/',
              'de/quellen/archiv/'}

# A holding's page (.unit) is laid out at --wide (62rem = 992px) on purpose: its
# head, About and Method share one measure (assets/style.css, "a holding's
# page"). Its text is checked against that width, everything else against LIMIT.
UNIT_LIMIT = 1000

# the sections whose every page is checked: first path segment(s), English and German
SECTIONS = ('literature/', 'newspapers/', 'places/', 'people/', 'sources/',
            'de/literatur/', 'de/zeitungen/', 'de/orte/', 'de/personen/', 'de/quellen/')

JS = r'''
const { chromium } = require('playwright');
const [,, base, listFile, width, limit, unitLimit] = process.argv;
const urls = require('fs').readFileSync(listFile, 'utf8').split('\n').filter(Boolean);
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: +width, height: 900 }, deviceScaleFactor: 1 });
  const bad = [];
  for (const u of urls) {
    await page.goto(base + u, { waitUntil: 'load' });
    await page.waitForTimeout(60);
    const r = await page.evaluate(([limit, unitLimit]) => {
      const out = [];
      for (const el of document.querySelectorAll('main p, main li')) {
        if (el.closest('nav, header.site-head, footer, table, .nav-drop, script, [hidden]')) continue;
        if (!el.offsetParent) continue;
        let w = 0;
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        let n;
        while ((n = walker.nextNode())) {
          if (!n.nodeValue.trim()) continue;
          const rg = document.createRange(); rg.selectNodeContents(n);
          for (const c of rg.getClientRects()) w = Math.max(w, c.width);
        }
        if (w > (el.closest('.unit') ? unitLimit : limit)) out.push([Math.round(w), el.tagName.toLowerCase() + '.' + (el.className || '') + ' in ' +
          (el.parentElement ? el.parentElement.tagName.toLowerCase() + '.' + (el.parentElement.className || '') : ''),
          el.textContent.trim().slice(0, 50)]);
      }
      out.sort((a, b) => b[0] - a[0]);
      return out;
    }, [+limit, +unitLimit]);
    if (r.length) bad.push([u, r.length, r.slice(0, 3)]);
  }
  await browser.close();
  console.log(JSON.stringify({ n: urls.length, bad }));
})();
'''


def baseurl():
    with open(os.path.join(SITE, '_config.yml'), encoding='utf-8') as f:
        return (yaml.safe_load(f).get('baseurl') or '').rstrip('/')


def built_pages():
    pages = []
    for dp, dn, fn in os.walk(OUT):
        if 'index.html' in fn:
            rel = os.path.relpath(dp, OUT).replace(os.sep, '/')
            pages.append('' if rel == '.' else rel + '/')
    return sorted(pages)


def redirect(p):
    """An old address that only redirects (meta refresh) has no text to measure."""
    with open(os.path.join(OUT, p, 'index.html'), encoding='utf-8') as f:
        return 'http-equiv="refresh"' in f.read(3000)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=760)
    ap.add_argument('--width', type=int, default=1440)
    ap.add_argument('--docs', type=int, default=40, help='how many document pages to sample')
    ap.add_argument('--only', default='', help='check only pages whose path contains this')
    a = ap.parse_args()
    if not os.path.isdir(OUT):
        sys.exit('site/_site is not built: cd site && bundle exec jekyll build')
    pages = built_pages()
    chosen = [p for p in pages if p.startswith(SECTIONS) and p not in LIST_PAGES]
    docs = [p for p in pages if p.startswith(('documents/', 'de/dokumente/'))]
    random.Random(7).shuffle(docs)
    sample = sorted(set(chosen + docs[:a.docs]))
    sample = [p for p in sample if not redirect(p)]
    if a.only:
        sample = [p for p in sample if a.only in p]
    bu = baseurl()

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args): pass
    handler = functools.partial(Quiet, directory=OUT)
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{srv.server_address[1]}{bu}/'
    with tempfile.TemporaryDirectory() as td:
        lst, js = os.path.join(td, 'urls.txt'), os.path.join(td, 'run.js')
        open(lst, 'w', encoding='utf-8').write('\n'.join(sample))
        open(js, 'w', encoding='utf-8').write(JS)
        env = dict(os.environ)
        env.setdefault('NODE_PATH', subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip())
        r = subprocess.run(['node', js, base, lst, str(a.width), str(a.limit), str(UNIT_LIMIT)],
                           capture_output=True, text=True, env=env, cwd=ROOT)
    srv.shutdown()
    if r.returncode:
        sys.exit(r.stderr)
    import json
    res = json.loads(r.stdout.strip().splitlines()[-1])
    print(f"{res['n']} pages at {a.width}px, text lines wider than {a.limit}px:")
    for u, n, ex in res['bad']:
        print(f"  /{u}  ({n} blocks)")
        for w, sel, txt in ex:
            print(f"      {w}px  {sel}  \"{txt}\"")
    if not res['bad']:
        print('  none')
    sys.exit(1 if res['bad'] else 0)


if __name__ == '__main__':
    main()
