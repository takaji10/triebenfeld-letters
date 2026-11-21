# -*- coding: utf-8 -*-
"""List unplaced labels with the structure line text at their top."""
import json, re
from collections import Counter

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
DRAFT = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
         r'\rusinski1947\literature\rusinski1947\original.md')

t = open(DRAFT, encoding='utf-8').read()
body = Counter(re.findall(r'\[\^(\d+-\d+)\](?!:)', t))
defs = Counter(re.findall(r'\[\^(\d+-\d+)\]:', t))
missing = sorted(k for k in defs if defs[k] > body.get(k, 0))

s = json.load(open(OCR + r'\structure4.json', encoding='utf-8'))
mk = json.load(open(OCR + r'\markers.json', encoding='utf-8'))

SCAN = {}
# printed page -> scan: body scan = page + 15
for pg_scan, marks in mk.items():
    for m in marks:
        SCAN[m['label']] = (pg_scan, m)

for lab in missing:
    pg = lab.split('-')[0]
    entry = SCAN.get(lab)
    if not entry:
        print(lab, 'NO MARKER RECORD')
        continue
    scan, m = entry
    lines = [l for l in s[scan]['lines'] if abs(l['top'] - m['top']) <= 12]
    txt = lines[0]['text'] if lines else '???'
    print('%s %-6s %-16r | %s' % (lab, m['kind'], m['tok'], txt[:100]))
