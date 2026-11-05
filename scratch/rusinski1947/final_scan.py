# -*- coding: utf-8 -*-
import re
t = open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\literature\rusinski1947\original.md',
         encoding='utf-8').read()
ms = re.findall(r'.{0,30}\b\d{1,3}\s*[%9§]\s*/[,.;:].{0,15}', t)
print('pct_art remaining:', len(ms))
for m in ms:
    print('  ', repr(m[:80]))
print('slash_comma:', t.count('/,'))
for needle in ['750/y', '13.6%%', 'conajmniej 75']:
    print(needle, '->', t.count(needle))
