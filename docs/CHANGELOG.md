# Changelog

Full history of decisions and corrections applied to the corpus, database, and reports. `NEEDS_CONFIRMATION.md` tracks only what's still open — this is the record of everything already settled.

---

## Phase 1 — Structural cleanup

- Letter boundaries tagged (`[LETTER N]`), gaps and duplicate/out-of-sequence numbers documented.
- Front matter separated from the letter corpus.
- Line-wrap hyphenation (`¬`) and existing `[?]` uncertainty markers preserved as-is throughout — never rejoined or removed.

## Phase 2 — Proper noun standardization

- Full Kurrentschrift confusion taxonomy established (b/v/w, ck/ch, minim n/u/m, doubled-letter, sz/cz/s, I/J, j/y) and applied across ~230 proper-noun tokens in several rounds, root-only with grammatical endings preserved throughout.
- Key resolved clusters: Trąbczyn (confirmed real place, Konin district), Köckritz, Stägemann, Falkenhausen, Kwilecki, Schlabrendorff, Grävenitz, Knobelsdorff, Hawich, Habick→**Hawich**, Kopojno (confirmed real village), Kulm (distinct from Kolno), Sobottendorff, Rapacki, Eysenhardt, Cosmar (incl. `Casman`/`Casmus` merge from the opening letter), Metternich, Talleyrand, Scharnhorst, Ingelfingen.
- **Rule ④ full-list pass** (rare-token-vs-anchor similarity scan, 222 candidates reviewed individually): 147 tokens fixed; ~40 held back as genuine false positives — real, distinct people or common German words that only matched on letter-similarity (`Reinhardt`, `Zagorowski`, `Weidel`, and the words in the current `NEEDS_CONFIRMATION.md` list). `Prusimskische` kept throughout, per confirmation that Prusimska (daughter) and Prusimski (father) are different people.
- `Hohenlohn`/`Hohenlahn`/`Hohenlohnsche` → `Hohenlohe`/`Hohenlohesche`, all instances (16 tokens) — corrected after initially (wrongly) treating `Hohenlohn` as an accepted period variant.
- `Hinrich`/`Heinrich` → `Honrichs` where confirmed the same referent (3 tokens); letter 48's `Heinrich` (L3684) → `Hawich` instead, after cross-checking against letter 302 (its twin) at the identical sentence position — both copies of that document now agree.
- `Plenck` → `Glenck` (2 tokens).

## Phase 2b — Transcription audit (AI-transcription-aware)

Scoped as audit-first given the transcription was AI-produced, not human — see `transcription_error_profile.md` and `phase2b_transcription_audit.md` for full methodology.

- 23 narrow word-level fixes applied (mostly corrupted forms of `Durchlaucht`/`Hochfürstl`), each individually context-verified; 85 of 108 automated candidates rejected as real words or line-wrap artifacts.
- Financial figure L1625 (`14 g. 4 d.` → `14 g. 11 d.`) — proven via the estate-revenue table's own arithmetic *and* its duplicate elsewhere in the corpus.

## Phase 3 — Database, chronology, currency

- **Currency normalized**: `/m` expanded to full numbers (125 tokens); Reichsthaler-family abbreviations → `Rthl` (1,272 tokens); `d` resolved to `Rthl` where value ≥12 (131 tokens), left as Pfennig where ≤11 and following a Groschen figure (correct as transcribed); `#` → `Ducaten` (19 tokens). See `currency_normalisation_report.md`.
  - **Bug found and fixed**: a regex character-class error meant `Rthl`/`d` resolution never recognized the "Maerz" spelling of März, plus a separate gap for the "d. M." (this month) construction. 23 ordinal-day references (`5t`, `15t`, `28t`...) had been wrongly converted to currency amounts; all reverted, two of those lines' legitimate currency conversions re-applied after the revert.
  - The 12 originally-ambiguous `d` cases (§B) resolved by hand: 10 → Reichsthaler, 1 → Groschen, 1 (`2.d Preſectio`) turned out not to be currency at all — a garbled rendering of *Podprefect*, corrected to `Pod Prefecta`; `6. d.` turned out to be a corrupted `64/m`, expanded to `64000`.
  - L9997/L10008 set to `2099 Rthl 4 d` (through two rounds of correction — a Groschen guess, then a literal `rt` per instruction, then standardized to `Rthl`).
- **Month convention settled**: `7br`=Sep, `8br`=Oct, `9br`=Nov, `Xbr`=Dec — verified externally and against the corpus's own internal date sequences (see `NEEDS_CONFIRMATION.md` history / prior turns for the proof).
- **Bundled letters split** into 20 new sub-letter records after reading each candidate in full (see the table format previously in `NEEDS_CONFIRMATION.md` §E — now folded in here):

  | Original | Split into | What they are |
  |---|---|---|
  | 31, 50 | *(not split)* | Both turned out to be single continuous documents — original flagging over-matched "von Triebenfeld" mentioned in running prose, not just signatures |
  | 72 | 72a–72f (6) | Report to a third party; report to the Prince; Kreis-Rath Thiel's own enclosed letter; Brzechta's note in German (72d) and in **Polish** (72e, language-duplicate of 72d); a further report 3 months later |
  | 74 | 74a–74e (5) | A bundle of **legal documents** (court petition, two Kammergericht citations, an Ober-Landes-Gericht citation, one personal note from Triebenfeld) — not correspondence, which is why it first looked like a false positive |
  | 118 | 118a–118c (3) | Main letter (10 Feb 1804); postscript re: Countess Schlabrendorff (29 Mar 1804); a near-duplicate of that postscript (118c, `duplicate_of=118b`) — the same within-letter double-transcription pattern as 48/302, just shorter |
  | 179 | 179, 179a | Main letter; enclosure explicitly marked `179. a) Abschrift` **in the original source**, a 4-exhibit financial dossier |
  | 265 | 265a, 265b | Two unrelated petitions to two different recipients, 8 and 15 Jan 1815 |
  | 269 | 269, 269a | Main letter; enclosure explicitly marked `269 a)` **in the original source**, dated *before* the covering letter |

  Each sub-letter carries a `parent_letter` field. Database: **316 rows**, content-preservation verified lossless throughout every change in this changelog.
- **Dates**: 8 supplied, 6 inferred from bounding neighbours (basis recorded per-row), 4 corrected outliers (letters 109, 254, 186, 232 — misread years/dates), 1 from the letter-48 twin (letter 302). Letter 5 (27 Jan 1816) confirmed correct as originally parsed.
- **Collation (letters 48/302)**: `exmittirt` (not `committirt`) and `Verrechnungen` (not `Rechnung`) confirmed as the correct readings and applied to the synthesised reading text in `collation_48_302.md` — the corpus text of 48 and 302 themselves was left as transcribed throughout, since collation only ever proposed a *third*, separate reading. `Heinrich`/`Howich` → confirmed `Hawich`, and (uniquely) this one *was* applied directly to the corpus, per explicit instruction.
- **§B rare-proper-noun spellings, manuscript-checked** — all 7 resolved:
  - `Lang` → `König` (letter 16, L855; letter 64, L5026) — both genuine transcription errors.
  - `Longrich` → `Congress` (letter 280, L20229) — genuine transcription error.
  - `Aich` → `Asch` (letter 109, L8633) — genuine transcription error.
  - `Choma` (letter 17, L914) — confirmed correct as transcribed: not a different person, but the first half of `Chomanowski`, split across a line-wrap onto L915 (`nowski...`). Left untouched, consistent with the existing policy of never rejoining line-wrapped words.
  - `Wedel` (letter 96, L7651) and `Hache` (letter 59, L4563) — both confirmed correct as transcribed, no change.
- **§B, second batch** — 3 more manuscript-checked:
  - `Reinhardt` (letter 75, L6346; letter 140, L10523) — confirmed correct as transcribed, both instances, no change.
  - `Weidel` → `Wedel` (letter 77, L6471) — genuine transcription error; same person as the already-confirmed `Wedel` in letter 96.
  - `Zagorowski` → `Zagorower Güter` (letter 218, L15988) — genuine transcription error. Corpus-internal evidence was decisive: "Zagorower Güter" is the recurring name for this estate, attested 90+ times elsewhere (vs. a single `Guts` in a compound and a single `Güther` spelling-variant); `Güte` (kindness) doesn't fit at all. This is a two-word expansion, not a like-for-like root swap — word count rose by 1 as a result, checked and expected, not a content-preservation violation.

## Book cross-reference

The 2018 Seidel biography (`Friedrich Ludwig, Fürst zu Hohenlohe-Ingelfingen`) was confirmed as an active reference source for the project. It's sourced from the Hohenloher Zentralarchiv Neuenstein (HZAN) — almost certainly the same archive this correspondence was transcribed from — and its Appendix 6 is a scholarly transcription of the exact same 7 March 1809 Kontopp letter as the corpus's letter 48/302 pair, making it a genuine third witness for that letter specifically.

