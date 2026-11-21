# -*- coding: utf-8 -*-
"""Match the c-table's superscript row marks against the footnote-leading
digits by normalized pixel correlation (both rendered from the same
print, same bold style)."""
import io
from PIL import Image

with open(r'C:\Users\Tersnaus\Downloads\tom5\tom5_0158.tif', 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
px = im.load()

BANDS = {1: (487, 645), 2: (650, 810), 3: (850, 1030), 4: (1045, 1210),
         5: (1245, 1432), 6: (1435, 1595), 7: (1618, 1780),
         8: (1782, 1945), 9: (1950, 2140)}
marks = {1: (1335, 1357, 525, 555), 2: (1630, 1651, 703, 732),
         3: (1369, 1391, 898, 930), 4: (1617, 1639, 1096, 1127),
         5: (1449, 1471, 1292, 1323), 6: (1363, 1384, 1486, 1517),
         7: (1561, 1580, 1663, 1692), 8: (1355, 1377, 1908, 1938),
         9: (1735, 1757, 2081, 2111)}
notes = {1: (1140, 1159, 2309, 2341), 2: (1144, 1166, 2380, 2413),
         3: (1143, 1166, 2522, 2555), 4: (1140, 1163, 2592, 2625),
         5: (1146, 1169, 2734, 2766), 6: (1141, 1168, 2873, 2905),
         7: (1138, 1170, 2944, 2976)}

def grid(x0, x1, y0, y1, W=20, H=28):
    gw = []
    for gy in range(H):
        row = []
        for gx in range(W):
            xa = x0 + (x1 - x0) * gx / W
            xb = x0 + (x1 - x0) * (gx + 1) / W
            ya = y0 + (y1 - y0) * gy / H
            yb = y0 + (y1 - y0) * (gy + 1) / H
            n = tot = 0
            for x in range(int(xa), max(int(xa) + 1, int(xb))):
                for y in range(int(ya), max(int(ya) + 1, int(yb))):
                    tot += 1
                    if px[x, y] < 170:
                        n += 1
            row.append(n / max(tot, 1))
        gw.append(row)
    return gw

def corr(a, b):
    ma = sum(sum(r) for r in a) / (len(a) * len(a[0]))
    mb = sum(sum(r) for r in b) / (len(b) * len(b[0]))
    num = den_a = den_b = 0.0
    for i in range(len(a)):
        for j in range(len(a[0])):
            num += (a[i][j] - ma) * (b[i][j] - mb)
            den_a += (a[i][j] - ma) ** 2
            den_b += (b[i][j] - mb) ** 2
    return num / ((den_a ** .5) * (den_b ** .5) + 1e-9)

ng = {k: grid(*v) for k, v in notes.items()}
for num in sorted(marks):
    mg = grid(*marks[num])
    scores = sorted(((corr(mg, ng[k]), k) for k in ng), reverse=True)
    print('r%d best:' % num, [('n%d %.3f' % (k, s)) for s, k in scores[:3]])
