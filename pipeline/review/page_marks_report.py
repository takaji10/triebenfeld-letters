# -*- coding: utf-8 -*-
"""
Report the forms of printed page marks in every work of the literature and
every newspaper item, and whether the generators recognise them.

The editor, 2026-11-24: literature pages got the page-number styling, but in
some texts the page numbers stood as plain text ("[720]" in "On the nutrition
of the people"). All page marks now go through one margin-marker style
(site/assets/style.css, .pg) and one recogniser, pipeline/pagemarks.py.

For a work of the literature (cut page by page by build_literature.py) the
marks are the passage files themselves: the report counts the passages by
the form of their key (a number, a roman number, "N-front", "N-uK" for an
unnumbered page, "cNN" for a section) - all drawn as margin markers by
literature_site.py - and then lists any page-mark-shaped LINE inside a
passage's text, which would be a mark the cut left in the text.

For a newspaper item the marks are lines of the text itself: each form found
is listed with its numbers, and whether it is accepted (pagemarks.find_marks:
a bare [N] only inside a run of consecutive pages).

Also counted, as "not page marks": [^n] footnote markers, "<!-- p.[...] -->"
comments (the cut's own, a page without a number), "[N]" inside a line of
text or a table cell.

Usage: python pipeline/review/page_marks_report.py [--newspapers] [--literature]
"""
import io, os, re, sys, json, collections, argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'pipeline'))
import pagemarks

CORPUS = os.path.join(ROOT, 'dataset', 'literature')
NEWS = os.path.join(ROOT, 'newspapers')
INLINE = re.compile(r'(?<![\^\w])\[(\d{1,4})\](?!\()')


def key_form(key, part=None):
    if part and key.startswith(f'{part}-'):
        return 'part-page (P-page, a multi-part work)'
    if re.fullmatch(r'\d+', key):
        return 'N (arabic page)'
    if re.fullmatch(r'[ivxlcdm]+', key, re.I):
        return 'roman page'
    if re.fullmatch(r'\d+-\d+', key):
        return 'N-M (page range)'
    if re.fullmatch(r'\d+x', key):
        return 'N+letter (a page with a suffix)'
    if key.endswith('front'):
        return 'front (no page)'
    if re.search(r'-u\d+$', key):
        return 'N-uK (unnumbered page)'
    if re.fullmatch(r'c\d+', key):
        return 'cNN (section)'
    return 'other: ' + key


def body(path):
    with io.open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    i = 0
    while i < len(lines) and lines[i].startswith('#'):
        i += 1
    return lines[i:]


def literature():
    print('== The literature: marks are the passage files (one per printed page) ==')
    with io.open(os.path.join(CORPUS, 'index.json'), encoding='utf-8') as f:
        works = json.load(f)
    for w in works:
        forms = collections.Counter(key_form(p['key'], p.get('part')) for p in w['passages'])
        inside = collections.Counter()
        comments = footnotes = 0
        for p in w['passages']:
            for lg in {w['language'], 'en'}:
                fp = os.path.join(CORPUS, w['slug'], f"{p['key']}.{lg}.txt")
                if not os.path.isfile(fp):
                    continue
                ls = body(fp)
                for i, ln in enumerate(ls):
                    if re.match(r'\s*<!--\s*p\.', ln):
                        comments += 1
                    footnotes += len(re.findall(r'\[\^[^\]\s]+\]', ln))
                for i, pg, form in pagemarks.candidates(ls):
                    inside[form] += 1
        shown = 'shown' if w.get('visible') else 'summary only'
        print(f"{w['slug']} ({w['language']}, {shown}): "
              + ', '.join(f'{k} x{v}' for k, v in sorted(forms.items())))
        if inside:
            print('    page-mark-shaped lines INSIDE passage text (not drawn as marks): '
                  + ', '.join(f'{k} x{v}' for k, v in inside.items()))
        if comments or footnotes:
            print(f'    not page marks: {footnotes} [^n] footnote markers, '
                  f'{comments} "<!-- p.[...] -->" comments')


def newspapers():
    print('\n== The newspapers: marks are lines of the text ==')
    for slug in sorted(os.listdir(NEWS)):
        d = os.path.join(NEWS, slug)
        if not os.path.isdir(d):
            continue
        for fn in ('original.md', 'english.md'):
            fp = os.path.join(d, fn)
            if not os.path.isfile(fp):
                continue
            ls = body(fp)
            cands = pagemarks.candidates(ls)
            ok = pagemarks.find_marks(ls)
            inline = [m.group(1) for ln in ls if ln.strip() and not pagemarks.candidates([ln])
                      for m in INLINE.finditer(ln)]
            if not cands and not inline:
                print(f'{slug}/{fn}: no page marks')
                continue
            by = collections.defaultdict(list)
            for i, pg, form in cands:
                by[form].append((pg, i in ok))
            for form, items in by.items():
                nums = ', '.join(p for p, _ in items)
                n_ok = sum(1 for _, a in items if a)
                verdict = ('recognised' if n_ok == len(items)
                           else 'NOT recognised (no consecutive run)' if n_ok == 0
                           else f'recognised {n_ok} of {len(items)}')
                print(f'{slug}/{fn}: {form} x{len(items)} [{nums}] -> {verdict}')
            if inline:
                print(f'{slug}/{fn}: "[N]" inside a line of text x{len(inline)} '
                      f'[{", ".join(inline)}] -> not a page mark (inline)')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--newspapers', action='store_true')
    ap.add_argument('--literature', action='store_true')
    a = ap.parse_args()
    both = not (a.newspapers or a.literature)
    if a.literature or both:
        literature()
    if a.newspapers or both:
        newspapers()
