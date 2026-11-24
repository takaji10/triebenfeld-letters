# -*- coding: utf-8 -*-
"""
The places that have their own page on the website (docs/PLACES_PLAN.md).

Reads  : places/<slug>/place.yml              the authored page of the place
        places/<slug>/<source>/source.yml     one source of the place
        places/<slug>/<source>/original.md    the source as printed
        places/<slug>/<source>/english.md     Claude's English of it
        site/_data/estates.yml                the estates in focus (the build's)
Writes : site/_data/places_pages.yml          the places and their sources
        site/_places/<slug>.md                /places/<slug>/
        site/_places_de/<slug>.md             /de/orte/<slug>/

The place pages are the editor's ruling of 2026-10-22 ("a new source to a
place: Zagórów ... added under the place name, on a separate page for the
place"): a page per place, hung on the place's card on the Places page and
linked from it, bilingual like the person pages, carrying the sources
brought in for the place — each shown whole (the original as printed,
nothing tidied, with Claude's English beside it, the English first by the
literature's buttons, assets/literature.js) with its own facts, account and
caveat, as a newspapers item's page is. The first place is Zagórów
(slug zagorowo), whose first source is the town's own presentation on
zagorow.pl, captured by the Wayback Machine on 14 June 2022.

A source kept off the site (`visible: false`, the rule of the literature,
LITERATURE_PLAN section 4) is listed with summary_only: true and its page
holds only the summary of its contents — summary_en and summary_de are
required, or the build stops.

The slug of a place's page is the place's slug in reference/places.yml, the
same slug its card on the Places page carries; the build fails loudly if it
is neither an estate of the edition nor a place of the gazetteer, so a
misspelt slug cannot make an orphan page (docs/PLACES_PLAN.md, section 7:
the widened index).
Run as a step of pipeline/regenerate.py, after build_site_data.py (the estates) and
beside person_pages.py.

Usage: python pipeline/places/place_pages.py [--quiet]
"""
import io, os, re, sys, json
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLACES = os.path.join(ROOT, 'places')
SITE = os.path.join(ROOT, 'site')
BASES = {'en': ('_places', '/places/', '/de/orte/'),
         'de': ('_places_de', '/de/orte/', '/places/')}

HEADING = re.compile(r'^(#{1,6})(?=\s)', re.M)

# The fields of source.yml the site reads.
SOURCE_FIELDS = ('slug', 'ref', 'title', 'title_en', 'cite', 'site',
                 'original_url', 'captured', 'published', 'year',
                 'date_span', 'language', 'kind', 'era', 'english_by',
                 'source', 'account_en', 'account_de')



# The citations of a place entry (the editor, 2026-11-24): the citation itself
# is the link ("Ibid No. 1363." linked, no "The document."), a second document
# of the same citation follows as "(also)". The links are written through
# relative_url, out of the raw block for the moment, so that they carry the
# live site's prefix (/triebenfeld-letters); a plain /documents/... link inside
# {% raw %} missed it and was broken on the live site. The entries of the
# Słownik geograficzny and Nazwy miejscowe Polski, shown in full since
# 2026-11-24, are linked to their entry on the work's page, found by the
# volume and page in the entry's heading.
_LIT_ENTRY_CACHE = {}


def lit_entry_link(source, locator, name=''):
    if source not in ('slownik', 'nmpol') or not locator:
        return None
    if source not in _LIT_ENTRY_CACHE:
        heads = []
        path = os.path.join(ROOT, 'literature', source, 'original.md')
        if os.path.isfile(path):
            with open(path, encoding='utf-8') as fh:
                heads = [ln for ln in fh if ln.startswith('## ')]
        _LIT_ENTRY_CACHE[source] = heads
    norm = lambda t: re.sub(r'\s+', ' ', t).strip().rstrip('.').lower()
    want = norm(locator)
    hits = []
    for i, h in enumerate(_LIT_ENTRY_CACHE[source], 1):
        m = re.search(r'\[([^\]]*)\]', h)
        if not m:
            continue
        b = norm(m.group(1))
        j = b.find(want)
        if j >= 0 and (b[j + len(want):] == '' or b[j + len(want):].startswith(', sub')):
            hits.append((i, norm(h[3:m.start()])))
    if len(hits) > 1 and name:
        n = norm(name)
        named = [x for x in hits if x[1] and (x[1] in n or n in x[1])]
        hits = named or hits
    if not hits and name:
        # an entry that runs over a page: the same volume and the same name
        vol = re.match(r'(t\. [^,]+),', want)
        n = norm(name)
        for i, h in enumerate(_LIT_ENTRY_CACHE[source], 1):
            m = re.search(r'\[([^\]]*)\]', h)
            if m and vol and vol.group(1) in norm(m.group(1)) and norm(h[3:m.start()]) == n:
                hits.append((i, n))
                break
    return f'/literature/{source}/#p-c{hits[0][0]:02d}' if hits else None


