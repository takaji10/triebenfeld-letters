# -*- coding: utf-8 -*-
"""
The literature on the website: a list of the works and a page for each.

Reads  : dataset/literature/index.json and the passage files beside it
         (made by build_literature.py), site/_data/i18n.yml (the labels),
         literature/links.yml (the hand-made links), dataset/letters.json and
         units/<slug>/unit.yml (the linked documents)
Writes : site/_data/literature.yml         the visible works, for the list page
         site/_data/literature_links.yml   the links, by document (letter.html)
         site/_literature/<slug>.md        /literature/<slug>/
         site/_literature_de/<slug>.md     /de/literatur/<slug>/

A passage named in literature/links.yml gets an entry in the "Related"
column beside it, with the passage's own note (`about:` in the link, or the
link's sentence where the link names one passage) and the documents that
belong to it there; the document's page shows the link's sentence and the
passages where that document belongs, "In the literature". The script stops
on a link to a passage or a document that does not exist, or to a work not
shown, and on a link whose per-passage notes do not cover it.

A work with `visible: false` (Seidel, Pinkas Hakehillot: under copyright,
docs/LITERATURE_PLAN.md section 4) has none of its text on the site. It is
listed, and its page holds only the detailed summary of its contents from its
work.yml (`summary_en`, `summary_de`; the editor, 2026-10-21). pipeline/verify_site.py
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

Each page gives the work passage by passage (a passage is a printed page),
as one continuous read in a book-width column (the editor's "reading column
with a contents panel", 2026-11-24): the printed page number is a marker in
the left margin (`.pg`, id "p41", the same marker the newspapers use), a
contents panel stands at the left (the work's headings, else its page ranges,
and a "Go to page" box), and each passage holds both texts, the original and
the English: side by side from 80rem, one at a time (the English first) on a
narrower screen, by the buttons of _layouts/literature.html
(site/assets/literature.js). The text is the passage file's, rendered as
Markdown by Jekyll. Only the rendering
is changed, never the words: footnote markers [^n] become links to their notes
(kramdown's own footnotes would clash between the two texts), headings are
set one level down under the page's own, and the four-space indent of a
note's second paragraph is taken off so that it is not shown as code, a "|"
outside a table is escaped (kramdown would make the line a table), and a line
break inside a paragraph is kept as a break. There is no index of pages (the
editor, 2026-11-24: "this is useless"); the contents panel replaces it.

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
CORPUS = os.path.join(ROOT, 'dataset', 'literature')
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
    t = HEADING.sub(lambda m: '#' * min(6, len(m.group(1)) + 1), t)
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


def marker(p, s, used):
    """The passage's page mark for the margin (assets/style.css, .pg), or None
    for a passage that is a section with its own heading (a Minakowska
    section, a regest, the notes). The mark is the printed page (a link,
    id "p41"), "front" for the matter before page 1, "after p. 12" for a
    page without a number. Ids are unique over the work: a part's pages carry
    the part's number ("p2-IV")."""
    key = p['key']
    if key == 'notes' or p.get('title'):
        return None
    if key.endswith('front'):
        return f'<div class="pg"><a href="#p-{key}">{s["lit_front_short"]}</a></div>'
    m = re.search(r'(\w+)-u(\d+)$', key)
    if m:
        return f'<div class="pg"><a href="#p-{key}">{html.escape(s["lit_after"].replace("%s", m.group(1)))}</a></div>'
    page = str(p['page'])
    pid = f'p{p["part"]}-{page}' if p['part'] else f'p{page}'
    if pid in used:
        pid += f'-{key}'
    used.add(pid)
    return (f'<div class="pg" id="{pid}"><a href="#{pid}">'
            f'{html.escape(s["lit_page"].replace("%s", page))}</a></div>')


MDHEAD = re.compile(r'^(#{1,6})[ \t]+(.*?)\s*$', re.M)


def clean_heading(t):
    """A heading's words as plain text for the contents panel."""
    t = IAL.sub('', t)
    t = re.sub(r'\[\^[^\]\s]+\]', '', t)
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'[*_\\]', '', t)
    return re.sub(r'\s+', ' ', t).strip()


def headings(text):
    return [(len(m.group(1)), clean_heading(m.group(2))) for m in MDHEAD.finditer(text or '')
            if clean_heading(m.group(2))]


