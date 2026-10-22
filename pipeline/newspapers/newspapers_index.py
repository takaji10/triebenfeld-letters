# -*- coding: utf-8 -*-
"""
Who and which places the newspapers name, for questions and for the site.

Reads  : newspapers/<slug>/original.md (the items shown on the site), the
         edition's authorities through pipeline/build/entities.py
         (reference/people.yml, name_seeds.json, places.yml), and
         newspapers/index.yml, the rulings
Writes : corpus/newspapers/mentions.json   every hit that was ruled right
         site/_data/newspapers_mentions.yml for the "In the newspapers" list
                                            of a person (/people/) or an
                                            estate (/places/)
         review/newspapers/mentions.md      (--sheet) every hit in context,
                                            grouped by name and spelling

It is the literature's index (pipeline/literature/literature_index.py) run
over the items of the press, the editor's word of 2026-10-22 ("The
people/places index should run over the items"), with two differences:

- an item is one page, so a mention links the item's page, with no anchor;
- **the uid of an item is its slug with "-1"**, the shape a document's uid
  has (kuryerpolski1754075-1): the authority's `only_in` filters were built
  for the corpus, and the Kuryer Polski's spellings ("Pawłá Prusinskie",
  "Rozrazeskich Prusimskiey") are pinned to that uid in
  reference/people.yml. The alias keeps those filters working when the
  patterns run over the item that left the corpus.

No hit goes live unread: each pair of a name and a spelling is ruled in
newspapers/index.yml as the literature's are (yes, no with the reason, or a
default with exceptions); `--check` fails on a pair with no ruling, so a new
item cannot bring unread hits to the site. Only the originals are searched.

Usage: python pipeline/newspapers/newspapers_index.py [--sheet] [--check]
"""
import io, os, re, sys, json, argparse, collections
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'build'))
sys.path.insert(0, os.path.join(HERE, '..', 'literature'))
sys.path.insert(0, ROOT)
import entities                     # noqa: E402
import literature_index             # noqa: E402  (the ruling mechanics)

sys.stdout.reconfigure(encoding='utf-8')

NEWS = os.path.join(ROOT, 'newspapers')
OUT = os.path.join(ROOT, 'corpus', 'newspapers')
RULINGS = os.path.join(ROOT, 'newspapers', 'index.yml')
SHEET = os.path.join(ROOT, 'review', 'newspapers', 'mentions.md')


def items():
    """Every item shown on the site, as literature_index.hits reads a work."""
    out = []
    for slug in sorted(os.listdir(NEWS)):
        d = os.path.join(NEWS, slug, 'item.yml')
        if not os.path.isfile(d):
            continue
        with open(d, encoding='utf-8') as f:
            it = yaml.safe_load(f)
        if not it.get('visible', True):
            continue
        out.append(it)
    return out


