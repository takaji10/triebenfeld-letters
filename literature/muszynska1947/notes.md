# Muszyńska-Zygmańska (1947): notes

Janina Muszyńska-Zygmańska, *Wielkopolska w powstaniu kościuszkowskim*,
Nakładem Głównego Komitetu Kościuszkowskiego w Krakowie, Poznań 1947.

## How it came in (2026-10-31)

The editor supplied the Polish transcription
(`wielkopolska-w-powstaniu-kosciuszkowskim-1947.md`, with page marks
`[7] <!-- p.7 -->`) and an AI-made English translation. The translation was
audited whole against the Polish before it was brought in: all 411 body
paragraphs and all 521 notes were read, and the corrections are recorded in the
translation package's `qa/issue-log.csv` (87 findings: 3 S1, 23 S2, 61 S3; 68
fixed, 15 source notes, 3 author queries, 1 rejected). This is stronger than
the spot check the literature normally gets; the English in `english.md` is the
corrected text, not the first draft.

The translation package is outside the repository. Its source file, the
corrected English, the termbase and the QA reports were used; nothing of the
package's intermediate drafts is kept here.

## The text

- **What is here:** the front matter (title pages, colophon, contents), the
  five chapters (pp. 7–154) and the notes. The bibliography (pp. 178–181), the
  index (pp. 182–188) and the errata (p. 189) are apparatus and are not cut
  into passages; the translation package holds them corrected, and the
  bibliography and index are not part of the argument. This follows the
  treatment of a work's endnotes in Frost (2007): the notes are the book's own
  argument, the apparatus is not.
- **Page marks:** `[N] <!-- p.N -->`, the transcription's own marks. The
  English carries the same marks; the build pairs the two and reports every
  page found in one language only (none).
- **The notes** are one passage, keyed `notes` (`## Przypisy` / `## Notes`).
  The print's notes pages 155–177 carry no page marks in the transcription, so
  they cannot be cut page by page; a note is cited by its number, not by a
  page.
- **The four illustrations** of the print (Kościuszko, Dąbrowski, Madaliński,
  Székely) are not in the package. Their captions stand as text; the image
  links are dropped so the site has no broken files.
- **150 passages:** the front, pp. 7–154, and the notes. Every numbered page
  is present in both languages.
- The transcription's own slips and the print's errata are handled in the
  translation: the errata are applied where they have an English effect (see
  the package's `qa/reports/errata.md`), and the print's oddities (the folio
  digits caught in the text, the duplicated `z` at pp. 19/20, the missing
  parenthesis in n. 17) are resolved in the English and recorded there.

## The English

Claude's, made from the Polish and corrected in the bilingual QA pass of
2026-10-31. The terminology is the translation package's termbase (Greater
Poland, voivodeship, district, Commission of Order, Regierung, Landrat and the
rest); the full decisions are in its `termbase.md` and `qa/decisions.md`, not
repeated here. The English keeps the author's long periodic sentences and her
plain judgements; it does not modernise the argument.

## How it bears on the edition

The book is the setting, not a source about Trąbczyn: it does not name the
estate or the Hohenlohe family. It gives the Prussian province of South Prussia
from the Second Partition to the aftermath of 1794 — the administration the
edition's documents come from, the insurrection in Greater Poland, Dąbrowski's
expedition, the Prussian trials, sequestrations, fines and reforms. It is the
context for the South Prussian files, the Landrat and Chamber vocabulary, the
1794 rising and the post-1794 prosecutions that the edition's letters touch.
Searches for people and places in it will find the edition's official world,
not its estate.

## On the site

Published in full at the editor's word (2026-11-01): `visible: true`, the text
on the site like any other work, with the English first and a button for the
Polish. The book is of 1947; the rights remain the editor's responsibility.
The detailed summary in `work.yml` is kept as metadata, not shown in place of
the text.

The literature index found 269 hits of the edition's people and places in the
work; 243 stand after the false friends were ruled out. Every pair was read;
26 pairs (68 hits) were new and were ruled in `literature/index.yml`, and
false friends were ruled out — among them the Silesian minister Danckelmann
(not the edition's vice-president), the Prussian general Lichnowski (not the
creditors), Jacek Małachowski (not Stanisław), Colonel Pirch of 1794 (not Major
von Pirch of 1809), Kamionna on the Bzura (not the estate), the Silesian
Oleśnica and the town Świecie (not the estate Święcia), and the surnames
Kaliszowski, Łukomski and Rogaliński. `--check` passes with no unruled hit.

## What was not done

- No hand-made links: the book names none of the edition's people, estates or
  holdings, so there is nothing to tie a passage to a document.
- The apparatus (bibliography, index, errata) is not cut into passages; the
  translation package holds it, corrected, if it is wanted later.
