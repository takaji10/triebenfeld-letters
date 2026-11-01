# Connections between documents — the standing method

How documents of the edition are tied to each other and to the sources
around them, where the ties live, and how a new source's ties are proposed.
Updated 2026-11-01, when the cross-holding connections were built.

## The four kinds of connection, and where each lives

| Kind | Authored in | Shown where |
|---|---|---|
| Document ↔ document, **within one holding** | `relations:` in the holding's `rulings.yml` (DATA_MODEL, `relations.json`) — typed (`answers`, `supplements`, `transmits`, …), each with a `note` giving the evidence | the small list under a document's heading |
| Document ↔ document, **across holdings** | `reference/connections.yml` (this file, below) | each participant's own note and the others' links, in a document page's "About this document" box |
| Literature/newspaper/place passage ↔ document | `literature/links.yml` (`about:` per passage), the place sources' and gazetteer's own citation fields | the "Related"/"Bezüge" column on a work page; "In the literature" on the document page |
| Person/place ↔ everything naming them | computed from the index; the gazetteer's footnotes in `reference/gazetteer_sources.yml` | the boxes on people and place pages |

The split is by custody, not by importance: one holding's documents are
keyed by the archive's own numbers and ruled in its `rulings.yml`, so their
relations live there; a chain that runs from a Berlin ministry file to a
Breslau letter crosses holdings, so it is authored in
`reference/connections.yml`. A connection with more than two participants is
one connection, not several: every participant gets its own note, and each
page shows its own.

## Cross-holding connections

`reference/connections.yml` — each connection:

```
- id: <short name, never shown>
  documents:
    - uid: <the document, as in dataset/letters.json>
      en: <the note THIS document's page shows>
      de: <the same in German>
    - uid: ...
```

Rules, held by `pipeline/build/connections_site.py` (in `regenerate.py`
after the mention joining, before the website data) and
`pipeline/verify_site.py` (each participant's page must link every other
participant, both languages):

- at least two documents, none named twice in one connection;
- every participant has its own `en` and `de` — the note **that document's
  page shows**, so no page carries a sentence written for the other side
  (the per-passage lesson, LITERATURE_PLAN section 32);
- say who says what — "the dossier proposes", "the letter reports" — never
  "it was"; every figure was read in both documents;
- where a connection rests on Claude's identification, the comment above it
  says so and `docs/NEEDS_CONFIRMATION.md` lists it until the editor has
  ruled. The first four connections (2026-11-01) restate material of links
  the editor has already ruled, and carry no new identifications.

The label under a link is the same reference the literature links use
(`I. HA GR, Rep. 7 C, Nr. 3570, document 1 (9 August 1796)`), so the two
kinds of connection read alike.

## The method: how connections are found

Written for the sweeps and for the Connections step of every
adding-a-source procedure (NEW_UNIT section 8, the newspapers', the places',
the literature's). The candidate generator is mechanical; the reading is
where the connection is made. In order of yield:

1. **Chains, not pairs.** Court books and ministry files come in procedural
   chains — proposal → cabinet order → deed; citation → service → return;
   decree → execution → delivery → demolition. Each member names its
   neighbours. The within-holding `relations:` capture the chain inside one
   box; the sweep generalises it across boxes, using the summaries (`has_summary`,
   `has_summary_de` in the dataset) as the cheap first read: two documents
   whose summaries touch the same event with a figure, a name or a date in
   common become a candidate pair; only those get the full two-text read.
   A document's own text often names the chain outright ("the enclosed
   extract of the resident's dispatch"), which is an `answers`/`transmits`
   relation waiting to be recorded.
2. **Per-entity sweeps from the index.** For each rare person or place, the
   index already lists every document naming them; the sweep asks of each
   pair: same event, two sides? Cheapest for the people who appear in few
   documents, which is most of them. A shared name alone is not a
   connection; the event is.
3. **Figures as hooks.** A sum, a date or a count appearing in two
   documents — 26,000 rt; 30,100; the 8,400 rt yield of Trąbczyn — is the
   strongest single trigger, and a disagreement between the two is the most
   valuable find of all: the documents-first rule (HOUSE_STYLE) then sends
   the difference to NEEDS_CONFIRMATION, and the notes say who says what.
4. **The era essay and the-story as maps.** Their chains were written and
   verified; each narrative link between two documents is a candidate
   connection already half-made. Reading those pages against
   `dataset/letters.json` is the fastest way to a batch.

What counts as **relevant** — the measure used on the literature's links,
the same here: a document confirms, corrects, extends or dates what the
other says, in that order of value. Two documents about the same estate a
generation apart are not a connection; two counts of the same villages
eight years apart are.

## The Connections step, when a source is added

Every kind of source gets it, in its own procedure's checklist
(NEW_UNIT section 8, NEWSPAPERS_PLAN, PLACES_PLAN, LITERATURE_PLAN):

1. **Read the new source whole** (it has just been read anyway — the
   reading record, the summaries, the index ruling are already done).
2. **Propose its connections into the existing documents** — by the method
   above, chains first: what existing document does the new source bear on
   directly? Write the participants' notes (the new source's own note among
   them) and put them before the editor as a proposal, flagged as Claude's
   reading where an identification is Claude's.
3. **Propose the reverse**, where the new source is a document of a
   holding: which existing documents does it *bear on* — a new letter
   answering an old one, a new deed confirming a lease the letters
   describe? The existing document's note is written then, not left to a
   later pass.
4. **Enter the settled ones** in the right home (the table above), rebuild,
   and let the verify gate hold both sides.

The same sitting, like every other hand-written file the holding owes the
site (NEW_UNIT section 8): a source that silently lacks its connections is
the same kind of gap as a holding without its bios — nothing regenerates
them.
