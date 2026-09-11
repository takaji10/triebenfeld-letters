# -*- coding: utf-8 -*-
"""
Apply the standing editorial bars to a transcription-fix sheet, and rule on
every row a rule can settle.

    python triage_fixes.py --unit oe1bu9454            # report only
    python triage_fixes.py --unit oe1bu9454 --write    # write the decisions

docs/EDITORIAL_RULES.md states what may be corrected without asking and what is
never changed without the editor. Those bars were applied by hand to 478
proposals on the deeds; the correspondence has 2,868, which is too many to hold
in one head and exactly the kind of work a rule should do.

So this writes the decisions the rules dictate, and only those:

  APPLIED     the transcribed form is a hapax the corpus does not know, the
              proposed reading is one it does or is a fixed formula, the change
              is word-for-word, and it is one slip rather than a reading
  REJECTED    the classes the rules never touch - names, figures, abbreviations,
              diacritics, grammar-only changes, and any proposal offering two
              readings, which is an admission that neither is settled
  LEFT OPEN   everything else, with the reason attached, for a person

Nothing here decides anything a human has not already decided in the same shape.
Every rule below is one the editor ruled on for the deeds, and the count of rows
it settles is printed so the bar can be seen working before it is trusted.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, csv, difflib, argparse
from collections import Counter

import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

WORD = re.compile(r'[^\W\d_]+', re.UNICODE)
STRIP = """.,;:()[]"'¬"""

# A proposal offering the editor a choice has not settled anything.
TWO_WAYS = re.compile(r'\bor\b|/|\?|\(|\[')
# Diacritics and Polish orthography: the page may simply carry the plain letter.
DIACRITIC = str.maketrans('ąćęłńóśźżäöüß', 'acelnoszzaous')


def pairs(before, after):
    a, b = before.split(), after.split()
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b).get_opcodes():
        if tag == 'equal':
            continue
        if tag != 'replace' or (i2 - i1) != (j2 - j1):
            return None
        out.extend(zip(a[i1:i2], b[j1:j2]))
    return out


def only_diacritics(a, b):
    return a != b and a.lower().translate(DIACRITIC) == b.lower().translate(DIACRITIC)


def only_case(a, b):
    return a != b and a.lower() == b.lower()


def build_index():
    freq = Counter()
    for u in unitlib.load_units():
        p = os.path.join(u.dir, u.get('corpus') or 'corpus.txt')
        if os.path.isfile(p):
            freq += Counter(WORD.findall(io.open(p, encoding='utf-8').read()))
    sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'build'))
    from entities import load_people, load_places
    names = set()
    for _, disp, _ in load_people():
        names.update(w.lower() for w in WORD.findall(disp))
    for v, c in load_places().items():
        names.update(w.lower() for w in WORD.findall(v))
        names.update(w.lower() for w in WORD.findall(c))
    return freq, {w for w in names if len(w) >= 5}


def near_name(w, names):
    lw = w.lower()
    if len(lw) < 5:
        return ''
    for nm in names:
        if lw == nm or lw.startswith(nm) or nm.startswith(lw):
            return nm
        if difflib.SequenceMatcher(a=lw, b=nm).ratio() >= 0.7:
            return nm
    return ''


