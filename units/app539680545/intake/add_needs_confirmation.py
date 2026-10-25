# -*- coding: utf-8 -*-
"""Add the APP 53/968/0/-/545 entry to docs/NEEDS_CONFIRMATION.md, under
"Readings, the other holdings". Run once, 2026-10-25.
"""
import io

p = 'docs/NEEDS_CONFIRMATION.md'
s = io.open(p, encoding='utf-8').read()
anchor = '- **APP 53/968/0/-/669** (Albert Breyer'
assert anchor in s

entry = '''- **APP 53/968/0/-/545** (Breyer's sheets on the Polonised names, added and
  translated 2026-10-25, on the branch app539680545; not published;
  `units/app539680545/notes.md`): the lists read by the machine reader and
  settled on the editor's sheet (30 of 31 rows answered); the prose sheets
  0031-0033 are the editor's transcription, kept as typed, their doubtful
  words recorded in the holding's `intake/unresolved.md`; 0034 has no
  transcription (the editor's word). Open: the word read as "pronihige[?]"
  in the Themen block of 0030 (the candidates and the 3x picture are named
  in the holding's notes); whether "1843. Szuberski" is the last line of
  0025; the three doubtful names of the lists (Nowaczyński[?] of 0026,
  Micklewski[?] and Sekerowski[?] of 0029). The sheet's two unanswered rows
  are recorded in the holding's notes.

'''
s = s.replace(anchor, entry + anchor, 1)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('added')
