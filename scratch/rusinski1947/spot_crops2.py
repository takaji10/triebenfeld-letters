# -*- coding: utf-8 -*-
"""Generate spot crops for the current (post-noise-pass) residue:
sum/mark items + the 15 deep-garble text cells (grouped per cluster)."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import SRC
import digit_read
from PIL import Image

at = digit_read.at
OUT = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba' \
      r'\rusinski1947\literature\rusinski1947\spot_crops'
os.makedirs(OUT, exist_ok=True)

# (name, sheet, y0, y1) - full-width band crops, 3x
ITEMS = [
    ('S23_a_totals_0146',   '0146', 3560, 3980),
    ('S24_b_totals_0157',   '0157', 3400, 3900),
    ('S25_marks_0140',      '0140', 540, 660),
    ('S26_mark_0139_r8',    '0139', 2430, 2570),
    ('S27_notes_0140',      '0140', 3240, 3560),
    ('S28_0147_r5',         '0147', None, None),   # r5 band
    ('S29_0148_r18_r24',    '0148', None, None),   # r18..r24
    ('S30_0151_r68',        '0151', None, None),   # r68 band
    ('S31_0154_r105',       '0154', None, None),   # r105 band
    ('S32_0154_r109_r115',  '0154', None, None),   # r109..r115
    ('S33_0157_r146',       '0157', None, None),   # r146 band
    ('S34_0158_r1_r5',      '0158', None, None),   # r1..r5
    ('S35_0159_r10',        '0159', None, None),   # r10 band
]


def band(n, num):
    y0, y1 = at[n]['rows'][str(num)]['y']
    return y0 - 20, y1 + 30


ims = {}
for name, n, ya, yb in ITEMS:
    if ya is None:
        continue
    if n not in ims:
        with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
            im = Image.open(io.BytesIO(fh.read())).convert('L')
        im.load()
        ims[n] = im
    im = ims[n]
    c = im.crop((860, ya, 5300, yb))
    sc = min(2400.0 / c.size[0], 3.0)
    c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)), Image.LANCZOS)
    c.save(os.path.join(OUT, name + '.png'))
    print(name, c.size)

# row-band items
for name, n, nums, in (
        ('S28_0147_r5', '0147', (5,)),
        ('S29_0148_r18_r24', '0148', (18, 24)),
        ('S30_0151_r68', '0151', (68,)),
        ('S31_0154_r105', '0154', (105,)),
        ('S32_0154_r109_r115', '0154', (109, 110, 111, 115)),
        ('S33_0157_r146', '0157', (146,)),
        ('S34_0158_r1_r5', '0158', (1, 2, 5)),
        ('S35_0159_r10', '0159', (10,))):
    if n not in ims:
        with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
            im = Image.open(io.BytesIO(fh.read())).convert('L')
        im.load()
        ims[n] = im
    im = ims[n]
    ya = min(band(n, k)[0] for k in nums)
    yb = max(band(n, k)[1] for k in nums)
    c = im.crop((860, ya, 5300, yb))
    sc = min(2400.0 / c.size[0], 3.0)
    c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)), Image.LANCZOS)
    c.save(os.path.join(OUT, name + '.png'))
    print(name, c.size)
