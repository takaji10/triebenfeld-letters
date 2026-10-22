# -*- coding: utf-8 -*-
"""
The literature on the website: a list of the works and a page for each.

Reads  : corpus/literature/index.json and the passage files beside it
         (made by build_literature.py), site/_data/i18n.yml (the labels),
         literature/links.yml (the hand-made links), corpus/letters.json and
         units/<slug>/unit.yml (the linked documents)
Writes : site/_data/literature.yml         the visible works, for the list page
         site/_data/literature_links.yml   the links, by document (letter.html)
         site/_literature/<slug>.md        /literature/<slug>/
         site/_literature_de/<slug>.md     /de/literatur/<slug>/

A passage named in literature/links.yml gets a box, "In the edition", with
the link's sentence and its documents; the document's page shows the same
sentence and the passages, "In the literature". The script stops on a link to
a passage or a document that does not exist, or to a work not shown.

A work with `visible: false` (Seidel, Pinkas Hakehillot: under copyright,
docs/LITERATURE_PLAN.md section 4) has none of its text on the site. It is
listed, and its page holds only the detailed summary of its contents from its
work.yml (`summary_en`, `summary_de`; the editor, 2026-10-21). verify_site.py
holds the built site to that.

A work with `parent:` (Janocki 1779, attached to Paciorkowski 1776: the
sub-item, docs/LITERATURE_PLAN.md section 18) is shown on the Literature page
inside its parent's section, and its page links back to the parent; the
parent's page carries the sub-work's note (`note_en`, `note_de`).

A work made from a page of the Minakowska genealogy database
(docs/LITERATURE_PLAN.md section 22) is an excerpt of that page: the work's
`make_original.py` makes both `original.md` (the editor's sections, shown
here) and `full.md` (the whole page, the knowledgebase, never shown here).
No page marks: cut at its headings.

Each page gives the work passage by passage, each passage headed by its
printed page so that it can be cited, and holding both texts, the original and
the English; the page shows one of them at a time, the English first, by the
buttons of _layouts/literature.html (site/assets/literature.js). The
text is the passage file's, rendered as Markdown by Jekyll. Only the rendering
is changed, never the words: footnote markers [^n] become links to their notes
(kramdown's own footnotes would clash between the two texts), headings are
set two levels down under the page's own, and the four-space indent of a
note's second paragraph is taken off so that it is not shown as code, a "|"
outside a table is escaped (kramdown would make the line a table), and a line
break inside a paragraph is kept as a break.

A work printed in English (`language: en`, Mączak 1968) has one text, shown
without the buttons. A work's `figures` (page key -> file in
site/assets/literature/<slug>/) put the picture of that page above its text:
a map, a chart, a photograph (the editor, 2026-10-20).

The list page is in the order of the authors' names (`author_sort`, "Breyer,
Albert"; an anonymous work by its title), each author's works by year (the
editor, 2026-10-20).
Everything under site/_literature* is generated output.

Usage: python pipeline/literature/literature_site.py
"""
import io, os, re, sys, json, html, unicodedata
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORPUS = os.path.join(ROOT, 'corpus', 'literature')
SITE = os.path.join(ROOT, 'site')
BASES = {'en': ('_literature', '/literature/', '/de/literatur/'),
         'de': ('_literature_de', '/de/literatur/', '/literature/')}

DEF = re.compile(r'^\[\^([^\]\s]+)\]:[ \t]*', re.M)
# a note ([^5]: at the start of a line) or a marker ([^5] anywhere else)
NOTE = re.compile(r'^\[\^(?P<d>[^\]\s]+)\]:[ \t]*|\[\^(?P<r>[^\]\s]+)\]', re.M)
HEADING = re.compile(r'^(#{1,6})(?=\s)', re.M)
IAL = re.compile(r'[ \t]*\{#[^}]*\}[ \t]*$', re.M)


