# -*- coding: utf-8 -*-
"""Both raised glyphs of 0105/2622 at 12x in one image."""
from PIL import Image
import io

with open(r'C:\Users\Tersnaus\Downloads\tom5\tom5_0105.tif', 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
g1 = im.crop((2280, 2615, 2330, 2680)).resize((600, 780), Image.LANCZOS)
g2 = im.crop((2450, 2615, 2520, 2680)).resize((840, 780), Image.LANCZOS)
canvas = Image.new('L', (1500, 800), 255)
canvas.paste(g1, (10, 10))
canvas.paste(g2, (650, 10))
canvas.save(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\zO.png')
print('ok')
