# A full audit of the Latin transcriptions - the plan

The editor, 2026-11-27: "perhaps this is the right time to do a full audit of the Latin on the site to
fix and identify any transcription errors, and to resolve any ~ or similar marks as best as you can. Can
you make a plan for this that also determines if any summaries or texts (e.g. Eras) would need to be
amended based on the corrections?"

Nothing is done yet. Section 8 holds the questions for the editor.

## 1. What is in scope (counted 2026-11-27)

Every document whose language is Latin (rulings.yml `documents.language`, or the holding's first
language), except the Kodeks:

| Holding | Docs | Pages | Words | ~ forms | Marks of doubt | Checked so far |
|---|---|---|---|---|---|---|
| Poznań Gr.1181 (app5320pozgr1181) | 1 | 14 | 5,548 | 157 | 355 | light; a spot sheet of 61 rows is still open |
| Konin Gr.118 | 29 | 40 | 4,731 | 286 | 20 | full (2026-10-07) |
| Konin Gr.117 | 13 | 19 | 4,267 | 138 | 47 | full |
| Konin Gr.153 | 2 | 26 | 4,940 | 0 | 1 | full |
| Konin Gr.119 | 8 | 10 | 1,447 | 147 | 10 | full |
| Konin Gr.115 | 10 | 11 | 1,291 | 13 | 2 | light |
| Konin Gr.116 | 12 | 15 | 804 | 16 | 20 | full |
| Konin Gr.114, 120, 121, 136 | 6 | 13 | 2,070 | 19 | 6 | light |
| Kalisz Gr.414, 424, 425 | 3 | 8 | 1,065 | 11 | 4 | light |
| Land court of Konin 53/6/0/-/17, 36, 40, 45, 46, 47 | 8 | 18 | 2,924 | 49 | 8 | 47 full, the rest light |
| Land court of Kalisz 53/4/0/-/62 | 1 | 1 | 51 | 3 | 3 | light |
| Pyzdry Gr.75 | 1 | 2 | 352 | 1 | 12 | full (2026-11-26) |
| Ląd copy-book 53/1455/0/2/21 | 6 | 9 | 2,198 | 0 | 22 | light |
| Oe 1 Bü 14526, the Latin deed | 1 | 5 | 965 | 0 | 0 | light |
| **Total** | **101** | **191** | **32,653** | **840** | **510** | |

**Out of scope:**
- **The Kodeks Dyplomatyczny Wielkopolski** (31 documents, 12,620 words): printed text, taken from
  the editor's file and never corrected (units/kdw/notes.md). The WBC has no page images.
- **The Polish documents and the Polish passages**: these are a later audit, as the reading guide puts
  the Polish second.

## 2. The standard (unchanged; NEW_UNIT 3a, EDITORIAL_RULES)

A reading changes only when something proves it:
- the letters on the page;
- a fixed formula;
- the same word written plainly elsewhere;
- a sentence with exactly one grammatical reading;
- a settled form.

Since 2026-11-26 two further rules apply:
- **A correction argued from grammar or sense alone goes to the editor**, not into the text. Claude's
  *hasce* for *hisce* and *hac ... recognitione* for *haec ... recog~tioni* in Pyzdry Gr.75 were wrong.
- **An omission or a placing shown by the page itself** (words a line skipped, the crosses of an
  insertion) is a correction. This audit should find these first.

A word that cannot be read is not completed. Struck words are left out. The scribe's spelling stays.

## 3. The tilde forms and the other marks

**What the rule says.** The editor's ruling of 2026-11-22, confirmed for Pyzdry Gr.75 on 2026-11-26:
abbreviations are expanded in square brackets **where certain**. Certainty comes from the document
itself, a witness, or the one possible sense. Where the expansion is not certain, the abbreviation stands
as written and the possibility goes in the holding's `intake/unresolved.md`.

**What exists already.** All 816 tilde occurrences of the court books are expanded by case, with the
reason for each, in `reference/guide/abbreviations_expanded.yml`: 588 sure and 228 not. This is the
draft. Claude checks every sure one against its own sentence before it is applied. The unsure ones stay
as written, unless the audit's reading of the page settles them.

**The form of the brackets needs the editor's ruling** (section 8, question 1). The tilde stands in
three kinds of place:
- **after a stem:** *Calissien~* would become *Calissien[sibus]*;
- **inside a word:** *Cond~nis* would become *Cond[escensio]nis*, as *recog[ni]tioni* in Pyzdry Gr.75;
- **after a doubled consonant that marks the plural:** for *Citt~* (*Citationes*), either *Cit[ationes]*,
  dropping the clerk's second t, or *Citt[ationes]*, keeping it.

**Other marks:**
- **The 510 marks of doubt** (`[?]`, `[word?]`, `[...]`) are each read again on the page. A doubt the
  page settles is removed. The rest stand.
- **Superscripts and the strokes on p and q** are looked at where they decide a reading: per, pro or
  prae; -que.

## 4. The method, holding by holding (sub-agents first)

1. **Strips.** A script cuts every page image into overlapping strips at 2x, from the site's page images
   (`site/assets/scans/`). These are the web copies, 1,100 pixels wide, which were enough for Pyzdry
   Gr.75. Where a line cannot be read on them, the page goes on a list for the editor's original scan.
