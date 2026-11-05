# -*- coding: utf-8 -*-
"""Verify the footnote inventory of tom5: did the structure parse miss
any notes?

For every page, an independent walk of the raw text from the bottom
collects lines that begin with a 1-2 digit number (the note starts); the
collected set should form the chain 1..k and match structure.json's
notes. Differences are listed per page.
"""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
struct = json.load(open(os.path.join(OCR, 'structure.json'),
                        encoding='utf-8'))

suspects = []
for n in sorted(struct):
    d = json.load(open(os.path.join(OCR, n + '.json'), encoding='utf-8'))
    lines = [l.strip() for l in d['pol'].split('\n') if l.strip()]
    got = [x['num'] for x in struct[n]['notes']]
    # walk from the bottom; keep the last run of leading-number lines
    found = []
    i = len(lines) - 1
    run = []
    while i >= 0:
        m = re.match(r'^(\d{1,2})[.,]?\s+(\S.*)$', lines[i])
        if m and 1 <= int(m.group(1)) <= 30:
            run.append(int(m.group(1)))
        else:
            # a non-number line: wrapped note text only continues the run
            # if we are inside a run and the line is short/foot-like
            if run and len(lines[i]) <= 80:
                pass
            elif run:
                break
        i -= 1
    ind = sorted(set(run))
    if ind and ind != list(range(1, len(ind) + 1)):
        suspects.append((n, 'chain', ind[:16]))
    if len(ind) != len(got) or (ind and got and ind != got[:len(ind)]):
        suspects.append((n, 'count', 'indep', ind[:16], 'struct', got[:16]))

print('suspect pages:', len(suspects))
for s in suspects:
    print(s)
