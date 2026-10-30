# -*- coding: utf-8 -*-
"""
The maps that are in the edition get their pages on the website
(docs/MAPS_SITE_PLAN.md, the site half of docs/MAPS_PLAN.md section 7).

Reads  : reference/maps.yml                 the register of maps
         maps/<key>/labels.yml              the editor's marks on the map
         maps/<key>/positions.yml           the fit's ground position of each mark
         maps/<key>/legend.yml              the map's own legend, where it has one
         reference/gazetteer/*.yml          the places and their map appearances
Writes : site/_data/maps.yml                per in-project map: its page's data
         site/_data/maps_list.yml           the Maps page's cards
         site/_data/place_maps.yml          per place: the maps that show it
         site/_maps/<key>.md                /maps/<key>/
         site/_maps_de/<key>.md             /de/karten/<key>/

Only a map with in_project: true gets a page and a card: the editor chooses
which maps come in, one at a time (docs/MAPS_PLAN.md), and a map the
gazetteer cites and the edition does not hold stays a citation - it appears
on a place's page as its short form only, and on the missing list
(docs/MISSING_SOURCES.md). A map brought in by docs/ADDING_A_MAP.md turns
its in_project to true and this script gives it its page.

Every mark is in the pixels of the original image (docs/MAPS_PLAN.md,
section 2); the data carries it adjusted for the map's crop, which is what
the tiles show, so the viewer places it right whatever the crop.

The appearances of a place come from the gazetteer's `maps:` lists, which
pipeline/maps/import_labels.py fills; an appearance with absent: true is a
record of a check (the place judged not to be on the map), not an
appearance, and is shown nowhere.

Run as a step of pipeline/regenerate.py, after the place pages (the place pages'
layout reads place_maps.yml, which this writes).

Usage: python pipeline/maps/map_pages.py [--quiet]
"""
import io, os, json, sys
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from common import GAZETTEER_DIR, MAPS_YML, ROOT, die, read_yaml  # noqa: E402

SITE = os.path.join(ROOT, 'site')
MAPS_DIR = os.path.join(ROOT, 'maps')

# The label's `shows` values (docs/MAPS_PLAN.md, section 4), for the page in
# both languages. The editor's list, with the simple kinds the marking uses.
SHOWS_EN = {
    'village': 'Village', 'town': 'Town', 'oleder-settlement': 'Olęder settlement',
    'folwark': 'Folwark', 'folwark-or-manor': 'Folwark or manor', 'manor': 'Manor',
    'tavern': 'Tavern', 'water-mill': 'Water mill', 'windmill': 'Windmill',
    'mill': 'Mill', 'forest': 'Forest', 'field': 'Field',
    'field-or-meadow': 'Field or meadow', 'meadow': 'Meadow', 'water': 'Water',
    'road': 'Road', 'road-or-crossing': 'Road or crossing', 'crossing': 'Crossing',
    'church': 'Church', 'other': 'Other', 'unsure': 'Unsure',
}
SHOWS_DE = {
    'village': 'Dorf', 'town': 'Stadt', 'oleder-settlement': 'Haulandsiedlung',
    'folwark': 'Vorwerk', 'folwark-or-manor': 'Vorwerk oder Herrenhaus',
    'manor': 'Herrenhaus', 'tavern': 'Kretscham', 'water-mill': 'Wassermühle',
    'windmill': 'Windmühle', 'mill': 'Mühle', 'forest': 'Wald', 'field': 'Flur',
    'field-or-meadow': 'Flur oder Wiese', 'meadow': 'Wiese', 'water': 'Gewässer',
    'road': 'Weg', 'road-or-crossing': 'Weg oder Übergang', 'crossing': 'Übergang',
    'church': 'Kirche', 'other': 'Sonstiges', 'unsure': 'Unsicher',
}

# The register's `kind` values (the head of reference/maps.yml), for the card.
KIND_EN = {
    'estate': 'Estate plan', 'parish': 'Parish map', 'regional': 'Regional map',
    'topographic': 'Topographic map', 'military': 'Military map',
    'town': 'Town plan', 'sketch': 'Sketch map', 'atlas': 'Atlas',
}
KIND_DE = {
    'estate': 'Gutsplan', 'parish': 'Pfarrkarte', 'regional': 'Regionalkarte',
    'topographic': 'Topographische Karte', 'military': 'Militärkarte',
    'town': 'Stadtplan', 'sketch': 'Skizze', 'atlas': 'Atlas',
}

TILE_BASE = 'https://takaji10.github.io/triebenfeld-maps'


def yaml_str(v):
    return json.dumps(v, ensure_ascii=False)


