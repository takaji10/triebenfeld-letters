# -*- coding: utf-8 -*-
"""Date-cell image strips: for each flagged date cell render the cell
crop at 6x into a batch image (one strip per cell, labeled) for direct
visual reading."""
import sys, os, json, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from annex_cells import detect, fit
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                   encoding='utf-8'))

targets = []
for ln in open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode'
               r'\noise1.txt', encoding='utf-8'):
    import re
    m = re.match(r'(\d+) r(\d+) c(\d+) (.*)$', ln)
    if m and int(m.group(3)) == 7:
        targets.append((m.group(1), int(m.group(2)),
                        m.group(4).strip()))

ims = {}
rules_c = {}
BATCH = 8
for bi in range(0, len(targets), BATCH):
    grp = targets[bi:bi + BATCH]
    H = 150
    W = 760
    out = Image.new('L', (W * 2 + 30, (H + 6) * len(grp) + 10), 255)
    for i, (n, num, ctx) in enumerate(grp):
        if n not in ims:
            rows = at[n]['rows']
            nums = sorted(int(k) for k in rows if k.isdigit())
            y_lo = min(rows[str(k)]['y'][0] for k in nums)
            y_hi = max(rows[str(k)]['y'][1] for k in nums)
            im, runs = detect(n, y_lo, y_hi)
            got = fit(runs)
            rules = got[1] if got else runs
            ims[n] = im
            rules_c[n] = rules
        im = ims[n]
        rules = rules_c[n]
        bounds = rules + [rules[-1] + 120]
        y0, y1 = at[n]['rows'][str(num)]['y']
        # the date cell = column 7 (x between rules 7 and 8), wide
        # margin left (the data column's label can wrap)
        c = im.crop((int(bounds[7]) + 6, y0 + 2, int(bounds[9]) - 6,
                     y1 - 2))
        sc = min(W / c.size[0], 1.1)
        c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)),
                     Image.LANCZOS)
        out.paste(c, (10, 5 + i * (H + 6)))
    out.save(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode'
             r'\datestrip_%02d.png' % (bi // BATCH))
    print('wrote batch', bi // BATCH, len(grp))
