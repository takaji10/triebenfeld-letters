# -*- coding: utf-8 -*-
"""Per-page audit report: body lines + markers + note one-liners."""
import json, sys

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(OCR + r'\structure4.json', encoding='utf-8'))
mk = json.load(open(OCR + r'\markers.json', encoding='utf-8'))

for n in sys.argv[1:]:
    page = s[n]
    tops = [x['top'] for x in page['notes'] if x['top'] is not None]
    note_top = min(tops) if tops else None
    print('=====', n, 'note_top', note_top, '| notes:', len(page['notes']))
    for i, nt in enumerate(page['notes']):
        print('  n%d @%s %s' % (i + 1, nt['top'], nt['text'][:85]))
    for m in mk.get(n, []):
        print('  MK %s @%s %-14r %s nc=%s' % (m['label'], m['top'],
              m['tok'], m['kind'], m.get('num_ctx')))
    for l in sorted(page['lines'], key=lambda x: x['top']):
        if note_top is not None and l['top'] >= note_top:
            continue
        t = l['text']
        if t.strip():
            print('  b%5d %s' % (l['top'], t[:110]))