def hits(patterns=None):
    """Every hit in the originals of the visible items, in order."""
    authority = {'person': entities.load_people(), 'place': entities.place_authority()}
    extra = literature_index.extra_patterns(authority, patterns)
    edition_rx = collections.defaultdict(list)
    for kind, auth in authority.items():
        for slug, _, rx in auth:
            edition_rx[(kind, slug)].append(getattr(rx, 'rx', rx))
    out = []
    for it in items():
        slug = it['slug']
        path = os.path.join(NEWS, slug, 'original.md')
        text = '\n'.join(l for l in io.open(path, encoding='utf-8').read().split('\n')
                         if not l.startswith('#')).strip('\n')
        lines = text.split('\n')
        # the uid alias: see the module docstring
        rec = {'uid': f'{slug}-1',
               'pages': [{'diplomatic': text, 'page': '1', 'line_start': 1}]}
        for kind, auth in authority.items():
            found = entities._mentions(rec, auth, kind)
            found += [m for m in entities._mentions(rec, extra.get(kind, []), kind)
                      if not any(rx.fullmatch(m['surface'])
                                 for rx in edition_rx[(kind, m['entity'])])]
            for m in sorted(found, key=lambda m: m['line']):
                out.append({'kind': kind, 'entity': m['entity'], 'display': m['display'],
                            'surface': m['surface'], 'work': slug, 'cite': it['cite'],
                            'passage': 'item', 'line': m['line'],
                            'context': lines[m['line'] - 1].strip()})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sheet', action='store_true', help='write review/newspapers/mentions.md')
    ap.add_argument('--check', action='store_true', help='fail if a hit has no ruling')
    args = ap.parse_args()

    data = {}
    if os.path.isfile(RULINGS):
        with open(RULINGS, encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
    rulings = {'person': data.get('people') or {}, 'place': data.get('places') or {}}

    found = hits(data.get('patterns'))
    kept, unruled = [], collections.Counter()
    for h in found:
        r = literature_index.ruling_of(
            (rulings[h['kind']].get(h['entity']) or {}).get(h['surface']),
            f"{h['work']}/{h['passage']}")
        if r is None:
            unruled[(h['kind'], h['entity'], h['surface'])] += 1
        elif r:
            kept.append(h)

    # an exception naming a passage where the spelling is not found is a slip
    where = collections.defaultdict(set)
    for h in found:
        where[(h['kind'], h['entity'], h['surface'])].add(f"{h['work']}/{h['passage']}")
    stale = [(kind, ent, surf, k)
             for kind, per in rulings.items() for ent, surfs in per.items()
             for surf, rule in (surfs or {}).items() if isinstance(rule, dict)
             for k in (rule.get('except') or {}) if k not in where[(kind, ent, surf)]]
    stale_pairs = [(kind, ent, surf)
                   for kind, per in rulings.items() for ent, surfs in per.items()
                   for surf in (surfs or {}) if not where[(kind, ent, surf)]]

    if args.sheet:
        groups = collections.defaultdict(list)
        for h in found:
            groups[(h['kind'], h['entity'], h['surface'])].append(h)
        os.makedirs(os.path.dirname(SHEET), exist_ok=True)
        with open(SHEET, 'w', encoding='utf-8', newline='\n') as f:
            f.write("# Hits of the edition's index in the newspapers\n\n"
                    'Made by pipeline/newspapers/newspapers_index.py --sheet. Rule each '
                    'pair in newspapers/index.yml.\n')
            for (kind, ent, surf), hs in sorted(groups.items()):
                r = (rulings[kind].get(ent) or {}).get(surf)
                f.write(f'\n## {kind} `{ent}` "{surf}" ({len(hs)}; ruling: '
                        f'{"none" if r is None else json.dumps(r, ensure_ascii=False)})\n\n')
                for h in hs:
                    f.write(f"- {h['work']}/{h['passage']} line {h['line']}: "
                            f"{literature_index.context(h)}\n")
        print(f'wrote {os.path.relpath(SHEET, ROOT)}: {len(groups)} pairs, {len(found)} hits')

    # corpus: every hit that stands, for questions
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'mentions.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(kept, f, ensure_ascii=False, indent=1)
        f.write('\n')

    # site: for each person and estate, the items that name them. Places that
    # are not estates have no list on the site (they stay in mentions.json).
    with open(os.path.join(ROOT, 'site', '_data', 'estates.yml'), encoding='utf-8') as f:
        estates = {e['slug'] for e in yaml.safe_load(f)}
    site = {'person': {}, 'place': {}}
    for h in kept:
        if h['kind'] == 'place' and h['entity'] not in estates:
            continue
        ws = site[h['kind']].setdefault(h['entity'], [])
        if not ws or ws[-1]['slug'] != h['work']:
            ws.append({'slug': h['work'], 'cite': h['cite'], 'pages': []})
        pages = ws[-1]['pages']
        if not pages:
            pages.append({'key': 'item',
                          'en': 'The item', 'de': 'Das Stück'})
    out = {kind: dict(sorted(per.items())) for kind, per in site.items()}
    with open(os.path.join(ROOT, 'site', '_data', 'newspapers_mentions.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by pipeline/newspapers/newspapers_index.py from the rulings in\n'
                '# newspapers/index.yml. Do not edit by hand.\n')
        yaml.safe_dump(out, f, allow_unicode=True, sort_keys=False, width=1000)

    links = sum(len(w['pages']) for per in out.values() for ws in per.values() for w in ws)
    print(f'{len(found)} hits in {len(items())} items; {len(kept)} stand '
          f'({links} links from a person or place to a page); '
          f'{sum(unruled.values())} hits in {len(unruled)} pairs not yet ruled')
    for kind, ent, surf, k in stale:
        print(f'  exception for a passage without the hit: {kind} {ent} "{surf}" {k}')
    for kind, ent, surf in stale_pairs:
        print(f'  ruling for a spelling not found: {kind} {ent} "{surf}"')
    if (unruled or stale) and args.check:
        for (kind, ent, surf), n in sorted(unruled.items()):
            print(f'  no ruling: {kind} {ent} "{surf}" ({n})')
        sys.exit(1)


if __name__ == '__main__':
    main()
