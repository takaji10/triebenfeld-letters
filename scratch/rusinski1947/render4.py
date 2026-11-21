# -*- coding: utf-8 -*-
"""Render 0105 glyph zones: after '30' and after '60' on line 2622."""
from PIL import Image
import io

with open(r'C:\Users\Tersnaus\Downloads\tom5\tom5_0105.tif', 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
im.crop((1500, 2615, 2450, 2730)).resize((2850, 345), Image.LANCZOS).save(
    r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\zM1.png')
im.crop((1500, 2615, 2450, 2730)).resize((2850, 345), Image.LANCZOS)
print('ok')
