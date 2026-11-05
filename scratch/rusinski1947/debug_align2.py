# -*- coding: utf-8 -*-
import json, os, re, sys, difflib
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947')
import structure2 as S

n = sys.argv[1] if len(sys.argv) > 1 else '0097'
d = json.load(open(os.path.join(S.OCR, n + '.json'), encoding='utf-8'))
lns = S.lines_of(d)
H = lns[-1]['top'] + 100
body_hs = sorted(l['h'] for l in lns if l['top'] < H * 0.45 and l['h'] >= 30)
BH = body_hs[len(body_hs) // 2] if body_hs else 80
foot = [l for l in lns if l['top'] > H * 0.45]
strip = S.strip_lines(n)
fseen = [l for l in foot if l['top'] >= strip['y0'] - 20]
assign = S.align(strip['lines'], fseen)
for i, s in enumerate(strip['lines'][:16]):
    j, kind = assign.get(i, (None, 'none'))
    pj = fseen[j]['text'][:38] if j is not None else '-'
    ph = fseen[j]['h'] if j is not None else 0
    print(i, kind, 'pg=%d h=%d' % (j or -1, ph), '|', s['text'][:52])
    print('      pg:', pj)
