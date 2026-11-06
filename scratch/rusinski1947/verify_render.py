# -*- coding: utf-8 -*-
"""Verification renders: single cells for mid-series rows; numeric-zone
(dymy/obl/ludn) crops for the b-tail rows where bands glue rows."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image, ImageDraw

at = digit_read.at
SINGLE = [
    ('0141', 32, 11), ('0141', 35, 11), ('0141', 41, 11),
    ('0142', 45, 11), ('0142', 48, 11), ('0144', 78, 9), ('0144', 82, 11),
    ('0145', 90, 9), ('0145', 90, 11), ('0145', 91, 11), ('0145', 96, 9),
    ('0145', 96, 11), ('0145', 97, 9), ('0145', 97, 10), ('0145', 97, 11),
    ('0145', 98, 9), ('0145', 98, 11), ('0146', 102, 9), ('0146', 102, 11),
    ('0146', 111, 9), ('0146', 111, 11),
    ('0149', 34, 11), ('0149', 39, 9), ('0149', 40, 9), ('0149', 41, 9),
    ('0149', 42, 9), ('0149', 43, 9), ('0149', 43, 11), ('0149', 44, 9),
    ('0149', 46, 11), ('0149', 48, 9),
    ('0150', 49, 9), ('0150', 50, 9), ('0150', 53, 9), ('0150', 54, 9),
    ('0150', 55, 9), ('0150', 56, 9), ('0150', 58, 10), ('0150', 59, 9),
    ('0150', 63, 9), ('0150', 65, 9), ('0150', 66, 9),
    ('0151', 67, 9), ('0151', 73, 9), ('0151', 78, 9),
    ('0152', 82, 9), ('0152', 92, 10),
    ('0153', 93, 9), ('0153', 96, 9), ('0153', 98, 10), ('0153', 101, 11),
    ('0154', 105, 9), ('0154', 106, 9), ('0154', 108, 9),
    ('0156', 139, 9), ('0156', 145, 9), ('0159', 11, 10),
]
ZONE = ['0154', '0155', '0156', '0157', '0158', '0159']


def main():
    ims = {}
    panels = []
    for n, num, col in SINGLE:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        rules = RULES[n]
        y0, y1 = at[n]['rows'][str(num)]['y']
        x0, x1 = rules[col - 1] + 3, rules[col] - 3
        c = im.crop((x0, y0 - 6, x1, y1 + 6))
        sc = min(6.0, 1350 / c.size[0], 1050 / c.size[1])
        c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)),
                     Image.LANCZOS)
        panels.append(('%s r%d c%d' % (n, num, col), c))
    for n in ZONE:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im = ims[n][0]
        rules = RULES[n]
        nums = sorted(int(k) for k in at[n]['rows'] if k.isdigit())
        for num in nums:
            key = str(num)
            if key not in at[n]['rows']:
                continue
            y0, y1 = at[n]['rows'][key]['y']
            if y1 - y0 > 240:
                continue
            c = im.crop((rules[8] + 2, y0 - 4, rules[11] - 2, y1 + 4))
            sc = min(2.2, 1600 / c.size[0], 1000 / c.size[1])
            c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)),
                         Image.LANCZOS)
            panels.append(('%s r%d zone' % (n, num), c))
    per = 6
    for si in range(0, len(panels), per):
        chunk = panels[si:si + per]
        W = max(p.size[0] for _, p in chunk) + 180
        H = sum(p.size[1] + 12 for _, p in chunk) + 10
        out = Image.new('L', (W, H), 255)
        d = ImageDraw.Draw(out)
        yy = 5
        for tag, p in chunk:
            out.paste(p, (170, yy))
            d.text((5, yy + p.size[1] // 2), tag, fill=0)
            yy += p.size[1] + 12
        fn = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\ver_%02d.png' \
            % (si // per)
        out.save(fn)
        print(fn, out.size, [t for t, _ in chunk])


if __name__ == '__main__':
    main()
