# Słowiński and Połom (2024): notes

*Zerwane ogniwo. Ewangelicy na ziemi zagórowskiej*, a collective work edited
by Mirosław Słowiński and Katarzyna Połom, Zagórów 2024; issued by the
Municipal Office in Zagórów (Urząd Miejski w Zagórowie), with the book
concept and introduction by Słowiński, an editorial committee under Łukasz
Parus (director of the town's House of Culture, MGOK), Dr Zbigniew Chodyła
as scientific consultant, and the German-language materials translated by a
team of seven (Jacek Kin the greater part); ISBN 978-83-969906-0-0. The
sister volume of *Przeżyć tę jedną zimę* (2023, `slowinski2023`), whose
note 4 named it as the collective volume the study of the letters was first
to appear in - that mention printed the year 2023; the title page in hand
says Zagórów 2024, and the mentions in `slowinski2023` were corrected to
2024 (2026-10-22, this session).

## How it came in (2026-10-22)

The editor's word: "Add a new literary source to the project:
C:\Users\Tersnaus\Downloads\Zerwane ogniwo. There are English/Polish .md
files which you can use." Asked, they ruled (2026-10-22):

- **summary only**: the book is under copyright (© 2024, the Municipal
  Office's publication; sold by the town's public library at 40 zł; no
  open-access copy found - the searches found the library's page, the
  zagorowzhistoria.com pages and Słupianek-Winkowska's review in *Polonia
  Maior* only), so it is kept like Seidel (2018) and Słowiński (2023): in
  the repository for questions, the site showing only the detailed summary
  (`summary_en`, `summary_de` in `work.yml`), none of the text;
  `verify_site.py` checks that.
- **no pictures**: 119 of them, the editor's word, as for Słowiński 2023
  and Mielewczyk 2017; the .md names them in lines pointing at an images
  folder beside it ("Zerwane ogniwo - images", not kept in the
  repository); their captions stay, being text.
- **the balance rule** (the editor's word with the task): "Be careful not
  to go too deep into this text: don't call out new people/estates/etc.
  unless it's something related to Trąbczyn/Zagórów areas/people - be
  balanced with this." So the summary carries the Łazińsk / Trąbczyn /
  Zagórów ground and its people in detail - the founding accounts, the
  parish's history, the kantorate schools, the Mielke letters chapter, the
  German-language sources with their lists and tables - and names the
  chapters that lie off it (the Beutlers, the Doctor's wife, Ida
  Disterheft, Mrs Dolkowa, the Brudlers, the memoirs of Hennings and
  Plitt) briefly, by their chapter, without working their people into the
  edition. No new person or estate entries were made from this book.
- **the English is the editor's own checked English .md** (the export of
  2026-10-22, the product of the earlier session's translation of the
  book, its own comments in it: "the user, 2026-10-22: write OGNIWO"),
  used at the editor's word above; `english_by: "the editor's files"` in
  `work.yml`. One repair made in the .md before the run: the export had
  broken one page mark over two lines (s. 165, in the Mielke chapter's
  letter about sister Anna's wedding); joined, the repair mechanical.
- the slug `slowinskipolom2024` (the editor's choice, asked among four).

## The text

The editor's .md files are the checked export of 2026-10-22
(docs/WORKING_NOTES.md, "Two of Słowiński's books checked against their
PDFs"): made again from the PDF's text layer with PyMuPDF, the standing
word **the checked .md is the text to start from** - and no OCR on images.
The PDF ("Zerwane ogniwo.pdf", 336 PDF pages, the editor's Downloads
folder) is the book as printed; it and the .md files are not kept in the
repository.

`original.md` (Polish) and `english.md` are made from the checked .mds by
`pipeline/literature/slowinskipolom_md.py`, the twin of
`pipeline/literature/slowinski_md.py`:

    python pipeline/literature/slowinskipolom_md.py "<Downloads>/Zerwane ogniwo/Zerwane ogniwo (Polish).docx.md" "<Downloads>/Zerwane ogniwo/Zerwane ogniwo.pdf"
    python pipeline/literature/slowinskipolom_md.py "<Downloads>/Zerwane ogniwo/Zerwane ogniwo (English).md" "<Downloads>/Zerwane ogniwo/Zerwane ogniwo.pdf" --english

then `--check` holds every PDF page's letters against the layer. What the
script does, and nothing else (its docstring says the same):

- the .md's page marks `<!-- s. N [PDF M] -->` stand on their own lines
  and also inside lines; the script splits every line at an inline mark,
  so each printed page keeps its own words. The unnumbered pages' `s. ?`
  becomes `s. unnumbered`.
- **the pictures are dropped; their captions stay.** The .md repeats a
  page's mark beside its pictures, and this book's export **brackets the
  caption block between two marks**: the running text flows past the plate
  (the marks inline, `s. 9 … s. 10 …`), then the block opens with the
  plate's own mark again and closes with the mark of the page the text had
  reached. So a mark whose page is already open is not dropped but is a
  **return**: the script switches to that page's object, and the captions
  and the text's continuation land on their own pages. (Słowiński 2023's
  script dropped such marks; that book's caption blocks carried no resume
  mark, so the dropping was right there and wrong here.) Words round a
  returned mark are an error, reported; none occurred.
- **one caption paragraph per plate stands in the print on the page the
  .md set one page later** (twenty of them, the .md's own way of setting
  the pictures); the script finds each paragraph by its letters in the
  PDF's Polish layer and moves it to the page the print prints it on.
  For the English this step is skipped: an English line cannot be looked
  for in the Polish layer, and the one hit it found was a false one (the
  imprint's "Dr Zbigniew Chodyła" matched the German Kurzfassung's credit
  on PDF 326). So the English's captions keep the export's placement - in
  those twenty spread cases a page off the print. Both texts are
  `visible: false`, so nothing of it reaches the site.
- the .md's own comments (`<!-- caption -->`, `<!-- byline -->`, the
  cover's note) are dropped, being chrome.
- **the notes go back to their pages.** The print has 97 notes at the foot
  of their pages (checked on the PDF); the .md gathered them at the very
  end, after a `---` divider, each piece under a mark repeating the page
  of its reference. The script sets each piece at the foot of that page's
  text. Ten notes (4, 6, 8, 17, 31, 33, 40, 46, 63, 69) carry no marker in
  the text (the print set the asterisk where the .md has none, or the
  export lost it) - the notes stand on their pages with their text; the
  missing markers are the .md's own state, not tidied.
- the print's slips kept: among them the list-tables' German spellings
  ("Michalinow", "Zagorow", "Lazinsk", "Kantoratsschulen"), the protocol's
  "very illegible" names, "Diesterheft"/"Disterheft" both standing in the
  print for the mayor, "Marly Las" for Mały Las in the compiled parish
  history, "Deckoffizier" for "Reproduction Officer" in the German table
  of contents' form of the forged document's title.

**The check** (`--check`): the letters of every PDF page against the
letters the file written carries for it, compared page by page as
multisets - the form WORKING_NOTES records ("the letters equal page by
page"). Left out of the print's side: the folio at the foot (in the bottom
band, about y 513 of a 566.9-point page) and the running heads at the top
(the author's name on the left pages, the section titles on the right
ones, the Kurzfassung's, the acknowledgements' and the tables of contents'
own - no real heading of this book stands above y 46). Left out of the
.md's side: the `[^n]` markers (the print's asterisks) and the export's
markup for what the print's layer does not carry as letters - the `<br>`
tags of the table cells (the chronology tables) and the circled caption
numerals ①-④ (the print's glyphs are private-use characters). The
allowances the check reports and accepts: the cover's and the half-title's
clock-face O (the title written OGNIWO, the editor's ruling of 2026-10-22;
two pages), the print's own doubled section titles on the two tables of
contents (one letter of the repeated title a private-use glyph the layer
does not carry; two pages), words the print divides over a page's end and
the spread captions the export set under one mark (reconciled with the
neighbouring page). The result: **0 PDF pages differ**, the Polish and the
English alike (the English held to the marks of the original.md, which it
mirrors in order - 364 marks).

## How it bears on the edition

The volume is the edition's fullest witness for the Protestant ground
around Zagórów and Trąbczyn - the parishes, the cantorates, the colonies,
the twentieth century - beside Chodyła (2015), Kneifel (1964) and the
sister book:

- **The founding of Łazińsk in 1718 by fourteen families from Silesia**:
  the introduction, the annex's German-era note (Der Heimatbote 8/81-3)
  and the chronology table all say it - the **third** witness to the 1942
  article's founding date, which stands against the edition's records and
  is open (NEEDS_CONFIRMATION, "The newspapers"). The note names the
  families Kuhn, Merk, Schönfisch and Haupt and dates the cemetery's
  first grave to 1727.
- **The founders of 1746**: the volume's four forms - the introduction
  and the Kurzfassung "Katarzyna i Paweł Prusińscy"; Kowalski's study
  "Paweł Prusiński i Katarzyna née Rozdrażewska" (the maiden name the
  edition's prose has not carried; it is the book's, not followed against
  the documents); the annex's contemporary note "Andrzej i Paweł" -
  against Chodyła's Prusimscy (NEEDS_CONFIRMATION, "Słowiński (2023)",
  the open item; the volume does not settle it and adds the forms).
- **The kantorate schools of the parish at the outbreak of the war**
  (Połom's list): Łazińsk - cantor and teacher Gustav Adolf Mielke from
  1925; Anielewo - cantor and teacher Bruno Mielke; Olchowo - Ferdinand
  Homt from 1924; Tarszewo - Adolf Münch; Michalinów Oleśnicki - Ludwig
  Schulz; Michalinów Trąbczyński - the farmer Paul Schulz. The visitation
  of 1877: one school in Michalinów and seven cantors' schools, 230
  pupils.
- **The cantor Gustav Adolf Mielke** - the edition's person entry
  (`mielke`, the editor's ruling of 2026-10-22 that he and the 1942
  article's and Breyer's Mielke are one man): the volume's dates for his
  works at Łazińsk differ among themselves - 1925 (the introduction, the
  letters chapter, Breyer's notebook) against "from 1932" (the school
  chronicle Połom quotes); his removal from Łazińsk 1932 (the chronicle)
  against 1936 (the introduction) against "four years from 1933" (the
  1942 article); his new school 1933 (the annex, the chronology table -
  whose "teacher Adolf Mielke" is the table's form of the name) against
  the introduction's "a hundred years later". Open,
  NEEDS_CONFIRMATION, "Słowiński (2024)".
- **The brother Bruno Edwin Mielke** - the letters' writer: born 8
  September 1911 at Białołęka, the State German Teachers' Seminary at
  Łódź 1932, teacher and cantor at Anielewo, then Maślaki (the gmina of
  Wilczyn) and Konary (the gmina of Grodziec), the Wehrmacht from 1942
  (the 2nd Gebirgs Division, the Eismeerfront at Petsamo/Pieczenga), the
  last letter 14 May 1944 in Norway. The chapter is the study of 2023 in
  its first form; the cache's contents counted (63 letters, 43 postcards,
  18 documents, the Taufe of 1912-1918 kept by the cantor E. Cellmer -
  the name near the edition's Zelmer, not identified here).
- **Eryk Stark of Łazińsk** - the Łazińsk man on the Polish side of the
  war (deported to the Reich, fled across the Alps, the Polish Army in
  Italy, Monte Cassino, Britain; the introduction's form "Erik Starcki").
  Recorded here and in the summary only; not an entry of the edition (the
  editor's balance rule).
- **The Zagórów ground**: the parish's dates (the filial of 1843, the
  independence of 1856, the church of 1878-1882, Gross 1923-1945, the
  first post-war service 18 July 1954, the branch of Konin 1968), the
  town's loss and regaining of its rights (1869, 1916), the 1936 riots,
  the "Barka" action of 1918 and the murder of the POW men near Grabina
  (22 November 1939, named), the ghetto of 1940-1941 and the murders near
  Kazimierz Biskupi - the material of the Zagórów place page's era; the
  forged document of 1943 and the Sokół excerpt of 1931 printed as
  sources.
- **The chronology table** (the Gliege family website's, translated by
  Kin): its early history (the monastery of 1145, the flight of 1553)
  stands against the edition's KDW (the grant of 1240 and the rest); its
  confiscation entry names five estates (Trombczyn, Nowa-Wieś, Oswiery,
  Łazy, Szetlewek) given to Hohenlohe-Öhringen (Ingelfingen) and half
  sold to Weigel - the book's account, beside the edition's documents,
  which are first; its 1846 entry ("Michelina Miaczynska is now the owner
  of the Trabczyn estate") is the edition's own ownership line's witness
  (the transfer the wlodzimierz era records).
- **The list of the inhabitants of Michalinów Trąbczyński, Łazińsk and
  Huta Trąbczyńska** of 1945 (compiled by Leonard Kuske of Syke) and the
  protocol of the Łazińsk cantors' council of 26 November 1928 - printed
  sources for the edition's places, kept in the book (summary only).
- **The German place names** - the table from the Gliege website and
  Breyer's study of 1938: Trabczyn = Drommin, Zagorow = Hinterberg and
  the rest; the same Breyer the edition carries (breyer1938).

**The index**: the work is `visible: false`, so the passage index does not
run over it and nothing of it reaches the search or the "In the
literature" lists (LITERATURE_PLAN, sections 4 and 8; the Słowiński 2023
precedent). No person or place rulings were made from this book.

**Hand-made links** (`literature/links.yml`): none written - the work's
text is on the site in summary only, so a link's passage box could not be
shown (the Słowiński 2023 precedent). The candidates, if the editor ever
wants them recorded differently: the letters chapter against
`slowinski2023`, the 1942 item and Breyer's notebook; the settlement
study against Chodyła (2015) and Wąsicki (1953); the parish material
against the Zagórów place page and ADWł 85.

## Open

- Committed (2026-10-22); not pushed, not published. The merge to the
  live site waits on the editor's word (the standing rule).
- The founding date of 1718 (NEEDS_CONFIRMATION, "The newspapers"): the
  volume is a third witness; the editor's ruling still wanted.
- The founders of 1746 (NEEDS_CONFIRMATION, "Słowiński (2023)"): the
  volume adds the Rozdrażewska form.
- The Mielke dates (NEEDS_CONFIRMATION, "Słowiński (2024)", new): 1925
  against 1932 for the works' start; 1932 against 1936 against "four
  years from 1933" for the removal; 1933 against "a hundred years later"
  for the new school.
- The slowinski2023 work's English on file is the editor's own English
  .md (from their Downloads folder, processed by this session's script),
  not the Claude translation the work's notes had planned: the folder had
  no english.md and the build needs one; recorded here and in that work's
  notes, the editor's look wanted (NEEDS_CONFIRMATION, "Słowiński
  (2023)").
- The editor's look at the summary, when they want it.
- The passage builder's one warning for this work, "lengths differ much:
  139": on printed page 139 the English runs 1371 characters against the
  Polish 2319 - the editor's English breaks the page mid-paragraph at a
  different point, so the paragraph the Polish page ends with ("Wśród
  książek są oczywiście...") opens the English page 140; nothing lost, the
  same class of difference the other bilingual works report.
- `translation_chunks/` at the project root - the earlier session's
  working files of the English translation of this book (30 files) - left
  untracked, not needed now that the assembled English .md stands in the
  editor's Downloads folder.
