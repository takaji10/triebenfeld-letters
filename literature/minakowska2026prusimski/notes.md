# Minakowska (2026): the page of Antoni Prusimski in Wielka genealogia Minakowskiej

The page of Antoni Michał Kazimierz Ostroróg-Prusimski z Kolna h. Nałęcz,
person 4.285.619 of M. J. Minakowska's online database
(https://www.sejm-wielki.pl/b/4.285.619), its own citation line "Maria Jadwiga
Minakowska, Wielka genealogia Minakowskiej (Wielcy.pl), wydanie z
22.10.2026". Added 2026-10-22 at the editor's word, as a source for his
descendants and ancestors, the first of the database's pages the editor means
to send.

## The source

The editor's saved page, in their Downloads folder: "Antoni Michał Kazimierz
Ostroróg-Prusimski z Kolna h. Nałęcz (M.J. Minakowska, Genealogia potomków
Sejmu Wielkiego).htm". The page is **not** kept in the repository: its header
carries the editor's login and its footer the visitor's IP address.
`make_original.py` makes `original.md` and `full.md` from it and says what it
does.

The page is written in **ISO-8859-2 (latin2)**, not Windows-1250 as its
headers do not say: the first reading took it for cp1250 and turned Łoś into
"Ło¶", Dąmbska into "D±mbska". A future page of the database is read with
`encoding='iso8859-2'` unless it says otherwise.

## The standing rule (the editor, 2026-10-22)

A saved page of the database becomes one excerpt work, slug
`minakowska2026<name>`, cited "Minakowska (2026, *name*)", the person ID and
the page's edition date in `published:`. The page is never kept. Its whole
text, the sections not brought in included, is written to `full.md` in the
work's folder: the knowledgebase (docs/LITERATURE_PLAN.md, section 22),
tracked and searchable, never shown on the site. Only the sections the editor
names go into `original.md`, and those are shown on the site in full detail;
here that is the biography, the parents, the ancestor tree, and the marriage
with the children and grandchildren. The database's estimated dates (its
"?1710-" tokens) are never taken into the edition's prose, whatever person
they concern; a date enters the edition's prose only where a source the
edition can cite anchors it. The page's subject has a page of his own on the
site (see `reference/genealogy.yml`), where his family, his document mentions
and the literature are brought together; a future page of the database makes
one for its subject the same way.

## What the page holds, and what was done with it

