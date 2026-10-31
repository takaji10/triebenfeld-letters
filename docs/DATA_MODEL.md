# The dataset

What is in `dataset/`, what each field means, and how to scope a question against
it without loading the whole edition.

This edition is not only correspondence. It holds **630 documents** from 51
holdings in six repositories: files of letters, volumes of title deeds,
ministry files, court books and single instruments, and one source that is a
print (the Kodeks Dyplomatyczny Wielkopolski). Everything below is generated
from the units' `corpus.txt` and their `rulings.yml`; a rebuild reproduces it
exactly. Nothing here is hand-edited. The `repository` field of the manifest
names which.

---

## Where to start

```
dataset/index/documents.json     the manifest - one compact row per document
```

Read this first. It carries only the fields worth narrowing on, so you reach a
working set before opening a single document. 630 rows, about half a
megabyte.

Each row points at the two places the full text lives:

```
dataset/documents/<uid>.json     the document, whole
dataset/text/<uid>.txt           the same text, plain, for grepping
```

Grep the `text/` files, not the JSON: a hit in JSON is unreadable and cannot be
quoted. Each `.txt` opens with four comment lines giving the uid, kind, date,
place and permalink, so a hit can be cited from the file it was found in.

The German comes first, then the summary and the English translation under
their own headings (`--- SUMMARY (English) ---`, `--- ENGLISH TRANSLATION
(draft) ---`), so a grep hit says which language it was found in and whether
that language is the archival record or a machine rendering of it.

---

## Identifiers

The archive's own document number is the citation key, and it is only unique
inside its holding. Four fields carry the namespace:

| field | example | |
|---|---|---|
| `unit` | `oe1bu9454` | the archival holding |
| `letter_id` | `48` | the archive's own number, untouched |
| `uid` | `oe1bu9454-48` | **globally unique - join on this** |
| `permalink` | `/documents/oe1bu9454/48/` | the public address |

Two holdings both have a document 7. Never key on `letter_id` alone.

---

## `index/documents.json`

One row per document.

| field | meaning |
|---|---|
| `uid`, `unit`, `letter_id`, `permalink` | identifiers, above |
| `doc_type` | what kind of instrument - see below |
| `language` | the document's language, `de` where German alone; a mixed document as a comma list (`la,pl`), as the document's ruling records it |
| `date_iso` | `YYYY-MM-DD`, or `` if undated. Truncated where imprecise |
| `date_precision` | how much of the date is known - see below |
| `date_source` | **where the date came from - see below** |
| `place` | place of writing, canonical spelling, or `Unknown` |
| `n_pages`, `n_lines` | extent |
| `uncertainty_count` | surviving `[?]` and `[...]` markers |
| `translation_status` | `untranslated`, `draft` or `reviewed` - see below |
| `has_summary` | an English finding-aid summary exists |
| `has_summary_de` | a German summary exists (9454: written from the German, claims checked) |
| `sender`, `recipient` | the correspondents, as in the letter record; empty where not identified |
| `legibility` | from the whole-letter reading: sound / partly garbled / largely garbled |
| `has_damage` | text is missing or illegible |
| `mentions` | how many distinct people are named |
| `places_named` | how many distinct places are named, from `place_mentions.json` |
| `era` | which of the site's eras the document sits in (`hohenlohe`, `medieval`, `prusimski-boundary`, `restitution`, `twentieth-century`, `wlodzimierz`); blank where none is assigned |
| `estates` | the estates the document is filed under, as slugs |
| `repository` | which repository holds the holding (`hzan-neuenstein`, `app-poznan`, `gstapk-berlin`, `bkpan-kornik`, `agad-warszawa`, `apl-lodz`, `adwl-wloclawek`) |
| `scans` | one entry per page carrying its `page_id` and scan file, where paired |
| `rough_transcription` | true where the transcription is still a machine's reading, not settled against the manuscript |
| `title` | a human label, e.g. `contract 18` |
| `path`, `text_path` | where the full document and its plain text are |

### `date_source` - the provenance of the date

**This distinction is the point of the field.** A date read off the page is not
the same fact as one a researcher assigned, and the dataset must not blur them.

