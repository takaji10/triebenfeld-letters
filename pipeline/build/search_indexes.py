# -*- coding: utf-8 -*-
"""
The search indexes of the one search bar (assets/browse.js; the editor,
2026-11-24; docs/SITE_OVERHAUL_PLAN.md, Phase 2).

Reads  : site/assets/search-index.json        the documents (build_site_data.py)
         site/_data/translations/*.yml        the documents' English
         site/_data/newspapers.yml, newspapers/<slug>/original.md, english.md,
                                              item.yml
         site/_data/literature.yml, dataset/literature/index.json and the
                                              passages beside it (build_literature.py)
         site/_data/literature_mentions.yml, newspapers_mentions.yml
         site/_data/maps.yml, maps_list.yml   (map_pages.py)
         site/_data/people.yml, places_named.yml, units.yml, eras.yml, stats.yml
Writes : site/assets/search-newspapers.json   one row per item of the press
         site/assets/search-literature.json   one row per printed page / passage
         site/assets/search-maps.json         one row per map (titles, legend, texts)
         site/assets/search-<kind>-en.json    {id: English text}, loaded only
         site/assets/search-documents-en.json when a reader searches the English
         site/assets/search-facets.json       names of people and places, holdings
                                              and the places each document names
         site/_data/stats.yml                 year_min / year_max: the earliest and
                                              latest year of documents, newspapers,
                                              literature and maps (the year range
                                              selector's limits; pipeline/verify_site.py
                                              holds the built limits to the data)

Run AFTER build_site_data.py, literature_site.py, newspapers_site.py and
map_pages.py (regenerate.py does), and after any change to the literature's,
newspapers' or maps' texts:  python3 pipeline/build/search_indexes.py

A work of the literature kept off the site (`summary_only`) has no passages
here, only a row for its summary: pipeline/verify_site.py's leak check holds.
The anchor of a passage on its work's page is ANCHOR below ("p-<key>" today).
"""
import io, os, re, sys, json, html
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'pipeline'))

SITE = os.path.join(ROOT, 'site')
DATA = os.path.join(SITE, '_data')
ASSETS = os.path.join(SITE, 'assets')
LIT = os.path.join(ROOT, 'dataset', 'literature')
NEWS = os.path.join(ROOT, 'newspapers')

# The id of a passage on its work's page: what browse.js appends to the link.
ANCHOR = 'p-{key}'


