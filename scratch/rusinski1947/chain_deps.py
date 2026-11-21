# -*- coding: utf-8 -*-
import re, os
D = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947'
for f in ('markers3.py', 'marked_lines.py', 'compose.py'):
    t = open(os.path.join(D, f), encoding='utf-8').read()
    print('=====', f)
    for mm in re.finditer(r'spath\s*=\s*(.{0,100})', t):
        print('  spath =', mm.group(1).strip())
    for mm in re.finditer(r"'structure[^']*'", t):
        print('  mentions:', mm.group(0))
    for mm in re.finditer(r"'(?:marked_lines|markers|annex_table|pct_frac)[^']*'", t):
        print('  mentions:', mm.group(0))
