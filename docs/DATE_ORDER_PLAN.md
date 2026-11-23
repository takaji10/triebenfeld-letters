# The date after the signature (planned 2026-11-23)

## The problem

The editor transcribed many letters with the date where it stands on the page:
between the salutation of the closing and the rest of it.

    Ewr Hochfürstliche Durchlaucht
    Wien den 25ten Octobr.
    1814.
    treu gehorsamster Knecht
    v Triebenfeld

The reading text and the English then break the closing sentence with the date
("Your Most Serene Highness's Vienna, the 25th of October / 1814. / most
faithful and obedient servant"). A German reader puts the date after the
signature; the editor, who does not read German, kept the page's order. The
proper order:

    Ewr Hochfürstliche Durchlaucht
    treu gehorsamster Knecht
    v Triebenfeld
    Wien den 25ten Octobr.
    1814.

## The editor's rulings (2026-11-23)

1. Move the lines in the transcription itself. Where the text sits on the page
   is not important.
2. In the reading text and the English, a date written on two or three lines
   becomes one line ("Vienna, the 25th of October 1814.").
   In the English a place that stood on a line of its own takes a comma
   after it ("Trąbczyn, the 31st of March 1805"), as the other dates have
   (the editor's answer on the pilot).
3. Where a postscript follows the signature, the date goes directly after the
   signature, before the postscript.
4. **Text is only moved, never created.** No word is added, dropped or changed
   in the transcription, the reading text or the English; in the reading text
   and the English the date's lines may be joined into one. No pattern is
   assumed to hold because it held elsewhere: every case is read. Anything odd
   met on the way is flagged to the editor, not mended in passing.

## Method

1. **Find** (`pipeline/review/date_order.py`, free, reads only): every date
   among the last fifteen lines of a document that has text after it, sorted
   into *regular* (salutation, date, closing, signature on one page, nothing
   else between) and *irregular*; `review/date_order/candidates.md`. The first
   run: 465 cases in 392 documents, 96 regular. Most irregular ones are dates
   inside the text, which are not moved; others have two-line signatures,
   a hyphenated closing ("gehor¬ / samstes"), an office note after the
   signature, or a salutation that is only "Ewr".
2. **Read**: a Sonnet sub-agent reads every case from the text alone and says
   whether a date stands between closing and signature, which lines are the
   date, and after which line it goes. Claude compares its answers with the
   script's, settles each difference, and reads every irregular case himself.
   The decisions go into `units/<slug>/intake/date_order.yml`, one entry per
   document, with the date lines and the anchor line written out as they
   stand in corpus.txt.
3. **Move** (`date_order.py --move --unit <slug>`): per entry, the date lines
   are found by their exact text, and moved to directly after the anchor line.
   An entry is refused, and nothing of it written, if:
   - the lines are not found exactly once, or the anchor is not within a few
     lines after the date on the same page;
   - the lines before and after are not the same lines in a new order;
   - a hyphenated line, a line-break decision, a set-apart block (sideways,
     office, margin, hand notes, catchwords) or a recorded transcription
     decision touches the moved lines;
   - the page file under `transcriptions/` does not hold the same lines.

   The same move is made in the page file. The paragraph sheet gets held rows
   for the moved lines (the first closing line takes over the date's old link
   to the salutation; the date is one paragraph after the signature, its lines
   joined; every other decision as it was), cue `hand` so a re-run keeps them.
   The holding's `intake/changes.yml` lists every move for the page of changes.
4. **Check nothing else moved**: before and after the rebuild, every
   document's date, place, sender, recipient, pages, lines and marks of doubt
   are compared (`date_order.py --snapshot` / `--compare`); a difference stops
   the work until understood (the dating reads the last lines of a letter).
5. **The English**, without re-translating: one entry per page in
   `reference/english_corrections.yml` that moves the date in the English the
   same way. A check refuses an entry whose words, counted, differ between
   `find` and `replace`, and a page whose English then has a different number
   of paragraphs from the German. The cached translations' `source_hash` is
   restamped for the moved documents, so that `translate.py --stale` does not
   ask for a paid re-run of German whose words did not change.
6. Verify, look at the pages, commit holding by holding, publish at the
   editor's word.
7. Afterwards: the rule in EDITORIAL_RULES and NEW_UNIT.md, and a warning in
   the build for a new holding with a date between closing and signature.

## Steps

1. Pilot: Nr. 12765 document 1 and Oe 1 Bü 9454 letters 39, 76, 168
   (a postscript follows) and 182 (the date line has a time of day). The
   editor looks at them on the site before the rest is done.
2. The reading of every case (Sonnet, then Claude).
3. The moves, holding by holding, Oe 1 Bü 9454 first.

## Done

- Pilot (2026-11-23): 5 letters, approved by the editor.
- **Oe 1 Bü 9454** (2026-11-23): 253 documents read by the Sonnet reader and
  by Claude; 177 moved (97 where script and reader agreed exactly, the rest
  read case by case: an abbreviated salutation, other signers, a title line
  under the name, a date between closing formula and signature, a hyphenated
  closing word that moves as a pair, letter 151's year joined). English: 121
  corrections drafted by `date_order_english.py`, 56 by a Sonnet drafter,
  every one read by Claude; checked word for word, paragraph counts against
  the German, and a publish from the cache shown to give the same text.
  Left for the editor: NEEDS_CONFIRMATION, "The date after the signature".
- Tools: `date_order.py` (scan, move, snapshot/compare with the reading
  text's words, restamp), `date_order_sheet.py` (the reading sheet),
  `date_order_compare.py` / `date_order_oneline.py` (settling),
  `date_order_entries.py`, `date_order_english.py`, `date_order_add_english.py`,
  `date_order_verify.py`, `date_order_unstamp.py`.
- Next: the other holdings (the scan's counts: Oe 1 Bü 14525 52 cases,
  Nr. 12765 28, Nr. 3709 19, Oe 1 Bü 14526 19, and fewer elsewhere), after
  the editor's answer on the postscripts.

Paid runs: none.
