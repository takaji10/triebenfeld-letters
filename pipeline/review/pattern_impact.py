# -*- coding: utf-8 -*-
"""What a pattern actually hits, before anything is translated against it.

    python pipeline/review/pattern_impact.py '\\bMichaelis\\b'
    python pipeline/review/pattern_impact.py --audit          # every authority

Every expensive mistake on this project has the same shape: a pattern was added to
an authority because it was obviously right, and it was wrong in a way a hundred
lines of the corpus would have shown at once.

  * `Michaelis` was added as the feast day. It is the surname 30 times in 38
    documents - the merchant Michaelis, the court fiscal Michaelis, Christiane
    Dorothea Michaelis - and people.yml already had him.
  * Folding an entity's variants into its match pattern undid the negative
    lookaheads written to protect them. `Hon(?![a-zà-ÿ])` became a bare `Hon`,
    and one man went from 43 documents to 48.
  * `chestnut` was banned outright and blocked a letter about fetching the
    chestnuts out of the fire. `bailiff` was banned outright and blocked eight
    documents that name the Oberamtmann, who is a Chief Bailiff and correctly so.

None of those is a subtle error. Each survived because nobody counted first.
Counting is free: this reads the corpus off disk and calls nothing.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import os, re, sys, json, argparse

import unitlib

ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__))))
SAMPLE = 6          # lines printed per pattern; enough to see the sense, not a dump

# What pipeline/build/entities.py wraps every authority pattern in, and the flags
# it compiles with. This tool is only worth running if it matches what the
# pipeline does. It did not at first: it counted case-insensitively, reported
# Honrichs in 216 documents because `Hon(?![a-z...])` case-folded onto the word
# `schon`, and sent me looking for a bug in the authority rather than in itself.
ANCHOR = r'(?<![A-Za-zÀ-ÿ])(?:%s)'
FLAGS = re.UNICODE


def corpus_lines():
    """(pad, page, text) for every line of German in the project."""
    recs = json.load(open(os.path.join(ROOT, 'corpus', 'letters.json'),
                          encoding='utf-8'))
    out = []
    for r in recs:
        pad = f"{r['unit']}-{str(r['letter_id']).zfill(3)}"
        for p in r.get('pages') or []:
            text = p.get('reading') or p.get('diplomatic') or ''
            for line in text.split('\n'):
                if line.strip():
                    out.append((pad, p.get('page'), line.strip()))
    return out


def report(label, pattern, lines, anchored=True):
    try:
        rx = re.compile(ANCHOR % pattern if anchored else pattern, FLAGS)
    except re.error as e:
        print(f'{label}: BAD PATTERN - {e}')
        return 0
    hits = [(pad, page, ln) for pad, page, ln in lines if rx.search(ln)]
    docs = sorted({pad for pad, _, _ in hits})
    print(f'\n{label}')
    print(f'  {pattern}')
    print(f'  {len(hits)} line(s) in {len(docs)} document(s)')
    if not hits:
        print('  NOTHING. A pattern that matches nothing is either premature or wrong.')
        return 0
    for pad, page, ln in hits[:SAMPLE]:
        show = ln if len(ln) <= 140 else ln[:137] + '...'
        print(f'    {pad} p{page}  {show}')
    if len(hits) > SAMPLE:
        print(f'    ... and {len(hits) - SAMPLE} more')
    if len(docs) > 25:
        print(f'  WIDE: {len(docs)} documents. Read more than six lines before'
              f' committing this.')
    return len(docs)


def authority_patterns():
    """Every match pattern the authorities assert, with where it came from.

    Both files nest their entries under a top-level key and carry sibling keys
    that are not entities - places.yml has `reject` beside `places` - so the
    entity map is taken by name rather than by assuming the file is the map.
    """
    import yaml
    out = []
    for kind, fn, key in (('place', 'places.yml', 'places'),
                          ('person', 'people.yml', 'people')):
        doc = yaml.safe_load(open(os.path.join(ROOT, 'reference', fn),
                                  encoding='utf-8')) or {}
        for name, rec in (doc.get(key) or {}).items():
            if isinstance(rec, dict) and rec.get('match'):
                out.append((f'{kind} {name}', rec['match']))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pattern', nargs='?', default=None,
                    help='a regex to count, quoted')
    ap.add_argument('--audit', action='store_true',
                    help='count every pattern in people.yml and places.yml')
    ap.add_argument('--raw', action='store_true',
                    help='count the pattern as given, without the left anchor '
                         'the pipeline wraps authority patterns in')
    ap.add_argument('--wide', type=int, default=25,
                    help='flag any pattern hitting more documents than this')
    a = ap.parse_args()

    lines = corpus_lines()
    print(f'{len(lines)} lines of German across the project.')

    if a.pattern:
        report('given pattern', a.pattern, lines,
               anchored=not a.raw)
        return 0

    if not a.audit:
        ap.error('give a pattern, or --audit')

    counts = []
    for label, pat in authority_patterns():
        counts.append((report(label, pat, lines), label))
    counts.sort(reverse=True)
    print('\nWidest patterns, which are where a false match does most damage:')
    for n, label in counts[:12]:
        print(f'  {n:4d}  {label}')
    dead = [l for n, l in counts if n == 0]
    if dead:
        print(f'\n{len(dead)} pattern(s) match nothing at all:')
        for l in dead:
            print(f'  {l}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
