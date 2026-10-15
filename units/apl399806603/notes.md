# APŁ 39/98/0/-/6603

The liquidation table of the Łazińsk colony ("Колонія Лазинская", commune
of Trąbczyn), its copy of 1869 and the later entries, from the State
Archive in Łódź, fonds 39/98, Urząd Gubernialny Kaliski do Spraw
Włościańskich (Kalisz Governorate Board for Peasant Affairs). Six
documents, 1868 to 1901, on 23 page images made from 27 scans; Russian;
three are tables. Added on 2026-10-15 at the editor's request: read from
the scans in session (there was no transcription of the tables),
translated, summarised in both languages and claim-checked, with its page.
**Built and committed; not published.** Era: `liquidation`, new on
2026-10-15 at the editor's word ("a general liquidation era ... which began
under Włodzimierz's ownership").

Everything about how the holding was made is in the docstrings of
`intake/holding.py` (the steps), `intake/text6603.py` (the reading and its
conventions) and `intake/english6603.py` (the English).

## Division (the editor's choice, 2026-10-15: six documents)

1 the table, confirmed 8 February 1868 (scans 000 to 014; table); 2 its
copy, Kalisz, 10 September 1869, labelled the copy as it calls itself one
(015 to 029; table); 3 the inscription of March 1884 in the copy (the end
of 028/029 and 030); 4 the certified copy (1900) of the inscription of 12
October 1894 (031, 032); 5 the certified copy (1901) of the inscription of
29 November 1897 (033); 6 the statement after the survey of 1896 (034 to
036; table). Relations: 2 copies 1; 3 is entered in 2; 4, 5 and 6 in 1
(two new relation kinds, `copies` and `entered_in`, labelled in
`i18n.yml`).

## Images

Page ids are the scan's number and side, `0001_a` for scan 001, as
`match_scans.py` reads them (`NNNN_[a-h]`); a first try with "013_014" did
not parse. The openings 013/014, 016/017, 026/027 and 028/029 (the editor
named the first three; 016/017 has the servitudes beside the first
entries) are joined: each scan cut at its page edge (`EDGES` in
`holding.py`, placed in session) and the halves set side by side as the
left scan's page (`0013_a` and so on). The fold page
(`review/apl399806603/folds/index.html`) shows the green edge lines; the
editor let them stand (2026-10-15: "The page edges look fine").

## The reading

21 marks of doubt (24 before the comparison with Breyer's copy). Checks: copy A's land adds up to 1691 Morgen 219 rods
and its dues to 603 roubles 34⅕ kopecks; every row and column of the
statement was added.

- **The statement's slips**: as written, rows 2, 5, 13 and 38 do not add up
  (by 2, 200, 10 and 6 sazhens). The columns show where: the totals at the
  foot imply 986 (not 984) for row 2's arable, 342 (not 542) for row 5's
  buildings, 2114 (not 2104) for row 13's meadow and 318 (not 312) for row
  38's arable. The photo shows the figures as read; they stand as written.
- **Copy B against A**: no. 65 has 36-234 (A 254, which the total
  confirms); no. 48 only "Мурицъ" (A: "Мурицъ" struck through, "Бандзертъ
  Морицъ" written under it); no. 91 without its sum of dues. Names in B in
  its own spelling (Мартинъ for A's Марцинъ, Іосифъ for Осипъ).
- **Doubtful names**: A no. 19 [Стурценбехеръ?], B no. 2 [Глебель?], no. 4
  [Холмъ?].
- **Not transcribed**: the archive's stamps and numbers, the seals (the
  Commission's on 028, the Governorate Government's stamp and a wax seal on
  030), dotted leaders.

## Against Breyer's copy (53/968/0/-/716, document 4)

Compared row by row on 2026-10-15 at the editor's request ("It should
match the actual table"), each difference looked up again on Breyer's
photo. Most were misreadings of Breyer's hand, now corrected in 716: his 4
is shaped like Ч (nos. 12, 20, 51, 52, 61, 65), his 5 has a flat top (no.
60), his н and п are both shaped like a Latin n (наличный, Саниковскій,
Промистъ), and some figures stand across the ruled
line (no. 11 22, no. 44 53) or are plain (no. 87 1-288). What Breyer did
write otherwise: Мержъ for Мерцъ, Скипковскій for Саниковскій (no. 9),
Кнакфусъ, Штирценбекеръ, Кинастъ Эман. for Матеушъ (no. 43), and other
names; at the editor's word (2026-10-15) his names in 716 now follow this
table's spelling (716's notes list them). The figures in 716 follow this
table too (the editor: "the authority with the numbers"): no. 12 was read
222 rods (original 122), no. 29 184 (188), no. 46 38-61 (66, written over a
struck 42-99), and nos. 47 and 48 stood in the other order. Breyer's
тлахтами for плахтами in the servitudes stands as he wrote it.

**Zelmer is always written with m** (the editor, 2026-10-15: "there's
no Zelner, ever in this project"): Цельмеръ at nos. 37, 50, 53, 65 and 67
in the table, its copy and the statement (read Цельнеръ at first; the
clerk's м is easily taken for н).

The comparison settled one doubt in this holding too: no. 43 is Матеушъ in
the table, its copy and the statement alike (was [Мануилъ?] and
[Матеушъ?]).

## Open

- The editor's look at the reading: all 21 marks of doubt on the spot sheet
  "Doubtful readings in the liquidation table of Łazińsk" (16 rows, the
  recurring signatures asked once; `intake/spot_sheet.py`, rows in
  `review/apl399806603/readings.csv`, `queries.py --unit apl399806603
  --sheet readings.csv --port 4103`), 2026-10-15.
- The era's name (`liquidation`, a working name).
