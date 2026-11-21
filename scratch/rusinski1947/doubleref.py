# -*- coding: utf-8 -*-
"""List both positions of each doubled ref (old miswire vs new wiring)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
lines = t.splitlines()
from collections import Counter
b = Counter(re.findall(r'\[\^(\d+-\d+)\](?!:)', t))
d = Counter(re.findall(r'\[\^(\d+-\d+)\]:', t))
doubled = [k for k in set(b) & set(d) if b[k] != d[k]]
for k in sorted(doubled):
    print('=== %s (%d refs, %d defs)' % (k, b[k], d[k]))
    for j, ln in enumerate(lines):
        for m in re.finditer(r'\[\^%s\](?!:)' % re.escape(k), ln):
            print('   L%d: ...%s...' % (j + 1,
                  ln[max(0, m.start() - 75):m.end() + 40]))
