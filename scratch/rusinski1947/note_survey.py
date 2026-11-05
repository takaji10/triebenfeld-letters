# -*- coding: utf-8 -*-
"""Survey the note chains: where the parsed notes' read numbers have
gaps against the 1..k assignment, or where a note opens with an
artifact glyph (the '%' class, a stray 'w', a lone '+').

This is the survey for the targeted note re-reads; every page listed
here gets its gap bands re-read at 3x, and the band's own reading of
the leading digit settles the chain. No chain assumption is patched
silently: the re-read is the evidence.
"""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
struct = json.load(open(os.path.join(OCR, 'structure2.json'),
                        encoding='utf-8'))

ART = re.compile(r'^[%*+!§£|.,)\-—–w]\s*(\S.*)$', re.UNICODE)
gapped = []
for n in sorted(struct):
    notes = struct[n]['notes']
    if not notes:
        continue
    reads = [x.get('num_read', x['num']) for x in notes]
    # the assignment is 1..k by order; the reads should equal it
    k = len(notes)
    issues = []
    for i, r in enumerate(reads):
        want = i + 1
        if r != want:
            issues.append((i + 1, r))
    # artifact-leading texts (a note whose text begins with a non-word
    # glyph or a stray lowercase letter before a capital)
    for i, x in enumerate(notes):
        if ART.match(x['text']) and re.match(r'^[%*+!§£|.,)\-—–w]\s*[A-ZĄĆĘŁŃÓŚŹŻ„"(]',
                                             x['text']):
            issues.append(('art', i + 1, x['text'][:40]))
    if issues:
        gapped.append((n, k, issues))
print('pages with chain/artifact issues:', len(gapped))
for g in gapped:
    print(g)