def yload(path):
    with open(os.path.join(DATA, path), encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def dump(name, obj):
    p = os.path.join(ASSETS, name)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
    kb = os.path.getsize(p) / 1024
    print(f'wrote {name} ({kb:.0f} KB, {len(obj)} entries)')


def squeeze(s):
    return re.sub(r'[ \t]+', ' ', re.sub(r'\n{3,}', '\n\n', s or '')).strip()


def strip_tags(s):
    """Markup out of a text (a table's cells, an italic), entities decoded."""
    s = re.sub(r'</(td|th|tr|p|li|div)>', ' ', s)
    return html.unescape(re.sub(r'<[^>]+>', '', s))


def body_of(path):
    """A newspaper file's text without its leading comment header."""
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    i = 0
    while i < len(lines) and (lines[i].startswith('#') or lines[i].strip() == ''):
        if lines[i].strip() == '':
            i += 1
            break
        i += 1
    return '\n'.join(lines[i:]).strip('\n')


FN = re.compile(r'\[\^[^\]\s]+\]:?')
IAL = re.compile(r'[ \t]*\{#[^}]*\}[ \t]*$', re.M)
HEAD = re.compile(r'^#{1,6}\s+', re.M)


def lit_text(slug, key, lang):
    path = os.path.join(LIT, slug, f'{key}.{lang}.txt')
    if not os.path.isfile(path):
        return ''
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    t = '\n'.join(lines[4:]) if len(lines) > 4 and lines[3] == '' else '\n'.join(lines)
    t = IAL.sub('', HEAD.sub('', FN.sub('', t)))
    return squeeze(strip_tags(t.replace('*', '')))


def i18n(lang):
    return yload('i18n.yml')[lang]


def lit_label(p, s):
    if p['key'] == 'notes':
        return s['lit_notes']
    if p.get('title'):
        return p['title']
    part = s['lit_part'].replace('%d', str(p['part'])) + ', ' if p.get('part') else ''
    if p['key'].endswith('front'):
        t = part + s['lit_front']
        return t[:1].upper() + t[1:]
    m = re.search(r'(\w+)-u(\d+)$', p['key'])
    if m:
        return part + s['lit_unnumbered'].replace('%s', m.group(1))
    return part + s['lit_page'].replace('%s', str(p['page']))


def mention_map(path, work_key):
    """{(work or item slug, passage key): {'people': [...], 'pl': [...]}}"""
    d = yload(path)
    out = {}
    for kind, field in (('person', 'people'), ('place', 'pl')):
        for who, rows in (d.get(kind) or {}).items():
            for r in rows:
                for pg in r.get('pages') or []:
                    out.setdefault((r[work_key], str(pg['key'])), {'people': [], 'pl': []})[field].append(who)
    return out


def main():
    en_i, de_i = i18n('en'), i18n('de')
    docs = json.load(open(os.path.join(ASSETS, 'search-index.json'), encoding='utf-8'))
    eras = yload('eras.yml')
    years = []

    # ---- documents' English ------------------------------------------------
    en_docs = {}
    for r in docs:
        p = os.path.join(DATA, 'translations', r['pad'] + '.yml')
        if not os.path.isfile(p):
            continue
        with open(p, encoding='utf-8') as f:
            t = yaml.safe_load(f) or {}
        segs = [strip_tags(str(s.get('en') or '')) for s in t.get('segments') or []]
        txt = squeeze('\n\n'.join(x for x in segs if x.strip()))
        if txt:
            en_docs[r['uid']] = txt
        if r.get('year'):
            years.append(int(r['year']))
    dump('search-documents-en.json', en_docs)

    # ---- newspapers --------------------------------------------------------
    nm = mention_map('newspapers_mentions.yml', 'slug')
    rows, en = [], {}
    for it in yload('newspapers.yml'):
        slug = it['slug']
        d = os.path.join(NEWS, slug)
        with open(os.path.join(d, 'item.yml'), encoding='utf-8') as f:
            meta = yaml.safe_load(f)
        only = bool(it.get('summary_only'))
        orig = '' if only else squeeze(strip_tags(body_of(os.path.join(d, 'original.md'))))
        eng = '' if only else squeeze(strip_tags(body_of(os.path.join(d, 'english.md'))))
        m = nm.get((slug, 'item'), {'people': [], 'pl': []})
        rows.append({
            'id': slug, 'title': it['title_en'] or it.get('title') or slug,
            'title_de': it['title_de'] or it['title_en'], 'orig_title': it.get('title') or '',
            'cite': it['newspaper'], 'year': str(it['year']), 'date': str(it['year']),
            'label': it['date_en'], 'label_de': it['date_de'],
            'az': it['title_en'], 'text': orig,
            'summary': ' '.join(filter(None, [it.get('account_en'), it.get('brief_en')])),
            'summary_de': ' '.join(filter(None, [it.get('account_de'), it.get('brief_de')])),
            'people': sorted(set(m['people'])), 'pl': sorted(set(m['pl'])),
            'era': meta.get('era') or '', 'n': 0,
        })
        if eng:
            en[slug] = eng
        years.append(int(it['year']))
    dump('search-newspapers.json', rows)
    dump('search-newspapers-en.json', en)

    # ---- literature --------------------------------------------------------
    lm = mention_map('literature_mentions.yml', 'work')
    works = {w['slug']: w for w in yload('literature.yml')}
    idx = json.load(open(os.path.join(LIT, 'index.json'), encoding='utf-8'))
    rows, en = [], {}
    for w in idx:
        slug = w['slug']
        meta = works.get(slug)
        if not meta:
            continue
        years.append(int(meta['year']))
        base = {'slug': slug, 'cite': meta['cite'], 'title': meta.get('title_card') or meta['title'],
                'title_en': meta.get('title_en_card') or meta.get('title_en') or meta['title'],
                'year': str(meta['year']), 'date': str(meta['year']),
                'az': meta.get('author_sort') or meta['title']}
        if meta.get('summary_only'):
            rows.append(base | {'id': slug, 'text': '', 'n': 0, 'label': '', 'label_de': '',
                                'summary': meta.get('account_en') or '', 'summary_de': meta.get('account_de') or '',
                                'people': [], 'pl': [], 'only': 1})
            continue
        orig_lang = w['language']
        for n, p in enumerate(w['passages']):
            key = p['key']
            orig = lit_text(slug, key, orig_lang) if orig_lang != 'en' else ''
            eng = lit_text(slug, key, 'en')
            if orig_lang == 'en':
                orig = eng
            if not (orig or eng):
                continue
            m = lm.get((slug, key), {'people': [], 'pl': []})
            row = base | {
                'id': f'{slug}/{key}', 'a': ANCHOR.format(key=key), 'n': n,
                'label': lit_label(p, en_i), 'label_de': lit_label(p, de_i),
                'text': orig, 'summary': '', 'summary_de': '',
                'people': sorted(set(m['people'])), 'pl': sorted(set(m['pl'])),
            }
            rows.append(row)
            if eng and orig_lang != 'en':
                en[row['id']] = eng
    dump('search-literature.json', rows)
    dump('search-literature-en.json', en)

    # ---- maps --------------------------------------------------------------
    maps_full = yload('maps.yml')
    rows, en = [], {}

    def strings(o, keys, out):
        """Every string under the given keys, anywhere in o."""
        if isinstance(o, dict):
            for k, v in o.items():
                if k in keys and isinstance(v, str):
                    out.append(v)
                elif k in keys and isinstance(v, list):
                    out.extend(x for x in v if isinstance(x, str))
                else:
                    strings(v, keys, out)
        elif isinstance(o, list):
            for x in o:
                strings(x, keys, out)

    for m in yload('maps_list.yml'):
        slug = m['slug']
        full = maps_full.get(slug) or {}
        legend = full.get('legend') or {}
        texts = full.get('texts') or []
        orig, eng, deu = [], [], []
        orig.append(m['title'] or '')
        eng += [m.get('title_en') or '', m.get('kind_en') or '']
        deu += [m.get('title_de') or '', m.get('kind_de') or '']
        # the sheet's own words: legend and texts (orig / pl / ru), English, German
        lo, le, ld = [], [], []
        strings(legend, {'orig', 'pl'}, lo); strings(legend, {'en'}, le); strings(legend, {'de'}, ld)
        strings(texts, {'lines', 'orig'}, orig)
        strings(texts, {'en'}, eng); strings(texts, {'de'}, deu)
        orig += lo; eng += le; deu += ld
        place_slugs, forms = set(), []
        for lb in full.get('labels') or []:
            if lb.get('place'):
                place_slugs.add(lb['place'])
            for k in ('form', 'name'):
                if lb.get(k):
                    forms.append(lb[k])
        orig += forms
        desc = ' · '.join(x for x in (m.get('maker'), m.get('holder'), m.get('reference')) if x)
        rows.append({
            'id': slug, 'title': m['cited_as'], 'title_en': m.get('title_en') or m['cited_as'],
            'orig_title': m['title'], 'year': str(m['year']), 'date': str(m['year']),
            'label': str(m['year']), 'label_de': str(m['year']), 'az': m['cited_as'],
            'text': squeeze('\n'.join(x for x in orig if x)),
            'summary': squeeze(' · '.join(x for x in (m.get('title_en'), m.get('kind_en'), desc) if x)),
            'summary_de': squeeze(' · '.join(x for x in (m.get('title_de') or m.get('title_en'), m.get('kind_de'), desc) if x)),
            'people': [], 'pl': sorted(place_slugs), 'era': '', 'n': 0,
        })
        e = squeeze('\n'.join(x for x in eng if x))
        if e:
            en[slug] = e
        years.append(int(m['year']))
    dump('search-maps.json', rows)
    dump('search-maps-en.json', en)

    # ---- facets ------------------------------------------------------------
    people = {p['slug']: [p['heading'], p.get('heading_de') or p['heading']] for p in yload('people.yml')}
    named = yload('places_named.yml')
    places = {p['slug']: p['name'] for p in named}
    docplaces = {}
    for p in named:
        for l in p.get('letters') or []:
            docplaces.setdefault(l['uid'], []).append(p['slug'])
    units = {u['slug']: {'ref': u['ref'], 'archive': u['archive'], 'types': u.get('types') or [],
                         'lit': u.get('listed_in') == 'literature'} for u in yload('units.yml')}
    eras_f = [{'slug': e['slug'], 'first': int(e['first']) if e.get('first') else None,
               'last': int(e['last']) if e.get('last') else None} for e in eras]
    dump('search-facets.json', {'people': people, 'places': places, 'docplaces': docplaces,
                                'units': units, 'eras': eras_f})

    # ---- year limits -> stats.yml -----------------------------------------
    lo, hi = min(years), max(years)
    sp = os.path.join(DATA, 'stats.yml')
    with open(sp, encoding='utf-8') as f:
        lines = [l for l in f.read().split('\n') if not l.startswith(('year_min:', 'year_max:'))]
    out = []
    for l in lines:
        out.append(l)
        if l.startswith('last_year:'):
            out += [f'year_min: {lo}', f'year_max: {hi}']
    with open(sp, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out))
    print(f'year range {lo}-{hi} written to stats.yml')


if __name__ == '__main__':
    main()
