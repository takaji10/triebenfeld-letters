# Mączak 1968, Export of Grain

One document on 24 pages: Antoni Mączak, "Export of Grain and the Problem of
Distribution of National Income in the Years 1550-1650", *Acta Poloniae
Historica* 18 (1968), pp. 75-98, translated by Ewa Tymowska. The second holding
of published literature (after Pachoński 1973). Added 2026-10-20: read from the
editor's PDF in session, summarised, claim-checked, with its page. **Not
published**: see "Open" below.

Everything about how the text was made is in the docstring of
`intake/holding.py`; the summary is in `intake/summaries.py`, its check in
`intake/claim_check.yml`.

## The editor's instructions (2026-10-20)

- "Add the article Antoni Mączak - Export of Grain 1550-1650.pdf at
  J:\Documents\Archive\Genealogy\References\Books to the site, to provide
  supporting material for the agricultural activities of the Olęders. It
  remains to be seen how useful the article will be, but that can be
  determined later."
- "Nowa Wieś" is a common place name in Poland: a link must be sure it means
  the village of the Trąbczyn estate. (The article names no Nowa Wieś. The
  holding page points to Konin Gr.136, whose Nowa Wieś is inspected with
  Trąbczyn, Osiny and Łazy as one of Katarzyna Prusimska's villages, and says
  so. The place index matches "Nowa Wieś" only in the visitation of 1791:
  `reference/places.yml`, `nowawies-trabczyn`.)

## Provenance

- The PDF is the digital copy in RCIN (https://rcin.org.pl/dlibra/publication/19109/edition/5534),
  digitised by the Institute of History of the Polish Academy of Sciences
  from its library's copy; RCIN's record: "Rights Reserved - Free Access",
  "Copyright-protected material. May be used within the limits of statutory
  user freedoms". Publisher of the journal: Zakład Narodowy im. Ossolińskich,
  Wrocław. Each page is an image of about 150 dpi with a text layer; it was
  rendered at 300 dpi to be read.
- The two figures were rendered from the PDF by `holding.py --crop` into a new
  folder beside the editor's other references,
  `J:\Documents\Archive\Genealogy\References\Mączak 1968, Export of Grain\processed\`.
- **Repository** `published`, with this holding's own credit line (unit.yml
  `credit`, new 2026-10-20: the Licences page prints a holding's credit in
  place of the repository's, so each publisher is named).
- **Kind** `kind: literature`; **document type** `article`; dated 1968, no
  place, no estate. **Language** `en`: the page has no English tab
  (letter.html, letter.js), and the holding's status is `transcribed`.
- **Era** `prusimski-boundary`, the era of its years (1550-1650, the era from
  1589), decided in session.

## The text

- By paragraph, footnote marks as raised figures, each page's notes at its
  foot; `footnotes.yml` (`note_start`) sets the notes apart.
- Tables as rows, "| a | b |", "<" for a cell joined to the one before it;
  drawn as tables in the reading view (`build_site_data.text_table_html`, new
  2026-10-20).
- Four words broken over a page end given whole where they begin
  (`holding.py`, PAGE_ENDS).
- The print's slips kept (list in `holding.py`).

## People and places

- No person is indexed: the names are of historians and of sixteenth-century
  magnate families (Tęczyński, Firlej, Lubomirski), none in another holding.
  The name list matched none.
- Places found: Warsaw, and Germany (from the title in note 1). Gdańsk,
  Cracow, Włocławek and the provinces are not in the place index and are not
  added for one article.

## Open

- **Copyright.** The article is in copyright (RCIN: rights reserved; the
  translator's and the journal's rights). Publishing it whole needs the
  editor's decision, as for Pachoński 1973 (`docs/NEEDS_CONFIRMATION.md`).
  The Licences page already names it beside Pachoński as outside CC BY.
- The editor's view of how useful it is, and the word to publish.
