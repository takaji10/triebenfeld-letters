# -*- coding: utf-8 -*-
"""Scan every b-series c11 (ludn) cell whose draft value is dash/empty;
report blob shapes to find hidden numbers (a true dash: w~66, h<=8,
n~300; digits have more ink and height)."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

at = digit_read.at
SHEETS = ['0147', '0148', '0149', '0150', '0151', '0152', '0153',
          '0154', '0155', '0156', '0157', '0158', '0159']


def draft_val(n, num):
    t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', '..', 'literature', 'rusinski1947',
                          'original.md'), encoding='utf-8').read()
    i = t.find('<!-- annex sheet %s -->' % n)
    seg = t[i:]
    nxt = seg.find('<!-- annex sheet', 20)
    if nxt != -1:
        seg = seg[:nxt]
    for ln in seg.splitlines():
        m = re.match(r'\| (%d) \| ' % num, ln)
        if m:
            cells = [c.strip(' |') for c in ln.split(' | ')]
            return cells[10] if len(cells) > 10 else '?'
    return None


import re


def main():
    ims = {}
    out = []
    for n in SHEETS:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im, px = ims[n]
        rules = RULES[n]
        nums = sorted(int(k) for k in at[n]['rows'] if k.isdigit())
        for num in nums:
            have = draft_val(n, num)
            if have is None or have not in ('—', '-', ''):
                continue
            y0, y1 = at[n]['rows'][str(num)]['y']
            x0, x1 = rules[10] + 6, rules[11] - 6
            bl = digit_read.blobs(px, x0, x1, y0 + 2, y1 - 2, minpx=40)
            desc = []
            for b in bl:
                w, h = b[1] - b[0], b[3] - b[2]
                desc.append('w%d h%d n%d' % (w, h, b[4]))
            out.append('%s r%d draft=%s | %s' % (n, num, have,
                                                 ' ; '.join(desc)
                                                 if desc else 'EMPTY'))
    open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\dashscan.txt',
         'w', encoding='utf-8').write('\n'.join(out))
    print(len(out), 'dash-cells')


if __name__ == '__main__':
    main()
