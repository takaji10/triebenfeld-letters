# Taking a new holding through the pipeline

The order of operations, and the reasons the order is what it is. Written after
Oe 1 Bü 14526 went through it, at the cost of one avoidable re-run; sections 3a and 3b and
mistakes 11-15 were added after 9454's new transcription was corrected and read (September 2026).

Every stage takes `--unit <slug>` and means it. Nothing here is automatic:
several of these steps cost money, and a run that sweeps every holding because a
flag was forgotten is worse than one that stops.

---

## Before anything

```
python new_unit.py --ref "Oe 1 Bü 14526"
```

Writes `units/<slug>/` with `unit.yml`, an empty `corpus.txt`, `rulings.yml` and
`notes.md`. Fill in `unit.yml` — where the scans are, how the files are named,
and the three fields the machine cannot infer:

- **`description`** — what this holding actually is, in a paragraph. It opens
  the translator's and the summariser's prompts. "Not correspondence but title
  deeds" is doing real work there. The reader no longer sees it: what the
  reader gets is the holding's own page (below).
- **`date_span`**, **`ref`** — the archival identity.
- **`title`** and **`title_de`** — one sentence saying what the holding is
  about, in English and German. It is the line under the reference on the
  Sources page. Not the file's own heading with a gloss ("Acta betr: ... - the
  ministry's file on ..."): the editor found that unhelpful (2026-10-01). The
  archive's own title can be kept as `archive_title`, which nothing displays.
- **`about.md`** and **`process.md`**, beside `unit.yml` — the two texts of the
  holding's own page (`/sources/<slug>/`): a full description, and a short
  account of how the holding was prepared. Write them last, once the documents
  are read and summarised. Length follows the holding: a few paragraphs for a
  single deed, several thousand words for a long correspondence. Cite the
  documents a statement rests on as `[[41]]` or `[[41, 44]]`; name another
  holding as `[[unit:<slug>]]`; end a paragraph that states nothing from a
  document with `<!-- context -->`. `check_unit_text.py` (run by
  `regenerate.py`) fails on a year or a sum the cited documents do not have.
  `about_de.md` and `process_de.md` are used on the German page where they
  exist; until then it shows the English and says so. A relation note or a
  date basis written in `rulings.yml` is English; its German goes in
  `reference/site_notes_de.yml`, keyed by the English text. Rules for the prose are
  in `HOUSE_STYLE.md`.
- **`translation_note`** — facts about the source that change how it must be
  read, not instructions about style. Latin tags that belong to the legal
  register; passages in another language that are source text rather than
  corruption; names that look like foreign text and are not. This is the field
  that stops the translator treating a Polish signature formula as broken
  German.

None of this belongs in code. `pipeline/check_pipeline.py` enforces that.

### If this replaces an existing transcription

A new reading of a holding that is already built (9454 received one in September
2026) is not a fresh intake. The hand-made layer on top of the old text does not
travel with it by itself:
- `correspondents.json`;
- the `rulings.yml` dates, place overrides, languages, twins and estates;
- the scan decisions.

On 9454 the swap silently cost 214 letters their sender and recipient, 44 dates
and 77 places, and nothing failed: the site built and verified clean.

- **Before importing,** move the old unit into `Trash/<slug>_old/` whole: corpus,
  rulings, correspondents, decisions, and its built `corpus/documents`.
- **After the first build,** compare the old and new outputs letter by letter:
  - date;
  - place of writing;
  - sender and recipient;
  - language;
  - twins.

  Then restore each ruling that still applies. Where the new text now reads a
  date or place differently, put the disagreement to the editor. Don't pick one
  silently.
- **Treat the old transcription's corrections as candidates, not decisions.**
  Several of its "fixes" were wrong, and the new reading showed it.
- Letters the archive no longer holds get a placeholder document whose text is
  `(missing)`, so their numbers still resolve.

## 1. Intake

```
python pipeline/intake/crop_scans.py    --unit <slug>
python pipeline/intake/split_spreads.py --unit <slug>
python pipeline/intake/stage_pages.py   --unit <slug>
python pipeline/intake/import_pages.py  --unit <slug>
```

If the transcriptions arrive already matched to their scans — one file per page
— say so in `unit.yml` under `transcriptions:` and let `import_pages.py` write
`corpus.txt` with a `[PAGE <id>]` before each page. **Declared pairing is worth
a great deal**: 14526 paired 287 of 288 pages with no review at all, against 865
done by hand for the holding that had to be reconstructed.

