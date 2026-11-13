# 39/98/0/-/1333

The first part of the file "О составлении ликвидационных табелей по имению
Тромбчин владельца Миончинскаго, Слупецкаго уезда ч. I" of the Kalisz
Governorate Board for Peasant Affairs, State Archive in Łódź (APŁ), fonds
39/98 "Urząd Gubernialny Kaliski do Spraw Włościańskich". Added 2026-11-13 at
the editor's request. Six documents on 30 pages: the index of the file (1, a
table), the plan of Trąbczyn of 15 May 1865 (2, an image only), Count
Włodzimierz Miączyński's petitions of 10/22 August 1865 (3) and 23 July 1865
(4), and the Łazińsk colonists' petitions of 6/18 December 1867 (5) and 10/22
August 1868 (6). Read `intake/holding.py` first: its docstring has the
documents, the page ids and the steps.

## Provenance and images

The editor's photographs, in their folder on J: (unit.yml, `raw_dir`): the
index on scans 39_98_0_0_1333_001 to _014, and the papers named by their
number in the index and their folio (No.59_39_98_0_0_1333_88.jpg). The
folder's `_mapa.jpg` is not used. `holding.py --crop` copies each scan into
`processed/` under its page id. The plan (No.30, folio 41) was photographed
upside down and is turned. **The image named "116" is folio 115 verso**: its
text runs straight on from 115 ("Ponieważ tenże w czasie || Ukazu nie
pasał"), the editor's transcription file calls the page 115v, and the index
gives the petition three leaves from 113 (folio 116 is the start of no. 76).

## The index (document 1)

Read in two passes on 2026-11-13 (the editor's plan: a rough pass, then a
fine one at their word):

- **Rough**: four Sonnet sub-agents, one reading per page, from three bands
  per page; for the editor's first look (`review/apl399801333/index_rough.xlsx`).
- **Fine**: each page cut into eleven overlapping strips of the text columns
  at near-full size and three pieces of the figure columns enlarged 1.5x;
  eight Sonnet sub-agents, two independent readers per page run at the same
  time, neither allowed to open the other's work or the rough pass. A script
  compared them (spelling trivia normalised); Claude settled every
  difference on the strips. 146 rows (145 entries and the secretary's
  signature): 70 read alike by both, 62 settled, 14 left open. The editor
  ruled the open ones minor and settled Osiny (nos. 115, 117). The record is
  in `review/apl399801333/` (readings, `diffs.md`, `final.json`,
  `index_fine.xlsx` with a picture of each open entry); `intake/index.csv`
  was made from `final.json` once by `intake/make_index_csv.py` and is the
  source from then on.

What the comparison settled, beyond single letters:
- The minutes entries (6, 13, 16, 19, 23, 27, 31, 36, 50, 55, 58, 62, 67, 70,
  74, 77, 79, 84) are all **"Проектъ журнала засѣданія"** (draft of the
  minutes). Both readers read "Выписка" in 6-36 and "Протокъ" in 74-84; set
  side by side the word is the same everywhere, its opening the "Пр" of
  "Прошеніе".
- **Months by the clerk's numbering.** Іюня and Іюля are written alike. An
  office's papers are numbered in order: the Central Commission's no. 3600 of
  23 June 1869 (no. 114) makes nos. 119-126 (nos. 4378-4405) **24 July**;
  the Słupca commission's no. 568 before its no. 607 of 29 June makes no.
  105 1 June; the Turek commission's 801 before 806 makes no. 144 June and
  no. 142 July. No. 75 is 23 July 1865, the date of the petition itself
  (document 4).
- "Владимірова" is the 10th-district commissioner **Vladimirov** (his no.
  60 follows the district's no. 59); the colonists' letter of 1868 names
  "Komisarz Władimirow".
- Formulas the readers could not read: no. 41 "съ надписями", no. 69
  "его-же", no. 81 "ликв. таб." (the liquidation table submitted by Count
  Miączyński).
- "Гома" (nos. 89-91) is **Hohm**: the colonists' letter of 1867 is signed
  Daniel Hohm.
- Two hands: a second, rougher hand from no. 115; it writes "Коммис." where
  the first writes "Комм.".
- The folio chain (folio + leaves = next folio) breaks 16 times. Both
  readers agree on every figure, so the breaks are the clerk's: corrections
  on the page (14, 75, 77) or miscounts. They are kept as written.

The table is given with the printed heading once, on the first page. The
14 open entries and the readers' alternatives are in `index.csv` (`note`).

## The letters (documents 3 to 6)

### Sources of the text

- **Document 4 (folios 113-114), 5 and 6**: the editor's own transcription
  ("О составлении ликвидационных... Тромбчин, Слупецкаго уезда ч. I
  (39_98_0_-_1333).md", Downloads, 2026-11-13), kept as written but for the
  corrections below. Their file's English was not used (they had not checked
  it): the English is new.
- **Document 4, folios 114v, 115, 115v**: not in the editor's file. Two
  Sonnet readers transcribed them independently; they agreed word for word
  but for dashes, accents and two words, which Claude settled on the image
  (plain e, not é; "wzrasli", not "wzrośli"; "Łask").
- **Document 3 (folios 88-89v)**: not in the editor's file; transcribed at
  the editor's word (2026-11-13) by two Sonnet readers and settled by Claude
  on the images. Settled from context and confirmed on the image: "w celu
  przyłączenia" (readers: "wielu"), "w ścisłem zastosowaniu" ("usilném",
  "istém"), "w myśl Art. 2" ("wymyśl", "wymysł"), "przeszły w rozporządzenie
  dziedziców" ("wrozu ze drzenie"), "upraszać ma zaszczyt" ("na"),
  "opuszczający", "z wolą", "Ztąd", "podaje", "dołącza się". The left margin
  of 89v carries the petition's own dateline, "Kalisz dnia 10/22 Sierpnia
  1865", and "Dowody w liczbie sztuk 4 dołącza się".

### Corrections to the editor's transcription

The editor's word: correct only a glaring error, from context first, the
image only where context cannot settle it. A Sonnet sub-agent read each
suspect word on the image without being told the suspicion
(`review/apl399801333/letters/check/check.json`); Claude looked again at
every medium or low reading. Changed:

| Folio | Was | Now | Evidence |
|---|---|---|---|
| 113 | z koni i 7in | 2 koni i 7iu | image: the figure 2; 113v "siedmiu sztuk bydła i dwóch koni" |
| 113v | ugotowało | ugorowało | image; 114 "to pole ugorowało" |
| 114 | zmierciłem | zmieniłem | image (high) |
| 114 | ugorowała | ugorowało | image; "pole" is neuter |
| 163 | zamieszkaych | zamieszkałych | image ("zamieszka-/łych") |
| 163 | dawno Dominium | dawne Dominium | image; one grammatical reading |
| 163 | wrb. | w. r. b. | image (w roku bieżącym) |
| 163 | prawo do służy | prawo to służy | image ("to / Służy") |
| 163 | Daniel Hohm, Wilhelm Moritz | xxx Daniel Hohm, xxx Wilhelm Moritz | image: their marks, three crosses each |
| 176 | v Dziedzica | b. Dziedzica | image (b. underlined, były) |
| 176 | przywilejów prowa | przywileju prawa | image |
| 176 | gając się w Boru Jurami | [gajć?] się w Boru furami | image; "furami", with carts |
| 176 | i a prócz | i oprócz | image |
| 176 | v mórg | 6. mórg | image (high) |
| 176v | bremior | rewior | the same word "Rewiory" two lines below, "Rewiorże" on 176 |
| 176v | zrobił v 11 | zrobił 11 | image: "zro-/bił 11" |
| 176v | dałem, po 12 Rubli | dał im, po 12 Rubli | image (high); the owner paid, not the writers |
| 176v | swiaden | świadek | image |
| 177 | następuje | następnie | image (high) |
| 177 | pawłorną | powtórną | image |
| 177 | browienią | bronienia | image ("bro-/nienia") |
| 177v | załwierdzić | zatwierdzić | image (high) |
| 177v | kaszta | koszta | image ("kosz-/ta") |
| 177v | krzywdym ale | krzywdy, ale | image (high) |
| 177v | przychy lić | przychylić | image (high) |
| 177v | przywraći | przywróci | image; one grammatical reading |
| 177v | (missing) | O co w najgłębszej pokorze błagamy. — | image: a line above the signatures the transcription leaves out |
| 177v | Najunizensi | Najuniżensi | image |
| 163 | u[?]głąbonem | [uszgłębonem?] | image; on the spot sheet |

Left as transcribed although the image differs in spelling (not glaring):
"hipotecznej" (written "hyppotecznej"), "w każdym czasie" ("w każdem
czaśie"), "Krystianowi" ("Krystjanowi"), "majem territorium" (on the spot
sheet). The editor's expansion "Wielmożnego" (written "Wgo") on 163 stays.
The dashes of the editor's file (" - ") are written " — ", the edition's
punctuation dash; the export's escaping backslashes are dropped.

### Conventions

The letters are transcribed **by paragraph** (`rulings.yml`, `pages:
by_paragraph:`). The catchwords stand on lines of their own at the foot of
88 ("osad"), 88v ("z usilną", `catchwords.yml`) and 89 ("uwłaszczeni").
"osad" is put after the office's notes, as the last line of the page, so
the line-break pass finds it. The word divided across the page end at
113/113v ("przedsta-/wiam") is joined by a held decision in
`linebreak_decisions.csv`.

### The office's notes on folio 88

In the left margin of the first page of document 3: the Commission's
resolution in Russian, eight lines, and below it a receipt in Polish. Set
apart in `office_notes.yml` and put at the end of the page. The Russian is
only partly read: "Объ [обмѣнѣ?] признать земли, которыя были прежде заняты
крестьянами пустками — но такъ какъ ихъ возвратить нельзя, то поручить
[Комм…?] добровольную сдѣлку, а потомъ назначить." The receipt: "Dowody
[oddane?] odebrałem. / Kalisz dnia 11 [Paźdz.?] / [A. Kowal…?]". On the spot
sheet.

Not transcribed: the pencil note at the head of 176 (Russian, a few words),
the archive's folio numbers and stamps, the pencil "167" and "A M" at the
foot of 163.

## English and summaries

Translated in session, no paid run (`intake/english1333.py`); the index's
English is a column of `index.csv`. Forms: folwark, servitude, commissioner,
the Constituent Committee and the Central Commission, Morgen and rods,
Nowawies (the edition's form for the Nowa Wieś of Trąbczyn), "manorial
lordship (Dominium)". "smugi" stays Polish. "[gajć?] się" and "ugaj"
(176-177) are words not understood and stay in Polish in the English. The
catchwords are not said in the English.

`check_translations.py` raises 124 number rows: the clerk's two-digit years
("65 г."), which the English writes in full (1865), and figures the check
reads glued to the next cell of the table ("1,350.,2,185"). None is a
discrepancy. Its marker rows count only its own forms of doubt; every doubt
mark of the text is in the English.

Summaries: `intake/summaries1333.py`, German first, English from the
German; claim check `intake/claim_check.yml`.

## Open

- The spot sheet (`intake/spot_sheet.py`, served by
  `pipeline/review/queries.py --unit apl399801333`): seven readings of the
  letters and the office's note.
- Łazińsk: the register leaves the bare Polish form unmatched until the
  editor says (reference/places.yml, `trabczynskie-stare-oledry`), so the
  colonists' letters do not yet link to the colony (NEEDS_CONFIRMATION).
- People: Krystian Lippeldt, Baron von Rosen, Vladimirov, Daniel and Wilhelm
  Hohm, Wilhelm Moritz, Ludwig Hintz, Krystyan Sehr, Grodziecki, Swiderski,
  Rywarski, Libner, Janicki, Sowiński, Czajka: no person entries yet
  (NEEDS_CONFIRMATION).
