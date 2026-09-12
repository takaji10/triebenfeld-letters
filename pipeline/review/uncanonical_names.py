# -*- coding: utf-8 -*-
"""Published English that still spells a name the way the manuscript did.

    python pipeline/review/uncanonical_names.py
    python pipeline/review/uncanonical_names.py --unit oe1bu9454

The edition settles one spelling per person and per place, in reference/people.yml
and reference/places.yml, and the termbase hands the translator the resulting
table. Nothing checked that the English came back obeying it.

This is a second kind of staleness, and it is the one no other tool sees.
translate.py --stale catches a translation whose GERMAN has changed. But a ruling
can change the AUTHORITIES while leaving the German untouched: the editor settles
that Szettleich is Szetlewek, or that Oleschnitzer is Olesnica, and every English
page already translated is now wrong without a character of the transcription
moving. check_translations.py reads the canonical table only to avoid reporting
those names as lost in translation, which is the opposite question.

Costs nothing to run. Found Szettleich standing in letter 168 three weeks after
the ruling that renamed it, in a document that no other check had any reason to
look at.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__))), 'translate'))

import os, re, sys, argparse

import yaml

import unitlib
import termbase

ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__))))
PUBLISHED = os.path.join(ROOT, 'site', '_data', 'translations')


def rulings():
    """(regex, variant, canonical, kind) for every name the edition renames.

    Only where the variant and the canonical form actually differ: an entry whose
    term already equals its render asserts nothing about the English.

    Exonyms come in too. Wien -> Vienna is the same promise as Trombczin ->
    Trąbczyn, and a German place name left standing in the English is the same
    failure whichever table it came from.
    """
    g = termbase.load()
    out = []
    for sect in ('canonical_names', 'exonyms'):
        for e in g.get(sect, []):
            term, render = e.get('term') or '', e.get('render') or ''
            if not term or not render or term == render:
                continue
            # Word-bounded on the variant itself, not the entry's pattern: the
            # pattern is written to match GERMAN and is deliberately greedy
            # (\w* tails, case folding), which over English prose reports the
            # canonical form as though it were the variant.
            out.append((re.compile(r'\b' + re.escape(term) + r'\b'),
                        term, render, e.get('kind') or sect))
    return out


def english_of(path):
    d = yaml.safe_load(open(path, encoding='utf-8')) or {}
    return [(s.get('page'), s.get('en') or '')
            for s in (d.get('segments') or [])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', default=None,
                    help='one holding; default is every published translation')
    a = ap.parse_args()

    rules = rulings()
    names = sorted(f for f in os.listdir(PUBLISHED) if f.endswith('.yml'))
    if a.unit:
        names = unitlib.scope_to_unit(names, unitlib.resolve_unit(a.unit).slug)

    hits, docs = 0, 0
    for fn in names:
        found = []
        for page, en in english_of(os.path.join(PUBLISHED, fn)):
            for rx, term, render, kind in rules:
                for m in rx.finditer(en):
                    lo = max(0, m.start() - 45)
                    found.append((page, term, render, kind,
                                  ' '.join(en[lo:m.end() + 45].split())))
        if not found:
            continue
        docs += 1
        hits += len(found)
        print(f'\n{fn[:-4]}')
        for page, term, render, kind, ctx in found:
            print(f'  p{page}  {term} -> {render}  ({kind})')
            print(f'        ...{ctx}...')

    print(f'\n{hits} occurrence(s) in {docs} document(s) of {len(names)} checked'
          f', against {len(rules)} renaming rule(s).')
    if hits:
        print('Re-translate those documents, or rule that the variant stands.')
    return 1 if hits else 0


if __name__ == '__main__':
    sys.exit(main())
