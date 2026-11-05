# -*- coding: utf-8 -*-
import sys
t = open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\literature\rusinski1947\original.md',
         encoding='utf-8').read()
i = t.find('[^8-1]:')
print('8-1:', t[i:i+700].replace('\n', ' / ')[:700])
print()
i = t.find('Kremmer u. Dalchow, Provinz')
print('Kremmer-in-body check:', repr(t[max(0, i - 120):i + 60].replace('\n', ' / ')))
print()
i = t.find('nie mają nic wspólnego')
print('wspólnego:', repr(t[max(0, i - 150):i + 60].replace('\n', ' / ')) if i >= 0 else 'NOT FOUND')
