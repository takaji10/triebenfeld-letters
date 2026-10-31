# -*- coding: utf-8 -*-
"""
Do the other datasets' ruled name hits name someone the edition indexes?

    python pipeline/review/check_mentions_join.py

The literature and the newspapers run their texts against the SAME authorities
the corpus runs against (pipeline/build/entities.py), but every hit is first
read and ruled: literature/index.yml and newspapers/index.yml say for each
(name, spelling) pair whether it stands, with the work or passage named in
every row of the mention lists they produce. A slug that is spelled wrong,
or a section-only `patterns:` form keyed to a slug that does not exist,
would not fail at that stage - it would simply name a person or place the
edition publishes nothing about, and every connection it carries would
vanish without a trace: no card on /people/, no heading, no page to link.

This check holds every ruled slug to the authorities:

  a person slug must be  reference/people.yml (curated, even when it names
                         no document: Hans von Held lives in the books, the
                         press-only names like Głowecki live in the press),
                         or in the corpus index (dataset/index/people.json),
                         or in reference/genealogy.yml (a person page);
  a place slug must be   reference/places.yml or a gazetteer entry
                         (reference/gazetteer/<slug>.yml), which is a place
                         of the edition with its own page.

It runs in pipeline/regenerate.py after the two index steps, so a new work
or item cannot bring slugs past it unread. Exits 1 on any failure.

Usage: python pipeline/review/check_mentions_join.py [--quiet]
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_os.path.dirname(_HERE))
_sys.path.insert(0, _os.path.join(_ROOT, 'pipeline', 'gazetteer'))
_sys.path.insert(0, _ROOT)

import io, sys, os, json, collections, argparse
import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = _ROOT
DATASET = os.path.join(ROOT, 'dataset')
SOURCES = (
    # (path, what it is, where the row keeps the work or item it came from)
    (os.path.join(DATASET, 'literature', 'mentions.json'), 'literature',
     'work'),
    (os.path.join(DATASET, 'newspapers', 'mentions.json'), 'newspapers',
     'work'),
)


def people_slugs():
    """Every slug that counts as a person of the edition."""
    out = set()
    with open(os.path.join(ROOT, 'reference', 'people.yml'), encoding='utf-8') as f:
        out |= set((yaml.safe_load(f) or {}).get('people') or {})
    with open(os.path.join(DATASET, 'index', 'people.json'), encoding='utf-8') as f:
        out |= {r['entity'] for r in json.load(f)}
    with open(os.path.join(ROOT, 'reference', 'genealogy.yml'), encoding='utf-8') as f:
        out |= set((yaml.safe_load(f) or {}).get('people') or {})
    return out


def place_slugs():
    """Every slug that counts as a place of the edition."""
    with open(os.path.join(ROOT, 'reference', 'places.yml'), encoding='utf-8') as f:
        out = set((yaml.safe_load(f) or {}).get('places') or {})
    import gazetteer
    out |= set(gazetteer.load_places())
    return out


def main():
    quiet = '--quiet' in sys.argv
    valid = {'person': people_slugs(), 'place': place_slugs()}
    active = {}

    errors, rows = [], 0
    for path, section, workfield in SOURCES:
        active[section] = True
        if not os.path.isfile(path):
            print('%s: no mention list yet (%s)' % (section,
                    os.path.relpath(path, ROOT)))
            active[section] = False
            continue
        with open(path, encoding='utf-8') as f:
            mentions = json.load(f)
        missed = collections.defaultdict(set)
        # one counter per section and kind, for the passing print
        counts = collections.Counter()
        for m in mentions:
            rows += 1
            kind = m.get('kind')
            slug = m.get('entity')
            if kind not in valid:
                errors.append('%s: row with kind %r' % (section, kind))
                continue
            counts[kind] += 1
            if not slug or slug not in valid[kind]:
                missed[(kind, slug or '(no slug)')].add(m.get(workfield) or '?')
        if missed:
            for (kind, slug), works in sorted(missed.items()):
                errors.append(
                    '%s: %s slug %r names no %s of the edition - named in %s'
                    % (section, kind, slug, kind,
                       ', '.join(sorted(works)[:4])
                       + (' and %d more' % (len(works) - 4) if len(works) > 4 else '')))
        if not quiet:
            print('%s: %d hits (%s), %d unjoined slugs'
                  % (section, sum(counts.values()),
                     ', '.join('%s %d' % kv for kv in counts.most_common()),
                     len(missed)))

    if errors:
        print('%d join problem(s):' % len(errors))
        for e in errors:
            print('  FAIL ' + e)
        sys.exit(1)
    print('mention joins OK: every %s slug resolves to a person or place '
          'of the edition' %
          ' and '.join(s for s, ok in active.items() if ok))


if __name__ == '__main__':
    main()
