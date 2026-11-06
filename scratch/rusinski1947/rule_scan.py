# -*- coding: utf-8 -*-
"""Per-sheet vertical-rule candidates for the annex sheets."""
import json, os, io
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(os.path.join(OCR, 'structure2.json'), encoding='utf-8'))
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
    for th in (250, 400):
        cols = []
        for x in range(200, W - 10, 2):
            dark = sum(1 for y in range(y_lo, y_hi, 4) if px[x, y] < 150)
            if dark > th:
                cols.append(x)
        runs = []
        for x in cols:
            if runs and x - runs[-1] <= 8:
                runs[-1] = (runs[-1] + x) // 2
            else:
                runs.append(x)
        print(n, 'y%d-%d th%d:' % (y_lo, y_hi, th), runs)
