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
editor has not yet looked at it.

## The reading

24 marks of doubt. Checks: copy A's land adds up to 1691 Morgen 219 rods
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
- **Doubtful names**: A no. 19 [Стурценбехеръ?], no. 43 Кинастъ
  [Мануилъ?] (B [Матеушъ?]), B no. 2 [Глебель?], no. 4 [Холмъ?].
- **Not transcribed**: the archive's stamps and numbers, the seals (the
  Commission's on 028, the Governorate Government's stamp and a wax seal on
  030), dotted leaders.

## Against Breyer's copy (53/968/0/-/716, document 4)

This table settles many of Breyer's figures and names: the original has
no. 9 Саниковскій (Breyer Скипковскій), no. 11 22-273 (Breyer 20), no. 12
14-122 (17-22), no. 20 24-187 (27), no. 29 15-188 (184), no. 37 Цельнеръ
Готфридъ (Breyer [Цельмеръ Фр.?]), no. 44 53-196 (3-196), no. 46 38-66
(61), nos. 51 and 52 14 (17), no. 60 Штаркъ Даніилъ 8-157 ([Дет.?] 8-187),
no. 61 52-94 (97), no. 65 36-254 (257), no. 71 Обстъ, no. 88 1-288 (218);
Breyer also gives nos. 45 to 48 in another order. The servitudes in the
copy read "наличный скотъ" and "плахтами" where Breyer's copy has
[паленный?] and [тлахтами?]. Breyer's copy is transcribed as he wrote it;
these are for the editor's answers on 716.

## Open

- The editor's look at the reading and at the page edges.
- The era's name (`liquidation`, a working name).