### A file the office wrote on

How to read such a file (registry marks, paraphs, who signs what) is in
`docs/GOVERNMENT_FILES.md`. Read it before the first correction pass.

A ministry file (III. HA MdA, III Nr. 12765 was the first) keeps incoming
letters with the office's own writing on them, photographed as openings:

- **One page per written side.** `review_folds.py` lets the editor place the
  fold on every opening; a side with no writing is moved out of `processed/`
  before staging. Transcriptions arrive one per scan, so they are cut into one
  file per side, and the record of which source line went where is kept as a
  script in `units/<slug>/intake/`.
- **A reply drafted on a petitioner's page is its own document**, starting
  partway down that page (`first_line` in the boundaries sheet).
- **Shorter marks by the receiving office** go to the end of that document's
  part of the page and are listed in `units/<slug>/office_notes.yml`, the same
  shape as `sideways.yml`. The site sets them apart under a label.
- **Pages transcribed by paragraph** are listed in `rulings.yml` under
  `pages: by_paragraph:`. Every line then begins a paragraph, and the page
  says how it was transcribed.

## 2. Build, and read what it says

```
python regenerate.py --unit <slug>
```

Runs the self-check, then line-break decisions, the database, and the scan
mapping. Read `review/<slug>/scan_review.html` and settle the pairings before
going further: everything downstream is keyed to pages.

Set `status: transcribed` in `unit.yml` when the transcription is fit to build
from. It is documentation, not a gate.

## 3. Rulings

`units/<slug>/rulings.yml` carries what the editor has decided about this
holding: `doc_type` per document, dates the parser could not reach and where
they came from, place overrides, document languages, relations between
documents, duplicates, damage. See `docs/DATA_MODEL.md` for the fields and
`docs/EDITORIAL_RULES.md` for the bars.

One field is worth stating plainly: **`dates.read` is not `dates.supplied`.** A
date read off the dateline by the editor is evidence from the document; a date a
researcher assigned is not. Filing thirty of the first as the second told the
reader the opposite of the truth.

**`doc_type` is not decoration, and its default is wrong for anything but a
letter file.** A document absent from `doc_type` is `letter`, and `summarise.py`
tests that value: anything other than `letter` or `document` spanning more than
one page is told "this is not a letter, the pages that follow are one package,
summarise the package." Leave a volume of deeds at the default and every
multi-page instrument in it is summarised as though the first enclosure were the
whole record. 14525 reached the summariser with 42 of its 44 documents still
defaulting to `letter`. Classify them all, and reuse the vocabulary a sibling
holding already established rather than inventing terms — nothing validates this
field, so a typo silently becomes a generic "Document" label on the site and is
handed to the model verbatim in the prompt.

Editing `rulings.yml` makes `corpus/letters.json` stale, and
`require_fresh_corpus()` will stop the next paid step until you rebuild. Run
`regenerate.py --unit <slug>` after this section, not after discovering it.

**Correspondents** come from `derive_correspondents.py`. Run it once, then settle
the letters with only a sender or only a recipient from context (signature,
salutation, hand, business), writing each ruling with its reason into
`correspondents.json`. **Do not run the script again after that:** it overwrites
the file, rulings included.

## 3a. Correct the transcription — free passes, before anything is paid for

An AI Kurrent reading, even one hand-corrected for names and layout, still
carries thousands of small slips. Every one left in is translated, summarised
and indexed. 9454 went through these passes in roughly this order; each is
logged in its `notes.md`.

**The standard for every correction.** A reading is changed only when something
proves it:
- a fixed formula;
- the same word written correctly elsewhere in the same letter;
- a form attested across the units, with the count checked;
- a copy of the letter;
- a sentence with exactly one grammatical reading;
- an edition form already settled.

Never change a word because another would make better sense: every error the
editor caught on 9454 was of that kind. Leave alone:
- his grammar (case endings, dropped endings);
- period spelling and doubled letters;
- figures, dates, and the editor's own `[..]` expansions.

Don't correct inside a largely garbled passage. A corrupt word with no reading
that meets the standard stays as it is and is logged in
`review/<slug>/unresolved.md`. No `[?]` is added.

1. **Recurring misreadings.** Count a pattern across the unit first; the editor
   approves it once (Ewr before Durchlaucht, Jezt, Schicken Sie, Indes, Summa).
