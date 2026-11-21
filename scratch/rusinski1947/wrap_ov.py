# -*- coding: utf-8 -*-
"""Wrap the alignment + dispute-loop region in 'if n not in OVERRIDES:'
and add the override-hint numbering pass."""
p = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947\annex_rows2.py'
lines = open(p, encoding='utf-8').readlines()
i0 = next(i for i, l in enumerate(lines)
          if l.strip().startswith('# pre-first-hint alignment'))
i1 = next(i for i, l in enumerate(lines)
          if l.strip().startswith("state['prev'] = p0"))
block = lines[i0:i1]
indented = ['    ' + l if l.strip() else l for l in block]
lines[i0:i1] = ['    if n not in OVERRIDES:\n'] + indented
# the override-hint pass before the state update
ins = """    if n in OVERRIDES:
        p = p0
        for r in rows:
            if r['num'] is None:
                continue
            if r['src'] == 'override' and r['hint'] is not None:
                p = r['hint']
                r['num'] = r['hint']
            else:
                p += 1
                r['num'] = p
"""
lines.insert(i1, ins)
open(p, 'w', encoding='utf-8').writelines(lines)
print('wrapped + override pass inserted')
