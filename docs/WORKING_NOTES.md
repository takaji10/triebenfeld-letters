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
  copy of its rows is `docs/PRUSIMSKI_before_publishing.csv`, and the
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
  question is written into `docs/PRUSIMSKI_QUESTIONS.md` with the default
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
  `regenerate.py --unit`, a diff of the letter's front matter against HEAD
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
  `corpus/index/uncertainties.json` is the number the essays give. Recount
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
  byte as before: compare `render_table` against `git show HEAD:unitlib.py`
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
  place the picture by the line's place in `transcriptions/<page>.txt`
  (716's `intake/spot_sheet.py`). Where the page has two columns or a
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
- **Run `check_translations.py` after `regenerate.py`, not before.** Run on
  the old `corpus/letters.json`, it reported five false marker-count rows
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
  take it out: `git checkout` the generated files (corpus/, site/_data/
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
  verifications (build_site_data's and `verify_site.py`, `FN_MARKUP`) strip
  that markup before comparing the text. A mark with no note, or a note
  with no mark, goes under `unmatched:` with the reason. The holding's
  `intake/check_footnotes.py` checks every mark and note is found once.
- **The figures of a medieval holding are years** (2026-10-16). The
  reading text and the English group four-digit numbers by thousands
  unless they can be a year, which `numerals.py` took to mean 1500 to 1999:
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
- **A new holding needs `regenerate.py --unit <slug>` twice after
  `relabel_scans.py --apply`**: its database step runs before the scan step
  refreshes `page_scan_map.csv`, so the first run keeps the unlabelled image
  names and `verify_site.py` fails on broken `/assets/scans/` links. Make
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
  in the repository**: a fresh checkout has none, and `regenerate.py --site`
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
  `regenerate.py --site` (a literature index with hits not yet ruled, a
  file locked while it rebuilds): run `build_site_data.py`, the Jekyll
  build and `verify_site.py` directly, and leave the generated files that
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
- **Then rebuild each holding the branch touched** (`regenerate.py --unit
  <slug>`), the site once, and read `git status` for files of any other
  holding.
- `relabel_scans.py` reports three labels to update in Oe 1 Bü 14526
  (scans 0167 to 0169, from the merging of documents 30 to 32). It has said
  so since that merge, the site checks pass with it, and it was left alone.

## Traps in this shell (2026-10-13)

- A heredoc in the Bash tool fails on an unbalanced apostrophe even when it
  is quoted. Write any script that holds prose with the Write tool and run
  the file.
- A heredoc also eats backslashes and turns "\'" into "'" (2026-10-16):
  a Python patch with regular expressions or escaped quotes, sent through
  a heredoc, half-applied twice in one sitting. Use the Edit tool for such
  changes, or Write the script whole.
- **`regenerate.py` has no `--help`**: it ignores unknown arguments and
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
  primary source for it). A search of `corpus/documents/*.json` for the year or the
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
- **A changed line of transcription** is changed in `corpus.txt`, in the page
  file under `transcriptions/`, in a row of `transcription_decisions.csv`, in
  `sideways.yml` or `office_notes.yml` if it is the first line of a block
  there, and in `intake/translation/doc<N>.yml` (with its `marker_count`).
  Then `write_cache.py <N>`, `check_translations.py`,
  `publish_translations.py`.
- **Summaries written again for a holding already published** (Oe 1 Bü 14525
  and 14526, 2026-10-08). Read each document whole in `corpus/text/<pad>.txt`
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

## Traps in the tools

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
- **OCR a page as the agreement of passes, not from one run.** The five
  passes over the clipping (two upscalings ×3/×4, psm 6 and 4, tessdata_best
  beside the standard model, Windows.Media.Ocr as a third witness) agreed on
  almost every word; each pass that disagreed was the one wrong. Tesseract's
  word confidences (`words()`) sort what goes to the spot sheet; Tesseract's
  TSV wants `-c tessedit_create_tsv=1` (the bare `tsv` config name prints
  plain text instead), and its output ends each line with \r. Small scans
  want upscaling: the clipping is 712×960 and only reads well at ×3 and ×4.
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
- **`build_literature.py` empties `corpus/literature/`, and
  `literature_index.py` writes `mentions.json` back into it** (2026-10-21).
  Run the literature's steps in order, build, index, site, before
  committing; `git add -u` after the build alone recorded `mentions.json`
  as deleted (commit adc3ad1a, put right in the next). Before any commit
  with `git add -u`, read `git status --short` for a `D`.
- **A saved web page can carry the editor's login** (the online Boniecki,
  2026-10-21: an e-mail address in its header). Keep such a page out of the
  repository, make the text from it with a script that takes only the
  part wanted, and say in the script why the page is not kept.
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
  after it (the order in regenerate.py too). After tagging a new estate,
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
  say otherwise; never quote stretches of the text (`verify_site.py` looks
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
- **`new_unit.py` makes `units/<digits>/`.** Rename it to `app<digits>`
  before writing anything into the new name, or two folders exist.

- **A Python script typed into the shell loses its backslashes**, even
  inside a quoted heredoc: `'\n\n'` arrives as a line break and the file
  being patched is left broken. Write the script to a file with the Write
  tool and run that. (Happened three times on 2026-10-06.)

- **One very long document** (31,000 words) broke the merge: Python's CSV
  reader refuses a field over 131,072 characters. `unitlib.py` now raises
  the limit for every script that imports it; a script that reads
  `letters.csv` without importing `unitlib` must raise it itself.
- **A new holding's folder is named `app<digits>` for Poznań** like the
  others; `new_unit.py` does not add the prefix. Rename the folder and set
  `slug` before anything is built. `review/<slug>/` must exist before the
  first `regenerate.py --unit`.
- **`python regenerate.py --help` prints no help.** It runs the whole pipeline
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
    `verify_site.py`) and the 9135 generated files were hashed before and
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
  (`corpus/documents/<uid>.json`, `mentions` and `place_mentions`) and shut
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
  `numerals.py` took only 1500-1899 as years, and the edition had reached
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
  regenerate.py's MERGED order, because it reads the generated
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
  folders mid-run; the shared generated files (`corpus/literature/
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
