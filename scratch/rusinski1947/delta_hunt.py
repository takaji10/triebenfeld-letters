# -*- coding: utf-8 -*-
"""Delta hunters: obl cells (5 clean) digit-verify + ludn trailing-0s."""
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
rows = []
for ln in t.splitlines():
    m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'\| (\d+) \| ', ln)
    if m and cur in AS:
        c = [x.strip() for x in ln.split('|')][1:-1]
        rows.append((cur, int(c[0]), c[8], c[9], c[10]))

print('--- obl cells ---')
for sh, num, d, o, l in rows:
    if o not in ('—', ''):
        print('%s r%d obl=%s (dym=%s ludn=%s)' % (sh, num, o, d, l))
print('--- ludn trailing-0 cells ---')
for sh, num, d, o, l in rows:
    if re.fullmatch(r'\d*0', l or ''):
        print('%s r%d ludn=%s (dym=%s)' % (sh, num, l, d))

# grid the obl digits of each clean obl cell + the trailing-0 ludn digits
ims = {}
jobs = []
for sh, num, d, o, l in rows:
    if o not in ('—', ''):
        jobs.append((sh, num, 9, o, 'obl'))
    if re.fullmatch(r'\d*0', l or ''):
        jobs.append((sh, num, 10, l, 'ludn'))
for sh, num, ci, val, tag in jobs:
    if sh not in ims:
        with open(os.path.join(SRC, 'tom5_%s.tif' % sh), 'rb') as fh:
            im = Image.open(io.BytesIO(fh.read())).convert('L')
        im.load()
        ims[sh] = (im, im.load())
    im, px = ims[sh]
    rules = RULES[sh]
    y0, y1 = at[sh]['rows'][str(num)]['y']
    x0, x1 = rules[ci] + 4, rules[ci + 1] - 4
    bl = digit_read.blobs(px, x0, x1, y0 - 16, y1 + 30, minpx=40)
    digs = [b for b in sorted(bl, key=lambda t: t[0])
            if 16 <= b[3] - b[2] <= 66 and b[1] - b[0] >= 8]
    reads = []
    for b in digs:
        g = digit_read.grid(px, b)
        ds = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                     for d, gs in lib.items()), reverse=True)[:2]
        reads.append('%s@%.2f' % (ds[0][1], ds[0][0]))
    print('%s r%d c%d %s: draft=%r px=%s'
          % (sh, num, ci, tag, val, ' '.join(reads)))
