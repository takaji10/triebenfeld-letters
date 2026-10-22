# -*- coding: utf-8 -*-
"""
Who and which places the literature names, for questions and for the site.

Reads  : corpus/literature/ (build_literature.py), the edition's authorities
         through pipeline/build/entities.py (reference/people.yml,
         name_seeds.json, places.yml), and literature/index.yml, the rulings
Writes : corpus/literature/mentions.json   every hit that was ruled right
         site/_data/literature_mentions.yml for the "In the literature" list
                                            of a person (/people/) or an
                                            estate (/places/)
         review/literature/mentions.md      (--sheet) every hit in context,
                                            grouped by name and spelling, for
                                            reading

The edition's patterns were written for its documents and match wrongly in
books: "August" the month is not Prince August, "Sommer" the season is not a
man named Sommer (docs/LITERATURE_PLAN.md, section 5). So no hit goes live
unread. Each pair of a name and a spelling found (`hoym` / "Hoym") is ruled in
literature/index.yml, as right everywhere, wrong everywhere, or right except
in the passages listed (or the reverse). A pair with no ruling is left out of
the outputs and reported; `--check` fails on it, so a new or corrected text
(Guradze) cannot bring unread hits to the site.

The books also print names in forms the edition's patterns miss: the black
register gives Trąbczyn as "Trombczyn" and "Trobozyn", Krotoszyn as
"Krotoczyn". The `patterns:` section of literature/index.yml adds such forms
for the literature only; their hits are read and ruled like any other.

Only the originals are searched: the original decides (WORKING_NOTES, "The
literature"), and the English would count every hit twice. Only the works
shown on the site: a work with `visible: false` (Seidel) has no page to link
to, and its hits are not read.

Usage: python pipeline/literature/literature_index.py [--sheet] [--check]
"""
import io, os, re, sys, json, argparse, collections
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'build'))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import entities                     # noqa: E402
import literature_site              # noqa: E402  (the page labels)

# After the imports: literature_site wraps sys.stdout itself, and a second
# wrapper made before it would be dropped and close the stream.
sys.stdout.reconfigure(encoding='utf-8')

CORPUS = os.path.join(ROOT, 'corpus', 'literature')
RULINGS = os.path.join(ROOT, 'literature', 'index.yml')
SHEET = os.path.join(ROOT, 'review', 'literature', 'mentions.md')


def ruling_of(rule, where):
    """True if the hit stands, False if not, None if there is no ruling.

    A ruling is `true`, a string beginning "no" (with the reason), or a
    mapping {default: <one of those>, except: {"<work>/<passage>": reason}}
    where the passages listed take the opposite of the default."""
    if rule is None:
        return None
    if isinstance(rule, dict):
        d = ruling_of(rule.get('default'), where)
        return (not d) if where in (rule.get('except') or {}) else d
    if rule is True or (isinstance(rule, str) and rule.lower().startswith('yes')):
        return True
    if rule is False or (isinstance(rule, str) and rule.lower().startswith('no')):
        return False
    raise ValueError(f'literature/index.yml: cannot read the ruling {rule!r}')


def extra_patterns(authority, patterns):
    """The literature's own spellings, as authority entries of their kind.

    `patterns` is the `patterns:` section of literature/index.yml,
    {person|place: {slug: regex}}: forms the books print that the edition's
    patterns do not catch ("Trombczyn", "Krotoczyn"). They are kept out of
    reference/ so the edition's own matching is not changed by them."""
    out = {}
    for kind, per in (patterns or {}).items():
        names = {slug: disp for slug, disp, _ in authority[kind]}
        out[kind] = []
        for slug, pat in per.items():
            if slug not in names:
                raise ValueError(f'literature/index.yml: no {kind} {slug!r} in the edition')
            out[kind].append((slug, names[slug], re.compile(entities._ANCHOR % pat, re.UNICODE)))
    return out


def _applies_or_true(rx, uid):
    """Whether the authority's pattern may match in this record: a plain
    compiled pattern may everywhere; an entities._Rx (only_in, not_in)
    answers for itself."""
    return True if not isinstance(rx, entities._Rx) else rx.applies(uid)


