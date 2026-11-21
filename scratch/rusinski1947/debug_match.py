# -*- coding: utf-8 -*-
import json, sys, os, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947')
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
import structure2 as S

n = sys.argv[1] if len(sys.argv) > 1 else '0020'
d = json.load(open(os.path.join(OCR, n + '.json'), encoding='utf-8'))
lns = S.lines_of(d)
H = lns[-1]['top'] + 100
foot = [l for l in lns if l['top'] > H * 0.45]
wstarts = S.strip_openings(n)
print('openings:', len(wstarts))
for i, s in enumerate(wstarts[:4]):
    f = S.fold(s['text'])[:20]
    print(i, 'read=%s' % s.get('read'), 'fold=', f)
    for l in foot:
        lt = re.sub(r'^[\d!%*+$§£|.,)»\s\-—–]+', '', l['text'])
        lf = S.fold(lt)[:20]
        if len(lf) >= 8 and min(len(lf), len(f)) >= 8 and \
                (lf.startswith(f) or f.startswith(lf)):
            print('    MATCH', l['top'], 'h=%d' % l['h'], '|',
                  l['text'][:60])
