# -*- coding: utf-8 -*-
import re
p = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947\annex_rows2.py'
t = open(p, encoding='utf-8').read()
m = re.search(r'def cell_cands.*?\n\n\n', t, re.S)
block = m.group(0)
t = t.replace(block, '')
anchor = '        imgs[n].load()\n    return imgs[n]\n\n\n'
t = t.replace(anchor, anchor + block, 1)
open(p, 'w', encoding='utf-8').write(t)
print('moved cell_cands after img()')
