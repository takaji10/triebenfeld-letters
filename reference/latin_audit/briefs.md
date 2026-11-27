# The Latin audit: the readers' briefs

The desktop session gives these to its Sonnet readers (docs/LATIN_AUDIT_PLAN.md, section 4), one holding
at a time, with the placeholders filled. Both readers write files only and never commit. Claude settles
what they find.

## The led reader (reader A)

> You are checking a transcription of an eighteenth-century Latin entry from a court book of Greater
> Poland ({REF}, the {COURT}) against photographs of the page. The photographs are cut into overlapping
> bands, top to bottom: {STRIP_FILES} (and `{PAGE}_whole.jpg` for the whole page, to find the entry).
> Open every band file one by one. At the end, list any you did not open.
>
> The transcription of the entry on this page, line by line, is:
>
> ```
> {TRANSCRIPTION}
> ```
>
> Compare it with the page word by word. Report every place where the letters on the page differ from the
> transcription, including:
> - words or lines the transcription skipped;
> - words written above the line or in the margin and marked for insertion (crosses, carets), and where
>   they go;
> - struck-out words (these are not transcribed: report them only if the transcription has them);
> - every mark of doubt in the transcription (`[?]`, `[word?]`, `[...]`): what the page shows there;
> - every word with a tilde (`~`): the letters on the page, and whether a stroke or a superscript shows
>   more letters than the transcription has.
>
> The standard. A reading changes only when something proves it: the letters on the page; a fixed
> formula; the same word written plainly elsewhere; a sentence with exactly one grammatical reading. A
> correction argued from grammar or sense alone is not a correction: report it as a question. The clerk's
> spelling stays as written (no "tidying": *Calissien~*, *Trąmpczyn*, *haeredi*). A word that cannot be
> read is not completed.
>
> Look-alikes to watch: the stylised p of *per*, *pro* and *prae*; *-que* written as q with a stroke;
> *c* and *t*; *u* and *n*; long s and f; *ł* and *t*; Roman numerals and figures.
>
> Write `{OUT}/reader_a.json`: a list of {"page_id", "line" (number in the transcription, or "after N"
> for a skipped line), "transcribed", "page_shows", "kind" (one of: misread, omission, insertion, struck,
> doubt_settled, doubt_stands, tilde, question), "strip" (the band file), "certainty" (sure / likely /
> unsure), "why"}. Then a line {"unopened": [files]}.

## The blind reader (reader B)

> You are reading parts of a page of an eighteenth-century Latin court book of Greater Poland ({REF})
> from photographs. You are not given the transcription. For each item below, read on the named band
> what the page has at the place described, letter by letter, and say how sure you are. Where a word is
> abbreviated, give the letters as written (with ~ for a stroke) and, separately, the full word if the
> letters fix it.
>
> {ITEMS}
>
> (Each item: the band file, the line's first and last words as a guide to the place, and the word
> asked about, given only by its position, never by the reading under question.)
>
> Write `{OUT}/reader_b.json`: a list of {"item", "page_shows", "full", "certainty", "why"}.

## What Claude does with them

- Where A and B agree and the page proves it: a row in `units/<slug>/intake/latin_audit.json` (`ROWS`).
- Where they disagree, or the case rests on grammar or sense: a row in `review/latin_audit/questions.csv`
  with a tight crop (for the one spot sheet at the end).
- A tilde form: the certain expansions prepared in the cloud (`reference/latin_audit/expansions.json`,
  plan section 3) go in `EXPAND`, unless the page shows letters that change them.
