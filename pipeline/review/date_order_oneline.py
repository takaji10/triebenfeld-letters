# -*- coding: utf-8 -*-
"""One line per proposed move: before ‖ DATE ‖ between ... signature ‖ next.

    python pipeline/review/date_order_oneline.py --unit oe1bu9454 [--class A] [--agree|--noscript]
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
from date_order_compare import klass  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    slug = unitlib.unit_arg()
    unit = unitlib.one_unit(slug)
    wantc = sys.argv[sys.argv.index('--class') + 1] if '--class' in sys.argv else None
    reader = json.load(io.open(os.path.join(ROOT, 'review', 'date_order', 'reader_%s.json' % slug), encoding='utf-8'))
    regular = {c['letter'] for c in json.load(io.open(os.path.join(ROOT, 'review', 'date_order', 'candidates.json'),
                                                     encoding='utf-8')) if c['unit'] == slug and c['regular']}
    docs = dict(D.documents(unit))
    for r in reader:
        if r['verdict'] != 'move':
            continue
        L = r['letter']
        if '--agree' in sys.argv and L not in regular:
            continue
        if '--noscript' in sys.argv and L in regular:
            continue
        lines = docs[L]
        idx = {n: k for k, (n, _, _) in enumerate(lines)}
        ks = [idx[n] for n in r['date_lines']]
        s, e, a = min(ks), max(ks), idx[r['after_line']]
        c = klass(lines, s, e, a)
        if wantc and c != wantc:
            continue
        pg = '' if lines[s][1] == lines[a][1] else ' PAGEBREAK'
        nxt = lines[a + 1][2] if a + 1 < len(lines) else '(end)'
        print('%s [%s]%s %s ‖ %s ‖ %s ‖ %s' % (
            L, c, pg, lines[s - 1][2][-45:], ' / '.join(lines[k][2] for k in range(s, e + 1)),
            ' / '.join(lines[k][2] for k in range(e + 1, a + 1)), nxt[:40]))


if __name__ == '__main__':
    main()