def passage_text(slug, key, lang):
    path = os.path.join(CORPUS, slug, f'{key}.{lang}.txt')
    if not os.path.isfile(path):
        return None
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    # three comment lines and a blank line (build_literature.header)
    assert all(l.startswith('# ') for l in lines[:3]) and lines[3] == '', path
    return '\n'.join(lines[4:]).rstrip('\n')


def footnotes(texts, lang):
    """Turn [^n] into links and [^n]: into anchored notes, across one work.

    A marker links to the first note of its number at or after it, else the
    last one before it: a book may number its notes again in each chapter."""
    defs = []                       # (passage index, offset, id)
    for i, t in enumerate(texts):
        if t:
            defs += [(i, m.start(), m.group(1)) for m in DEF.finditer(t)]
    anchor = {d: f'n-{lang}-{n}' for n, d in enumerate(defs, 1)}

    def target(i, pos, fid):
        same = [d for d in defs if d[2] == fid]
        after = [d for d in same if (d[0], d[1]) >= (i, pos)]
        d = after[0] if after else (same[-1] if same else None)
        return anchor.get(d)

    out, missing = [], 0
    for i, t in enumerate(texts):
        if t is None:
            out.append(None)
            continue
        def one(m):
            nonlocal missing
            if m.group('d'):
                return (f'<span class="lit-note" id="{anchor[(i, m.start(), m.group("d"))]}">'
                        f'{m.group("d")}</span> ')
            a = target(i, m.start(), m.group('r'))
            if not a:
                missing += 1
                return m.group(0)
            return f'<sup class="lit-fn"><a href="#{a}">{m.group("r")}</a></sup>'
        out.append(NOTE.sub(one, t))
    return out, missing


BLOCK = re.compile(r'^\s*(\||#|[-*+] |\d+[.)] )')


def render(t):
    t = IAL.sub('', t)
    t = HEADING.sub(lambda m: '#' * min(6, len(m.group(1)) + 2), t)
    t = re.sub(r'^    (?=\S)', '', t, flags=re.M)
    # a name printed as asterisks ("v. ****d") is not emphasis
    t = re.sub(r'\*{4,}', lambda m: '\\*' * len(m.group(0)), t)
    lines = t.split('\n')
    for i, line in enumerate(lines):
        table = line.lstrip().startswith('|')
        # kramdown takes any line with a "|" for a table row ("16|38.")
        if not table:
            line = line.replace('|', '\\|')
        # a line break inside a paragraph is kept, as the files show it
        nxt = lines[i + 1] if i + 1 < len(lines) else ''
        if (line.strip() and nxt.strip() and not table and not line.lstrip().startswith('#')
                and not BLOCK.match(nxt) and not line.endswith(('  ', '\\'))):
            line += '  '
        lines[i] = line
    return '\n'.join(lines)


def label(p, s):
    t = _label(p, s)
    return t[:1].upper() + t[1:] if p['key'].endswith('front') else t


def _label(p, s):
    if p['key'] == 'notes':
        return s['lit_notes']
    if p.get('title'):
        return p['title']
    part = s['lit_part'].replace('%d', str(p['part'])) + ', ' if p['part'] else ''
    if p['key'].endswith('front'):
        return part + s['lit_front']
    m = re.search(r'(\w+)-u(\d+)$', p['key'])
    if m:
        return part + s['lit_unnumbered'].replace('%s', m.group(1))
    return part + s['lit_page'].replace('%s', str(p['page']))


def short(p, s):
    """The label in the list of pages at the head of a work."""
    if p['key'] == 'notes':
        return s['lit_notes']
    if p.get('title'):
        return p['title']
    if p['key'].endswith('front'):
        return (f"{p['part']}: " if p['part'] else '') + s['lit_front_short']
    if re.search(r'-u\d+$', p['key']):
        return None
    return (f"{p['part']}: " if p['part'] and p['page'] in ('1',) else '') + str(p['page'])


def yaml_str(v):
    return json.dumps(v, ensure_ascii=False)


MONTHS = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
          7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November',
          12: 'December'}
