# The dataset

What is in `corpus/`, what each field means, and how to scope a question against
it without loading the whole edition.

This edition is not only correspondence. It holds **350 documents** from two
archival holdings: a file of letters and a volume of title deeds. Everything
below is generated from the units' `corpus.txt` and their `rulings.yml`; a
rebuild reproduces it exactly. Nothing here is hand-edited.

---

## Where to start

```
corpus/index/documents.json     the manifest - one compact row per document
```

Read this first. It carries only the fields worth narrowing on, so you reach a
working set before opening a single document. 350 rows, a few hundred KB.

Each row points at the two places the full text lives:

```
corpus/documents/<uid>.json     the document, whole
corpus/text/<uid>.txt           the same text, plain, for grepping
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
| `permalink` | `/letters/oe1bu9454/48/` | the public address |

Two holdings both have a document 7. Never key on `letter_id` alone.

---

## `index/documents.json`

One row per document.

| field | meaning |
|---|---|
| `uid`, `unit`, `letter_id`, `permalink` | identifiers, above |
| `doc_type` | what kind of instrument - see below |
| `language` | `de` unless the document is not in German |
| `date_iso` | `YYYY-MM-DD`, or `` if undated. Truncated where imprecise |
| `date_precision` | how much of the date is known - see below |
| `date_source` | **where the date came from - see below** |
| `place` | place of writing, canonical spelling, or `Unknown` |
| `n_pages`, `n_lines` | extent |
| `uncertainty_count` | surviving `[?]` and `[...]` markers |
| `translation_status` | `untranslated`, `draft` or `reviewed` - see below |
| `has_summary` | an English finding-aid summary exists |
| `has_damage` | text is missing or illegible |
| `mentions` | how many distinct people are named |
| `title` | a human label, e.g. `contract 18` |
| `path`, `text_path` | where the full document and its plain text are |

### `date_source` - the provenance of the date

**This distinction is the point of the field.** A date read off the page is not
the same fact as one a researcher assigned, and the dataset must not blur them.

| value | meaning | count |
|---|---|---|
| `signature` | parsed from the document's own dateline by the build | 276 |
| `dateline` | read off the dateline by the editor, recorded because the parser could not reach it - the deeds are formulaic, Latinate and often corrupt | 30 |
| `supplied` | **assigned by a researcher**, not present in the document | 28 |
| `inferred` | reasoned from neighbouring documents; `date_inferred_from` gives the basis, and it is shown to the reader | 7 |
| `twin` | taken from the document's own duplicate | 1 |
| `none` | undated, and left so | 8 |

`signature` and `dateline` are both *read from the document*. Only `supplied`
and `inferred` are editorial acts.

### `translation_status` - how far the English has got

| value | meaning | count |
|---|---|---|
| `draft` | machine-translated, mechanically checked, published; **not yet read against the manuscript by a human** | 345 |
| `reviewed` | every row raised against it in `review/<slug>/translation_review.csv` has been ruled on | 0 |
| `untranslated` | no English. Five documents whose German is too fragmentary to translate | 5 |

The distinction matters the way `date_source` does: a `draft` translation is
evidence of what the German probably says, not a settled reading. Quote the
German for anything load-bearing.

### `date_precision`

`day`, `month`, `year` say how much of the date is known - `date_iso` is
truncated to match. `unknown` means undated. `inferred` appears where a date was
reasoned rather than read; check `date_source` alongside it.

### `doc_type`

13 kinds in use:

| | | | |
|---|---|---|---|
| `letter` 320 | `contract` 16 | `privilege` 2 | `confirmation` 2 |
| `royal_rescript` 2 | `certified_copy` 1 | `protocol` 1 | `punctation` 1 |
| `donation` 1 | `certification` 1 | `lease` 1 | `note` 1 |
| `register` 1 | | | |

`letter` and `register` come from the correspondence; the rest from the deeds.
It is an open list, set per document in the unit's `rulings.yml`.

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
| `relations` | typed links to other documents - below |
| `sender`, `recipient` | derived from salutation and signature, where confident |
| `parent_letter`, `duplicate_of` | document-level links |
| `line_start`, `line_end` | the document's range in the unit's `corpus.txt` |
| `text_english` | the whole English translation, flowed. Empty where `untranslated` |
| `translation` | the same English, one segment per manuscript page: `{page, en}` |
| `summary_en`, `summary_de` | one-paragraph finding-aid summaries, written from the English |

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
| `entity` | slug in `reference/people.yml` |
| `display` | the edition's name for that person |
| `surface` | **what the page actually says** - the spelling found |
| `page`, `page_id`, `line` | where. `line` is absolute in `corpus.txt` |

`surface` vs `display` is deliberate: one man is written `Glenk`, `Glenck` and
`Glencke`, and the dataset records both what was written and who it was.

---

## The indexes

| file | shape |
|---|---|
| `index/people.json` | `entity` → `count`, `documents[]`, and every `mention` with its location |
| `index/places.json` | `place` → `documents[]`. Place of *writing*, not places named |
| `index/dates.json` | `year` → `documents[]` |
| `index/relations.json` | `{from, kind, to, note}` - see below |
| `index/uncertainties.json` | every surviving marker: `{uid, marker, page, page_id, line, context}` |

### `relations.json`

Typed links between documents, asserted on something a document *says* - not on
two documents being about the same estate. Kinds in use: `duplicate_of`,
`translates`, `certifies`, `transmits`, `confirms`, `refuses`, `supersedes`.
Each carries a `note` giving the evidence.

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
reference/place_canon.yml    variant spellings of one place
```

