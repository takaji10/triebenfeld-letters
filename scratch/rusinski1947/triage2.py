# -*- coding: utf-8 -*-
"""Triage v2: compare the lead block's line heights with the page's
note-region type height (median h of lines at/below first note top).
lead_h <= note_h * 1.10  -> note-type lead (suspicious, needs the print)
otherwise               -> body-type lead (class c, no action)"""
import json, os, statistics

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
    nh = [l['h'] for l in lines if l['top'] >= first_top and l['h'] >= 35]
    note_h = statistics.median(nh) if nh else 50
    lead_hs = [l['h'] for l in tail if l['h'] >= 35]
    lead_med = statistics.median(lead_hs) if lead_hs else 0
    verdict = 'NOTE-TYPE' if lead_med and lead_med <= note_h * 1.10 \
        else 'body-type'
    print('%s  lead_med=%4.1f  note_h=%4.1f  -> %s  (%d lead lines)'
          % (n, lead_med, note_h, verdict, len(tail)))
