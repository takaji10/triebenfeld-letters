# Oe 1 Bü 9454

318 documents, 869 manuscript pages, 1798 to 1816. The backbone of the edition.

## Provenance

Hohenloher Zentralarchiv Neuenstein. 549 archival scans, each a two-up photograph of
one or two document sides. Cropped to 872 single pages by `crop_scans.py`, with the
bifolium cases split again by `split_spreads.py`.

## Transcription

Machine-transcribed from Kurrentschrift, not by a human palaeographer. That shapes every
editorial decision in `rulings.yml`: the failure mode is plausible German that is not what
is on the page, so readings that could not be settled from evidence were left alone rather
than guessed at.

## Quirks worth knowing

- **The archive's numbering is not chronological.** Letters 1 to 74 are a jumbled block
  spanning 1806 to 1815; 75 to 301 run in order from 1798. Numbers 302 and 303 sit outside
  the sequence.
- **Several archival numbers hold more than one document**, split into sub-records: 72 into
  72a to 72f, 74 into 74a to 74e, and so on. Each keeps a link back to its parent.
- **Three documents survive in two copies**: 48 and 302 are the same letter of 7 March 1809
  transcribed twice, as are 72d/72e (German and Polish) and 118b/118c. The duplicate pairs
  are the only place in the corpus where two independent transcriptions of one page can be
  compared, which is what makes them valuable.
- **One financial figure differs between the two copies** of the 7 March 1809 letter,
  23,000 against 32,000 Rthl. Both are faithful to their own page, so the discrepancy
  belongs to the original copyist.
- **Letter 72e is Polish and 283 is French.** Everything else is German.
- **Four archival numbers have no surviving text**: 121, 181, 225, 293.
- **150 uncertain readings** stand marked in the text, 98 illegible and 52 offered as
  guesses.
- **Letter 48's two page-image pairings were never human-confirmed.** They are
  `status=auto, confidence=check` in the scan map, and 48 is the corpus's accuracy
  benchmark, so it is worth an eye.

## Damage

Five passages are damaged. Their line ranges are in `rulings.yml` under `damage`, and the
loader now validates each against the corpus line count. Two of the five ranges that had
been hardcoded in `build_db.py` pointed past the end of the file, which is why `has_damage`
was false for every record until this was fixed.
