# -*- coding: utf-8 -*-
"""Definitive a-series figure audit: for each row, window the row's own
print line via its Lp anchor (Lpmid-60..Lpmid+15), read c8/c9/c10 digits
x-sorted, diff vs draft. Rows without an anchor are reported UNVERIFIED."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

at = digit_read.at
lib = digit_read.digit_lib()
AS = ['0139', '0140', '0141', '0142', '0143', '0144', '0145', '0146']
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
cur = None
draft = {}
order = []
for ln in t.splitlines():
    m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'\| (\d+) \| ', ln)
    if m and cur in AS:
        c = [x.strip() for x in ln.split('|')][1:-1]
        draft[(cur, int(c[0]))] = (c[8], c[9], c[10])
        order.append((cur, int(c[0])))

ims = {}
out = []
for sh, num in order:
    if sh not in ims:
        with open(os.path.join(SRC, 'tom5_%s.tif' % sh), 'rb') as fh:
            im = Image.open(io.BytesIO(fh.read())).convert('L')
        im.load()
        ims[sh] = (im, im.load())
    im, px = ims[sh]
    rules = RULES[sh]
    y0, y1 = at[sh]['rows'][str(num)]['y']
    bl = digit_read.blobs(px, rules[0] + 4, rules[1] - 4,
                          y0 - 60, y1 + 60, minpx=100)
    anch = [(b[2] + b[3]) // 2 for b in bl if 25 <= b[3] - b[2] <= 75]
    dv = draft[(sh, num)]
    if not anch:
        out.append('%s r%-3d NOANCHOR draft=%s' % (sh, num, dv))
        continue
    am = min(anch, key=lambda a: abs(a - y0))   # anchor nearest band top
    ya, yb = am - 60, am + 15
    vals = []
    for ci in (8, 9, 10):
        x0, x1 = rules[ci] + 4, rules[ci + 1] - 4
        bl = digit_read.blobs(px, x0, x1, ya, yb, minpx=40)
        parts = []
        for b in sorted(bl, key=lambda t: t[0]):
            w, h, ink = b[1] - b[0], b[3] - b[2], b[4]
            if w >= 38 and h <= 20 and ink <= 1100:
                parts.append('-')          # dash
            elif h > 66 or w <= 3:
                continue                   # stroke
            elif h >= 16 and ink >= 80:
                g = digit_read.grid(px, b)
                ds = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                             for d, gs in lib.items()), reverse=True)[:1]
                parts.append(ds[0][1])
        vals.append(''.join(parts))
    pxs = (vals[0], vals[1], vals[2])
    def norm(v):
        return re.sub(r'[^0-9-]', '', v or '')
    dn = tuple(norm(x) for x in dv)
    pn = tuple(norm(x) for x in pxs)
    flag = 'OK ' if dn == pn else 'DIFF'
    out.append('%s r%-3d %s draft=%s px=%s'
               % (sh, num, flag, dv, pxs))
open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\aaudit.txt',
     'w', encoding='utf-8').write('\n'.join(out))
import collections
print(collections.Counter(l.split()[2] for l in out))
for l in out:
    if 'DIFF' in l or 'NOANCHOR' in l:
        print(l)
