# -*- coding: utf-8 -*-
"""Phase 1: per-page footnote closure. For each body page:
- refs used in the page's text must reference only that page's notes
- every def on the page must be referenced at least once on the page
Flags: CROSS (ref to another page's note), DEAD (def never referenced),
ORDER (ref numbers not in 1..N or out of sequence), DUP-OK count."""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
MD = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
      r'\rusinski1947\literature\rusinski1947\original.md')
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
        cur.append(ln)
if cur_lab is not None:
    blocks.append((cur_lab, cur))

cross, dead, order = [], [], []
rows = []
for lab, bl in blocks:
    if not lab.isdigit() or not (1 <= int(lab) <= 144):
        continue
    esc = re.escape(lab)
    paras = [ln for ln in bl if ln.strip()
             and not re.match(r'\[\^%s-\d+\]:' % esc, ln)]
    defs = sorted(int(re.match(r'\[\^%s-(\d+)\]:' % esc, d).group(1))
                  for d in bl
                  if re.match(r'\[\^%s-\d+\]:' % esc, ln if False else d)
                  or re.match(r'\[\^%s-\d+\]:' % esc, d))
    used = []
    for p in paras:
        used += [int(x) for x in
                 re.findall(r'\[\^%s-(\d+)\](?!:)' % esc, p)]
    other = []
    for p in paras:
        other += [x for x in re.findall(r'\[\^(\d+)-(\d+)\](?!:)', p)
                  if x[0] != lab]
    used_set = set(used)
    dset = set(defs)
    row = (lab, len(defs), len(used), sorted(set(other)))
    rows.append(row)
    if other:
        cross.append((lab, sorted(set(other))))
    if dset - used_set:
        dead.append((lab, sorted(dset - used_set)))
    # order: refs must be 1..N page notes; flag refs > max def
    if used and max(used) > max(defs or [0]):
        order.append((lab, sorted(used_set)))

print('%d pages checked' % len(rows))
print()
print('=== CROSS-page refs (%d pages):' % len(cross))
for lab, o in cross:
    print('  p.%s -> %s' % (lab, o))
print()
print('=== DEAD defs (%d pages):' % len(dead))
for lab, missing in dead:
    print('  p.%s defs %s never referenced' % (lab, missing))
print()
print('=== ORDER violations (%d pages):' % len(order))
for lab, u in order:
    print('  p.%s uses %s > max def' % (lab, u))
