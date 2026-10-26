# 53/968/0/-/782

One document: the contract of 14 March 1820 between the village board of
Tropiczyner Holland and the school teacher Samuel Adolph of Borwiezer
Holland, two photographed pages (Image00002, Image00003), German throughout.
The editor's own transcription, kept as written.

## Provenance

Archiwum Państwowe w Poznaniu (APP), fond Albert Breyer - spuścizna. The
unit number is 53/968/0/-/782; the archive's title is "Umowa zawarta między
nauczycielem Samuelem Adolphem 1820". Two archival scans, each a page
photographed whole (no fold, no two-up opening), copied by
`intake/build_pages.py` into `processed/` as Image0002_a and Image0003_a.
Image00001 is the title page of the holding and is left out (the editor,
2026-10-25).

## Transcription

The editor's own reading, given by paragraph in their file (`Umowa zawarta
między nauczycielem Samuelem.md` on J:) and kept as written - the phonetic
spellings and the slips stand (Freihe wohnung, Ale hohe Pfest-Tage,
veroblogiert, Begräbniß). The lines here follow the manuscript's own lines,
laid out in session against the two images: a matter of layout only, no
reading changed. The editor's word was that the file's line breaks are
paragraph-level, so the layout was read from the pages (an OCR pass over
both pages for the line scaffold, then a line-by-line read of both). A word
the manuscript divides at a line end keeps its hyphen (auszu-/nehmen,
stel-/ten, Vo-/cation), as in the sibling holdings 545 and 669; the build's
line-break pass joins all three (high confidence, DWDS-attested or in this
corpus). The export's escaping backslashes were stripped as a file artifact;
the double space in "6 gr.  pohl." was closed with it.

The editor ruled, before the spot sheet: item 7 of the terms stands with its
number and nothing after it (the file's "[empty]" mark resolved); item 9
opens with the ordinal "9te." (the file's "[h/ti?]" resolved as "te").

The line division went to the editor on the spot sheet
(`intake/spot_sheet1.py`, answers in `review/app539680782/lines_answers.json`,
2026-10-25), and every row is answered. The editor's rulings:

- the opening paragraph and term 3 divide as the session had drafted them;
- term 9 breaks after "Ostern" and after "Wirt" (not after "Weinachten" and
  "einem" as drafted): "9te. Ale hohe Pfest-Tage als Weinachten Ostern /
  Pfingsten bekommt er von einem jeden Wirt / ein Opfertorium vom Wirthe
  6 gl.";
- term 10 breaks after "und": "10. Erhält derselbe einen Neujahrsumgang und /
  grünen Donnerstag Neujahr 6 gr. pohl. gründon 3 gr. pohl";
- the closing sentence has no break after "Sontags": its third line runs
  "Mann fortzusetzen. Die Sontags Schule so wie";
- the board's last line breaks before "wir": "treulich gegen den Mann zu
  erfüllen worauf / wir uns Eigen-händig Unter-schrieben.", with "Eigen-
  händig" and "Unter-schrieben" keeping their hyphens as drafted;
- the foot of the second page, which the session had taken for a pencil
  inscription, is blank paper - the editor read the region on the sheet and
  there is nothing to transcribe.

Applied to the page files and rebuilt; the paragraph decisions carry the
closing sentence, the board's sentence and the signature block as hand-set
breaks. A trap worth the record: a hand row whose context contains a comma
("Johann George Lindner, Schulz.") must carry the field quoted in
`paragraph_decisions.csv`, or `resolve_paragraphs.py` reads the context short
of the comma and drops the row as "not found again".

## Quirks worth knowing

- The ten terms are numbered 1. to 10. in the manuscript; item 9 is the
  ordinal "9te.".
- Item 7 carries its number and nothing else.
- "pohl." after a sum (term 10) marks Polish money; the sums of terms 4, 5
  and 10 carry no currency word of their own.
- The signature titles are as written: "Schulz." (the Schulze Johann George
  Lindner), "beisitzer" (Christoph Rimpel), "gerichten" (Samuel Gellert) -
  what office the last names is not clear.
- "Tropiczyner Holl." (the dateline) and "Borwiezer Holland" (the teacher's
  home) keep the manuscript's spellings; identifications open
  (NEEDS_CONFIRMATION). The canon records "Trąbczyner Holländ" as a variant
  of Łazińsk; the contract's spelling is one more form of it, probably.

## Damage

None recorded. The pages are whole; the writing is firm throughout.

## Where the line division stands

The layout was read from the images and then ruled by the editor on the spot
sheet (see "Transcription" above): every division is now the editor's. The
session's two false readings are worth the record: the marks at the foot of
the second page, which the session took for a pencil inscription, are blank
paper (the editor, on the sheet); and the closing sentence runs
"Mann fortzusetzen. Die Sontags Schule so wie" on one line, wider than the
session's draft had it.

## Translation and summary

No paid run (the editor's word, for a two-page document). The English was
written in session under translate.py's rules - the termbase (Morgen kept,
Schulze the village mayor, Holländ a place kept as spelled), the numbers
rule, the names rule - and written into the translation cache by
`intake/translation/write_cache.py`, so the checks and the publish read it
exactly as a paid run's. `check_translations.py` raises no row. The garbled
stretches are kept or bracketed, never guessed: "an ihm einen gefallen
fragen" (evidently Gefallen fanden), "nach seinen ohnentgeltlich", the
doubled "vom Wirthe" of term 9, "gründon" (Grünen Donnerstag), "pohl."
(Polish), "veroblogiert" (verobligiert), "gerichten". Whether term 9's
"6 gl." is gulden is open (NEEDS_CONFIRMATION, "Translations"): the standing
english_forms rule rewrites "gl." after a figure to Groschen.

The summary was written in English and German in session; its 18 statements
were claim-checked in session (`intake/claim_check.yml`), all supported
after one corrected in the draft (the one-year term belongs to the contract
the board issues, not to the teacher's obligation).

## What the holding owes the site

- `about.md`/`process.md` and their German, written in session.
- `rulings.yml`: doc_type contract, language de, the date read from the
  dateline, place of writing left empty (the identification open), estates
  trabczyn.
- No correspondents (a contract is not a letter; the sibling 783 records
  none). The four men are not profiled people: the sibling's 97 colonists
  are not either. A person page for Samuel Adolph is offered, not made.
- The glossary gate passes; the single-document terms are offered on the
  spot sheet's report (NEEDS_CONFIRMATION, "Glossary").
- The edition guide's counts and the APP list updated, both languages.
- Timeline: no event added - the contract bears on the colony's school, not
  directly on the estate's owner; offered to the editor.
- The era is `restitution`, proposed in the plan the editor approved; the
  restitution era's essay does not name the holding yet (offered).
