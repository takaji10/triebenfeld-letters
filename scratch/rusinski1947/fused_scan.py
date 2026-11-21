# -*- coding: utf-8 -*-
"""Scan all footnote defs for fused print-note numbers:
'. <digit> <Capital' or '). <digit> <Capital' inside a def's text =
the next print note glued to this def."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
hits = []
for m in re.finditer(r'\[\^(\d+)-(\d+)\]: (.{0,600})', t, re.S):
    pg, num, txt = m.groups()
    # fused-number patterns inside the def text
    pat = re.compile(r'(?:\.|\)|”|")\s+(\d{1,2})\s+(?=[A-ZĄĆĘŁŃÓŚŹŻ„])')
    for fm in pat.finditer(txt[5:]):
        n2 = int(fm.group(1))
        if n2 == int(num) + 1:      # the next sequential note number
            i = 5 + fm.start()
            hits.append((pg, num, txt[max(0, i - 40):i + 50]
                         .replace('\n', ' ')))
print(len(hits), 'fused-number hits')
for pg, num, ctx in hits:
    print('p.%s n%s: ...%s...' % (pg, num, ctx))