MONTHS_DE = {1: 'Januar', 2: 'Februar', 3: 'März', 4: 'April', 5: 'Mai', 6: 'Juni',
             7: 'Juli', 8: 'August', 9: 'September', 10: 'Oktober', 11: 'November',
             12: 'Dezember'}


def doc_date(r, lang):
    """The date as the document's own page gives it (build_site_data.date_label)."""
    if not r['date_iso']:
        return 'undatiert' if lang == 'de' else 'undated'
    y, m, d = r['year'], r['month'], r['day']
    months = MONTHS_DE if lang == 'de' else MONTHS
    if d:
        return f"{d}. {months[m]} {y}" if lang == 'de' else f"{d} {months[m]} {y}"
    return f"{months[m]} {y}" if m else str(y)


def load_links(works):
    """literature/links.yml, checked against the passages and the documents.

    Returns the links, each with `docs` (the documents' records from
    corpus/letters.json, with their holding's `ref`). Stops on a passage or a
    document that does not exist, and on a passage of a work not shown."""
    path = os.path.join(ROOT, 'literature', 'links.yml')
    if not os.path.isfile(path):
        return []
    with open(path, encoding='utf-8') as f:
        links = yaml.safe_load(f) or []
    with open(os.path.join(ROOT, 'corpus', 'letters.json'), encoding='utf-8') as f:
        letters = {r['uid']: r for r in json.load(f)}
    by_slug = {w['slug']: w for w in works}
    refs, errors = {}, []
    for ln in links:
        for k in ('id', 'passages', 'documents', 'en', 'de'):
            if not ln.get(k):
                errors.append(f"{ln.get('id', '?')}: no {k}")
        for pk in ln.get('passages', []):
            slug, _, key = pk.partition('/')
            w = by_slug.get(slug)
            if not w:
                errors.append(f"{ln['id']}: no work {slug}")
            elif not w.get('visible'):
                errors.append(f"{ln['id']}: {slug} is not shown on the site")
            elif key not in {p['key'] for p in w['passages']}:
                errors.append(f"{ln['id']}: no passage {pk}")
        ln['docs'] = []
        for uid in ln.get('documents', []):
            r = letters.get(uid)
            if not r:
                errors.append(f"{ln['id']}: no document {uid}")
                continue
            if r['unit'] not in refs:
                with open(os.path.join(ROOT, 'units', r['unit'], 'unit.yml'), encoding='utf-8') as f:
                    refs[r['unit']] = yaml.safe_load(f)['ref']
            ln['docs'].append(r | {'ref': refs[r['unit']]})
    if errors:
        sys.exit('literature/links.yml:\n  ' + '\n  '.join(errors))
    return links


def links_box(lns, s, lang):
    """The "In the edition" box under a passage: each link's sentence and documents.

    Outside the {% raw %} block of the page, for relative_url."""
    out = ['{% endraw %}<aside class="lit-links">',
           f'<p class="lit-links-head">{s["lit_in_edition"]}</p>']
    for ln in lns:
        out.append(f'<p>{html.escape(ln[lang], quote=False)}</p>')
        out.append('<p class="lit-links-docs">' + ''.join(
            f'<a href="{{{{ \'{r["permalink"]}\' | relative_url }}}}">'
            + html.escape(s['lit_doc'].replace('%s', r['ref'], 1).replace('%s', str(r['letter_id']), 1))
            + f' ({doc_date(r, lang)})</a>'
            for r in ln['docs']) + '</p>')
    out.append('</aside>{% raw %}')
    return out


def sort_key(w):
    """The author's name as the list sorts it: brackets and accents ignored, Ł as L."""
    name = w.get('author_sort') or w['title']
    name = name.replace('[', '').replace(']', '').replace('Ł', 'L').replace('ł', 'l')
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()
    return (name, w['year'])


