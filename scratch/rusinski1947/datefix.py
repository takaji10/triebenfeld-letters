# -*- coding: utf-8 -*-
"""Build the DATE-FIX table: for every flagged date cell, extract the
candidate date(s) from the strip's raw row text (the '|' pipe layout
delimits the date column in the strip read). The candidate goes
through glue + normalization; where the raw carries no candidate, the
cell goes to the spot list."""
import json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
at = json.load(open(OCR + r'\annex_table.json', encoding='utf-8'))
md = json.load(open(OCR + r'\annex_md.json', encoding='utf-8'))

targets = []
for ln in open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode'
               r'\noise1.txt', encoding='utf-8'):
    m = re.match(r'(\d+) r(\d+) c7 (.*)$', ln)
    if m:
        targets.append((m.group(1), int(m.group(2))))

MON = r'[XIVLl]{1,6}'
DATE_PATS = [
    re.compile(r'(\d{1,2}\s*%s\s*\d{4})' % MON),
    re.compile(r'(%s\s*\d{4})' % MON),
    re.compile(r'(\d{1,2}\s*%s)' % MON),
]
fixes = {}
spot = []
for n, num in targets:
    raw = at[n]['rows'][str(num)].get('raw') or ''
    flat = raw.replace('„', '').replace('"', '')
    # the strip's date column: a '|' delimited group with a month
    cand = None
    for pat in DATE_PATS:
        m = pat.search(flat)
        if m:
            cand = m.group(1)
            break
    if cand is None:
        spot.append((n, num, flat[:80]))
        continue
    c = cand.replace('l', 'I').replace('ł', 'I')
    c = re.sub(r'(\d{1,2})(%s)' % MON, r'\1 \2', c)
    c = re.sub(r'(%s)(\d{4})' % MON, r'\1 \2', c)
    c = re.sub(r'\s+', ' ', c).strip()
    fixes[(n, num)] = c
print('fixable from strip raw:', len(fixes))
print('spot (no strip candidate):', len(spot))
for f in sorted(fixes):
    print('  ', f, fixes[f])
print()
for s in spot:
    print('SPOT', s)
