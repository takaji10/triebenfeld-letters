# -*- coding: utf-8 -*-
import re, os
D = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947'
for f in ('note_apply.py', 'note_polish.py', 'markers3.py',
          'marked_lines.py', 'compose.py'):
    t = open(os.path.join(D, f), encoding='utf-8').read()
    print('=====', f, len(t), 'chars')
    m = re.search(r'"""(.*?)"""', t, re.S)
    if m:
        print(m.group(1).strip()[:350])
    for mm in re.finditer(r'(?:open|json\.load|json\.dump)\((.{0,90})', t):
        print('   ', mm.group(1).replace('\n', ' '))
