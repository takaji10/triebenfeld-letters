# -*- coding: utf-8 -*-
"""Inventory the table-footnote lines printed below each annex sheet's
table (structure4 lines whose left margin sits at the note indent after
the last table row)."""
import json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(OCR + r'\structure4.json', encoding='utf-8'))
at = json.load(open(OCR + r'\annex_table.json', encoding='utf-8'))

for n in sorted(at):
    rows = at[n]['rows']
    nums = [int(k) for k in rows if k.isdigit()]
    if not nums:
        continue
    y_end = max(rows[str(k)]['y'][1] for k in nums)
    # notes start below the table + a gap; note lines start near x1140
    cand = [l for l in s[n]['lines'] if l['top'] > y_end + 40]
    if not cand:
        continue
    print('=== sheet', n, 'table ends y', y_end)
    for l in sorted(cand, key=lambda x: x['top']):
        left = l.get('left', -1)
        tag = 'NOTE' if 1100 <= left <= 1180 else '    '
        print('  %s y%-5d left=%-5d %r' % (tag, l['top'], left,
                                           l['text'][:100]))
