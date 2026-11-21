# -*- coding: utf-8 -*-
"""Generate spot crops for the current residue - GENEROUS context:
~1000px of surrounding sheet height per item (neighbour rows, Lp
numbers, headers visible), full table width."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import SRC
import digit_read
from PIL import Image

at = digit_read.at
OUT = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba' \
      r'\rusinski1947\literature\rusinski1947\spot_crops'
os.makedirs(OUT, exist_ok=True)
SHEET_H = 5936


def band(n, num):
    y0, y1 = at[n]['rows'][str(num)]['y']
    return y0 - 20, y1 + 30


ims = {}


def get(n):
    if n not in ims:
        with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
            im = Image.open(io.BytesIO(fh.read())).convert('L')
        im.load()
        ims[n] = im
    return ims[n]


def save(name, n, ya, yb):
    im = get(n)
    ya = max(0, ya)
    yb = min(SHEET_H, yb)
    c = im.crop((700, ya, 5300, yb))
    sc = 2800.0 / c.size[0]
    c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)), Image.LANCZOS)
    c.save(os.path.join(OUT, name + '.png'))
    print(name, (ya, yb), '->', c.size)


# (name, sheet, rows, pad)  - pad = extra height beyond the row band
ITEMS = [
    ('S23_a_totals_0146', '0146', (99, 111), 700),
    ('S24_b_totals_0157', '0157', (150, 156), 700),
    ('S25_marks_0140', '0140', (14, 18), 300),
    ('S26_mark_0139_r8', '0139', (6, 10), 420),
    ('S27_notes_0140', '0140', (29, 29), 900),
    ('S28_0147_r5', '0147', (4, 6), 420),
    ('S29_0148_r18_r24', '0148', (18, 24), 420),
    ('S30_0151_r68', '0151', (67, 69), 420),
    ('S31_0154_r105', '0154', (105, 107), 420),
    ('S32_0154_r109_r115', '0154', (108, 115), 420),
    ('S33_0157_r146', '0157', (146, 148), 420),
    ('S34_0158_r1_r5', '0158', (1, 5), 420),
    ('S35_0159_r10', '0159', (10, 11), 420),
]
for name, n, nums, pad in ITEMS:
    ya = min(band(n, k)[0] for k in nums) - pad
    yb = max(band(n, k)[1] for k in nums) + pad
    save(name, n, ya, yb)
