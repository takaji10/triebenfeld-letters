# -*- coding: utf-8 -*-
"""All page-pass word boxes in a y-range (line inspection)."""
import json, sys

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
n, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
d = json.load(open(OCR + '\\' + n + '.json', encoding='utf-8'))
ws = [w for w in d['words'] if w[5].strip() and lo < w[1] < hi]
ws.sort(key=lambda w: (w[1], w[0]))
for w in ws:
    print('x=%4d y=%4d w=%3d h=%3d | %r' % (w[0], w[1], w[2], w[3], w[5].strip()))
