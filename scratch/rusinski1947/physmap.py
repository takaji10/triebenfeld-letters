# -*- coding: utf-8 -*-
"""Phase 2a: paragraph -> physical print page. Every body paragraph's
opening words are matched against each scan's word set; mismatches
with the block the paragraph currently sits in are reported."""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
MD = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
      r'\rusinski1947\literature\rusinski1947\original.md')

# per-scan word sets + word->min-y index (body scans only)
scans = {}
for i in range(16, 138):
    n = '%04d' % i
    p = os.path.join(OCR, n + '.json')
    if not os.path.isfile(p):
        continue
    d = json.load(open(p, encoding='utf-8'))
    ws = d['words']
    words = {}
    for w in ws:
        tok = re.sub(r'[^a-ząćęłńóśźż0-9]', '', w[5].lower())
        if len(tok) >= 5:
            y = w[1]
            if tok not in words or y < words[tok]:
                words[tok] = y
    scans[n] = words
print('%d scans indexed' % len(scans))

t = open(MD, encoding='utf-8').read()
lines = t.splitlines()
blocks = []
cur_lab, cur = None, None
for j, ln in enumerate(lines):
    m = re.match(r'^\[p\. ([IVXL\d]+)\]$', ln.strip())
    if m:
        if cur_lab is not None:
            blocks.append((cur_lab, cur))
        cur_lab, cur = m.group(1), []
        continue
    if cur is not None:
        cur.append((j + 1, ln))
if cur_lab is not None:
    blocks.append((cur_lab, cur))

REF = re.compile(r'\[\^\d+-\d+\]')
mismatch, okcnt, unk = 0, 0, 0
report = []
for lab, bl in blocks:
    if not lab.isdigit() or not (1 <= int(lab) <= 144):
        continue
    true_lab = '%d' % (int(lab) + 15)
    for j, ln in bl:
        s = ln.strip()
        if not s or s.startswith('[^') or s.startswith('|') \
                or s.startswith('<!--') or s.startswith('TABELA') \
                or s.startswith('* '):
            continue
        toks = [re.sub(r'[^a-ząćęłńóśźż0-9]', '', w.lower())
                for w in REF.sub(' ', s).split()]
        toks = [w for w in toks if len(w) >= 5][:8]
        if not toks:
            continue
        best, besthits, besty = None, 0, 10 ** 9
        for n, words in scans.items():
            hits = sum(1 for w in toks if w in words)
            if hits > besthits or (hits == besthits and hits > 0):
                # earliest y among matched tokens
                ys = [words[w] for w in toks if w in words]
                y = sorted(ys)[0]
                if hits > besthits or (hits == besthits and y < besty):
                    best, besthits, besty = n, hits, y
        if best is None or besthits < 3:
            unk += 1
            continue
        if best != true_lab:
            mismatch += 1
            report.append((lab, j, int(best) - 15, besthits, s[:90]))
        else:
            okcnt += 1

print('paragraphs: ok=%d mismatch=%d unknown=%d' % (okcnt, mismatch, unk))
print()
for lab, j, true, hits, s in report:
    print('p.%s L%d -> physical p.%d (%d hits): %s' % (lab, j, true,
                                                       hits, s))
