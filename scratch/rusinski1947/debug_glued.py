# -*- coding: utf-8 -*-
import json, os, re, sys, difflib
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947')
import structure2 as S

n = '0024'
d = json.load(open(os.path.join(S.OCR, n + '.json'), encoding='utf-8'))
lns = S.lines_of(d)
H = lns[-1]['top'] + 100
body_hs = sorted(l['h'] for l in lns if l['top'] < H * 0.45 and l['h'] >= 30)
BH = body_hs[len(body_hs) // 2] if body_hs else 80
foot = [l for l in lns if l['top'] > H * 0.45]
strip = S.strip_lines(n)
fseen = [l for l in foot if l['top'] >= strip['y0'] - 20]
assign = S.align(strip['lines'], fseen)
i = 11
sl = strip['lines'][i]
l = sl['text']
j, kind = assign.get(i, (None, 'none'))
print('line:', repr(l[:60]))
print('kind:', kind, 'j:', j, 'h:', fseen[j]['h'] if j is not None else None)
print('BH:', BH, '0.88*BH:', 0.88 * BH)
small = j is not None and fseen[j].get('h', 0) <= 0.88 * BH
print('small:', small)
md = S.DIGIT.match(l)
ad = S.ARTIFACT.match(l)
od = S.ONE.match(l)
print('md:', bool(md), 'ad:', bool(ad), 'od:', bool(od))
go = re.match(r'^[lI1¡|U]([A-ZĄĆĘŁŃÓŚŹŻ]\S*)\s+(.*)$', l)
print('go:', bool(go), go.group(1)[:20] if go else '')
