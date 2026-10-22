# -*- coding: utf-8 -*-
"""
Verify the built site against the canonical database.

Checks:
  1. Every record has a built page.
  2. The diplomatic text on each built page is character-identical to the corpus,
     or, for a document transcribed as a table, cell-identical to it.
  3. Every internal link resolves to something that exists.
  4. No page requests anything from an external host.

Run after `jekyll build`. Exits non-zero on any failure.
"""
import io, sys, os, re, json, html, collections
from collections import Counter
import unitlib

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


FN_MARKUP = re.compile(r'<sup class="fn">|</sup>|<span class="fn-note">|</span>')

def fail(msg):
    failures.append(msg)
    print('  FAIL ' + msg)


def main():
    # Read the per-document files, which are what the dataset is. Verifying
    # against the merged array would leave the primary form unchecked.
    recs = unitlib.load_documents(ROOT)
    # Keyed by uid: an archival number is unique only within its holding, so
    # keying by letter_id drops one unit's document 7 on top of another's.
    by_uid = {r['uid']: r for r in recs}

    if not os.path.isdir(SITE):
        print('No _site/ - run `bundle exec jekyll build` in site/ first.')
        sys.exit(1)

    # A tabulated document's transcription is its table, so its pages are
    # checked cell by cell against the table rows in the corpus.
    tables = {(u.slug, lid): t for u in unitlib.load_units()
              for lid, t in unitlib.load_tables(u).items()}

    # ---- 1 & 2: coverage and text fidelity -------------------------------
    print('checking letter pages...')
    seen = set()
    total_ms_pages = 0
    n_tables = 0
    for lid, rec in by_uid.items():
        # The record carries its own URL, so this follows the unit-scoped
        # permalink rather than assuming a shape.
        rel = rec.get('permalink', f'/documents/{lid}/').strip('/').replace('/', os.sep)
        path = os.path.join(SITE, rel, 'index.html')
        if not os.path.isfile(path):
            fail(f'letter {lid}: no page built at {rec.get("permalink", lid)}')
            continue
        seen.add(lid)
        with open(path, encoding='utf-8') as f:
            page = f.read()
        tbl = tables.get((rec.get('unit'), rec.get('letter_id')))
        if tbl:
            recovered = unitlib.table_rows_in_page(page)
            expected = unitlib.table_expected_rows(tbl)
            if recovered != expected:
                fail(f'letter {lid}: table differs from the corpus '
                     f'({len(recovered)} rows vs {len(expected)})')
            n_tables += 1
            ms = len(re.findall(r'<section class="ms-page"', page))
            total_ms_pages += ms
            if ms != len(rec.get('pages') or []):
                fail(f'letter {lid}: {ms} page sections built, '
                     f'{len(rec.get("pages") or [])} expected')
            continue
        # The diplomatic view is one <li> per manuscript line, inside
        # <ol class="dip">. Scope the extraction to those lists: the page also
        # carries other <li> - the typed relations to other documents - and a
        # bare <li> match would read them back as if they were transcription.
        # A printed edition's footnote markers are raised and its note lines
        # set apart (build_site_data.footnote_html); the text under the markup
        # is what is checked.
        recovered = [html.unescape(FN_MARKUP.sub('', x))
                     for blk in re.findall(r'<ol class="dip"[^>]*>(.*?)</ol>', page, re.S)
                     for x in re.findall(r'<li>(.*?)</li>', blk, re.S)]
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
    print(f'  {len(seen)}/{len(by_uid)} documents built with exact text'
          + (f' ({n_tables} as tables, checked cell by cell)' if n_tables else ''))
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

    # ---- URLs a script builds, which the link check cannot see -------------
    # Everything above reads href="..." out of the built HTML. browse.js used to
    # assemble each result's href from a base plus the unit and id, so the whole
    # browse list could point at a URL space the pages had left and every check
    # here would still pass. Grepping the built assets is crude and catches
    # exactly that.
    print('checking for stale URLs in scripts...')
    stale = collections.Counter()
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs if d not in ('redirects', 'redirects-static')]
        for fn in files:
            if not fn.endswith('.js'):
                continue
            p = os.path.join(root, fn)
            with io.open(p, encoding='utf-8', errors='replace') as f:
                for m in re.finditer(r'[\'"]/(?:letters|de/briefe)/', f.read()):
                    stale[os.path.relpath(p, SITE) + ': ' + m.group(0)] += 1
    for where, n in stale.most_common():
        fail(f'script builds a pre-migration URL ({n}x): {where}')
    print(f'  {len(stale)} stale URL literal(s) in built scripts (want 0)')

    # ---- the literature (docs/LITERATURE_PLAN.md) -------------------------
    # Every visible work has its page in both languages. A work with
    # visible: false (under copyright: Seidel, Pinkas Hakehillot) has none of
    # its text on the site: it has a page in both languages holding only the
    # summary of its contents (the editor, 2026-10-21), with no passage, and
    # no stretch of its text, original or English, is found in any built file.
    # Its title and its citations ("Seidel 2018, ch. ...") are allowed.
    print('checking the literature...')
    lit_index = os.path.join(ROOT, 'corpus', 'literature', 'index.json')
    lit_dir = os.path.join(ROOT, 'corpus', 'literature')
    works = []
    if os.path.isfile(lit_index):
        with io.open(lit_index, encoding='utf-8') as f:
            works = json.load(f)
    shown = [w for w in works if w.get('visible')]
    hidden = [w for w in works if not w.get('visible')]
    for w in shown:
        for base in ('literature', os.path.join('de', 'literatur')):
            if not os.path.isfile(os.path.join(SITE, base, w['slug'], 'index.html')):
                fail(f"literature: no page {base}/{w['slug']}/")
    if hidden:
        needles = {}
        for w in hidden:
            for base in ('literature', os.path.join('de', 'literatur')):
                page = os.path.join(SITE, base, w['slug'], 'index.html')
                if not os.path.isfile(page):
                    fail(f"literature: {w['slug']} has no summary page {base}/{w['slug']}/")
                    continue
                with io.open(page, encoding='utf-8') as f:
                    built = f.read()
                if 'lit-summary' not in built or 'lit-passage' in built:
                    fail(f"literature: {base}/{w['slug']}/ is to hold only a summary, not the text")
            # stretches of its text: the middle of the longest line of up to
            # 40 passages, evenly spread, in each language it has
            ps = w.get('passages') or []
            step = max(1, len(ps) // 40)
            for q in ps[::step]:
                for lg in (w['language'], 'en'):
                    fp = os.path.join(lit_dir, w['slug'], f"{q['key']}.{lg}.txt")
                    if not os.path.isfile(fp):
                        continue
                    with io.open(fp, encoding='utf-8') as f:
                        body = [ln.strip() for ln in f if not ln.startswith('#')]
                    longest = max(body, key=len, default='')
                    if len(longest) >= 120:
                        mid = len(longest) // 2
                        needles[longest[mid - 30:mid + 30]] = w['slug']
        leaks = collections.Counter()
        for root, dirs, files in os.walk(SITE):
            for fn in files:
                if not fn.endswith(('.html', '.js', '.json', '.xml', '.txt', '.csv')):
                    continue
                p = os.path.join(root, fn)
                with io.open(p, encoding='utf-8', errors='replace') as f:
                    text = html.unescape(f.read())
                for needle, slug in needles.items():
                    if needle in text:
                        leaks[f'{slug} in {os.path.relpath(p, SITE)}'] += 1
        for where in leaks:
            fail(f'literature: the text of a work not to be shown appears on the site: {where}')
    print(f'  {len(shown)} works with pages in both languages, '
          f'{len(hidden)} kept off the site (summary only)')

    # ---- the newspapers (docs/NEWSPAPERS_PLAN.md) -------------------------
    # Every visible item has its page in both languages, and its page holds
    # its text. An item with visible: false has a page holding only the
    # summary of its contents, and no stretch of its text appears anywhere.
    print('checking the newspapers...')
    np_data = os.path.join(ROOT, 'site', '_data', 'newspapers.yml')
    if os.path.isfile(np_data):
        import yaml
        with io.open(np_data, encoding='utf-8') as f:
            np_items = yaml.safe_load(f) or []
        np_shown = [w for w in np_items if not w.get('summary_only')]
        np_hidden = [w for w in np_items if w.get('summary_only')]
        for w in np_shown:
            for base in ('newspapers', os.path.join('de', 'zeitungen')):
                if not os.path.isfile(os.path.join(SITE, base, w['slug'], 'index.html')):
                    fail(f"newspapers: no page {base}/{w['slug']}/")
        needles = {}
        for w in np_hidden:
            for base in ('newspapers', os.path.join('de', 'zeitungen')):
                page = os.path.join(SITE, base, w['slug'], 'index.html')
                if not os.path.isfile(page):
                    fail(f"newspapers: {w['slug']} has no summary page {base}/{w['slug']}/")
                    continue
                with io.open(page, encoding='utf-8') as f:
                    built = f.read()
                if 'np-summary' not in built or 'lit-orig' in built:
                    fail(f"newspapers: {base}/{w['slug']}/ is to hold only a summary, not the text")
            for fn, lg in (('original.md', w['language']), ('english.md', 'en')):
                fp = os.path.join(ROOT, 'newspapers', w['slug'], fn)
                if not os.path.isfile(fp):
                    continue
                with io.open(fp, encoding='utf-8') as f:
                    body = [ln.strip() for ln in f if not ln.startswith('#')]
                longest = max(body, key=len, default='')
                if len(longest) >= 120:
                    mid = len(longest) // 2
                    needles[longest[mid - 30:mid + 30]] = w['slug']
        leaks = collections.Counter()
        for root, dirs, files in os.walk(SITE):
            for fn in files:
                if not fn.endswith(('.html', '.js', '.json', '.xml', '.txt', '.csv')):
                    continue
                p = os.path.join(root, fn)
                with io.open(p, encoding='utf-8', errors='replace') as f:
                    text = html.unescape(f.read())
                for needle, slug in needles.items():
                    if needle in text:
                        leaks[f'{slug} in {os.path.relpath(p, SITE)}'] += 1
        for where in leaks:
            fail(f'newspapers: the text of an item not to be shown appears on the site: {where}')
        print(f'  {len(np_shown)} items with pages in both languages, '
              f'{len(np_hidden)} kept off the site (summary only)')

    # The hand-made links (literature/links.yml), on both sides: each passage's
    # box links each document, and each document's page links each passage.
    links_data = os.path.join(ROOT, 'site', '_data', 'literature_links.yml')
    if os.path.isfile(links_data):
        import yaml
        with io.open(links_data, encoding='utf-8') as f:
            per_doc = yaml.safe_load(f) or {}
        with io.open(os.path.join(ROOT, 'corpus', 'letters.json'), encoding='utf-8') as f:
            permalink = {r['uid']: r['permalink'] for r in json.load(f)}
        n = 0
        for uid, lns in per_doc.items():
            doc_page = os.path.join(SITE, permalink[uid].strip('/'), 'index.html')
            with io.open(doc_page, encoding='utf-8') as f:
                doc_html = f.read()
            for ln in lns:
                for w in ln['works']:
                    for base in ('literature', os.path.join('de', 'literatur')):
                        with io.open(os.path.join(SITE, base, w['work'], 'index.html'),
                                     encoding='utf-8') as f:
                            work_html = f.read()
                        for pg in w['pages']:
                            n += 1
                            sec = work_html.split(f'id="p-{pg["key"]}"', 1)[-1].split('</section>', 1)[0]
                            if f'href="{BASEURL}{permalink[uid]}"' not in sec:
                                fail(f"literature: {base}/{w['work']}/#p-{pg['key']} does not link {uid}")
                            if f'/literature/{w["work"]}/#p-{pg["key"]}"' not in doc_html:
                                fail(f"literature: {uid}'s page does not link {w['work']}/#p-{pg['key']}")
        print(f'  {n} hand-made links checked on both sides ({len(per_doc)} documents)')

    # ---- summary ----------------------------------------------------------
    print()
    if failures:
        print(f'FAILED - {len(failures)} problem(s)')
        sys.exit(1)
    print('ALL CHECKS PASSED')
    print(f'  {len(by_uid)} documents, text verified character-exact')
    print(f'  {checked} internal links resolve')
    print('  no external network dependencies')


if __name__ == '__main__':
    main()