The page's sections, in its order: the biographical line; **Rodzice**
(parents); the ancestor tree (16, 32 and 64 ancestors); **Śluby i dzieci**
(marriage, children, grandchildren, great-grandchildren); **Inne małżeństwa i
dzieci matki** (the mother's other marriage and its children); **Stryjowie
lub wujowie oraz ciotki, i kuzynki** (the paternal uncle's family and the
cousins); **Najbliżsi sławni ludzie** (the nearest persons with a PSB entry);
**Uwagi** (the page's sources, with a long regest of the Teki Dworzaczka).

`original.md` carries the biography, Rodzice, the tree, and the marriage with
its descendants. Inne małżeństwa i dzieci matki, Stryjowie and Najbliżsi
sławni ludzie are not brought in; Uwagi is not brought in, and reaches the
site only as a sentence on the person's page saying what its sources are
(the editor's instruction of 2026-10-22). All of them are in `full.md`.

The page's own marks, kept as printed in both files:

- the heading "śluby i dzieci" opens with a small letter (the site's own
  slip); the English capitalises it;
- the tags in brackets after an office ("[str]", "[bku]", "[cen]") are the
  site's marks of the province or court of the office. What [str] stands for
  is not said on the page; not expanded;
- "bohater PSB": the site's mark for a person with an entry in the Polski
  Słownik Biograficzny. "bohater Wiki": the site's mark for a person its wiki
  has an article on;
- "artykuł w Nekrologii": a link to the database's obituaries section;
- "(linia: August Iliński 11.1.1147)": a link to the line of kinship through
  that person; the number is the person's ID in the database;
- the squares ■ and □ of the Stryjowie section (full.md) stand before a
  spouse: as the page uses them, the filled square before the spouse the
  children listed beneath descend from, the empty one before the others;
- "?1710-" and the like: the database's estimated dates, its own
  notation, not evidence;
- "ca 1763-": about 1763, no death known. "1744-ca 1806": about 1806.

Two headings are the script's, not the page's: "# Przodkowie" before the
ancestor tree (whose rows the page labels pradziadkowie, dziadkowie, rodzice)
and "# Wnuki" where the grandchildren's list begins. The tree's connector
cells and Sosa numbers are dropped; the couples stand father then mother,
four couples to a row of the page's table, which the linear text cannot show.

## Against the documents (the documents first)

What the edition's documents say, and where the page agrees or differs:

- **Father Stefan, grandfather Krzysztof.** The citation of 1782 (APP
  53/17/0/-/Konin Gr.118, document 23) names Paweł among the sons of
  Krzysztof Prusimski and Teresa Golińska, with Jan, Bogumił, Antoni and
  Stefan, the Starost's father; the boundary decree of 1775 (Konin Gr.145)
  calls Krzysztof the grandfather of the Starost. The page's tree agrees,
  and identifies the grandmother further: **Teresa Łoś-Golińska**, daughter
  of Jan Łoś-Goliński, burgrave of Konin, and Konstancja née Krusińska — the
  regest of 1786 in the page's Uwagi says the same of her parents. The
  documents name her only as Golińska.
- **The Starost's starosty.** The page's header line says "starosta [str]
  nieszawskie". The documents say Niszczewice throughout (and the page's own
  Uwagi regest "starosta nieszczewicki", and its PSB line "star.
  nieszczewicki" in the edition's own copy of the entry): the header's
  "nieszawskie" is the site's slip. The edition says Niszczewice.
- **The PSB volume.** The page cites "Polski Słownik Biograficzny t. 28 s.
  582: psb.24386.1". The edition's copy of the entry (`pachonski1982`) is
  from the editor's file "…(Polski Slownik Biograficzny T.27).md", pp.
  582-584: the volumes differ by one, the page range by its end. The entry
  is one and the same (the heading "Prusimski (Ostroróg-Prusimski) Kazimierz
  Józef Antoni", the dates 1744 to about 1806, the wife Marianna née
  Dąmbska). Which volume is right is not settled here; the difference is in
  NEEDS_CONFIRMATION ("The literature"), and nothing is changed on
  `pachonski1982` without the editor.
- **Born 4 March 1744 at Bieganowo.** The PSB entry (the edition's copy,
  p. 582): "Ur. 4 III w Kamionnej (wg Dworzaczka w Bieganowie)" — born 4
  March at Kamionna, at Bieganowo by Dworzaczek's account. The page's
  "w Bieganowie" follows Dworzaczek, whose Teki it cites in the Uwagi. The
  two accounts agree on the day and differ on the place named first; the
  entry itself records both.
- **Died about 1806.** Both the page and the PSB. Nothing in the edition's
  documents dates his death.
- **The marriage.** The page: Marianna née Dąmbska, married about 1770, born
  about 1763, daughter of Józef Wojciech Dąmbski, castellan of Kowal, and
  Barbara née Komorowska, a canoness of Warsaw. The PSB names her only as
  "Marianna z Lubraanca Dąmbska, daughter of Józef, castellan of Kowal, and
  Barbara née Komorowska" (p. 584), and has her with the Starost in Venice
  at the end of 1794. The edition's documents: the Prussian resident's
  dispatch from Venice of 14 December 1796 already speaks of Prusimski's
  grief at his wife's death (I. HA GR, Rep. 7 C, Nr. 1414, document 2),
  against Żychliński's death-year of 1797 (NEEDS_CONFIRMATION, settled by
  the rule of 2026-10-21: the edition keeps to the dispatch). No document
  dates the marriage; the page's "about 1770" is the database's estimate and
  stays out of the edition's prose.
- **Michalina, the only child.** The page: Michalina Zofia, 1778-1851,
  married first Józef Count Dąmbski (ca 1790-), then Stanisław Adam
  Miączyński (1780-1845). The edition: the only child (the bios, the PSB),
  died 19 January 1851 (editor, 2026-10-14); her marriages to Józef Dąmbski
  and Stanisław Miączyński are in the documents and the bios. Agrees.
- **Włodzimierz Miączyński 1811-1879.** The page's grandchildren's list: the
  edition's dates (died 20 December 1879, editor, 2026-10-14; his nephew
  Władysław the heir after him). Agrees. The page's Władysław Atanazy
  Gustaw, born 1852, is the nephew; the edition's documents name him only in
  the passing.
- **The regest of 1786** (Uwagi; Teki Dworzaczka, Księgi grodzkie
  poznańskie, seria Relacje, nr 197, Rel. C. Posn. T. 1113): the division
  carried out at the manor of the Trąbczyn estates on 29 March 1784, after
  the childless deaths of Paweł and the elder Antoni Prusimski; the parties
  the Zakrzewski, Tomicki, Taczanowski and Kołaczkowski claimants and
  Franciszek Tworowicz, the heirs of the Starost's aunts, with Antoni z
  Kolna Prusimski, starosta nieszczewicki; the court upheld the division of
  1740 between the sons of Krzysztof (Antoni, Paweł, Stefan; Jan died
  childless in 1740 before it) — Scheda I, chosen by Stefan the youngest:
  the estate of Kolno, the town of Kamionna and the wood-cutting of the
  woods of Goraj and Krobielnia, valued at 250,000 złp.; Scheda II, Paweł's,
  the under-chamberlain of His Royal Majesty: the estates of Trąmpczyn
  Drzazgowo, the mill of Osiny, Łazy, Nowawieś, Oporowo, parts of Oporówek,
  Kałowo Podbiele, Prusinowo, at 254,000 złp.; Scheda III, the elder
  Antoni's: Wierzbno, Brzeźno, part of Prusimia, and the wood-cutting and
  pasture of Goraj and Krobielnia and Szetlewko, at 201,000 złp. — and gave
  the whole paternal estate to Antoni the Starost as the only successor of
  the dead uncles, save the 40,000 złp. Katarzyna née Rozdrażewska had
  recorded for Paweł her future husband, which the Zakrzewscy, Tomiccy,
  Taczanowscy and Kołaczkowscy were to inherit (k. 161).
  This is the Starost's title to Trąbczyn, Kolno and Kamionna as the
  documents of the edition carry it (the founders of 1746, the decree of
  1775, the inspection of 1754), from a register the edition does not hold:
  the Poznań municipal court's Relacje series, not its Konin or Kalisz
  books. Whether the holding behind it is to be sought is the editor's
  (NEEDS_CONFIRMATION). The regest stays in `full.md`; the person's page
  says in a sentence what the Uwagi hold.

## The index

The work's 31 hits were read in context (Claude, 2026-10-22) and ruled in
`literature/index.yml`:

- `prusimski`: the page's own line (front) and his line at the foot of the
  ancestor tree (c02) stand; the parents' section (c01) is ruled out, its
  Prusimski being Stefan his father. The tree also names Jan, Krzysztof and
  Stefan; the ruling stands because the passage is the tree of his ancestry,
  which names him at its foot — the reason is in the comment at the ruling.
- `prusimska`: c03 stands for "Prusimska" (Michalina herself); "Dąmbska"
  there is ruled out (Marianna, the Starost's wife); "Miączyńska" in the
  grandchildren's list (c04) is ruled out (her daughters and
  granddaughters).
- `miaczynski`: c03 stands (Stanisław Adam Miączyński in the marriage
  section; the "Kajetan Miączyński" of the (linia:) beside him is his
  forebear); the grandchildren's list (c04) is ruled out, its Miączyńskis
  being his sons and grandsons.
- `kolno`: every "z Kolna" stands, the family's designation from the
  Prusimskis' estate.

The brought-in text names none of the edition's other people or places.

## Links

None written yet. The obvious ones, when the editor wants them: the regest's
division of 1740 and of 1784 against Konin Gr.118 document 23 (the citation
of 1782 naming the brothers), the decree of 1775 (Konin Gr.145) and the
inspection of 1754 (Konin Gr.136); the marriage section against the PSB
(pachonski1982, p. 584).
