# -*- coding: utf-8 -*-
"""Per-line blob analysis for the tall flagged cells: cluster blobs by
y-center, match each cluster against the digit library."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC, OCR
import digit_read
from PIL import Image

JOBS = [('0145', 88, 9), ('0145', 94, 11), ('0148', 31, 10),
        ('0148', 33, 11), ('0149', 34, 11), ('0149', 43, 11),
        ('0149', 46, 11), ('0150', 61, 9),
        ('0140', 14, 9), ('0140', 29, 9),
        ('0149', 44, 9), ('0153', 94, 10), ('0157', 146, 9),
        ('0158', 4, 9), ('0154', 105, 9), ('0154', 110, 9),
        ('0154', 113, 9), ('0154', 114, 9), ('0154', 118, 9),
        ('0157', 147, 9), ('0157', 152, 9), ('0157', 154, 9),
        ('0157', 155, 9), ('0157', 156, 9), ('0158', 2, 9),
        ('0156', 136, 11), ('0154', 106, 10), ('0154', 107, 10)]


def main():
    lib = digit_read.digit_lib()
    for n, num, col in JOBS:
        if n not in digit_read._ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            digit_read._ims[n] = (im, im.load())
        im, px = digit_read._ims[n]
        rules = RULES[n]
        y0, y1 = digit_read.at[n]['rows'][str(num)]['y']
        x0, x1 = rules[col - 1] + 8, rules[col] - 8
        bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2)
        if not bl:
            print(n, 'r%d c%d EMPTY' % (num, col), flush=True)
            continue
        # cluster by y-center with gap threshold
        bl2 = sorted(bl, key=lambda b: ((b[2] + b[3]) // 2, b[0]))
        lines = []
        for b in bl2:
            yc = (b[2] + b[3]) // 2
            if lines and yc - lines[-1]['yc'] <= 30:
                lines[-1]['blobs'].append(b)
                lines[-1]['yc'] = (lines[-1]['yc'] + yc) // 2
            else:
                lines.append({'yc': yc, 'blobs': [b]})
        parts = []
        for L in lines:
            ds = []
            for b in sorted(L['blobs'], key=lambda x: x[0]):
                w, h = b[1] - b[0], b[3] - b[2]
                tag = 'DASH' if w >= 38 and h <= 20 and b[4] <= 1100 else \
                      ('tiny' if b[4] < 300 or h < 25 else None)
                if tag:
                    ds.append(tag)
                    continue
                g = digit_read.grid(px, b)
                sc = sorted(((max(digit_read.corr(g, rg)
                                  for rg in gs), d)
                             for d, gs in lib.items()), reverse=True)
                ds.append('%s%.2f[x%d-%d y%d-%d w%d h%d]'
                          % (sc[0][1], sc[0][0], b[0], b[1], b[2], b[3],
                             w, h))
            parts.append(' | '.join(ds))
        print(n, 'r%d c%d y%d-%d n=%d' % (num, col, y0, y1, len(bl)),
              '   LINES:', ' // '.join(parts), flush=True)


if __name__ == '__main__':
    main()
