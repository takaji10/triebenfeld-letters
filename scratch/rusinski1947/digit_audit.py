# -*- coding: utf-8 -*-
"""Audit the ANEKS I sheets against the print's own number column:
ink bands inside the number cell (between the first two rules) are the
rows' printed digits. A data-row span must contain exactly one band;
bands outside all spans = missed rows; spans with 2+ bands = missed
boundaries; spans with 0 bands = phantom spans."""
import json, os, io
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                   encoding='utf-8'))
cells = json.load(open(os.path.join(OCR, 'annex_cells.json'),
                       encoding='utf-8'))

for n in sorted(at):
    rows = at[n]['rows']
    nums = sorted(int(k) for k in rows if k.isdigit())
    if not nums:
        continue
    y_lo = min(rows[str(k)]['y'][0] for k in nums)
    y_hi = max(rows[str(k)]['y'][1] for k in nums)
    fn = os.path.join(SRC, 'tom5_%s.tif' % n)
    with open(fn, 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    px = im.load()
    # the sheet's number-cell interior from the fitted rules
    sh = cells.get(n)
    if not sh:
        print(n, 'NO CELLS')
        continue
    first = sh[str(nums[0])].get('_rules')
    # rules were not stored per sheet - recompute from the fit inputs:
    # use the x-band from the first row's cells? fall back to a fixed
    # window derived from the cell OCR column 0 (Lp) - recompute rules
    # here instead (same predicate as annex_cells.detect/fit)
    sys_path = r'C:\Users\Tersnaus\.local\share\opencode\worktree' \
               r'\14ffba\rusinski1947\scratch\rusinski1947'
    import sys
    sys.path.insert(0, sys_path)
    from annex_cells import detect, fit
    im2, runs = detect(n, y_lo, y_hi)
    got = fit(runs)
    rules = got[1] if got else runs
    x0, x1 = int(rules[0]) + 14, int(rules[1]) - 8
    bands = []
    prev = False
    for y in range(y_lo, y_hi, 3):
        dark = sum(1 for x in range(x0, x1, 2) if px[x, y] < 150)
        cur = dark > 5
        if cur and not prev:
            a = y
        if prev and not cur:
            if y - a >= 9:
                bands.append((a, y))
            prev = cur
            continue
        prev = cur
    # merge close bands
    merged = []
    for b in bands:
        if merged and b[0] - merged[-1][1] < 40:
            merged[-1] = (merged[-1][0], b[1])
        else:
            merged.append(list(b))
    spans = [(num, rows[str(num)]['y']) for num in nums]
    probs = []
    used = [False] * len(merged)
    for num, (sy0, sy1) in spans:
        inside = [i for i, (b0, b1) in enumerate(merged)
                  if sy0 <= b0 < sy1]
        for i in inside:
            used[i] = True
        if not inside:
            probs.append('slot %d y%s: NO digit band' % (num, (sy0, sy1)))
        elif len(inside) > 1:
            probs.append('slot %d y%s: %d bands %s (missed boundary?)'
                         % (num, (sy0, sy1), len(inside), inside))
    for i, (b0, b1) in enumerate(merged):
        if not used[i]:
            probs.append('band y%d-%d outside all slots (MISSED ROW)'
                         % (b0, b1))
    print(n, 'bands %d slots %d' % (len(merged), len(spans)),
          ('OK' if not probs else ''))
    for p in probs:
        print('   ', p)
