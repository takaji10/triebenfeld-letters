# Working notes

What Claude has learned working on this edition that is not a rule of the
edition itself: how the editor works, the mistakes already made once, and the
traps in the tools. Read it at the start of a session, after `CLAUDE.md`.

**Why this file exists.** A desktop session keeps a private memory folder on
the editor's machine. A cloud session cannot see it. The editor moves between
the two, so anything worth remembering has to be in the repository. This file
is that copy.

**The rule that keeps it true** (the editor's, 2026-10-05; in full in
`CLAUDE.md`, "Lessons go into the repository"). When a session learns
something that will matter again (a correction from the editor, a trap, a
method that worked), it writes it here, or into the document it belongs to,
in the same sitting, and commits it. A desktop session may also save it to
memory; memory is never the only place. Every report on committed work ends
with a line beginning "Lessons:". Claude Code runs
`.claude/hooks/lessons_check.py` whenever Claude is about to stop, and it
holds the session to this: see that file's first lines for what it checks
and what it cannot. Where a rule already lives in another document, this
file points to it and does not repeat it.

Where the rest is:

| | |
|---|---|
| State of each holding, what is open | `CLAUDE.md` ("Where things stand"), `docs/TODO.md`, `docs/NEEDS_CONFIRMATION.md`, each `units/<slug>/notes.md` |
| What may be corrected, the editor's rulings on the text | `docs/EDITORIAL_RULES.md` |
| How prose is written | `docs/HOUSE_STYLE.md` |
| Taking a holding through the pipeline, and its fifteen mistakes | `docs/NEW_UNIT.md` |
| Ministry files: registry marks, paraphs, hands | `docs/GOVERNMENT_FILES.md` |
| Publishing | `docs/DEPLOY.md` |

---

## Working with the editor

- **What they want** (2026-09-17): a website for browsing archival holdings
  that shows the links between them (one person, place or estate across a
  letter, a contract and a mortgage certificate), and a tested way of bringing
  in a new holding. Judge proposed work by which of the two it serves.
- **Plumbing is Claude's to decide.** The editor is a historian, not the
  pipeline's maintainer: "Regarding commits and everything else, I don't
  really have an opinion on this." Bring them questions about the sources,
  editorial rulings and anything that costs money. Do not ask them to rule on
  staging, caches or checker internals; decide, and say it in a line.
- **They have transcribed this handwriting for some years**, with their work
  supported by AI, and they have accepted for this project that some
  inaccuracy always remains (2026-10-06). The edition never says its text
  was "not made by a trained reader"; the wording to use is in
  `docs/HOUSE_STYLE.md`, "About the edition".
- **They do not read German.** Whether a summary or a translation is faithful
  is for Claude and the checks to guarantee. They do compare words with the
  scans, letter by letter, and are good at it: on the spot sheet for I. HA
  Rep. 162, Nr. 295 their readings held four times out of five against
  Claude's doubts. When their view of content is needed, show it in English
  and ask about focus and usefulness.
- **Pages for readers are not the project's memory.** The About page had
  grown to 2,500 words of counts, thresholds and file names. The editor:
  "It feels like you're treating it as your own memory for the project.
  Think about what a reader or researcher would be interested in knowing."
  What a page for readers answers, and what it leaves out, is now in
  `docs/HOUSE_STYLE.md`, "About the edition". The project's own record goes
  in `docs/` and the holdings' notes.
- **Replies are short.** They said mid-project that the replies were "overly
  verbose" and that they were losing the thread. Lead with what changed or
  what is wrong, in their terms; no file names or tool names where a plain
  description will do.
- **Anything for them to look at goes on a spot sheet**, not at the end of a
  chat reply (2026-09-28): `pipeline/review/queries.py --unit <slug>`, with
  the site served beside it. Keep sheets short, and decide first what can be
  decided without them.
- **A list of rows to rule on is not a deliverable.** Given 173 paragraph
  decisions to review, they answered: "I can't review 173 rows. Please take
  informed decisions on what to do." Read every row in context, decide it
  against principles stated up front, and record the principles and the
  reversals in the holding's `notes.md`. Where a real judgement call remains,
  ask it as one question with counts attached.
