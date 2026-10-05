# AGAD 1/174/0/1/6

Two documents on three pages, 12 and 21 July 1807: two entries from the
register of the Governing Commission's orders and resolutions. The second is
the resolution that returned the Prusimski estates to Michalina Dąbska; the
first is the order for Wybicki on which it rests. Added on 2026-10-04 at the
editor's request: pages cut out of the images, the editor's text cut to
pages, corrected, summarised, and given its place on the site; translated
and its summaries claim-checked in session on 2026-10-05. Its companion is AGAD 1/174/0/2/73 (`units/agad11740273/`), the
commission's file with her petitions and the draft of the resolution; read
that unit's `notes.md` for what the two share (archive, era, authorities).

## Provenance

Archiwum Główne Akt Dawnych, Warsaw, fonds 174 (Komisja Rządząca), series 1,
unit 6: "Zbiór wyroków, uchwał, zaleceń i wszelkich rezolucji Komisji
Rządzącej". A bound register in a clerk's fair hand, paged in ink (struck
out) and again in pencil.

- **Images.** Three: 028, 029, 180.
- **What the editor asked for.** "Note the page numbers at the top corners of
  the pages in the scans - only 47, 48, and 331 are relevant", and the images
  "cropped to remove the unrelated pages".
- **Pages.** Page 47 is the right side of image 028 (`0028_a2`), page 48 the
  left side of image 029 (`0029_a1`), page 331 the right side of image 180
  (`0180_a2`); cut out by `intake/build_pages.py --crop`.
- Pages 47 and 48 also hold other entries: on 47 an order of 11 July on the
  staff of the internal directorate, on 48 an order of 12 July on the Piarist
  college and the archivist's certificate "Zgodno z Aktami, Ignacy
  Szczurowski, Sekr. Archiwista". They are on the page images and not in the
  edition.

## Transcription

The editor's single Markdown file stays in `<raw_dir>`. It is by paragraph
and marks the pages "[47]", "[48]", "[331]". `intake/build_pages.py` cut it
into `transcriptions/<page id>.txt`. Marks 47 and 48 are one document.

- Page 47 ends "Poznań-" with the catchword "skim"; page 48 begins with the
  whole word. The transcription has the word once, at the foot of page 47.
- Not transcribed: "podpisano" (signed) before the names, and "(LS)".

## The documents

| No. | Pages | What it is |
|---|---|---|
| 1 | 0028_a2, 0029_a1 | Order to the Director of Internal Affairs to carry out Napoleon's decree of 5 June 1807 for Wybicki; Warsaw, 12 July 1807 |
| 2 | 0180_a2 | Resolution extending that decree to Michalina Dąbska, General Niemojewski and Wichrowski; Dresden, 21 July 1807; with the heading of the section of resolutions taken at Dresden |

## Corrections (2026-10-04)

Nine passages: `intake/corrections.py`, logged in
`transcription_decisions.csv`. The entry on page 331 had been spelled out and
modernised and is given as the page has it. In the section heading "lub do
Directorium Generalnego" is "tak do ... iako i do": issued both to the
general directorate and to the directors singly.

## Rulings and correspondents (2026-10-04)

Dates and places from each entry's closing formula ("Działo się w Warszawie
na Sessyi dnia 12 Lipca 1807", "w Dreznie ... 21. Lipca 1807"). Both are
`note`, the vocabulary's word for an authority's own decree or minute.
Document 2 supplements 1. The sender is the commission; document 1 is
addressed to the Director of Internal Affairs, whom it does not name.

Document 2 is the fair copy of the draft in AGAD 1/174/0/2/73, document 1.
The two are not linked as duplicates: `duplicate_of` works inside one holding
only. Both holdings' pages say so.

## Worth knowing from the reading

- Wybicki's estates are named: Manieczki (the editor reads "Maniezki"),
  Przylepki, Boreczek and Esterpol, department of Poznań. The decree is "of
  the Emperor of the French and King of Italy", given at Finckenstein on 5
  June 1807, and charges "the provisional Polish government" with carrying it
  out.
- The register calls her "Michaliny z Prusinskich Dambskiey": the clerk's
  form of Prusimskich. In the heading he wrote "Dąbskiey" and added an m
  above.

## Summaries, authorities, era

As for AGAD 1/174/0/2/73: summaries written in session, claim-checked in
session on 2026-10-05 (`intake/claim_check.yml`, 14 statements, all supported);
people Małachowski and Łuszczewski added; era `hohenlohe` for now.

## Still to do

- The editor's ruling on the era, with 1/174/0/2/73.
- Reading the English against the scans. (Translated in session on
  2026-10-05 like 1/174/0/2/73: pages in `intake/translation/`, status
  `translated`, untagged; check_translations.py and uncanonical_names.py
  raised nothing. "Maniezki" and "z Prusińskich" stand as the register
  writes them.)
- The words in `intake/unresolved.md`.
