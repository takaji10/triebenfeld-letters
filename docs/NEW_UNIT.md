# Taking a new holding through the pipeline

The order of operations, and the reasons the order is what it is. Written after
Oe 1 Bü 14526 went through it, at the cost of one avoidable re-run.

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

- **`description`** — what this holding actually is. It reaches the reader, and
  it reaches the translator and the summariser as the opening of their prompts.
  "Not correspondence but title deeds" is doing real work there.
- **`date_span`**, **`title`**, **`ref`** — the archival identity.
- **`translation_note`** — facts about the source that change how it must be
  read, not instructions about style. Latin tags that belong to the legal
  register; passages in another language that are source text rather than
  corruption; names that look like foreign text and are not. This is the field
  that stops the translator treating a Polish signature formula as broken
  German.

None of this belongs in code. `pipeline/check_pipeline.py` enforces that.

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
python pipeline/translate/publish_translations.py --unit <slug>
python pipeline/translate/summarise.py --unit <slug> --batch     # then --collect
python pipeline/translate/summarise.py --unit <slug> --lang de --batch
python regenerate.py --site
```

Summaries are written from the English, so they follow it: if the translation
was re-run, the affected summaries must be too. `summaries.yml` is one file for
the whole project and the build refuses to write a smaller one than it found —
a unit-scoped walk once quietly replaced 345 summaries with 32.

## 7. Verify

`verify_site.py` runs inside `regenerate.py --site` and fails on a one-character
difference, a missing document, a dead internal link, or any external fetch.

Check by hand, once, that the new holding did not disturb the old one: rebuild
and diff the other unit's `corpus.txt` against its committed state. The expected
answer is *no differences*, or differences you can name exactly.

---

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

### State files

Any file the pipeline keeps between runs is keyed by `pad`, never by the archive's
own document number, and never flat across holdings. `_batches.json` was written
flat twice — once in `translate.py`, once in `summarise.py` — and each time the
second holding's submission erased the first holding's batch IDs, which had to be
recovered from the API. Mistake 2 is about records; this is the same mistake about
state.
