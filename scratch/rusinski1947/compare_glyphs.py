# -*- coding: utf-8 -*-
"""Side-by-side comparison: each mystery blob vs its top-4 library
candidates, rendered at matched scale for visual identification."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC, OCR
import digit_read
from PIL import Image, ImageDraw

at = digit_read.at
JOBS = [
    ('0142', 55, 11), ('0145', 87, 9), ('0145', 87, 10), ('0145', 90, 11),
    ('0145', 91, 11), ('0145', 96, 9), ('0145', 96, 11), ('0145', 97, 9),
    ('0145', 97, 11), ('0145', 98, 11), ('0146', 102, 9), ('0143', 73, 9),
    ('0143', 72, 9), ('0145', 94, 9), ('0140', 17, 9),
]


def crop_blob(im, b, pad=3):
    return im.crop((b[0] - pad, b[2] - pad, b[1] + pad + 1, b[3] + pad + 1))


def main():
    lib = digit_read.digit_lib()
    ims = {}
    rows = []   # list of (label, [tiles...])
    for n, num, col in JOBS:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        rules = RULES[n]
        y0, y1 = at[n]['rows'][str(num)]['y']
        x0, x1 = rules[col - 1] + 8, rules[col] - 8
        bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2)
        for i, b in enumerate(bl):
            w, h = b[1] - b[0], b[3] - b[2]
            if w >= 38 and h <= 20 and b[4] <= 1100:
                rows.append(('%s r%d c%d b%d = DASH' % (n, num, col, i),
                             [crop_blob(im, b, 2)]))
                continue
            if b[4] < 120 or h < 22 or h > 80 or w > 45:
                rows.append(('%s r%d c%d b%d = small?' % (n, num, col, i),
                             [crop_blob(im, b, 2)]))
                continue
            g = digit_read.grid(px, b)
            sc = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                         for d, gs in lib.items()), reverse=True)[:4]
            tiles = [crop_blob(im, b)]
            labels = ['MYST']
            for s, d in sc:
                rc = _harvest(d)
                if rc is not None:
                    tiles.append(rc)
                    labels.append('%s %.2f' % (d, s))
            rows.append(('%s r%d c%d b%d' % (n, num, col, i), tiles))
    # render each comparison row
    W = 1900
    per = 14
    k = 0
    for si in range(0, len(rows), per):
        chunk = rows[si:si + per]
        H = 0
        layout = []
        for lab, tiles in chunk:
            Hh = 0
            for t in tiles:
                sc = 150 / t.size[1]
                t2 = t.resize((max(1, int(t.size[0] * sc)), 150),
                              Image.LANCZOS)
                Hh = max(Hh, 150)
            Hh += 24
            H += Hh
            layout.append((lab, tiles))
        H += 10
        out = Image.new('L', (W, H), 255)
        d = ImageDraw.Draw(out)
        yy = 5
        for lab, tiles in layout:
            xx = 175
            d.text((5, yy + 60), lab, fill=0)
            for t in tiles:
                scc = 150 / t.size[1]
                t2 = t.resize((max(1, int(t.size[0] * scc)), 150),
                              Image.LANCZOS)
                out.paste(t2, (xx, yy))
                xx += t2.size[0] + 14
            yy += 174
        fn = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\cmp_%02d.png' % k
        out.save(fn)
        print(fn, out.size)
        k += 1


_HARVEST_CACHE = {}


def _harvest(d):
    if d in _HARVEST_CACHE:
        return _HARVEST_CACHE[d]
    lib = digit_read.digit_lib()
    # find the source cell for one instance of d by scanning known cells
    import num_read
    known = [('0139', 1, 9, '60'), ('0139', 4, 9, '5'), ('0139', 5, 9, '5'),
             ('0139', 6, 9, '34'), ('0139', 7, 9, '23'),
             ('0139', 8, 9, '51'), ('0143', 65, 11, '120'),
             ('0143', 67, 11, '104'), ('0143', 68, 9, '14'),
             ('0143', 71, 9, '19'), ('0145', 88, 9, '22'),
             ('0145', 92, 9, '10'), ('0145', 94, 11, '159'),
             ('0150', 61, 9, '24'), ('0140', 16, 9, '11'),
             ('0140', 25, 11, '122'), ('0142', 59, 11, '50'),
             ('0143', 63, 9, '11'), ('0143', 63, 11, '80'),
             ('0143', 64, 9, '30'), ('0143', 66, 9, '51'),
             ('0143', 67, 9, '17'), ('0143', 70, 9, '17'),
             ('0143', 70, 11, '110'), ('0143', 71, 11, '129'),
             ('0145', 87, 10, '11'), ('0142', 60, 8, '21'),
             ('0142', 61, 11, '41')]
    for n, num, col, val in known:
        if n not in digit_read._ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            digit_read._ims[n] = (im, im.load())
        im, px = digit_read._ims[n]
        rules = RULES[n]
        y0, y1 = at[n]['rows'][str(num)]['y']
        x0, x1 = rules[col - 1] + 8, rules[col] - 8
        bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2)
        dsz = [b for b in bl if 300 <= b[4] <= 1400
               and 30 <= (b[3] - b[2]) <= 70]
        digits = [c for c in val if c.isdigit()]
        if len(dsz) != len(digits):
            continue
        for b, dd in zip(dsz, digits):
            if dd == d:
                _HARVEST_CACHE[d] = crop_blob(im, b)
                return _HARVEST_CACHE[d]
    return None


if __name__ == '__main__':
    main()
