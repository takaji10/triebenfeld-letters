# -*- coding: utf-8 -*-
"""Tie-breaker v2: harvest digit refs from the SAME sheet's draft-clean
numeric cells (all rows), size-matched to each mystery blob (h within
35%), then score."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

at = digit_read.at
MYST = [
    ('0141', 35, 11), ('0144', 78, 9), ('0145', 90, 9), ('0145', 97, 9),
    ('0145', 97, 10), ('0145', 97, 11), ('0145', 98, 9), ('0145', 98, 11),
    ('0146', 102, 9), ('0146', 102, 11), ('0146', 111, 9),
    ('0146', 111, 11), ('0149', 42, 9), ('0149', 43, 11),
    ('0149', 46, 11), ('0150', 49, 9), ('0150', 50, 9), ('0150', 53, 9),
    ('0150', 54, 9), ('0150', 55, 9), ('0150', 56, 9), ('0150', 58, 10),
    ('0150', 59, 9), ('0150', 63, 9), ('0150', 65, 9), ('0150', 66, 9),
    ('0151', 78, 9), ('0152', 82, 9), ('0153', 93, 9), ('0153', 96, 9),
    ('0153', 98, 10), ('0153', 101, 11), ('0154', 105, 9),
    ('0154', 106, 9), ('0154', 108, 9), ('0154', 109, 9),
    ('0154', 110, 9), ('0154', 111, 9), ('0154', 112, 9),
    ('0154', 116, 9), ('0154', 117, 9), ('0155', 120, 9),
    ('0156', 134, 9), ('0156', 137, 9), ('0156', 144, 9),
    ('0156', 145, 9), ('0157', 146, 9), ('0157', 147, 9),
    ('0157', 148, 9), ('0157', 149, 9), ('0157', 150, 9),
    ('0157', 152, 9), ('0157', 154, 9), ('0157', 155, 9),
    ('0157', 156, 9), ('0158', 2, 9), ('0158', 3, 9), ('0158', 5, 11),
    ('0158', 7, 9), ('0158', 8, 9), ('0159', 11, 10), ('0140', 29, 9),
    ('0140', 14, 9), ('0140', 15, 9), ('0145', 91, 11),
]


def draft_clean(n):
    """All draft numeric values for the sheet, from original.md."""
    t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', '..', 'literature', 'rusinski1947',
                          'original.md'), encoding='utf-8').read()
    seg = t[t.find('<!-- annex sheet %s -->' % n):
            t.find('<!-- annex sheet %s -->' % n) + 60000]
    nxt = seg.find('<!-- annex sheet', 20)
    if nxt != -1:
        seg = seg[:nxt]
    out = []
    for ln in seg.splitlines():
        m = re.match(r'\| (\d+) \| ', ln)
        if not m:
            continue
        cells = [c.strip(' |') for c in ln.split(' | ')]
        for col in (9, 10, 11):
            v = cells[col].replace('*', '').strip() \
                if col < len(cells) else ''
            if re.fullmatch(r'[0-9]{1,4}', v):
                out.append((int(m.group(1)), col, v))
    return out


def main():
    ims = {}
    out = []
    for n, num, col in MYST:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        rules = RULES[n]
        # harvest refs once per sheet
        key = 'refs_' + n
        if key not in ims:
            lib = {}
            for rnum, rcol, rval in draft_clean(n):
                y0, y1 = at[n]['rows'][str(rnum)]['y']
                x0, x1 = rules[rcol - 1] + 8, rules[rcol] - 8
                bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2)
                dsz = [b for b in bl if 150 <= b[4] <= 1600
                       and 18 <= (b[3] - b[2]) <= 75
                       and (b[1] - b[0]) <= 48]
                digits = [c for c in rval if c.isdigit()]
                if len(dsz) != len(digits):
                    continue
                for b, d in zip(dsz, digits):
                    lib.setdefault(d, []).append(
                        (b[3] - b[2], digit_read.grid(px, b)))
            ims[key] = lib
        lib = ims[key]
        y0, y1 = at[n]['rows'][str(num)]['y']
        x0, x1 = rules[col - 1] + 8, rules[col] - 8
        bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2, minpx=25)
        for i, b in enumerate(bl):
            w, h = b[1] - b[0], b[3] - b[2]
            if w >= 38 and h <= 20 and b[4] <= 1100:
                out.append('%s r%d c%d b%d: DASH' % (n, num, col, i))
                continue
            if b[4] < 150 or h < 18 or h > 78:
                out.append('%s r%d c%d b%d: tiny(w%d h%d n%d)'
                           % (n, num, col, i, w, h, b[4]))
                continue
            g = digit_read.grid(px, b)
            parts = []
            for d, gs in sorted(lib.items()):
                cand = [rg for hh, rg in gs if abs(hh - h) <= h * 0.45]
                if not cand:
                    cand = [rg for hh, rg in gs]
                parts.append((max(digit_read.corr(g, rg) for rg in cand),
                              d))
            parts.sort(reverse=True)
            top = ' '.join('%s:%.2f' % (d, s) for s, d in parts[:4])
            out.append('%s r%d c%d b%d [x%d-%d y%d-%d w%d h%d n%d]: %s'
                       % (n, num, col, i, b[0], b[1], b[2], b[3], w, h,
                          b[4], top))
    open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tiebreak2.txt',
         'w', encoding='utf-8').write('\n'.join(out))
    print(len(out), 'lines')


if __name__ == '__main__':
    main()