- **Investigated and closed**: whether `Hawich` and `Honrichs` had been wrongly merged. They hadn't — the two already co-occur as clearly distinct people dozens of times throughout the corpus, and the one place they were ever conflated (letter 48, L3684, a `Heinrich`→`Hawich` fix from an earlier round) is independently confirmed correct by Appendix 6's identical sentence.
- **Investigated and closed**: the book spells this recurring fraudulent-Sequestor figure `Henrichs`, raising the question of whether the corpus's ~100+ `Honrichs` instances (including the 3-token `Hinrich`/`Heinrich`→`Honrichs` normalization at letters 43/179/284) were systematically wrong. Confirmed `Honrichs` is correct — the book's `Henrichs` is the biography author's own editorial spelling choice, not an authoritative period rendering. General takeaway: the book's proper-noun spellings are not treated as authoritative over the corpus's own internal evidence, particularly for Polish place names (flagged by the user in advance) but evidently for German names too.
- **No corpus edits resulted.** `Honrichs` and `Hawich` both stand as already fixed.
- §A (`23000`/`32000` Rthl) is independently corroborated by Appendix 6's `23000 Rth` reading (matching letter 48) but this is **not** being used to resolve it — the user is checking the original manuscripts directly for that one.
- Broader book integration (who's-who index, estate/property cross-reference, chapter-to-letter-date map) declined for now; revisit later if wanted.

## Liquidation register added (letter 303)

`Auszug aus Den Fürstlich Hohenloheschen Liquidations Protocollen.xlsx - Edit.csv` — a 142-entry creditor register (undated) — was added to the project and integrated so it's searchable alongside the letters.

- **Names standardized** against already-decided project canon (established fixes only, nothing new invented for this document): `Bornstaedt`→`Bornstädt`; `Stoessel`→`Stössel` (×2, plus the adjectival `Stoesselschen`→`Stösselschen`); `Koekritzschen`→`Köckritzschen`; `Schlabendorffschen`→`Schlabrendorffschen`. Everything else in the register — the large majority of the 142 names — has no established form in this project (they don't otherwise appear in the letters), so was left exactly as transcribed; existing `[?]` uncertainty markers (2, on rows 5 and 62) preserved as-is.
- **Added to the corpus** as `[LETTER 303]`, appended at the end of the archival text file, each row rendered as one line (`N. Name — Gold X Rthl Y g Z d; Courant X Rthl Y g Z d`), using the same `Rthl`/`g`/`d` units already standard throughout the letters. The Gold/Courant distinction (two different period Reichsthaler denominations) is preserved exactly as given, not collapsed into one figure. Append-only edit — nothing in the existing corpus was touched; word count and line count both grew by exactly the amount added.
- **Added to the database** as record 303 (317 total now), with a new `doc_type` column (`letter` for all prior records, `register` for this one) so it's distinguishable in queries. No date in the source — `date_precision=unknown`, `date_source=none`, same convention as the 5 undated/missing letters, sorts to the end of the chronological reading copy.
- Content-preservation and chronological-ordering checks re-verified after the addition (317 records, archival/chronological content line sets identical).

## Who's-who reference

`whos_who.md` added — every person named in the letters (and the letter 303 register), cross-referenced against the biography for identity where possible. Each entry is labeled by evidence type: externally confirmed (real, independently documented historical figures, from Phase 2's Tier 1/2 research), book-confirmed (matched to the Seidel biography), context-inferred (a role guessed from how the letters/register describe the person, always flagged as uncertain rather than stated as fact), or role unclear. People who appear only in the book, not in the letters, are excluded per instruction. ~65 people individually profiled; the register's remaining ~134 one-off creditors listed using their own stated professions only, no further research.

Two things worth follow-up, both left open rather than resolved:
- **Possible family link**: the book's Ch. 2.3 concerns "Marianne Gräfin von Hoym," the Prince's own wife's birth family. The letters separately discuss a "Minister/Graf Hoym" (8 occurrences) and the register lists a "Fr. Gräfin Höym, geb. v Tauenzien" as a creditor — surname, era, and rank line up, but the letters never state the connection explicitly.
- **Unresolved identity**: `Wedel` (letters 77/96/98) sits next to "Hoyms und Wedells" in letter 98, suggestive of a real contemporary Prussian official (Karl von Wedell), but not confirmed — the book's one `Wedel` hit is in an unrelated chapter.

## Who's-who update — Prusimska/Dąbska identity confirmed

User-provided identification: **Michalina Prusimska**, daughter of Antoni Prusimski (original owner of the Trąbczyn estates), later married and became **Dąmbska/Dąbska**. This directly matches text already in the corpus — L1858 (letter 28, 1807-10-05): "der Frau v Dąbska gebohrnen v Pru[simska]" ("née Prusimska") — and resolves what the who's-who had flagged only as an unconfirmed family link.

Checking the dates of every Prusimska/Dąbska mention surfaced a further pattern: `Dąbska` is used consistently 1807–1811, then from late 1814 the letters instead use `Moscinska` / describe her husband as a Moszyński, with letter 266 (Jan 1815) hedging "Dąbska oder Moscinska" — exactly the line Phase 2 had flagged as possibly reflecting genuine period uncertainty rather than a transcription error. This chronology-based hypothesis of a second marriage was flagged to the user and **confirmed**: her second husband's real surname was **Miączyński**, not "Moscinski"/"Moszynski" as the letters render it — an error made by the original letter-writers themselves, not the AI transcription. Per project policy (only transcription errors get corrected, not period scribal/writer errors), the corpus text is left exactly as written; the correct identification is recorded in `whos_who.md` instead. No corpus text was changed — `Prusimska`, `Dąbska`, and `Moscinska` are genuinely different words the original writers used for the same person at different points in her life, not transcription variants of one name.

## Web edition — Phase A (foundation)

A Jekyll site in `site/`, built to deploy to GitHub Pages with no custom plugins (Pages runs Jekyll in safe mode, which ignores them). Everything dynamic is either pre-generated by Python or done client-side in dependency-free JavaScript — no CDN, no external requests, so the site behaves identically offline and deployed.

- **`build_site_data.py`** (new) generates all 317 letter pages, `_data/people.yml`/`places.yml`/`stats.yml`, and the client-side search index from `letters.json`. Rerunnable; the corpus is never touched. It **asserts character-exact fidelity** and refuses to finish if any page's text differs from the corpus.
- **`verify_site.py`** (new) checks the *built* site: every record has a page, every page's diplomatic text matches the corpus exactly, every internal link resolves, and no page references an external host. Currently: 317/317 exact, 6,201 links resolve, 0 external dependencies.
- **Two text views per document.** *Diplomatic* is canonical and default — original line breaks, `¬` marks and `[?]` flags all intact. *Reading* flows lines into paragraphs; it is generated for legibility only and never stored as truth.
  - The reading view joins a broken word only where evidence is unambiguous: at `¬`, and at a word-attached hyphen whose continuation starts lower case. Line-final hyphens followed by a capital were checked against the corpus and turned out to be genuinely mixed — real compounds (`Haupt-`+`Ersaz`) alongside the writer's habitual punctuation dash — so they are left exactly as written rather than silently merged.
- **Faceted browse** with instant client-side filtering (year, person, place, condition, date certainty) and full-text search that is diacritic- and long-s-insensitive, so `Trabczyn` finds `Trąbczyn`.
- **Timeline** combining letter-density per year, historical events from the biography's Zeittafel and chapters (each with its citation), and the six narrative movements. Events live in `_data/timeline.yml` for easy extension.
- **People and Places indexes** generated from the corpus, with per-person occurrence counts and links to every appearance.
- **"About this edition"** page documenting the AI-transcription provenance, every editorial mark, the four ways documents are dated, the currency system, the bundled/duplicate documents, and what remains unresolved.
- **Translation scaffolding** in place: the letter layout renders `_data/translations/*.yml` with a status badge when present, and says plainly that a document is untranslated when not. Nothing about translation touches the canonical corpus.
- **`.gitignore`** added at the project root that excludes the copyrighted Seidel biography from any future repository, alongside build output and backups.

Bug caught during verification and fixed at source: Liquid treats the empty string as *truthy*, so empty metadata fields were rendering "part of letter", "duplicate of letter ␣", and a false `[supplied]` badge on every page. The generator now emits real YAML nulls for absent values.

Still to come: theme tagging pass with review report (Phase B), translations (Phase C), publication (Phase D — gated on the archive-permissions question).

## Line-break resolution and the page-based three-view edition

The transcription's word-continuation marks turned out to be unreliable, which blocked any readable text. Of the **1,314** line-end marks in the corpus, **484 (37%) join nothing** — `die¬`+`serhalb` really is *dieserhalb*, but `die¬`+`nöthigsten` is two words and the mark is simply an error.

- **Every mark decided on evidence**, not assumption (`resolve_linebreaks.py`). Two sources: this corpus itself (which knows period spelling), and the **DWDS frequency API** — lemma-aware, so inflected forms resolve (`Mitgliedern` → *Mitglied*, 12.0M hits), and covering historical German. A modern offline dictionary was rejected as unfit: it misjudges `laßen`, `nöthigsten` and the long-s forms. Threshold for "real word" set at 1,000 corpus hits, chosen from the observed gap between real words (thousands to millions) and proper-name noise (`denich` 414, `derdurch` 41). Lookups cached to `dwds_cache.json`, so re-runs are free and offline.
- **Result: 825 joins, 484 non-joins, 5 catchwords, 19 flagged** for checking against the originals — down from 527 unresolved when corpus evidence alone was used.
- **Catchwords discovered.** Five pages end with the scribal habit of writing the next page's first word at the foot of the current one (133 `Con¬`→`Contract`, 140 `Vor-`→`Vorwerk`, 168 `Win¬`→`Winnickischen`, 177 `be¬`→`benennung`, 235 `ver-`→`verliehren`). Joining these would manufacture "ConContract". They stay in the diplomatic view and are dropped from the reading copy.
- **Two possible lacunae found** while reading the cross-page cases: letter 223 has `Güter ange¬` never completed, and `entweder ver¬ / oder aufgegeben` missing its word — both recorded in `linebreak_report.md`. Letter 136's `Collo¬`+`Mitten` is almost certainly a mis-transcribed *Collonisten*.
- **`linebreak_decisions.csv`** — one row per wrap with the full evidence, **hand-editable**. Change a `decision` cell and regenerate; nothing is buried in code.

**Structure: letters are now made of pages.** The corpus's blank lines (page breaks preserved back in Phase 1) yield **913 manuscript pages**. The letter remains the unit of navigation, citation and search — pages are structure inside it, so text always stays beside the right scan when images are added. Each page carries a `scan` slot, empty for now, so adding images later is a data change rather than a re-architecture.

- **Three views** on the site: *Diplomatic* (one line per manuscript line, numbered to the archival file, marks intact — canonical), *Reading* (wraps resolved, lines flowed, never the text of record), *English* (per page, empty until translated).
- **New artefacts**: `von_Triebenfeld_..._reading.txt` (generated fair copy, every page labelled with its archival line range), `pages.csv` (one row per manuscript page, ready for scan matching), plus `text_reading`/`pages`/`n_pages` in the database.
- **`build_db.py` moved out of the temporary session scratchpad into the project**, so the whole pipeline is durable and self-contained.

The archival text was **not touched**. Verification enforces it: pages must reconstruct each letter, the reading copy must contain the same letters in the same order (catchword pages excepted by design), and every built page must reproduce its archival lines character-for-character. All pass — 317 letters, 913 pages, 6,201 internal links, zero external fetches.

## Matching scans to transcribed pages

`pages/` holds 874 curated JPEGs (1.08 GB) against 913 transcribed pages — a 39-page shortfall to explain.

- **The gap is not missing scans.** Blank images (blank versos, unused spread halves) were deliberately deleted before this work, so 146 captures have a pruned counterpart — expected, and documented rather than flagged as damage. But pruning cannot cost a transcript page: a blank page was never transcribed. The real cause is **over-segmentation of the transcript**.
- **38 short blocks are almost certainly not page breaks** — against a shortfall of 39, which essentially closes it. They are datelines (19), signature blocks (7), salutations (4) and other very short fragments (8) that the transcriber set off with a blank line; Phase 1 read every blank line as a page break and turned each into its own "page". Examples: `Wien d. 6ten May 1815.`, `treu unterthänigsten Diener v Triebenfeld`, `Gnädigster Fürst und Herr!`. **The fix belongs in the corpus** (remove the blank line), not in the mapping.
- **`match_scans.py`** aligns captures to letters by dynamic programming, minimising per-letter page-count mismatch while preserving order and treating each capture as atomic. Result: 856 pages matched, 57 gaps, 18 surplus images, all 874 images assigned, none twice, capture order strictly increasing.
- **`scan_inventory.md`** — capture composition, the pruning record, the 38 not-a-page-break candidates with their blank-line positions, and the per-letter excess list.
- **`page_scan_map.csv`** — one row per transcript page with its proposed image; hand-editable, and the file the pipeline will read.
- **`scan_review.html`** — a standalone reviewer opened by double-clicking. Shows each page's text beside its proposed image, referencing `pages/` **in place** so the 1.08 GB is never duplicated. Four actions per row (confirm / no image / drop image / merge into previous), corrections re-flow the alignment live, state persists in the browser, and "Copy as CSV" round-trips back into the map. The 38 suspects are highlighted, and merges are collected separately because they are corpus fixes rather than mapping fixes.

- **Anchoring** added to the reviewer: type the letter an image actually belongs to, and it pins that image to that letter's first page while everything downstream re-flows to follow. This makes the corpus fixable by jumping to any point, stating one known fact, and letting the sequence fall into place — rather than clicking through 900 rows in order. Anchors are keyed by filename so they survive re-alignment, and the reviewer reports the two failure modes: an anchor that would reuse already-assigned images (flagged as a conflict) and one that strands images (visible in the leftover counter). Verified against the generated file with Node: JS parses, anchoring shifts downstream letters as intended, and both failure modes are caught.

- **Front matter (`0`)** — entering `0` marks an image as belonging to no letter at all (the series title page). It leaves the sequence entirely, so everything after shifts up by one, and it is held in a panel with thumbnails and a *Put back* button rather than being discarded. Exported with status `front_matter`.
- **Proposing new letters** — typing an ID the corpus doesn't have (e.g. `1a`, when the scans show transcript letter 1 is really two documents) records it as a **proposal** rather than an anchor, because the corpus has no pages for it until the text is split. Proposals collect in their own panel showing which existing letter and page the image currently sits in, and export with status `starts_new_letter` plus a `new_letter` column. A new sub-lettered ID whose base number doesn't exist (a likely typo, e.g. `9999a`) prompts for confirmation instead of being silently accepted.

**Sequencing note for the splits:** applying a proposal means inserting a `[LETTER 1a]` tag at the right line of the archival text. Everything downstream then re-derives itself — `build_db.py` re-splits pages on blank lines, re-parses the date from the letter's own text, and assigns `parent_letter` from the ID, exactly as it already does for the 72a–72f and 179/179a splits. No separate date entry is needed unless the parser gets it wrong.

Letter 9 (missing in the archive) and letter 303 (the register, from a different source) are correctly excluded from matching rather than forced onto images. Nothing in the corpus, database or `pages/` was modified.

Still to come: apply confirmed merges to the corpus, then fill the `scan` slot in `build_db.py` and generate web-sized derivatives (~130 MB) for publication.

## Scan review applied to the corpus

The visual review of all 872 images against the transcript produced its first round of corrections, now applied. The archival text was edited only by adding four letter tags and removing four blank lines — **no letter text changed**, verified by comparing the 20,756 non-tag content lines before and after (byte-identical).

**Two letters split** — the scans showed one archival number holding two documents. Boundaries verified individually: each follows a dateline or signature and opens with a fresh salutation.

| New letter | Split from | Evidence |
|---|---|---|
| **1a** | letter 1, at line 67 | previous ends *"Schlawenschitz den 29ten Januar 1815"*; new opens *"Durchlauchtigster Fürst"*. Dateline *"Wien d. 12. in Febr. 1815"* — the parser caught month and year but not the day, so **12 Feb 1815** is supplied. |
| **72 / 72a** | old 72a was two documents | pages 1–4 address the *Kriegs- und Forstrath* (now letter **72**); pages 5–8 open *"Durchlauchtigster Fürst"* (now **72a**). The bare number 72 finally has a record, so the sub-letters' parent link resolves. |

Two further splits were made and then **reverted at your instruction**: `13a` (letter 13 stays whole) and `20a` (letter 20 stays whole, its enclosed *Abschrift* to the banker van der Lahr remaining part of the letter). Removing the tags restored both letters exactly — the blank lines that had preceded the tags went back to being ordinary page breaks, and the letter text was never touched.

**Four page merges applied** — blank lines that were separating a dateline or signature from its own page, not marking a page break: letters 146, 237, 254 (merge into previous) and 303 (the register's title line, merge into next).

**Findings recorded rather than silently absorbed** — see `NEEDS_CONFIRMATION.md` §E–§H: 9 scanned pages with no transcribed text (including four consecutive sheets, captures 0543–0546, at the very end of the Büschel), 1 transcribed page with no scan (letter 231 page 2), 6 images excluded as front matter or not-pages, and a mis-transcribed year in letter 237 (`1873` for 1813).

Result: **318 documents, 862 pages, 872 images.** All verifications pass — pages reconstruct their letters, reading copy lossless, every archival line character-exact on the site, 6,214 links resolve.

## Scan mapping completed

The image-level review decisions were moved out of browser storage and into **`scan_decisions.json`**, which `match_scans.py` now reads. They therefore survive every regeneration, and the reviewer opens on the corrected state instead of resetting to naive folder order.

Recorded: 1 front-matter image (`0001_a`, the series title page), 5 images that are not manuscript pages, 1 image left untranscribed on purpose (`0345_a2` — a list of calculation figures only, **not** a missing page; the reason is stored in the file's `notes` so it can't later be mistaken for a gap to fill), and a corrected reading order — `0345_a2` before `0344_a1`, where a spread's halves had been photographed across two captures.

**The mapping is now complete and fully accounted for:**

| | |
|---|---|
| Images | 872 |
| Paired to a transcript page | 865 |
| Set aside with a stated reason | 7 |
| Unexplained surplus | **0** |
| Pages with no image | 4 — letters 121, 181, 225, 293, the archive's own missing numbers |

Splitting letter 303 into 9 pages resolved the long-standing tail surplus: the trailing captures 0543–0546 turned out to be the register's own pages, not untranscribed documents. `NEEDS_CONFIRMATION.md` §E and §F have been narrowed accordingly.

Two markers in the export were **deliberately not applied** — the proposed splits `13a` and `20a`, which had been made and then reverted at your instruction. Anchors persist in the browser by filename, so they re-exported; re-applying them would have silently undone the reversion.

Verification was tightened rather than relaxed to accommodate the custom order: the mapping is now checked against the *intended* sequence (folder order, or the corrected order when one is recorded), with front matter, drops and no-text images excluded from that check since they sit outside the sequence by design.

## Letter 237's year corrected

The dateline had been transcribed `d. 29ten April 1873` — impossible, and previously worked around with a supplied date of 29 April 1813. You corrected the digit in the archival text, so **the supplied-date override was removed**: the parser now reads 1813 from the manuscript itself (`date_source: signature` rather than `supplied`). One fewer manual override masking what the text actually says.

`NEEDS_CONFIRMATION.md` was then trimmed to the three genuinely outstanding items — the 23,000/32,000 discrepancy, the 224 uncertainty markers, and the 5 damaged blocks — with the resolved sections folded into this changelog. Two of the three are now far more tractable than before: since every page has a matching scan, checking an uncertain reading or a damaged block is a matter of looking at the image rather than hunting for it.

## Scans wired into the edition

**Images renamed** to be ASCII and self-describing, so URLs no longer carry an encoded `ü` and spaces:

```
Oe 1_Bü 9454_0343_a1.jpg   ->   Oe_1_Bu_9454_0343_a1-L179a_04.jpg
```

`<signature>_<capture>_<crop><half>-<label>`, where the label is `L{letter}_{page}` for a mapped page, or `front` / `notext` / `notapage` for the seven set aside. The capture and crop still carry the archival identity, so nothing is lost, and **`scan_rename_map.json` records every original name** — the rename is fully reversible. All 872 renamed in one pass via temporary names so a rename could never clobber an existing file; zero collisions.

**Web derivatives** — `make_scan_derivatives.py` produces 1100px copies into `site/assets/scans/`: **231 MB**, against 1.08 GB of originals, generated in under a minute. 1100px was chosen after measuring three widths; it reads Kurrentschrift comfortably and sits well inside the GitHub Pages limit. Re-running skips anything already current. **`pages/` is now gitignored** — the full-resolution originals stay local as archival masters and are never published.

**Two panes per manuscript page** — the scan on the left, its own text on the right, so image and transcription sit together rather than being toggled between. The image stays in view while its page's text scrolls. Tabs now switch only the text (Diplomatic / Reading / English), and a *hide scans* checkbox gives the text full width for straight reading. Both preferences persist between letters.

**The reviewed pairing is now the source of truth.** The mapping had been *recomputed* on every run by pairing pages and images sequentially — so it kept drifting away from what had actually been checked by eye. That was the wrong architecture: a pairing established by looking at the scans is evidence, not something to re-derive. `scan_decisions.json` now holds `pairs` (865 page→image assignments) and `gaps` (4 pages confirmed to have no scan), taken from the review and applied verbatim. Only pages the review doesn't cover fall back to sequential fill.

This came out of a real misalignment: letter 48's second page was showing the wrong scan. The cause was a rule I had added that **assumed** archival numbers recorded as missing could have no scan, so numbers 9, 121, 181, 225 and 293 were made to take no image. Four of those were right — but **letter 9 does have a physical page behind it**, as the review recorded, and skipping it shifted every pairing after it by one. An assumption about the archive was overriding an observation of it.

**Letter 303 was also still flagged as "not part of this Büschel."** The scans disprove it: the trailing captures are the register's own pages. It now takes images like any other document, and all nine of its pages have one.

**Filename labels made self-maintaining.** The `-L<letter>_<page>` part of each filename is *derived* from the mapping, so fixing those two bugs left 846 of 864 labels stale and actively misleading. `relabel_scans.py` recomputes them from `page_scan_map.csv`, renames via temporary names, and carries `scan_decisions.json` and `scan_rename_map.json` across. It runs in report-only mode at the end of every `regenerate.py`, so drift is caught rather than discovered later; renaming stays a deliberate `--apply`.

Verification extended, and now includes the check that matters most: **every built page is compared against the reviewed pairing**. Currently 865 paired images, **0 of 865 disagreeing with the review**, zero label disagreements, zero missing files, 7,943 links resolving, archival text character-exact.

## The transcription layer replaces the diplomatic view

The first view is now **Transcription**, not Diplomatic: the manuscript's own line breaks are kept, but the line-end marks are resolved. Where a word really is broken it carries a plain hyphen (`abge-` / `nommen`); where the mark was spurious it is gone. The rename matters — a corrected text should not be called diplomatic — and `About the edition` now sets out what has been changed and why.

The archival text is untouched and still canonical. A build-time check enforces the relationship: the transcription may differ from it **only on lines carrying a recorded decision, and only in the line-end mark, never in a word**. Anything else fails the build.

**Three orphan marks found** while adding that check — `¬` on a line whose next line holds only figures, so there is nothing to continue into (two are table rows, one a dateline). They had fallen through the wrap collector entirely and had no decision at all. They are now a category of their own, `orphan`, and the mark is removed.

**A verification bug of my own, caught and fixed.** The new check used variable names `a` and `b`, shadowing the outer variables holding the archival-vs-chronological comparison. That silently reduced a 20,750-line check to a 13-line one comparing a page against itself, and reported "identical content: True" on the strength of it. Renamed, and the real check restored.

## Spelling audit — report only, nothing applied

`spelling_audit.py` looks for demonstrable transcription slips in ordinary words. The bar is deliberately high, because **63% of the distinct words here appear exactly once** and the text is full of correct period forms (*laßen*, *seyn*, *nöthig*, *Ewr*). A candidate must be rare here, have a near neighbour at least 10× more common, differ by a confusion this transcription is known to make, and be unknown to DWDS while its neighbour is attested.

Getting to a usable list took three passes, and the discards are worth recording:

- **1,131 candidates** at first — mostly junk. Any four-letter word is one edit from *und*, *die*, *der*, so `dire` (French), `Rich.` (an abbreviation) and `Diet` (a surname) were all "corrections".
- **Tightened** to a six-letter minimum, eight for dropped/added letters → 335, but now dominated by **German inflection**: `Fürstens` (genitive) and `hochfürstlicher` (dative) are correct, not errors. Differences confined to a final *e/n/r/s/m* are now excluded as grammar.
- **Checked each survivor against DWDS** → any rare form that is itself a real German word was dropped: *Kasten* is a box, *erkalten* is to grow cold.
- **Two faults in my own word extraction**, each inventing errors: a stray diacritic split `şondern` into `ondern` (proposed as a slip for *andern*), and line-wrap fragments were counted as words (`Nachrich-` proposed as a slip for *Nachricht*).

**106 candidates** remain, and the strong ones are unambiguous — `Durchaucht` → *Durchlaucht*, `Grädigster` → *Gnädigster*, `Schreibn` → *Schreiben*, `erſterebe` → *ersterbe*, `Geſehichte` → *Geschichte*. Some still need your judgement: `Antworth` may simply be period spelling. See `spelling_audit.md`; nothing applied at this stage — the accept/reject pass is the next section.

## Spelling audit — applied

The 106 candidates from the report above were read one by one against the manuscript context. **66 accepted, 40 kept.** The 66 touch 72 token instances (six forms — `Triebenfeldt`, `Schreibn`, `Fürstern`, `gestandt`, `umsamehr`, `Liefster` — occur twice). Applied root-only to `von_Triebenfeld_Hohenlohe-Ingelfingen_cleaned.txt`, one pinned `(line, whole-word old → new)` at a time, backup at `von_Triebenfeld_Hohenlohe-Ingelfingen_cleaned.txt.bak5`, then `regenerate.py`: transcription still differs from the archival text only on decided line-end marks, reading copy lossless, 20,750 archival lines = 20,750 chronological lines, every built site page character-exact.

What went in: corrupted honorifics and formulae (`Durchaucht`→*Durchlaucht*, `Grädigster`→*Gnädigster*, `Durchlauchtigter`→*Durchlauchtigster*, `Liefster`→*Tiefster* ×2, `erſterebe`→*ersterbe*); place and person names against project canon (`Schlawerschitz`/`Schlawentschitz`/`Schlowenschitz`→*Schlawenschitz*, `Worſchau`/`Warschan`→*Warschau*, `Triebenfeldt`→*Triebenfeld* ×2, `Brzechsa`/`Berzechsta`/`Brezechsta`→*Brzechsta*, `Zagorowa`→*Zagorowo*, `Zerbani`→*Zerboni*, `Palajewo`→*Polajewo*, `Königberg`→*Königsberg*, `Scherck`→*Schenck*); the recurring excrescent-*r* cluster (`Fürstern`/`tiefstern`/`höchstern`/`Sonstern`/`Bemühern`/`einreichern` → *-en*); single visual confusions producing non-words (`ſerden`→*senden*, `wünden`→*würden*, `läglich`→*täglich*, `Nußland`→*Rußland*, `geweldet`→*gemeldet*, `geſchieben`→*geschrieben*, `Geſchiehte`/`Geſehichte`→*Geschichte*, `Augenblik`→*Augenblick*, `glüklich`→*glücklich*, `dardurch`→*dadurch*, `wordurch`→*wodurch*, `bestehnt`/`bestreht`→*besteht*, `getrettet`→*gerettet*, `gesanndt`/`gestandt`→*gesandt*, `Sequestation`/`Sequetration`→*Sequestration*, `Hypoteque`→*Hypotheque*, `Wechſtel`→*Wechsel*, `Intresen`→*Intressen*, `Expresen`→*Expressen*, `Comision`→*Commission*, `Revenuce`→*Revenue*, `Triebunal`→*Tribunal*, `Mandatorius`→*Mandatarius*, `Cuhrischen`→*Curischen*, `Hoffroth`→*Hofrath*, `Geheimte`→*Geheime*, `konzler`→*kanzler*, `durchlaus`→*durchaus*, `Scharden`→*Schaden*, `ſehleunig`→*schleunig*, `angewiſen`→*angewiesen*, `umsamehr`→*umsomehr* ×2, `Antworth`→*Antwort*, `vorgesten`→*vorgestern*). `gnädigter` at L263 had two proposed corrections in the report (`gnädigster` / `gnädiger`); the set salutation `gnädigster Fürst und Herr` was applied.

What was kept (full table with reasons in `spelling_audit.md`): valid period forms the automated inflection filter missed — `hiedurch`, `geschiehet`, `kleinern`, `urtheilt` (a finite verb), the `-ff`/`-fft` orthography (`verkauff(en)`, `zukunfft`, `dürfften`, `geworffen`, `herrschafft`), `gezahlet`, `gebetten`, `hochwolgeb` (`wol`), `creditorn` (syncope, parallel to `andern` in the same clause); cases where the report's proposed target is wrong or ambiguous — `vesten` = *Vestungen*/*Festungen* not *besten*, `durcht` = *deucht*/*dünkt mir*, `wenschen` = *Wünschen* at L36 but *Menschen* at L47, `gewinnten` = *gemeinten*, `klogen` = a place name, `desten` = *dessen*, `commer` = *Cammer* or a surname, `unglückt` → *unglückliche*; line-wrap fragments — `geleiste` (+ `ten`) = *geleisteten*, `hochfürst` (+ `laucht`) = *Hochfürstl. Durchlaucht*; a source dittography (`vorgestern vorgesteren`, L73); and several readings the surrounding text is too garbled to settle (`gnädigte`, `gewißert`, `weines`, `wohren`, `kurgen`, `eingericht`, `gesundtheit`, `ewodurch`). The two address-honorific variants `hochwohlgebohrnen`/`hochwohlgebohrn` were left as possibly deliberate.

## Name catalogue — built, adjudicated, first batch applied

`name_catalogue.py` (new) catalogues every person and place name and its variant
spellings. Names defeat the spelling audit's assumptions — 527 of the 738 tokens in name position occur exactly once, so frequency proves nothing; a wrong name still looks like a name; and plain edit distance is the wrong metric (`Köckritz`/`Koekritzsch` are four edits but one misreading apart, `Wien`/`Bier` one edit apart and unrelated). So it seeds from the settled canon in `whos_who.md` and `CHANGELOG.md`, strips German derivational morphology before comparing (`Cosmarischen`, `Zagorower` are inflections, not rival spellings), and matches with a Kurrent-weighted distance scaled to name length. Output: **267 names, 206 proposed variants, 21 one-entity-or-two decisions, 18 withheld as ambiguous**, each row carrying its scan filename for checking in `scan_review.html`.

**Two method errors found and fixed while building it**, both worth recording:
- The "is this an ordinary noun?" test was *"does it ever appear lowercase"* — meaningless in German, where every noun is capitalised. That admitted `Geld`, `Gott`, `König`, `Ende` as "names" and produced 1,706 junk proposals. Replaced with an explicit `NOT_NAMES` list of the prepositional-idiom nouns that ride in on "zu X"/"nach X" (`zu Gunsten`, `zu Füßen`).
- This register writes **articles with surnames** (`dem Hawich`, `der Cosmar`), so an article-rate test can only *veto* a candidate, never nominate one. The settled canon therefore has to be trusted outright rather than re-derived — it carries exactly the names the statistics cannot see.
- A third gap: two names that are *both* common are never compared, which is how `Brzechsta` (36) and `Brzechta` (8) sat side by side unnoticed. Added a seed-pair section; nothing there is ever auto-merged.

**Precision was poor in the discovered-seed tier.** Of ~25 proposals checked against the manuscript, about 20 were wrong (`Eines`→`Einer`, `Pforte`→`Pferd`, `Schriften`→`Schritte`, `Schweizern`→`Schweiner`, `Coeln`→`Cosel`…). Every fix anchored on a canon name held up; the failures all came from statistically-discovered seeds. Next pass restricts proposals to canon-anchored names and treats discovered seeds as review-only.

**Adjudicated in full — see `name_decisions.md`.** Canonical forms settled: `Brzechsta`, `Kalisz` (absorbing `Kalicz`/`Kaliz`/`Kalisch`), `Hardenberg`, `Krotoszyn`, `Napoleon`, `Triebenfeld`, `Hohenlohe`, `Petersburg`. **`Wrąbczyn` confirmed a separate place from `Trąbczyn` — never to be merged.** `Swięcier` confirmed a legitimate inflection of `Swięcia`. `Werthe`, `Wirth`, `Bedeutung`, `Eines`, `Inneres` dropped as seeds — not names.

**21 corrections applied** (backup `…cleaned.txt.bak6`, all regeneration checks green, 20,750 archival lines, every site page character-exact): `Extaffette`→`Estaffette` ×5 (*estafette*, a courier — long-s read as x), `Curant`→`Courant`, `Appete`→`Oppeln`, `Bengelin`→`Beugelin` ×3, `Moszincka`→`Miączyńska`, `Plate`→`Pluto`, `Plaß`→`Paß`, `Panie`→`Panin`, `Unger`→`Ungar` (Hungarian *wine*, beside Champagner — not a person), `Kálitz`→`Kalisz`, `Napolien`→`Napoleon`, `Tribenfeldschen`→`Triebenfeldschen`, `Sakkin`→`Sacken` ×3.

`Sakkin` was resolved against the Seidel biography on explicit instruction — it uses `Sacken` ×55 and names the woman herself, *"Fürstin Christiane Charlotte Sophie von der Osten-Sacken (1733–1811)"*, matching L18192's reference to her after her death. The corpus's own `Sakken` ×4+ was **not** merged into `Sacken`: standing policy is that the book's spellings are not authoritative over the corpus's internal evidence, so that stays open.

Still open: `Holländer`→`Hauländer` on the three settler-context lines only (L216's *"die Hauländer oder Collonisten"* settles the term; the military `Holländer` and the country `Holland` are correct), `Schlawen` vs `Schlawenschitz`, `Stege`, `Franckfurten`, and `Märck` — where `Märkische Landschafts-Obligationen` is a real instrument and the form may be a correct abbreviation.

## Name canonicalisation — §H merges applied

The seven canonical forms you settled, plus `Sakken` → `Sacken`, applied as **64 substitutions** (backup `…cleaned.txt.bak7`; regeneration clean, 20,750 archival = 20,750 chronological lines, every site page character-exact).

`Sacken` 7→17 · `Brzechsta` 36→47 · `Kalisz` 44→59 · `Hardenberg` 26→32 · `Krotoszyn` 40→43 · `Triebenfeld` 326→329 · `Hohenlohe` 39→45 · `Petersburg` 3→10.

Absorbed: `Sakken`/`Sakkensche(n)` ×13, `Brzechta` ×8 + `Brzechffa`/`Brzechtsa`/`Briechsto`, `Kalicz` ×5 + `Kaliz` ×4 + `Kalisch` ×4 + `Kalis` + `Kaliszž`, `Hardenburg` ×6, `Krotoszin` ×3, `Treibenfeld` ×3, `Hohenlose` ×5 + `Hoferlohn`, `Peterbourg` ×6 + `Petersbourg`.

**Deliberately not merged — `Kalisch` is doing double duty.** Four occurrences are the city as a bare noun (`zu Kalisch`, `in Kalisch`) and were merged; **eight are the German adjective** — `Kalischen Krieges und Domainen Cammer`, `Kalischer Regierung`, `Kalischen Tribunal` — which is correct derivation from `Kalisz`, exactly like `Zagorower` and `Cosmarischen`. Merging those would have produced non-German. `Kaliszer` ×1 kept for the same reason, and `Brzechſta` (long-s) was already canonical. A `keep_derivations` list now guards these.

**`Sakken` → `Sacken` resolved on instruction to follow the biography**, which uses `Sacken` ×55 and names her outright — *"Fürstin Christiane Charlotte Sophie von der Osten-Sacken (1733–1811)"*. This is a deliberate, instructed exception to the standing policy that the book's spellings are not authoritative over the corpus's own evidence.

**`name_rulings.json` (new) makes the catalogue an outstanding-work list.** Every ruling — applied, rejected, dropped-as-seed, settled-pair, locked-apart, keep-derivation — is recorded there, and `name_catalogue.py` suppresses it on rebuild. Nothing already decided is put to the reviewer twice. The file is append-only by design: removing an entry re-opens a settled question. Catalogue now stands at **167 proposed variants across 83 names, 6 one-entity-or-two pairs, 5 withheld** — down from 206/21/18.

## Archival letter numbers removed from the letter bodies

Most letters opened with a line carrying nothing but the document's own number — `48`, `257` — written on the manuscript. Redundant now that every record carries a `letter_id`, so **298 such lines were removed from the archival text** (backup `…cleaned.txt.bak8`).

Only the line immediately following a `[LETTER n]` marker was eligible, and only when it was nothing but a document number. **293** matched their letter id exactly; **5** did not and were removed on explicit instruction — `74`, `118`, `265` (parent numbers standing at the head of split sub-letters) and the two enclosure markers `179. a)` and `269 a)`. **20 letters were untouched**: the split sub-letters that never carried a number (`1a`, `72a–f`, `74b–d`, `118b/c`, `265b`) and the `(missing)`/`(skipped)` placeholders.

**Page structure was the risk, and it was checked rather than assumed.** `corpus_pages.split_pages` divides on blank lines, not on these number lines, so removal should be structurally inert — the strip script simulated the page split before and after and refused to write unless the count matched. It held: **869 pages before and after**, 318 records, and the re-derived line-break decisions came back identical (483 split, 825 join, 3 orphan, 5 catchword). Archival content lines **20,750 → 20,452**.

**Line-number references across the documentation went stale** as a direct result, since every line below the first removal shifted. Those in `NEEDS_CONFIRMATION.md` and `name_decisions.md` were re-derived (`Märck` 2864→2827; the `Holländer` settler lines 7942/7943/14923→7842/7843/14718; the Dutch `Holländer` 548→539), and both files now carry a standing note that line numbers move and the token should be searched for rather than the number trusted.

## Place of writing — re-derived from the dateline

The `place` field was produced by a hardcoded whitelist (`PLACE_RE`) scanned across each letter's last 15 lines, which failed two ways at once: it matched any listed town mentioned in the closing prose — letter 221 took `Neisse` from *"wider nach Neisse"*, the line immediately above its real dateline `Blizanow`; letter 237 took `Dresden` from *"von Dresden retournire"* — and it returned nothing at all for towns absent from the list, which produced most of the 95 blanks.

Replaced with extraction from the letter's **own dateline**, in both shapes the corpus uses: place and date on one line (`Breslau den 1ten Febr. 1799.`) and place on its own line above the date (`Kalisz` / `d. 29ten April`). The foot is checked first, then the head — Polish letters and some German ones date from the top (`w Warszawie dnia 5 Marca`).

Extraction stays faithful to the page; a separate `PLACE_CANON` map normalises manuscript spellings afterwards, so both layers remain inspectable: `Schlawenzitz`→Schlawenschitz, `Bleranow`→Blizanow, `Trąbczin`→Trąbczyn, `Franckfurth a d h`/`Fr a. d. Oder`/`Prandfurth a d O[der]`/`Fraudfurth an der Oder`→Frankfurt an der Oder, `Poser`→Posen, `Wein`→Wien, `Konigsberg`→Königsberg, `Kopoyno`→Kopojno, `Brzeg`→Brieg. A `PLACE_REJECT` set blanks readings too corrupt to be a place (`So bekomme ich`, `Thl. 13`, `Uria`) rather than recording them as towns.

**21 places set by explicit ruling, 206 derived, 92 with none found.** Distinct places 19 → 30. `place_review.md` (new) lists every letter with no place, its closing lines and why nothing was found — a blank is frequently correct here, and the point is to make the absence a decision rather than an oversight.

`74b` took `Berlin`: letter 74 was split into a bundle of legal documents written in *different* places (74a Berlin, 74c Glogau, 74d Berlin), and 74b carries no dateline of its own, so it follows the bundle's head and majority. 74d's `Berlin` was separately confirmed correct — its Silesian address (`zu Kontop bey Grüneberg in Schlesien`) is the addressee's, not the place of writing.

## `Sachen` → `Sacken` where it is the Fürstin

Surfaced while checking letter 74d: **8 instances of `Sachen` carry a noble title** — `Fürstin Sachen`, `der verstorbenen Fürstin von Sachen`, `Nachlas der Fürsten von Sachen` — and are the Fürstin von der Osten-Sacken, not the ordinary word. This vindicated the original instinct behind the earlier "Sakkin should be Sachen" reading: the name genuinely does appear as *Sachen* in this corpus. Following the biography simply makes `Sacken` canonical for all of them.

Corrected with a **title-anchored** substitution rather than a whole-word replace — the other **116** `Sachen` are the ordinary German word, and a blanket replace would have corrupted every one of them. `Sacken` 17 → **25**; ordinary `Sachen` unchanged at 116. Backup `…cleaned.txt.bak9`; all regeneration checks green.

`name_rulings.json` gained a `context_sensitive` section for exactly this class — tokens that are a name in some contexts and an ordinary word in others, recorded with the rule that separates them. `Holländer`/`Hauländer` is entered there too, still open.

## `Amelung` → `Amelang`, settled from the signature

You read the signature on letter 138 directly from the scan. That resolved a §E pair the statistics could not: `Amelang` ×33 against `Amelung` ×11 — frequency is no evidence at all about which spelling a man used for his own name, which is precisely why that section never auto-merges.

Searching for the shape rather than the token surfaced **12 distinct forms**, of which four proved to be the same signature corrupted four different ways, each in identical position — directly under a closing formula, on a Berlin-dated letter from the same correspondent: `AMelerich[?]` (L46), `AMelan[tt?]` (L138, the one read), `AMelang` (L143), `Amelrath` (L144). Two carried transcriber uncertainty markers that the manuscript reading now resolves.

**19 substitutions**: `Amelung` ×11 → `Amelang`, `Amelungs` ×4 → `Amelangs` (root-only, genitive preserved), and the four pinned signatures. `Amelang` 33 → **48**, `Amelangs` 2 → **6**. Backup `…bak10`; all regeneration checks green.

**Three left alone, recorded so the omission is a decision:** `Amel:` (line 13117) is an abbreviation like `Hochfürstl.`; `Amelan¬` (11817) is a line-wrap fragment, a line-break question rather than a spelling one; `Amelange` (4014) already has the correct root and only an odd ending.

**A seed-list error of mine, corrected at source.** `Amelung` was the canonical form in `name_catalogue.py`'s `EXTRA_SEEDS`, so the catalogue had been anchoring on the wrong spelling and proposing corrections *toward* it. Fixed. My note in `NEEDS_CONFIRMATION.md` that "the rarer form is the one in your who's-who" was also wrong — neither spelling appears in `whos_who.md`; `Amelung` came from my own list. §E is now 4 pairs; the catalogue stands at 166 variants across 82 names.

## `Munduhr` → `Medzibor` (letter 196)

The dateline of letter 196 read `Schwarzwald bey Munduhr d. 25ten May 1810.` The scan rules `Munduhr` out at once — there is a clear `b` loop and the word runs several letters longer — but the page is ~162 DPI and will not separate `Med-` from `Mied-` on its own, so the identification rests on the geography.

**Medzibor was the official name of Międzybórz until 1886**, when it was renamed Neumittelwalde; it lay in **Kreis Groß Wartenberg, Regierungsbezirk Breslau**, Prussian Silesia. `Schwarzwald` is a recorded village in that same Kreis, so `Schwarzwald bey Medzibor` is the ordinary construction — hamlet, then nearest town. Three things corroborate: letters 193–195 and 199–201 are dated Kontop and Breslau, the same corner of Silesia; the sources place a *forester* at Schwarzwald, which fits a Kriegs- und **Forst**rath writing from there; and the period form is `Medzibor`, not the modern Polish `Międzybórz`. Applied as the pre-1886 attested spelling; backup `…bak11`, checks green, and `place` for letter 196 now derives as `Schwarzwald bey Medzibor` without needing a normalisation entry.

**Worth recording as a limit of the tooling.** `Munduhr` is a hapax that none of the methods built so far could reach: it is not close to any anchor name, is not a German word, and sat in a dateline the old whitelist extractor ignored entirely. It took a human reading the page. The same class of error is likely present among the 92 blanks and the odder values in `place_review.md`.

`name_rulings.json` gained a `places_identified` section holding the evidence, so the identification is not re-litigated later.

## Place list: two more identified, and "Unknown" made visible

- **L115** `Bretz den 3ten Aug` -> **Breslau**, on your reading of the page. `Bretz` was a hapax, not close to any anchor, sitting in a dateline - the same shape of error as `Munduhr`.
- **`Peysern` -> `Peisern`** (L28 dateline, L271 prose), normalising to the form the corpus already used at L31. Peisern is the German name for **Pyzdry**, on the Warthe.

**The places list was quietly hiding a third of the corpus.** `build_site_data.py` indexed a letter only `if p:` - so the 92 letters that name no place of writing were dropped from `places.yml` entirely, and the list looked complete when it was not. They are now grouped under **"Unknown"**, sorted last rather than alphabetically among the real places. `places.yml` now carries 28 entries covering all 318 records: Unknown 92, Berlin 54, Breslau 41, Wien 40, Blizanow 17, Kontop 16, Kalisz 10, and so on.

Distinct real places fell 29 -> 27 as `Bretz` merged into Breslau and `Peysern` into Peisern. Backup `...bak12`; all regeneration checks green.

## Michalina Prusimska — four surnames merged into one person

She appeared as **three separate people** in the site's people index and the who's-who — `Michalina Prusimska` (14 letters), `Dąbska (Michalina)` (8), `Miączyńska (Michalina)` (5) — with letters 242, 266 and 270 counted more than once because she is named differently within a single letter. Merged into one entry: **Michalina Prusimska (Dąbska / Miączyńska / Moscinska)**, 26 tokens across **18** letters.

The four surnames are one life: born **Prusimska**; married **Dąbska**, used consistently 1807–1811 and confirmed in the text itself (L28, *"der Frau v Dąbska gebohrnen v Pru[simska]"*); remarried late 1814, after which the letters write **Moscinska/Moszynska** — the writers' own error for **Miączyńska**, not a transcription defect. Letter 266 hedges openly, *"Dąbska oder Moscinska"*, exactly at the remarriage; letter 285 states the chain outright: *"gab sie der Tochter des Prussiemski, jezt verehelichte Miączyńska zurück."*

**The merge exposed an over-broad regex that had been conflating father and daughter.** The old `prusimska` pattern was bare `Pru[sz]imsk`, which also swept in the adjectival `Prusimskische(n)` ×6 — *"die Prusimskische Erben"*, *"die Confiscirte Prusimskische Güter"*, *"von der Prusimskischen Familie"* — references to the family and its estates, not to her. Phase 2 had explicitly established father ≠ daughter, and the site index was quietly undoing that.

Her pattern now requires a feminine **`-a`** ending, which excludes both the adjectival family forms and `Moszynski` (masculine — her second husband, a third referent). A separate **`Prusimski family (Trąbczyn estates)`** entry catches those instead, 19 tokens across 12 letters, so nothing is orphaned: L297 names him directly, *"Güter nach einen gewißen **Anton v. Prussiemski**"* — Antoni Prusimski. The two patterns were checked for overlap: **zero tokens match both.**

`whos_who.md` collapsed from three entries to one merged plus one family entry, recording the corpus forms (`Prusimska` ×11, `Dąbska` ×10, `Moscinska` ×3, `Moszynska` ×1, `Miączyńska` ×1) and why the family is kept apart.

## People index generated rather than hand-curated

The site's `PEOPLE` list was 55 hand-written entries, and it matched **54 of the 807 tokens sitting in person position**. Anyone nobody had thought to add was invisible everywhere on the site — not obscure figures either: `Grotowski` ×15, `Brzechsta` ×29, `Hardenberg` ×24, `Sacken` ×22, `Amelang` ×8, `Schimmelpfennig`, `Struensee`. The same failure as the places whitelist, in a different file.

`name_catalogue.py` now exports its vetted seeds to `name_seeds.json`, and `build_site_data.py` merges them in. **Curated entries stay authoritative** — they carry display names, merged identities (Michalina Prusimska's four surnames) and distinctions the statistics cannot see (Hawich vs Honrichs); the export only fills the long tail. `people.yml` went **55 → 103** entries.

Three rounds of filtering were needed first, each a real defect:
- **`Minister` ×127 entered as *canon***, because `harvest_canon()` splits `**Graf/Minister Hoym**` from `whos_who.md` into three tokens. `NOT_NAMES` now gates the canon too, not just discovered seeds.
- **`Wien` and `Krotoszyn` typed as people** — German `von X` fires identically for `Herr von Triebenfeld` and `von Krotoszin`. The derived place field plus an explicit estate list now settles type.
- **Countries and common words** — `Preußen` 25, `Sachsen` 17, `Italien` 12, `Hard` 43, `Graf` 37, `Beym` 16, `Fond` 15, `Advocat`, `Circa`, `Moratorium` — all blocklisted.

Recovered by the pass: Grotowski, Napoleon, **Gneisenau**, Nesselrode, Haugwitz, Massow, Bülow, Dohna, Wartensleben, Blomberg, Nöldichen, Lipski, Pirch, Struensee, Schimmelpfennig.

**A standing limit worth recording:** this list cannot be complete by construction. It is built from tokens the corpus puts in a recognisable name slot, and 527 of 738 such tokens are hapax. Anyone named once without a title still will not appear.

## `Humboldt`, `Gärtner`, `Napoleon` standardised

**29 substitutions** (backup `…bak13`, checks green):
- `Humbolt` ×11 and `Humbold` ×5 → **`Humboldt`**. Neither corpus form was correct — this is Wilhelm von Humboldt, Prussian plenipotentiary at Vienna, named beside Hardenberg and Nesselrode (*"Humboldt und auch Nesselrode wolten ihm ihren Monarchen præsentiren"*). The 17th instance was `Humbo[?].` standing alone under *"Wien d. 5ten November 1814."* above *"An den Herrn v. Triebenfeld"* — **his signature on a letter to Triebenfeld**, so the uncertainty marker resolves too.
- `Gartner` ×6 → **`Gärtner`**, the Geh. Rath.
- `Napolion` ×5 → `Napoleon`, `Napolons` ×1 → `Napoleons`.

**`Gärtner` is a surname *and* an occupation.** L303's creditor register lists *"der Gärtner Nickel"* beside *"der Sattler Hennig"* and *"Major von Münchow"* — that entry is the gardener, a different referent. Line 4089's `Gartner` has no title and sits in a garbled passage, so it was **left as written**. The people index cannot separate the two, so the display name reads `Gärtner (Geh. Rath)` to say which is meant, and `name_rulings.json` records it under `context_sensitive`.

`whos_who.md` gained entries for Humboldt, Gärtner and Napoleon, none of which had one. §E is down to **3** open pairs: `Sachsen`/`Sachßen`, `Wartemberg`/`Würtemberg`, `Bartenstein`/`Brandenstein`.

## Polish surnames: a whole class the seeding was missing

You noticed `Trzcinski` was absent from the people index. It had missed the cue-rate threshold by **one hundredth** - 0.14 against 0.15 - because the letters name him bare ("Weder Trzcinski, Zerboni, noch Koenig"), not as "Herr v. Trzcinski". Chasing that turned up the real problem: of **80 Slavic-surname-shaped tokens in the corpus, only 12 were seeded.**

Two rules were wrong for this class, and both are now fixed:

- **Requiring a title cue.** No German common noun ends in `-ski`/`-cki`/`-owicz`, and these estates are in Posen and Kalisz, so the suffix alone settles that a token is a person. Morphology now seeds them directly, with no cue required.
- **The article veto, at low frequency.** This register takes articles with surnames routinely - "dem Hawich", "der Cosmar" - so for a name occurring twice, a single "der X" gives a 50% article rate and vetoed it. That was silently dropping `Smiedecki` (the Kalisz Prefect), `Chwalowski`, `Szczucki`, `Zglinski`, `Chelmski`, `Protowski`, `Smidkowski`. The veto no longer applies where the suffix has already decided.

**Slavic-shaped tokens occurring twice or more that remain unseeded: 0.** `people.yml` is now **118** entries, up from 55 before this work began. Recovered here: Trzcinski, Garczynski, Lichnowski, Lignowski, Dombrowski, Kurnatowski, Uminski, Smiedecki, and a dozen more.

**Recorded as unresolvable by the index:** there are **two different men named Trzcinski**, and letter 299 says so outright - *"Trzcinski ist wieder hier. Es ist nicht dieser sondern den Major Trzcinski der erstickt ist."* Same spelling, so no index can separate them; noted in `name_rulings.json` under `context_sensitive`, along with the variant `Trzczynski` that sits beside `Trzcinski` on a single line in letter 3.

## Two more names, and the People/Places pages made usable

- **`Protowski` -> `Grotowski`** (x2). Decisive from position, not similarity: `Protowski` sits at lines 8813 and 8822 while `Grotowski` sits at 8815, 8827 and 8861 - the same passage, about the same cession instrument. P/G is a standard Kurrent confusion.
- **`Trzczynski` -> `Trzcinski`** (x1) - the two spellings shared a single line in letter 3.

Backup `...bak14`; checks green. `Grotowski` now 16, `Trzcinski` 8.

**Both pages were truncating their evidence.** Each entry listed at most 40 letter references and then said "... and N more" - which is unusable, because the whole point of the list is to reach the letters. The limit is gone: **every reference is now a link**. Internal links checked by `verify_site.py` rose from 6,201 to **9,561**, all resolving, 0 external resources.

**Sorting added** to both pages - most/fewest mentions, A-Z, Z-A - as a small vanilla-JS reorder of the DOM (`site/assets/sort-list.js`). No dependency: the site is built to behave identically offline and on GitHub Pages, so nothing is fetched. Sorting by count falls back to alphabetical on ties, so equal-count entries do not shuffle arbitrarily between clicks. Buttons carry `aria-pressed` for the current state, and the reference lists are styled to wrap as chips rather than run off the measure.

## `Portalis` = `Pourtalès` — merged, with one instance deliberately preserved

Four spellings of one man collapsed into the corpus's own dominant form: `Portalis` ×5, `Pourtalles` ×3 and `Portales` ×1 → **`Pourtales`**, now 15. Backup `…bak15`; checks green.

The identification does not rest on spelling similarity but on biography. Letter 264 describes *"Der reiche Gr[af] **Portalis** mit Barbe in **Neufchatel** erzogen"* — raised in Neuchâtel with Barbe, having sold his English and French estates for millions. Letter 266 describes *"**Pourtales** … folgt blind seinen Jugend Freund und Schul Cammereden B[arbe]"* — the same school friend, the same fortune. Neuchâtel is the Pourtalès family seat. One man, under two spellings.

**Line 18917 was excluded from the substitution and must stay excluded.** It reads *"den **Pourtales (nicht Portalis)** wird sehr schnell etworten"* — the writer's own note that the name should be Pourtales rather than Portalis. A blanket replace would render it *"Pourtales (nicht Pourtales)"*, destroying the very remark that establishes the identification. Recorded in `name_rulings.json` under `context_sensitive`; the site's pattern matches `Portalis` too, so that one mention still indexes to the right man.

**Canonical form is `Pourtales`, not `Pourtalès`.** The writer never used the accent, and project policy is root-only correction that does not invent period orthography. The family's proper form appears as the site display name, `Pourtalès (Pourtales)`.

## Place of writing: 91 unresolved down to 24, and four extraction bugs

The dateline extractor was finding a place for 227 of 318 letters. The gap was not that the
remaining letters were silent about where they were written - most of them say so plainly - but
that four assumptions in `extract_place()` were wrong.

**A place after the signer's name was invisible.** `v. Triebenfeld, Breslau den 2ten April 1804`
puts the signature before the place on the dateline. The extractor only looked at text before the
date and required it to *begin* with a capital, so it saw `v. Triebenfeld, Breslau` and rejected it.

**A dateline sharing a line with prose was skipped entirely**, because a 64-character guard
assumed datelines stand alone.

**A bare day-number was mistaken for a place.** In `16ten 8br.` the regex matches the month
`8br`, leaving `16ten` as the candidate - not empty, so the "place on the line above" check never
ran, and `Breslau` sitting directly above went unread. Restricted to the foot of a letter: at the
head this same fix fires on document openers like `P[ro]. M[emoria].`

**One failed match ended the search.** A postscript's own date (`die Rükkunft nach Breslau ist
ohnfehlbar d 25ten bestimmt!`) was found first, failed to yield a place, and the function returned
- never reaching the real `Erhringen den 7ten Juli 1805` above it.

Fixing these recovered 11 letters mechanically. Reading the remaining 63 by hand recovered 20 more,
almost all the same shape: **the signature block is not on the last page.** A postscript, an
enclosure or a schedule of figures follows it, pushing the real dateline out of the search window -
letters 147, 192, 197, 203, 222, 242, 247, 260, 261, 262, 268, 284 and 286 all fail this way. Also
found: letter 207 heads a copy `Kalisz am 30ten Septr 1810` where `Septr` without a full stop is not
matched by the month pattern; letter 283 is French and dated `Vienne le 26 Mars 1815`; letter 302 is
undated but is the twin of letter 48, dated and placed at Kontop.

A separate bracket bug produced malformed values: `Bre[slau?]` came out as `Bre[slau?` because the
unwrapping stripped a closing bracket from a partially-bracketed reading, which broke the
`PLACE_CANON` lookup that would have resolved it. Fixed by unwrapping only wholly-bracketed guesses.

**91 unresolved to 24.** Of those 24: five are the archive's own missing numbers, one is a standing
ruling of "no place", and eighteen are enclosures, petitions and registers that genuinely name no
place - confirmed by reading each. Ten further readings rest on content rather than a dateline and
carry a `[?]` accordingly.

## Phase C — English translation

Scaffolding that had been in place since the site was built is now populated: the letter layout
already had an **English** tab reading `site/_data/translations/<pad>.yml`, a status badge, and a
"Not yet translated" fallback. Nothing about the translation touches the corpus, `letters.json` or
anything `regenerate.py` rebuilds; all three character-exactness verifications still pass with
translations present.

**The governing problem is that translation is a fluency machine.** Handed a corrupt German
sentence a capable model returns a smooth English one, silently converting a transcription error
into a fluent falsehood no reader can detect - the exact opposite of this edition's practice of
leaving unsettled readings alone. Every design decision follows from that.

- The unit of work is a **letter**, not a page: sentences run across page breaks. Segments come back
  per page, keyed `(letter_id, page)` - the only join key that survives a corpus edit.
- Output is forced through a **tool schema**, so the model must return, beside the English, what it
  could not parse, what it could read two ways, and what it thinks the manuscript really said.
- **Emendations are kept in their own field** and never folded into the English. A guess at fixing
  the *transcription* is a separate editorial act, reviewed against the manuscript by a human.
- The German's holes stay holes: `[?]` becomes `[illegible]`, `[word?]` becomes
  `[uncertain: word]`, `[...]` becomes `[text lost]`.
- `translation_glossary.yml` fixes 63 renderings - currency, the graduated honorifics
  (`Durchlaucht` outranks `Hochwohlgeboren` outranks `Wohlgeboren`, and English must keep them
  apart), closing formulas, and the estate and legal vocabulary - so 318 letters do not drift.

**What the mechanical checks can and cannot do, stated rather than implied.** Numerals of two or
more digits, catalogued names, marker parity, glossary consistency and segment count are all
verified without reading the English. The common function-word confusions are not: `nach`/`noch`,
`als`/`da`, `wie`/`wir` and `vor`/`von` run to about 7,750 occurrences, nine per page, and no
mechanical test separates a correct one from a misread one when both are fluent. The rare pairs are
a different matter - `Anweisung`/`Abweisung` and `committirt`/`exmittirt` occur **42 times in the
whole corpus**, so every one is required to be flagged and an unflagged occurrence blocks
publication.

**The pilot earned its keep.** Twelve letters spanning the range - clean, known-bad, the Polish 72e,
the French 283, and the 48/302 twin - found real transcription errors as a by-product of having to
make sense of every sentence: `drückte mich schier zu Baden` for `zu Boden` ("crushed me to the
ground"), and the `Abweisung`/`Anweisung` split on letter 48 where its twin 302 reads the opposite.
Also surfaced a class worth watching: 31 pages where the translator marked doubt the German does not
mark, reported as `unmarked-in-german` - candidate silent corruption.

**A separate bug found on the way.** `has_damage` in `build_db.py` is 0 for every letter and always
has been: it tests whether a letter's *endpoints* fall inside a damage run, but a damage run always
sits strictly inside a letter, so it can never fire. Worse, two of the five hardcoded ranges
(21684-21713) now point past the end of the file (21643 lines), and the three that are in range
(letters 253, 254, 295) contain no `[...]` markers at all, while the pages that do carry them - 247
with 18, 289 with 11, 300 with 17 - are different letters entirely. The ranges went stale when the
corpus was re-split. The in-text markers are the reliable signal and are what the checker uses.

## Summaries, and correspondents made visible

**`sender` and `recipient` are no longer empty.** Both fields were declared in the letters.json
schema when the database was first built and never populated - 0 of 318. `derive_correspondents.py`
reads them off the salutation and the signature, which are highly formulaic here: 192 letters open
`Durchlauchtigster Fürst`, 197 close `v Triebenfeld`. Where a letter opens mid-flow with no
salutation the recipient is still recoverable from the form of address used throughout the body -
a letter that says `Ewr Durchlaucht` twenty times is written to the prince whether or not it says
so at the top - and that is evidence, so it is used. It is used **only** for the recipient: nothing
in an address form identifies the sender, so an unsigned letter stays unattributed rather than
being guessed at, even where one correspondent would be overwhelmingly likely.

214 letters carry both. The residue is listed in `correspondents_review.csv`, and most of it is not
a gap to fill: four are the archive's missing numbers and the rest are largely documents with no
correspondent pair at all - `Copia` and `Abschrift` copies, two `Pro Memoria` memoranda, the L303
liquidation register, an address slip. Perhaps six could be identified from content by a person.

They now appear under the date in the letter header, as a `Correspondents` row in the document
panel - stating their provenance, "read from the salutation and signature" - and as a `from -> to`
line on each row of the browse list.

**One-paragraph summaries for all 313 translated documents**, written by `summarise.py` from the
**English** rather than the German. That is the cheaper and the more reliable direction: the
translation has already resolved the line-wraps, the abbreviations and the obvious corruptions, so
the summariser is reading sound prose instead of re-deriving it. Median 89 words, and deliberately
concrete - the value of a summary in a list of 313 documents is entirely in its detail, so
"presses for the sequestration of Zagorowo to be lifted" earns its place where "discusses estate
business" would not.

They live in `site/_data/summaries.yml`, which nothing else generates and which is outside every
regenerated artifact, so no verification can be disturbed by them. On the letter page the summary
sits between the header and the text panes, set in the sans face above a rule so it is never
mistaken for something the letter itself says. In the browse list it replaces the old
opening-words snippet, which was close to useless because nearly every letter opens with the same
salutation; a search query still brings back the matching passage instead, since that is what the
reader is looking for. Clamped to three lines in the list so one long summary cannot push the next
result off the screen.

Summaries are a finding aid, not part of the edition's text, and are marked as such in the file
itself. Cost: about $2.80 through the Batch API.

## A German interface, and German summaries

The site is now bilingual, on a deliberately asymmetric plan: **the chrome exists twice, the
documents once.**

**Chrome pages are rendered in both languages at build time** - `/de/`, `/de/briefe/`,
`/de/zeitleiste/`, `/de/personen/`, `/de/orte/` - so a German URL is a real, shareable,
bookmarkable address that works with JavaScript switched off. To avoid keeping two copies of the
same markup in step, each page body was lifted into an include under `_includes/` and
parameterised; the ten page files are now thin wrappers that declare a language, a permalink and
their counterpart. All interface strings live in `site/_data/i18n.yml`, 107 keys in each language,
checked to have no key present on one side and missing on the other.

**Letter pages are shared.** The transcription, the scans and the English translation are the same
documents whichever language the interface is in, so duplicating 313 pages to change a dozen labels
would have been a poor trade - it would have doubled the site to alter its furniture. Those pages
render in English, carry both dictionaries inline, and swap their labels in the browser
(`assets/i18n.js`), remembering the choice so the rest of the site follows it. The switch is
therefore a link on a chrome page and a button on a letter page, which is the honest reflection of
the fact that only one of them has a counterpart URL.

Everything degrades honestly: with JavaScript off the chrome is still fully bilingual by URL, and a
letter page simply stays in English.

**"About the edition" stays in English by decision, not oversight.** It is the essay that sets out
the edition's own method and standards, and machine-translating the document that explains how
carefully the text was established would be a poor advertisement for the care. The German
navigation links to it and the German footer says plainly that it is in English.

**German summaries for all 313 documents**, written by `summarise.py --lang de`. They are written
from the same English translation as the English summaries rather than translated from them:
running a summary through a second summarisation compounds whatever the first pass got wrong, and
the source was equally available either way. The German follows the edition's own forms - `Rthl`,
`Sequestration`, `Erbpacht`, `Fideicommißgüter`, and the name spellings established for this
edition. Cost about $2.30 through the Batch API.

The browse list shows whichever summary matches the page's language, and falls back to the search
snippet when there is a query, since a reader who has typed something wants the passage that
matched. Internal links checked by `verify_site.py` rose from 9,615 to **11,839**, all resolving,
still no external fetches.

## A narrative introduction: "The story the letters tell"

A 2,600-word essay at `/the-story/` for readers meeting the correspondence for the first
time, with **57 inline links** into 43 individual letters, so any claim can be left behind
for the evidence in one click. Styled deliberately quieter than an ordinary link - the prose
should read as prose, with the citation available rather than insistent.

**Written from the summaries and translations rather than from memory.** The whole
correspondence was read in chronological digest form first - date, place, sender and the
opening of each of the 313 summaries - which is what the translation and summary passes made
possible and what the earlier `narrative_overview.md` (an explicit first-pass sample of every
15th-20th letter) could not do. Every letter cited was checked to exist and to have a
translation before publication; `verify_site.py` then re-checks all 57 links as part of the
12,239 it resolves.

Three things the essay is careful about, because the edition is:

- **Jena is not claimed.** Letter 26 is relief that the Prince survived, learned at second
  hand amid "malicious rumours"; it never names the battle or the capitulation. The essay
  says the identification is an inference from date and biography, and says so in the text
  rather than in a note.
- **The 112,000 Rthl coincidence is left open.** The liquidation register's largest private
  creditor is a *Frau Charlotte von Triebenfeld* owed 112,000 - the same figure as the advance
  running through the whole correspondence, and the same name as the daughter who writes
  letter 7. Whether these are one sum and one woman is recorded as an unanswered question.
- **The figures carry a warning.** The closing paragraph tells the reader plainly that the
  sums are the least reliable thing in the letters, coming mostly from Triebenfeld's own
  advocacy, and that numerals are the weakest point of the transcription.

Verified while writing: letter 7 is signed `Charlotte von Triebenfeld ... ganz unterthänigste
Dienerin`, Breslau, 20 March 1815, and its text says she writes "directed by a letter from my
father" - so the daughter's letter, the father's absence in Vienna and her not knowing his
address are all in the document, not supplied.

**A German version followed** at `/de/die-geschichte/`, written rather than machine-translated,
and better sourced than the English for one reason: it quotes the manuscript directly instead
of translating the English translation back into German. Where the English page has "I am as
though crushed, and, since my good wife is being laid to rest today", the German page has what
Triebenfeld actually wrote - *"ich bin wie zermalmt und habe mich, da meine gute Frau heute
beigesezt wird, mit den Kindern bei meinen Schwager retwirt"* - and the same for Charlotte's
letter, for "ohne alle Decrete und Urtels", for "die Leute aus halsstarrigkeit gar nichts
geben", and for Hardenberg on "dieser redliche Mann". Six quotations recovered from the
transcription for the purpose.

Both pages carry the same 57 links to the same 43 letters, both were checked against
`letters.json` before publication, and neither contains an em or en dash. The story is now the
only long-form page that exists in both languages; "About the edition" remains English by
decision, since machine-translating the document that explains how carefully the text was
established would undercut the point of it.

## Colon abbreviations: a class of mention the index was losing

These writers shorten a familiar name to its first syllable and a colon - "Min: v. Hard:",
"Gen Lieut v. Koch:", "der Gr. Pourt:", "der faula Amel:". There are **182 such forms across
125 distinct abbreviations**, and nothing in the edition was reading them as names.

**The people index was undercounting.** Its patterns match full spellings, so a letter that
discusses Hardenberg and never writes his name out was simply not indexed under him. Nine
letters are in that position (134, 213, 214, 239, 240, 241, 255, 264, 295), which left the
State Chancellor of the Vienna years showing in 31 letters instead of 40 - a 29% undercount
on a central figure. Also lost: five letters for Köckritz, one each for Amelang, Pourtalès
and Grävenitz.

A `NAME_ABBREV` table now folds verified abbreviations into the matching patterns. Result:
Hardenberg 31 -> 40, Köckritz 29 -> 33, Amelang 31 -> 32, Pourtalès 12 -> 13, Grävenitz
2 -> 3, Sacken 21.

**Only abbreviations verified in context were added**, because a wrong expansion invents a
mention that is not in the letter, which is worse than missing one. Four traps were found and
excluded, each checked by reading the passage:

- `Ant:` is **Antwort**, not Anton - "Ant: wir zahlen schon zu viel"
- `Kur:` is **Curländisch**, not a person - "der Kur: Erben"
- `Ko:` is **Koschentin**, the estate, not Köckritz. L2's "In der Ko: Geschichte" is followed
  by Pourtalès answering that he wants to buy, which settles it
- `Sch:` could be Schlabrendorff, Schenck or Schimmelpfennig; `B:` could be Barbe, Beyme or
  Brzechsta

`Sa:` was admitted only in its title-anchored form. Both corpus instances read "der Fürstin
Sa:" and "Die Fürsten Sa:", and Sacken is the only Fürstin S- in the correspondence; a bare
`Sa:` would not have been safe.

**The translations were inconsistent about the same thing, and that was a prompt fault.** The
system prompt said to reproduce every proper noun exactly as spelled and never normalise a
name, which fought against ordinary comprehension, so the model decided case by case: L239's
"Min Hard:" became "Minister Hardenberg" while L264's "Fürsten Hard:" stayed "the Prince
Hard:". Seventeen English pages carried an unexpanded abbreviation. The glossary now has an
`abbreviations` block stating that expanding an abbreviation is not correcting a name and is
applied silently, with the same trap list, and `repair_translations.py --abbrev` brought those
pages into line for $0.82.

Sixteen of the seventeen were expanded. The seventeenth is the interesting one: on L107 the
model **declined** to expand `Sa:`, on the ground that doing so "would fix which Princess is
meant" - which is precisely the criterion the editorial policy sets for leaving a mark
visible. It stands as `[uncertain: Sa: - Sacken?]`. The index does match that letter, on the
strength of the title, so index and translation take slightly different views of the same two
words; the index is a finding aid and errs toward retrieval, the translation errs toward not
asserting. Both positions are recorded rather than reconciled by force.

## The German timeline

`/de/zeitleiste/` existed but was German only in its heading and lede. Everything with
substance in it was still English: all 20 historical events, the "six movements" summary,
and the bar tooltips, because the include hardcoded them rather than reading i18n.

Events now carry `title_de` / `note_de` / `source_de` in `_data/timeline.yml`, and the
include falls back to the English field when a German one is absent, so an event can be
added in English alone and translated later. The movements moved out of the include into
i18n as a list of lead/body pairs, which is what let one shared include serve both
languages. Tooltips inflect: "1 Dokument", "2 Dokumente".

One translation is worth noting. The Prenzlau entry quoted "malicious rumours", itself a
translation; letter 26 turns out to read **"so viel boshafte Gerüchte ausgestreut wurden"**,
so the German page now quotes the manuscript instead of back-translating the English gloss.

A build check confirms all 20 German titles present on the German page with no English
leakage, the reverse on the English page, and identical bar counts and year links across
both.

## The About page: German version, and a factual audit

`/de/ueber-diese-edition/` now exists, and the nav, footer, home card, people lede,
story page and shared letter pages all route to the right language. The English page
had no `alt_url`, so readers could reach English from German but not the reverse;
it does now.

The humanizer pass found the usual em dashes, about thirty of them, which also put
this page out of step with the two story pages already scrubbed. Both versions are
now at zero. Some mechanical boldface came off too, the sentences that were bolded
whole for emphasis rather than to name a thing.

**Checking the page's figures against the data turned out to matter more than the
prose.** Six numbers were wrong, and three of them contradicted each other inside the
same page:

| Claim | Was | Is |
|---|---|---|
| Documents | 317 | **318** |
| Manuscript pages | 913 | **869** |
| Line-end marks | 1,316, then 1,314 | **1,317** |
| Genuine joins | 826, then 825 | **826** |
| Marks joining nothing | 482, then 484 | **483** |
| Uncertain readings | 147 | **150** (98 illegible, 52 guesses) |

The scan figures were right: 872 photographed, 865 beside a transcribed page, seven
others, which reconciles exactly against `page_scan_map.csv`.

Two further corrections. The numbering note claimed the sequence runs 75 to 301, but
302 and 303 exist and sit outside it. And the page said uncertain readings and damaged
passages "are recorded in the metadata of every document that has them" - the marks are
indeed in the text, but `has_damage` is false for all 318 records, so the metadata half
of that sentence was not true. It now claims only what holds.

## Dashes: the last of the site chrome

The em dashes in `i18n.yml` were the last prose on the site that had never had a
humanizer pass. Rewritten rather than repunctuated, in both languages: ledes, hints,
the home paragraphs, the footer, the missing-number notice. Also caught a stale
German string, `card_about_p`, still promising "(auf Englisch)" a day after the
German About page went up.

The sweep then found dashes the i18n file did not account for:

- **Templates**, as `&ndash;`/`&mdash;` entities, which grep for the literal
  characters had missed: sort buttons (A-Z), year and line ranges, the people count,
  and two bundled-document notes.
- **The letter-page generator** in `build_site_data.py`, which emitted them into all
  318 generated pages.
- **Summaries**, 63 English and 52 German. Numeric ranges became hyphens, name pairs
  like Rochlitz-Honrichs became hyphens, and prose dashes became commas. Eight places
  where a paired dash carried a real parenthetical were given brackets instead,
  because collapsing those to commas made them ambiguous: "Creditors range from
  tradesmen and household servants, the saddler..., the joiner..., to bankers" loses
  the from/to spine that "(the saddler..., the joiner...)" keeps. Three German
  summaries also had a malformed `-,` in the original.

Every chrome page is now clean. **Two sources were deliberately left alone.**

The corpus holds **1,167 dashes** in the diplomatic and reading text. That is the
manuscript, it is verified character-exact, and it is not ours to tidy.

The English translations hold **2,767 across 266 of 313 letters**, and the argument
for leaving them is not just cost. The German these render is itself dash-heavy, by
exactly the 1,167 above; a translation that keeps that punctuation is following its
source rather than betraying a machine author. The humanizer exists to stop AI prose
passing as human, and this edition states on its About page that the translation is
machine-made. Rewriting 2,767 spots in historical prose would risk meaning to fix
something that is not a fault.

## Restructured for a growing corpus

The edition was built around one archival holding, Oe 1 Bü 9454, and it showed: adding a
second would have meant editing a 500-line script by hand, and would have collided at
once, because 14525 will also have a document numbered 48.

A unit is now a directory. `units/<slug>/` holds the transcription, the editorial rulings
keyed by the archive's own document number, and the provenance. Ten constants came out of
`build_db.py` into `rulings.yml`, lifted by parsing the source and checked to round-trip;
the place canon moved to `reference/`, because spelling knowledge is shared while
decisions are not. Adding a holding is writing a file, not editing the pipeline.

Documents carry `unit`, `uid`, `pad` and `permalink`. URLs became
`/documents/oe1bu9454/48/`, with 318 stubs forwarding from the old flat addresses.
`letter_id` stays the bare archival number, which is what let every existing ruling
survive the move untouched.

The build runs per unit into `corpus/units/<slug>/`, and `merge_corpus.py` combines them,
refusing to merge if two units claim the same uid. A unit whose `corpus.txt` is empty is
skipped and reported, so a holding can be scaffolded long before it is transcribed.

**Three bugs surfaced that only bite with a second unit**, and one that had been biting
all along:

- Archival position maps were keyed by `letter_id`, which collides the moment two
  holdings both number a document 48. Archival sort ignored the unit, so the two would
  have interleaved. Both now key on the unit.
- The scan map was keyed by `(letter, page)`, for the same reason.
- `browse.js` never read the query string at all, so the timeline's `?year=` links have
  always landed unfiltered. They work now, along with `?unit=`.

**`has_damage` was false for all 318 records.** It tested corpus line ranges: two of the
five pointed past EOF, and the surviving three no longer land on damaged text, because
the ranges went stale when the corpus was edited. Correcting the overlap test would have
falsely flagged letters 253, 254 and 295 as damaged. Damage is now read from the text's
own `[...]` markers, which travel with the words: 12 letters, 56 marks.

The cache move was the step with money at stake. `translate.py` computed a bare pad and
would have found nothing under the new names, re-translating 313 letters and paying for
them twice; `publish` and `summarise` trusted a stale pad recorded inside old cache
files. 965 files moved with their contents untouched, and `translate.py` now filters the
merged corpus to its own unit, or a run would translate every holding in the project.

Through all of it the transcription hash never moved: 318 documents, 869 pages,
character-identical at every step.

## A glossary for the reader (2026-10-02)

A reader who is interested but not an expert meets words no one now uses:
Rthl and Courant, Hufe and Morgen, Vorwerk and Erbpacht, Sequestration,
Durchlaucht. The first batch of a glossary explains 61 of them, chosen from a
candidate sheet built from the translation termbase, words rare in modern
German, and the timeline. Six kinds: money and measures, land and tenure, law
and administration, titles and address, formulas and dates, and the events and
states the letters take for granted (South Prussia, the Duchy of Warsaw,
Tilsit, the Congress of Vienna, the Partitions).

The false friends were the reason to do it: *Execution* is the enforcement of
a debt, *Resignation* the conveyance of an estate, *Intressen* interest on
money, *Canon* a fixed rent, and the English keeps *execution* in 55
documents.

In the documents each word is faintly underlined, once per manuscript page
(once per document for formulas), in the transcription, the reading text,
the English and both summaries: 8,837 marks in 411 documents. A tap opens a
short definition in the interface language, under the word on a wide screen
and as a sheet from the bottom on a phone. The marks are added by the page's
script from a list the build makes, so the verified German in the HTML is
untouched. The glossary page (/glossary/, /de/glossar/) lists every entry,
with search, filters by kind, an A-Z bar, and a link to the documents each
appears in (/documents/?term=). A switch beside "hide scans" turns the marks
off; the privacy section of /rights/ now names four stored preferences.

The definitions are drafts: the reference works (Adelung, Krünitz, the
Allgemeines Landrecht, Gloger) could not be reached from where they were
written, so each names the work it is to be checked against, and the page
says so. False hits found in review and fixed in the patterns: *Morgen* as
"tomorrow", *Schulze* as a surname, *resignation* as patience, *Canonicus*.
The "hide scans" checkbox, which had no style and crowded the view hint on a
phone, is styled with the new switch.

## The glossary's second batch, and the English money written out (2026-10-02)

Fr. d'or, in 19 documents, was not in the glossary: the first batch came from
the translation termbase, which has no entries for abbreviations or Latin. A
probe for both now runs in `glossary_candidates.py`, and 30 more entries take
the glossary to 91: the Friedrich d'or; four measures (rod, Centner, cord,
bushel); seven of land and tenure (donation, Taxe, Competenz, appurtenances,
entry money, fief, allodial); twelve courts and offices; and the Latin and
formulas of the deeds (pp., geruhen, L. S., Actum, in fidem, de dato, vigore).

The most useful of them is a false friend the English repeats in 60
documents: before 1808 a Prussian province's *Regierung* was its high court,
keeper of the mortgage book, not its government. The entry says so wherever
"Government" stands for it. Patterns were read against their matches and
narrowed where they caught the wrong thing: the King's *Regierung* in "the
eleventh year of Our reign", the French documents' *Gouvernement de Pologne*,
a *General Gouverneur* (a person), and the garrison's "Government Auditor".

The English kept the German money abbreviations in a dozen forms. They are now
written out by rule, not by a model: `reference/english_forms.yml`, applied by
`english_forms.py` and by publish_translations.py and summarise.py as they
write, so a re-publish keeps them. About 1,400 replacements in 186
translations and 32 summaries: rt, rtl, rttl, rthlr to the termbase's Rthl;
gg, ggr, g., gl. to Groschen; pf. and d. (after Groschen) to Pfennig; fl. to
gulden and x to kreuzer; every Fr. d'or to Friedrich d'or. Every Groschen and
gulden replacement was read in context first. "Polish gulden", the złoty of
the deeds, stays gulden, and the glossary's gulden now covers it.

## Patrimonial courts, Regierung in the termbase, and the glossary's third batch (2026-10-02)

The editor supplied a description of the patrimonial courts of South Prussia
from Szukaj w Archiwach, after T. Mencel's introduction to an inventory. It is
kept in the Polish, with a working translation, as
`reference/sources/patrimonial_courts_mencel.md`, and it corrected the draft
glossary: the owner could judge in person, and the court heard everything
between lord and peasants except criminal cases. The patrimonial court entry is
rewritten from it and names it; the justiciary, the peace court and South
Prussia take what it supports; and the General Law Code (Landrecht), cited in
8 documents, has an entry.

The translation termbase gains Regierung -> Government: the institution's
own name, which the published English already uses, with a gloss on its
meaning before 1808 for future translations. The reader's glossary explains it
on the page.

A third batch from the abbreviation and Latin probe takes the glossary to 101:
the months by number (7br. to Xbr.), d. J. and a. c., the possessives of
address (Ew., Sr., Ihro, Dero), pct., titulus possessionis, Quantum,
Inventarium, ex officio, and Protocoll, which the English renders "protocol"
in 24 documents: the court's record, not etiquette. Two more house forms for
the English, applied the same mechanical way: the four dates left with 8br and
Xbr now name the month, and six pct. read per cent.

## Regierung in the published English (2026-10-02)

Of 96 manuscript pages whose German has Regierung, 56 already said
Government. Of the rest, the plurals were already "Governments", and "court",
"authorities" and "reigning" turned out to render other words. What remained:

- 15 places named the institution by its seat in lower case ("the government
  at Kalisz", "the Poznań government"). A house-form rule in
  `reference/english_forms.yml` capitalises them, and the same 14 times in the
  English summaries.
- 11 needed the sentence read, and go in a new file,
  `reference/english_corrections.yml`: page-by-page corrections, each with the
  German that decided it, applied after the house forms by english_forms.py and
  so at every publish. A correction whose words are not on the page exactly
  once is reported, not applied. Eight are the institution without its seat
  (the Government sending execution, appointing a sequestrator, leaving Breslau
  in 1813; a Government councillor and director); two are "our Government
  here" against the Government at Thorn; one is "Our successors in the
  government", the King's successors on the throne.
- The political sense stays lower case: the previous government, the Prussian
  government, a democratic government.

One page that seemed to leave Regierung untranslated (14525, 17, page 8) does
not: the sentence runs over the page, and the English puts "of the Royal South
Prussian Government" on the next.

## The glossary's candidates ruled, and a gate in the build (2026-10-02)

Every word the candidate sheet raises from the termbase and the abbreviation
and Latin probes, in 3 documents or more, is now an entry or ruled out: seven
new entries (H. and dH., the closing formulas with the Diener and the humbler
Knecht, Einsassen, in Ratis, in solidum, the Kreis-Justiz-Commission, the
Justiz-Commissarius), 87 rulings with reasons (section numbers, plain month
and number abbreviations, names, salutations the English renders plainly,
words plain in English), and patterns widened to the forms the entries
missed. Prefect and Podprefect had never matched in the German, the pattern
expecting Prä-; they do now. 108 entries, 14,037 marks in 417 documents.

`glossary_candidates.py --check` is the gate the plan called for, and
regenerate.py runs it after the holdings' descriptions: it fails the build if
a translated holding brings a qualifying word that is neither an entry nor
ruled out, and names it. Tested by removing one ruling: it failed and named
the word; restored, it passed.

## The glossary checked against the reference works (2026-10-02)

With woerterbuchnetz.de, kruenitz.uni-trier.de and pl.wikisource.org now
allowed, 54 of the draft entries were read against Krünitz, Adelung, Grimm
and Gloger and set `checked: true`, each with a `source:` naming the entry and
its URL. The glossary page now links the entry name (`source_html`, built by
glossary_build.py); a path into `reference/` is still dropped, and the rest of
the line now shows (the Mencel source's "for the rule of 1795").

Where the work said otherwise, the English and German were corrected:
- Money and measures: Courant is the coin of everyday trade, small change
  apart; the Friedrichsdor stood by law at 5¼ Rthl Courant, in trade at five
  in gold with a moving premium, and at six in the royal offices in 1809; the
  Centner was 110 pounds at Berlin but 132 in Silesia (and grain, measured
  by the Scheffel, is dropped from it); the Klafter is six feet by six, as deep as the logs are long; the
  Morgen is a day's or a morning's ploughing; the Hufe is 30 Morgen, and in
  Greater Poland the włóka itself was called Hufe; the Polish gulden is a
  money of account; the legal rate of interest in Prussia was five per cent.
- Land and law: the canon is not "never raised" (Krünitz has the hereditary
  rent set in grain or by grain prices too), and the same correction goes into
  Erbpacht, which stays unchecked; the Erbzins acknowledges the lord's
  ownership of the soil and is not said to replace labour; the Laudemium is
  paid for the lord's confirming the new holder, with no "fixed share"; a Taxe
  can be made by a court or privately; Sequestration pays the income to the
  court for the creditors.
- Offices: a Hofrath is a councillor of the prince's court and often a bare
  title; a Conducteur is a building official (in the letters, a sworn
  surveyor); an Auditeur conducts a military court's proceedings; an
  Estaffette goes by relays of mounted postilions; a starost's judicial
  powers belonged only to the castle starosts, and the title stayed with
  those who held starost lands after the partitions.
- Address and formulas: Durchlaucht is the style of princes and electors,
  not only reigning ones; Hochwohlgeboren is for every noble, not for senior
  officials; Wohlgeboren went to commoners near noble rank; Knecht is used
  only to persons far above the writer; Einsassen are set against outsiders,
  not lodgers.

Left unchecked, and why: the entries resting on the Allgemeines Landrecht, the
Hypothekenordnung, the Gerichtsordnung, Acta Borussica, Grotefend or a
standard history, none online here (Erbpacht, Einstand and Resignation
among them, though Krünitz was read for each; it has no Dominium); and those the
works online have no entry for: olędrzy, the Duchy of Warsaw's prefects,
tribunals and peace courts (Gloger stops at 1795), Dismembration, pp., Actum,
in fidem, ex officio, Rendant and the abbreviations of Herr. 55 of 108
entries are now checked.

## The Sources page's one-line descriptions made to stand alone (2026-10-02)

The editor found that the line under each holding on the Sources page assumed
the reader knew which ministry, which king and which agent was meant. Each of
the nine (`title` and `title_de` in `units/<slug>/unit.yml`, also the
standfirst on the holding's own page) now names in full the king (Friedrich
Wilhelm II or III, King of Prussia), the office that kept the file (the
Prussian central administration for South Prussia, the Prussian Ministry of
Foreign Affairs), the Prince (Prince Friedrich Ludwig of Hohenlohe-Ingelfingen)
and his agent (Peter Friedrich von Triebenfeld), and says what South Prussia
was: Prussia's share of partitioned Poland. First mentions take "a", per the
house style. The same line opens the translator's and summariser's prompts,
which will carry the fuller context at the next paid run.

## Antoni Prusimski as a person in his own right (2026-10-02)

At the editor's request, the "Prusimski family" entry in
`reference/people.yml` is now Antoni Prusimski, Starost of Niszczewice
(Ostroróg-Prusimski), the original owner of the Trąbczyn and Kamionna estates,
whose estates were confiscated after the uprising of 1794 and granted to the
Prince of Hohenlohe-Ingelfingen in 1796. The slug stays `prusimski`, so links
and the counted mentions carry over. The adjectival Prusimskische(n) (his
estates, heirs and family) stays counted to him; Michalina Prusimska keeps her
own entry, and the two are now marked `distinct_from` each other, which also
puts them on the translator's never-merge list. "Johann von Prusimski", whose
inscription of 1673 charges an annuity on Kolno (14525), is an earlier man and
is no longer matched. The People page biography (`reference/people_bios.yml`)
and `reference/whos_who.md` are rewritten to match. The queryable dataset in
`corpus/` was regenerated with it, which also brought in the English money
forms already on the site.

## The Hohenlohe-Ingelfingen years rewritten from all nine holdings (2026-10-02)

The era page (`site/hohenlohe.md`, `site/de/hohenlohe.md`) had been written
on 2026-09-29 from the letters and the contracts alone. It is rewritten on the
plan in `docs/HOHENLOHE_ERA_PLAN.md`, in the voice the editor set (story voice,
little metaphor, plain facts), in English and German written separately. New
sections tell the confiscation and the grants of 1796 and 1797 (Nr. 3570,
Oe 1 Bü 14525), Michalina Prusimska's complaints of 1800 to 1802 (Nr. 3709, as
far as the scans show), the sales of Szetlewek, Kamionna and Kolno and
Pszczew, the Erbet lease and the Oleśnica petition, the entail of 1805
(Oe 1 U 199), the tribunal at Kalisz, Zerboni di Sposetti's report, the
Russian refusal of 1816 and the heirs' claim to 1820 (Nr. 12765). The reading
list draws on all the holdings. The document count, span and number of
holdings now come from the site data. Corrections on the way: letter 28 is
Hawich's, not Triebenfeld's; letter 217 is von Sanitz's report of what he had
heard, and letter 198 a refusal of Michalina's petition; the German quotations
follow the transcription as it now stands (Beyme, not Beyhm; retirirt; lassen).
The era blurb in `reference/eras.yml` dated the takeover to the Third
Partition and the claim to 1816, and said the edition calls Pszczew Betsche;
all three are corrected (the Second Partition of 1793; 1820; Pszczew).

## Triebenfeld was Kriegs- und Forstrath (2026-10-02)

The editor confirmed that Triebenfeld's title was Kriegs- und Forstrath,
Councillor of War and Forests, as the deeds write it throughout ("Krieges und
ForstRath von Triebenfeld", 14525 and 14526). The earlier ruling in
`reference/people.yml`, `reference/translation_glossary.yml` and the comment in
`units/oe1bu9454/unit.yml`, that he was Kriegsrath and "NOT Forstrath" because
of a long-s misreading, was wrong and is withdrawn. Corrected there, on the
home page (English and German) and on the era page. The translator's note on
Kriegsrath now says that, of Triebenfeld, it shortens the full title. The
published English already used "Councillor of War and Forests" (68 times) and
never the shortened form for him, so no translation changes.

## Names standardised in the English and tagged (2026-10-03)

The editor asked that Prussiemski be standardised to Prusimski and tagged as
Antoni Prusimski, noted that Kähmen had slipped through for Kamionna, and asked
for all names and places in the English to be checked. A names audit compared
every name the translator recorded, German beside English, with the settled
form in `reference/people.yml` and `places.yml`. The transcriptions are not
touched: what the writers wrote stays.

- Registers: the spellings found are now recorded variants, so the termbase
  tells the translator the settled form and the build tags them. Antoni
  Prusimski takes Prussiemski, Prussimski, Prussimsky and Prusimsky (30
  documents, from 29). Kamionna takes Kähmen and Kamienne, and Kamen, Kämen
  and Kamener only where they name the estate (they are also the verb).
  Kolno takes Kollno. Michalina Prusimska gets a running-text form,
  Miączyńska, so the translator no longer prints her catalogue entry inside
  a sentence; her second husband, Stanisław Miączyński, gets his own entry
  (Moscinski, Mięczynsky), with a People-page biography. Prince Wilhelm of
  Prussia gets his English form. Some forty other spellings of people and
  places join their entries.
- English: rules in `reference/english_forms.yml` bring the published
  English into line (86 translation files, 31 English summaries): Prusimski;
  Miączyńska and Miączyński for Moscinska, Moscinski, Mięczynsky; Kamionna
  for Kähmen, Kamen, Kamienne, and "Kamionna or Kamionna" made one; Kolno for
  Kulm (31) and Kollno (20); Prince Wilhelm of Prussia for "Prinz Wilhelm
  von Preußen"; and the other spellings by table (a new `names` lookup in
  english_forms.py). Two one-page corrections: "the peasants of Stoki" is
  Skokum (letter 191, die Skokumer Bauren), and the French letter of 1815
  says "in favour of Madame Miączyńska", where the English had printed her
  catalogue entry.
- German summaries: the same forms in `site/_data/summaries_de.yml` and the
  units' checked German summaries (42 places).

Left standing, and listed in NEEDS_CONFIRMATION: the Grand Duchy of Posen,
Betsche below Strehlen, Klein Althammer, Pourtalès / not Portalis (the
writer's own correction), and the names that need a ruling (Tarmowo or
Tarnowo, Wrocławek, Schliefen and others).

## The editor's rulings on the names audit (2026-10-03)

Tarnowo, not Tarmowo (the register's `tarmowo` now displays Tarnowo); Ribbeck
for Rybbeck and Rybbek; Kunkel for Kunckel; Dormowe is Dormowo; and in letter
155 the doubtful "Hussaczinski[?]" is Hussarzewski, applied to the
transcription as a recorded ruling (`transcription_decisions.csv`, line
11069), which takes the letters' doubt marks from 252 to 251. Klein Althammer,
from which Hahn wrote letter 189, is Stara Kuźnia by Bierawa (the gazetteer
GOV, LANAWAJO90CG), the works estate of the entail; the register had excluded
it, and now folds it in. The cathedral chapter "zu Wraclawek" in 14525, 28 is
Włocławek: a new place in the register, and the English says so. The scan
shows "Wraclawek" where the transcription reads "Wrocławek"; whether to
correct the transcription is left to the editor. The English and the German
summaries follow (a rule in english_forms.yml; 43 places in the translations,
12 in the English summaries, 25 in the German).

Betsche below Strehlen (letter 119) is left as it is, with the evidence that
it is not Pszczew, for the editor to rule.

Bątkowo (editor, 2026-10-03). The village the contracts and the entail call
Batkowo or Botkow, the village of the Włocławek cathedral chapter from 1239
until the partition, is Bątkowo in Polish and in the English, Batkowo in
German. The register entry, the English translations (7 documents) and
summaries, the German summaries, the era page and the holdings' About pages
follow; Botkow and Botkowo are folded in. The place stays Włocławek, as ruled.

Betsche below Strehlen (editor, 2026-10-03). The small estate in letter 119,
divided among Hussite settlers about 1801, lay near Strzelin in Silesia and is
not Pszczew. The Pszczew entry in the register no longer matches it, so the
letter is no longer listed under Pszczew; the English keeps "Betsche".

Wraclawek and Posen (editor, 2026-10-03). The transcription of 14525, 28 now
reads "Wraclawek" and "Wracla-/wek", as the page has them (scans 0121_b,
0122_a1), where it read "Wrocławek"; the place is still Włocławek, and the
change is recorded in the holding's transcription_decisions.csv. "Grand Duchy
of Posen" stands in the English of 12765 (14, 27, 28) as the state's English
name. Schliefen / Schlieffen stays open. The 9454 and 14525 letters.json files
are back to their CRLF line endings.

Miączyński / Miączyńska (editor, 2026-10-03). Every spelling of the name
(Mięczynsky, Mięczynska, Mieczynski, Miaczynska, Moscinska, Moszynski, ...)
is written Miączyński for Stanisław and Miączyńska for Michalina in the
English. The English was already so; the register's patterns and the rules in
english_forms.yml now cover the forms with e and ę too, and "Madame
Mięczynsky" in the French letter of 1815 is written Madame Miączyńska, so a
new holding is standardised as well. The live site still showed "M. de
Mięczynsky" in 12765, 6 because the names work had not yet been published.

Catchwords said once (editor, 2026-10-03). Every page break in every holding
was read for a catchword the reading text or the English still said twice
("zu || zu", "Salomon Natan || Nathan junior", "§. 1. || § 1."). The line-break
pass had dropped those that stand on a line of their own and open the next
page; it could not see one at the end of a full line, one the transcription
misread, or a repeated section number. 59 more are now recorded in a new
`units/<slug>/catchwords.yml` (Oe 1 Bü 14526: 41, Oe 1 Bü 9454: 11, the Erbet
record 53/71/0/-/57: 5, Oe 1 Bü 14525: 2), which `corpus_pages.py` reads with the line-break
decisions: the reading text drops the whole line or only the words named, and
the transcription keeps them. Each entry names its line by number, text and
the next page's first line, so a shifted corpus is found again or stops the
build. The English followed in 39 corrections in english_corrections.yml
(two of them join a word the page break had split: voluntarily, misfortune);
the translator reads the reading text, so a new translation will not need
them. The repeats that the sentence needs stay ("mit Kolno. || Kolno
grentzet", 14525, 13). english_forms.py no longer applies a correction twice
where the words it looks for are part of its own replacement.

Écus are Reichsthaler (editor, 2026-10-03). The Prince's French letter to
Stein of 1815 (12765, 6) counts in écus, the French that Prussians wrote for
the Thaler; the ministry's German note in the same file gives his 55,000 as
"55000 rt.". The English, as everywhere on the site, now writes Reichsthaler
(a rule in english_forms.yml: 10 in the translation, 3 in its summary), the
German summary Reichstaler, and the era page the same in both languages.

Figures grouped by thousands (editor, 2026-10-03). The reading text and the
English now show 316,000 for 316000 and 76,000 for 76000; the transcription
keeps the page's figures, and verify_site still checks it character for
character. Every number of five digits or more is grouped; one of four digits
only before a currency or measure (1,800 Rthl, 1,500 Morgen) or where it
cannot be a year, so 1797 stays 1797; archive and section numbers are never
grouped. The comma is the documents' own separator where they use one. New
`numerals.py`, applied by corpus_pages.py to the reading text and by
english_forms.py to the English (456 changes in 229 translations, 177 in the
English summaries). All nine holdings rebuilt; their checks pass.

Relation notes on their own line (editor, 2026-10-03). In a document's
header, the note explaining a relation ("Answers Letter 6" and why) ran on
from the link with no space ("Letter 6Stein has passed on ..."). It now sits
on its own line under the link, in the header's softer colour (style.css,
.rel-note).

The timeline brought up to all nine holdings (editor, 2026-10-03). Fifteen
events added, from the holdings and letters the timeline did not yet use: the
sale of Szetlewek (1798), the failed exchange for Krotoszyn and Polajewo
(1798 to 1800), the Hussite and Mennonite settlers (1804), Triebenfeld's
wife's burial (1804), the Invalids' Fund loan (1805), the Erbet lease in court
(1806), the revenue survey (1806), the estates' court still at work in January
1808, the thirty-one lawsuits and the tribunal's refusal (1811), the remission
and the proposed eviction (1811), word of the restitution to Michalina
Prusimska (1811), Humboldt and Hardenberg (1814), the petition of March 1815,
Charlotte von Triebenfeld's letter (1815) and the widow von Brehmer's
petition (1816). Existing events gained documents and corrections: the
title registration now starts in December 1798; the Kamionna and Kolno sale
cites both contracts; Triebenfeld's first arrest is March 1808, not January
1809; the Vienna and Prosna events name his arrival and the line's settlement;
the St Petersburg instruction cites the order of 20 April 1816; the note on
his death no longer says Trąbczyn was sold after 1818. Names follow the
register (Kamionna, Zagórów, Pszczew, Oleśnica, Konotop, Sławięcice, Wrocław,
Poznań, Kalisz), Hohenlohe-Ingelfingen is named as the house style has it, and
the dashes are gone. 54 events, every document link resolving.

Primary sources before Seidel (editor, 2026-10-03). The timeline's
estate claims that rested on Seidel's biography were checked against the
documents. The 1811 proceedings are now told from letters 74a and 74d: the
Invalids' Fund applied on 30 July 1811 to enforce its 50,000 Rthl loan, with
9,375 Rthl of interest unpaid since 1807, and on 1 August the Kammergericht
attached Princess von Sacken's legacy of 80,000 Rthl; the claim that the case
file survives in Berlin is gone. The 1797 entry no longer says Zagórów was the
lordship kept after Trąbczyn was lost; Tilsit and the Final Act cite general
history and letter 271 in place of Seidel. Seidel remains a source, a
secondary one: the documents come first and decide where the two disagree, and
a fact from him alone is cited to him (his separation, the house arrest, Jena,
Prenzlau, his death). The rule is in HOHENLOHE_ERA_PLAN.md and the timeline's
header.

Correspondents named in full, with their titles (editor, 2026-10-03). The
From and To line in a document's header showed the names as the holdings
record them, some in German ("Friedrich Ludwig, Fürst zu
Hohenlohe-Ingelfingen", "Ministerium der auswärtigen Angelegenheiten") and
most as a bare surname ("Hardenberg"). A new reference/correspondents.yml
gives each of the 43 recorded forms a name and the person's title at the time
of the documents, in English and German; the header now reads, for example,
"Karl August von Hardenberg, Prussian State Chancellor -> Prince Friedrich
Ludwig of Hohenlohe-Ingelfingen". The lists on Browse and in search show the
name alone, in the page's language. A recorded form with no entry is shown as
it stands and reported by build_site_data.py.

Places of writing in the page's language (editor, 2026-10-03). The place line
under a document's date showed "Wien" on English pages, and "Blizanow" and
"Swiątniki" without their Polish accents. English pages now use the
register's English form where English has one (render: Vienna, Warsaw), and
German pages the register's name (Wien, Warszawa (Warschau)); "Unknown" is
"Unbekannt" in German. The register gives Blizanów and Świątniki their accents,
with the letters' spellings kept as variants, and St. Petersburg in a dateline
now finds its entry. The English (67 changes in 48 translations, 10 in the
summaries, by a rule in english_forms.yml) and the German summaries follow
("Blizanower Güter" stays, a German adjective).

Document navigation stays in its holding (editor, 2026-10-03). The previous
and next links on a document page, in archival and in chronological order,
ran across the whole edition: the last document of one holding led to the
first of the next, and the chronological order moved between holdings by
date. Both orders are now kept per holding (build_site_data.py), so a reader
browsing one holding stays in it; at a holding's first and last document the
arrow is shown disabled. Checked: no navigation link leaves its holding.

A stray full stop in 12765, 8 (editor, 2026-10-03). Page 2, line 212 read
"den man die Gütter genommen hat. / und der Entschädiget werden muß", one
clause cut in two; the English followed ("have been taken. and who must be
compensated"). The full stop is gone from the transcription (ruling in the
holding's transcription_decisions.csv), and so from the reading text, and the
English reads "have been taken and who must be compensated" (a correction in
english_corrections.yml). The corpus dataset was regenerated with it, and
now also carries Blizanów and Świątniki.

Extent gives the pages only (editor, 2026-10-03). A document's details panel
gave its extent as "34 lines across 2 manuscript pages" with "lines 1-34"
beneath; it now gives the number of manuscript pages alone ("2 manuscript
pages", "1 manuscript page"; German "Handschriftenseite(n)"). The line numbers
stay in the transcription view, where a line is cited.

Document headers tidied (editor, 2026-10-03). Every document is now called
"Document 9 · Draft": the number first, then the kind, where the header had
put the kind first and changed it from one document to the next ("Letter 8",
"Draft 9"); relations and enclosures name "Document 8", and the browser tab
reads the same. The relation notes, which were the evidence for each link
("'den Empfang Ihres ... Schreibens vom 12 v. M.': the Prince's letter of 12
May 1815"), stay in each holding's rulings.yml and are no longer shown. The
[supplied] badge was shown on every date not read from a signature, so also on
the 57 dated from their own dateline; it now marks only the 25 dates supplied
by research, and a new [inferred] badge the 9 inferred from neighbouring
letters, each with its explanation on hover.

The holding named above the document navigation (editor, 2026-10-03). A
document page now states its archival holding on a line of its own above the
archival and chronological navigation, which stays inside that holding: the
reference, linked to the holding's page on Sources, and the archive
("Holding: Oe 1 Bü 9454, Hohenloher Zentralarchiv Neuenstein (HZAN)").

The Szetlewek sale explained (editor, 2026-10-03). "Most of the price goes to
the man who held the farm on pledge" said too little. The timeline and the
era page now say, from the contract (14526, 25), that 8,333 Rthl of the
12,333 went to Ignatz von Radzinski, who had lent money on the farm and held it as
security until he was repaid, and was to vacate it once paid.

Toruń, not Thorn (editor, 2026-10-03). The place register has a new entry,
Toruń (German Thorn), so the documents that name it are tagged with it: the
two replies of February 1799 sending Hohenlohe-Ingelfingen to the Government
at Thorn for the confiscation judgment (14525, 43, 44), and the 1815 frontier
letters (9454, 246, 266, 271). "Thoren" counts only where it names the town;
in letter 104 it means "fools" and is left alone. The English writes Toruń (a
rule in english_forms.yml: 4 translations, 2 summaries), as do the timeline,
the era page and the About page of 14525; the German gives Toruń (Thorn).

No full stop between a day and its ending (editor, 2026-10-03). The 14525
transcription wrote "27.ten Juny 1796", "18.ten Februar" and so on, eight
times; it now reads 27ten, 18ten, 26ten, 20ten, 11ten, each recorded in the
holding's transcription_decisions.csv. With the stop gone the dateline reader
recognises the day, so documents 4, 6 and 9 are now dated 18 February 1802
(they read "February 1802"). The English never carried the stop.

No full stop between the month and the year (editor, 2026-10-03). Every
transcription was searched for stray full stops in dates. Five stood between
a month and its year and are gone: "18ten Februar. 1802" three times in 14525
(4, 6, 9), "20. August. 1796" in Nr. 3570 and "13. May. 1816" in 12765, 19
(whose office note in office_notes.yml is keyed by that line, and follows).
Each is recorded in the holding's transcription_decisions.csv. None remains
between a day and its ending, and the full stops of German ordinals ("den 5.
Juny") and of abbreviations ("d.", "Febr.") are correct and stay. No date and
no English changed.

The Konotop instructions explained (editor, 2026-10-03). The timeline listed
the thirteen powers of attorney of 7 March 1809 (letters 48 and 302) without
saying what they were for. The entry, and the passage on the era page, now
say it from the letter: Hawich, a notary of the Duchy of Warsaw, was to sue to
have Michalina Dąbska removed from Trąbczyn; to have the court administration
put on the remaining estates for unpaid interest lifted, the King of Saxony
having granted debtors three years' grace; to remove Honrichs, who had had
himself appointed its administrator and had sold land without authority; to
sue Oppenheimer and Wolff over 72,000 Rthl; to collect the arrears; and to
appear at the Diet in Warsaw, where every landowner had to appear in person or
lose his estates. The era page writes Konotop, not Kontop.

- **Timeline and era page: who was not paying, and what** (editor, 2026-10-03). The
  entries for 1 January 1811 and July 1811, and the matching paragraphs of the Hohenlohe-
  Ingelfingen years page, now say that the colonists holding farms in hereditary lease on the
  Zagórów estates paid none of their yearly rent ("interest"), that the tenants of Oleśnica,
  Kopojno and Drzewce paid no lease money, and what still fell due (letter 212). The remission
  of a third of the rent is given as Triebenfeld's proposal (letter 215, a Pro Memoria), and the
  eviction as the course he put forward if the estates were to be kept (letter 216).

- **Timeline: Konotop shortened; the 1811 news from Sanitz retitled** (editor, 2026-10-03).
  The Konotop entry gives only the main charges (the full list stays on the era page). The
  entry of 15 August 1811 no longer reads as if the estates were only then to go to Michalina
  Dąbska (Prusimska): they were handed over in 1807, and letter 217 reports how that came about
  (her petition to Napoleon, passed on to the Polish governing commission, which ordered it).

- **Timeline: cryptic entries rewritten; a house-style rule against them** (editor,
  2026-10-03). About thirty entries, in English and German, now say who people were
  (Hoym, Beyme, Struensee, Barbe, Zerboni, Princess von Sacken), what offices and procedures
  were (the War and Domains Chambers, the provincial courts, the mortgage books, court
  administration, the entail), and what happened, from the documents: letter 179a is a draft
  petition for a royal loan of 698,000 Rthl, not a survey that "promises" villages; the 1808
  copies show the Zagórów court still working after Trąbczyn was taken; the King, not the
  chamber, refused the Pszczew sale in 1805; Erbet's costs were 9 Thaler 18 groschen. Polish
  place names: Witów, Piotrków, Nysa. New section "No cryptic statements" in HOUSE_STYLE.md.

- **Timeline: "What was happening" removed** (editor, 2026-10-03). The six-period summary
  under the timeline (site/_data/i18n.yml `movements`) was stale against the rewritten
  entries, and is gone in both languages.

- **People page: one entry per person, full names, alphabetical** (editor, 2026-10-04).
  The two kings appeared twice: a person with a second, document-limited pattern
  (`issuer_match`) was listed once per pattern; build_site_data.py now lists each person
  once. Each person is headed by the full name, surname first ("Hardenberg, Karl August
  von"), from the new reference/people_headings.yml; forenames only where the documents or
  the biography establish them. The list is alphabetical by that heading by default, with
  Z-A, most mentions and fewest mentions as options; equal counts stay A-Z. The person
  filter on Browse uses the same headings and order.

- **People: one entry per person** (editor, 2026-10-04). Michaelis, Goldbeck, Kleist and
  Meyer each covered several people. They are now eleven entries, each found only in the
  documents that name that person (a new `only_in` in reference/people.yml, honoured by
  entities.py). "Michaelis" as the feast of 29 September (14526-4, -5, -10) no longer
  counts as a person, and Meyer Bernhard's mentions no longer count under a separate
  "Meyer". Open points in NEEDS_CONFIRMATION (Identifications).

- **van der Lahr** (editor's question, 2026-10-04). The documents write the Berlin creditor
  "van der Lahr" 23 times and "von der Lahr" 6 times. The English, the People page and the
  era page now write van der Lahr throughout (english_forms.yml, name-van-der-lahr); the
  transcriptions keep each spelling as written.

- **Sort buttons readable when pressed** (editor, 2026-10-04). The pressed button's text used
  an undefined colour (`--bg`), so it took the button's own background colour and vanished in
  dark mode. It now uses `--paper`, light on dark in the light theme and dark on light in the
  dark one (People and Places pages).

- **People: duplicates merged** (editor's question, 2026-10-04). Four people had two
  entries under two spellings: Grevenitz (Grävenitz, "Grev:"), Carl Titz (Tietz, the forest
  inspector who leased Drzewce), Koppe (Koppen, back from Paris in 1808) and Metzig (Melzig,
  written both ways in one passage of letter 41). Each is now one entry, and the English
  uses one spelling (english_forms.yml, person-spellings). The "Born" entry was catching the
  start of Bornstädt and Bornsted: it is now Dr Ernst Gottlob Born of Frankfurt an der Oder
  alone (two certifications), and Bornstädt finds all his spellings. Haugt now also finds
  "Haucht" (letter 31). Knoblauch and Knobloch are two men and stay apart.

- **German biographies: Polish place names** (editor's question, 2026-10-04). 79 German
  biographies on the People page used German place names (Kaemen, Betsche, Kalisch, Breslau,
  Koschentin, Wittow and others). They now give the Polish name with the German in brackets
  at its first mention (Kamionna (Kaemen), Pszczew (Betsche)), as the site does elsewhere;
  Warschau and the Großherzogtum Posen stay as German writes them. The biographies of the
  people merged or split today were rewritten with them.

- **People and Places: documents as cards** (editor, 2026-10-04). Each person and place
  now shows a counts line and a list that opens to the documents as cards, the same card as
  Browse (the card code moved from browse.js to a shared assets/doc-cards.js, which Browse
  now uses too), with the summary cut to two lines, in date order or grouped by archival
  holding. People and named places are counted by mentions (how often the documents name
  them, entities.mention_counts), with the number of documents beside it; each card says
  how often that document names them. Places of writing and estates count documents. The
  cards come from assets/cards.json (the search index without the texts, fetched when a
  list is first opened); without script the numbered links remain. A link to
  /people/#slug opens that person's list.

- **Document lists indented** (editor, 2026-10-04). An opened list of documents on the People
  and Places pages is indented under its entry, with a rule down the left, so the cards read
  as that person's or place's.

- **Places page: estates only** (editor, 2026-10-04). The page lists only the estates the
  documents concern (55), sortable and with each estate's documents as cards; places of
  writing and places named in the text are no longer listed there (a document page still
  shows both). Its introduction is rewritten to say plainly what an estate entry is. On a
  document page, a place named in the text links to the Places page only where it is also an
  estate.

- **Nr. 3709 transcribed** (2026-10-04). The editor supplied the transcriptions of I. HA GR, Rep. 7 C,
  Nr. 3709 and a second reading of its French petition. The file is divided into fifteen documents
  (one per letter, order or draft), the receiving office's writing set apart, 57 words corrected on
  the witness of the file's own twins and formulas, the Grand Chancellor's paraph given as
  G[oldbeck], and each document summarised in German and English. It is the suit for Brzyce
  ("Brzezier Güter"), now tagged as that estate. The holding's page, the timeline entry and the
  paragraph of the era essay are rewritten from the text, in both languages. The edition has 441
  documents. Not yet translated; the summaries have not had the claim check. See
  `units/ihagrrep7cnr3709/notes.md`.

- **Nr. 3709 translated** (editor, 2026-10-04). The fifteen documents of I. HA GR, Rep. 7 C,
  Nr. 3709 (Michalina Prusimska's suit for the Brzyce estates, 1800-1802) translated into
  English in session, under the rules translate.py gives its translator (its system prompt,
  termbase and canonical names, generated for this unit), written to the translation cache
  as translate.py writes it, checked by check_translations.py (nine rows, none blocking) and
  published. The French petition (document 15) translated from the French; the badly read
  draft of 31 December 1800 (document 14) marked illegible where it does not read. Sixteen
  glossary candidates ruled under excluded:; the holding is marked translated.

- **Nr. 3709 worked into People, Places and the timeline** (editor, 2026-10-04).
  - People: the biographies of Michalina Prusimska (her suit of 1800 for the Brzyce estates,
    the judgment of 9 December 1800, her petition from Dresden of 1802), Antoni Prusimski
    (still living in 1800; the life interest argued over), Goldbeck (his order of
    December 1800 and its withdrawal), Danckelmann (vice-president at Poznań, then president
    at Kalisz) and von der Reck (the petition of 1802), in both languages. Danckelmann is
    now also found where his name is broken over a line.
  - Correspondents: the Grand Chancellor Goldbeck, the South Prussian Governments at Poznań
    and Warsaw, the Superior Appeal Senate of the Kammergericht and Michalina Prusimska.
  - Places: "Ingelfingen" was tagged as a place named in the text wherever a document wrote
    the Prince's name, "Hohenlohe Ingelfingen" (170 of 215 matches); the pattern now finds
    only the town, the principality and the Prince "von Ingelfingen".
  - Timeline: the 1800 entry is retitled "Prusimski's daughter sues for the Brzyce estates".

- **III. HA MdA, III. Nr. 12366 added** (2026-10-04). The foreign ministry's file on Michalina
  Miączyńska's claim and on the Polish judgments against Hohenlohe-Ingelfingen's creditors, 1818
  to 1827: six documents on 37 pages and the cover, five in French and one in Polish. The fifteen
  openings were cut at folds the editor placed or approved, and scans 0004 and 0005, one opening
  photographed twice round a slip in the gutter, give the left and the right page. The editor's
  transcription, one text by paragraph, was cut to the pages; three datelines and addresses stand
  on the page where they are written; the editor added the cover's volume line. The whole text was
  corrected against the scans: 72 words in the clean French copies, 21 passages in the
  ministry's draft and 64 in the Polish judgment. A reader's pencil notes in the margins of the
  Warsaw report, first read by the editor, are transcribed at the foot of each page. Dates, places, senders, types and languages are
  set, each document is summarised in German and English, and the holding has its page, three
  timeline entries and a paragraph in the era essay, in both languages. New people: Bernstorff,
  Tarczewski, Wybicki, Niemojewski, Wichrowski, Rembowski; Grotowski given an entry; "Leyner",
  "Zastrof", "Varsovie" and "Kamienno" matched to Leixner, Zastrow, Warsaw and Kamionna. The
  edition has 447 documents. Not yet translated; the summaries have not had the claim check. See
  `units/iiihamdaiiinr12366/notes.md`.

- **Nr. 12366 translated and its summaries checked** (editor, 2026-10-04). The six documents of
  III. HA MdA, III. Nr. 12366 translated into English in session under the rules translate.py
  gives its translator, a pilot first (Alopeus's letter and the Polish judgment, French and Polish
  being new to the edition), written to the translation cache as translate.py writes it, checked
  by check_translations.py (two rows, French words the termbase mistakes for German) and
  uncanonical_names.py (nothing), and published. The five French documents translated from the
  French, the judgment from the Polish, the reader's German pencil notes where they stand. The
  pages are kept in `units/iiihamdaiiinr12366/intake/translation/`. The six German summaries
  claim-checked against the documents, as read_letters.py --verify checks: 70 statements, one
  overstated (a pencil note given to the Prince that names no one), weakened in both languages
  and on the holding's page. Szetlowek, Szeltowek and Szetlowka matched to Szetlewek. The
  holding is marked translated.

- **III. HA MdA, III. Nr. 12367 added** (2026-10-04). Fourteen scans from the second volume of
  the foreign ministry's file on Michalina Miączyńska's claim, 1828 to 1832: eleven documents on
  15 pages and the cover, eight in French, two in Polish and one in German. All concern the
  compensation of the Breslau banker Weigel for the mortgage of 30,000 thalers the Polish courts
  struck off Trąbczyn: the answers of Baron Mohrenheim, of the finance commission and of Engel to
  the Prussian consul general Schmidt, and the exchange between the finance minister Prince
  Lubecki and Weigel in the autumn of 1830. The one opening (scan 0009) was cut at its fold. The
  editor's transcription, by paragraph except for Weigel's German letter, was cut to the pages;
  one page holds the end of one document and the head of the next. The signature the editor asked
  about is Baron Mohrenheim's, and it is given on each of his four pieces as it stands there. The
  whole text was corrected against the scans: 62 passages, most in the two hurried notes and the
  two Polish letters, with the German translation written beside the Polish as a witness. Dates,
  places, senders and languages are set; two notes are left undated. Each document is summarised
  in German and English, and the holding has its page, three timeline entries (the timeline now
  runs to 1832) and a paragraph in the era essay, in both languages. New people: Mohrenheim,
  Schmidt (the consul), Lubecki, Engel, Lubowidzki, Drake, Eisenhardt (the banker, parted from
  the Berlin agent Eysenhardt); "Césarévitch" matched to Grand Duke Constantine. Two small
  additions to the build: a by-paragraph ruling can name one document's part of a shared page
  ("8:0009_a2"), and a paragraph break no cue proposes can be written into
  `paragraph_decisions.csv` by hand (cue `hand`). The edition has 458 documents. Not yet
  translated; the summaries have not had the claim check; the German translations beside the two
  Polish letters are not transcribed. See `units/iiihamdaiiinr12367/notes.md`.

- **AGAD 1/174/0/2/73 and 1/174/0/1/6 added** (2026-10-04), the first holdings from the Archiwum
  Główne Akt Dawnych in Warsaw: the papers of July 1807 by which the Governing Commission, the
  provisional Polish government, returned the Prusimski estates to Michalina Dąbska. From the
  commission's file of its stay at Dresden (1/174/0/2/73), four documents on five pages: her
  petitions to the commission of 20 and 23 July and to Napoleon of 21 July, and the commission's
  draft resolution of 21 July 1807. From its register of orders and resolutions (1/174/0/1/6),
  two documents on three pages: the order of 12 July to carry out Napoleon's decree for Józef
  Wybicki, and the fair copy of the resolution of 21 July. Each image shows an opening, of which
  the editor wanted one side; the eight pages were cut out by boxes recorded in each unit's
  `intake/build_pages.py`. The editor's marks 05, 07 and 08 are leaf numbers, so image 06 is
  used as well. The transcriptions were cut to the pages; the commission's received notes stand
  at the foot of each petition as office text; the address of the petition to the Emperor is a
  page of its own. Corrected against the scans: 25 passages and two added lines in the first
  holding, nine passages in the second, most of them the writers' spelling and abbreviations put
  back; the received note on the petition to the Emperor now reads that it was presented by the
  Prince Director of War on the Emperor's order. Dates, places, senders, types and languages
  are set; each document is summarised in German and English; each holding has its page in both
  languages; one timeline entry (21 July 1807) and two sentences in section V of the era essay.
  New people: Małachowski, Łuszczewski, Bischoffwerder; Sanitz, Niemojewski, Hohenlohe and
  Michalina Dąbska matched in the forms of 1807; Dresden, Warsaw and Kolno matched in their
  Polish and French forms. The glossary entry for the Prussian court called Regierung no longer
  marks "die preußische Regierung" or "the Prussian Government": 36 marks gone, in these
  holdings and in Nr. 12366 and Nr. 12765. Both holdings are placed in the Hohenlohe-Ingelfingen
  years pending the editor's ruling. The edition has 464 documents. Not yet translated; the
  summaries have not had the claim check. See `units/agad11740273/notes.md` and
  `units/agad1174016/notes.md`.

- **Nr. 12367 and the two AGAD holdings translated and their summaries checked** (editor,
  2026-10-05). The seventeen documents of III. HA MdA, III. Nr. 12367 (eleven), AGAD
  1/174/0/2/73 (four) and AGAD 1/174/0/1/6 (two) translated into English in session under the
  rules translate.py gives its translator, each from its own language (French, Polish, and
  Weigel's German reckoning), written to the translation cache as translate.py writes it,
  checked by check_translations.py (one deliberate row: Polish florins for "fl." in a Polish
  church capital) and uncanonical_names.py (nothing), and published. The pages are kept in
  each unit's `intake/translation/`. The seventeen summaries claim-checked against the documents, as
  read_letters.py --verify checks: 119 statements, one overstated (Nr. 12367, document 6: the
  German said the finance minister had the estates valued on the spot; he only ordered it),
  weakened in the German summary and on the German holding page. Before translating, a fault
  in Nr. 12367 was put right: the dateline "Mardi." of Mohrenheim's note (document 3) stood
  under the next document's marker, so document 4 had an empty first page; the marker, the
  scan map and the two web images' labels are corrected (the edition now has 1529 manuscript
  pages). Glossary candidates "JW." and "mars" ruled out. The three holdings are marked
  translated.

- **Home page figures** (editor, 2026-10-05). The span under the counts was typed into the page
  as 1798-1816; it is now written by build_site_data.py from the dated documents (1794-1832).
  The opening paragraph, in both languages, now says the originals are German, French and
  Polish and that the published papers run on to the dispute over the Prince's debts, until
  1832.

- **Edition guide brought up to date** (editor, 2026-10-05). "About this edition", in both
  languages, described two HZAN files and 348 documents. It now lists the thirteen holdings in
  four archives (HZAN, GStA PK, APP, AGAD), gives 464 documents and 1,529 pages, the French and
  Polish documents, 609 marks of doubt in 233 documents (with the gap mark `[...]` added to the
  table), nine undated documents, that every published document is in the Hohenlohe era, how
  écus and Polish florins are rendered, and that all 459 translations are drafts.

- **APP 53/968/0/-/801 added** (2026-10-05), the second holding from the State Archive in
  Poznań: sixteen pages from the papers of Albert Breyer, copied about 1930, of three papers on
  the parcelling of the Zagórów and Trąbczyn estates. One document, dated 21 March 1806: the
  Prince's general power of attorney for Triebenfeld of 19 February 1805, the consent of the War
  and Domains Chamber at Kalisz of 28 January 1806, and the hereditary lease of 100 Hufen of the
  Drzewce forest to eighteen settlers, whose opening is missing. The seventeen images were
  staged uncropped; the editor's transcription was cut to the pages (page 16 had no mark) and
  the cover's text added from the image. Corrected against the scans: 84 passages, with the
  copies of the power of attorney in APP 53/71/0/-/57 and of the consent in Oe 1 Bü 14526
  (document 8) as second witnesses. A skipped line and a half of the consent was restored;
  Michael Just's share is 5 Hufen, not 10; the lessee Siemert or Liemert is Liewert; "Petenck"
  is Schenck; the three crosses of the eleven lessees who could not write are given as "xxx".
  Summarised in German and English; holding page in both languages; two timeline entries (28
  January and 21 March 1806) and a third source for the entry of 19 February 1805. Five place
  patterns widened for the copyist's forms (Trompczyn, Marianten, Szedlewek, Święcia and Święca,
  Nowawieś); the last also matches "Nowawieś" in III. HA MdA, III. Nr. 12367, document 7. The
  edition has fourteen holdings and 465 documents. Not yet translated; the summary has not had
  the claim check. See `units/app539680801/notes.md`.

- **APP 53/968/0/-/801 divided into three documents** (2026-10-05, the editor's ruling the
  same day): the power of attorney (document 1, 19 February 1805, Guhrwitz), the consent
  (document 2, 28 January 1806, Kalisz) and the lease contract (document 3, 21 March 1806,
  Mariantów), with a relation from each of the first two to the contract. Three summaries in
  place of one; the holding page cites each paper by its own number; the timeline entries
  point to the right documents; the correction log re-keyed
  (`intake/split_documents.py`). The address `/documents/app539680801/1/` is now the power
  of attorney; the contract is at `/3/`. The editor also confirmed "Dr." before Johann
  Wendel Heilmann and Michael Just's 5 Hufen. New person: Heinrichs, the chamber's
  Commissionsrath and Oeconomie-Commissarius who attests this lease and the Althütte lease
  (Oe 1 Bü 14526, document 16), kept apart from Martin Honrichs. The edition has 467
  documents.

- **What the rest of the site owed APP 53/968/0/-/801** (2026-10-05). The era essay said the
  crown had licensed the division of Trąbczyn and Zagórów the year before the punctation of
  April 1805. Both copies of the consent are dated 28 January 1806, on cabinet orders of
  October and December 1805; the sentence is corrected in both languages and links both
  copies. A short paragraph on the Drzewce lease added to section III (no entry money, four
  free years, on uncleared forest). The holding pages of APP 53/71/0/-/57, Oe 1 Bü 14526,
  Nr. 3705 and Oe 1 Bü 9454 name the new holding among their related holdings, in both
  languages. APP 53/71/0/-/57 is no longer described as the only holding from Poznań.

- **APP 53/968/0/-/801 translated and its summaries claim-checked** (2026-10-05, in session at
  the editor's word). The three documents were translated beside the published English of the
  other copies of the same texts, so the same formula has the same English; where this copy
  differs from them in a word it is followed and the difference flagged. check_translations.py
  raised two rows, neither a fault; uncanonical_names.py nothing in this holding. Seven of the
  copyist's spellings became variants in `reference/places.yml` (Trompczyn, Marianten,
  Mariantow, Szedlewek, Święcia, Święca, Świątnik). The claim check held 35 statements of the
  three summaries to the documents and weakened two. The English summaries, the holding page
  and a timeline entry now use the termbase's words (demesne farm, Government, Midsummer).
  Status `translated`; every document with text now has an English translation, 462 of 467.

- **I. HA Rep. 162, Nr. 295 added** (2026-10-05), from the file of the Prussian state treasury
  on the 50,000 Rthl registered on Zagórów: the cover and eleven pages of copies of 1805, in
  three documents. Triebenfeld's bond to the General Invalids' Fund (Berlin, 28 January 1805),
  which pledges a fifth of the Prince's bond for 250,000 Rthl; the South Prussian Government's
  certificate of its second acknowledgement (Kalisz, 5 March), with the note of its entry in
  the mortgage book; and the mortgage certificate for Zagórów (13 March). The editor
  transcribed from the joined page images, line by line. Corrected against the images: 34
  passages; the list of estates in the bond ends "Grądzyn", not "Trąbczyn"; "Seehandlungs-
  Obligationen", "Koniner Kreise", "Frist". Line ends and paragraphs ruled by hand. Summarised
  in German and English and claim-checked (27 statements, one weakened); translated in session
  (no check rows); holding page in both languages; the timeline entry for the loan, section III
  of the era essay and the pages of Oe 1 Bü 14525, Oe 1 Bü 9454 and Nr. 3705 link to it. New
  person: the Regierungsrath v. Lichnowski at Kalisz, kept apart from the creditors of that
  name. Glossary: `rubrik` added, three abbreviations ruled out. The edition has fifteen
  holdings, 470 documents and 1,558 pages; 465 have an English translation. See
  `units/iharep162nr295/notes.md`.

- **I. HA GR, Rep. 7 C, Nr. 1414 added** (2026-10-05), "Aufenthalt des Anton v. Prusimski in
  Venedig": three documents on four pages. An extract in French from dispatch No. 423 of Count
  Cattaneo, the Prussian resident at Venice, of 14 December 1796 (Prusimski, ill and broken by
  his wife's death, has asked for and been given a certificate that he cannot travel), with
  the slip on which the councillor Raumer directs on 8 January 1797 that Hoym and Schrötter be
  notified; the department of foreign affairs' draft of 11 January 1797 to Hoym, Schroetter
  and the Grand Chancellor von Goldbeck; Schrötter's reply of 29 January. Of seven scans the
  editor wanted four; three openings were cut to the written side. The editor's line-by-line
  transcription was cut to pages, with the department's marks on the papers it received set
  apart as office text. Corrected against the scans: 20 passages; Raumer (for Rammer, Maunes,
  Maurer), Goldbeck as third addressee, Haugwitz and a doubtful Alvensleben as signatories,
  "affatigué" restored in the extract. Summarised in both languages and claim-checked (19
  statements, two weakened); translated in session, no check rows; holding page in both
  languages; a timeline entry (14 December 1796) and two sentences in section I of the era
  essay; Nr. 3570 and Nr. 3709 link to it. New people: Cattaneo, Raumer, Schroetter and
  Haugwitz, who is now also indexed in the letters of Oe 1 Bü 9454 that name him. New place:
  Venice. The statement of Miączyńska's claim of 1818 (III. HA MdA, III. Nr. 12366, document
  2) tells what the certificate was for and names the resident as "Comte Cathane"; he is now
  indexed there, and the holding page, the essay and the timeline say so. The edition has
  sixteen holdings, 473 documents and 1,562 pages; 468 have an English translation. See
  `units/ihagrrep7cnr1414/notes.md`.

- **The editor's rulings of 2026-10-05, and what was done on them.** Struck-out text is not
  transcribed, and a translation of the time written beside a document is not transcribed
  where the original is given: both are now standing rules (`docs/EDITORIAL_RULES.md`), which
  closes the struck clause of the draft resolution of 1807 (AGAD 1/174/0/2/73) and the German
  columns beside the Polish letters of III. HA MdA, III. Nr. 12367. Heinrichs and Honrichs are
  kept separate. In I. HA GR, Rep. 7 C, Nr. 1414 Raumer, Goldbeck and Haugwitz stand, the
  papers are filed under no estate, and the signature given as "[Alvensleben?]" is on a spot
  sheet. The three unread words of the Polish judgment in Nr. 12366 stand. In Nr. 12367 the
  end of Baron Mohrenheim's undated note (document 3, scan 0004) was read again on
  enlargements: the last sentence is "J'ai ici un tems affreux qui glace parfois mes passions
  champêtres" (for "qui font parfois mon pain de négrêtes [?]"), and the line written
  sideways in the margin is added, "Pourriez Vous m'accorder pour 2 j. le [Courier?] de
  [Londres?] ?", set apart on the page (`sideways.yml`), with the English and the summary
  rewritten to match. The signature of the letter of 29 September 1830 (scan 0007) was tried
  and is still not read. The fifteen German summaries of I. HA GR, Rep. 7 C, Nr. 3709 were
  checked statement by statement against their documents
  (`units/ihagrrep7cnr3709/intake/claim_check.yml`): 67 statements, 65 supported, two
  weakened in both languages (document 5: the office's date of 2 December 1800 is not said to
  be the day of receipt; document 15: the note that refers the petition to Minister von der
  Reck does not name the Cabinet). Later the same day the editor looked at three of these
  readings. The two last words of the margin line, first given as "[Courier?]" and
  "[Londres?]", are left as "[Rev…?]" and "[P…?]", what the editor sees of them, and the
  guess that had gone into the summary was cut. The signature on scan 0007 is not Prince
  Lubecki's as far as the letter shows: the writer speaks of the minister of finance as
  another person. The first signature under the draft of Nr. 1414, which the editor cannot
  verify, now stands as "A[lvensleben]", the initial read and the name supplied from his
  office, as with Goldbeck's paraph in Nr. 3709; Alvensleben is indexed. The edition has 610
  marks of doubt.

- **Published** (2026-10-05, at the editor's word): I. HA Rep. 162, Nr. 295 and I. HA GR,
  Rep. 7 C, Nr. 1414, with the rulings and readings of the same day. Sixteen holdings, 473
  documents, are live.

- **`docs/WORKING_NOTES.md` added** (2026-10-05, at the editor's word). The editor works in
  desktop and cloud sessions, and what a desktop session had learned was kept only in a
  memory folder on that machine. It is now in the repository: how the editor works, the
  lessons behind the editorial rules, what went wrong when holdings were added, where a
  summary is kept, the traps in the tools, and what differs between desktop and cloud.
  `CLAUDE.md` tells every session to read it and to write new lessons into it. Two rulings
  of the same day were added to `docs/EDITORIAL_RULES.md`: an unread word is not completed
  with a guess, and an initial with a supplied name is written `A[lvensleben]`.

- **Lessons go into the repository: made a rule, with a check** (2026-10-05, at the editor's
  word). `CLAUDE.md` now states it as a standing rule: what a session learns is written into
  `docs/WORKING_NOTES.md` or the document it belongs to and committed in the same sitting,
  and every report on committed work ends with a line beginning "Lessons:". A check enforces
  it in desktop and cloud sessions: `.claude/settings.json` has Claude Code run
  `.claude/hooks/lessons_check.py` whenever Claude is about to stop; if work was committed
  without the notes changing and without that line, Claude is stopped from finishing once and
  told to answer. Tested on nine cases in a throwaway repository.

- **The About page rewritten for the reader** (2026-10-05, at the editor's word: it was "way
  too dense" and read like the project's own memory). `site/reading-this-edition.md` and its
  German counterpart went from about 2,500 words to about 1,600, in the order a reader asks:
  what the edition is, where the documents are held, how the text was made and how far to
  trust it, how to read a document and its marks, the translations and summaries, dates,
  names and money, numbering and grouping, what is open, how to cite. Removed: the counts of
  line-break marks and how they were decided, the catchword table, file names, image sizes,
  per-holding page counts and single unresolved readings. Corrected: the page described a
  line-end mark the transcription view no longer shows and listed the page image as a
  fourth view; it said "all 459" translations are drafts where there are 468. Added: that
  the translations and summaries are drafted by an AI model, the bracketed-letters mark,
  the labels for office notes and sideways text, and the advice to check a passage against
  the page image. The site footer now names Warsaw among the archives. The rule for this
  page is in `docs/HOUSE_STYLE.md`, "About the edition".

- **How the edition describes who made the text** (2026-10-06, the editor's correction). The
  About page said the transcription "was not made by a trained palaeographer". The editor
  is an amateur palaeographer, with the work supported by AI. The page now says so in those
  words, says that machine reading leaves a share of wrong characters which a language
  model reduces but does not remove, that the editor has accepted the remaining inaccuracy
  for this project because of the number of documents, and that anything taken from the
  texts for academic work should first be checked against the original document. The
  sentence "It was not made by a trained reader of old handwriting" was removed from the
  "How it was prepared" text of eight holdings, in both languages.

- **The English translations are no longer called drafts** (2026-10-06, the editor's ruling).
  The About page no longer says that all translations are drafts or that none has been read
  against the manuscript; a document page no longer shows "status: draft" above its English;
  the rights page says the translations were made by an AI model and to quote the original
  language; and the closing sentence "The English has not yet been read against the scans"
  is gone from the eight holdings that had it, in both languages. The `status:` field in the
  translation files is unchanged. The Glossary page no longer opens with "The definitions are
  drafts", which was also out of date (56 of its entries are checked), and an unchecked entry
  now reads "to be checked against" its reference work, without the word "draft".

- **APP 53/17/0/-/Konin Gr.145 checked in full** (2026-10-06). The editor asked for the whole
  text to be checked for dropped phrases. All 122 pages were read against the scans: 233
  passages corrected, 26 of them places where the transcription lacked words that stand on
  the scan (27 with the one found before), the rest misread words that change a meaning.
  Three of the dropped phrases change what the record says the court found or did; the
  largest, about sixty words on leaf 709 verso, is the court's finding that Chełmski raided
  the inn with armed men. The English, which is the editor's, already had the right sense in
  most places and was changed in 32: 24 to add what had been dropped, seven where it had
  followed a misread word, and one where it read the Polish differently (two weeks in the
  tower, not twelve). One paragraph on leaf 680 which the English lacked was translated in
  session. The summary's sentence on Chełmski's sentence was rewritten and checked (18
  statements). The fonds and the archive's account of the castle court are on the holding's
  page. The folds the scans are cut at were found again, after the first ones proved to cut
  the line ends of left pages, and wait for the editor's approval
  (`review/app53170koningr145/folds/`). The dropped phrases are on a sheet for the editor
  (`review/app53170koningr145/dropped/`). Not published.

- **APP 53/17/0/-/Konin Gr.145 added** (2026-10-06), the first holding of the Prusimski era:
  the decree of the commission that the Polish parliament appointed in 1774 to settle the
  boundary between Antoni Prusimski's Trąbczyn and the Chełmski brothers' Łukomia. It sat on
  the disputed ground from 13 September 1775 under Ludwik Dąmbski, voivode of Brześć
  Kujawski, and its decree was entered there on 23 September 1776 and copied into a court
  book of Konin. One document, 122 pages, Polish with Latin. The 62 scans of openings were
  cut at the fold. The editor's transcription (modern Polish spelling, by paragraph) and the
  editor's own English translation were brought in page by page; the translation was not made
  again. At the editor's word the text had a light check: four of 121 written pages and the
  signatures were read against the scans, 23 readings corrected (one restores six dropped
  words on leaf 673, in both languages), a line of the title page added, and 93 dropped
  accents put right through the text. Summary in both languages, 16 statements checked;
  holding page in both languages; the era is now populated and the story page and the About
  page say so; a timeline entry for 13 September 1775. New person: Ludwik Dąmbski. New place:
  Brześć Kujawski. Three changes to the tools: a document longer than Python's CSV field
  limit can be read (`unitlib.py`); a person or place entry can be shut out of named
  documents with `not_in` (`pipeline/build/entities.py`), used for seven entries that matched
  other people or ordinary Polish words here; and `decree` is a kind of document. The
  edition has seventeen holdings, 474 documents and 1,684 pages; 469 have an English
  translation. See `units/app53170koningr145/notes.md`.

- **I. HA Rep. 162, Nr. 295 scaffolded** (2026-10-05): the editor photographed each of its
  eleven pages twice, top and bottom. The two photographs of each page were joined into one
  page image along a seam between two lines of writing (`units/iharep162nr295/intake/`), so
  that no line stands twice. Twelve page images wait for the editor's transcription; the unit
  is `draft` and not built.

## Deliverables produced

`letters.csv` / `letters.json` (database), `von_Triebenfeld_Hohenlohe-Ingelfingen_chronological.txt`, `collation_48_302.md`, `transcription_error_profile.md`, `phase2b_transcription_audit.md`, `currency_normalisation_report.md`, `parsed_dates_review.csv`, `phase2_proper_noun_report.md`.
