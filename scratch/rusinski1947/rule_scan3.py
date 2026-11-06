# -*- coding: utf-8 -*-
"""Adaptive per-sheet rule detection: lower the count threshold until a
rule ladder emerges; each candidate must also be fairly continuous."""
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
    ys = list(range(y_lo, y_hi, 3))
    n_y = len(ys)
    best = None
    for th in (280, 220, 170, 130, 100):
        cols = []
        for x in range(200, W - 10, 2):
            dark = sum(1 for y in ys if px[x, y] < 160)
            frac = dark / n_y
            if dark > th and frac > 0.55:
                cols.append(x)
        runs = []
        for x in cols:
            if runs and x - runs[-1] <= 10:
                runs[-1] = (runs[-1] + x) // 2
            else:
                runs.append(x)
        if len(runs) >= 8:
            best = (th, runs)
            break
    print(n, best)
