# -*- coding: utf-8 -*-
"""Extract the annex sheets' rotated top-bands (the landscape right
margin): running heads, folios, TABELA titles, repeated headers, and
the table-notes the first OCR missed. Renders each for reading."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from num_read import SRC
from PIL import Image, ImageOps

OUT = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\bands'
os.makedirs(OUT, exist_ok=True)
for i in range(139, 160):
    n = '%04d' % i
    with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    c = im.crop((5290, 0, 5936, 3999))
    r = c.rotate(-90, expand=True)
    r = ImageOps.autocontrast(r)
    # slice into ~1000px-tall strips at 2.2x for readability
    W, H = r.size
    sc = 2300.0 / W
    rh = int(H * sc)
    r = r.resize((2300, rh), Image.LANCZOS)
    per = 1100
    k = 0
    for ya in range(0, rh, per):
        s = r.crop((0, ya, 2300, min(ya + per, rh)))
        s.save(os.path.join(OUT, 'band_%s_%d.png' % (n, k)))
        k += 1
    print(n, 'strips:', k, 'total h:', rh)
