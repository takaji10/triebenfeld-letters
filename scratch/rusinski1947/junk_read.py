# -*- coding: utf-8 -*-
"""Per-blob decode of junk numeric cells (dymy ci8 / obl ci9 / ludn ci10):
matcher top-2 + dash detection + exact y positions (band-glue triage)."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

at = digit_read.at
lib = digit_read.digit_lib()

JOBS = [l for l in open(
    r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\junklist.txt',
    encoding='utf-8').read().splitlines() if re.match(r'0\d\d\d r', l)]

ims = {}
out = []
for line in JOBS:
    m = re.match(r'(0\d\d\d) r(\d+) c(\d+) \w+=(.*?) RAW', line)
    n, num, ci, cur = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
    if n not in ims:
        with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
            im = Image.open(io.BytesIO(fh.read())).convert('L')
        im.load()
        ims[n] = (im, im.load())
    im, px = ims[n]
    rules = RULES[n]
    y0, y1 = at[n]['rows'][str(num)]['y']
    x0, x1 = rules[ci] + 4, rules[ci + 1] - 4
    bl = digit_read.blobs(px, x0, x1, y0 - 12, y1 + 26, minpx=15)
    parts = []
    for b in sorted(bl, key=lambda t: (t[2], t[0])):
        w, h, ink = b[1] - b[0], b[3] - b[2], b[4]
        if w >= 38 and h <= 20 and ink <= 1100:
            parts.append('DASH(y%d)' % b[2])
            continue
        if h < 16 or ink < 100:
            parts.append('.(w%dh%dn%d y%d)' % (w, h, ink, b[2]))
            continue
        g = digit_read.grid(px, b)
        ds = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                     for d, gs in lib.items()), reverse=True)[:2]
        parts.append('%s@%.2f(w%dh%d y%d-%d)' % (
            ds[0][1], ds[0][0], w, h, b[2], b[3]))
    out.append('=== %s r%d c%d cur=%s band y%d-%d\n   %s' % (
        n, num, ci, cur[:20], y0, y1, ' '.join(parts) if parts else 'EMPTY'))
open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\junkdec.txt',
     'w', encoding='utf-8').write('\n'.join(out))
print(len(out), 'cells decoded')
