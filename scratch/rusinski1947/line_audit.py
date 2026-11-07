# -*- coding: utf-8 -*-
"""Quantify marked-line misassignment: for each body scan, count its
marked lines whose tokens do NOT match the scan's own OCR words but
DO match a neighbour scan (within +-4)."""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
ML = os.path.join(OCR, 'marked_lines.json')

scans = {}
for i in range(16, 138):
    n = '%04d' % i
    p = os.path.join(OCR, n + '.json')
    if not os.path.isfile(p):
        continue
    d = json.load(open(p, encoding='utf-8'))
    words = set()
    for w in d['words']:
        tok = re.sub(r'[^a-ząćęłńóśźż0-9]', '', w[5].lower())
        if len(tok) >= 6:
            words.add(tok)
    scans[n] = words

ml = json.load(open(ML, encoding='utf-8'))
total, moved = 0, 0
per_scan = []
for n in sorted(scans):
    lines = ml.get(n, {}).get('lines', [])
    bad = 0
    for l in lines:
        txt = l.get('text', '')
        toks = [re.sub(r'[^a-ząćęłńóśźż0-9]', '', w.lower())
                for w in txt.split()]
        toks = [w for w in toks if len(w) >= 6][:10]
        if not toks:
            continue
        own = sum(1 for w in toks if w in scans[n])
        if own >= 2:
            continue
        # find a better neighbour
        best, besthits = None, 0
        for k in range(-4, 5):
            m = '%04d' % (int(n) + k)
            if m not in scans or m == n:
                continue
            hits = sum(1 for w in toks if w in scans[m])
            if hits > besthits:
                best, besthits = m, hits
        if besthits >= 3 and besthits > own:
            bad += 1
            moved += 1
        total += 1
    if bad:
        per_scan.append((n, int(n) - 15, bad, len(lines)))
print('lines checked: %d; misplaced: %d' % (total, moved))
print('%-6s %-5s %-5s %-5s' % ('scan', 'page', 'moved', 'total'))
for n, lab, bad, tot in per_scan:
    print('%-6s %-5d %-5d %-5d' % (n, lab, bad, tot))
