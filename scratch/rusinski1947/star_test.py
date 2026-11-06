# -*- coding: utf-8 -*-
"""1) Match the raised small glyphs against KNOWN star blobs.
2) Scan other sheets for the tall-stroke pattern."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC, OCR
import digit_read
from PIL import Image

at = digit_read.at

# known starred cells (sheet, row) from annex_fixes 'N *' values
STARS = [(('0139', 9)), (('0140', 21)), (('0140', 26)), (('0141', 36)),
         ('0142', 48), ('0142', 54), ('0144', 77), ('0144', 78),
         ('0147', 1), ('0147', 12), ('0148', 15), ('0148', 17),
         ('0148', 22), ('0148', 24), ('0149', 44), ('0149', 48),
         ('0150', 62), ('0151', 74), ('0151', 75), ('0151', 77),
         ('0151', 79), ('0152', 82), ('0152', 83), ('0152', 84),
         ('0152', 85), ('0152', 87), ('0152', 91), ('0153', 103),
         ('0155', 119), ('0155', 123), ('0155', 127), ('0158', 1),
         ('0159', 1), ('0159', 3), ('0154', 107)]
# uncertain-star cells to test
TESTS = [('0146', 102, 9), ('0140', 17, 9), ('0149', 47, 9),
         ('0151', 78, 9), ('0154', 106, 9), ('0154', 110, 9),
         ('0154', 111, 9), ('0154', 113, 9), ('0157', 154, 9)]


def blob_grid(px, b):
    return digit_read.grid(px, b)


def main():
    # harvest star blobs: in starred cells the star = the raised small
    # blob (h < 40, above baseline) OR trailing blob
    star_grids = []
    ims = {}
    for n, num in STARS:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        rules = RULES[n]
        y0, y1 = at[n]['rows'][str(num)]['y']
        x0, x1 = rules[8] + 6, rules[9] - 6
        bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2, minpx=25)
        for b in bl:
            h = b[3] - b[2]
            if 12 <= h <= 40 and (b[1] - b[0]) <= 30 and b[4] < 700:
                star_grids.append((blob_grid(px, b), (n, num, b)))
    print('star templates:', len(star_grids))
    # also harvest digit smalls for contrast
    for n, num, col in TESTS:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        rules = RULES[n]
        y0, y1 = at[n]['rows'][str(num)]['y']
        x0, x1 = rules[col - 1] + 6, rules[col] - 6
        bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2, minpx=25)
        print('=== %s r%d c%d' % (n, num, col))
        for b in bl:
            w, h = b[1] - b[0], b[3] - b[2]
            if h < 42 and w <= 30 and b[4] < 700:
                g = blob_grid(px, b)
                ss = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                             for d, gs in digit_read.digit_lib().items()),
                            reverse=True)[:2]
                st = max(digit_read.corr(g, sg) for sg, _ in star_grids)
                print('   small x%d-%d y%d-%d w%d h%d n%d digit:%s star:%.2f'
                      % (b[0], b[1], b[2], b[3], w, h, b[4],
                         ' '.join('%s:%.2f' % (d, s) for s, d in ss), st))
            else:
                g = blob_grid(px, b)
                ss = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                             for d, gs in digit_read.digit_lib().items()),
                            reverse=True)[:3]
                print('   big   x%d-%d y%d-%d w%d h%d n%d %s'
                      % (b[0], b[1], b[2], b[3], w, h, b[4],
                         ' '.join('%s:%.2f' % (d, s) for s, d in ss)))


if __name__ == '__main__':
    main()
