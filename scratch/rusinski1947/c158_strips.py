# -*- coding: utf-8 -*-
"""Column strips for the c-table (0158 rows 1-9): render each column's
cells stacked top-to-bottom at high zoom for visual transcription."""
import io
from PIL import Image

with open(r'C:\Users\Tersnaus\Downloads\tom5\tom5_0158.tif', 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()

# text bands (from ink profile), r1..r9
BANDS = [(487, 645), (650, 810), (850, 1030), (1045, 1210),
         (1245, 1432), (1435, 1595), (1618, 1780), (1782, 1945),
         (1950, 2140)]
BOUNDS = [821, 1019, 1885, 2379, 2930, 3211, 3708, 4206, 4545, 4810,
          5039, 5268, 5388]
COLS = {'nazwa': (1, 2), 'parafia': (2, 3), 'dzis': (3, 4),
        'rokchar': (4, 6), 'zrodlo': (6, 7), 'data': (7, 8),
        'dymy': (8, 9)}
GROUPS = [('A', 'nazwa', (1, 5)), ('B', 'nazwa', (6, 9)),
          ('C', 'parafia', (1, 5)), ('D', 'parafia', (6, 9)),
          ('E', 'dzis', (1, 5)), ('F', 'dzis', (6, 9)),
          ('G', 'rokchar', (1, 5)), ('H', 'rokchar', (6, 9)),
          ('I', 'zrodlo', (1, 5)), ('J', 'zrodlo', (6, 9)),
          ('K', 'data', (1, 5)), ('L', 'data', (6, 9)),
          ('M', 'dymy', (1, 9))]
for tag, col, (r0, r1) in GROUPS:
    ci, cj = COLS[col]
    x0, x1 = BOUNDS[ci] + 3, BOUNDS[cj] - 3
    crops = []
    for num in range(r0, r1 + 1):
        y0, y1 = BANDS[num - 1]
        crops.append(im.crop((x0, y0, x1, y1)))
    w = x1 - x0
    target = 1500
    sc = target / w
    H = sum(int(c.size[1] * sc) + 14 for c in crops)
    out = Image.new('L', (target + 20, H + 10), 255)
    yy = 5
    for c in crops:
        c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)),
                     Image.LANCZOS)
        out.paste(c, (10, yy))
        yy += c.size[1] + 14
    out.save(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode'
             r'\c158_%s.png' % tag)
    print(tag, col, r0, r1, out.size)