def _liquid_url(link):
    return "{% endraw %}{{ '" + link + "' | relative_url }}{% raw %}"


def footnote_md(f_, name=''):
    text = (f_.get('text') or '').strip()
    links = []
    for r_ in (f_.get('refs') or []):
        if r_.get('status') == 'linked' and r_.get('link'):
            links.append(r_['link'])
        else:
            lk = lit_entry_link(r_.get('source'), r_.get('locator'), name)
            if lk:
                links.append(lk)
    # the citation is the first sentence that carries a number ("Ibid No.
    # 672."); what follows is commentary and stays outside the link
    m = re.match(r'^(.*?\d[^.]*?\.)(\s+[A-ZŁŚŻŹ(].*)?$', text, re.S)
    cite, rest = (m.group(1), m.group(2) or '') if m else (text, '')
    if not cite.endswith('.'):
        cite += '.'
    if not links:
        return cite + rest
    # several documents: each number its own link, when the numbers of the
    # citation ("Nos. 1478, 1490, 1491 & 1519") match the links one for one
    if len(links) > 1:
        tail = re.search(r'Nos?\.\s*(.*)$', cite)
        nums = list(re.finditer(r'\d+', tail.group(1))) if tail else []
        if len(nums) == len(links):
            base = tail.start(1)
            out, pos = cite[:base], base
            for n_, lk in zip(nums, links):
                a, b = base + n_.start(), base + n_.end()
                out += cite[pos:a] + f'[{cite[a:b]}]({_liquid_url(lk)})'
                pos = b
            return out + cite[pos:] + rest
    out = f'[{cite}]({_liquid_url(links[0])})'
    for lk in links[1:]:
        out += f' ([also]({_liquid_url(lk)}))'
    return out + rest

def body_of(path):
    """The file's text: leading comment lines and the blank line after them
    are the file's own header, as in dataset/literature/."""
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    i = 0
    while i < len(lines) and (lines[i].startswith('#') or lines[i].strip() == ''):
        if lines[i].strip() == '':
            i += 1
            break
        i += 1
    text = '\n'.join(lines[i:]).strip('\n')
    assert text, path
    return text


def render(t):
    """Only the rendering is changed, never the words: headings sit two
    levels down under the page's own, a line break inside a paragraph is
    kept (a printed line stays a printed line), a "|" is escaped so kramdown
    does not make a table of the line. As the newspapers' site builder
    renders its items."""
    t = HEADING.sub(lambda m: '#' * min(6, len(m.group(1)) + 2), t)
    lines = t.split('\n')
    for i, line in enumerate(lines):
        if not line.lstrip().startswith('|'):
            line = line.replace('|', '\\|')
        nxt = lines[i + 1] if i + 1 < len(lines) else ''
        if (line.strip() and nxt.strip() and not line.lstrip().startswith('#')
                and not line.endswith(('  ', '\\'))):
            line += '  '
        lines[i] = line
    return '\n'.join(lines)


def yaml_str(v):
    return json.dumps(v, ensure_ascii=False)


