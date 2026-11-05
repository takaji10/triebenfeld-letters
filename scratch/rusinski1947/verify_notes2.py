# -*- coding: utf-8 -*-
"""Second footnote check: pages with no parsed notes, scanned by
geometry. A note start is a line in the page's bottom 45% whose first
token is a 1-2 digit number, whose y follows a vertical gap > 1.6x the
line pitch, and whose text is short-ish (notes are 1-3 print lines).
"""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
spath = os.path.join(OCR, 'structure2.json')
if not os.path.isfile(spath):
    spath = os.path.join(OCR, 'structure.json')
struct = json.load(open(spath, encoding='utf-8'))
# the same exclusions structure2 applies: these pages carry no notes by
# design, so their number-like foot lines are not misses
NO_NOTES = ({f'{i:04d}' for i in range(6, 16)}
            | {f'{i:04d}' for i in range(138, 172)} | {'0138'})

found = []
for n in sorted(struct):
    if struct[n]['notes'] or n in NO_NOTES:
        continue
    d = json.load(open(os.path.join(OCR, n + '.json'), encoding='utf-8'))
    ws = [(x[1], x[0], x[5].strip()) for x in d['words'] if x[5].strip()]
    ws.sort()
    lines = []
    for top, left, word in ws:
        if lines and abs(lines[-1][0] - top) < 30:
            lines[-1][2].append((left, word))
        else:
            lines.append([top, left, [(left, word)]])
    lns = []
    for top, left, parts in lines:
        parts.sort()
        lns.append((top, ' '.join(w for _, w in parts)))
    if not lns:
        continue
    H = lns[-1][0] + 100
    foot = [l for l in lns if l[0] > H * 0.55]
    if not foot:
        continue
    tops = [l[0] for l in foot]
    pitch = min(b - a for a, b in zip(tops, tops[1:]) if b - a > 20) \
        if len(tops) > 1 else 90
    hits = []
    for i, (top, text) in enumerate(foot):
        m = re.match(r'^(\d{1,2})[.,]?\s+\S', text)
        if not m:
            continue
        gap = top - foot[i - 1][0] if i else 10 ** 9
        if gap > pitch * 1.6 or i == 0:
            hits.append((int(top), int(m.group(1)), text[:70]))
    if hits:
        found.append((n, hits[:4]))

print('pages without parsed notes that show note-like foot lines:',
      len(found))
for f in found:
    print(f)
