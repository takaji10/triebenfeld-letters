# A full audit of the Latin transcriptions - the plan

The editor, 2026-11-27: "perhaps this is the right time to do a full audit of the Latin on the site to
fix and identify any transcription errors, and to resolve any ~ or similar marks as best as you can. Can
you make a plan for this that also determines if any summaries or texts (e.g. Eras) would need to be
amended based on the corrections?"

**Status (2026-11-27): every holding read on the desktop the same day (Oe 1 Bü 14526 once the editor named where its scans are); the spot sheet answered by the editor and applied the same day (47 of 57; section 10), with the two rulings for all court books (routine forms stay written out; nothing dropped, the king's titles written out); the impact sweep done the same day (the English and the dating notes; reference/latin_audit/english_impact*.json).** The editor's answers are in section 8. The
audit is to be **run in a desktop session on the editor's PC**, where the original scans are; section 9
is the procedure for that session. A cloud session cannot do the reading: it has only the site's web
copies.

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
| Konin Gr.114 | 2026-11-27 | 2026-11-27: 2 corrections | 2026-11-27 |
| Konin Gr.120 | 2026-11-27 | 2026-11-27: 1 correction, 10 expansions | 2026-11-27 |
| Konin Gr.121 | 2026-11-27 | 2026-11-27: 4 corrections (one changes the English, after the review) | 2026-11-27 |
| Konin Gr.136 (the Latin record only) | 2026-11-27 | 2026-11-27: 2 corrections | 2026-11-27 |
| Kalisz Gr.414 | 2026-11-27 | 1 correction | 2026-11-27 |
| Kalisz Gr.424 | 2026-11-27 | 5 expansions | 2026-11-27 |
| Kalisz Gr.425 | 2026-11-27 | nothing to change in the Latin (one Polish reading, "kładamy", for the Polish audit) | 2026-11-27 |
| Land court of Konin 53/6/0/-/17, 36 | 2026-11-27 | nothing proved: the 1589 and 1644 hands read "unsure" throughout | 2026-11-27 |
| Land court of Konin 53/6/0/-/40 | 2026-11-27 | 1 correction | 2026-11-27 |
| Land court of Konin 53/6/0/-/45 | 2026-11-27 | 2 corrections | 2026-11-27 |
| Land court of Konin 53/6/0/-/46 | 2026-11-27 | 1 correction (a date: the 20th, not the 28th), 13 expansions | 2026-11-27 |
| Land court of Kalisz 53/4/0/-/62 | 2026-11-27 | 2 corrections | 2026-11-27 |
| The Ląd copy-book | 2026-11-27 | 5 doubts lifted | 2026-11-27 |
| Poznań Gr.1181 | 2026-11-27 | 75 corrections (a skipped line with 40,000 fp; three figures), 57 expansions, 53 questions (49 of the old sheet's rows) | 2026-11-27 |
| Konin Gr.116 (lighter pass) | 2026-11-27 | 4 corrections, 7 expansions | 2026-11-27 |
| Konin Gr.117 (lighter pass) | 2026-11-27 | 3 corrections, 76 expansions, 1 question; a dating note to correct (2 April 1778) | 2026-11-27 |
| Konin Gr.118 (lighter pass) | 2026-11-27 | 2 corrections, 171 expansions; the king's titles a general question | 2026-11-27 |
| Konin Gr.119 (lighter pass) | 2026-11-27 | 2 corrections, 80 expansions | 2026-11-27 |
| Konin Gr.153 (lighter pass) | 2026-11-27 | 2 corrections, 1 question | 2026-11-27 |
| Land court of Konin 53/6/0/-/47 (lighter pass) | 2026-11-27 | 23 expansions | 2026-11-27 |
| Oe 1 Bü 14526, the Latin deed | 1 | 5 | 965 | 0 | 0 | light |
| **Total** | **101** | **191** | **32,653** | **837** | **510** | |

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

**Prepared in the cloud (2026-11-27; section 11).** The 837 tilde forms were expanded twice,
independently, and the 451 that both readings give the same way with certainty are ready to apply
(`reference/latin_audit/expansions.json`). The rest keep their tilde unless the page settles them.

**The form of an expansion (the editor, 2026-11-27).** The tilde is dropped and the supplied letters
stand in square brackets, with no mark of doubt:
- **after a stem:** *Calissien~* becomes *Calissien[sibus]*;
- **inside a word:** *Cond~nis* becomes *Cond[escensio]nis*, as *recog[ni]tioni* in Pyzdry Gr.75;
- **a doubled consonant that marks the plural is written once:** *Citt~* becomes *Cit[ationes]* (the
  editor: "Cit[ationes]"), *praesen~* by the same rule as the case requires.

**An uncertain form keeps its tilde** (the editor, 2026-11-27: "Leave them with a tilde"): no
*notificat[am?]*. The possibilities go in the holding's `intake/unresolved.md`.

**Other marks:**
- **The 510 marks of doubt** (`[?]`, `[word?]`, `[...]`) are each read again on the page. A doubt the
  page settles is removed. The rest stand.
- **Superscripts and the strokes on p and q** are looked at where they decide a reading: per, pro or
  prae; -que.

## 4. The method, holding by holding (sub-agents first)

1. **Strips from the original scans** (the editor, 2026-11-27: run on the PC where the scans are). A
   script cuts every page into overlapping strips from the editor's original scan, turned and cut at the
   editor's folds (`intake/folds.json`), not from the 1,100-pixel web copies. Section 9 says where each
   holding's scans are.
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
4. **One spot sheet at the end** (the editor, 2026-11-27: "All at once"): the questions of every holding
   are gathered as the holdings are read, and the editor answers them in one review after the last holding,
   as in the Prusimski-era run of October. Until then each holding is built on the reading as transcribed,
   with the proved corrections in; a question's default is the transcription. The sheet is the HTML form
   (images as CSS backgrounds, no script; WORKING_NOTES), a card per question, grouped by holding.
5. **Applying.** The settled rows go in one file per holding, `units/<slug>/intake/latin_audit.json`, in
   two lists: `ROWS` (corrections the page proves) and `EXPAND` (certain tilde expansions), so that a later
   reader can tell a correction from an expansion. `python pipeline/review/latin_audit.py apply <slug>`
   checks that every row's old text stands exactly once on its page; `--write` puts them into `corpus.txt`
   and logs each in `transcription_decisions.csv`. The same command works for every holding, court book or
   not; no holding's own script is changed. The graded list goes in `intake/changes.yml` (marked `new:`),
   so the page of changes shows the editor what moved.

## 5. What else must change when the Latin changes (the impact sweep)

Every correction is checked for its effect on everything else written from that document. A script does
the finding; Claude reads and rewrites. `python pipeline/review/latin_audit.py impact <slug>` writes
`review/latin_audit/<slug>/impact.md`: for each correction, the documents it is in and every authored
text that cites them (from `reference/latin_audit/references.json`, made in the cloud: 396 citing lines
for the 101 documents), the lines that contain the old word marked. Beyond that list:

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

The impact list is kept per holding as the work goes and reported to the editor with the one spot sheet
at the end, so the editor sees which public texts changed and why. The rewriting of English, summaries and
pages is done after the editor's review, so that the answers are in it.

## 6. Order of work

1. **A first holding: Konin Gr.115.** It has ten documents on eleven pages, had only the light check,
   and has few tilde forms. It shows how much the two readers find and what a holding costs in tokens; the
   session writes the rate into WORKING_NOTES and goes on without waiting (the review is at the end).
2. **The holdings checked lightly**, smallest first:
   - Konin Gr.114, 120, 121, 136;
   - Kalisz Gr.414, 424, 425;
   - the land court of Konin (53/6/0/-/17, 36, 40, 45, 46) and of Kalisz (53/4/0/-/62);
   - the Ląd copy-book;
   - the Latin deed of Oe 1 Bü 14526.
3. **Poznań Gr.1181**, its open spot sheet taken over by the audit (the editor, 2026-11-27: "You can try
   it"): its 62 rows, the 108 completions withdrawn in October, and its 355 marks of doubt are read on the
   original scans; what the pages settle is applied, and what they do not goes on the one sheet at the end.
   The old sheet (to-do t088, t089) is closed.
4. **The holdings checked fully**: Konin Gr.116-119, 153 and 53/6/0/-/47. A lighter pass, for the marks
   of doubt, the tilde forms and words skipped, which the earlier checks did not look for in the same way.
5. **The editor's review**, the one spot sheet for all holdings.
6. **The impact sweep**: the answers applied, the English, summaries, pages, era essays and the rest
   rewritten as section 5 lists, every rewritten text audited by a second reader.
7. **Publishing**, at the editor's word (the editor, 2026-11-27: yes, batch by batch at their word).

## 7. The cost

No paid run is needed: the readers are sub-agents of the working session. Figures from the Gr.75 work:
two readers and Claude's settling took about an hour for two pages. The pilot will give the real rate.

## 8. The editor's answers (2026-11-27)

1. **The form of an expansion:** "Cit[ationes]" - the tilde dropped, the letters in brackets, a doubled
   plural consonant written once. Recorded in EDITORIAL_RULES.
2. **Uncertain tilde forms:** "Leave them with a tilde."
3. **The images:** "Update the plan so I can run it on my local PC where the scans are stored." Section 9.
4. **Poznań Gr.1181:** "You can try it" - the audit takes its open spot sheet over.
5. **The review:** "All at once" - one spot sheet at the end.
6. **Publishing:** "Yes" - the corrected texts published batch by batch, at the editor's word each time.
7. **Two or more gaps** (asked after the cloud preparation): "Each gap should be bracketed" -
   `v[e]n[ien]tis`. Recorded in EDITORIAL_RULES; the 21 such forms moved into the ready list.

## 9. Running it on the desktop

The editor starts a desktop session (Claude Code in the repository on the PC with the J: drive) and says
**"Run the Latin audit"**. That session:

1. **Pulls `main`** (and this branch, if the plan is not yet merged), reads CLAUDE.md, WORKING_NOTES and
   this plan, and checks the state in section 10 to see where a previous sitting stopped.
2. **Finds each holding's original scans** where they are recorded: `RAW` in the holding's
   `intake/holding.py` (the court books of Konin, Kalisz and the land court of Konin) or `raw_dir` in its
   `unit.yml` (Poznań Gr.1181, Pyzdry Gr.75, Kalisz 53/4/0/-/62, the Ląd copy-book, Oe 1 Bü 14526, whose
   scans are in Downloads, not on J:). `scan_rename_map.json` and `page_scan_map.csv` tie each page of the
   site to its scan; `intake/folds.json` gives the fold and the turn. If a folder is missing, the session
   says which and goes on with the next holding.
3. **Cuts the strips**: `python pipeline/review/latin_audit.py strips <slug>`. It takes each page from
   `<raw>/processed/<scan>` (where the holding's cutting step put the pages, turned and cut at the editor's
   folds), else `<raw>/<scan>`, and cuts it into eight overlapping bands at full resolution (at most 2,400
   pixels wide) plus a picture of the whole page, into `review/latin_audit/<slug>/strips/` (not committed).
   If a court book's `processed/` folder is gone, `python units/<slug>/intake/holding.py --crop` cuts the
   pages again from the editor's folds. It says which pages it could not find; it falls back to the web
   copies only with `--web`, and says so for every page.
4. **Runs the two readers** (section 4) as Sonnet sub-agents, holding by holding, in the order of
   section 6, with the briefs of `reference/latin_audit/briefs.md`. Each writes
   `review/latin_audit/<slug>/reader_a.json` and `reader_b.json`. For Poznań Gr.1181 the readers also take
   the 61 open rows of its old sheet (`reference/latin_audit/gr1181_open_rows.json`).
5. **Settles** each finding on a crop and writes, for each holding: `units/<slug>/intake/latin_audit.json`
   (`ROWS` from the readers; `EXPAND` from the prepared expansions of section 11, less any the page
   changes), the graded list in `intake/changes.yml` with `new:`, the questions in
   `review/latin_audit/questions.csv` (one file for all holdings; columns holding, page_id, uid, crop,
   transcribed, question, options; the crop a tight cut saved beside it), then runs
   `latin_audit.py apply <slug> --write` and `latin_audit.py impact <slug>`.
6. **Rebuilds the holding** (the later steps of `regenerate.py` for that unit), runs `verify_site.py`,
   **commits the holding** and ticks it in section 10 before starting the next, so a sitting can stop
   anywhere. It does not publish.
7. After the last holding, `latin_audit.py sheet` makes **the one spot sheet**
   (`review/latin_audit/sheet.html`), and the session tells the editor it is ready. The impact sweep
   (section 6, step 6) follows the editor's answers.

**Two sessions in one working copy**: if another session is working in the checkout, the audit runs in a
worktree (WORKING_NOTES, "Two sessions, one working copy").

## 10. Progress

| Holding | Read | Settled | Committed |
|---|---|---|---|
| Konin Gr.115 (pilot) | 2026-11-27 | 2026-11-27: 5 corrections, 2 expansions, 2 questions | 2026-11-27 |
| Oe 1 Bü 14526, the Latin deed | done 2026-11-27 (the scans on J:, the editor's word): lighter pass, one Sonnet reader, Claude on the band | 1 correction ("zatym") | none |

## 11. Prepared in the cloud (2026-11-27)

What a cloud session could do without the scans, so that the desktop sitting only reads the pages.

- **The tools**: `pipeline/review/latin_audit.py` (`scope`, `manifest`, `tildes`, `refs`, `strips`,
  `apply`, `impact`, `sheet`; its docstring has the usage). The strip cutter was tried on the web copies
  of Konin Gr.115; `apply` was tried, without writing, on every holding with expansions.
- **`reference/latin_audit/manifest.json`**: for every page in scope, its document, page id, the name of
  its scan in the holding's scan folder, its web copy, its tilde forms and its marks of doubt.
- **`reference/latin_audit/references.json`**: every authored text that cites each of the 101 documents
  (396 lines: holding pages, era essays, the timeline, connections, the family pages, the guide,
  literature links). `impact` reads it.
- **`reference/latin_audit/briefs.md`**: the two readers' briefs.
- **`reference/latin_audit/gr1181_open_rows.json`**: the 61 open rows of Poznań Gr.1181's old sheet.
- **The tilde expansions** (`reference/latin_audit/tildes.json`, every occurrence with its context, and
  `expansions.json`, the rows to apply). Each of the 837 forms was expanded twice: the guide's draft and
  a blind Sonnet reader given only the sentence (four readers, about 210 forms each). Then:
  - **451 ready** (`expansions.json`, `ready`): both readings certain and the same, in the editor's
    form (`Cit[ationes]`, `Calissien[sibus]`, `Cond[escensio]nis`, and since the editor's word on
    2026-11-27 each gap bracketed where letters are missing in two places: `v[e]n[ien]tis`,
    `M[ajes]t[a]tis`; 21 such forms); every group of them read by Claude; three disagreements settled
    by Claude on the grammar (`ad acta Castren[sia] Coninen[sia]`, `Eundem Illust[rem] M. Capit[aneum]
    Nieszczevicen[sem] habere`, `olim Magnif[icos] Antonium et Paulum`). Each row is anchored on words
    without a tilde so that it stands exactly once on its page; all 451 apply cleanly in a trial.
  - **5 certain but not anchored** (on Konin Gr.118, 119, 120: the same words twice on the page): the
    desktop session writes them by hand.
  - **381 keep their tilde**: one of the two readings unsure, or no draft (35), or a form whose letters
    are not the full word's in order (103: `ott~` for *olim*, the *JM* forms), settled by hand or left.
  The desktop session copies a holding's `ready` rows into its `latin_audit.json` (`EXPAND`), less any
  the page shows to be otherwise (a stroke or superscript with more letters).
- **A slip found and fixed**: Poznań Gr.1181, a Latin decree, was shown as German (its language stood
  under a key nothing reads); fixed in its `rulings.yml` and its data rebuilt (published with the next
  publish).

