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
- **The editor's answers on Oe 1 Bü 9454** (2026-11-23): a postscript
  written beside the closing moves too, after the signature and the date
  (41 letters; `ps:` in the entry, `plan_move_ps`, which moves any blocks and
  sets a row wherever a line's neighbour changed); the dates before a bare
  signature in Triebenfeld's notes move (17), the official papers stay (74a,
  74c, 74d, 252, 264). Letter 217's date and address moved together. Letter
  179 left (a line mixes postscript and closing). Letter 104 needed a place
  override. English: a Sonnet drafter, 54 and 292 by hand, every one read.
- **The other holdings** (2026-11-23): 144 documents in 30 holdings read by
  the Sonnet reader (91 official papers, 18 no case, 27 proposed moves, 8
  unsure) and by Claude, who applied the editor's two answers together: a
  date that breaks a closing (between the salutation or closing formula and
  the signature) moves, whoever wrote the letter; a date directly before a
  bare signature in an official paper stays (as Hardenberg's 252 did). 17
  moved: APŁ 1333 nos. 3, 4, 6 (Miączyński; the colonists' petition, whose
  date stood inside the signature block, before "w Imieniu Ogółu —"); Nr.
  3705 no. 1; Nr. 3709 nos. 5, 6, 11, 14, 15; Nr. 12765 nos. 4, 6, 8, 19;
  Oe 1 Bü 14525 nos. 36, 38, 41; Oe 1 Bü 14526 no. 27. Left: the ministers'
  and offices' letters (1414/1, 1414/3, 3132/1-3, 5, 8, 12366/5, 12765/3, 5,
  14, 25, 27, 30, 14525/32); 12765/12 and 13 (no signature); 14525/33 (the
  date shares its line with the text). The stale lists were taken first and
  are unchanged. English: 6 drafted mechanically, 11 by the drafter (two
  added full stops taken out), each read.
- Earlier "Next": the other holdings (the scan's counts: Oe 1 Bü 14525 52 cases,
  Nr. 12765 28, Nr. 3709 19, Oe 1 Bü 14526 19, and fewer elsewhere), after
  the editor's answer on the postscripts.

Paid runs: none.
