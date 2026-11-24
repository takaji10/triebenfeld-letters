# The site overhaul of 2026-11-24: plan

The editor's list of 2026-11-24 (Sources page, search, descriptions, crops,
literature, page numbers, prose rules, individual works), with their answers
to the four questions put the same day. Each step names who does it, by the
rule of CLAUDE.md, "Sub-agents first": a script first, then Haiku (mechanical
work with a machine check), then Sonnet (code to a written spec, reading,
flagging, claim checks), and Opus, the main session, for the specs, the
rulings, every word of prose a reader sees, and the check of every finding it
acts on. Nothing is published before the editor's word.

## The editor's answers (2026-11-24)

1. **The list pages' search** (Manuscripts, Newspapers, Literature, Maps):
   full text, results listed. With no query or filter the page shows its
   tiles; once the reader types or filters, the tiles give way to a list of
   the matching documents, passages or maps of that kind only, the matched
   words highlighted, as on a holding's page.
2. **The literature**: a reading column with a contents panel. One
   continuous read in a book-width column, the printed page numbers in the
   margin, a sticky contents panel (sections, jump to a page), the English
   and the original side by side on a wide screen, the Related gutter kept.
3. **The new writing rules** are applied to all the English prose: the
   holding and work descriptions, the document summaries, and the era,
   place and person pages. The German is skipped.
4. **The literature's thumbnails**: the editor supplies a title page for a
   work where one exists; a work without one gets a typographic tile
   (author, short title, year), not an empty frame.

## Assumptions taken (say if any is wrong)

- The list of works to show in full ends in a truncated third title. It is
  taken to be **Słownik geograficzny Królestwa Polskiego — cytowane hasła**
  (`slownik`), the twin of `nmpol`. The three: `nmpol`, `slowinski2023`,
  `slownik`, each shown with the entries or pages the edition uses, in full.
- "Replace the Order option": the order "by reference" (archival) goes; the
  choices are Chronological (oldest first / newest first) and A-Z (A-Z / Z-A).
- "Remove the Show option": the filters by dating, damage, uncertain reading
  and duplicate go from the bar entirely (the marks themselves stay on the
  pages).
- German labels: "Manuscripts" is **Handschriften**; "Pages" **Seiten**;
  "Date" **Datum**.
- A map's tile counts sheets where it has more than one, else no count; a
  newspaper item counts its pages.

## Phase 0. The rules (Opus; first, everything else follows them)

Written into `docs/HOUSE_STYLE.md` (with an example from the site for each)
and into the brief every summary or description sub-agent is given. Proposed
wording, to be settled in the commit:

