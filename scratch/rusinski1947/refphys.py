# -*- coding: utf-8 -*-
"""Phase 2b: ref-level physical verification. For each paragraph
carrying refs: physical page of the paragraph's opening (from the
scan word index) vs the refs' page label. Verdicts:
  OK        - physical == ref page == our block
  SLOT      - physical == ref page but our block differs (re-slot the
              paragraph; refs are already right)
  MISWIRE   - physical == our block but refs point elsewhere (the
              marker sits in this page's text; renumber to this page)
  SPAN?     - physical page N, our block N+1 (leaf overflow: the ref
              may sit on either side of the break - needs y-level
              check or the editor's eye)
Only clear cases (>=3 token hits, start y < 5000) get verdicts."""
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
        if len(tok) >= 5:
            y = w[1]
            if tok not in words or y < words[tok]:
                words[tok] = y
    scans[n] = words

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

REF = re.compile(r'\[\^(\d+)-(\d+)\](?!:)')
verdicts = {'OK': 0, 'SLOT': [], 'MISWIRE': [], 'SPAN': []}
for lab, bl in blocks:
    if not lab.isdigit() or not (1 <= int(lab) <= 144):
        continue
    true_lab = '%d' % (int(lab) + 15)
    for j, ln in bl:
        s = ln.strip()
        refs = REF.findall(s)
        if not refs or not s or s.startswith('[^') or s.startswith('|'):
            continue
        toks = [re.sub(r'[^a-ząćęłńóśźż0-9]', '', w.lower())
                for w in REF.sub(' ', s).split()]
        toks = [w for w in toks if len(w) >= 5][:8]
        if not toks:
            continue
        best, besthits, besty = None, 0, 10 ** 9
        for n, words in scans.items():
            hits = sum(1 for w in toks if w in words)
            if hits:
                ys = [words[w] for w in toks if w in words]
                y = sorted(ys)[0]
                if hits > besthits or (hits == besthits and y < besty):
                    best, besthits, besty = n, hits, y
        if best is None or besthits < 3:
            continue
        phys = int(best) - 15
        refpages = {int(a) for a, b in refs}
        if len(refpages) > 1:
            verdicts['SPAN'].append((lab, j, phys, refs, s[:80]))
            continue
        rp = refpages.pop()
        if rp == phys == int(lab):
            verdicts['OK'] += 1
        elif rp == phys and phys != int(lab):
            verdicts['SLOT'].append((lab, j, phys, besty, s[:90]))
        elif rp == int(lab) and phys != int(lab):
            verdicts['MISWIRE'].append((lab, j, phys, besty, s[:90]))
        else:
            verdicts['SPAN'].append((lab, j, phys, refs, s[:80]))

print('OK refs in place:', verdicts['OK'])
print()
print('=== SLOT (paragraph on wrong page of OURS; refs already right):'
      ' %d' % len(verdicts['SLOT']))
for lab, j, phys, y, s in verdicts['SLOT']:
    print('  our p.%s L%d -> physical p.%d (y%d): %s' % (lab, j, phys,
                                                         y, s))
print()
print('=== MISWIRE (paragraph physically on OUR page; refs point '
      'elsewhere): %d' % len(verdicts['MISWIRE']))
for lab, j, phys, y, s in verdicts['MISWIRE']:
    print('  our p.%s L%d (physical p.%d, y%d): %s' % (lab, j, phys, y,
                                                       s))
print()
print('=== SPAN/AMBIGUOUS: %d' % len(verdicts['SPAN']))
for lab, j, phys, refs, s in verdicts['SPAN']:
    print('  our p.%s L%d (physical p.%d) refs %s: %s' % (lab, j, phys,
                                                          refs, s))
