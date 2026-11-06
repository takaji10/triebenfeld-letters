# -*- coding: utf-8 -*-
"""Digit-ish tokens in the page-pass TSV for a y-range (marker hunt)."""
import json, re, sys

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
n, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
d = json.load(open(OCR + '\\' + n + '.json', encoding='utf-8'))
ws = [w for w in d['words'] if w[5].strip() and lo < w[1] < hi]
ws.sort(key=lambda w: (w[1], w[0]))
for w in ws:
    t = w[5].strip()
    if re.search(r'\d', t) or re.fullmatch(r'[*?$§£?"\']+|»|„|”', t) \
            or re.fullmatch(r'[lI|ZzsS]"?,?', t):
        print('x=%4d y=%4d w=%3d h=%3d | %r' % (w[0], w[1], w[2], w[3], t))
