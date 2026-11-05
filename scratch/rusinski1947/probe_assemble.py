# -*- coding: utf-8 -*-
"""Probe: assemble_marked + the compose join logic for the join pairs,
to see the exact para lists before/after the join."""
import sys, os, json, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947')
from paragraphs2 import assemble_marked

for n in ('0047', '0048', '0124', '0125', '0064', '0065', '0116', '0117',
          '0131', '0132', '0133', '0017', '0018', '0114', '0115'):
    paras = assemble_marked(n)
    print('=== %s (%d paras)' % (n, len(paras)))
    for k, p in enumerate(paras):
        print('  [%d] %s' % (k, p[:100].replace('\n', ' / ')))
    print('      LAST-60: ...%s' % paras[-1][-60:] if paras else '')
    print()
