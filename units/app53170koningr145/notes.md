# 53/17/0/-/Konin Gr.145 (APP)

One document on 122 pages: the decree of the boundary commission that sat
between Trąbczyn and Łukomia from 13 September 1775, as entered in the castle
court records at Brześć Kujawski on 23 September 1776 and copied into a book
of the castle court of Konin. Polish with Latin. Added on 2026-10-06 from the
editor's scans, transcription and English translation. Status `translated`.
The first holding of the Prusimski era (`era: prusimski-boundary`): the
editor, 2026-10-06, "from the Prusimski era. It's not related to Hohenlohe."

## Provenance

Archiwum Państwowe w Poznaniu, fonds 53/17, "Konin Gr. 145": a volume the
editor's folder calls "Relationes-oblatae [protocollon] 1776". The archive's
page for the unit (szukajwarchiwach.gov.pl, unit 982231) could not be opened
from here: the site refuses automated access. What is said of the volume
comes from the editor's files and the scans. **If the archive's description
says more (the fonds' name, the volume's extent), it should be added.**

- **Scans.** 62, `654.jpg` to `715.jpg`, each an opening, named after the
  leaf on its right. Scan 673 shows leaf 672 verso and leaf 673 recto.
- **Pages.** `intake/build_pages.py --crop` cuts each at the fold, which it
  records per scan (found by the darkest column near the middle, checked on
  contact sheets). `<scan>_a1` is the left page, `<scan>_a2` the right. Two
  halves are cut and not staged, kept in `processed/_not_staged/`: `0654_a1`
  (the end of another entry, Zakrzewski, dated at Konin 15 November 1776) and
  `0655_a1` (leaf 654 verso, blank and crossed through).
- The entry before ours being dated at Konin on 15 November 1776, ours was
  copied into the book after that day. The transcription has no date for the
  copying.

## Transcription

The editor's file, "... - Polish Original.md", marks each page by its leaf
("[655]", "[655v]"). `intake/build_pages.py --write` cut it into
`transcriptions/<page id>.txt` and wrote `corpus.txt`, checking that nothing
was lost. Leaf N recto is `<N>_a2`; leaf N verso is `<N+1>_a1`.

- **Modern spelling.** The Polish is normalised by the editor: i for y, j for
  i before a vowel, small letters, modern endings. This is unlike the other
  Polish holdings, which keep the scribe's spelling. Kept as supplied; said
  in `about.md`, `process.md` and on the edition's About page.
- **By paragraph**, all 122 pages (`rulings.yml`, `pages: by_paragraph`).
- The editor's asterisks round Latin words are taken off. Their one footnote
  (an English rendering of the Latin on leaf 656) is left out of the text.
- Words in square brackets are the editor's additions. Two carry a doubt:
  "[Marszałek Miecznik?]" (leaf 657 verso) and "J[egomość?]" (leaf 715).

## The light check (2026-10-06)

The editor asked whether the text could be handled "using a light touch,
since it's already been worked over before", adding that the Prusimski era
texts are less error-prone than the Hohenlohe ones. Answered yes, with a
caveat, after reading pages word for word against the scans:

- Leaves 673, 688 and 707 verso (about 900 words) and then 656: the
  translation follows the Polish closely and reads well; the transcription
  has about one small slip in a hundred words ("omiema" for "obiema",
  "paniete" for "pariete", "ze znanej" for "zeznanej"), more in the
  abbreviated Latin of leaf 656 ("Janosza" for "Junosza", "extra" left out
  before "Ordinariorum"), and **one dropped phrase**: on leaf 673 six words,
  "las cały Lusnie zajmujących i zabierających", skipped between two words of
  the same ending. The English lacked them too.
- `intake/corrections.py`: those 23 readings, one line added to the title
  page, and 93 accents put right through the whole text without the scans
  (non-words only, where the transcription itself has the right form many
  times). Logged in `transcription_decisions.csv`.
- **Not done:** the other 117 pages were not compared with the scans. More
  dropped phrases are likely. A full check means reading every page (three
  enlarged strips a page); it can be done in stages if the editor wants it.

## The document

