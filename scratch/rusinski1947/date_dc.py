# -*- coding: utf-8 -*-
"""Data-cell-only crops at high zoom for the 15 residue rows."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image, ImageDraw

at = digit_read.at
JOBS = [
    ('0145', 96, 8), ('0150', 63, 30), ('0152', 88, 34),
    ('0153', 102, 30), ('0154', 110, 44), ('0154', 111, 44),
    ('0154', 113, 34), ('0154', 114, 8), ('0154', 115, 8),
    ('0154', 116, 8), ('0154', 118, 8), ('0157', 150, 8),
    ('0158', 1, 34), ('0158', 5, 34), ('0158', 6, 8),
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
        y0, y1 = at[n]['rows'][str(num)]['y']
        c = im.crop((rules[7] + 2, y0 - 8, rules[8] - 2, y1 + yext))
        sc = min(9.0, 1450 / c.size[0], 1100 / c.size[1])
        c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)),
                     Image.LANCZOS)
        panels.append(('%s r%d' % (n, num), c))
    per = 5
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
        fn = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\dc_%02d.png' % k
        out.save(fn)
        print(fn, out.size, [t for t, _ in chunk])
        k += 1


if __name__ == '__main__':
    main()