| value | meaning | count |
|---|---|---|
| `signature` | parsed from the document's own dateline by the build | 327 |
| `dateline` | read off the dateline by the editor, recorded because the parser could not reach it - the deeds are formulaic, Latinate and often corrupt | 180 |
| `supplied` | **assigned by a researcher**, not present in the document | 28 |
| `inferred` | reasoned from neighbouring documents; `date_inferred_from` gives the basis, and it is shown to the reader | 57 |
| `sitting` | an entry of a court book, which has no date of its own: **taken from the heading of the court's sitting** it stands under, often on another leaf (`dates: sitting:` in `rulings.yml`, with a basis that is shown to the reader). Read from the book, so shown without brackets. Added 2026-10-06 for the Poznań court books | 18 |
| `twin` | taken from the document's own duplicate | 1 |
| `none` | undated, and left so | 19 |

`signature` and `dateline` are both *read from the document*. Only `supplied`
and `inferred` are editorial acts.

### `translation_status` - how far the English has got

| value | meaning | count |
|---|---|---|
| `draft` | machine-translated, mechanically checked, published; **not yet read against the manuscript by a human** | 626 |
| `reviewed` | every row raised against it in `review/<slug>/translation_review.csv` has been ruled on | 0 |
| `untranslated` | no English, because there is no text to translate: four numbers missing from the archive (9454: 121, 181, 225, 293) | 4 |

The distinction matters the way `date_source` does: a `draft` translation is
evidence of what the German probably says, not a settled reading. Quote the
German for anything load-bearing.

### `date_precision`

`day`, `month`, `year` say how much of the date is known - `date_iso` is
truncated to match. `unknown` means undated. `inferred` appears where a date was
reasoned rather than read; check `date_source` alongside it.

### `doc_type`

26 kinds in use:

| | | | |
|---|---|---|---|
| `letter` 367 | `note` 49 | `report` 29 | `draft` 22 |
| `donation` 21 | `contract` 21 | `register` 19 | `decree` 17 |
| `protest` 17 | `royal_rescript` 16 | `certified_copy` 14 | `confirmation` 9 |
| `certification` 8 | `privilege` 5 | `attestation` 3 | `power_of_attorney` 2 |
| `delivery` 2 | `notarial_attestation` 1 | `visitation` 1 | `protocol` 1 |
| `cession` 1 | `punctation` 1 | `lease` 1 | `royal_consent` 1 |
| `memorandum` 1 | `summons` 1 | | |

`letter`, `draft` and `note` come from the correspondence; the rest from the
deeds, the court books and the added single instruments. It is an open list,
set per document in the unit's `rulings.yml`.

A document is one **package**: an instrument together with the enclosures filed
with it. Document 23 is a royal confirmation reciting eleven enclosed
instruments - contract, ratifications, attestations, powers of attorney - and
its `doc_type` is `confirmation`, the kind of the instrument that heads it. The
enclosures are not separate records; what each package contains is set out in
`review/<slug>/document_boundaries.csv`.

---

## `documents/<uid>.json`

Everything in the manifest row, plus:

