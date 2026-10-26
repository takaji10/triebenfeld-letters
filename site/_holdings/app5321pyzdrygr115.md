---
unit: "app5321pyzdrygr115"
title: "53/21/0/-/Pyzdry Gr.115"
lang: en
permalink: "/sources/app5321pyzdrygr115/"
alt_url: "/de/quellen/app5321pyzdrygr115/"
has_about: true
has_process: true
about_lang: en
process_lang: en
---
One page of a register of the grod court and office of Pyzdry, kept in the
State Archive in Poznań (Archiwum Państwowe w Poznaniu) in the fond "Księgi
sądu i urzędu grodzkiego w Pyzdrach", the court books of the grod court and
office of Pyzdry. The archive calls the volume "Relationes [protocollon]
1791-1792"; the page here is page 543 of it, on the editor's own trim of the
photographed page. <!-- context -->

### The fonds and its court

The archive describes the fond's contents as resignations, inscriptions,
relations, judgments, oblates, registers of cases, plenipotencies and
dissoluta. The grod court took shape at the end of the fourteenth century
and, as concerned the nobility, took within its competence the criminal
matters of the so-called four grod articles: arson, attack on a nobleman's
house, robbery on a public road, and rape. In time its competence changed
and came to cover the remaining criminal matters as well, and also matters
of land and of sums of money, and it took over the right of appeal from the
town courts. Beside the court there developed the grod office, where the
court books were kept; the office was open every day for entries of
uncontested matters, and the books had the force of the so-called public
faith. <!-- context -->

### Contents

The page carries the head of a table of the parish of Trąbczyn, in Polish:
five columns, the parish, the names of the towns, villages and demesne
farms, the agricultural hearths (dymy rolne), and two columns of dues whose
headings read "gara zyta" and "gara owcza" <span class="cite">[<a href="{{ '/documents/app5321pyzdrygr115/1/' | relative_url }}">1</a>]</span>. Seven rows stand under the
parish: the village of Trąbczyn itself, 21 hearths, 22 and 84; the parsonage
(Plebania), 4, 8 and 16; Nowawieś, 5, 10 and 20; Osiny, 6, 12 and 24; Łazy,
5, 10 and 20; Kuznia Maryantów, the smithy, 1, 2 and 4; and "Hollendry Luzne
Stare i nowe z Hutą", the scattered Hollander settlements old and new with
the Huta, 31, 62 and 124 <span class="cite">[<a href="{{ '/documents/app5321pyzdrygr115/1/' | relative_url }}">1</a>]</span>.

In every row but the first the figures double from column to column; the
village's own row, 21, 22 and 84, is the one whose middle figure does not
follow the doubling, and it stands as written, the editor to resolve it
<span class="cite">[<a href="{{ '/documents/app5321pyzdrygr115/1/' | relative_url }}">1</a>]</span>. <!-- context -->

The entry stands in the first half of the page; the rest of the page belongs
to the entry after it and is not transcribed. The table carries no date of
its own; the volume's title names the years 1791 and 1792. <!-- context -->

### The places of the table

The rows are the villages of the parish of Trąbczyn. The smithy "Kuznia
Maryantów" of the table is the Marianton of the edition, Mariantów, where
the Hohenlohe patrimonial court for Trąbczyn sat ("Actum Marianton") - the
editor's identification <span class="cite">[<a href="{{ '/documents/app5321pyzdrygr115/1/' | relative_url }}">1</a>]</span>. The one row "Hollendry Luzne Stare i nowe z
Hutą" names both Olęder colonies of the estate together, the old and the new
<span class="cite">[<a href="{{ '/documents/app5321pyzdrygr115/1/' | relative_url }}">1</a>]</span>.

The visitation of the parish made in 1791 lists the same places: the church
in the village of Trąbczyn, the inheritance of Antoni Prusimski, Starost of
Niszczewice, and in its parish Maryanton, Porąbki, the demesne farm, the
Olęder colonies old and new, Łazy, Osiny and Nowa Wieś <a href="{{ '/sources/adwl85/' | relative_url }}">85</a>. The
hearth-tax register of 1789 enters the same group with the sums they paid:
Trąbczyn, the parsonage's subjects, Łazy, Osiny, Nowa Wieś and the "Olendry
Trąbczynskie" <a href="{{ '/sources/app53640kalisztab21/' | relative_url }}">53/64/0/-/Kalisz Tab.21</a>. <!-- context -->

<!--prepared-->

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
follow. The edition's table machinery sorted a table by the numbers of its
first column and stopped on a table that has none. It was extended, and the
extension was checked the way shared code is checked here: the version
before the change, taken from the repository, and the new one were run over
every table the edition already carries, and the two outputs agree exactly
(`pipeline/review/verify_table_of_diff.py`; 12 table documents in 5 units).

The figures of six of the seven rows double from column to column; the
village's own row does not follow the doubling in its middle figure and
stands as written, the editor to resolve it.
