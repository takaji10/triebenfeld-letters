# -*- coding: utf-8 -*-
"""
Check that the section numbers in each document run in sequence, and mend the
ones that do not.

    python section_numbering.py --unit oe1bu14526            # report only
    python section_numbering.py --unit oe1bu14526 --apply     # renumber

A deed's paragraphs are numbered by the scribe in an unbroken run. Where the
transcription shows §XIII, §IV, §XV in that order, the §IV is not a scribe's
lapse: it is a machine reading of Kurrent numerals that dropped a stroke, and
the run on either side says what it must have been. The same goes for §XV
followed by §XII, and for a `5. I` standing where §IX belongs.

Three things that look like breaks and are not, all handled here:

  catchwords    the scribe writes the next page's opening at the foot of the
                current one, so a header appears twice around a [PAGE ...]
                line. That is one section, not two, and when the pair is
                misnumbered both halves are mended together
  inline heads  `§. 6. Außer den in §. 3. bemerkten Kirchen Capitalien` is a
                header run into its own first line, and the number is present
  gaps          a number simply missing from the run. The header was not
                transcribed at all, so there is nothing to renumber - it is
                reported, because a dropped header is worth knowing about

Only a number that breaks the run *and* is pinned by the numbers on both sides
is changed. The line's own style is kept: `S. XI.` stays `S.`, arabic stays
arabic, and the trailing point is left as it was found.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, argparse
from collections import namedtuple

import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# a header on its own line: '§. XIV.', '§ 2.', 'S. XI.', '5. I'
ALONE = re.compile(r'^(\s*[§Ss5]\W{0,3}\s*)([IVXLC]+|\d{1,2})(\s*\.?\s*)$')
# a header run into its first line: '§. 6. Außer den ...'
# An inline header opens its own section, so what follows begins a sentence.
# '§ 3. stipulirte Erbzins in den Hipotheken buhe' is a cross-reference caught
# at a line start by the line break, and its lower-case continuation says so.
INLINE = re.compile(r'^(\s*§\.?\s*)([IVXLC]+|\d{1,2})(\.\s+)(?=[A-ZÄÖÜ])')
DOCTAG = re.compile(r'^\[DOC (\d+)\]')
PAGETAG = re.compile(r'^\[PAGE ')

ROMAN = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'),
         (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'),
         (5, 'V'), (4, 'IV'), (1, 'I')]

Head = namedtuple('Head', 'line prefix token suffix value roman')


def to_int(token):
    if token.isdigit():
        return int(token)
    n, s = 0, token.upper()
    for v, r in ROMAN:
        while s.startswith(r):
            n += v
            s = s[len(r):]
    return n if not s else None


def to_roman(n):
    out = ''
    for v, r in ROMAN:
        while n >= v:
            out += r
            n -= v
    return out


def read_heads(lines):
    """Every section header in the unit, as {doc: [Head, ...]}."""
    docs, doc = {}, None
    for i, line in enumerate(lines, 1):
        m = DOCTAG.match(line)
        if m:
            doc = m.group(1)
            continue
        if doc is None:
            continue
        m = ALONE.match(line)
        if not m:
            m = INLINE.match(line)
        if not m:
            continue
        tok = m.group(2)
        val = to_int(tok)
        if val is None or not 1 <= val <= 60:
            continue
        docs.setdefault(doc, []).append(
            Head(i, m.group(1), tok, m.group(3), val, not tok.isdigit()))
    return docs


def fold_catchwords(heads, lines):
    """A header repeated across a page break is one section, not two."""
    out = []
    for h in heads:
        if out and out[-1][-1].value == h.value:
            between = lines[out[-1][-1].line:h.line - 1]
            if all(PAGETAG.match(b) or not b.strip() for b in between):
                out[-1].append(h)       # the same section, previewed and begun
                continue
        out.append([h])
    return out


def bare_number(lines, lo, hi, want, roman):
    """A header whose section mark was not read, standing as a bare number.

    Between §2 and §4 a line reading just `3.` is the missing header with its §
    lost, not a missing section. Worth separating from a real gap: one is a
    mark that was not recognised, the other is a header that is not there at
    all. Neither is renumbered - the number is already right, and supplying a
    § would be reading a character off the page that nobody read.
    """
    forms = {to_roman(want), str(want)} if roman else {str(want)}
    for i in range(lo, hi - 1):
        t = lines[i].strip().rstrip('.')
        if t in forms:
            return i + 1
    return 0


def check(groups, lines):
    """Return (fixes, gaps). A fix is (group, wanted value)."""
    fixes, gaps = [], []
    vals = [g[0].value for g in groups]
    for k in range(1, len(groups)):
        want = vals[k - 1] + 1
        if vals[k] == want:
            continue
        # A run restarting at 1 is a new enclosure - but only if it carries on
        # from 1. A lone I between VIII and X is a misread IX, not a restart.
        if vals[k] == 1 and (k + 1 >= len(vals) or vals[k + 1] == 2):
            continue
        nxt = vals[k + 1] if k + 1 < len(vals) else None
        if vals[k] > want and (nxt is None or nxt == vals[k] + 1):
            at = bare_number(lines, groups[k - 1][-1].line, groups[k][0].line,
                             want, groups[k][0].roman)
            gaps.append((groups[k], want, vals[k], at))
            continue
        if nxt is None or nxt == want + 1:
            fixes.append((groups[k], want))           # pinned on both sides
            vals[k] = want
        else:
            at = bare_number(lines, groups[k - 1][-1].line, groups[k][0].line,
                             want, groups[k][0].roman)
            gaps.append((groups[k], want, vals[k], at))
    return fixes, gaps


def render(h, value):
    """The header as it should read, in the line's own style.

    One exception to keeping the style: a section mark read as `5` is not a
    style, it is the § itself misread, and it occurs once. `S.` is left alone -
    it recurs across documents and reads as a transcription convention rather
    than a slip.
    """
    token = to_roman(value) if h.roman else str(value)
    prefix = h.prefix
    if prefix.lstrip().startswith('5'):
        prefix = prefix.replace('5', '§', 1)
        return prefix.rstrip() + ' ' + token + (h.suffix if h.suffix.strip() else '.')
    return prefix + token + h.suffix


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', help='unit slug; required when the project holds '
                                   'more than one')
    ap.add_argument('--apply', action='store_true', help='write corpus.txt')
    a = ap.parse_args()
    slug = unitlib.resolve_unit(a.unit)
    unit = unitlib.one_unit(slug)
    corpus = os.path.join(unit.dir, unit.get('corpus') or 'corpus.txt')
    text = io.open(corpus, encoding='utf-8').read()
    lines = text.split('\n')

    all_fixes, all_gaps, n_docs = [], [], 0
    for doc, heads in read_heads(lines).items():
        groups = fold_catchwords(heads, lines)
        if len(groups) < 3:
            continue
        n_docs += 1
        fixes, gaps = check(groups, lines)
        for g, want in fixes:
            all_fixes.append((doc, g, want))
        for g, want, got, at in gaps:
            all_gaps.append((doc, g, want, got, at))

    print(f'{n_docs} document(s) with numbered sections')
    lost_mark = sum(1 for g in all_gaps if g[4])
    print(f'{len(all_fixes)} number(s) out of sequence, '
          f'{len(all_gaps) - lost_mark} header(s) missing entirely, '
          f'{lost_mark} whose section mark alone was not read\n')
    for doc, g, want in all_fixes:
        where = ', '.join(str(h.line) for h in g)
        print(f'  DOC {doc} line {where}: {g[0].prefix.strip()}{g[0].token}'
              f' -> {render(g[0], want).strip()}')
    if all_gaps:
        print()
        for doc, g, want, got, at in all_gaps:
            style = to_roman(want) if g[0].roman else str(want)
            if at:
                print(f'  DOC {doc} line {at}: numbered {style} but with no '
                      f'section mark - the § was not read. Left as it stands')
            else:
                print(f'  DOC {doc} line {g[0].line}: nothing numbered {style} '
                      f'before this {g[0].token} - a header that was not read')

    if not a.apply:
        print('\n(report only - re-run with --apply to renumber)')
        return
    if not all_fixes:
        return

    log = [f'# Section numbering - {slug}\n',
           f'{len(all_fixes)} section(s) renumbered where the run on either '
           f'side pins the value.\n']
    for doc, g, want in all_fixes:
        for h in g:
            before = lines[h.line - 1]
            lines[h.line - 1] = render(h, want)
            log.append(f'- document {doc}, line {h.line}: `{before}` -> '
                       f'`{lines[h.line - 1]}`')
    assert len(lines) == len(text.split('\n'))
    io.open(corpus, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    dest = os.path.join(unitlib.review_dir(slug), 'section_numbering.md')
    io.open(dest, 'w', encoding='utf-8', newline='\n').write('\n'.join(log) + '\n')
    print(f'\nwrote {corpus}\nwrote {dest}')


if __name__ == '__main__':
    main()
