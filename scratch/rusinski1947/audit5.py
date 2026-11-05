# -*- coding: utf-8 -*-
"""State for the five editor marker pages: markers.json entries,
structure2 lines around the anchors, note counts."""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(OCR + r'\structure2.json', encoding='utf-8'))
mk = json.load(open(OCR + r'\markers.json', encoding='utf-8'))
for n in ('0058', '0083', '0093', '0101', '0113'):
    print('===', n, '| notes:', len(s[n]['notes']),
          '| markers:', len(mk.get(n, [])))
    for m in mk.get(n, []):
        print('   %s top=%5d tok=%-10r kind=%s nc=%s' %
              (m['label'], m['top'], m['tok'], m['kind'], m['num_ctx']))
    ft = min(x['top'] for x in s[n]['notes'])
    print('   note tops:', [x['top'] for x in s[n]['notes']])
    print('   first note top:', ft)
    print()
