# -*- coding: utf-8 -*-
"""
Who and where a document names, found once and shared.

Entity matching used to live inside build_site_data.py, and it ran while that
script was emitting HTML - so a mention only ever existed as a `<span>` on a
page. Nothing survived the build that an agent could scope a question against,
and nothing else in the pipeline could ask who appears in a document without
re-implementing the matching and drifting from it.

This module owns the matching. It loads the authorities, compiles them once,
and reports mentions with their location:

    {entity, display, kind, surface, page, page_id, line}

`line` is the absolute line in the unit's corpus.txt, so a mention is citable
against the archival text rather than against a rendering of it.

Authorities
  reference/people.yml       the curated people, their patterns, abbreviations
  reference/name_seeds.json  the long tail vetted by name_catalogue.py
  reference/place_canon.yml  variant spellings of one place
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import json, os, re, unicodedata
import unitlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Anchored at a word start so a pattern cannot match inside a longer word.
_ANCHOR = r'(?<![A-Za-zÀ-ÿ])(?:%s)'


def _slug(s):
    s = re.sub(r'[^a-z0-9]+', '-',
               unicodedata.normalize('NFKD', s.lower())
               .encode('ascii', 'ignore').decode()).strip('-')
    return s


def load_people():
    """[(slug, display, compiled)] - the curated authority, then the long tail.

    Curated entries win: they carry display names, merged identities and
    distinctions the statistics cannot see. The tail only fills what they miss,
    and is skipped wherever a curated pattern already matches the name.
    """
    import yaml
    path = os.path.join(ROOT, 'reference', 'people.yml')
    with open(path, encoding='utf-8') as f:
        data = (yaml.safe_load(f) or {}).get('people') or {}

    out, covered = [], []
    for slug, e in data.items():
        pat = (e.get('match') or '').strip()
        if not pat:
            continue
        if e.get('abbrev'):
            pat = pat + '|' + e['abbrev']
        rx = re.compile(_ANCHOR % pat, re.UNICODE)
        out.append((slug, e.get('display') or slug, rx))
        covered.append(re.compile(pat, re.UNICODE))

    seeds = os.path.join(ROOT, 'reference', 'name_seeds.json')
    if os.path.isfile(seeds):
        with open(seeds, encoding='utf-8') as f:
            for e in json.load(f):
                if e.get('kind') != 'person' or e.get('count', 0) < 2:
                    continue
                name = e['name']
                if any(rx.search(name) for rx in covered):
                    continue
                slug = _slug(name)
                if not slug or any(s == slug for s, _, _ in out):
                    continue
                pat = re.escape(name) + r'(?:s|n|en|es|sche\w*|ische\w*)?'
                out.append((slug, name, re.compile(_ANCHOR % pat, re.UNICODE)))
    return out


def load_places():
    """Variant spelling -> the form this edition uses."""
    return unitlib.load_place_canon()


def mentions(rec, people=None):
    """Every person mentioned in one record, with where it was found.

    Walks the record's pages so a mention carries its page and its absolute
    line, which is what makes it citable. A person named several times on a
    page is reported once per occurrence.
    """
    people = people if people is not None else load_people()
    out = []
    for p in rec.get('pages') or []:
        lines = p['diplomatic'].split('\n')
        base = p['line_start']
        for i, line in enumerate(lines):
            for slug, disp, rx in people:
                for m in rx.finditer(line):
                    out.append({
                        'entity': slug,
                        'display': disp,
                        'kind': 'person',
                        'surface': m.group(0),
                        'page': p['page'],
                        'page_id': p.get('page_id', ''),
                        'line': base + i,
                    })
    out.sort(key=lambda x: (x['line'], x['entity']))
    return out


def entities_in(rec, people=None):
    """The slugs a record mentions, in authority order - the old behaviour.

    build_site_data only ever needed the set, and searched the whole document
    text at once. Kept exactly so, so moving the matching here changes nothing
    it emits.
    """
    people = people if people is not None else load_people()
    return [slug for slug, _, rx in people if rx.search(rec['text'])]