2. **Nonwords.** `pipeline/review/spelling_audit.py`: a rare form one Kurrent
   confusion away from a common one, and unknown to DWDS
   (`reference/dwds_cache.json`).
3. **Line ends.** A word broken at the line end is `¬`; a real hyphen stays `-`.
   Check every `¬` whose halves don't join to a known word, and every `-` that
   breaks a word.
4. **Dashes.** A punctuation dash is `—`. A hyphen stays only in compounds and on
   paired words (`Kriegs- und Forst Rath`); figure ranges stay as written.
5. **Names, titles, places.** Standardise misreadings to the settled forms in
   `people.yml` / `places.yml`:
   - Titles take the writer's commonest spelling.
   - A one-letter name variant with no settled form stays: it may be the
     writer's own.
   - Places: German text keeps the German name, Polish text the Polish.
   - Keep a watch-list of names the transcriber habitually misreads.
   - Count the index hits before and after any authority change (mistake 7).
6. **Abbreviations.** Expand in brackets only where the letters or the period
   settle them: title abbreviations, forms of address (`E[wr]. D[urchlaucht].`),
   single-letter initials. `p`/`pp`/`ppp` and `rt` stay.
7. **Doubt marks.** Decide `[?]` words from context where the evidence is solid;
   the rest stay. A settled letter drops its brackets; brackets stay only on
   expansions.
8. **Letters too garbled to correct** get `rough: letters:` in `rulings.yml`. The
   site then marks them "Rough transcription". Asking a model to re-read them
   from the scan was tested and rejected: 72% of words right against 89% for the
   editor's recognition model.

**Tools:**
- `pipeline/review/show_letter.py` prints a letter with corpus and letter line
  numbers.
- `pipeline/review/fix_sheet.py` turns rulings (corpus line, old, new, reason)
  into the sheet that `apply_transcription_fixes.py --apply` applies and logs.

Text added to a unit later goes through the same passes. See
`units/oe1bu9454/new_text_checklist.md` for the order.

## 3b. Read every document whole — paid, before translating

```
python pipeline/review/read_letters.py --unit <slug> --dry-run        # free: prompt and token count
python pipeline/review/read_letters.py --unit <slug> --letters a,b,…  # pilot, live
python pipeline/review/read_letters.py --unit <slug> --batch          # then --collect
python pipeline/review/read_letters.py --unit <slug> --verify --batch # the claim check, then --collect
python pipeline/review/read_letters.py --unit <slug> --check          # free local filters
```

Each document is read with the one before and after it in date order. The model:
- proposes corrections, each with a witness;
- writes a German summary, citing the lines for every statement;
- records reading notes, legibility and suspected misreadings.

A second, separate call checks every statement against the document. It may
only cut or weaken, never add. On 9454 it changed 132 of 313 summaries:
- hearsay stated as fact;
- a sum attached to the wrong item;
- a plan written up as done;
- a garbled word interpreted.

- **Proposed corrections** pass a machine filter, and then a human read of each
  line. 180 of 250 were applied on 9454.
- **The reading record** goes into `units/<slug>/reading.json`, which is tracked:
  the cache is gitignored and the reading is expensive. `build_dataset.py`
  carries it into each document.
- **Summaries** go into `units/<slug>/summaries_de.yml`, and are published
  through `summarise.py --build --lang de`.
- **English summaries:** when the English exists, translate the checked German
  summaries rather than summarising the English afresh.

Do this before translating. The translation then starts from corrected German,
and the reading notes and doubtful words can go to the translator.

Cost on 9454: about $30 for 313 letters. Two lessons from that run:
- **Re-estimate from the pilot, not the dry run.** The model wrote about 2,500
  output tokens per letter against the 1,500 assumed.
- **Budget the claim check** at about a third of the reading on top.

## 4. Translate — and expect to do it twice

**First, a pilot, if this holding is a new kind of source.** Name ten documents
in `unit.yml` under `translation_pilot:` and run them alone:

```
python pipeline/translate/translate.py --unit <slug> --pilot
python pipeline/translate/check_translations.py --unit <slug>
```

About a dollar, and it is the cheapest place to find out that the termbase does
not fit. 14526's entire second pass was register: an *Ausfertigung* came back as
an engrossment, a *woźny* as a bailiff, a Polish court formula as broken German.
Every one of those would have shown in ten documents, and each was instead found
after paying for thirty-two. A new *kind* of source — deeds after letters,
court records after deeds — earns a pilot. A second letter file does not.

