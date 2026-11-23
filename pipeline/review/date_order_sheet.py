# -*- coding: utf-8 -*-
"""The reading sheet for one holding's date-order cases (docs/DATE_ORDER_PLAN.md,
Method 2): one entry per document, the end of the document with corpus line
numbers and page markers, the lines the scan took for a date marked ">".

    python pipeline/review/date_order_sheet.py --unit oe1bu9454

Reads review/date_order/candidates.json (run date_order.py first); writes
review/date_order/read_<slug>.md.
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
import date_order  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    slug = unitlib.unit_arg()
    unit = unitlib.one_unit(slug)
    cases = [c for c in json.load(io.open(os.path.join(ROOT, 'review', 'date_order', 'candidates.json'),
                                          encoding='utf-8')) if c['unit'] == slug]
    docs = dict(date_order.documents(unit))
    by = {}
    for c in cases:
        by.setdefault(c['letter'], []).append(c)
    out = ['# Date-order cases: %s' % slug, '',
           '%d documents. Lines marked ">" are what the scan took for a date.' % len(by), '']

    def key(l):
        import re
        m = re.match(r'(\d+)(.*)', l)
        return (int(m.group(1)), m.group(2)) if m else (10 ** 6, l)
    for letter in sorted(by, key=key):
        lines = docs[letter]
        nums = [n for c in by[letter] for n, _ in c.get('date_lines') or []] or \
               [n for c in by[letter] for n, _ in c['window'][:1]]
        first = min(nums)
        i = next(k for k, l in enumerate(lines) if l[0] == first)
        a, z = max(0, i - 6), min(len(lines), i + 26)
        marked = {n for c in by[letter] for n, _ in c.get('date_lines') or []}
        out.append('## %s letter %s' % (slug, letter))
        out.append('')
        out.append('```')
        page = None
        for k in range(a, z):
            n, pg, t = lines[k]
            if pg != page:
                page = pg
                out.append('            [PAGE %s]' % pg)
            out.append('%s %9d  %s' % ('>' if n in marked else ' ', n, t))
        if z < len(lines):
            out.append('            [... %d more line(s) to the end of the document]' % (len(lines) - z))
        else:
            out.append('            [END OF DOCUMENT]')
        out.append('```')
        out.append('')
    p = os.path.join(ROOT, 'review', 'date_order', 'read_%s.md' % slug)
    with io.open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out))
    print('%s: %d documents -> %s' % (slug, len(by), os.path.relpath(p, ROOT)))


if __name__ == '__main__':
    main()
