# APP 53/968/0/-/716

Albert Breyer's notebook "Łazińsk, Emilienheim, Ликвидац. табель" (archive's
title "Łazińsk [pow. słupecki, woj. poznańskie - notatki, statystyka]
1937"), with a loose sheet of 1858 laid in it: thirteen documents, 1858 to
1936, on 34 pages of the notebook and the sheet (40 document pages, as a
page holding the end of one document and the start of the next stands
under both), with the archive's title page and the cover in front. Russian,
German and Polish; six documents are tables. Added on 2026-10-14 at the
editor's request: read from the editor's photos in session (there was no
transcription), translated, summarised in both languages and
claim-checked, with its page, a timeline entry (29 June 1868) and a
paragraph in the story. **Built and committed; not published.** The editor
approved the folds and page edges (2026-10-15) and answered both spot
sheets; it waits for their word.

Everything about how the holding was made is in the docstrings of
`intake/holding.py` (the steps), `intake/photos.py` (the images),
`intake/text716.py` (the reading and its conventions) and
`intake/english716.py` (the English).

## Division (the editor's choice, 2026-10-14: by content)

1 the sheet of 1858 (table); 2 the Emilienheim liquidation table of 1868
(table); 3 Breyer's extracts on Emilienheim, 1870 and 1892; 4 the Łazińsk
liquidation table, Słupca, 29 June 1868 (table), with Breyer's pencil of
1875; 5 the Łazińsk servitudes (copy); 6 Breyer's counts 1875 to 1914; 7
farmers and Morgen of (by its figures) Łazińsk, 1840 to 1935 (table); 8
notes of July 1935, Huta Trąbczyńska, Orlin, Józefów and the morals of the
settlers; 9 the farmers of the Orlin Hauland Biskupice (table); 10 notes on
Orlin, July 1936; 11 the Orliny liquidation table (table, undated); 12
Breyer's notes on the separation; 13 the Orliny servitudes (copy, undated).
Places and dates: `rulings.yml`.

