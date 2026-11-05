# -*- coding: utf-8 -*-
"""Per-candidate dump: stored notes vs lead lines, for adjudication."""
import json, os, re, sys

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(os.path.join(OCR, 'structure2.json'),
                  encoding='utf-8'))
ORDER = sorted(s)

for n in sys.argv[1:]:
    notes = s[n]['notes']
    first_top = min(x['top'] for x in notes) if notes else None
    lines = s[n]['lines']
    top3 = lines[:max(1, len(lines) // 3)]
    hs = sorted(l['h'] for l in top3 if l['h'] >= 30)
    BH = hs[min(len(hs) - 1, int(0.9 * len(hs)))] if hs else 80
    tail = []
    if first_top:
        for l in reversed(lines):
            if l['top'] >= first_top:
                continue
            if l['h'] <= 0.88 * BH and l['h'] >= 25:
                tail.append(l)
            else:
                break
        tail.reverse()
    print('===', n, '| notes:', len(notes))
    for x in notes[:3]:
        print('   note %d top=%s | %s' % (x['num'], x['top'],
                                          x['text'][:55]))
    print('   LEAD lines:', len(tail))
    for l in tail[:4]:
        print('     %d h=%d | %s' % (l['top'], l['h'], l['text'][:70]))
    # the line above the lead
    if tail:
        lt = tail[0]['top']
        above = [l for l in lines if l['top'] < lt]
        if above:
            a = above[-1]
            print('   ABOVE: %d h=%d | %s' % (a['top'], a['h'],
                                              a['text'][:70]))
    print()
