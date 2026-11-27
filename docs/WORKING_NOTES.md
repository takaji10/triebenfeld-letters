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
- **They are an amateur palaeographer** (their own phrase, and the one the
  site uses), with their work supported by AI, and they have accepted for
  this project that some inaccuracy always remains (2026-10-06). The edition never says its text
  was "not made by a trained reader"; the wording to use is in
  `docs/HOUSE_STYLE.md`, "About the edition".
- **The site does not call the English translations drafts** or say that
  they are unchecked (2026-10-06). The caution the editor wants is the one
  general sentence on the About page: check against the original before
  citing. Rule in `docs/HOUSE_STYLE.md`, "About the edition".
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
  A row can carry a picture of its line (an `image` column, a file in
  `review/<slug>/spot_img/`): use it wherever the editor would have to count
  lines on a dense page. On 2026-10-08 they could not find four lines of
  letter 289 by number, although the numbers matched the page.
  A sheet can run across holdings (2026-10-07): a row with a `unit` column
  is a line of that holding's corpus, and a row with a `summary` column asks
  for a decision instead of a reading (its options are the buttons). The
  sheet "Before publishing" was made so: `python pipeline/review/queries.py
  --unit app536046 --sheet before_publishing.csv`, with the built site
  served on port 4000 (`python -m http.server 4000` in `site/_site`); a
  copy of its rows is `docs/archive/PRUSIMSKI_before_publishing.csv`, and the
  answers are read with `--read`. The first option of each row is what
  is already built.
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
  checks (check_translations.py, pipeline/regenerate.py, any `--dry-run`) need no
  permission and should not be held up for it.
- **Work in the session before paying.** Since 2026-10-04 holdings have been
  translated, summarised and claim-checked in the session, not by a paid run
  (`CLAUDE.md`, "How a holding is translated in session").
- **A word or a name changed in the German means editing the English**, not
  paying to translate the document again (2026-09-30: "Translation costs
  money"). Translate again only where the sense of a passage changes.
- **Publish only at their word.** "Publish" and "update the website" mean
  push `main`. **Every push of `main` deploys the site**
  (`.github/workflows/pages.yml`): "merged to main, not published" is only
  true while the merge stays local. On 2026-10-22 and 23 several sessions
  merged into `main` at the editor's word and pushed it, and the docs went
  on calling the work "not published"; the deploy history showed it had
  been live since those days (found at the Publish of 2026-10-24). When
  the editor says "merge to main", merge locally and do not push; push
  only at "Publish". To date a piece of work's publication, ask
  `gh run list --workflow pages.yml` for the first successful run whose
  commit contains it (`git merge-base --is-ancestor`).
- **Writing the editor gives as a sample is for style only** (2026-10-20).
  They gave three samples of their writing, among them the preface and
  introduction of their own book on the estate, so that their voice could
  be analysed (`docs/EDITORS_VOICE.md`). Claude then set a sentence of the
  book against the documents and offered the difference as a point to
  rule on. The editor: "Please don't incorporate the sample text into the
  understanding of the site. Those were just samples and they should only
  be used for analysing my writing style." What a sample says about the
  estate, its people or its dates is not a source, is not checked against
  the documents, and does not go into NEEDS_CONFIRMATION, the story, a
  person's entry or anything else on the site.
  **The exception is writing they give as content** (2026-10-23): their
  index of places ("Place Names.md", the gazetteer) is both a style sample
  and text for the site, so its facts are read against the documents and
  the differences go into NEEDS_CONFIRMATION, as for any source. Ask which
  it is if a new sample does not say.
- **Simple steps go to a Sonnet sub-agent** (the editor, 2026-10-23: "For
  the simple steps, use a sub-agent with the Sonnet model. Save the tough
  stuff for Opus."), and since 2026-11-22 **every step is first offered to
  a sub-agent**: the next section, "Sub-agents and token use", is the rule.
  The gazetteer import was the first (`docs/GAZETTEER_PLAN.md`, step 1).

### Sub-agents and token use (the editor, 2026-11-22)

The editor: "always try and use Sonnet sub-agents (or even Haiku if it makes
sense) to reduce token use - but obviously to not reduce quality in any way.
You'll need to be careful and strategic with this." The main session's
tokens are the dear ones; a sub-agent's reading is cheaper, and its pages
of output never enter the main context if it writes them to a file. But a
sub-agent's error that reaches the site costs more than it saved. So:

1. **Before each step, ask in this order.** Can a script do it (free)?
   Can a sub-agent do it from a written brief, with an output Claude can
   check quickly? Only then does the main session do it itself. A plan
   names the model for each step (`docs/NR421_ENGLISH_PLAN.md` is the
   pattern).
2. **Which model.**
   - **Haiku**: purely mechanical work with a machine check behind it:
     running scripts and reporting the result, moving or renaming files
     from a list, filling a schema from structured data where a validator
     runs after, counting, collecting grep hits into a table, laying out a
     spot sheet from rows already decided. Never reading handwriting or
     print from an image, never judging a language, a name or a sense,
     never writing words a reader of the site sees.
   - **Sonnet**: reading from images (transcription checks, independent
     second readings, table cells, signatures cropped onto a sheet); claim
     checks of summaries; faithfulness checks of a translation against its
     original; sorting a diff or a candidate list into kinds; citation
     audits; connections sweeps; fetching a web source and copying it
     verbatim; writing a script to a precise spec; building review sheets.
   - **The main session (Opus)** keeps: the plan and the rules; settling
     where readers disagree (by looking at the crop, not the whole page);
     identifications of people, places and signatures; the English and
     German prose readers see (translations, summaries, holding and era
     pages); every ruling put to the editor; and anything told to the
     editor as fact.
3. **Quality is held by the method, not by trust.** These are the lessons
   already learnt with sub-agents, gathered:
   - Anything read from an image is read by **two readers independently**
     (one of them blind, when the brief's witnesses could lead it); Claude
     settles the differences. A reading only the led reader gives stays a
     question.
   - A reader **says which strips it did not open**; Claude reads those
     itself (Nr. 3067, Nr. 421: two of four readers left strips unread).
   - **Figures** a reader gives are checked digit by digit against a second
     reader (the 1882 reports: a reader cut digits off a figure).
   - The brief **quotes the plan's rule word for word**, not a stricter or
     looser paraphrase, and names the file's internal witnesses (two copies,
     a decision and its draft).
   - **Every finding Claude acts on is checked** by Claude (the citation
     audit: 14 of 22 flags were real). Claude need not re-read what an agent
     found in order; it reads what will change the text.
   - A sub-agent **writes only where the brief says** (`scratch/`,
     `review/`, a named script), never the editor's files (`folds.json`,
     answers, transcriptions they supplied), and **never commits**.
4. **Spending fewer tokens without losing anything.**
   - Give **paths, not pasted text**, in a brief; the agent reads the files.
   - Ask for the result **in a file** (TSV or YAML) and a **short reply**:
     counts, what was not done, the doubtful items. The main session then
     reads only the rows it needs.
   - Start **independent agents together** in one message; work on
     something else while they run.
   - For a follow-up, **message the agent that already has the files
     read** (SendMessage) rather than briefing a new one.
   - When the main session must look at an image, look at a **crop** of the
     line or the signature, not the page.
   - **Do not delegate** what is smaller than its brief (one grep, a
     one-line fix), or what needs so much of the conversation that the brief
     would be as long as the work.
5. **Say who did what.** A holding's notes say which steps went to which
   model, and the report to the editor names them; `prepared:` in unit.yml
   (the holding page's "How it was prepared") names the models truly.
- **The editor chooses which maps come in** (2026-10-23: "I don't want to
  add all of these maps - I will be selective with them"). A map cited by
  the gazetteer, or lying in their Maps folder, is not thereby wanted; ask
  before bringing one in (`docs/MAPS_PLAN.md`). Before planning work on a
  map, look beside its image on J: for a `.kml`: it names the map's
  MapWarper number, and the editor's control points are there already
  (sixteen maps, 2026-10-23). Read them from its API, not the CSV page,
  and take as the map's original the file whose size equals the API's
  width and height (MAPS_PLAN, section 5): for Łukom 1766 that is the PNG,
  not the JPG beside it. A first `curl` to mapwarper.net failed with
  "Could not resolve host" and worked an hour later: a passing failure,
  not a block. Try again before telling the editor a host is blocked.
- **No method talk on a reader's page** (the editor, 2026-10-23: "I never
  explain to the reader what I'm doing or how (like this project tends to
  over-do)"): HOUSE_STYLE, "No method talk".

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
- **A signature in the same document is a witness for a name** (editor,
  2026-10-09). In Oe 1 Bü 14526, document 26, "Der Schütze Reise" was left
  as transcribed because the downscaled scan did not settle it, although the
  protocol is signed "Jacob Kriede" and another letter names him Kriede. The
  editor: it should be Kriede. Where the same document signs or names the
  person plainly, propose the correction with that witness instead of
  leaving the reading.
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
- **A derivation of a name is a claim like any other** (2026-10-26,
  app534062). The session wrote of the surname Szetlewicz that "the name is
  formed from the place, as Szetlewek itself is formed from Szetlew" - and
  the editor's one correction before publication was that Szetlewicz is a
  surname, not a place name. An etymological analogy is not settled by the
  documents or by another name's behaviour; state what they show (a family
  of that name living at the place) and leave the derivation out unless a
  source or the editor settles it. The same rule that keeps a plausible
  word out of a transcription keeps a plausible etymology out of the prose.

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
- **Finding the fold of an opening by the darkest band near the middle is
  wrong.** On APP 53/17/0/-/Konin Gr.145 it put the line 60 to 170 pixels
  left of the gutter on most of 62 scans and cut the ends of the left
  page's lines; a contact sheet of whole openings was too small to show it.
  Look for the thin dark line of the gutter (a few pixels darker than the
  paper 25 to 60 pixels either side), check every fold on a strip cut round
  it at readable size, and let each page keep 30 pixels beyond the fold.
  Then make the editor's approval sheet (`intake/fold_sheet.py` in that
  holding) before the pages are used for anything.
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

- **A holding the editor has already worked over** (APP 53/17/0/-/Konin
  Gr.145, 2026-10-06). They asked whether a light touch would do. The way
  to answer: read three or four pages spread through the text word for
  word against the scans before saying anything, and report the rate and
  the kinds of slip found, with an example of the worst. There the
  translation was sound and the transcription had about one small slip in
  a hundred words, but one page of three had dropped a phrase, which only
  a full reading finds. Say what a light touch will and will not catch,
  do it, and put on the holding's page how many pages were compared.
- **A full check for dropped phrases** (the same holding, 2026-10-06; the
  editor asked for it after the light check). What it took and what it
  found, for the court books still to come:
  - Read every page as two enlarged halves beside its text. Record each
    find as a row (page, kind, old, new, the scan's own spelling, weight,
    a note in plain English) in one file, apply them once with a script
    that demands each `old` exactly once on its page, and log them.
  - **A dropped phrase is nearly always a skip between two occurrences of
    the same word** ("urodzony Chełmski ... urodzony Chełmski", "względem
    ... względem"). 26 in 122 pages, from one word to sixty. The longest
    was the most important passage in the document. A light check cannot
    promise there are none.
  - **The translation was right where the transcription was wrong** in most
    places: it had been made from the scan or from an earlier state of the
    text. So before changing the English for a corrected Polish word, look:
    of 233 corrections the English needed 32 changes.
  - **Check the other direction too.** The English had itself dropped a
    paragraph (a hundred Polish words with no English, at the seam between
    two of the editor's sections). A page whose English is much shorter
    than its Polish is the place to look.
  - Grade each find for the editor in three plain grades (changes what the
    court found or did; adds a fact; legal wording) and give it to them on
    a sheet (`intake/dropped_sheet.py`), not in the reply.
  - A reading on one page is often settled by the next: "tęże" was Latin
    "ferme", "komornik" was "Komisarz". Withdraw a row rather than keep a
    guess.
- **The early Latin court-book entries are not "already corrected"** (batch
  2 of the Prusimski era, 2026-10-06). Their Latin is a first reading with
  many doubts, and the English and its notes rest on it. What worked:
  - Read the whole entry against the scan (they are one or two pages), and
    **read the neighbouring entries on the same pages first**: they use the
    same set words and settle most doubts ("Contumaces", not
    "Concessionis"; "Ministerialem ad pronuntiandam ... rotham", the court's
    messenger speaking the oath, not a roll).
  - Then revise the editor's English where the Latin changed, keep their
    terms, drop the notes that discuss readings now settled, and record
    each passage as it stood and as it stands (`build_docs.py`, `FIXES`).
  - The heading of the sitting is often on a leaf with no scan: it is not
    a page; quote it on the holding's page and date the entry by it
    (`dates: sitting:` in `rulings.yml`).
  - `pipeline/intake/courtbook.py` has the shared steps (cutting, the fold
    sheet, corrections, the English, summaries). Copy `units/app536036/`
    for a holding with two entries on one page.
  - 53/6/0/-/17 (1589) is far rougher than the rest: 109 doubts in 713
    words, leaf 27 verso given twice, part of that page under a dark
    patch, and a related entry ("Eorundem Visio", leaves 27v-28) not
    transcribed. Put to the editor before it is built.
- **Folds are the editor's to place** (2026-10-07). On Konin Gr.145 the
  lines I found still ran through the ends of the left pages' lines on
  many scans, and the editor asked for a page to move them on instead of
  reporting scan numbers. `courtbook.fold_sheet` writes it for every
  holding that is cut; `courtbook.py folds <slug> <file>` takes the saved
  folds back. Do not publish a cut holding before the editor has saved or
  approved its folds.
- **Compare the scans with the text before building** (batch 2). Three
  things turned up that the editor's files did not say: other entries
  about the same people on the same scans (53/6/0/-/17 has three); a
  page given twice (the end of that entry, in two readings: take one); and
  a middle left out of both transcription and translation (Konin Gr.136,
  the house-by-house list of the villages). The first two are noted and
  the holding built; the third is put to the editor before building.
- **A re-reading "only if you're confident"** (53/6/0/-/17): confidence
  came from reading every phrase in each place it occurs, in the entries
  that follow on the same scans. Replace the paragraph whole, keep the
  editor's reading in the log, and leave marked whatever one place alone
  cannot settle (an ending, one word).
- **The decree of 1775 dates and explains the older entries.** It cites
  the decrees of 1589 ("Monday before Saint Vitus", which settled a
  weekday the editor could not read on a leaf with no scan) and of 1728,
  and says who was grandfather and uncle of the Starost. Search its
  English for the year before writing a holding's page.
- **Person entries across two centuries.** "Prusimski" and "Prusimska"
  are different people in different documents (Krzysztof and the elder
  Antoni in 1728, Katarzyna in 1763, the Starost and Michalina later).
  Each gets an entry matched `only_in` its documents, and the later
  person's entry is shut out with `not_in`. A family named from a place
  (Trąmpczyński) is matched `only_in` too, because the same word is the
  place's adjective in Polish.
- **A run without stops** (the editor, 2026-10-07): for the Prusimski-era
  court books every unit is processed in turn, and questions, fold
  adjustments and the editor's review of readings wait for the end. A
  question is written into `docs/archive/PRUSIMSKI_QUESTIONS.md` with the default
  taken, and the holding is built on that default. Do not stop to ask.
- **A rough register (Konin Gr.115).** Entries are a few lines among many,
  and a sitting's date line may be pages earlier. Before anything else,
  read the leaf numbers off the scans (a montage of the top right corners
  does it in one look) and make small overviews of the pages to find each
  entry. An entry whose date line is on a page that was not photographed
  is dated to the month from the dated headings before and after it
  (`dates: inferred`, with the basis). Photographs numbered in a series
  are not numbered by leaf.
- **"Gaza" is a hut or house**, not goods; "trajectio gazae" is shooting
  through a house. The editor's English had "goods" for it.
- **Sąd grodzki is the "municipal court" in all the edition's English**:
  the translations (the editor's English; the translation check forbids
  "castle court") and the edition's own prose (holding pages, summaries,
  the timeline, the literature's English) alike. The prose said "castle
  court" until 2026-10-21, when the editor ruled it wrong and it was
  changed throughout (502 places). The glossary entry `grod` explains that
  "municipal" here means the gród's court, not a town's. Urząd grodzki is
  the "municipal court office". The German summaries keep "Burggericht".
- **Names in the English follow the edition's forms.** The estate is
  Trąbczyn whatever the clerk wrote (`reference/english_forms.yml`, rule
  `trabczyn-place`); Celmer is Zelmer. Run `uncanonical_names.py` after
  publishing a holding's English and clear what it lists.
- **The editor's own transcription and translation are kept as theirs.**
  That holding's Polish is in modern spelling and its English is the
  editor's: neither is redone, the English is cut to the pages by a
  script (`intake/translation/build_doc1.py`), their headings and notes
  go in square brackets, and their page marks may sit a few lines from the
  Polish ones (move only those that are most of a page out).
- **Polish text and German-made patterns.** A new Polish holding matched
  seven existing entries wrongly ("brzeg" as the town Brzeg, "święcie" as
  Swięcia, "Florian" as Florian Gelanski). After adding a holding in
  another language, list what the index finds in it and read every entry
  that is not obviously right. `not_in:` on a person or place entry shuts
  it out of named documents.
- **A page can be shared only by neighbouring documents** (Konin Gr.117).
  `match_scans.py` fails with "image assigned more than once" when the pages
  of the corpus do not run in order: document 2 on leaves 54v, 55, 55v and
  document 3 on leaf 54v again. Number the documents so that the one that
  runs on comes second, and say why in `holding.py`. To renumber after a
  build, reset the unit first (the generated files, `pages/`, the scans,
  the translations: the scratch script for 53/6/0/-/46 is the pattern),
  since `--write` refuses once corrections are logged.
- **Kinship words decide who is who: look at them on the scan.** In Konin
  Gr.117 "Patrui" (the uncle's, written "Patruj") had been read "Patrii"
  sixteen times and put into English as "father" fifteen times; the same
  text had "Patruum" and "Patruo" a few lines away. One look settled how
  Paweł and Antoni Prusimski were related, which no other holding says.
- **An unwritten entry is still an entry** (Konin Gr.116). A heading with
  the clerk's "Vacuum" across the space, or pen strokes, and often a
  signature under it: the party announced an entry and never supplied the
  text. Build it as a short document, transcribe "Vacuum" and the
  signature, and say on the page what it is.
- **Signatures are usually missing from the editor's text** and are worth
  adding: in a register they are the party's own hand. Give them as
  written, "[?]" for a word not read, never the office the man is known to
  have held.
- **Use the review page the editor already knows; do not build another**
  (the editor, 2026-10-07). For the court books I wrote a new fold page (a
  long page of narrow strips with a small picture beside each) when
  `review_folds.py` already had one the editor used: one opening at a time,
  shown whole, arrow keys to page through. They asked for the old one back.
  The page is now `pipeline/intake/fold_page.py`, used by both
  `review_folds.py` and `courtbook.fold_sheet`. Before writing any page for
  the editor to work on, look in `pipeline/intake/` for `review_*.py`.
- **A fold photographed at a slant needs the sheet turned, not only the
  line moved** (the editor, 2026-10-07). On the court-book fold page the
  mouse wheel, or shift-drag, turns the sheet about its centre under the
  vertical line; the saved file has `{"fold": x, "angle": degrees}` for
  every scan, the angle counter-clockwise as PIL's rotate() takes it.
  `courtbook.cut` turns the scan first (the canvas grows, nothing is lost)
  and cuts at the fold plus the shift of the left edge, which is what the
  page shows. `take_folds` runs `make_scan_derivatives.py` without
  `--force`: with it, every web image of the edition is remade.
- **Folds on photographs**: `courtbook.find_fold` is 20 to 60 px too far
  right. Cut the gutter strip of every scan side by side with a ruler
  (ticks every 50 px) and read the folds off one image.
- **The light check, when a holding is too long for a full one**
  (PRUSIMSKI_ERA_PLAN): every heading and date line, every name of a judge
  or party, and the short entries word for word; say on the holding's page
  which pages were compared, mark the unread long documents `rough` in
  `rulings.yml`, and hold each statement of a summary to words that carry
  no mark of doubt.
- **`courtbook.read_english` takes leaf marks dressed as headings**
  ("### **[78v]**") as well as bare ones.
- **A later holding can correct an earlier one: go back.** Prusimski's
  protest in Konin Gr.119 ("Alios vero arestum non praevenit": the arrest
  did not reach the others) showed that the oath in the land court's decree
  53/6/0/-/47, built an hour before, had been misunderstood by the editor's
  English and by me ("he did not forestall the arrest"). The decree, its
  summary, its page and its English were corrected in the same sitting.
  When two holdings use the same formula, read them side by side.
- **An abbreviation written out wrongly is wrong everywhere.** In Konin
  Gr.153 "Jur~to" had been written "jurisdictione" eleven times (it is
  "jurato", sworn) and "Cond~nis" "conditionis" nineteen times (it is
  "condescensionis"). Look at three or four occurrences on the scan, then
  correct all, and say in `holding.py` and on the page of changes which
  were seen and which follow. But "Cond~nem" is "condemnationem": one
  letter apart, so look at each form.
- **Skipped lines hide between repeated words.** Three were found where the
  same two words stand twice a line apart ("et quoniam ... et quoniam" in
  53/6/0/-/47; "Judicibus ... Judiciis" in Konin Gr.117; "Protocollo ...
  Relationis" in Konin Gr.119). A sentence that does not construe, or a
  certificate that certifies the wrong thing, is the sign.
- **What the editor photographed and did not transcribe** is listed in the
  questions file with what each scan shows, and is not built, except a
  note of a few clear lines that belongs to the story (Konin Gr.118,
  document 2).
- **The check for "chestnut"** (a misread hypocaustum) fired on a real
  chestnut mare; the rule in `reference/translation_glossary.yml` now
  excepts "Equam Castaneam". A forbidden rendering that blocks a page may
  be the rule's fault: read the Latin before changing the English.
- **Apostrophes in a "why" string written through a shell heredoc** broke
  two `holding.py` files (the backslash was lost). Write scripts with the
  Write tool, or avoid the apostrophe.
- **When the context was summarised mid-run**, the next step was taken from
  the holding in hand (its scratch images and the editor's two files), not
  from memory of readings: read the scans again before writing a row.

- **What the full checks of the Konin registers taught** (Konin Gr.117,
  Gr.118, Gr.153, Gr.119; 2026-10-07, 406 corrections in four holdings that
  had already had the light check). The editor's first readings of these
  hands go wrong in the same few ways, and a check should look for them
  first:
  - **A line passed over.** Ten times in four holdings. The eye jumps
    from a word to the same word a line or two on ("Chełmski ... Chełmski",
    "Calissien ... Calissien", "Tribunalitii ... Tribunalitii"), or joins
    the end of one line to the start of the next but one ("verten|nem",
    "Au|vis" read as "Auris"). The sign is a sentence that will not
    construe. Count the lines of the scan against the text.
  - **Abbreviation signs written out wrongly, everywhere.** "p" with a
    stroke through the tail is "per", not "pro" (with an accusative: "by").
    The hook after "b" is "-us" ("partibus"), not "-busque". "jurto" is
    "juramento", an oath, or "jurato", sworn: never "jurisdictio".
    "Cmrius", "Cmrlia" are "Camerarius", "camerarialia" (the boundary
    chamberlain and his office), not "Commissarius". "Condnis" is
    "condescensionis". "ol" with a stroke is "olim", the late. "Dcam",
    "Dn" before the name of a Sunday is "Dominicam". "ptium" is "partium",
    "pns" "praesens", "Mafnes" "Manifestationes", "Succores" "Successores".
    Correct such a word in every place only after looking at several.
  - **"Tibi", "Te", "tuis" in a citation.** A royal citation addresses the
    man cited. The editor read "Sibi", "se", "suis", and the English then
    lost who was cited. The close is a formula: "Sis pariturus Terminum
    attentaturus et Judicialiter responsurus".
  - **Case endings decide who does what.** "Illri Mgfco Prusimski" is a
    dative: he is paid, he does not pay. "Illris Magnifice Prusimski" is a
    vocative, not a lady. Read the ending before the English is trusted.
  - **"invalibilis" is "invalid".** The English had "inviolable" for it.
- **How a full check is recorded** when the light check's rows are already
  applied: the new rows go into `units/<slug>/intake/full_check.json`
  (ROWS, FIXES, DROP), written against the text as the light check left it,
  and are applied once with `holding.py --full`; `english()` adds its FIXES
  after the script's own. JSON, written with the Write tool, because the
  rows quote Latin and English with every kind of quotation mark and a
  here-document breaks on them.
- **After a full check the claim check quotes the old text.** Bring the
  Latin quoted under `where:` up to the corrected text and read each
  statement against it again; say in the file's head that this was done.
- **An entry first transcribed in session** (53/6/0/-/46 no. 17, 53/6/0/-/47
  no. 43) is a document like any other, with its text and English as
  constants in the holding's script. The holding is cleared and built again
  (`--write` refuses once corrections are logged), and the entry goes on the
  page of changes as a new source, with its whole text, for the editor to
  read. A scan the editor has not seen cut gets a fold set by eye and a line
  in the to-do list.
- **Look at the word before saying what the text has.** While reading entry
  no. 43 of 53/6/0/-/47 I told the editor that entry no. 26 had "Capit~"
  where no. 43 has "Capitalis", from memory of its English. The text and
  the scan of no. 26 have "Capitanealis", written out; the editor then told
  me to "fix" it, and there was nothing to fix. A remark about another
  document is checked against that document's text and scan first.
- **Ask whether an entry matters before building it.** Entry no. 43 of
  53/6/0/-/47 was transcribed, translated, built and written up, and the
  editor then found it not relevant and had it taken out: Prusimski is only
  cited in it. Before an untranscribed entry is built, tell the editor in a
  sentence who the parties are and what it decides, and let them say. To
  take a document out: restore the holding's files from the commit before it
  (`git show <commit>:<file>`), keep the text as a record in `intake/`,
  clear what the build wrote (the letter page, the translation, the corpus
  files, the scan images, the cache file) and build the holding again.
- **The editor's reading on the page overrules the check's.** In Rajewicz's
  protest (Konin Gr.116) the check read "Citraque", built "without his
  consent" on it, and said so in the English, the summary, the holding's
  page and the page of changes. The editor, on the spot sheet, read
  "Cumque". A reading that turns the sense of a sentence goes on a spot
  sheet before anything is built on it; and when it is withdrawn, the
  summary and the pages are cut back to what the remaining words say.
- **A spot-sheet answer can carry leftover text.** The sheet keeps what was
  typed under "Something else" after another button is picked. Read the
  button as the answer, and ask about the leftover.
- **Look at the page, not only at the data, when an era is added.** The
  timeline page listed the years 1794 to 1832 in its template, so the
  entry written for the commission of 1775 was in the data and never on
  the page, through a whole run and a publish; and that entry still said
  what the later holdings had disproved. When holdings change what is
  known, the timeline, the story page and the About page are read again
  as a reader sees them.
- **New scans of pages already in the edition** (Oe 1 Bü 9454, letters 245
  and 289, 2026-10-07). The text is not swapped for the new transcription:
  it is made line by line from the corpus text (which carries every earlier
  ruling), the new transcription and the new scan, the scan deciding. Then,
  in this order: the images (archive folder, `pages/`, the two scan maps),
  `pipeline/regenerate.py --unit`, a diff of the letter's front matter against HEAD
  (date, place, sender must not move), the English (`doc<N>.yml`,
  `write_cache.py`, publish with the holding's tag, diff: only those
  letters), the summaries, the `rough` list, the count of marks of doubt.
- **Do not run `summarise.py --build` on this machine to publish a changed
  summary.** It assembles the whole file from the local cache, which is
  behind the repository: on 2026-10-07 it would have reverted fifty
  summaries and brought back one for a document that no longer exists.
  Change the entry in `site/_data/summaries.yml` and `summaries_de.yml`
  directly, and the cache file too.
- **`scan_rename_map.json` and `scan_decisions.json` are unsorted.**
  A script that loads and dumps them rewrites every line. Replace the name
  in place as text. (They were CRLF until 2026-10-19; now LF like every
  text file, "Line ends" below.)
- **The page of changes is the editor's working copy.** They read it once
  and work from it afterwards. Whatever is added later carries `new:` in the
  holding's `changes.yml` and is marked on the page; an entry that no longer
  holds ("not checked") is taken out, and the new entry says so.

- **A table with no transcription, read from the scans in session** (AGAD
  1/169/0/1/1745, 2026-10-13). What worked, in this order:
  - Look at the top of the page before anything else. The heading was
    printed on a leaf behind the written ones and was outside the first
    crops; the editor's "the headers stay the same on each page" meant
    that.
  - Read each page in overlapping bands of six or seven lines at full
    size, figures first. Then check the arithmetic before believing
    anything: every line (men + women = sum, sums = total) and every page
    against its "Latus", in every column. 164 lines and six page totals
    held at the first reading; a misread digit cannot hide. Names have no
    such witness: read them a second time on strips enlarged twice, and a
    third time at three times for the doubtful ones.
  - Keep the reading in one file (`intake/table.csv`) and make everything
    from it: page files, corpus, the English table, the spreadsheet. A
    correction is then made in one place.
  - For the editor's check, a spreadsheet with a picture of each line of
    the scan beside its row (`holding.py --xlsx`; row positions found from
    the dark pixels of the figure columns, the slant of each page measured
    and taken out), check formulas that turn to LOOK when a sum breaks,
    and a way back (`--take`). It needs `openpyxl` (`pip install openpyxl`;
    the row finder in the scratch folder also used `numpy`).
  - The kind of place and the name share a column on the page: one cell in
    the text, two columns in the spreadsheet.
  - The site's table code took a two-level heading and one closing row.
    It now takes any number of heading rows and sets off a row without a
    number (`unitlib.render_table`); the English table may translate its
    heading (`publish_translations.english_table` compares where the
    labels stand, not their words).
- **`courtbook.find_fold` looks between 40 and 60 per cent of the width.**
  On a scan with a colour chart beside the book the fold lies outside that
  and the function returns a ruled column line (2393 for a fold at 3122).
  Read every fold off a strip, as the notes above say; here it mattered.
- **A place pattern made for running text matches a village's by-name in a
  list.** "Kurow Koninsk." was indexed as the town of Konin and the village
  "Ostrow" as the town of Ostrów; both are shut out with `not_in`. After
  adding a list of places, read every place the index finds in it.
- **`uncanonical_names.py` dies on the desktop console** when a hit has a
  Polish letter (cp1252). Run it with `PYTHONIOENCODING=utf-8`.
- **Taking back a spreadsheet the editor has checked** (AGAD 1/169/0/1/1745,
  2026-10-13). Four things the first version of `holding.py --take` did not
  allow for:
  - The editor clears a doubt by emptying the "Doubt" cell, and may shorten
    one. Take that column back as well as the data, or the notes of the
    reading keep doubts the editor has settled.
  - Taking a "[?]" out of a cell, the editor retypes it and a period after
    the name can go with it ("Leysce[?]." came back as "Leysce"). Look at
    every changed cell that lost its last character against the scan, put
    the period back if it is on the page, and say so in the report.
  - The editor may write out what an abbreviation sign stands for
    ("Trąmpczyn." where the page has "Trąmpczy" and the sign). Keep their
    form and say in the line's note what is on the page.
  - The script that made the spreadsheet must not be able to write over the
    file they saved (`--xlsx` now refuses while it is there). The record of
    their changes is a table in the holding's `notes.md`, not the
    spreadsheet, which is in `review/` and not in the repository.
  - A name that comes back without its colon is not always the editor
    writing out an abbreviation (APP 53/64/0/-/Kalisz Tab.21, 2026-10-14):
    three were written in full on the page, and the first reading had
    shortened them in error. Look at the picture before writing a note.
  - **A tailed stroke at the end of a name can look like ę.** In the
    hearth-tax register of 1789 (Kalisz Tab.21) the clerk ends a shortened
    name with a looped, tailed stroke; at the end of "Kiedrow" it was taken
    for ę, by the first reading and by the editor, until the editor saw it
    as the sign for -skiego (2026-10-14). Compare such a letter with the
    sign on lines already given as shortened ("Jaroszew:") before reading
    it as a letter.
  - A corrected name can fall out of the English word table (`WORDS` in
    `holding.py`): three did on Kalisz Tab.21 and stood untranslated in
    the English. After `--take`, run `--english` and read
    `git diff --word-diff` of `translation/doc1.yml` line by line.
- **"A clean, archival version of the spreadsheet"** (editor, 2026-10-13)
  is a workbook in the unit's folder, tracked: the table as written, the
  table in English (the editor does not read German headings), and a sheet
  saying what the source is, how it is written down and who read and
  checked it. Values only: no pictures, formulas, check columns or colours
  (`holding.py --archive`).
- **"Update the table to the site"**, said together with their corrections
  and "the folds look fine", was taken as the editor's word to publish
  (2026-10-13). "The site" in the editor's mouth is the live one.

- **An English translation in the editor's folder may be a machine's**
  (APP 53/968/0/-/783, 2026-10-13; the editor: "I'd check the English
  translation to ensure it's accurate"). Read it against the original
  sentence by sentence before using a word of it. There it was wrong where
  the paper turns: "Zapozwałem" (I have summoned) was "I have acquainted
  myself with", a counterclaim's demands were told as things done, "ojcu"
  was "her husband", "dworu" (the manor) "the court", the masculine
  accusative "Bogumiła" a woman five times. Such an English is written
  again from the corrected text, in the edition's terms, and the
  differences that matter go on the page of changes
  (`intake/changes.yml`), since the editor may have written from the old
  one. The signs of a machine: a passage it could not read left out with
  "<...>", untranslated words carried over ("SSrów"), and names put through
  a grammar they do not have.
- **A transcription of print reads like machine recognition and errs like
  it**: "Scbonfisch", "czynszowmkami", "lego" for "tego", "§111" for "§
  III", "11stu" for "14stu", "10/28" for "16/28". Check every figure, date
  and name; a double date of the Kingdom of Poland is twelve days apart,
  which catches a wrong one.
- **A printed form filled in by hand has two texts.** The print is the same
  on every copy; the pen is this copy: names struck out and replaced in the
  margin, letters written over, the server's own lines and signature. Read
  the pen separately and enlarged, and say on the holding's page which is
  which. A struck-out name is left out (the rule), but a name written in
  its place is text.
- **A tax register has no totals, but it has a rate** (APP 53/64/0/-/Kalisz
  Tab.21, 2026-10-13). The hearth tax was so much a hearth, so every
  village's sum is a multiple of the rate (3 zł 15 gr in two districts, 2
  zł 15 gr in the third). Finding the rate from the data and listing the
  lines that do not fit took a minute and is the only witness the figures
  have (`holding.py --look`). Look for such a regularity in any list of
  sums before saying the figures cannot be checked.
- **Receipt numbers place a page.** The file named `017v.jpg` continued
  leaf 9 recto exactly (75, then 76) and could not stand before leaf 18
  (which begins at 58 of another district). A verso has no leaf number: a
  file's name is not evidence. Check that the numbers run on across every
  pair of pages before the pages are named.
- **A table with headings inside it.** A district's name over its entries
  is a row with only the name cell filled; `unitlib.table_of` now keeps
  such a row directly above the first entry in the body. The printed title
  of a table goes into the name cell of the first heading row and becomes
  the caption; the labels of the first two columns stand in the last
  heading row.
- **Row pictures without finding every row**: where the lines are ruled at
  even distances, the first and last line of each page are enough
  (`POS` in that holding's script). The pictures then show two or three
  lines, and the spreadsheet tells the editor to go by the number.
- **Word rules for the English of a list** catch words inside names:
  `\bWieś\b` turned "Nowa Wieś" into "Nowa Village". Anchor a kind-of-place
  word to the start of the cell, and print one example of every kind of
  line before publishing (`scratch` script `en_sample.py` was the pattern).
- **The glossary gate also stops on an abbreviation** in a newly translated
  holding ("JP."): rule it under `excluded:` with the reason.
- **Front matter with a table or with `courtbook`**: the cover is put
  before `[DOC 1]` after the pages are written (`with_cover` in both new
  holdings' scripts); `courtbook.correct` and `write_pages` do not know a
  cover and would drop it.

- **Read a copy against its original before deciding what the copyist got
  wrong** (the editor, 2026-10-15: "It should match the actual table").
  Comparing Breyer's copy with the original table showed that most of the
  "errors" I had listed were my misreadings of his hand: his 4 looks like
  Ч, his 5 has a flat top, his н and п are both a Latin n, and figures run
  across the ruled line. Look at every difference on the photo, correct
  what the hand allows, and keep, as written, only what the hand clearly
  says otherwise. Learn a hand's letter forms from words whose reading is
  certain before trusting a single letter.
- **Never overrule the editor's answer on a name from my own reading of a
  letter** (2026-10-15). The editor had answered Цельмеръ at no. 37; I
  changed it to Цельнеръ because the original table seemed to read so, and
  read the original's four other Zelmers as Цельнеръ too. The editor:
  "there's no Zelner, ever in this project. There's Celmer, Zelmer,
  Zellmer, but all have the -m." Before a name departs from the family the
  edition already knows (people.yml, the editor's answers), check that
  family's spellings; a clerk's м is easily taken for н. If the hand still
  seems to say otherwise, put it to the editor: do not change it.
- **A copy's names follow the original it copies** (the editor,
  2026-10-15: "Don't use Breyer's spelling, standardise it to the actual
  liquidation table"). Where a copyist spelled a name otherwise than the
  original does, the text gives the original's spelling; list what the
  copyist wrote in the holding's notes and say so on its process page.
  **The original is the authority for the figures too** (the editor, the
  same day: "you may have transcribed Breyer's incorrectly, or he might
  have made mistakes"). I had kept a copyist's figures where they differed,
  reading the ruling on names narrowly; when an original exists, compare
  every figure and give the original's.
- **The editor writes a word read with doubt as "nur[?]"**, the word with
  "[?]" after it (and "Polzfu[h?]l" for one letter). Keep their form in the
  text; the English needs a rule that turns it into "[uncertain: nur]"
  before "[?]" becomes "[illegible]" (716's `english716.WORDS`).
- **Answered rows come off a spot sheet** when the sheet is made again:
  their words have changed, so the sheet script can no longer find them.
  Copy the answers file into the holding's `intake/` first and list the
  answered keys in the script (716's `spot_sheet2.ANSWERED`). A note in a
  row without a choice ("Should be Schmechel") is an answer too.
- **When an original turns up for a copy already in the edition**, read the
  copy's doubtful words against it and put them to the editor; do not
  change the copy's text to the original's (Breyer's [паленный?] and
  [тлахтами?] against "наличный" and "плахтами" in APŁ 39/98/0/-/6603).
- **Page ids must read `NNNN_[a-h]`** (`match_scans.py`): a capture
  number of four digits and a side. "000" or "013_014" do not parse, the
  scan mapping finds no images and the build stops in `write_inventory`
  (APŁ 39/98/0/-/6603, 2026-10-15). An archive's scan 001 is page `0001_a`.
- **Two scans of one opening, joined into one page** (the editor: where
  "the text runs across both pages, they should be displayed together").
  Each archive scan of a page in a bound file shows a strip of the facing
  page; cut each at its page edge with the green lines (`EDGES`,
  `courtbook.placed`), then set the halves side by side as the left scan's
  page and move the right half to `_not_staged` (6603's `holding.py`,
  `join()`). Transcribe a line that runs across as one line.
- **A table with totals checks its own reading.** Add the column to its
  total before anything else: on 6603 it confirmed every figure of 97 rows
  and showed which of Breyer's copied figures in 53/968/0/-/716 were wrong.
  Where every row has parts and a total, add each row across and each
  column down: a misread digit then shows in both its row and its column,
  and a clerk's own slip shows in its row only, or against the written
  totals; look at the scan before deciding which it is, and transcribe the
  clerk's figure as written.
- **A table's text rows (a title page, a section heading, a confirmation
  across the foot) are rows with only the name cell**; every one needs an
  entry in the English `CELL`, or it is transliterated as a name.
- **A heading row of units under the column groups** ("Десятины и сажени"
  under six groups) renders under the first group only; put it with the
  group heading above and say so in the conventions.
- **New relation kinds need labels**: `rel_<kind>` in both languages of
  `site/_data/i18n.yml` (6603 added `copies` and `entered_in`).
- **A new archive** goes into `reference/repositories.yml` and the credits
  in `site/_data/rights.yml`; the Central Archives of Historical Records
  had been left out of the credits since its first holding (found
  2026-10-15).
- **A copy takes the date and era of what it copies** (the editor,
  2026-10-14: "a copy of an 1828 document from 1939 should not belong to
  the 20th century"). The first build of 53/968/0/-/716 put the whole
  notebook in the twentieth century, Breyer's copies of 1858 to 1892
  included. Where a copyist's own notes and a copy share a document,
  divide it, give the copy its original's date (or an inferred one with its
  basis, or none) and set its era per document (`documents: era:` in the
  rulings). Renumbering means: the reading, the English keys, rulings,
  summaries, claim record, `about` citations, timeline `refs`, `not_in` in
  `reference/people.yml`, spot-sheet rows, then `relabel_scans.py --apply`
  and two rebuilds (scan labels carry the document number).
- **Page edges on the fold page** (the editor, 2026-10-15): besides the red
  fold line, two green lines mark what is kept of each scan, the outer edge
  of each page or both sides of a single page; outside them is shaded and
  cut away. They are saved as "left" and "right" in pixels in
  `folds_<slug>.json`, read by `courtbook.placed()` and applied by
  `courtbook.cut()`; a holding proposes them with `placed(here, scans,
  EDGES)`. A page cut at the fold alone kept the edge of the facing page
  (716, the last page) or a blank half (the back of the sheet of 1858).
  The court-book holdings get the lines the next time their `--sheet` is
  run; nothing of theirs changes until the editor saves a file.
  `review_folds.py` pages are unchanged (`crop=False`). Test the page's
  script with `node --check` and a stub DOM before handing it over.
- **A spot sheet's answers are saved as `review/<slug>/<sheet>_answers.json`**
  (`readings.csv` gives `readings_answers.json`); only `open_queries.csv`
  uses `query_answers.json`. Look for the right name before saying nothing
  was answered, and copy the answers into the holding's `intake/` when they
  are worked in, as `review/` is not in the repository.
- **On a printed table form, place a spot sheet's pictures by box, not by
  line count** (APŁ 39/98/0/-/6603's `intake/spot_sheet.py`, 2026-10-15):
  the ruled rows of a form do not fall at an even pitch. Find each box on a
  gridded preview, then look at every crop before serving the sheet. On a
  joined, wide page the preview is shorter than it is wide: read the
  position from the grid lines, not from pixels (one crop showed row 5
  for row 4). Say clearly which sheets the editor has had: they asked
  whether they had gone over the original's readings, which had never
  been put on a sheet.
- **"Missing" or "skipped" in a page map is a claim, not a fact** (Oe 1 Bü 9454,
  letter 9, 2026-10-15). The map said "no document to scan" and the corpus held
  "(skipped)", yet the archive's processed folder had the page, a damaged leaf
  with eighteen lines. Before treating a number as lost, open its scan. The
  holding's method for a letter added later is `intake/scripts/letter_9.py`
  (after `rescan_245_289.py`): text from the editor's file and the scan, the
  date, place and writer rulings, the reading record and the summaries in one
  script run once; the English as `intake/translation/doc<N>.yml`.
- **The paid run's reading notes are a witness worth reading before re-reading a letter**
  (9454 letter 300, 2026-10-15): `reading.json` (doubtful_words) and the translation cache
  (`emendation_suggestions`, `flagged`) had suspected gerüffelt, zurück and kömt, and the new
  crops confirmed all three. They are not evidence on their own, but they say where to look.
  After re-making a letter's text, update its reading record: claim lines below an inserted
  line move, and settled doubtful words come off (`recrop_300.py`, `reading_record`).
- **The edition's "marks of doubt" count includes "[...]"** (lost text):
  `dataset/index/uncertainties.json` is the number the essays give. Recount
  from it, not with a regex for "[word?]" alone.
- **Checking the pictures of a spot sheet is a second reading.** On
  53/968/0/-/716 it showed a word read without doubt that looks otherwise
  (Вдовьiй / Вельскiй) and a word broken across two lines that was
  transcribed on one. Put such finds on the sheet as rows of their own.
- **The era bands on the timeline are fixed years** in
  `site/_includes/timeline.html`, and a band only shows on a year the
  timeline shows (one with a document or an event). When documents of an
  era are added earlier than its band, or an era's dates change, move the
  band to the era's first shown year: 2026-10-15 the Włodzimierz band went
  from 1860 to 1858 (the tax sheet) and the twentieth century's from 1936
  to 1935, though the era itself begins in 1851 (Michalina's death, a year
  with no document).
- **Dates the editor gives for people** go into `reference/people_bios.yml`
  (`life`, and a sentence in both languages, with a comment naming the
  editor as the source) and the person's `identity` in
  `reference/people.yml`; an owner's dates also into the era's `ownership`
  and blurb (`reference/eras.yml`), the timeline note (`i18n.yml`) and the
  story's era heading.
- **Moving documents to another era, or making two eras one** (2026-10-20,
  the liquidation into Włodzimierz Miączyński's years). The era is set in
  a holding's `unit.yml` (`era:`) and per document in its `rulings.yml`
  (`documents: era:`); `grep` both for the old slug. Then
  `build_db.py --unit <slug>` for each holding changed, `merge_corpus.py`,
  `build_dataset.py`, `build_site_data.py`: `build_site_data.py` alone
  still counts the old eras, since it reads the era from the corpus. By
  hand: `reference/eras.yml`, the band in `site/_includes/timeline.html`
  and its note in `i18n.yml` (both languages), and the era's section of
  the story page in both languages (heading, count, span).
  `site/_data/eras.yml` gives the new count to copy.
- **A notebook in three languages, divided by content** (APP 53/968/0/-/716,
  2026-10-14; the editor chose "by content" over one document). A page that
  ends one document and starts the next stands under both (`DOCS` in
  `intake/text716.py`); a document's place and date come from its own
  lines, so a note with no place of writing needs `places: overrides: ""`,
  or its last line is taken for one.
- **Tables in a notebook do not keep the shape of a printed register.** The
  title can stand on the page before the entries, the totals on the page
  after them, and a heading can be one row of column labels. `unitlib`
  now records the pages of the heading and of the closing rows
  (`head_pages`, `foot_pages`) and shows them where they stand; a heading
  row that holds only a title goes into the caption; a single row of labels
  is one heading row, not a title. Before that, the title of the Łazińsk
  table and its totals page were missing from the table view, and the
  English publish stopped (`KeyError`). The other tables render byte for
  byte as before: compare `render_table` against `git show HEAD:pipeline/unitlib.py`
  for every table page after any change to it.
- **An English table cell with a figure inside words** ("To the landowner
  4420 roubles 53 kopecks") must be quoted in the CSV: the house forms make
  it "4,420" and the comma splits the cell, so the English no longer has
  the German's shape and is published as plain text. 716's `english()`
  quotes such cells.
- **Summaries of a copied table** (716): say what the table says. The first
  draft added from the edition's knowledge that the table "gave the
  peasants their land after the emancipation of 1864" and that Łazińsk lay
  on the Trąbczyn estate; that belongs in the holding's description. Count
  the rows, not the last number (numbers are skipped and doubled), and add
  up a column before quoting its total: Breyer's own sum on one page was 6
  Morgen out, and the summary says so. Do not give a German form of a name
  that the English transliterates from the Russian.
- **The page check of `about.md` reads only the first of two adjacent
  citations** (`[[5]] [[6]]`): figures from the second are reported as
  missing. Cite the one document that holds them.
- **The edition guide's page figure** is kept by adding each new holding's
  pages, a page shared by two documents counted once (716: 34). The
  build's "manuscript pages" counts such a page twice and is not the
  guide's figure.
- **Spot-sheet pictures for a holding whose pages stand under two
  documents**: find the corpus line within the document and the page, and
  place the picture by the line's place in the page (716's
  `intake/spot_sheet.py` used `transcriptions/<page>.txt`, removed
  2026-11-23; the page's lines are in `dataset/units/<slug>/letters.json`,
  `pages[].diplomatic`). Where the page has two columns or a
  heading in large script, set the picture's box by hand (`BOX`). Look at
  every picture before serving the sheet: 5 of 17 needed moving.

- **A transcript "of these pages" may cover only parts of them** (ADWł 85,
  2026-10-15). The editor's file named nine leaves, but left out the souls
  of the parish, a small table, half of two pages and the foundations of
  1668 to 1694, some of the most useful passages. Before building, look at
  every page the transcript names beside it and list what is not there; put
  that to the editor in one question with a sentence on what each gap holds
  (they chose to have the gaps transcribed in session). Say which passages
  belong to another document of the volume and are left out.
- **The editor's expansions of abbreviations are readings too.** Their
  Polish wrote "JWo Mści" as "Jego Wysokość Magnifici" (it is Jaśnie
  Wielmożnego Mości) and "JKMci" as "Jli Magnifici". The edition gives
  abbreviations as written (EDITORIAL_RULES), and the English renders them.
- **A table without numbered rows cannot use the site's table view**:
  `unitlib.table_of` takes an entry to be a row with a number in its first
  cell. ADWł 85's population tables, two of them inside a page of prose, are
  lines of text with cells parted by " | "; process.md says so.
- **Before adding `not_in` to a person or place entry, read the whole
  entry.** Swięcia already had one; the second key silently replaced the
  first in YAML, and the false hit stayed. Put the new document into the
  existing list.
- **A catchword that is only the end of a broken word** ("te=" at the foot
  of leaf 29, "raz" below it, "teraz" overleaf): the line-break pass joins
  "te-" and "raz" and the reading text says "teraz" twice. A line in the
  holding's `catchwords.yml` (drop: line) settles it.
- **A word with a second sense in an old Polish document**: "komornik" is a
  court officer in the glossary and the termbase, but "trzech Komornikow"
  on a clearing are landless cottagers. Narrow the pattern (count its hits
  first) rather than let the definition attach.
- **"tymże Dekretem" refers to the decree named last.** The land and tithes
  after the inn of 1694 belong to the decree of 1694, not to that of 1692;
  the first draft of the holding's page had them wrong.
- **The story page's era headings are written by hand** ("92 documents,
  1589 to 1788"): two holdings had been added to the Prusimski era without
  it changing. The count and span are in the generated
  `site/_data/eras.yml`; copy them from there after adding a holding to an
  era, and read the era's blurb in `reference/eras.yml` too.
- **An archive with no website of its own** (the Diocesan Archive in
  Włocławek): `url: ""` in `reference/repositories.yml` and
  `site/_data/rights.yml`; `site/_includes/rights_archives.html` names it
  without a link.

- **A script that applies answers to several files checks them all before
  writing any** (ADWł 85, 2026-10-16). `spot_answers.py` wrote the Polish,
  then stopped on a pattern in the English, and could not be run again. And
  quote a word, not a phrase: the texts in `text85.py` are Python strings
  wrapped across lines, so a phrase may span a line break and match nothing.
- **Run `check_translations.py` after `pipeline/regenerate.py`, not before.** Run on
  the old `dataset/letters.json`, it reported five false marker-count rows
  for marks the editor had just settled.
- **A note without a button can carry the answer** ("Maybe Ułazwany, if
  that's a word?"). Read it against the hand: this scribe's ł is a t with a
  bar, so it was "Uła" and the separate word "zwany", kept with its doubt
  because the editor was unsure. Say in the report how it was taken.

- **A holding from print, not from an archive** (Kuryer Polski 1754, nr 75,
  2026-10-16; the editor means to add more newspaper items). The library
  is a repository like an archive (`bkpan-kornik`); the reference is its
  shelfmark and the issue, and the digital library's link goes in
  `scan_source:` and the holding's page. Transcribe only the item, from its
  dateline, line by line as printed, with the printer's letters (ſ, ß, æ,
  á). Date it by its own dateline and place it where it was written; the
  issue's date is said in the rulings and the page.
- **The line-break pass does not know words spelt with the long s**: it
  split five words of the newspaper that the print breaks with a hyphen
  ("Pru¬ſińſkich", "Gło¬wiecki"). Read `linebreak_decisions.csv` after the
  first build of any text with ſ and rule such rows `join` by hand (they
  are kept as "held"). The name matcher, by contrast, reads ſ as s.
- **A summary never rests on a word read with doubt**: the first draft of
  the newspaper's summary named "the secular clergy" from "[Cleri?]". It
  was cut, and the claim check says so.
- **Before a place pattern goes in, read every hit**: Ląd (from the print's
  "Łędzki") also found "konwent Lądzki" in the decree of 1775 and "Kloster
  Ląd" in two other holdings, all right; a looser "L[ąa]d" would have
  needed checking against Polish "ład".

- **A holding with no images** (the Kodeks Dyplomatyczny Wielkopolski,
  2026-10-16: the digital library has only an electronic text). The
  pipeline takes it: each document is one page with an id and no image.
  `match_scans.py` failed on a holding with no captures at all and now
  says so instead. A document with a `citation:` (below) says in the image
  pane that it comes from a printed edition and has no page image, and its
  by-paragraph note says "the whole entry of the printed edition".
- **`documents: citation:` in rulings.yml** gives a document's place in a
  printed edition that holds many ({work, volume, number, page, url});
  `build_site_data.citation_of()` writes it into the page's front matter
  only where there is one, and the page shows it under the place, linked
  to the volume. Added for the Kodeks, whose entries come from many volumes
  and whose numbers restart in volumes 5 and 6.
- **A holding set up before its documents exist is kept off the site** by
  naming its settings `unit.yml.draft`: every folder with a `unit.yml` is a
  holding to the build, and an empty one would show on the Sources page.
  Likewise an era with no documents: keep its entry as a script until then.
- **Try a new kind of holding end to end with one sample document**, then
  take it out: `git checkout` the generated files (dataset/, site/_data/
  except i18n.yml, site/assets/), delete the sample's generated files, and
  rebuild to see that nothing generated differs from HEAD.
- **The Wielkopolska Digital Library** serves a volume's electronic text at
  `https://www.wbc.poznan.pl/Content/<id>/download/`, and answers a burst
  of requests with a 1.7 KB "High Load" page with status 200: check the
  size of every download.
- **Footnotes of a printed edition** (the Kodeks, 2026-10-16). The marks
  stand in the electronic text glued to their words ("Mezeconis1",
  "Zagorowo,1)"), and the text is not to be changed. `units/<slug>/
  footnotes.yml` records each mark as a piece of text with the mark in
  braces (`"Mezeconis{1},"`) and each note line by its start (`"{1}Mieszko"`);
  `build_site_data.footnote_html()` raises them on the site, and both
  verifications (build_site_data's and `pipeline/verify_site.py`, `FN_MARKUP`) strip
  that markup before comparing the text. A mark with no note, or a note
  with no mark, goes under `unmatched:` with the reason. The holding's
  `intake/check_footnotes.py` checks every mark and note is found once.
- **The figures of a medieval holding are years** (2026-10-16). The
  reading text and the English group four-digit numbers by thousands
  unless they can be a year, which `pipeline/numerals.py` took to mean 1500 to 1999:
  the Kodeks's 1411 became "1,411". A holding whose documents are older is
  named in `numerals.YEARS_FROM` (`kdw: 1100`), and the slug or document id
  is passed down (`build_pages(slug=)`, `english_forms.apply(pad=)`).
  Lowering the floor for everyone was tried and is wrong: it took the
  commas out of sums such as 1,302 in the tables of the 1860s. After any
  change there, compare the reading text and `site/_data/translations/`
  with a copy taken before, and see that only the intended holding moved.
- **Medieval spellings of a place** go in `reference/places.yml` as a
  `medieval:` list of "year: forms" (the editor: "1252: Trupcino"); the
  build copies them into `site/_data/estates.yml` and the Places page shows
  them as "Medieval: ...". Collect them from the documents' Latin, not the
  editors' notes.
- **A long-tail name the index finds by itself** (name_seeds) can be shut
  out of a document with `seed_not_in:` at the top of
  `reference/people.yml` (`{Otto: [kdw-19]}`), where the person has a full
  entry of their own in that document.
- **A case ending can cross from one place to its neighbour**: Wrąbczyn's
  pattern also caught "Wrąbczynka", a form of Wrąbczynek; the patterns now
  exclude each other's endings (`(?!ek|k[aui])`). With two places whose
  names differ by a suffix, read the hits of both.
- **An editor's note can be wrong where the text is plain**: the Kodeks's
  note puts "Magna Wronczino" (1418) in the district of Poznań, but the
  document sets it between the abbey's estates of Great Wrąbczyn and
  Zagórów. The note stays as printed; the tag follows the text, and the
  summary and the holding page say so.
- **A document the editor chose that gets no estate tag is a question,
  not a ruling** (the Kodeks, 2026-10-16). The gift of 1243 named none of
  the sixteen estates on the editor's list and was left untagged; the
  editor then said Imielno, among its villages, "should have been on the
  list of estates in focus". The editor's list is not closed: when a
  chosen document matches none of it, read its places against the
  holding's neighbourhood (Imielno is Łukom's neighbour in the decree of
  1775) and propose the place before building.
- **The translation check's flags on a Latin holding are mostly noise**:
  footnote numbers of 10 and more become superscripts (¹⁰) and read as
  "numeral missing", and the German termbase catches Latin words
  ("Dominium", "Johannis"). Read them, and say in the report that they were.

- **A work about the sources is literature, not a holding** (the editor,
  2026-10-20: "Literature definitely has its own page! Don't touch the
  Sources page, that's for primary-source material from archives"). When
  the editor gives a "literary source", it goes into `literature/<slug>/`
  (docs/LITERATURE_PLAN.md), never `units/`. A desktop session that had not
  fetched GitHub built Pachoński 1973 and Mączak 1968 as holdings; they were
  moved the same day (section "The literature", below). **Fetch and compare
  with `origin/main` at the start of a desktop session** (`git fetch`,
  `git rev-list --left-right --count main...origin/main`): the cloud sessions
  may have built what the editor is about to ask for.
- **Glossary entries take `not_in`** (a list of document uids), as people
  and places do (`glossary_build.py`).
- **`courtbook.write_summaries` left a blank line, and no final newline,**
  when the holding's slug sorted after every other in the summary files.
  Fixed; read `git diff` of `site/_data/summaries*.yml` after writing
  summaries for a new holding.
- **"Nowa Wieś" is a common place name** (the editor, 2026-10-20): before any
  link or index match names a Nowa Wieś as the Trąbczyn estate's, make sure
  the text means that village (Konin Gr.136 inspects it with Trąbczyn,
  Osiny and Łazy). The place index matches the name only where it is certain
  (`reference/places.yml`, `nowawies-trabczyn`). The same care for any
  common name (Łazy, Osiny, Wola).
- **A new holding needs `pipeline/regenerate.py --unit <slug>` twice after
  `relabel_scans.py --apply`**: its database step runs before the scan step
  refreshes `page_scan_map.csv`, so the first run keeps the unlabelled image
  names and `pipeline/verify_site.py` fails on broken `/assets/scans/` links. Make
  `review/<slug>/` before the first run (the line-break report fails
  without it).

- **Pages named by the editor are the archive's pencil pagination**
  (APP 53/1455/0/2/21, 2026-10-21). A volume photographed page by page can
  carry three numbers at the top corner: the archive's in pencil, an older
  one in red crayon, a third struck out. The editor's "pages 13-14" were the
  pencil numbers; read them off every photograph (turned upright, the top
  corner enlarged) and map photograph to page before cutting anything. The
  editor's own cropped .jpg files in the same folder were other pages
  (5, 6, 18-20, 54): do not take a file in the folder for a chosen page
  without reading its number.
- **"Trim what belongs to other sections" on a copy-book page**: cut the
  picture and the text at the heading of the first entry that begins on the
  page (find the gap by the ink in each row, then look at the cut line drawn
  on the picture: a first guess cut through a heading twice). A page that
  lies wholly inside an entry is given whole. An entry that begins on a
  chosen page and runs on to one not chosen is kept as far as the page goes,
  as its own document, undated if its date is on the next page, and the
  next page is offered.
- **A name swap by regular expression also rewrites the sentences that quote
  the old form** (2026-10-21): replacing Gradziem with Grądzyń everywhere
  turned "the copy's "Gradziem" is Grądzyń" into "the copy's "Grądzyń" is
  Grądzyń" in five comments and notes. Protect the quoted forms, or grep for
  the new form in quotation marks afterwards.
- **Read a whole entry before saying what it is** (APP 53/1455/0/2/21,
  2026-10-21). No. 16 was first described from its heading and its first
  lines as the king's confirmation of the sale copied before it (1461);
  the page that finished it, added later at the editor's word, showed a
  confirmation of 1447 of an earlier purchase of the same land. A heading
  names the matter, not the deed: an entry given only in part is described
  as a beginning, with no relation or summary claim that rests on its
  unread rest.
- **When another session has left the folder on its branch with work not
  committed**, make your change in a separate checkout of `main` (`git
  worktree add ../vonTriebenfeld-main main`), copying in the cache files
  your step needs (`cache/translation-raw/<slug>-*.json`), and remove the
  checkout when done. Rebuilding in the shared folder would put the other
  session's half-built holding into your generated files. **`pages/` is not
  in the repository**: a fresh checkout has none, and `pipeline/regenerate.py --site`
  then rewrites every holding's `page_scan_map.csv` with empty images
  ("gap"). Copy the whole of `pages/` in, or run only `--unit <slug>` and
  the later site steps there, and look at `git show --stat` before pushing
  (2026-10-21: caught and restored before it left the machine).
- **A holding from raw camera files cuts its own pages.** `courtbook.cut`
  opens the scans with PIL, which cannot read a .CR2; the holding's
  `intake/holding.py` takes the full-size JPEG inside each file
  (`units/app539680669/intake/photos.py`, `preview()`), turns it and cuts it
  to a box (`BOXES`), and handles `--crop` before `courtbook.holding_main`.
  Page ids must look like `0013_a` (four digits, a letter): `stage_pages`,
  `relabel_scans` and `match_scans` read only names of that form.
- **A note in the margin has its own label** (2026-10-21): list it in
  `units/<slug>/margin_notes.yml` (the shape of `sideways.yml`); the site
  sets it apart under "Written in the margin", and the English page gives it
  after a paragraph `[Written in the margin:]`, as the office notes have
  theirs.
- **`publish_translations.py` deletes the translation file of a holding that
  no longer exists**: on 2026-10-21 it removed
  `site/_data/translations/pachonski1973-001.yml`, left over from Pachoński
  before it became literature. It was restored (`git checkout`); a
  deletion of another holding's file is not the new holding's business, so
  check `git status` for a `D` after publishing, and ask before letting it
  stand.
- **Another session may be building a holding in the same folder** (an
  untracked `units/agad118501169/` on 2026-10-21). Commit only your own
  holding's paths, never with `git add -A`. Its half-done work can stop
  `pipeline/regenerate.py --site` (a literature index with hits not yet ruled, a
  file locked while it rebuilds): run `build_site_data.py`, the Jekyll
  build and `pipeline/verify_site.py` directly, and leave the generated files that
  carry its work (`git diff | grep` its slug) unstaged.

## Merging a cloud branch on the desktop

Done on 2026-10-13 for `claude/peaceful-meitner-snu6qx` ("merge the other
cloud branches").

- **See first which branches have anything.** `git fetch --prune`, then for
  each remote branch `git rev-list --count main..origin/<branch>`. Of four
  cloud branches one was ahead of `main`; the other three were already in
  it.
- **Conflicts fall in the generated files** (`site/assets/cards.json`,
  `search-index.json`, `site/_data/glossary.yml`, `glossary_hits.json`),
  because both sides rebuilt them, and in "Where things stand" in
  `CLAUDE.md`. Take the desktop's copy of the generated files
  (`git checkout --ours`) and let the rebuild write them; settle
  `CLAUDE.md` by hand.
- **Before any rebuild, bring the desktop's cache up to the cloud's work.**
  The cloud cannot write `cache/`. For summaries written there, run the
  holding's `intake/summaries_draft.py` on the desktop: it writes the cache
  files as well, and leaves the committed files unchanged (check with
  `git status`). Corrections to the English made there are in
  `reference/english_corrections.yml` and survive a republish.
- **Then rebuild each holding the branch touched** (`pipeline/regenerate.py --unit
  <slug>`), the site once, and read `git status` for files of any other
  holding.
- `relabel_scans.py` reports three labels to update in Oe 1 Bü 14526
  (scans 0167 to 0169, from the merging of documents 30 to 32). It has said
  so since that merge, the site checks pass with it, and it was left alone.

## Traps in this shell (2026-10-13)

- **An FFT NCC over a big image wants float64 integral images** (2026-11-06,
  the bulk maps' correlation work). The Lewis-method matcher's local sums
  through `np.cumsum` in float32 lose hundreds of absolute accuracy over a
  31-Mpx image; the near-flat regions then get `var_f ≈ 0`, the clamped
  denominator turns the NCC into a huge spurious peak (>1), and the match
  silently lands in white margin. The formula itself is the exact one
  (numerator = plain correlation − t̄·(local sum), denominator from the
  local variance), the trap is only the accumulator's dtype: cast the image
  to float64 before the cumsums, and zero out positions whose local
  variance is below 1e-4·n. A flat-template guard (`var_t < 1e-4·n` → all
  zeros) keeps white-margin templates from matching anything. The
  self-match check (a content patch against the whole, peak at 0,0 with NCC
  ≈ 1) catches both this and the numerator form's errors — run it before
  any score is believed (the standing rule, "Correlation matchers").
- **A georeference made on one version of a map cannot be transferred to
  another version — and the tell is the total correlation failure**
  (2026-11-06, Gilly 1802). BII.jpg matched neither of the folder's other
  Gilly images nor any warped tiles, at every scale and turn of
  translation-only search, while the matcher itself was proven on a
  self-match: not a tooling miss but a fact about the images. The editor
  confirmed it: the MapWarper reference was made on a different version.
  Two lessons: (a) when a correlation "cannot fail" yet finds nothing,
  suspect the VERSION before the method — re-engraved states of one map do
  not correlate; (b) before concluding anything, search ROTATION as well as
  scale: old survey sheets are commonly drawn with the meridian tilted
  (Gilly's sheet sits at ~16 deg), which no translation-only search can
  bridge. The joint search (rotation every 5 deg at a coarse frame, then a
  fine pass) found the match at once. Scale ranges must be reasoned from
  the images' coverage — a wrong guess about what a scan spans sends the
  search to the wrong octave entirely (the first pass searched k 0.3-0.6
  when the answer was 0.65 on another frame).
- **A lunaroute URL fetch happens server-side: localhost is unreachable**
  (2026-11-06, the Mapa dróg OCR). The converter's `url:` parameter is
  fetched by the backend, not by this machine — a `http://127.0.0.1:8781/...`
  crop URL fails with fetch_failed even while the server answers locally.
  Code Mode has no filesystem access either, so base64-through-context is
  the only converter route for local images (too heavy for a batch). The
  better tool was there all along: **the Read tool presents images to the
  session** — for a batch of small crops (label bands), reading them
  directly beats any OCR pipeline, with the extra check of the editor's own
  standards to read each result against.
- **The rotated file of Zagórów 1841 is a different version — five probes,
  no content transfer** (2026-11-06, the editor's ruling to use 001.jpg "so
  that we can work with the straight map and not the one at a weird
  angle"). The MapWarper 75688 points live in the rotated derivative's
  pixels; transferring them needed the rotated→orig transform, which five
  independent methods refused to find: (1) whole-image template match at
  the consensus angle (330°/scale 1): peak −0.45; (2) patch NCC at the
  SIFT consensus's own inlier positions: 0.05–0.26; (3) template matching
  the whole rotated file inside the rotated canvas: peak −0.45; (4) the 11
  GCP patches searched over all of 001.jpg at all angles and scales: 9 of
  11 collapsed onto ONE generic location with scattered angles; (5) the
  SIFT model itself (5328 inliers, RMS 0.17 px, rotation 30.2°, scale
  1.00000) mapped a control point into the original's white margin — a
  lattice consensus of the map's regular hatching, right rotation,
  arbitrary phase. The lesson stack: a repetitive-texture image defeats
  RANSAC's global consensus (thousands of identical glyphs agree on many
  rigid models); SIFT's inlier count and RMS prove NOTHING about
  photometric correspondence — verify with patch NCC at inlier positions
  before believing any transform; and when "the rotation is right but the
  phase is wrong" survives every check, suspect the VERSION first (the
  Gilly lesson, met twice in one sitting). zagorow1841 is now registered on
  001.jpg (8916 × 5470, the map as drawn, its tilt to be carried by the
  georeference) with no MapWarper points; it georeferences from the
  editor's marks alone.
- A heredoc in the Bash tool fails on an unbalanced apostrophe even when it
  is quoted. Write any script that holds prose with the Write tool and run
  the file.
- A heredoc also eats backslashes and turns "\'" into "'" (2026-10-16):
  a Python patch with regular expressions or escaped quotes, sent through
  a heredoc, half-applied twice in one sitting. Use the Edit tool for such
  changes, or Write the script whole. Again on 2026-10-23: a Windows path
  in a heredoc'd Python patch lost a backslash, and "\1" became a control
  character in reference/maps.yml. Paths in data files use forward
  slashes, which Python and PyYAML read on Windows.
- **`pipeline/regenerate.py` has no `--help`**: it ignores unknown arguments and
  rebuilds every holding (it was started that way by mistake on
  2026-10-16 and stopped; nothing tracked changed). Read its docstring
  instead (`--unit <slug>`, `--site`).
- The session's scratch folder can be withdrawn in the middle of a sitting.
  One-shot scripts worth a second look go into `scratch/` at the project
  root, which git ignores.
- **PyYAML missing on the desktop Python** (2026-10-19): `import yaml`
  failed under `C:\Program Files\Python312`, because APPDATA is empty in
  this shell and Python looks for the user's packages in the wrong place.
  `python -m pip install --user pyyaml` mended it.
- **archive.org through curl** needs `--ssl-no-revoke` on this machine
  (the certificate check fails otherwise).
- **Building the site on the desktop** (2026-10-19): Ruby is scoop's
  (4.0), and the gems were not installed. `bundle install` failed the
  certificate check against rubygems.org (the network re-signs TLS, as
  with curl above). Mended without turning the check off: the Windows
  root and CA stores exported to `scratch/windows_roots.pem`, then
  `SSL_CERT_FILE=../scratch/windows_roots.pem bundle install` in `site/`.
  Builds then run with `bundle exec jekyll build`; the warnings "already
  initialized constant Gem::Platform" are harmless. A build takes one to
  four minutes. If `scratch/` was cleared, export the stores again
  (PowerShell, `Cert:\LocalMachine\Root` and `CA`, as Base64 PEM).
- **The browser tools can hang on the desktop** (2026-10-19: opening and
  screenshotting a local page were cut off twice). Serve `site/_site` with
  `python -m http.server` for the editor to look at, and check the built
  HTML from the shell (counts of sections, leftover markup) rather than
  waiting on a screenshot.
- The heredoc trap with backslashes (above) was hit again on 2026-10-19,
  in a patch to `literature_site.py`. There is no small exception.
- **A stray `struct.py` in the temp folder breaks Python** (2026-10-21):
  `%LOCALAPPDATA%\Temp\opencode` carries scripts left by earlier sittings;
  run from that folder, a `struct.py` there shadows the standard-library
  module and `import zipfile` (so PyMuPDF) fails with "module 'struct' has
  no attribute 'calcsize'". Run repository scripts from the repository (the
  working directory), not from the temp folder; or move the helper into the
  repo's `scratch/`.
- **archive.org's IIIF crops are flaky** (2026-10-21): region requests for
  one item answered 500 and 504 over and over while whole-page downloads
  came through. When the editor has supplied the PDF or the images, render
  them locally (PyMuPDF `get_pixmap(dpi=300)`) and crop locally — steadier
  and faster than the server.
- **A Google scan's djvu OCR can mislead badly** (2026-10-21, Janocki's
  *Ianociana*, 1779 Latin): "1636, et 1643, 13" for "et 1642, 12" (the 12mo
  mark), "COMITIGRUM" for "COMITIORUM", "1737" mangled. The Jagiellonian
  Library's copy of the same edition (`jbc.bj.uj.edu.pl.NDIGSTDR019959`) has
  a cleaner tesseract OCR and settled every doubtful spot. When an
  archive.org Google scan must be read, look for a second library's copy of
  the same edition first.
- **An image read is not remembered long** (2026-10-21): the harness keeps
  only the most recent image reads; a reading not written down at once is
  lost and must be fetched again. Transcribe or note what a page shows
  immediately, before the next tool call.

## The literature (2026-10-19)

- **The literature page lists the works by author** (the editor,
  2026-10-20): the author surname first (`author_sort` in `work.yml`,
  "Breyer, Albert"; brackets for an attributed author; empty for an
  anonymous work, listed by its title as "Anonymous"), then the title as
  printed with the English title in italics under it, then where it was
  published, then its language. No separate "Author" line and no short
  citation in the list (the work's own page keeps them). A new work needs
  `author_sort`.
- **Pictures in a work** (2026-10-20): `figures:` in `work.yml` maps a page
  key to a file in `site/assets/literature/<slug>/`; the page's picture
  stands above its text. Pachoński's map, Mączak's map and chart, and the
  80 photograph pages of Szwiec's catalogue.
- **A work printed in English** (`language: en`, Mączak 1968) has no
  `english.md`; its page shows the one text without the buttons.
- **Tables with cells across two columns**: write them in `original.md` as
  one-line HTML tables with `colspan` (kramdown has none).
- **A PDF printed from Word has a usable text layer** (Szwiec 2009); a PDF of
  scans has OCR, which is not the text (Mączak 1968). For the first, a
  script that rejoins the justified lines and tells notes from captions by
  their raised marks (`pipeline/literature/szwiec_pdf.py`), checked by
  counting the words against the PDF's own text. For the second, read every
  page from images at 300 dpi and compare the reading with the OCR word by
  word (it catches a dropped line). In small type at about 150 dpi the
  stroke of "ł" can vanish.
- **A new work's index hits can be taken by old rulings**: a ruling is per
  name and spelling across every work, so "Venise: no" (a book title in the
  PSB) silently dropped 69 Venices of Pachoński 1973. After
  `literature_index.py --sheet`, read the new works' hits under rulings
  that say "no", not only those with none.
- **A modern work is in copyright**: say so to the editor before it is
  published; the Licences page (`site/rights.md`, `site/de/rechte.md`) says
  the modern works on the Literature page are outside CC BY.
- **A scanned journal with spaced-out OCR** (Wąsicki 1953): rebuild a draft
  from the characters' positions (PyMuPDF `rawdict`; a gap wider than a
  third of the type size is a space), then read every page from its image
  in two halves and correct the draft. Half pages at 300 dpi are readable;
  thirds are not needed. The PDF may hold tables printed sideways over a
  spread and a fold-out sheet with a blank back: turn the pages upright,
  key the fold-out "[p. unnumbered]" (it becomes "<page>-u1"), and show a
  table too wide to transcribe faithfully as a picture, saying so in the
  work's notes.
- **Look for the book's own PDF before using a Word conversion of it**
  (Chodyła 2015, 2026-10-21). The editor gave a ".docx.md" of the book:
  no pages, note numbers run into the words ("przywilejami1"), notes at the
  end, broken tables, slips of its own. The Books folder held the printed
  book as an InDesign PDF, whose text layer is the book's text with the
  printed pages and the notes on their pages. Build from the PDF and check
  the result word by word against the editor's file (difflib over the
  words, body and notes apart); say in the notes which was used and why.
- **Traps of an InDesign PDF** (`pipeline/literature/chodyla_pdf.py`, its
  docstring has every rule): note marks carry the superscript flag, but two
  were printed in the text's own type (set by hand), and a raised "2" is
  also "km²", so take marks only in the order of the notes; a few letters
  are set at 0.1 point and do not show in print ("B|ü|sching"); a note's
  continuation line can start with a title set larger than the note (count
  everything in small type below the page's first note as notes); a
  caption beside a portrait falls into the paragraph unless captions are
  held out; text set round a picture starts further in and is not an
  indent, and neither is the second line of a hanging point ("5)" and a
  tab); a word divides over two pages, and an italic runs over a page end;
  in a ruled table (PyMuPDF `find_tables` reads them) one PDF line can
  cross two cells, so assign words, not lines, and read sideways headers
  left to right. Compare every table page with its picture.
- **The tool input turns "\u00a0" and "\t" into the raw characters**, in
  Write, Edit and a Python heredoc alike (2026-10-21): the script got a
  literal no-break space and a literal tab inside its regexes. To write an
  escape into source, build it in a script with `chr(92)`, then grep the
  file for raw tabs and no-break spaces.
- **Read a new book's hits under the old "yes" rulings too** (2026-10-21,
  again): "Poniatowskiego: yes" (Prince Józef) took Chodyła's King
  Stanisław August, and the family pattern "Przespolewski", with no word
  end, matched the colony's name "Przespolewskie Ol." in 30 places.
- **A modern book's details checked against the edition's documents find
  differences** (Chodyła's note 34): the owner in 1860 and the date of the
  sitting of 1782 both differ from the documents the book itself cites.
  Read every figure and name the book takes from a record the edition
  holds before a link is written (HOUSE_STYLE, "The documents first").
- **A book's note can point to the wrong record** (Chodyła 2015, p. 28):
  it gives the inspection of 1754 twelve Olęders and an inn in the wood
  Lusina, under a note citing that inspection; the inspection has neither,
  and they are in the act of 1771. And a table of sums of money is not a
  table of hearths: the book's hearth counts for 1789 are its own
  reckoning. Read the cited record for every statement a link repeats, not
  only the quotation.
- **Heredocs eat backslashes** (again, three times on 2026-10-20): a Python
  edit with a backslash inside a quoted heredoc (a regex escape, a group
  reference, an escaped quote) changed the code it wrote. Use the Edit or
  Write tool for code with backslashes.

- **The repository is public: committing a file publishes it**, whether or
  not the site shows it. The editor chose to keep Seidel's book (2018,
  under copyright) in it for questions, with no page on the site
  (`visible: false` in its `work.yml`). Every page of the site that lists
  the literature must skip such a work.
- **Write the account of a book from the book, not from memory.** The
  first accounts of the six works, written from general knowledge, had
  wrong pages, a wrong subject for Held's book and claims about Guradze
  that the text does not bear out; each was put right by reading the
  pages. A page number in an account is looked up in the passage files.
- **Triebenfeld's entry in the black register is not about Trąbczyn**
  (Materialien pp. 162-164; Piotrow, Lasky and others). A question about
  the value of his estates must say which estates it means.
- The editor's file names are not to be trusted for the language or the
  year: "(French)" of Paciorkowski is the Latin, "1918" of Guradze is
  1898. `blackregister.txt` in their folder "Books" is pages 140 to 171 of
  the Materialien and was not brought in twice.
- **The Neue Feuerbrände numbers its pages from 1 in each part**: its
  passages are keyed `<part>-<page>` (`3-133`), and the build script finds
  a new part where the numbers fall.
- The English of these books is Claude's and uneven in places (Guradze's
  is weaker than the German): an answer that rests on a passage is read in
  the original.
- **The site renders the books with kramdown, not GitHub Markdown**, and
  that matters for text it was not written for: any line with a "|" in it
  is taken for a table row ("**16|38.**" in the Materialien became a
  table), single line breaks vanish (the German lists ran together), a
  name printed as asterisks ("v. ****d") becomes emphasis, a four-space
  indent becomes code, and Jekyll cuts an "excerpt" inside a `{% raw %}`
  block and warns. `literature_site.py` deals with each (its docstring);
  a new work with a new kind of markup is checked in the built page:
  `<pre>`, `<table>` against the source's table lines, leftover `[^`.
- **The edition's index matches wrongly in books** (the index over the
  literature, 2026-10-19; LITERATURE_PLAN.md, section 8): of 2,690 hits,
  182 were wrong. The patterns were made for letters about the estates, and
  books use the same names for other things: words ("Sommer", "Kuh",
  "Gärtner", "Götzen", "Löwin" the lioness), measures ("Berliner
  Scheffel"), regiments ("Grevenitz", "Zastrow"), and other men of the name
  (Danckelmann, Raumer, Hoym's cousin). So every pair of name and spelling
  is ruled in `literature/index.yml` after reading its hits, and a
  ruling's exceptions name the passage. Read the person's description in
  the book before saying who he is: a first draft called the Regierungsrath
  Grevenitz "the general".
- **An identification put to the editor carries its evidence** (2026-10-19).
  They do not read German and cannot look a man up in the books, so "taken
  to be the edition's, on the strength of the name, the time and the
  place" gives them nothing to judge. Write what the book says, what the
  edition's document says (with its number), and what joins them: for
  Stenger, that Karge and Unruhstadt are one town. They left Stenger open
  at first, not knowing the Karge connection, and accepted him once it was
  written out plainly.
- **The books spell places in ways the edition never met**, and the
  edition's patterns miss them: Trąbczyn had no hit at all until
  "Trombczyn" and "Trobozyn" were added under `patterns:` in
  `literature/index.yml`. Look for the estates of focus by hand in each
  new work (the black register is the place to start).
- **Traps in `literature_index.py`**: some of the edition's patterns are
  `entities._Rx` wrappers with no `fullmatch` (the compiled pattern is
  `.rx`); a YAML anchor that shares one exceptions list between two
  spellings makes every exception stale for one of them (the script's
  `--check` now fails on an exception naming a passage without the hit, so
  give each spelling its own list); and `literature_site` wraps
  `sys.stdout` when imported, so a script importing it reconfigures stdout
  after the imports, not before.
- **Jekyll 3 cannot take `a[b]` in an include's parameters**
  (`{% include x.html works=site.data.m.person[p.slug] %}` stops the build
  with "Invalid syntax for include tag"): assign it to a variable first.
  And `assets/doc-list.js` takes every `details.doclist` on the page for a
  list of documents, so another closed list on /people/ or /places/ needs
  its own class (`litlist`).
- **Two Liquid traps of the newspapers pages** (2026-10-22). Liquid counts
  the empty string as true: `{% if w.image %}` rendered the figure for an
  item whose `image:` is empty, with the file name empty after it, and
  pipeline/verify_site.py caught the broken link — the comparison is explicit now
  (`{% if w.image and w.image != '' %}`, `_layouts/newspaper.html`). And
  Liquid cannot build a bracket key by concatenation:
  `t['lit_lang_' + w.language]` is nil, which left the Language fact of
  every item on the Newspapers list page blank (the item pages had done it
  right, with an `assign`); `_includes/newspapers.html` assigns
  `w_lang` first now.
- **A hand-made link says what each side says, and every figure in it is
  read in both** (the links of the black register, 2026-10-19;
  `literature/links.yml`). Its sentence is shown under the passage and
  beside the document, so it names the book, the document and what each
  says: "the register says", never "it was". Where they disagree, the
  sentence says so: the register has Triebenfeld sell his estates to Prince
  George for 400,000, his own letter of July 1800 280,000. Since 2026-10-21
  (the editor: "Always take the facts/dates from primary documents over
  literary sources, and flag when there's a discrepancy") it also says that
  the edition follows the document, and the difference goes into
  NEEDS_CONFIRMATION as settled, not as a question. A name in a letter taken to be a man of the book is Claude's
  identification until the editor rules: the comment at the link says so
  and NEEDS_CONFIRMATION lists it. **Look at the scan first**: "Gen.
  Ruchts" in letter 103, taken for Rüchel, was a misreading of "Ruchels"
  (the editor, 2026-10-19), which the site's scan showed at once; the
  question need not have gone to the editor as an identification.
  **Search the corpus before writing "the edition has no document"**: the
  link `breyer1935gaue-hollanders` said so of Breyer's year 1746, and the
  boundary decree of 1775 (Konin Gr.145, p. 76: "the rights granted them in
  1746") and the summons of 1860 (53/968/0/-/783, which names the grantors)
  both cite the privilege (found 2026-10-20; the editor: Gr.145 is the
  primary source for it). A search of `dataset/documents/*.json` for the year or the
  name takes a second. The rule this broke is the editor's of 2026-10-20,
  HOUSE_STYLE, "The documents first".
- **`english_forms.py --apply` rewrites every page and every summary**,
  not only the one a new line of `english_corrections.yml` is for. On
  2026-10-19 it also re-wrapped 23 summaries in `site/_data/summaries.yml`
  and grouped article numbers as if they were sums ("articles 1,302 and
  2,800", APŁ 39/98/0/-/6603, doc. 3). After running it, read `git diff`
  and put back (`git checkout --`) every file the correction was not for.
- **A correction to the English does not reach the name pairs.** The
  `names:` list of a page in `site/_data/translations/<pad>.yml` (German
  form and English form of each name) is matched against the German by
  check_translations.py; when a name in the German is corrected, change
  its pair too, in the same script as the text.
- **`yaml.safe_dump` writes an anchor (`&id001`) for a list used twice**
  (one link's passages written under each of its documents); copy the list
  first, so the site's data file has no aliases.
- **The browser preview may not be available to Claude**: in this sitting
  every browser action's permission request was cancelled. Check the built
  page in `site/_site/` with Python instead (`PYTHONIOENCODING=utf-8`, the
  shell's own encoding cannot print "ą"), and tell the editor that is what
  was done rather than waiting on the browser.
- **A planned link is checked against the document before it is written**
  (the second set, 2026-10-19). Three of the links planned in the works'
  notes from memory did not hold when the documents were read. The Łazińsk
  tables of 1868 were to show the estate's owner, and they never name him.
  Breyer was to have named the Drzewce forest, and it is the lease that
  names it. The lease's paragraphs were written down as "I to XV" from
  memory; the copy has I to XIX. The same reading found the best thing in
  the set: the dispatch from Venice of December 1796 already mourns
  Prusimski's wife, whom Żychliński has die in 1797. So read the document
  for every link, and look up every paragraph number and spelling in the
  file before writing it in a note.
- **The edition's form of a place goes in the sentence, the document's in
  brackets** ("the woods near Drzewce (the lease's 'Drzewiec')"). One link
  had both spellings, and a German adjective made from one of them.
- **Brought in from a PDF**:
  - UpstreamVistula reissues: `pipeline/literature/upstream_pdf.py`, whose
    docstring lists every rule. Their articles of 1935 set chapter headings
    in plain 12-point type, not bold; a raised 2 after "km" is the square,
    not a footnote; pages printed on their side are drawn upright before
    they are read.
  - Photographed pages: a text layer can be useless (Żychliński, vol. 13).
    Render the pages with PyMuPDF (PIL is not installed here), cut them into
    strips, read them, and write the text by hand.
  - In a work's Markdown, spaced type is given as bold and italic as italic.
    A numbered paragraph at a line start ("1. Hr. Aleksander") is written
    "1\.", or kramdown renumbers it as a list. Footnotes `[^n]` restart on
    every page, as the book has them.
- **The mentions sheet shows the first place a spelling stands in the line,
  not necessarily the hit**: when a hit's context looks wrong, find the hit
  by its offset. And an edition pattern can match inside a longer Polish
  word, because ł and other letters fall outside the `à-ÿ` range a pattern
  uses for a word's edge; read such hits before ruling them.
- **The Bash heredoc trap again** (2026-10-19): an append of English prose
  to `links.yml` failed on an apostrophe and wrote nothing. Append with the
  Edit tool, anchored on the file's last lines.
- **Two of Słowiński's books checked against their PDFs** (2026-10-22, the
  editor's request; outside the repository, in their Downloads folder):
  *Przeżyć tę jedną zimę* (2023) and *Zerwane ogniwo* (2024). The editor's
  .md files of them were exports with damage (line-break hyphens left in
  words, drop caps split off, runaway italics, notes cut or misplaced,
  captions missing, pictures embedded as base64). Each .md was **made again
  from the PDF's text layer** with PyMuPDF, with the old .md only as a second
  witness; the old file kept as `*.original.md` and a check report beside
  it. The editor's rule for this work: **no OCR on images** (a rendered page
  may be looked at for layout only). The scripts and plans are in that
  session's scratch folder, not kept; what to carry over:
  - The checks that made the result trustworthy: the PDF's words and the
    .md's words equal as multisets and in order; the letters equal page by
    page (with `<!-- s. N [PDF M] -->` page marks in the .md); note
    references and definitions counted against the print's `*` markers;
    italic and bold words compared by font; tables cell by cell. Write the
    checker apart from the generator, and run it after every hand edit.
  - **InDesign text layers carry look-alike letters**: in *Zerwane ogniwo*
    German "ß" is Greek β (U+03B2) and "ä" Cyrillic ӓ (U+04D3) in 13 places;
    they print the same and break searching. The editor ruled them written ß
    and ä. Search a new PDF's layer for Greek and Cyrillic letters in Latin
    words.
  - **A letter can be a picture**: the cover's "O" of OGNIWO is a clock, and
    the layer reads "GNIWO"; the editor ruled the title written as seen.
  - **Most line-end hyphens there are hard, not soft** (2,162, only 30
    soft): each was decided against the book's own words (a compound the
    book writes joined elsewhere is joined).
  - Rulings the editor accepted: an ornament as "◼"; italics exactly as the
    fonts have them, even mid-word; misprints kept and listed; notes at the
    end as `[^n]`. A mistake made: the ornament replace also turned the
    notes divider `---` into "◼" and broke the checker, which finds the notes
    by the last `---`: replace by the generator's own kind, not by text.
  - If either book comes into the literature, the checked .md is the text
    to start from (the books bear on Łazińsk and Zagórów).
- **Kneifel 1937 read from the images** (2026-10-23, the sitting's own
  branch `kneifel1937`): 79 pages of Tesseract+layer OCR with the editor's
  Kalisch .md as base text where it exists. What carries over:
  - **Two witnesses agreeing settles a page; zoom only for what matters**
    (2026-10-23). The session's course correction after overspending: where
    layer and Tesseract agree, write the page and move on; a zoom is for a
    name, date or number that is actually contested or where all witnesses
    are damaged. A spot sheet (`scratch/slowo1892_sheet.py` pattern) is the
    tool for what remains — four rows on the Administratoren list settled
    in one pass.
  - **A zoom crop the reading agent cannot see is not a reading**:
    large crops come back "[image removed]", and "reading" one is
    invention. The honest tools are Tesseract re-run on the crop at higher
    resolution (`--psm 7` for a single line), or the editor's eyes via a
    spot sheet.
  - **A seam script before assembly** (`scratch/k1937_seams.py`): print
    the last 45 characters of each page against the first 45 of the next,
    flagging no-stop ends and lower-case starts. It finds every mid-word
    and mid-sentence page join and every elision point in one run — no
    hunting through finals by hand.
  - **Tipped-in plates inside a page range** (2026-10-23): the two
    unnumbered portrait plates between printed pp. 10 and 11 carry typeset
    captions that continue in engraved script no pass can read. Transcribe
    the typeset lines, mark the script `[…]`, say what was skipped in the
    notes, and let the printed page number at the foot — not the PDF
    index — anchor every `[p. N]`, because the mapping drifts wherever
    plates intervene.
  - **Footnote numbering restarts at each sub-entry** (Maślaki, the
    Lissewo-Pyzdry filial): check the page foot before assuming a page's
    markers continue the previous page's numbers.
  - Asterisk footnote markers inside GFM tables are written `\*\*` in the
    cells as at their definitions, or a renderer may pair them into bold.

- **Kneifel 1937 translated and integrated** (2026-10-23, the same sitting,
  same branch): the English `english.md`, `work.yml`, the index rulings and
  the site pages, on the pattern of `literature/kneifel1964`. What carries
  over:
  - **The sibling work's work.yml is the template, but check its state
    first**: the sibling's integration was already merged to main, so
    `work.yml` had to be written fresh — and PowerShell's `Test-Path` in a
    `ForEach-Object` loop misreported every `work.yml` as missing while
    `Test-Path` on the single path was true; settle file existence with
    Python or `git ls-tree`, not a PowerShell loop.
  - **The index check's unruled hits are read, not bulk-ruled**: the new
    work brought 49 hits in 18 pairs, each read from the generated sheet
    against the entity's identity in `reference/people.yml` — six turned out
    to be different people or the office of Küster rather than the man
    (the first literature hits several entities have ever had), and the
    place rulings follow the work's own cross-references (the book's p. 263
    names Wrąbczynek a part of the cantorate Wrąbczynkowska Kolonia, which
    settles the "Wrąbczyner Hauland" question).
  - **A footnote marker glued to a word is its own surface** ("Warschau6"):
    the index match's negative lookahead admits digits, so a hit can be
    word+marker; rule it by the word, and say so in the comment.
  - **An unsure identification is ruled yes only with the presumption
    said**: Zelmer (Heinrich, elder of the Zagórów church council,
    presumably of the Trąbczyn family) is ruled yes with the comment and a
    line in NEEDS_CONFIRMATION — not silently.

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
  added. When the text itself gains something that matters (a passage
  restored from the scan), the summary may be rewritten there, and the new
  statements are then checked like the rest and the count corrected
  wherever it is given (`claim_check.yml`, `process.md`, `notes.md`). A date an office wrote on a paper is not the day it arrived unless
  the mark says so; a note that names no office is not "the Cabinet".
- **Fixing names in the English after an authority changes:** take the hits
  from `pipeline/review/uncanonical_names.py`. On the desktop, change the
  translation cache as well as the published file, or the next publish rolls
  the fix back; compare the published file with HEAD before committing.
- **A changed line of transcription** is changed in `corpus.txt` (the page
  files under `transcriptions/` were removed, 2026-11-23), in a row of
  `transcription_decisions.csv`, in
  `sideways.yml` or `office_notes.yml` if it is the first line of a block
  there, and in `intake/translation/doc<N>.yml` (with its `marker_count`).
  Then `write_cache.py <N>`, `check_translations.py`,
  `publish_translations.py`.
- **Summaries written again for a holding already published** (Oe 1 Bü 14525
  and 14526, 2026-10-08). Read each document whole in `dataset/text/<pad>.txt`
  (the German part, above `--- SUMMARY`), write the German, translate it, then
  hold every statement to a quoted line in `intake/claim_check.yml`. Two free
  checks catch most slips before the file is closed: every quoted fragment
  must occur in the document's text, and every figure in a summary must occur
  in the document (a sum written out in words, "Sechs und Siebenzig Tausend",
  shows up as missing and is read). Where several copies of one deed stand in
  a holding, summarise what each copy says: two copies of the grant of 1796
  leave out villages the original names. The holding's `summaries_draft.py`
  writes the site's two summary files itself, and passes the English through
  `numerals.group_digits`, or `english_forms.py --apply` and a re-run of the
  script undo each other. Run `english_forms.py` (without `--apply`) after
  writing English summaries: it also fixes name spellings (Tietz is Titz).
- **The site's downscaled scans settle a word in the cloud.** The raw scans
  are on the editor's machine, but `site/assets/scans/` (about 1100 px wide)
  is in the repository and readable enough for a date or a dropped line: crop
  the part of the page with PIL and look at it. It settled "1801" in 14525,
  document 7. It is not enough for a doubtful name; leave those to the editor.
- **After publishing English, read the holding's glossary matches.** English
  "entails" and "cession" drew false glossary marks and were reworded. The
  checker forbids "hypothec" in English, Latin "sub hypotheca" included.
- **No comment header in original.md or english.md** (2026-10-23): what
  stands before the first page mark is the work's front passage, and the
  build compares the two languages' front lengths - leading comment lines
  make a front that never matches. Provenance lives in notes.md and the
  work.yml header.

## Traps in the tools

- **Automating a step of the labelling page must not take the editor's
  typing moment with it** (2026-10-31, the type filled from the
  gazetteer). The first take saved the label the instant the trace ended
  when the type came from the gazetteer — one step fewer, as asked — but
  the "form as written on the map" was typed at the pause before saving,
  and the pause was gone: "I need to be able to still add 'Form as
  written on the map'". The settled shape: the last step remains, but
  with the type shown as filled in and the form field focused — Enter
  saves, a type key overrides. The rule: when a step's *decision* is
  automated, keep the step's *fields*; a form the editor types is never
  skipped past, only prefilled.
- **Correlation matchers: prove them on a self-match first** (2026-10-31,
  the mosaic fit of Pełzucki 1896, scratch/map4456/). Finding one image
  inside another by FFT patch correlation ran three takes before it worked,
  and every take "found" confident matches that were noise: (1) the
  denominator normalised by the window's standard deviation without
  subtracting the window's own mean gave scores ~0.007 everywhere (the
  peak still sits right, the score is meaningless — never threshold on
  such scores); (2) the local sums `sum(I)` and `sum(I²)` were taken as a
  plain convolution (`fs*f1`) where a correlation (`fs*conj(f1)`) was
  wanted, so the normalisation was computed at the wrong offset; (3)
  numpy's `rfft2(s=...)` pads to `s` but `irfft2(s=...)` interprets `s`
  as the *output* length, so mixing them broadcasts garbage — plain
  `fft2`/`ifft2` with one shared padded size `s=(H+h-1, W+w-1)` avoids the
  whole class. The rule: before believing any "match", run the matcher on
  a patch cut from the search image itself; it must return ~1.0 at the
  patch's own position. A score below ~0.9 on a self-match means the
  formula is wrong, not that the images do not match.
- **A redirect stub's permalink keeps its trailing slash** (2026-10-27, the
  cemeteries' move under Places). A stub written with
  `permalink: "/cemeteries"` (no slash) renders to `cemeteries.html`, a
  flat file a request to `/cemeteries/` never reaches - GitHub Pages
  serves a directory URL only from its `index.html`. With the slash
  (`"/cemeteries/"`) Jekyll writes `cemeteries/index.html` and the old
  address keeps working. The rule generalises: every redirect stub's
  permalink is a full directory URL, slash and all, like the documents'
  stubs in `site/redirects/`; and after generating redirects, check the
  built `_site` for the `index.html` at each old address, not just for the
  stub file.
- **`git add` on a file that still carries conflict markers commits the
  markers** (2026-10-27, the maps' publish). During a rebase, a generated
  data file (site/_data/places_pages.yml) was staged with `git add` to
  "mark it resolved" before the markers were resolved - 302 pairs of
  `<<<<<<<`/`>>>>>>>` went into the commit and were caught only by the
  byte check before the push. The standing rule: `git add` marks a
  conflict resolved, it does not resolve it; before staging a conflicted
  file, its markers are resolved or its content is taken from one side
  whole (`git checkout <side> -- <file>`), and after any conflict
  resolution `git grep -l '<<<<<<<' -- '*.yml' '*.py' '*.md'` must come
  back empty before the commit. A second trap the same hour: a regex
  resolving conflict markers whose tail was greedy (`>>>>>>>.*\n` with
  re.S) swallowed the following hunk whole - anchor the marker tail to
  one line (`>>>>>>>[^\r\n]*\n`), and make the script assert the number
  of hunks it resolved before it writes.
- **PowerShell's backtick eats markdown into the bytes it writes** (2026-10-27,
  the maps' changelog entry). `Add-Content` with a here-string, and every
  `python -c "..."` inline script passed through the shell's double quotes,
  runs the string through PowerShell's escape processing first: a backtick
  before a letter is an escape (`a becomes the BEL character, so the word
  `absent` was written as BEL+"bsent" and its backticks vanished), and any
  non-ASCII in the command line risks the console's codepage. What stands:
  never write repository text through a shell string - write the text with
  the file tools, or put the script in a real .py file and run it; and
  after any shell-borne write, check the bytes (CRLF counts, control
  characters, the Polish letters present) before committing. Related: this
  shell's *display* of UTF-8 files shows Ł as "�?" and the like - the
  files are fine; judge them with Python reading `encoding='utf-8'`, not
  by the console.
- **The session's image reads can come back stripped, and a session that
  did not notice will write "confirmed on the image" of things it never
  saw** (2026-10-26, Poznań Gr.1181). Every `read` of an image in that
  session returned "Image read successfully" followed by the harness's
  note that the image had been removed to reduce the request size - the
  session saw nothing, yet kept reasoning "the crop shows...", until the
  contact-sheet check exposed the gap. The standing rule for any session:
  treat "Image read successfully" as NO confirmation; verify by other
  means (formulas, sibling units, the editor's spot sheet) and say in the
  repo where each claim's evidence really lies. The settled-reading log of
  Gr.1181 records exactly this on its face.
- **A spot sheet the editor answers from a phone at work goes to the
  public sheet repo, not to a local server** (2026-10-26). The pattern:
  `make_sheet.py` in the unit's `intake/` builds a self-contained page
  (crops under `img/`, answers in localStorage, a copy-to-clipboard block
  the editor pastes back into the chat); the page is pushed to
  **triebenfeld-spot** (beside this repo; takaji10.github.io/triebenfeld-spot/),
  under `sheets/<slug>/`, and GitHub Pages serves it. The crops are cut
  from scans already public on the edition's own site, so the sheet
  publishes nothing new in kind. Every imaged row carries two escape
  buttons: "wrong line" (the window landed in the wrong place) and "not
  shown on crop" (the band marks the spot but the word itself is not
  there to read; widen or re-crop on request) - the crops are placed by
  machine and no session has yet been able to check them by eye, so the
  editor's tap on one of the two is the check.
- **Crop placement for a sheet: a tall window around a position, not a
  line** (2026-10-26, the editor: "the crops don't generally line up ...
  make them bigger, wider, more zoomed in, taller because you don't know
  where the line breaks are"). What failed first: the editor's rough y
  guesses overriding the anchor estimate, and an OCR-box band detector
  that merged whole paragraphs. What stands: the row's centre is the
  anchor's character fraction of the page's transcription mapped into the
  span of inked rows (a darkness profile, not OCR boxes - the text is
  beyond the engine, the lines are not), and the crop is a fixed
  +-380 px window (about eleven lines), full page width, near-native
  resolution. The ink check that can replace an eye: dark-pixel fraction
  at native resolution (a 200x80 thumbnail washes hairline strokes to
  gray and reports every crop blank - a false alarm). The trap in the
  first profile: a leftover loop variable (`h`, the page height) inside a
  comprehension offset every band by 528 px and pushed every estimate
  down the page; a variable named in a comprehension is the comprehension's
  own, and reusing an outer name there is silent corruption. A template
  lesson beside it: **never rewrite a free-text box from its own trimmed
  value inside the `input` handler** - the trim-and-write-back eats every
  space the moment it is typed (the editor could not type spaces, 2026-10-26).
  Keep the raw value while typing; trim only when the answers are copied out;
  and let `mark()` write a value only when the box is not focused.
- **Lineation by machine, measured against the editor's own layout, fails
  for this hand - and the measurement is the answer** (2026-10-26, Poznań
  Gr.1181). The editor laid out p. 161 in the manuscript's lines; tested
  against that ground truth, char-wrap at the mean characters-per-line put
  only 3 of 8 line ends within +-1 word (drift 2-4 words, growing along the
  page - the manuscript's own lines run 55-81 chars), and three line
  detectors (OCR boxes, row-darkness runs, pitch-split bands, autocorrelation
  pitch) counted 22, 24, 39, 41 and 50 lines against the true 38: the hand's
  lines touch and the spacing is not uniform. So the corpus takes the
  editor's layout for p. 161 verbatim, the other pages keep the paragraph
  layout, and machine drafts sit in `intake/lineation_draft/` as a typing
  aid only, clearly marked. The general form: when the editor asks "how
  easy would it be", run the measurement against their sample FIRST and
  answer with numbers, not with an attempt.
- **The editor's fresh transcription outruns the session's completions**
  (2026-10-26, the same holding). The morning session had applied 108
  grammar-driven completions to the editor's doubtful readings; the
  editor's own line-by-line re-typing of p. 161 kept the original doubts
  (and settled five other readings: 1783, videlicet, Mensis, oblatam,
  camera-/riali). The completions were withdrawn the same day to match
  their text - the transcription is the editor's, kept as written, and a
  completion waits on their explicit ruling (the sheet's principle rows).
  When a fresh editor text arrives, diff it against the working corpus and
  follow IT, not the session's earlier reasoning.
- **A bare web fetch of an HTML page invents print slips** (2026-10-22,
  the Luteranie Konin parish page). The text conversion drops `<br/>` and
  `&nbsp;` runs: the page's "proboszczowie parafii<br/>z Grodźca" arrived
  as "parafiiz Grodźca" — a missing space that the page does not have —
  and a padded second line arrived as a run of spaces mid-paragraph. For
  a web item, fetch the **HTML source** (curl into scratch/) and read
  that before ruling anything a slip; the page's own line breaks are
  part of "as printed" for a page that sets them deliberately, and a
  run of non-breaking spaces at a broken line's start cannot stand at a
  line's start in the Markdown (four spaces and more make a code block)
  — keep the break, leave the padding to the notes.
- **A file named .jpg can be a WebP** (2026-10-22, the Dziennik Poznański
  clipping). Windows' own imaging (GDI+, WIC) refuses it —
  `System.Drawing.Bitmap` throws "Parameter is not valid" — while PIL reads
  it without a word. If a picture "will not open" on Windows, ask PIL what
  `im.format` says. `pipeline/ocr.py` and PIL read the clipping as it is.
- **Tesseract in the project** (installed 2026-10-22 at the editor's word,
  when the clipping was read): the engine is Tesseract 5.5.3 (winget
  `tesseract-ocr.tesseract`, `C:\Program Files\Tesseract-OCR`), the Polish
  models are in `%LOCALAPPDATA%\Tesseract\tessdata` (tessdata_best and the
  standard model, fetched from the tesseract-ocr/tessdata repository; the
  installer's own tessdata carries English only), `pytesseract` is installed.
  **Neither the engine nor the data is on PATH** — `pipeline/ocr.py` looks
  them up itself (`read()`, `words()`), so pipeline code imports that and
  never calls tesseract.exe by hand. It runs on the editor's Windows machine;
  a cloud session cannot OCR this way, and needs the text given or paid out
  for.
- **Display capitals of a rough scan defeat every upscale — go back to the
  source for more resolution** (2026-10-23, the Dziennik Poznański death
  notice of 1879). The WBC's microfilm page at 300 dpi read its body but
  not its giant name line at any upscale or model (Tesseract returned
  nothing for the row at ×1-×6, psm 7/8/11/13, pol, pol-std, eng, even a
  fetched Fraktur model). The issue's DjVu fetched again from the WBC and
  rendered at 600 dpi read the same lines at a plain pass — the letters
  were twice the size, not twice the noise. Upscaling multiplies what the
  raster has; re-fetching gets what it never had. Downscale a too-big
  render to ~40 px letter height before OCR: Tesseract reads 30-50 px
  letters, not 120 px ones.
- **The WBC serves its files behind a proof-of-work challenge, and the
  DjVu components directly** (2026-10-23). Every request may come back as
  a "High Load - Verifying Browser" page: solve it by finding the nonce
  with `MD5(signature + nonce)` starting `00000` (the page's script
  carries `ts` and `signature`), send it as the cookie `captcha_pow=<ts>_<nonce>`,
  and the real page follows. The digitised issue's pages sit at
  `/Content/<edition id>/DjVu/<file>.djvu` (e.g.
  `/Content/84585/DjVu/0004_0001.djvu`); the bundle's own `DP_*.djvu` is a
  73-byte indirect index, not the pages. The reader page's HTML
  (`/dlibra/publication/<id>/edition/<ed>/content`) carries the addresses.
- **A stray `struct.py` in the session's scratch folder shadows the
  stdlib** (2026-10-23, `%TEMP%\opencode`). A script placed in the folder
  itself imports the leftover file (it opens a path on J: and crashes) in
  place of Python's `struct`, which `urllib` needs. Keep session scripts
  in their own subfolder; leave the leftover file alone (another session's
  work).
- **`name_catalogue.py` rewrites `reference/name_seeds.json` wholesale, and
  a bare run drops curated seeds** (2026-10-25, the contract of 1820). The
  committed file carried 196 seeds; a bare `--unit <slug>` run re-derived
  473 from the whole corpus - 28 of them gone, among them Drzewce, Kolno,
  Betsch and Gneizenau, and junk in their place ("Allodial" a place,
  "Amerika"). Restored with `git checkout` and the holding needed none of
  it: the sibling 783 put its 97 colonists into no authority either. A new
  holding's people are not seeded by a bare catalogue run; the names pass
  and the editor rule who is profiled. Treat the file as write-protected
  until the tool's intended mode is understood.
- **A hand row in `paragraph_decisions.csv` whose context carries a comma
  must have the field quoted** (2026-10-25, the contract of 1820). The
  hand-set rows are found again by exact context match, and the sheet is
  plain CSV: the unquoted context "Johann George Lindner, Schulz." was read
  as "Johann George Lindner", the match failed, and the row was dropped
  with "hand-set row not found again" - twice, before the quoted form
  (`1,44,break,held,hand,0,0,0,,"Johann George Lindner, Schulz."`) held
  through a rebuild. Quote any hand row whose context contains a comma.
- **Stale spot-sheet servers outlive their sessions and hijack their
  port** (2026-10-25). Earlier sessions left `spot_sheet*.py` servers
  running on 4103, 4107, 4108 and 4109 (the oldest two days back); Windows
  lets a new server bind the same port with `allow_reuse_address`, and then
  the STALE one answers - a new sheet opens as a different holding's page,
  with no error anywhere. Check what answers before handing a port to the
  editor (`urllib` the title, or look for `class=row`), and take a port
  `netstat` shows free. Leave the stale processes alone unless the editor
  says otherwise: another session's work.
- **OCR a manuscript for its LINE SCAFFOLD, not its words** (2026-10-25,
  the same contract). Neither Tesseract's German print model nor the
  lunaroute converter can read an 1820 hybrid hand - the lunaroute pass
  returned word salad - but the converter reads the page whole and its
  LINE BREAKS were right where the darkness-run profile and the
  transcription could check them (the "Vo-/cation" division, the ten
  numbered terms). The method for laying out a secure transcription by
  paragraph onto the manuscript's lines: count and place the lines with
  the darkness runs, scaffold the contents with the OCR pass, map the
  editor's words onto the scaffold, and leave the few unsettled divisions
  to a spot sheet.
- **OCR a page as the agreement of passes, not from one run.** The five
  passes over the clipping (two upscalings ×3/×4, psm 6 and 4, tessdata_best
  beside the standard model, Windows.Media.Ocr as a third witness) agreed on
  almost every word; each pass that disagreed was the one wrong. Tesseract's
  word confidences (`words()`) sort what goes to the spot sheet; Tesseract's
  TSV wants `-c tessedit_create_tsv=1` (the bare `tsv` config name prints
  plain text instead), and its output ends each line with \r. Small scans
  want upscaling: the clipping is 712×960 and only reads well at ×3 and ×4.
- **Anchor a pixel probe to its line with the words() boxes first** (2026-10-22,
  the Kurjer Poznański clipping). The body lines sat about 26 px apart (the
  TSV's tops 83, 109, 135, ...), and a probe cut between two of them (y 90-110)
  caught the neighbouring line's letters and read them as the word the probe
  was looking for - "Trąbczyn" was "found" in the "ra ilość" band, and only
  the whole page rendered at ×2 showed the error. The ogonek was real, but on
  line 3 (y 54-80), not where the probe had it. Render the whole page enlarged
  and mark the line bands before probing, and never probe a band the word
  boxes do not cover.
- **A printed book's numbered notes: the lunaroute converter resolves the
  superscript markers, Tesseract does not** (2026-10-23, Kraus 2001).
  Tesseract renders an unresolved superscript as `?`, `*`, `'` or `"` - its
  apparent closing quotes after "helfen." and "verstarb." were the markers
  30 and 41, not quotation marks. The lunaroute pass prints them as `^N$`
  where it can. Read a noted page with both engines, place each marker from
  the reads, and settle the doubtful ones at crops; where a marker cannot be
  seen, place it by sense and say so in the notes. TSV also helps:
  `-c tessedit_create_tsv=1` (the bare `tsv` config name fails when
  TESSDATA_PREFIX points at a folder without the configs), and the token
  widths betray a marker (a merged token reads taller or wider; `9.`
  one digit wide against `1799` four).
- **Tesseract's German model** (2026-10-23): the installer's tessdata
  carries English only; a `deu.traineddata` from the tesseract-ocr/tessdata
  repository was already in the session's tessdata folder
  (`%TEMP%\opencode\tessdata`, TESSDATA_PREFIX) from an earlier session -
  it reads a modern Antiqua German book well and is the right second
  engine beside the lunaroute converter (the converter better at Romance
  quotations: its French reading of the 1792 letter stood where
  Tesseract's garbled).
- **Never rewrite a UTF-8 file with PowerShell's Get-Content /
  Set-Content** (2026-10-23). A file without BOM is read through the
  system codepage (cp1252) and written back mojibaked through the whole
  file; the build does not complain (both languages wrong alike) and the
  error surfaces only in the built pages. Cut lines with Python
  (`bytes.split` or read/decode/write), not with Get-Content.
- **When appending sections to literature/index.yml, check the key is
  not there already** (2026-10-23). A duplicate key silently shadows the
  earlier one, and the old ruling vanishes - `--check` catches it as a
  resurrected "no ruling" for a spelling the file does rule.
- **An item's uid in the newspapers index is its slug with "-1"**
  (2026-10-22). The register's `only_in` filters pin a spelling to the uid
  it was read in ("Pawłá Prusinskie" to kuryerpolski1754075-1); when the
  Kuryer Polski left the corpus for the newspapers, the index re-created
  that uid for the item, so the filters kept working and no register entry
  had to change. A person named by no document any more (Głowiecki) still
  stands on /people/: build_site_data takes the newspapers' mentions as a
  second reason to show a person.
- **A stand-alone spot sheet** (2026-10-22, `scratch/dp1937_sheet.py`): for
  an item that is not a unit yet, copy the queries.py page and saving into a
  scratch script with its own rows and crops (its `--read` prints the
  answers); the crops are cut from an upscale of the scan and the whole page
  is shown at the top. Answers went to `review/dp19370807/
  query_answers.json` (git-ignored, like all review/); the rulings are
  recorded in the item's notes.md, which is tracked.
- **A WBC content URL sits behind the site's browser check** (2026-10-22,
  the Ostdeutscher Beobachter item). `webfetch` to
  `wbc.poznan.pl/dlibra/publication/<pub>/edition/<ed>/content` returns only
  "Site is under high load"; the record's citation is still to be had —
  search results carry the WBC titles verbatim ("... 1943.07.17 Jg.5
  Nr195"), and the library's BibTeX endpoint
  (`wbc.poznan.pl/dlibra/dlibra.bib?type=e&id=<object>`) returns the record
  as a citation. Do not block the item on the record: the issue's year and
  number, the place and the publisher are enough to cite, and the
  Zeitschriftendatenbank carries the paper's full title.
- **Sessions share the desktop tree, and one may commit the whole dirty
  file** (2026-10-22). The Twoja Słupca session's commit of
  `newspapers/index.yml` carried the Ostdeutscher-Beobachter work's
  uncommitted rulings that sat in the same file — harmless here, both being
  finished rulings for committed items, but a half-written hunk of yours can
  travel in another session's commit. When a file you must edit is shared,
  make the edit and stage or commit it promptly (a filtered
  `git apply --cached` for a file that also carries another session's
  work), and check `git log` for new commits from parallel sessions before
  assuming what HEAD holds.
- **A Wikisource page of Arct's dictionary has no text of its own**
  (2026-10-21). Its source (`action=raw`) is only a template naming the
  scanned page (`{{Ilustrowany|strona = 405|tom = 1}}`). Ask for the
  rendered page instead and strip the tags:
  `https://pl.wikisource.org/w/api.php?action=parse&page=<title>&prop=text&format=json&formatversion=2`.
  Gloger's pages carry their text and need no such step.
- **One institution, several names in the edition.** Gród, the municipal
  court, is "Acta Castrensia" in the Latin, "gród, grodzki" in the Polish,
  "municipal court" in all the English and "Burggericht" in the German
  summaries. A glossary entry
  for such a term matches all of them (match_de also runs over the German
  summaries, match_en over the English ones), and keeps place names that
  share the root ("Grodziec", "Grodzisko") out of its pattern.
- **A noun that is also a name (stawisko, 2026-10-21).** The editor: the
  glossary entry is for the noun, not the place Stawisko. In the court
  books a capital does not make a name (the clerks capitalise most nouns);
  the sign is the word beside it: "zwany", "nuncupatus", "called",
  "namens", or "known" in the English. The entry's pattern leaves those
  out with lookarounds, and a `\b` after `\w*` keeps the regex from
  backtracking into a shorter match that slips past the lookahead
  ("Stawisk" out of "Stawisku zwanym").
- **`build_literature.py` empties `dataset/literature/`, and
  `literature_index.py` writes `mentions.json` back into it** (2026-10-21).
  Run the literature's steps in order, build, index, site, before
  committing; `git add -u` after the build alone recorded `mentions.json`
  as deleted (commit adc3ad1a, put right in the next). Before any commit
  with `git add -u`, read `git status --short` for a `D`.
- **A saved web page can carry the editor's login** (the online Boniecki,
  2026-10-21: an e-mail address in its header). Keep such a page out of the
  repository, make the text from it with a script that takes only the
  part wanted, and say in the script why the page is not kept.
- **A work brought in from the editor's Markdown pair** (Kneifel 1964,
  2026-10-22): the first literature work taken from the editor's own
  Markdown files - a German transcription with the printed page numbers on
  their own lines and GFM footnotes defined at the foot of their own page,
  and an English that pairs it page for page. `make_original.py` in the
  work's folder reads both files from the editor's folder (here on J:) and
  writes the excerpt; the source files are not committed. What worked:
  - **Scan the whole book for the edition's ground first** (every page
    against the edition's places and people), decide the excerpt as pages
    and paragraph ranges, and verify the boundary phrases in both languages
    before writing them into the script (the print's hyphen-broken names,
    "Zagö-röw", are boundaries of their own).
  - **A slice that runs to the page's end already carries the page's
    footnote definitions.** The script's first run appended the kept notes
    a second time; the fix is to append only a def the kept text needs and
    the kept slice does not already carry, and to check every kept marker
    has a def. The footnotes are named per page (`[^p41-4]`), so a marker
    never reaches across pages.
  - Excerpt pages open with their own `[p. N]` mark even where the page is
    kept from mid-page (the Karwowski pattern), so every kept page is its
    own passage and the pairing holds page for page.
  - The scan found the relevant material scattered through a general
    church history: search for false friends too ("Trombin bei Rypin",
    p. 101, is not Trąbczyn).
  - **A German print spells a Polish town with the umlaut on one vowel
    only** ("Zagörow", not "Zagöröw"): a literature pattern for such a name
    takes the umlaut where the print has it and the plain vowel where it
    does not, `Zagö-?r[öo]w`, and an optional hyphen takes the print's
    line-break form. And a German print drops the Polish ń
    ("Kolno-Prusinski"): extend the pattern to both, and rule the new
    spelling. (2026-10-23: p. 257 spells it with the umlaut on both
    vowels after all, "Zagöröw" - the print varies within itself; the new
    form is ruled in `literature/index.yml` beside the pattern.)
  - **The excerpt's English anchors are bound to the English source's
    wording, not the German's** (2026-10-23). When the editor's pairing
    file was replaced by a fresh whole-book translation, every "en" anchor
    in `make_original.py` had to be re-taken from the new file's phrasing
    ("the urban immigration", "frustrated the realization", the inverted
    "made very much his concern Pastor Groß" sentences) - the German
    anchors were unaffected. Take the anchors fresh from the source in
    hand, per language, and never assume the old file's sentences stand.
- **Two keys one letter apart are not duplicate keys** (2026-10-22,
  `wielun` in `literature/index.yml`): `Wieluń` (yes) and `Wielun` (no) are
  different spellings, each with its own ruling - the ń key takes the
  Polish-language works, the plain-n key the German print. Read the keys
  byte for byte before crying duplicate; the real duplicate-key trap (the
  second `Miączyński` above) was two keys spelled alike.
- **A JSTOR PDF** (2026-10-21, `pipeline/literature/warthegau_pdf.py`):
  every page's foot names the internet address it was downloaded from, so
  the PDF stays out of the repository and the script drops the foot. Its
  text layer has three traps. Polish letters come from an accent font that
  stores each under its plain letter ("Łódz" is "Łód" + accent-font "z"):
  map them by font, and stop on one not in the table. Spaces of no width
  stand after hyphens, in ligatures and inside words ("or ga nized"): a
  space whose next letter begins in its first half, or that follows a
  space, hyphen, dash or bracket, is not real (a real space before a
  kerned capital, "Poylishe Yidn", ends where the capital begins). And the
  layer keeps a space after a real line-end hyphen ("mid-July") and none
  after a break, which tells them apart without a dictionary. Check every
  letter of the result against the PDF: it caught a lost backreference at
  once. Read the licence on the cover page: CC BY-NC-ND allows no
  translation.
- **A new place, and an estate in focus** (2026-10-21, Grodziec and
  Rzgów). A place in `reference/places.yml` is found in the documents and
  the literature by its `match`; it shows on the Places page only as an
  estate in focus, which comes from the per-document tags under
  `documents: estates:` in a holding's `rulings.yml` ("concerns", not
  "names"). Tag by reading each document, as for the neighbours already
  tagged on it; then `build_db.py --unit <slug>` for each tagged holding,
  `merge_corpus.py`, `build_dataset.py`, and the literature and site steps.
  Search the documents with Python, not `grep -E '\b...'`: grep's word
  boundary misses words with Polish letters ("Rzgów" in Konin Gr.117,
  doc. 12 was found only by the build). Look a place up on Nominatim from
  Python (urllib): the shell mangles "ó" in a curl query and the search
  returns nothing.
- **A new estate in focus needs the literature index run twice**
  (2026-10-21). `literature_index.py` lists the literature only for the
  places in `site/_data/estates.yml`, which `build_site_data.py` writes
  after it (the order in pipeline/regenerate.py too). After tagging a new estate,
  run `literature_index.py` again once the site data is built, then
  Jekyll: otherwise its card on the Places page has no literature (Rzgów).
- **Look at the branch before committing** (2026-10-21). The checkout was
  switched to a new branch (`frost2007`) by someone else mid-session, and a
  commit landed there unnoticed. `git status -sb` before each commit; if
  the branch moved, say so and ask. Moving a branch ref (`git fetch .
  a:main`, `git branch -f`) is refused by the session's permission check;
  at the editor's word to publish, `git checkout main` and `git merge
  --ff-only <branch>` did it.
- **A glossary word the editor names may already have an entry**
  (komornik, 2026-10-21). Read the entry and every use of the word in the
  documents first: the entry, checked against the same Gloger article, had
  only the officer, and its definition was shown in four documents where
  komornik is the landless lodger. Two senses make two entries, kept apart
  by `not_in` and `only_in`. Search the English too: the translations call
  the Latin camerarius "Boundary Surveyor" and "Land (Court) Chamberlain",
  and use "cottager" for chałupnik and Einlieger, so "cottager" cannot
  stand for the lodger. The same with pisarz: "notarius" in the court books
  is the court's clerk, not the notary public of the existing entry, and
  "Antoni Pisarz" in a list of Olęders is a surname. Read every hit, in
  every language, before writing the pattern.
- **A work kept off the site still has a page: its summary** (the editor,
  2026-10-21). A work under copyright (`visible: false`) is listed and its
  page holds only `summary_en`/`summary_de` from its `work.yml`. Write the
  summary from a reading of the whole work, in your own words, chapter by
  chapter for a book, with a last section on where the edition's documents
  say otherwise; never quote stretches of the text (`pipeline/verify_site.py` looks
  for them on the whole site). A long German summary goes into a file
  written with the Write tool and is appended from there: a heredoc breaks
  on an apostrophe ("Kraus' Untersuchung").
- **Another session may push your commits** (2026-10-21). A session working
  in the same folder pushed `main`, and with it a commit of this session
  marked "not published". After `git fetch`, compare `origin/main` with your
  own commits and correct the records to say "published" where they went
  out.
- **A work with no page breaks** (an online edition) is cut at headings
  (`chapter: '^# '`); where the edition numbers its items, the headings are
  those numbers ("# 2.976.177-182"), so each passage can be found online.
  The headings are the edition's and the notes say so.

- **The glossary gate and Latin documents.** `glossary_candidates.py
  --check` counted every common word of a wholly Latin document as a
  Latin term needing an entry (partium, quibus, Judicium) and stopped the
  build at the third such holding. It now skips documents whose language
  is `la`. A Latin phrase inside a German or Polish document still counts.
- **`pipeline/new_unit.py` makes `units/<digits>/`.** Rename it to `app<digits>`
  before writing anything into the new name, or two folders exist.

- **A Python script typed into the shell loses its backslashes**, even
  inside a quoted heredoc: `'\n\n'` arrives as a line break and the file
  being patched is left broken. Write the script to a file with the Write
  tool and run that. (Happened three times on 2026-10-06.)

- **One very long document** (31,000 words) broke the merge: Python's CSV
  reader refuses a field over 131,072 characters. `pipeline/unitlib.py` now raises
  the limit for every script that imports it; a script that reads
  `letters.csv` without importing `unitlib` must raise it itself.
- **A new holding's folder is named `app<digits>` for Poznań** like the
  others; `pipeline/new_unit.py` does not add the prefix. Rename the folder and set
  `slug` before anything is built. `review/<slug>/` must exist before the
  first `pipeline/regenerate.py --unit`.
- **`python pipeline/regenerate.py --help` prints no help.** It runs the whole pipeline
  for every holding. `--site` also rebuilds every holding first. Use
  `--unit <slug>` for one, then `--site` once at the end.
- **After any full rebuild read `git status`** for files of holdings that were
  not touched.
- **Scripts with backslashes or apostrophes are written to a file and then
  run** (broken four more times on 2026-10-06, each time by a regex in a
  heredoc: there is no exception for "a short one"). In the desktop's Bash tool a heredoc turns `\\[` into `\[` and `\b`
  into a backspace (this corrupted `reference/glossary.yml` once) and fails on
  an unbalanced apostrophe.
- **A one-shot edit script asserts each replacement exactly once.** Commit
  before running it, so a partial failure can be undone. Never run one again
  after it has partly applied: it duplicated summary lines once.
- **Line ends: every text file is LF, everywhere (editor, 2026-10-19).**
  Until then the repository held both kinds: some files were committed with
  CRLF, others with LF, and Git for Windows (`core.autocrlf=true` in its
  system config) turned LF into CRLF on the desktop only. So a script that
  rewrote a file whole, a build on Linux, `sed -i`, or Python's `csv`
  module turned hundreds of unchanged lines into a diff, and every session
  had to check each file before editing it. The fix:
  - `.gitattributes` says `* text=auto eol=lf`: Git stores and checks out
    every text file with LF, on Windows and Linux, whatever `core.autocrlf`
    says. Commit 6ef4dcce converted the 2438 files that were CRLF or mixed,
    and nothing else; it is listed in `.git-blame-ignore-revs` so that
    `git blame` skips it.
  - Before it went to `main`, everything was rebuilt on the branch (every
    holding's `build_db.py`, the merge and site steps, Jekyll,
    `pipeline/verify_site.py`) and the 9135 generated files were hashed before and
    after with CR LF counted as LF: none differed.
  - `build_db.py` and `merge_corpus.py` now write LF (`newline='\n'` for
    text and JSON, `lineterminator='\n'` for `csv`). **A new script that
    writes a file to be committed does the same**: Python's `csv` ends rows
    with CRLF unless told, and `open(..., 'w')` without `newline=` writes
    CRLF on Windows. Other writers still write CRLF on the desktop; Git
    turns it back to LF when the file is added, but `git status` may list
    such a file as changed until then (`git add` it, or `git diff` shows
    nothing).
  - A file with a lone carriage return (`\r` not followed by `\n`) is taken
    by Git for binary and escapes the rule. `reference/name_rulings.json`
    and `units/oe1bu9454/scan_decisions.json` both ended in one; they were
    fixed in the same commit.
  - `git ls-files --eol <file>` tells the truth about a file's line ends
    (`i/` the index, `w/` the disk). `grep -c $'\r$'` in Git Bash reported
    0 for CRLF files: do not trust it.
  - On another clone made before the change, after pulling, Git may show
    every file as modified. `git add --renormalize .` and then `git status`
    should show nothing; if it still does, a fresh clone settles it.
- **`git ls-files` quotes paths with letters outside ASCII** (`Bü` comes
  out as `"B\303\274"`), so a command fed its output fails on those files.
  Use `git -c core.quotepath=off ls-files`.
- **`gh` is not installed on the desktop.** To check the Pages run, read
  `https://api.github.com/repos/takaji10/triebenfeld-letters/actions/runs?per_page=1`
  with `curl`.
- **Marks of doubt** are counted by hand in the edition guide. Recount from
  `dataset/index/uncertainties.json` after any change to a marker.
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

- **A rule in `reference/english_forms.yml` with `\b` in double quotes
  needs two backslashes** (`"\\bGorski\\b"`): YAML reads `"\b"` as a
  backspace and the rule then matches nothing, silently. Run
  `english_forms.py` without `--apply` and see that it would change
  something.
- **`rest.sh`-style scripts with `set -e` stop at the first `grep` that
  finds nothing.** Do not use `set -e` where the steps are filtered through
  `grep`.

- **Two holdings' `intake/photos.py` share a module name.** A holding
  that reuses another's `preview()` must load it by path
  (`importlib.util.spec_from_file_location`), or Python imports its own
  `photos.py` again and the name is missing (716, 2026-10-14).
- **`courtbook.fold_sheet` with image names in a subfolder**
  (`photos/IMG_5163.jpg`): it now takes the base name for the page id.
- **Line breaks in Russian.** `resolve_linebreaks.py` matched words in
  Latin letters only, so a Russian word broken with "¬" was left undecided
  and `build_db.py` reported that the transcription layer changed
  something. Cyrillic is now in `WORD`. And a hyphen after a figure in a
  table cell ("39-", 39 złoty) was taken for a broken word: the test now
  needs a letter before the hyphen, in both scripts. A table has no
  catchwords: two entries of one family either side of a page break looked
  like one ("Хауптъ" / "Хауптъ"), so documents listed under `tables:` are
  skipped in the catchword check.
- **A false glossary or name hit on a verb**: "schenkte" (gave) is raised
  as the name Schenk by `check_translations.py`; "Kuh" (cow) matched the
  person `kuh`. Shut a person out of the document with `not_in` in
  `reference/people.yml`; the translation row needs nothing.
- **Two traps in the literature PDF scripts** (Mielewczyk, 2026-10-22,
  `mielewczyk_pdf.py`). (1) **Test fonts by the layer's own name**, not a
  short form: the script first asked for `'TNR' in font` and nothing was a
  note (the layer prints `TimesNewRomanPSMT`), so the notes ran into the
  body and --check failed on every page with notes; the same bug in three
  places, each found only by the check. (2) **A note's first line is built
  from its span runs, never from a raw join of the spans' texts**: the
  number's span sits with runs of only spaces (after an italic title, the
  print's space is its own italic span), and a raw join loses them
  ("Rolnictwo,w:" for "Rolnictwo, w:"); take the spans over 6.5 points and
  run `span_runs` on them. Related traps already recorded: the paragraph
  whose last run is a raised mark needs the sentence test to look past
  raised runs (`ended()`), and a paragraph's run-over line must never join
  a paragraph of another kind on a page that is mostly figures.

- **The content is rendered before the layout** (2026-10-22, the place
  pages). A generated page's body cannot use the layout's assignments:
  Jekyll renders the content first and inserts it into the layout
  afterwards, so a `{{ t.something }}` in the body renders empty - the
  urls.html include has not run in the content's scope. A generated body
  that wants the site's labels includes urls.html itself at its top
  (pipeline/places/place_pages.py does). Caught on the first build, by the
  eye on the built page (the `<dt>`s came out empty); the verifier's
  section check did not catch it, because it looked for the section and
  not for the labels - a check that a label is non-empty would have.
- **The console's display is not the file** (2026-10-22). PowerShell's
  output mangles UTF-8 on this machine (Polish diacritics become "?"),
  which nearly sent a session to "fix" correct files. When a built page
  looks wrong in the console, read it with Python
  (`python -X utf8 -c "..."`) before changing anything.
- **The translation-review reader had never run with `--unit`** (2026-10-26,
  app534062). Two defects, both fixed in `pipeline/translate/translation_review.py`:
  the module referenced `unitlib` without importing it (NameError on the
  first `--unit` run), and `key()` built the cleared key from the row's
  `letter` while `check_translations.py` filters on `pad` - so an "OK"
  ruling was recorded under a key the checker never matches and the row came
  back at every re-run. The key is now built from the row's `pad` column,
  with the letter as fallback. Lesson on top of the fix: `check_translations.py`
  REWRITES the review sheet at every run, so a ruling typed into the csv is
  wiped by the next check - rule the sheet and run `translation_review.py
  --apply` in one command, before the next check run. (The pre-existing
  entries in `reference/translation_rulings.json` are pad-keyed, as the
  file's own comment says; they predate the bug or were entered by hand.)

## Desktop and cloud

| | Desktop (the editor's machine) | Cloud session |
|---|---|---|
| Raw scans, `review/`, `cache/` | present | absent |
| Paid runs | possible, at the editor's word | not possible (no key) |
| `pipeline/regenerate.py` end to end | yes | no: run the later steps directly (`CLAUDE.md`) |
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
- **The deploy step can time out on its own** (2026-11-06): build and
  verify had passed, and actions/deploy-pages then aborted after ten
  minutes of polling GitHub Pages' "syncing_files". A re-run of the whole
  run (`gh run rerun <id>`, not --failed, the failure being in the deploy
  job) succeeded in the normal few minutes; the live page was checked
  after.
- The "Build and deploy" run can take ten minutes. Watch it in the
  background (`gh run watch <id> --exit-status`) and then fetch one page of
  each kind from the live site: a document is `/documents/<slug>/<n>/`, a
  holding page `/sources/<slug>/`, a scan `/assets/scans/<file>.jpg`.
- **A file the editor leaves beside the scans may belong to other pages.**
  For APP 53/968/0/-/669 (2026-10-14) "Breyer Notes.md" in the folder of
  one notebook's scans was a partial English rendering of a different
  notebook in the same archival unit. Read the pages before relying on
  the file, and ask which notebook makes the holding. Raw CR2 photos can be
  viewed through their embedded full-size JPEG preview.
- **Pages cut by a holding's own script are named by page id** (0002_a1.jpg
  in `processed/`). Its `unit.yml` then needs `raw_glob: "*.jpg"`:
  `stage_pages.py` takes the part before the wildcard as the start of every
  name, and with "Image*.jpg" it staged nothing and said so only by a count
  of 0 (APP 53/968/0/-/669, 2026-10-14).
- **A mark of doubt stays on one line.** "[Krai¬" / "nik?]" across a line
  break made the manifest and the uncertainty index count differently and
  stopped build_dataset.py. Give such a word whole on the line where it
  ends, and say so in the holding's notes.
- **The name list made from the corpus matched half a word broken at a line
  end** ("Emilien¬" as Emilie). Its pattern now refuses a following "¬".
  After adding a holding, read the people and places the index finds in it
  (`dataset/documents/<uid>.json`, `mentions` and `place_mentions`) and shut
  out the false ones with `not_in`.
- **A picture for a spot-sheet row** worked out from a line's place among
  the page's lines misses on a page written only at the top. Space the
  lines at the pitch of the ruled lines, and look at every picture before
  serving the sheet.
- **A new era needs four things beside its entry in `reference/eras.yml`**
  (2026-10-14): a band in `site/_includes/timeline.html` at the first year
  shown that has its documents, a `tl_era_note_<name>` in both languages
  of `site/_data/i18n.yml`, the timeline's year range reaching that year
  (the loop stopped at 1860 and the band of 1936 was silently missing),
  and a section on the story page in both languages. Then the holdings'
  `era:`. An era the editor has not named carries a working name, said to
  be one on the story page.
- **The editor's reading of doubtful words differs from Claude's often
  enough to matter**: on the notebook's sheet three of ten (2026-10-14),
  on Rep. 162 Nr. 295 one of five. A word left marked is not a word to
  build on.
- **Breyer's S before m, w or t** (APP 53/968/0/-/669, 2026-10-14): the
  editor read "Swięcer" and "St?pin" where Claude read "Smięcer" and "Sm…".
  Read such a name against the places of the edition (Swięcia is one) before
  settling it, and do not take the first reading of it without doubt.
- **A Canon CR2 the viewer shows on its side** (APP 53/968/0/-/669,
  IMG_5205, 2026-10-14) carries EXIF orientation 6; the full-size JPEG
  inside the file is stored unturned. Read the orientation tag before
  turning anything: here the picture taken from the file was already
  upright although the editor asked for it turned.
- **Adding a document to a holding read from photos of a table top**: cut
  each photo to the notebook first (the wood around it confuses the fold
  finder and the line positions), keep the photos in a folder under the
  scans folder so that `courtbook.cut` writes the pages to the same
  `processed/`, and give the pages ids that cannot collide with the scans'
  (the photo number: 5193_a2). `save_cache` finds a new document only
  after a build has put it in the database.
- **A spot-sheet picture must show its line whole, with a line of margin
  below** (2026-10-14): two rows of readings4 came back "image is not
  cropped correctly" because the line sat at the very foot of the picture.
  Check that the target line is not on the bottom edge, not only that it is
  in the picture.
- **Years after 1899 were grouped as sums** ("1,907") until 2026-10-14:
  `pipeline/numerals.py` took only 1500-1899 as years, and the edition had reached
  the twentieth century. When an era or a holding extends the edition's
  range of dates, check the numerals rule.
- **`english_forms.py --apply` runs on every English summary**, and a place
  rule rewrote a spelling quoted from the page ('written "Trąpczyn"'). A
  rule for a name must not touch a quoted form; after running it, compare
  the summaries with HEAD and look at every one that changed.
- **A WBC DjVu digitisation** (Karwowski 1900, 2026-10-21). DjVuLibre
  (winget `DjVuLibre.DjView`) gives `ddjvu.exe -format=tiff` for the page
  image and `djvutxt.exe` for a text layer. The text layer is only a check:
  it mangles the Polish letters through the console encoding and can drop or
  guess digits ("1828" was readable only in the image; it read "nowey" for
  the print's "nowej"). Render the page at its default 300 dpi, read the
  image, and re-read doubtful words in word-level crops scaled ×6-10. A
  stray ink fleck can reach both the text layer and the first OCR ("r.
  .1806"); look at the spot before ruling it a mark of the print.
- **A scratch file in the temp folder can shadow the standard library**
  (2026-10-21). `C:\Users\Tersnaus\AppData\Local\Temp\opencode\struct.py`
  from an earlier session was imported by PIL, ran its own main code and
  printed its old output. Run Python from a subfolder (the `djvucrop`
  pattern), never from the temp folder itself.

- **The Minakowska pages** (2026-10-22). A saved page of sejm-wielki.pl is
  written in **ISO-8859-2**, not cp1250 - the first reading turned Łoś into
  "Ło¶" and Dąmbska into "D±mbska"; a byte is the same letter in both
  charset's lower half only by luck. The rule and the method are in
  `docs/LITERATURE_PLAN.md`, section 22. The gender icons are images with
  alt text; the ■ and □ marks stand before a spouse, the filled one before
  the spouse the children beneath descend from (as the page uses it). The
  pages' chrome is dropped by the work's `make_original.py`, keyed on the
  Polish strings; the footer's "Związek z M.J. Minakowską" is a mangled
  byte in the page itself ("Minakowskš"), so the chrome key matches the
  prefix, not the whole word.
- **A new `_dir` under site/ must be declared a collection** (2026-10-22).
  Jekyll ignores any directory beginning `_` whose collection is not
  declared in `site/_config.yml`: the first person pages were written to
  `site/_people/` and the build produced nothing, without an error.
  Declaring the collection (and its `_de` twin, with `output: true` and a
  `defaults:` layout) is part of adding a generated page kind. The project's
  generated page dirs are collections: `_literature*`, `_newspapers*`,
  now `_people*`.
- **`person_pages.py` runs after build_site_data** (2026-10-22), in
  pipeline/regenerate.py's MERGED order, because it reads the generated
  `site/_data/people.yml` and the index's `literature_mentions.yml` and
  writes the genealogy the layout renders. Editing `reference/genealogy.yml`
  alone is not enough: run the script (or regenerate) before building the
  site, or the page keeps the old data.
- **The literature index and only_in** (2026-10-22). A person entry with
  `only_in:` (a list of document uids) never matches in the literature -
  the literature record's uid is not a document's - so the grandson
  Włodzimierz is not matched there, and his bare "Miączyński" would be
  counted to his father Stanisław. The ruling that keeps the grandchildren
  off Stanisław's list is the passage-level `except:` in
  `literature/index.yml`; the mechanism cannot rule per line, so a passage
  that names both the subject and a relative is ruled by whichever the
  passage is about, with the reason in a comment.
- **Concurrent sessions share the working tree** (2026-10-22, seen twice in
  one day). While this session worked, another committed its Mielewczyk
  work onto main and a third created its Łukasiewicz (1997) in the same
  folders mid-run; the shared generated files (`dataset/literature/
  index.json`, `site/_data/literature*.yml`) pick up whatever is in
  `literature/` when the scripts run. Commit only the files the session
  made or alone modified, leave the shared generated files uncommitted,
  and say so in the report; a fresh rebuild regenerates them from the
  committed works. A verify failure naming a work this session never
  touched is that work's session's in-flight state.

- **The second Minakowska page, three lessons** (2026-10-22). The database
  renders its pages in the reader's language: Helena Zielonacka's page was
  saved in the ENGLISH interface ("Parents", "Married about 1720 to"),
  where the first was Polish - so a work of this database takes its
  language from the page as saved, and a work with `language: en` has no
  `english.md` (Mączak's case; the chrome keys of `make_original.py` are
  per work, keyed on the language's own strings). The ID tells where the
  person's entry comes from: `2.976.216` is an entry of the online
  Boniecki's article 2.976 - the article the edition holds as
  `boniecki1900` - and the first thing to check is what that work already
  carries of the person. And a page's subject may be no person of the
  edition at all: `standalone: true` in `reference/genealogy.yml` gives
  the block its own heading and bio, the page drops the documents section,
  and `literature_passages:` names the literature by hand; `person_pages.py`
  validates the shape, and a source may name a work without a passage
  (the work's own page).
- **`genealogy.yml` and the "ca"** (2026-10-22). The first block had
  silently dropped a "ca" (Stanisław Miączyński "ca 1849-1860" was written
  "1849–1860"); the rule says a "ca" keeps its "ca". When a date moves from
  a source into the genealogy block, diff the token against the source, not
  against memory.

- **YAML duplicate keys shadow silently** (2026-10-22). The miaczynski
  section of `literature/index.yml` had TWO `Miączyński:` keys - the
  second, added for the first Minakowska work, was shadowing the first
  (which carries the zychlinski exceptions), and safe_load raises nothing:
  the three exceptions were simply dead. When adding a ruling, merge into
  the existing key; never add a second one of the same name. A `--check`
  that passes does not catch this - only reading the section as text does.
- **The Minakowska pages vary in their section set** (2026-10-22). The
  first page had no Rodzeństwo section (the database knew no siblings of
  Antoni Prusimski), the third does - so `make_original.py` stops the
  editor's selection at the first section outside it (here Rodzeństwo,
  there the mother's other marriages), not at a fixed heading. New marks
  the third page brought: "hr. [tytuł] nadany" (a count's title granted,
  translated "count [title] granted"), the Towarzystwo Rolnicze districts
  as offices, the page's own Wikipedia line (kept), and the status list
  with its "(linia: …)" markers joined into one line.
- **A genealogy page can sharpen a date the edition only inferred**
  (2026-10-22). The letters of 1815 name Miączyński the husband; the
  edition inferred "about 1814"; the database's page cites the marriage
  act of 17 August 1810. The conflict is shown on the site (both, the
  flag beside the new date) and nothing is corrected until the editor
  rules - NEEDS_CONFIRMATION carries it.
- **An `only_in` person is invisible to the literature index until the
  dedup asks `applies()`** (2026-10-22). The edition's `trampczynski`
  entry carries `only_in`, so its pattern cannot fire in a literature
  uid; the extra-pattern route would have supplied the hits, but the
  dedup in `literature_index.hits()` dropped them - it asked only whether
  an edition pattern of the same slug fullmatched the surface, not
  whether it could apply to the record. Fixed (2026-10-22,
  `minakowska2026ottotrampczynski`): the dedup now asks `applies()`
  first. Lesson: when a work's hits come out as zero while the text
  plainly carries the name, suspect a fence (only_in, not_in) before
  suspecting the pattern.
- **A standalone block's slug must not be an entry's slug** (2026-10-22).
  The fourth Minakowska page's block was first keyed `trampczynski` - the
  family entry's own slug - and the page took the family's heading and
  bio from people.yml, the block's bio nowhere on it. The block was
  renamed `wojciech-otto-trampczynski`; the collision and the rule are
  recorded in the block's comment in `reference/genealogy.yml`. The
  family entry itself keeps no page (it never had a genealogy block).
- **Reading a Fraktur scan with no local Tesseract** (2026-10-23, Werner
  1904). The editor's machine has no `tesseract` on PATH; the *lunaroute*
  document converter (`tools.lunaroute.convert_document`, base64 of the
  image through the Code Mode `fetch` of a local `python -m http.server`,
  since the tool takes no local path) read the 1904 Fraktur well at three
  scales - whole page, bands, single lines cut by a dark-pixel row profile.
  Whole-page and band passes garble names; the line cut at 3x was the pass
  to trust, with doubtful words re-cut at 6x. Fraktur rules used throughout:
  ſ reads as f or j, kt as ft, ſch as sch, the print's "=" is a hyphen,
  O reads as D (Orangeriehaus), ß as f (Neßla). Where two passes disagree
  on letters that change a name, the word goes to the editor on a scratch
  spot sheet (`scratch/slowo1892_sheet.py` pattern) - the first use of that
  pattern for a literature work, its answers to `review/<slug>/`.
- **The WBC's challenge: do not fight it** (2026-10-23). The
  `dlibra/.../content` and `doccontent` URLs answer a proof-of-work browser
  challenge (a JS MD5 puzzle writing a `captcha_pow` cookie that does not
  clear server-side); solving the puzzle locally got the same challenge
  back. The `docmetadata?id=N` page answers without any challenge and
  carries the full DC/citation metadata - take the bibliographic facts
  there and read the text from the editor's saved images.
- **An incomplete sibling work stops the whole literature build**
  (2026-10-23). `build_literature.py` walks every `literature/*/work.yml`
  and dies on the first without an `english.md`; a concurrent session's
  half-built work (`slowinski2023`) therefore blocks any other session's
  rebuild. `scratch/build_literature_without.py <slug>...` shadows
  `literature/` with directory junctions minus the named works and runs
  the build's own `main()` against the shadow: nothing of the skipped work
  is read or built, and the next full run picks it up. The build also
  rmtree's `dataset/literature/` - running the full script with a
  concurrent session's untracked passages present would delete them; the
  shadow avoids that too. Where only the shared `index.json` is impure (a
  concurrent build added an entry whose sources are uncommitted), filtering
  the entry out of `index.json` with a one-line script is the smaller
  touch - the passages and pages are then regenerated from the filtered
  index.
- **An English that comes with the editor's file is still read whole**
  (2026-10-22, the Lidmanowski batch). "The transcription is secure" does
  not extend to a translation carried beside it: the three texts' English
  had eleven artifacts against the Polish, among them a sentence printed
  twice, "several dozen rubles" for kilkanaście (some fifteen) and
  "woolen sailor suit" for ubranie marynarkowe (a jacket suit). Read it
  paragraph by paragraph against the original, correct in the item's
  english.md, and record every correction in the notes with the Polish
  that decided it.
- **Fixing generated YAML by string pairs: fetch the wrap first**
  (2026-10-22). The item.yml files are written with a 76-character flow,
  so a phrase meant for a replacement-pair script is often hyphen-broken
  or line-wrapped inside itself ("des Guts-/  diensten", "der Gutsdiest —"
  with the der on the line before); eight of one pass's 44 pairs missed
  on that alone. Read the actual lines before writing the pairs, or use
  the edit tool on prose files and keep scripts for uniform fields.
- **Learned-journal items in the newspapers**: the citation's "issue" is
  the zeszyt (fascicle), and it goes in the slug's issue place
  (`zdrowie1912z10`, `jutrzenka1913z8`, `zdrowie1914z6`), the way a web
  item's date stands there (`twojaslupca20150706`); the journal's own
  masthead and the library's metadata may style the paper differently
  (Jutrzenka: "popularno-naukowy" in print, "ogólno-kształcący"
  in the metadata) - cite the library's form, record the print's own in
  the notes. An article's authorship can rest on the issue's table of
  contents alone when the print carries no signature; say so in the
  account rather than filling `author:` on the file's word alone.
- **verify_site's leak check and a shared quoted source** (2026-10-23):
  two books may both quote the same letter (Kraus 2001 and the hidden
  Seidel 2018 both carry the letter of 12 October 1811), and the 60-
  character needles of the hidden work then match the shown work's own
  page. The leak scan now skips the built pages of the works shown on the
  site (a shown page is the editor's authorised text in full; a hidden
  work's own page is still checked strictly). Checker internals - decided
  in session, recorded in the changelog.
- **Two sessions, one working copy** (2026-10-26): a second session may be
  working in the same checkout (its work showed up as modified files and a
  new `units/` folder mid-session). Before `git checkout -b`, run
  `git status`: a checkout in the shared directory moves the other
  session's branch under it. Work in a worktree instead
  (`worktree_create`, then `session_move` onto it) and give the worktree
  its own branch. **The worktree lacks the gitignored `pages/`**, and a
  `regenerate --site` run there then rewrites every unit's
  `page_scan_map.csv` with `gap` rows (the images are what the mapping
  pairs against; the db is built before the mapping, so the site itself
  survives). Junction the worktree's `pages/` to the main checkout's
  (`New-Item -ItemType Junction`) before any build, and put the new
  holding's staged pages there too. Recovery if it happened anyway:
  `git checkout -- units/*/page_scan_map.csv` and the other churned
  generated files, then rebuild.
  **And when the merge comes** (2026-10-26, publishing): remote `main`
  moves while you work - fetch and merge immediately before pushing, and
  expect a second merge if the other session pushes in between. Resolve a
  generated-file conflict by taking either side and rebuilding
  (`pipeline/regenerate.py --site` rewrites them all), but anything spliced into
  those files by hand goes with the side you took: this holding's summary
  lines vanished with `site/_data/summaries*.yml` taken from the other
  side, and `holding.py --summaries` had to be run again. The guide's
  hand-kept figures (documents, pages, translated, undated, marks of
  doubt) must be recomputed against the merged state, not either side's -
  the merged truth was 629 documents on 2,089 pages in 50 holdings, 625 of
  629 translated, 19 undated, 910 marks of doubt.
  **And the worktree you merge in is not necessarily on `main`**
  (2026-10-26, the same evening): check `git branch --show-current` in the
  target worktree before merging there. A merge meant for main was run in
  the cemeteries worktree and fast-forwarded the `cemeteries` branch
  instead - reset the foreign branch back to its own tip and move `main`
  with `git branch -f` (branch checked out nowhere) or a fresh `git
  worktree add` for main. The degradation a merge can carry in also sits
  deeper than the guard: the merged state's `dataset/units/*/letters.json`
  had lost the scan fields (built where the staged images were absent) -
  after a merge, run the build once and commit the repair it makes, not
  only the `page_scan_map.csv` restore.
- **A table with no column of entry numbers** (2026-10-26, APP 53/21/0/-/
  Pyzdry Gr.115): `unitlib.table_of` sorted a table by its first column's
  numbers and crashed (`StopIteration`) on a table that has none - the
  parish stands in the first cell and the figures follow. It now sorts such
  a table with every figure row in the body and the rows above the first of
  them in the head; `render_table` puts the first cell with the name, not
  the number column, and applies no total styling, judged over the whole
  table (a closing page of a numbered table has no numbers of its own - the
  scope was wrong once and the before-and-after check caught it). The
  check: `pipeline/review/verify_table_of_diff.py`, the pristine and the new code
  over every existing table, parse and render. And a trap in the checker:
  `check_unit_text.py`'s `digits()` reads a comma-run of a table row
  ("…,31,62,124") as one thousands number ("31,62124"), so figures quoted
  from such a row fail the citation check unless the document's summary
  carries them with spaces ("31, 62 and 124") - the summaries are part of
  the checked haystack by design; write the summary before rebuilding.
- **A generated page loop that reuses the language loop's variables**
  (2026-10-26, cemetery_pages.py): a per-language cleanup loop
  (`for lang, (folder, base, other) in BASES.items()`) leaves `lang` and
  `folder` bound to the LAST language, and a following per-item loop that
  writes pages with them writes every page into one language's folder -
  the English folder empty, the German one with all ten, no error raised.
  Destructure the language inside the item loop, and after writing a
  section's pages COUNT the files per folder before building - the
  mismatch showed up only as broken links in the verifier, one step
  downstream.

## The layout (2026-10-28)

- **All code lives under `pipeline/`.** `unitlib.py`, `numerals.py`,
  `new_unit.py`, `regenerate.py` and `verify_site.py` moved there on
  2026-10-28 (run them as `python pipeline/regenerate.py --site`,
  `python pipeline/verify_site.py`). Every script that imports `unitlib` or
  `numerals` puts both the repository root and `<root>/pipeline` on
  `sys.path`; a new script copies the pair of lines from a neighbour. The
  moved files compute their root with two `dirname` calls.
- **The generated dataset is `dataset/`** (it was `corpus/`). A holding's own
  transcription is still `units/<slug>/corpus.txt`, and the `corpus` key in
  `unit.yml` and `merge_corpus.py` keep their names.
- **Finished working files go to `docs/archive/`** (the Prusimski-era
  questions and spot sheet, the early context brief), not into `docs/`'s
  top level or the repository root.
- Older notes and `docs/CHANGELOG.md` cite the old paths (`corpus/`,
  `python regenerate.py`) and were left as written; read them with the
  renaming in mind.
- The move changed no output: `pipeline/regenerate.py --site` before and
  after gave byte-identical `site/_site`.
- **A full rebuild blanks a holding's scan map where its raw scans are not
  in `pages/`** (found 2026-10-28): `match_scans.py` rewrote
  `units/app5320pozgr1181/page_scan_map.csv` with every image empty
  ("gap, check"), Gr.1181's scans being in another checkout. The verifier
  does not catch it. After a full run, look at `git diff units/*/page_scan_map.csv`
  and restore any map that lost its images (`git checkout -- <file>`), then
  run the merged steps again (`regenerate.MERGED`) and the site build.
  **It happened again** (the faithfulness review's rebuild of 2026-11-04
  blanked Gr.1181 and Ossolineum 2289, and the blank maps were published;
  the editor found it 2026-11-19): a note is not a guard. Now
  `match_scans.py` pairs from the web copies in `site/assets/scans/` when
  `pages/` holds none of a holding's pages, and `verify_site.py` fails when
  a page of a holding with scans shows none (unless its map row's note
  says why, as Oe 1 Bü 9454's missing letters do). The maps were restored
  from their last good commits; the line ranges were unchanged.
- The committed `dataset/` had gone stale after the register's Grądzyń
  pattern was widened (the gazetteer's sources commit) and was rebuilt on
  2026-10-28; the literature index's three unruled pairs were ruled by the
  editor the same day (Grądzeń the modern name of Grądzyń; Kolonia Lisewo,
  not the village of Lisewo; "Rogaler" the Rogall hymn-book).

## Polish surnames in -o read back from the genitive (2026-10-28)

A Polish masculine surname ending in *-o* declines like a feminine noun in
*-a*: Fredro, Fredry; Kościuszko, Kościuszki; **Turno, Turny**. A book that
names a man only in the genitive ("pełnomocnika Szczepana Turny") gives a
false nominative if read back as a noun in *-a*: the gazetteer's "Szczepan
Turna" came so from Chodyła p. 49, where p. 52 has "Szczepana Turno" and his
mother "Turnowa". Before writing a surname from a Polish oblique case, find
it in the nominative, or in the undeclined form, in the same source.


## Rewording the site's own prose (2026-10-29)

- **What may be touched.** The editor, 2026-10-29: a pass over the site's
  own prose never touches the transcriptions, the reading copies or the
  translations - nor a translator's note inside a translation (`english.md`
  of a work: the "edition" pass changed Janocki's "[T.N.]" lines and they were
  put back). The timeline and the static pages wait for a rewrite of their
  own. No paid run. The review plan is `docs/VOICE_REVIEW_PLAN.md`.
- **Find the text on the built site, then its source.** Scanning the source
  files for a phrase misses text kept in attributes (`data-en`, the date
  basis) and finds internal notes no reader sees; scanning `site/_site` with
  tags stripped misses attributes too. Scan the raw HTML, then locate each hit's
  source by a 50-character fragment, whitespace normalised (folded YAML wraps
  sentences across lines).
- **A summary or a date basis lives in more places than its source.** The
  date basis of a document is in `rulings.yml` and, keyed by the English, in
  `reference/site_notes_de.yml`; the built copies are in `dataset/`
  (documents, `letters.csv`/`.json`, the unit's copies), which only
  `build_db.py` rewrites. Rather than a full rebuild (it blanks the scan map of
  a holding whose scans are not here), apply the same edit to the `dataset/`
  copies.
- **`build_literature.py` empties `dataset/literature/`**, and
  `mentions.json` comes back only from `literature_index.py --check`. Run the
  two together, as `regenerate.py` does, or the dataset loses 4.5 MB.
- **Rule-based rewording needs reading after.** Regex rules over prose
  ("The edition has ..." -> "It has ...") also caught "The edition has these
  pages" and wrote "It has these pages". Every sentence such a pass changes is
  read before it is published. The reading of the 444 changed sentences
  (2026-10-29) found about 40 to put right by hand: German sentences that lost
  their verb, "the ground" left where "the edition's ground" stood (now "the
  area", "das Gebiet"), a dangling "it", "der Sammlung" where nothing was
  needed. Extract the pairs from the commit's diff (old sentence against its
  closest new one) and read them all.
- **German has two words for it.** The German texts call the site both
  "Edition" and "Ausgabe" ("der Grund der Ausgabe", "die Literatur der
  Ausgabe"); a search for one misses the other. "Ausgabe" also means an
  issue of a paper and a database's version ("Ausgabe der Datenbank vom
  22.10.2026") and, as "Ausgaben", expenses: those stay.
- **Traps met:** Python's `re` refuses a variable-width look-behind (`(?<=[.:;]\s+)`);
  a replacement written as `'\1'` through a Bash heredoc reached the file as
  the control character U+0001, which YAML then refused - write such scripts
  with the Write tool and use `chr(92)` or raw strings (the 2026-10-13 shell
  traps, again).
- **Count sentences by paragraph.** A scanner that collapses a Markdown page
  into one string runs a bold run-in heading ("**The bond, 1805.**") and the
  paragraph's first sentence into the sentence before: the holdings' pages
  showed 111 "long" sentences that way, 66 once `voice_scan.py` split at
  paragraphs and headings first.
- **What went to a Sonnet sub-agent, and how.** Splitting the holdings'
  sentences of more than 60 words (85 of them, listed in
  `review/voice/holdings_long.yml`) is mechanical: the sub-agent got the list,
  hard rules (no fact, name, number or quotation changed; markup, footnote
  marks and links kept; only the listed sentences; no commit) and a report to
  write. Its diff is read in the main session before anything is committed.
  The rewriting of accounts, cards and link sentences stayed in the main
  session (the batches in `review/voice/`, applied by
  `pipeline/review/set_work_texts.py` and `set_link_texts.py`).
- **`check_unit_text.py` kept the old dash rule.** It failed every English
  holding page with an en dash, the rule of before 2026-10-20 ("no dashes at
  all"); since then the spaced en dash is the rule (HOUSE_STYLE, "Typography").
  It now fails only an em dash or a hyphen standing for a dash. When a style
  rule changes, look for a check that still enforces the old one.
- **Changing a summary: `pipeline/review/set_summaries.py`.** It rewrites the
  site's copies, the holding's `summaries_de.yml` and the cache
  (`cache/summaries-raw[-de]`, on the desktop), then `build_dataset.py` and
  `build_site_data.py` carry it on. The drafting scripts
  (`intake/summaries_draft.py`) are changed only where the old text stands as
  one string; where they split it over several strings they keep the older
  wording, as the record of how the summary was first written, and the
  script says "draft not found".
- **A sub-agent stopped by the usage limit keeps its work.** Two Sonnet
  sub-agents stopped mid-task on the five-hour limit (2026-10-29); after the
  reset a SendMessage to each ("continue from where you stopped; do not
  split anything twice") finished the job without starting over.
- **"How it was prepared" without the repository (2026-10-30).** The
  editor agreed: method stays on the tab, file and script names,
  NEEDS_CONFIRMATION, the spot sheet and dated rulings go (HOUSE_STYLE, "A
  holding's own page"). Five holdings carried them, all added 2026-10-25/26
  (53/4/0/-/62, Pyzdry Gr.115, Poznań Gr.1181, -/782, a date in -/716): the
  tab was written from the session's own notes. Write it for the reader, and
  check it with `voice_scan.py` (the `method-repo` flag) before committing.
- **A list item begun with "– " is no list item.** 53/4/0/-/62's tab had
  ten items (four in the German) written "– " instead of "- ", since the day it was added;
  Markdown ran them into the line above. `check_unit_text.py` now fails a
  line that starts with an en or em dash and a space. A dash pass must leave
  a line-initial "- " alone.

## The mentions' robustness pass (2026-10-31)

The editor asked whether the tagging of people still finds the connections
it was built for. It does where it was built to, and its limits turned out
to be places where nothing forced a look:

- **Zero-mention documents were invisible.** 60 of 630 documents carry no
  tagged person; 30 of them are 15 lines or more, and two of those are the
  correspondence's own (`oe1bu14526-30`, 137 lines; the 1820 contract
  `app539680782-1`, whose Samuel Adolph is in the text and tagged nowhere:
  people.yml had only `prinz-adolph`, whose pattern demands a title). The
  blank is not an error anywhere - nothing fails - which is why it never
  surfaced. `pipeline/review/zero_mentions.py` now ships the sheet on every
  rebuild, with heuristic lead tokens (post von/zu/honorific, -schen forms,
  minus stopwords and authorities) to say which blanks are real blanks.
  Rulings go to `reference/zero_mention_rulings.json`, which the sheet
  reads back. It does NOT gate: an honest empty record passes.
- **The other datasets' slugs had no check.** literature/newspapers hits
  are ruled per (name, spelling), but nothing held a ruled row's slug to
  the people/places authorities: a mis-spelt slug would silently name
  someone the edition publishes nothing about.
  `pipeline/review/check_mentions_join.py` is that check and is a gate in
  `pipeline/regenerate.py`, placed after the two index steps. Valid person
  slugs are people.yml ∪ the corpus index ∪ genealogy.yml (Hans von Held
  proves curated-without-corpus is a real case; Głowecki and Lidmanowski
  prove press-only people are); valid place slugs are places.yml ∪ the
  gazetteer (Lisewska Kolonia proves gazetteer-only is real).
- **The gazetteer checker is a gate now.** It passed on the day it was
  wired (120 entries, 173 footnotes, 79 links resolved).
- **`docs/DATA_MODEL.md` had drifted far.** It still said 441 documents,
  claimed places merely named were unindexed while `place_mentions.json`
  had existed for weeks, and offered `August` as a defect the data no
  longer had. A standing reference that describes last season misroutes
  every session that trusts it; it now matches the build and got the new
  fields' rows (`era`, `estates`, `repository`, `scans`, `places_named`,
  `rough_transcription`, `mentions_english`, `is_missing`, `seq_archival`).
- **Python's `re` has no branch reset.** A `(?|...)` alternation of
  same-numbered groups fails to compile; give every branch its own group
  and read `m.group(m.lastindex)`.
- **The dataset manifest's `text_path` is dataset-relative** (`text/uid.txt`,
  not `dataset/text/uid.txt`). A visitor script that joins it to the
  project root reads nothing and reports empty.
- **"Always tag a Zelmer/Celmer/Zellmer" was already in force; the work is
  proving it and writing it into the ledger.** All of the family's forms sit
  in one curated entry (`zelmer`): `match: (?:[CZ]ell?mer|Цельмер)\w*`
  catches Celmer, Cellmer, Zelmer, Zellmer and the Russian tables' Цельмеръ
  with their inflections, wherever the document is from, and the seed tail
  is skipped wherever a curated pattern matches. A coverage test over
  `dataset/text/` found every strong form and every Cyrillic run inside a
  tagged document - 28 mention rows over 7 documents, none untagged - and
  found no new spelling the entry does not name. A variant `match` already
  finds is dropped by `_pattern_for`, so the four `variants:` lines are
  documentation, not machinery. The standing rule is recorded in
  EDITORIAL_RULES.md and at the entry. The proving found the gap that is
  real: `mentions_english` comes only from the translation's own `names`
  marks, and the five older units that name the family have none - their
  English pages say the Zelmers with no link (TODO 58; a translation pass,
  the editor's word, money).
- **The full `regenerate.py` has been locked since something drifted.** Its
  first step is the code-hygiene gate `pipeline/check_pipeline.py`, which
  exits 1 on five files that carry a holding's facts in code - `new_unit.py`
  (the `--archive` default), `review/drop_form_and_language.py`,
  `review/set_np_titles.py`, `review/set_short_titles.py`,
  `review/write_prepared.py` (per-unit literals, exactly what the rule
  against naming a holding in code governs) - with 23 problems and three
  files already `# pipeline-check-file:`-waived. Nothing downstream ran, so
  no rebuild could start: the checks the two previous commits wired in were
  each run alone and never met the lock. Proven pre-existing by rerunning
  the gate on a stashed-clean tree, exit 1 both ways. The checker's own
  principle is the right one: "silence with a reason attached is a
  decision; silence without one is a bug waiting to be rediscovered."
  TODO 58 carries the choice: waive each file, or refactor the literals
  into `units/<slug>/`. Today's affected steps were run directly, in the
  merged order `regenerate.py` itself defines, skipping none of the checks
  that gate them.
- **Two stdout wrappers close each other.** A visitor script that wraps
  `sys.stdout` with `io.TextIOWrapper(...)` and then imports a pipeline
  module that does the same loses its wrapper mid-run ("I/O operation on
  closed file"): when the first wrapper is collected, closing it closes the
  buffer both were built on. Import the pipeline module first and let it
  own the wrapper, or rewrap nothing.
- **A module-level loop variable answers a comprehension that names it.**
  `for n, r in stmt.items():` leaves `r` (and `k`, `v`) bound at module
  scope; a later comprehension that writes `row_vals[r]` without binding `r`
  silently reads the leftover dict and returns nonsense instead of raising.
  It bit twice in one session (the hits' row attribution printed every row
  as "total"; the spatial test's `ok` clause compared against the whole
  statement). Name loop variables uniquely at module level, and inside a
  comprehension bind every name the body uses.

## The holding pages: header, languages, "How it was prepared" (2026-10-30)

The editor's ruling of the day, in three parts; the work is in the branch
`unit-pages-tightening`.

- **The header.** The page's heading is the holding's translated title
  (`card_title`, the German `card_title_de`); the original title stands under
  it, and the reference number stands beside the archive's name
  (`53/4/0/-/62 · Archiwum Państwowe w Poznaniu`). The browser tab names the
  holding by its title too (`unit_pages.page_title`). The languages of the
  documents are one line of the facts under it (`languages:` in unit.yml,
  `reference/languages.yml`).
- **No "Form and language".** The editor: the physical descriptions (hand,
  ruling, leaf numbers, film frames, abbreviations) are useless; what changes
  how a document is read is not. So the section is gone from 48 holdings in
  both languages; the sentences that matter (the basis of a date, a part not
  transcribed, which sheet is the original, a spelling kept) were moved to the
  end of "Contents", and the whole old text is in each holding's `notes.md`
  (`drop_form_and_language.py` did it once). The same test applies to any new
  page: say what the reader needs to understand the source, not what it looks
  like.
- **"How it was prepared" tells the AI's part only.** It is written from
  `prepared:` in unit.yml (`reference/prepared.yml` has the sentences, in both
  languages), so it stays short and the German is not written holding by
  holding. HOUSE_STYLE, "A holding's own page", has the four questions and the
  list of what stays in the notes. The old accounts are in each `notes.md`
  under "How it was prepared (the public text before 2026-10-30)"; there is no
  `process.md` any more. A new holding fills `prepared:` when the work is done.
- **Traps.** A heredoc to `python -` in this shell can turn `\n` into a real
  newline inside a string, which breaks the script with a SyntaxError that
  points at a string; write such a script with the Write tool, or use Edit.
  A sentence splitter that breaks at "L. S." cuts a quoted abbreviation in
  half: check the kept text of a split by printing it before applying.
  `[[unit:...]]` is a link, not a citation: a paragraph with only that still
  needs `<!-- context -->`.
- **"Paraph" is a real word and not a typo** (a short mark an official puts
  after or instead of a signature), but it reads like "paragraph" to a
  newcomer. Reader-facing English says "initials"; the German keeps "Paraphe",
  the term of the German finding aids; `docs/GOVERNMENT_FILES.md` and the
  notes keep "paraph" as the working term.

## OCR of a Fraktur print (2026-11-01)

The Dorow (1843) sitting's lessons, for the next pre-1850 German print:

- **Tesseract needs the Fraktur model.** The `deu` traineddata of
  `%LOCALAPPDATA%\Tesseract\tessdata` (the newspaper work's install) does not
  read Fraktur type; it was only ever used on 20th-century Antiqua. The model
  that reads it is `script/Fraktur` from tessdata_best, now fetched into the
  same directory beside `deu`, `pol` and `pol-std`, so
  `pipeline/ocr.py`'s `tessdata()` finds it: `read(img, lang='Fraktur')`.
- **The Fraktur model's standing noise** (learned over 12 pages of Dorow):
  the long s comes through as `ſ` (transcribe `s`); the capital `J` of the
  face is the letter I (transcribe `I`, as the editor's own Materialien file
  does); the `ch` digraph is often dropped (`niht`, `durh`, `beschützen`);
  the `tz` ligature is misread as `ß` (`benußt` for benutzt, `Saß` for
  Satz, `Küß` for Kütz) or as `st` (`Eigennust`); stray marks ride at line
  ends. Restoring `ch` and `tz` by German orthography is safe; what the
  passes genuinely disagree on goes to a spot sheet.
- **A clean reprint of the same text beats a second OCR engine.** The
  Materialien (1861) reprints Dorow's memoir in extract in the editor's own
  file; a `difflib` word-diff of the draft against the reprint settled most
  doubts in a stroke and exposed the 1861 compiler's own additions, slips
  and normalisations at the same time. Where a session cannot reach a second
  engine (the lunaroute converter takes only a URL or base64, and the
  sandbox could reach neither the SBB's IIIF nor a local server), look first
  for a reprint of the text already in the project.
- **Image-only PDFs split by page** (`fitz.insert_pdf` one page at a time)
  are the way to feed a converter later; and a 245 MB digitisation PDF
  renders its 240 images fine with `get_pixmap(dpi=300)` page by page.
- **Unnumbered leaves consume printed numbers in some 1843 volumes**: the
  memoir's title and motto leaves are the volume's pp. 11-12 without printed
  numbers, the contents list the piece at p. 11, and the text begins at
  p. 13. Check the neighbour pieces' numbers before assuming an offset.
- **Page numbers of this print stand at the top of the page**, so a page's
  own OCR begins with the number - handy for checking an offset, but strip
  it before transcribing; the signature marks at the page foot ("I 9",
  "I 10") are furniture, not text.

## The mobile overflow pass (2026-11-01)

The editor reported an overflow on the literature page on mobile; the whole
site was checked with a headless browser (puppeteer-core + the machine's
Edge, served locally), first a sample then every page. Lessons for the next
layout work:

- **A grid item's automatic minimum is its min-content, and an image with
  `width: 100%` counts its intrinsic width into it.** This is the standard
  grid blowout: the 400px list thumbs made every card refuse to shrink
  below ~432px. `min-width: 0` on the item (and the inner column's item)
  is the fix; the same mechanism bit the map page's sticky stage (whose
  viewer derives a width from its height through aspect-ratio).
- **Text overflowing its box does not widen any element**, so a
  getBoundingClientRect crawl reports nothing while `scrollWidth` grows:
  long tokens (bare URLs in notes and footnotes, a licence URL in a facts
  line) overflow as ink. When a page overflows with no offender listed,
  recurse by hiding blocks until `scrollWidth` drops - the guilty subtree
  shows itself; then look for the long token.
- **A `<select>`'s intrinsic width is its widest option's.** Any filter bar
  that must survive a phone needs `min-width: 0` on the label and the
  select (the label is a flex column; the select then stretches to the
  shrunk label).
- **`white-space: nowrap` on generated links is a trap** whenever the link
  text is data: a document reference ran 350px, a Minakowska section
  heading 427px. Let them wrap; nowrap is only safe for text you control.
- **Wide data tables scroll inside their block**: `display: block;
  max-width: 100%; overflow-x: auto` on the table itself is the one-rule
  fix (the literature's and the map pages' tables; the cemeteries' wrap
  had the room but lacked `overflow-x: auto`).
- **The crawler** (in the session's temp folder, `mobilecheck/`): list the
  built pages, `page.setViewport` at 360/390/320, measure
  `documentElement.scrollWidth > clientWidth` after `domcontentloaded` +
  250ms, and report the widest elements' rects. It needs the site rebuilt
  and served (`python -m http.server` over `site/_site`).
- **Not done, offered:** a read of the other pages for descriptions that exist
  for their own sake (the literature's, newspapers' and places' account /
  brief / summary say the same thing three times; "Scans"-style handling
  sentences were the same problem in the process tabs). A pattern scan found
  nothing like it in the people's bios, the cemeteries or the place pages.
- **The tab labels (2026-10-30, the editor).** "About this holding" is now
  "About" (German "Beschreibung") and "How it was prepared" is "Method"
  (German "Methode"): `unit_tab_about` and `unit_tab_prepared` in
  `site/_data/i18n.yml`. The docs call the tab "Method"; older entries in the
  changelog keep the old name.

- **The newspaper pages (2026-10-30, the editor).** They were laid out
  differently from every other source: a title that was a paragraph, an
  account, a caveat and a hint above the text, and a clipping at full width.
  The page is now built like a document page (NEWSPAPERS_PLAN, last section).
  The rule that came out of it, for any new page: **the title is a title** (the
  headline as printed, or a few words), the facts are one line, the
  description is the brief, and what a page says about itself is one caveat
  at most. `pipeline/review/set_np_titles.py` set the new titles once.

- **Page titles (2026-10-30, the editor).** The tab title of a page is a
  short form of its name, never a slug ("Echotureckie1931018") and never a
  paragraph. A newspaper item's page had no `title:` and the layout fell back
  to the slug; a holding's tab used its whole translated title (up to 660
  characters). Now the newspaper pages carry `title_en` / `title_de`, and a
  holding with a long `card_title` has `short_title` / `short_title_de`
  (`set_short_titles.py` set 24 once). After a build, list every page's
  `<title>`: no slug-like one, none over 70 characters.


## The Related column (2026-11-01)

The literature's call-outs were reworked (LITERATURE_PLAN, section 32):
per-passage notes in `links.yml`'s `about:`, the heading "Related"/"Bezüge",
a gutter column from 64rem with a toggle in the viewbar. Lessons:

- **A CSS grid on only some siblings shows in the rules.** The first plan
  put every passage in a two-column grid; the passages without entries
  would then carry a shorter border-top than the ones with (or every rule
  would run the page's full width). The built shape: the grid only on
  `.lit-passage.has-related`, capped at 60rem, other passages unchanged —
  the rules are ragged between linked and unlinked passages, and that is
  the honest shape of it; do not "fix" it by widening every rule.
- **The entry's own measure**: the gutter column's `min-width: 0` is what
  keeps a long token in a note from blowing the column out (the grid
  lesson above, again); the notes' links wrap like text (the nowrap lesson
  of the mobile pass applies to them as to all generated links).
- **`about:` is validated at build time, both directions**: every passage
  of a many-passage link needs an entry, no entry may name documents
  outside the link's own list, and every link document must belong to at
  least one passage — the last rule is what keeps a link from carrying a
  document no passage of it can show. A one-passage link must NOT carry
  `about:` (its sentence is the note) — the build says so if it does.
- **PowerShell appends CRLF** (`Add-Content` on an LF file put a `
` at
  the end); the repo's files are LF (`newline='\n'` everywhere). Appending
  to a text file here goes through Python, and afterwards check
  `data.count(b'\r\n') == 0`.
- **A session branch cut from an in-progress branch carries that branch's
  unpublished work.** `related-callouts` was cut from `pelzucki1896`, so
  "merge into main and push" would have published the Pełzucki map work
  too (marked in progress, a second session still working on it). Before
  publishing: `git log --oneline main..branch` and read what is actually
  in the delta, not what the session worked on. If the delta carries
  another piece of work, cherry-pick the session's own commits onto main
  in a worktree (this working copy stays where it is, the other session's
  uncommitted files untouched), verify the build on the cherry-picked main
  before pushing, and say in the paperwork that the publish was by
  cherry-pick — a later whole-branch merge is then a content-noop for
  these files. The editor decides what goes live (asked, 2026-11-01: only
  the session's own commits).
- **The verify gate's link count fell with the rework** (326 pairs before,
  302 after): the count is the number of (document, link, passage) pairs
  actually rendered, and the per-passage document subsets mean fewer pairs,
  not a weaker check — each rendered pair is still checked on both sides.

## The cross-holding connections (2026-11-01)

Built from the editor's questions: how to find connections across all the
documents, and the step folded into adding any source (CONNECTIONS.md).
Lessons:

- **The per-passage lesson generalises**: a connection's note is written
  for the page it stands on — each participant its own `en`/`de` — the same
  rule the literature's `about:` entries obey. A shared sentence was the
  original sin of the old call-outs; do not reintroduce it on the document
  side.
- **`lit_doc` in i18n is the reference label both link kinds share**
  (`"%s, document %s"`): connections_site.py reads it, so the wording of
  the document references stays in one place. The build reads the *whole*
  i18n file (it needs both languages), like literature_site.py.
- **Document pages are single-URL** — the language is swapped in-page
  (`data-en`/`data-de` spans, letter.js), not by a `/de/` address: a check
  script that fetches `/de/dokumente/...` gets a 404 that means nothing.
  The Related entry's links therefore carry `data-en`/`data-de` like the
  literature's do.
- **The verify gate's two link blocks sit side by side** (the literature's
  302 pairs, the connections' 8): both read the generated `_data` file and
  walk the built pages, so a new kind of cross-reference that wants a
  both-sides check has its pattern right there — copy the block, not the
  idea.

## Non-German text in the line-break resolver (2026-11-01)

- **`resolve_linebreaks.py` decides on German evidence and cannot see
  Polish.** With ossol2289 (a Polish letter) its DWDS check read every
  Polish word as unattested and marked five of six wraps `split, review`;
  the decisions were made by hand from the sense, each with its reason,
  in `units/ossol2289/linebreak_decisions.csv`. The file is hand-editable
  by design, so this is the intended path for a non-German holding - but
  expect the resolver's defaults to be wrong for one, not right.
- **The resolver's word-regex has no Ć/ć.** Its WORD class carries
  ĄąĘęŁłŃńÓóŚśŹźŻż but not Ć ć, so a wrap whose halves end or begin in ć
  loses the letter: the row for "nara|żać" came out with tail "ża" and
  joined "naraża" until the row was corrected by hand to "żać"/"narażać".
  Check any row touching ć against the corpus text before trusting it.
- **The full-build order for a new unit, on this machine:** per-unit
  steps (resolve_linebreaks, resolve_paragraphs, build_db, match_scans),
  then `merge_corpus.py`, `build_dataset.py`, `build_site_data.py`,
  `make_thumbs.py` (the card thumbnail the verifier checks for - a
  missing one is a broken-link failure, not a warning), the translations'
  publish, then `jekyll build` and `verify_site.py`.
  `pipeline/regenerate.py --unit` and `--site` wrap these, but the
  pipeline self-check (`check_pipeline.py`) currently fails
  project-wide on pre-existing debt (23 problems in checked-in files,
  identical on main before any of this session's work) and stops the
  wrapper; running the underlying steps directly is the working path
  until that debt is cleared.
- **Image delivery can fail outright after a request-budget error**
  (2026-11-01, the Ossolineum sweep): every later read returned "Image
  read successfully" with no image content - a known-good band re-read
  and a small diagnostic crop included, files on disk intact. Not a size
  issue; an endpoint-side failure. Rule: stop reading images, do not
  narrate from undelivered calls, verify with one small diagnostic crop,
  and move to text-only work until delivery recovers. Leaf 0061 of the
  Ossolineum set is parked on exactly these terms.

## The faithfulness review and the fix implementation (2026-11-04)

- **The summaries have two homes and the build cannot carry them.** The
  628-pad site/_data/summaries.yml and summaries_de.yml include summaries
  written in working sessions whose pads have no entry in
  cache/summaries-raw[-de]/ (the in-session holdings: app5320pozgr1181,
  app534062, app539680545, ossol2289 and others). summarise.py --build
  assembles from the cache alone, and its lost-summary guard - rightly -
  refuses to write a file that drops a live document's summary. So a
  summary correction must be written to the cache where the cache has the
  pad AND to the generated file; it cannot be carried by a --build. The
  same for a translation whose holding was translated in session
  (app5320pozgr1181 has no translation-raw entry at all): fix
  site/_data/translations/<uid>.yml directly.
- **The translation cache is split by tag; check both before saying a
  cache file is missing.** Most holdings sit in cache/translation-raw/,
  but oe1bu14526, oe1bu9454, iiihamdaiiinr12765, oe1u199,
  ihagrrep7cnr3570 and ihagrrep7cnr3705 sit in translation-raw-v2/
  (unit.yml binds them). A cache miss in the untagged directory is not a
  miss; and publishing those units needs publish_translations.py --tag v2.
- **publish_translations.py refuses a stale sheet after cache edits.**
  Its guard compares the review sheet's mtime against the newest cache
  file; editing the cache makes the cache newer. After hand-applied cache
  fixes, republish with --force (the edits were already review-approved)
  or re-run check_translations.py first.
- **One language clean is not both clean.** oe1bu9454-285: the English
  summary's reversed grantee was fixed; the German summary carried the
  same fault and was first judged not at fault - against the German
  corpus, which fails the same way. A finding proven in one language must
  be tested in the other before it is closed.
- **Rewrites slip on the dash rule.** check_unit_text caught an em dash
  the fix agents introduced into app536047's about.md (the spaced en dash
  has been the rule since 2026-10-20, HOUSE_STYLE). Any hand- or
  agent-written prose in the tracked files goes through the checker before
  it is called done.
- The regenerate wrapper's self-check block is known (see the session
  above); the working path there was a small driver importing
  pipeline.regenerate and replaying its step lists (PER_UNIT, MERGED,
  POST_UNIT, jekyll, verify_site) without the check - the lists are
  imported, not transcribed, so the order cannot drift.
- The review's own artefacts stay out of git (review/ is ignored by
  design); what travels is the prompt doc, the fixes and these notes. The
  selection sheet's choices live in the editor's browser and the exported
  JSON, not in the repository.

## The Pełzucki 1896 map: labels, plots and proper names on the site (2026-11-06)

- **A selected label draws no name on the labelling page, and the editor
  reads that as "not saved"** (2026-11-06, the bulk marking): the page's
  design hides a selected label's form text (only finished labels draw
  theirs), but until this sitting nothing released the selection — Enter in
  the form field did nothing for an existing label, a click on empty map
  space did nothing, Esc did not let go — so an edit looked unsavable and
  the name never came back. The fix (Enter commits and releases; empty-map
  click releases; Esc releases when no step is in progress) is in
  pipeline/maps/label_page.py and written into the page's own help; the
  general rule for any marking page: **every editing action needs a visible
  commit that returns the page to the state the editor expects to see**, or
  the silent persistence reads as failure.
- **A hint that says "press a key" is void while a text field holds the
  focus** (2026-11-06, the same session's second report: the auto-fill
  pause's "a type key overrides" — with the form field focused, the key
  typed its character into the form, and on a saved label the type keys did
  nothing at all; the only path ran through the unlabelled "Change what it
  shows" button). The fix: the type buttons stand in the pause itself
  (clicking one keeps the pause, the form still to be typed), a type key
  overrides when pressed in the EMPTY form field or on a selected saved
  label, and the help carries the whole workflow. The general rule: a
  keyboard hint must name where the focus has to be, and every hinted
  action needs a mouse path beside it.


- **A state endpoint needs `Cache-Control: no-store`, or the browser edits
  history.** The save server's `/__save/state` answered with `Last-Modified`
  and no cache header; the browser heuristically caches such a response for
  a tenth of the file's age, so a reload after a save could hand the page
  the pre-save state and a window could save against a version the file had
  outgrown. The test battery failed on exactly this, erratically; the fix
  is three headers on the state, version and save answers of
  scratch/map4456/save_server.py (the editor's own server carried the same
  latent bug). Any JSON endpoint whose answer must track a file belongs on
  this list.
- **A test suite that hardcodes the dataset's shape breaks silently when
  the data moves.** Nine suites assumed the pre-import world - the baked 73
  labels, farms 12/20/78 unmarked, `83` the sample unsure red - and after
  the editor's import put labels on 83 farms, they failed with symptoms
  pointing everywhere but the cause. Counts should be read from the data or
  asserted once at the top; a suite that needs an unmarked farm must create
  one (remove the label) rather than assume a row stays unmarked; a suite
  that clicks a pill by its reading must resolve the pill by its record's
  own position, because a row number repeats on every parcel of its farm.
- **A page's status wording is part of its contract with its tests.** The
  labelling page says "Restored" whenever ANY working state file has
  content - even the reds' alone. A suite waiting for "Loaded" must start
  from an empty sandbox, not from whatever the previous suite left; the
  100-label state one suite beached cost the next an hour of looking at the
  wrong end of the page.
- **Two processes can listen on one Windows port**, and the requests then
  split between an old build and a new one: port 8791 held two servers from
  October, serving the previous site build, while the fresh build answered
  on the same port number elsewhere. `Get-NetTCPConnection -State Listen`
  before believing which build a local port serves; kill by pid, not by
  "the port is taken".
- **Edit a generated YAML file with its own writer's parameters.** The
  published translations are written by `yaml.safe_dump(..., width=100)`,
  which folds long scalars across lines - a surgical regex over the raw
  text fights the folding and loses. Loading, changing the one field and
  re-dumping with the same call reproduces the canonical shape; the check
  that matters is parsed-data-equality against the expectation, not a
  diff of the raw text (folding alone moves hundreds of lines).
- The whole integration pass is recorded in docs/CHANGELOG.md
  (2026-11-06): the imported labels and field numbers, the plots layer, the
  grey ruling, the proper names on the map and in document 6's translation,
  the 14-suite battery and the real-browser check of the built site.
- **Retiring a feature the editor drew by hand is a one-line revert if the
  data file stayed separate.** The farm plots lived in their own
  maps/pelzucki1896/polygons.yml with the carry-through isolated in one
  `if os.path.isfile` block, so the editor's "this method wasn't reliable,
  take it off the map" cost: delete the file, drop the block, lift the
  button/CSS/JS out, rerun the builder. Keep each experimental layer's data
  and plumbing separable like this - the judgement about the method (the
  polygons drifted from the parcels) need not burn the work that fed it
  (the drawing tool and its JSON stay in scratch/map4456/ as the record).
- **A computed string can change type between two YAML readers.**
  PyYAML writes the string `1,167` unquoted (legal, and PyYAML itself
  re-reads it as a string); Jekyll's Ruby YAML takes the same plain
  scalar for the integer 1167 - the comma silently gone by render time.
  A generated value that one language's YAML may read as a number must
  not dress as one: plain digits, or a string with a letter in it (the
  Morgen column's `1,643 M 138 r` was safe for exactly that reason).
  The general form: when two programs read one generated file, test the
  round trip through the SECOND reader, not the one that wrote it.
- **A headless browser's failed-resource console error names no URL.**
  The page's own favicon 404 read in the console exactly like a page
  resource failing, and a filter on the message's text could not tell
  them apart - the message carries no address at all. Watch the
  responses instead (`page.on('response')`, status 400 and up, by URL)
  and leave the console for exceptions and script errors
  (scratch/map4456/check_sat_overlay.py).

## The genealogy explorer and the deployment prefix (2026-11-06)

The explorer hung on "Loading the family database" for a visitor while the
site built and verified clean. The cause was a deployment-shape assumption
that no check covered: the vite build carried `base: '/genealogy/'`, an
absolute bundle path that is correct only when the site is published at a
domain root. This repository is published as a project site
(takaji10.github.io/triebenfeld-letters/), so the browser asked for
/genealogy/assets/app.js one level too high, got the server's HTML 404
page back, and the module load died on the disallowed text/html MIME type
- Firefox's console names the MIME, not the missing path behind it. The
lesson generalises: **a hard-coded absolute path in a built asset is a
silent bet on where the site is published; every reference a build tool
emits should be relative (base './') or templated from the baseurl, and a
link checker that wants to catch this class of bug must resolve relative
URLs the way a browser does - against the page's own directory - and be
run once with the project baseurl and once without.** A missing module
also never reaches the application's own error handling, so the static
boot page carries the guidance (shell.html's inline watch: script error or
15 s timeout, hard-reload, blockers, settings, a link home), and the
application's boot screen reports progress over the eight opening files
and after eight seconds admits that a blocker or a slow connection can be
holding the database back. Found by the editor's Firefox console; the fix
and the checks are recorded in docs/CHANGELOG.md (2026-11-06).
- **Svelte 5's mount() appends to its target; it does not replace what is
  inside.** The static boot placeholder inside `#app` therefore survives
  the mount and sits above the rendered application - invisible until the
  application first really loaded in production, then unmistakable. Clear
  the target by hand (`target.textContent = ''`) before `mount()`, and
  wrap the mount in a try/catch that leaves a word on the page if the
  component itself fails to start - after the clear, a thrown mount leaves
  a blank page with the watch already stood down.
- **A fixpoint of pairwise rules can deadlock against itself.** The
  exclusion's old rule (b) kept a child with one kept parent, and the
  spouse was that kept parent - so a removed sibling's line survived its
  own removal, each rule holding the other's subject alive. When a cut
  has an "except through X" clause, compute the two reachable sets
  (from the cut seed, from the protected root) and subtract - walks
  cannot deadlock, and the invariant (nothing protected is ever removed)
  is checkable in one line. The sibling lesson: when a graph rule keeps
  failing to remove what it names, suspect two rules leaning on each
  other, not one rule applied wrongly.
- **A URL join is only as right as its shortest test.** The media
  manifest's file fields were relative to the repo's media/ directory,
  the config base omitted media/, and every image on the site 404ed into
  the viewer's "image not published" fallback - visible for days,
  reported for one person's two records. Assert one built URL per shape
  (image, thumb, originals/) against the live host in the site checks;
  a join that no test ever fetches is a join nobody has run.
- **Svelte 5 template identifiers must be declared, but the compiler
  only warns for some.** Tree.svelte iterated an undeclared `links` and
  compiled clean - the route threw a ReferenceError at first render,
  invisible until someone opened it. When a component compiles but a
  route has never been seen working, render it once headlessly (or read
  the compiled output for the bare identifier) before trusting it.
- **The second failure of the exclusion cut was the mirror of the
  first.** The fixpoint kept a removed line alive through its kept
  spouse; replacing it with a blood-only walk then left the in-laws'
  natal families standing behind the removed spouses - the editor
  found Trzeciaks and Klowaks the ruling had clearly named. Blood is
  not connectivity: a marriage is a real edge and the families behind
  it are real members of the world being cut. When a cut is defined by
  belonging ("everyone connected to X only through Y"), partition by
  reachability in BOTH worlds and subtract - and check the result by
  asking the data the question the editor will ask ("is any of these
  surnames still there?"), not by trusting the algorithm's own count.
- **Islands need naming, not walking.** Two [Living] Trzeciak
  placeholders had no recorded link to any person - unreachable by any
  graph rule, invisible to every check that reasons over edges. The
  honest tool is an explicit named list in the config (exclusion.people),
  reported like every other removal; a surname heuristic would have
  been neither visible nor reversible.
- **A decorative effect with an unbounded spread is a page-wide
  overlay waiting to happen.** The media viewer dimmed the photo around
  a focus rectangle with a 9999px box-shadow and no clipping ancestor -
  correct-looking while no image ever loaded, then a grey film over the
  whole page the day images worked. Any "dim everything but X" effect
  must be clipped to the container it belongs to (overflow: hidden on
  the frame), and ideally seen once with real data before shipping.
- **d3-flextree for anything tree-shaped.** The hand-rolled genealogy
  layout drowned in its own special cases (couples, focus rows,
  hourglass folding) and still overlapped cards. The standard
  tidy-tree algorithm with variable node sizes (d3-flextree, WTFPL,
  bundles clean with Vite) takes the geometry; only the genealogy
  semantics (who is a child, where spouses sit) belong in our code.
  API trap: call layout.hierarchy(data) then layout(tree) - the layout
  function on raw data wraps it halfway and the nodeSize accessor meets
  a node without .data.
- **setPointerCapture retargets every later pointer event to the
  capture element - click included.** The tree viewport captured the
  pointer for panning and the cards' onpointerup never fired. Moving
  the handlers onto click failed the same way: the Pointer Events spec
  retargets the compatibility mouse events (click, auxclick,
  contextmenu) to the capture element too, and Firefox follows the
  spec. When a surface must both pan and host clickable children, do
  not hang the clicks on the children's events at all: read the target
  under the press at pointerdown (closest on data attributes), decide
  click-vs-drag by pointer travel at pointerup, and run the action from
  the container's own handlers - capture then harms nothing.
- **A portrait is a picture of the person, not a document about
  them.** The avatar pass first fell back to "first publishable media",
  which would have dressed hundreds of people in their birth
  certificates; the editor's "some people will have actual pictures"
  means pictures - photo/portrait-titled media only (51 people here),
  placeholder disc for everyone else. When a rule maps a class to a
  representation, check what the representative actually is.
- **SVG text does not wrap; textLength is the fitter.** For card
  layouts with variable names, lay the words by hand into lines and let
  textLength/lengthAdjust="spacingAndGlyphs" compress any line that
  would still overflow - character-count estimates alone stay estimates
  (fonts vary by script and weight). A single unbreakable token needs
  its own ellipsis; wrap-then-compress-then-ellipsis covers every name
  shape.
- **A PowerShell round-trip can silently mojibake a source file.**
  Reading UTF-8 bytes as cp1252 (the console's default codepage) and
  writing UTF-8 back turns every … › – into â€¦ â€º Ã¢ - the build
  still succeeds, the damage only shows in the rendered glyphs. When a
  scripted edit touches a file with non-ASCII text, list the file's
  non-ASCII character set afterwards; encode-cp1252/decode-utf-8
  reverses this particular corruption.
- **Two id dialects meet at every Gramps join: @I0001@ (GEDCOM) vs
  I0001 (data.gramps XML).** The avatar pass found zero candidates with
  a plain membership test that "looked" right both sides. Strip at the
  boundary (one .strip('@') at the join) and assert the join's yield
  ("1077 avatars to crop" - a zero that should not be zero is the bug
  speaking).
- **A reused variable from a previous loop iteration is a silent
  cross-talk bug.** The index avatar assignment wrote into `row`, which
  was only assigned when a photo entry existed - 1,034 avatars landed
  in other people's rows and 43 in the right ones, all plausibly
  looking like "some people have pictures". Bind the target before any
  conditional writes, or the previous person's row inherits them.
- **A genealogy viewer wants a window, not a canvas.** Rendering the
  whole descendant forest of the oldest-known ancestor made a
  117,000-px SVG that no browser pans comfortably; the editor's model
  - show children and grandchildren, an arrow renders the next step
  while the previous derenders - keeps the chart at ~30 cards and the
  navigation honest (the arrows advance one generation; specific
  branching goes through the card's detail panel, whose "centre here"
  re-roots in place). The general shape: a view window plus frontier
  queries (hasMoreUp/hasMoreDown decide whether the arrows show at
  all), never a full-graph layout.
- **A region box means what the drawer used it for.** The Gramps focus
  rectangles on record scans mark where the person's name sits on the
  form (a finding aid for the reader), not where their face is - only
  on photographs do they mark the face. Cropping "whatever has a
  region" turned 1,037 avatars into slivers of handwriting before the
  editor caught I1706. Before reusing any annotation as geometry, ask
  what kind of media it was drawn on: the same gesture means different
  things on a photograph and on a register.
- **Equal-specificity rules fight by source order, and the loser is
  whichever came first.** `ul.people { margin: 0 }` after
  `ul.kids { margin-left: 2.4rem }` silently zeroed the indent. When a
  variant must override a base rule in Svelte-scoped CSS, give it more
  specificity (two classes), not a later position.
- **Read the deploy log before rerunning.** Four identical-looking
  failures at deploy-pages were not four transient blips: the action's
  own 5-minute status-poll timeout was killing a deployment that (by
  the fourth attempt's log) was genuinely still syncing. Rerun helps
  when the run dies of a service error mid-flight; it does nothing when
  every attempt dies of the same built-in deadline. The action exposed
  a `timeout` input all along - raising it to 20 minutes fixed it.
- **Don't hide the ID column to fit a screen.** The mobile audit's
  tempting fix for the six-column People table was dropping the Gramps
  id on narrow screens - but the editor's standing ruling is that the
  id appears wherever a person does. A sideways scroll inside a
  wrapper keeps both: the data intact, the page unbroken. When space
  and a ruling conflict, scroll beats omission.
- **An SVG clips its children to its own box.** The tree's pan/zoom
  transform lives *inside* the SVG, so any translated content outside
  the SVG's width/height vanished - invisible, not merely off-screen.
  The empty big tree (2026-11-07) was exactly this: the viewport grew
  to 80vh, the load centring put the focus at y≈308 in SVG
  coordinates, the SVG was 296 tall, and every card clipped away. The
  standard pan/zoom setup is `overflow: visible` on the SVG with the
  clipping left to the wrapper element; design a chart so the transform
  can move its content anywhere, not so the initial view happens to
  fall inside the canvas.
- **Render on demand, not everything that exists.** A genealogy chart
  that draws every descendant of a prolific family grows past any
  screen (21 of them for I0272) and zoom-out cannot rescue it - at the
  scale where it fits, nothing reads. Progressive disclosure (the
  children visible, the grandchildren behind +badges, one branch open
  at a time) keeps the chart at reading size and turns "seeing
  everything" into "walking anywhere", which is what a reader actually
  does. The bounded resource (screen width) needs a bounded render,
  not a smaller font.
- **Keep the reader's place unless they aimed somewhere.** A control
  that modifies content (open a branch, close it) must not also move
  the camera: the centring effect keyed on expansion state and snapped
  the view back on every badge click. Separate "what is shown" from
  "where it is shown" - navigation acts re-centre, content acts leave
  the viewport alone. And when a re-layout moves many things at once,
  let the DOM elements persist (key by identity, position by a
  transitioning transform) so the change reads as movement instead of
  a flash.
- **Freezing the transform is not freezing the view.** When a re-layout
  recomputes the chart's coordinate base, a stationary transform shows
  different content - the badge click "moved the view" even after the
  centring effect stopped running. Anchoring a chosen content point to
  its previous viewport position (record before, re-read the derived
  layout after, solve the transform) is what "the view does not
  change" actually means.
- **Key the drawn elements, not just the data.** An animation between
  two layouts needs DOM elements that survive the re-layout: nodes
  keyed by person, links keyed by their parent>child identity. Without
  link keys the each-block patches by index and a surviving path is
  assigned a different link's geometry - morphing across the chart.
  Enter/exit fades on the same keys are what make newly revealed rows
  appear as part of the movement rather than popping in after it.



## The Timeline rebuilt, the eras as pages, the story page retired (2026-11-07)

The editor's brief: combine the eras and timeline pages into one Timeline
page — the eras introduced, under each a brief timeline of the events that
matter to Trąbczyn (primary) and Zagórów (secondary); each era's introduction
one paragraph with a Read more link to a proper era page, whose detailed
narrative quotes its sources inline; the timelines completely rebuilt, no
document counts, 1-2 compact sources per event, no skips between years; a
link to each era's documents kept. Questions asked and answered first: the
story page is REMOVED (a brief introduction stays on the home page, which
already had one in the right voice; the nav's first item, renamed
Introduction, points at the home page); English first, German after approval;
era pages at /eras/<slug>/; the editor's eras.yml blurbs rewritten for the
Timeline page (their text stays in the register and git history).

- **The events data rebuilt** (site/_data/timeline.yml, rewritten from 102
  events to 69): each event carries `era` (an editorial assignment like the
  documents' — the insurgency years sit inside the Hohenlohe ones), `when`
  (display date; `when_de` later), a concise note, and `sources` (1-2, as
  text+url, linked to our document, literature or newspaper pages; the
  territorial.de link for the Drommin renaming is the one external). Dropped
  by the importance rule: the Ląd-internal events (the 1362 Drzewce forest
  exchange, the 1447 and 1461 Łukomia purchases — the editor's own
  examples), the purely personal ones (the marriage separation, the burial,
  the daughter's death), and the sub-steps whose substance lives in the
  era pages (the 1777 decree-entry order, Pszczew, Oleśnica, the Erbet
  lease, Humboldt, the Kammergericht). Added: the twentieth century had no
  events — the 1911 parceling of Włodzimierow, Breyer's 1935/1936 visits,
  and the 1940 Drommin renaming (from the estates.yml renamed field's
  citation). The old German notes are gone with the rewrite; /de/zeitleiste/
  falls back to the English notes until the German pass — reported to the
  editor.
- **The Timeline page** (site/_includes/timeline.html, rewritten): per era —
  label, who held the estate, the narrative intro (intro_en, new field in
  reference/eras.yml; German falls back to the editor's blurb_de), Read more
  where an era page exists (page_en/page_de flags), the era's events
  (era-events.html, shared with the era pages), the documents link
  (?era=). The per-year bar chart, its counts and its ⋮ skips are gone.
- **Seven era pages** at /eras/<slug>/ (site/eras/*.md): the Hohenlohe page
  moved from /hohenlohe/ (its stale pointers fixed, the events block added
  at the foot), six written new — narrative prose in the story page's
  voice, inline links to every source quoted, glossary links on first use
  (Olęder → /glossary/#haulaender, Morgen, starost, South Prussia), and
  each foot carrying the era's events and its documents link. The honesty
  markers stay where the corpus is thin ("A fuller account of these years
  is still to be written"; "this era is one document deep").
- **The story page retired**: site/the-story.md and site/de/die-geschichte.md
  are redirect stubs to the home pages (a new `redirect` layout, meta
  refresh + canonical + location.replace, no plugins); /eras/ and
  /de/epochen/ redirect to the Timeline; /hohenlohe/ and /de/hohenlohe/
  redirect to the era pages' new addresses. The navbar: Introduction
  (home), Timeline, Sources, People, Places, Genealogy, Glossary, About —
  Sources moved up to third; nav.story/nav.eras gone from the i18n
  (letter.html's i18n dict carries nav_introduction now); urls.html lost
  u_story and u_eras; about.md and de/ueber.md point their "tells this in
  order" sentence at the Timeline.
- **Verified**: build_site_data passes (the run had been broken on main —
  the Ossolineum holding's correspondent Tadeusz Kościuszko had no entry in
  reference/correspondents.yml; added, title "General, in exile in Paris"
  per the documents-first rule); gazetteer --check passes; Jekyll build;
  verify_site passes (its era check retargeted from /eras/ to
  /timeline/); the mobile check passes on all eleven new and redirected
  pages at 390/360/320; screenshots of the Timeline and an era page
  checked by eye.
- **Two traps, both PowerShell's**: Get-Content -Raw without -Encoding
  reads UTF-8 as ANSI, so a `-replace | Set-Content` round-trip mojibake'd
  the moved Hohenlohe pages (Jekyll then demoted them to static copies —
  the build "succeeded" while dropping two pages; only verify_site's broken
  links exposed it). And Set-Content on Get-Content-catenated UTF-8 parts
  mangles the same way — file concatenation for the repo belongs to Python
  or the edit tool, never the shell pipeline. Liquid's `sort` on the
  events' `date` needed uniform types: Psych reads `1173-08-31` as a Date
  and `1814-09` as a String, so the dates are quoted strings now.
- **Still open**: the German pass (the Timeline's intro paragraphs, the six
  era pages' German mirrors, the events' when_de/title_de/note_de — the
  German story page is a redirect meanwhile, so German readers have lost
  the narratives until it lands); the nav labels' German ("Einführung"
  set); NEEDS_CONFIRMATION entries for the curation judgement calls.
  [SETTLED 2026-11-07, the editor's word after their read of the English
  ("This is looking much better"): the German pass is done — see the next
  section.]

## The German pass and the Introduction off the navbar (2026-11-07, afternoon)

The editor's follow-up: remove Introduction from the top navbar; write the
eras pages for each era (the seven English pages were already in place from
the morning — verified and kept); the German versions of all the era pages
and the timeline; the home page updated if necessary; publish.

- **Introduction off the navbar**: the nav opens with Timeline now; the
  nav_introduction link, the i18n keys (en, de) and letter.html's
  i18n-dict line are gone. The home page stays as it is (the editor's "if
  necessary": the hero, the figures, the cards and the About paragraphs
  carry it, and the brand link still leads home).
- **The events' German fields** (timeline_german.py): when_de, title_de,
  note_de and sources[].text_de on all 69 events — fresh translations of
  the condensed English notes (the old German notes were fuller than the
  new English ones and no longer matched), with the old file's terminology
  kept (Burggericht, Landgericht, Krontribunal, Kondeszension, Erbpacht,
  Vorwerk, Hufe, Turmhaft). The include renders text_de/when_de on the
  German side; /de/zeitleiste/ is fully German now. The file's section
  dividers were restored on the rewrite (the previous safe_dump had
  consumed them) and a BOM that had slipped into the file is gone.
- **intro_de + page_de: true** for all seven eras (eras_intros_de.py):
  /de/zeitleiste/ shows the German narrative intros instead of falling back
  to the editor's blurb_de, and its Read more links open the German era
  pages.
- **Six German era pages written** (site/de/epochen/*.md, translations of
  the English ones with the Liquid links and glossary anchors kept —
  /de/glossar/#haulaender and friends); the German Hohenlohe page (moved
  this morning) had its stale pointers fixed ("Eine von drei Epochen" → the
  Timeline pointer, "die dritte Epoche... noch nicht veröffentlicht" → the
  link to the restitution page) and its events foot added. The English era
  pages got their alt_url back (the German counterparts now exist), so the
  language switch works both ways.
- **The caveat, recorded in NEEDS_CONFIRMATION**: the editor does not read
  German, so the German prose (intros, era pages, event notes) is
  machine-authored and awaits a German reader's review before it is treated
  as settled. The German terminology follows the site's existing German
  text throughout.
- **Verified**: build_site_data, gazetteer --check, Jekyll, verify_site
  (58,951 internal links, 0 broken — the drop from 60,244 is the removed
  nav link, ~1,300 counted instances), the mobile check on all nine German
  and mixed pages at 390/360/320, screenshots of /de/zeitleiste/ and a
  German era page checked by eye.

## The mobile-readiness re-check (2026-11-07)

The editor asked for a mobile/responsiveness check of the whole site
(excluding the genealogy section). The 2026-11-01 crawler was rebuilt
(puppeteer-core + Edge, `$TEMP/opencode/mobilecheck/`): all 2,490 built
pages at 390, 360 and 320 px, served from `site/_site`, measuring
`documentElement.scrollWidth` after load + 250 ms, 6 pages in parallel
(the full sweep is ~4 minutes per width; 2,490 pages ≈ 25 s/100).

- **The site is mobile-clean**: 0 overflows at 390 and 360; at 320 exactly
  one defect — the German Pełzucki 1896 map page overflowed 15 px. The
  fix: `flex-wrap: wrap` on `.map-tools` (the German overlay link
  "Kartenüberlagerung auf OpenStreetMap ansehen" was squeezed to its
  min-content and the bar's total min-content exceeded 320 by exactly the
  link's overshoot; the English page passed because its text is shorter —
  the same trap, the language decides). Re-crawl: 0 problems at all three
  widths. Re-checked the three crawler "errors" individually — all clean;
  they are races (a navigation destroying the execution context,
  documentElement briefly null), so the crawler's error lines are noise to
  re-run, never findings.
- **Reading an overflow report needs the ancestor walk.** The 320 report
  named the farm table (456 px) as the offender, but its wrap clips
  correctly — a clipped element's rect still reports its layout width, so
  offenders lists name clipped descendants that cannot extend the
  document. The real extender was found by walking the ancestor chain and
  then listing only elements *outside* every clipping container; its right
  edge matched `scrollWidth` exactly.
- **Screenshots at 390** (home, sources, letter, places, literature, the
  map page): the navbar wraps to two rows, cards stack, the letter viewer
  adapts, the Sources icons sit beside their headings, the wrapped
  `.map-tools` reads as two deliberate lines, the farm table scrolls
  within its wrap. No visual defect found.
- **The check became pipeline (2026-11-07, the editor's word: new map
  pages will keep coming)**: `pipeline/mobile_check.py` +
  `pipeline/mobile_check/crawl.js` in the repository — the temp-folder
  crawler was one editor question away from vanishing. The wrapper starts
  its own server on a free port, keeps puppeteer-core in a persistent
  cache under the system temp (never `node_modules` in the repo), copies
  the crawler out to run it (so `require` resolves), and enumerates pages
  three ways: `--map <key>` (the map's en + de pages — ADDING_A_MAP
  step 9, after the pages are built), `--pages` (list or file), `--all`
  (everything built, the genealogy section excluded). Proven three ways:
  the five map pages pass, a planted overflowing self-test page fails
  with exit 1 and the correct offender, and `--all` (2,490 pages,
  320-only) re-confirms 0 problems. The offender logic now walks the
  clippers itself (elements with overflow auto/scroll/hidden/clip): only
  elements outside every clipping container are named, so the report
  points at the real extender, not at clipped descendants whose rects
  report their full layout width.

## The bulk maps batch and the Łukom re-backing (2026-11-06)

- **Łukom 1766 re-backed onto the archive's JPG (2026-11-06).** The editor's
  word: the map of record is 1_407_0_0_283-29_0001.jpg as drawn, not the
  rotated north-up PNG they had georeferenced. The transfer probes ran the
  full ladder - SIFT full-affine, whole-image rot180 at matched scales,
  anisotropic rescale, centred paste, a local discrepancy grid, a GCP-patch
  sweep (72 angles x 3 scales), all 8 dihedral orientations - and every one
  failed photometric verification: the PNG is a different raster, not a
  transform of the JPG, so the eleven marks cannot carry over and the editor
  re-marks (their offer stood). Recorded in maps/lukom1766/notes.md; the
  PNG-era labels/positions/georef archived in png-record/; the register now
  has view_rotation 0 (the JPG's lettering reads upright as drawn) and no
  mapwarper field; tiles re-cut (346 files), georef.json removed, the
  labelling page rebuilt - the map waits for the editor's marks on the JPG.
- **A helper copied without its guards is a bug factory.** The GCP sweep's
  fft_ncc was re-typed from lukom_affine.py without the two float32 casts
  added there after the float32-integral lesson: with uint8 input, img*img
  overflowed (255^2 mod 256 = 33), the local-variance term went negative
  everywhere and the low-variance guard zeroed the whole output - the sweep
  'found nothing' because the correlator was broken, not because the maps
  disagreed. Copy the function, not a paraphrase of it; run the self-match
  check (a template taken from the search image must come back ~1.0) before
  reading any sweep's result as a negative.
- **Env-dependent output paths bite across shells.** tiles.py cuts into
  TRIEBENFELD_MAPS if set, else ROOT/../triebenfeld-maps - a fresh shell
  without the variable silently tiled 15 MB into an unversioned folder
  beside the worktree while the git repo kept the old tiles. Check where a
  pipeline script's output actually landed (timestamps in the target repo)
  before believing its success line; export TRIEBENFELD_MAPS in every shell
  that runs tiles.py.
- **The bulk labelling pages are rebuilt, not looked for (2026-11-14).** The
  batch's 23 sheets and their index were built in a side worktree
  (`review/` and `scratch/` are not committed), whose git link later broke,
  so the main checkout had only three sheets. To pick the marking up again:
  `python pipeline/maps/label_page.py <map>` for each map, then
  `python pipeline/maps/label_index.py` (the to-do list; moved out of
  scratch into the pipeline 2026-11-14), then serve `review/maps` on
  **port 8780**, the port the editor
  marked on: the browser keeps unsaved work per site and port, so a
  different port shows empty sheets. `.claude/launch.json` has the
  configuration `map-labelling`. The to-do list leaves out every map
  published with `in_project: true` (it reads the register on
  origin/main), so run it again after each publish; Łukom 1766 has its row
  since 2026-11-14.
- **The labelling page: one button saves, and nothing else does (the
  editor's report, 2026-11-14).** Choosing a type other than the
  gazetteer's re-rendered step 3 with a second row of type buttons that
  saved at the next click and jumped to the next place: the editor saw the
  label "reset". And the trace's end put the cursor in the form field, so
  [ and ] typed into it instead of setting the band. Rules since: an
  action that only chooses must never also save; saving has its own
  visible button (Create); focus is never moved into a field the editor
  did not click, where the step's keys are wanted. Test the page on port
  8791 (`map-labelling-test`), not 8780, so the editor's browser storage
  is not touched, and clear the test origin's storage afterwards.
  The same holds for editing a saved label (the editor, the same day): its
  edits used to be saved at every keystroke, silently, while the list kept
  showing the gazetteer's form, so nothing told the editor the change had
  taken. Now the edits wait for a red Save changes, the list shows the
  label as saved, and leaving unsaved edits asks. A list that shows a
  record must show the record, not the template it was made from.
- **A map's card thumbnail follows its tiles (the editor, 2026-11-14).**
  Łukom 1766's thumbnail kept the face of the old north-up PNG for eight days
  after the map was re-backed onto the JPG: make_thumbs.py skipped any map
  thumb that already existed. It now fetches the served whole-map picture and
  rewrites the thumb when the bytes differ. When a map's image changes, run
  `python pipeline/build/make_thumbs.py` and `map_pages.py`, and look at the
  thumb.
- **"The map tiles did not load (HTTP 503 ...)" is GitHub Pages, not the
  tiles (2026-11-14).** The editor saw it on the published Mapa dróg 1890;
  the same info.json answered 200 a few minutes later and the page opened.
  Check the URL with curl before suspecting the tiles or the push. The
  viewer (`site/assets/maps/map-viewer.js`) now retries the opening three
  times and each tile (`tileRetryMax`) before it shows the message. To
  test a change to that path, copy a built map page into `site/_site`
  with the info.json address changed to a missing map, and remove the
  copy afterwards.
- **A script that adds a comment to a labels.yml must not append the file
  to itself.** `maps/mapadrogi1890/labels.yml` held its 37 labels twice,
  the stale copy first, and the new header comment ran into the `map:`
  line, so the key went into the comment (pelzucki1901's header has the
  same missing line break, its key survived). PyYAML keeps the last of
  duplicate keys without a word, so nothing failed. After any script
  writes a labels.yml, load it and check `map` and the label count
  against the saved file (fixed 2026-11-14).
- **A place the editor marks as `new_place` that the register already
  has** (Świątniki, `reference/places.yml` `swiatniki`) gets a gazetteer
  entry with `register:` set to that slug: the place page already
  exists from the register, and the entry adds the text, the dated names,
  the OSM map and the map appearance to it. Write the text from the
  edition's documents (the place's `places_docs` list), and say where a
  document's writer or date is uncertain (letter 24 has no writer; letter
  212 only a year).
- **"Kolonia X" is not the Holendry of X (the editor, 2026-11-14).** The
  roads map's Колонія Вромбчинъ had gone onto Wrąbczynkowskie Holendry,
  the Olęder settlement of 1781; it is Kolonia Wrąbczyn, one of the
  Prince's colonies, a place of its own - today's Wrąbczyn Górski (the
  editor's word, which also merged the first, separate entry into that
  one: look for the place's modern entry before writing a new one). The same map also names the
  Holendry separately (Вромбчинковские Голендры), which should have
  given it away. After an import, read the label list for two labels on
  one place, and for a "Kolonia"/"Holendry"/"Olędry" form on an entry of
  another kind; put each to the editor before the map is called finished.
- **A value set in code must be redrawn where it is shown (2026-11-14).** The labelling page set a label's type from the gazetteer correctly but did not redraw the panel when the Place field was filled in at step 3, so the editor saw "unsure" for Trąbczyn and Nowa Wieś. When a handler changes state, check the visible text and highlighted button, not only the data; I first told the editor Osiny was fine from the data alone and had to look again.
- **Renaming a published map's slug (2026-11-14, Trójwiorstówki 1914 -> 1880).**
  Touches: the register key and `tiles`; `maps/<key>/` (and `map:` inside its
  georef.yml and labels.yml); the two page files in `site/_maps*/` (front matter
  `map:`, `permalink`, `alt_url`); every gazetteer `maps:` item (grep the old key);
  the thumbnail (`git mv`, then make_thumbs compares bytes); the label_index script's
  comments; and **the tiles repository**: `git mv` the folder, rewrite the key in its
  info.json, map.json and georef.json (the IIIF `id` carries it), then push it and
  wait for Pages before `make_thumbs.py`, which fetches the new URL. Leave a
  redirect page for each old address (`site/redirect-<old>.md`, layout `redirect`,
  as hohenlohe.md). Do not rename the J: folder of the original.
- **Do not name a map's maker or series from one catalogue line (2026-11-14).**
  The register called the Pyzdry-Konin sheet "the survey of F. F. Schubert, the
  1914 printing"; Mapster says ±1880, the sheet code (XVII D) belongs to the Russian
  three-verst series' scheme, not to the Kingdom of Poland map's (Kol./Sek.), and a
  Russian article calls "Schubert's map" a misnomer. I first wrote the wrong
  original into the map's notes. Check a sheet's code scheme against the series
  before naming the series, and say "not confirmed" in the notes until a source
  (Glushkov, *Zapiski VTD*, Kartografia Królestwa Polskiego) names it.
- **Tools for map research (2026-11-14).** RCIN's certificate was expired: the
  built-in browser and WebFetch refuse it; Claude in Chrome worked in the editor's
  Chromium once they had loaded the page. Mapster (igrek.amzp.pl) lists every
  series with its sheets and dates (maplist.php?cat=...) and a record page per sheet;
  its category list is the quickest way to see which series exist. Large sheets are
  read from the J: file with pyvips, cut by the georeference's pixel position.
- **Do not merge two places on a guess from one map** (2026-11-14): Kolonia Wrąbczyn was merged into Wrąbczyn Górski at the editor's yes, and the editor undid it hours later after reading Trójwiorstówki 1914, where the two lie in different places. A later map can overturn an identification made on an earlier one; keep two entries until a map shows the same spot, and say in the text what the place is not.
- **Check a secondary work's quotation against the work it quotes.**
  Seidel (2018) quotes Breyer (1938) with "Kolonweiler [Wrombczyn]" where
  Breyer prints "Kolonie *Wrombczyn*": a name that exists only in a
  misquotation. When a hidden work gives a new name, look for its source in
  the edition first.
- **The Prince's renamed colonies show both names on the maps** (the
  editor, 2026-11-14): `founded_as` in the gazetteer entry
  (GAZETTEER_PLAN, section 2); map_pages.py writes "Kolonia Adolfsberg
  (Zalesie)". Give a new entry for such a colony the field.
## A Jekyll include reads its parameters as include.<name> (2026-11-11)

The Sources page icons (`site/_includes/sources-icon.html`) rendered as empty
`<svg></svg>` on the live site, on light and dark alike: the include tested a
bare `kind`, which is empty inside a Jekyll include; the parameter passed as
`kind="book"` is `include.kind`. A first fix on 2026-11-07 diagnosed it as a
stroke-weight problem and changed nothing that mattered. **Check a "missing
icon" against the built HTML (`<svg>` with no `<path>`) before touching the
styling**, and in any include use `include.<name>` for every parameter.

## The 1882 consistory reports: sub-agents and burnt text (2026-11-11)

- **A sub-agent reading a figure can cut digits off it.** The Zagórów reader
  wrote "72 / 87 / 159" for 726 / 871 / 1597 and noted that the last stroke
  was "a comma". A second, independent reader (told to read before opening the
  first reading) found it; arithmetic alone could not (72+87=159 also adds up).
  Always have figures read twice, and check against the enlarged band yourself.
- **Two readers, in this order**: first reader writes; second reads the pages
  *before* opening the first reading, then compares. It caught 30 differences,
  among them "kirchliche" for "häusliche" and a sentence that read "die ersten"
  for "diensten".
- **A builder hook must not emit blank lines.** `body.append(supplied_html(...))`
  returned "" and added an empty line to all 631 letter pages. Guard with `if`.
- **A line-end hyphen before a burnt edge must not be joined**
  (`linebreak_decisions.csv`, `split`); paragraph breaks added by hand need
  cue `hand` or `resolve_paragraphs.py` drops them on the next run.
- **`pipeline/regenerate.py` stops at `check_pipeline.py`** (23 "names one
  holding" problems in old review scripts, present at HEAD): run the steps
  directly (resolve_linebreaks, resolve_paragraphs, build_db, match_scans
  for the unit; then merge_corpus, build_dataset, connections_site,
  build_site_data, person_pages, place_pages; jekyll; verify_site). After them,
  the repository shows drift in generated files of other holdings (place
  footnotes in `site/_places/`, the table English of apl399806603-6):
  committed sources moved since those were last built; review before
  committing them with this unit.
- **A summary of a burnt text leaves out any statement whose negation, figure
  or subject lies in a lost stretch** (the "vices" and "conversions" lines of
  Zagórów, where "nicht" is lost).
- **An agent can stall silently**: `ListAgents` showed one "running" after ten
  hours with no output; `TaskStop` it and start it again.
- **A "missing icon" is checked in the built HTML first**: the Sources icons
  were empty `<svg>`s because an include reads `include.kind`, not `kind`.

- **A re-import and a rerun of `resolve_linebreaks.py` re-derive the
  line-break decisions**, undoing a hand ruling (the burnt-edge `split`):
  re-apply it after every corpus change, then `build_db.py`.
- **A layer the editor rules off the site stays as data** behind a unit flag
  (`show_supplied`), not deleted: the plan and `supplied.yml` remain.
- **A burnt or damaged text's English is for reading** (the editor,
  2026-11-13): "[text lost]" after every broken word, and broken German words
  left half-translated, made the 1882 English hard to read. Translate a broken
  word whole where the legible part fixes its sense; put words taken from a
  twin text, the form or the grammar in square brackets; keep "[text lost]"
  only for what would add a fact (figure, name, place, date, negation). The
  transcription keeps every `[...]`. Clear the marker-check rows this raises
  in `reference/translation_rulings.json` with the reason, and replace the
  `l-auto-check` line in the unit's `prepared:`, which says every mark of
  doubt survives (units/agad14320139/intake/translation/build_docs.py).
- **Completing a transcription in brackets moves the line machinery**
  (2026-11-13). A supplied hyphen goes inside the bracket, "fo[lgen-]", and
  is a wrap only because `corpus_pages._wrap_mark`, `resolve_linebreaks` and
  `resolve_paragraphs` now accept a line ending "-]"; the resolver still
  scores such joins "split" (it does not know "lgenden"), so set them to
  `join` by hand - they are then held. The paragraph step drops the breaks a
  short burnt line used to cause, and adds wrong ones once the lines are full:
  read the reading text of every page after the rebuild. The translation's
  marker-check rulings are keyed by the German's count, so they must be
  re-keyed after the text changes, and `write_cache.py` run again so the
  cache carries the new German's hash.
- **A reader's page does not describe the physical state of a source**
  (the editor, 2026-11-13, of the burnt 1882 reports: "there's no need to
  describe the physical condition of the texts"). Titles, descriptions,
  introductions, summaries, timeline notes and era essays say what the
  documents say; burns, stains and torn edges go in the holding's `notes.md`.
  Given for that holding; the same restraint suits any new one.
- **Python's `textwrap` breaks at hyphens, and a folded YAML scalar (`>-`)
  then reads "Olędry- Kolonisten"** (2026-11-13, the homepage text in
  `site/_data/i18n.yml`): a line break inside a `>-` block becomes a space.
  Wrap prose for YAML with `textwrap.wrap(text, 76, break_on_hyphens=False)`,
  and load the file back to compare the values before committing.
- **The homepage** (`site/_includes/home.html`, text in `site/_data/i18n.yml`,
  keys `home_lede`, `home_h2`, `home_p1`-`home_p4`) introduces the whole
  edition to a first-time reader (the editor, 2026-11-13: it "still only
  talk[ed] about the prince"). When a new era or section is added, check that
  the homepage's short history still covers it.
- **Write for a reader who meets the page in pieces** (the editor,
  2026-11-14): no bare "this", "that", "these", "they" pointing back to an
  earlier sentence, and every paragraph that follows a heading, figures or
  buttons names its subject again. The rule and its examples are in
  HOUSE_STYLE, "Name the subject; do not point back". Read every new
  paragraph once as if the one before it were not there.
- **A holding's description opens with the story, not the header**
  (the editor, 2026-11-14). All 54 opening paragraphs were rewritten that day
  (English and German): no counts, archive, volume or languages, which the
  page's header already shows; what the documents are and why they matter.
  HOUSE_STYLE, "A holding's own page". A new holding's `about.md` starts the
  same way.
- **Trąbczyn's owners before 1698 were the Trąmpczyński family**, not the
  Prusimskis: the court records of 1589 and 1644 name Trąmpczyńskis, and
  `reference/genealogy.yml` has their sale of Trąbczyn to Jan na Kolno
  Prusimski in 1698. The homepage and the boundary era's ownership line said
  "Prusimski from 1589" until 2026-11-14; check the genealogy before writing
  an ownership line.
- **No "the edition", "the project", "the site" or "the collection" on a
  reader's page** (the editor, 2026-11-14; HOUSE_STYLE, "The pages do not
  talk about themselves"). A sweep that day fixed the homepage, the era pages,
  holding descriptions, the literature's Related notes, a timeline note, two
  works' accounts and a newspaper summary. To find new ones, parse the YAML
  and search only displayed values (a grep also hits comments and the
  `translation_note` prompts, which no reader sees).
- **`english_forms.py --apply` also rewrites the English summaries, and
  damages them** (2026-11-14). Run to apply one page correction from
  `reference/english_corrections.yml`, it changed 34 summaries in
  `site/_data/summaries.yml`: years given digit groups ("1,173", "1,399" in
  the kdw and app5314550221 summaries, "(2,026-11-01)"), écus turned into
  Reichsthaler, the open "gl." made "Groschen". The summaries file was
  restored with `git checkout`. After running it, keep only the translation
  file it was run for and check `git diff site/_data/summaries.yml` before
  committing.
- **Look a place up before giving it a descriptor** (the editor, 2026-11-14:
  "towns" for Konin and Kalisz, both cities). HOUSE_STYLE, "Check what a place
  is before you call it something"; run
  `pipeline/review/check_place_descriptors.py` before publishing. Its first run
  listed 40 descriptors to read; the register itself needs the editor's word
  where it disagrees with the present day (Konin was `town`).
  **Corrected the same night** (editor: "correct any other issues relating to
  place names"): `kind:` in `reference/places.yml` is what the place is today
  (city: about 50,000 inhabitants or more, or a regional or national
  capital); 13 towns became cities (Konin, Opole, Legnica, Częstochowa,
  Głogów, Zielona Góra, Mysłowice, Włocławek, Jena, Weimar, Bayreuth, Fürth,
  Memel); Ostrów and Neusatz stay open (which place?). **The Places index
  printed "— city" in lowercase, in English even on the German page, because
  `_KIND_EN`/`_KIND_DE` in build_site_data.py had no `city`, `country` or
  `region`**; added. A new kind needs a label in both maps, or the raw word
  shows.
- **Do not make the act of writing the news** ("people wrote down who owned
  ..."): say what the documents show. HOUSE_STYLE, "State the facts, not the
  fact that they were written down".

## The Trąmpczyński family pages (2026-11-12)

- **The boundary decree of 1775 (APP 53/17/0/-/Konin Gr.145) is the
  family's deed chest.** Its Polish recites the Trąmpczyński partitions,
  decrees and sales from 1522 to 1698 with the kinship words that decide
  a tree: "stryj" (father's brother) and "synowcy" (brother's sons),
  "bracia między sobą rodzeni" (full brothers), "pozostała małżonka"
  (widow). Search its corpus for "Trąpczy" (the decree's spelling, without
  the m), not "Trąmpczy". The Poznań decree of 1784 (APP 53/20/0/-/Poznań
  Gr.1181) does the same for the Prusimskis of Kolno and the Golińska
  inheritance.
- **A regest is cited as a literature work** (`literature/tekidworzaczka`),
  one regest per passage cut at an edition-made heading ("# Nr. 1420
  (1642)"), so a person page can cite it like any passage; a further
  regest goes at the end (c05...) so the keys already cited stay put.
  `reference/sources/` is for the glossary's sources; person pages
  resolve only "work/passage", a document uid, or "editor".
- **In the Teki Dworzaczka, "s. o." is not "the late"**: the same regests
  write "ol." for that. Infer no death from "s. o.".
- **A regest's "ż." dates a settlement, not a wedding**: "Anna Bojanowska
  ... ż. Władysława" in 1663 means she was already his wife.
- **Check a tree's generations against the dates before anything else**:
  the editor's draft had a man marrying in 1692 as the grandson of a man
  married by 1663 - the same Jan entered twice.
- **A standalone person page is linked from nowhere by itself.** The
  People page links an entry's page, not a standalone one; give the
  family entry a block with `members:` so its page lists them.
- **verify_site.py's life-line check** compares a block's `life` with the
  entry on /people/; a standalone block has none, so it is skipped.
- **The dataset can lag its source**: `build_literature.py` rewrote
  `dataset/literature/nmpol/` because `literature/nmpol` had been changed
  (2026-11-06) without a rebuild. Rebuild after any change to a work's
  original.md or english.md.

## The owners' family tree (2026-11-12, afternoon)

- **Minakowska's database through the editor's sign-in.** The editor signs
  in in the browser pane; a page script fetches `/b/<ID>` with the
  session and POSTs the bytes to a local receiver on 127.0.0.1 that writes
  `review/minakowska/raw/<ID>.html` (gitignored - each page carries the
  login). Pages are ISO-8859-2; a converter makes `review/minakowska/text/`
  with every linked person's `{ID}`. This keeps the pages off the chat and
  out of the repository. The kinship search is
  `/s/i.php?kolig=<the page's hidden kolig>&koligtroi=<ID>&qt=<other ID>&et=S`.
- **The database's Uwagi quote Teki Dworzaczka regests**: bring each one a
  fact rests on into `literature/tekidworzaczka` (appended, c05...), so the
  tree cites the regest, not the database.
- **"s. o." again**: a sub-agent read it as "son of the late" twice (a
  death "before 1706" for a man the regest does not call dead). Check every
  death bound drawn from a regest against "ol.".
- **A newspaper's issue date is not the event's date**: the edition carried
  Włodzimierz Miączyński's death as 20 December 1879, the date of the paper
  that printed "died on the 18th".
- **The database's "1707/"** (a trailing slash) marks a date the person was
  alive, not a death; the editor's chart had read it as a death.
- **Inserting before a YAML key by replacing "
families:
"** drops the
  newline unless the replacement starts with one: twice a new person landed
  on the previous line. Write such edits as scripts that find the block
  bounds.
- **A colon inside an unquoted YAML value** breaks the file (`page: notice
  printed 20 December 1879: "..."`): quote values that may hold colons.
- **The explorer's layout battery** (`node check_tree_layout.mjs <tree>`)
  covers remarriages since 2026-11-12; run it on both trees after any
  change to `src/lib/tree.js`.

- **A source the editor reports but the edition does not hold** (a sign, a
  conversation) goes into `reference/sources/` with the editor's own words,
  what the edition's sources say against it, and what is still to find; the
  tree cites it as a source of kind `report`, and MISSING_SOURCES lists the
  primary source still wanted (the repurchase of 1896, 2026-11-13).

- **Brief a sub-agent with the plan's own rule, not a stricter paraphrase**:
  the estate tree plan admitted a database year "without '?', 'ok.' ..."; the
  drafting brief said "day + month + year, or month + year", and the agent
  dropped years the database states plainly (Michalina's 1778). The editor
  asked "why not?" (2026-11-13). Copy the rule's words into the brief.
- **Geneteka** (geneteka.genealodzy.pl, public) indexes the parish and civil
  registers: `index.php?op=gt&lang=pol&bdm=S|B|D&w=71wa&rid=S|B|D&search_lastname=...&from_date=...&to_date=...`
  (71wa = Warsaw; 07mz = Mazowieckie). The row's tooltips carry the index's
  notes (the exact date, "karta nr 67, 1810.08.17") and the Szukaj w
  Archiwach unit of the scans; read them with a page script. It settled
  the marriage of 1810 that two printed works put in 1809. Cite the
  register and act, with the index named; the scans were not read.

## The index of APŁ 39/98/0/-/1333: two readers and the clerk's numbers (2026-11-13)

The editor asked for the 14-page Russian index (опись) of APŁ 39/98/0/-/1333
(liquidation tables of Trąbczyn, 1864-1870) as a spreadsheet, a rough pass
first and a fine pass at their word. The files are in
`review/apl399801333/` (not in the repository): `index_rough.xlsx`,
`index_fine.xlsx`, the readings, and the scripts that rebuild them.

- **What worked for the fine pass.** Each page cut into eleven overlapping
  strips of the text columns at near-full size, and the figure columns in
  three pieces enlarged 1.5x. Eight Sonnet sub-agents, two independent
  readers per page **run at the same time**, each forbidden to open the
  other's folder or the rough pass: independence without waiting for one to
  finish. A script compares them after normalising spelling trivia (ъ, ѣ/е,
  "65г"/"65 г"); Claude settles each difference on a montage of the strips
  (three strips stacked per image cuts the number of image reads to a
  third). 146 entries: 70 agreed, 59 settled, 17 left open on a "To check"
  sheet with a picture of each entry.
- **Two readers can agree on a wrong word.** Both read the minutes entries
  of nos. 6-36 as "Выписка" and of 74-84 as "Протокъ"; set side by side, the
  word is the same in all of them, its opening the "Пр" of "Прошеніе"
  below: "Проектъ журнала засѣданія". Compare a recurring word across the
  whole document, not entry by entry.
- **The clerk's own numbering settles months the letters cannot.** Іюня and
  Іюля (June/July) are indistinguishable in both hands. An office's papers
  are numbered in sequence, so a number fixes the order: the Central
  Commission's no. 3600 of 23 June 1869 makes no. 4386 "24 July", not June;
  the Turek commission's 801 before 806 makes one June and the other July.
  The same check found that "Владимірова" is the 10th-district commissar
  Vladimirov (his no. 60 follows that district's no. 59). Look for an
  office's number series before asking the editor about a month.
- **Sense words the readers garble are often formulas**: "съ надписями"
  (with endorsements), "его-же"/"ея-же" (of the same man/woman), "ликв.
  таб." (liquidation table). Try the formula before calling a word unread.
- **The xlsx skill's `recalc.py` does not run on this Windows machine**
  (LibreOffice needs `socket.AF_UNIX`): a formula column (here the folio
  check) is written and computes when Excel opens the file; check the same
  logic in Python.

### The letters and the holding (2026-11-13, evening)

- **Checking an editor's transcription without re-reading it.** The editor's
  word was: correct only a glaring error, from context first. List the
  suspect words with their context, and give the list to a Sonnet reader
  *without the suspected correction*, asking only what the page has at each
  spot; then look yourself at every medium or low answer. Of 29 suspects, 27
  were real misreadings (zmierciłem/zmieniłem, dałem/dał im — the latter
  reverses who paid the false witnesses) and a whole line was missing.
- **A Sonnet claim checker finds what the writer of a summary cannot see.**
  It cut "with carts two days a week" (the verb is a doubtful reading), a
  "widows" no entry names, and a date range the index does not hold: 9 of
  87 statements. Apply its cuts to the English, the holding page and the
  timeline too, where the same sentence was repeated.
- **`holding.py --cache` (courtbook.save_cache) reads the merged
  `dataset/letters.json`**: for a new holding, run `merge_corpus.py` first,
  or it writes nothing and says nothing.
- **Running `regenerate.py` past its self-check**: a few lines that import
  `regenerate`, replace `run()` for `pipeline/check_pipeline.py` only and
  call `main()` with `--unit <slug> --site` run every other step in order
  (the self-check's 25 problems are old and not the holding's).
- **A catchword above an office note is not found**: the line-break pass
  looks at the page's last line. Put the office's notes before the
  catchword (the notes are set apart anyway), and list a two-word catchword
  ("z usilną") in `catchwords.yml`.
- **`csv.DictWriter(open(path, 'w'))` truncates the file before it fails**:
  a row with an extra field emptied `index.csv`. Write to a list first and
  open the file only to write it; keep the script that made the file
  (`intake/make_index_csv.py`) so it can be made again.
- **A new document kind needs its label** in `site/_data/i18n.yml`, both
  languages (`petition`, `plan`), or the page says "Document".
- **A shared surname pattern tags the wrong man.** "W. Miączyński" in 1865
  matched `miaczynski` (Stanisław, Michalina's husband); check `people:` in the
  holding's `site/_letters/*.html` after the first build, and fix with
  `only_in`/`not_in` limited to the holding.
- **A place form to be matched in a few documents only**: places had only
  `not_in`, people `only_in`. A place in reference/places.yml can now carry
  `match_in:` (a list of `{match, only_in}`), read by
  `entities.place_authority`; the bare "Łazińsk" of the colonists' petitions
  is matched that way, and stays unmatched elsewhere (Breyer's Łazinsk of
  1936 waits on the editor). Use it rather than widening `match`.
- **A spot-sheet answer under "Something else" is the editor's own reading**
  and may be none of the options ("czynu" for "[czynionem?]" / "czynnem"):
  take it as written, and change the English to follow. An "unsure" answer
  leaves the doubt mark as it stands; say so in NEEDS_CONFIRMATION.
- **Russian place names** are matched in the place's own `match` (Тромбчин\w*,
  Лаз[иіе]нск\w*, ...), parallel to the Polish pattern: where the Polish
  matches only the noun (Słupca) the Russian adjectives of the district were
  taken in all the same (Слупецк\w*), the editor having asked for the
  index's names matched (2026-11-13).
- **Generated data left behind by an earlier commit.** The Teki Dworzaczka's
  `work.yml` (e72f2e6ab) and the maps register (bd48f76e3) were committed
  without the files the build makes from them (`dataset/literature/index.json`,
  `site/_data/literature.yml`, `site/_data/maps.yml`, `maps_list.yml`), so the
  next session's rebuild showed them as changes it had not made. Commit the
  regenerated files with the source edit. A session that finds such
  changes says what they are and where they come from, keeps them out of its
  own commit, and commits them separately at the editor's word (done
  2026-11-13, 2025e0ff0).

## I. HA GR, Rep. 7 C, Nr. 3067: checking the editor's transcription with four readers (2026-11-19)

- **Four Sonnet readers, two per part, started at the same time**, worked
  well for a short file (six pages). Each got the page in overlapping strips
  at full resolution (about 650 px high, 130 px overlap; 520 px for the
  table), the editor's text with line numbers, and a list of suspect spots
  *without* the suspected answer; one reader of each pair read the hardest
  part (the King's hand, the list's names and dates) from the image before
  opening the transcription. They found the spacing slips the editor's
  recognition model makes ("Weiler" for "Weil er", "Ausgleicher",
  "zufürtzerer"), a wrong line start ("geldet" for "ge-/meldet"), case
  endings ("des Insurrektion"), and struck-out words; they disagreed on the
  King's words, which Claude settled on enlarged crops and sent the rest to
  the spot sheet. Every correction was taken only with a witness or a plain
  page (NEW_UNIT 3a), and recorded with it in `intake/build_pages.py`.
- **A reader can say it wrote its report and not have written it**: reader 1
  ended "Report written to .../report.md" and the folder held only its
  crops. Its hand-back message carried the main findings; check the file
  exists before relying on it.
- **Readers report the filler dots and dashes of a table, the braces and
  underlining**: not text, not transcribed; say so once in the notes.
- **A claim checker flags what rests on the edition's own identification**
  ("the Grand Chancellor Goldbeck" where the paper signs "Goldbeck"). Keep
  such a statement when a person entry or the archive's title settles it,
  and write the reason into the claim-check record's header.
- **A Python script written through a bash heredoc can turn "\n" inside
  its strings into real newlines** (the CORRECTIONS list broke twice). Write
  a script with string escapes through the Write tool, not a heredoc.
- **`pattern_impact.py` dies on a Polish letter in this shell's cp1252
  console**: run it with `PYTHONIOENCODING=utf-8`.
- **Ask before splitting a file's papers into documents** (2026-11-19, the
  editor: "Do not split this into three documents - it is a single
  document"). The promemoria, the King's decision beneath it and the list
  it encloses were built as three, by NEW_UNIT's rule for a reply written on
  the page it answers; the editor ruled them one. Where a unit holds a paper
  with a decision or an enclosure, ask how many documents it is before the
  boundaries are cut: unmaking a split touches the rulings, the English,
  the summaries, the index, the timeline, the scan labels and the
  paragraph rulings keyed to the old numbers.
- **A document can be a table on some pages only**: `documents: tables`
  with `table_pages: {"1": [5, 6]}` in rulings.yml (unitlib.load_tables;
  the page build, both checks and publish_translations follow it). After
  merging documents, delete the old `dataset/documents/` and `dataset/text/`
  files of the numbers that are gone (the build does not), and the cache
  and `site/_data/translations/` files of them (publish_translations works
  from the cache files).
- **A table's title page is text, and look at every page of a table in the
  browser** (2026-11-19). The list's title page (I. HA GR, Rep. 7 C, Nr.
  3067, page 4) was first built as the table's first rows: `render_table`
  drew it as a caption over column heads taken from the next page, the
  title's line ends gone. The editor saw it on the local site ("weird
  styling ... table headings that don't belong there"). The checks passed
  it: they compare words, not what a page looks like. A page with no rows
  of the table stays text (leave it out of `table_pages`); then set its
  reading by hand where a heading word ("Liste") would run on into the
  next line.
- **A brace on the page is a merged cell** (2026-11-19, the editor: the
  "Nature of the crime" cells of Wittwicki and Retznowski "need to be merged
  into one", and Czimay's and Ruba's, with their "Its beginning"). The
  spreadsheet gave the joined text in the first row and left the second
  empty, and I built it so, as two cells. `table_merged_cells` in rulings.yml
  now draws one cell over both rows (NEW_UNIT). When a table comes in, look
  at the scan for braces and set them before showing it. Headless Edge with
  a `#page` anchor in the address gives a blank screenshot; read the built
  HTML instead.
- **The editor overruled a correction made on two readers' word**
  (2026-11-19, the spot sheet): the King's "Nach genauer Betrachtung" had
  been changed to "Untersuchung[?]" on reader 1 and Claude (reader 2 had a
  third word, "Erwegung"). The editor's reading stood. In a hard hand,
  where the readers do not agree among themselves and the editor's word is
  not plainly impossible, leave the editor's word in the text and put the
  alternatives on the spot sheet; do not change it first.
- **A spot sheet as one HTML file, no server**
  (`units/ihagrrep7cnr3067/intake/spot_sheet_html.py`, the editor asked for
  "a html spot sheet"): the crops embedded as data URIs (a close crop and a
  taller view of the lines around it), answers in localStorage, a "Copy
  answers" button giving JSON in the shape of `query_answers.json` for the
  editor to paste into the chat. Look at every crop before handing it over
  (one here cut off the first letter of its word).
- **After a change to a page file, the order of the rebuild matters**:
  `import_pages.py --boundaries` needs the CSV's path
  (`review/<slug>/document_boundaries.csv`), and `write_cache.py` takes the
  German from the dataset, not from `corpus.txt`, so `regenerate.py` must
  run before the English is re-cached. Otherwise `check_translations.py`
  counts the old marks of doubt and reports a missing one.
- **A name's `variants` entry is also a translation rule**: a form listed
  under `variants:` in people.yml makes check_translations demand the
  entry's whole `render` ("Antoni Prusimski") wherever the form occurs.
  For a variant that stands in a list of bare surnames ("Prudzinski"), put
  it in the `match` alone and let reference/english_forms.yml carry the
  English form.
- **A connections sweep by a Sonnet reader works**: hand it the candidate
  uids (found by grep for the shared names and terms), the rule "a shared
  name alone is not a connection", and ask for exact quotes; then check the
  quotes the connections will rest on against both texts before writing
  them. Reading the strongest candidate whole oneself still pays: the
  reader cited the deed's signature "Hoym. Goldbeck." but missed that
  3570-1 has Goldbeck laying all seven deeds of gift before the King.
- **Look for the editor's own table before keeping a list as lines**
  (2026-11-19): the list of the condemned was kept line by line because the
  table code could not set words in its columns, while the editor had a
  spreadsheet of it in Downloads (`I_HA_Rep_7_C_Nr_3067_tables.xlsx`, not in
  the holding's folder). When a document is a table, search the editor's
  folders for a `*table*` file and ask before settling for lines.
- **Filling a table's cells from a corrected transcription**: place each
  cell's words on the page's uncorrected words (first unused occurrence,
  every word used exactly once), then carry the corrections across with
  `difflib` opcodes into the cell that holds the word
  (`units/ihagrrep7cnr3067/intake/build_pages.py`, `to_table`). The
  spreadsheet and the text file were checked against each other word for
  word in the same pass.
- **verify_table_of_diff.py covers table_of and render_table, not the page
  around them**: a change to the page rule's "entries 32-48" label in
  build_site_data.py altered three other holdings' pages and passed it; only
  `git status site/_letters` after the rebuild showed it. After any change
  to the shared table code, read that list: only the holding being worked on
  may appear. (The script also skips Pyzdry Gr.115 since the numberless
  extension, which HEAD now has; a copy without the skip ran clean.)

## I. HA GR, Rep. 7 C, Nr. 3132: a slip out of order, and the heredoc trap again (2026-11-20)

- **A document's pages can stand out of the file's order.** The editor
  ruled the office's slip (fol. 9, bound between 8v and 10r) part of
  document 4 (Goldbeck's letter of 11 May, whose registry number it
  carries). `import_pages.py` assembles the corpus in the order of the page
  files, so the holding's script writes `corpus.txt` itself (DOCS: each
  document's pages and line ranges, every line checked to be in exactly
  one document), and `units/<slug>/scan_decisions.json` gives match_scans
  the reading order (`image_order`, the staged file names); without it
  match_scans stops with "mapping does not follow the intended image
  sequence".
- **Openings photographed whole go through courtbook's fold page** for any
  holding: a `holding.py` with SCANS (file, fold x, left id, right id),
  SKIP for blank sides, EDGES for the first page edges, and
  `courtbook.placed/cut/fold_sheet`; `courtbook.find_fold` proposes the
  folds. units/ihagrrep7cnr3132/intake/holding.py is a compact model.
- **Four readers on fifteen pages**: one each for the clean chancery hands
  and the clerk's copy, two independent readers on the drafts and the slip.
  The clean-hand readers found real slips the editor's model makes ("Straßen"
  for "Starosten", "Verbauung", "urtheilt", "Aldels"); on the drafts the two
  readers disagreed often and one was plainly wrong once ("Entwurf" where
  the page has "Bericht"), so a draft reading changes only where two agree
  or the image settles it on a crop. The editor's "und" in "Huldigungs und
  ableisten" was "eid" (Kurrent e-i-d with the i dotted looks like u-n-d):
  look for the dot.
- **A pattern widened for one spelling reached the literature**: adding the
  one-f "Bischofswerder" to the person's match (and to `variants`, which
  the literature index also matches) put 40 unruled hits into
  `literature_index.py`, which stops the build. Count a widened pattern
  against the literature too (mistake 7 of NEW_UNIT), or tie it to the
  document's words (`Bischofswerder(?= geschenkt)`), and keep the form out
  of `variants`.
- **The heredoc trap bites with `python - <<'EOF'` as well**: a "\n" inside a
  Python string in a quoted bash heredoc still came out as a real newline
  in the file written (three times this session). Edit scripts with string
  escapes through the Write or Edit tool, or use chr(10).
- **A catchword above an office note** again (0005_a2): the note moved
  before the catchword in SPEC, as WORKING_NOTES says.
- **The heredoc trap a fourth time**, the other way round: a search string
  holding a literal backslash-n (to match the `\n` written in holding.py's
  CORRECTIONS) found nothing when sent through `python - <<'EOF'`. Any
  script with a backslash in it goes into a file in the scratchpad through
  the Write tool and is run from there; build a backslash with chr(92).
- **A `--site` rebuild after the holding's paragraphs.py resets the cues**:
  regenerate keeps the held run/break decisions of paragraph_decisions.csv
  but writes its own cue over "hand". The site does not change, but the
  file in the repository does: run `intake/paragraphs.py` once more after
  the last rebuild, before committing.
- **Blank sides out of the set**: the editor does not want the blank halves
  of the openings kept at all, not even in `processed/_not_staged/`.
  `courtbook.cut(raw, scans, skip, keep_skipped=False)` leaves them unwritten
  and removes old copies; the default still keeps them, for the holdings
  built before.
- **Joining documents after the build** (7 + 8, 9 + 10, the editor's word):
  change DOCS, then everything keyed by document number - rulings.yml
  (places, dates, types, relations), paragraphs.py, the English dict,
  write_summaries.py, `only_in`/`issued_in` in people.yml, the `[[n]]`
  citations of about.md and about_de.md - delete the old doc<N>.yml and
  cache files, `git rm` the tracked outputs of the numbers that are gone
  (dataset/documents, dataset/text, site/_data/translations, site/_letters,
  site/redirects), and run `relabel_scans.py --apply`. **Then build twice**:
  the database step reads page_scan_map.csv before the scan-mapping step
  rewrites it with the new labels, so the first build links the old scan
  names and verify_site fails on them; the second passes.
- **A join of two pieces leaves the second one's opening without a
  paragraph break** where the resolver proposes none (the reply's "An" after
  the first draft's dateline). A hand row (cue `hand`) is carried over by
  the line's words; where the words stand twice in the document,
  resolve_paragraphs.py now tells them apart by `prev_line` (2026-11-20).
  `intake/paragraphs.py` of Nr. 3132 writes such rows (NEW).
- **A spot-sheet decision the editor cannot read is explained in chat,
  not decided**: d2 (a connection "Keep|Drop") came back "I need more
  explanation". Write a decision card so it says what the connection does on
  the site (a box on each document's page linking the others, with the
  sentence shown) and what dropping it loses, not only what the documents
  say.

## I. HA GR, Rep. 7 C, Nr. 421: crops, a catchword under a margin, the instances (2026-11-21)

- **The editor's own crops of a scan need four-digit page ids.** The editor
  sent 0014a and 0014b (the two sides of opening 0014, cropped by them) with
  transcriptions named after them. match_scans and relabel_scans take a
  capture of four digits (`_(\d{4})_([a-h])`), so a page `0014a_a` would
  break the pairing: name the crops `0014_a1` and `0014_a2`, leave out the
  uncut 0014, and say in the holding script which source file each page
  reads (`SOURCE_OF` in units/ihagrrep7cnr421/intake/holding.py).
- **A margin block beside a column that ends in a broken word and a
  catchword goes first on the page.** On 0002_a2 the column ends "von Kö¬"
  with the catchword "nigl:" at its foot; the notes in the margin, put
  before the catchword as WORKING_NOTES says for an office note, split the
  word in the reading text ("Kö¬ || Es [sind?]"). Put the block before the
  column's first line instead: the line-break pass then joins "Kö¬" to the
  catchword and drops the catchword as usual. The block is set apart on the
  site wherever it stands.
- **Read every "split" the line-break resolver proposes.** It splits a
  "¬"-broken word whose joined form neither the corpus nor DWDS knows: here
  19 of 21 were one word (Ur¬tel, Perso¬nalklagen, Re¬visions, Mier¬zewo,
  the Polish wy¬rażone). Keep the joins in a holding script that writes
  `held` rows (units/ihagrrep7cnr421/intake/linebreaks.py); resolve_linebreaks
  carries held rows over.
- **Run make_scan_derivatives.py after relabel_scans.py --apply.** The
  relabelling prunes the old web copies and says so; the regenerate wrapper
  does not make new ones, and verify_site.py then fails on broken scan links
  for every page of the holding.
- **"Second instance" is not "revision".** In Prussian procedure of the 1790s
  the appeal was the second instance and the revision the third: when one
  document says a suit was lost "in der 2ten Instanz" and another speaks of
  the "Revisions Erkenntniß", do not equate them in a connection note.
- **A copy's date can be checked against its own chronology.** The suit
  copied in document 6 is dated 1799, but its "27. Februar c." and "Johanni
  v. J." fit 1796; put the digit on the spot sheet, keep the date the page
  bears, and write the doubt into the holding page without a year the
  documents do not state (check_unit_text fails on one).
- **An existing person entry may already hold a new holding's man.** Mondro,
  the Prince's attorney in Nr. 3705 (1805), is Chełmski's lawyer in Nr. 421
  (1799); the index found him only because the entry's one form matched two
  of the editor's readings. Look through people.yml for the names of a new
  holding before proposing entries.
- **A name the editor reads several ways is settled from the man's own
  signature, then corrected everywhere at once.** The editor wrote "Mondio" in
  five places and "Mondro" in two; his signature reads Mondro plainly, the
  Kurrent n written like u ("Moudro" to the eye). Do not leave such a name on
  the spot sheet when the scans settle it: correct every place in CORRECTIONS
  and grep the hand-written files for both forms *and* for the editor's
  bracketed form (here "Mond[io?]", which a plain search for "Mondio" misses
  and which stood on in the English).
- **A person entry carved out of a family entry.** For Stanisław Chełmski
  (2026-11-21) the family entry stays whole and the person entry is added
  beside it: `match` takes the surname after his forename forms (one fixed-
  width lookbehind per forename and middle word: Python's re takes no
  variable-width lookbehind) or before his title; `issuer_match` with
  `issued_in` takes the bare surname only in the documents that already name
  him so, computed once and written out; lookbehinds shut out his forebears'
  forenames. Three more files want the entry: `reference/people_bios.yml`
  (verify_site fails a person page with no bio), `reference/genealogy.yml`
  (no block, no page) and `literature/index.yml` (every literature hit of a
  new entry must be ruled, or literature_index.py stops the build).
- **The editor's own spot-sheet options carry no line-end mark.** "die Rük /
  zalung" was written so on the sheet; the scan has the copyist's line-end
  mark, so the correction writes "Rük¬", as the editor's own answers ("nehm¬
  / lich", "ab¬ / hören") do. Write "¬" into the options next time.
- **Sub-agents as readers, again**: two of four left strips unopened and said
  so; read those strips yourself before settling. A brief that names the
  file's internal witnesses (two copies of one petition, a decision and its
  clean draft) lets the readers settle many readings on their own.


## Nr. 421 read again, the English repaired, registry numbers (2026-11-22)

- **The in-session translator's rule "words still unread are kept as
  written" produced English such as "Es [sind?] [wir?] Acta [t?]orm[?] has
  the two in this Storstell[s?] ..."**; the editor called it "a horrible
  attempt at an English translation". Withdrawn (EDITORIAL_RULES, "An
  unread word in the English"): read the passage again first; then the
  sense with "[?]", or "[...]". A page of German fragments in the English
  means the reading was never finished, not that the translation is
  faithful. check_translations now counts "[...]" as a mark of doubt, and a
  holding's english.py should count marks with the same pattern (Nr. 421's
  `MARK`).
- **Two readers on the doubtful lines, one blind, worked as the new rule
  says**: they agreed on 16 of 46 lines outright, and both read the same
  signature ("Willenz") in two places. The blind reader also caught what
  the led one and Claude had passed over: the bond's "Zaro?" ends in a
  letter shaped like the long s, not b; the witness of 1830 decides the
  place, the letter stays "[b?]". **Check that the rows file holds every
  line asked about**: the endorsement's line (the "Mazący" word) was left
  out of `rows.tsv` by an off-by-one, and the blind reader had to be sent
  back for it.
- **A place's `match` must also match the line-by-line text.** The place
  pages (build_site_data's "named here") search `r['text']`, where a word
  broken at the line end stands as "Zaro[b?]¬\nney"; the dataset's tagger
  reads the reading text, where it is joined. A pattern for a broken word
  needs `¬?\s*` at the break, or the page lists one document fewer than
  the dataset tags.
- **A margin block in `office_notes.yml` is found by its first line**: a
  correction to that line must change `first:` too, or build_db stops.
- **The registry-number rule was narrowed twice on the diff**: first it
  also took "Seehausen. 5000" and "... 7720" (a figure after a word or an
  ellipsis), then a column's total ("= 800 rt" / "3631."). Measure such a
  rule on the text as the pipeline groups it (a reading-text paragraph, an
  English page), not line by line: the first diff script fed lines, so the
  total looked changed when the paragraph keeps it grouped.
- **publish_translations refuses a holding whose review sheet is older than
  its cache**: run check_translations for it first. Nr. 12765 publishes
  only with `--tag v2`. Nr. 3709's English is not published from the cache
  (0 letters): fix it through `reference/english_corrections.yml`.
- **`english_forms.py --apply` rewrites `site/_data/summaries.yml`**
  (re-wrapped, 46 entries "changed"): restore it from HEAD and let the
  build write it.
- **The heredoc trap a third time**: a Python string with `\n` inside a
  replacement written through Bash put a real line break into
  numerals.py. Use the Edit tool for code.
- **The Słownik's converted text is searchable locally**: the sparse clone
  of `sources/sg` (WORKING_NOTES, "The candidate places") answered for
  Zarobna in seconds, where the web reader was turned away by the ICM
  site's bot check.

### The same evening: abbreviations, voices, the sweep (2026-11-22)

- **Expanding abbreviations moves the paragraph machinery.** resolve_paragraphs
  carries held decisions over by the line's text, and a holding's
  `paragraphs.py` rules match by the line's start: after the expansions four
  held decisions were lost and five rules found nothing (two lines no longer
  short enough to be candidates). Run the holding's paragraph script after
  any text change, restate lost decisions as rules, and drop the rules whose
  candidate has gone. A break no cue proposes is a row with cue `hand`
  appended to paragraph_decisions.csv (letter, decision, the line's first
  words in `context`).
- **A per-line table is safer than CORRECTIONS for many small changes to the
  same words**: CORRECTIONS needs each find to be unique on its page, which
  "d." and "v." never are. Nr. 421's `intake/abbreviations.tsv` is applied by
  page, line and occurrence, the form matched as a word, and the build stops
  on a miss.
- **A Sonnet reader drops trailing punctuation when told to insert, not
  replace**: a dozen of its expansions lost the page's full stop ("v." to
  "v[on]"). Check the shape of every proposed rewrite mechanically before
  applying it.
- **A sweep reader does not know the edition's deliberate terms**: it
  proposed to translate Actum, ex officio, Pro Memoria and in solidum, which
  have glossary entries and stay in the English. Grep `reference/glossary.yml`
  (match_en) and `translation_glossary.yml` for a term before changing it
  across the edition.
- **The house forms run before the one-page corrections**: a correction's
  `find` must be the text as the forms leave it (the registry number "3681"
  mid-line is regrouped "3,681" before the correction sees it).
- **`english_forms.py --apply` reports a correction "not applied" where an
  earlier publish already applied it and a later correction changed the
  words**: harmless when a fresh publish would apply both in order; read the
  row before acting on it.
- **The set-apart kinds** live in `pipeline/build/corpus_pages.py`
  (SET_APART), `build_site_data.py` (SET_APART_OPEN and the two view loops),
  `build_db.py`, `build_dataset.py`, `translate.py` (the marks and the notes
  to the model), `site/assets/letter.js` (the English labels) and
  `site/_data/i18n.yml`: a new kind touches all seven.

### The layout editor and its tests (2026-11-22, late)

- **A page script can be tested in headless Edge without installing
  anything**: Edge is on the machine (`C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe`),
  Node 24 has `fetch` and `WebSocket` built in. Start Edge with
  `--headless=new --remote-debugging-port=9333 --user-data-dir=<scratch>`,
  open the page with `PUT http://127.0.0.1:9333/json/new?<url>`, and drive it
  with `Runtime.evaluate` over the target's WebSocket: set a selection with a
  Range, dispatch `InputEvent('beforeinput', {inputType, cancelable: true})`
  and `KeyboardEvent('keydown')`, read the DOM back. Serve the built site
  with `python -m http.server` in `site/_site` (the baseurl is empty). The
  Claude in Chrome extension was not connected this session; this did the job.
- **Pure logic first in Node**: the editor exposes its operations
  (`window.tfLayoutEditor`); a stand-in `window`/`document` of a few lines
  was enough to run them, and found a real bug (a run list passed where a
  paragraph was expected) before the browser test.
- **`english_forms.py --apply` must never be left to rewrite
  `site/_data/summaries.yml`**: its summaries pass groups digits with no
  document's year range ("Corpus Christi 1,399", "articles 1,302"),
  changes "écus" to "Reichsthaler" and so on (44 summaries). Restore the file
  from HEAD after every `--apply` until the pass is fixed or removed.
- **An import that maps lines by number must check the text too**: the test
  export's guessed line was the wrong line, and the first version of
  import_layout.py "took it by the line number". It now refuses a line whose
  text does not match.
- **A rewrite that removes and adds one block keeps the count**: the import's
  "write if the number of blocks changed" missed a cut block; track the
  change itself.

### Joining split documents and renumbering (2026-11-23)

The plan and the editor's rulings: `docs/DOCUMENT_MERGE_PLAN.md`. The tools:
`pipeline/review/merge_documents.py` (from `units/<slug>/intake/merges.yml`;
writes `intake/merge_map.json`), `pipeline/review/merge_check.py` (`--before`,
then `--after`: every document compared through the map). Never Oe 1 Bü 9454.
Traps met in the pilot (Nr. 12765):

- **Back up the holding's cache files first**: the cache is not in git, and
  the merge renames and rewrites them.
- **A set-apart block is found by its first line, which must be unique in the
  document**: two drafts on one page both starting "An" stopped the build.
  Consecutive voices on one page are one block with one label.
- **A merged document's place moves** (the place is read from the last lines,
  now the enclosure's or the draft's): give the main letter's place as an
  override in `rulings.yml`. `merge_check.py --after` catches it.
- **The order of the rebuild**: after `relabel_scans.py --apply` (the page
  images carry the document number in their names) run
  `make_scan_derivatives.py`, then the per-unit steps TWICE (build_db runs
  before match_scans, so the first pass leaves the old image names in the
  dataset), then the site.
- **Legacy addresses**: `/letters/<unit>/<n>/` forwards used to be written
  from the current number; a renumbered holding's are now written from
  `merge_map.json` (`build_site_data.py`), and a `/documents/` number no
  document holds any more forwards to where its document went.
- **The dataset build never prunes**: `dataset/documents/` and
  `dataset/text/` kept the retired numbers' files (Nr. 12765, 25-30) until
  removed by hand; merge_documents.py now removes them.
- **More places name a document than the pilot showed** (the second batch):
  the registers by key `slug-N` (people.yml `only_in`, glossary `only_in` /
  `not_in`, connections `uid`, gazetteer sources), the family tree and the
  gazetteer by address, the era pages by markdown links whose visible text
  is the number ("[2]", "[Nr. 3709, document 5]", "[Contract 24]"), and
  `catchwords.yml` by `letter:` (missed at first: a catchword was said twice
  in Oe 1 Bü 14526, caught by `merge_check.py`). The tool now does them all;
  `merge_refcheck.py --units …` checks every changed line of the shared files
  against the maps, and the holding's own `[[n]]` citations are checked
  separately. Read the era pages after a merge.
- **A holding translated in session** keeps `intake/translation/doc<N>.yml`
  and `write_cache.py` under the old numbers: never run them again after a
  merge (said in the holding's notes).
- **Citations come in three forms**: `[[4]]` in a holding's own about.md
  (checked by check_unit_text.py), `<a href="{{ '/documents/…/4/' … }}">4</a>`
  and plain `/documents/…/4/` (timeline). Map each once; check the changed
  lines against the map afterwards.

### The date after the signature (2026-11-23)

The editor's rulings and the method are in `docs/DATE_ORDER_PLAN.md`; the
tool is `pipeline/review/date_order.py` (scan, `--move`, `--snapshot` /
`--compare`, `--restamp`). Traps met in the pilot:

- **The page files under `transcriptions/` and `corpus.txt` already
  differ** in places: letter 182 of Oe 1 Bü 9454 has "zu" in the corpus and
  "z[u?]" in its page file (the correction "z[u] -> zu" was made in one
  only). The move takes the page file's own lines where every line is nearly
  the same and reports the difference; it does not mend it.
- **`transcription_decisions.csv`'s "@n" line numbers go stale**: three of
  them pointed at lines of other documents. The sheet is a record keyed by
  `pad`, read by no build step; never use its numbers to find a line.
- **`resolve_paragraphs.py` carries a decision over by the line's text even
  when it is not held**: a moved line keeps its old break ("1814." stayed a
  paragraph of its own) unless its row is set. Set a row for every line whose
  neighbour changed.
- **`regenerate.py` shows only lines matching its KEEP list**, so
  `resolve_paragraphs.py`'s "hand-set row not found again" is hidden: after
  writing hand rows, run the step directly and read its output.
- **Moving German lines changes the translation cache's `source_hash`**, and
  `translate.py --stale` then asks for a paid re-run of words that did not
  change: `date_order.py --restamp <letters> --unit <slug>`. (Before this
  work 199 letters of Oe 1 Bü 9454 and 13 of Nr. 12765 were already listed as
  stale: their German was corrected after translation and the English
  mended by corrections. Not this work's; reported to the editor.)
- `english_forms.py --apply` rewrote `site/_data/summaries.yml` again (46
  changes): restored from HEAD, as the note above says. To bring one new rule
  into the summaries, apply that rule alone to the file's values.
- **A new house-form rule can break the page corrections**: the forms run
  before `english_corrections.yml`, so a correction whose `find` has the old
  form ("v. Triebenfeld") stops matching at the next publish from the cache,
  silently undoing it. After adding a rule, run its pattern over every
  correction's `find` and `replace` and update the hits. (The editor's "von
  Triebenfeld across the English", 2026-11-23: three of the date corrections
  were hit.)
- **A restamp can hide an older change** (a mistake made and repaired,
  2026-11-23): `--restamp` set 177 moved letters current, and 109 of them had
  been on `translate.py --stale`'s list before for corrections made after
  translation; the list fell from 199 to 90. Repaired with
  `date_order_unstamp.py` (the hash of the German before the move). Take the
  `--stale` list BEFORE moving, and restamp only letters that were not on it.
  The pilot's four were found stale by diffing their German at the v2
  translation (commit af752fb55) against the German before the pilot.
- **What the page files are** (asked by the editor, 2026-11-23): the
  transcription as first delivered, one file per page;
  `pipeline/intake/import_pages.py` assembles `corpus.txt` from them once,
  when a holding comes in, and refuses to overwrite a non-empty corpus without
  `--force`. From then on `corpus.txt` is the text: the site, the dataset and
  every check are built from it, and corrections are made there. Keeping the
  page files in step by hand (the rule under "A changed line of
  transcription") was often not done, so they lag. Never rebuild a corpus from
  them. **Removed from all 57 holdings at the editor's word (2026-11-23)**:
  "I won't look at them again - I look at what's on the website, and we
  could always build them from the website view." `courtbook.py` no longer
  writes them; NEW_UNIT.md says to delete them once `import_pages.py` has
  assembled a new holding's corpus.
- **The full-size originals of the Neuenstein files** (Oe 1 Bü 9454, 14525,
  14526, Oe 1 U 199) are on the editor's J: drive:
  `J:\Documents\Archive\Genealogy\References\Hohenlohe-Zentralarchiv
  Neuenstein\<file>\` (an opening per image, about 2,760 px wide). The site's
  copies (`site/assets/scans/`, 1,100 px) are too small to settle a doubtful
  word: letter 85's closing was read four ways from them. Crop the original,
  open it for the editor (`Start-Process <png>`), and look for the same
  word elsewhere in the document: the King's salutation "Freundlich lieber
  Oheim!" settled "gutwilliger Oheim" (the editor confirmed it on the image).
- **Letters from officials** (the editor's two answers of 2026-11-23 taken
  together): a date that breaks a closing (between the salutation or the
  closing formula and the signature) moves, whoever wrote the letter; a date
  directly before a bare signature stays in an official paper (a minister's
  or office's letter, a rescript), and moves in a private person's note or
  petition.
- **A change to `pipeline/numerals.py` is proved over the whole edition**:
  run the HEAD version and the new one over every corpus line and English
  line and read every line that differs (the Polish "1865 r." fix changed
  nine lines, all dates). The pattern is in `verify_numerals_diff.py`.
- **Moving a postscript to the end can change a letter's place**: the build
  reads the place from a letter's last lines, and letter 104's moved
  postscript ("Etwann den 16ten April gehn ich…") gave "Etwann". The
  before/after compare caught it; a place override in `rulings.yml` (the
  letter's own dateline) put it right.
- **The page files are older than corpus.txt in many places**: word
  corrections made in the corpus only ("Wein" for Wien, "E h[?] d" for the
  expanded salutation). Find a page's own file by the page id at the end of
  its name, not by its text.
- **A sub-agent drafting English dropped the full stop ending the date**
  ("1798." to "1798") in 33 of 56 drafts against the rule; put back by a
  check (a paragraph-final full stop of the original kept). Read every draft.
- **A line that ran on after the signature runs on into the moved date**
  (letter 167's postscript): the move step now sets the line after the date
  to begin a paragraph.
- **Proof that a hand-mended published page survives a re-publish**: run the
  cache's English through `english_forms.apply_page` and compare it with the
  published page; equal means a publish would write the same.

### The German follows the editor's English layout (2026-11-23)

- **The editor's rule** (2026-11-23, on app539680782): when they lay out a
  document's English and hand over the export, the session reads the German
  reading text against it and makes the reading text's paragraphs match the
  English, by hand, for the documents in that export only. They don't touch
  the German view themselves (they don't read German), so the export's
  `german` list is usually empty and the work falls to Claude. No machine
  for this was wanted: the session proposed a mirroring script and the
  editor declined it ("I only am talking about this one document").
- **How**: for each English paragraph that now begins where no German one
  does, find the German line where the same text begins and add a row to
  the holding's `paragraph_decisions.csv`: `decision break`, `confidence
  held`, **`cue hand`** (any other cue is dropped by `resolve_paragraphs.py`
  on the next run), `prev_line` the line before, `context` the line's first
  70 characters. For a join, `decision join` on the second paragraph's first
  line. A split that falls mid-way through a German line can't be shown in
  the reading text (breaks are by line): report it to the editor.
- On app539680782 the published English had followed the German paragraph
  for paragraph; the editor's layout split off the dateline and the last two
  signatures, and three breaks were added (corpus lines 4, 45, 46).
- **A paragraph with a Shift+Enter line break has no first-line indent**
  (the editor, 2026-11-23: "Vienna, the 25th of October // 1814." showed its
  first line indented, the second flush). The English indents every `p + p`
  by 1.4em; `layoutPara` in letter.js now gives a paragraph with a line
  break the class `lines`, and style.css sets it flush. The editor draws
  with the same function, so it shows there too.

## OCR of a ruled Polish table (2026-11-05)

The Rusinski 1947 sitting's lessons, for the next ruled-table scan:

- **A ruled table defeats full-page psm 3**: Tesseract segments the grid
  by its columns (column-major output) or mangles the rows. The row-major
  reading comes from psm 4 ('single column of text of variable sizes'),
  the geometry from the word boxes. Neither alone suffices: psm 4's row
  parse drops rows whose leading number misreads, so the numbers anchor
  targeted strip re-reads (the row's y from the number column's token
  tops, x 650-1300 in these sheets) and the missing rows are recovered
  band by band.
- **Tesseract conf 0.0 is a quirk, not a badness signal** (psm 3): words
  read perfectly carry 0.000000 confidence. The doubtful set is conf
  1..threshold plus the pass-vs-pass disagreements (difflib over the
  token sequences, the Dorow method); conf 0 counts as unknown.
- **Superscript footnote markers in a print of this kind are lost by the
  page passes** (they glue to the host word or vanish; the box-height
  signal does not separate them). They resurface in 2.5x single-line
  re-reads (psm 7) as glued digit tails and standalone 1-2 digit tokens;
  context rules (a digit after a letter-word, not between numerics)
  filter the false positives; the page's own note count (the footnotes'
  leading numbers, parsed from the page foot) is the assignment check.
- **A footnote parse that requires note 1 to read as "1" silently drops
  whole note blocks** (2026-11-05, the editor's "are you sure you didn't
  miss any footnotes?" caught it: 336 -> 549 notes). Parse the note
  block by GEOMETRY (the body-to-notes whitespace gap, candidate blocks
  scored by which yields a proper 1..k chain), and recover a note start
  whose printed number the page pass mangled from the 2.5x line pass
  ('ty Schmidt' -> '% Schmidt' -> note 2). Verify the inventory with an
  independent bottom-of-page scan, not by re-reading the parser's own
  output. Beware a printed source's own numbered clauses (the wilkierz's
  1.-44.) parsing as notes: they are the text, not apparatus.
- **Strip-band reads settle orientation empirically**: probe each sheet
  in four orientations with a middle band at 1.5x and score the plausible
  Polish words; do not assume scan parity decides.
- **A footnote parse built on one witness cannot see its own boundary**
  (2026-11-05, Rusinski 1947, second sitting of the problem): the
  largest-gap block parse under-counted (0103: 17 notes in the print,
  5 found - the printed numbers 8..17 sat unread in the note texts)
  and swallowed body (0075: the section heading '2. Sklad spoleczny',
  digit-led with a big gap above, parsed as a note). The parse that
  held: the page's own lines are 1:1 with the print's lines when the
  TSV words are grouped in READING ORDER (a top-sort orphans the first
  word of lines on warped baselines); a 3x strip of the whole foot is
  read with **psm 4** (psm 6 reflows dense note blocks into one
  paragraph and loses the note boundaries) and its lines are ALIGNED
  to the page's lines; a strip line matching a page line's prefix
  starts a note iff its leading token is a small digit (requiring
  footnote-size type - a section heading is body-size type), a strong
  artifact glyph, or a digit-1 lookalike; a strip line inside a page
  line is a psm-4 split artifact; every alignment pair must earn its
  ratio (debris strip lines otherwise consume page lines and leave
  real note lines homeless); the strip is trusted only within its own
  y-coverage. A note block is re-segmented, not re-read: per-note crops
  polish texts afterwards, and a marker-less note (the OCR dropped the
  glyph) is recovered from the psm4 paragraph break + sentence end +
  citation opener.
- **An abbreviation period is not a sentence end** ('C.', 'fol.',
  'AW. A. 1-4.' end mid-citation lines; writing the abbreviation list
  as a character class [fol|s|nr] matches ONE character and never
  works - alternation, not a class).
- **A page's last body line often ends mid-sentence** (the paragraph
  runs over the leaf): a body/notes boundary check demanding
  sentence-final punctuation flags dozens of innocent pages.
- **A script named after a stdlib module shadows it**: fractions.py
  broke PIL's TIFF plugin (UnidentifiedImageError on every open, only
  inside that process) because PIL imports Fraction from 'fractions'.
- **Witness chains must be re-verified after any upstream boundary
  change**: marker tops from the old lineation never equal-matched the
  rebuilt line tops and label placement silently collapsed (469 -> 45);
  match by proximity, not equality, when the lineation changes.
- **The hyphen-join must REPLACE the fragment, not append the joined
  word after it** - the append duplicates every broken word ('zna-
  znanej'); ~70 kB of duplication hid inside a 415 kB draft.

## Working on main; merging the old branches (2026-11-21)

- **The editor's word: work on `main`, push and publish.** The per-holding
  branches are gone (38 merged ones deleted, the superseded
  `agad143201139` with them); `rusinski1947` merged and `kneifel1964-pages`
  cherry-picked into `main`; `place-name-sources` kept (unmerged work the
  editor did not name). Pushing `main` is publishing (CLAUDE.md, "Branch and
  publishing").
- **A conflict resolver's check must look for marker lines, not marker
  text, and nothing may be committed after it fails.** WORKING_NOTES itself
  quotes "<<<<<<<" in prose, so `assert '<<<<<<<' not in s` failed after the
  markers were gone; the shell's `&&` chain then ran `git add` and `git
  commit` on the next line regardless (the failing Python was not the
  chain's first link), and the merge commit carried the markers until a
  fix commit. Check with `grep -n '^<<<<<<< \|^=======$\|^>>>>>>> '`, run
  the commit as a separate step after reading that it is empty.
- **Cherry-picking an old branch's one commit beats merging it** when the
  branch is hundreds of commits behind: the generated files conflict
  (take `main`'s and rebuild), and its TODO section number is already
  taken on `main` (give it the next free number).

## The place-name databases (from the branch place-name-sources, 2026-10-24; merged 2026-11-21)

These lessons were written on the branch and reached main only when its
work was picked over (the Kodeks entries 22 to 31, the plan and the match
script; the branch then deleted). The plan is
`docs/PLACE_NAME_DATABASES_PLAN.md`; step 6, the candidates from the
Słownik's gmina and parish tables, is still to do.

- **The place-name databases and PowerShell's console** (2026-10-24): the
  converted text of the three Polish reference works (Nazwy miejscowe
  Polski, Kodeks dyplomatyczny Wielkopolski, Słownik geograficzny
  Królestwa Polskiego) is now committed in Igor's repository
  (`C:\Users\Tersnaus\Downloads\polish-place-name-sources`, cloned beside
  this one; its `RIGHTS.md` permits reading, searching and citing).
  PowerShell's console garbles Polish diacritics in `Select-String` and
  `Get-Content` output and cannot take a path with "Trąbczyn" as typed —
  the text is UTF-8 and clean; read it through Python with
  `io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')`, and match
  files by glob, not by typed name. SGKP's page anchors (`<!-- p.NNN -->`)
  give printed pages (Trąbczyn's entry sits at p. 448 of t. XII, as the
  gazetteer cites; Łukom's is in t. V, not t. XII); the Kodeks files have
  no page anchors — cite by charter number. NMPol is alphabetical and
  stops at Ś (t. 18, 2025): names from T to Ż have no entry yet. The
  Słownik's homonyms are real: its Łukom search returns the Łukomski
  estate near Orsha before ours — match on name plus
  powiat/gmina/parish context, never the bare name. Plan:
  `docs/PLACE_NAME_DATABASES_PLAN.md`.
- **Add-Content mangles more than diacritics** (2026-10-24). A PowerShell
  here-string appended with `Add-Content -Encoding UTF8` garbled Polish
  letters ("S\latwo" for Słownik) and ate backslashes in code spans
  ("`rzgow`" became a newline plus "zgow"; "\build_site_data" became a
  backspace plus "uild_site_data") — the console layer, not the file. Write
  any content with diacritics or backticks through the edit tool or a
  Python script file; never `Add-Content` for prose. (Extends "The
  place-name databases and PowerShell's console" above.)
- **YAML reads a bare yes or no as a boolean** (2026-10-24). A decision
  written unquoted into the match log's flow mapping
  (`{ decision: no }`) round-tripped as `False`, and the restore of the
  editor's decisions silently skipped every `no` (`False` is falsy). Quote
  every string value that is a bare yes/no/on/off/true/false in a
  hand-rolled YAML line — or better, quote all of them
  (`pipeline/gazetteer/match_sources.py`, `_log_row`). Found because a
  test decision did not survive a rebuild.
- **Hand-written JSON with OCR text inside: scan for invalid escapes
  before parsing** (2026-10-25). Three of 2,306 translations carried a
  stray backslash copied from the OCR (e.g. "Bisch\i'itz",
  "Czieln iro\vo"), each of which broke `json.loads` on the whole
  per-batch file. A one-line scan for `\x` where x is not a valid JSON
  escape (`\\[^"\\/bfnrtu]`) found all of them; the merge script now runs
  after it. Same day: the merge script checks every batch line's id
  against the per-batch translation file, which caught four pieces
  skipped while writing the batches — always merge with a coverage
  check, never assume the per-batch files are complete.

## The candidate places (2026-11-21)

- **The dictionaries' converted text is in Igor's private repository**
  (`igor/polish-place-name-sources` on GitHub; the editor is a
  collaborator). The copy in Downloads that `match_sources.py` reads had
  gone; fetch only the folders wanted: `git clone --filter=blob:none
  --no-checkout`, then `git sparse-checkout set --cone sources/sg` (75 MB;
  `sources/nmpol` 29 MB, `sources/kdw` 19 MB) - the whole repository is
  about 500 MB.
- **The Słownik's gmina paragraphs do not list the gmina's villages** in
  powiat słupecki (they give the court, the post office, the area and the
  population). The places of a parish are found from the other side: every
  entry that names "par. X" or "gm. X", with an OCR-tolerant pattern
  (Trąbczyu, Zagorów, "gm. i par."), and the estates' own lists of their
  parts inside the big entries.
- **A page's next entry is not the entry.** The Olchowo footnote of
  2026-10-26 took "gm. Kołki ... 141 dm., 776 mk." from the line after
  "Olechowo ... Do r. 1891 nosiła nazwę Sophienthal"; they are Olejniki's,
  in Volhynia. The Słownik's entries run on without breaks in the converted
  text: read a cited fact back to its own headword before writing it.
- **Sonnet readers for the Słownik's entries worked** with a brief that
  told them how numbered runs abbreviate the headword ("3. B. , wś"), to
  give the full headword and the printed one, to list an estate's parts,
  and to put every doubt in a note: 65 entries in two batches, the
  headwords and facts right where checked; the two entries whose head was
  on the previous page were left empty, as the brief asked, not guessed.
  The identifications against the edition stay Claude's.
- **Search Nazwy miejscowe by headword, not by nearby local words.** Its
  entry names the district before the attestations ("Goździków (1), wś,
  koniń., gm. Rzgów, 8 km na płd.-wsch. od Zagorowa: Gozdzików ... 1827"),
  so a search that wanted "Zagór" or "słup" in the text after the name
  missed Goździków, and Claude told the editor the remaining candidates were
  "too small" for the work - a guess stated as a finding. Find the
  headword line ("Name (n), wś|os.|kol.|cz. wsi ...") and read its district;
  say plainly what is not covered (T-Ż not yet published; streams and hills
  are not its subject) rather than explain an absence.
- **The editor's scope for the candidates, widened 2026-11-21:** "Yes, read
  the Słownik around the others as well" - the parishes of Rzgów, Pyzdry,
  Stawiszyn and Zbiersk and the gmina of Grodziec, beside Trąbczyn and
  Zagórów. Filter by powiat (słupecki, koniński, kaliski) after the mark:
  another Rzgów lies in powiat łódzki, and the OCR writes "powiat", "pow,"
  and "koniu Hki" for the district.
- **The heredoc trap, twice more this sitting (2026-11-21).** A Python
  script passed through a Bash heredoc to rewrite another Python file had
  its `'\\n'` turned into a real line break, and a sed-style replacement
  of a line with backslashes and quotes silently failed to match. Write
  such a script with the Write tool and run it, or make the change with
  Edit; check the edited file compiles before moving on.
- **The dictionary sentences of 2026-10-26 had systematic errors (audit of
  2026-11-21: 15 of 53).** The generated pattern "records it as KIND, gmina
  G, parish P, with N houses and M inhabitants at the time of the
  Słownik" took the first figures and names it met: the next entry's
  (Olchowo, Tarszewo), another sub-entry's parish (Zalesie), the 1827
  figures (Grądzeń, Kopojno), the village's figures for the folwark
  (Imielno). The Nazwy miejscowe pattern "records the name as X by YEAR"
  took a locative (na Stawisku), a location (między Łukomiem a
  Myszkowem), a genitive (Czarnegobrodu) or the next entry's form
  (Crosczino) for a name. Write such sentences by hand from the entry's
  own bounds, and say which year a figure belongs to.
- **Auditing citations with Sonnet readers works if Claude checks every
  finding.** Of 22 flags, 14 were real; the rest came from what the
  readers could not know: Nazwy miejscowe's printed page is the converted
  text's page mark minus one (Adamierz: mark 45, printed 44); the edition's
  corrected excerpts (`literature/slownik`, three OCR witnesses on the
  page image) outrank the raw converted text (Augustynów 358 against 368);
  and an entry outside the snippet given is not a missing entry.
- **verify_site's leak check for works kept off the site** takes 60
  characters from the middle of each excerpt's longest line, in both
  languages. An English summary written in the same words as the
  gazetteer's sentence trips it on the place page: keep the summaries of
  `literature/slownik` and `literature/nmpol` in clipped note form ("Colony;
  gm. Emilienheim, par. Zagórów; 17 versts; 8 houses / 61 inhabitants").
- **The gazetteer's `aliases` are the editor's cross-reference headings**
  (the import of 2026-10-23 made them from "X, see Y" lines). Since
  2026-11-21 the Places index shows each as "X - see Y", leaving out an
  alias that is now an entry's own heading. A new "see" name goes into
  `aliases` (the editor, 2026-11-21: Biały and Bawół under Czarna Struga).

## The site overhaul of 2026-11-24 (docs/SITE_OVERHAUL_PLAN.md)

- **Crops of staged page images are recorded, not just made.** A crop goes
  into `units/<slug>/intake/crops.json` (box as fractions of the uncropped
  1100-px derivative, with its `from_size`) and is applied by
  `pipeline/intake/apply_crops.py`, which only touches an image still at
  `from_size`; `make_scan_derivatives.py` applies the same boxes when it
  remakes a derivative from `pages/` on the desktop. Cropping
  `site/assets/scans/` by hand would be undone by the next `--force`.
- **The crop page is the fold page's box mode** (`crop_sheet.py <slug>...`),
  self-contained (images embedded), with "Copy JSON" so the editor can paste
  the boxes into a cloud chat; `apply_crops.py --grouped <file>` takes it.
- **`site/_data/summaries.yml` is authored**, despite its "Generated"
  header. Change a summary only through `pipeline/review/set_summaries.py
  <batch.yml>`, which also updates the holding's drafting record.
  `docs/PROSE_SOURCES.md` lists where every kind of English prose is kept.
- **`pipeline/review/prose_lint.py`** lists candidate breaches of the rules
  of 2026-11-24; its R1 and R4 hits are good, its R2 ("the" at first
  mention) is noisy and only a pointer.
- **A rewrite that supplies a missing fact must be read from the holding**,
  not reasoned out: the first draft of the Weigel summary (agad118501169)
  gave the courts' grounds and the finance commission's argument from
  general knowledge and got the latter wrong; the holding's about.md had the
  real ones.
- **Sub-agents can stop on the account's usage limit** (2026-11-24, both
  Sonnet agents at once). Their edits so far stay in the working tree;
  resume them with SendMessage after the reset rather than starting anew.

### The work pages: reading column, margin page marks, the width check (2026-11-24)

The editor's chosen answer for a work of the literature ("a reading column
with a contents panel"): `literature_site.py` writes the whole reader
(`.lit-reader`: the contents panel `.lit-toc`, then `.lit-text` with one
`.lit-passage` per printed page); the layout only adds the head and the
viewbar. Lessons:

- **One page-mark style for everything**: `.pg` (a zero-size block whose link
  hangs in the left margin, id `p41`; on a phone it becomes a label line). The
  literature draws one per passage (a passage is a printed page; "front" and
  "after p. 12" for the unnumbered ones); the newspapers draw one for each
  page-number line the text carries, found by `pipeline/pagemarks.py`. A bare
  `[720]` line counts only inside a run of consecutive numbers (at least two);
  the named forms (`[s. 720]`, `[p. 720]`) and `- 720 -` count alone; footnote
  `[^n]` markers, table cells and years never do. `pipeline/review/page_marks_report.py`
  lists the forms per work and item. Found: the passage keys of the literature
  (all drawn), and in the press only the bare `[N]` lines of zdrowie1912z10,
  zdrowie1914z6 and jutrzenka1913z8; nothing else in the texts.
- **The full-width bug** was the summary-only works (Seidel, Słowiński &
  Połom 2024, 2023, Dąbrowska, the two dictionaries): `.lit-summary` had no
  measure. Also uncapped: the English title line of every work, the "In the
  literature" paragraphs on a document page (1331px), the clamped summary of a
  document and of a newspaper item, and a newspaper's text beside its clipping.
  All capped now (70ch for text, 46rem for facts and summaries).
- **`pipeline/review/check_text_width.py`** serves `site/_site`, opens every
  built page of the literature, newspapers, places, people, holdings and a
  sample of the documents (`--docs N`) at 1440px in Chromium (Node +
  Playwright) and reports any paragraph or list item with a text line wider than
  760px. A holding's page is laid out at `--wide` (62rem, 992px) by the
  editor's earlier rule, so its text is held to 1000px, not 760; the list pages
  (cards) are skipped. Run it after any layout change, after the Jekyll build.
- **Side by side needs 80rem** (two 70ch columns do not fit a narrower
  screen beside the contents panel); between 64 and 80rem the panel stays and one
  text shows; below 64rem the panel is a sticky button and drawer. The saved
  view moved to `tf-lit-view2` so the old "English" default does not hide the
  side-by-side one. The translation labels ("English translation by
  Claude...") are gone from the work and newspaper pages; `np_caveat` stays
  for the Zagórów place page only (the About page keeps the statement).
- **A grid row with a Related note**: side by side, the original spans the
  English row and the note's row (`grid-row: 1 / span 2`); otherwise the note's
  row adds blank space under the original.

- **Rewriting a holding page: read its notes.md rulings first.** The rewrite
  of APP 53/4/0/-/62 put back a claim the editor had struck on 2026-10-26
  (that the Szetlewicz surname is formed from the village); it was caught
  and taken out. A ruling recorded in a holding's notes, or in CLAUDE.md's
  "Where things stand", binds every later rewrite of its prose.
- **`pipeline/review/check_unit_text.py` checks the rewrites.** It fails a
  sentence of an about.md whose figures or dates are not in the documents
  it cites, and a sentence with no citation that is not marked
  `<!-- context -->`. Run it after every rewrite: on 2026-11-24 it caught two
  dates supplied from outside the cited document and two citations lost in
  rewording.
- **Supplying a missing fact (the editor's "stopped paying whom?")** is
  done from the holding's own documents, summaries or a holding that
  explains the term (the hereditary-lease terms from 53/968/0/-/801, the
  mother-in-law from Kraus 2001), never from general knowledge alone; where
  the documents do not say, the sentence stays without it.
- **The 57 holding pages were rewritten to the rules on 2026-11-24**: the
  archive's description of its fonds dropped from the court books (the
  account of the court kept), "Dating", "Notes on the entries", "The copy"
  and "Originals and copies" sections dropped (their content is in each
  holding's notes and in the documents' own date fields), the Latin legal
  terms of Poznań Gr.1181 put into plain English. The document summaries,
  the era, place and person pages are the next steps (SITE_OVERHAUL_PLAN,
  Phase 6).
- **Search anchors.** A literature passage has two anchors on its work's
  page, `id="p-<key>"` (what the search index links to, ANCHOR in
  `search_indexes.py`) and `id="p<page>"` (the margin page number). Keep
  both if the work pages are rebuilt.
- **The year range** of the search bar is written to `site/_data/stats.yml`
  (`year_min`, `year_max`) by `search_indexes.py`, and `verify_site.py` fails
  when new material falls outside it: run `search_indexes.py` again.
- **The era pages carried errors the rewrite found** (2026-11-24): the
  insurgency page dated Prussia's taking of the Konin country to 1795 (it
  was 1793, the Second Partition); the boundary page made the division of
  1740 the father's (it was the brothers' own); the Hohenlohe page had a
  stray half-sentence and called the restitution "the third era ... not yet
  published". Read an era page against its holdings' pages, not only
  against the rules.
- **The editor on the title pages** (2026-11-24): no typeset title tiles for
  literature without a picture; they will supply title pages. The duotone
  icons stand, at a lighter stroke (1.15).
- **The German waits** (the editor, 2026-11-24, at the publish of the
  overhaul): the English prose rewrites are published without their German;
  "we'll do it all at once later in the project". Do not rewrite German
  pages piecemeal meanwhile.
- **Publishing from a cloud session** went as CLAUDE.md says: the session
  branch fast-forwarded onto `main` (`git merge-base --is-ancestor
  origin/main HEAD` first), `git push origin HEAD:main`, then the "Build and
  deploy" run (pages.yml) watched with the GitHub tools until it succeeded.
- **Root-relative links 404 on the live site** (2026-11-24). The live site
  is served under `/triebenfeld-letters`; the local build has an empty
  baseurl, so a link written `/documents/...` in a page source, or inside a
  `{% raw %}` block, looks fine locally and breaks live. The place entries'
  citations (generated into raw blocks) and fourteen glossary links of the
  era pages were broken this way. Every internal link goes through
  `relative_url`; inside a raw block, step out of it for the URL
  (`{% endraw %}{{ '/x/' | relative_url }}{% raw %}`, as
  `place_pages.footnote_md` does). verify_site now fails on any such link.
- **Showing a hidden work takes two steps**: setting `visible: true` in its
  work.yml is not enough; run `build_literature.py` before
  `literature_site.py`, or the page stays a summary (Nazwy, the Słownik and
  Słowiński 2023 stayed summaries on the live site after 2026-11-24's
  publish until this was found).

### Places, people and the glossary (2026-11-24/25, docs/PLACES_PEOPLE_GLOSSARY_PLAN.md)

- **Place coordinates have one source of truth for the site**:
  `site/_data/place_coords.yml`, written by `pipeline/places/coords.py`
  (gazetteer `location:` first, then `reference/place_coords.yml`, then
  `reference/places_osm.yml` by printed name, then an approximate
  position for a gazetteer place described only as "north of X"). The
  script fails, in regenerate.py and verify_site, on a place with no
  position and no reason in `reference/place_coords_unplaced.yml`: a new
  place needs one or the other. The place pages read the generated file,
  not the reference one.
- **The old positions were not safe**: the hand placings of 2026-10-27 lay
  10 to 60 km out, and OpenStreetMap's search had matched Dresden to a
  village in Lubusz, Cosel and Wieruszów to namesakes. Wikidata (its API is
  reachable from the cloud) gave better matches, but only after each was
  chosen by hand: the first hit for a German or Polish place name is often a
  namesake. Prefer the town with the German name the documents use
  (Medzibor = Międzybórz near Syców; Scheitnig = Szczytniki, Wrocław).
- **Importing a script that rewraps `sys.stdout`** (`io.TextIOWrapper(
  sys.stdout.buffer)` at module level) closes the importer's stdout when
  the old wrapper is collected ("I/O operation on closed file"). A script
  meant to be imported (coords.py by verify_site) rewraps only under
  `__main__`.
- **The bios' conventions** (all 324 rewritten 2026-11-25): open with the
  role, never the name the heading gives; "Prince Hohenlohe-Ingelfingen"
  and "Peter Friedrich von Triebenfeld" (or "the Prince's agent,
  Triebenfeld,") at first mention in every bio, since each bio stands
  alone; say whose estates, debts or claim, and against whom; no "the
  letters", "the report", "named once in a document": a person known only
  by a mention is "Named in 1799 in the affairs of ...; who he was is not
  known." Reichsthaler written out, not "Rthl". Rewriting adds no fact the
  old bio or the documents do not give: two of Claude's additions (a motive
  for a certificate, "on the Łukom side") were struck before applying.
- **The Places page's Near search** shows an approximate place's distance
  as "c. 3 km" or "close by", never a precise figure; approximate places
  get no map marker.
- **Playwright from Python is not installed in the cloud**; Node's resolves
  (`require('playwright')`, from /opt/node-tools/node_modules). Write
  screenshot checks in Node.
- **The People page's era view** gives a person in two eras a card in each;
  only the first carries the `id` anchor, and the A-Z and mentions views
  move the first cards into one list and hide the rest (people-index.js).
  The relevant people come from `reference/people_relevant.yml`.
- **Removing a glossary entry** leaves its words unruled: run
  `pipeline/review/glossary_candidates.py --check`, and put each word it
  lists under `excluded:` with the reason (2026-11-25: the twenty letter
  formulas and courtesy styles, the editor's ruling). Check first whether
  the English keeps the term as written: "L. S." does, so *locus sigilli*
  stayed.
- **A unit the English renders inconsistently keeps its own name**
  (the editor, 2026-11-25, of grzywna): fix the forms with a rule in
  `reference/english_forms.yml` (the translations) and by hand in the
  literature's english.md, and give the unit a glossary entry.
- **Person pages' biographies** (2026-11-25): `biography:` in a person's
  block of `reference/genealogy.yml`, a list of paragraphs, each with
  `text` and `source` (document uids, `doc:<uid>`, literature
  `work/passage`, or `editor`); English only, shown under "Life". Method
  that worked: a Sonnet reader per group of people writes a facts file
  (dated chronology with uids, life dates, discrepancies) from the
  summaries and the turning-point translations; Claude writes from it and
  checks anything doubtful against the translation (letter 107's "Princess
  Sacken" said less than the summary). The readers also found errors in the
  short bios and a document wrongly tagged to Michalina: fix those in the
  same sitting. verify_site needs every person page to have a short `bio`
  in people_bios.yml as well.
- **Rewriting summaries at scale** (2026-11-25, all 649): Sonnet readers
  draft per batch of about 105 (brief: the house-style sections, keep every
  fact, add none, read the holding's notes.md); a script compares old and
  new for lost figures and names and for paper words, and lists names a
  draft added; Claude reads the flagged ones and the readers' reports of
  contradictions, and fixes against the translation; then one batch file
  through `set_summaries.py`. Traps seen: a reader supplying whose
  plenipotentiary a man was, a summary dated by the enclosure's year
  instead of the note's, "at the same sitting" (pointing back), and bare
  "Triebenfeld" at the start (finalize adds "Peter Friedrich von
  Triebenfeld, agent of Prince Hohenlohe-Ingelfingen,"). The readers found
  a dozen old summaries that misread their letters: ask them to report
  those separately.

## Merge markers in a holding page (2026-11-25)

The commit "Holding pages to the rules: Oe 1 Bü 14526" (064634c7) left raw `>>>` / `<<<` / `===` blocks, the two versions of a sentence, in the `about.md` of four holdings (agad14320139, app53170koningr153, ihagrrep7cnr3709, iiihamdaiiinr12367); the site showed them as a quote in "Contents", and in agad14320139 the section's opening sentence was gone. Fixed by taking the newer wording; the German pages had been spared. After any bulk edit of `about.md` files, `grep -ln '^>>>$\|^<<<$\|^===$\|>>>$' units/*/about*.md` must be empty.

## The to-do audit and page (2026-11-25)

- **Audit method that worked** (docs/TODO_AUDIT_2026-11-25.md): the open boxes pulled out by script (a box and its continuation lines), five Sonnet readers of ~27 each, read-only, each verdict DONE / SUPERSEDED / DUPLICATE / OPEN / UNSURE with a quoted file as evidence; Claude then re-checked every verdict that closes a box (files exist, dates agree) before TODO.md was touched. Of 133 boxes 45 closed, 88 stayed. A reader that finds a question already in NEEDS_CONFIRMATION calls it a duplicate: that is "moved", not "answered".
- **Background Sonnet readers die on the account's usage limit** (HTTP 429, "resets at ..."): their half-written files may be missing or partial. After a restart list the output files, check each against its batch (same count, same `n` order) and send only the missing batches again; do not trust a file just because it exists.
- **Liquid trap:** `where_exp` cannot see a loop variable (`x.types contains ty.slug` is a syntax error in Liquid 4); count with a plain `for` loop.
- **Looking at a built page:** the site's links are root-relative (`baseurl: ""`), so a `file://` screenshot has no CSS; serve `site/_site` with `python3 -m http.server` from that folder and open `http://localhost:<port>/...`.
- **The search bar** is one component (`_includes/browse.html`, `.filters` in style.css); a new bar (Places, Glossary, the to-do page) uses the same classes (`f-main`, `f-bar`, `f-grid`), never its own look.
- **Run order trap in the to-do build** (2026-11-25): `build_todo.py` overwrites `docs/TODO.md`. Archive an old `TODO.md` (git mv or `git show HEAD:docs/TODO.md >`) BEFORE the first run, or restore it from git afterwards.

## Pyzdry Gr.75 begun, and the Tracholz entry (2026-11-26)

- **The volume is settled** (the editor, 2026-11-26): Pyzdry Gr.75 is
  "Inscriptiones [protocollon] 1768-1781"; the "Relationes 1768-1771" folder
  was a second copy of the same volume and is deleted on their machine. Two
  scans are the whole extent, no cropping or fold step, and the editor's own
  transcription is used and checked against the scans. The editor's translation
  is a guide only. The holding is **not yet built**: the scans, the Latin and
  the English are on the editor's J drive, which a cloud session cannot read
  (TODO t900).
- **Check what is already built before planning from the notes.** The first plan
  of the sitting treated entry no. 17 of 53/6/0/-/46 as "never built" because
  the old questions file (`docs/archive/PRUSIMSKI_QUESTIONS.md`) said so. It has
  been document 2 of that holding since 2026-10-07 (`units/app536046/notes.md`).
  The editor then agreed (2026-11-26, mid-sitting): no fresh transcription of it
  is needed, and the to-do item for one (t901) was removed. Document 2 stands as
  built; any close pass of it is the editor's own, whenever they choose.
- **The person entry `tracholz`** (`reference/people.yml`, the editor's yes,
  2026-11-26): surname pattern `Trach[ou]lt?z`, no `only_in`; 8 documents, 15
  hits (Konin Gr.117 docs 2, 3, 7, 8, 9; Gr.118 doc 14; 53/6/0/-/46 doc 2; Gr.120
  doc 2). Gr.120's "Trachultz" is Claude's reading (TODO t902). When Gr.75 is
  built, count its hits and read each (WORKING_NOTES mistake 7 of NEW_UNIT).
- **Trap: `build_site_data.py` rewrites unrelated generated files.** On
  2026-11-26 it regenerated four `site/_holdings/*.md` that were stale in the
  commit, and dropped `year_min`/`year_max` from `site/_data/stats.yml`. Check
  `git diff --stat` after it and commit only what the change caused (the
  holdings were checked out again, the two stats lines restored by hand).
- **Pyzdry Gr.75 built in the cloud from images the editor sent in chat**
  (2026-11-26): `units/app5321pyzdrygr75/` (slug of the reference; page ids
  `0019_a`/`0019_b`). With no raw scans in the cloud, the steps that need them were
  replaced by hand: `page_scan_map.csv`, `scan_rename_map.json`, the web copies written
  by `intake/holding.py --scans`; run the rest (`resolve_paragraphs`, `build_db`,
  `merge_corpus`, `build_dataset`, `check_mentions_join`, `connections_site`,
  `build_site_data`, `person_pages`, `search_indexes`) as separate scripts, not
  `regenerate.py`. `translate.py`'s `load_letters()` reads the merged
  `dataset/letters.json`, so `merge_corpus.py` must run before `holding.py --cache`;
  `courtbook.save_cache` also needs `pip install anthropic` in a fresh container.
- **A reader who does not crop is no second reader.** The first blind reader was
  given the whole page at the delivered size and its report (honestly) said it had guessed
  most lines; the brief said "crop and zoom" and nothing enforced it. What worked: cut the
  page into overlapping 2x strips myself (`scratchpad/gr75/strips/`, 340 px high, 240 px
  step), name every strip in the brief, ask which strips were opened. The led reader
  (the editor's text as a table of differences) found the one substantive omission, 13
  groschen after the 1,053 imperials.
- **A `str.index("S = {")` edit matched `IMAGES = {`** and deleted three blocks of
  the holding's script; the restore cost a turn. Edit a script with an anchor that holds
  once and check the file with `grep -n "^[A-Z]* = "` before running.
- **Name pattern for a scribe's variant.** Tracholz was `Trach[ou]lt?z`; the Pyzdry
  clerk writes "Traholtz" (no c) and the pattern missed the transfer itself. Check the
  new holding's own hits after building: `site/_data/people.yml` count for the person.
- **A spot sheet from strips** (2026-11-26, Pyzdry Gr.75): when the editor asks to check
  highlighted changes against the image, one HTML page does it: a card per change or
  question, the words in context with the change marked, "you had / now", and the enlarged
  strip of the page (the images inside the file once, set by a few lines of script;
  `units/app5321pyzdrygr75/intake/spot_sheet.py` is the pattern). Say on the sheet which
  strips Claude did not read itself.
- **No script in a sheet or page the editor opens in the app** (2026-11-26): the first spot
  sheet set its images with a few lines of JavaScript and showed white boxes (the viewer
  does not run scripts). Put images in the CSS (`.s_name{background-image:url(data:...)}`)
  and the card's `div` takes its height from the strip's aspect ratio (`padding-top: %`).
  Check a sheet with scripts switched off (`javaScriptEnabled: false` in Playwright).
- **Two of Claude's "corrections" were wrong when the editor looked** (Pyzdry Gr.75, 2026-11-26): "hasce"
  (from the accusative) and "hac ... recognitione" (from an ablative absolute) were argued from grammar the
  editor's reading did not have: the page shows "hisce" and "recog~tioni". A reading changed on grammar alone,
  against the editor's transcription, is a question for the sheet, not a correction: the standard (NEW_UNIT 3a)
  allows "a sentence with exactly one grammatical reading", and these had two. Likewise "usuq[ue]" for the
  editor's "sisce[?]": the shape fitted a word that suited the sense. What held: the omission (words the
  editor's line jumped over) and the crosses, whose placing the editor, looking at the page, read as one
  sentence ("una cum ... ac cum processu juris per Recognoscentem ... instituto") that Claude had cut in two.
- **Read the English-doubt rule before translating a holding** (2026-11-26): Pyzdry Gr.75's first English
  used "[uncertain: <the original's letters>]", the in-session form of the October holdings, which the
  editor's ruling of 2026-11-22 withdrew (EDITORIAL_RULES, "An unread word in the English": the English
  never carries the original's letters; the sense with `[?]` after it, or `[...]`). The editor had to ask.
  The sibling holding is not a guide to the current rule: check EDITORIAL_RULES for rulings dated after the
  sibling was built. `courtbook.write_doc_yml` still counts only the old `[uncertain:` form for
  `marker_count`; holding.py sets it from `[?]`, `[...]` and `[uncertain`.
- **"Municipal court", never "castle court" - in Claude's own prose too** (the editor, 2026-11-26,
  "Castle court is the wrong term. Check the rules!!"). The rule was already written
  (`reference/translation_glossary.yml`: sąd grodzki / iudicium castrense = "municipal court"; this
  file, "Sąd grodzki is the municipal court"), and Claude still wrote "castle court" in the guide's
  plan, in Pyzdry Gr.75's holding page (published) and in the Tracholz person entry, and "grod court"
  in the holding's description and summaries; the Sonnet readers' briefs did not name the rule, so
  their files said it too. All corrected the same day. **Before writing prose or briefing a reader,
  look up the termbase's rendering of every institution named** (`reference/translation_glossary.yml`,
  the glossary's `head_en`), and quote the rendering in the brief. "In Castro Calissiensi" in a dating
  line is the seat of the municipal court, not a castle to be named as such.
- **The rules audit of 2026-11-26** (the editor: "go through what you made and ensure you didn't skip any
  other rules"). Reading HOUSE_STYLE against Pyzdry Gr.75's pages found, beside "castle court": "the edition"
  on a reader's page (HOUSE_STYLE, "The pages do not talk about themselves"); the entry narrated as paper
  ("The entry has no date of its own", "In this volume ... this is no. 39": "The content, not the paper");
  a storytelling heading; Polish money as "florins" and "groschen" (the rule: złoty, grosz, groszy); the
  coin "imperial" used in prose before it had a glossary entry; Antoni Prusimski and Chełmski not
  identified at first mention; ranges with a hyphen (1780-82, en dash required); the Method tab saying
  "put to the editor" and naming image handling; a timeline note with a method sentence ("The date is the
  one a decree of 1777 gives"). All corrected, then a second reader audited the prose against every rule.
  **Before writing reader prose, read HOUSE_STYLE whole once in the sitting**, not only the termbase; and
  run `pipeline/review/prose_lint.py --unit <slug>` and `check_place_descriptors.py`.
- **The `IMAGES = {` trap again** (2026-11-26, the second time in one sitting): `s.index("S = {")` matched
  inside `IMAGES = {` and cut the English out of the holding's script. Anchor on `"\nS = {\n"` (with the
  newlines), and never write a replacement with `s[:a] + new + s[b:]` without asserting what lies between.
- **The second reader caught facts, not only style** (Pyzdry Gr.75, 2026-11-26). Claude's prose about
  the *other* documents of a chain was written from memory of their summaries, and was wrong twice: the
  citation of 1781 (Konin Gr.118, doc. 14) is to a hearing on the ground at Grab ordered by the Crown
  Tribunal, not "to the Crown Tribunal"; the "olim" Tracholz is in a messenger's report (Gr.117, doc. 8),
  not a protest. Also: two men named Antoni Prusimski (Paweł's brother and the Starost) on one page,
  never told apart; a sum described by the wrong purpose; an end date ("until 1786") no document gives;
  the person index filing the document under the Starost and under another merchant Simon (fixed with
  `not_in` / `only_in`); and the German for a new `dates.inferred` note forgotten
  (`reference/site_notes_de.yml`). **When prose names what another document says, open that document's
  text or summary in the same sitting; give every new holding the audit by a second reader against all
  the rule documents before it is published.**
- **The reading guide, chapter 3, and its audit** (2026-11-26/27). The guide is pages under
  `site/guide/court-books/` (layout `page`, English only; a contents page and one page per chapter; plan
  `docs/COURT_RECORDS_GUIDE_PLAN.md`). Every Latin quotation is checked by script against the transcriptions
  before publishing (the snippet in the sitting of 2026-11-27: blockquoted italics, expansions in brackets
  dropped, each "..." piece looked up). The second reader's audit caught, again, Claude's general claims made
  from a few documents: "JM" is not Jegomość but **Illustris Magnificus** (written out "J Magnificum",
  "JMagnifici"; Latin endings JMcum, JMci) - the existing English of Konin Gr.119 has "His Honour" (TODO
  t906); "each party used a summoner from its own side" holds only for Trąbczyn and Łukom; "Recognovit is the
  verb of every declaration" and "nine parts every time" were too strong; a royal-citation formula was quoted
  as a composite of several documents. **In the guide, a general statement is checked against all the entries
  of its kind (the harvest has them, `reference/guide/formulas.yml`), not a sample; a formula is quoted from one
  named document.** The reader was itself wrong once ("praesente Economo" is attested, Konin Gr.117): its
  findings are checked before acting.

## The Latin audit planned (2026-11-27)

The editor asked for a full audit of the Latin transcriptions with the tilde forms expanded, and for the
plan to say which public texts change with the corrections: `docs/LATIN_AUDIT_PLAN.md`, to-do t907. Two
things learned while measuring it:
- **Counting the Latin**: a document's language is in its holding's `rulings.yml` (`documents.language`)
  or, failing that, the first of `languages:` in `unit.yml`; `dataset/letters.json` gives the text. Of
  132 Latin documents, 31 are the Kodeks (printed, never corrected), so the audit is 101 documents on 191
  pages.
- **A correction is not finished when the transcription is right.** The same fact sits in the English,
  both summaries, the holding page, the era essays, the timeline, the connections, the index patterns, the
  dates and the reading guide's quotations. Each batch of corrections gets an impact list (the plan's
  section 5) before anything is published.
- The to-do builder has no link type for a file in `docs/`: name the file in the item's text and link a
  unit or document instead.
- **The editor's rulings on the plan (2026-11-27)**: `Cit[ationes]` (the doubled plural consonant written
  once), uncertain tilde forms keep the tilde, one spot sheet at the end, and the reading done **on the
  desktop from the original scans**, not from the site's 1,100-pixel copies. Every Latin holding records
  where its scans are: `RAW` in `intake/holding.py` or `raw_dir` in `unit.yml` (Oe 1 Bü 14526's are in
  Downloads, not on J:). The desktop procedure is the plan's section 9; the trigger phrase is in CLAUDE.md.

- **A document's language sits under `documents:` in `rulings.yml`, as `language: {"1": la}`.** Poznań
  Gr.1181 had a top-level `languages: {"1": latin}`, which nothing reads; the build fell back to German and
  the Latin decree showed as German until 2026-11-27. When counting by language, check the dataset's
  `language` against each holding's `languages:` in unit.yml (a script did it in a minute: only Gr.1181 was
  wrong).
- **The audit's cloud preparation** (2026-11-27): `pipeline/review/latin_audit.py` does every step
  (scope, manifest, tildes, refs, strips, apply, impact, sheet) and works for court books and the rest
  alike; `reference/latin_audit/` holds the manifest, the tilde list, the citing texts, the briefs and the
  Gr.1181 open rows. The strip cutter cuts eight bands per page whatever the entry's line count: a
  two-line entry on a full page gave one useless band when it went by lines.
- **Anchoring a change to a word that stands twice on a line**: take the occurrence by its position
  (`word` in `tildes.json`), never the first match on the line. The first build of the expansion rows
  anchored two different `Calissien~` of one line on the first, and gave the same anchor two different
  endings; a duplicate check caught it. Anchor on neighbouring words that will not change (no tilde), and
  test the rows in order on a copy of the text before writing (`latin_audit.py apply` without `--write`).
- **Two independent readings for expansions work**: the guide's draft and a blind Sonnet reader given
  only the sentence agreed with certainty on 435 of 837 forms; of the rest, most were marked unsure by one
  side, and only three were real disagreements of case. Agreement must compare the whole word: comparing
  only the last bracketed gap failed every form with a gap inside (`Cit[at]os`).
- **The doubled-consonant rule must match the same letter in the same case**: `Ssmae~` (Sanctissimae) is
  S with a superscript s, not a doubled consonant; a case-blind test dropped the capital.
- **The editor's ruling on contractions (2026-11-27): each gap bracketed** (`v[e]n[ien]tis`). The
  bracketing script matches the clerk's letters into the word left to right; where that gives three or
  more gaps it takes the match from the end if it has fewer (`Condsnis~`: `Cond[escen]s[io]nis`, not
  `Cond[e]s[ce]n[s]i[oni]s`). Two gaps are left as matched left to right, so that a gap stands where the
  tilde is (`v[e]n[ien]tis`, the form the editor approved).

## The Latin audit begun on the desktop (2026-11-27)

- **The pilot, Konin Gr.115** (9 scans, 11 entries): two Sonnet led readers (half the pages each) used
  about 155-180k tokens and 1.5-2.5 minutes each; the blind reader 110k. Their yield: 43 findings, of
  which 5 corrections and 2 questions survived Claude's look at the bands. Most led-reader findings were
  "unsure" readings of abbreviation strokes, the old convention (below) or the Polish's modern spelling.
- **`regenerate.py --unit` stops at the pipeline self-check** (`check_pipeline.py`, 30 problems already
  on `main`: records keyed on letter_id in the date_order scripts, holdings named in set_*_titles.py and
  write_prepared.py). Run the steps by hand, as for Pyzdry Gr.75: resolve_linebreaks, resolve_paragraphs,
  build_db (each `--unit <slug>`), then merge_corpus, build_dataset, check_mentions_join,
  connections_site, build_site_data, person_pages --quiet, search_indexes. An in-line correction moves no
  line, so match_scans is not needed. `build_site_data.py` again rewrote four unrelated
  `site/_holdings/*.md`: check them out before committing.
- **`verify_site.py` fails on the desktop** on `site/genealogy/node_modules/fdir/README.md` (a link that
  bypasses relative_url): the folder is git-ignored and exists only on this PC, so CI does not see it.
  Read past that one failure.
- **The led reader reports the old silent expansions** ("Pro Pte" given as "Pro Parte", "M. R. G." as
  "Ministerialis Regni Generalis"): the court books were transcribed by the rule "Latin is given as
  written, with abbreviations filled out", before the bracket rule of 2026-11-22. The audit leaves them
  (the brief now says not to report them; `review/latin_audit/brief_a.md`) and asks the editor once, on
  the spot sheet, whether they are to be bracketed throughout.
- **The blind reader needs the right band, and its neighbours.** On Gr.115 it answered 13 of 16 items
  "unsure", read one item from the next entry down, and could not answer two whose words lay in the
  band above or below the one named. Name the band and its neighbours, and quote the line's first words
  so it can find the entry. Its "unsure" adds nothing: Claude settles on the band.
- **The Polish inside a Latin entry is partly modern** (leaf 186 verso of Gr.115): a reader's *y* for
  *i* there is not a correction (EDITORIAL_RULES, "Modern spelling beside the scribe's spelling").
- **A prepared expansion can be wrong in its letters, not its sense**: *praesen~* on leaf 242 is
  "pn~ti" on the page; *Castren~ Bidgosten~* on leaf 37 is "Castr~ Bydgost~". The cloud's expansions
  bracket the transcription's letters, so a reader's look at the page comes before applying them.
- `latin_audit.py` gained `texts` (each page's text, numbered, for the briefs) and `crop` (a tight cut
  into `review/latin_audit/crops/`, the sheet's folder).
- **The blind reader works when given three bands and the words on either side** (the second and third
  batches, 2026-11-27): briefed with the band, its neighbours and "between the words X and Y", it read 8
  of 11 items "likely" and found every place; given one band and a vague place it had read 13 of 16
  "unsure". Make its items with `nb(page, n)` and the guide words from `pages/<page>.txt`
  (`review/latin_audit/batch3_items_b.json` is the pattern).
- **Two readers agreeing can both be wrong at a line end.** On Konin Gr.121 both read "ho-" + the next
  line as "ho nunc"; the band shows "ho-/rumce", and the transcription's "horumce" stood. Claude's look
  at the band also found what neither reported (the clerk's "Extradionis" without -ti-). Settle on the
  band, never on the readers' agreement alone.
- **A led reader's "doubt_settled" is not a settlement**: it was shown the doubtful reading and agrees
  with it. Lift a mark of doubt only when the blind reader gives the same letters and Claude sees them
  (the Ląd copy-book: 5 of 13 lifted, the other 8 kept, where the blind reader read otherwise).
- **The doubled-consonant rule is for plurals only**: a prepared expansion "Actt~" → "Act[oris]"
  (Konin Gr.120, one plaintiff) was not applied; it would drop a letter the clerk wrote.
- **Saving the main session's tokens on images**: the copy-book's text fills the left half of its pages,
  so the left halves of three bands stacked into one image (PIL, `review/latin_audit/crops/`) settled
  three readings in one look.
- **A reader's English consequence waits**: a correction that moves the sense (Gr.121, "praesentatos"
  to "presenttes") is noted in the holding's changes and notes, and the English is changed in the impact
  sweep after the editor's review (plan, section 5), not at once.
- **A large holding's blind reading is made by script** (Poznań Gr.1181, 2026-11-27): the led readers'
  sure/likely findings (247) became blind items automatically, the transcription's three words before
  and after each place as guides (marks of doubt stripped), the named band and its neighbours, grouped by
  page so each reader opens few pages (`review/latin_audit/app5320pozgr1181/items_b_*.json`). A comparison
  script (fuzzy word match, `scratchpad/compare_ab.py`, now `pipeline/review/latin_audit_compare.py <slug>`) sorted
  the 234 pairs into agree / differ / the blind reader unsure / with the transcription. Claude then read
  the agreements as a list and dropped those that only looked alike (7 of 82). Thirteen findings could
  not be located by their quoted words (the led reader quoted across a line join).
- **A led reader's band number can be wrong**: for the skipped clause on Gr.1181 leaf 161 the named band
  holds another passage. An omission the blind reader did not confirm goes to the sheet with the band
  and its neighbours, never into the text.
- **A reader holds about four pages of bands, no more** (the lighter pass, 2026-11-27). Of nine readers given
  9 to 13 pages each, seven came back short: two read only the whole-page pictures and called it done,
  others lost images to "media removed: request limit" part-way, one stopped after two pages. Readers
  given three or four pages opened every band and reported cleanly. Give a reader at most four pages
  (about 36 images), say in the brief that a pass from the whole-page picture is not acceptable, and tell
  it to retry a failed image and list what still failed. Many readers running at once may also share the
  limit: start the reruns once the first wave is in.
- **For the short entries of a register a reader may open only the bands that hold the entry** (Konin
  Gr.118: 26 of 96 bands, the rest blank paper or other entries), provided it says which it skipped and why.
