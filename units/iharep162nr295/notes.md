# I. HA Rep. 162, Nr. 295 (GStA PK)

The cover and eleven pages of copies, papers of 28 January to 13 March 1805,
from the head of a file the Prussian state treasury kept from 1820 to March
1827 on the 50,000 thalers that Peter Friedrich von Triebenfeld had borrowed
from the Invalids' Fund and secured on the Zagórów estates. Three documents
on 13 pages. Scaffolded on 2026-10-05, when the page images were made; the
editor's transcription came the same day and was brought in, corrected,
summarised, translated and claim-checked. Status `translated`.

## Provenance

Geheimes Staatsarchiv Preußischer Kulturbesitz, Berlin, I. HA Rep. 162
Verwaltung des Staatsschatzes, Nr. 295. Older marks on the cover: "Rep 162",
"Sectio III Pars. 26. No: 1", "Vol. I, cont. Vol. 2", "1820 bis med: Maerz
1827", and the numbers 295 (blue pencil) and 281 (red, struck through). The
printed heading is "Central-Activa", with "Pohlen" written under it. The
editor's folder calls it "Capital on the Zagorow estates, now owned by
Trzcinski".

- **Photographs.** 23 images taken by the editor at the archive on 28 July
  2023 with a telephone (`PXL_20230728_*.jpg`, 3072 by 4080 pixels), the file
  lying on a table and a hand holding the page flat. The first is the cover.
  The other 22 are eleven pages, each photographed twice: the top of the page,
  then the bottom, overlapping by more than half the page.
- **Page images.** `intake/build_pages.py --crop` joins each pair into one
  image of the whole page and cuts the page out, into
  `<raw_dir>/processed/I_HA_Rep_162_Nr_295_<page id>.jpg`. `0001_a` is the
  cover, `0002_a` to `0012_a` the eleven pages in the order photographed. How
  the join is made, and what was checked, is in that script's heading; the
  numbers are in `intake/stitch.json`.
  - Above the seam a page image is the top photograph unchanged; below it,
    the bottom photograph laid onto the top one. The seam runs through the
    gap between two lines of writing, so no line is doubled, lost, or made of
    two photographs. On pages 0003, 0005, 0007 and 0009 the seam crosses the
    tail of a letter in a few places (under 2 in 100 of its length); the two
    photographs agree there to within about two pixels.
  - Outside the written area the two photographs do not always agree, because
    the page was not lying the same way in both: a small step can be seen at
    the fold on 0005 and at the edge of the leaves on 0006 and 0009. No
    writing is affected.
  - The hand holding the page is in the right or left margin of most images.
- **What is not there.** The pages carry no leaf numbers in the photographs.
  The last page (0012) ends with the opening words of a further mortgage
  certificate ("Die in der Provinz Südpreußen und deren Ko-"), which was not
  photographed. Nothing from the file's own years, 1820 to 1827, was
  photographed.

## The documents

Three documents, one per instrument, following the editor's ruling for APP
53/968/0/-/801 the same day ("three documents is fine"). Not asked again; if
the bond and its second acknowledgement should be one document, documents 1
and 2 can be joined.

| Document | Pages | What it is | Date, place |
|---|---|---|---|
| 1 | 0002 to 0005 (line 12) | Triebenfeld's bond to the General Invalids' Fund, with the protocol of its acknowledgement before the first Kurmark justice office, signed Wilmanns | 28 January 1805, Berlin |
| 2 | 0005 (line 13) to 0008 (line 7) | The South Prussian Government's certificate of the second acknowledgement (hearing of 27 February before Stosch and v. Zelislawski, v. Lichnowski as witness of identity; signed Schiller), its fee note and docket, and the Ingrossator Beda's note of the entry in the mortgage book, 13 March | 5 March 1805, Kalisz |
| 3 | 0008 (line 8) to 0012 | The mortgage certificate for the town of Zagórów, No. 1179, signed Danckelmann, Husarzewski, Schlegel, Beda; its last two lines are the stamp note and first line of a further certificate | 13 March 1805, Kalisz |

The cover (0001) is front matter. Documents 2 and 3 begin partway down a page
(`intake/document_boundaries.csv`, `first_line`). Types: `cession`,
`attestation`, `certified_copy` (the term Oe 1 Bü 14525 uses for a mortgage
register statement). Relations: 2 confirms 1, 3 registers 1.

## Transcription

The editor's twelve files (one per page image, line by line, with ¬ at broken
words) were put in `<raw_dir>/txt/` on 2026-10-05 and copied unchanged into
`transcriptions/` under their own names
(`<n>_I_HA_Rep_162_Nr_295_<page id>.txt`); `import_pages.py` assembled
`corpus.txt`.

- **Line ends.** Five words broken at a line end were joined by hand in
  `linebreak_decisions.csv` (Hundert, inhalts, Commissarien,
  Aufkündigungsfrist, constituirt).
