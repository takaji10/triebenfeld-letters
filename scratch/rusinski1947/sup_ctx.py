# -*- coding: utf-8 -*-
"""Context + page + note-defs for each superscript candidate."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', '..', 'literature', 'rusinski1947',
                      'original.md'), encoding='utf-8').read()
lines = t.splitlines()
WANT = (444, 833, 835, 1321, 1450, 1764, 1894, 2045)
for wl in WANT:
    # find the nearest preceding page label
    lab = None
    for j in range(wl - 1, -1, -1):
        m = re.match(r'^\[p\. ([IVXL\d]+)\]$', lines[j].strip())
        if m:
            lab = m.group(1)
            break
    print('=== line %d (p. %s)' % (wl, lab))
    print('   ' + lines[wl - 1][:220])
    # note defs of that page block
    if lab:
        blk_start = next(j for j in range(wl - 1, -1, -1)
                         if re.match(r'^\[p\. ', lines[j].strip()))
        blk_end = next((j for j in range(blk_start + 1, len(lines))
                        if re.match(r'^\[p\. ', lines[j].strip())),
                       len(lines))
        defs = [lines[j][:150] for j in range(blk_start, blk_end)
                if re.match(r'\[\^%s-\d+\]:' % lab, lines[j])]
        for d in defs:
            print('   DEF ' + d)