2. **Two readers for each page** (WORKING_NOTES, "Sub-agents and token use"):
   - **A led reader (Sonnet)** compares the transcription with the strips, word by word. Its output is a
     table of differences, omissions, struck words and insertions, and it says which strips it did not
     open.
   - **A blind reader (Sonnet)** reads, unled, only the lines the first reader flagged, every mark of
     doubt, and every unsure tilde form.
   - **The brief** quotes the standard of section 2 word for word, names the termbase renderings, and
     names the strip files one by one. Both readers write files only, and never commit.
3. **Claude settles every finding on a crop.** What the page proves is applied. What rests on grammar or
   sense, or where the two readers disagree, goes to the spot sheet.
4. **The spot sheet** is the HTML form the editor uses (images as CSS backgrounds, no script; WORKING_NOTES),
   with a card per question. It covers a batch of holdings at a time.
5. **Applying the rulings** follows each holding's usual procedure. The corrections become rows in its
   `intake/holding.py` (`ROWS`), applied once and logged in `transcription_decisions.csv`. The graded list
   goes in `intake/changes.yml` (marked `new:`), so the page of changes shows the editor what moved.
6. **The tilde expansions** are applied in the same pass, as their own set of rows, so that a later reader
   can tell a correction from an expansion.

## 5. What else must change when the Latin changes (the impact sweep)

Every correction is checked for its effect on everything else written from that document. A script does
the finding; Claude reads and rewrites. The script, `pipeline/review/latin_impact.py`, is to be written;
for each changed document it lists:

| What may be affected | How it is found | What is done |
|---|---|---|
| **The English translation** | the changed passage, by page | The English is corrected where the meaning moved, in the holding's translation files or `reference/english_corrections.yml`, then `check_translations.py` and `publish_translations.py` run. An expansion alone changes no English unless it shows a case was misread. |
| **The summaries** (German and English) | every summary of a changed document whose figures, names, dates or places the change touches | The summary is corrected and claim-checked again; `check_unit_text.py` already holds figures to the documents. |
| **The holding's page** (`about.md`, `about_de.md`) | sentences citing the document (`[[n]]`) that contain the old word, name, figure or date | Rewritten, then audited by a second reader. |
| **The era essays** (`site/eras/`, `site/de/epochen/`) | links to the document (`/documents/<slug>/<n>/`) and the old wording | Rewritten where the fact moved. |
| **The timeline** (`site/_data/timeline.yml`) | events whose sources cite the document | The same. |
| **The connections** (`reference/connections.yml`) | notes on the document | The same. |
| **People and places** (`reference/people.yml`, `places.yml`, `genealogy.yml`, `people_bios.yml`) | a changed name or place form; each authority's matches counted before and after (`pattern_impact.py`) | Patterns and identities corrected. `zero_mentions.py` is re-run. |
| **Dates** (`rulings.yml` dates) | a changed date line, feast or figure | The date and its basis are corrected, with the German in `site_notes_de.yml`. |
| **The glossary** | a changed term | `glossary_candidates.py --check`, and the holding's rows of `glossary_matches.csv`. |
| **The reading guide** | Latin quoted from a changed document | The guide's quotation check (WORKING_NOTES, "The reading guide, chapter 3") is re-run, and quotations are corrected. |
| **The literature links and NEEDS_CONFIRMATION** | notes that quote the old reading | Corrected, or the question closed. |

The impact list for each batch is reported to the editor with the corrections, so the editor sees which
public texts changed and why.

## 6. Order of work

1. **A pilot holding: Konin Gr.115.** It has ten documents on eleven pages, had only the light check,
   and has few tilde forms. The pilot measures how much the two readers find, whether the web images are
   enough, and the cost in tokens. The editor sees one spot sheet and one impact list before the rest.
2. **The holdings checked lightly**, smallest first:
   - Konin Gr.114, 120, 121, 136;
   - Kalisz Gr.414, 424, 425;
   - the land court of Konin (53/6/0/-/17, 36, 40, 45, 46) and of Kalisz (53/4/0/-/62);
   - the Ląd copy-book;
   - the Latin deed of Oe 1 Bü 14526.
3. **Poznań Gr.1181**, after the editor has answered its open spot sheet of 61 rows (or folded into this
   audit, as the editor chooses): it has 355 marks of doubt and 14 pages.
4. **The holdings checked fully**: Konin Gr.116-119, 153 and 53/6/0/-/47. A lighter pass, for the marks
   of doubt, the tilde forms and words skipped, which the earlier checks did not look for in the same way.
5. **The impact sweep and the publishing**, batch by batch, each with a second reader's audit of any
   rewritten public prose before it is published.

## 7. The cost

No paid run is needed: the readers are sub-agents of the working session. Figures from the Gr.75 work:
two readers and Claude's settling took about an hour for two pages. The pilot will give the real rate.

## 8. Questions for the editor

1. **The form of an expansion.** For a word ending in a tilde, write *Calissien[sibus]*, with the tilde
   dropped and the supplied letters bracketed. For a doubled consonant, *Cit[ationes]* or *Citt[ationes]*?
   For a contraction, *Cond[escensio]nis*?
2. **Uncertain tilde forms.** Leave them with the tilde (the rule), or expand them with a doubt mark,
   e.g. *notificat[am?]*?
3. **The images.** Are the web copies enough for this audit? Where a line cannot be read on them, will
   you supply the original scan for that page?
4. **Poznań Gr.1181.** Answer its open spot sheet first, or let the audit take it over?
5. **The review.** One spot sheet per batch, as above, or everything held for one review at the end, as
   in the Prusimski-era run of October?
6. **Publishing.** May the corrected English, summaries and pages be published batch by batch, at your
   word each time?
