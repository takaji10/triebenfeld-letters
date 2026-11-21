# -*- coding: utf-8 -*-
"""Full pixel census of a-series (0139-0146) figure columns (c8 dymy,
c10 ludn): every row, blobs at the row's band-top zone, matcher top-2,
diffed against the draft. Finds all value discrepancies at once."""
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
draft = {}
cur = None
for ln in t.splitlines():
    m = re.match(r'<!-- annex sheet (0\d+) -->', ln)
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'\| (\d+) \| ', ln)
    if m and cur in AS:
        c = [x.strip() for x in ln.split('|')][1:-1]
        if len(c) >= 11:
            draft[(cur, int(c[0]))] = (c[8], c[10])

ims = {}
out = []
for n in AS:
    if n not in ims:
        with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
            im = Image.open(io.BytesIO(fh.read())).convert('L')
        im.load()
        ims[n] = (im, im.load())
    im, px = ims[n]
    rules = RULES[n]
    for k in sorted(int(x) for x in at[n]['rows'] if x.isdigit()):
        y0, y1 = at[n]['rows'][str(k)]['y']
        line = ['%s r%-3d' % (n, k)]
        for ci, dtag in ((8, 'd'), (10, 'l')):
            x0, x1 = rules[ci] + 4, rules[ci + 1] - 4
            bl = digit_read.blobs(px, x0, x1, y0 - 14, y0 + 78, minpx=60)
            parts = []
            for b in sorted(bl, key=lambda t: (t[0])):
                w, h, ink = b[1] - b[0], b[3] - b[2], b[4]
                if w >= 38 and h <= 20 and ink <= 1100:
                    parts.append('DASH')
                    continue
                if h < 18 or ink < 150:
                    continue
                if h > 66:
                    parts.append('TALL(w%dh%d)' % (w, h))
                    continue
                g = digit_read.grid(px, b)
                ds = sorted(((max(digit_read.corr(g, rg) for rg in gs), d)
                             for d, gs in lib.items()), reverse=True)[:2]
                parts.append('%s@%.2f(w%dh%d)' % (ds[0][1], ds[0][0], w, h))
            dval = draft.get((n, k), ('?', '?'))[0 if ci == 8 else 1]
            line.append('%s[%s] px=%s' % (dtag, dval[:12],
                                          ''.join(p[0] for p in parts)
                                          if parts else '-'))
        out.append('  '.join(line))
open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\acensus.txt',
     'w', encoding='utf-8').write('\n'.join(out))
print(len(out), 'rows censused')
