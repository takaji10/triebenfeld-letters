# One page, one document: merging documents that were split (planned 2026-11-23)

## The problem

Some holdings split what stands on one sheet into several documents, so the
same page appears twice on the site and the holding counts more documents
than it has. Example: III. HA MdA, III Nr. 12765, page 0003_a2 holds
Triebenfeld's letter to Hardenberg (document 1) and Hardenberg's draft reply
written on it (document 2); the copy that letter encloses is document 3. The
editor (2026-11-23): follow the pages as they stand — the letter, with the
reply as a second voice on the same page, using the standard the site already
has for several voices; and an enclosure should not be a document of its own.
**First rule: a page is shown only once on the site.** A page under two
documents is very likely one document split in two, but each case is read.

## What there is (the scan of 2026-11-23)

**32 pages stand under two documents, in 13 holdings:**

| kind | cases | proposal |
|---|---|---|
| a reply or draft written on the incoming letter, or two drafts on one sheet (government files) | Nr. 12765 1+2, 9+10, 21+22; Nr. 3709 5+6, 8+9+10; Nr. 12367 7+8 | merge: one document, the later writing as a second voice |
| one entry of a register ends and the next begins on the page | Konin Gr.115, 116, 117, 118, 119; 53/6/0/-/36; the Ląd copy-book (app5314550221) | leave: separate acts of a court or a copy-book |
| Breyer's notebook, divided by content at the editor's word (2026-10-14) | APP 53/968/0/-/716 (8 pages) | leave, unless the editor says otherwise |
| copies written one after another | Rep. 162 Nr. 295 (three documents the editor confirmed, 2026-10-05); APŁ 6603 2+3 (a later certification on the copy) | leave; 6603's certification could become a second voice — ask |

**Enclosures kept as documents of their own:** the records link them
("transmits", "supplements"): Nr. 12765 1→3, 27→28, 29→27; Nr. 3709 1→2,
3→4; Nr. 3132 4→5, 4→6; Nr. 1414 1→2; Nr. 421 1→2, 4→6; Nr. 12366 1→2;
Oe 1 Bü 14526 22→23; and the sub-numbers of Oe 1 Bü 9454 (1a; 72a-f; 74a-d;
118a-c; 179a), where the archive filed several items under one number: some
are enclosures of the letter beside them, others are separate letters
(72a, 72b and 72f are three letters of February, March and May 1812).
Every one is read; only a true enclosure (sent with the letter, standing
with it in the file) is merged.

## How a merge is made

For each merge, a main document (the first, the letter) keeps its number;
the other's number is retired.

1. **Text** (`corpus.txt`): the absorbed document's `[DOC]` marker goes; a
   page that stood under both stands once, the main document's lines first,
   then the other's. The reply or draft on the same sheet is set apart as a
   second voice ("Written in another hand", `hand_notes.yml`; an office note
   stays an office note). An enclosure follows on its own pages. No line is
   added, dropped or changed: checked by counting every line before and
   after.
2. **Records**: the holding's `rulings.yml`, `unit.yml`, decision sheets and
   set-apart blocks keyed by the retired number move to the main document
   or, where they only described the retired one (its date, sender, type),
   are kept in the holding's `notes.md`. The main document's date, place,
   sender, recipient and type stay as they are; estates and people are the
   union of both.
3. **Addresses**: the retired document's address
   (`/documents/<slug>/<m>/`) forwards to the main one, through the site's
   existing redirect stubs. No other document is renumbered, so no other
   address changes.
4. **English**, without re-translating: the merged pages are joined from the
   published English (the second voice under its label, the enclosure's
   pages after), the same in the translation cache so that a re-publish
   keeps it; corrections keyed to the retired document are moved to the main
   one and its new page numbers.
5. **Summaries**: one summary for the merged document, in both languages,
   written from the two and claim-checked.
6. **Everything that names the retired number** — the holding's page (its
   citations and counts), literature links, connections, the timeline,
   NEEDS_CONFIRMATION, the notes — is pointed at the main document; a search
   for the retired id must find nothing but the redirect.
7. **Checks**: every other document in the holding unchanged (the date-order
   snapshot and compare); every page shown once (a new check in
   `verify_site.py`, so it cannot come back); the site verifies; the merged
   document looked at on the site.

Tools: `pipeline/review/merge_documents.py` (one entry per merge in
`units/<slug>/intake/merges.yml`, refused if anything does not add up), with
a dry run that prints the merged document's pages before anything is written.

## Steps

1. **Pilot: Nr. 12765 documents 1, 2 and 3** (the editor's example: the
   letter, the draft reply on it as a second voice, the enclosed copy after
   it). The editor looks at it on the site.
2. The reading of every other case (a Sonnet reader and Claude), listed with
   a proposal for each; the editor confirms the list.
3. The merges, holding by holding, each checked and committed on its own.
4. The page-once check added to `verify_site.py`; NEW_UNIT.md says how a
   letter, its reply on the sheet and its enclosures are divided from now on.

Paid runs: none.

## The editor's answers (2026-11-23)

1. A reply on the letter's sheet: a second voice, "Written in another hand". Yes.
2. An enclosure: its pages follow the letter's, no box. Yes.
3. Registers, the copy-book, Breyer's notebook, Rep. 162 Nr. 295: leave as is.
4. **Renumber** the holding where documents are joined (no gaps). **Oe 1 Bü
   9454 is not touched at all**: its numbers are the archive's, written at
   the head of the letters.

## Done

- **Pilot, Nr. 12765** (2026-11-23): 30 documents to 24 — 1+2+3, 8+9+10,
  21+22, 27+28 joined (the two drafts of 9 and 10 on one page are one voice
  block). Every other document checked unchanged through the map
  (`merge_check.py`); each page once; the out-of-date translation list the
  same under the new numbers; the English from the cache equals the
  published; old `/letters/` and freed `/documents/` addresses forward to
  where their documents went.

## For the editor (asked before the answers)

1. A reply or draft written on the same sheet as the letter: the second voice
   labelled "Written in another hand", as already used. Agreed?
2. An enclosure: its pages simply follow the letter's in the same document
   (no box), the summary saying what it is — or set apart with a label of
   its own?
3. Registers, the copy-book, Breyer's notebook and the copies of Rep. 162 Nr.
   295, where two acts share a page: leave as separate documents?
4. The retired number leaves a gap in the holding's numbering (1, 4, 5 …),
   and its address forwards to the merged document: agreed?
