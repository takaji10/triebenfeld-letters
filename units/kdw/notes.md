# BK PAN Kodeks Dyplomatyczny Wielkopolski

**Built, translated and claim-checked (2026-10-16); not published.** Twenty-one
entries, 1173 to 1440, each one document, in the era `medieval` (working name
"Trąbczyn in the Middle Ages"). Nothing waits on the editor but the word to
publish and the era's name.

## What the editor decided (2026-10-16)

- **One holding** for every entry the edition uses, whatever its volume;
  **each entry is its own document**, numbered by date (the order the
  editor gave is not important). Volumes used: 1, 2, 3, 5, 6, 7, 10, 11.
  **Volume 8 is not used** and is left out.
- **Text only.** The WBC has the Kodeks only as a proofed electronic text,
  one HTML file a volume, with no page images and no printed page numbers.
  Each document's page shows its text, its citation (volume, number) linked
  to the volume in the WBC, and "From the electronic text of a printed
  edition: there is no page image."
- **The whole entry is the transcription**, from the editor's file
  `intake/kodeks.txt`, copied verbatim: "Don't try to amend any of the
  transcription, since it should be taken as secure." Nothing in it is
  corrected, not even the editors' evident slips.
- **Footnotes styled as footnotes** on the site (the editor: in the file
  they "look like letters").
- **Estates of focus: the editor's sixteen only**: Zagórów, Skokum,
  Kopojno, Ląd, Szetlew, Szetlewek, Łukom, Trąbczyn, Wrąbczyn, Wrąbczynek,
  Świątniki, Oleśnica, Łazy, Adamierz, Drzewce, Przybysław.
- **People only where they are of Trąbczyn** ("No need to identify people
  in here ... unless they are people associated with Trąbczyn").
- **A new era**, working name `medieval`, first in order.
- **Medieval spellings of each place, with their years**, beside the
  German forms on the Places page ("1252: Trupcino").
- Łęd is Ląd (editor, from the Kuryer Polski holding).

## The sources

`intake/kdw_source.py` has the eight volumes (VOLUMES: WBC id, year) and
reads any entry by volume and number from the saved HTML. The volumes'
texts are in the editor's references folder, `Kodeks Dyplomatyczny
Wielkopolski/KDW_T<vv>_wbc<id>.html`, downloaded 2026-10-16 from
`https://www.wbc.poznan.pl/Content/<id>/download/`. The WBC answers a burst
of requests with a 1.7 KB "High Load" page: fetch one volume at a time and
check the size. Numbers restart in volume 5 and in volume 6, so an entry is
always named by volume and number. In volumes 6 to 11 "[s. 443]" in a text
is the page of the manuscript the editors printed from.

## How the holding is made

`intake/holding.py` (its docstring says it all): ENTRIES lists each
document with volume, number, date, place, type, estates and why;
`--write` writes the page files, corpus and the generated blocks of
`rulings.yml`; `--english --cache` and `--summaries` take the English and
summaries from `intake/english_kdw.py` (which joins `english_kdw_a/_b/_c.py`,
one string per document, and holds S and HOW). Then `check_translations.py
--unit kdw` and `publish_translations.py --unit kdw`.

- **Footnotes**: `footnotes.yml` (marks and notes per document);
  `intake/check_footnotes.py` checks them: 98 marks, 97 notes, two
  unmatched and recorded (document 16 note 1, run into note c's line in
  the file; document 20 note c, no mark in the text).
- **Years in figures**: `numerals.YEARS_FROM` has `kdw: 1100`, so the
  reading text and the English leave years such as 1411 without a comma.
- **The claim check**: `intake/claim_check.yml`, 107 statements, all
  supported after documents 4 and 6 were corrected (Kopojno is only a
  boundary in 4; Świątniki is the editors' identification).
- **The translation check** raised 36 rows, all read and none real:
  superscript note numbers from 10 up, German glossary terms caught in
  Latin, and Zagorowo kept as the Latin has it.

## Rulings taken

- **Estates.** Document 3 (the hospital of Gniezno, 1243) names none of the
  sixteen and is untagged. Łazy and Szetlewek occur in no entry.
  Przybysław occurs only as a man (the servant of the church of Zagórów,
  document 16) and is not tagged. In document 2 "Szetlevo" is Szetlew, not
  Szetlewek (`szetlewek not_in`).
- **Document 18 (1418)**: the editors' note puts Wronczyn in the district of
  Poznań and cannot say which Drzewce; the text sets Great Wrąbczyn beside
  Zagórów, so it is tagged Wrąbczyn and Drzewce. The note stays as printed;
  summary and holding page say so.
- **Document 12 (1384)**: "Vronczino", Wrąbczyn or Wrąbczynek in the
  editors' view: tagged both.
- **Places' patterns**: Wrąbczyn and Wrąbczynek exclude each other's case
  endings; Łukomia, Brzeg, Przybysław and Szetlewek are shut out of the
  entries where their patterns hit something else.
- **People**: 13 entries, each only in its document (people.yml
  `only_in`): Janko son of Szymon, the priest Mikołaj, Count Mikołaj the
  treasurer (5); Jan and Przedpełk (9); Andrzej (10); Jan the parish
  priest (13); Mikołaj and Andrzej of Trąbczyn (17); Otto, Mścichna,
  Wojciech, Jan and Tomasz Ocic (19). "Otto" as a long-tail name is shut
  out of document 19 (`seed_not_in`).
- **Dates**: the editors' headings. Document 17's copy has 1414, document
  19's 1435; the editors' 1415 and 1434 are taken, as their notes explain.
- **The "@" marks** in document 6 ("@M CC L XXX@") are in the editor's
  text and are kept in the English ("@1280@").

## Open

- The name of the era (working name `medieval`).
- Volumes 6 to 11 were published 1982 to 1999, and the WBC names the
  Kórnik Library as rights holder; the edition reproduces whole entries.
  Before the site is shared widely (NEEDS_CONFIRMATION).
