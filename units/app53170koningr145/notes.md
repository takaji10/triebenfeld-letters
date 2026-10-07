# 53/17/0/-/Konin Gr.145 (APP)

One document on 122 pages: the decree of the boundary commission that sat
between Trąbczyn and Łukomia from 13 September 1775, as entered in the castle
court records at Brześć Kujawski on 23 September 1776 and copied into a book
of the castle court of Konin. Polish with Latin. Added on 2026-10-06 from the
editor's scans, transcription and English translation. Status `translated`.
The first holding of the Prusimski era (`era: prusimski-boundary`): the
editor, 2026-10-06, "from the Prusimski era. It's not related to Hohenlohe."

## Provenance

Archiwum Państwowe w Poznaniu, fonds 53/17, "Księgi sądu i urzędu grodzkiego
w Koninie" (books of the castle court and castle office of Konin), unit
"Konin Gr. 145": a volume the editor's folder calls "Relationes-oblatae
[protocollon] 1776". The archive's page for the unit (szukajwarchiwach.gov.pl,
unit 982231) cannot be opened from here: the site refuses automated access.
The editor pasted the fonds' name and the archive's account of the castle
court on 2026-10-06; it is given, in English and German, in `about.md` and
`about_de.md` under the historical background, and the name is in `unit.yml`
(`fonds:`).

- **Scans.** 62, `654.jpg` to `715.jpg`, each an opening, named after the
  leaf on its right. Scan 673 shows leaf 672 verso and leaf 673 recto.
- **Pages.** `intake/build_pages.py --crop` cuts each at the fold, which it
  records per scan. The first folds, taken at the darkest column near the
  middle, stood 60 to 170 pixels left of the gutter on most scans and cut
  the line ends of the left pages; they were found again as the thin dark
  line of the gutter itself, and each page keeps 30 pixels beyond it.
  **The folds are the editor's**: reviewed on
  `review/app53170koningr145/folds/` on 2026-10-07 and saved in
  `intake/folds.json` (53 of 62 moved, 39 sheets turned).
  `<scan>_a1` is the left page, `<scan>_a2` the right. Two
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

## The full check (2026-10-06)

The editor: "we should check for dropped phrases, and in the end I want you
to highlight them for me and tell me if they are significant to the meaning
of the text or not. You can update the English translations with anything
that was dropped."

- **All 122 pages read against the scans** (`intake/full_check_pages.txt`),
  each as two enlarged halves. **233 findings** in
  `intake/full_check_rows.py`, applied once by `intake/corrections_full.py
  --write` and logged in `transcription_decisions.csv`. Do not run it, or
  `build_pages.py --write`, or `corrections.py --write`, again.
- **26 dropped phrases** (27 with the one of the light check), from one word
  to about sixty. Nearly all were skipped between two occurrences of the
  same word. **207 misread words** that change a meaning. Spelling slips
  that change nothing were not collected.
- By weight: 7 bear on what the court found or ordered, 58 add or correct a
  fact, 168 are legal wording. The largest: about sixty words on leaf 709
  verso, the court's finding that Chełmski raided the inn with armed men,
  had shots fired into it, and that it was set on fire.
- **The English was mostly right where the Polish had slipped.** It needed
  32 changes (`intake/translation/fixes_full.py`): 24 for dropped phrases,
  7 where it had followed a misread word, and one that is mine, not from the
  check: the tower. The Polish has Chełmski enter the tower twelve weeks
  from the decree and sit two weeks; the English read twelve weeks' sitting.
- **The English had dropped a paragraph of its own**: about a hundred Polish
  words at the head of leaf 680 (the start of the editor's section 5) had no
  English. Translated from the Polish in the editor's terms; the process
  page says so.
- **The sheet for the editor**: `review/app53170koningr145/dropped/`
  (`intake/dropped_sheet.py`), every dropped phrase with its verdict, the
  four misreadings in the court's rulings, and the other English changes.
- Left as read, with a doubt: the pond name "Garmin" (leaf 691); the name
  Krzeczkowski, written above the line (leaf 709 verso; the second vowel
  could be y).

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
- Five changes follow corrections to the Polish (`FIXES`, `EVERYWHERE`),
  and 32 more the full check (`fixes_full.py`, searched through the whole
  text, each found exactly once).
- **check_translations.py: 48 rows, none a fault.** Most are the termbase
  expecting its own rendering where the editor's translation has another
  that is right here: "komornik" is a boundary surveyor in this record, not
  a lodger; the Olęder settlers; "wall mound". Three pages have twice as many
  English words as Polish because the translator's notes stand on them. One
  doubt is the editor's own and stands in the English only ("[uncertain:
  Stefan] Zielonacki").
- The translation calls the court "Brest Kuyavia Municipal Court"; the
  edition's prose says "the castle court at Brześć Kujawski". The translation
  is the editor's and is left.
- **The editor's apparatus not yet used:** their glossary of 89 terms at the
  end of the English file. The edition's own glossary has some of the same
  words already. Bringing the rest in (each with a German definition and a
  pattern) is a job of its own: `docs/TODO.md`.

## Summary and claim check (2026-10-06)

One summary, German first (`intake/summaries_draft.py`), 18 statements, all
supported (`intake/claim_check.yml`). One rests partly on the editor's note:
that the settlement failed. After the full check the sentence on Chełmski's
sentence was rewritten (the raid on the inn, two weeks in the tower, 8,000
złoty) and checked again.

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

- Publishing, at the editor's word. (The folds are the editor's: reviewed on
  the fold page on 2026-10-07, 62 scan(s), 39 of them turned; saved in
  `intake/folds.json` and the pages cut again from it.)
- The editor's look at the sheet of dropped phrases
  (`review/app53170koningr145/dropped/`), above all the tower sentence and
  the paragraph translated for leaf 680.
- A `spelling:` label for the document (modern), once the field is built
  (`docs/PRUSIMSKI_ERA_PLAN.md`).
- The editor's glossary of 89 terms.
- An account of the Prusimski era like the Hohenlohe one: this is its first
  document and the era has no essay.
