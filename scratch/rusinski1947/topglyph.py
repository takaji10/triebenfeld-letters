# -*- coding: utf-8 -*-
"""Find top-aligned isolated glyphs (raised markers) in a y-range:
an x-bucket with ink in the top 40px of the line but no ink in the
x-height zone directly below it."""
import json, sys, io
from PIL import Image

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
n, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
s = json.load(open(OCR + '\\' + n.replace('tif', '') + '.json'
                   if False else OCR + '\\' + n + '.json', encoding='utf-8'))
# line tops from structure2
s2 = json.load(open(OCR + '\\structure2.json', encoding='utf-8'))
tops = sorted(l['top'] for l in s2[n]['lines'] if lo <= l['top'] < hi)
with open(r'C:\Users\Tersnaus\Downloads\tom5\tom5_%s.tif' % n, 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
px = im.load()
for lt in tops:
    zone_top = range(lt, lt + 40)
    zone_mid = range(lt + 45, lt + 90)
    print('--- line top', lt)
    prev = False
    for x in range(820, 3660, 4):
        d_top = sum(1 for y in zone_top for xx in range(x, x + 4)
                    if px[xx, y] < 128)
        d_mid = sum(1 for y in zone_mid for xx in range(x - 12, x + 16)
                    if px[xx, y] < 128)
        cur = d_top > 8 and d_mid == 0
        if cur and not prev:
            print('   isolated run start', x)
        if prev and not cur:
            print('   run end', x)
        prev = cur