def hits(patterns=None):
    """Every hit in the originals of the visible works, in order."""
    with open(os.path.join(CORPUS, 'index.json'), encoding='utf-8') as f:
        works = [w for w in json.load(f) if w.get('visible')]
    authority = {'person': entities.load_people(), 'place': entities.place_authority()}
    extra = extra_patterns(authority, patterns)
    edition_rx = collections.defaultdict(list)
    for kind, auth in authority.items():
        for slug, _, rx in auth:
            # the _Rx wrapper itself: applies() is asked of it (see below)
            edition_rx[(kind, slug)].append(rx)
    out = []
    for w in works:
        for p in w['passages']:
            text = literature_site.passage_text(w['slug'], p['key'], w['language'])
            if not text:
                continue
            lines = text.split('\n')
            rec = {'uid': f"literature:{w['slug']}/{p['key']}",
                   'pages': [{'diplomatic': text, 'page': p['key'], 'line_start': 1}]}
            for kind, auth in authority.items():
                found = entities._mentions(rec, auth, kind)
                # a literature pattern that also catches a form the edition's
                # own pattern catches would count that hit twice - but only
                # where the edition's pattern can actually fire here: a
                # pattern fenced with only_in (the Trąmpczyński family's five
                # documents) matches nothing in a literature uid, so its
                # literature pattern is the only route and nothing is
                # double-counted (2026-10-22, Minakowska 2026,
                # Wojciech Otto-Trąmpczyński)
                found += [m for m in entities._mentions(rec, extra.get(kind, []), kind)
                          if not any(_applies_or_true(rx, rec['uid'])
                                     and rx.fullmatch(m['surface'])
                                     for rx in edition_rx[(kind, m['entity'])])]
                for m in sorted(found, key=lambda m: m['line']):
                    out.append({'kind': kind, 'entity': m['entity'], 'display': m['display'],
                                'surface': m['surface'], 'work': w['slug'], 'cite': w['cite'],
                                'passage': p['key'], 'line': m['line'],
                                'context': lines[m['line'] - 1].strip(), '_p': p})
    return works, out


def context(h, width=110):
    t, s = h['context'], h['surface']
    i = t.find(s)
    if i < 0 or len(t) <= 2 * width:
        return t
    a, b = max(0, i - width), min(len(t), i + len(s) + width)
    return ('…' if a else '') + t[a:b] + ('…' if b < len(t) else '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sheet', action='store_true', help='write review/literature/mentions.md')
    ap.add_argument('--check', action='store_true', help='fail if a hit has no ruling')
    args = ap.parse_args()

    data = {}
    if os.path.isfile(RULINGS):
        with open(RULINGS, encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
    rulings = {'person': data.get('people') or {}, 'place': data.get('places') or {}}
    with open(os.path.join(ROOT, 'site', '_data', 'i18n.yml'), encoding='utf-8') as f:
        strings = yaml.safe_load(f)

    works, found = hits(data.get('patterns'))
    kept, unruled = [], collections.Counter()
    for h in found:
        r = ruling_of((rulings[h['kind']].get(h['entity']) or {}).get(h['surface']),
                      f"{h['work']}/{h['passage']}")
        if r is None:
            unruled[(h['kind'], h['entity'], h['surface'])] += 1
        elif r:
            kept.append(h)

    # an exception naming a passage where the spelling is not found is a slip
    # (a mistyped key, or a text since corrected), and would rule nothing
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
            f.write('# Hits of the edition\'s index in the literature\n\n'
                    'Made by pipeline/literature/literature_index.py --sheet. Rule each '
                    'pair in literature/index.yml.\n')
            for (kind, ent, surf), hs in sorted(groups.items()):
                r = (rulings[kind].get(ent) or {}).get(surf)
                f.write(f'\n## {kind} `{ent}` "{surf}" ({len(hs)}; ruling: '
                        f'{"none" if r is None else json.dumps(r, ensure_ascii=False)})\n\n')
                for h in hs:
                    f.write(f"- {h['work']}/{h['passage']}: {context(h)}\n")
        print(f'wrote {os.path.relpath(SHEET, ROOT)}: {len(groups)} pairs, {len(found)} hits')

    # corpus: every hit that stands, for questions
    with open(os.path.join(CORPUS, 'mentions.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump([{k: v for k, v in h.items() if k not in ('_p', 'cite')} for h in kept],
                  f, ensure_ascii=False, indent=1)
        f.write('\n')

    # site: for each person and estate, the works and pages that name them.
    # Places that are not estates have no list on the site (they stay in
    # mentions.json).
    with open(os.path.join(ROOT, 'site', '_data', 'estates.yml'), encoding='utf-8') as f:
        estates = {e['slug'] for e in yaml.safe_load(f)}
    site = {'person': {}, 'place': {}}
    for h in kept:
        if h['kind'] == 'place' and h['entity'] not in estates:
            continue
        works_of = site[h['kind']].setdefault(h['entity'], {})
        pages = works_of.setdefault(h['work'], {'work': h['work'], 'cite': h['cite'], 'pages': {}})['pages']
        if h['passage'] not in pages:
            p = h['_p']
            pages[h['passage']] = {'key': p['key'],
                                   'en': literature_site.label(p, strings['en']),
                                   'de': literature_site.label(p, strings['de'])}
    order = {w['slug']: i for i, w in enumerate(sorted(works, key=lambda w: w['year']))}
    out = {kind: {ent: [dict(w, pages=list(w['pages'].values()))
                        for w in sorted(ws.values(), key=lambda w: order[w['work']])]
                  for ent, ws in sorted(per.items())}
           for kind, per in site.items()}
    with open(os.path.join(ROOT, 'site', '_data', 'literature_mentions.yml'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# Generated by pipeline/literature/literature_index.py from the rulings in\n'
                '# literature/index.yml. Do not edit by hand.\n')
        yaml.safe_dump(out, f, allow_unicode=True, sort_keys=False, width=1000)

    links = sum(len(w['pages']) for per in out.values() for ws in per.values() for w in ws)
    print(f'{len(found)} hits in {len(works)} works; {len(kept)} stand '
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
