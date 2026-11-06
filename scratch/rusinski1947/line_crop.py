# -*- coding: utf-8 -*-
"""True-line cell reader: profiles the nazwa column to find each row's
real text line, then crops cells to that line (kills rule leaks and
neighbor-row pollution)."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC, OCR
import digit_read, json
from PIL import Image

at = digit_read.at
_NAZWA = (1060, 1920)


def line_profile(px, x0, x1, y0, y1, thr=200, minpx=5):
    prev = False
    out = []
    for y in range(y0, y1):
        n = sum(1 for x in range(x0, x1, 2) if px[x, y] < thr)
        cur = n > minpx
        if cur != prev:
            out.append((('start' if cur else 'end'), y))
            prev = cur
    return out


def true_lines(n, num, im, px, slack=14):
    """Return (ly0, ly1) of the row's real text line."""
    rules = RULES[n]
    y0, y1 = at[n]['rows'][str(num)]['y']
    x0, x1 = _NAZWA
    yw0, yw1 = max(0, y0 - 40), y1 + 40
    prof = line_profile(px, x0, x1, yw0, yw1)
    # build line intervals
    ivs = []
    open_y = None
    for kind, y in prof:
        if kind == 'start':
            open_y = y
        else:
            if open_y is not None:
                ivs.append((open_y, y))
                open_y = None
    if open_y is not None:
        ivs.append((open_y, yw1))
    # pick interval overlapping the band center most
    cy = (y0 + y1) // 2
    best = None
    for a, b in ivs:
        if a <= cy <= b or (a < y1 and b > y0):
            d = abs(((a + b) // 2) - cy)
            if best is None or d < best[0]:
                best = (d, a, b)
    if best is None:
        return y0, y1
    return max(y0 - 2, best[1] - 2), min(y1, best[2] + 2)


def read_cells(n, num, cols, pad=4):
    if n not in _ims:
        with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
            im = Image.open(io.BytesIO(fh.read())).convert('L')
        im.load()
        _ims[n] = (im, im.load())
    im, px = _ims[n]
    ly0, ly1 = true_lines(n, num, im, px)
    rules = RULES[n]
    out = [('LINE', ly0, ly1)]
    for col in cols:
        x0, x1 = rules[col - 1] + 6, rules[col] - 6
        bl = digit_read.blobs(px, x0, x1, ly0, ly1, minpx=25)
        parts = []
        for b in sorted(bl, key=lambda t: t[0]):
            w, h = b[1] - b[0], b[3] - b[2]
            if w >= 38 and h <= 20 and b[4] <= 1100:
                parts.append('DASH[x%d-%d]' % (b[0], b[1]))
                continue
            if b[4] < 120 or h < 20:
                parts.append('tiny[x%d-%d y%d-%d w%d h%d]'
                             % (b[0], b[1], b[2], b[3], w, h))
                continue
            g = digit_read.grid(px, b)
            sc = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                         for d, gs in digit_read.digit_lib().items()),
                        reverse=True)
            parts.append('%s%.2f[x%d-%d y%d-%d w%d h%d]'
                         % (sc[0][1], sc[0][0], b[0], b[1], b[2], b[3],
                            w, h))
        out.append((col, ' '.join(parts) if parts else 'EMPTY'))
    return out


_ims = {}

if __name__ == '__main__':
    JOBS = [('0145', 87, (8, 9, 10)), ('0143', 73, (8, 9, 10, 11)),
            ('0145', 96, (8, 9, 10, 11)), ('0145', 97, (8, 9, 10, 11)),
            ('0145', 98, (8, 9, 10, 11)), ('0146', 102, (8, 9, 10, 11)),
            ('0142', 55, (8, 9, 10, 11)), ('0144', 81, (8, 9, 10, 11)),
            ('0145', 90, (8, 9, 10, 11)), ('0145', 91, (8, 9, 10, 11)),
            ('0145', 94, (8, 9, 10, 11)), ('0140', 17, (7, 8, 9, 10, 11)),
            ('0140', 14, (7, 8, 9, 10, 11)), ('0140', 15, (7, 8, 9, 10, 11)),
            ('0140', 29, (8, 9, 10, 11)), ('0143', 72, (8, 9, 10, 11)),
            ('0143', 62, (8, 9, 10, 11)), ('0142', 51, (8, 9, 10, 11)),
            ('0142', 60, (8, 9, 10, 11)), ('0148', 19, (8, 9, 10, 11)),
            ('0148', 21, (8, 9, 10, 11))]
    for n, num, cols in JOBS:
        res = read_cells(n, num, cols)
        ly = [r for r in res if r[0] == 'LINE'][0]
        print('=== %s r%d line y%d-%d' % (n, num, ly[1], ly[2]), flush=True)
        for item in res:
            if item[0] == 'LINE':
                continue
            col, s = item
            print('   c%d: %s' % (col, s), flush=True)