def main():
    quiet = '--quiet' in sys.argv
    estates = {e['slug'] for e in (
        yaml.safe_load(io.open(os.path.join(SITE, '_data', 'estates.yml'),
                               encoding='utf-8')) or [])}
    # A place page hangs on the Places page (docs/PLACES_PLAN.md, section 7):
    # on an estate's card, or on the place's item in the page's index of
    # places — a place the gazetteer carries (reference/gazetteer/), the
    # editor's own index of the Trąbczyn/Zagórów area. The slug of a place's
    # page is the gazetteer's slug where the gazetteer has the place, and the
    # register's slug otherwise.
    gazetteer = set()
    _gz = os.path.join(ROOT, 'reference', 'gazetteer')
    for _fn in os.listdir(_gz):
        if not _fn.endswith('.yml'):
            continue
        with open(os.path.join(_gz, _fn), encoding='utf-8') as _gf:
            _g = yaml.safe_load(_gf) or {}
        gazetteer.add(_g.get('slug') or _fn[:-4])

    places = []
    named = {}
    np = os.path.join(SITE, '_data', 'places_named.yml')
    if os.path.isfile(np):
        with open(np, encoding='utf-8') as f:
            for row in (yaml.safe_load(f) or []):
                named[row['slug']] = row
    # the stubs' coordinates (reference/place_coords.yml): the places without
    # a gazetteer entry, geocoded where the identification is sure
    stub_coords = {}
    pc = os.path.join(ROOT, 'reference', 'place_coords.yml')
    if os.path.isfile(pc):
        with open(pc, encoding='utf-8') as f:
            stub_coords = yaml.safe_load(f) or {}
    for slug in sorted(os.listdir(PLACES)):
        d = os.path.join(PLACES, slug)
        if not os.path.isdir(d):
            continue
        where = f'places/{slug}/place.yml'
        with open(os.path.join(d, 'place.yml'), encoding='utf-8') as f:
            pl = yaml.safe_load(f)
        if pl.get('slug') != slug:
            raise SystemExit(f'{where}: slug {pl.get("slug")!r} does not '
                             f'match the folder {slug!r}')
        if slug not in estates and slug not in gazetteer:
            raise SystemExit(f'{where}: {slug} is neither an estate of the '
                             'edition nor a place of the gazetteer - the '
                             'page hangs on the Places page '
                             '(reference/places.yml, reference/gazetteer/, '
                             'site/_data/estates.yml)')
        for field in ('heading', 'heading_de', 'standfirst_en',
                      'standfirst_de', 'intro_en', 'intro_de'):
            if not pl.get(field):
                raise SystemExit(f'{where}: a place page needs a {field}')

        sources = []
        for src in sorted(os.listdir(d)):
            sd = os.path.join(d, src)
            if not os.path.isdir(sd):
                continue
            swhere = f'places/{slug}/{src}/source.yml'
            with open(os.path.join(sd, 'source.yml'), encoding='utf-8') as f:
                sy = yaml.safe_load(f)
            visible = sy.get('visible', True)
            keep = {k: sy.get(k, '') for k in SOURCE_FIELDS}
            keep['visible'] = visible
            if visible:
                for fn in ('original.md', 'english.md'):
                    if not os.path.isfile(os.path.join(sd, fn)):
                        raise SystemExit(f'{swhere}: a shown source needs {fn}')
            else:
                # Kept off the site: the detailed summary of the contents,
                # in both languages, or the build stops (the literature's
                # rule, LITERATURE_PLAN section 4).
                if not (sy.get('summary_en') and sy.get('summary_de')):
                    raise SystemExit(
                        f'{swhere}: kept off the site but has no summary_en '
                        'and summary_de')
            sources.append(keep | {
                'dir': src,
                'summary_only': not visible,
                'summary_en': sy.get('summary_en', ''),
                'summary_de': sy.get('summary_de', ''),
            })
        if not sources:
            raise SystemExit(f'{where}: a place page needs at least one '
                             'source under its folder')
        places.append(pl | {'sources': sources})

    for lang, (folder, base, other) in BASES.items():
        out_dir = os.path.join(SITE, folder)
        os.makedirs(out_dir, exist_ok=True)
        for fn in os.listdir(out_dir):
            os.remove(os.path.join(out_dir, fn))

    for pl in places:
        slug = pl['slug']
        for lang, (folder, base, other) in BASES.items():
            body = ['{%- comment -%} Generated by '
                    'pipeline/places/place_pages.py - do not hand-edit. '
                    'The urls.html include sets lang and t for the facts '
                    'below: the content is rendered before the layout, so '
                    'the layout\'s assignments are not in scope here. '
                    '{%- endcomment -%}',
                    '{% include urls.html %}']
            for s in pl['sources']:
                sd = os.path.join(PLACES, slug, s['dir'])
                lang_key = 'lit_lang_' + str(s['language'])
                published = s.get('published') or s['date_span']
                # The facts, the account and the caveat stand outside the
                # raw block: the page's labels are the site's i18n (the
                # newspapers' layout carries theirs; here the source is a
                # section of the place's page, and its facts stand with it).
                body += [f'<section class="place-source" id="s-{s["slug"]}">',
                         '',
                         f'<h2>{s["title"]}</h2>',
                         '',
                         '<dl class="source-facts">',
                         f'  <div><dt>{{{{ t.lit_published }}}}</dt>'
                         f'<dd>{published}</dd></div>',
                         f'  <div><dt>{{{{ t.lit_language }}}}</dt>'
                         f'<dd>{{{{ t["{lang_key}"] }}}}</dd></div>',
                         '</dl>',
                         '',
                         '<div class="prose">',
                         f'<p>{s["account_en"] if lang == "en" else s["account_de"]}</p>',
                         '<p class="lit-caveat">{{ t.np_caveat }}</p>',
                         (f'<p><a href="{s["source"]}" rel="noopener">'
                          f'{{{{ t.place_source_link }}}}</a></p>'
                          if s['source'] else '<!-- no source link -->'),
                         '</div>',
                         '',
                         '{% raw %}']
                if s['summary_only']:
                    body += ['<div class="np-summary" markdown="1">', '',
                             s['summary_' + lang].strip(), '', '</div>']
                else:
                    texts = {'en': body_of(os.path.join(sd, 'english.md')),
                             s['language']: body_of(os.path.join(sd, 'original.md'))}
                    for lg, cls in (('en', 'lit-en'), (s['language'], 'lit-orig')):
                        body += [f'<div class="{cls}" lang="{lg}" markdown="1">', '',
                                 render(texts[lg]), '', '</div>']
                body += ['{% endraw %}', '', '</section>', '']
            # the documents that name the place (section 8: every page
            # carries them, the authored pages included)
            hit = named.get(slug) or {}
            # the maps come before the documents (the editor, 2026-11-24)
            body += ['{% include place-maps.html %}', '']
            if hit.get('letters'):
                body += ['<section class="place-docs">',
                         '<h2>{{ t.places_docs_h2 }} ({{ page.hits_docs_count }})</h2>',
                         '',
                         '{% include doc-list.html letters=page.hits_docs '
                         'docs=page.hits_docs_count short=true %}',
                         '</section>', '']
                fm = ['---',
                      'layout: place',
                      f'place: {yaml_str(slug)}',
                      f'title: {yaml_str(pl["heading_de"] if lang == "de" else pl["heading"])}',
                      f'lang: {lang}',
                      f'permalink: {yaml_str(base + slug + "/")}',
                      f'alt_url: {yaml_str(other + slug + "/")}',
                      'excerpt_separator: ""',
                      'maps_in_body: true',
                      f'hits_docs: {yaml_str(hit["letters"])}',
                      f'hits_docs_count: {hit.get("docs") or 0}',
                      '---']
            else:
                fm = ['---',
                      'layout: place',
                      f'place: {yaml_str(slug)}',
                      f'title: {yaml_str(pl["heading_de"] if lang == "de" else pl["heading"])}',
                      f'lang: {lang}',
                      f'permalink: {yaml_str(base + slug + "/")}',
                      f'alt_url: {yaml_str(other + slug + "/")}',
                      'excerpt_separator: ""',
                      'maps_in_body: true',
                      '---']
            with open(os.path.join(SITE, folder, slug + '.md'), 'w',
                      encoding='utf-8', newline='\n') as f:
                f.write('\n'.join(fm) + '\n' + '\n'.join(body) + '\n')

    # ---- the pages of every place (docs/PLACES_PLAN.md, section 8) ----
    # Every place of the index gets its page. An authored place keeps its
    # sources machinery; every other place's page is generated from the
    # gazetteer entry (where one stands), the register and the document
    # mentions - no authored file required.
    idx = yaml.safe_load(io.open(os.path.join(SITE, '_data', 'places_index.yml'),
                                 encoding='utf-8'))
    index_rows = (idx.get('tier1') or []) + (idx.get('tier2') or [])
    authored = {pl['slug'] for pl in places}

    def gz_of(slug):
        p = os.path.join(ROOT, 'reference', 'gazetteer', slug + '.yml')
        if os.path.isfile(p):
            with open(p, encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}

    STAND_EN = ('The place\'s own page: its description in the'
                ' gazetteer, with the sources cited for it, and below, the'
                ' documents that name it.')
    STAND_DE = ('Die eigene Seite des Ortes: seine Beschreibung'
                ' im Gazetteer, mit den für ihn zitierten Quellen, und unten'
                ' die Dokumente, die ihn nennen.')
    auto = []
    REL_RX = re.compile(r'^(?:north|south|east|west|north-|south-|east-|west-'
                        r'|near |between |next |by |along |on the |in the )',
                        re.I)
    for row in index_rows:
        slug = row['slug']
        if slug in authored:
            continue
        g = gz_of(slug)
        head = row.get('name') or slug
        ger = g.get('german') or row.get('german') or ''
        heading = f'{head} ({ger})' if ger and ger.lower() != head.lower() else head
        kind_en, kind_de = row.get('kind_en') or 'Place', row.get('kind_de') or 'Ort'
        loc = g.get('location') or {}
        hit = named.get(slug) or {}
        n_docs = hit.get('docs') or 0
        # The standfirst is the kind and, where the entry says so in a short
        # relative clause, the place's situation (the editor, 2026-10-27:
        # "the line would be the type of place it is, and the approximate
        # location in relation to another place"). A longer location text
        # says what the description already says and is not repeated.
        rel = loc.get('text') or ''
        rel = rel if (rel and REL_RX.match(rel) and len(rel) <= 70) else ''
        ger_de = f', früher {ger} genannt' if ger else ''
        ger_en = f', once named {ger}' if ger else ''
        st = (f'{kind_en} {rel.rstrip(".")}{ger_en}.'.replace('  ', ' ')
              if rel else f'{kind_en}{ger_en}.')
        st_de = f'{kind_de}{ger_de}.'
        auto.append({
            'slug': slug, 'heading': heading,
            'heading_de': heading if ger else (row.get('name_de') or head),
            'standfirst_en': st, 'standfirst_de': st_de,
            'gaz': g, 'kind_en': kind_en, 'kind_de': kind_de,
            'name_de': row.get('name_de') or head,
            'docs': n_docs, 'letters': hit.get('letters') or [],
            'span': hit.get('span') or '',
            'sources': [],
        })

    # the document-hit lists, one hash for the pages' include
    docs_out = {a['slug']: {'docs': a['docs'], 'span': a['span'],
                            'letters': a['letters']} for a in auto}
    with open(os.path.join(SITE, '_data', 'places_docs.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by pipeline/places/place_pages.py from '
                'site/_data/places_named.yml\n'
                '# - do not hand-edit. slug -> the documents that name the '
                'place.\n')
        yaml.safe_dump(docs_out, f, allow_unicode=True,
                       default_flow_style=False, sort_keys=False, width=100)

    for lang, (folder, base, other) in BASES.items():
        for a in auto:
            slug = a['slug']
            g = a['gaz']
            body = ['{%- comment -%} Generated by '
                    'pipeline/places/place_pages.py - do not hand-edit. '
                    '{%- endcomment -%}',
                    '{% include urls.html %}',
                    '',
                    '<section class="place-gaz">',
                    '']
            loc = g.get('location') or {}
            # the header map: Leaflet over OpenStreetMap with a satellite
            # layer (assets/place-map.js), right after the header line that
            # says where the place lies; the link stays for no-script
            lat = lon = None
            if loc.get('lat') and loc.get('lon'):
                lat, lon = loc['lat'], loc['lon']
            elif stub_coords.get(slug):
                sc = stub_coords[slug]
                lat, lon = sc['lat'], sc['lon']
            map_html = []
            if lat:
                map_html = [
                    '<div class="place-map">',
                    f'<div class="place-leaflet" data-lat="{lat}" '
                    f'data-lon="{lon}" data-zoom="13" '
                    f'data-title="{a["heading"]}" data-sat="{{{{ t.map_satellite }}}}" '
                    f'data-street="{{{{ t.map_street }}}}"></div>',
                    f'<p class="refs"><a href="https://www.openstreetmap.org/'
                    f'?mlat={lat}&amp;mlon={lon}#map=15/{lat}/{lon}" '
                    'rel="noopener">{{ t.map_link }}</a></p>',
                    '</div>', '']
            body += map_html
            # the dated forms and the description, one markdown block: the
            # forms' footnote references resolve by the same kramdown
            # numbering as the description's (the editor, 2026-10-27: the
            # superscripts lead somewhere and count from one)
            names = [n for n in (g.get('names') or []) if n.get('form')]
            text_en = (g.get('text_en') or '').strip()
            fns = g.get('footnotes') or []
            if names or text_en or fns:
                body += ['{% raw %}',
                         '<div class="place-desc" lang="en" markdown="1">', '']
                if names:
                    items = []
                    for n in names:
                        y = f' {n["year"]}' if n.get('year') else ''
                        fn = (f' [^{n["footnote"]}]' if n.get('footnote') else '')
                        items.append(f'*{n["form"]}*{y}{fn}')
                    body += ['*Dated forms of the name:* ' + '; '.join(items)
                             + '.', '']
                if text_en:
                    body += [text_en, '']
                for f_ in fns:
                    body.append(f'[^{f_["n"]}]: ' + footnote_md(f_, g.get('heading') or ''))
                    body.append('')
                body += ['</div>', '{% endraw %}', '']
            body += ['</section>', '']
            # the documents that name the place
            # the maps that show the place, above the documents
            body += ['{% include place-maps.html %}', '']
            if a['letters']:
                body += ['<section class="place-docs">',
                         '<h2>{{ t.places_docs_h2 }} ({{ page.hits_docs_count }})</h2>',
                         '',
                         '{% include doc-list.html letters=page.hits_docs '
                         'docs=page.hits_docs_count short=true %}',
                         '</section>', '']
            # kramdown puts the footnotes at the end of the page: the
            # heading is the last thing before them
            if fns:
                body += ['<h2 class="place-cite-h">{{ t.place_citations_h2 }}</h2>', '']
            fm = ['---',
                  'layout: place',
                  f'place: {yaml_str(slug)}',
                  f'title: {yaml_str(a["heading_de"] if lang == "de" else a["heading"])}',
                  f'lang: {lang}',
                  f'permalink: {yaml_str(base + slug + "/")}',
                  f'alt_url: {yaml_str(other + slug + "/")}',
                  'excerpt_separator: ""',
                  'maps_in_body: true',
                  f'hits_docs: {yaml_str(a["letters"])}',
                  f'hits_docs_count: {a["docs"]}',
                  '---', '']
            with open(os.path.join(SITE, folder, slug + '.md'), 'w',
                      encoding='utf-8', newline='\n') as f:
                f.write('\n'.join(fm) + '\n' + '\n'.join(body) + '\n')

    # the site's copy: authored places keep their fields; the generated
    # places carry the heading and the standfirst the layout shows
    for a in auto:
        places.append({k: a[k] for k in (
            'slug', 'heading', 'heading_de', 'standfirst_en', 'standfirst_de',
            'intro_en', 'intro_de') if k in a} | {'sources': []})
    places.sort(key=lambda p: p['slug'])

    out = {}
    for pl in places:
        row = {k: pl.get(k, '') for k in (
            'heading', 'heading_de', 'standfirst_en', 'standfirst_de',
            'intro_en', 'intro_de')}
        out[pl['slug']] = row | {'sources': [
            {k: v for k, v in s.items() if k != 'dir'} for s in pl['sources']]}
    with open(os.path.join(SITE, '_data', 'places_pages.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by pipeline/places/place_pages.py from '
                'places/<slug>/place.yml\n'
                '# and the source folders under them - do not hand-edit.\n'
                '# A source with summary_only: true is kept off the site; '
                'its page holds\n'
                '# only the summary of its contents.\n')
        yaml.safe_dump(out, f, allow_unicode=True, default_flow_style=False,
                       sort_keys=False, width=100)
    if not quiet:
        print(f'wrote {len(places)} place pages to site/_places/ '
              'and site/_places_de/')


if __name__ == '__main__':
    main()
