# APP 53/968/0/-/783

One document on five pages, with the archive's cover before it: a printed
summons of 1860 in Polish, the copy served on Karolina Fridenberg of the
Staro-Łazińska colony, by which Count Włodzimierz Miączyński of Trąbczyn
counterclaims against 97 colonists over pasture and wood-gathering in his
forest. Added on 2026-10-13 at the editor's request: pages cut, the
editor's Polish checked against the scans, the English written again,
summarised in both languages, with its page. **Published at the editor's
word on 2026-10-14**, after they approved the folds, answered the spot
sheet on the pen marks and read the page of changes.

Everything about how the holding was made is in the docstring of
`intake/holding.py`.

## Provenance

Archiwum Państwowe w Poznaniu, fonds 968 (Albert Breyer - spuścizna), unit
783. The editor gave the reference, the archive's title and the archive's
description of the fonds (`reference/sources/app_spuscizna_alberta_breyera.md`).
The second holding from these papers, after 53/968/0/-/801. That one is
Breyer's own copies; this one is an original of 1860 that he collected.

- **Images.** Four: `Image00004.jpg` the cover, `Image00005.jpg` page 1,
  `Image00006.jpg` pages 2 and 3, `Image00007.jpg` page 4 and the note of
  service.
- **Pages.** `0004_a` (the cover, front matter before the document, as in
  801), `0005_a`, `0006_a1`, `0006_a2`, `0007_a1`, `0007_a2`.
- **Folds** of the two openings: 2520 on both, read off strips of the
  gutter, and approved by the editor as proposed (2026-10-14; their file
  is `intake/folds.json`).
