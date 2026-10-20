# Pachoński 1973, Les Polonais dans la République de Venise

One document on twenty pages: Jan Pachoński, "Les Polonais dans la République
de Venise (1794-1797)", in *Italia, Venezia e Polonia tra illuminismo e
romanticismo*, ed. Vittore Branca (Florence: Leo S. Olschki, 1973), pp.
237-256. The first holding of **published literature** (the editor,
2026-10-20: "a new literary source"). Added 2026-10-20: read from the scans in
session, translated, summarised, claim-checked, with its page. Cleared to
be published by the editor the same day ("Add this literature as an allowed
source to publish"); **not yet published**: see "Open" below.

Everything about how the text was made is in the docstring of
`intake/holding.py`; the English and the summaries are in `intake/english.py`.

## The editor's instructions (2026-10-20)

- Only Pachoński's article, scans `2026-10-17-0001_2R.tif` to
  `2026-10-17-0011_1L.tif`. The other scans (`01.tif` to `11.tif`) only for
  the book's title and imprint; the contents and the introduction are not
  relevant.
- An English translation, the footnotes, and the map; "other than the map,
  only the text needs to be included" (no page images of the text pages).
- "Antoni Prusimski is referenced here in a footnote as Prusiński" (note 10,
  p. 240: "Antoni Prusiński de Nieszczewice").
- "The home page and timeline should not be affected by the dates of literary
  sources - reserve this information for primary source documents."

## Provenance

- The editor's folder `D:\Pictures\Scans\Italia, Venezia e Polonia - Tra
  illuminismo e romanticismo (1973, Branca ed.)`: 600 dpi, black and white
  (the cover in colour). `2026-10-17-0006_1L.tif` is the map, scanned on its
  side; it is the only image of the edition (`processed/0246_a.jpg`, cut by
  `holding.py --crop`).
- The book: title page (03), imprint (04: "Atti del III convegno di studi
  promosso e organizzato dalla Fondazione Giorgio Cini dall'Accademia Polacca
  delle Scienze (Venezia, 15-17 ottobre 1970)", "Copyright 1973 Leo S.
  Olschki Editore"), series page (02: Fondazione Giorgio Cini, Centro di
  cultura e civiltà, Scuola di S. Giorgio per lo studio della civiltà
  veneziana), contents (05: the article at p. 237, the last of the volume's
  papers). Scan 04 also has a faint library stamp and a pencil mark, not read.
- **Repository** `published` ("Published works") in
  `reference/repositories.yml` and the credits (`site/_data/rights.yml`,
  credit "© 1973 Leo S. Olschki Editore, Firenze"). The credit is the
  repository's, so a second book from another publisher needs the credit
  line reconsidered (one entry per publisher, or a credit per holding).
- **Kind** `kind: literature` in `unit.yml`: `build_site_data.LITERATURE`
  keeps its date out of the home page's span, the timeline's yearly counts,
  the eras' spans and the "documented" years of people and places.
- **Document type** `article` ("Article", "Aufsatz"). Dated 1973 (`read`,
  from the imprint), no place, no estate (as I. HA GR, Rep. 7 C, Nr. 1414).
  Era `hohenlohe`, its subject's years and its neighbour Nr. 1414's era.
- **Citation**: `documents: citation:` with `kind: article` and a free text
  (`build_site_data.citation_of`, `citation_kind`); the text pages say "A
  page of printed text: the edition gives its words, not a picture of the
  page" instead of "No scan matched".

## The text

- By paragraph, footnote marks as raised figures, each page's notes at its
  foot; `footnotes.yml` (`note_start`) sets the note lines apart.
- Words broken over a page end, and note 4, given whole on the page where
  they begin (`holding.py`, PAGE_ENDS). The line-break pass would otherwise
  join the broken word to the first footnote below it.
- The print's slips kept; "Kosciuszko" (p. 237) and "Kościuszko" (p. 239)
  both as printed.

## People and places

- Antoni Prusimski (`prusimski`): matched by "(?<=Antoni )Prusiński(?= de
  Nieszczewice)"; his bio names the article.
- General Jan Henryk Dąbrowski: new entry `dabrowski-jan-henryk`, only in
  this document; the name list's "Dąbrowski" (a lessee in Oe 1 Bü 9454,
  letter 136) shut out of it (`seed_not_in`).
- Zajączek and Wybicki are the edition's men (Józef Zajączek, Józef
  Wybicki) and are matched. "Simon" (Simon Askenazy, a historian) and
  "Poniatowski" (here Stanisław, the King's nephew, not Prince Józef) shut
  out with `not_in`. Napoleon is not matched ("Napoléon"; widening his
  pattern would catch "Code Napoléon").
- The other forty or so emigrés are not indexed: they appear in no other
  holding. Places found (Venice, Paris, Warsaw, Dresden, Berlin, Bologna,
  Petersburg, Brześć Kujawski) read and right.

## Open

- ~~Copyright~~ **settled** (editor, 2026-10-20: "Add this literature as an
  allowed source to publish"). The article and its map are in copyright
  (Olschki 1973). The Licences page now carves them out of CC BY, with the
  English and summaries of the article, credits the publisher and promises
  a takedown on request. A later book of literature goes into that
  paragraph too (it names this article only).
- The editor's look at the map crop and the English.
