The holding came ready transcribed: the editor's own reading of the table,
given as a spreadsheet export ("Relationes [protocollon] 1791-1792 (53_21_0_-
_Pyzdry Gr.115) - Sheet1.csv"), one heading row and seven rows, five cells
each. The file is kept as `intake/table.csv`, as received, and everything
else is made from it.

The folder holds two photographs: the editor's own trim of page 543
(`543_trim.jpg`) and the spread (`542v-543.jpg`). Only the trim is used, at
the editor's word: page 543 is the page of the unit in focus. The trim is a
single page already, so no fold is placed and no crop is made; the intake
script (`intake/holding.py`) copies the one page whole under the page id
`0543_a`, by the way of the hearth-tax register (APP 53/64/0/-/Kalisz
Tab.21).

The transcription covers the table in the first half of the page, at the
editor's word; the rest of the page belongs to the entry after the table.
The document therefore has one page and nine corpus lines: the heading row,
which opens the table, and the seven rows of the parish.

One reading was changed, at the editor's word given in chat (2026-10-26):
the heading's first cell, "Parofie", is "Parafie". The change is applied by
the intake script's `--correct` and logged in
`transcription_decisions.csv`; everything else stands as the editor typed
it, diacritics included only where they gave them.

The table has no column of entry numbers: the parish stands in the first
cell, filled on the village's own row and empty under it, and the figures
follow. The table machinery sorted a table by the numbers of its
first column and stopped on a table that has none. It was extended, and the
extension was checked the way shared code is checked here: the version
before the change, taken from the repository, and the new one were run over
every table already built, and the two outputs agree exactly
(`pipeline/review/verify_table_of_diff.py`; 12 table documents in 5 units).

The figures of six of the seven rows double from column to column; the
village's own row does not follow the doubling in its middle figure and
stands as written – the transcription is the editor's own and correct.