- **How they answer a list of open questions** (2026-10-05): item by item, in
  a few words, and fast. "You can try" means do it now, in the session. Where
  an answer has an evident slip of the pen, act on the evident meaning and say
  in one line how it was taken. A ruling that is general goes into
  `docs/EDITORIAL_RULES.md` the same day.
- **Money: ask first, every time.** No paid model call (translate.py,
  summarise.py, read_letters.py, a batch) without the editor's agreement to
  that run. Approval of one pass is not approval of the next, even when the
  next is the obvious continuation. Say what a run would cost and wait. Free
  checks (check_translations.py, regenerate.py, any `--dry-run`) need no
  permission and should not be held up for it.
- **Work in the session before paying.** Since 2026-10-04 holdings have been
  translated, summarised and claim-checked in the session, not by a paid run
  (`CLAUDE.md`, "How a holding is translated in session").
- **A word or a name changed in the German means editing the English**, not
  paying to translate the document again (2026-09-30: "Translation costs
  money"). Translate again only where the sense of a passage changes.
- **Publish only at their word.** "Publish" and "update the website" mean
  push `main`.

## Reading and correcting the text

`docs/EDITORIAL_RULES.md` is the authority. These are the lessons behind it.

- **A reading taken from sense is not a reading.** Every correction the
  editor has caught was one Claude took from what a phrase ought to mean, not
  from the page or a witness. A real word is replaced by another only with a
  witness: a second copy, the same document, an attested fixed formula, or a
  sentence that can be read one way only.
- **Look for another copy before correcting.** The same power of attorney
  stands in three holdings and the same royal consent in two; they settled
  most doubtful readings in APP 53/968/0/-/801. A sum that must add up (the
  settlers' shares totalling 100 Hufen) catches a wrong figure.
- **An unread word gets only the letters that are read** (2026-10-05). On
  scan 0004 of III. HA MdA, III. Nr. 12367 Claude wrote two completed guesses
  into the text as "[Courier?]" and "[Londres?]" and put "perhaps the London
  newspaper The Courier" into the summary. The editor looked, saw "rev... de
  P...", and both guesses were wrong. Write "[Rev…?]" or "[?]"; keep any idea
  of what the word might be in the holding's `intake/unresolved.md`, labelled
  as a thought. A summary says "not read" and stops.
- **A name the editor cannot verify stays only on reasoning that does not
  depend on the unread letters** and can be checked, and that reasoning is
  given to them in a sentence. So "A[lvensleben]" in I. HA GR, Rep. 7 C,
  Nr. 1414: the initial is read, the name comes from his office.
- **Old rulings are candidates, not decisions.** Readings carried over from an
  earlier transcription, and the editor's own standardised names, can be
  wrong (Beugelin was Beguelin). A signature or a second source outranks them.
- **Paraphs:** crop them all and compare them side by side before reading any
  one (`docs/GOVERNMENT_FILES.md`). Before a date, a single letter is the
  place ("B. 18. Juny 16." is Berlin).
- **For Oe 1 Bü 9454** the rules and their reversals are in
  `units/oe1bu9454/notes.md`: doubled letters stay as written, `d` after a
  figure is `rt` except after `gg`, Hawich is often misread, Prusimska,
  Dąbska, Dąmbska and Moscińska are one woman, and its 313 letters were read
  whole once (`reading.json`): use that record, do not pay to read them again.
- **A termbase or authority pattern is checked against the corpus before it
  is trusted.** Three rules asserted from a word's meaning were wrong
  (Michaelis is a surname 30 times out of 38, not the feast; Holländer is
  usually the country's people, not Hauländer). `python
  pipeline/review/pattern_impact.py '<regex>'` prints what a pattern hits;
  `--audit` does every pattern. A pattern that matches nothing is as much a
  defect as one that matches too much.
- **Two matchers, two behaviours.** The entity matcher
  (`pipeline/build/entities.py`) is case-sensitive, anchors each pattern at a
  word start, and matches the line with the edition's expansion brackets taken
  out: "A[lvensleben]" is found by `Alvensleben`, not by `A\[lvensleben\]`
  alone. The forbidden-render checker is case-insensitive.
- **A person entry whose display includes a rank** needs a short `render:`
  ("Holtzendorff"), or the English is given the whole title as the name.

## Adding a holding

`docs/NEW_UNIT.md` is the procedure. What went wrong when it was followed:

- **Read what the holding touches before calling it done.** After adding one,
  read the section of the era essay it belongs to, the neighbours' "Related
  holdings", and any "the only holding from ..." wording, in both languages.
  Claude once wrote that the essay "already describes the consent" without
  reading it; the essay dated it a year early.
- **After adding people or places, look at which other documents' pages
  changed** in `git status`, and read why. That is how the statement of 1818
  in Nr. 12366 was found to explain the Venice certificate in Nr. 1414.
- **Then audit the data, not the prose:** run `build_site_data.py` and read
  its warnings ("people: no heading for ..."); check each new person and place
  in the generated data; add `reference/people_bios.yml`,
  `people_headings.yml` and `places_osm.yml` entries; recount the hand-written
  figures in the edition guide (holdings, documents, pages, languages, marks
  of doubt), in both languages.
- **German and English change in the same sitting.** Nothing checks that the
  German pages keep up; Claude writes the German.
- **One document or several:** a court file or deed package with its
  enclosures is one document by default (2026-09-30: "otherwise it gets too
  granular"). Complete instruments with their own dates and issuers may be
  separate documents joined by relations (APP 53/968/0/-/801, 2026-10-05).
  Ask where unsure.
- **Dividing a holding already built:** the model is
  `units/app539680801/intake/split_documents.py`. Then relabel the scans and
  rebuild twice.
- **Openings:** crop to the written side only where the other side is blank;
  an opening written on both sides stays whole. The editor says which is
  which. After cropping, look at the right margin at full size: first boxes
  for Nr. 1414 cut the line ends.
- **Pages photographed in two halves:** in `units/iharep162nr295/intake/`,
  `find_stitch.py` (needs OpenCV) and `build_pages.py --crop` join them into
  one image per page; the method and its pitfalls are in that holding's
  `notes.md`.
- **A transcription that comes line by line:** after the first build read
  `linebreak_decisions.csv` and `paragraph_decisions.csv`. A hand row in the
  second needs the whole line, up to 70 characters, in `context`, or it is
  dropped without a word.
- **Text written sideways** stays on its page, at the end, and is named in
  `units/<slug>/sideways.yml`; this works for any holding.
- **A holding's title** in `unit.yml` is one sentence saying what it is about,
  in English and in German, not the archive's heading with a gloss.

## The English, the summaries and the claim check

- **Where one summary is kept.** Change all of them together:
  `units/<slug>/intake/summaries_draft.py`, `units/<slug>/summaries_de.yml`,
  `site/_data/summaries.yml`, `site/_data/summaries_de.yml`, and on the
  desktop `cache/summaries-raw/` and `cache/summaries-raw-de/`; its statements
  in `intake/claim_check.yml`; and often the same words in `about.md` and
  `about_de.md`.
- **Never rebuild the site's summary files from the desktop cache.** Cloud
  sessions correct the published files directly, and the cache on the desktop
  does not have those corrections: a rebuild once put 46 lines of
  `site/_data/summaries_de.yml` back to older name forms. Insert or replace
  the lines of the holding being worked on, and read `git diff` for any line
  that belongs to another holding.
- **The claim check only weakens or cuts.** Each statement of a German
  summary is held to its document as supported or overstated; nothing is
  added. A date an office wrote on a paper is not the day it arrived unless
  the mark says so; a note that names no office is not "the Cabinet".
- **Fixing names in the English after an authority changes:** take the hits
  from `pipeline/review/uncanonical_names.py`. On the desktop, change the
  translation cache as well as the published file, or the next publish rolls
  the fix back; compare the published file with HEAD before committing.
- **A changed line of transcription** is changed in `corpus.txt`, in the page
  file under `transcriptions/`, in a row of `transcription_decisions.csv`, in
  `sideways.yml` or `office_notes.yml` if it is the first line of a block
  there, and in `intake/translation/doc<N>.yml` (with its `marker_count`).
  Then `write_cache.py <N>`, `check_translations.py`,
  `publish_translations.py`.
- **After publishing English, read the holding's glossary matches.** English
  "entails" and "cession" drew false glossary marks and were reworded. The
  checker forbids "hypothec" in English, Latin "sub hypotheca" included.

## Traps in the tools

- **`python regenerate.py --help` prints no help.** It runs the whole pipeline
  for every holding. `--site` also rebuilds every holding first. Use
  `--unit <slug>` for one, then `--site` once at the end.
- **After any full rebuild read `git status`** for files of holdings that were
  not touched.
- **Scripts with backslashes or apostrophes are written to a file and then
  run.** In the desktop's Bash tool a heredoc turns `\\[` into `\[` and `\b`
  into a backspace (this corrupted `reference/glossary.yml` once) and fails on
  an unbalanced apostrophe.
- **A one-shot edit script asserts each replacement exactly once.** Commit
  before running it, so a partial failure can be undone. Never run one again
  after it has partly applied: it duplicated summary lines once.
- **Line endings.** `git ls-files --eol <file>` tells the truth; `grep` for a
  carriage return does not in Git Bash. The files differ, so check each one
  before editing: the changelog, EDITORIAL_RULES, NEW_UNIT, DATA_MODEL, the
  era plan, the site essays and the edition guide are CRLF; this file,
  `CLAUDE.md`, TODO, NEEDS_CONFIRMATION, HOUSE_STYLE and the holdings'
  `about` files are LF.
- **Marks of doubt** are counted by hand in the edition guide. Recount from
  `corpus/index/uncertainties.json` after any change to a marker.
- **A local build after pulling a cloud session's work** can rewrite
  `page_scan_map.csv` from the local image names. Regenerate the holding, run
  `pipeline/build/relabel_scans.py --unit <slug> --apply` while it reports
  labels to update, rebuild twice, and check `git status` shows no scan
  changes.
- **Deleting files from a script:** the desktop's safety check refuses `rm`
  on a path held in a shell variable. Work in the session's scratch folder
  and leave test files there.
- **`python3` and `python` both run on the desktop; the cloud has
  `python3`.** A script meant for both is started through a small `sh`
  wrapper that tries each (`.claude/hooks/lessons_check.sh`).
- **Dates and coordinates:** Wikidata's search rate-limits hard; one SPARQL
  request with a list of labels works. szukajwarchiwach.gov.pl blocks
  automated access.

## Desktop and cloud

| | Desktop (the editor's machine) | Cloud session |
|---|---|---|
| Raw scans, `review/`, `cache/` | present | absent |
| Paid runs | possible, at the editor's word | not possible (no key) |
| `regenerate.py` end to end | yes | no: run the later steps directly (`CLAUDE.md`) |
| Claude's memory folder | yes | no: this file is the copy |

- Start every session with `git fetch` and `git status -sb`: the other kind of
  session may have pushed.
- Records a cloud session will need are copied from `review/<slug>/` into
  `units/<slug>/intake/` (unresolved words, rulings sheets, the translation
  pages, the claim check).
- A cloud session corrects published files directly; a desktop session must
  not overwrite them from its cache (above).

## Publishing and checking

- On the desktop, work is committed on `main` and published by `git push
  origin main`. In the cloud, work is on the session's branch and `main` is
  fast-forwarded to it. Either way only at the editor's word, and `TODO.md`,
  `CLAUDE.md` and the changelog say "published" in the commit that is pushed.
- **A run that fails with "The job was not acquired by Runner"** after
  waiting fifteen minutes is GitHub's fault, not the project's (seen three
  times on 2026-10-05, while https://www.githubstatus.com showed Actions as
  degraded). The repository is pushed all the same and the live site keeps
  its last good version. Start only the failed step again with `gh run rerun
  <id> --failed`; if GitHub is still degraded, leave it, since the next push
  rebuilds everything.
- The "Build and deploy" run can take ten minutes. Watch it in the
  background (`gh run watch <id> --exit-status`) and then fetch one page of
  each kind from the live site: a document is `/documents/<slug>/<n>/`, a
  holding page `/sources/<slug>/`, a scan `/assets/scans/<file>.jpg`.
