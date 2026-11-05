# -*- coding: utf-8 -*-
"""Line maps for the spanning-note repairs."""
import json, os, re, sys

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(os.path.join(OCR, 'structure2.json'),
                  encoding='utf-8'))
for spec in sys.argv[1:]:
    n, lo, hi = spec.split(':')
    print('===', n, 'lines', lo, '-', hi,
          '| first note top:', min((x['top'] for x in s[n]['notes']),
                                   default=None))
    for l in s[n]['lines']:
        if int(lo) < l['top'] < int(hi):
            print(' %5d h=%2d | %s' % (l['top'], l['h'], l['text'][:76]))
    print()
