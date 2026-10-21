# Chodyła (2015): notes

Zbigniew Chodyła, *Zarys najstarszych dziejów osad olęderskich w Puszczy
Pyzdrskiej 1746 – 1793* (Pyzdry: Lokalna Organizacja Turystyczna „Puszcza
Pyzdrska”, 2015, 1st edition, 156 pages; ISBN 978-83-943651-0-3), with two
forewords: "Bliskie nieznane" by the president of the Local Tourist
Organisation, Przemysław Kowalski (named in the table of contents; the
foreword is signed only with his office), and a greeting by Krzysztof Nosal,
Starost of the District of Kalisz. The author's own text is the Introduction,
six chapters, the Conclusion, a glossary of Old Polish terms and a list of 25
illustrations, with 369 notes numbered through the book.

## How it came in (2026-10-21)

The editor: "Add a new literary source from the Downloads folder - Zbigniew
Chodyła - Zarys najstarszych dziejów osad olederskich w Puszczy Pyzdrskiej
1746 – 1793.docx.md. There's an English translation made by machine at
(English) Zbigniew Chodyła - Outline of the oldest history of the Oleder
settlements in the Pyzdry Forest 1746 - 1793.docx.md."

- The editor's Polish file is a Word conversion of the book: it has no page
  numbers, the note numbers are run into the words ("przywilejami1"), the
  notes are gathered at the end, the tables are broken Markdown, and the
  conversion made slips of its own ("Zwielką", "wyaźną", "Dzierzbińkie",
  "wspomniae", "olęderskieo", divided words left with a space).
- The editor's Books folder holds the book itself as a PDF: "Zarys
  najstarszych dziejów osad olederskich w Puszczy Pyzdrskiej 1746 – 1793
  (Chodyła, 2015).pdf", printed from InDesign, with a clean text layer, the
  printed page numbers, the notes at the foot of each page and the
  illustrations. `original.md` is made from it by
  `pipeline/literature/chodyla_pdf.py` (its docstring lists every rule), so
  that every passage can be cited by its printed page and the pictures shown:

      python pipeline/literature/chodyla_pdf.py "<Books>/Zarys najstarszych dziejów osad olederskich w Puszczy Pyzdrskiej 1746 – 1793 (Chodyła, 2015).pdf" [--figures] [--report]

- **Checked against the editor's file word by word** (difflib over the words
  of the body and of the notes): the words are the same but for what the
  Word file lost or broke (the note numbers, the pages, the table of
  contents, the picture labels, words divided at the line's end, its own
  slips listed above) and the order of the table cells. Nothing of the
  book's text is missing from `original.md`.