Then the volume:

```
python pipeline/translate/translate.py --unit <slug> --dry-run   # spend nothing
python pipeline/translate/translate.py --unit <slug> --all --batch
python pipeline/translate/translate.py --unit <slug> --collect
```

The Batch API is half price and worth the wait. The collector refuses any result
whose segment count does not match the manuscript page count, so a truncated
tool call is never cached as though it were a finished translation.

**Two guards now stand in front of anything that spends money**, and both exist
because the thing they guard against happened:

- `unitlib.require_fresh_corpus()` refuses to run when a `corpus.txt` or a
  `rulings.yml` is newer than the `corpus/letters.json` built from it. The tools
  read the generated file; corrections are made in the authored one. Letter 73
  was translated twice from a reading the editor had already overturned, and
  nothing objected either time. **Always `regenerate.py` between applying
  corrections and translating.**
- Each cached translation carries a `source_hash` of the exact German it was made
  from. See step 5.

### `--tag` is part of the command, not an afterthought

Every generation of translations lives in `cache/translation-raw-<tag>/`, and a
run without `--tag` reads and writes the untagged directory. It will report
`already done, skipping` — a clean success, against the wrong generation. Pass
the current tag to `translate.py`, `check_translations.py`, `summarise.py` and
`publish_translations.py` alike, and to `--collect` as well as to the submission.

## 5. Harvest the corrections — **before publishing**

This is the step whose absence cost a re-run.

```
python pipeline/translate/check_translations.py --unit <slug>
python pipeline/review/transcription_fixes.py  --unit <slug>
python pipeline/review/unmarked_doubts.py      --unit <slug>
```

Translating a document is the most thorough reading its transcription ever gets.
The translator reports every place it could not make sense of, and on 14526 that
was 478 proposed corrections — of which 278 were applied. Acting on them changes
`corpus.txt`, which invalidates the English that produced them.

So: rule on the sheets (`docs/EDITORIAL_RULES.md`), apply them —

```
python pipeline/review/apply_transcription_fixes.py --unit <slug> --apply
python pipeline/review/section_numbering.py         --unit <slug> --apply
python regenerate.py --unit <slug>
```

— and only then re-translate the documents whose German actually changed. **Do
not work that list out by hand.** Ask:

```
python pipeline/translate/translate.py --unit <slug> --tag <tag> --stale
```

It compares each cached translation's `source_hash` against the German now in the
corpus and prints the `--letters` argument to pass. A hand-kept list is wrong in
both directions: it re-runs documents whose German never moved, and it misses
documents whose German did. Both have happened here, the second while a batch was
in flight — so the result arrived already superseded, and looked finished.

```
python pipeline/translate/translate.py --unit <slug> --tag <tag> --letters 1,2,5,... --batch
```

Re-running only the changed documents is the whole economy of this step. On
14526 that was 29 of 32 for about $3.50, against roughly $7 for the volume.

### The other kind of staleness

`--stale` catches a translation whose **German** changed. A ruling can instead
change the **authorities** and leave the German untouched: the editor settles that
Szettleich is Szetlewek, and every page already translated is wrong without a
character of the transcription moving. Nothing else in the pipeline can see that.

```
python pipeline/review/uncanonical_names.py
```

Costs nothing, reads the published English against every renaming the authorities
assert, and reports the document and the sentence. Run it after any ruling on a
name, and again before publishing. It found eight documents in a corpus that had
already passed every other check.

## 6. Publish, summarise, build

```
python pipeline/translate/publish_translations.py --unit <slug> --tag <tag>
python pipeline/build/relabel_scans.py            --unit <slug> --apply
python pipeline/build/make_scan_derivatives.py
python regenerate.py --unit <slug>                # twice - see below
python pipeline/translate/summarise.py --unit <slug> --batch     # then --collect
python pipeline/translate/summarise.py --unit <slug> --lang de --batch
python regenerate.py --site
```

Summaries are written from the English, so they follow it: if the translation
was re-run, the affected summaries must be too. A unit read whole in 3b already has checked German summaries: skip the `--lang de` run for it and translate those into English instead. `summaries.yml` is one file for
the whole project and the build refuses to write a smaller one than it found —
a unit-scoped walk once quietly replaced 345 summaries with 32.

