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
  reference/places.yml       canonical places, their variants and patterns
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


def load_people_records():
    """{slug: record} - reference/people.yml as authored, nothing dropped.

    load_people() below returns a three-tuple because three callers unpack it
    positionally, and widening that tuple would break all of them at once. But a
    tuple of (slug, display, regex) throws away tier, variants, identity and open
    questions - everything that makes an entity more than a pattern. So the whole
    record is available here, and load_people() is a projection of it.
    """
    import yaml
    path = os.path.join(ROOT, 'reference', 'people.yml')
    with open(path, encoding='utf-8') as f:
        return (yaml.safe_load(f) or {}).get('people') or {}


def load_place_records():
    """{slug: record} - reference/places.yml as authored."""
    return unitlib.load_places_authority().get('places') or {}


def _pattern_for(entry):
    """One entity's full pattern: `match`, its abbreviations, and its variants.

    Variants used to be decoration - twelve were recorded and not one was read
    by anything, so authoring a variant did nothing at all. Folding them in here
    means that recording an observed spelling is what makes the edition find it.
    A variant marked `match: false` is deliberately left out: that is how a
    spelling is documented as seen WITHOUT asserting it is this entity, which is
    what an unsettled identity needs.

    A variant the entity's own `match` ALREADY finds is left out too, and that
    one is not an optimisation. Seventeen variants restate an alternative that
    `match` spells more carefully: honrichs matches `Hon(?![a-zà-ÿ])` and lists
    `Hon` as a variant, knoblauch matches `Knob(?![a-zà-ÿ])` and lists `Knob`.
    Appending the bare form alongside re-admits everything the guard was written
    to exclude - the first run of this took Honrichs from 43 documents to 48 and
    Knoblauch from 1 to 11. A redundant alternative can only ever loosen a
    pattern, so a variant already covered is dropped.
    """
    parts = []
    pat = (entry.get('match') or '').strip()
    if pat:
        parts.append(pat)
    if entry.get('abbrev'):
        parts.append(entry['abbrev'])
    known = re.compile(pat) if pat else None
    for form, matched in unitlib.entity_variants(entry):
        if matched and not (known and known.search(form)):
            parts.append(re.escape(form))
    return '|'.join(parts)


def load_people():
    """[(slug, display, compiled)] - the curated authority, then the long tail.

    Curated entries win: they carry display names, merged identities and
    distinctions the statistics cannot see. The tail only fills what they miss,
    and is skipped wherever a curated pattern already matches the name.
    """
    data = load_people_records()

    out, covered = [], []
    for slug, e in data.items():
        pat = _pattern_for(e)
        if not pat:
            continue
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


def place_authority():
    """[(slug, display, compiled)] for places, in the shape load_people() uses.

    A place with no `match` is still canonicalised on the dateline; it simply
    cannot be found in the body of a document, which is the honest outcome for a
    place we know the name of but not how the writers spell it.
    """
    out = []
    for slug, e in load_place_records().items():
        pat = _pattern_for(e)
        if pat:
            out.append((slug, e.get('display') or slug,
                        re.compile(_ANCHOR % pat, re.UNICODE)))
    return out


def _mentions(rec, authority, kind):
    """Every entity of one kind in a record, with where each was found.

    Walks the record's pages so a mention carries its page and its absolute
    line, which is what makes it citable. An entity named several times on a
    page is reported once per occurrence.
    """
    out = []
    for p in rec.get('pages') or []:
        lines = p['diplomatic'].split('\n')
        base = p['line_start']
        for i, line in enumerate(lines):
            for slug, disp, rx in authority:
                for m in rx.finditer(line):
                    out.append({
                        'entity': slug,
                        'display': disp,
                        'kind': kind,
                        'surface': m.group(0),
                        'page': p['page'],
                        'page_id': p.get('page_id', ''),
                        'line': base + i,
                    })
    out.sort(key=lambda x: (x['line'], x['entity']))
    return out


def mentions(rec, people=None):
    """Every person mentioned in one record, with where it was found."""
    return _mentions(rec, people if people is not None else load_people(),
                     'person')


def place_mentions(rec, places=None):
    """Every place NAMED in a record - a different question from where it was
    written.

    The edition has always known where a document was written, from its
    dateline. It has never known which places a document talks about, which is
    why the estate at the centre of a holding stands in the place index with a
    count in the handfuls rather than the hundreds. Downstream the two counts are
    kept apart for the same reason: no single number for such a place is true on
    its own.
    """
    return _mentions(rec, places if places is not None else place_authority(),
                     'place')


def entities_in(rec, people=None):
    """The slugs a record mentions, in authority order - the old behaviour.

    build_site_data only ever needed the set, and searched the whole document
    text at once. Kept exactly so, so moving the matching here changes nothing
    it emits.
    """
    people = people if people is not None else load_people()
    return [slug for slug, _, rx in people if rx.search(rec['text'])]


# --------------------------------------------------------------- canon ----
# Variants that are rulings or fragments rather than spellings: a bracketed
# form records a doubtful reading, and a three-letter stub is an abbreviation
# whose expansion is a judgement the translator should not be asked to make.
_NOT_A_RENDER = ('[', ']')
_MIN_VARIANT = 5


def _not_a_spelling(form):
    """True for a variant that is a dateline fragment rather than a spelling.

    `Franckfurth a d h` and `Kontop. 27ten` are what a dateline looks like when
    it runs into the rest of the line. They belong in the canon, which is
    matching whole dateline strings, and nowhere near a rendering instruction
    given to a translator working on running prose.
    """
    if len(form) < _MIN_VARIANT or any(c in form for c in _NOT_A_RENDER):
        return True
    if any(c.isdigit() for c in form):
        return True
    return any(len(tok.strip('.')) < 2 for tok in form.split())


def canonical_renders():
    """[{term, pattern, policy, render, kind}] - variant spelling -> the form
    the English uses.

    The edition settles a name once, from the whole corpus, and the translation
    has to agree with what the site then displays. Typing that agreement into
    the termbase by hand guarantees it drifts, so it is generated here from the
    same two authorities the site indexes from: a variant recorded in
    people.yml or places.yml becomes a rendering instruction in the prompt AND
    an enforced check afterwards.

    Deliberately narrow. Only `variants` are emitted, never the alternations
    inside `match`: a `match` pattern exists to FIND an entity, and half of what
    it catches are inflections rather than misspellings. And nothing is emitted
    for an entity carrying `canonical: false`, whose own spelling is still open.
    """
    out = []
    for kind, records in (('person', load_people_records()),
                          ('place', load_place_records())):
        for slug, e in records.items():
            if e.get('canonical') is False:
                continue
            render = (e.get('render') or e.get('display') or '').strip()
            if not render:
                continue
            for v in unitlib.variant_records(e):
                form = v['form'].strip()
                if not (v['match'] and v['canon']) or _not_a_spelling(form):
                    continue
                if form.lower() == render.lower():
                    continue
                out.append({
                    'term': form,
                    'pattern': r'\b' + re.escape(form) + r'\w*',
                    'policy': 'translate',
                    'render': render,
                    'kind': kind,
                    'entity': slug,
                })
    out.sort(key=lambda e: (e['kind'], e['render'].lower(), e['term'].lower()))
    return out


if __name__ == '__main__':
    import sys
    rows = canonical_renders()
    sys.stdout.reconfigure(encoding='utf-8')
    for e in rows:
        print('%-8s %-24s -> %s' % (e['kind'], e['term'], e['render']))
    print('\n%d canonical rendering(s)' % len(rows))
