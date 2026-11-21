# -*- coding: utf-8 -*-
import json, os, re, sys, difflib
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947')
import structure2 as S

n = sys.argv[1] if len(sys.argv) > 1 else '0050'
d = json.load(open(os.path.join(S.OCR, n + '.json'), encoding='utf-8'))
lns = S.lines_of(d)
H = lns[-1]['top'] + 100
foot = [l for l in lns if l['top'] > H * 0.45]
strip = S.strip_lines(n)
assign = S.align(strip, foot)
for i, s in enumerate(strip[:14]):
    j, kind = assign.get(i, (None, 'none'))
    pj = foot[j]['text'][:40] if j is not None else '-'
    print(i, kind, 'pg=%s' % j, '| STR:', s['text'][:45])
    print('        | PG :', pj)