- **The cover** has the fonds stamp, the archivist's title in pencil in
  square brackets, the date "1860. 7/19. X.", the stamp with "Spuśc. A
  Breyera" and "783", and a struck-out "567". The pencil title has "z
  kolonii Staro-Łozińskiej" after the name and writes the Count
  "Mięczyńskim"; the title the editor gave (the archive's catalogue) differs
  in both and adds "pow słupski". The print itself has "Łazińskiej"
  throughout, and "Miączyński".

## What the paper is

Four printed pages and a fifth with the printed form of the note of
service. One summons was printed for all defendants and the court summoner
(woźny) completed each copy in pen. On this copy his hand wrote:

- page 1: the line naming himself ("Ja niżej podpisany woźny ... w Kaliszu
  mieszkający —"); corrections to the printed list (below); a margin note;
- page 4: his signature under "d. j. w.", and at the left "Koszta" and a
  line read "Raz Rs [47?] k 21." (razem, in all, silver roubles and
  kopecks; the figure 47 is blotted). If 47 roubles 21 kopecks is right it
  is the cost of serving all 97, about 49 kopecks each: a thought, not in
  the text;
- page 5: "No 173.", the name "Karolinie Fridenberg", "Staro" twice, the
  words "do rąk własnych oddałem świadczę —", the date and his signature.

Not transcribed: the revenue stamp (double eagle, "7½ КОПѢЕКЪ", "KOP:
SIEDM I PÓŁ"); a pen note "Odp" with a flourish beside it at the head of
page 1, probably "odpis", copy; red pencil underlinings ("Staro-Łazińskiej",
"mieszkającego", "Nowo-Łazińskiej", "14", "Studzianka", "Starosty
Nieszczewickiego", "Bogumiłem Karolem Wejgel"), which look like a later
reader's; the summoner's paraph.

## The check against the scans (2026-10-13)

All five pages read against the scans. 34 corrections (`ROWS` in
`holding.py`, logged in `transcription_decisions.csv`) and five added lines
(`ADDED`). The editor's text reads like machine recognition of the print:
its slips are of that kind ("Scbonfisch", "czynszowmkami", "lego", "tein",
"wjłącznem", "§111" for "§ III", "11stu" for "14stu", "10/28" for "16/28").

- **The print's "é"** is "e" in the editor's text and stays so.
- **Struck-out text** is left out (the rule of 2026-10-05): "Jerzego vel"
  before "Bogusława Gerke" in no. 24, and the printed no. 58, "Jerzego a
  raczej Bogusława Gerke". The print had the same man twice; the summoner
  kept him as no. 24 and gave no. 58 to another.
- **The printer's own slips** are given as printed: "pozołą" (no. 60, for
  pozostałą), "Tąbczyńskich" (page 2, for Trąbczyńskich), "podzielac".

## For the editor's eye

These are on the page of changes (`review/changes/index.html`) or need a
look at page 1. None is built on.

1. **No. 58, the margin.** "Marcina" and a surname: Hetke, Hecke or Heck.
   Given as "[Hetke?]"; **the editor read "Heck"** (spot sheet,
   2026-10-14). Under it is the summoner's paraph, not a third word.
2. **No. 7, "Jana Fryderyka Rasch".** The printed second name is covered by
   pen strokes. Struck out, or written over with another name? Left as the
   editor read it.
3. **No. 55, "Henryka Celmer".** The first letter is written over in pen
   and looks like a Z. Left "Celmer". The English has Zelmer either way.
4. **No. 70, "Krystjana Grünwald".** The "ja" is written over in pen.
   **The editor read Krystof** (2026-10-14): the line is now "Krystofa
   Grünwald", the printed ending "a" kept, the accusative of the list.
5. **Nos. 53 and 54** have a pen "c" over a printed letter: "Rogackiego" in
   both. The editor had "Bogackiego" for 53; the print's first letter is R.

**The editor's answers on the spot sheet "Pen marks on the summons"**
(2026-10-14): no. 58 is Marcina Heck; no. 70 Krystofa Grünwald; the costs
47 roubles 21 kopecks; nos. 7, 53, 54 and 55 stand as they were. Applied by
`intake/spot_answers.py` (a record, not to be run again) and logged in
`transcription_decisions.csv`.

## The English

Written again from the corrected Polish (`ENGLISH` in `holding.py`); the
reasons are in the docstring and the main differences in
`intake/changes.yml`. Choices a later session should know:

- **"Kolonja"** is two things in the paper: the settlement ("kolonja
  Staro-Łazińska", the Staro-Łazińska colony) and, in the argument, one
  colonist's holding ("14 tylko kolonjom"). The second is "holding".
- **Court Summoner** for woźny in the translation (the termbase); the
  edition's own prose says court messenger, as in the Konin holdings.
- **Hollanders** for holendrzy in the translation (the termbase); Olęders
  in the edition's prose.
- **Prusimski, Zelmer, Weigel, Zagórów** in the English; the Polish keeps
  Prusiński, Celmer, Wejgel, Zagurowie.
- "Sąd Najwyższej Instancji" is "the Court of the Highest Instance";
  "Kommissja Rządowa" is the Governing Commission of the other holdings.
- The dashes of the print are kept in the translation.

## People and places

- **Włodzimierz Miączyński** has his own person entry
  (`miaczynski-wlodzimierz`), matched only in this document; Stanisław's
  entry no longer takes "Hrabia Miączyński". He was Michalina's son
  (editor, 2026-10-14); the paper does not say so, and the page and his
  biography give it as context, not as the document's word.
- The print's "Prusiński" is matched to Paweł, Katarzyna and Antoni
  Prusimski by the forename or word beside it; "Wejgel" to Weigel;
  "Celmer" to the Zelmer family.
- The 97 colonists have no person entries. The Zelmers among them: Henryk
  (55), Anna Elżbieta, widow of Daniel, with Karolina, Krystyna, Julja,
  Krystjan and August (78), August (92), Michał (95).
- **The two colonies** (editor, 2026-10-14): two Olęder colonies were
  founded on the Trąbczyn estate, first called Trąbczyńskie Stare and Nowe
  Olędry and later Łazińskie Stare and Nowe Olędry, in several spellings.
  The print's "kolonja Staro-Łazińska" and "Nowo-Łazińska" are matched to
  the place entries `trabczynskie-stare-oledry` and
  `trabczynskie-nowe-oledry`. **Łazy is a distinct village**, not either
  colony (`lazy-trabczyn`, the grant of 1796). "Haul. Lazy." in the table
  of about 1797 (AGAD 1/169/0/1/1745, no. 150) is probably the Łazińskie
  Olędry, not the village (editor, 2026-10-14); it says neither old nor
  new and is not matched. Studzianka, the
  forest district also called Zarzyński, and Biskupice, the neighbouring
  estate, have no entries either; the existing "Biskupice" entry is a
  Silesian Bischdorf and is not matched here.

## What the paper cites and the edition has

- The resolution of the Governing Commission of 21 July 1807: AGAD
  1/174/0/1/6, document 2.
- Weigel's suit and the judgment of 1826: III. HA MdA, III. Nr. 12366,
  document 5 (which gives the dismissal at Kalisz on 6 March 1819 and the
  confirmation at Warsaw in 1826; the summons gives the day, 7 July 1826).
- Not in the edition: the contract of 18 May 1805 with fourteen colonists,
  the contract of 21 December 1828 with seven, the privilege of 1746.

## Era

**The era after Michalina Miączyńska, when her son Włodzimierz ran the
estate** (editor, 2026-10-14): era `wlodzimierz`, made that day under a
working name, "The estate under Włodzimierz Miączyński"; the editor will
name it.

## Still to do

1. **The editor's look** at the page of changes and at the five places
   above.
2. Published 2026-10-14.

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

Four pages are printed, on paper with a revenue stamp of 7½ kopecks at the head. One summons was printed for all the defendants, and the court messenger completed each copy by hand: the line in which he names himself, the name of the person served, the place and day, and his signature. On this copy he also corrected the printed list in pen. He struck out one name and wrote another in the margin, changed a letter in several names, and signed under the print beside a note of costs. The language is the legal Polish of the Kingdom of Poland, with German surnames in Polish spelling. 

The family given as Zelmer appears in the list as "Celmer": Henryk, August and Michał, and Anna Elżbieta, widow of Daniel, for her five children [[1]].

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The archive's images show the cover, the first page, and two openings of two pages each. The openings were cut at the fold, so that each of the five pages of the paper has its own image.

### Transcription

The editor supplied a transcription of the Polish by paragraph. The print's "é" is given as "e". Words that the court messenger struck out in pen are left out.

### Check against the scans

An AI model (Claude) read all five pages against the scans and corrected 34 readings. Most are single letters of the print. Four change a fact: a date of a law is 16/28 June 1830; a number of holdings is fourteen, where the transcription had eleven; a defendant is Paweł Rogacki, where it had Bogacki; and the line in which the court messenger names himself ends "residing in Kalisz". Five lines in his hand that the transcription did not have were added: his two signatures, a note of costs in two lines and the number of the service. His closing words under the note of service were added as well. Each change is logged with its reason.

The editor then read the court messenger's pen alterations on the scan, on a sheet that shows each beside a picture of it. The name he wrote in the margin for defendant 58, in place of the printed one he struck out, is Marcin Heck; he changed defendant 70 from Krystjan to Krystof Grünwald; and his note of costs is 47 roubles 21 kopecks. The other printed names he wrote over stand as printed.

### Division and dating

The paper is one document, dated by the court messenger's own line under his note of service: 7/19 October 1860, that is 19 October by the calendar now in use. The archive's cover stands before it.

### Translation

The editor's file had an English translation made by machine. It was checked against the Polish and found wrong in many places, some of them of substance: the opening "I have summoned" had become "I have acquainted myself with", Michalina Dąbska's father had become her husband, and the manor had become the court. The English was therefore written again from the corrected Polish by the AI model, keeping the editor's wording where it was right.

### Summary

The summary was written in German from the Polish and translated into English. Each of its 17 statements was then checked against the document. One was weakened: the paper names the woman served as Karolina Fridenberg and does not call her a widow; the widow is number 34 of the list, Karolina Friedenberg, who is probably the same woman.
