# -*- coding: utf-8 -*-
"""Digit-glyph reader for the annex's numeric cells.

1. digit_lib(): harvest digit-glyph blobs from TRUSTED cells (draft
   cells that are pure digit strings; each blob labeled by its digit
   from the value string) -> a reference library keyed by digit.
2. read_cell(): for a target cell, extract blobs, match each against
   the library by normalized-grid correlation, report the best digit
   per blob in x-order with scores.

Usage: python digit_read.py  -> full flagged-cell report
       python digit_read.py 0143 65 11  -> one cell (col 1-11)
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC, OCR
from PIL import Image

at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                    encoding='utf-8'))


def blobs(px, x0, x1, y0, y1, minpx=25):
    seen = set()
    out = []
    for x in range(x0, x1):
        for y in range(y0, y1):
            if px[x, y] < 175 and (x, y) not in seen:
                stack = [(x, y)]
                comp = []
                seen.add((x, y))
                while stack:
                    cx, cy = stack.pop()
                    comp.append((cx, cy))
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            nx, ny = cx + dx, cy + dy
                            if x0 <= nx < x1 and y0 <= ny < y1 \
                                    and (nx, ny) not in seen \
                                    and px[nx, ny] < 175:
                                seen.add((nx, ny))
                                stack.append((nx, ny))
                if len(comp) > minpx:
                    xs = [p[0] for p in comp]
                    ys = [p[1] for p in comp]
                    out.append([min(xs), max(xs), min(ys), max(ys),
                                len(comp)])
    return sorted(out)


def grid(px, b, W=16, H=24):
    x0, x1, y0, y1 = b[0], b[1], b[2], b[3]
    g = []
    for gy in range(H):
        row = []
        for gx in range(W):
            xa = x0 + (x1 - x0 + 1) * gx / W
            xb = x0 + (x1 - x0 + 1) * (gx + 1) / W
            ya = y0 + (y1 - y0 + 1) * gy / H
            yb = y0 + (y1 - y0 + 1) * (gy + 1) / H
            n = t = 0
            for x in range(int(xa), max(int(xa) + 1, int(xb))):
                for y in range(int(ya), max(int(ya) + 1, int(yb))):
                    t += 1
                    if px[x, y] < 175:
                        n += 1
            row.append(n / max(t, 1))
        g.append(row)
    return g


def corr(a, b):
    ma = sum(map(sum, a)) / (len(a) * len(a[0]))
    mb = sum(map(sum, b)) / (len(b) * len(b[0]))
    num = da = db = 0.0
    for i in range(len(a)):
        for j in range(len(a[0])):
            num += (a[i][j] - ma) * (b[i][j] - mb)
            da += (a[i][j] - ma) ** 2
            db += (b[i][j] - mb) ** 2
    return num / ((da ** .5) * (db ** .5) + 1e-9)


LIB = None


def digit_lib():
    """Harvest digit blobs from trusted pure-digit cells."""
    global LIB
    if LIB is not None:
        return LIB
    import re
    draft = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              '..', '..', 'literature', 'rusinski1947',
                              'original.md'),
                 encoding='utf-8').read()
    # trusted cells: | Lp | ... | where the target col is ^[\d .]+$
    vals = {}   # (sheet, row, col) -> value string
    cur = None
    for ln in draft.splitlines():
        m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
        if m:
            cur = m.group(1)
            continue
        m = re.match(r'\| (\d+) \| (.*) \|$', ln)
        if m and cur:
            cells = m.group(2).split(' | ')
            # cells[0..9] map to cols 2..11 (col 1 = Lp)
            for i, c in enumerate(cells):
                col = i + 2
                if re.fullmatch(r'[\d .]{1,8}', c.strip()) \
                        and c.strip().replace('.', '').replace(' ', '')\
                        .isdigit():
                    vals[(cur, int(m.group(1)), col)] = \
                        c.strip().replace(' ', '')
    ims = {}
    lib = {}
    for (n, num, col), val in sorted(vals.items()):
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        rules = RULES[n]
        y0, y1 = at[n]['rows'][str(num)]['y']
        x0, x1 = rules[col - 1] + 8, rules[col] - 8
        bl = blobs(px, x0, x1, y0 + 2, y1 - 2)
        digits = [d for d in val if d.isdigit()]
        # keep digit-sized blobs only, x-ordered; ignore tiny marks
        dsz = [b for b in bl if 300 <= b[4] <= 1400
               and 30 <= (b[3] - b[2]) <= 70]
        if len(dsz) != len(digits) or not digits:
            continue
        for b, d in zip(dsz, digits):
            lib.setdefault(d, []).append(grid(px, b))
    LIB = lib
    return lib


def read_cell(n, num, col, verbose=True):
    lib = digit_lib()
    if n not in _ims:
        with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
            im = Image.open(io.BytesIO(fh.read())).convert('L')
        im.load()
        _ims[n] = (im, im.load())
    im, px = _ims[n]
    rules = RULES[n]
    y0, y1 = at[n]['rows'][str(num)]['y']
    x0, x1 = rules[col - 1] + 8, rules[col] - 8
    bl = blobs(px, x0, x1, y0 + 2, y1 - 2)
    if not bl:
        return 'EMPTY', []
    dashes = [b for b in bl if (b[1] - b[0]) >= 38
              and (b[3] - b[2]) <= 20 and b[4] <= 1100]
    tiny = [b for b in bl if b[4] < 300 or (b[3] - b[2]) < 25]
    dsz = [b for b in bl if b not in dashes and b not in tiny]
    out = []
    for b in dsz:
        g = grid(px, b)
        scores = []
        for d, gs in lib.items():
            best = max(corr(g, rg) for rg in gs)
            scores.append((best, d))
        scores.sort(reverse=True)
        out.append((b, scores[:3]))
    kind = 'DASH' if dashes and not dsz else \
           ('EMPTY' if not bl else 'DIGITS' if dsz else 'DASH?')
    return kind, out


_ims = {}


def main():
    if len(sys.argv) > 1:
        n, num, col = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
        kind, ds = read_cell(n, num, col)
        print(n, 'r%d c%d' % (num, col), kind)
        for b, sc in ds:
            print('   blob x%d-%d y%d-%d n%d ->' % (b[0], b[1], b[2], b[3],
                                                    b[4]),
                  [('d%s %.3f' % (d, s)) for s, d in sc])
        return
    import num_read
    for n, num, col in num_read.CELLS:
        kind, ds = read_cell(n, num, col)
        seq = ''
        det = []
        for b, sc in ds:
            seq += sc[0][1]
            det.append('%s(%s%.2f)' % (sc[0][1], sc[1][1], sc[0][0]))
        print('%s r%d c%d %-7s blobs=%d dash=%d -> %s   %s'
              % (n, num, col, kind, len(ds), 1 if kind == 'DASH' else 0,
                 seq, ' '.join(det)), flush=True)


if __name__ == '__main__':
    main()
