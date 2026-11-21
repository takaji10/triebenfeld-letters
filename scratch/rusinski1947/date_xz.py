# -*- coding: utf-8 -*-
"""Extreme zoom (12x) on individual critical glyphs/ties."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image, ImageDraw

at = digit_read.at
# (sheet, row, col, x0rel, x1rel) rel = fraction 0..1 across the cell
JOBS = [
    ('0143', 69, 11, 0.55, 1.0),    # ludn last digit 5/9
    ('0151', 71, 7, 0.10, 0.45),    # day 2nd digit 0/6
    ('0151', 77, 7, 0.10, 0.50),    # blobs 2-3: I,I vs 1,I
    ('0153', 95, 7, 0.05, 0.60),    # 4 ? X: the narrow before X
    ('0153', 103, 7, 0.05, 0.55),   # blob2: 4/I
    ('0154', 106, 7, 0.35, 0.85),   # blob3: 4/2
    ('0142', 49, 7, 0.02, 0.40),    # leading glyph
    ('0143', 67, 7, 0.02, 0.35),    # leading glyph 1?
    ('0150', 66, 7, 0.15, 0.55),    # month glyph V/VI
    ('0157', 156, 7, 0.05, 1.0),    # whole data cell
    ('0154', 114, 7, 0.25, 0.75),   # blob3/4: I,V?
    ('0149', 38, 7, 0.0, 1.0),      # whole data cell incl. smalls
    ('0151', 70, 7, 0.30, 1.0),     # tail: 'i 1782'?
    ('0147', 12, 7, 0.40, 1.0),     # separator zone
    ('0152', 90, 7, 0.30, 1.0),     # tail: 'i 1 V 1677'
    ('0150', 65, 7, 0.0, 1.0),      # whole data cell
]


def main():
    ims = {}
    panels = []
    for n, num, col, fr0, fr1 in JOBS:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im = ims[n][0]
        rules = RULES[n]
        y0, y1 = at[n]['rows'][str(num)]['y']
        x0, x1 = rules[col - 1] + 2, rules[col] - 2
        xa = int(x0 + (x1 - x0) * fr0)
        xb = int(x0 + (x1 - x0) * fr1)
        c = im.crop((xa, y0 - 10, xb, y1 + 12))
        sc = min(12.0, 1500 / c.size[0], 950 / c.size[1])
        c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)),
                     Image.LANCZOS)
        panels.append(('%s r%d c%d %.2f-%.2f' % (n, num, col, fr0, fr1), c))
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
        fn = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\xz_%02d.png' % k
        out.save(fn)
        print(fn, out.size, [t for t, _ in chunk])
        k += 1


if __name__ == '__main__':
    main()
