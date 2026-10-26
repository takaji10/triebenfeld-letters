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

- **Four early entries from the court books of Konin added** (2026-10-06 and 10-07), the second
  batch of the Prusimski era, all Latin, six documents: APP 53/6/0/-/17, an order of 12 June
  1589 for an inspection after a new pond at Łukom flooded the woods of Trąbczyn, now the
  earliest document of the edition; 53/6/0/-/36, two default judgments of 1644 for notches cut
  into trees and timber felled; 53/6/0/-/40, the decree of 26 January 1728 sending a
  commissioner onto the disputed ground; 53/6/0/-/45, the decree of 1763 suspending a suit
  over potash until the boundary is decided. Each was read whole against its scans. The
  editor's Latin of these was a first reading (the entry of 1589 had 109 marks of doubt in 713
  words and was read again whole at the editor's word); the neighbouring entries on the same
  pages, in the same set words, settled most of it. The editor's English is revised to follow:
  the entries of 1644 are default judgments, not "concessions"; in 1589 the court adds one of
  its messengers, not "a mutual term"; in 1728 six thousand shingles were burned, not 160; in
  1763 it was Prusimska who sent the potash off. The decree of 1775 cites the orders of 1589
  and 1728 by their days, which dates both. Summaries in both languages, claim-checked;
  holding pages in both languages; new person entries (Katarzyna and Krzysztof Prusimski, the
  Trąmpczyński and Łukomski families; the Chełmski family curated). For the tools: a shared
  helper for court-book holdings (`pipeline/intake/courtbook.py`); a date taken from the
  heading of a court's sitting (`dates: sitting`); a fold page on which the editor moves the
  lines and saves them; a page of what the checks changed, graded
  (`pipeline/review/changes_page.py`); the glossary gate skips wholly Latin documents. Konin
  Gr.136 (1754) is not built: its middle is not transcribed. The edition has 21 holdings, 479
  documents and 1,696 pages; 474 have an English translation. Not published.

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

## The Prusimski era: the court books of Konin and Kalisz, 1589 to 1788 (2026-10-06 and 10-07)

