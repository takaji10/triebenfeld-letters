# APŁ 39/98/0/-/6603

The liquidation table of the Łazińsk colony ("Колонія Лазинская", commune
of Trąbczyn), its copy of 1869 and the later entries, from the State
Archive in Łódź, fonds 39/98, Urząd Gubernialny Kaliski do Spraw
Włościańskich (Kalisz Governorate Board for Peasant Affairs). Six
documents, 1868 to 1901, on 23 page images made from 27 scans; Russian;
three are tables. Added on 2026-10-15 at the editor's request: read from
the scans in session (there was no transcription of the tables),
translated, summarised in both languages and claim-checked, with its page.
**Published 2026-10-15** at the editor's word, with APP 53/968/0/-/716. Era: `liquidation`, new on
2026-10-15 at the editor's word ("a general liquidation era ... which began
under Włodzimierz's ownership"); made one with `wlodzimierz` on 2026-10-20
(editor, "for better clarity"), which is the holding's era now.

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

18 marks of doubt (24 before the comparison with Breyer's copy and the
editor's spot sheet). Checks: copy A's land adds up to 1691 Morgen 219 rods
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
- **Doubtful names**: A no. 19 [Стурценбехеръ?], B no. 4 [Холмъ?] (kept by
  the editor). B no. 2 is Глебель and B no. 19 Стурценбекеръ, B's own
  spellings (A: Гебель, [Стурценбехеръ?]), read without doubt by the
  editor.
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

- Done: the editor's look at the reading: all 21 marks of doubt on the spot sheet
  "Doubtful readings in the liquidation table of Łazińsk" (16 rows, the
  recurring signatures asked once; `intake/spot_sheet.py`, rows in
  `review/apl399806603/readings.csv`, `queries.py --unit apl399806603
  --sheet readings.csv --port 4103`), 2026-10-15. Answered the same day
  (`intake/readings_answers.json`): 10055 70 (the pencil figure under the
  table), Глебель and Стурценбекеръ read without doubt; the rest kept,
  among them all eleven signatures ("can't tell"). 18 marks remain.
- The era's name: the era is now `wlodzimierz` (2026-10-20), whose
  working name waits on the editor (NEEDS_CONFIRMATION, "The eras").

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

Russian, in the spelling of before 1918. The table is a printed form filled in by hand, with columns for the land of each farmstead and for the dues; the copy is another hand on the same form; the inscriptions of 1894 and 1897 are certified copies on separate sheets. The tables are given as tables. Where the writing runs across an opening, the two pages are shown as one.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The archive's scans, 27 images numbered 000 to 036, show only the written pages of the file. Where the writing runs across an opening (the editor named 013/014, 026/027 and 028/029; 016/017 is the same, as the servitudes stand on the right-hand page beside the first entries), each scan was cut at its page edge, since each shows a strip of the facing page. The two halves were joined into one page image. The edges were placed in session and approved by the editor. The archive's stamps, numbers and seals are not transcribed; they can be seen on the scans.

### Transcription

There was no transcription of the tables. An AI model (Claude) read the file from the scans, each page in strips at about twice the size. The editor's notes beside the scans render some passages, the confirmations and the inscriptions, in modern spelling with an English translation; they were read against the scans, which the transcription follows, in the old spelling (ѣ, і, ъ). Words not read are marked "[?]"; words read with doubt carry "?" inside square brackets. There were 21 such marks. The editor read them all on a sheet that shows each beside a picture of its place and settled three; 18 remain, among them eleven signatures. The editor has not checked the rest of the reading.

The figures were checked by their own sums. In the table, the land of all the entries adds up to the total, 1,691 Morgen 219 rods, and the dues to 603 roubles 34⅕ kopecks. In the statement of 1896 each row was added across and each column down to the totals at the foot. This showed which figures had been misread, and that in four rows the clerk's figures, as written, do not add up: the transcription gives them as written and the notes say what the totals imply.

### Division and dating

Six documents, at the editor's choice: the table, its copy (labelled the copy, as it calls itself one), the inscription of 1884, the certified copies of the inscriptions of 1894 and 1897, and the statement after the survey of 1896. The table is dated by its confirmation, 8 February 1868, and the copy by its certification at Kalisz, 10 September 1869. The certified copies, made in 1900 and 1901, take the dates of the inscriptions they copy, 12 October 1894 and 29 November 1897, as a copy takes the date of what it copies. The statement has no date; it is dated to 1897, the year of the inscription that put its figures into the table. All six stand in the era of the liquidation.

### Tables

Three documents are given as tables: the table, its copy and the statement. The columns are those of the printed form: the entry's number, the name, the number in the draft table, the land under the dwelling and garden, arable, meadow, pasture, unusable and in all, each in Morgen and rods, and the dues in roubles and kopecks; in the statement, desiatins and sazhens. Two dots stand where the clerk wrote them for nothing, a ditto mark where the copy has one. Two later pencil figures over entries in the table stand in the name cell after a dash. The text of the right-hand page of the form follows the entries of its page.

### Translation

The English was written by the AI model from the reading. In the tables only the names and the words are translated, and every figure stands in the same cell as in the original. Names are transliterated letter by letter, without the hard sign at the end of a word, so a German name written in Russian appears in its Russian form (Merts Karl). Morgen is kept; прентъ is a rod, the Polish pręt; плахта, the cloth in which wood was carried, is a cloth-load.

### Summary

The summaries were written in German from the reading and translated into English. Each of their statements was then checked against the document. Nothing in them rests on a word read with doubt.
