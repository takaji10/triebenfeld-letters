# -*- coding: utf-8 -*-
"""Render three glyph zones for direct visual comparison."""
from PIL import Image
import io

with open(r'C:\Users\Tersnaus\Downloads\tom5\tom5_0096.tif', 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
im.crop((2450, 1080, 2760, 1180)).resize((1860, 600), Image.LANCZOS).save(
    r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\zJ1.png')
im.crop((3480, 2470, 3660, 2570)).resize((1080, 600), Image.LANCZOS).save(
    r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\zJ2.png')
im.crop((600, 2570, 700, 2670)).resize((600, 600), Image.LANCZOS).save(
    r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\zJ3.png')
print('ok')
