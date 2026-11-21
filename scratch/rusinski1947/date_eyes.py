# -*- coding: utf-8 -*-
"""Eyes-batch: zoomed row-zone crops (rok..ludn columns) for the
uncertain date rows; b-tail rows get +40px bottom extension for the
wrapped second print line."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image, ImageDraw

at = digit_read.at
# (sheet, row, yext_bottom) - yext for wrapped rows
JOBS = [
    ('0143', 65, 6), ('0143', 66, 6), ('0143', 67, 6), ('0143', 69, 6),
    ('0143', 70, 6), ('0143', 71, 6),
    ('0144', 76, 6), ('0144', 77, 6), ('0145', 87, 6), ('0145', 90, 26),
    ('0145', 96, 6), ('0141', 39, 6),
    ('0141', 42, 6), ('0142', 49, 6), ('0147', 10, 26), ('0147', 12, 26),
    ('0149', 41, 6), ('0149', 34, 30), ('0149', 38, 30), ('0149', 46, 26),
    ('0149', 47, 26), ('0150', 51, 26), ('0150', 54, 26), ('0150', 61, 6),
    ('0150', 63, 26), ('0150', 65, 26), ('0150', 66, 26), ('0151', 67, 26),
    ('0151', 70, 26), ('0151', 71, 26), ('0151', 77, 26), ('0152', 88, 30),
    ('0152', 90, 26), ('0153', 95, 26), ('0153', 96, 26), ('0153', 98, 26),
    ('0153', 102, 26), ('0153', 103, 26), ('0154', 105, 26),
    ('0154', 106, 30), ('0154', 110, 40), ('0154', 112, 26),
    ('0154', 113, 30), ('0154', 114, 26), ('0154', 115, 26),
    ('0154', 116, 26), ('0154', 117, 26), ('0154', 118, 26),
    ('0155', 132, 26), ('0156', 136, 26), ('0156', 138, 30),
    ('0156', 140, 26), ('0156', 145, 26), ('0157', 146, 26),
    ('0157', 147, 26), ('0157', 149, 26), ('0157', 150, 26),
    ('0157', 151, 26), ('0157', 152, 26), ('0157', 154, 26),
    ('0157', 155, 26), ('0157', 156, 26),
]


def main():
    ims = {}
    panels = []
    for n, num, yext in JOBS:
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
        y1b = y1 + yext
        x0, x1 = rules[4] - 4, rules[11] + 4
        c = im.crop((x0, y0 - 6, x1, y1b))
        sc = min(2.6, 1560 / c.size[0], 1150 / c.size[1])
        c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)),
                     Image.LANCZOS)
        panels.append(('%s r%d' % (n, num), c))
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
        fn = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\deye_%02d.png' % k
        out.save(fn)
        print(fn, out.size, [t for t, _ in chunk])
        k += 1


if __name__ == '__main__':
    main()
