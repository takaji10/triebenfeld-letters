# -*- coding: utf-8 -*-
"""List capital-I inside lowercase-word contexts (l->I overcorrection
residue) with context, for case-by-case ruling."""
import os, re
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
hits = []
for m in re.finditer(r'[a-ząćęłńóśźż]I[a-ząćęłńóśźż]', t):
    i = m.start()
    hits.append((i, t[max(0, i - 40):i + 40].replace('\n', ' ')))
print(len(hits), 'I-inside-word hits')
seen = set()
for i, ctx in hits:
    w = re.search(r'[\wąćęłńóśźż]*I[\wąćęłńóśźż]*', ctx[40:])
    word = w.group(0) if w else '?'
    key = word
    if key in seen:
        continue
    seen.add(key)
    print('%-24s %s' % (word, repr(ctx)))
