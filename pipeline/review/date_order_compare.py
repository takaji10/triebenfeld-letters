# -*- coding: utf-8 -*-
"""Set the reader's answers beside the script's, and print each proposed move
compactly for Claude to read (docs/DATE_ORDER_PLAN.md, Method 2).

    python pipeline/review/date_order_compare.py --unit oe1bu9454 [--verdict move|unsure|no] [--class X]

Classes of a "move" (by the lines between the salutation-or-text and the date):
  A  the line before the date is a salutation (Ewr Durchlaucht ...), a closing
     formula follows, then the signature: the editor's example
  A2 as A, but the date stands between the closing formula and the signature
  B  no salutation line: the date follows the text and a closing formula follows
  C  no closing formula: the date stands directly before the signature
  X  anything else
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import unitlib  # noqa: E402
import date_order as D  # noqa: E402


def klass(lines, s, e, a):
    before = lines[s - 1][2]
    between = [lines[k][2] for k in range(e + 1, a + 1)]
    sig = between[-1]
    formula = between[:-1]
    if D.SAL.search(before) and formula and all(D.CLOSE.search(x) or len(x.split()) <= 3 for x in formula):
        return 'A'
    if D.CLOSE.search(before) and not formula:
        return 'A2'
    if not D.SAL.search(before) and formula and any(D.CLOSE.search(x) for x in formula):
        return 'B'
    if not formula:
        return 'C'
    return 'X'


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    slug = unitlib.unit_arg()
    unit = unitlib.one_unit(slug)
    want = sys.argv[sys.argv.index('--verdict') + 1] if '--verdict' in sys.argv else None
    wantc = sys.argv[sys.argv.index('--class') + 1] if '--class' in sys.argv else None
    reader = json.load(io.open(os.path.join(ROOT, 'review', 'date_order', 'reader_%s.json' % slug), encoding='utf-8'))
    cases = [c for c in json.load(io.open(os.path.join(ROOT, 'review', 'date_order', 'candidates.json'),
                                          encoding='utf-8')) if c['unit'] == slug]
    script = {}
    for c in cases:
        if c['regular']:
            script[c['letter']] = c
    docs = dict(D.documents(unit))
    counts = {}
    for r in reader:
        L = r['letter']
        lines = docs[L]
        idx = {n: k for k, (n, _, _) in enumerate(lines)}
        if r['verdict'] != 'move':
            counts[r['verdict']] = counts.get(r['verdict'], 0) + 1
            if want == r['verdict']:
                print('--- %s [%s] %s | odd: %s' % (L, r['verdict'], r['reason'], r.get('odd', '')))
            continue
        ks = [idx[n] for n in r['date_lines']]
        s, e, a = min(ks), max(ks), idx[r['after_line']]
        c = klass(lines, s, e, a)
        sc = script.get(L)
        agree = ''
        if sc:
            sd = [n for n, _ in sc['date_lines']]
            agree = 'script agrees' if sd == r['date_lines'] and sc['proposed']['signature'] == r['after_line'] \
                else 'SCRIPT DIFFERS (%s after %s)' % (sd, sc['proposed']['signature'])
        counts['move ' + c] = counts.get('move ' + c, 0) + 1
        if (want in (None, 'move')) and (wantc in (None, c)):
            print('--- %s [%s] %s %s' % (L, c, agree, ('| odd: ' + r['odd']) if r.get('odd') else ''))
            for k in range(max(0, s - 2), min(len(lines), a + 2)):
                mark = 'D' if s <= k <= e else ('S' if k == a else ' ')
                if k == s and lines[s][1] != lines[a][1]:
                    mark += '!'
                print('  %s %s' % (mark, lines[k][2]))
    print(counts, file=sys.stderr)


if __name__ == '__main__':
    main()