- Twenty-one holdings from the State Archive in Poznań added in one run, 92 documents: the boundary decree of 1775 (Konin Gr.145), six entries of the land court's books of decrees (53/6/0/-/17, -/36, -/40, -/45, -/46, -/47), three of the castle court of Kalisz (Kalisz Gr.414, Gr.424, Gr.425), and the Konin castle court registers Gr.136, Gr.114, Gr.115, Gr.116, Gr.117, Gr.118, Gr.119, Gr.120, Gr.121 and the decree of 1782 in Gr.153. Each entry of a court book is a document. Not published: the editor reviews the folds, the page of changes and `docs/PRUSIMSKI_QUESTIONS.md` first.
- The editor's transcriptions and English translations are kept. Every holding was read against its scans, the short ones whole, four long ones (Konin Gr.117, Gr.118, Gr.153, Gr.119) by the light check, which their pages say. Each correction is logged with its reason, and `review/changes/` lists for the editor what changed and how much it matters.
- Readings that changed what the documents say: Paweł Prusimski is Antoni's uncle ("Patrui", not "Patrii"; Konin Gr.117); the surveyor of 1782 is sworn ("jurato", not "jurisdictione"), and the sittings on the ground are "condescensio", not "conditio" (Konin Gr.153); the oath laid on Prusimski in 1783 is that the arrest did not reach his two men ("Arestum non praevenit"; 53/6/0/-/47, read with Konin Gr.119); the wood sold to Tracholz is oak (Konin Gr.120).
- What the holdings established together: the commission of 1775 ended in two decrees, one for each side (Konin Gr.116, Gr.117); the Crown Tribunal decided between them on 23 January 1782 and confirmed it on 17 October 1782, and forty-one mounds were raised from 30 November to 3 December 1782 (Konin Gr.118, Gr.153). The About page, the story page and the era's blurb say so now; they said that the decree of 1775 fixed the boundary.
- `pipeline/intake/courtbook.py` (new): the shared steps of a court-book holding, from cutting the scans to the summaries, driven by one `intake/holding.py` per holding. `pipeline/review/changes_page.py` (new): the page of changes. Dates may be taken from the heading of the court's sitting (`dates: sitting` in rulings.yml). Kinds of document added: report, delivery, protest.
- The translation check no longer takes a chestnut mare ("Equam Castaneam") for a misread "hypocaustum".
- Figures: 564 documents on 1,832 pages in 36 holdings, 1589 to 1832; 86 in Latin; 912 marks of doubt; 559 translated.
- **The editor's second review of the Prusimski-era run (2026-10-07).** At their word the four holdings that had only the light check were read through against the scans: Konin Gr.117 (159 more corrections), Gr.118 (133), Gr.153 (106) and Gr.119 (8). The record of each is `intake/full_check.json`, applied by `holding.py --full` (`courtbook.full_check`). No document is marked as a rough reading any more; the marks of doubt in the edition fell from 912 to 743. What changed the sense: in the Tribunal's decree of 1782 Orłowski is sentenced to pay Prusimski, not the reverse, the two officers are boundary chamberlains, and words passed over in the ruling on Martin Hunt are restored (Gr.153); in Chełmski's protests of 1778 "jurto" is an oath, not a jurisdiction, and "pro invalibili" is "invalid" (Gr.117); three lines restored in the protest against the land court of 1782, and Teresa Bogdańska is the successor of her two late sisters (Gr.118).
- Two entries the editor had photographed were transcribed and translated in session and added as documents: 53/6/0/-/46 entry no. 17 (the land court's decree of 1777 on the debt Chełmski bought from the merchant Tracholz) and 53/6/0/-/47 entry no. 43 (a hearing on the ground fixed in 1784 for the boundary of Biskupice and Łomów, with Prusimski cited).
- Jakub Górski, boundary chamberlain of Inowrocław, has his Polish form in the English; the transcription keeps "Gorski" (the editor). Paweł Prusimski as Antoni's uncle, "jurato" and "condescensio" confirmed by the editor.
- The fonds of 53/6 ("Księgi sądu ziemskiego w Koninie") and 53/15 ("Księgi sądu i urzędu grodzkiego w Kaliszu"), with the archive's description, are on the nine holdings' pages; the Skanoteka watermark is noted on the nine holdings whose photographs carry it.
- The page of changes marks what was written after the editor read it ("New"), and counts it at the top.
- In 53/6/0/-/47, entry no. 26, Prusimski's proxy is "Zeromski" (Wojciech Żeromski), on the witness of entry no. 43 (the editor, 2026-10-07).
- Entry no. 43 of 53/6/0/-/47, added earlier the same day, was taken out again at the editor's word: it is a suit between Skórzewski and Chełmski over the boundary of Biskupice and Łomów and not relevant to the project. Its text is kept in the holding (`intake/entry_43.md`), because the reading "Zeromski" in entry no. 26 rests on it.
- Figures: 565 documents on 1,833 pages in 36 holdings; 739 marks of doubt; 560 translated.
- **The spot sheet "Before publishing"** (fourteen rows across the holdings, answered by the editor on 2026-10-07; `docs/PRUSIMSKI_before_publishing.csv` and `..._answers.json`). Readings settled against the page: in 53/6/0/-/46, entry no. 17, "Vitkovien~" and "initorum"; "Laetare" there and "Invocavit" in Konin Gr.117 both stand, so the two documents disagree on the day of the hearing; the search of the 28th of October stands; in Rajewicz's protest (Konin Gr.116) the editor reads "Cumque", and "Citraque", "without his consent", is withdrawn from the text, the English, the summary and the holding's page. Confirmed as built: the closing sentence of 53/6/0/-/47 no. 26, the tower sentence and the paragraph on leaf 680 in Konin Gr.145, the note on leaf 266 verso in Konin Gr.118, the Kinos entry in Konin Gr.120. "Capitaneus" is "Starost" throughout the English of Konin Gr.119.
- **The timeline takes in the Prusimski era** (2026-10-07, at the editor's word): sixteen events from 1589 to 1788, one per matter, each linked to its documents, in English and German. The page had begun at 1794, so the one earlier entry (the commission of 1775) had never been shown, and it still said that the commission fixed the boundary; it is rewritten (the commission ended in two decrees). Years before 1794 appear only where they have documents or an event.
- **The timeline has a band where each era begins** (1589, 1794, 1807); the Prusimski years end and the Hohenlohe-Ingelfingen years begin with Prusimski's flight after the Kościuszko Uprising (the editor, 2026-10-07).
- **Oe 1 Bü 9454, letters 245 and 289: the archive's new scans** (2026-10-07). The images are replaced (289 is now pages 0522_b and 0522_c), the text is corrected against them line by line with the editor's new transcription beside it, the English is revised and the summaries are written again. Letter 245 gains the last line of its first page and is no longer marked as a rough reading; marks of doubt fall from 14 to 6 in 245 and from 13 to 1 in 289 (737 to 717 in the edition). The editor then answered a spot sheet on six words of 245 (2026-10-07): "praedikat", "dringen[?]", "Erröthen[?]", "aus der B[...] Casse"; two readings stand. On four words of 289 (2026-10-08): "zu Brieg", "Heneberg"; "bitte" and "Circa" stand (719 marks of doubt in the edition). Published at the editor's word on 2026-10-08, with the timeline.
- **The Prusimski-era holdings were published at the editor's word on 2026-10-07**: twenty-one holdings, 93 documents, 1589 to 1788. Figures: 565 documents on 1,833 pages in 36 holdings; 737 marks of doubt; 560 translated.
- **AGAD 1/169/0/1/1745 added** (2026-10-13; not published): six pages of a Prussian table of the villages around Konin, of about 1797, entries 140 to 303, with the houses, churches and Christian and Jewish inhabitants of each place and a total at the foot of every page. There was no transcription: the table was read from the editor's three scans in the working session and is kept in `units/agad1169011745/intake/table.csv`, from which the text, the English version and the editor's checking spreadsheet (`review/agad1169011745/table_check.xlsx`, a picture of each line beside its row) are made. Every line and every page total adds up as read. The site's tables now take a heading of three levels and set off a page's own total (`unitlib.render_table`); the English of a table may translate its heading (`publish_translations.py`). "Kurow Koninsk." and the village "Ostrow" are shut out of the place entries for Konin and Ostrów. Figures with it: 566 documents on 1,839 pages in 37 holdings; 725 marks of doubt; 561 translated. Waiting for the editor's check of the table.

## The summaries of Oe 1 Bü 14525 and 14526 written again (2026-10-08)

- At the editor's word, in a working session and at no cost: the 74 documents of the two Neuenstein volumes were read whole in their German text and summarised afresh in German, and the English summaries translated from the German. The first summaries had been written by the model from the English translations and never checked. Each statement was then held to its document (212 in Oe 1 Bü 14525, 182 in 14526; each holding's `intake/claim_check.yml`). Every holding's summaries have now been written from the original language and checked; the edition guide says so in both languages, and the two holdings' pages say how theirs were made.
- Oe 1 Bü 14525, document 7: the Government at Kalisz attested the copy on 7 July **1801**, not 1804; corrected against the scan (0021_a2) in the transcription and the English. Documents 3 and 4 were checked against the scans: both copies of the grant of 1796 name only Kamionna, Kolno and Brzyce in the deed's text, as transcribed.
- Two dates on the site that are not the documents' own (14525, documents 13 and 21) stay as they are (the editor, 2026-10-09).
- Oe 1 Bü 14526, document 26: the third party is **Kriede**, not "Reise" (the editor, 2026-10-09; the protocol is signed Jacob Kriede); corrected in the transcription, the English and the summary. Not yet published.

## AGAD 1/169/0/1/1745 checked by the editor and published; the cloud branch merged (2026-10-13)

- **The editor checked the table of villages line by line** on the spreadsheet with a picture of each line: 25 names corrected (most of them a mark on a letter the first reading had missed: Kuźnica, Łomow, Myżakow, Ośiek, Pępoćin, Sługoćin; and Lęka, Siąszyce, Siekierszyn, Sierszew, "Groi.", "Trąmpczyn."), the six "[?]" taken away, 24 notes of doubt cleared, no figure changed. The list is in `units/agad1169011745/notes.md`. Two periods that went with the "[?]" were put back from the scan ("Leysce.", "Lęka."). "Szyman." is short for Szymanowice (the editor); the text keeps the short form. The folds stand as proposed.
- **A clean spreadsheet of the table, to keep**: `units/agad1169011745/AGAD_1_169_0_1_1745_table.xlsx`, made by `holding.py --archive` from the reading: the table as written, the table in English, and a sheet on the source and the conventions; values only.
- `holding.py --take` now brings back the editor's "Doubt" column too, and `--xlsx` refuses to write over the spreadsheet the editor saved.
- **`claude/peaceful-meitner-snu6qx` merged into `main`**: the summaries of Oe 1 Bü 14525 and 14526 written again and claim-checked, and the two corrections with them (the section below). The other three cloud branches had nothing that `main` lacked. The two holdings' `summaries_draft.py` were run on the desktop so that its cache holds the new summaries.
- **Published at the editor's word.** Figures: 566 documents on 1,839 pages in 37 holdings; 719 marks of doubt (the new holding has none); 561 translated.

## Two holdings from the State Archive in Poznań added (2026-10-13; not published)

- **APP 53/968/0/-/783**: a printed summons in Polish, served on 7/19 October 1860 on Karolina Fridenberg of the Staro-Łazińska colony, by which Count Włodzimierz Miączyński of Trąbczyn counterclaims before the Civil Tribunal at Kalisz against 97 colonists and asks that Hohenlohe-Ingelfingen's contract of 18 May 1805 with fourteen colonists be held not to bind him. One document on five pages, with the archive's cover. The editor's Polish was read against the scans on every page: 34 corrections and five lines in the court messenger's hand added. The editor's English was a machine's and wrong in substance (the summoning verb, "father" for "husband", "manor" for "court", fourteen holdings for eleven); it is written again from the corrected Polish, and `units/app539680783/intake/changes.yml` lists the differences for the page of changes. Summary in both languages, claim-checked (17 statements, one weakened); a timeline entry and a paragraph in section VIII of the era essay.
- **APP 53/64/0/-/Kalisz Tab.21**: thirteen pages of the register of the hearth tax of the Kalisz voivodeship for the St John's instalment of 1789, 387 entries of the Pyzdry, Kalisz and Konin districts; Trąbczyn is entry 178 (80 złoty), with Łazy, Osiny, Nowa Wieś and its Olęders after it, and Łukom entry 106. There was no transcription: the register was read from the scans in the working session (`units/app53640kalisztab21/intake/table.csv`) and waits for the editor's check on a spreadsheet with a picture of each line. The pages have no totals; the sums are held by the rate of the tax instead (a multiple of 3 zł 15 gr, or of 2 zł 15 gr on leaves 18 to 20). The file named `017v.jpg` is placed as leaf 9 verso, by its receipt numbers.
- **The site**: the document kind "summons"; the timeline runs to 1860 and shows a year after 1832 only if it has a document or an event; a district's name directly above the first entry of a table is a row of the table (`unitlib.table_of`); a glossary entry for the court messenger (woźny, ministerialis), which marks 41 documents; Count Włodzimierz Miączyński and the Zelmer family on the people page; the 1860 print's spellings of Prusimski and Weigel matched; five entries shut out of the register, where they matched village names.
- The archive's descriptions of both fonds are in `reference/sources/`, with working translations.
- Figures with them: 568 documents on 1,857 pages in 39 holdings; 759 marks of doubt; 563 translated; sixteen documents in Polish; the edition now runs from 1589 to 1860.

## The editor's answers on the two Poznań holdings worked in (2026-10-14; not published)

- **APP 53/64/0/-/Kalisz Tab.21**: the editor checked the hearth-tax register line by line on the spreadsheet with a picture of each line. 69 names corrected, no figure changed; the twelve figures off the rate of the tax confirmed as read; 13 names keep "[?]" (45 before). Three names the first reading had shortened are written in full on the page (Jerzmanowskiego, Bardzińskiego, z Młynem). The text, the English (three new forms in the word table), `process.md` and the page brought into line; the clean spreadsheet made (`units/app53640kalisztab21/APP_53_64_0_Kalisz_Tab_21_register.xlsx`). `017v.jpg` is leaf 9 verso (editor). The list of corrections is in the unit's `notes.md`. Publishing the English again also mended its table: the version on file had been published before the heading was settled, without the printed title.
- **APP 53/968/0/-/783**: the folds approved as proposed. Count Włodzimierz Miączyński was Michalina Miączyńska's son (editor): in his biography and on the holding's page.
- **The Olęder colonies of Trąbczyn** (editor): two colonies, first Trąbczyńskie Stare / Nowe Olędry, later Łazińskie Stare / Nowe Olędry, in several spellings; Łazy is a separate village. The summons' Staro- and Nowo-Łazińska colonies are matched to the two place entries, and Łazy is kept apart from both. A paragraph on this in the pages of both holdings.
- **The tailed sign at the end of a name in the register** is the clerk's sign for an ending such as -skiego (editor): "Kiedrowę" (twice), "Trzebiesławę" and "Siedliskę" now stand as "Kiedrow:", "Trzebiesław:" and "Siedlisk:", given as a colon like the same sign elsewhere in the register.
- **"Haul. Lazy."** in the table of about 1797 (AGAD 1/169/0/1/1745, no. 150) is probably the Łazińskie Olędry, not the village of Łazy (editor). Recorded; not matched to either colony.
- **A spot sheet for the summons**, "Pen marks on the summons": the six places where the court messenger wrote on the print, each with a picture.
- Figures: 568 documents in 39 holdings; 727 marks of doubt.

## APP 53/968/0/-/669 added: Albert Breyer's notebook of July 1936 (2026-10-14; not published)

- **APP 53/968/0/-/669**: a pencil notebook of 35 pages in German from the papers of Albert Breyer, written in Łazińsk and Emilienheim, German settlements of the commune of Trąbczyn, with a log of his photographs at the back. Only the notebook whose scans are in the folder "Notes on Łazińsk" (editor); the editor's English notes beside it belong to another notebook of the unit and were not used.
- There was no transcription: read from the scans in session (88 marks of doubt), translated, summarised in both languages and claim-checked (16 statements, two weakened); holding page in both languages. A spot sheet of ten readings, with pictures, for the editor.
- The name list made from the corpus no longer takes a word cut by the line-break mark ("Emilien¬heim" was found as Emilie); nothing else in the edition changed. Neumann, Geheimer Finanzrat Schulze, Holland and Warszawa shut out of this document.
- "geb." ruled out of the glossary (geboren).
- Figures: 569 documents on 1,892 pages in 40 holdings, 1589 to 1936; 815 marks of doubt; 564 translated.

## Glossary: Matura (2026-10-14)

- A glossary entry for the Matura, the school-leaving examination, at the editor's word, in English and German; it marks the word in Breyer's first notebook (page 28). To be checked against the Encyklopedia PWN. Published.

## APP 53/968/0/-/669: the editor's corrections to the first notebook (2026-10-14)

- The editor read the English of Breyer's first notebook against the scans: Grodziec and Ciswica for Smaszew and Czarnica, Grądzeń, Moraß, Ed[uard] Zelmer, Chruściki, Kinder and Birke in the photo log, and others; the order of some lines; the German of the sayings kept beside the English; the inside back cover read again with the editor and completed (`units/app539680669/intake/editor_corrections.py`).
- Years from 1900 on were shown with a thousands comma ("1,907"): `numerals.py` now takes 1500 to 1999 as years.
- The English naming rule for Trąbczyn no longer rewrites a spelling quoted from the page ('written "Trąpczyn"'), which a run of it had done in two summaries; both kept as they were.
- Figures: 812 marks of doubt.

## APP 53/968/0/-/669: a second notebook added and published (2026-10-14)

- **Document 2**, Breyer's notebook "V. Grodziec Juli 1936", from the editor's raw photos IMG_5192 to IMG_5205: 25 pages read in session (33 marks of doubt), English, summary in both languages claim-checked (15 statements, three weakened), the holding's page and title for two notebooks. The camera's full-size picture inside each raw file was used; the last photo, flagged by the camera as turned, is upright inside the file.
- A spot sheet of 15 readings for the editor. Koppe, Küster and Stanisław Miączyński shut out of the new document; the glossary's Morgen takes "Mor." after a figure.
- Figures: 570 documents on 1,917 pages in 40 holdings; 828 marks of doubt.
- The editor's answers on the sheet of 15 readings worked in (Brudzewo, Kirschhacker, Swirkhaber, Chocz, Firstgugge and others); 824 marks of doubt. Three rows asked again on a short sheet and answered (Rhein…, "Die nach ins Posenschen gehen", Dachgugge). Published at the editor's word; 823 marks of doubt.

## Three holdings published (2026-10-14)

- **APP 53/968/0/-/783** (the summons of 1860), **APP 53/64/0/-/Kalisz Tab.21** (the hearth-tax register of 1789) and **APP 53/968/0/-/669** (Albert Breyer's notebook of 1936) published at the editor's word, with the two new eras under working names and the timeline to 1936. Figures: 569 documents on 1,892 pages in 40 holdings, 1589 to 1936; 795 marks of doubt.

## The editor's answers on both spot sheets; two new eras (2026-10-14)

- **APP 53/968/0/-/783**: no. 58 is Marcina Heck, no. 70 Krystofa Grünwald (the court messenger's pen over the printed "ja"), the note of costs 47 roubles 21 kopecks; the other pen alterations stand as printed. Text, English, process pages and the page of changes brought into line (`intake/spot_answers.py`).
- **APP 53/968/0/-/669**: seven of ten doubtful readings settled by the editor, three differently from the first reading (Wagelt, Hormann, Neumann L. 1889); Włodzimierow in the list of the school community. 83 marks of doubt remain.
- **Two new eras** at the editor's word, under working names until the editor names them: "The estate under Włodzimierz Miączyński" (`wlodzimierz`), the era after Michalina, with the summons of 1860; "The twentieth century" (`twentieth-century`), with Breyer's notebook. Each has its band on the timeline, which now runs to 1936, and its section on the story page, in both languages.
- Figures: 808 marks of doubt.
- **APP 53/968/0/-/669, the second sheet**: 29 of the most uncertain readings put to the editor; 22 changed or settled. Strażniki is a village (not the name Krainik), Noga a field name (not Kroge), Swięcer of Swięcia (not Smięcer), Mühle (not Müller). 70 marks of doubt remain; 795 in the edition. A third sheet of three readings on Breyer's Sm and Sw: the editor read Swięcia twice where the first reading had Smięcia, and St[y?]pin.

## APP 53/968/0/-/716 added, not published (2026-10-14)

- **APP 53/968/0/-/716**, Albert Breyer's notebook "Łazińsk, Emilienheim, Ликвидац. табель", with a loose sheet of 1858, from the editor's raw photos IMG_5159 to IMG_5180: eleven documents by content (the editor's choice), six of them tables. Breyer's Russian copies of the liquidation tables of Emilienheim (28 March 1868), Łazińsk (Słupca, 29 June 1868, 91 holdings, 1,691 Morgen 219 rods, with his pencil of who held each holding in 1875) and Orliny (of Count Albert Taczanowski), and of the servitudes of Łazińsk and Orliny; his counts of farmers and Morgen of Łazińsk from 1840 to 1935; his German notes of July 1935 and July 1936 on Orlin, Józefów, Huta Trąbczyńska and their people; a list of the farmers of the Orlin Hauland Biskupice; and the Polish list of the hearth tax of Emilienheim, Kopojno, 3/15 December 1858.
- Read from the photos in session (68 marks of doubt), translated, summarised in both languages and claim-checked (83 statements, 16 weakened or cut); holding page in both languages, a timeline entry for 29 June 1868, a paragraph in the story and the era's blurb. Breyer's own total on one page is 6 Morgen more than his figures; the summary says so.
- Tables: a table's title or totals standing on a page of their own now show there, a heading row that is only a title joins the caption, and a single row of column labels is shown as one heading row. Every other table of the edition renders as before. Line breaks in Russian are now decided, a figure ending in a hyphen in a table is no longer taken for a broken word, and tables are left out of the catchword check.
- A spot sheet of 17 readings for the editor. Kl., Wirte and dt. ruled out of the glossary; Kuh and Neumann shut out of the documents where they are not the people of the name list.
- Figures: 581 documents on 1,951 pages in 41 holdings, 1589 to 1936; 880 marks of doubt; 576 translated. Not published.

## Copies take the era of what they copy (2026-10-14)

- **The editor's ruling**: a copy belongs to the time of the document it copies, not to the date of the copy or the holding it is in ("a copy of an 1828 document from 1939 should not belong to the 20th century"). Recorded in `reference/eras.yml`.
- **APP 53/968/0/-/716** brought into line: two documents that held one of Breyer's copies and his own notes together were divided (now thirteen documents). The sheet of 1858, the liquidation tables of 1868, Breyer's extracts of 1870 and 1892 (now dated 26 November 1870) and his copies of the servitudes of Łazińsk (dated 1868) and Orliny now stand in the era of Włodzimierz Miączyński; Breyer's own notes and figures stay in the twentieth century. The story page and both era descriptions follow. No other holding has a copy dated by its copying: APP 53/968/0/-/801 and I. HA Rep. 162 Nr. 295 already carry their originals' dates.
- Figures: 583 documents; 880 marks of doubt; 578 translated. Not published.

## APP 53/968/0/-/716: the editor's answers; Michalina's and Włodzimierz's dates (2026-10-15)

- The editor answered the spot sheet of 17 readings in Breyer's notebook: 13 settled or changed (the renaming of Emilienheim in 1892, the commune of Trąbczyn in the heading of the Łazińsk table, Jesswein among the first farmers of Józefów, Maradza, Holędry Orliny Biskupicki, Skrzydlewski, Tilson, Seling, Polzfu[h?]l, "Bankrott geworden", and most of the heading of the Orlin list). Text, English, four summaries and the holding's pages follow. 55 marks of doubt remain in the notebook, 867 in the edition.
- **Dates from the editor**: Michalina Miączyńska, born Prusimska, died on 19 January 1851; her son Włodzimierz on 20 December 1879, and his nephew Władysław Miączyński became heir of Trąbczyn. In the people's notes, the era's description (now 1851 to 1879), the story and the timeline note; the era's band on the timeline now begins at its first document, 1858, and the twentieth century's at 1935.

## APŁ 39/98/0/-/6603 added, not published; the liquidation era (2026-10-15)

- **APŁ 39/98/0/-/6603**, from the State Archive in Łódź, the first holding from there: the liquidation table of the Łazińsk colony, confirmed 8 February 1868 (91 farmsteads, 1,691 Morgen 219 rods, liquidation capital 10,055 roubles 70 kopecks), its copy of 1869 with the servitudes, the inscription of 1884 on fuel and pasture, the certified copies of the inscriptions of 1894 (the servitudes given up to Countess Maria Wielopolska for 393 Morgen 154 rods) and 1897 (the survey of 1896), and the statement of each farmstead's land after the survey. Six documents at the editor's word, three of them tables; the openings where the writing runs across are shown as one page.
- Read from the scans in session (24 marks of doubt), checked by the table's own sums; translated, summarised in both languages and claim-checked (46 statements, two corrected); holding page in both languages.
- **The liquidation era** (`liquidation`, working name) at the editor's word: the enfranchisement of 1864 and the settling of the servitudes, which began under Włodzimierz Miączyński. The new holding and Breyer's copies of the tables and servitudes in 53/968/0/-/716 stand in it; the story has a section for it, the timeline a band from 1868, an entry for 8 February 1868 (moved from 29 June, the date of Breyer's source) and a new one for 1894.
- The State Archive in Łódź in the repositories and on the credits page, and the Central Archives of Historical Records, which was missing from the credits. Two new relation kinds, "Copy of" and "Entered in".
- Figures: 589 documents on 1,974 pages in 42 holdings, five archives; 891 marks of doubt; 584 translated. Not published.

## APP 53/968/0/-/716: the editor's answers on the second sheet (2026-10-15)

- 18 of the 47 readings answered and worked in: Дикгофъ, Диконфъ, Кинастъ, Обстъ, Готтлибъ, Дет., "Eingeschrieben jedoch", Цельмеръ Готф., Шмехель (Schmechel), and "nur[?]" twice. 46 marks of doubt remain in the notebook, 882 in the edition. The other 30 rows stay on the sheet, with two words the original table of 1869 now settles (плахтами, наличный) put to the editor.

## Breyer's Łazińsk table read against the original (2026-10-15)

- At the editor's request, every row of Breyer's copy of the Łazińsk liquidation table (APP 53/968/0/-/716, document 4) compared with the original (APŁ 39/98/0/-/6603). Most differences were misreadings of Breyer's hand and are corrected: figures at nos. 11, 12, 20, 44, 51, 52, 60, 61, 65 and 87, the names Саниковскій, Промистъ, Цельнеръ, Штирценбекеръ and Феттеръ, and наличный and тлахтами in the servitudes. Breyer's own departures from the original stand as he wrote them and are listed in the notes. In the original, no. 43 is Матеушъ in all three witnesses.
- Marks of doubt: 44 in the notebook, 21 in the original, 877 in the edition.

## Zelmer with m, Breyer's names to the original, the rest of the second sheet (2026-10-15)

- The editor's ruling: Zelmer is always written with m ("there's no Zelner, ever in this project"). Цельмеръ at nos. 37, 50, 53, 65 and 67 in both holdings, in the table, its copy and the statement of APŁ 39/98/0/-/6603 and in Breyer's copy (APP 53/968/0/-/716, document 4); the change to Цельнеръ the day before is undone.
- The editor's ruling: names in Breyer's copy of the Łazińsk table follow the original's spelling, not Breyer's: Мерцъ (for Мержъ), Саниковскій Марцинъ (no. 9), Марцинъ (for Март.), Кнафкусъ, Штирценбехеръ, Матеушъ (no. 43), Даніилъ (no. 60), the genitives Кинаста and Тарновскаго, and in the pencil Шейнфишъ and Гиршъ. What Breyer wrote is listed in the holding's notes and on its "How it was made" page. His figures stand as he wrote them.
- The editor's answers on the last 28 rows of the second sheet worked in: Brenda, "schlagen sich", Gottfr., Вангольдъ, Студзенка, "1909 9 Nov. hat das aufgehört", "mit d.", Велькiй боръ read without doubt; [Бонцлеръ?], [Гредъ?], […etli…?], [Solten?], [Zoget.?], [Crist.?] and [топоръ?] (an axe) changed with their doubt; eleven kept as they were.
- Marks of doubt: 35 in the notebook, 21 in the original, 868 in the edition.

## Breyer's figures to the original; Zelmer in the index (2026-10-15)

- The editor's ruling: the original liquidation table is the authority for the numbers too. Every figure of Breyer's copy (APP 53/968/0/-/716, document 4) compared with APŁ 39/98/0/-/6603; four differed and now follow the original: no. 12 122 rods (read 222), no. 29 188 (read 184), no. 46 38-66 (read 38-61), and nos. 47 and 48 in the original's order. The notes record what was read.
- At the editor's word, the Zelmer family in the people index now also matches Цельмеръ: the table, its copy and the statement of 6603 and Breyer's copy are linked to the family, and its bio names the five holdings of 1868.

## Page edges approved; a spot sheet for the original table (2026-10-15)

- The editor let the folds and page edges of APP 53/968/0/-/716 and APŁ 39/98/0/-/6603 stand ("The page edges look fine").
- All 21 marks of doubt in APŁ 39/98/0/-/6603 put on a spot sheet, "Doubtful readings in the liquidation table of Łazińsk": 16 rows, each with a picture, the signatures that recur under three documents asked once.
- The editor's answers worked in: the pencil figure under the table (10055 70), Глебель (no. 2 of the copy) and Стурценбекеръ (no. 19 of the copy) read without doubt; the rest, among them all eleven signatures, kept with their doubt. Marks of doubt: 18 in the original, 865 in the edition.

## Published (2026-10-15)

- At the editor's word, APP 53/968/0/-/716 (Breyer's Łazińsk notebook) and APŁ 39/98/0/-/6603 (the liquidation table of Łazińsk) published together: 589 documents in 42 holdings, 865 marks of doubt, with the new era `liquidation`.

## Oe 1 Bü 9454, letter 9 (2026-10-15)

- Letter 9, marked "skipped" since the holding was built, added from the editor's transcription: a single leaf in Triebenfeld's hand, holed and with a folded corner, 18 lines with 17 places of lost text and 3 marks of doubt. Read against the scan; where the editor's file and the scan differed the scan decided (Borgen, Bösewicht, schändlich, weiß, betreibe ... durch ihn), and those places are on a spot sheet for the editor. Dated to about January 1815 at Vienna, Triebenfeld to the Prince; English and summaries written in session. Not published.
- The editor's answers on the spot sheet worked in: seven readings confirmed, St[aats]. K[anzler]. F[ürst]. H[ardenberg]. confirmed and expanded, [seie?], [Kedl?] and [weiß?] marked as doubtful. Four marks of doubt.
- Letter 300 made again from the editor's new crops and transcription: the restored edges give the line starts of page 1 and settle gerüffelt, zurück, die Piece, kömt, Peterbourg, gärstig, Ciszewska and voll; the dateline reads "d 20t Januar", and the archive's pencil note "20. Jan 1816" dates it. Marks of doubt 25 to 18; English revised in session. The edition counts 879. Not published.
- Letters 9 and 300 published at the editor's word (2026-10-15).

## ADWł 85: the visitation of the parish of Trąbczyn (2026-10-15)

- A new archive and a new holding: nine pages of the volume of the visitation of the Konin deanery of 1790 and 1791 (Diocesan Archive in Włocławek, signature 85), the pages the editor's transcript covers. Two documents at the editor's word: the parish of Trąbczyn, and the table of the souls of the parish of Zagórów. Era `prusimski-boundary`.
- At the editor's word, the passages of these pages the transcript left out were transcribed in session; every page then read against the scans. A dropped phrase restored (leaf 24: Kalisz 5 miles, Konin 2); the editor's expansions of titles ("Jego Wysokość Magnifici") replaced by the abbreviations as written. All figures of both tables agreed. 12 marks of doubt, on a spot sheet.
- English and summaries written in session; 34 statements claim-checked. Holding page in both languages; timeline entry for 1791; the edition guide, the story page and the era's blurb brought up to 591 documents in 43 holdings and six archives, 891 marks of doubt. The 1788 timeline entry no longer calls itself the last document of the Prusimski years.
- Index: Katarzyna Prusimska (the Chamberlain's wife who enlarged the church), Antoni Prusimski, the Trąmpczyński family, seven new people; the parish's places; "po Swięcie" shut out of Swięcia and "Komornikow" (cottagers) out of the glossary's komornik. A document type "visitation"; an archive with no website is credited without a link.
- Not published.

## ADWł 85: the spot sheet, published (2026-10-16)

- The editor answered the spot sheet "Doubtful readings in the visitation of Trąbczyn": obok, trumną, Bogusławskiego, Golinską, Dręzgi, Illust:, Gralewska, 58 and rozrządzonę settled; Kozierog[?], Uła[?] and podciorze[?] kept with their doubt (`units/adwl85/intake/spot_answers.py`). 3 marks of doubt remain in the holding, 882 in the edition. Bogusławski and Golińska added to the index.
- The reference stays "ADWł 85": the archive's holdings have no series name (editor).
- Published at the editor's word: 591 documents in 43 holdings.

## Kuryer Polski 1754, nr 75: the funeral of Paweł Prusimski (2026-10-16)

- The first holding from print and from a library: the report from Kalisz of 5 December 1754 in the Warsaw newspaper Kuryer Polski, no. 75 of 1754 (Kórnik Library of the Polish Academy of Sciences, Cz2271, in the Wielkopolska Digital Library). Read from the editor's image in session, line by line with the printer's letters; one mark of doubt. Translated, summarised, claim-checked (11 statements), holding page in both languages, timeline entry, guide, story page and era blurb brought up to 592 documents in 44 holdings, 883 marks of doubt.
- A new repository `bkpan-kornik` (a library) and document type `newspaper`. Łęd is Ląd (editor): Ląd added to the places, which also links the boundary decree of 1775, the Prussian table of about 1797 and six contracts of Oe 1 Bü 14526. Paweł, Antoni and Katarzyna Prusimski matched in the print's spelling; the abbot Głowiecki added.
- Not published.

## Kuryer Polski 1754, nr 75: published (2026-10-16)

- The editor looked at the one doubtful word on the spot sheet and kept "[Cleri?]" as it stands. Published at the editor's word: 592 documents in 44 holdings, 883 marks of doubt.

## Kodeks Dyplomatyczny Wielkopolski: twenty-one medieval entries (2026-10-16)

- A new holding, `kdw`: twenty-one entries of the Kodeks Dyplomatyczny Wielkopolski, 1173 to 1440, from volumes 1, 2, 3, 5, 6, 7, 10 and 11 (volume 8 left out at the editor's word), each entry one document in order of date, given whole from the editor's file and not corrected. Text only, from the Wielkopolska Digital Library's electronic text; each page names its volume and number, linked to the volume.
- The editors' footnote marks are raised and their notes set apart on the site (`units/kdw/footnotes.yml`), without changing the text; both verifications allow for it.
- Estates tagged from the editor's sixteen; new places Szetlew and Adamierz; medieval spellings with their years for thirteen places, shown on the Places page. Thirteen people of Trąbczyn added, each to its document.
- A new era `medieval`, "Trąbczyn in the Middle Ages" (working name): on the timeline from 1173 with six events, on the story page, in the era list. English and summaries written in session; 107 statements claim-checked. Holding page in both languages; the edition guide brought up to 613 documents in 45 holdings, 2,005 pages, 1173 to 1936.
- Years before 1500 no longer get a thousands comma in the reading text and English of this holding (`numerals.YEARS_FROM`); no other holding changed.
- Not published.

## Kodeks Dyplomatyczny Wielkopolski: Imielno, published (2026-10-16)

- Imielno is an estate of focus (editor): a new place, matched also in its medieval form "Chemelino". The gift of the hospital of Gniezno (1243), which lists "Chemelino" among the hospital's villages, is tagged with it, and its summary and the holding page say so (claim check rewritten for that statement). Imielno also links the boundary decree of 1775, the protest of 1778 (Konin Gr.117) and the visitation of 1791.
- Published at the editor's word: 613 documents in 45 holdings, 1173 to 1936.

## The literature: six books, page by page (2026-10-19)

- A new kind of material, kept apart from the archival documents (`docs/LITERATURE_PLAN.md`): books and articles about them, each in its original language and in English, for questions such as whether Triebenfeld inflated the value of his estates. Six works from the editor's folder "Books", copied unchanged into `literature/<slug>/`, the English of all six Claude's (the editor): the Materialien of 1861 (with the black register of the gifted estates), Held's book of 1801, the Neue Feuerbrände of 1807, Paciorkowski's Latin treatise of 1776, Guradze's Der Bauer in Posen of 1898, and Seidel's book of 2018 on Hohenlohe-Ingelfingen.
- Each work has a `work.yml` (title, citation, language, how its pages are marked, an account in English and German) and a `notes.md` (how it came in, how the two files line up, a spot check of the English). `pipeline/literature/build_literature.py` cuts both files at the printed page marks, checks that the passages give back the whole file, and writes `corpus/literature/`: an index and one file per page and language. It runs in `regenerate.py` after the dataset.
- Seidel is under copyright: in the repository for questions but never shown on the site (`visible: false`; the editor, 2026-10-19, knowing that the repository is public). Until now `.gitignore` kept it out.
- Found on the way: Triebenfeld's entry in the black register (Materialien pp. 162-164) is about other estates than Trąbczyn (Piotrow, Lasky and others). Guradze has no page numbers yet (the editor will correct the text); the English of Paciorkowski lacks the mark of p. 27.
- Nothing on the site yet. Not published.

## The literature on the site (2026-10-19, not published)

- "Literature" in the menu (German "Literatur"), after Sources: a list of the five visible works (/literature/, /de/literatur/), and a page for each with the original and the English side by side, passage by passage, each headed by its printed page and with its own anchor so that a page can be cited and linked (for example /literature/materialien1861/#p-162). Footnote markers link to their notes. Made by `pipeline/literature/literature_site.py`, a new step of `regenerate.py`; the plan's section 7 says how.
- Seidel (2018) has no page; `verify_site.py` now fails if its slug or title shows up anywhere in the built site, or if a visible work lacks a page.
- Built and verified on the desktop; not published.
- The book's title is the heading on the list and on each work's page, the citation ("Materialien (1861)") under it (the editor).

## The literature: who and which estates the books name (2026-10-19, not published)

- The edition's index of people and places run over the originals of the five visible works (`pipeline/literature/literature_index.py`, a new step of `regenerate.py`; LITERATURE_PLAN.md, section 8). Every one of the 2,690 hits was read and ruled in `literature/index.yml`: 2,508 stand. The rest are words, measures, regiments and other men of the same name, each with the reason.
- Forms the books print and the edition's patterns miss are added for the literature only: Trąbczyn as "Trombczyn" and "Trobozyn" in the black register, Szetlewek as "Szellewen", Świechocin as "Schwiegoszyn", Łowyń as "Löwin", Krotoszyn as "Krotoczyn" and others, the Prince as "Hohenloh".
- On /people/ and /places/, a closed list "In the literature: N passages" under the documents of 35 people and 11 estates, linking to each page of each work that names them (1,174 links in the two languages, each checked to reach its passage). Places that are not estates have no list; their hits are kept in `corpus/literature/mentions.json`.
- Five of the people are Claude's identifications. The editor accepted four on Claude's reading, and Stenger once the evidence was written out for them (2026-10-19). What each rests on:
  - Grevenitz: the books' government councillor (Regierungsrath) von Grevenitz at Posen in the 1790s, given Tarnowo and a go-between in the Gurowski affair (Materialien pp. 127-153; Feuerbrände part 2, pp. 71 and 74, part 3, p. 132), is the edition's Kammergerichtsrat von Grevenitz, Triebenfeld's friend after 1807.
  - Stössel: the Baron von Stössel who lent Hoym his name to buy a gifted estate (Materialien p. 158) is of the edition's Stössel family, Silesian creditors on Koszęcin.
  - Nöldichen: the Nöldichen who signs for the General Direction of the Seehandlung in 1794 and 1795 (Held pp. 91 and 94) is the edition's councillor of war Nöldichen, who valued Krotoszyn, the estate Held's book is about.
  - Wartensleben: General Count Wartensleben at Liegnitz, no. 17 of the black register (Feuerbrände part 2, p. 84; Materialien pp. 165, 212), is listed under the edition's Silesian Counts Wartensleben, father and son, without saying which of them he is.
  - Stenger: the Justizkommissarius Stenger "in Unruhstadt" whose essay of 1798 on the Hauländer Guradze cites (chapters IV to VI) is the edition's Criminal Rath Stenger "hier aus Karge" (letter 23 of Oe 1 Bü 9454, 1809), Triebenfeld's agent for Zagórów, Trąbczyn, Pszczew and Witów: Karge and Unruhstadt are one town, Kargowa (the editor, 2026-10-19).
- Built and verified on the desktop; not published.

## The literature: passages tied by hand to documents (2026-10-19, not published)

- `literature/links.yml`: four links from the black register (the Materialien, pp. 141-171, and the Neue Feuerbrände, parts 2 and 3) to ten documents, each with a sentence in English and German saying what the book says and what the document says (LITERATURE_PLAN.md, section 9). Every figure in a sentence was read in both.
  - The Prince's gift and the exchange for Krotoszyn (I. HA Rep. 7 C Nr. 3570, document 1; Oe 1 Bü 9454, documents 85, 86, 87, 97, 101). The register says Beyme stopped the exchange; Cölln said Voss, and the letters bear him out. The register says the Prince gave the cabinet a yield of 50,000 a year; the letters give 41,500 (the Prince) and 40,500 (the King).
  - Triebenfeld's own estates (documents 104, 108, 112): the same valuation (over 700,000) and resale (750,000) in the register and the letters; for his sale to Prince George of Hesse-Darmstadt the register gives 400,000, his letter 280,000.
  - Krotoszyn's lease to Früson at 30,100 (documents 85, 86, 101).
  - The other gifts Triebenfeld cites in letter 103 (Bischofswerder, Zastrow, Dolffs and Treskow, "Gen. Ruchts"), beside the register's entries on them. "Ruchts" as Rüchel was Claude's identification; settled the same day (below).
- On the site: under each linked passage a box "In the edition" with the sentence and the documents; on each linked document's page an entry "In the literature" in the box "About this document". `literature_site.py` stops on a link to a passage or document that does not exist; `verify_site.py` checks both sides of every link (140 in the two languages).
- Built and verified on the desktop; not published.

## Letter 103: General Rüchel; the literature published (2026-10-19)

- Oe 1 Bü 9454, letter 103, page 4: "des Gen. Ruchts" is "des Gen. Ruchels", General Rüchel. The editor agreed with Claude's identification and took "Ruchts" for a misreading; the scan reads "Ruchels". Corrected in the transcription (logged in `transcription_decisions.csv`), in the English ("General Rüchel", by `reference/english_corrections.yml`) and in the link's sentence; the mark of doubt on the word is taken out. Rüchel's entry in `reference/people.yml` now finds the letter. The record is `units/oe1bu9454/intake/scripts/ruechel_103.py`.
- Published at the editor's word: the literature (five works on the site, the index of people and estates over them, the four links of the black register) with this correction.

## Line ends: every text file LF (2026-10-19)

- At the editor's word, so that line endings stop turning small edits into diffs of hundreds of lines. `.gitattributes` now stores and checks out every text file with LF, on the desktop and in the cloud alike; the 2438 files that were CRLF or mixed were converted in one commit (6ef4dcce, listed in `.git-blame-ignore-revs`). `reference/name_rulings.json` and `units/oe1bu9454/scan_decisions.json` ended in a stray carriage return, which made Git treat them as binary; it was taken out.
- `build_db.py` and `merge_corpus.py` now write LF on Windows too.
- Verified on a branch before it went to `main`: every holding rebuilt, the site built and `verify_site.py` passed (613 documents); the 9135 generated files were identical to before but for line ends. No text, translation or page changed.
- `CLAUDE.md` and `docs/WORKING_NOTES.md` ("Line ends") no longer ask sessions to preserve CRLF file by file.

## The literature: one text at a time, and six more works (2026-10-19, published)

- **The original and the English are no longer side by side** (the editor: "not ideal"). A work's page shows one text at a time, with buttons above the first page, "English" and the original's language, as a reader switches the views of a document. It opens on the English (editor), and the choice is kept from one work to the next (`site/assets/literature.js`). Without the script both texts stand one under the other.
- **Six works from the editor's folder "Books_2"** (LITERATURE_PLAN.md, section 10):
  - Albert Breyer's articles of 1935 ("Deutsche Gaue in Mittelpolen", the chapters on Kalisz and Konin only, at the editor's word; "Ostdeutschland als Mutterland") and of 1938 (the German villages of the Warthe marshes), from Jutta Dennerlein's digital reissues. They are read from the PDFs' text layer by the new `pipeline/literature/upstream_pdf.py`, and her forewords are left out (editor).
  - Teodor Żychliński's *Złota księga*, vol. 7, pp. 187-188 (the Prusimski) and vol. 13, pp. 219-225 (the Miączyński), read from the photographs in session.
  - Jan Pachoński's entry on Antoni Prusimski in the *Polski Słownik Biograficzny* (1982, editor).
  The English of all six is Claude's, from the original. The machine English in the editor's files was not used (the PSB's was wrong in substance). No German translation of the Polish works was made: an accepted gap (editor).
- The index of people and estates over the eleven visible works: 3,200 hits, every one ruled in `literature/index.yml`; 2,946 stand.
- **Eleven new hand-made links** (`literature/links.yml`; fifteen in all, to 32 documents), every figure read in the book and the document. They tie:
  - Breyer to the lease of 1806 and to Weigel;
  - Żychliński to the court books on the Prusimski line, to the letters on Michalina's marriage, to the dispatch from Venice and to the summons of 1860;
  - the PSB to the boundary commission, the confiscation, Venice and the restitution of 1807.
- Found while the links were checked, and put to the editor (NEEDS_CONFIRMATION.md, "The literature"):
  - The dispatch from Venice of 14 December 1796 already mourns Prusimski's wife, against Żychliński's date for her death, 2 September 1797.
  - Żychliński and the PSB give Michalina's second marriage as 1809, against "about 1814" in the edition's biographies.
  - Żychliński's account of who held Trąbczyn from 1809 to 1879 differs from the edition's.
  - The lease of 1806 differs from Breyer's account in its date, in the dike clause and on pasture and wood.
  No biography or era of the edition was changed.
- Published at the editor's word the same day, the questions above still open.

## Two eras made one: Włodzimierz Miączyński's years and the liquidation (2026-10-20, not published)

- At the editor's word, "for better clarity": the era "The estate under Włodzimierz Miączyński" and the era "The liquidation: the peasants' land and the servitudes" are one, under the working name "The colonists' land and forest rights" (slug `wlodzimierz`). The lawsuit of 1859 over the colonists' rights in the Count's forest and the liquidation that fixed those rights in 1868 and bought them out in 1892 are one story. The era has 14 documents, 1858 to 1897: APŁ 39/98/0/-/6603 and Breyer's copies of the tables in APP 53/968/0/-/716 moved into it.
- Changed with it: the era's ownership line and blurb (`reference/eras.yml`), the timeline (one band at 1858, its note covering both), and the story page in both languages (one section).
- Claude's proposed names for all the eras are put to the editor (NEEDS_CONFIRMATION.md, "The eras"); no other era is changed.

## The documents first: a rule; Paweł Prusimski and the privilege of 1746 (2026-10-20, not published)

- **A new rule of the editor's** (2026-10-20): every fact is first checked against the edition's archival documents, before a book or any other source; where they disagree, the edition keeps to the document, and the difference is flagged in NEEDS_CONFIRMATION.md and recorded in the source's `notes.md`. Written into `docs/HOUSE_STYLE.md` ("The documents first"), with pointers in CLAUDE.md, WORKING_NOTES.md and LITERATURE_PLAN.md.
- **Breyer's "Paul von Kolno-Prusiński" is Paweł Prusimski** (the editor, 2026-10-20). Recorded in `literature/index.yml`, the work's `notes.md` and NEEDS_CONFIRMATION.md.
- **The link from Breyer (1935) on Łazińsk Holland** said "the edition has no document of 1746". The corpus had not been searched: the boundary decree of 1775 (Konin Gr.145, p. 76) cites "the rights granted them in 1746", the primary source for the privilege (editor), and the summons of 1860 (APP 53/968/0/-/783) names its grantors, Paweł z Kolna Prusiński and his wife Katarzyna z Rozdrażewskich. Both documents are added to the link, and its sentence now says what each says; that the privilege was a hereditary lease is Breyer's account alone.
- For the era of 1851 to 1901, Claude proposes the name "The liquidation: the colonists become owners", from the heading of the Łazińsk table of 1868 (NEEDS_CONFIRMATION.md, "The eras"). Not applied: the name is the editor's.
- **What the liquidation did** (the editor, 2026-10-20): the land the colonists farmed became their own, and the demesne farms stayed with the estate. The documents agree: the Łazińsk table lists only the peasants' farmsteads and common land, the forest "Studzianka" stays the manor's, and in 1892 the colonists gave up their forest rights for "manor land" from the owner of the estate. The era's account (`reference/eras.yml`) and the story (EN and DE) now say that the manor kept its own land and forest, and that the government paid the former owner for the peasants' dues.

## The editor's voice documented (2026-10-20, docs only)

- From three samples of the editor's writing (the preface and introduction of their book on the Trąbczyn estate, and a statement of purpose), `docs/EDITORS_VOICE.md` records their voice: sentence length (counted), words, openings and closings, evidence, what they do not do, where it differs from HOUSE_STYLE, and a two-paragraph brief. The samples are not kept in the repository. No text on the site was changed; reading the site against the brief is in TODO.md, section 8.
- Corrected and extended at the editor's word the same day: the pronunciations were a rare exception and are out of the brief; the long dashes are the word processor's typography, not the voice, so the house style's rule on dashes is no longer listed as a difference; the tone the editor aims at (a historian and editor of narrative academic history, evidence turned into a story a non-specialist can follow without loss of rigour) and their self-assessments (dry against fluff; framed "side roads") are recorded, and the brief is rewritten to them. A framed side road on the site is a new item in TODO.md.

## The spaced en dash; no signposting (2026-10-20, docs only)

- The editor ruled that an aside takes the spaced en dash ( – ), never the em dash or a hyphen standing in for one; until now the English had no dashes at all. HOUSE_STYLE, "Typography". A range between two figures takes an unspaced en dash (8,000–9,000; the editor, the same day); ranges written before have a hyphen.
- A new HOUSE_STYLE section, "No signposting": a sentence about the text instead of the past (announcing, pointing back, listing topics) is not written, except to bring back a topic the reader has not met for a long time (the editor's exception), and then by restating the fact, not by "as mentioned earlier" (Claude's suggestion). Navigational text (the About page's guide, "How it was prepared", lists of contents) is proposed as not signposting, for the editor to confirm. A search of the site's English found no signposts and no dashes, so no published text changes. EDITORS_VOICE.md's brief says both.
- The editor's writing samples are for the analysis of style only: nothing in them is a source for the edition or is set against the documents (the editor, 2026-10-20). Written into WORKING_NOTES ("Working with the editor") and EDITORS_VOICE.md.

## The literature: Pachoński, Mączak and Szwiec; the list by author (2026-10-20, published)

- The desktop's `main` is brought up to GitHub's (eighteen commits of the cloud sessions: the literature, the eras, line ends LF, house style).
- Pachoński (1973), "Les Polonais dans la République de Venise", and Mączak (1968), "Export of Grain ... 1550-1650", first built that day as holdings by the desktop session, are moved into the literature (the editor: the Sources page is for primary sources); their holdings, page images and summaries are removed, and the code and data made for literature as holdings are taken out again.
- Szwiec (2009), the catalogue of the regional architecture of the Pyzdry Forest, is added: the Polish text from the Word-printed PDF (`pipeline/literature/szwiec_pdf.py`), Claude's English, and its 80 pages of photographs and maps as pictures. Trąbczyn, Wrąbczynek, Wrąbczynkowskie Holendry and Orlina are among its villages.
- A work's pages can now show pictures (`figures` in `work.yml`); a work printed in English has one text and no buttons.
- The Literature page lists the works by author (the editor): surname first, the title with the English title in italics under it, where it was published, its language.
- The new works' index hits read and ruled; "Venise" made a default with one exception. The Hohenlohe essay links Pachoński's note 10 on the literature page. The Licences page says the modern works on the Literature page are outside CC BY.

## The literature: Wąsicki (1953) on Prussian colonisation in South Prussia (2026-10-21, published)

- Jan Wąsicki, "Kolonizacja niemiecka w okresie Prus Południowych 1793 – 1806", Przegląd Zachodni 1953, no. 9-10, pp. 137-179, at the editor's word: read from the scanned PDF page by page (its OCR not taken over), 101 notes, nine tables in the text; the sideways table of the Poznań department's colonies, the plans and a fold-out table of costs as pictures; Claude's English. It names the Hohenlohe estates of Zagórów and Trąbczyn and the colonies of 1805 on the Warta. Index hits read and ruled (Frankfurt am Main and the Warsaw domain office as exceptions to older rulings).

## The literature: Chodyła (2015) on the Olęder settlements of the Pyzdry Forest (2026-10-21, published)

- Zbigniew Chodyła, *Zarys najstarszych dziejów osad olęderskich w Puszczy Pyzdrskiej 1746 – 1793* (Pyzdry 2015), at the editor's word. The editor's Word conversion has no pages and its note numbers run into the words, so the text is made from the book's PDF in their Books folder (`pipeline/literature/chodyla_pdf.py`), with its 156 printed pages, 369 notes on their pages, three tables as HTML and 39 pages of maps, charters and portraits as pictures, and checked word by word against the Word file. Claude's English, page by page; the tables by `literature/chodyla2015/make_english.py`. The editor's machine English was read and not used.
- The book dates the founding of the Trąbczyńskie Stare Olędry and the Luśnie Olędry to 1746 (Paweł and Katarzyna Prusimski) from Konin Gr.145, and cites Konin Gr.136, Gr.153, Kalisz Gr.414, the hearth-tax table of 1789, the register of 1796 and the summons of 1860, all in the edition. Two of its details differ from those documents (NEEDS_CONFIRMATION).
- Index hits read and ruled: the Polish case forms of Antoni, Paweł and Katarzyna Prusimski added for the literature; "Poniatowskiego" (here the King, not Prince Józef), "Przespolewski" and "Oppeln" given exceptions to older rulings.
- Six hand-made links from the book to Konin Gr.145 and the summons of 1860 (1746), Konin Gr.136 (1754), Kalisz Gr.414 (1771), Konin Gr.153 (1782), AGAD 1/169/0/1/1745 (the register of 1797) and Kalisz Tab.21 (the hearth tax of 1789). Five differences with the documents are recorded; the edition takes the documents.
- The editor's rule (2026-10-21): a fact or date from a primary document is taken over a literary source's without asking, and the difference is flagged so that it is known. HOUSE_STYLE, "The documents first", point 4; the doc-versus-book questions already in NEEDS_CONFIRMATION (Maryanna Dąmbska's death, Paweł Prusimski's generation) are marked settled.
- Published at the editor's word, with Wąsicki (1953).

## The glossary: gród, the municipal court (2026-10-21, published)

- A new entry, `grod`, at the editor's word, from the entry Gród in Arct's *Słownik ilustrowany języka polskiego* (1916, vol. 1, p. 405) on Wikisource, which they named, and the State Archive in Poznań's description of the Konin court books (`docs/PRUSIMSKI_ERA_PLAN.md`). It explains that the court the edition's English calls the "municipal court" was the starost's court in the gród, not a town's court: no document in the edition names a town court. Checked (`checked: true`).
- It marks the Polish forms (gród, grodu, w grodzie, grodzki), the Latin castrensis, "municipal court" in the English and "Burggericht" in the German summaries: 375 marks in 56 documents, every one read in `review/glossary_matches.csv`; none is a place (Grodziec, Grodzisko are kept out).
- **"Castle court" is not the English term** (editor, 2026-10-21): the edition's own prose (holding pages, summaries, timeline, places, the literature's English and its notes) now says "municipal court" for sąd grodzki, as the translations always did (`reference/translation_glossary.yml`), and "municipal court office" for urząd grodzki: 502 places. Kept: "Burggericht" in the German, and "the domain castle-office of Brieg" in Held (1801), a Prussian domain office, not a gród. The earlier entries of this changelog keep the old wording as history.
- Arct added to the glossary's reference works (`docs/GLOSSARY_PLAN.md`).
- A second entry, `stawisko`, at the editor's word, from Arct (vol. 2, p. 784: a large boggy pond, or ground taken up by a pond or left after one), with what the documents say of the ground: the boggy, wooded ground on the Trąbczyn-Łukom boundary, disputed from 1728 (Konin Gr.145), its embankment (Gr.114) and the line of 1782 through it (Gr.153). The noun only (editor: "there's a place called Stawisko, and then the noun"): where an act makes the word the ground's name ("na Stawisku zwanym", "stawisko nuncupatum", "called Stawisko", "namens Stawisko") it is not marked. 95 marks in 3 documents, all read. The clerks capitalise most nouns, so a capital is not taken for a name.
- 113 entries, 57 checked.

## The literature: Boniecki (1900), the Chełmski branch that held Łukomia (2026-10-21, published)

- Adam Boniecki, *Herbarz polski*, part I, vol. 2, "Chełmscy h. Ostoja", at the editor's word, as a source for the Chełmski family tree: only the branch that held Łukomia (items 2.976.162-240 of M. J. Minakowski's online edition), from the editor's saved page, by `literature/boniecki1900/make_original.py`. Stanisław Chełmski, Treasurer of Wschowa, his brother Heliodor, their father Józef and uncle Franciszek, the division of Łukomia about 1700, Ignacy's sale of Łukomia, Łomów, Mielno (Imielno) and Bukowe to Stanisław in 1766, and Stanisław's line to Władysław, owner of Łukomia in 1860. Cut at the item numbers (no page breaks online); Claude's English. The saved page is not kept: its header carries the editor's login.
- Read against the documents first: the brothers of 1728 (APP 53/6/0/-/40), of 1775 (Konin Gr.145) and the four estates of 1778 (Konin Gr.117) agree; Heliodor's canonry (Chełmno in 1775, Poznań in Boniecki) and the year of Stanisław's title (1778 in the document, 1779 in Boniecki) differ, and the edition follows the documents (NEEDS_CONFIRMATION, "Boniecki (1900)").
- Index rulings for the Chełmski forms, "Łukomi", and "Mielna" as Imielno in the list of the four estates only. Four hand-made links (`boniecki1900-*`), to 1644, 1728, 1775, 1778 and 1763; the first rests on Claude's reading and waits on the editor. `docs/LITERATURE_PLAN.md`, section 14. The literature has 18 works, 17 on the site.

## The literature: the Encyclopedia of Camps and Ghettos (2012), the Warthegau (2026-10-21, published)

- The USHMM *Encyclopedia of Camps and Ghettos, 1933-1945*, vol. II A (2012), the chapter "Warthegau Region", at the editor's word: only the pages they named, pp. 34-39 (the introduction), 48 (Chocz), 57-59 (Grodziec), 60-61 (Kalisz), 63-64 (Konin), 99-100 (Rzgów), 120-121 (Zagórów), for the twentieth-century part of the edition. In English as printed; CC BY-NC-ND 4.0, so no translation and no pictures (their lenders' credits), the captions given.
- Made from the editor's JSTOR PDF by `pipeline/literature/warthegau_pdf.py`: the Polish letters from the accent font, the spaces of no width dropped, line-end hyphens told apart by the space the text layer keeps after a real one, notes linked within each entry, web addresses joined. `--check` compares every letter with the PDF. "Betchatów" corrected to Bełchatów at the editor's word. The PDF is not kept: its page feet carry the download's internet address.
- Index rulings: Koppe and Reinhardt are not the edition's; "Konińska", "Konińskiej" and Słupca are. No hand-made links yet. The literature has 19 works, 18 on the site.

## The places Grodziec and Rzgów (2026-10-21, published)

- All of 2026-10-21 after Chodyła published together at the editor's word: the glossary's gród and stawisko, "municipal court" throughout, Boniecki (1900), the Encyclopedia of Camps and Ghettos (2012) and the places Grodziec and Rzgów.

- Two places added at the editor's word (`reference/places.yml`, with their map positions in `reference/places_osm.yml`, looked up on OpenStreetMap and read against the sources). **Rzgów** ("Rzgowo" 1261, "Irgouo" 1280, both the Rzgów east of Zagórów by the Kodeks editors' note) is found in seven documents and tagged an estate in focus on four that concern it: KDW 4 and 6 (granted with Szetlew and Świątniki) and Konin Gr.117, docs 11 and 12 (the pines cut by its subjects in 1779 and its owner Marcin Nosalski's protest). **Grodziec** is found in Breyer's notebooks of 1936 and his notes of 1935; no document is about it, so it is not an estate in focus.
- In the literature, all 122 hits read and ruled (Chodyła, Breyer, Szwiec, the Encyclopedia of Camps and Ghettos): every one is the Grodziec near Rychwał or the Rzgów near Konin.

## The glossary: komornik, the officer and the lodger (2026-10-21, published)

- At the editor's word, from Gloger's Komornik (the entry already rested on it for the officer). Every use in the documents read: two senses. **The court officer** (komornik graniczny and ziemski, Latin camerarius; Konin Gr.117, Gr.118, Gr.145, Gr.153, Kalisz Gr.425, Oe 1 Bü 9454 letters 17, 18, 232, 233): the entry `komornik`, now also matching the lower-case Polish, the Latin and the translations' "Boundary Surveyor" and "Land (Court) Chamberlain", 134 marks in 14 documents. **The landless lodger** (Gloger: "chłopi bezrolni ... za otrzymywaną komorę, ogród"): a new entry `komornik-lodger`, marked only in its six documents (ADWł 85, Konin Gr.136, Oe 1 Bü 14525 doc. 23, 14526 doc. 9, 9454 letters 146, 191), 23 marks. Before, the officer's definition was shown in four of those.
- `glossary_build.py` takes `only_in`, the documents an entry is marked in (beside `not_in`). 114 entries, 58 checked.

## The literature: Frost (2007), the nobility of Poland–Lithuania (2026-10-21, published)

- Robert I. Frost, "The Nobility of Poland–Lithuania, 1569–1795", ch. 9 of H. M. Scott (ed.), *The European Nobilities in the Seventeenth and Eighteenth Centuries*, vol. II: Northern, Central and Eastern Europe, 2nd ed. (Palgrave Macmillan, 2007), pp. 266-310, from the editor's PDF at their word "only the article by Frost": the volume's Guides to Further Reading (pp. 410-415, with the Poland–Lithuania section) and the Russian chapter's opening page (p. 311) left out, and the guides not to be added at their word ("Don't add the guides from the PDF"). On the site at their word ("Give it a page - I'll need to decide later what gets displayed"); what the page displays is a later decision of theirs (NEEDS_CONFIRMATION).
- The book is under copyright (its imprint: "No reproduction, copy or transmission of this publication may be made without written permission"; "All remaining chapters © their respective authors 1995, 2007"). Put in with `visible: false` after the Seidel precedent, then given a page the same day.
- Read spread by spread from the page images at 200 dpi (the scan has no text layer; not OCR), doubtful spots settled at 300 dpi crops; the print's own slips kept as printed and listed in the work's notes. The chapter's notes are endnotes, kept on their printed pages so a note can be cited to its page (no `notes:` in work.yml).
- Index ruling, all pairs read in the sheet: the Radziwiłł magnates (28), Hieronim Florian Radziwiłł's given name ("Florian", 1) and Augustus II (1, caught by the pattern's bare "f " lookbehind in "of Augustus") are not the edition's; Repnin, the Russian ambassador (p. 299, twice), is ruled to the letters' Prince Repnin (83, 84, 1798), which the editor confirms (2026-10-21: "I'm sure Repnin is the same as the one in the project"; settled in NEEDS_CONFIRMATION). The literature has 20 works, 19 on the site.

## The glossary: kopiec, the boundary mound (2026-10-21, published)

- At the editor's word, from Gloger's "Kopce graniczne", read against the documents first: the decree of 1775 (Konin Gr.145) records the bricks, slag, glass, stones and coals laid where the mounds stood and a glass bottle with the commission's description under one, the corner (narożne) and wall (ścienne) mounds and the stakes in the marsh, as Gloger describes them; the line of 1782 (Gr.153) has forty-one wall mounds. Marked in Polish (kopiec), Latin (scopulus), the German summaries (Grenz-, Wand-, Eck-, Endhügel) and the English ("mound", always a boundary mound there): 338 marks in 11 documents, all read. 115 entries, 59 checked.

## The glossary: pisarz, the court clerk (2026-10-21, published)

- At the editor's word, from Gloger's "Pisarze". Every use of pisarz and notarius in the documents read: the court's clerk (the land clerk of Kalisz, Ksawery Mikorski, sitting with the judge and sub-judge in 1778 and 1782, Konin Gr.117 and Gr.118; the land clerk of Sieradz and the deputy clerk of Greater Poland at the Tribunal, Gr.153; the land and castle clerks of Gr.145; the customs clerk at Pyzdry, 53/6/0/-/45; a manor's clerk, Gr.118 doc. 27; the clerk of the Civil Tribunal at Kalisz, Nr. 12366 doc. 6) is the new entry `pisarz`, marked only there (38 marks in 8 documents). Not the notary public of the Prussian and Warsaw papers (the entry `notarius`, which no longer marks Gr.153's deputy clerk), nor the surname "Antoni Pisarz" (Kalisz Gr.414), nor the dukes' notarius of the Kodeks.
- `komornik` also matches "Land Court Surveyor" (Gr.145's komornik ziemski). 116 entries, 60 checked.

## Summaries for the works kept off the site; Pinkas Hakehillot (1976) (2026-10-21, published)

- The editor: "For each literary source that you don't publish on the site, include an entry with a detailed summary of its contents." A work with `visible: false` is now listed on the Literature page with a note that it is under copyright, and its page holds only a detailed summary (`summary_en`, `summary_de` in its `work.yml`), none of its text. `build_literature.py` carries the summaries, `literature_site.py` writes the pages and stops on a kept-off work without them, the list and the page show the note and "Read the summary", and `verify_site.py` now checks the summary page and that no stretch of the text (the middle of the longest line of up to 40 passages, in each language) appears in any built file, in place of the old rule that the title appear nowhere.
- **Seidel (2018)**: a summary chapter by chapter (about 1,970 words), written from a reading of the whole book, with what the edition's documents say where it differs: Trąbczyn came by the deed of gift of 9 August 1796 as estates fallen to the crown (Oe 1 Bü 14525, doc. 1), Zagórów by the deed of 19 June 1797 (Rep. 162 Nr. 295, doc. 3), not both in 1796; the colonists' lease of "18 May 1805" can be neither confirmed nor ruled out (APP 801, doc. 3, lacks its beginning).
- **Pinkas Hakehillot (1976)** (`dabrowska1976`): JewishGen's English, by Morris Gradel, of the entries Zagórów (p. 103), Pyzdry (pp. 202-203) and Konin (pp. 235-238) of Yad Vashem's encyclopedia, at the editor's word; kept as Seidel (JewishGen's notice forbids copying). `make_original.py` takes the entries from saved copies of the pages, every letter checked. Read against the documents: the entry's 1368 for Zagórów's town status against the privilege of 19 November 1407 (KDW, doc. 14), which the edition follows.

## Trąbczyn: the wartime name Drommin (2026-10-21, published)

- At the editor's word: from 1939 to 1945 Trąbczyn was Drommin. The rural commune of Trąbczyn was provisionally renamed Drommin on 20 November 1939, the name confirmed on 18 May 1943, and from 1 April 1940 it formed the Amtsbezirk Drommin, run by an Amtskommissar at Grabina (Rolf Jehke, Territoriale Veränderungen in Deutschland und deutsch verwalteten Gebieten 1874-1945, s.v. Amtsbezirk Drommin, https://www.territorial.de/wart//konin/drommin.htm). A new field `renamed` in `reference/places.yml` (name, years, a sentence in each language, the source and its link), carried into `site/_data/estates.yml` and shown on the place's card on the Places page under the medieval spellings, with the source cited. The name is found in no document or work of the edition, so it is not matched.

## APP 53/1455/0/2/21: the copy-book of the privileges of Ląd (2026-10-21, published)

- A new holding at the editor's word, `app5314550221`: five pages (13, 14, 25, 26, 66) of the eighteenth-century copy-book "Series privilegiorum monasterii Landensis transcripta ex libro privilegiorum", in the fond Klasztor cystersów w Lądzie of the State Archive in Poznań. Six documents, in Latin: the boundary of Makownica (1399); the sale of three mansi of Łukom with the forest Gradziem to Ląd (Pyzdry, 21 September 1461); the beginning of King Kazimierz's confirmation of it; King Kazimierz's exchange of Little Wronczyn and the mill at Pyzdry for sixty mansi of the forest Czernietz, where Drzewce was founded (Pyzdry, 18 January 1362); the beginning of his grant of freedom to its colonists; and p. 66 of the compromissory decree of 1761 renewing the mounds between Łukom, Zagórów and Drzewce.
- The pages were found by the archive's pencil pagination among the editor's raw photographs and cut from the photographs' previews (`intake/holding.py`); pages 13 and 25 are cut below the end of the entry before, at the editor's word. Read in session (17 marks of doubt), translated, summarised in German and English, claim-checked (70 statements), with its page in both languages, three timeline entries (1362, 1461, 1761) and the German date and relation notes. Eras: `medieval`, and `prusimski-boundary` for the decree of 1761.
- A note in the margin is now a kind of its own (`margin_notes.yml`, "Written in the margin" / "Am Rand geschrieben"), beside text written sideways and the receiving office's notes: `corpus_pages.py`, `build_db.py`, `build_dataset.py`, `build_site_data.py`, `translate.py`, `letter.js`, `i18n.yml`.

## APP 53/1455/0/2/21: Grądzyń, and p. 15 (2026-10-21, published)

- The editor: "Gradziem is indeed Grądzyń." The copy's Gradziem, Gradzien and Graziem are matched to Grądzyń (`reference/places.yml`), docs 2, 3 and 6 are tagged with it, and the English, the summaries, the holding's page and the timeline say Grądzyń; the copyist's Latin headings stay as written.
- The editor: "you can add page 15 to finish the king's confirmation." P. 15 (IMG_5223) is added, cut below the end of no. 16. Read whole, no. 16 is King Kazimierz's confirmation at Gniezno, in a year written over and read as 1447, of the contract by which Abbot Maciej bought the same three mansi of Łukomia and the forest of Grądzyń from the brothers Mikołaj, Jan and Warsz of Koscielec: not the confirmation of the sale of 1461, as its heading had been taken to say. Document 3 is dated 8 August 1447, summarised and claim-checked again; its link to doc. 2 is now "supplements"; a timeline entry for 1447. No photograph of p. 27 (editor).

## The literature: Karwowski (1900), the convent at Ołobok (2026-10-21, published)

- At the editor's word: "Klasztor pp. cystersek w Ołoboku" (`literature/karwowski1900/`), from Roczniki Towarzystwa Przyjaciół Nauk Poznańskiego, T. XXVI (1900), pp. 1-114 — only the two paragraphs of p. 87 the editor quoted, with their footnote: the debts Prince Hohenlohe-Ingelfingen left on Zagórów, its loss at auction in 1827 to the Wrocław banker Karol Bogumił Weygel, and the Cistercian Nuns' 40,000 złp. lost with it. Read from the WBC digitisation (DjVu id 118639; the files not kept), the image at 300 dpi and word-level zooms, the scan's text layer only as a check. Out of copyright (the author died in 1917). Claude's English. Index ruled; the three identifications it raises wait on the editor (NEEDS_CONFIRMATION, "The literature"). `docs/LITERATURE_PLAN.md`, section 19.

## The literature: Janocki (1779), the Lochowski entry, a sub-item of Paciorkowski (2026-10-21, published)

- At the editor's word: the entry "Stanislaus Lochowski" (LXXVII, printed pp. 159-160) of Jan Daniel Janocki's *Ianociana, sive clarorum atque illustrium Poloniae auctorum Maecenatumque memoriae miscellae*, tomus II (Warsaw and Leipzig 1779), `literature/janocki1779/`, transcribed in session from the editor's PDF (the title page and the two pages; the PDF not kept). It says Lochowski's *Processus iuris limitanei* of 1641 was twice printed again by Marcin Paciorkowski, who, "suppressing the true author Lochowski's name, rashly and insolently claimed the work for himself", under the *Regula processus granicialis* title (1749 and 1760). Claude's English. The entry runs to p. 161; the extract stops at p. 160, where item IV closes whole.
- **The first sub-item** (`docs/LITERATURE_PLAN.md`, section 18): `parent: paciorkowski1776`. The Literature page shows Janocki inside Paciorkowski's section; Paciorkowski's page carries the note (Janocki's words, with a link to the sub-item's page); the sub-item's page links back. `build_literature.py` and `literature_site.py` carry `parent`, `note_en` and `note_de`; the empty `parent` is dropped from the site data (Liquid reads "" as true — an empty "Attached to" line appeared on every work page before the drop).
- **The citation of the parent work** is now "Paciorkowski (1776) [= Lochowski 1641]" (`literature/paciorkowski1776/work.yml`), so the corpus passage headers, the page's standfirst and the "In the literature" lists name Lochowski wherever the handbook is cited; the bracket's wording was chosen without the editor and may be reworded. The accounts of Paciorkowski (1776) name the attribution and the conflict with the 1776 title page ("Editio secunda ab ipso authore aucta").
- No new index hits (nothing in the entry matches the edition's people or places); the doubtful reading "Miedzyborze" (the place of Lochowski's subscription) and the transcription wait on the editor (NEEDS_CONFIRMATION, "The literature"). The literature has 22 works, 20 on the site.
- **The plan's section numbers** had gone wrong on the way in: Frost (2007) and Pinkas Hakehillot (1976) were both "section 16", and Karwowski (1900) and Janocki were both "section 17". Renumbered: Pinkas 17, Janocki 18, Karwowski 19, with the cross-references in CLAUDE.md, this file, TODO and `literature_site.py`'s docstring.

## The literature: Minakowska (2026), Wojciech Otto-Trąmpczyński's page (2026-10-22, committed; not published)

- The page of Wojciech Otto-Trąmpczyński (ID: sw.35437) in Minakowska's database (`literature/minakowska2026ottotrampczynski/`), at the editor's word: the sixteenth-century man of the edition's Trąmpczyński family - marriage about 1590 (the database's estimate) to Anna Cerekwicka, the son Stanisław, and the descent whose names are the brothers of the decree of 1644's generation. Polish interface, Claude's English. A short page: no biography, no parents, no tree, no siblings.
- **The database's "sw." numbers**: sw.35437 is of the branch of the Teki Dworzaczka regest numbers - the person came into the database from a regest, and the regest of 1614 (Księgi grodzkie pyzdrskie, nr 2152, Nr 137: his son's marriage portion of 7,000 zł on half the estates) is the page's one source. A fourth kind of number beside the Boniecki (2.976.*) and family-branch (4.285.*) ones.
- **The pipeline fix the work forced** (`pipeline/literature/literature_index.py`): the index dedup dropped an extra pattern's hit whenever an edition pattern of the same slug fullmatched the surface, whether or not it could fire in the record - the edition's `trampczynski` entry carries `only_in`, so its pattern cannot fire in a literature uid, and the work's hits were invisible. The dedup now asks `applies()` first. General, not particular: any future `only_in` person stands the same way.
- **The page** /people/wojciech-otto-trampczynski/ (/de/personen/wojciech-otto-trampczynski/), the second standalone - and the rule's addition: **a standalone block's slug must not be an entry's slug**. The first try keyed the block `trampczynski`, the family entry's own slug, and the page showed the family's heading and bio; the block was renamed and the collision is recorded in `reference/genealogy.yml`.
- The index: 9 hits, all ruled (`--check` clean) - the family yes, "w Trąmpczyńskich Ol." no (the colony's name, Chodyła n. 34), "Janem Trąmpczyńskim herbu Topór" no (Żychliński p. 187, the Opaliński genealogy's man).
- NEEDS_CONFIRMATION gains the regest of 1614 (a possible holding: the Pyzdry books) and the descent's fit with the decree of 1644.

## The literature: Minakowska (2026), Stanisław Adam Miączyński's page (2026-10-22, committed; not published)

- The page of Stanisław Adam Miączyński (ID: 4.285.278) in Minakowska's database (`literature/minakowska2026miaczynski/`), at the editor's word: the edition's `miaczynski` himself - the second husband of Michalina Prusimska, colonel of the Polish army, adjutant of Prince Poniatowski, member of the Sejm of 1830-31, buried at Trąbczyn, heir of Trąbczyn and Wieniec by the legitymacja of 1838. Polish interface again (the work's language is the saved page's own, section 22), with Claude's English.
- **The marriage act of 17 August 1810** (Warsaw ASC Cyrkuł IV, act 67/1810, geneteka) against the edition's "about 1814" inferred from the letters of 1815: NEEDS_CONFIRMATION, nothing changed yet - the site shows both, the flag beside the new page's date.
- The page has a **Rodzeństwo section** the first page had not; the standing selection does not bring it in (it stays in the knowledgebase), and `make_original.py` stops there. New marks kept as printed: "hr. [tytuł] nadany" (a title granted), the Towarzystwo Rolnicze districts as offices, the page's own Wikipedia line, the "(linia: …)" kinship markers inside the status list.
- **The person's page** /people/miaczynski/ (/de/personen/miaczynski/): the first whose genealogy block hangs on an entry of the edition - the people.yml heading and biography, the life line 1780-1845 (stated dates, new in people_bios.yml), the family with the source of every fact, the 5 documents, and the automatic literature box. The wife is linked to her entry (prusimska), the son to his (miaczynski-wlodzimierz).
- **The index: 47 hits, all ruled** (`--check` passes, 0 unruled pairs) - including the four pairs the second page's session had left unruled (Bronisz no, Chełmska yes, Małachowski no, Wieruszowa no). **The two duplicate `Miączyński:` keys of the miaczynski section stood merged**: the second, added for the first Minakowska work, had shadowed the first in YAML and the three zychlinski exceptions were dead from 2026-10-22 until now.
- NEEDS_CONFIRMATION gains the marriage date, PSB t. 20 s. 562, and the page's other printed sources.

## The literature: Minakowska (2026), Helena Zielonacka's page (2026-10-22, committed; not published)

- The page of Helena Zielonacka (ID: 2.976.216) in Minakowska's database (`literature/minakowska2026zielonacka/`), at the editor's word "related to Chełmski": the Chełmski line through the wife of the decree of 1728's Józef Ścibor-Chełmski (heir of Łukomia and Łomowo). Saved in the **database's English user interface** - the rule now says the work's language is the saved page's own (`docs/LITERATURE_PLAN.md`, section 22), so this work is `language: en` with no english.md, the one text as Mączak (1968) is; the names, the offices and the regest stay Polish. The database's Boniecki-derived IDs: her 2.976.216 is an entry of the online Boniecki's article 2.976, inside the item range the edition's `boniecki1900` brought in (her marriage is in its passage c04).
- Against the documents: the husband and the family agree with the decree of 1728 (APP 53/6/0/-/40) and Boniecki c04; her sons are the Heliodor and Stanisław of the boundary decree of 1775, whose offices carry the same differences Boniecki raised (NEEDS_CONFIRMATION, settled - the documents stand); her children's birth years are the database's estimates and none is shown; the grandchildren's stated years are on her page with the work as their source. The Notes' regest of 1727 (Konin municipal books, her 3,000-złp dowry recorded on Józef's estates, he her guardian as well as her husband) is in the knowledgebase, and whether its holding is to be sought is the editor's (NEEDS_CONFIRMATION).
- **The standalone person page**: /people/helena-zielonacka/ (/de/personen/helena-zielonacka/) is the first for a person of no document of the edition - `standalone: true` in `reference/genealogy.yml`, with its own heading and biography, no documents section, and the literature named by hand (boniecki1900/c04 and the work's marriage passage). The index: 6 hits, all the Chełmski family entry's, all ruled.
- The first work's notes now record what its dropped status line said (chrome, but a fact about the person), and its grandchildren's "ca 1849" is kept as the rule requires.

## The literature: Minakowska (2026), the Starost's page, and the person pages (2026-10-22, committed; not published)

- The page of Antoni Michał Kazimierz Ostroróg-Prusimski z Kolna h. Nałęcz (ID: 4.285.619) in M. J. Minakowska's Wielka genealogia Minakowskiej (`literature/minakowska2026prusimski/`), the first of the database's pages the editor means to send, and with it **the standing rule for them** (`docs/LITERATURE_PLAN.md`, section 22): one excerpt work per person, slug `minakowska2026<name>`; the saved page never kept (the editor's login, the visitor's IP); the whole page kept as the knowledgebase (`full.md`, never shown, the Uwagi and their Teki Dworzaczka regest of 1786 included); only the editor's sections shown, **in full detail** (here the biography, the parents, the ancestor tree, the marriage, the children and grandchildren); **the database's estimated dates never taken into the edition's prose** (`docs/EDITORIAL_RULES.md`, the editor's ruling of 2026-10-22); the documents first on every fact.
- **The person pages** (the new site feature, designed with this work): a page per person from the authored `reference/genealogy.yml` - who they are, their life dates, their family with the source of every fact, the documents that name them, the literature that names them - built by `pipeline/build/person_pages.py` (a step of regenerate.py, after the website data and the index), the layout `person`, both languages, linked from the entry on the People page; checked by `verify_site.py`. The pilot: **/people/prusimski/** and /de/personen/prusimski/, with the life-line 1744–ca 1806 (the PSB entry's, accepted; the "ca" open, NEEDS_CONFIRMATION), the family (the parents Stefan Prusimski and Wiktoria née Malczewska, the marriage to Marianna née Dąmbska, Michalina with her two husbands and her children and grandchildren, the edition's Włodzimierz linked), and the sentence on the Uwagi's sources.
- Against the documents: the father and the grandfather agree (the citation of 1782, the decree of 1775); the page's grandmother Teresa née Łoś-Golińska is more than the documents say; its header "starosta nieszawskie" is the site's slip (the documents, the page's own Uwagi and the PSB all say Niszczewice); its PSB citation says t. 28 where the edition's copy is t. 27 (NEEDS_CONFIRMATION). The index: 31 hits, all read and ruled - the tree names the Starost's forebears, the grandchildren's list his descendants, and the rulings keep the bare surnames from the wrong persons (`literature/index.yml`).
- Encoding note for the pages of this database: they are ISO-8859-2, not Windows-1250.

## The literature: Kucharski (2023), the noble judiciary (2026-10-22, published)

- Robert Kucharski, "Sądownictwo szlacheckie od XV do XVIII wieku", Consilium Iuridicum 1(3-4) 2022, pp. 226-253 (`literature/kucharski2023/`), at the editor's word: the whole article from the journal's own PDF (`pipeline/literature/kucharski_pdf.py`, every page's letters held against the text layer by --check, all 28 pages match), the three pictures not rendered, their captions and "Źródło:" lines as text; Claude's English, page by page, the article's own English abstract and key words standing as printed. CC BY 4.0, so shown whole, and named on the Licences page as the literature's one open-access exception.
- Index hits read and ruled: Józef Wybicki and the Warsaw of two bibliographical references stood; the municipal court "w Brześciu" of the Matuszewicz story is Brześć on the Bug, not Brześć Kujawski - ruled out (NEEDS_CONFIRMATION). No hand-made links yet. `docs/LITERATURE_PLAN.md`, section 20.

## The literature: Mielewczyk (2017), the maps of the villages (2026-10-22, committed; not published)

- Wojciech Mielewczyk, "Zmiany przestrzeni wsi w drugiej połowie XIX i na początku XX wieku na przykładzie wybranych map ze zbiorów Muzeum Narodowego Rolnictwa i Przemysłu Rolno-Spożywczego w Szreniawie", Z Dziejów Kartografii XXI (2017), pp. 41-57 (`literature/mielewczyk2017/`), at the editor's word with the rulings: visible, the figures skipped, a link to the article provided, the whole article brought in. The link is the open-access copy at maphist.waw.pl (the `scan:` of `work.yml`).
- The text from the annual's PDF (`pipeline/literature/mielewczyk_pdf.py`, --check holds all 17 pages against the text layer); the layer's "fi" ligature with its stray space joined (twelve joins listed); the 19 notes at the foot of their pages; the fourteen figures (Ryc. 1-14) not rendered, their captions as text - on four pages a caption stands between two pieces of one paragraph, and a body line never joins a paragraph of another kind. A paragraph ends even when its last run is a note mark (p. 52, "347 tysięcy.[^16]"). The article's own slips kept (the caption of Ryc. 6 reads 1866 against the body's 1886; note 4's "t. 3" against Literatura's "t. 2"; Burszta's title "gospodarstwa wojskowego" in Literatura against note 3's "wiejskiego"; the map titles' own spellings; the unfinished year "192…" of the Lisewo entry). Claude's English; the article's own English block of p. 57 stands as printed.
- The article bears on the edition's ground: fig. 4 is a fragment of the map of the estates of Trąbczyn of 1861 with the field of the enfranchised peasants marked, and p. 48 names Kolonia Łazińskie and Kolonia Huta on the parcelled lands of the Trąbczyn property (the edition's Staro- and Nowo-Łazińska colonies, which the article does not say). Copyright the Institute's (2017), no open licence stated - shown whole at the editor's word; the Licences page not changed.
- Index hits read and ruled: 17 mentions; the map titles' "Kaliszskoj" and "Konińskim" ruled to Kalisz and Konin with the reasons written, the minister Poniatowski of 1938 refused to Prince Józef (an exception added); "Kolonia Łazińskie" is not matched by the edition's patterns (they take only the Staro-/Nowo-Łazińska forms) - whether to add a pattern waits on the editor (NEEDS_CONFIRMATION). No hand-made links yet. `docs/LITERATURE_PLAN.md`, section 21. The literature has 25 works, 23 on the site (two summary-only).

## The newspapers: a new section, and Dziennik Poznański R. 79, nr 180 (7 sierpnia 1937) (2026-10-22, committed; not published)

- The editor's ruling: "Let's make a new section for newspaper articles, since it doesn't really fall under archival sources or literature." A third section stands between the Sources (archival) and the Literature (works about the history): `newspapers/`, on the site at /newspapers/ ("Zeitungen" in German), the menu entry between Sources and Literature. Plan, reading method and open questions: `docs/NEWSPAPERS_PLAN.md`.
- The first item (`newspapers/dziennikpoznanski19370807/`): the "Z Zagórowa" local column of Dziennik Poznański, R. 79, nr 180 (7 August 1937), three anonymous municipal notes closed "(mat)" - the recruitment of some sixty unemployed of Zagórów for seasonal farm work in Germany, the moving of the old people's home to a property of the heirs of Ignacy Ciszewski at Oleśnica on the road to Konin under deputy mayor Franciszek Łukaszewski, and the paving of the streets with trees to be planted along them. Transcribed line by line as printed ("¬" at a word broken at the line's end, the Kuryer Polski convention); Claude's English beside it; era `twentieth-century`. The clipping came as a single JPG in Downloads and is not kept in the repository.
- **No paid run.** The editor asked instead that OCR be installed for the project: Tesseract 5.5.3 (winget `tesseract-ocr.tesseract`) with the Polish models in %LOCALAPPDATA%\Tesseract\tessdata, `pytesseract` installed, and `pipeline/ocr.py` wrapping them (`read()`, `words()`). The text is the agreement of five passes (tessdata_best and the standard model, the page upscaled ×3 and ×4, psm 6 and 4, the Windows.Media.Ocr engine as a third witness); what they did not settle went to the editor on a stand-alone spot sheet of 13 rows with pictures (`scratch/dp1937_sheet.py`, the queries.py page and saving) and was answered in full the same day: m. Zagórowa, zapracowanej, odciążony ("relieved"), the stray fragment between the notes left out, "starców." with its period, Ignacego, **"we wsi i gmina Oleśnica" as printed (the grammar's "gminie" refused)**, szosie, Oleśnicę, przytułkiem, "(mat)" without a period inside, chcąc, the printer's edge fragments ("Pd", "PDZ") left out.
- The site: `pipeline/newspapers/newspapers_site.py` (a step of regenerate.py) writes site/_data/newspapers.yml and one page per item in each language; `_layouts/newspaper.html` shows the item like a work of the literature (one text at a time, the English first); the Newspapers include lists the items by year under their newspaper's name; i18n strings in both languages; verify_site.py checks every visible item's page in both languages and holds a kept-off item (visible: false) to its summary, as it does the literature's. verify_site.py passes whole.
- Open on the editor (NEEDS_CONFIRMATION, "The newspapers"): the clipping's source (its `scan:` stays empty until they say); the rights (anonymous press of 1937 read as public domain by the 70 years from publication - Claude's reading, to be confirmed); whether Kuryer Polski 1754 moves here from the Sources page; whether the index of people and places runs over the items; whether the site carries the clipping itself. Published only at the editor's word.

## The newspapers: Kuryer Polski (1754) moves in; the clipping carried; the index run (2026-10-22, committed; not published)

- The editor's rulings, all worked in the same day: the clipping comes from the blog Zagórów w historii (its post of 2 October 2024, "Kolejne wycinki z prasy sprzed lat, cz. 3") - the `source:` of the item, shown on its page; **the rights are approved** ("Assume the rights are approved"); **the site carries the clipping** (`image:` in item.yml, the figure above the texts - the Dziennik clipping converted from its WebP to JPEG, the Kuryer Polski's page a copy of the derivative the document page showed); **Kuryer Polski 1754 moves** from the Sources page into the newspapers; **the people/places index runs over the items**.
- **Kuryer Polski 1754, nr 75** (`newspapers/kuryerpolski1754075/`): the report on the funeral of Paweł Prusimski at Trąbczyn, 5 December 1754, is the section's second item. The text, the editor's English, the summaries and the page image come over unchanged in their words; the item is no longer one of the edition's documents (the edition counts 619 documents in 46 holdings), its page is /newspapers/kuryerpolski1754075/ with redirects standing at /documents/kuryerpolski1754075/ and /documents/kuryerpolski1754075/1/, the timeline's event of 1754 links the item's page, and the story's and the KDW holding's links point there. The item's caveat names the English the editor's own, not Claude's (`translation: editor`).
- **The index** (`pipeline/newspapers/newspapers_index.py --check`, a step of regenerate.py): the literature's index machinery run over the items' originals, rulings in `newspapers/index.yml`, every hit read before it was ruled - 18 hits in 14 pairs, all ruled: Głowiecki, Paweł, Katarzyna and Antoni Prusimski (the print's Prusiński and Łędzki forms), Kalisz, Konin, Ląd, Oleśnica, Trąbczyn, Zagórów. The People and Places pages carry a box "In the newspapers" beside the literature's; a person of the newspapers who names no document (Głowiecki, whose report left the corpus) stands on /people/ all the same, with no documents shown. The Oleśnica ruling rests on the item's own geography (the village and commune of that name on the road from Zagórów to Konin) and waits for the editor's confirmation (NEEDS_CONFIRMATION). An item's uid in the index is its slug with "-1", so the register's `only_in` filters keep working for the spellings they were written for.
- verify_site.py passes whole: 619 documents character-exact, 2 items with pages in both languages, no broken links (the redirects included).

## The newspapers: Ostdeutscher Beobachter, Jg. 4, Nr. 197 (19. Juli 1942) (2026-10-22, committed; not published)

- The section's third item (`newspapers/ostdeutscherbeobachter19420197/`), given by the editor as a folder with the page image (`1492.jpg`, the WBC object), a markdown file with the German transcription and Claude's English beside it, and the link https://www.wbc.poznan.pl/dlibra/publication/121214/edition/131605/content: the feature "225 Jahre alte deutsche Siedlung im Wartheland" (signed Willi Spatz) on the "purely German settlement" of Lazinsk — Łazińsk — in the Amtsbezirk Drommin. The citation: the Ostdeutscher Beobachter, Organ der NSDAP, Verkündungsblatt des Reichsstatthalters im Reichsgau Wartheland und seiner Behörden, Posen, NS-Gauverlag; the paper ran from 1 November 1939 to 1945 as the successor of the Posener Tageblatt.
- The editor's rulings on the direct questions: the English is Claude's (the item's page carries the standing caveat, like the 1937 item's), and **the item is shown whole without the rights flagged** ("Show it, no need to flag the rights") — put to the editor because the item is signed, unlike the anonymous 1937 clipping. No OCR, no spot sheet, no paid run: "the transcription is secure", the editor's word, and the text stands as the file gives it (the md's escapes resolved; the article's picture marked "[Abbildung]" with its caption kept as text; the print's line division not kept, the file came with the paragraphs whole).
- **What the item bears on the edition's ground**: the Amtsbezirk Drommin of the article is the wartime name of the rural commune of Trąbczyn (`renamed` in reference/places.yml, 2026-10-21); its Lazinsk is the Łazinsk of Breyer's notebook of July 1936 (APP 53/968/0/-/669), which names the same teacher Mielke ("Lehrer i. Łazinsk: Mielke seit 1925") and Michalinow beside it — the article and the notebook, six years apart, witness the same place and the same man. The article's founding date of 1718 stands against the edition's own records (the Łazińskie Olędry from the 1746 foundation, the register and Chodyła 2015; the Nowe Olędry first attested 1776): kept as printed, the difference recorded in the summary (NEEDS_CONFIRMATION, "The newspapers"). The item's judgements are the party paper's own; the account on its page says so.
- The index: two new pairs, read and ruled (`newspapers/index.yml`) — "Konin" (the Kreisstadt itself, the article's walk to the Amtsbezirk begins there) and "Schlesien" (the region the fourteen founding families set out from; the article's "Schlesierlande" is matched by no pattern). 20 hits in 3 items, all ruled, 8 links. **"Drommin" and "Lazinsk" are matched by no pattern** — whether to add patterns waits on the editor (NEEDS_CONFIRMATION, with the Mielewczyk "Kolonia Łazińskie" question).
- Housekeeping: the generated site pages of the Kuryer Polski item (`site/_newspapers/kuryerpolski1754075.md` and its German twin) and the index's corpus record (`corpus/newspapers/mentions.json`), left untracked by the move's commit, are committed here. verify_site.py passes whole: 3 items with pages in both languages, 619 documents character-exact, no broken links. Not published.

## The newspapers: TwojaSłupca, 6 lipca 2015 ("Trąbczyn świętował 775 lat") (2026-10-22, committed; not published)

- The section's fourth item (`newspapers/twojaslupca20150706/`), given by the editor as the address https://twojaslupca.pl/trabczyn-swietowal-775-lat/: the report of the village of Trąbczyn's 775th-anniversary jubilee (the celebration the day before, 5 July 2015; the portal counts from the document of 1240), in TwojaSłupca, the local news portal of Słupca — the first item of the press from the web, no scan, no OCR: the portal's HTML taken as printed, nothing tidied, its own oddities standing ("Wiesław Radniecki Andrzej Kin" without the comma, "Marzena kazimierska" with the small letter, "Anna Siuba" named twice, the spaces after the hyphens, the article's own grammar).
- The editor's rulings on the direct questions: **shown whole** (the article is the press of 2015 and under copyright, unlike the 1937 and 1942 items — the rights approved), and **no picture** — the article's one photograph stays off the site, its place marked "[Obraz]", the `source:` link pointing to the article. The slug's date stands in the issue's place (`twojaslupca20150706`; `docs/NEWSPAPERS_PLAN.md`, sections 1 and 5). The page's one reader's comment is not part of the article and is not kept. Claude's English; the standing caveat on the page.
- **What the item bears on**: its history paragraph is the edition's own documents' story, each claim matched by the KDW holding — the "Trampczin" of 1240 is the KDW's no. 2 (Archbishop Fulko's grant of tithes to Ląd, 30 September 1240 (sic), which the article's "a raczej Trampczin" quotes the Latin of); Janek son of Szymon and the count Mikołaj of Ląd are named in the KDW's charter of 27 March 1276 (Duke Bolesław the Pious's grant of Trąbczyn to count Mikołaj, which recites the earlier grantees); "komes Jan i Przedpełk" are the brothers, heirs of Trąbczyn, of the KDW's two judgments of 1346. The jubilee's arithmetic is the article's own (1240 + 775 = 2015). The article names no edition work; the edition keeps to its documents.
- The index: four new pairs read and ruled, one ruled out (`newspapers/index.yml`) — "Trąbczyn" and "Trąbczyna" in (the village, the honours' name, the exhibition's title), "Prusimski" in (Antoni Prusimski, the register's Starost, of whom the entry's identity says he took part in the uprising of 1794 — the article's context and the register's man agree), "Miączyński" ruled out (the report's heirs-list: Włodzimierz is the register's other entry, pinned to the summons of 1860; "Stanisław hrabia" and "Aleksander" are identified by nothing the edition holds — the register's own `not_in` precedent; NEEDS_CONFIRMATION), and the honouree's surname "Wolicki" ruled out of the place Wolica. 35 hits in 4 items, all ruled, 10 links; the Trąbczyn estate's Places entry and the Starost's /people/ entry each gained the item in their "In the newspapers" box. **"Lądzie", "lądzki" and "Trampczin" are matched by no pattern** — whether to extend the register's patterns waits on the editor (NEEDS_CONFIRMATION, "The newspapers").
- Two rendering faults found and fixed while the item went in (WORKING_NOTES, "Two Liquid traps"): the empty `image:` of an item without a picture made the item layout render a broken figure (Liquid counts the empty string as true; the comparison is explicit now), and the Newspapers list page's Language fact was blank for every item (Liquid cannot build the bracket key by concatenation; the include assigns it first). verify_site.py passes whole: 4 items with pages in both languages, 0 kept off the site, 619 documents character-exact, no broken links. Not published.

## The newspapers: the editor's identifications — Drommin, Lazinsk, Kolonia Łazińskie (2026-10-22, committed; not published)

- The editor's three rulings, put to them with the 1942 item's open questions and answered the same day: **"Drommin = Trąbczyn"** (the article's Amtsbezirk Drommin is the commune of Trąbczyn under its occupation name — the register's `renamed` entry confirmed as the identification); **"Lazinsk = German-era name for Łazińsk, the colony which went by many name variants"** (the article's Lazinsk is Łazińsk, the colony and not a part of one — settling the register's open question "whether Łazińsk is that name or a part of the colony"; the register records Łazińsk as a variant of Trąbczyńskie Stare Olędry, so the article's Lazinsk is that colony, the 1746 foundation; Breyer's notebook of 1936 distinguishes its Alt and Nowo Łazinsk — the Stare and Nowe colonies); **"Kolonia Łazińskie is a variant of Łazińsk/Lazinsk"** (Mielewczyk's form names the same colony, settling which colony his p. 48 form names).
- Worked in: `reference/places.yml` — "Drommin" a matched variant of trabczyn, "Lazinsk" and "Kolonia Łazińskie" matched variants of trabczynskie-stare-oledry, the open questions rewritten with the rulings; `newspapers/index.yml` — the 1942 item's "Drommin" (1) and "Lazinsk" (6) ruled in; `literature/index.yml` — Mielewczyk's "Kolonia Łazińskie" ruled yes (the hit his item's index had left unmade). The index over the items: 42 hits in 4 items, all ruled, 11 links; the Trąbczyn estate's Places entry keeps the 1942 item in its "In the newspapers" box. The bare Polish "Łazińsk"/"Łaziny" stay `match: false` (their literal would also catch the Nowe colony's "Łazińskie", and matching them would bring Breyer's "Łazinsk" of 1936 in — NEEDS_CONFIRMATION, the editor's word). The 1942 item's account and summary state the identifications as the editor's rulings; the item's `notes.md` has the block.
- verify_site.py passes whole (4 items with pages in both languages, 619 documents character-exact). Not published.

## The literature: Łukasiewicz (1997), the "Black Register" studied (2026-10-22, committed; not published)

- Dariusz Łukasiewicz, "Nowa analiza „Czarnego Rejestru". Studium źródłoznawcze", *Kwartalnik Historyczny* R. CIV (1997), nr 2, pp. 31-62 (`literature/lukasiewicz1997/`), at the editor's word with the rulings: the whole article, visible, the appendix tables as HTML tables. The RCIN digitisation is the `scan:` of `work.yml`.
- The text read from page images (300 dpi, two halves; the four appendix pages printed sideways, read rotated): the PDF's OCR text layer used as a scaffold only and corrected against the images. The register's manuscript in GStAPK (I HA Rep. 7c Südpreußen Nr 14) is the article's own discovery, and its findings correct the register's headline: 48 donataries, 52 donations, 245 estates, nominal value 2 069 550 Thaler, real value 4-7 million (nearer 4) against the title page's 20 million.
- The tables as HTML (Tabela 1's six columns and its number row 1-6 taken from the print's own rules; the print has no serial numbers in the name column - the draft's first pass had added them and they were struck); the table notes as `[^t1-n]`/`[^t4-n]`; the print's slips kept and listed (`notes.md`); the two notes split across page feet keep their split; the journal's own English summary stands as printed with its French-stressed spellings, verified on enlargements. Claude's English page for page.
- Where the article's figures differ from the edition's documents, the documents stand (the Triebenfeld sale: the register's entry and the letters 400,000 to Prince George and 750,000 on, the article 450,000 and "the same year" - his reading of Dorow's printing).
- Index hits read and ruled (the kings yes; Massenbach yes on the article's own n. 24; Niemojewski and Wybicki yes on the confiscation list; Adelheid Simsch refused to the Princess; the donatary Grävenitz, councillor Schmaling and the Freiherr von der Reck refused with reasons and open in NEEDS_CONFIRMATION, "The literature"; the imprint towns and the titles carrying Berlin refused). Two hand-made links: the Triebenfeld story and Tabela 4's row to the Prince's three letters, and Tabela 1's Hohenlohe row to the five letters of the register's Hohenlohe link. `docs/LITERATURE_PLAN.md`, section 23.

## The newspapers: Słowo (1892) sells Trąbczyn (2026-10-22, committed; not published)

- Słowo, R. XI, nr 2 (4 January 1892), p. 3, the "Sprzedaże dóbr" notice
  (`newspapers/slowo18920104/`), at the editor's word: the snippet named, the
  editor's own crop of the column carried on the item's page (`slowo.jpg`),
  the Crispa digitisation as the `source:`.
- The notice's five printed lines transcribed line by line as printed ("¬"
  at the two broken words), read by Tesseract (three passes) with word-level
  zooms; five readings ruled on a spot sheet: **za** (no acute), the buyer's
  **Władysławowa** (the married form), **peckim** (the print is grammatical),
  the figure **150 włók** against the draft's 159, and both digitisation
  artefacts (the streak before the number, the sliver at the crop's foot)
  left out.
- The item is the press witness of Trąbczyn's sale by Count Miączyński to
  Countess Władysławowa Wielopolska for 225,000 rs. — the transfer the
  wlodzimierz era's ownership line records ("by 1892 Countess Maria
  Wielopolska"); the item sits in that era. Open: whether the press's
  "Władysławowa Wielopolska" and the era's "Countess Maria Wielopolska" name
  one woman (NEEDS_CONFIRMATION, "The newspapers").
- The index run over it: one hit, Trąbczyn, ruled (`newspapers/index.yml`);
  the notice's "hr. Miączyńskiego" is outside the Miączyński patterns' forms
  (the genitive after "hr."), said in the notes. The "In the newspapers" box
  on Trąbczyn's page on /places/ now carries the item beside the Kuryer
  Polski's. `docs/NEWSPAPERS_PLAN.md`, section 5.

## The place pages: Zagórów (2026-10-22, committed; not published)

- The editor's new section (`places/`, `docs/PLACES_PLAN.md`): a page per
  place that has sources of its own, hung on the place's card on the Places
  page and linked from it — "Let's add a new source to a place: Zagórów.
  This site has a lot of information that should be added under the place
  name, on a separate page for the place." Built like the newspapers'
  machinery, bilingual like the person pages; a place page hangs on an
  estate card, and the build fails loudly if its slug is no estate.
- The first place, Zagórów (`zagorowo`): /places/zagorowo/ and
  /de/orte/zagorowo/ (`pipeline/places/place_pages.py`, collection `places`
  and `places_de`, layout `place`, one viewbar for the whole page, the
  "More about the place" line on the card, the checks in verify_site.py).
- The first source, `zagorowpl20220614`: the town's own presentation on
  zagorow.pl ("Miasto i gmina Zagórów" — historia, położenie, atrakcje,
  kultura), a digital flip-book, kept by the Wayback Machine in the capture
  of 14 June 2022 the editor gave. The editor's rulings of the day: the
  source shown whole (Polish as printed, nothing tidied; Claude's English
  beside it, the English first); a new per-place page; **no pictures** —
  the page's photographs (the document of 1240, the coat of arms, the
  flag) stay off the site, their places marked "[Obraz]". The viewer's
  furniture is not kept; the page's slips stand and are recorded
  (`places/zagorowo/zagorowpl20220614/notes.md`).
- What it bears on: the quoted fragment names "Zagorowo" among the villages
  of the confirmation of 1261 — the form the edition's Places page records
  from the KDW; the box "Historia" names the Olędrzy of the Puszcza
  Pyzdrska; the page names Ląd, Rzgów, Drzewce, Imielno and the rest of the
  edition's ground. Its self-contradictions (1262/1261; 1869/1870) are
  kept as printed and recorded (NEEDS_CONFIRMATION, "The places").

## The literature: Kneifel (1964), the church history excerpted (2026-10-22, committed; not published)

- Eduard Kneifel, *Geschichte der Evangelisch-Augsburgischen Kirche in
  Polen* (Selbstverlag des Verfassers, Niedermarschacht 1964)
  (`literature/kneifel1964/`), at the editor's word with the rulings asked
  before the work began: the excerpt carries the place-named pages **and**
  the two colonisation sections that set them; the work is shown on the site
  (in copyright: published 1964, put to the editor first); only the excerpt
  scripts and the cut pages are committed, not the two source files (313
  printed pages, most of it not bearing on the edition).
- The editor's two files (German transcription with printed page numbers and
  GFM footnotes; English pairing it page for page) are read by
  `make_original.py` from their folder on J:; 21 printed pages brought in,
  whole where the relevance is dense, cut to paragraphs with "[…]" elsewhere
  (`notes.md` lists the selection and the cuts): the rural colonisation
  (III.1, pp. 39-42, p. 41 naming "Paul von Kolno-Prusinski, Grundherr von
  Trombezyn" and the founding of Łazińsk in 1746), the Prussian colonisation
  (VI.1, pp. 89-93, the towns "Konin, Zagö-röw und Kolo"), the schools of
  the Kalisch land (pp. 45, 112), the Grodziec parish contract of 1796
  (p. 94), the parishes Stawiszyn/Prazuchy/Sobiesenki/Łask/Slesin (p. 102),
  the diocese of Kalisch's parish list "Zagörow mit dem Filial
  Lissewo-Pyzdry, Konin mit dem Filial Maslaki" (p. 123), the churches of
  the region (pp. 165, 166: the Zagórów church of 1878-1896; p. 179 Konin
  and Masłaki), the inter-war parishes (p. 226, the Zagórów pastor Alexander
  Groß 1923-1945), the brethren's circles in Łazińsk (pp. 235-236) and the
  statistics of 1938 with the "rein deutsche evangelische Gemeinde Zagorow"
  (p. 256).
- The false friend ruled out in the scan: p. 101's colony "Trombin bei
  Rypin" (the Dobrzyń land) is not Trąbczyn. Nothing tidied: the print's
  slips stand and are recorded in the notes.
- Index hits read and ruled (140 in the work): new forms `Trombezyn`,
  `Zagörow`/`Zagö-röw`, `Lazinsk` (the editor's Łazinsk ruling of
  2026-10-22) and `Prusinski` (the print drops the ń); `Brzyczka` refused
  (Reptowski's colony near Łódź); old rulings sharpened with exceptions
  (Schröttersdorf, the Posen imprints, "Lissewo-Pyzdry", Dembina- and
  Koneck-Holland, and Wielun now taking the town by exception against
  Guradze's field). One hand-made link: p. 41 against the summons of 1860
  and the boundary decree of 1775 — Kneifel names the husband alone, the
  documents the couple; the edition follows the documents.
  `docs/LITERATURE_PLAN.md`, section 24. **Published 2026-10-22** at the
  editor's word.

## The literature: Werner (1904), the parish histories of the province of Posen (2026-10-23, committed; not published)

- Albert Werner, *Geschichte der evangelischen Parochien in der Provinz
  Posen*, überarbeitet von Johannes Steffani, herausgegeben von dem
  Königlichen Consistorium der Provinz Posen (Lissa: Friedrich Ebbecke 1904)
  (`literature/werner1904/`), at the editor's word with the page images of
  the WBC digitisation (publication 34695, edition 51858) in Downloads:
  "only entry 201 about Wreschen is relevant for the project, hence that's
  what's made available here". The excerpt is entry 201, the parish of
  Wreschen (Września), printed pp. 422-424, whole, with the book's title
  page as the work's front. Out of copyright; shown whole as far as brought
  in.
- The entry's bearing on the edition: the Wreschen parish originally served
  the German Hauländer country around **Peisern (Pyzdry)** and **Zagorowo
  (Zagórów)**, and "eine an deutschen Hauländereien reiche Gegend" went from
  it in 1817 when those places came to Russia - the edition's Olęder ground
  and its place `peyserschen-hauland`. The parish's founding by the
  Ponińskis (1758, 1760, the orangery of 1 May 1778, the parish of 1779),
  the churches of 1822 and 1895, the Filial Wilhelmsau of 1892 with its
  Bethaus of the Royal Settlement Commission, and the ten pastors of
  1779-1904. No document, person or settlement of the edition is named: no
  hand-made links.
- **Read by OCR alone** (no transcription existed, and the scans' text layer
  is not in the repository): the lunaroute document converter over the whole
  pages, the bands and the single lines, the passes checked against each
  other (Fraktur ſ→f/j, kt→ft handled by rule; no local Tesseract on the
  editor's machine). The readings a name or fact rests on that the passes
  did not settle are on the editor's spot sheet (`scratch/werner1904_sheet.py`,
  20 rows with crops; answers to `review/werner1904/query_answers.json`).
  Two identifications from outside the page (Orangeriehaus, against the
  Polish accounts of the same gift; the General Superintendent Hesekiel)
  are recorded in the notes and NEEDS_CONFIRMATION.
- Index hits read and ruled: `Peisern`, `Zagorowo` (the print's German form)
  and `Rußland` stand; refused: the title page's and heading's `Posen` (the
  province and the Diözese), `Liegnitz` and `Pommern` (pastors' birthplaces),
  and `Sokolnik` (a village of the Wreschen parish, not the edition's Amt
  Sokolnik - open in NEEDS_CONFIRMATION). `docs/LITERATURE_PLAN.md`, section
  25. The literature has 32 works, 30 on the site (two summary-only). The
  spot sheet open; not published.

## 2026-10-22 — The newspapers: the three Lidmanowski texts

- **Three new items** (`newspapers/zdrowie1912z10/`, `newspapers/
  jutrzenka1913z8/`, `newspapers/zdrowie1914z6/`), from the editor's file
  "Texts by Dr. Konstanty Lidmanowski, Zagórów (1912-1913).md" — English
  and Polish together, each with its digitisation link, the transcription
  secure (the editor's word; no OCR, no spot sheet, no page image carried).
  The first items that are articles of learned journals: two in *Zdrowie*
  (the organ of the Warsaw Hygiene Society) — the nutrition study of the
  Słupca powiat, R. XXVIII, z. 10 (1912), pp. 720-725, and the housing
  survey, R. XXX, z. 6 (1914), pp. 432-440 — and one in *Jutrzenka* of
  Łódź (R. 3, nr 8, 24 April 1913, pp. 7-10), the digest of Lidmanowski's
  attire article in the March 1913 *Zdrowie*.
- **The housing survey dated 1914** against the file's name
  ("1912-1913"): Polona's metadata, the issue's table of contents ("Lidma-
  nowski K. Dr. z Zagórowa. Jak mieszka lud nasz? . . 432") and the
  literature (Boldyrew) agree. The editor's word.
- **The English came with the file** (made by Claude) and was read
  against the Polish and corrected in session — eleven artifacts, among
  them a sentence the translation printed twice (the nutrition text's),
  "several dozen rubles" for *kilkanaście* (some fifteen), "woolen sailor
  suit" for *ubranie marynarkowe* (a jacket suit), and the like; every
  correction recorded in the item's `notes.md` with the Polish that
  decided it.
- **Rights**: the author, Dr. Konstanty Lidmanowski (30 March 1865,
  Słupca - 6 January 1943, Zagórów; the Polish Wikipedia's article, with
  Kumosa 1992), died 1943, so Polish copyright (life + 70) lapsed in
  2014 — all three shown whole at the editor's word. The Jutrzenka digest,
  if anonymous, out of copyright since 1984 either way.
- **A person entry** `lidmanowski` (reference/people.yml, heading
  "Lidmanowski, Konstanty"), the Głowiecki shape: no documents of the
  edition, the Jutrzenka digest's "dr. Lidmanowski" ruled to him in
  `newspapers/index.yml` (the one text that names him in its body; the
  Zdrowie articles stand on their issue's table of contents).
- **Open in NEEDS_CONFIRMATION**: the Jutrzenka signature (the
  digitisation unreachable from the working session); the life dates
  resting on Wikipedia; Słupca as a place of the edition (it is in no
  register, so the powiat's name matches no pattern); the 1914 date.
  `docs/NEWSPAPERS_PLAN.md`, section 5. Not published.

## 2026-10-22 — The newspapers: the parish's own chronicle of the Zagórów filial

- **A new item**, `newspapers/luteraniezagorow/`: the page "Zagórów filiał
  Parafii Ewangelicko - Augsburskiej w Koninie" on **Luteranie Konin**
  (luteranie.konin.pl/zagorow.html), the Parafia
  Ewangelicko-Augsburska w Koninie's own website — headed "Ważniejsze
  wydarzenia z życia Parafii w Zagórowie", a chronicle in dated entries:
  the Reformation among the monks of Ląd in the sixteenth century; the
  evangelicals from Silesia, Pomerania and Prussia, 1720-1817, under the
  care of the incumbent of the evangelical parish at Września; the
  incumbents of Grodziec, Konin and Żychlin, 1817-1856, and the filial of
  Grodziec founded in Zagórów; the parish erected 24 December 1856; the
  plot of 1857, the foundation stone of 8 May 1878, the consecration on
  the first Sunday in Advent 1882; the cantor's house of 1913; the
  rectory of 16 October 1938; the first service after the Second World
  War, 18 July 1954, the Rev. Karol Świtalski; the Evangelical Senior
  Citizens' Home consecrated in the former cantor's house by Bishop
  Michał Warczyński, 16 June 1995, closed 30 November 2009; the
  electronic clock and bells, 17 August 2008. Given by the editor as a
  website "so I'd group it with newspapers and journals", with their own
  pasted text as first witness. Worked on a **separate branch from main**
  at the editor's word (other work being done there).
- **The page is undated.** No date anywhere on it; the site's footer reads
  "Projekt i wykonanie © Walrom 2011" (the site's making), and the page's
  own menus point its top "Archiwum" at archiwum2015.html and its footer
  menu still at archiwum2013.html — the page stands as of about 2015. The
  editor's rulings: **no date in the slug** (the plan's rule for a web
  item given a recorded exception, `docs/NEWSPAPERS_PLAN.md` section 1) —
  the slug is `luteraniezagorow`, site and page; the footer's 2011 kept as
  the `year:` of item.yml **for the list's order alone**, the comment in
  the file saying so; the citation reads "bd. [bez daty]".
- **Rights**: the page is the parish's own and under copyright; shown
  whole at the editor's word, the rights approved, no rights entry added.
  **No picture**: the page's two photographs of the church stay off the
  site, their places marked "[Obraz]" ("[Picture]" in the English), and
  so does the page's small-print line crediting the photographs to the
  studio Foto Sypniewski (the editor's ruling). **No era**: the item
  stands in no era, the `era:` field left out of item.yml for the first
  time (the comment in the file records it).
- **How it was read**: from the page's HTML, fetched in session, nothing
  tidied; no OCR, no spot sheet. The editor's pasted text settled against
  the HTML: the twice-standing "Kościół Ewangelicko-Augsburski w
  Zagórowie" is the two photographs' alt/title text, not prose;
  "parafiiz Grodźca" of a bare fetch is an artifact, the page breaking
  the line after "parafii" (the transcription keeps the break); the page
  pads the broken second lines of the 1856 and 1995 entries with ten
  non-breaking spaces — layout, not text, the break kept and the padding
  not; "plebani" (1938) stands as printed, for plebanii; the "(czytaj
  więcej)" of the 2009 entry is a link to the site's own page about the
  Dom Seniora, kept as printed.
- **The index run**: 54 hits in 9 items; the item's three new pairs all
  ruled in — `zagorowo` "Zagórów" (the heading, the bare nominative) and
  `grodziec` "Grodziec"/"Grodźca" (the parish of Grodziec, named by its
  place). Not matched by any pattern: "Lądu" (the genitive) and the
  Polish region names "Śląska, Pomorza, Prus" (the register's Schlesien
  pattern is the German word only) — the same open question as the 2015
  report's Ląd forms (NEEDS_CONFIRMATION, "The newspapers").
- **What it bears on**: Werner (1904), entry 201 — the Wreschen
  (Września) parish that served Zagórów's evangelicals until 1817 is the
  page's "1720 - 1817 ... we Wrześni", and the page's Grodziec, Konin and
  Żychlin years are the story Werner's entry stops at; Kneifel (1964) —
  the church of 1878-1896 (the plot, the foundation stone, the
  consecration) and the diocese list's "Zagörow mit dem Filial
  Lissewo-Pyzdry". The page names no sources; nothing in it contradicts
  the edition's documents. Not published.
  `docs/NEWSPAPERS_PLAN.md`, section 5;
  `newspapers/luteraniezagorow/notes.md` first.

## 2026-10-22 — The literature: Słowiński and Połom (2024), "Zerwane ogniwo", and Słowiński (2023) finished

- **A new work**, `literature/slowinskipolom2024/`: the collective volume
  *Zerwane ogniwo. Ewangelicy na ziemi zagórowskiej* (Zagórów: Urząd
  Miejski w Zagórowie 2024, edited by Mirosław Słowiński and Katarzyna
  Połom, ISBN 978-83-969906-0-0), from the editor's checked Polish and
  English Markdown exports of the same day (made from the PDF's text
  layer; the PDF and the .md files not kept in the repository). All 336
  printed pages read: the studies (the parish history, the Hauländer
  settlement of 1746-1806, the interwar church, the kantors, the Beutlers,
  the Mielke letters, Breede), the memoirs (Erich Kuhn's among them) and
  the German-era testimonies (*Der Heimatbote*'s note on Łazińsk, the
  chronology table, the 1945 inhabitants list of Michalinów
  Trąbczyński/Łazińsk/Huta Trąbczyńska, the forged Reichsstelle document).
- **A new intake script**, `pipeline/literature/slowinskipolom_md.py`, the
  twin of `slowinski_md.py` with one change: this book's export sets each
  picture plate's captions in a block of their own after the running text
  has flowed past the plate, the block opening with the plate's page mark
  again and closing with the mark of the page the text had reached - often
  a greater number, which the old rule (marks never run backwards) dropped.
  The script returns on any mark whose page was opened before and switches
  to that page's object. The letter check holds every PDF page to the
  layer: 0 differ (the allowances - the clock-face O of the cover written
  OGNIWO, the twice-printed section titles of the tables of contents, the
  word divisions and the spread captions - in the work's notes.md); the
  English's 336 marks are the original.md's, in order. The 119 pictures
  are not rendered (the editor's word); their captions stay, being text.
- **Under copyright, summary only** (the editor's ruling, like Seidel 2018
  and Słowiński 2023): in the repository for questions, `visible: false`,
  the site showing the detailed summary in both languages and none of the
  text (verify_site.py checks - one stretch the two Słowiński summaries
  shared, the Mielke letter's "temples" sentence, shortened in the older
  one so the check stays clean).
- **Słowiński (2023) committed alongside** (the folder had stood untracked):
  its English is the editor's own English .md, not the planned Claude
  translation (`slowinski_md.py --english`; `translation_chunks/` left
  untracked); its year corrected to 2024 where the texts spoke of the
  sister volume (the title page's).
- **What it bears on**: the 1718 founding of Łazińsk a third witness (the
  ruling still wanted); the founders of 1746 in yet another form; the
  Mielke dates conflicting (NEEDS_CONFIRMATION). The work is invisible, so
  no index rulings and no hand-made links (the precedent). The literature
  has 34 works, 30 on the site and four summary-only. `docs/LITERATURE_
  PLAN.md`, section 26. Not published.

## 2026-10-22 — The newspapers: Echo Tureckie, R. 8, nr 18 (6 maja 1931), nr 379, "Zajście w Zagórowie"

- **A new item**, `newspapers/echotureckie1931018/`: the Zagórów edition
  of the Turek weekly Echo Tureckie's report of the clash at the
  recruiting commission of 24 April 1931 — the workers' crowd stoning the
  premises when the season's quota ran out, the starosta of Słupca
  arriving with reinforcements of police, the second storming, the
  dispersal, a dozen or more persons arrested — anonymous, no signature
  and no siglum. From the blog **ZAGÓRÓW-MIEJSCE Z HISTORIĄ** (the
  editor's word for the title; the same post of 2 October 2024 the 1937
  clipping came from, the file's leading "8." the image's order in the
  post), the rights approved, the clipping carried on the page, the item
  shown whole.
- **Read by four Tesseract passes** — the Windows.Media.Ocr engine, the
  plan's third witness, unavailable the day (`winrt` not importable in
  the session's Python) — with six rulings on a spot sheet
  (`scratch/et1931_sheet.py`, port 4108): "widownią" the print's
  line-broken word (the engines' shared "hią" the print's fractured "ń"),
  the mark on the k of "rekrutacyjna" not a letter, "kontyngent" against
  the engines' agreed "kontygent" (the print carries the n), the
  right-edge sliver and the final line's leading mark left out, "lokal."
  with its period. This clipping breaks its words **with printed
  hyphens** (the Kuryer Polski and the 1937 clipping broke without), so
  the "¬" convention appears nowhere.
- **The editor's rulings of the day**: the paper's title Echo Tureckie
  ("Zagórów" the edition's name; the `newspaper:` field carries Echo
  Tureckie, the citation's full shape recorded under `published:` and in
  the notes); the whole clipping transcribed; the slug
  `echotureckie1931018` (the year's issue number in the Kuryer Polski's
  shape, the absolute nr 379 in the citation alone); shown whole, the
  rights approved (anonymous press of 1931, public domain since 2001
  besides); the blog's new name for this item, the 1937 notes untouched.
- **On its own branch**: the work stands on `echotureckie1931018`, cut
  from main as the session found it (the luteraniezagorow commit
  beneath, the parallel work's own; main itself left where that work
  stands); built and verified (ALL CHECKS PASSED, 619 documents
  character-exact, 46,468 internal links resolving); not published.
- **What it bears on**: the recruitment of seasonal workers for Germany
  — the "Z Zagórowa" column of Dziennik Poznański of 1937 records the
  trade as routine, this item its violence six years earlier; both from
  the same blog post. The item names nobody; the index's hits are
  Zagórów's three forms, already ruled. The report's "yesterday" against
  the issue's 6 May is the dispatch's own arithmetic, recorded in the
  summary, corrected nowhere. `docs/NEWSPAPERS_PLAN.md`, section 5;
  `newspapers/echotureckie1931018/notes.md` first.

## The newspapers: Kurjer Poznański, "(Zhitleryzowani koloniści)" (2026-10-22, committed; not published)

- The anonymous note in Kurjer Poznański of 12 July 1933 (`newspapers/kurjerpoznanski19330712/`), the eleventh item of the press and the third from the blog ZAGÓRÓW-MIEJSCE Z HISTORIĄ (its post of 24 May 2024, "To i owo, cz. 2"): the German colonists of the rural communes of Oleśnica, Trąbczyn and Szymanowice around Zagórów, whose colonies once bore German names (Emilienhain, Ludwigslust), who since Hitler's taking power in Germany "as if something turned over in their heads" speak German at the commune office and answer German to a Polish "dzień dobry" at school — and the closing incident: the school where an Evangelical taught, empty of the colonists' children on the school inspector's visit, the teacher dismissed from his post after it. The citation carries the date only (the clipping gives no issue number): `kurjerpoznanski19330712`.
- **Read by OCR, four passes** (Tesseract best and standard, ×3 and ×4, psm 6 and 4) with the doubtful places settled at the pixel level first (the ogonek of "Trąbczyn" — the print has it and every pass dropped it — the ł of "nosiły", the ę of "języku" and "uczęszczające", the g of "ewangelik" where two passes read "selik", the period after "Niemców", the comma after "Hitlera", the period after "przekręciło", the „…” round "dzień dobry"), and four rulings on a spot sheet: the parenthesised lead "(Zhitleryzowani koloniści)." with the word set solid (the completive z- on hitleryzowani), "Ludwigslust" (the German form, against the passes' split), the plain "a" of "nie w polskim a niemieckim języku". The print's "kolonje" stands as printed; nothing tidied, 22 lines, the "¬" at each break.
- **Shown whole** (`visible: true`): anonymous press of 1933, the rights approved on the 1937 clipping's ruling; the clipping carried on the item page (a genuine JPEG this time, 648 × 573, unlike the Dziennik's WebP in .jpg clothing); the English Claude's, the standing caveat.
- **What it bears on**: the press witness of the colonists' "hitleryzacja" seven years before the 1942 feature's "purely German settlement" of the same population; the print's "Emilienhain" against the documents' "Emilienheim", and the dismissed teacher identified by nothing the edition holds (both NEEDS_CONFIRMATION). `docs/NEWSPAPERS_PLAN.md`, section 5. Not published.

## The register: Ludwigslust (2026-10-22, at the editor's word)

- **Ludwigslust made a place of the edition** (`reference/places.yml`, `ludwigslust`, kind settlement, tier Book-confirmed, `match: 'Ludwigslust\w*'`): the colony of the Zagórów lordship's dismemberment — named in the edition's own documents (Oe 1 Bü 9454: letter 24's list "12 Ludwigslust"; letter 177's naming list "Friedrichsfeld, Ludwigslust. = Grądzyń." and its register of new villages "7. Collonie von 1590 Morgen besezt mit 40 wirthe heiß Ludwigslust") and in the literature (Breyer 1935 Gaue among the villages keeping their old German names; Breyer 1938's section "Ludwigslust - Mały Las" with the refused petition of two colonists to the Königsberg government of August 1816 in the name of 10 families; Wąsicki 1953's list of the villages founded on Hohenlohe's estates; Słowiński and Połom 2024, "Kolonia Ludwigslust (obecnie Mały Las)"). The editor's word came with the Kurjer Poznański item, which names the colony among the German-named colonies around Zagórów.
- **The Polish name recorded, not matched**: "Mały Las" (Słowiński and Połom's "obecnie", Breyer's section title) is a `match: false` variant — a common-noun phrase a bare pattern would catch all over the corpus.
- **An open question recorded in the entry**: the naming list and the register of new villages, two enclosures of the one letter (177), do not agree which old ground the colony sat on (the naming list pairs it with Grądzyń, the register lists it under "bey Kopojno").
- **The literature's six hits ruled** (`literature/index.yml`: breyer1935gaue one, breyer1938 four including the adjective "Ludwigsluster", wasicki1953 one; `--check` passes), and **the item's fourth hit** in `newspapers/index.yml`.
- **The corpus dataset rebuilt on the merged tree** (`pipeline/build/build_dataset.py`, then build_site_data, Jekyll, verify_site all pass): oe1bu9454-177 and oe1bu9454-24 gain their Ludwigslust place mentions (the surfaces stood unlinked, `entity: ""`, since no register entry existed), `corpus/index/place_mentions.json` and the site's `places_named.yml` carry the place; the two letters' pages relinked. The Mielke catch-up in Breyer's notebook (app539680669-1) the parallel session's rebuild had already made (its commit e6ea4f43); the merge carries it once.

## Deliverables produced

`letters.csv` / `letters.json` (database), `von_Triebenfeld_Hohenlohe-Ingelfingen_chronological.txt`, `collation_48_302.md`, `transcription_error_profile.md`, `phase2b_transcription_audit.md`, `currency_normalisation_report.md`, `parsed_dates_review.csv`, `phase2_proper_noun_report.md`.

## 2026-10-23 - The literature: Kraus (2001), chapter III and Anlagen 8 and 10

- **A new work**, `literature/ostensacken2001/`: Gerlinde Kraus,
  *Christiane Fürstin von der Osten-Sacken: Eine frühkapitalistische
  Unternehmerin und ihre Erben während der Frühindustrialisierung im
  18./19. Jahrhundert* (Stuttgart: Franz Steiner 2001, Beiträge zur
  Unternehmensgeschichte Bd. 10), the biography of the mother of
  Marianne Gräfin von Hoym, the Prince's wife. Chapter III whole (printed
  pp. 33-42) and, from the appendices, Anlage 8 (the daughter's letter of
  12 October 1811, "Ein Wort des Vertrauens") and Anlage 10 (the mother's
  codicil of 6 November 1807) - the editor's word "Skip what's between"
  keeps Anlage 9 and the first lines of Anlage 11 out, marked with `[.]`
  (the Kneifel convention). Read from the editor's two-up page scans by
  two OCR engines checked against each other (Tesseract 5.5.3 with the
  German traineddata installed for the newspaper work - found on the
  machine though not on PATH - and the lunaroute converter), doubtful
  words read at 3x-6x zoom crops; the readings settled and the print's own
  slips („Zransact", the "(1792-1822)" of Hardenberg, "Vollblütigkeit",
  the codicil's "60/m tausendstel") written out in the work's notes.md.
  Footnote keys page-scoped (`[^p33-1]`, `[^p325-4]`) because the
  chapter's notes 1-43 and the Anlagen's own numbering collide.
- **The copyright ruling**: the book is in copyright (2001, the imprint
  forbids reproduction and translation). Put to the editor with the
  summary-only rule named (section 4 of the plan), they ruled "Full text,
  at my word" - `visible: true`, the third full-text exception (the
  TwojaSłupca report, Werner's entry).
- **What it bears on**: p. 42 - the prince sold the lordships "Betsche,
  Zogorowo, Trobczyn, Botkowo und Winiec weit unter Wert" to come by
  "baare Mittel", the book's spellings of the edition's Zagórów and
  Trąbczyn among them. A hand-made link ties the passage to the royal
  consent of 28 January 1806 to the parcelling of "Zagurowo und Trompczyn"
  (app539680801-2). The new spellings entered as literature-only patterns
  in `literature/index.yml` and ruled; Baildon, Cosmar, Glenk,
  Kircheisen, Emilie, the princes August, Adolph and Alexander, Öhringen,
  Langenburg, Neuenstein, Kirchberg, Oppurg and Schlawentzitz ruled yes;
  the medieval Albrecht and Eberhard of Hohenlohe and the house of
  Bartenstein ruled no. 14 passages, 5,450 literature hits all ruled,
  29 hand-made links.
- **verify_site.py's leak check refined** (checker internals, Claude's
  call): the leak scan for hidden works' text now skips the built pages of
  the works shown on the site. Kraus (2001) and the hidden Seidel (2018)
  both carry the letter of 12 October 1811 - a shared quoted source - and
  the scan's 60-character needles matched Kraus's own page. A shown page
  is the editor's authorised text in full; a hidden work's own page is
  still checked strictly (summary only).
- Committed, not published; publish at the editor's word.

## 2026-10-23 - The newspapers: the death notice of Włodzimierz hr. Miączyński

- **A new item**, `newspapers/dziennikpoznanski18791220/`: the nekrolog in
  the black-bordered box on p. 4 of Dziennik Poznański, R. 21, nr 292 of
  20 December 1879 (the WBC digitisation, sygn. Cz4293 of PAN Biblioteka
  Kórnicka, "domena publiczna") — the press witness of the death of Count
  Włodzimierz Miączyński, "dziedzic majętności Trąbczyna w Królestwie
  Polskiem", at Trąbczyn on the 18th of December 1879 after long
  sufferings, "opatrzony ss. sakramentami"; the "Ekspedycya zwłok" on
  Monday the 22nd, the funeral "nazajutrz"; signed by the grieving nephew,
  Władysław hr. Miączyński of Pawłowa. The section's first death notice,
  and the press witness of the event the wlodzimierz era's ownership line
  turns on (it names the nephew who succeeds).
- **Read by Tesseract** at the editor's word (the item's own readings
  ruled in session; the doubtful list in the item's notes.md): the
  microfilm's 300 dpi page defeated the display-capital name line and the
  body's first word ("Zmarł"), so the issue's DjVu was fetched again from
  the WBC (`/Content/84585/DjVu/0004_0001.djvu`) and rendered at 600 dpi,
  where the same lines read — the heading "Włodzimierz hr. Miączyński,"
  one giant line, then "dziedzic / majętności Trąbczyna / w Królestwie
  Polskiem," stacked, then the body. Open readings: "Polskiem" (the 600
  dpi crops suggesting "Polském"), "Ekspedycya" (against the passes'
  "Eksportac"/"Ekoportacja" shapes; the standard phrase and the descender
  pattern decide), and the funeral day after "nazajutrz" — the glyph
  reads as an 8 to every pass but is no digit to the English engine set to
  digits alone, and the sense after a Monday the 22nd allows only the 23rd.
- **The death date stands against the edition's records**: the notice says
  the 18th of December, the editor's ruling of 2026-10-15 (the notebook
  APP 53/968/0/-/716) the 20th — and Żychliński (1891, p. 222) has the
  18th too, the question already open (NEEDS_CONFIRMATION, "The
  literature"). The notice is a period witness on Żychliński's side; the
  documents first, the ruling the editor's. The item keeps the press's
  date as printed.
- **The index run**: one hit, Trąbczyn, standing under the ruling already
  in `newspapers/index.yml`; no new rulings needed. The Count's own
  mention the register's patterns bring in nowhere (the Włodzimierz
  entry's `only_in` pin to the summons of 1860; the bare "Miączyński"
  under the 2015 report's standing "no" ruling).
- The image carried on the item's page (the editor's 0004_0001.jpg of the
  WBC download). The item is visible (anonymous press of 1879, public
  domain); committed, not published; publish at the editor's word.


## 2026-10-23 - The gazetteer: the editor's index of places (step 1, the import)

- **The editor's "Place Names.md"** (their own index of the places around
  Trąbczyn and Zagórów: 112 entries, 21 cross-references, 119 footnotes)
  kept verbatim in `reference/gazetteer/source/` and imported into one
  YAML per place (`reference/gazetteer/<slug>.yml`) by
  `pipeline/gazetteer/import_place_names.py` (a record; the YAML is edited
  by hand from here on). The plan, agreed with the editor the same day, is
  `docs/GAZETTEER_PLAN.md`: the modern name heads an entry, the register's
  slugs stay, the editor's text is kept as written, every place gets a
  page, the work is on the branch `gazetteer`.
- **The footnotes resolved**: every work they cite is a key of
  `reference/gazetteer_sources.yml`, with how a locator becomes a link.
  76 of the 119 footnotes link to the edition (the Kodeks entries by volume
  and number; the leaves of the boundary decree of 1775 to their pages,
  the foliation checked against five quoted phrases; the Ląd copy-book,
  the lease of 1806, Breyer's notebook, the village table of 1797, the
  visitation of 1791, Chodyła, Breyer, Szwiec, Słowiński & Połom,
  Minakowska, the glossary's "stawisko"). The Kodeks no. 1464 (1362) the
  edition holds as the Ląd copy-book's copy, and the footnote links to it.
- **The maps** the entries cite listed in `reference/maps.yml` (27 maps,
  179 appearances; none in the edition yet).
- **`docs/MISSING_SOURCES.md`**, the running list of sources still to bring
  in (the editor's word): its gazetteer part made by
  `pipeline/gazetteer/gazetteer.py --missing`, a part by hand for what the
  rest of the project waits on. `gazetteer.py --check` holds the links,
  keys and slugs.
- **Read against the documents**: the points where the entries and the
  edition's documents differ are in NEEDS_CONFIRMATION, "The gazetteer",
  the text unchanged until the editor rules (Mieszko III for the grant of
  1173; the 1411 *scultetia* read as "scullery"; the 1418 exchange of farms;
  the 1440 charges of 300 and 200 marks; the colonies' names as the
  Prince's lists of 1805-1808 write them; Augustynów and the lease of 1806;
  the archive of the visitation; the renaming of 1891; four identifications
  with the register). The 1287 of the exchange of Wrąbczyn agrees with the
  Kodeks (no. 685 confirms in 1292 an exchange "made five years before").
- **The editor's voice**: the file analysed as a fourth sample, of index
  entries, with a brief of its own (`docs/EDITORS_VOICE.md`); the editor's
  remark on method made a house rule (`docs/HOUSE_STYLE.md`, "No method
  talk").
- The parsing and the scripts were done by a Sonnet sub-agent at the
  editor's word (WORKING_NOTES, "Working with the editor"); its output read
  and the links spot-checked before commit.

## 2026-10-23 - The gazetteer: "Stara Huta Olędry", a name of two places

- The editor's cross-reference "*Stara Huta Olędry* — See **Huta**" pointed
  to no entry. The edition's sources use the name for both Hutas, and the
  editor ruled it listed as both (2026-10-23): a name item with
  `shared_with` and its sources in each entry. Huta Trąbczyńska: Słowiński
  (2023), p. 98 (Łazińsk Drugi "dawniej ... Holendry Stara Huta"),
  Chodyła (2015), p. 84, note 154, the village table of about 1797, entry
  283, and the Prince's papers of 1806 (Oe 1 Bü 14526, document 8; Oe 1
  Bü 9454, letter 24), beside Richter 1843's "H. Stara Huta". Huta
  Łukomska: Chodyła, pp. 70 and 76, and the 1797 table, entry 281. A third,
  Stara Huta-Grójeckie Olędry in Grodziec parish, is not to be confused
  (the 1797 table, entry 282). Three source keys added to
  `reference/gazetteer_sources.yml` (slowinski2023, oe1bu14526, oe1bu9454).

## 2026-10-23 - The maps: the plan

- `docs/MAPS_PLAN.md`, at the editor's request ("how can we setup the
  architecture needed to process maps?"): the originals stay on the
  editor's drive; each chosen map cropped to the area and cut into IIIF
  level-0 tiles in a second repository with its own GitHub Pages site (the
  edition's repository is 854 MB packed, its site 700 MB); a labelling page
  built like the fold page (OpenSeadragon; the place's point, the traced
  lettering, what the map shows); every mark in the original's pixels;
  georeferencing from the editor's own MapWarper control points (sixteen
  maps already warped there, found from the `.kml` files beside the images)
  and from the marks of the places with coordinates, the warp shown in the
  browser by Allmaps; coordinates for the vanished places from the fit; a
  viewer page per map, the crops on the place pages, and the interactive
  map over OpenStreetMap. A pilot (proposed: Łukom 1766) before the rest.
- **The editor chooses the maps** (2026-10-23: "I will be selective with
  them"): the plan, `reference/maps.yml` and the missing list say so; the
  list's maps section is now "Maps cited", not a list of wants.
- The editor agreed the plan's recommendations (2026-10-23): the second
  repository for the tiles, the pilot Łukom 1766, libvips (installed:
  pyvips 3.2.0, libvips 8.18.7). MapWarper's API answers: a map's
  record gives the uploaded image's size, its `gcps` the control points
  (Łukom 1766: five). The map's original is the file of that size (for
  Łukom the PNG, not the JPG), recorded in MAPS_PLAN, section 5.

## 2026-10-23 - The maps: the pilot, Łukom 1766

- At the editor's word ("go ahead with the Łukom map ... Let's only do this
  one map for now"): the second repository **triebenfeld-maps**
  (github.com/takaji10/triebenfeld-maps, published at
  takaji10.github.io/triebenfeld-maps/), public, holding the image tiles
  and georeferences only.
- **The scripts** (`pipeline/maps/`): `tiles.py` (IIIF level-0 tiles with
  libvips; the info.json id fixed after libvips doubles the name),
  `mapwarper.py` (the editor's control points from MapWarper's API),
  `georef.py` (the affine fit, residuals in metres, positions of the marked
  places, the Allmaps annotation), `label_page.py` (the labelling page,
  OpenSeadragon 4.1.1 kept in the project), `import_labels.py` (the saved
  marks into `maps/<map>/labels.yml`, the crops of the lettering, the links
  to the gazetteer), `test_crops.py`. Written by Sonnet sub-agents to a
  spec at the editor's word, read and corrected in the main session (a
  gazetteer file that does not parse now stops the run; items marked
  `absent` skipped).
- **Łukom 1766**: the editor's north-up PNG (10,280 × 8,523) as the
  original, `view_rotation: 180` (drawn south-up, the editor's word); 502
  tiles, 15.8 MB; five control points, affine RMS 336 m; the warp test
  page. The gazetteer's nine names to find read against the text first:
  Myszakówek marked absent (the entry says it is not on the map), the stray
  "Stara Huta" item of Huta Łukomska removed, Imielno's *Dezerta Iemielno*
  supplied, Stawisko's *Brod Kaliski* noted as the crossing west of it
  (`maps/lukom1766/notes.md`).
- **The procedure recorded** for the next maps: `docs/ADDING_A_MAP.md`
  (what the editor does, what Claude runs, the traps).
- **The editor's first marks imported** (ten labels, among them Myszaków,
  which they added). At their word two readings corrected, read on the
  image: *Lomaw* (no Ł) and *Dezerta Jemielno* (a J), in the labels, the
  map forms and the entries' text. The inscription *Tres mansi Conventûs
  Landensis* they pointed out added as a label (the abbey of Ląd's three
  mansi, the purchase of 1447/1461 in the Ląd copy-book; its place in the
  gazetteer asked in NEEDS_CONFIRMATION). Two-line names: a trace's return
  against the reading direction is a line break (or the key L), in the
  page and the crop (a Sonnet sub-agent, tested). The bands were left at
  the default and cut the tops of large lettering: the help says so, the
  keys step by 20; the editor widens them and the marks come in again.
- **The band stands on the baseline** (the editor: "I trace the baseline
  of words - therefore assume a bit of padding underneath to account for
  possible descenders, and then use the [] to increase proportionally from
  the top"): the band runs from `height` above the traced line to 35% of
  it below; the crop the same; default height 80 (a Sonnet sub-agent,
  tested; checked on Dezerta Jemielno at 120: whole and level).
- **Tres mansi Conventûs Landensis** recorded under Grądzeń as its second
  appearance on Łukom 1766, linked to the Ląd copy-book's documents of 1447
  and 1461, at the editor's word; label 025 now belongs to Grądzeń.
- **Padding at both ends** of a band and its crop (the editor's word; a
  Sonnet sub-agent).
- **The final marks on Łukom 1766** imported (the editor's bands, 100 to
  240 pixels): eleven labels, eleven crops whole and upright. The import
  fixed for a second run on the same map: it reuses the gazetteer item
  linked to a label and unlinks labels deleted since (it would have added
  a duplicate for every place).
- **The warp checked by the editor**: the map lands in the right place
  ("This map is very crudely drawn so it's not perfect"). Allmaps handles
  the level-0 static tiles, the pilot's open point.

## 2026-10-26 — The cemeteries: the section planned and built (branch `cemeteries`)

- **The editor's survey of the Evangelical cemeteries** of the
  Trąbczyn/Zagórów area and its neighbourhood brought in as a fourth
  section (`cemeteries/`, plan `docs/CEMETERIES_PLAN.md`): ten cemeteries
  visited on one visit in 2023 (the editor's word), each with its page in
  both languages — the survey's account of its condition kept as written,
  the headstones as a table (Name / Born / Died / Note), the readings kept
  as the survey has them, nothing tidied, the same table on both pages. No
  person entries behind the names (the editor's word). The asterisked
  numbers beside eight readings are genealogical identifiers for certain
  Zelmers/relations and are kept, in the note column's place and explained
  in one line under the table (the editor's ruling, the second batch of
  the day); the survey's figure references ("Fig. 25" and its neighbours)
  are left off the pages (the editor, the same day). About 200 rows: 5 at
  Łazińsk Pierwszy, 11 at Huta Łazińska, 81 at Michalinów Trąbczyński
  (two stones carrying two names, the survey's "&"), 20 at
  Wrąbczynkowskie Holendry, 62 at Orlina Duża, 10 at Anielewo, 2 at
  Friedrichsfeld, none read at Michalinów gm. Oleśnica, 3 at Stawiszyn,
  8 at Zbiersk Kolonia.
- **The Places page widened** to a general index of places (the editor's
  ruling; `docs/PLACES_PLAN.md`, section 7): tier 1 the places of the
  Trąbczyn/Zagórów area — the gazetteer's 112 places and the register's
  `area: trabczyn-zagorow` ones (the 27 the gazetteer registers, plus
  Słupca, Konin and Kalisz) — tier 2 the register's remaining 126. The
  estates in focus stand as the cards above, their metadata untouched; an
  estate's list item links its card, a place with its own page links it,
  the rest stand named with their anchors.
- **The places machinery widened**: `pipeline/places/place_pages.py` takes
  a gazetteer slug as well as an estate. `pipeline/cemeteries/
  cemetery_pages.py` is a step of `regenerate.py`, after the place pages;
  the checks in `verify_site.py` hold the Places page's index and the ten
  cemetery pages (both languages, the account and every row on the page,
  the list page's links, the place anchors).
- **The survey's second source named** (the editor): "Der evangelische
  Friedhof in Łazińsk Drugi", Arbeitsgemeinschaft Ostdeutscher
  Familienforscher (Jürgen Frantz, 31 July 2016), members-only — cited
  behind one reading of Huta Łazińska, not held
  (`docs/MISSING_SOURCES.md`). The five new gazetteer entries (Łazińsk
  Pierwszy and Łazińsk Drugi split from `lazinskie-oledry` at the
  editor's word, and Orlina Duża, Stawiszyn and Zbiersk Kolonia) are
  drafted in `scratch/gazetteer_drafts/` and wait on the editor's eye.

## 2026-10-26 - APP 53/21/0/-/Pyzdry Gr.115 added, translated and published (branch app5321pyzdrygr115)

- The holding built: the head of the table of the parish of Trąbczyn on
  page 543 of the Relationes [protocollon] of 1791-1792, the register of the
  grod court and office of Pyzdry (fond "Księgi sądu i urzędu grodzkiego w
  Pyzdrach"), from the editor's own transcription, given as a spreadsheet
  export and kept as `intake/table.csv` as received. One document, one page
  (`0543_a`, the editor's own trim of the photographed page), seven rows and
  a heading row: the village of Trąbczyn, the parsonage, Nowawieś, Osiny,
  Łazy, "Kuznia Maryantów" and "Hollendry Luzne Stare i nowe z Hutą", each
  with its hearths (dymy rolne) and the two figures the headings call "gara
  zyta" and "gara owcza".
- Only `543_trim.jpg` is used, the editor's word; the spread `542v-543.jpg`
  stays out, and only the table in the page's first half is transcribed.
- The one reading changed at the editor's word, given in chat while they
  were away from the PC: the heading's "Parofie" is "Parafie" (applied by
  the intake script's `--correct`, logged).
- The editor's rulings of the day: "Kuznia Maryantów" is the Marianton of
  the edition - Mariantów, where the Hohenlohe patrimonial court for
  Trąbczyn sat. `reference/places.yml` (`mariantow`) now also matches
  "Maryantów", which brings the Prussian table's "Maryantow."
  (agad1169011745, row 175, unmatched before) in as well; 4 hits in 3
  documents, each line read. The Trąbczyn figure (22, where the doubling of
  the other rows gives 42) stands as written, the editor to resolve it.
- A table with no column of entry numbers: `unitlib.table_of` crashed on
  one (StopIteration). Extended: where no row has a number in its first
  cell, the figure rows are the body and the rows above the first of them
  the head; in `render_table` the first cell belongs with the name and no
  row takes the total styling, judged over the whole table. Checked the way
  shared code is checked: the pristine and the new code over every existing
  table, parse and render page by page, outputs identical
  (`pipeline/review/verify_table_of_diff.py`, 12 table documents in 5 units). The
  first cut of the change got the polarity and the scope of the new flag
  wrong; the before-and-after check caught both.
- Translated in session (the English table, hand-written, the common words
  rendered, the names as written); summaries in both languages, written in
  session. The index extended:
  "Maryantów" (above), the comma-bounded "Łazy" of the table rows (the
  hearth-tax register's entry 180 comes in with it), and "Hollendry Luzne
  Stare i nowe" matched to both Olęder colony entries, as the visitation's
  "Olędry nowe i stare" already is.
- The editor's closing word of the day, in chat: "No spot sheet is
  necessary - use my transcription, which is correct." The figures stand as
  transcribed (the village's row 21, 22, 84), the "gara" headings stand as
  written, and no dated heading is carried - the document stays undated.
  The sheet built for the holding was removed from the branch unused and
  its server stopped. Open: only whether the Huta of the Hollendry row is a
  distinct place (NEEDS_CONFIRMATION).
- The glossary gate passes (0 candidates); the site verifies clean (628
  documents, text exact, tables checked cell by cell). The edition guide's
  counts corrected (forty-nine holdings) and the Poznań bullet extended,
  English and German; the era's blurb names the table. Published at the
  editor's word, 2026-10-26: merged to main with the Szetlewicz holding
  built in parallel (the edition 629 documents in 50 holdings) and pushed.
- Still open (NEEDS_CONFIRMATION): whether the Huta of the Hollendry row is
  a distinct place.

## 2026-10-26 - APP 53/968/0/-/782: Tropiczyner Holl. identified; published

- The editor ruled: "Tropiczyner Holl.", the contract's dateline, is the
  Olędry on Trąbczyn - the Trąbczyńskie Stare Olędry, the edition's
  canonical settlement (its later name Łazińsk). Recorded in
  reference/places.yml as a matched variant of trabczynskie-stare-oledry
  (it hits the one document only, counted before matching); the place of
  writing override carries the manuscript's form and the build shows the
  canonical name the pattern resolves to. The holding's page names the
  identification, both languages.
- No timeline event (the editor's word): the contract bears on the colony's
  school, not directly on the owner.
- Still open: "Borwiezer Holland"; whether the ruling covers the
  "Trąbczyner Holländ" spelling of oe1bu14526-17; "6 gl."; the glossary
  terms (NEEDS_CONFIRMATION).
- Published at the editor's word.

## 2026-10-25 - APP 53/968/0/-/782: the line division ruled

- The editor answered all 7 rows of the holding's spot sheet. Corrections
  applied to the transcription: term 9 breaks after "Ostern" and after
  "Wirt" (not after "Weinachten" and "einem"); term 10 breaks after "und";
  the closing sentence's third line runs "Mann fortzusetzen. Die Sontags
  Schule so wie" (no break after "Sontags"); the board's last line breaks
  before "wir" ("... zu erfüllen worauf / wir uns Eigen-händig
  Unter-schrieben.", hyphens as drafted); the foot of the second page,
  which the session had taken for a pencil inscription, is blank paper.
  The opening paragraph and term 3 confirmed as drafted. Re-imported,
  rebuilt, the site verified clean.
- Trap recorded (WORKING_NOTES): a hand row in `paragraph_decisions.csv`
  whose context carries a comma must have the field quoted, or
  `resolve_paragraphs.py` reads the context short of the comma and drops
  the row as "not found again" - the signature row was lost twice this way
  before the quoted form held.

## 2026-10-25 - APP 53/968/0/-/782 added and translated (branch app539680782)

- The holding built: the contract of 14 March 1820 between the village board
  of Tropiczyner Holland and the school teacher Samuel Adolph of Borwiezer
  Holland, one document on two photographed pages (the folder's title page
  left out at the editor's word). All scans paired.
- The editor's own transcription carried in whole, the lines laid out against
  the two images at the editor's word (their file was paragraph-level); the
  layout read in session with an OCR pass and a line-by-line read as
  witnesses; item 7 empty and item 9 opening "9te." ruled by the editor.
  Six places where the line division is not certain are on the spot sheet
  (`intake/spot_sheet1.py`).
- The line-end divisions join as they should: auszunehmen, stelten,
  Vocation (three decisions, all high confidence).
- Translated in session at the editor's word (no paid run for two pages;
  intake/translation/write_cache.py writes the cache), the check clean.
  Summaries written in both languages in session and claim-checked in
  session (intake/claim_check.yml): 18 statements, one corrected in the
  draft (the one-year term belongs to the board's contract).
- The holding's page written in both languages; the glossary gate passes
  (the single-document terms offered, not entered); rulings: doc_type
  contract, the date read from the dateline, place of writing empty (the
  identification of "Tropiczyner Holl." open), estates trabczyn; era
  `restitution` (proposed in the plan, the editor approved it).
- The edition guide's counts corrected (627 documents, 2,087 pages,
  forty-eight holdings) and the Poznań bullet extended, English and German.
- Open on the editor: the spot sheet; "6 gl." gulden or Groschen; the
  identifications of "Tropiczyner Holl." and "Borwiezer Holland"; glossary
  entries for the single-document terms; a timeline event and the era's
  story (TODO section 36).

## 2026-10-25 - The word of the Themen block ruled

- The editor ruled the doubtful word of 0030's Themen block "polnische"
  ("Verschlungen hat ihr der polnische Mund"). The transcription, the
  English and the holding's pages corrected; the check clean; rebuilt.

## 2026-10-25 - Published

- The editor said "Publish". Main was pushed after a local build and
  verify passed; the "Build and deploy" run succeeded. APP 53/968/0/-/545
  went live with it.

## 2026-10-25 - APP 53/968/0/-/545 added and translated (branch app539680545)

- The holding built: Albert Breyer's ten photographed research sheets on the
  Polonisation of German surnames in the gmina Zagórów, seven documents on
  ten pages (the folder photograph left out; 0034 carried as "(skipped)",
  shown but not transcribed, at the editor's word). All scans paired.
- The four list sheets read by the machine reader in bands and settled on
  the editor's spot sheet "Readings in Breyer's sheets 1" (30 of 31 rows
  answered 2026-10-25; two rows unanswered, recorded in the holding's
  notes). The prose sheets 0031-0033 are the editor's own transcription,
  kept as typed; their doubtful words recorded in
  `units/app539680545/intake/unresolved.md`.
- Translated in session (intake/translation/, write_cache.py); the check
  clean after it caught the page split of document 5, the edition's Wrocław
  for Breslau, and doubt marks the German does not carry.
- Summaries written in both languages in session
  (intake/write_summaries.py) and claim-checked in session
  (intake/claim_check.yml): 33 statements, two corrected in the draft (the
  "Gem. Zagórów" line, and where the schools lie).
- The holding's page written in both languages; check_unit_text clean after
  it caught four citations ordered so the years stood past the documents
  that carry them.
- Two shared repairs: the pipeline self-check had failed on main since the
  gazetteer merge (its place-name mapping now carries the file waiver), and
  a stale translation record of kuryerpolski1754075-001 (the item moved to
  the newspapers section) removed by publish_translations.py.
- The edition guide's counts corrected (626 documents, 2,021 pages) and the
  Poznań bullet extended, English and German.

## 2026-10-24 - Published

- The editor said "Publish". Main was pushed at 5830d718 after a local
  Jekyll build and `verify_site.py` passed (619 documents character-exact,
  46848 internal links resolve); the "Build and deploy" run succeeded.
- Went live with it: Kneifel (1937), the gazetteer import and the maps'
  first crops.
- The other items this section first named (Kraus, Werner, the Lidmanowski
  texts, Słowiński, the Zagórów place page, the newspaper items, Łukasiewicz,
  Mielewczyk) had already been live since 22 or 23 October, because every push
  of main deploys the site, though the docs still called them not published.

## 2026-10-26 - Published

- The editor said "Publish". Main was pushed after a local Jekyll build and
  `verify_site.py` passed (628 documents character-exact, 47329 internal
  links resolve); the "Build and deploy" run succeeded. APP 53/4/0/-/62
  went live with it.

## 2026-10-26 - APP 53/4/0/-/62 added (branch app534062)

- **The holding**: one entry, in Latin, at the foot of page 222 of the
  relation and citation book of the land court at Kalisz for 1726-1727
  (scan 231 of 349 of the archive's online unit, jednostka 980058): the
  report of the general royal messenger Sebastian Szetlewicz of Szetlewko
  (Szetlewek) that he carried a citation to the estate of Szetlew and left
  it on the table in the heated room, on the Thursday next past. The editor
  added it for the name: a Szetlewicz family lived at Szetlewek in the
  1720s. The editor's transcription kept as written; two rulings of the day
  applied ("Judicius" → "Judicio"; "Citti~" read as Citati, the tilde kept).
  Dated 1727, year only, supplied from the volume's title pending the
  editor's reading of the sitting's heading on the preceding pages; place of
  writing left empty for the same reason. doc_type `report` (the Konin
  vocabulary), language `la`, estates szetlew and szetlewek, era
  prusimski-boundary. Translated, summarised and claim-checked in session,
  no paid run; the checks clean after three rows resolved.
- **Szetlew and Szetlewek told apart for the first time**
  (`reference/places.yml`): szetlewek's pattern passes "Szetlew...o" and
  "Szetlewicz" over, and szetlew is matched in the exact form "Szetlewo"
  (the Kodeks editors' identification). Counted against the committed
  index: szetlewek keeps its 91 rows but one - the hearth-tax table's row
  "Szetlewo z Częś: Jaroszew:" (APP 53/64/0/-/Kalisz Tab.21) moves to
  szetlew, where it belongs - and szetlew gains 4 rows (ours; the table's;
  and the Kodeks's own gloss "Szetlewo" in the kdw entries of 1173 and 1261,
  newly matched). The matching ruling added to `literature/index.yml`
  beside the standing refusal of Breyer 1938's "Szetlewo" for szetlewek.
  Put to the editor.
- **A person**: Sebastian Szetlewicz, court messenger (`reference/people.yml`,
  `reference/people_bios.yml`; no life dates - documented 1727).
- **The era blurb's count corrected** (`reference/eras.yml`,
  prusimski-boundary): it said twenty-four holdings, but the era held
  twenty-two before this one - two fewer than the blurb claimed, with
  nothing in the docs recording why. It now says twenty-three, with the
  entry of 1727 named in both languages, and the count is the computed
  truth (units with the era, 2026-10-26).
- **Two shared repairs** in `pipeline/translate/translation_review.py`
  (WORKING_NOTES, "Traps in the tools"): the missing `unitlib` import (the
  script had never run with `--unit`), and the cleared key built from the
  row's `letter` where the checker clears by `pad`, so an OK ruling never
  took. The key now comes from the row's pad column.
- The edition guide's counts updated (628 documents, 2,088 pages; the
  Poznań clause extended and the Latin count corrected to a hundred and
  eight, both languages) and the translation count corrected with them
  (624 of the 628 have English; the sentence still said 614 of the 619,
  the figures of an earlier state of the edition). The guide's other two
  hand-kept figures corrected against the dataset the same sitting: 910
  marks of doubt (the page said 905) and eighteen undated documents (it
  said nine).
- **Szetlewicz is a surname, not a place name** (the editor, 2026-10-26):
  the session's claim that the name was "formed from the place" is dropped
  from the holding's page and the person entry's comment; the fact stands
  (a family of the name at Szetlewek in the 1720s). The place-matching
  change above was confirmed by the editor the same day. The German holding
  page (`about_de.md`), first written as a copy of the English, was written
  again in German before publication.

