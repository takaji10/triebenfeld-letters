# -*- coding: utf-8 -*-
"""Wide-window rescan for window-edge-clipped blobs + draft ratio dump."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

at = digit_read.at
lib = digit_read.digit_lib()

# --- draft dump for ratio law ---
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
cur = None
WANT = {('0158', n) for n in range(1, 10)}
WANT |= {('0154', n) for n in (104, 105, 106, 112, 113)}
WANT |= {('0156', n) for n in (133, 134, 135, 136, 137, 144, 145)}
WANT |= {('0151', 78), ('0157', 146), ('0157', 147)}
print('--- draft rows ---')
for ln in t.splitlines():
    m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'\| (\d+) \| ', ln)
    if m and (cur, int(m.group(1))) in WANT:
        c = [x.strip() for x in ln.split('|')][1:-1]
        print('%s r%-3s dym=%-8r obl=%-4r ludn=%r'
              % (cur, c[0], c[8], c[9], c[10]))

# --- wide rescan ---
print('--- wide rescans ---')
JOBS = [
    ('0154', 105, 8, 280, 480),
    ('0154', 112, 8, 1700, 1900),
    ('0156', 134, 8, 500, 700),
    ('0156', 137, 8, 950, 1150),
]
ims = {}
for n, num, ci, ya, yb in JOBS:
    if n not in ims:
        with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
            im = Image.open(io.BytesIO(fh.read())).convert('L')
        im.load()
        ims[n] = (im, im.load())
    im, px = ims[n]
    rules = RULES[n]
    x0, x1 = rules[ci] + 4, rules[ci + 1] - 4
    bl = digit_read.blobs(px, x0, x1, ya, yb, minpx=25)
    print('=== %s r%d c%d y%d-%d' % (n, num, ci, ya, yb))
    for b in sorted(bl, key=lambda t: (t[2], t[0])):
        w, h, ink = b[1] - b[0], b[3] - b[2], b[4]
        info = ''
        if w >= 38 and h <= 20 and ink <= 1100:
            info = 'DASH'
        elif h > 66 or w <= 3:
            info = 'TALL'
        elif h >= 16 and ink >= 80:
            g = digit_read.grid(px, b)
            ds = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                         for d, gs in lib.items()), reverse=True)[:3]
            info = ' '.join('%s@%.2f' % (d, s) for s, d in ds)
        else:
            info = '.'
        print('   x%d-%d y%d-%d w%d h%d n%d  %s'
              % (b[0], b[1], b[2], b[3], w, h, ink, info))
