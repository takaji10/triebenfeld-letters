# -*- coding: utf-8 -*-
"""Dump a-series dymy/obl/ludn cell values; sum the numeric obl."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
cur = None
vals = []
AS = ('0139', '0140', '0141', '0142', '0143', '0144', '0145', '0146')
for ln in t.splitlines():
    m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'\| (\d+) \| ', ln)
    if m and cur in AS:
        c = [x.strip() for x in ln.split('|')][1:-1]
        vals.append((cur, c[0], c[8], c[9], c[10]))
tot = 0
for sh, num, d, o, l in vals:
    if o not in ('—', ''):
        m = re.fullmatch(r'(\d+)(?: \*)?', o)
        if m:
            tot += int(m.group(1))
            print(sh, 'r' + num, 'dym=%s obl=%s ludn=%s' % (d, o, l))
        else:
            print(sh, 'r' + num, 'dym=%s obl=JUNK:%r ludn=%s' % (d, o, l))
print('obl numeric sum:', tot)
