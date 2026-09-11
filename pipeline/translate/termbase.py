# -*- coding: utf-8 -*-
"""The termbase the translation is written to and then checked against.

reference/translation_glossary.yml is authored by hand. One of its sections is
not: CANONICAL NAMES is generated from reference/people.yml and
reference/places.yml, because it has to say exactly what the site's entity index
says. A name the edition settled once, from the whole corpus, must read the same
way in the English as it does under the person's own entry - and a hand-kept
second copy of eighty spellings drifts from the first copy within a month.

So the glossary is loaded through here, in one place, by both the script that
writes the prompt and the script that checks the result. That is the point: a
rendering the model was never told about cannot be enforced afterwards, and a
rendering enforced afterwards but never taught is exactly the failure this
module was written to end - `exonyms` had been checked and not taught for the
whole of the first published pass.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'build'))

import yaml

GLOSSARY = os.path.join(ROOT, 'reference', 'translation_glossary.yml')

# Sections rendered into the prompt AND enforced afterwards, in prompt order.
# One tuple, read by translate.glossary_table() and by check_translations, so
# the two can no longer disagree about which sections exist.
SECTIONS = (
    ('currency', 'CURRENCY'),
    ('honorifics', 'FORMS OF ADDRESS'),
    ('formulas', 'CLOSING FORMULAS'),
    ('terms', 'TERMS OF ART'),
    ('exonyms', 'PLACE NAMES'),
    ('canonical_names', 'CANONICAL NAMES'),
)


def load():
    """The authored termbase, with the generated sections folded in."""
    import entities
    g = yaml.safe_load(open(GLOSSARY, encoding='utf-8')) or {}
    g['canonical_names'] = entities.canonical_renders()
    for sect, _ in SECTIONS:
        g.setdefault(sect, [])
    g.setdefault('forbidden_renders', [])
    g.setdefault('latin_terms', [])
    return g


def forbidden(g):
    """[(pattern, note)] - English that must never appear, whatever the German.

    The one mechanism that stops a settled correction being undone. A glossary
    entry says what a term SHOULD become; nothing until now said what a term
    must never become, so `hypocaustum` could come back as "chestnut" a second
    time and every check would pass.

    `when` is why this returns pairs rather than a list of banned words. An
    English word is not wrong in itself - it is wrong as a rendering of a
    particular German or Latin one, and this corpus proves the point twice.
    "chestnut" stands in L286 in "fetch the chestnuts out of the fire", and
    "bailiff" stands eight times as Chief Bailiff, the Oberamtmann, an office
    with nothing to do with the Court Summoner. Banning either outright would
    have blocked eight sound documents and taught the next reader of this file
    to distrust it. So a rule may carry `when:`, a pattern that must ALSO match
    the source page before the rendering counts as an error.
    """
    import re
    out = []
    for e in g.get('forbidden_renders') or []:
        if isinstance(e, str):
            e = {'render': e}
        r = (e.get('render') or '').strip()
        if not r:
            continue
        when = (e.get('when') or '').strip()
        out.append((re.compile(r'\b' + re.escape(r) + r'\w*', re.I),
                    re.compile(when, re.I) if when else None,
                    r, e.get('note') or ''))
    return out
