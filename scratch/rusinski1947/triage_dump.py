# -*- coding: utf-8 -*-
"""Full triage dump for the 49 lead-in pages: the lead block's lines,
the first stored note's opening, and the previous page's last-note tail -
to split the leads into (a) runover, (b) missed note, (c) small body."""
import json, os, re, difflib

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(os.path.join(OCR, 'structure2.json'),
                  encoding='utf-8'))
ORDER = sorted(s)

for i, n in enumerate(ORDER):
    page = s[n]
    notes = page['notes']
    if not notes:
        continue
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
    if not tail:
        continue
    prev = None
    for j in range(i - 1, -1, -1):
        if s[ORDER[j]]['notes']:
            prev = ORDER[j]
            break
    pt = s[prev]['notes'][-1]['text'].rstrip()[-100:] if prev else ''
    print('=== %s  lead=%d  first-note-top=%d' % (n, len(tail), first_top))
    for l in tail:
        print('   L %5d h=%2d | %s' % (l['top'], l['h'], l['text'][:78]))
    print('   PREV-TAIL: ...%s' % pt[-95:].replace('\n', ' / '))
    print()
