# -*- coding: utf-8 -*-
"""Trace parse_strip for one page: the work list, the branch decisions."""
import json, os, re, sys, difflib
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947')
import structure2 as S

n = sys.argv[1] if len(sys.argv) > 1 else '0043'
d = json.load(open(os.path.join(S.OCR, n + '.json'), encoding='utf-8'))
lns = S.lines_of(d)
H = lns[-1]['top'] + 100
body_hs = sorted(l['h'] for l in lns if l['top'] < H * 0.45 and l['h'] >= 30)
BH = body_hs[len(body_hs) // 2] if body_hs else 80
foot = [l for l in lns if l['top'] > H * 0.45]
strip = S.strip_lines(n)
fseen = [l for l in foot if l['top'] >= strip['y0'] - 20]
assign = S.align(strip['lines'], fseen)
claimed = {}
for i in sorted(assign):
    j, kind = assign[i]
    if kind == 'start' and j not in claimed:
        claimed[j] = i
work = []
for i, s in enumerate(strip['lines']):
    j, kind = assign.get(i, (None, 'none'))
    if kind == 'start' and j is not None and j + 1 < len(fseen) \
            and (j + 1) not in claimed:
        f_all = S.fold(s['text'])
        f1 = S.fold(fseen[j]['text'])
        f2 = S.fold(fseen[j + 1]['text'])
        if f_all and f1 and f2 and len(f_all) > len(f1) + 12:
            r1 = difflib.SequenceMatcher(None, f_all, f1).ratio()
            r12 = difflib.SequenceMatcher(
                None, f_all, (f1 + f2)[:len(f_all)]).ratio()
            if r12 >= 0.75 and r12 > r1 + 0.05:
                print('SPLIT at strip', i)
    work.append({'text': s['text'], 'para': s['para'], 'j': j,
                 'split': False})
# now walk manually for strip idx 8..12
for i in range(8, 13):
    s = work[i]
    j = s['j']
    l = s['text']
    small = j is not None and fseen[j].get('h', 0) <= 0.88 * BH
    smallish = j is not None and fseen[j].get('h', 0) <= 0.95 * BH
    md, ad, od = S.DIGIT.match(l), S.ARTIFACT.match(l), S.ONE.match(l)
    prev = work[i - 1]['text'] if i else ''
    prev_ok = bool(re.search(r'[.!?»:;][”"]?\s*$', prev))
    print(i, 'p%d' % s['para'], 'j=%s' % j, 'small=%s' % small,
          'md=%s ad=%s od=%s prev_ok=%s' % (bool(md), bool(ad), bool(od),
                                            prev_ok), '|', l[:50])
