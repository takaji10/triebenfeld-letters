# -*- coding: utf-8 -*-
"""Dump the rebuilt rows for inspection (num, src, top, text head)."""
import json, os, re, sys

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
rows = json.load(open(os.path.join(OCR, 'annex_rows2.json'),
                      encoding='utf-8'))
s = json.load(open(os.path.join(OCR, 'structure2.json'),
                   encoding='utf-8'))
for n in (sys.argv[1:] or ['0140', '0157', '0153', '0144', '0152']):
    print('===', n)
    for r in rows[n]:
        print('  n=%-4s %s top=%5d | %s' %
              (r['num'], r['src'][:12], r['y0'], r['text'][:66]))
    # the sheet's first lines (title?)
    print('  first lines:')
    for l in sorted(s[n]['lines'], key=lambda x: x['top'])[:4]:
        print('    %5d | %s' % (l['top'], l['text'][:70]))
    print()