def toc_entries(w, ps, raw, orig):
    """The contents panel's entries from the headings of the text, or [] where
    the work has fewer than two: (passage key, level, English, original)."""
    ent = []
    for i, p in enumerate(ps):
        he = headings(raw['en'][i]) if raw.get('en') else []
        ho = headings(raw[orig][i]) if orig != 'en' and raw.get(orig) else []
        if orig == 'en':
            rows = [(l, t, None) for l, t in he]
        elif len(he) == len(ho):
            rows = [(l, e, o) for (l, e), (_, o) in zip(he, ho)]
        else:
            rows = [(l, t, None) for l, t in (he or ho)]
        for l, e, o in rows:
            if ent and ent[-1][0] == p['key'] and ent[-1][2] == e:
                continue                      # a running head repeated on the page
            ent.append((p['key'], l, e, o))
    # the original's first-level heading of the work's own title page etc. is
    # kept; shorten very long lists to the upper levels
    while len(ent) > 120 and max(e[1] for e in ent) > min(e[1] for e in ent):
        top = max(e[1] for e in ent)
        ent = [e for e in ent if e[1] < top]
    return ent if len(ent) >= 2 else []


def toc_ranges(ps, s):
    """No headings: the printed pages in groups ("pp. 1-30"), each a link to
    the first page of the group."""
    pages = [(p['key'], str(p['page'])) for p in ps if p['page'] and p['key'] != 'notes']
    if len(pages) < 2:
        return []
    g = max(5, -(-len(pages) // 12))
    g = -(-g // 5) * 5
    out = []
    for k in range(0, len(pages), g):
        grp = pages[k:k + g]
        a, b = grp[0][1], grp[-1][1]
        out.append((grp[0][0], s['lit_toc_range'].replace('%s', a, 1).replace('%s', b, 1)
                    if a != b else s['lit_page'].replace('%s', a)))
    return out


def toc_html(w, ps, raw, orig, s):
    """The contents panel: the work's headings (the English, and the
    original's where its headings pair with them), else the page ranges; a
    "Go to page" box when the work has printed pages."""
    ent = toc_entries(w, ps, raw, orig)
    pageof = {p['key']: (str(p['page']) if p['page'] else '') for p in ps}
    out = ['<details class="lit-toc" open>',
           f'<summary>{html.escape(s["lit_contents"])}</summary>',
           '<div class="lit-toc-body">']
    if any(p['page'] for p in ps):
        out.append(f'<form class="lit-goto" action="#" data-none="{html.escape(s["lit_goto_none"])}">'
                   f'<label for="lit-goto-in">{html.escape(s["lit_goto"])}</label>'
                   '<input id="lit-goto-in" type="text" inputmode="text" autocomplete="off" '
                   'spellcheck="false" size="6">'
                   f'<button type="submit">{html.escape(s["lit_goto_go"])}</button>'
                   '<span class="lit-goto-msg" role="status"></span></form>')
    out.append('<ol>')
    if ent:
        lo = min(e[1] for e in ent)
        for key, lvl, en, o in ent:
            rel = min(lvl - lo, 2) + 1
            txt = f'<span class="toc-e">{html.escape(en)}</span>'
            if o and o != en:
                txt += f'<span class="toc-o" lang="{orig}">{html.escape(o)}</span>'
            elif o:
                txt = f'<span>{html.escape(en)}</span>'
            pg = pageof.get(key)
            pgs = (f' <span class="toc-p">{html.escape(s["lit_page"].replace("%s", pg))}</span>'
                   if pg else '')
            out.append(f'<li class="l{rel}"><a href="#p-{key}">{txt}{pgs}</a></li>')
    else:
        for key, lab in toc_ranges(ps, s):
            out.append(f'<li class="l1"><a href="#p-{key}">{html.escape(lab)}</a></li>')
    out += ['</ol>', '</div>', '</details>']
    return out


def yaml_str(v):
    return json.dumps(v, ensure_ascii=False)


def card_extra(w):
    """The card's additions to the list row: the work's brief (written into
    its work.yml, the long account staying on the work's page), the card's
    shorter published line (`published_card`, the original imprint only, the
    full line staying on the work's page; 2026-11-01) and the thumb
    of its first imaged page - written only when make_thumbs.py has put the
    file here, so the card shows no image the site does not carry. Null for
    absent: Liquid reads "" as true."""
    thumb = (f'/assets/thumbs/lit-{w["slug"]}.jpg'
             if os.path.isfile(os.path.join(SITE, 'assets', 'thumbs',
                                            f'lit-{w["slug"]}.jpg'))
             else None)
    return {'brief_en': w.get('brief_en') or None,
            'brief_de': w.get('brief_de') or None,
            'published_card': w.get('published_card') or None,
            'title_card': w.get('title_card') or None,
            'title_en_card': w.get('title_en_card') or None,
            'thumb': thumb}


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
    dataset/letters.json, with their holding's `ref`) and `notes` (the
    per-passage remarks: `about:` entries, or the link's own sentence where
    the link names one passage). Stops on a passage or a document that does
    not exist, on a passage of a work not shown, and on an `about:` that does
    not cover every passage of a link with several passages.

    A link that names more than one passage of one work would otherwise stamp
    the same box under each of them, so every such passage needs its own
    `about:` note and its own documents (`documents:`, a subset of the link's;
    left out, the link's documents stand). Every document of the link must
    belong to at least one passage: a document named by no passage has no
    place in the link."""
    path = os.path.join(ROOT, 'literature', 'links.yml')
    if not os.path.isfile(path):
        return []
    with open(path, encoding='utf-8') as f:
        links = yaml.safe_load(f) or []
    with open(os.path.join(ROOT, 'dataset', 'letters.json'), encoding='utf-8') as f:
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
        # the per-passage remarks: notes[pk] = the passage's own note
        # (en, de) and the documents that belong to it there
        about = ln.get('about') or {}
        pks = set(ln['passages'])
        for k, v in about.items():
            if k not in pks:
                errors.append(f"{ln['id']}: about {k} is not a passage of the link")
                continue
            for f in ('en', 'de'):
                if not v.get(f):
                    errors.append(f"{ln['id']}: about {k} has no {f}")
            sub = v.get('documents')
            if sub is not None and not sub:
                errors.append(f"{ln['id']}: about {k} names no document")
            for uid in sub or []:
                if uid not in ln['documents']:
                    errors.append(f"{ln['id']}: about {k}: {uid} is not among the link's documents")
        many = len(ln['passages']) > 1
        missing = [pk for pk in ln['passages'] if pk not in about]
        if many and missing:
            errors.append(f"{ln['id']}: names {len(ln['passages'])} passages, "
                          f"no about for {', '.join(missing)}")
        if about and not many:
            # a single passage needs no about; the link's own sentence is its note
            errors.append(f"{ln['id']}: names one passage; drop the about, the sentence is the note")
        ln['notes'] = {}
        for pk in ln['passages']:
            a = about.get(pk) or {'en': ln['en'], 'de': ln['de']}
            ln['notes'][pk] = {'en': a['en'], 'de': a['de'],
                               'documents': a.get('documents') or ln['documents']}
        # every document must belong to at least one passage
        if ln.get('documents'):
            orphans = [u for u in ln['documents']
                       if not any(u in n['documents'] for n in ln['notes'].values())]
            if orphans:
                errors.append(f"{ln['id']}: {', '.join(orphans)} belongs to no passage of the link")
    if errors:
        sys.exit('literature/links.yml:\n  ' + '\n  '.join(errors))
    return links


def links_box(lns, pk, s, lang):
    """The "Related" column entry for one passage: each link's own note for
    the passage (`about:`, or the link's sentence where it names one passage)
    and the documents that belong to it there.

    Outside the {% raw %} block of the page, for relative_url."""
    out = ['{% endraw %}<aside class="lit-related">',
           f'<p class="lit-related-head">{s["lit_related"]}</p>']
    for ln in lns:
        nt = ln['notes'][pk]
        out.append(f'<p>{html.escape(nt[lang], quote=False)}</p>')
        uids = set(nt['documents'])
        out.append('<p class="lit-related-docs">' + ''.join(
            f'<a href="{{{{ \'{r["permalink"]}\' | relative_url }}}}">'
            + html.escape(s['lit_doc'].replace('%s', r['ref'], 1).replace('%s', str(r['letter_id']), 1))
            + f' ({doc_date(r, lang)})</a>'
            for r in ln['docs'] if r['uid'] in uids) + '</p>')
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
        texts, raws = {}, {}
        for lg in langs:
            raws[lg] = [passage_text(slug, p['key'], lg) for p in ps]
            texts[lg], missing = footnotes(raws[lg], lg)
            if missing:
                print(f'{slug} ({lg}): {missing} note markers with no note, left as they stand')
        listing_row = {k: w.get(k, '') for k in (
            'slug', 'kind', 'parent', 'title', 'title_en', 'cite', 'author',
            'author_sort', 'published', 'year', 'language', 'english_by', 'scan',
            'note_en', 'note_de', 'account_en', 'account_de')}
        if not listing_row['parent']:       # Liquid reads "" as true
            del listing_row['parent']
        # the number of passages with a Related entry, for the toggle button
        n_related = sum(1 for p in ps if f"{slug}/{p['key']}" in at)
        if n_related:
            listing_row['related'] = n_related
        listing.append(listing_row | card_extra(w)
                       | {'pages': sum(1 for p in ps if p['page'])})
        for lang, (folder, base, other) in BASES.items():
            s = strings[lang]
            body = ['{% raw %}', '<div class="lit-reader">']
            body += toc_html(w, ps, raws, orig, s)
            body.append('<div class="lit-text">')
            used, last_part = set(), None
            for i, p in enumerate(ps):
                pk = p['key']
                lns = at.get(f'{slug}/{pk}', [])
                if p['part'] and p['part'] != last_part:
                    body.append(f'<h2 class="lit-sec" id="part-{p["part"]}">'
                                + html.escape(s['lit_part'].replace('%d', str(p['part']))) + '</h2>')
                last_part = p['part']
                body += ['', f'<section class="lit-passage'
                             f'{" has-related" if lns else ""}" id="p-{pk}"'
                             + (f' data-page="{html.escape(str(p["page"]))}"' if p['page'] else '')
                             + (f' data-part="{p["part"]}"' if p['part'] else '') + '>']
                mk = marker(p, s, used)
                if mk:
                    body.append(mk)
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
                        head = p.get('title') or (s['lit_notes'] if pk == 'notes' else None)
                        if head and not MDHEAD.match(t.lstrip()):
                            t = f'# {head}\n\n{t}'
                        body += [f'<div class="{cls}" lang="{lg}" markdown="1">', '',
                                 render(t), '', '</div>']
                if lns:
                    body += links_box(lns, f'{slug}/{pk}', s, lang)
                body.append('</section>')
            body += ['</div>', '</div>', '{% endraw %}']
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
        listing.append(listing_row | card_extra(w)
                       | {'pages': 0, 'summary_only': True})
        for lang, (folder, base, other) in BASES.items():
            body = ['{% raw %}', '<div class="lit-reader lit-reader--solo"><div class="lit-text">',
                    '<div class="lit-summary" markdown="1">', '',
                    w['summary_' + lang].strip(), '', '</div>', '</div></div>', '{% endraw %}']
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
    # each link's sentence, then the passages where that document belongs
    # (its passage's `about:` may name fewer), by work, with their labels.
    by_slug = {w['slug']: w for w in works}
    per_doc = {}
    for ln in links:
        for r in ln['docs']:
            uid = r['uid']
            ws = []
            for pk in ln['passages']:
                if uid not in ln['notes'][pk]['documents']:
                    continue
                slug, _, key = pk.partition('/')
                w = by_slug[slug]
                if not ws or ws[-1]['work'] != slug:
                    ws.append({'work': slug, 'cite': w['cite'], 'pages': []})
                p = next(p for p in w['passages'] if p['key'] == key)
                ws[-1]['pages'].append({'key': key, 'en': label(p, strings['en']),
                                        'de': label(p, strings['de'])})
            if not ws:                  # cannot happen: the build checks it
                continue
            per_doc.setdefault(uid, []).append(
                {'id': ln['id'], 'en': ln['en'], 'de': ln['de'],
                 'works': ws})
    with open(os.path.join(SITE, '_data', 'literature_links.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by pipeline/literature/literature_site.py from\n'
                '# literature/links.yml: the passages tied by hand to each document.\n')
        yaml.safe_dump(per_doc, f, allow_unicode=True, sort_keys=True, width=1000)
    print(f'{len(links)} hand-made links: {sum(len(v) for v in at.values())} passage entries,'
          f' {len(per_doc)} documents')
    print(f'wrote {len(shown)} works to site/_literature/ and site/_literature_de/'
          + (f"; summary only: {', '.join(hidden)}" if hidden else ''))


if __name__ == '__main__':
    main()
