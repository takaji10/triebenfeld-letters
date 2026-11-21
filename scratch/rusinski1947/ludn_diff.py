# -*- coding: utf-8 -*-
"""Diff census ludn reads vs draft values."""
import re
txt = open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\acensus.txt',
           encoding='utf-8').read()
for ln in txt.splitlines():
    m = re.search(r'l\[([^\]]*)\] px=(\S+)', ln)
    if not m:
        continue
    dv, px = m.group(1), m.group(2)
    dnum = re.sub(r'[^0-9]', '', dv)
    pclean = px.replace('D', '').replace('T', '')
    if dv in ('', '—') and len(pclean) >= 2:
        print('MISSING?', ln)
    elif dnum and pclean and sorted(dnum) != sorted(pclean) \
            and len(pclean) >= len(dnum):
        print('DIFF    ?', ln)
