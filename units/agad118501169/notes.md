# 1/185/0/1/169

One document: the report of the Commission of Instruction on the Weigel/
Miączyńska conflict of jurisdiction, dated at the session of 28 October
1834 (final page) and signed by the commission's president, Faltz. 42
manuscript pages, pencil-numbered 157-198, plus the blank p. 199; the
pages run 1800 back-story to 1834, the report itself of 1834.

## Provenance

Archiwum Główne Akt Dawnych, Warszawa (AGAD), fond II Rada Stanu
Królestwa Polskiego. 22 scans arrived with the export; 22 are mapped, the
one scan per opening for the 22 openings pages 156|157 through 198|199 -
156 and 199 being the two halves that are not ours (156 is the preceding
file's matter, 199 blank) and are cut into processed/_not_staged/. Scan
98320273 is a re-photograph of the opening 170|171 already carried
by 98320272 - same pages written out identically, different files (MD5s),
so not a corruption pair - and sits in `raw_dir/duplicates/`, excluded
whole.

The pages are cut by `intake/holding.py` (courtbook.cut) straight out of
the raw scans, each half ±30px of overlap round the fold; the fold page
the editor reviews the splits on is `review/<slug>/folds/index.html`
(courtbook.fold_sheet: fold line, sheet turning, page edges). The fold
proposals in holding.py are the split detector's first cuts, all high
confidence; the editor's placements (intake/folds.json via
`python pipeline/intake/courtbook.py folds agad118501169 <file>`)
override them.

## Transcription

Not transcribed from the scans: the archive supplied its own transcript
(`(French).md` in the download folder) and its English translation, both
per page with [p. N] marks. The corpus is that transcript, page by page,
with four rulings of the editor (2026-10-21):

1. p. 157 heading: heavily corrected in the manuscript and transcribed as
   the transcript gives it, garbles included ("par a Tribunal Suprème",
   "en vertu daquelle", "rayée l'hypotheque"). Not repaired.
2. Block A - the passage on the Hohenlohe action of 1808 before the
   Tribunal of Kalisz, which the transcript jumps from "…l'inscription
   de ladite somme sur son nom." to "En 1810 le dit Weigel intenta…" - is
   plain manuscript text and is restored on p. 159 from the scan reading
   (rec. in `review/agad118501169/split_proposal.md` § 5).
3. The manuscript's crossed-out passages are NOT recorded: block C ("Le
   Tribunal ayant pris en considération qu'il ne s'agissait plus ici …
   s'est reconnu compétent.") and the lead "En statuant ensuite sur le
   fond et considérant :" on p. 160 are struck in the manuscript. What
   survives flows "Le Tribunal ayant pris en considération: 1° que dans
   l'affaire…", block C's opening line being the one line of p. 159
   beyond "…de 30.000 écus." The archive transcript kept the struck
   "En statuant ensuite sur le fond et considérant ;" its [p. 160] bloc
   therefore starts with a line the corpus does not carry, and the
   supplied English translation needs the same adjustment at the
   [159]/[160] fold when it is imported.
4. p. 199 (blank) is not published; the page run ends at 198.

Excepting these, the transcript's [p. N] cuts fall on the manuscript's
own page breaks, checked against every scan; carry words at the folds
make the pairing self-proving (table in the split proposal).

The English translation is the archive's own, imported per page
(`intake/translation/`); the editor approved import with an accuracy check
against the French, skipping the archive's translator notes (21) and
glossary (31).

## Quirks worth knowing

- Documents in the folder name pages "Michalina Miaczynska" in ASCII, but
  the folder's own name carries ą; the raw_dir path must keep the
  diacritics. Tools that choke on them read the paths copied under
  `C:\Users\Tersnaus\AppData\Local\Temp\opencode\agad118501169_src\`.
- The report's numbering: 1°-4° (three runs of four: the Tribunal's
  grounds, the Supreme Tribunal's grounds, the four conditions of a
  conflict), a°-c° (the Finance Commission's arguments), ad a. / ad b. /
  ad c. as the Instruction Commission's counters.
- The transcript's French spacing before punctuation ("considérant :")
  is the archive's and is kept.
- The year of the struck-out judgment in the heading is bracketed [1829]
  in the archive transcript itself.

## Damage

None recorded beyond the correcting/editing on the heading page: the
manuscript's title block reads heavily edited, which the transcript
reflects. The document otherwise reads in a fair hand.

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

The report is in French, the working language of the Kingdom's central bodies, in the administrative prose of the period: long sentences, grounds numbered 1° to 4° and 1° to 5°, arguments lettered a° to c° and answered ad a., ad b., ad c. The heading on the first page is heavily corrected in the manuscript. A passage on p. 160, a first draft of the grounds, is struck out with a line through it; crossed-out text is not recorded. A passage on p. 159, on the Hohenlohe action of 1808, which the archive's transcript skips, is restored from the scan.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The archive's export holds 22 photographs. Twenty-one show an opening of the bound report, two pages at a time, photographed with the fold in the middle; one more shows the opening whose right side is the report's first page (the left side belongs to the preceding file of the archive). One scan is a second exposure of an opening already among them, with the same pages written out identically; it is set aside. The blank last page and the preceding file's page were not published. Each opening was cut at the fold into two page images, on a review page on which the fold line of every opening was checked and, where a fold was photographed at a slant, the sheet turned until the cut ran along it. <!-- context -->

### Transcription

The archive supplied its own transcript of the report, in French, page by page, and the text is taken from that transcript. Every page of it was read against the scan before anything was built. Two departures from the transcript, both on the editor's ruling: the passage on p. 159 on the Hohenlohe action of 1808, which the transcript skips, is restored from the scan. The passages crossed out on p. 160 are not recorded, so the text runs from the end of p. 159 (the Tribunal, having taken into consideration:) straight into the numbered grounds. The corrected heading of p. 157 is kept
as the transcript reads it, slips and all. <!-- context -->

### The English

The English is the archive's own translation, imported page for page, and read against the French. It is accurate; where the source's own grammar or spelling slips, the translation renders the sense and the transcription keeps the slip. The one passage the transcript skips is translated here. The archive translator's notes and glossary are not carried over. <!-- context -->

### Date

The report carries its date in the closing formula: done at the session of the Commission of Instruction, Warsaw, 28 October 1834. <!-- context -->
