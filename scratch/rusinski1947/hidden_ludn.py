# -*- coding: utf-8 -*-
"""Extract b-series c11 audit lines: draft=dash/empty but pixels show
digit blobs -> hidden ludn values."""
import re

lines = open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\audit.txt',
             encoding='utf-8').read().splitlines()
out = []
for l in lines:
    m = re.match(r'(015\d) r(\d+) c11 \| draft=([^|]*) \| pix=(.*)', l)
    if not m:
        continue
    have = m.group(3).strip()
    pix = m.group(4)
    digits = re.findall(r'\^?\d\(', pix)
    if have in ('—', '-', '') and digits:
        out.append(l)
print(len(out))
open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\hiddendludn.txt',
     'w', encoding='utf-8').write('\n'.join(out))
