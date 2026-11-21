# -*- coding: utf-8 -*-
"""The inventory audit: classify every page's note chain by its read
evidence, and flag the three residue classes for reading:

  A. reads == 1..k          - clean;
  B. reads start above 1    - possible missed notes ABOVE the block
                              (or the first reads misread);
  C. reads have gaps/dups   - mid-chain misses or misreads;
  D. last read > k          - notes likely missing at the bottom.

Also the body-swallow check: if the body's last line before the block
lacks sentence punctuation while the first note's text continues it,
the boundary ate body text (0018-class).
"""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'

s = json.load(open(os.path.join(OCR, 'structure2.json'), encoding='utf-8'))
v1 = json.load(open(os.path.join(OCR, 'structure.json'), encoding='utf-8'))

rows = {'A': [], 'B': [], 'C': [], 'D': [], 'swallow': []}
for n in sorted(s):
    notes = s[n]['notes']
    if not notes:
        continue
    reads = [x.get('num_read') for x in notes]
    k = len(notes)
    known = [r for r in reads if r is not None]
    if reads == list(range(1, k + 1)):
        rows['A'].append(n)
        continue
    if known and min(known) > 1:
        rows['B'].append((n, k, reads))
    elif known and max(known) > k:
        rows['D'].append((n, k, reads))
    else:
        rows['C'].append((n, k, reads))
    # body-swallow check: the v1 inventory's line list is the body's
    # source; find the last body line before the first note top
    first_top = min(x['top'] for x in notes)
    v1lines = [l for l in v1[n]['lines'] if l['top'] < first_top]
    if v1lines:
        last = v1lines[-1]['text'].strip()
        if last and not re.search(r'[.!?»”]"?\s*$', last) \
                and len(last.split()) > 3:
            rows['swallow'].append((n, last[-60:]))

print('A clean:', len(rows['A']))
print('B starts-high:', len(rows['B']))
for x in rows['B']:
    print('  ', x)
print('C gaps:', len(rows['C']))
for x in rows['C']:
    print('  ', x)
print('D last-read>k:', len(rows['D']))
for x in rows['D']:
    print('  ', x)
print('body-swallow suspects:', len(rows['swallow']))
for x in rows['swallow']:
    print('  ', x)