**Record the tag you published from, in `unit.yml` as `published_tag`.** Nothing
else in the pipeline remembers it, and every tool defaults to the untagged
cache. 14526 was published from `--tag v2`; months later a check run without the
tag read the abandoned untagged generation, reported 80 ruled-against renderings
and 23 of 30 documents blocked, and all of it described text no reader has ever
seen. The published English was clean. An hour went into investigating a defect
that did not exist, and the repair being prepared would have overwritten the
good text with the worse generation.

### The images are a separate publication, and they are not automatic

`regenerate.py` never renames a scan and never makes a web copy. Both are
deliberate acts, and a holding that skips them reaches the site with every image
link broken.

- **`relabel_scans.py --apply` first**, then derivatives. The label after the
  hyphen is derived from the mapping, so relabelling renames the originals and
  prunes any derivative whose name has changed — without recreating it. Make
  the derivatives first and you have simply thrown them away.
- **`make_scan_derivatives.py` takes no `--unit`.** It walks all of `pages/` and
  skips whatever is already current, so it is safe, and the count it reports
  ("209 made, 1160 already current") is the check that it touched only the new
  holding.
- **Then rebuild twice.** `PER_UNIT` runs `build_db.py` *before* `match_scans.py`,
  so `build_db` writes each page's `scan` field from the mapping as it stood at
  the start of the run. After a relabel the first rebuild therefore bakes in the
  old filenames and `verify_site.py` fails on every image — 165 broken links on
  14525. The second pass reads the mapping the first pass rewrote and comes out
  clean. This is worth knowing rather than fixing blind: the order is load
  bearing elsewhere.

## 7. Verify

`verify_site.py` runs inside `regenerate.py --site` and fails on a one-character
difference, a missing document, a dead internal link, or any external fetch.

Check by hand, once, that the new holding did not disturb the old one: rebuild
and diff the other unit's `corpus.txt` against its committed state. The expected
answer is *no differences*, or differences you can name exactly.

---

## 8. What the holding owes the rest of the site

A holding is not finished when its documents are up. Each of these is a
hand-written file that nothing regenerates, so a new holding silently lacks it
until someone writes it. Do them in the same sitting, English and German
together (the editor reads no German; the German is written here, free).

| What the reader sees | File | Note |
|---|---|---|
| The holding's page: description and how it was prepared | `units/<slug>/about.md`, `process.md`, and `about_de.md`, `process_de.md` | Finding-aid form, see `HOUSE_STYLE.md`. `check_unit_text.py` holds figures to the cited documents. |
| The one sentence on the Sources page | `title`, `title_de` in `unit.yml` | |
| People page: who each person is, and when they lived | `reference/people_bios.yml` | One entry per new person. Dates only for an identified historical figure, checked against a reference work; everyone else shows "documented <years>", which the build works out. |
| Places page: the map link | `reference/places_osm.yml` | Keyed by the printed name. Only where the identification is firm. |
| Glossary: the definitions in the documents and on the glossary page | `reference/glossary.yml` | Run `python pipeline/review/glossary_candidates.py --unit <slug>`: it lists the holding's words that may qualify and that no entry covers or `excluded:` rules out. Rule on each: an entry in English and German (each with `check_against`; Gloger's *Encyklopedia staropolska* for Polish terms), or a line under `excluded:` with the reason. Then rebuild and read the holding's rows in `review/glossary_matches.csv` for false hits, including those of existing entries. See `docs/GLOSSARY_PLAN.md`. |
| German for a date note or a relation note | `reference/site_notes_de.yml` | Keyed by the English note exactly as it stands in `rulings.yml`. A note with no entry shows in English on the German view. |
| Timeline | `site/_data/timeline.yml` | Add the events the holding documents that bear on the estate's owner, with `refs:` to the documents and the `_de` fields. Extend the year range in `site/_includes/timeline.html` if the holding runs past it. |
| The era essay and the edition guide | `site/hohenlohe.md`, `site/reading-this-edition.md` and their `site/de/` counterparts | They name holdings and give counts by hand. Nothing checks them against the data, or the German against the English. |

## The mistakes this order exists to prevent

1. **A holding's facts written into code.** The translator's prompt described
   one estate agent's correspondence whatever it was pointed at. Facts belong in
   `unit.yml`; `check_pipeline.py` fails the build if they come back.
2. **The archive's document number used as an address.** It is unique only
   inside its holding, and both units have a document 2. Records are keyed by
   `pad`, through `unitlib.records_by_pad()`, and nothing else.
