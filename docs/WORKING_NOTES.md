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
- **The translation check forbids "castle court" in an English
  translation**: sąd grodzki is "municipal court" there, as in the
  editor's English. The edition's own prose (holding pages, summaries)
  says "castle court". Keep the two apart.
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
- **The page of changes is the editor's working copy.** They read it once
  and work from it afterwards. Whatever is added later carries `new:` in the
  holding's `changes.yml` and is marked on the page; an entry that no longer
  holds ("not checked") is taken out, and the new entry says so.

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
- **After publishing English, read the holding's glossary matches.** English
  "entails" and "cession" drew false glossary marks and were reworded. The
  checker forbids "hypothec" in English, Latin "sub hypotheca" included.

## Traps in the tools

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

- **A rule in `reference/english_forms.yml` with `\b` in double quotes
  needs two backslashes** (`"\\bGorski\\b"`): YAML reads `"\b"` as a
  backspace and the rule then matches nothing, silently. Run
  `english_forms.py` without `--apply` and see that it would change
  something.
- **`rest.sh`-style scripts with `set -e` stop at the first `grep` that
  finds nothing.** Do not use `set -e` where the steps are filtered through
  `grep`.

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
