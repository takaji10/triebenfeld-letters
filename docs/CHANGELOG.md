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
`/letters/oe1bu9454/48/`, with 318 stubs forwarding from the old flat addresses.
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

## Deliverables produced

`letters.csv` / `letters.json` (database), `von_Triebenfeld_Hohenlohe-Ingelfingen_chronological.txt`, `collation_48_302.md`, `transcription_error_profile.md`, `phase2b_transcription_audit.md`, `currency_normalisation_report.md`, `parsed_dates_review.csv`, `phase2_proper_noun_report.md`.