3. **A structural failure discovered several stages late.** Three deed packages
   hit the output ceiling and cached empty after being paid for; nobody noticed
   until a crash four stages on. Assert the invariant where the damage happens.
4. **Publishing before harvesting the corrections.** Cheap to avoid, and it is
   the difference between translating a holding once and translating it twice.
5. **Paying for text the editor has already overturned.** Fixed by
   `require_fresh_corpus()` and by `--stale`. Both replace a thing that was being
   remembered with a thing that is computed, which is the only version that stays
   true.
6. **A ruling written down in one place when it applies in two.** Every style
   ruling used to be restated inside each prompt, and the second copy drifted:
   banned for the translator, reached the summaries anyway. Both tools now read
   `reference/translation_glossary.yml`, so a row added once holds in both. A new
   ruling goes in the termbase or in `docs/HOUSE_STYLE.md` — never only in a
   prompt. The table at the end of HOUSE_STYLE says which.
7. **A pattern added to an authority without counting what it hits.** A feast-day
   reading of `Michaelis` was added, and it was the merchant Michaelis 30 times
   out of 38. Folding variants into a match pattern quietly undid the negative
   lookaheads that kept `Hon` from matching Honrichs, and took one man from 43
   documents to 48. Count the documents a new pattern touches, and read a sample
   line from each, **before** anything is translated against it.

8. **A placeholder reaching a paid prompt.** `unit.yml`'s `description` and
   `translation_note` are read by `unit_preamble()` and open the prompt for both
   the translator and the summariser. 14525 was translated in full, 44
   documents, with the literal string "TODO: a sentence for the reader." sitting
   in every request. The title carried enough that the output survived it, which
   is the worst version of this: it cost money and left no mark. Fill the fields
   before the first paid run; `check_pipeline.py` now refuses a build that finds
   a placeholder in one.
9. **Checking a change against whatever happens to be on disk.** Before altering
   shared checking code, take the "before" by running the *pristine* version —
   `git show HEAD:<file>` into a sibling path, so its `ROOT` still resolves —
   and diff that against the new output. The review sheets lying in `review/`
   may be months old and built by different code; comparing against them
   produces a diff full of rows that no edit caused, and hides the ones it did.
   Assert explicitly that no row disappeared from a category the change did not
   touch, and that no document left the blocked list.
10. **Counting occurrences in a data file by grepping its bytes.** A YAML block
   scalar folds and re-indents the text it holds, so `grep -c` over
   `site/_data/translations/*.yml` answers a question about the file's bytes and
   not about the edition. Parse it and walk the segments. Grepping bytes
   reported 27 ruled-against renderings in a published holding; parsing the same
   files reported none, which was the truth.

11. **Asking the editor to judge what they cannot see.** The editor reads Kurrent
   letter shapes on a scan but does not read German. Accuracy of anything drawn
   from the German (summaries, translations, readings made from sense) rests on
   the checks and on us. When the editor's view is needed, put it on a short spot
   sheet (`pipeline/review/queries.py --sheet`): a word against the scan, or an
   English rendering to judge for focus. Never a long queue: decide what the
   rules decide, and record why.
12. **A correction made from sense.** See the standard in 3a. Each of the three
   misses the editor caught on 9454 was a plausible word chosen because it fit.
   A spelling that varies within one letter is not proof of a misreading either:
   the editor kept Kiełszewski beside Kiełczewski.
13. **Place names in the wrong language.**
   - The transcription keeps what the page says: German names in German text,
     Polish in Polish.
   - The site labels every place now in Poland "Polish (German)": the `display`
     and `german` fields in `places.yml`.
   - The English translation uses the Polish name.

   One pass that put Polish names into the German text had to be reversed.
14. **Trusting a model's defaults.** Opus 5.5 refuses a forced `tool_choice`: ask
   for the tool in the prompt and retry a result without it. Batch timestamps
   are UTC. An API outage leaves batches running, and their results stay
   collectable for 29 days.
15. **Paying for a check the build already makes.** Figures in a summary are
   compared with the document for free, including figures written out in words.
   Only claims about meaning need the paid check.

### State files

Any file the pipeline keeps between runs is keyed by `pad`, never by the archive's
own document number, and never flat across holdings. `_batches.json` was written
flat twice — once in `translate.py`, once in `summarise.py` — and each time the
second holding's submission erased the first holding's batch IDs, which had to be
recovered from the API. Mistake 2 is about records; this is the same mistake about
state.
