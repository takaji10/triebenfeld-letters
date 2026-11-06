# -*- coding: utf-8 -*-
"""Zoomed crops of the ambiguous cells, 6 per image."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC, OCR
import digit_read
from PIL import Image, ImageDraw

at = digit_read.at
JOBS = [
    ('0140', 14, 9), ('0140', 14, 11), ('0140', 15, 9), ('0140', 15, 11),
    ('0140', 29, 9), ('0140', 29, 10),
    ('0142', 55, 11), ('0145', 87, 9), ('0145', 87, 10), ('0145', 90, 11),
    ('0145', 91, 11), ('0145', 96, 9), ('0145', 96, 11), ('0145', 97, 9),
    ('0145', 97, 11), ('0145', 98, 11), ('0146', 102, 9), ('0144', 81, 10),
    ('0143', 73, 9),
]


def main():
    ims = {}
    panels = []
    for n, num, col in JOBS:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        rules = RULES[n]
        y0, y1 = at[n]['rows'][str(num)]['y']
        x0, x1 = rules[col - 1] + 4, rules[col] - 4
        c = im.crop((x0, y0, x1, y1))
        sc = min(3.0, 1400 / c.size[0], 1900 / c.size[1])
        c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)),
                     Image.LANCZOS)
        panels.append(('%s r%d c%d' % (n, num, col), c))
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
        fn = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\amb_%02d.png' \
            % (si // per)
        out.save(fn)
        print(fn, out.size, [t for t, _ in chunk])


if __name__ == '__main__':
    main()