def write_data(path, header, data, dump=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(header)
        (dump or yaml.safe_dump)(data, f, allow_unicode=True,
                                 default_flow_style=False, sort_keys=False,
                                 width=100)


def label_point(lb, crop):
    """The mark's anchor in the pixels the tiles show: the place's symbol,
    or where the symbol is missing the start of the lettering; moved into
    the crop, which is what the viewer's image is."""
    p = lb.get('point') or (lb.get('trace') or [[None]])[0]
    if not p or p[0] is None:
        return None
    if crop:
        return [p[0] - crop[0], p[1] - crop[1]]
    return list(p)


def main():
    quiet = '--quiet' in sys.argv
    maps = read_yaml(MAPS_YML)['maps']
    in_project = {k: dict(v or {}, key=k) for k, v in maps.items()
                  if v.get('in_project')}
    if not in_project:
        die('no map of reference/maps.yml has in_project: true - nothing to '
            'build (docs/ADDING_A_MAP.md brings one in)')

    # The gazetteer, keyed as the place pages key it (the register's slug
    # where the entry names one): the appearances' labels and the refs sit
    # there, and the place's heading is the name the site shows.
    gaz = {}
    for p in sorted(GAZETTEER_DIR.glob('*.yml')):
        g = read_yaml(p)
        if isinstance(g, dict) and g.get('slug'):
            gaz[g.get('register') or g['slug']] = g
    headings = {s: (g.get('heading') or s) for s, g in gaz.items()}

    # The label refs: the gazetteer item of each label may carry the
    # documents the appearance belongs to (the inscription of Łukom 1766:
    # the Ląd copy-book's two documents).
    refs_of = {}
    for g in gaz.values():
        for item in (g.get('maps') or []):
            if item.get('label'):
                refs_of[item['label']] = item.get('refs') or []

    out_maps = {}
    for key, m in sorted(in_project.items()):
        where = f'map {key}'
        labels_y = read_yaml(os.path.join(MAPS_DIR, key, 'labels.yml'))
        positions_p = os.path.join(MAPS_DIR, key, 'positions.yml')
        pos, rms = {}, None
        if os.path.isfile(positions_p):
            ps = read_yaml(positions_p)
            rms = ps.get('rms_m')
            pos = {p['label']: p for p in (ps.get('positions') or [])}
        crop = m.get('crop') or None
        disp_w = crop[2] if crop else m.get('width')
        disp_h = crop[3] if crop else m.get('height')
        labels = []
        for lb in (labels_y.get('labels') or []):
            lid = lb['id']
            place = lb.get('place')
            if place and place not in gaz:
                die(f'{where}: label {lid} names {place}, which the '
                    'gazetteer does not carry')
            pp = pos.get(lid) or {}
            labels.append({
                'id': lid,
                'place': place,
                'place_name': headings.get(place) if place else None,
                'form': lb.get('form'),
                'shows': lb.get('shows'),
                'shows_en': SHOWS_EN.get(lb.get('shows'), lb.get('shows')),
                'shows_de': SHOWS_DE.get(lb.get('shows'), lb.get('shows')),
                'note': lb.get('note'),
                'point': label_point(lb, crop),
                'crop': f'/assets/maps/crops/{key}/{lid}.jpg',
                'lat': pp.get('lat'),
                'lon': pp.get('lon'),
                'refs': refs_of.get(lid) or lb.get('refs') or [],
                'sort_name': (headings.get(place) if place else None) or lb.get('form'),
            })
        kind = (m.get('kind') or 'unknown').lower()
        out_maps[key] = {
            'slug': key,
            'cited_as': m.get('cited_as') or key,
            'title': m.get('title'),
            'title_en': m.get('title_en'),
            'maker': m.get('maker'),
            'scale': m.get('scale'),
            'year': m.get('year'),
            'kind': kind,
            'kind_en': KIND_EN.get(kind, kind),
            'kind_de': KIND_DE.get(kind, kind),
            'holder': m.get('holder'),
            'reference': m.get('reference'),
            'url': m.get('url'),
            'tiles': m.get('tiles'),
            'warp': f'{TILE_BASE}/warp.html?map={key}',
            'view_rotation': m.get('view_rotation') or 0,
            'width': disp_w,
            'height': disp_h,
            'rms_m': rms,
            'n_labels': len(labels),
            'n_places': len({l['place'] for l in labels if l['place']}),
            'labels': labels,
        }
        legend_p = os.path.join(MAPS_DIR, key, 'legend.yml')
        if os.path.isfile(legend_p):
            out_maps[key]['legend'] = read_yaml(legend_p)
        if not m.get('tiles'):
            die(f'{where}: no `tiles` in reference/maps.yml - the page has '
                'nothing to open')

    # The Maps page's cards, by date (docs/MAPS_SITE_PLAN.md, section 2).
    # The card's picture: the map's whole face, fetched by make_thumbs.py
    # from the tiles' lowest whole-map level; written only when the file is
    # here, so the card shows no image the site does not carry.
    out_list = []
    for m in sorted(out_maps.values(), key=lambda x: (x['year'] or 0, x['slug'])):
        thumb = (f'/assets/thumbs/map-{m["slug"]}.jpg'
                 if os.path.isfile(os.path.join(SITE, 'assets', 'thumbs',
                                                f'map-{m["slug"]}.jpg'))
                 else None)
        out_list.append({
            'slug': m['slug'], 'cited_as': m['cited_as'], 'year': m['year'],
            'kind_en': m['kind_en'], 'kind_de': m['kind_de'],
            'maker': m['maker'], 'holder': m['holder'],
            'reference': m['reference'], 'n_places': m['n_places'],
            'thumb': thumb,
        })

    # The place side (docs/MAPS_SITE_PLAN.md, section 4): per place, the
    # maps that show it, the appearances in date order, absent items
    # dropped. Keyed as the place pages key the place.
    place_maps = {}
    for slug, g in sorted(gaz.items()):
        apps = []
        for item in (g.get('maps') or []):
            if item.get('absent'):
                continue
            mk = maps.get(item.get('map'))
            if mk is None:
                die(f'gazetteer {slug}: names the map {item.get("map")!r}, '
                    'which reference/maps.yml does not carry')
            inproj = bool(mk.get('in_project'))
            lid = item.get('label')
            app = {
                'map': item['map'],
                'cited_as': mk.get('cited_as') or item['map'],
                'year': mk.get('year'),
                'in_project': inproj,
                'form': item.get('form'),
                'note': item.get('note'),
                'label': lid,
                'crop': (f'/assets/maps/crops/{item["map"]}/{lid}.jpg'
                         if inproj and lid else None),
                'refs': item.get('refs') or [],
            }
            apps.append(app)
        if not apps:
            continue
        apps.sort(key=lambda a: (a['year'] or 0, a['map']))
        on_site, seen = [], set()
        for a in apps:
            if a['in_project'] and a['map'] not in seen:
                seen.add(a['map'])
                on_site.append({'map': a['map'], 'cited_as': a['cited_as'],
                                'label': a['label']})
        place_maps[slug] = {'appearances': apps, 'maps_on_site': on_site}

    gen = ('# Generated by pipeline/maps/map_pages.py - do not hand-edit.\n')
    write_data(os.path.join(SITE, '_data', 'maps.yml'),
               gen + '# The maps in the edition (in_project: true), each with '
                     'its page\'s data\n# (docs/MAPS_SITE_PLAN.md).\n',
               out_maps)
    write_data(os.path.join(SITE, '_data', 'maps_list.yml'),
               gen + '# The Maps page\'s cards, by date '
                     '(docs/MAPS_SITE_PLAN.md, section 2).\n', out_list)
    write_data(os.path.join(SITE, '_data', 'place_maps.yml'),
               gen + '# Per place of the gazetteer: the maps that show it, '
                     'the appearances in date\n# order; absent items are not '
                     'appearances and are not here '
                     '(docs/MAPS_SITE_PLAN.md,\n# section 4).\n', place_maps)

    # The pages (docs/MAPS_SITE_PLAN.md, section 3): one per in-project map
    # in both languages; the layout map.html renders everything from the
    # data, so the page's body is a comment only.
    BASES = {'en': ('_maps', '/maps/', '/de/karten/'),
             'de': ('_maps_de', '/de/karten/', '/maps/')}
    for lang, (folder, base, other) in BASES.items():
        out_dir = os.path.join(SITE, folder)
        os.makedirs(out_dir, exist_ok=True)
        for fn in os.listdir(out_dir):
            os.remove(os.path.join(out_dir, fn))
        for key, m in out_maps.items():
            fm = ['---',
                  'layout: map',
                  f'map: {key}',
                  f'title: {yaml_str(m["cited_as"])}',
                  f'lang: {lang}',
                  f'permalink: {yaml_str(base + key + "/")}',
                  f'alt_url: {yaml_str(other + key + "/")}',
                  'excerpt_separator: ""',
                  '---', '']
            with open(os.path.join(SITE, folder, key + '.md'), 'w',
                      encoding='utf-8', newline='\n') as f:
                f.write('\n'.join(fm) + '\n')

    if not quiet:
        print(f'maps: {len(out_list)} in the edition '
              f'({", ".join(m["cited_as"] for m in out_list)}); '
              f'{sum(m["n_labels"] for m in out_maps.values())} labels; '
              f'{len(place_maps)} places with map appearances '
              f'-> site/_maps*/ and the maps data')


if __name__ == '__main__':
    main()
