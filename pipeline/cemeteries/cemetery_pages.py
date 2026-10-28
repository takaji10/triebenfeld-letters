# -*- coding: utf-8 -*-
"""
The cemeteries of the editor's survey on the website (docs/CEMETERIES_PLAN.md).

Reads  : cemeteries/<slug>/cemetery.yml      the facts, the account, the place,
                                             the sources the survey cites
        cemeteries/<slug>/headstones.yml     the headstones, one entry each,
                                             as read (nothing tidied)
        site/_data/places_pages.yml          the places that have their own page
        reference/gazetteer/                 the gazetteer's places (the
                                             Places page's tier-1 anchors)
        reference/places.yml                 the register's places (the same)
Writes : site/_data/cemeteries.yml           the cemeteries, keyed by slug,
                                             for the page layout
        site/_data/cemeteries_list.yml       the list page's order
        site/_cemeteries/<slug>.md           /places/cemeteries/<slug>/
        site/_cemeteries_de/<slug>.md        /de/orte/friedhoefe/<slug>/

The section is the editor's own field record of the ten Evangelical
cemeteries of the Trąbczyn/Zagórów area and its neighbourhood, visited in
2023, each one's condition noted and its headstones read as far as they read
(docs/CEMETERIES_PLAN.md). No person entries stand behind the names; the
table is the record. The readings are kept as the survey has them - the
bracketed letters, the [?] of the unread, the stones' own spellings - nothing
tidied, and the same table stands on both language pages: the names are
readings of German inscriptions, not prose to translate. The asterisked
numbers of the survey are genealogical identifiers for certain
Zelmers/relations and are kept (the editor, 2026-10-26); the survey's figure
references ("Fig. 25") are left out (the editor, the same day).

A cemetery's place is linked three ways, decided here once: the place's own
page where one exists (site/_data/places_pages.yml), otherwise the place's
item on the Places page's index (/places/#place-<slug>), otherwise no link
at all - a place the gazetteer does not carry yet (Orlina Duża, Stawiszyn,
Zbiersk Kolonia) is named without a link until its entry is in.

Run as a step of pipeline/regenerate.py, after place_pages.py (the place pages decide
the first kind of link).

Usage: python pipeline/cemeteries/cemetery_pages.py [--quiet]
"""
import io, os, re, sys, json
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CEM = os.path.join(ROOT, 'cemeteries')
SITE = os.path.join(ROOT, 'site')
# The cemeteries are a subset of Places (the editor, 2026-10-27): their
# pages hang under the Places section, English /places/cemeteries/, German
# /de/orte/friedhoefe/. The addresses they were published at (/cemeteries/,
# /de/friedhoefe/) redirect - the stubs in site/redirects-static/.
BASES = {'en': ('_cemeteries', '/places/cemeteries/', '/de/orte/friedhoefe/'),
         'de': ('_cemeteries_de', '/de/orte/friedhoefe/', '/places/cemeteries/')}
# The Places page's two bases, for the index anchor of a place without a page.
PLACES_BASES = {'en': '/places/', 'de': '/de/orte/'}

CEM_FIELDS = ('slug', 'order', 'title', 'title_de', 'place', 'place_anchor',
              'place_name', 'place_name_de', 'graves', 'visited',
              'account_en', 'account_de', 'sources')


def yaml_str(v):
    return json.dumps(v, ensure_ascii=False)


