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

```
python pipeline/translate/translate.py --unit <slug> --dry-run   # spend nothing
python pipeline/translate/translate.py --unit <slug> --all --batch
python pipeline/translate/translate.py --unit <slug> --collect
```

The Batch API is half price and worth the wait. The collector refuses any result
whose segment count does not match the manuscript page count, so a truncated
tool call is never cached as though it were a finished translation.

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

— and only then re-translate the documents whose German actually changed:

```
python pipeline/translate/translate.py --unit <slug> --letters 1,2,5,... --batch
```

Re-running only the changed documents is the whole economy of this step. On
14526 that was 29 of 32 for about $3.50, against roughly $7 for the volume.

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

## The four mistakes this order exists to prevent

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
