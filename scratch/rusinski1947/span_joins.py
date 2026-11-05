# -*- coding: utf-8 -*-
"""Print the join candidates: the previous page's last note tail and
this page's lead-in head, so each spanning-note case is verified by
reading the sentence across the break."""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(os.path.join(OCR, 'structure2.json'),
                  encoding='utf-8'))
ORDER = sorted(s)

CANDS = ['0017', '0035', '0048', '0049', '0054', '0061', '0065', '0081',
         '0099', '0113', '0119', '0132', '0133']
for i, n in enumerate(ORDER):
    if n not in CANDS:
        continue
    notes = s[n]['notes']
    first_top = min(x['top'] for x in notes)
    lines = s[n]['lines']
    top3 = lines[:max(1, len(lines) // 3)]
    hs = sorted(l['h'] for l in top3 if l['h'] >= 30)
    BH = hs[min(len(hs) - 1, int(0.9 * len(hs)))] if hs else 80
    tail = []
    for l in reversed(lines):
        if l['top'] >= first_top:
            continue
        if l['h'] <= 0.88 * BH and l['h'] >= 25:
            tail.append(l)
        else:
            break
    tail.reverse()
    prev = None
    for j in range(i - 1, -1, -1):
        if s[ORDER[j]]['notes']:
            prev = ORDER[j]
            break
    pt = s[prev]['notes'][-1]['text'].rstrip() if prev else ''
    print('=== %s (prev %s)' % (n, prev))
    print('  PREV ends:  ...%s' % pt[-90:].replace('\n', ' / '))
    lead_text = ' '.join(l['text'] for l in tail)
    print('  LEAD (=%d lines): %s...' % (len(tail), lead_text[:130]))
    print('  JOIN: %s >>> %s' % (pt[-35:], lead_text[:55]))
    print()
