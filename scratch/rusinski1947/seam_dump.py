# -*- coding: utf-8 -*-
"""Seam context for the undecided pages: the two lines above the lead,
the lead, and the first stored note's first line - to see whether the
body sentence flows through the lead (class c) or breaks (a/b)."""
import json, os

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(os.path.join(OCR, 'structure2.json'),
                  encoding='utf-8'))

PAGES = ['0019', '0022', '0023', '0031', '0034', '0037', '0038', '0043',
         '0055', '0056', '0058', '0059', '0060', '0069', '0070', '0071',
         '0090', '0093', '0102', '0104', '0105', '0107', '0109', '0110',
         '0114', '0116', '0123', '0124', '0127']
for n in PAGES:
    page = s[n]
    notes = page['notes']
    first_top = min(x['top'] for x in notes)
    lines = page['lines']
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
    lt = tail[0]['top']
    above = [l for l in lines if l['top'] < lt]
    print('===', n)
    for l in above[-2:]:
        print('   ^ %5d h=%2d | %s' % (l['top'], l['h'], l['text'][:74]))
    for l in tail[:3]:
        print('   L %5d h=%2d | %s' % (l['top'], l['h'], l['text'][:74]))
    n0 = min(notes, key=lambda x: x['top'])
    print('   N1 %5d     | %s' % (n0['top'], n0['text'][:74].replace('\n', ' / ')))
    print()
