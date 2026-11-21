# -*- coding: utf-8 -*-
"""Def-level physical check: each note def's text should be found on its
own page's scan (note zone). Flags defs whose tokens match a LATER scan
better - the signature of overflow text glued into the def."""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
MD = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
      r'\rusinski1947\literature\rusinski1947\original.md')

scans = {}
for i in range(16, 138):
    n = '%04d' % i
    p = os.path.join(OCR, n + '.json')
    if not os.path.isfile(p):
        continue
    d = json.load(open(p, encoding='utf-8'))
    words = {}
    for w in d['words']:
        tok = re.sub(r'[^a-ząćęłńóśźż0-9]', '', w[5].lower())
        if len(tok) >= 6:
            y = w[1]
            if tok not in words or y < words[tok]:
                words[tok] = y
    scans[n] = words

t = open(MD, encoding='utf-8').read()
cur = None
defs = []          # (page, label, text)
for ln in t.splitlines():
    m = re.match(r'^\[p\. (\w+)\]', ln.strip())
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'^\[\^(\w+)-(\d+)\]: ?(.*)$', ln)
    if m and cur:
        defs.append([cur, m.group(2), m.group(3)])
        continue
    if defs and ln.strip() and not ln.strip().startswith('[p.') \
            and not re.match(r'^\[\^', ln.strip()):
        defs[-1][2] += ' ' + ln.strip()

print('%d defs' % len(defs))
flagged = 0
for page, num, text in defs:
    if not page.isdigit() or not (1 <= int(page) <= 122):
        continue
    toks = [re.sub(r'[^a-ząćęłńóśźż0-9]', '', w.lower()) for w in text.split()]
    # sample tokens across the WHOLE def (overflow sits at the tail)
    toks = [w for w in toks if len(w) >= 7]
    if len(toks) < 4:
        continue
    sample = toks[-10:]         # the def's tail - where overflow gets glued
    own = '%04d' % (int(page) + 15)
    scores = []
    for n, words in scans.items():
        hits = sum(1 for w in sample if w in words)
        if hits:
            scores.append((hits, n))
    if not scores:
        continue
    scores.sort(reverse=True)
    best_hits, best = scores[0]
    lookup = {n: h for h, n in scores}
    own_hits = lookup.get(own, 0)
    if best != own and best_hits >= 4 and own_hits <= 1 \
            and int(best) > int(own):
        flagged += 1
        print('def %s-%s: own p.%s hits=%d, best p.%s hits=%d: %s'
              % (page, num, page, own_hits, int(best) - 15, best_hits,
                 text[:70]))
print('flagged:', flagged)
