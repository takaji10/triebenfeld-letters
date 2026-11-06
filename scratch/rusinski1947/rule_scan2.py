# -*- coding: utf-8 -*-
"""Detect the vertical table rules per annex sheet: an x is a rule when
it is dark for nearly the whole table y-range (rules are continuous;
text columns are not)."""
import json, os, io
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
at = json.load(open(os.path.join(OCR, 'annex_table.json'), encoding='utf-8'))

for n in sorted(at):
    rows = at[n]['rows']
    nums = sorted(int(k) for k in rows if k.isdigit())
    y_lo = min((rows[str(k)]['y'][0] for k in nums), default=1000)
    y_hi = max((rows[str(k)]['y'][1] for k in nums), default=3200)
    fn = os.path.join(SRC, 'tom5_%s.tif' % n)
    with open(fn, 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    px = im.load()
    W, H = im.size
    step = 3
    ys = list(range(y_lo, y_hi, step))
    n_y = len(ys)
    out = []
    for x in range(200, W - 10, 2):
        dark = sum(1 for y in ys if px[x, y] < 160)
        if dark / n_y > 0.92:
            out.append(x)
    runs = []
    for x in out:
        if runs and x - runs[-1] <= 10:
            runs[-1] = (runs[-1] + x) // 2
        else:
            runs.append(x)
    print(n, 'y%d-%d:' % (y_lo, y_hi), runs)
