# Słowiński (2023): notes

Mirosław Słowiński, *Przeżyć tę jedną zimę. Listy żołnierza Wehrmachtu
odkryte w ścianie domu kantora*, Konin 2023; Wydawnictwo Setidava Miejskiej
Biblioteki Publicznej im. Zofii Urbanowskiej w Koninie, ze Stowarzyszeniem
Współpraca Polska-Wschód; ISBN 978-83-67258-15-9, ISBN 978-83-63554-53-8.
The author is the editor of *Zagórów. Album miasta* (2007), of *Dwa życia jak
dwa psalmy* (2012, with Krzysztof Makowski) and of *Zerwane ogniwo.
Ewangelicy na ziemi zagórowskiej* (2024, with Katarzyna Połom), which its own
note 4 names as the collective volume the study of the letters was first to
appear in; the manuscript was read by Professor Artur Kijas at the author's
request (his conclusion quoted on pp. 14-15).

## How it came in (2026-10-22)

The editor's word: "Add a new literary source to the project:
C:\Users\Tersnaus\Downloads\Przeżyć tę jedną zimę. There are English/Polish
.md files which you can use." Asked, they ruled (2026-10-22):

- **summary only**: the book is under copyright (© 2023 Mirosław Słowiński /
  Wydawnictwo Setidava, a living author; no open licence; the library sells
  it, no open-access copy found - the searches found the library's page, the
  SWPW's pages and Sierpowski's review in *Kronika Wielkopolski* only), so it
  is kept like Seidel (2018), Frost (2007) and Pinkas Hakehillot (1976): in
  the repository for questions, the site showing only the detailed summary
  (`summary_en`, `summary_de` in `work.yml`), none of the text;
  `verify_site.py` checks that.
- **the English is Claude's**, written page by page from the Polish. The
  editor's English .md is read as a witness and not used (the standing rule
  that an English in the editor's files is a machine's unless they say
  otherwise; the Books_2 precedent).
- **the pictures are skipped** (26 of them, the editor's word, as for
  Mielewczyk 2017): the .md names them in lines pointing at an images folder
  that was not supplied; they are in the PDF, which is not kept in the
  repository. Their captions stay, being text.
- **the Mielkes are ruled in**: the cantor Gustav (Adolf) Mielke of Łazińsk,
  in whose house the letters were found, and the teacher and farmer Mielke of
  the Ostdeutscher Beobachter's feature of 19 July 1942 and of Breyer's
  Łazińsk notebook of 1936 (APP 53/968/0/-/669) are one man - the editor's
  ruling of 2026-10-22, which the book's own facts support: it gives the
  full name Gustav Adolf Mielke and says his works at Łazińsk ran from 1925,
  which is what Breyer's notebook records ("Mielke seit 1925"). He is added
  to `reference/people.yml` (the Głowiecki shape: an entry, no person page),
  and his two mentions in the 1942 item are ruled true in
  `newspapers/index.yml`; his three mentions in Breyer's notebook follow from
  the entry at the build. The book itself, being `visible: false`, is not
  searched by the index (LITERATURE_PLAN, sections 4 and 8); its hits would
  have been ruled like the others had it been shown.

## The text

The editor's .md files are the checked export of 2026-10-22
(docs/WORKING_NOTES.md, "Two of Słowiński's books checked against their
PDFs"): made again from the PDF's text layer with PyMuPDF, the editor's first
export (with its damage: line-break hyphens, drop caps, runaway italics,
pictures as base64) kept only as a witness and no longer in the Downloads
folder. The standing word: **the checked .md is the text to start from** -
and no OCR on images.

`original.md` is made from the checked Polish .md by
`pipeline/literature/slowinski_md.py`:

    python pipeline/literature/slowinski_md.py "<Downloads>/Przeżyć tę jedną zimę/Przeżyć tę jedną zimę (Polish).md" "<Downloads>/Przeżyć tę jedną zimę/Przeżyć tę jedną zimę.pdf" [--report] [--check]

What the script does, and nothing else (its docstring says the same):

- the .md's page marks `<!-- s. N [PDF M] -->` (N the printed page, M the
  PDF page) stand on their own lines and also inside lines, where the text
  runs over a page's end mid-sentence; the script splits every line at an
  inline mark, so each printed page keeps its own words. The unnumbered
  pages' `s. ?` becomes `s. unnumbered`, the form the passage builder knows.
- the picture lines (`![...`) are dropped; the placement marks the export
  repeated beside them (page marks never run backwards in a book, so a mark
  whose printed page is not greater than the page now open is a placement
  mark) are dropped with them: 26 pictures, 34 placement marks.
- the .md's own comments (`<!-- caption -->`, two of them) are dropped,
  being chrome.
