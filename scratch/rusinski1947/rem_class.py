# -*- coding: utf-8 -*-
"""Classify remaining superscript remnants (* % $ glyphs) in prose:
with a ref nearby = deletion-only; without = the marker's number is
unknown -> SPOT."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
lines = t.splitlines()
only, wired = [], []
for j, ln in enumerate(lines):
    if ln.startswith('|') or ln.startswith('[^'):
        continue
    for m in re.finditer(r'[a-ząćęłńóśźż]\s[*%$]\s*[.,;:]', ln):
        i = m.start()
        ctx = ln[max(0, i - 70):i + 70]
        near = re.search(r'\[\^\d+-\d+\](?!:)', ln[max(0, i - 90):i + 90])
        # page label
        lab = None
        for k in range(j, -1, -1):
            mm = re.match(r'^\[p\. ([IVXL\d]+)\]', lines[k].strip())
            if mm:
                lab = mm.group(1)
                break
        rec = (j + 1, lab, ctx, near is not None)
        (wired if near else only).append(rec)
print('%d deletion-only, %d need-the-number' % (len(wired), len(only)))
print('--- deletion-only (auto-fix) ---')
for j, lab, ctx, _ in wired:
    print('L%d p.%s: %r' % (j, lab, ctx))
print('--- need the number (SPOT) ---')
for j, lab, ctx, _ in only:
    print('L%d p.%s: %r' % (j, lab, ctx))
