# Editorial rules

What gets changed in a transcription, what does not, and who decides.

These are the bars a proposed correction has to clear. They exist so that
adjudication is the same in January and in June, on the letters and on the
deeds, and so that the editor is asked only about what the rules genuinely
cannot settle. Every one of them was arrived at by making the decision once and
writing down the reason.

The governing principle, from which the rest follows:

> **Transcribe what the page says, not what it ought to say.** A visibly
> doubtful reading is a better outcome than a confident wrong one. Where
> evidence cannot settle a reading, it is left alone rather than guessed at.

---

## What may be corrected without asking

A proposal is applied when the transcribed form is demonstrably not a word, and
the proposed reading is pinned by something other than plausibility:

| the evidence | example |
|---|---|
| the corpus knows the word and not the transcription — a hapax against a form attested three times or more | `berahlen` → `bezahlen` (173 occurrences) |
| the same instrument spells it correctly elsewhere | `Hypotheken Kuche` → `Buche`, as page 9 has it |
| a fixed chancery or legal formula | `maßen könntet` → `folgendermaßen lautet` |
| a word broken across a line and mended on the wrong half | `ver-/abgerüdeter` → `ver-/abredeter` |
| the parallel clause in a twin document | `in eine Bonification` → `nie eine`, as the duplicate reads |
| a numbered run that must be sequential | `§XIII, §IV, §XV` → the middle is `§XIV` |

Two constraints on all of these. The change must be **one slip**, not a
reading: a proposal further than about 0.6 similarity from what stands on the
page is a guess at a corrupt word, however right it may be in sense
(`Früffrichter` → `Erbpächter` is refused, and is probably correct). And it must
be **word for word**: a proposal that adds or drops words is restructuring the
sentence, which is an editorial act.

## What is never changed without the editor

- **Place names that are simply garbled.** The editor's ruling: a mangled
  place-form is usually transcription damage, not a different place -
  `Traperiner` is Trąbcziner, `Wun` is Wien, `Owringen` is Öhringen, `Königubern`
  is Königsberg. Where the proposed form is a place the canon already knows,
  correct it. The one exception is the exception that matters: a change that
  moves a reading between **Trąbczyn, Wrąbczyn and Wrąbczynek** alters which
  village is meant, and only the editor makes it.

- **Names.** Of people and of places. `Wittowes`, `Breschlau`, `Marianton`,
  `Rzadkowski` stay as written. A name silently improved destroys the evidence
  that the reading was wrong, and place-name variants are frequently the whole
  question: **Wrąbczyn, Wrąbczynek and Trąbczyn are three different villages.**
  The exception the editor has granted: where the *same instrument* spells the
  name another way, the internal witness settles it — Greust signs *Gneust*,
  Chmura signs *Chmara*, Glenth is *Glenck* on page 1.
- **Figures.** Never re-derived, only read. A sum that reads 23000 in the German
  reads 23000 in the English, even where the arithmetic of the surrounding
  schedule says otherwise. A figure reached by calculation — "five per half-year
  implies ten annually" — is a finding, not a correction.
- **Abbreviations.** `Mund: 22 gg.` in a fee table, `JJWW`, `Rzplity`, `c. a.`
  are the scribe's own. Expanding one is reading something off the page that
  nobody read.
- **Diacritics and orthography in Polish and Latin.** `Rzadkowski` without its
  nasal may be exactly what the page carries; `sub paena executiones` is
  chancery Latin as written.
- **Grammar.** Case endings, agreement, tense. `eine Vergleich` for `einen`
  changes nothing a reader needs and asserts a letterform nobody saw.
- **Anything that reverses meaning on an inference.** `verboten` → `gebothen` in
  the clause about Polish protocols would rewrite what the parties asked for.
  Such a discrepancy is usually worth more than the fix.
- **Watch-list confusions.** `Anweisung`/`Abweisung`, `committirt`/`exmittirt`.
  The whole checking apparatus exists to *not* decide these mechanically.

## Where the line falls on marks

Marks of doubt are evidence and are never quietly removed. Applying a fix that
would delete a `[?]`, `[word?]` or `[...]` needs the editor. The marker total is
checked before and after every pass for exactly this reason.

A section mark misread as `5` is corrected to `§`, because `5` is not a section
mark and occurs once. A section mark rendered `S.` is left, because it recurs
across documents and reads as a transcription convention rather than a slip.

## Who proposes, who decides

Proposals come from the translator: rendering a document is the most thorough
reading it ever gets, and it reports what it could not make sense of. Those
reports are mined by `pipeline/review/transcription_fixes.py`, which anchors
each to a page id and a corpus line, and by
`pipeline/review/unmarked_doubts.py`, which finds the places where the English
admits doubt and the German does not.

The model then rules on everything the bars above can settle and records **why**
each remaining row needs a person — a name, a figure, a reading rather than a
slip. The editor sees that shorter sheet, not the raw one. On 14526 that was 478
proposals reduced to about 90 real questions.

Rulings live in `units/<slug>/transcription_decisions.csv`, which is **tracked
and authored** — not in `review/`, which is generated and git-ignored. A ruling
survives every rebuild of the sheet, and is keyed on what the row says rather
than where it sits.

## Rulings the editor has given, standing until withdrawn

- A document is one **package**: an instrument together with the enclosures
  filed with it. Do not sub-divide into one record per enclosure.
- **Paragraph breaks** are visible on the page: a line noticeably shorter than
  the page's own median ends a paragraph.
- **Section numbering runs in sequence.** A number that breaks the run is a
  machine misreading of the numeral, not a scribe's lapse.
- Some German documents carry a few lines of **Polish**, and they are source
  text: translate them, do not treat them as corrupt German.
- `Tromczin` is **Trąbczyn**.
- Standardise `Głazewo`; standardise the Trąbczyn spellings; leave Wrąbczyn and
  Wrąbczynek alone.
