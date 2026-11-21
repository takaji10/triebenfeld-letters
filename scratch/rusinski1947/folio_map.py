# -*- coding: utf-8 -*-
"""Folio-drift map: find the printed folio in each body scan's
running-head band (top ~y300) and compare with label(n) = n-15."""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
for i in list(range(16, 138)):
    n = '%04d' % i
    p = os.path.join(OCR, n + '.json')
    if not os.path.isfile(p):
        continue
    d = json.load(open(p, encoding='utf-8'))
    ws = d['words']
    # folio candidates: standalone 1-3 digit tokens in the top band
    cands = [w[5] for w in ws if w[1] < 420 and re.fullmatch(r'\d{1,3}', w[5])]
    # also bottom band
    ymax = max(w[3] for w in ws) if ws else 0
    cands_b = [w[5] for w in ws if w[1] > ymax - 420
               and re.fullmatch(r'\d{1,3}', w[5])]
    print('%s label=%3d top=%s bottom=%s' % (n, i - 15, cands[:4],
                                             cands_b[:4]))
