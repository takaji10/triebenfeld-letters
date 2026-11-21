# -*- coding: utf-8 -*-
import sys
t = open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\literature\rusinski1947\original.md',
         encoding='utf-8').read()
for needle in ['Por. daty przypisu', 'nie mają nic wspólnego', 'Kremmer u. Dalchow, Provinz',
               'Vol. Leg. II, 982', 'Zupełnie wyjątkowo', 'Tak np. w przywileju z r. 1737']:
    i = t.find(needle)
    if i < 0:
        print(needle[:30], '-> NOT FOUND')
        continue
    print(needle[:30], '->', repr(t[max(0, i - 100):i + 100].replace('\n', ' / ')))
    print()
