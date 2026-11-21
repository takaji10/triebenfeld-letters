# -*- coding: utf-8 -*-
"""Furniture sweep: find running-head / binder-mark remnants in the
body text: series-title strings, and short junk lines."""
import os, re, sys
MD = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
      r'\rusinski1947\literature\rusinski1947\original.md')
t = open(MD, encoding='utf-8').read()
lines = t.splitlines()
cur = None
for j, ln in enumerate(lines):
    m = re.match(r'^\[p\. ([IVXL\d]+)\]', ln.strip())
    if m:
        cur = m.group(1)
        continue
    s = ln.strip()
    if not s or s.startswith('[^') or cur is None:
        continue
    if not cur.isdigit() or not (1 <= int(cur) <= 144):
        continue
    # series-title strings
    if re.search(r'(?i)prace komisji atlasu|polska akademia|akademii '
                 r'umiej', s):
        print('SERIES  p.%s L%d: %r' % (cur, j + 1, s[:100]))
        continue
    # short junk lines (<= 8 chars, not table/heading syntax)
    if len(s) <= 8 and not s.startswith(('|', '#', '-', '*', '[')) \
            and not re.fullmatch(r'[IVXL]+|\d+|[a-ząćęłńóśźż. ]{1,8}',
                                 s.lower()) is None:
        pass
    if len(s) <= 8 and re.fullmatch(r'[A-Za-z0-9ąćęłńóśźż .,;:!?-]{1,8}',
                                    s):
        print('SHORT   p.%s L%d: %r' % (cur, j + 1, s))
