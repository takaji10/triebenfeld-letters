# -*- coding: utf-8 -*-
"""One image per residue data cell, generous zoom."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import RULES, SRC
import digit_read
from PIL import Image

at = digit_read.at
JOBS = [
    ('0145', 96, 8), ('0150', 63, 30), ('0152', 88, 34),
    ('0153', 102, 30), ('0154', 110, 44), ('0154', 111, 44),
    ('0154', 113, 34), ('0154', 114, 8), ('0154', 115, 8),
    ('0154', 116, 8), ('0154', 118, 8), ('0157', 150, 8),
    ('0158', 1, 34), ('0158', 5, 34), ('0158', 6, 8),
]


def main():
    ims = {}
    for n, num, yext in JOBS:
        if n not in ims:
            with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
                im = Image.open(io.BytesIO(fh.read())).convert('L')
            im.load()
            ims[n] = (im, im.load())
        im = ims[n][0]
        rules = RULES[n]
        y0, y1 = at[n]['rows'][str(num)]['y']
        c = im.crop((rules[7] + 2, y0 - 10, rules[8] - 2, y1 + yext))
        sc = min(8.0, 1500 / c.size[0], 1400 / c.size[1])
        c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)),
                     Image.LANCZOS)
        fn = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\dcell_%s_%d.png' \
            % (n, num)
        c.save(fn)
        print(fn, c.size)


if __name__ == '__main__':
    main()