One document (the package rule). Dated 23 September 1776, the entry at
Brześć Kujawski; `doc_type: decree`, a kind added for it (label in
`site/_data/i18n.yml`). Place of writing Brześć Kujawski. Estates: trabczyn,
lukomia, drzewce. No sender or recipient.

The seven "sections" are the editor's division, from their outline:
the entry (leaf 655); 1 the decree's opening, the commissioners, the act of
parliament and the oath (655 to 658); 2 the opening of the commission, the
quarrel over the pen, the failed settlement (658 to 660); 3 summonses,
appearances, documents produced (660v to 661v); 4 Prusimski's boundary line
(661v to 680); 5 the review of Chełmski's line, the Trąbczyn and Biskupice
boundary, sworn testimony, the ruling on the starting point (680 to 690); 6
the ruling on the whole line, the mounds between Trąbczyn and Łukomia, the
oath (690 to 702); 7 the Trąbczyn and Biskupice boundary, its mounds,
penalties, the delivery of possession of 1771 set aside, default judgment,
signatures (702 to 715).

## Translation (2026-10-06)

The English is the editor's ("... - English Translation.md"), not made again.
`intake/translation/build_doc1.py` cuts it to the pages and writes `doc1.yml`;
`write_cache.py` saves it; then check_translations.py and
publish_translations.py as for any holding.

- The editor's headings become lines in square brackets; their twenty
  footnotes become "[Translator's note: ...]" after the paragraph.
- Their page marks stand at sentence ends, so a page's English can run a few
  lines past the Polish. Two marks were most of a page late (pages 27 and
  107) and the English was moved (`MOVES`).
- Five changes follow corrections to the Polish (`FIXES`, `EVERYWHERE`).
- **check_translations.py: 49 rows, none a fault.** Most are the termbase
  expecting its own rendering where the editor's translation has another
  that is right here: "komornik" is a boundary surveyor in this record, not
  a lodger; the Olęder settlers; "wall mound". Three pages have twice as many
  English words as Polish because the translator's notes stand on them. Two
  doubts are the editor's own and stand in the English only ("[uncertain:
  Stefan] Zielonacki", "[uncertain: narożnik]").
- The translation calls the court "Brest Kuyavia Municipal Court"; the
  edition's prose says "the castle court at Brześć Kujawski". The translation
  is the editor's and is left.
- **The editor's apparatus not yet used:** their glossary of 89 terms at the
  end of the English file. The edition's own glossary has some of the same
  words already. Bringing the rest in (each with a German definition and a
  pattern) is a job of its own: `docs/TODO.md`.

## Summary and claim check (2026-10-06)

One summary, German first (`intake/summaries_draft.py`), 16 statements, all
supported (`intake/claim_check.yml`). One rests partly on the editor's note:
that the settlement failed.

## Authorities (2026-10-06)

New person: Ludwik Dąmbski, the president (`dambski-ludwik`, matched only with
his forename). The existing entry for the Chełmski family now has the decree
in its biography. New place: Brześć Kujawski. Matched without change:
Prusimski, Trąbczyn, Łukomia, Łukom, Drzewce, Zagórów, Osiny, Szetlewek,
Kalisz, Konin. **Seven existing entries matched other people or ordinary
Polish words in this document** and are now shut out of it by a new field,
`not_in` (`pipeline/build/entities.py`): Simon, Radziwiłł, Małachowski,
Florian Gelanski; Brzyce ("Brzyzna"), Brzeg ("brzeg", a bank), Swięcia
("święcie", a feast). The commissioners other than the president, and the
many witnesses, are not indexed.

## The site (2026-10-06)

`about.md` and `process.md` in both languages; the era is now `populated`
in `reference/eras.yml`, and the story page says the era has its first
document; a timeline entry for 13 September 1775; the About page's figures
and three of its sentences (the spelling, who made the English, which eras
have documents).

## Still to do

- The editor's word on a full check of the 117 pages not compared.
- The archive's description of the volume, if the editor can paste it.
- The editor's glossary of 89 terms.
- An account of the Prusimski era like the Hohenlohe one: this is its first
  document and the era has no essay.
