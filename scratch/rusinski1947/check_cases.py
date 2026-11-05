# -*- coding: utf-8 -*-
import sys
t = open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\literature\rusinski1947\original.md',
         encoding='utf-8').read()
for needle in ['najczęściej', '608 morg', '60 morg', 'wynosiła  ', 'wynos ła',
               'typu „olęderskiego', 'zwiększyła się tylko o', 'co 4 tygodnie',
               'co 2 tygodnie', 'od 30 do 70', '301 do 70']:
    i = t.find(needle)
    if i < 0:
        print(needle[:28], '-> NOT FOUND')
        continue
    print(needle[:28], '->', repr(t[max(0, i - 90):i + 130].replace('\n', ' / ')))
    print()
