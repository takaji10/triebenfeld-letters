# -*- coding: utf-8 -*-
"""Raised-glyph sweep across a page's body: for every structure line,
find x-runs with ink in the ascender zone and NO ink in the x-height
zone beneath (candidate raised markers). Prints line top + runs."""
import json, sys, io
from PIL import Image

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
n = sys.argv[1]
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 560
hi = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9
s = json.load(open(OCR + r'\structure4.json', encoding='utf-8'))
tops = [x['top'] for x in s[n]['notes'] if x['top'] is not None]
note_top = min(tops) if tops else None
with open(r'C:\Users\Tersnaus\Downloads\tom5\tom5_%s.tif' % n, 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
px = im.load()
for l in sorted(s[n]['lines'], key=lambda x: x['top']):
    lt = l['top']
    if lt < lo or (note_top is not None and lt >= note_top):
        continue
    if not l['text'].strip():
        continue
    runs = []
    prev = False
    for x in range(820, 3660, 3):
        dt = sum(1 for y in range(lt - 6, lt + 32) for xx in range(x, x + 3)
                 if px[xx, y] < 160)
        dm = sum(1 for y in range(lt + 38, lt + 78)
                 for xx in range(x - 9, x + 12) if px[xx, y] < 160)
        cur = dt > 5 and dm == 0
        if cur and not prev:
            a = x
        if prev and not cur:
            if x - a >= 6:
                runs.append((a, x))
        prev = cur
    if runs:
        print('line %5d %-70s %s' % (lt, l['text'][:66], runs))