def main():
    quiet = '--quiet' in sys.argv

    # The places that have their own page (place_pages.py runs first).
    pages = {}
    pp = os.path.join(SITE, '_data', 'places_pages.yml')
    if os.path.isfile(pp):
        with io.open(pp, encoding='utf-8') as f:
            pages = yaml.safe_load(f) or {}

    # The anchors the Places page's index carries: the gazetteer's slugs and
    # the register's, the same set the index was built from.
    anchors = set()
    _gz = os.path.join(ROOT, 'reference', 'gazetteer')
    for _fn in os.listdir(_gz):
        if _fn.endswith('.yml'):
            with io.open(os.path.join(_gz, _fn), encoding='utf-8') as _gf:
                _g = yaml.safe_load(_gf) or {}
            anchors.add(_g.get('slug') or _fn[:-4])
    with io.open(os.path.join(ROOT, 'reference', 'places.yml'),
                 encoding='utf-8') as _pf:
        anchors.update((yaml.safe_load(_pf) or {}).get('places') or {})

    cems = []
    for slug in sorted(os.listdir(CEM)):
        d = os.path.join(CEM, slug)
        if not os.path.isdir(d):
            continue
        where = f'cemeteries/{slug}/cemetery.yml'
        with open(os.path.join(d, 'cemetery.yml'), encoding='utf-8') as f:
            c = yaml.safe_load(f)
        if c.get('slug') != slug:
            raise SystemExit(f'{where}: slug {c.get("slug")!r} does not '
                             f'match the folder {slug!r}')
        for field in ('title', 'title_de', 'place', 'place_name',
                      'place_name_de', 'graves', 'visited',
                      'account_en', 'account_de'):
            if not c.get(field):
                raise SystemExit(f'{where}: a cemetery needs a {field}')
        if not c.get('order'):
            raise SystemExit(f'{where}: a cemetery needs an order '
                             '(the list page runs in the survey\'s order)')

        # The place's link, decided once for both languages.
        anchor = c.get('place_anchor') or c['place']
        if c['place'] in pages:
            c['place_url_en'] = f'/places/{c["place"]}/'
            c['place_url_de'] = f'/de/orte/{c["place"]}/'
        elif anchor in anchors:
            c['place_url_en'] = f'/places/#place-{anchor}'
            c['place_url_de'] = f'/de/orte/#place-{anchor}'
        else:
            # Named without a link until its gazetteer entry is in.
            c['place_url_en'] = ''
            c['place_url_de'] = ''

        # The sources the survey cites, as the page's Sources list gives them.
        sources = []
        for s in c.get('sources') or []:
            sources.append({'slug': s.get('slug', ''),
                            'label_en': s.get('label_en', ''),
                            'label_de': s.get('label_de', ''),
                            'url': s.get('url', ''),
                            'link_en': s.get('link_en', ''),
                            'link_de': s.get('link_de', ''),
                            'external': bool(s.get('external'))})
        c['sources'] = sources

        # The headstones, one entry each, as read.
        hs_path = os.path.join(d, 'headstones.yml')
        with open(hs_path, encoding='utf-8') as f:
            headstones = yaml.safe_load(f) or []
        for i, h in enumerate(headstones):
            if not h.get('name'):
                raise SystemExit(f'{hs_path}: row {i + 1} has no name '
                                 '(an unreadable stone is name: "?")')
        c['has_gid'] = any(h.get('gid') for h in headstones)

        cems.append(c | {'headstones': headstones})

    if not cems:
        raise SystemExit('cemeteries/: no cemetery found')

    cems.sort(key=lambda c: c['order'])

    # ---------- the page files ----------
    for lang, (folder, base, other) in BASES.items():
        out_dir = os.path.join(SITE, folder)
        os.makedirs(out_dir, exist_ok=True)
        for fn in os.listdir(out_dir):
            os.remove(os.path.join(out_dir, fn))

    for c in cems:
        slug = c['slug']
        # The table: the same rows on both pages, the headers the site's i18n.
        body = ['{%- comment -%} Generated by '
                'pipeline/cemeteries/cemetery_pages.py - do not hand-edit. '
                '{%- endcomment -%}',
                '{% include urls.html %}']
        if c['headstones']:
            body += ['<div class="cem-table-wrap">',
                     '<h2>{{ t.cem_names_h2 }}</h2>',
                     '',
                     '<table class="cem-table">',
                     '<thead><tr>'
                     '<th>{{ t.cem_th_name }}</th>'
                     '<th>{{ t.cem_th_born }}</th>'
                     '<th>{{ t.cem_th_died }}</th>'
                     '<th>{{ t.cem_th_note }}</th>'
                     '</tr></thead>',
                     '<tbody>']
            for h in c['headstones']:
                name = h['name']
                if h.get('gid'):
                    name += f' ({h["gid"]})'
                cells = [name, h.get('born', ''), h.get('died', ''),
                         h.get('note', '')]
                if h.get('source'):
                    cells[-1] += (f' — <a class="cem-fn" '
                                  f'href="#cem-sources">'
                                  f'{{{{ t.cem_sources_h2 }}}}</a>')
                body.append('<tr>' + ''.join(f'<td>{v}</td>' for v in cells)
                            + '</tr>')
            body += ['</tbody>', '</table>', '</div>', '']

        for lang, (folder, base, other) in BASES.items():
            fm = ['---',
                  'layout: cemetery',
                  f'cemetery: {yaml_str(slug)}',
                  f'title: {yaml_str(c["title_de"] if lang == "de" else c["title"])}',
                  f'lang: {lang}',
                  f'permalink: {yaml_str(base + slug + "/")}',
                  f'alt_url: {yaml_str(other + slug + "/")}',
                  'excerpt_separator: ""',
                  '---', '']
            with open(os.path.join(SITE, folder, slug + '.md'), 'w',
                      encoding='utf-8', newline='\n') as f:
                f.write('\n'.join(fm) + '\n' + '\n'.join(body) + '\n')

    # ---------- the site's data ----------
    def pub(c):
        return {k: c[k] for k in
                ('slug', 'order', 'title', 'title_de', 'place', 'place_name',
                 'place_name_de', 'place_url_en', 'place_url_de', 'graves',
                 'visited', 'account_en', 'account_de', 'has_gid', 'sources')}

    with open(os.path.join(SITE, '_data', 'cemeteries.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by pipeline/cemeteries/cemetery_pages.py from\n'
                '# cemeteries/<slug>/cemetery.yml and headstones.yml - do\n'
                '# not hand-edit. Keyed by slug; the layout reads the page\'s\n'
                '# cemetery from here.\n')
        yaml.safe_dump({c['slug']: pub(c) for c in cems}, f,
                       allow_unicode=True, default_flow_style=False,
                       sort_keys=False, width=100)
    with open(os.path.join(SITE, '_data', 'cemeteries_list.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by pipeline/cemeteries/cemetery_pages.py - do\n'
                '# not hand-edit. The list page\'s order: the Trąbczyn area\n'
                '# first, the outliers after (the editor, 2026-10-26).\n')
        yaml.safe_dump([{k: c[k] for k in
                         ('slug', 'order', 'title', 'title_de', 'place',
                          'place_name', 'place_name_de', 'graves')}
                        for c in cems], f,
                       allow_unicode=True, default_flow_style=False,
                       sort_keys=False, width=100)
    if not quiet:
        print(f'wrote {len(cems)} cemetery pages to site/_cemeteries/ '
              'and site/_cemeteries_de/')


if __name__ == '__main__':
    main()
