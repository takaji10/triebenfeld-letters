# -*- coding: utf-8 -*-
"""Ratio audit: flag rows where ludn/dymy is implausible or cells are
non-numeric - catches truncated 'clean' reads the junk filter misses."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
cur = None
flags = []
for ln in t.splitlines():
    m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'\| (\d+) \| ', ln)
    if m and cur:
        c = [x.strip() for x in ln.split('|')][1:-1]
        if len(c) < 11:
            continue

        def num(v):
            v = v.strip().rstrip('*').strip()
            return int(v) if re.fullmatch(r'\d+', v) else None
        d, o, l = num(c[8]), num(c[9]), num(c[10])
        naz = c[1][:26]
        if d:
            if l is None and c[10] not in ('—', ''):
                flags.append('%s r%-3s ludn=%r (dym=%d) NONNUM %s'
                             % (cur, c[0], c[10][:14], d, naz))
            elif l is not None and not 2.5 <= l / d <= 12:
                flags.append('%s r%-3s dym=%d obl=%s ludn=%d ratio=%.2f %s'
                             % (cur, c[0], d, c[9], l, l / d, naz))
        if o is not None and d is not None and o > d:
            flags.append('%s r%-3s obl=%d > dym=%d %s'
                         % (cur, c[0], o, d, naz))
print('\n'.join(flags))
print(len(flags), 'ratio flags')