def figure(slug, key, files, cite, s):
    """The picture of a page, outside the {% raw %} block for relative_url."""
    f = files.get(str(key))
    if not f:
        return []
    url = f"/assets/literature/{slug}/{f}"
    alt = html.escape(f"{cite}, {s['lit_page'].replace('%s', str(key))}")
    link = "{{ '" + url + "' | relative_url }}"
    return ['{% endraw %}<figure class="lit-figure">'
            f'<a href="{link}" target="_blank" rel="noopener">'
            f'<img src="{link}" alt="{alt}" loading="lazy"></a>'
            '</figure>{% raw %}']


def main():
    with open(os.path.join(CORPUS, 'index.json'), encoding='utf-8') as f:
        works = json.load(f)
    with open(os.path.join(SITE, '_data', 'i18n.yml'), encoding='utf-8') as f:
        strings = yaml.safe_load(f)
    shown = [w for w in works if w.get('visible')]
    hidden = [w['slug'] for w in works if not w.get('visible')]
    links = load_links(works)
    at = {}                         # "<work>/<key>" -> the links naming it
    for ln in links:
        for pk in ln['passages']:
            at.setdefault(pk, []).append(ln)

    for lang, (folder, base, other) in BASES.items():
        out_dir = os.path.join(SITE, folder)
        os.makedirs(out_dir, exist_ok=True)
        for fn in os.listdir(out_dir):
            os.remove(os.path.join(out_dir, fn))

    listing = []
    for w in sorted(shown, key=sort_key):
        slug, orig = w['slug'], w['language']
        ps = w['passages']
        langs = [orig] if orig == 'en' else [orig, 'en']
        texts = {}
        for lg in langs:
            texts[lg], missing = footnotes([passage_text(slug, p['key'], lg) for p in ps], lg)
            if missing:
                print(f'{slug} ({lg}): {missing} note markers with no note, left as they stand')
        listing_row = {k: w.get(k, '') for k in (
            'slug', 'kind', 'parent', 'title', 'title_en', 'cite', 'author',
            'author_sort', 'published', 'year', 'language', 'english_by', 'scan',
            'note_en', 'note_de', 'account_en', 'account_de')}
        if not listing_row['parent']:       # Liquid reads "" as true
            del listing_row['parent']
        listing.append(listing_row | {'pages': sum(1 for p in ps if p['page'])})
        for lang, (folder, base, other) in BASES.items():
            s = strings[lang]
            body = ['{% raw %}', '<nav class="lit-jump" aria-label="' + s['lit_pages'] + '">']
            jumps = [(p['key'], short(p, s)) for p in ps]
            body.append(' '.join(f'<a href="#p-{k}">{v}</a>' for k, v in jumps if v))
            body.append('</nav>')
            for i, p in enumerate(ps):
                body += ['', f'<section class="lit-passage" id="p-{p["key"]}">',
                         f'<h2 class="lit-loc"><a href="#p-{p["key"]}">{label(p, s)}</a></h2>']
                body += figure(slug, p['key'], w.get('figures') or {}, w['cite'], s)
                pairs = (((orig, 'lit-only'),) if orig == 'en'
                         else ((orig, 'lit-orig'), ('en', 'lit-en')))
                for lg, cls in pairs:
                    t = texts[lg][i]
                    if t is None:
                        which = s['lit_english'] if lg == 'en' else s['lit_original']
                        body += [f'<div class="{cls} lit-none" lang="{lg}">',
                                 '<p>' + s['lit_missing'].replace('%s', which) + '</p>', '</div>']
                    else:
                        body += [f'<div class="{cls}" lang="{lg}" markdown="1">', '',
                                 render(t), '', '</div>']
                if f'{slug}/{p["key"]}' in at:
                    body += links_box(at[f'{slug}/{p["key"]}'], s, lang)
                body.append('</section>')
            body.append('{% endraw %}')
            fm = ['---',
                  f'work: {yaml_str(slug)}',
                  f'title: {yaml_str(w["cite"])}',
                  f'lang: {lang}',
                  f'permalink: {yaml_str(base + slug + "/")}',
                  f'alt_url: {yaml_str(other + slug + "/")}',
                  # no excerpt: Jekyll would cut one inside the {% raw %} block
                  'excerpt_separator: ""',
                  '---']
            with open(os.path.join(SITE, folder, slug + '.md'), 'w',
                      encoding='utf-8', newline='\n') as f:
                f.write('\n'.join(fm) + '\n' + '\n'.join(body) + '\n')

    # A work kept off the site (visible: false) is listed all the same, with a
    # page that holds only a detailed summary of its contents and none of its
    # text (the editor, 2026-10-21: "For each literary source that you don't
    # publish on the site, include an entry with a detailed summary of its
    # contents"). A kept-off work without its summary in both languages stops
    # the build.
    for w in works:
        if w.get('visible'):
            continue
        slug = w['slug']
        if not (w.get('summary_en') and w.get('summary_de')):
            raise SystemExit(f'{slug}: kept off the site but has no summary_en and '
                             'summary_de in its work.yml')
        listing_row = {k: w.get(k, '') for k in (
            'slug', 'kind', 'parent', 'title', 'title_en', 'cite', 'author',
            'author_sort', 'published', 'year', 'language', 'english_by', 'scan',
            'note_en', 'note_de', 'account_en', 'account_de')}
        if not listing_row['parent']:       # Liquid reads "" as true
            del listing_row['parent']
        listing.append(listing_row | {'pages': 0, 'summary_only': True})
        for lang, (folder, base, other) in BASES.items():
            body = ['{% raw %}', '<div class="lit-summary" markdown="1">', '',
                    w['summary_' + lang].strip(), '', '</div>', '{% endraw %}']
            fm = ['---',
                  f'work: {yaml_str(slug)}',
                  f'title: {yaml_str(w["cite"])}',
                  f'lang: {lang}',
                  f'permalink: {yaml_str(base + slug + "/")}',
                  f'alt_url: {yaml_str(other + slug + "/")}',
                  'excerpt_separator: ""',
                  '---']
            with open(os.path.join(SITE, folder, slug + '.md'), 'w',
                      encoding='utf-8', newline='\n') as f:
                f.write('\n'.join(fm) + '\n' + '\n'.join(body) + '\n')
    listing.sort(key=sort_key)

    with open(os.path.join(SITE, '_data', 'literature.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by pipeline/literature/literature_site.py from\n'
                '# literature/<slug>/work.yml. A work kept off the site is listed\n'
                '# with summary_only: true; its page holds only its summary.\n')
        yaml.safe_dump(listing, f, allow_unicode=True, sort_keys=False, width=1000)

    # The "In the literature" entry beside each linked document (letter.html):
    # each link's sentence, then its passages by work, with their labels.
    by_slug = {w['slug']: w for w in works}
    per_doc = {}
    for ln in links:
        ws = []
        for pk in ln['passages']:
            slug, _, key = pk.partition('/')
            w = by_slug[slug]
            if not ws or ws[-1]['work'] != slug:
                ws.append({'work': slug, 'cite': w['cite'], 'pages': []})
            p = next(p for p in w['passages'] if p['key'] == key)
            ws[-1]['pages'].append({'key': key, 'en': label(p, strings['en']),
                                    'de': label(p, strings['de'])})
        for r in ln['docs']:
            per_doc.setdefault(r['uid'], []).append(
                {'id': ln['id'], 'en': ln['en'], 'de': ln['de'],
                 'works': json.loads(json.dumps(ws))})   # a copy: no YAML aliases
    with open(os.path.join(SITE, '_data', 'literature_links.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by pipeline/literature/literature_site.py from\n'
                '# literature/links.yml: the passages tied by hand to each document.\n')
        yaml.safe_dump(per_doc, f, allow_unicode=True, sort_keys=True, width=1000)
    print(f'{len(links)} hand-made links: {len(at)} passages, {len(per_doc)} documents')
    print(f'wrote {len(shown)} works to site/_literature/ and site/_literature_de/'
          + (f"; summary only: {', '.join(hidden)}" if hidden else ''))


if __name__ == '__main__':
    main()