| field | meaning |
|---|---|
| `text` | the archival text, exactly as transcribed. **Canonical** |
| `text_reading` | the same, flowed into readable prose |
| `pages` | one entry per manuscript page - below |
| `mentions` | every person named, with location - below |
| `place_mentions` | every place *named* in the text, in the shape `mentions` has, `kind: 'place'` |
| `mentions_english` | the names the **English** names, tied to the same entity slugs as the German (`surface_de` / `surface_en`, since the forms differ: Wien -> Vienna). Without it a reader of the English cannot be shown who a passage is about, and grepping the English is no substitute |
| `place_canonical` | the place of writing, canonical form |
| `relations` | typed links to other documents - below |
| `sender`, `recipient` | derived from salutation and signature, where confident |
| `parent_letter`, `duplicate_of` | document-level links |
| `seq_archival` | the document's order within its holding, which sorts the holding's list when the numbers themselves do not |
| `is_missing` | true for a placeholder carrying a number the archive lost (its text is `(missing)`) |
| `date_inferred_from` | for a `date_source: inferred` date, what the reasoning leans on |
| `line_start`, `line_end` | the document's range in the unit's `corpus.txt` |
| `text_english` | the whole English translation, flowed. Empty where `untranslated` |
| `translation` | the same English, one segment per manuscript page: `{page, en}` |
| `summary_en`, `summary_de` | one-paragraph finding-aid summaries. In 14525 and 14526 both are written from the English translation, each separately (the German is not a translation of the English summary), and neither had the second, claim-by-claim check. In every other holding the German is written from the German and checked claim by claim, and the English is translated from it. None where a document has no text: I. HA GR, Rep. 7 C, Nr. 3709 (not yet transcribed) and 9454's skipped and missing numbers |
| `reading` | the whole-letter reading (units/<slug>/reading.json): `notes`, `legibility`, `claims` (each summary statement with its letter lines, and the check's objection where there was one), `doubtful_words` |

The English is **generated and not canonical**. It is never checked against
`text` for fidelity, because it cannot be: the build's character-exact
verification covers the German only. `translation` is aligned to `pages[]` by
`page`, so an English passage can be cited to the manuscript page it renders.

### `pages[]`

A document is a sequence of manuscript pages, and each page carries three views
of the same lines:

| field | meaning |
|---|---|
| `page` | 1-based within the document |
| `page_id` | **the manuscript page's archival identity**, e.g. `0011_a1` - capture and crop. Stable: it never changes when files are relabelled |
| `diplomatic` | the archival lines, exactly as transcribed. **Canonical** |
| `transcription` | the same lines, with line-end marks resolved per recorded decisions |
| `reading` | the page flowed into prose |
| `paragraphs` | that prose, divided |
| `continues_previous` / `continues_next` | the paragraph runs on across the page break. Reading text never crosses a page break, so a paragraph that continues starts a new entry here |
| `line_start`, `line_end` | the page's range in `corpus.txt` |
| `scan` | the image file, where paired |

`diplomatic` is the record everything else is checked against. The build asserts
that `reading` alters no letter of it.

### `mentions[]`

| field | meaning |
|---|---|
| `entity` | slug in `reference/people.yml` - or of the long tail, a slug minted from the name itself |
| `display` | the edition's name for that person |
| `kind` | `person`; the same matcher runs for places, whose rows say `place` |
| `surface` | **what the page actually says** - the spelling found |
| `scan` | the page's image file, so a citation resolves to the manuscript without another lookup |
| `page`, `page_id`, `line` | where. `line` is absolute in `corpus.txt` |
| `doc_line` | the same point as the published page numbers it - numbered from 1 within the document, which is what the site shows |

`surface` vs `display` is deliberate: one man is written `Glenk`, `Glenck` and
`Glencke`, and the dataset records both what was written and who it was.

---

## The indexes

| file | shape |
|---|---|
| `index/people.json` | `entity` → `count`, `documents[]`, and every `mention` with its location |
| `index/places.json` | `place` → `documents[]`. Place of *writing*, not places named |
| `index/place_mentions.json` | `entity` → `count`, `documents[]`, and every `mention` with its location: the places **named** in a document. A different question from `places.json`, and now a different answer |
| `index/dates.json` | `year` → `documents[]` |
| `index/relations.json` | `{from, kind, to, note}` - see below |
| `index/uncertainties.json` | every surviving marker: `{uid, marker, page, page_id, line, context}` |

The other datasets carry their own mention lists, only on the site as ruled:
`dataset/literature/mentions.json` (each row `{entity, kind, display, surface, work, passage, line, context}`) and
`dataset/newspapers/mentions.json` (the same shape, the item in place of the work). Every hit was read and ruled in
`literature/index.yml` or `newspapers/index.yml` before it went live, and
`pipeline/review/check_mentions_join.py` holds their slugs to the same
authorities the corpus indexes from.

### `relations.json`

Typed links between documents, asserted on something a document *says* - not
on two documents being about the same estate. Kinds in use: `answers`,
`certifies`, `confirms`, `copies`, `duplicate_of`, `entered_in`, `refuses`,
`registers`, `supersedes`, `supplements`, `transmits`. Each carries a `note`
giving the evidence.

### `uncertainties.json`

Every `[?]`, `[word?]` and `[...]` still in the text, with its line and context.
This is what makes "where is the evidence still weak here" a question you can
ask. The manifest's `uncertainty_count` totals must equal the rows here, and the
build asserts it.

---

## What is authored, and what is generated

**Authored** - edit these:

```
units/<slug>/corpus.txt      the transcription. Canonical, never rewritten by any script
units/<slug>/rulings.yml     editorial decisions: doc_type, language, dates, places,
                             relations, duplicate_of, damage
units/<slug>/unit.yml        where the scans are, how files are named
reference/people.yml         who the edition recognises, and how each is matched
reference/places.yml         canonical places, their variants, patterns and
                             the distinctions that must never be merged
reference/genealogy.yml      the family of each person who has their own page
                             on the site, every fact with its source
                             (docs/LITERATURE_PLAN.md, section 22)
```

**Adjudicated** - proposed by a tool, decided by a human, then applied:

```
units/<slug>/linebreak_decisions.csv    is this really one broken word
units/<slug>/paragraph_decisions.csv    where the paragraphs fall
```

Both are re-derived on each run, and a decision changed by hand is carried over.

**Generated** - everything under `dataset/` and `site/`. Do not edit.

The one thing under `site/` that a rebuild does *not* reproduce is the English:

```
site/_data/translations/<pad>.yml   the translation, one entry per page
site/_data/summaries.yml            English summaries, keyed by pad
site/_data/summaries_de.yml         the German ones
```

These are written by the translation pipeline, cost money to produce, and are
read into the dataset by `build_dataset.py` rather than regenerated by it.
`pipeline/regenerate.py` never touches them.

---

## Worked examples

**Everything mentioning Trąbczyn between 1804 and 1806.**
`place_mentions.json` gives the documents that *name* it, with the spelling
each hit found and the line it sits on; `places.json` gives those *written*
there. Filter either set on `date_iso` from the manifest. The two questions
are different and the dataset keeps them apart.

**Every person everywhere, including the press and the books.**
`people.json` is the corpus; `dataset/literature/mentions.json` and
`dataset/newspapers/mentions.json` are the ruled hit lists of the other
sections, keyed by the same slugs, so "what do we hold on this person" is
three conjunctive lookups rather than a read of every text.

**Every document whose date a researcher assigned.**
Filter the manifest on `date_source == 'supplied'`. Not `!= 'signature'`: that
also catches the 180 read off a dateline by the editor, which are read, not
assigned.

**What is linked to document 18, and how.**
Filter `relations.json` on `from` or `to` == `oe1bu14526-18`. Each row's `kind`
says what the link is and `note` says on what evidence.

**Where is the evidence weak in one holding.**
Filter `uncertainties.json` on `uid` prefix. Group by `uid` for the documents
that need work most.

**Who appears in a holding, and where exactly.**
`people.json` → each entity's `mentions[]` carries `page_id` and `line`, so a
claim can be cited to a manuscript page rather than to a document.

---

## Known limits

- `place` is the place of **writing**. The places *named* have their own index
  (`place_mentions.json`), run against the same authority - so a name no
  pattern covers appears in neither index, and `grep text/` remains the
  catch-all for it.
- The people authority was built from the correspondence first. The deeds
  and court-book volumes' casts have been ruled in as they were read, and
  the long tail in `reference/name_seeds.json` is statistical: it carries
  errors that must be ruled out one by one (the review sheets do). What is
  not settled anywhere is the non-German naming: a medieval Latin charter or
  a Russian-file record can name its actors in forms no pattern reaches, and
  a German document whose names were never ruled comes out of the build with
  tags for no one. `pipeline/review/zero_mentions.py` (run by
  `regenerate.py`) lists those documents of any size, each with its leads,
  for the editor to rule - "truly names no one", or author the entry.
- `language` names the document's main language, `de` where German alone;
  mixed documents carry a comma list (`la,pl`) as their ruling records it.
  Several German deeds still carry passages of Polish or Latin inside a
  German record without the field saying more than that.
- Every translation is `draft` (626 of 630; four are missing from the
  archive outright). The mechanical checks in
  `review/<slug>/translation_review.csv` have been run but the rows have not
  been ruled on, so the English carries whatever the model got wrong. The
  German is the record; the English is a finding aid to it.
- Summaries are written from the English, not from the German, so an error in a
  translation propagates into its summary.
- `dataset/letters.json` is the older single-array form of the same content. It
  is still what the website and `pipeline/verify_site.py` read. Prefer the per-document
  files and the indexes.

### Text a page sets apart

A page entry in `documents/<uid>.json` may carry `sideways_lines` /
`sideways_paragraphs` (text written sideways on the page, from
`units/<slug>/sideways.yml`) and `office_lines` / `office_paragraphs` (text the
receiving office wrote on the letter, from `units/<slug>/office_notes.yml`):
0-based positions among that page's lines and paragraphs. The text itself is
ordinary text of the document. `by_paragraph: true` marks a page transcribed by
paragraph, where a line of the transcription is a paragraph of the manuscript
(`rulings.yml`, `pages: by_paragraph:`). The office and by-paragraph keys are
present only where they apply. `doc_type: draft` is an outgoing letter as it
stayed in the sender's file.
