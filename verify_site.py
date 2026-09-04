# -*- coding: utf-8 -*-
"""
Verify the built site against the canonical database.

Checks:
  1. Every record has a built page.
  2. The diplomatic text on each built page is character-identical to the corpus.
  3. Every internal link resolves to something that exists.
  4. No page requests anything from an external host.

Run after `jekyll build`. Exits non-zero on any failure.
"""
import io, sys, os, re, json, html
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site', '_site')


def _baseurl():
    """The path prefix the site is served under.

    Empty for a local build or a user/organisation site; "/<repo>" for a project
    site, where the deploy workflow passes the prefix in. Built links carry it,
    so it has to come off again before resolving them against _site/.
    """
    b = os.environ.get('SITE_BASEURL')
    if b is None:
        b = ''
        try:
            with open(os.path.join(ROOT, 'site', '_config.yml'), encoding='utf-8') as f:
                for line in f:
                    if line.startswith('baseurl:'):
                        b = line.split(':', 1)[1].strip().strip('"').strip("'")
                        break
        except OSError:
            pass
    b = b.strip().strip('/')
    return '/' + b if b else ''


BASEURL = _baseurl()

failures = []


def fail(msg):
    failures.append(msg)
    print('  FAIL ' + msg)


def main():
    with open(os.path.join(ROOT, 'letters.json'), encoding='utf-8') as f:
        recs = json.load(f)
    by_id = {r['letter_id']: r for r in recs}

    if not os.path.isdir(SITE):
        print('No _site/ - run `bundle exec jekyll build` in site/ first.')
        sys.exit(1)

    # ---- 1 & 2: coverage and text fidelity -------------------------------
    print('checking letter pages...')
    seen = set()
    total_ms_pages = 0
    for lid, rec in by_id.items():
        # The record carries its own URL, so this follows the unit-scoped
        # permalink rather than assuming a shape.
        rel = rec.get('permalink', f'/letters/{lid}/').strip('/').replace('/', os.sep)
        path = os.path.join(SITE, rel, 'index.html')
        if not os.path.isfile(path):
            fail(f'letter {lid}: no page built at {rec.get("permalink", lid)}')
            continue
        seen.add(lid)
        with open(path, encoding='utf-8') as f:
            page = f.read()
        # The diplomatic view is one <li> per manuscript line; pulling them back
        # out must reproduce the corpus's non-blank lines exactly, in order.
        recovered = [html.unescape(x) for x in re.findall(r'<li>(.*?)</li>', page, re.S)]
        # The rendered view is the transcription layer: the manuscript's own
        # lines, with line-end marks resolved per the recorded decisions.
        expected = [l for p in rec['pages']
                    for l in p.get('transcription', p['diplomatic']).split('\n')
                    if l.strip()]
        if not recovered:
            fail(f'letter {lid}: no diplomatic lines in built page')
            continue
        if recovered != expected:
            fail(f'letter {lid}: diplomatic text differs from the corpus '
                 f'({len(recovered)} lines vs {len(expected)})')
        ms = len(re.findall(r'<section class="ms-page"', page))
        total_ms_pages += ms
        expected_pages = len(rec.get('pages') or [])
        if ms != expected_pages:
            fail(f'letter {lid}: {ms} page sections built, {expected_pages} expected')
    print(f'  {len(seen)}/{len(by_id)} letters built with exact text')
    print(f'  {total_ms_pages} manuscript page sections')

    # ---- 3: internal links -----------------------------------------------
    print('checking internal links...'
          + (f'  (baseurl {BASEURL})' if BASEURL else ''))
    pages = []
    for dirpath, _, filenames in os.walk(SITE):
        for fn in filenames:
            if fn.endswith('.html'):
                pages.append(os.path.join(dirpath, fn))

    def exists(url):
        u = url.split('#')[0].split('?')[0]
        if BASEURL:
            if u == BASEURL:
                u = '/'
            elif u.startswith(BASEURL + '/'):
                u = u[len(BASEURL):]
        if not u or u == '/':
            return os.path.isfile(os.path.join(SITE, 'index.html'))
        rel = u.strip('/').replace('/', os.sep)
        target = os.path.join(SITE, rel)
        return (os.path.isfile(target)
                or os.path.isfile(target + '.html')
                or os.path.isfile(os.path.join(target, 'index.html')))

    broken = Counter()
    checked = 0
    for p in pages:
        with open(p, encoding='utf-8') as f:
            content = f.read()
        for url in re.findall(r'(?:href|src)="([^"]+)"', content):
            if url.startswith(('http://', 'https://', 'mailto:', 'data:', '#')):
                continue
            checked += 1
            if not exists(url):
                broken[url] += 1
    if broken:
        for url, n in broken.most_common(15):
            fail(f'broken link ({n}x): {url}')
    print(f'  {checked} internal links checked, {len(broken)} distinct broken')

    # ---- 4: no external requests -----------------------------------------
    # Only resources the browser FETCHES count. A plain <a href> to an external
    # site is a citation, not a dependency - the page renders fine without it.
    print('checking for external dependencies...')
    ext = Counter()
    links = Counter()
    for p in pages:
        with open(p, encoding='utf-8') as f:
            content = f.read()
        for url in re.findall(r'\ssrc="(https?://[^"]+)"', content):
            ext[url] += 1
        for tag in re.findall(r'<link\b[^>]*>', content):
            m = re.search(r'href="(https?://[^"]+)"', tag)
            if m:
                ext[m.group(1)] += 1
        for url in re.findall(r'<a\b[^>]*href="(https?://[^"]+)"', content):
            links[url] += 1
    if ext:
        for url, n in ext.most_common():
            fail(f'external resource fetched ({n}x): {url}')
    print(f'  {len(ext)} external resources fetched (want 0)')
    print(f'  {len(links)} outbound citation links (fine)')

    # ---- summary ----------------------------------------------------------
    print()
    if failures:
        print(f'FAILED - {len(failures)} problem(s)')
        sys.exit(1)
    print('ALL CHECKS PASSED')
    print(f'  {len(by_id)} documents, text verified character-exact')
    print(f'  {checked} internal links resolve')
    print('  no external network dependencies')


if __name__ == '__main__':
    main()