**Adjudicated** - proposed by a tool, decided by a human, then applied:

```
units/<slug>/linebreak_decisions.csv    is this really one broken word
units/<slug>/paragraph_decisions.csv    where the paragraphs fall
```

Both are re-derived on each run, and a decision changed by hand is carried over.

**Generated** - everything under `corpus/` and `site/`. Do not edit.

The one thing under `site/` that a rebuild does *not* reproduce is the English:

```
site/_data/translations/<pad>.yml   the translation, one entry per page
site/_data/summaries.yml            English summaries, keyed by pad
site/_data/summaries_de.yml         the German ones
```

These are written by the translation pipeline, cost money to produce, and are
read into the dataset by `build_dataset.py` rather than regenerated by it.
`regenerate.py` never touches them.

---

## Worked examples

**Everything mentioning Trąbczyn between 1804 and 1806.**
`places.json` gives the documents *written* there; grepping `text/` finds those
that *name* it. Filter either set on `date_iso` from the manifest. The two
questions are different and the dataset keeps them apart.

**Every document whose date a researcher assigned.**
Filter the manifest on `date_source == 'supplied'`. Not `!= 'signature'`: that
also catches the 30 read off a dateline by the editor, which are read, not
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

- `place` is the place of **writing**. A place merely named in the text is not
  indexed; grep `text/` for those.
- The people authority was built from the correspondence first. The deeds
  volume's cast has been adjudicated in, but the long tail in
  `reference/name_seeds.json` is statistical and still carries errors - `August`
  is indexed as a person and is Triebenfeld's own middle name.
- `language` is recorded only where a document is not in German. It names the
  document's main language: several German deeds carry passages of Polish, and a
  few of Latin, without being recorded as anything but German.
- Every translation is `draft`. The mechanical checks in
  `review/<slug>/translation_review.csv` have been run but the rows have not
  been ruled on, so the English carries whatever the model got wrong. The
  German is the record; the English is a finding aid to it.
- Summaries are written from the English, not from the German, so an error in a
  translation propagates into its summary.
- `corpus/letters.json` is the older single-array form of the same content. It
  is still what the website and `verify_site.py` read. Prefer the per-document
  files and the indexes.