- Left out: page 2 (a decoration), page 4 (the table of contents, as the
  editor ruled for Pachoński's book), the page number at each page's foot,
  and the words inside the sponsors' logos on p. 155 (the publisher's appeal
  and the author's note there are kept). The title page (p. 1) and p. 3
  ("Pyzdry 2015") are the front.
- **Pictures** (`figures` in `work.yml`, `site/assets/literature/chodyla2015/`,
  rendered at 1100 pixels by `chodyla_pdf.py --figures`): the three maps
  (pp. 22-27, each over two pages), the founding charters and other
  documents (illustrations 4 and 6-23, 25) and the portraits (5, 15, 18, 24):
  39 pages. Their captions are text too. The signatures on pp. 7-8 and the
  logos are not shown.

## The text

Never tidied (`docs/EDITORIAL_RULES.md`). What the script does is in its
docstring; among the things found in making it:

- **Two note marks are printed in the text's own type, not raised**: note
  25 (p. 18, "z 1789 r. 25 tabele") and note 366 (p. 147, "mieszkańców
  366."). They are set by hand (`FLAT_MARKS`). Every other mark was found in
  the order of the notes, 1 to 369; a raised figure out of that order is a
  square ("km²", "m²") and stays so.
- **A few letters are set at 0.1 point and do not show in print**: "für",
  "Perthées", "Mitwürking" (pp. 17-21), "Büsching", "Örter", "für" (p. 45,
  where the print reads "Bsching", "...rter", "fr"), "Südpreussen" (p. 82),
  "Blätter" (p. 121). The text layer holds them; they are kept, being the
  words' letters. A stray invisible " ű" after a printed "fü" (p. 17) is left
  out.
- **The print's slips are kept**, among them: "emfiteutycznowieczystym"
  (p. 39), "26 tycznia 1774" (p. 39), "1 V 776" (n. 77), "6 1787" without a
  month (captions 22), "Jan Wężyk" in captions 7 for Józef, "Jarantowkich"
  (p. 134), "Pyzdrksiej" (p. 148), "6776" for 677 (p. 143), "Chłocy" for
  Chłopcy and "Kobie-ty" (Tab. 3c), "d0" (Tab. 2), row 6 of Tab. 1 without
  its number, note 130 breaking off at "DuninWąsowicz, Stam", note 76 ending
  with a comma, and the misplaced words "Dzierzbin i majętności
  sul[i]szewskiej" (p. 59).
- **Tables** (Tab. 1, pp. 12-15; Tab. 2, pp. 89-91; Tab. 3a-c, pp. 97-103)
  are read cell by cell and written as HTML, each page's part under its
  page. Pages 13, 89, 90 and 97 were compared with their pictures, and the
  cells of the others read through: the merged cells, the sideways headers,
  the wide row numbers ("10.-11.") and two figures printed in one span
  ("1 177") came out right once the script had rules for them.
- Pages 22, 24 and 26 hold only the left half of a map and have no text.

## The English

Claude's (2026-10-21), page by page from `original.md`, with the same
pages, paragraphs and notes; the tables are put in by `make_english.py`
(their headers and remarks in English, names and figures as printed).
Bibliographical notes keep the Polish titles, with an English rendering in
square brackets. Quotations from the documents are given in English, the
Polish beside them where the book's wording matters (the 1754 inspection in
note 35).

**The editor's machine English was read against the Polish and not used**
(the rule of 2026-10-19: unless the editor says otherwise, an English in
their files is a machine's). On the Trąbczyn passage of p. 28 alone it gives
*wolnizna* as "leisure time" (free years), *wizja* as "vision" (inspection),
*tradowana* as "traded" (handed over by the court), *niegrodowe starostwo* as
"non-garden starosty" (non-castle), and *dziedzic* as "heir" where the word
means the owner.

Terms: *olędrzy* Olęders, *osada olęderska* Olęder settlement, the names of
the settlements kept in Polish ("Trąbczyńskie Stare Ol."); *przywilej
lokacyjny* foundation charter; *emfiteutyczno-wieczysty* emphyteutic-perpetual;
*wolnizna* free years; *okupne* (*grundgeld*, *gruntgielt*) entry money;
*czynsz* rent; *sołtys* sołtys (village mayor), *ławnik* assessor; *wilkierz*
village ordinance; *dym* hearth; *dymy samorolne* self-tilling hearths;
*podymne* hearth tax; *zsypka* grain levy; *wizja* inspection; *lustracja*
survey; *księgi grodzkie* castle-court books; *oblata* entry (*oblata*);
*huba*, *włóka*, *łan*, *mórg* (morgen), *pręt* rod, *łokieć* ell; *folwark*
demesne farm; *komornicy* lodgers; *czeladź* farm servants; *luźni* landless
people; *dysydenci* dissenters; *powiat* district; *starosta* starost. The
glossary's English headwords (`reference/glossary.yml`) were followed.

## How it bears on the edition

The book is about the edition's ground: the Olęder colonies of the Trąbczyn
estate are its oldest settlements, and it cites, folio by folio, records the
edition holds.

- **The founding of 1746** (pp. 28-31, notes 34-36; ill. 4, the decree's
  folios 681 and 692): the Trąbczyńskie Stare Olędry and the Luśnie Olędry,
  founded by Paweł and Katarzyna Prusimski by a charter that does not
  survive, known from the boundary decree recorded in 1776 (the edition's
  **APP 53/17/0/-/Konin Gr.145**). The book calls it "the decree of 1776";
  the commission sat from 13 September 1775 and the decree was entered at
  Brześć Kujawski on 23 September 1776 (the book's own note 150): no
  contradiction.
- **The inspection of 1754** (note 35, p. 84): the edition's **Konin
  Gr.136**. The quotation agrees with the edition's transcription ("Olędrów
  15 szesnasta huba próżna") except one word: the book prints "drugi (!)",
  the edition reads "drudzy". The edition keeps its reading.
- **The handing over of 1771** (note 36): "Konin Gr. 142 ... the same in
  Kalisz Gr. 414": the edition's **Kalisz Gr.414** has the act, with the
  Olęders "ufundowane niezbyt dawnym czasem" in the wood Luśnie and twelve
  names with the shepherd, as the book says.
- **The decree of 1782** (note 34): the edition's **Konin Gr.153**. The book
  says the commission sat "on 17 X 1782 in the house of the Olęder Marcin
  Hunt"; in the edition 17 October 1782 is the date of the Crown Tribunal's
  decree, and the commission sat in Hunt's house from 28 November 1782.
  Flagged in `docs/NEEDS_CONFIRMATION.md`.
- **The summons of 1860** (note 34): the edition's **APP 53/968/0/-/783**,
  served on Karolina Fridenberg of the Staro-Łazińska colony on 7/19 October
  1860, as the book says. **The book names the owner "hr. Władysław
  Miączyński"; the summons names Count Włodzimierz Miączyński.** The edition
  keeps to the document; flagged in NEEDS_CONFIRMATION. (Władysław was the
  heir after 1879, the editor, 2026-10-15.)
- Also cited and in the edition: the inspections of 1767 (Konin Gr.114,
  note 37), Konin Gr.115 (notes 36, 53), the Pyzdry Olędry's charter entered
  in Konin Gr.118 (note 91), the protest of 1787 (Konin Gr.121, note 87), the
  hearth-tax table of 1789 (Kalisz Tab.21, notes 44, 154: "Olędry
  Trąbczyńskie" 10 and "Nowa Wieś" 13 hearths), the Prussian register of
  1796 (AGAD General Directorium Südpreussen 1745, the edition's AGAD
  1/169/0/1/1745: "Trąbczyn H." 34, "Stara Huta Trąbczyn" 2, "Łazy H." 5),
  and the visitation of the deanery of Konin of 1790-1791 (ADWł Wiz. 85).
  Read against the documents for the links (below): the register's
  figures agree, but the book dates it 1796 where the archive dates the
  volume 1797; and the hearth-tax register gives sums of money (Łazy and
  Nowa Wieś 12 zł 15 gr each, the Olędry 35 zł), from which the book's
  hearths (3, 13 and 10) do not follow at any one rate.
- **The wood Lusina** (p. 28): the book gives the inspection of 1754 twelve
  Olęders and an inn in the wood Lusina; the inspection counts fifteen
  under Nowa Wieś and names no Lusina, twelve or inn. Those are in the act
  of 1771.
- **Łazy** (p. 32): an existing village of the estate moved to Olęder law
  after 1754, Catholics, 48 persons in 1791. Tab. 1 gives the modern names:
  the Trąbczyńskie Luźne Nowe Ol. are Łazińsk Drugi, the Stare Ol. Łazińsk
  Pierwszy and Drugi. Note 105: the charter of the Oborskie Olędry (1783)
  was modelled on those of the Łukomskie or Trąbczyńskie Olędry.
- The later colonies of the estate (p. 146: Święcia, Olchowo, "Emilienheim
  czyli Oleśnica", Michalinów, Drzewce, Kopojno) and the chapels and prayer
  houses at Łazińsk Pierwszy and Michalinów Trąbczyński (p. 138). "Nowa
  Wieś" in this book is the Trąbczyn estate's ("Trąbczyna Małego albo Nowej
  Wsi", p. 28; the inspection of 1754).
- The book uses the literature already in the edition: Breyer (its "Breyer
  2", "3", "4" are `breyer1935gaue`, `breyer1938`, `breyer1935mutterland`),
  Wąsicki (1953) and Szwiec (2009).

**The index** (`literature/index.yml`): every hit read and ruled. The Polish
case forms of the Prusimskis ("Antoniemu Prusimskiemu", "Pawła i Katarzynę z
Rozdrażewskich Prusimskich", "Katarzyny Prusimskiej") are added under
`patterns:` for the literature only. "Poniatowskiego" here is King Stanisław
August, not the Prince Józef of the edition, and is ruled so; "Przespolewski"
is the family only where the lessees of Zbiersk are meant; "Oppeln" is part
of a man's name. The colonies are indexed under Trąbczyn; the edition's
entries for the colonies themselves have no pattern and are not used here.

**Hand-made links** (`literature/links.yml`, `chodyla2015-*`, at the
editor's word, 2026-10-21), every figure, name and date read on both sides:
the founding of 1746 (Konin Gr.145, the summons of 1860), the inspection of
1754 (Gr.136), the handing over of 1771 (Kalisz Gr.414), Hunt in 1782
(Gr.153, both documents), the register of 1797 (AGAD 1/169/0/1/1745) and
the hearth tax of 1789 (Kalisz Tab.21). Where the book and the document
differ, the sentence says so and that the edition follows the document (the
editor's rule of 2026-10-21).

## Open

- Published at the editor's word, 2026-10-21.
- Copyright: the book (2015) is in copyright; the Licences page says the
  modern works on the Literature page are outside CC BY. No statement in the
  imprint forbids copying (unlike Seidel's).
- The differences above are in NEEDS_CONFIRMATION, settled by the rule of
  2026-10-21: the documents are taken.
