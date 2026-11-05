# -*- coding: utf-8 -*-
import sys
t = open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\literature\rusinski1947\original.md',
         encoding='utf-8').read()
needle = 'typu '
i = t.find(needle)
print(repr(t[max(0, i - 250):i + 400]))
