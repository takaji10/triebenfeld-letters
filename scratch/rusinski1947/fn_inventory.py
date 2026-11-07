# -*- coding: utf-8 -*-
"""Footnote inventory per body page: (a) how many note-lines the
print's bottom block holds (from the OCR's note segmentation),
(b) how many defs the transcription carries on that page,
(c) how many refs are wired in that page's body text.
Also: running-head / binder-mark remnants in the body text."""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
MD = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
      r'\rusinski1947\literature\rusinski1947\original.md')
t = open(MD, encoding='utf-8').read()
lines = t.splitlines()

# per-page blocks in the transcription
blocks = []          # (label, para_lines, def_lines)
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

out = []
for lab, bl in blocks:
    paras = [ln for ln in bl if ln.strip()
             and not re.match(r'\[\^%s-\d+\]:' % re.escape(lab), ln)]
    defs = [ln for ln in bl if re.match(r'\[\^%s-\d+\]:' % re.escape(lab),
                                        ln)]
    n_defs = len(defs)
    # distinct note numbers defined on the page
    nums = sorted(int(re.match(r'\[\^%s-(\d+)\]:' % re.escape(lab), d)
                      .group(1)) for d in defs)
    # refs wired within this page's paragraphs
    n_refs = sum(len(re.findall(r'\[\^%s-\d+\](?!:)' % re.escape(lab), p))
                 for p in paras)
    out.append((lab, n_defs, nums, n_refs))

# the print's note-block counts (structure4 = the OCR's per-page notes)
s4 = json.load(open(os.path.join(OCR, 'structure4.json'),
                    encoding='utf-8'))
print('%-5s %-8s %-8s %-8s' % ('page', 'print', 'defs', 'refs'))
flags = []
for lab, n_defs, nums, n_refs in out:
    if not lab.isdigit():
        continue                 # roman-numbered front matter
    scan = '%04d' % (int(lab) + 15)
    n_print = len(s4.get(scan, {}).get('notes', []))
    mark = ''
    if n_print != n_defs:
        mark = ' <<< print %d vs defs %d' % (n_print, n_defs)
        flags.append((lab, n_print, n_defs))
    # refs vs defs: re-used notes allowed, so refs >= defs; flag if
    # refs < defs (a def never referenced)
    if n_refs < n_defs:
        mark += ' (refs<defs)'
    print('%-5s %-8d %-8d %-8d%s' % (lab, n_print, n_defs, n_refs, mark))
print()
print('%d count-mismatch pages:' % len(flags))
for f in flags:
    print('  ', f)
