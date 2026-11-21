# -*- coding: utf-8 -*-
"""Per-blob decode dump for bad data cells (col 8, ci 7): digit matcher
top-3 + roman templates (I/V/X) harvested from verified clean dates."""
import io, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

at = digit_read.at

# verified clean date cells (sheet, row, value) - roman harvest sources
CLEAN = [
    ('0139', 7, '11 XI 1720'), ('0139', 9, '6 VII 1702'),
    ('0139', 11, '18 IV 1785'), ('0140', 17, '2 IV 1757'),
    ('0143', 66, '1 V 1713'), ('0143', 67, '8 IV 1785'),
    ('0143', 73, '17 V 1746'), ('0145', 92, '20 II 1742'),
    ('0145', 94, '29 X 1738'), ('0145', 95, '6 VIII 1724'),
    ('0145', 98, '5 VI 1712'), ('0146', 102, '21 X 1744'),
    ('0149', 43, '10 XII 1643'), ('0144', 80, '29 X 1728'),
    ('0145', 88, '1 III 1743'),
]


def harvest(px, n, num, val):
    rules = RULES[n]
    y0, y1 = at[n]['rows'][str(num)]['y']
    x0, x1 = rules[7] + 6, rules[8] - 6
    bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2, minpx=25)
    toks = val.split()
    # map tokens to blobs: digits get blobs in order; roman letters too
    want = []
    for tok in toks:
        if re.fullmatch(r'\d+', tok):
            want.extend(tok)
        elif re.fullmatch(r'[IVX]+', tok):
            want.extend(tok)
    dsz = [b for b in bl if b[4] >= 150 and 18 <= (b[3] - b[2]) <= 78
           and (b[1] - b[0]) <= 60]
    if len(dsz) != len(want):
        return None
    out = []
    for b, ch in zip(dsz, want):
        out.append((ch, digit_read.grid(px, b)))
    return out


def main():
    ims = {}
    rom = {}   # ch -> [grid]
    for n, num, val in CLEAN:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        h = harvest(px, n, num, val)
        if h is None:
            print('harvest fail', n, num, val)
            continue
        for ch, g in h:
            rom.setdefault(ch, []).append(g)
    print('roman templates:', {k: len(v) for k, v in sorted(rom.items())})
    lib = digit_read.digit_lib()

    bad = [l for l in open(
        r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\datebad.txt',
        encoding='utf-8').read().splitlines() if re.match(r'0\d\d\d r', l)]
    out = []
    for line in bad:
        m = re.match(r'(0\d\d\d) r(\d+) \| (.*?) \| RAW', line)
        n, num, cur = m.group(1), int(m.group(2)), m.group(3)
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        rules = RULES[n]
        key = str(num)
        if key not in at.get(n, {}).get('rows', {}):
            continue
        y0, y1 = at[n]['rows'][key]['y']
        x0, x1 = rules[7] + 6, rules[8] - 6
        bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2, minpx=20)
        parts = []
        for b in sorted(bl, key=lambda t: t[0]):
            w, hgt, ink = b[1] - b[0], b[3] - b[2], b[4]
            near = (abs(b[0] - rules[7]) < 12 or abs(b[1] - rules[8]) < 12) \
                and w <= 14
            if near:
                continue
            if w >= 38 and hgt <= 20 and ink <= 1100:
                parts.append('-')
                continue
            if hgt > 80:
                parts.append('|T%d' % hgt)
                continue
            if ink < 130 or hgt < 16:
                parts.append('.(w%dh%dn%d)' % (w, hgt, ink))
                continue
            g = digit_read.grid(px, b)
            ds = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                         for d, gs in lib.items()), reverse=True)[:3]
            rs = sorted(((max(digit_read.corr(g, rg) for rg in gs), c)
                         for c, gs in rom.items()), reverse=True)[:2]
            parts.append('%s[%.2f|%s %s]' % (
                ds[0][1], ds[0][0],
                ' '.join('%s%.2f' % (c, s) for s, c in rs),
                'w%dh%d' % (w, hgt)))
        out.append('=== %s r%d cur=%r\n   %s' % (n, num, cur[:36],
                                                 ' '.join(parts)))
    open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\datedec.txt',
         'w', encoding='utf-8').write('\n'.join(out))
    print(len(out), 'cells decoded')


if __name__ == '__main__':
    main()
