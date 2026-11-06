# -*- coding: utf-8 -*-
"""Max-zoom crops (5-8x) of individual cells or cell-groups for the
final date-pass decisions."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image, ImageDraw

at = digit_read.at
# (sheet, row, col_lo, col_hi, yext)  col indexes 0..11 (rules idx)
JOBS = [
    ('0141', 39, 7, 8, 8), ('0141', 42, 7, 8, 8), ('0142', 49, 7, 8, 8),
    ('0143', 66, 8, 9, 8), ('0143', 67, 7, 8, 8), ('0143', 69, 10, 11, 8),
    ('0143', 70, 7, 8, 8), ('0144', 76, 7, 8, 8), ('0144', 77, 7, 8, 8),
    ('0145', 87, 7, 11, 8), ('0145', 90, 4, 8, 30), ('0145', 96, 7, 8, 8),
    ('0147', 10, 4, 8, 30), ('0147', 12, 7, 8, 30), ('0149', 41, 7, 8, 8),
    ('0149', 34, 7, 8, 34), ('0149', 35, 7, 8, 8), ('0149', 38, 7, 8, 34),
    ('0149', 39, 7, 8, 8), ('0149', 46, 7, 8, 30), ('0149', 47, 7, 8, 30),
    ('0150', 51, 7, 8, 30), ('0150', 54, 7, 8, 30), ('0150', 61, 7, 8, 8),
    ('0150', 63, 4, 8, 30), ('0150', 65, 7, 8, 30), ('0150', 66, 7, 8, 8),
    ('0151', 67, 7, 11, 30), ('0151', 70, 7, 8, 30), ('0151', 71, 7, 8, 8),
    ('0151', 77, 7, 8, 8), ('0152', 88, 7, 8, 34), ('0152', 90, 7, 11, 30),
    ('0153', 95, 7, 8, 30), ('0153', 96, 7, 9, 26), ('0153', 98, 7, 8, 8),
    ('0153', 102, 7, 8, 30), ('0153', 103, 7, 8, 8), ('0154', 105, 4, 8, 30),
    ('0154', 106, 7, 8, 8), ('0154', 107, 7, 8, 8), ('0154', 110, 7, 8, 44),
    ('0154', 111, 7, 8, 44), ('0154', 112, 7, 11, 8), ('0154', 113, 7, 8, 34),
    ('0154', 114, 7, 8, 8), ('0154', 115, 7, 8, 8), ('0154', 116, 7, 8, 8),
    ('0154', 117, 7, 8, 8), ('0154', 118, 7, 8, 8), ('0155', 132, 7, 8, 30),
    ('0156', 136, 10, 11, 8), ('0156', 138, 7, 8, 34), ('0156', 140, 7, 8, 8),
    ('0156', 145, 7, 9, 26), ('0157', 146, 7, 8, 30), ('0157', 147, 7, 9, 30),
    ('0157', 149, 7, 8, 8), ('0157', 150, 7, 8, 8), ('0157', 151, 7, 8, 30),
    ('0157', 152, 7, 8, 8), ('0157', 154, 7, 9, 30), ('0157', 155, 8, 9, 8),
    ('0157', 156, 7, 8, 8),
]


def main():
    ims = {}
    panels = []
    for n, num, clo, chi, yext in JOBS:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im = ims[n][0]
        rules = RULES[n]
        key = str(num)
        if key not in at[n]['rows']:
            continue
        y0, y1 = at[n]['rows'][key]['y']
        x0, x1 = rules[clo] + 2, rules[chi] - 2
        c = im.crop((x0, y0 - 8, x1, y1 + yext))
        sc = min(7.0, 1420 / c.size[0], 1000 / c.size[1])
        c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)),
                     Image.LANCZOS)
        panels.append(('%s r%d c%d-%d' % (n, num, clo, chi), c))
    per = 6
    k = 0
    for si in range(0, len(panels), per):
        chunk = panels[si:si + per]
        W = max(p.size[0] for _, p in chunk) + 190
        H = sum(p.size[1] + 12 for _, p in chunk) + 10
        out = Image.new('L', (W, H), 255)
        d = ImageDraw.Draw(out)
        yy = 5
        for tag, p in chunk:
            out.paste(p, (185, yy))
            d.text((5, yy + p.size[1] // 2), tag, fill=0)
            yy += p.size[1] + 12
        fn = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\dmax_%02d.png' % k
        out.save(fn)
        print(fn, out.size, [t for t, _ in chunk])
        k += 1


if __name__ == '__main__':
    main()