**A copy takes the date and era of what it copies** (editor, 2026-10-14:
"a copy of an 1828 document from 1939 should not belong to the 20th
century"). The holding was first built as eleven documents, two of which
held a copy and Breyer's own notes together; they were divided the same
day (old 5 into 5 and 6, old 11 into 12 and 13; numbers from 6 on moved).
Documents 1 to 5, 11 and 13 stand in the era `wlodzimierz` (per-document
`era:` in `rulings.yml`), the rest in the holding's `twentieth-century`.
Document 3 is dated by its first entry (26 November 1870), 5 to 1868 (the
year of the table it follows), 11 and 13 are undated.

## Images

The editor's raw photos IMG_5159 to IMG_5180 (CR2) in the unit's folder.
`intake/photos.py` takes the camera's full-size JPEG out of each and cuts
it to the paper (BOXES; IMG_5160 turned 90°) into `photos/`;
`holding.py --crop` cuts the openings at the fold (FOLDS, placed in
session) into `processed/`. IMG_5159: only the archive's title page is
taken (editor). IMG_5168 repeats IMG_5169 and is not used; the blank
inside front cover (5163_a1) is left out. The fold page is
`review/app539680716/folds/index.html` (`holding.py --sheet`); the editor
looked at it and let the folds and edges stand (2026-10-15: "The page
edges look fine"). Page edges (2026-10-15, the editor): the back
of the sheet of 1858 (IMG_5161) is cut at its fold, x 2260, where its
writing ends, and the last page (IMG_5180) at x 1680, before the inside
back cover (`EDGES` in `holding.py`, the first proposal; the green lines
of the fold page move them). The blank lower half of IMG_5161 is still in
the picture: the lines are vertical only.

## The reading

35 marks of doubt (68 before the editor's answers on two sheets and the comparison with the original). The tables follow the edition's convention (number
first, name second; abbreviated numbers in full; the copyist's dash after
a name dropped; a heading repeated on a page given once). In the Łazińsk
table Breyer's pencil of 1875 stands in the name cell after " — ".

- **Breyer's sum on 5176_a2** (document 10) is 1157.69 Morgen; his figures
  (17 + 370 + 464.69 + 300) make 1151.69. The photo shows the figures as
  read. The summary says so; the text is not corrected.
- **The heading of document 9** (5174_a2) is four lines of Kurrent. Read
  first as "[?] von dem Orliner Hauland Biskupice [?] [?] [?] [?] [?]";
  read again on a closer picture (2026-10-14) as "... gehörig, sämtlich auf
  das Buch ...". The editor's reading (2026-10-15): "von dem Orliner Hauland
  zu Biskupice gehörig, sämtlich au[f/s?] das [?]". Their answer begins at
  "von dem"; the long first word, on its own line, is not read and stays
  "[?]" before it.
- **Spot sheet** "Readings in Breyer's Łazińsk notebook": 17 rows
  (`intake/spot_sheet.py`, port 4102), the readings a name, a place, a
  heading or the sense rests on. Not asked: the doubtful names of the
  Russian tables (documents 2, 4, 11) and the pencil of 1875, which the
  editor may not read in Cyrillic; the rest of document 8's marks.
- **The editor's answers** (2026-10-15), worked into `intake/text716.py`
  and `intake/english716.py`: переименов. (renamed), Тромбчинъ (the
  commune, Trąbczyn), Jesswein, Hufe, Holędry, Skrzydlewski, Tilson,
  Seling and geworden ("Bankrott geworden", went bankrupt) read without
  doubt; Maradza for Mądrosza (the editor: a locality called Maradz is
  likely meant); [Zrost?] for [Zwrsze?]; Polzfu[h?]l for [Rohrfuss?]; the
  heading of document 9 as above. Kept with their doubt: [7.?] on the sheet
  of 1858, [паленный?], [Jäke?], [Jaschek?] (the editor could not tell).
  The summaries of documents 3, 4, 8 and 10 now say what the settled words
  allow (the renaming of 1892, the commune of Trąbczyn, Jesswein, the
  heading Holędry Orliny Biskupicki, the bankruptcy); recorded in
  `intake/claim_check.yml`.
  The answers as saved are kept in `intake/readings_answers.json`.
- **Second spot sheet** "The other readings in Breyer's Łazińsk notebook"
  (2026-10-15, at the editor's request): `intake/spot_sheet2.py`, rows in
  `review/app539680716/readings2.csv`, answers in `readings2_answers.json`
  there; port 4102. All 46 marks not yet asked, each Cyrillic word also in
  Latin letters, and one unmarked reading a second look put in doubt: the
  first name of the forestry plan on 5172_a1, read Вдовьiй боръ, which may
  be Вельскiй боръ, the forest of the Orliny servitudes (s47). The picture
  of s46 suggests напоръ is broken across two lines ("на-" / "поръ").
- **The editor's answers on the second sheet** (2026-10-15, 18 of 47 rows;
  kept in `intake/readings2_answers.json`): Дикгофъ, Диконфъ, Кинастъ,
  Обстъ, Готтлибъ and Дет. read without doubt; "Eingeschrieben jedoch"
  (not "j. Wloch"); Цельмеръ Готф. (not Фр.); Шмехель, Schmechel (not
  [Шменель?]); "nur[?]" for [пол.?] twice, the editor's form for a word read
  with doubt, which the English gives as "[uncertain: nur]". Kept with their
  doubt: [Мар.?], [Брушк.?], [Франц.?], [Бромке?], [Геп.?], [Пашка?],
  [Торно?]. The answered rows are taken off the sheet (`ANSWERED` in
  `spot_sheet2.py`); 30 rows remain, with s20 and a new row s48 giving the
  original's плахтами and наличный (APŁ 39/98/0/-/6603, document 2).
- **The rest of the second sheet** (2026-10-15, the last 28 rows; every row
  now answered and in `ANSWERED`). Read without doubt: Brenda, "schlagen
  sich", Gottfr. twice (doc. 9, nos. 24, 25), Вангольдъ (doc. 11, no. 20),
  Студзенка for [Стурценгеръ?] (doc. 11, no. 8), "1909 9 Nov. hat das
  aufgehört" for "1909 [?] hat das [entgekoit?]", "mit d." for "mit
  [L…?]", Велькiй боръ for Вдовьiй боръ (the editor: "It's Velkiy"; no с
  is to be seen on the picture). Changed, still doubtful: [Бонцлеръ?] for
  [Бенцлеръ?] (doc. 4, no. 89), [Гредъ?] for [Бредъ?] (the editor: the first
  letter is a G), […etli…?] for [Sattlern?], [Solten?], [Zoget.?],
  [Crist.?], and [топоръ?] (an axe) for [напоръ?] (the editor: the first
  letter may be т; the sense, an axe for grubbing stumps, agrees). Kept
  with their doubt ("can't tell"): [Гедпаръ?], [Frierk?], and in doc. 11
  [Ланитцъ?], [Гралька?], [Веречъ?], [Дайгеръ?], [Ш.?], [Куркина?],
  [Шпицеръ?], [Шиммеръ?], [Курвина?].

- **Against the original table** (APŁ 39/98/0/-/6603, 2026-10-15, at the
  editor's request: "It should match the actual table"). Every row of
  document 4 was compared with the original and each difference looked up
  again on the photo. Corrected, as misreadings of Breyer's hand: nos. 11
  (22), 12 (14), 18 and 20 Саниковскій, 20 (24), 25 Промистъ, 44
  (53, the 5 left of the ruled line), 51 and 52 (14), 60 (157), 61 (94),
  65 (254), 83 Феттеръ, 87 (1-288); in document 5 наличный (was
  [паленный?]) and тлахтами without doubt (Breyer's т, his slip for
  плахтами).
- **Names standardised to the original** (the editor, 2026-10-15: "Don't
  use Breyer's spelling, standardise it to the actual liquidation table").
  Where Breyer spelled a name otherwise than the original's table
  (6603, document 1), it now stands as the original writes it; his
  abbreviations stay where they fit the original's name. Breyer wrote:
  Мержъ (nos. 3, 5, 16, 17, 49, and the pencil at 10; now Мерцъ),
  Скипковскій Март. (9; Саниковскій Марцинъ), Март. where the original
  has Марцинъ (17, 28, 68), Кнакфусъ (31; Кнафкусъ), Штирценбекеръ (41,
  84; Штирценбехеръ), Эман. (43; Матеушъ), Дет. (60, the editor's reading
  of Breyer; Даніилъ), Кинастъ and Тарновскій after Нас. (63, 88; the
  genitive Кинаста, Тарновскаго), and in the pencil Шенфишъ (85;
  Шейнфишъ) and Хиршъ (86; Гиршъ). No. 19 stays Стирценбехеръ: the
  original's own reading there is in doubt. **Zelmer is always written
  with m** (the editor: "there's no Zelner, ever in this project"):
  Цельмеръ at nos. 37, 50, 53, 65 and 67, and the same in 6603.
- **Figures follow the original too** (the editor, 2026-10-15: "The
  original liquidation table is the authority with the numbers - you may
  have transcribed Breyer's incorrectly, or he might have made mistakes").
  Every figure of document 4 was compared with the original; four
  differed and now follow it: no. 12 122 rods (read 222), no. 29 188 (read
  184), no. 46 38-66 (read 38-61, written over a struck 42-99), and nos.
  47 and 48 in the original's order and numbering (Breyer: 47 Бандзертъ,
  48 Зееръ; each row keeps its name, figures and pencil). Whether these
  were Breyer's slips or misreadings is not decided.

## The English

`intake/english716.py`. In the tables only names and words are translated
and every figure keeps its cell; Russian names are transliterated letter by
letter (Shults Gotfr.), without the final hard sign. A cell holding a
figure of four digits inside words ("4420 roubles") is written quoted, as
the house forms group it (4,420) and an unquoted comma would split the
cell (`holding.py`, `english()`).

## Summaries

`intake/summaries716.py`, claim-checked in `intake/claim_check.yml`: 86
statements, 16 weakened or cut (the first draft told what the tables do
not say, counted rows wrongly where numbers are skipped or doubled, and
named people from the Russian tables in German forms).

## Index and checks

- People: `kuh` shut out of document 8 ("Kuh", a cow), `neumann` out of
  document 9 (a farmer of Orlin, not the edition's Neumann).
- Glossary: Kl., Wirte and dt. (after "geb.") ruled out.
- The translation check raises "Schenk" in document 8: it is "schenkte"
  (gave), not the name. Nothing to do.

## Open

- Settled (editor, 2026-10-15): Michalina died on 19 January 1851 and
  Włodzimierz on 20 December 1879, so 1858 to 1870 are his years. His
  nephew Władysław Miączyński became heir; the edition has no era for the
  years after 1879 yet, and no document of them.

## Damage

None recorded.