def rule(r, freq, names):
    """(decision, why). decision '' means leave it for a person."""
    de, prop = r['transcribed'].strip(), r['proposed'].strip()

    # --- rejected outright, and ONLY these --------------------------------
    # Rejecting a row hides it from the editor for good, so it is reserved for
    # rows that cannot be a correction at all. Everything else is left open:
    # scoring this against 701 rows ruled by hand showed the first draft
    # rejecting eleven good fixes because a figure stood elsewhere in the span,
    # or because one word-pair of several differed only in case.
    if not prop or prop in ('-', '—'):
        return 'n', 'no reading proposed'
    if de == prop:
        return 'n', 'the proposal is the transcription'
    if only_diacritics(de, prop):
        return 'n', 'the whole change is a diacritic the page may not carry'
    if only_case(de, prop):
        return 'n', 'the whole change is capitalisation'

    # --- left open: a person decides --------------------------------------
    if r['confidence'] == 'hedged' or TWO_WAYS.search(prop):
        return '', 'the proposal offers a choice, so nothing is settled'
    # A row that cannot be anchored cannot be applied, and worse: "the
    # transcribed form is a hapax" reads as strong evidence when the form is
    # absent from the corpus altogether, which is what absent means. The first
    # run picked 37 such rows and every one was refused for want of a line.
    if not (r.get('line') or '').strip():
        return '', 'not located: no line to apply it to'

    ps = pairs(de, prop)
    if ps is None:
        return '', 'rewrites the passage rather than a word'
    if not ps:
        return 'n', 'nothing to change'

    for old, new in ps:
        o, n = old.strip(STRIP), new.strip(STRIP)
        # a figure is read, never re-derived - but only the words that actually
        # change are the proposal; a sum standing untouched beside them is not
        if any(c.isdigit() for c in o + n):
            return '', 'changes a figure: read, never re-derived'
        if only_case(o, n) or only_diacritics(o, n):
            return '', 'one of the changes is only case or a diacritic'
        near = near_name(o, names) or near_name(n, names)
        if near:
            return '', f'a name ({near}): the spelling is the editor\'s call'
        if freq.get(o, 0) == 0:
            return '', f'{o} is not in the corpus - the quotation is not the page'
        if freq.get(o, 0) > 2:
            return '', (f'{o} occurs {freq.get(o)}x here - the claim is that this '
                        f'reading is wrong, not that the word is')
        sim = difflib.SequenceMatcher(a=o.lower(), b=n.lower()).ratio()
        if sim < 0.62:
            return '', f'{o} -> {n}: a reading of a corrupt word, not a slip'
        if freq.get(n, 0) < 3 and sim < 0.8:
            return '', f'{n} is not attested here and {o} -> {n} is not close'

    # --- everything above passed: the rules settle it ---------------------
    worst = min(difflib.SequenceMatcher(a=o.strip(STRIP).lower(),
                                        b=n.strip(STRIP).lower()).ratio()
                for o, n in ps)
    best_attested = max(freq.get(n.strip(STRIP), 0) for _, n in ps)
    return 'y', (f'hapax against an attested form ({best_attested}x), '
                 f'one slip (similarity {worst:.2f})')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', help='unit slug; required when the project holds '
                                   'more than one')
    ap.add_argument('--write', action='store_true',
                    help='write the decisions into the sheet')
    a = ap.parse_args()
    slug = unitlib.resolve_unit(a.unit)
    sheet = os.path.join(unitlib.review_dir(slug), 'transcription_fixes.csv')
    if not os.path.isfile(sheet):
        sys.exit(f'no sheet at {sheet} - run transcription_fixes.py first')

    freq, names = build_index()
    rows = list(csv.DictReader(io.open(sheet, encoding='utf-8-sig')))
    counts, why_open = Counter(), Counter()
    touched = 0
    for r in rows:
        if (r.get('decision') or '').strip():
            counts['already ruled'] += 1
            continue
        if not (r.get('needs') or '') or r['needs'] == 'applied':
            continue
        d, why = rule(r, freq, names)
        if d:
            counts['applied' if d == 'y' else 'rejected'] += 1
            touched += 1
            if a.write:
                r['decision'] = d
        else:
            counts['left for a person'] += 1
            why_open[why.split(' -')[0].split(' occurs')[0][:46]] += 1

    for k in ('already ruled', 'applied', 'rejected', 'left for a person'):
        print(f'  {counts[k]:5d}  {k}')
    print('\nwhat is left, and what it wants:')
    for k, v in why_open.most_common(12):
        print(f'  {v:5d}  {k}')

    if not a.write:
        print('\n(report only - re-run with --write to record these decisions)')
        return
    with io.open(sheet, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f'\nwrote {touched} decision(s) into {sheet}')
    print('apply_transcription_fixes.py records them and acts on them')


if __name__ == '__main__':
    main()
