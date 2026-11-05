# -*- coding: utf-8 -*-
"""The final footnote gate: per page, the line pass's marker-ish tokens
vs the parsed note count. Deviations beyond one are listed (the marker
count runs slightly high: quoted figures read as tails)."""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
struct = json.load(open(os.path.join(OCR, 'structure2.json'),
                        encoding='utf-8'))
TAIL = re.compile(r'^(?P<base>[^\W\d_][\wąćęłńóśźż.\-]*?)[*?]*\d{1,2}'
                  r'[*?]?[.,;:»”?]*$', re.UNICODE)
DIGIT = re.compile(r'^\d{1,2}[.,]?$')

bad = []
for fn in sorted(os.listdir(os.path.join(OCR, 'lines'))):
    if not fn.endswith('.json'):
        continue
    n = fn[:4]
    notes = struct[n]['notes']
    if not notes:
        continue
    recs = json.load(open(os.path.join(OCR, 'lines', fn),
                          encoding='utf-8'))
    got = 0
    for r in recs:
        if r.get('skipped'):
            continue
        toks = (r.get('line_pol') or '').split()
        for i, w in enumerate(toks):
            m = TAIL.match(w)
            glued = bool(m and re.search(r'\d$', w)
                         and len(m.group('base')) >= 2)
            standalone = bool(DIGIT.match(w) and i > 0
                              and re.search(r'[^\W\d_]$', toks[i - 1],
                                            re.UNICODE))
            if glued or standalone:
                got += 1
    if abs(got - len(notes)) > 1:
        bad.append((n, len(notes), got))
print('pages deviating >1:', len(bad))
for b in bad:
    print(b)
