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

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

The register is a fair copy in a clerk's hand. The names under the entries are written by the clerk after the word "podpisano" (signed), with the letters "LS" for the place of the seal; neither is transcribed. Pages 47 and 48 also hold three other entries, which are not included. The commission's draft of the resolution of 21 July, with the corrections made to it, is in its files: [[unit:agad11740273]].

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The editor supplied three images from the volume. Each shows two facing pages, of which one is wanted; that page was cut out of the image and the other left aside. The holding has three pages: those numbered 47, 48 and 331 in pencil at the top corner.

### Transcription

The editor transcribed the two entries that concern the estates, paragraph by paragraph and not line by line. The other entries on pages 47 and 48 are not transcribed, so those two page images show more text than is transcribed. The order of 12 July begins in the lower half of page 47 and ends in the upper half of page 48.

### Division into documents

Each of the two entries is one document. The heading of the section that the resolution of 21 July opens is kept with it. Dates are taken from each entry's closing formula.

### Corrections

An AI model (Claude) compared the transcription with the scans and corrected it where the page is plain: nine passages. The transcription of page 331 had spelled out the abbreviations and modernised the spelling; the entry is given as the page has it. One word of the section heading was misread: the resolutions were issued "both to the general directorate and to the directors singly", not "or". Each change is logged with its reason.

### Summaries

The summaries were written in German from a reading of each document against its scan, and translated into English. Each statement in them was then checked against its document, under the same rules as the separate check that the summaries of other holdings received: a summary may say only what the document says. All of them held.

### Translation

The documents were translated into English in a working session under the same rules as the other holdings: every figure, name and mark of doubt carried across, names in their settled forms where these exist and otherwise as the page spells them, and passages that do not read left visibly doubtful rather than smoothed. Both entries were translated from the Polish, with the forms of address given in English (the Most Illustrious, the Honourable, Mrs). The same automatic check as elsewhere then confirmed that every figure and every mark of doubt survives into the English.
