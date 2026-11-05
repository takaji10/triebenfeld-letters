# -*- coding: utf-8 -*-
"""Trace parse_strip's walk for one page: strip line, para flag,
matched page line, decision."""
import json, os, re, sys, difflib
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947')
import structure2 as S

n = sys.argv[1] if len(sys.argv) > 1 else '0020'
d = json.load(open(os.path.join(S.OCR, n + '.json'), encoding='utf-8'))
lns = S.lines_of(d)
H = lns[-1]['top'] + 100
body_hs = sorted(l['h'] for l in lns if l['top'] < H * 0.45 and l['h'] >= 30)
BH = body_hs[len(body_hs) // 2] if body_hs else 80
foot = [l for l in lns if l['top'] > H * 0.45]
strip = S.strip_lines(n)
fseen = [l for l in foot if l['top'] >= strip['y0'] - 20]
assign = S.align(strip['lines'], fseen)
print('BH=%d, strip lines=%d, foot lines=%d' % (BH, len(strip['lines']), len(fseen)))
for i, sl in enumerate(strip['lines']):
    j, kind = assign.get(i, (None, 'none'))
    h = fseen[j]['h'] if j is not None else -1
    print('%2d p%d %-6s pg=%s h=%3d | %s' % (
        i, 1 if sl['para'] else 0, kind, j if j is not None else '-',
        h, sl['text'][:58]))