- **R1. No physical description the counts already give.** The tile and the
  header count pages and documents; prose does not ("Thirteen pages of the
  register of the hearth tax", "Two of Albert Breyer's field notebooks"
  become "The register of the hearth tax ...", "Albert Breyer's field
  notebooks ..."). A physical fact stays only where it changes how the
  document is read (a lost leaf, a burnt edge, a copy rather than the
  original).
- **R2. New things are introduced as new.** A person, group or thing met
  for the first time takes "a", a number, or no article, not "the": "after
  three townsmen who held it in hereditary lease stopped paying", not "after
  the three townsmen". "The" is for what the reader already knows: named
  before, unique (the King, the Kalisz chamber), or defined in the same
  sentence.
- **R3. Written for a reader who does not know the subject.** Every action
  is complete: whom a debt was owed to, who refused what, for whom a
  petition was made ("stopped paying the rent they owed the Prince"). An
  office, an institution or a term is explained on first mention in a few
  words, or linked to the glossary. No sentence leans on a document the
  reader has not seen.
- **R4. The content, not the paper** (the editor's examples from agad1174016
  and elsewhere). A description tells what happened, who wanted what, and
  why it matters; it does not narrate the document as an object or the act
  of reading it. Out: "The text states that ..." (say what happened: "The
  Emperor had referred Dąbska's case to the commission"); clerical
  furniture with no bearing on the matter (the president's and secretary's
  names under every entry, the order in which the register copied its
  resolutions, "the entry is dated at ..."); repeating what a heading or the
  date field already says (a paragraph headed "The order for Wybicki,
  12 July 1807" does not end "dated ... 12 July 1807"). A signature, a seal
  or a copyist's note stays when it tells the reader something: who decided,
  that a copy may differ, that a hand is the King's own.
- **R5. The tile's standard form** (Phase 3): translated title, original
  title in italics, source, a short description, the relevant counts, the
  date.

**Machine help, free:** `pipeline/review/prose_lint.py` (Sonnet writes it to
this spec, Opus checks its patterns): flags in the English prose number-word
page/leaf/notebook openings, "the text (states|says|records|notes)", "the
entry (is dated|reads)", "copied into", "under each entry", "signed by" in a
summary's last sentence, a date that repeats the heading, and "the" + plural
noun at the first mention of a group in a text. It lists candidates only;
nothing is changed by the script. Lessons into WORKING_NOTES.

## Phase 1. The Sources page (Sonnet to spec; Opus reviews)

- The four kinds as **clickable tiles** (the whole tile one link, as the
  holding cards are): icon, name, one-line description, count.
- **"Size" removed** (`sources_kind_count`); the count stands as "52
  holdings".
- **Icons**: redrawn as larger duotone icons (a tinted disc of the site's
  accent behind a 1.6-stroke line drawing; one drawing per kind, both colour
  schemes from `currentColor` and a CSS token), drawn and checked on a
  Playwright sheet in light and dark before the commit (the 2026-11-07 dark
  background bug). Opus chooses between two or three drawings on the sheet.
- **"Archival material" renamed "Manuscripts"** (Handschriften) wherever it
  stands: the Sources page, the list page's heading, the header menu, the
  breadcrumbs.

## Phase 2. One search bar for every list (Opus spec; Sonnet builds; Haiku runs the checks)

One component, `browse.html` + `browse.js`, generalised, used on a
holding's page, /documents/, the four list pages and a work of literature.

- **The index.** The documents' index stays; added beside it (separate
  files, loaded only by the page that needs them): the newspaper items, the
  literature's passages (original and English, by printed page) and the maps
  (titles, accounts, labels). Built by `build_site_data.py` and the
  literature/newspaper/maps site scripts.
- **Order**: Chronological ↑/↓ and A-Z ↑/↓.
- **Eras**: the name with its date range, "Hohenlohe-Ingelfingen
  (1795-1806)", from `reference/eras.yml`.
- **Year**: a range selector (two handles, two number boxes) whose limits
  are the earliest and latest year the site holds, written at build time.
  **The check**: `verify_site.py` fails if the built limits are not the
  minimum and maximum of the data, so new material that widens the range
  cannot be published with a stale selector.
- **People and places**: multi-select (chips with type-ahead); more than
  one selected means AND.
- **"Show" removed.**
- **Search options**: exact phrase (also by quotes), all words / any word,
  whole words only, ignore accents (on by default: "Zagorow" finds
  "Zagórów"), match case, and where to look (original, English, summaries).
- **Layout**: the search box and Order always shown; a small arrow opens
  "Advanced search" (eras, years, people, places, theme, holding, options).
  The open/closed state is remembered per reader.
- Playwright screenshots of every page that carries the bar, desktop and
  phone, light and dark (Sonnet takes them; Opus looks).

## Phase 3. The tiles, standardised (Sonnet to spec; Opus checks every kind)

One card include for all kinds, in this order: **translated title**;
**original title in italics**; **source** (archive and reference; newspaper,
issue and page; publisher and place; map repository); **short
description**; **counts**, only the relevant ones (manuscripts: documents
and pages; a book or article: pages; a newspaper item: pages; a map: sheets
where more than one); **date** (a range where the material spans years).
"Manuscript pages" becomes **"Pages"**, "Span" **"Date"**. The literature's
cards that show the original title first are put right (the English title
heads in the English site). The **document type tag** moves to the foot of
the tile and appears only on manuscripts.

## Phase 4. The literature (Opus spec; Sonnet builds; Opus reviews)

- **The reading column and contents panel** (answer 2), the same layout for
  every work, summary-only ones included.
- **The full-width bug**: Seidel (2018) and Zerwane ogniwo (2024) are
  summary-only pages, which miss the column wrapper. A Playwright check
  (script, Haiku runs it) measures the text width on every built page of the
  literature, newspapers, places and people and lists any wider than the
  measure; all found are fixed, and the check goes into `verify_site.py`.
- **A search bar within the work** (Phase 2, scoped to the work).
- **Out**: the lines "English translation by Claude ..." (both forms, and
  their German), and the index-of-pages browser.
- **Page numbers standardised** for the literature and the newspapers: one
  marker style; the intake recognises the printed forms the texts use
  ("[720]", "s. 720", "— 720 —", running heads), so Lidmanowski's articles
  in Zdrowie get their markers. Sonnet lists every work's page-mark forms
  (grep, from a written brief); Opus rules the patterns; the script applies
  them and checks that every work's markers run in order.
- **Thumbnails**: title pages from the editor (answer 4) into
  `literature/<slug>/title.jpg`; `make_thumbs.py` takes them; a work without
  one gets the typographic tile. Haiku stages the editor's files from a
  list.
- **Three works shown in full** (`nmpol`, `slowinski2023`, `slownik`):
  `visible: true`, the entries or pages the edition uses shown whole, the
  summary rewritten without "only a summary" (Opus), the leak check of
  `verify_site.py` told which works are now shown. The copyright is the
  editor's to clear: a line in NEEDS_CONFIRMATION, not on the page.

## Phase 5. Crops

- **I. HA GR, Rep. 7 C, Nr. 3705** (script; Opus checks the two images):
  the first page (scan 0002) is cut to its right half, losing the blue
  inner cover with the archive's user slip; the last (scan 0018) to its left
  half, losing the blank page. The cut is found at the fold by a script and
  written into the holding's intake, so a rebuild on the desktop keeps it.
- **53/6/0/-/17, -/36, -/45, -/46, -/47** (17 page images in all): the
  existing fold page (`pipeline/intake/fold_page.py`) gets a **box mode**
  (draw a rectangle per page, drag its corners, arrow keys to page through,
  Save gives `crops_<slug>.json`) rather than a new review page (the
  editor's rule of 2026-10-07: no second page where one exists). It runs on
  the staged page images, so it works from the cloud too. Sonnet builds it to
  spec; the editor draws; Haiku applies the saved file
  (`courtbook.py crops <slug> <file>`, into `intake/crops.json`, read by
  `holding.py` too); Opus looks at the 17 results.

## Phase 6. The prose, rewritten to the rules (the largest part)

Opus writes every changed sentence; Sonnet only flags and checks. Changes go
into the sources of the prose (each unit's `about.md`, `unit.yml`,
`site/_data/summaries.yml`, the era, place and person YAML/Markdown), never
into built files.

1. **The holding and work descriptions** (~130 texts: the tiles, the
   holding pages, the literature, newspaper and map accounts). Sonnet reads
   each against R1-R4 and writes, per text, the sentences that break a rule
   and the questions an unfamiliar reader would ask ("stopped paying
   whom?"), to a file. Opus rewrites, reading the document where a missing
   fact has to be supplied (the documents first). 3705's "stopped paying"
   is the first.
2. **The era, place and person pages**: the same, one page at a time.
3. **The document summaries** (~640, English only), holding by holding:
   `prose_lint.py` and a Sonnet reader flag; Opus rewrites the flagged
   summaries; a second Sonnet claim-checks every changed summary against the
   document (the existing claim-check method) and Opus settles each finding.
   Because the German is skipped, the German summaries will no longer match
   the English sentence for sentence: recorded in NEEDS_CONFIRMATION for a
   later German pass.

Done over several sessions; each holding is committed as it is finished,
with the CHANGELOG line.

## Phase 7. Build, check, record

Each phase ends with `build_site_data.py`, `jekyll build`, `verify_site.py`
(Haiku runs them and reports), Playwright screenshots where the look
changed, the CHANGELOG, NEEDS_CONFIRMATION, TODO, and the lessons in
WORKING_NOTES. Publishing at the editor's word, phase by phase or all at once.

## Order

0 (rules) → 5 (3705 at once; the box page so the editor can draw while the
rest goes on) → 1 → 3 → 2 → 4 → 6. Phases 1 to 4 are code; 6 is writing and
runs last so the rewritten texts land in their new tiles. Phase 6.3 is the
longest and can run in the background of the others.

## What the editor is asked for along the way

- the crop boxes of five court books (Phase 5);
- the title pages that exist (Phase 4);
- a choice between two or three icon drawings (Phase 1);
- the word to publish.