- **Paragraphs.** Set by hand where the cues failed
  (`paragraph_decisions.csv`): nine automatic breaks before a date or figure
  that opens a line inside a sentence ("31. Juli 1801.", "330. Morgen", "6.
  monatliche") were turned into runs, and thirteen breaks added (rows with
  cue `hand`) before signatures, fee lines and the numbered entries. A hand
  row is found again only by the whole line, up to 70 characters.

## Corrections (2026-10-05)

34 passages, each read on the page image: `intake/corrections.py`, logged in
`transcription_decisions.csv`. What was left is in `intake/unresolved.md`.

- **Changes of sense:** "Trąbczyn" at the end of the list of estates in the
  bond is "Grądzyn" (the page; the same list on 0011); "Verhandlungs-" is
  "Seehandlungs-Obligationen"; "Kommer Kreise" is "Koniner Kreise"; "Ernst"
  is "Frist"; "einramme" is "einräume"; "gehöscht" is "gelöscht"; "minus[?]"
  is "[Ju]nius"; "[T?]hurmarkisches" is "Churmärkisches". The cover's "lig
  Med:" is "bis med:".
- **Signs and marks:** the Reichsthaler sign is "rt" throughout (five places
  had rn, rd, rl, rue); the pfennig sign is "pf."; seven ¬ added or put in
  place of a hyphen; "Königl" three times for "König".
- **Added:** "und deren" in the last line, and the stamp note in the margin
  beside it.

## Summaries, translation, claim check (2026-10-05)

German summaries written in the session from the reading, the English
translated from them (`intake/summaries_draft.py`); 27 statements checked
against the documents, one weakened (`intake/claim_check.yml`). The site's
summary files were not rebuilt from the local cache: the three lines were
inserted into each.

Translated in session, as Nr. 12366 was; the pages are in
`intake/translation/doc<N>.yml`, written into the untagged cache by
`intake/translation/write_cache.py`. Status `translated`, `published_tag:
""`. check_translations.py: no row, after "sub hypotheca generali" and
"speciali" were put into English (the checker forbids "hypothec" by the
editor's ruling of 2026-09-17). uncanonical_names.py: nothing in this
holding. Names in the edition's forms where settled (Zagórów, Wrocław,
Kalisz, Brzeg, Świątniki, Grądzyń); Olesnica as other published English has
it.

## Authorities (2026-10-05)

Matched without change: Triebenfeld, Hohenlohe, Friedrich Wilhelm II,
Danckelmann, Husarzewski (entry `hussarzewski`), and the three lessees of
Oleśnica, Giese, Bagans and Gietzinger, who are in I. HA GR, Rep. 7 C, Nr.
3705. New: `lichnowski-kalisz`, the Regierungsrath v. Lichnowski who vouches
for Triebenfeld's identity in document 2; the entry for the creditors
(`lichnowski`) no longer matches after "Regierungsrath v." or "gez. v.", so
he is not counted among them. The Landesältester v. Lichnowski at Brzeg in
document 3 is the creditor. Place variant added: Grądzyn. Not added: Stosch,
v. Zelislawski, Schiller, Schlegel, Beda, Wilmanns (officials named once
each, in signatures).

Glossary: new entry `rubrik` (the sections of the mortgage book; not checked
against the Hypothekenordnung, which is not online here); "vol.", "Cop." and
"Ins." ruled out. Every match of the new pattern was read: this holding and
Nr. 12367, document 7, all genuine.

## The site (2026-10-05)

`about.md` and `process.md` in both languages. The timeline entry for the
Invalids' Fund loan (26 January 1805) gained two sentences and documents 1
and 3 as sources; section III of the era essay gained two sentences with
links to the bond and the certificate, in both languages. The holding pages
of Oe 1 Bü 14525, Oe 1 Bü 9454 and Nr. 3705 name this holding among their
related holdings.

## Quirks worth knowing

- Everything is a copy made for the file, in one clerk's hand: signatures are
  "gez.", seals "L. S.".
- The file is of 1820 to 1827, the papers copied into it of 1805;
  `date_span` gives 1805, the years of what was photographed.
- The pages carry no leaf numbers. The last page ends with the first line of
  a further mortgage certificate, which was not photographed.
- Trąbczyn is not among the estates the bond of 250,000 Rthl was registered
  on: Zagórów, Drzewce, Kopojno, Świątniki, Skokum, Oleśnica, Wrąbczyn,
  Grądzyń. The certificate names Trąbczyn only for Lichnowski's claim.

## Still to do

- The English has not been read against the page images.
- The items in `intake/unresolved.md`; the editor may want to look at
  "nachstehende" (0004) and the figure in the fee note on 0007.
- The editor's word on the division into three documents.
