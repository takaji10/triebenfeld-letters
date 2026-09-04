# The Triebenfeld Letters

A digital edition of the correspondence of Peter Friedrich von Triebenfeld and
Friedrich Ludwig, Fürst zu Hohenlohe-Ingelfingen, built from archival holdings at the
Hohenloher Zentralarchiv Neuenstein. Each document is shown four ways: the page scan, a
diplomatic transcription, a reading text, and an English translation that marks its own
uncertainty. The site is bilingual.

Live at <https://takaji10.github.io/triebenfeld-letters/>.

## Layout

```
units/<slug>/     one archival holding
  unit.yml        where its scans are, how its files are named
  corpus.txt      the transcription. [LETTER N] before each document
  rulings.yml     editorial decisions, keyed by document number
  notes.md        provenance and quirks
pipeline/
  intake/         crop and split the raw scans
  build/          transcription -> database -> website data
  translate/      translate, check, publish, summarise
  review/         name and spelling review sheets
reference/        shared by every unit: glossary, name rulings, place canon
corpus/           generated, merged across units
review/<slug>/    generated review sheets
cache/            model output. Expensive; never deleted casually
docs/             changelog, deploy notes, method reports
site/             the Jekyll site
```

## Where things go

- **Raw scans stay outside the project.** Put them anywhere; record the path in
  `units/<slug>/unit.yml`. Cropping writes into a `processed/` folder beside them.
- **The transcription goes in `units/<slug>/corpus.txt`**, with `[LETTER N]` on its own
  line before each document. That file is the canonical input and is never rewritten by
  the pipeline.
- **Decisions go in `units/<slug>/rulings.yml`**, keyed by the archive's own document
  number. Never edit a pipeline script to record one.

## Adding a holding

```bash
# 1. scaffold. PDFs must be exported to JPGs into the scans folder first.
python new_unit.py oe1bu14525 --ref "Oe 1 Bü 14525" \
    --scans "C:/Users/Tersnaus/Downloads/Oe 1_Bue 14525"
#    then fill in the TODOs in units/oe1bu14525/unit.yml

# 2. crop the two-up scans into single pages
python pipeline/intake/crop_scans.py --unit oe1bu14525

# 3. split any bifolia the crop left as one wide page
python pipeline/intake/split_spreads.py --unit oe1bu14525 --auto
python pipeline/intake/split_spreads.py --unit oe1bu14525 --review
#    check the proofs in processed/_spreads_review/, then:
#      --apply-review processed/_spreads_review/INDEX.md
#    for any the detector could not place, put the line by hand:
python pipeline/intake/review_folds.py --unit oe1bu14525
#      open processed/_spreads_review/review.html, drag each red line onto
#      the fold, Save folds.json, then:
python pipeline/intake/split_spreads.py --unit oe1bu14525 \
    --apply-folds processed/_spreads_review/folds.json

# 4. transcribe offline, save to units/oe1bu14525/corpus.txt

# 5. build. Repeat after every edit to corpus.txt or rulings.yml.
python regenerate.py --unit oe1bu14525

# 6. work through review/oe1bu14525/*.csv, record what you settle in
#    units/oe1bu14525/rulings.yml, and re-run step 5 until it is clean

# 7. translate (batched, roughly half price, results arrive within a few hours)
python pipeline/translate/translate.py --unit oe1bu14525 --batch
python pipeline/translate/translate.py --unit oe1bu14525 --collect
python pipeline/translate/check_translations.py --unit oe1bu14525
python pipeline/translate/repair_translations.py --unit oe1bu14525   # only if flagged
python pipeline/translate/publish_translations.py --unit oe1bu14525
python pipeline/translate/summarise.py --unit oe1bu14525 --build
python pipeline/translate/summarise.py --unit oe1bu14525 --build --lang de

# 8. build and verify the whole site
python regenerate.py --site
```

Set `status:` in `unit.yml` as you go: `draft` → `transcribed` → `translated` →
`published`. A unit with an empty `corpus.txt` is skipped by the build, so scaffold as
early as you like.

## Rebuilding

```bash
python regenerate.py           # every transcribed unit, then merge
python regenerate.py --site    # also build and verify the website
cd site && bundle exec jekyll serve
```

`regenerate.py` runs the per-unit steps in dependency order, merges the units, then
builds the site once. Editing a `corpus.txt` shifts its line numbers, which invalidates
that unit's line-break decisions, which changes the page structure, which changes the
scan mapping, so the order is not optional.

## Verification

`verify_site.py` checks the built HTML against `corpus/letters.json` and fails if a
document is missing, if any transcription differs by one character, if an internal link
does not resolve, or if a page fetches anything external. It runs on every deploy and a
failure blocks publication.

## Identifiers

The archive's document number stays as it is and is unique only within its holding, so
the slug carries the namespace:

```
unit       oe1bu9454
letter_id  48
uid        oe1bu9454-48
permalink  /letters/oe1bu9454/48/
```

Documents published before the namespace existed keep working: `legacy_flat_urls: true`
in `unit.yml` generates stubs at the old addresses.

## Licence

Not yet determined. Until a `LICENSE` file is added, no reuse rights are granted.

Deployment: [docs/DEPLOY.md](docs/DEPLOY.md). Editorial method:
[the About page](https://takaji10.github.io/triebenfeld-letters/reading-this-edition/).