- **the notes go back to their pages.** The print has its 32 notes at the
  foot of their pages (checked on the PDF); the .md gathered them at the very
  end, after a `---` divider, each piece under a mark repeating the page of
  its reference. The script sets each piece at the foot of that page's text,
  as the print does. A note that runs over a page's foot keeps the split
  (note 2, on pp. 10 and 11).
- **one caption is set back to its printed page.** The caption "Znak
  taktyczny 2. Gebirgs-Division." the .md set in the flow of p. 35 (beside
  the pictures of the spread); the print has it at the foot of p. 34. The
  script finds each paragraph of at least twelve letters in the PDF's own
  text and moves any that the print prints on another page than the .md gave
  it; this one is the only one.
- **one PDF page carries two printed pages**: PDF 12 holds the whole of
  printed pp. 15 and 16, and the .md marks it once, as s. 15; so the passage
  keyed 15 carries both pages' text (the mark's PDF number is kept in
  `original.md`'s marks for exactly such cases). The printed numbers
  otherwise run 7 to 101 with photo pages unmarked (14, 17, 37, 41, 53, 59,
  67, 73, 75 are among the picture pages).
- `--check` holds the letters of every PDF page (the folio block the layer
  carries at the foot left out; the .md's `[^n]` marks, which stand for the
  print's asterisks and other symbols, left out) against the letters the
  original.md carries for it. Every difference is accounted for: **six words
  the print divides over a page's end are given whole on the first page**,
  as the .md sets them - "wszy|scy" (pp. 10/11), "pra|wa" (12/13),
  "niemieck|ą" (20/21, the word's tail before the footnote, an order the
  check records), "niewy|mownym" (79/80), "naroduniemieckie|go" (81/82),
  "Z koń|cem" (90/91) - and the imprint page's block order: the layer's
  stream sets "Druk i oprawa perfekt Poznań" before the Stowarzyszenie
  block, the .md reads the page as the print shows it (the block last,
  under the publishers'); the letters are the same and stand on the same
  page. The check ends: 0 PDF pages differ.
- Nothing tidied (`docs/EDITORIAL_RULES.md`). What the .md carries stands:
  the print's slips kept, among them "Prusińscy" for the family the edition
  writes Prusimscy, "Aubruch" for Aufbruch, "Einfürung" for Einführung,
  "Weinnachts glanz", "Das Freüdige Herz", "Das Liebes und Geschletsleben
  des Menschen", "wirtschften", the Taufe book's kantorem "E. Cellmer", the
  annex's "Rhytthammer", the letter of thanks' "MGOK" (the archive the book
  names so), the last page's own rendering of the address "Łazińsk, poczta
  Dromin (Trabczyn) przez Konin Wartheland (Niemcy)" - the print's own
  forms, left as they stand.

## The English

**Recorded 2026-10-22, the second session**: the English on file is the
**editor's own checked English .md** (from their Downloads folder, the
sister volume's export of the same day), processed into `english.md` by
`slowinski_md.py --english` - not the Claude translation this section had
planned, because the folder had no `english.md` and the build needs one.
The editor's word for the sister volume ("There are English/Polish .md
files which you can use") is the standing word for the pair; the change is
flagged (NEEDS_CONFIRMATION, "Słowiński (2023)"), and `english_by` in
`work.yml` says "the editor's files". The original.md (below) and the
marks of the English match: the English's 96 marks are the original's, in
order.

The plan of the first session, **not carried out**: Claude's English, page
by page from `original.md`, with the same pages,
paragraphs and notes. The headings are translated; the epigraphs are
translated; the German titles of the books quoted stand as printed, with
bracketed English renderings where the Polish gives one (the book's own
convention was German title with bracketed Polish rendering). The forged
"Reichsstelle für Familienzuwachs" document of pp. 74-76 stands as a
blockquote, translated; its signature "Hüpfauf" stands. The biblical
quotations are given in the wording of the Polish text's Warsaw Bible
rendering, Englished.

- Terms: *prawo olęderskie* Olęder law, *olędrzy* the Olęders, *kantor* the
  cantor, *kantorówka* the cantor's house, *kantorat* the kantorat, *Kraj
  Warty* the Warta Country (the Reichsgau Wartheland), *Eismeerfront* the
  Eismeerfront, *Volksliste* the Volksliste, *Volksdeutsche / Reichsdeutsche*
  kept, *folwark* the folwark, *sołtys* the village headman, *Urwłaszczenie*
  enfranchisement (not used: the book reaches only the twentieth century).
- The soldiers' ranks, units and post numbers follow the book: Oberschütze
  (the book's "starszy szeregowiec", 1 December 1942), corporal
  (Obergefreiter, 20 April 1944), the 2nd Gebirgs Division, the 136th
  Gebirgsjäger Regiment (field post 31 059), the 67th Medical Company (field
  post 48 341), the field post 39 801 (note 11: the Feld-/Ortskommandantur
  578).

## How it bears on the edition

The book is the edition's fullest witness for Łazińsk in the twentieth
century, beside the Ostdeutscher Beobachter's feature of 19 July 1942 and
Breyer's notebook of July 1936 (APP 53/968/0/-/669):

- **The kantorem Gustav Adolf Mielke** (the book's full name for him),
  cantor, teacher and schoolmaster of Łazińsk "since 1925" - Breyer's
  notebook's own words - the builder of the new German school, the man made
  to leave Łazińsk (the book: 1936; the 1942 article: four years from 1933),
  back with the Wehrmacht in 1939 and teaching again from 1940, later called
  to the navy (the artilleryman of the naval infantry at Hamburg of the
  letter of 12 December 1944). **The editor ruled (2026-10-22) that he and
  the article's and Breyer's Mielke are one man**; he is now a person of the
  edition (`reference/people.yml`, `mielke`).
- **The founding of Łazińsk in 1718 by fourteen families from Silesia**,
  leased their forest land by the lord of Trąbczyn: the book's introduction
  and its annex's German-era note (Der Heimatbote 8/81-3) both say it - the
  second witness to the 1942 article's founding date, which stands against
  the edition's records and is open (NEEDS_CONFIRMATION, "The newspapers").
  The note names the families Kuhn, Merk, Schönfisch and Haupt, and dates
  the cemetery's first grave to 1727.
- **The founders of 1746.** The introduction: "the owners of the estates in
  Trąbczyn, Katarzyna and Paweł Prusińscy, mark out places for further
  settlements" - the edition's Paweł and Katarzyna **Prusimscy** (Chodyła
  2015, the register's family), in the book's own spelling of the name; the
  annex's contemporary note, from Wikipedia, gives Łazińsk Pierwszy's
  founders as "Andrzej i Paweł Prusińscy" - a third form. The book does not
  settle them and is not followed against the documents
  (NEEDS_CONFIRMATION, "Słowiński (2023)").
- **The new school's date.** The introduction: the first brick building of
  1839 and "a hundred years later" the new one; the 1942 article and the
  annex's German-era note both say the new school rose from 1933, built by
  Mielke's own means. The difference is the book's; the edition records it
  and takes the article and the note (NEEDS_CONFIRMATION, "Słowiński
  (2023)").
- The field post address of the letter of December 1942 gives the print's
  own form "Łazińsk, poczta Dromin (Trabczyn) przez Konin Wartheland
  (Niemcy)" - Drommin/Trabczyn, the occupation's names the 1942 item's
  rulings already record.
- The baptism book (Taufe) of the kantorat of Łazińsk, 1912-1918, kept by
  the cantor E. Cellmer - the name near the Zelmer of the liquidation
  tables (the editor: Zelmer is always Цельмеръ); not identified here,
  recorded as the book gives it.

**The index**: the work is `visible: false`, so the passage index does not
run over it and nothing of it reaches the search or the "In the literature"
lists. The person entry of Mielke was ruled in by the editor before the work
was built; no other person or place of the edition is called out from this
book (the editor's word: do not call out new people or estates unless they
are of the Trąbczyn/Zagórów ground - the names of the letters' people, the
soldiers, the reviewers, stay out, recorded here and in the summary only).

**Hand-made links** (`literature/links.yml`): none written. The candidates,
the letters' discovery in the cantor's house against the 1942 item and
Breyer's notebook, and the introduction's founding account against Chodyła
(2015), wait on the editor's word; the work's text is on the site in summary
only, so a link's passage box could not be shown anyway.

## Open

- **Committed on `main` (2026-10-22, the second session)**; not pushed, not
  published. The merge to the live site waits on the editor's word (the
  standing rule). (The first session's notes said "committed"; the folder
  was in fact untracked until the second session committed it with the
  sister volume.)
- The founding date of 1718 (NEEDS_CONFIRMATION, "The newspapers"): the book
  is a second witness; the editor's ruling on it is still wanted.
- The founders of 1746 and the new school's date (NEEDS_CONFIRMATION,
  "Słowiński (2023)").
- The English on file is the editor's own English .md, not the planned
  Claude translation (NEEDS_CONFIRMATION, "Słowiński (2023)"): the
  editor's look wanted.
- The sister volume, *Zerwane ogniwo* (2024), is in the literature
  (`slowinskipolom2024`, the same day); its summary carries the volume's
  own account of the letters' cache, and the year mentions here were
  corrected to 2024 (the title page's year, against the 2023 the notes
  printed).
