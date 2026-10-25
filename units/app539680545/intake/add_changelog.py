# -*- coding: utf-8 -*-
"""Add the APP 53/968/0/-/545 entry to docs/CHANGELOG.md, dated 2026-10-25.
Run once.
"""
import io

p = 'docs/CHANGELOG.md'
s = io.open(p, encoding='utf-8').read()
entry = '''## 2026-10-25 - APP 53/968/0/-/545 added and translated (branch app539680545; not published)

- The holding built: Albert Breyer's ten photographed research sheets on the
  Polonisation of German surnames in the gmina Zagórów, seven documents on
  ten pages (the folder photograph left out; 0034 carried as "(skipped)",
  shown but not transcribed, at the editor's word). All scans paired.
- The four list sheets read by the machine reader in bands and settled on
  the editor's spot sheet "Readings in Breyer's sheets 1" (30 of 31 rows
  answered 2026-10-25; two rows unanswered, recorded in the holding's
  notes). The prose sheets 0031-0033 are the editor's own transcription,
  kept as typed; their doubtful words recorded in
  `units/app539680545/intake/unresolved.md`.
- Translated in session (intake/translation/, write_cache.py); the check
  clean after it caught the page split of document 5, the edition's Wrocław
  for Breslau, and doubt marks the German does not carry.
- Summaries written in both languages in session
  (intake/write_summaries.py) and claim-checked in session
  (intake/claim_check.yml): 33 statements, two corrected in the draft (the
  "Gem. Zagórów" line, and where the schools lie).
- The holding's page written in both languages; check_unit_text clean after
  it caught four citations ordered so the years stood past the documents
  that carry them.
- Two shared repairs: the pipeline self-check had failed on main since the
  gazetteer merge (its place-name mapping now carries the file waiver), and
  a stale translation record of kuryerpolski1754075-001 (the item moved to
  the newspapers section) removed by publish_translations.py.
- The edition guide's counts corrected (626 documents, 2,021 pages) and the
  Poznań bullet extended, English and German.

'''
i = s.index('## 2026-10-24 - Published')
s = s[:i] + entry + s[i:]
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('added')
