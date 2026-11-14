# Changelog

Full history of decisions and corrections applied to the corpus, database, and reports. `NEEDS_CONFIRMATION.md` tracks only what's still open â€” this is the record of everything already settled.

---

## Phase 1 â€” Structural cleanup

- Letter boundaries tagged (`[LETTER N]`), gaps and duplicate/out-of-sequence numbers documented.
- Front matter separated from the letter corpus.
- Line-wrap hyphenation (`Â¬`) and existing `[?]` uncertainty markers preserved as-is throughout â€” never rejoined or removed.

## Phase 2 â€” Proper noun standardization

- Full Kurrentschrift confusion taxonomy established (b/v/w, ck/ch, minim n/u/m, doubled-letter, sz/cz/s, I/J, j/y) and applied across ~230 proper-noun tokens in several rounds, root-only with grammatical endings preserved throughout.
- Key resolved clusters: TrÄ…bczyn (confirmed real place, Konin district), KÃ¶ckritz, StÃ¤gemann, Falkenhausen, Kwilecki, Schlabrendorff, GrÃ¤venitz, Knobelsdorff, Hawich, Habickâ†’**Hawich**, Kopojno (confirmed real village), Kulm (distinct from Kolno), Sobottendorff, Rapacki, Eysenhardt, Cosmar (incl. `Casman`/`Casmus` merge from the opening letter), Metternich, Talleyrand, Scharnhorst, Ingelfingen.
- **Rule â‘£ full-list pass** (rare-token-vs-anchor similarity scan, 222 candidates reviewed individually): 147 tokens fixed; ~40 held back as genuine false positives â€” real, distinct people or common German words that only matched on letter-similarity (`Reinhardt`, `Zagorowski`, `Weidel`, and the words in the current `NEEDS_CONFIRMATION.md` list). `Prusimskische` kept throughout, per confirmation that Prusimska (daughter) and Prusimski (father) are different people.
- `Hohenlohn`/`Hohenlahn`/`Hohenlohnsche` â†’ `Hohenlohe`/`Hohenlohesche`, all instances (16 tokens) â€” corrected after initially (wrongly) treating `Hohenlohn` as an accepted period variant.
- `Hinrich`/`Heinrich` â†’ `Honrichs` where confirmed the same referent (3 tokens); letter 48's `Heinrich` (L3684) â†’ `Hawich` instead, after cross-checking against letter 302 (its twin) at the identical sentence position â€” both copies of that document now agree.
- `Plenck` â†’ `Glenck` (2 tokens).

## Phase 2b â€” Transcription audit (AI-transcription-aware)

Scoped as audit-first given the transcription was AI-produced, not human â€” see `transcription_error_profile.md` and `phase2b_transcription_audit.md` for full methodology.

- 23 narrow word-level fixes applied (mostly corrupted forms of `Durchlaucht`/`HochfÃ¼rstl`), each individually context-verified; 85 of 108 automated candidates rejected as real words or line-wrap artifacts.
- Financial figure L1625 (`14 g. 4 d.` â†’ `14 g. 11 d.`) â€” proven via the estate-revenue table's own arithmetic *and* its duplicate elsewhere in the corpus.

## Phase 3 â€” Database, chronology, currency

- **Currency normalized**: `/m` expanded to full numbers (125 tokens); Reichsthaler-family abbreviations â†’ `Rthl` (1,272 tokens); `d` resolved to `Rthl` where value â‰¥12 (131 tokens), left as Pfennig where â‰¤11 and following a Groschen figure (correct as transcribed); `#` â†’ `Ducaten` (19 tokens). See `currency_normalisation_report.md`.
  - **Bug found and fixed**: a regex character-class error meant `Rthl`/`d` resolution never recognized the "Maerz" spelling of MÃ¤rz, plus a separate gap for the "d. M." (this month) construction. 23 ordinal-day references (`5t`, `15t`, `28t`...) had been wrongly converted to currency amounts; all reverted, two of those lines' legitimate currency conversions re-applied after the revert.
  - The 12 originally-ambiguous `d` cases (Â§B) resolved by hand: 10 â†’ Reichsthaler, 1 â†’ Groschen, 1 (`2.d PreÅ¿ectio`) turned out not to be currency at all â€” a garbled rendering of *Podprefect*, corrected to `Pod Prefecta`; `6. d.` turned out to be a corrupted `64/m`, expanded to `64000`.
  - L9997/L10008 set to `2099 Rthl 4 d` (through two rounds of correction â€” a Groschen guess, then a literal `rt` per instruction, then standardized to `Rthl`).
- **Month convention settled**: `7br`=Sep, `8br`=Oct, `9br`=Nov, `Xbr`=Dec â€” verified externally and against the corpus's own internal date sequences (see `NEEDS_CONFIRMATION.md` history / prior turns for the proof).
- **Bundled letters split** into 20 new sub-letter records after reading each candidate in full (see the table format previously in `NEEDS_CONFIRMATION.md` Â§E â€” now folded in here):

  | Original | Split into | What they are |
  |---|---|---|
  | 31, 50 | *(not split)* | Both turned out to be single continuous documents â€” original flagging over-matched "von Triebenfeld" mentioned in running prose, not just signatures |
  | 72 | 72aâ€“72f (6) | Report to a third party; report to the Prince; Kreis-Rath Thiel's own enclosed letter; Brzechta's note in German (72d) and in **Polish** (72e, language-duplicate of 72d); a further report 3 months later |
  | 74 | 74aâ€“74e (5) | A bundle of **legal documents** (court petition, two Kammergericht citations, an Ober-Landes-Gericht citation, one personal note from Triebenfeld) â€” not correspondence, which is why it first looked like a false positive |
  | 118 | 118aâ€“118c (3) | Main letter (10 Feb 1804); postscript re: Countess Schlabrendorff (29 Mar 1804); a near-duplicate of that postscript (118c, `duplicate_of=118b`) â€” the same within-letter double-transcription pattern as 48/302, just shorter |
  | 179 | 179, 179a | Main letter; enclosure explicitly marked `179. a) Abschrift` **in the original source**, a 4-exhibit financial dossier |
  | 265 | 265a, 265b | Two unrelated petitions to two different recipients, 8 and 15 Jan 1815 |
  | 269 | 269, 269a | Main letter; enclosure explicitly marked `269 a)` **in the original source**, dated *before* the covering letter |

  Each sub-letter carries a `parent_letter` field. Database: **316 rows**, content-preservation verified lossless throughout every change in this changelog.
- **Dates**: 8 supplied, 6 inferred from bounding neighbours (basis recorded per-row), 4 corrected outliers (letters 109, 254, 186, 232 â€” misread years/dates), 1 from the letter-48 twin (letter 302). Letter 5 (27 Jan 1816) confirmed correct as originally parsed.
- **Collation (letters 48/302)**: `exmittirt` (not `committirt`) and `Verrechnungen` (not `Rechnung`) confirmed as the correct readings and applied to the synthesised reading text in `collation_48_302.md` â€” the corpus text of 48 and 302 themselves was left as transcribed throughout, since collation only ever proposed a *third*, separate reading. `Heinrich`/`Howich` â†’ confirmed `Hawich`, and (uniquely) this one *was* applied directly to the corpus, per explicit instruction.
- **Â§B rare-proper-noun spellings, manuscript-checked** â€” all 7 resolved:
  - `Lang` â†’ `KÃ¶nig` (letter 16, L855; letter 64, L5026) â€” both genuine transcription errors.
  - `Longrich` â†’ `Congress` (letter 280, L20229) â€” genuine transcription error.
  - `Aich` â†’ `Asch` (letter 109, L8633) â€” genuine transcription error.
  - `Choma` (letter 17, L914) â€” confirmed correct as transcribed: not a different person, but the first half of `Chomanowski`, split across a line-wrap onto L915 (`nowski...`). Left untouched, consistent with the existing policy of never rejoining line-wrapped words.
  - `Wedel` (letter 96, L7651) and `Hache` (letter 59, L4563) â€” both confirmed correct as transcribed, no change.
- **Â§B, second batch** â€” 3 more manuscript-checked:
  - `Reinhardt` (letter 75, L6346; letter 140, L10523) â€” confirmed correct as transcribed, both instances, no change.
  - `Weidel` â†’ `Wedel` (letter 77, L6471) â€” genuine transcription error; same person as the already-confirmed `Wedel` in letter 96.
  - `Zagorowski` â†’ `Zagorower GÃ¼ter` (letter 218, L15988) â€” genuine transcription error. Corpus-internal evidence was decisive: "Zagorower GÃ¼ter" is the recurring name for this estate, attested 90+ times elsewhere (vs. a single `Guts` in a compound and a single `GÃ¼ther` spelling-variant); `GÃ¼te` (kindness) doesn't fit at all. This is a two-word expansion, not a like-for-like root swap â€” word count rose by 1 as a result, checked and expected, not a content-preservation violation.

## Book cross-reference

The 2018 Seidel biography (`Friedrich Ludwig, FÃ¼rst zu Hohenlohe-Ingelfingen`) was confirmed as an active reference source for the project. It's sourced from the Hohenloher Zentralarchiv Neuenstein (HZAN) â€” almost certainly the same archive this correspondence was transcribed from â€” and its Appendix 6 is a scholarly transcription of the exact same 7 March 1809 Kontopp letter as the corpus's letter 48/302 pair, making it a genuine third witness for that letter specifically.

- **Investigated and closed**: whether `Hawich` and `Honrichs` had been wrongly merged. They hadn't â€” the two already co-occur as clearly distinct people dozens of times throughout the corpus, and the one place they were ever conflated (letter 48, L3684, a `Heinrich`â†’`Hawich` fix from an earlier round) is independently confirmed correct by Appendix 6's identical sentence.
- **Investigated and closed**: the book spells this recurring fraudulent-Sequestor figure `Henrichs`, raising the question of whether the corpus's ~100+ `Honrichs` instances (including the 3-token `Hinrich`/`Heinrich`â†’`Honrichs` normalization at letters 43/179/284) were systematically wrong. Confirmed `Honrichs` is correct â€” the book's `Henrichs` is the biography author's own editorial spelling choice, not an authoritative period rendering. General takeaway: the book's proper-noun spellings are not treated as authoritative over the corpus's own internal evidence, particularly for Polish place names (flagged by the user in advance) but evidently for German names too.
- **No corpus edits resulted.** `Honrichs` and `Hawich` both stand as already fixed.
- Â§A (`23000`/`32000` Rthl) is independently corroborated by Appendix 6's `23000 Rth` reading (matching letter 48) but this is **not** being used to resolve it â€” the user is checking the original manuscripts directly for that one.
- Broader book integration (who's-who index, estate/property cross-reference, chapter-to-letter-date map) declined for now; revisit later if wanted.

## Liquidation register added (letter 303)

`Auszug aus Den FÃ¼rstlich Hohenloheschen Liquidations Protocollen.xlsx - Edit.csv` â€” a 142-entry creditor register (undated) â€” was added to the project and integrated so it's searchable alongside the letters.

- **Names standardized** against already-decided project canon (established fixes only, nothing new invented for this document): `Bornstaedt`â†’`BornstÃ¤dt`; `Stoessel`â†’`StÃ¶ssel` (Ã—2, plus the adjectival `Stoesselschen`â†’`StÃ¶sselschen`); `Koekritzschen`â†’`KÃ¶ckritzschen`; `Schlabendorffschen`â†’`Schlabrendorffschen`. Everything else in the register â€” the large majority of the 142 names â€” has no established form in this project (they don't otherwise appear in the letters), so was left exactly as transcribed; existing `[?]` uncertainty markers (2, on rows 5 and 62) preserved as-is.
- **Added to the corpus** as `[LETTER 303]`, appended at the end of the archival text file, each row rendered as one line (`N. Name â€” Gold X Rthl Y g Z d; Courant X Rthl Y g Z d`), using the same `Rthl`/`g`/`d` units already standard throughout the letters. The Gold/Courant distinction (two different period Reichsthaler denominations) is preserved exactly as given, not collapsed into one figure. Append-only edit â€” nothing in the existing corpus was touched; word count and line count both grew by exactly the amount added.
- **Added to the database** as record 303 (317 total now), with a new `doc_type` column (`letter` for all prior records, `register` for this one) so it's distinguishable in queries. No date in the source â€” `date_precision=unknown`, `date_source=none`, same convention as the 5 undated/missing letters, sorts to the end of the chronological reading copy.
- Content-preservation and chronological-ordering checks re-verified after the addition (317 records, archival/chronological content line sets identical).

## Who's-who reference

`whos_who.md` added â€” every person named in the letters (and the letter 303 register), cross-referenced against the biography for identity where possible. Each entry is labeled by evidence type: externally confirmed (real, independently documented historical figures, from Phase 2's Tier 1/2 research), book-confirmed (matched to the Seidel biography), context-inferred (a role guessed from how the letters/register describe the person, always flagged as uncertain rather than stated as fact), or role unclear. People who appear only in the book, not in the letters, are excluded per instruction. ~65 people individually profiled; the register's remaining ~134 one-off creditors listed using their own stated professions only, no further research.

Two things worth follow-up, both left open rather than resolved:
- **Possible family link**: the book's Ch. 2.3 concerns "Marianne GrÃ¤fin von Hoym," the Prince's own wife's birth family. The letters separately discuss a "Minister/Graf Hoym" (8 occurrences) and the register lists a "Fr. GrÃ¤fin HÃ¶ym, geb. v Tauenzien" as a creditor â€” surname, era, and rank line up, but the letters never state the connection explicitly.
- **Unresolved identity**: `Wedel` (letters 77/96/98) sits next to "Hoyms und Wedells" in letter 98, suggestive of a real contemporary Prussian official (Karl von Wedell), but not confirmed â€” the book's one `Wedel` hit is in an unrelated chapter.

## Who's-who update â€” Prusimska/DÄ…bska identity confirmed

User-provided identification: **Michalina Prusimska**, daughter of Antoni Prusimski (original owner of the TrÄ…bczyn estates), later married and became **DÄ…mbska/DÄ…bska**. This directly matches text already in the corpus â€” L1858 (letter 28, 1807-10-05): "der Frau v DÄ…bska gebohrnen v Pru[simska]" ("nÃ©e Prusimska") â€” and resolves what the who's-who had flagged only as an unconfirmed family link.

Checking the dates of every Prusimska/DÄ…bska mention surfaced a further pattern: `DÄ…bska` is used consistently 1807â€“1811, then from late 1814 the letters instead use `Moscinska` / describe her husband as a MoszyÅ„ski, with letter 266 (Jan 1815) hedging "DÄ…bska oder Moscinska" â€” exactly the line Phase 2 had flagged as possibly reflecting genuine period uncertainty rather than a transcription error. This chronology-based hypothesis of a second marriage was flagged to the user and **confirmed**: her second husband's real surname was **MiÄ…czyÅ„ski**, not "Moscinski"/"Moszynski" as the letters render it â€” an error made by the original letter-writers themselves, not the AI transcription. Per project policy (only transcription errors get corrected, not period scribal/writer errors), the corpus text is left exactly as written; the correct identification is recorded in `whos_who.md` instead. No corpus text was changed â€” `Prusimska`, `DÄ…bska`, and `Moscinska` are genuinely different words the original writers used for the same person at different points in her life, not transcription variants of one name.

## Web edition â€” Phase A (foundation)

A Jekyll site in `site/`, built to deploy to GitHub Pages with no custom plugins (Pages runs Jekyll in safe mode, which ignores them). Everything dynamic is either pre-generated by Python or done client-side in dependency-free JavaScript â€” no CDN, no external requests, so the site behaves identically offline and deployed.

- **`build_site_data.py`** (new) generates all 317 letter pages, `_data/people.yml`/`places.yml`/`stats.yml`, and the client-side search index from `letters.json`. Rerunnable; the corpus is never touched. It **asserts character-exact fidelity** and refuses to finish if any page's text differs from the corpus.
- **`verify_site.py`** (new) checks the *built* site: every record has a page, every page's diplomatic text matches the corpus exactly, every internal link resolves, and no page references an external host. Currently: 317/317 exact, 6,201 links resolve, 0 external dependencies.
- **Two text views per document.** *Diplomatic* is canonical and default â€” original line breaks, `Â¬` marks and `[?]` flags all intact. *Reading* flows lines into paragraphs; it is generated for legibility only and never stored as truth.
  - The reading view joins a broken word only where evidence is unambiguous: at `Â¬`, and at a word-attached hyphen whose continuation starts lower case. Line-final hyphens followed by a capital were checked against the corpus and turned out to be genuinely mixed â€” real compounds (`Haupt-`+`Ersaz`) alongside the writer's habitual punctuation dash â€” so they are left exactly as written rather than silently merged.
- **Faceted browse** with instant client-side filtering (year, person, place, condition, date certainty) and full-text search that is diacritic- and long-s-insensitive, so `Trabczyn` finds `TrÄ…bczyn`.
- **Timeline** combining letter-density per year, historical events from the biography's Zeittafel and chapters (each with its citation), and the six narrative movements. Events live in `_data/timeline.yml` for easy extension.
- **People and Places indexes** generated from the corpus, with per-person occurrence counts and links to every appearance.
- **"About this edition"** page documenting the AI-transcription provenance, every editorial mark, the four ways documents are dated, the currency system, the bundled/duplicate documents, and what remains unresolved.
- **Translation scaffolding** in place: the letter layout renders `_data/translations/*.yml` with a status badge when present, and says plainly that a document is untranslated when not. Nothing about translation touches the canonical corpus.
- **`.gitignore`** added at the project root that excludes the copyrighted Seidel biography from any future repository, alongside build output and backups.

Bug caught during verification and fixed at source: Liquid treats the empty string as *truthy*, so empty metadata fields were rendering "part of letter", "duplicate of letter â£", and a false `[supplied]` badge on every page. The generator now emits real YAML nulls for absent values.

Still to come: theme tagging pass with review report (Phase B), translations (Phase C), publication (Phase D â€” gated on the archive-permissions question).

## Line-break resolution and the page-based three-view edition

The transcription's word-continuation marks turned out to be unreliable, which blocked any readable text. Of the **1,314** line-end marks in the corpus, **484 (37%) join nothing** â€” `dieÂ¬`+`serhalb` really is *dieserhalb*, but `dieÂ¬`+`nÃ¶thigsten` is two words and the mark is simply an error.

- **Every mark decided on evidence**, not assumption (`resolve_linebreaks.py`). Two sources: this corpus itself (which knows period spelling), and the **DWDS frequency API** â€” lemma-aware, so inflected forms resolve (`Mitgliedern` â†’ *Mitglied*, 12.0M hits), and covering historical German. A modern offline dictionary was rejected as unfit: it misjudges `laÃŸen`, `nÃ¶thigsten` and the long-s forms. Threshold for "real word" set at 1,000 corpus hits, chosen from the observed gap between real words (thousands to millions) and proper-name noise (`denich` 414, `derdurch` 41). Lookups cached to `dwds_cache.json`, so re-runs are free and offline.
- **Result: 825 joins, 484 non-joins, 5 catchwords, 19 flagged** for checking against the originals â€” down from 527 unresolved when corpus evidence alone was used.
- **Catchwords discovered.** Five pages end with the scribal habit of writing the next page's first word at the foot of the current one (133 `ConÂ¬`â†’`Contract`, 140 `Vor-`â†’`Vorwerk`, 168 `WinÂ¬`â†’`Winnickischen`, 177 `beÂ¬`â†’`benennung`, 235 `ver-`â†’`verliehren`). Joining these would manufacture "ConContract". They stay in the diplomatic view and are dropped from the reading copy.
- **Two possible lacunae found** while reading the cross-page cases: letter 223 has `GÃ¼ter angeÂ¬` never completed, and `entweder verÂ¬ / oder aufgegeben` missing its word â€” both recorded in `linebreak_report.md`. Letter 136's `ColloÂ¬`+`Mitten` is almost certainly a mis-transcribed *Collonisten*.
- **`linebreak_decisions.csv`** â€” one row per wrap with the full evidence, **hand-editable**. Change a `decision` cell and regenerate; nothing is buried in code.

**Structure: letters are now made of pages.** The corpus's blank lines (page breaks preserved back in Phase 1) yield **913 manuscript pages**. The letter remains the unit of navigation, citation and search â€” pages are structure inside it, so text always stays beside the right scan when images are added. Each page carries a `scan` slot, empty for now, so adding images later is a data change rather than a re-architecture.

- **Three views** on the site: *Diplomatic* (one line per manuscript line, numbered to the archival file, marks intact â€” canonical), *Reading* (wraps resolved, lines flowed, never the text of record), *English* (per page, empty until translated).
- **New artefacts**: `von_Triebenfeld_..._reading.txt` (generated fair copy, every page labelled with its archival line range), `pages.csv` (one row per manuscript page, ready for scan matching), plus `text_reading`/`pages`/`n_pages` in the database.
- **`build_db.py` moved out of the temporary session scratchpad into the project**, so the whole pipeline is durable and self-contained.

The archival text was **not touched**. Verification enforces it: pages must reconstruct each letter, the reading copy must contain the same letters in the same order (catchword pages excepted by design), and every built page must reproduce its archival lines character-for-character. All pass â€” 317 letters, 913 pages, 6,201 internal links, zero external fetches.

## Matching scans to transcribed pages

`pages/` holds 874 curated JPEGs (1.08 GB) against 913 transcribed pages â€” a 39-page shortfall to explain.

- **The gap is not missing scans.** Blank images (blank versos, unused spread halves) were deliberately deleted before this work, so 146 captures have a pruned counterpart â€” expected, and documented rather than flagged as damage. But pruning cannot cost a transcript page: a blank page was never transcribed. The real cause is **over-segmentation of the transcript**.
- **38 short blocks are almost certainly not page breaks** â€” against a shortfall of 39, which essentially closes it. They are datelines (19), signature blocks (7), salutations (4) and other very short fragments (8) that the transcriber set off with a blank line; Phase 1 read every blank line as a page break and turned each into its own "page". Examples: `Wien d. 6ten May 1815.`, `treu unterthÃ¤nigsten Diener v Triebenfeld`, `GnÃ¤digster FÃ¼rst und Herr!`. **The fix belongs in the corpus** (remove the blank line), not in the mapping.
- **`match_scans.py`** aligns captures to letters by dynamic programming, minimising per-letter page-count mismatch while preserving order and treating each capture as atomic. Result: 856 pages matched, 57 gaps, 18 surplus images, all 874 images assigned, none twice, capture order strictly increasing.
- **`scan_inventory.md`** â€” capture composition, the pruning record, the 38 not-a-page-break candidates with their blank-line positions, and the per-letter excess list.
- **`page_scan_map.csv`** â€” one row per transcript page with its proposed image; hand-editable, and the file the pipeline will read.
- **`scan_review.html`** â€” a standalone reviewer opened by double-clicking. Shows each page's text beside its proposed image, referencing `pages/` **in place** so the 1.08 GB is never duplicated. Four actions per row (confirm / no image / drop image / merge into previous), corrections re-flow the alignment live, state persists in the browser, and "Copy as CSV" round-trips back into the map. The 38 suspects are highlighted, and merges are collected separately because they are corpus fixes rather than mapping fixes.

- **Anchoring** added to the reviewer: type the letter an image actually belongs to, and it pins that image to that letter's first page while everything downstream re-flows to follow. This makes the corpus fixable by jumping to any point, stating one known fact, and letting the sequence fall into place â€” rather than clicking through 900 rows in order. Anchors are keyed by filename so they survive re-alignment, and the reviewer reports the two failure modes: an anchor that would reuse already-assigned images (flagged as a conflict) and one that strands images (visible in the leftover counter). Verified against the generated file with Node: JS parses, anchoring shifts downstream letters as intended, and both failure modes are caught.

- **Front matter (`0`)** â€” entering `0` marks an image as belonging to no letter at all (the series title page). It leaves the sequence entirely, so everything after shifts up by one, and it is held in a panel with thumbnails and a *Put back* button rather than being discarded. Exported with status `front_matter`.
- **Proposing new letters** â€” typing an ID the corpus doesn't have (e.g. `1a`, when the scans show transcript letter 1 is really two documents) records it as a **proposal** rather than an anchor, because the corpus has no pages for it until the text is split. Proposals collect in their own panel showing which existing letter and page the image currently sits in, and export with status `starts_new_letter` plus a `new_letter` column. A new sub-lettered ID whose base number doesn't exist (a likely typo, e.g. `9999a`) prompts for confirmation instead of being silently accepted.

**Sequencing note for the splits:** applying a proposal means inserting a `[LETTER 1a]` tag at the right line of the archival text. Everything downstream then re-derives itself â€” `build_db.py` re-splits pages on blank lines, re-parses the date from the letter's own text, and assigns `parent_letter` from the ID, exactly as it already does for the 72aâ€“72f and 179/179a splits. No separate date entry is needed unless the parser gets it wrong.

Letter 9 (missing in the archive) and letter 303 (the register, from a different source) are correctly excluded from matching rather than forced onto images. Nothing in the corpus, database or `pages/` was modified.

Still to come: apply confirmed merges to the corpus, then fill the `scan` slot in `build_db.py` and generate web-sized derivatives (~130 MB) for publication.

## Scan review applied to the corpus

The visual review of all 872 images against the transcript produced its first round of corrections, now applied. The archival text was edited only by adding four letter tags and removing four blank lines â€” **no letter text changed**, verified by comparing the 20,756 non-tag content lines before and after (byte-identical).

**Two letters split** â€” the scans showed one archival number holding two documents. Boundaries verified individually: each follows a dateline or signature and opens with a fresh salutation.

| New letter | Split from | Evidence |
|---|---|---|
| **1a** | letter 1, at line 67 | previous ends *"Schlawenschitz den 29ten Januar 1815"*; new opens *"Durchlauchtigster FÃ¼rst"*. Dateline *"Wien d. 12. in Febr. 1815"* â€” the parser caught month and year but not the day, so **12 Feb 1815** is supplied. |
| **72 / 72a** | old 72a was two documents | pages 1â€“4 address the *Kriegs- und Forstrath* (now letter **72**); pages 5â€“8 open *"Durchlauchtigster FÃ¼rst"* (now **72a**). The bare number 72 finally has a record, so the sub-letters' parent link resolves. |

Two further splits were made and then **reverted at your instruction**: `13a` (letter 13 stays whole) and `20a` (letter 20 stays whole, its enclosed *Abschrift* to the banker van der Lahr remaining part of the letter). Removing the tags restored both letters exactly â€” the blank lines that had preceded the tags went back to being ordinary page breaks, and the letter text was never touched.

**Four page merges applied** â€” blank lines that were separating a dateline or signature from its own page, not marking a page break: letters 146, 237, 254 (merge into previous) and 303 (the register's title line, merge into next).

**Findings recorded rather than silently absorbed** â€” see `NEEDS_CONFIRMATION.md` Â§Eâ€“Â§H: 9 scanned pages with no transcribed text (including four consecutive sheets, captures 0543â€“0546, at the very end of the BÃ¼schel), 1 transcribed page with no scan (letter 231 page 2), 6 images excluded as front matter or not-pages, and a mis-transcribed year in letter 237 (`1873` for 1813).

Result: **318 documents, 862 pages, 872 images.** All verifications pass â€” pages reconstruct their letters, reading copy lossless, every archival line character-exact on the site, 6,214 links resolve.

## Scan mapping completed

The image-level review decisions were moved out of browser storage and into **`scan_decisions.json`**, which `match_scans.py` now reads. They therefore survive every regeneration, and the reviewer opens on the corrected state instead of resetting to naive folder order.

Recorded: 1 front-matter image (`0001_a`, the series title page), 5 images that are not manuscript pages, 1 image left untranscribed on purpose (`0345_a2` â€” a list of calculation figures only, **not** a missing page; the reason is stored in the file's `notes` so it can't later be mistaken for a gap to fill), and a corrected reading order â€” `0345_a2` before `0344_a1`, where a spread's halves had been photographed across two captures.

**The mapping is now complete and fully accounted for:**

| | |
|---|---|
| Images | 872 |
| Paired to a transcript page | 865 |
| Set aside with a stated reason | 7 |
| Unexplained surplus | **0** |
| Pages with no image | 4 â€” letters 121, 181, 225, 293, the archive's own missing numbers |

Splitting letter 303 into 9 pages resolved the long-standing tail surplus: the trailing captures 0543â€“0546 turned out to be the register's own pages, not untranscribed documents. `NEEDS_CONFIRMATION.md` Â§E and Â§F have been narrowed accordingly.

Two markers in the export were **deliberately not applied** â€” the proposed splits `13a` and `20a`, which had been made and then reverted at your instruction. Anchors persist in the browser by filename, so they re-exported; re-applying them would have silently undone the reversion.

Verification was tightened rather than relaxed to accommodate the custom order: the mapping is now checked against the *intended* sequence (folder order, or the corrected order when one is recorded), with front matter, drops and no-text images excluded from that check since they sit outside the sequence by design.

## Letter 237's year corrected

The dateline had been transcribed `d. 29ten April 1873` â€” impossible, and previously worked around with a supplied date of 29 April 1813. You corrected the digit in the archival text, so **the supplied-date override was removed**: the parser now reads 1813 from the manuscript itself (`date_source: signature` rather than `supplied`). One fewer manual override masking what the text actually says.

`NEEDS_CONFIRMATION.md` was then trimmed to the three genuinely outstanding items â€” the 23,000/32,000 discrepancy, the 224 uncertainty markers, and the 5 damaged blocks â€” with the resolved sections folded into this changelog. Two of the three are now far more tractable than before: since every page has a matching scan, checking an uncertain reading or a damaged block is a matter of looking at the image rather than hunting for it.

## Scans wired into the edition

**Images renamed** to be ASCII and self-describing, so URLs no longer carry an encoded `Ã¼` and spaces:

```
Oe 1_BÃ¼ 9454_0343_a1.jpg   ->   Oe_1_Bu_9454_0343_a1-L179a_04.jpg
```

`<signature>_<capture>_<crop><half>-<label>`, where the label is `L{letter}_{page}` for a mapped page, or `front` / `notext` / `notapage` for the seven set aside. The capture and crop still carry the archival identity, so nothing is lost, and **`scan_rename_map.json` records every original name** â€” the rename is fully reversible. All 872 renamed in one pass via temporary names so a rename could never clobber an existing file; zero collisions.

**Web derivatives** â€” `make_scan_derivatives.py` produces 1100px copies into `site/assets/scans/`: **231 MB**, against 1.08 GB of originals, generated in under a minute. 1100px was chosen after measuring three widths; it reads Kurrentschrift comfortably and sits well inside the GitHub Pages limit. Re-running skips anything already current. **`pages/` is now gitignored** â€” the full-resolution originals stay local as archival masters and are never published.

**Two panes per manuscript page** â€” the scan on the left, its own text on the right, so image and transcription sit together rather than being toggled between. The image stays in view while its page's text scrolls. Tabs now switch only the text (Diplomatic / Reading / English), and a *hide scans* checkbox gives the text full width for straight reading. Both preferences persist between letters.

**The reviewed pairing is now the source of truth.** The mapping had been *recomputed* on every run by pairing pages and images sequentially â€” so it kept drifting away from what had actually been checked by eye. That was the wrong architecture: a pairing established by looking at the scans is evidence, not something to re-derive. `scan_decisions.json` now holds `pairs` (865 pageâ†’image assignments) and `gaps` (4 pages confirmed to have no scan), taken from the review and applied verbatim. Only pages the review doesn't cover fall back to sequential fill.

This came out of a real misalignment: letter 48's second page was showing the wrong scan. The cause was a rule I had added that **assumed** archival numbers recorded as missing could have no scan, so numbers 9, 121, 181, 225 and 293 were made to take no image. Four of those were right â€” but **letter 9 does have a physical page behind it**, as the review recorded, and skipping it shifted every pairing after it by one. An assumption about the archive was overriding an observation of it.

**Letter 303 was also still flagged as "not part of this BÃ¼schel."** The scans disprove it: the trailing captures are the register's own pages. It now takes images like any other document, and all nine of its pages have one.

**Filename labels made self-maintaining.** The `-L<letter>_<page>` part of each filename is *derived* from the mapping, so fixing those two bugs left 846 of 864 labels stale and actively misleading. `relabel_scans.py` recomputes them from `page_scan_map.csv`, renames via temporary names, and carries `scan_decisions.json` and `scan_rename_map.json` across. It runs in report-only mode at the end of every `regenerate.py`, so drift is caught rather than discovered later; renaming stays a deliberate `--apply`.

Verification extended, and now includes the check that matters most: **every built page is compared against the reviewed pairing**. Currently 865 paired images, **0 of 865 disagreeing with the review**, zero label disagreements, zero missing files, 7,943 links resolving, archival text character-exact.

## The transcription layer replaces the diplomatic view

The first view is now **Transcription**, not Diplomatic: the manuscript's own line breaks are kept, but the line-end marks are resolved. Where a word really is broken it carries a plain hyphen (`abge-` / `nommen`); where the mark was spurious it is gone. The rename matters â€” a corrected text should not be called diplomatic â€” and `About the edition` now sets out what has been changed and why.

The archival text is untouched and still canonical. A build-time check enforces the relationship: the transcription may differ from it **only on lines carrying a recorded decision, and only in the line-end mark, never in a word**. Anything else fails the build.

**Three orphan marks found** while adding that check â€” `Â¬` on a line whose next line holds only figures, so there is nothing to continue into (two are table rows, one a dateline). They had fallen through the wrap collector entirely and had no decision at all. They are now a category of their own, `orphan`, and the mark is removed.

**A verification bug of my own, caught and fixed.** The new check used variable names `a` and `b`, shadowing the outer variables holding the archival-vs-chronological comparison. That silently reduced a 20,750-line check to a 13-line one comparing a page against itself, and reported "identical content: True" on the strength of it. Renamed, and the real check restored.

## Spelling audit â€” report only, nothing applied

`spelling_audit.py` looks for demonstrable transcription slips in ordinary words. The bar is deliberately high, because **63% of the distinct words here appear exactly once** and the text is full of correct period forms (*laÃŸen*, *seyn*, *nÃ¶thig*, *Ewr*). A candidate must be rare here, have a near neighbour at least 10Ã— more common, differ by a confusion this transcription is known to make, and be unknown to DWDS while its neighbour is attested.

Getting to a usable list took three passes, and the discards are worth recording:

- **1,131 candidates** at first â€” mostly junk. Any four-letter word is one edit from *und*, *die*, *der*, so `dire` (French), `Rich.` (an abbreviation) and `Diet` (a surname) were all "corrections".
- **Tightened** to a six-letter minimum, eight for dropped/added letters â†’ 335, but now dominated by **German inflection**: `FÃ¼rstens` (genitive) and `hochfÃ¼rstlicher` (dative) are correct, not errors. Differences confined to a final *e/n/r/s/m* are now excluded as grammar.
- **Checked each survivor against DWDS** â†’ any rare form that is itself a real German word was dropped: *Kasten* is a box, *erkalten* is to grow cold.
- **Two faults in my own word extraction**, each inventing errors: a stray diacritic split `ÅŸondern` into `ondern` (proposed as a slip for *andern*), and line-wrap fragments were counted as words (`Nachrich-` proposed as a slip for *Nachricht*).

**106 candidates** remain, and the strong ones are unambiguous â€” `Durchaucht` â†’ *Durchlaucht*, `GrÃ¤digster` â†’ *GnÃ¤digster*, `Schreibn` â†’ *Schreiben*, `erÅ¿terebe` â†’ *ersterbe*, `GeÅ¿ehichte` â†’ *Geschichte*. Some still need your judgement: `Antworth` may simply be period spelling. See `spelling_audit.md`; nothing applied at this stage â€” the accept/reject pass is the next section.

## Spelling audit â€” applied

The 106 candidates from the report above were read one by one against the manuscript context. **66 accepted, 40 kept.** The 66 touch 72 token instances (six forms â€” `Triebenfeldt`, `Schreibn`, `FÃ¼rstern`, `gestandt`, `umsamehr`, `Liefster` â€” occur twice). Applied root-only to `von_Triebenfeld_Hohenlohe-Ingelfingen_cleaned.txt`, one pinned `(line, whole-word old â†’ new)` at a time, backup at `von_Triebenfeld_Hohenlohe-Ingelfingen_cleaned.txt.bak5`, then `regenerate.py`: transcription still differs from the archival text only on decided line-end marks, reading copy lossless, 20,750 archival lines = 20,750 chronological lines, every built site page character-exact.

What went in: corrupted honorifics and formulae (`Durchaucht`â†’*Durchlaucht*, `GrÃ¤digster`â†’*GnÃ¤digster*, `Durchlauchtigter`â†’*Durchlauchtigster*, `Liefster`â†’*Tiefster* Ã—2, `erÅ¿terebe`â†’*ersterbe*); place and person names against project canon (`Schlawerschitz`/`Schlawentschitz`/`Schlowenschitz`â†’*Schlawenschitz*, `WorÅ¿chau`/`Warschan`â†’*Warschau*, `Triebenfeldt`â†’*Triebenfeld* Ã—2, `Brzechsa`/`Berzechsta`/`Brezechsta`â†’*Brzechsta*, `Zagorowa`â†’*Zagorowo*, `Zerbani`â†’*Zerboni*, `Palajewo`â†’*Polajewo*, `KÃ¶nigberg`â†’*KÃ¶nigsberg*, `Scherck`â†’*Schenck*); the recurring excrescent-*r* cluster (`FÃ¼rstern`/`tiefstern`/`hÃ¶chstern`/`Sonstern`/`BemÃ¼hern`/`einreichern` â†’ *-en*); single visual confusions producing non-words (`Å¿erden`â†’*senden*, `wÃ¼nden`â†’*wÃ¼rden*, `lÃ¤glich`â†’*tÃ¤glich*, `NuÃŸland`â†’*RuÃŸland*, `geweldet`â†’*gemeldet*, `geÅ¿chieben`â†’*geschrieben*, `GeÅ¿chiehte`/`GeÅ¿ehichte`â†’*Geschichte*, `Augenblik`â†’*Augenblick*, `glÃ¼klich`â†’*glÃ¼cklich*, `dardurch`â†’*dadurch*, `wordurch`â†’*wodurch*, `bestehnt`/`bestreht`â†’*besteht*, `getrettet`â†’*gerettet*, `gesanndt`/`gestandt`â†’*gesandt*, `Sequestation`/`Sequetration`â†’*Sequestration*, `Hypoteque`â†’*Hypotheque*, `WechÅ¿tel`â†’*Wechsel*, `Intresen`â†’*Intressen*, `Expresen`â†’*Expressen*, `Comision`â†’*Commission*, `Revenuce`â†’*Revenue*, `Triebunal`â†’*Tribunal*, `Mandatorius`â†’*Mandatarius*, `Cuhrischen`â†’*Curischen*, `Hoffroth`â†’*Hofrath*, `Geheimte`â†’*Geheime*, `konzler`â†’*kanzler*, `durchlaus`â†’*durchaus*, `Scharden`â†’*Schaden*, `Å¿ehleunig`â†’*schleunig*, `angewiÅ¿en`â†’*angewiesen*, `umsamehr`â†’*umsomehr* Ã—2, `Antworth`â†’*Antwort*, `vorgesten`â†’*vorgestern*). `gnÃ¤digter` at L263 had two proposed corrections in the report (`gnÃ¤digster` / `gnÃ¤diger`); the set salutation `gnÃ¤digster FÃ¼rst und Herr` was applied.

What was kept (full table with reasons in `spelling_audit.md`): valid period forms the automated inflection filter missed â€” `hiedurch`, `geschiehet`, `kleinern`, `urtheilt` (a finite verb), the `-ff`/`-fft` orthography (`verkauff(en)`, `zukunfft`, `dÃ¼rfften`, `geworffen`, `herrschafft`), `gezahlet`, `gebetten`, `hochwolgeb` (`wol`), `creditorn` (syncope, parallel to `andern` in the same clause); cases where the report's proposed target is wrong or ambiguous â€” `vesten` = *Vestungen*/*Festungen* not *besten*, `durcht` = *deucht*/*dÃ¼nkt mir*, `wenschen` = *WÃ¼nschen* at L36 but *Menschen* at L47, `gewinnten` = *gemeinten*, `klogen` = a place name, `desten` = *dessen*, `commer` = *Cammer* or a surname, `unglÃ¼ckt` â†’ *unglÃ¼ckliche*; line-wrap fragments â€” `geleiste` (+ `ten`) = *geleisteten*, `hochfÃ¼rst` (+ `laucht`) = *HochfÃ¼rstl. Durchlaucht*; a source dittography (`vorgestern vorgesteren`, L73); and several readings the surrounding text is too garbled to settle (`gnÃ¤digte`, `gewiÃŸert`, `weines`, `wohren`, `kurgen`, `eingericht`, `gesundtheit`, `ewodurch`). The two address-honorific variants `hochwohlgebohrnen`/`hochwohlgebohrn` were left as possibly deliberate.

## Name catalogue â€” built, adjudicated, first batch applied

`name_catalogue.py` (new) catalogues every person and place name and its variant
spellings. Names defeat the spelling audit's assumptions â€” 527 of the 738 tokens in name position occur exactly once, so frequency proves nothing; a wrong name still looks like a name; and plain edit distance is the wrong metric (`KÃ¶ckritz`/`Koekritzsch` are four edits but one misreading apart, `Wien`/`Bier` one edit apart and unrelated). So it seeds from the settled canon in `whos_who.md` and `CHANGELOG.md`, strips German derivational morphology before comparing (`Cosmarischen`, `Zagorower` are inflections, not rival spellings), and matches with a Kurrent-weighted distance scaled to name length. Output: **267 names, 206 proposed variants, 21 one-entity-or-two decisions, 18 withheld as ambiguous**, each row carrying its scan filename for checking in `scan_review.html`.

**Two method errors found and fixed while building it**, both worth recording:
- The "is this an ordinary noun?" test was *"does it ever appear lowercase"* â€” meaningless in German, where every noun is capitalised. That admitted `Geld`, `Gott`, `KÃ¶nig`, `Ende` as "names" and produced 1,706 junk proposals. Replaced with an explicit `NOT_NAMES` list of the prepositional-idiom nouns that ride in on "zu X"/"nach X" (`zu Gunsten`, `zu FÃ¼ÃŸen`).
- This register writes **articles with surnames** (`dem Hawich`, `der Cosmar`), so an article-rate test can only *veto* a candidate, never nominate one. The settled canon therefore has to be trusted outright rather than re-derived â€” it carries exactly the names the statistics cannot see.
- A third gap: two names that are *both* common are never compared, which is how `Brzechsta` (36) and `Brzechta` (8) sat side by side unnoticed. Added a seed-pair section; nothing there is ever auto-merged.

**Precision was poor in the discovered-seed tier.** Of ~25 proposals checked against the manuscript, about 20 were wrong (`Eines`â†’`Einer`, `Pforte`â†’`Pferd`, `Schriften`â†’`Schritte`, `Schweizern`â†’`Schweiner`, `Coeln`â†’`Cosel`â€¦). Every fix anchored on a canon name held up; the failures all came from statistically-discovered seeds. Next pass restricts proposals to canon-anchored names and treats discovered seeds as review-only.

**Adjudicated in full â€” see `name_decisions.md`.** Canonical forms settled: `Brzechsta`, `Kalisz` (absorbing `Kalicz`/`Kaliz`/`Kalisch`), `Hardenberg`, `Krotoszyn`, `Napoleon`, `Triebenfeld`, `Hohenlohe`, `Petersburg`. **`WrÄ…bczyn` confirmed a separate place from `TrÄ…bczyn` â€” never to be merged.** `SwiÄ™cier` confirmed a legitimate inflection of `SwiÄ™cia`. `Werthe`, `Wirth`, `Bedeutung`, `Eines`, `Inneres` dropped as seeds â€” not names.

**21 corrections applied** (backup `â€¦cleaned.txt.bak6`, all regeneration checks green, 20,750 archival lines, every site page character-exact): `Extaffette`â†’`Estaffette` Ã—5 (*estafette*, a courier â€” long-s read as x), `Curant`â†’`Courant`, `Appete`â†’`Oppeln`, `Bengelin`â†’`Beugelin` Ã—3, `Moszincka`â†’`MiÄ…czyÅ„ska`, `Plate`â†’`Pluto`, `PlaÃŸ`â†’`PaÃŸ`, `Panie`â†’`Panin`, `Unger`â†’`Ungar` (Hungarian *wine*, beside Champagner â€” not a person), `KÃ¡litz`â†’`Kalisz`, `Napolien`â†’`Napoleon`, `Tribenfeldschen`â†’`Triebenfeldschen`, `Sakkin`â†’`Sacken` Ã—3.

`Sakkin` was resolved against the Seidel biography on explicit instruction â€” it uses `Sacken` Ã—55 and names the woman herself, *"FÃ¼rstin Christiane Charlotte Sophie von der Osten-Sacken (1733â€“1811)"*, matching L18192's reference to her after her death. The corpus's own `Sakken` Ã—4+ was **not** merged into `Sacken`: standing policy is that the book's spellings are not authoritative over the corpus's internal evidence, so that stays open.

Still open: `HollÃ¤nder`â†’`HaulÃ¤nder` on the three settler-context lines only (L216's *"die HaulÃ¤nder oder Collonisten"* settles the term; the military `HollÃ¤nder` and the country `Holland` are correct), `Schlawen` vs `Schlawenschitz`, `Stege`, `Franckfurten`, and `MÃ¤rck` â€” where `MÃ¤rkische Landschafts-Obligationen` is a real instrument and the form may be a correct abbreviation.

## Name canonicalisation â€” Â§H merges applied

The seven canonical forms you settled, plus `Sakken` â†’ `Sacken`, applied as **64 substitutions** (backup `â€¦cleaned.txt.bak7`; regeneration clean, 20,750 archival = 20,750 chronological lines, every site page character-exact).

`Sacken` 7â†’17 Â· `Brzechsta` 36â†’47 Â· `Kalisz` 44â†’59 Â· `Hardenberg` 26â†’32 Â· `Krotoszyn` 40â†’43 Â· `Triebenfeld` 326â†’329 Â· `Hohenlohe` 39â†’45 Â· `Petersburg` 3â†’10.

Absorbed: `Sakken`/`Sakkensche(n)` Ã—13, `Brzechta` Ã—8 + `Brzechffa`/`Brzechtsa`/`Briechsto`, `Kalicz` Ã—5 + `Kaliz` Ã—4 + `Kalisch` Ã—4 + `Kalis` + `KaliszÅ¾`, `Hardenburg` Ã—6, `Krotoszin` Ã—3, `Treibenfeld` Ã—3, `Hohenlose` Ã—5 + `Hoferlohn`, `Peterbourg` Ã—6 + `Petersbourg`.

**Deliberately not merged â€” `Kalisch` is doing double duty.** Four occurrences are the city as a bare noun (`zu Kalisch`, `in Kalisch`) and were merged; **eight are the German adjective** â€” `Kalischen Krieges und Domainen Cammer`, `Kalischer Regierung`, `Kalischen Tribunal` â€” which is correct derivation from `Kalisz`, exactly like `Zagorower` and `Cosmarischen`. Merging those would have produced non-German. `Kaliszer` Ã—1 kept for the same reason, and `BrzechÅ¿ta` (long-s) was already canonical. A `keep_derivations` list now guards these.

**`Sakken` â†’ `Sacken` resolved on instruction to follow the biography**, which uses `Sacken` Ã—55 and names her outright â€” *"FÃ¼rstin Christiane Charlotte Sophie von der Osten-Sacken (1733â€“1811)"*. This is a deliberate, instructed exception to the standing policy that the book's spellings are not authoritative over the corpus's own evidence.

**`name_rulings.json` (new) makes the catalogue an outstanding-work list.** Every ruling â€” applied, rejected, dropped-as-seed, settled-pair, locked-apart, keep-derivation â€” is recorded there, and `name_catalogue.py` suppresses it on rebuild. Nothing already decided is put to the reviewer twice. The file is append-only by design: removing an entry re-opens a settled question. Catalogue now stands at **167 proposed variants across 83 names, 6 one-entity-or-two pairs, 5 withheld** â€” down from 206/21/18.

## Archival letter numbers removed from the letter bodies

Most letters opened with a line carrying nothing but the document's own number â€” `48`, `257` â€” written on the manuscript. Redundant now that every record carries a `letter_id`, so **298 such lines were removed from the archival text** (backup `â€¦cleaned.txt.bak8`).

Only the line immediately following a `[LETTER n]` marker was eligible, and only when it was nothing but a document number. **293** matched their letter id exactly; **5** did not and were removed on explicit instruction â€” `74`, `118`, `265` (parent numbers standing at the head of split sub-letters) and the two enclosure markers `179. a)` and `269 a)`. **20 letters were untouched**: the split sub-letters that never carried a number (`1a`, `72aâ€“f`, `74bâ€“d`, `118b/c`, `265b`) and the `(missing)`/`(skipped)` placeholders.

**Page structure was the risk, and it was checked rather than assumed.** `corpus_pages.split_pages` divides on blank lines, not on these number lines, so removal should be structurally inert â€” the strip script simulated the page split before and after and refused to write unless the count matched. It held: **869 pages before and after**, 318 records, and the re-derived line-break decisions came back identical (483 split, 825 join, 3 orphan, 5 catchword). Archival content lines **20,750 â†’ 20,452**.

**Line-number references across the documentation went stale** as a direct result, since every line below the first removal shifted. Those in `NEEDS_CONFIRMATION.md` and `name_decisions.md` were re-derived (`MÃ¤rck` 2864â†’2827; the `HollÃ¤nder` settler lines 7942/7943/14923â†’7842/7843/14718; the Dutch `HollÃ¤nder` 548â†’539), and both files now carry a standing note that line numbers move and the token should be searched for rather than the number trusted.

## Place of writing â€” re-derived from the dateline

The `place` field was produced by a hardcoded whitelist (`PLACE_RE`) scanned across each letter's last 15 lines, which failed two ways at once: it matched any listed town mentioned in the closing prose â€” letter 221 took `Neisse` from *"wider nach Neisse"*, the line immediately above its real dateline `Blizanow`; letter 237 took `Dresden` from *"von Dresden retournire"* â€” and it returned nothing at all for towns absent from the list, which produced most of the 95 blanks.

Replaced with extraction from the letter's **own dateline**, in both shapes the corpus uses: place and date on one line (`Breslau den 1ten Febr. 1799.`) and place on its own line above the date (`Kalisz` / `d. 29ten April`). The foot is checked first, then the head â€” Polish letters and some German ones date from the top (`w Warszawie dnia 5 Marca`).

Extraction stays faithful to the page; a separate `PLACE_CANON` map normalises manuscript spellings afterwards, so both layers remain inspectable: `Schlawenzitz`â†’Schlawenschitz, `Bleranow`â†’Blizanow, `TrÄ…bczin`â†’TrÄ…bczyn, `Franckfurth a d h`/`Fr a. d. Oder`/`Prandfurth a d O[der]`/`Fraudfurth an der Oder`â†’Frankfurt an der Oder, `Poser`â†’Posen, `Wein`â†’Wien, `Konigsberg`â†’KÃ¶nigsberg, `Kopoyno`â†’Kopojno, `Brzeg`â†’Brieg. A `PLACE_REJECT` set blanks readings too corrupt to be a place (`So bekomme ich`, `Thl. 13`, `Uria`) rather than recording them as towns.

**21 places set by explicit ruling, 206 derived, 92 with none found.** Distinct places 19 â†’ 30. `place_review.md` (new) lists every letter with no place, its closing lines and why nothing was found â€” a blank is frequently correct here, and the point is to make the absence a decision rather than an oversight.

`74b` took `Berlin`: letter 74 was split into a bundle of legal documents written in *different* places (74a Berlin, 74c Glogau, 74d Berlin), and 74b carries no dateline of its own, so it follows the bundle's head and majority. 74d's `Berlin` was separately confirmed correct â€” its Silesian address (`zu Kontop bey GrÃ¼neberg in Schlesien`) is the addressee's, not the place of writing.

## `Sachen` â†’ `Sacken` where it is the FÃ¼rstin

Surfaced while checking letter 74d: **8 instances of `Sachen` carry a noble title** â€” `FÃ¼rstin Sachen`, `der verstorbenen FÃ¼rstin von Sachen`, `Nachlas der FÃ¼rsten von Sachen` â€” and are the FÃ¼rstin von der Osten-Sacken, not the ordinary word. This vindicated the original instinct behind the earlier "Sakkin should be Sachen" reading: the name genuinely does appear as *Sachen* in this corpus. Following the biography simply makes `Sacken` canonical for all of them.

Corrected with a **title-anchored** substitution rather than a whole-word replace â€” the other **116** `Sachen` are the ordinary German word, and a blanket replace would have corrupted every one of them. `Sacken` 17 â†’ **25**; ordinary `Sachen` unchanged at 116. Backup `â€¦cleaned.txt.bak9`; all regeneration checks green.

`name_rulings.json` gained a `context_sensitive` section for exactly this class â€” tokens that are a name in some contexts and an ordinary word in others, recorded with the rule that separates them. `HollÃ¤nder`/`HaulÃ¤nder` is entered there too, still open.

## `Amelung` â†’ `Amelang`, settled from the signature

You read the signature on letter 138 directly from the scan. That resolved a Â§E pair the statistics could not: `Amelang` Ã—33 against `Amelung` Ã—11 â€” frequency is no evidence at all about which spelling a man used for his own name, which is precisely why that section never auto-merges.

Searching for the shape rather than the token surfaced **12 distinct forms**, of which four proved to be the same signature corrupted four different ways, each in identical position â€” directly under a closing formula, on a Berlin-dated letter from the same correspondent: `AMelerich[?]` (L46), `AMelan[tt?]` (L138, the one read), `AMelang` (L143), `Amelrath` (L144). Two carried transcriber uncertainty markers that the manuscript reading now resolves.

**19 substitutions**: `Amelung` Ã—11 â†’ `Amelang`, `Amelungs` Ã—4 â†’ `Amelangs` (root-only, genitive preserved), and the four pinned signatures. `Amelang` 33 â†’ **48**, `Amelangs` 2 â†’ **6**. Backup `â€¦bak10`; all regeneration checks green.

**Three left alone, recorded so the omission is a decision:** `Amel:` (line 13117) is an abbreviation like `HochfÃ¼rstl.`; `AmelanÂ¬` (11817) is a line-wrap fragment, a line-break question rather than a spelling one; `Amelange` (4014) already has the correct root and only an odd ending.

**A seed-list error of mine, corrected at source.** `Amelung` was the canonical form in `name_catalogue.py`'s `EXTRA_SEEDS`, so the catalogue had been anchoring on the wrong spelling and proposing corrections *toward* it. Fixed. My note in `NEEDS_CONFIRMATION.md` that "the rarer form is the one in your who's-who" was also wrong â€” neither spelling appears in `whos_who.md`; `Amelung` came from my own list. Â§E is now 4 pairs; the catalogue stands at 166 variants across 82 names.

## `Munduhr` â†’ `Medzibor` (letter 196)

The dateline of letter 196 read `Schwarzwald bey Munduhr d. 25ten May 1810.` The scan rules `Munduhr` out at once â€” there is a clear `b` loop and the word runs several letters longer â€” but the page is ~162 DPI and will not separate `Med-` from `Mied-` on its own, so the identification rests on the geography.

**Medzibor was the official name of MiÄ™dzybÃ³rz until 1886**, when it was renamed Neumittelwalde; it lay in **Kreis GroÃŸ Wartenberg, Regierungsbezirk Breslau**, Prussian Silesia. `Schwarzwald` is a recorded village in that same Kreis, so `Schwarzwald bey Medzibor` is the ordinary construction â€” hamlet, then nearest town. Three things corroborate: letters 193â€“195 and 199â€“201 are dated Kontop and Breslau, the same corner of Silesia; the sources place a *forester* at Schwarzwald, which fits a Kriegs- und **Forst**rath writing from there; and the period form is `Medzibor`, not the modern Polish `MiÄ™dzybÃ³rz`. Applied as the pre-1886 attested spelling; backup `â€¦bak11`, checks green, and `place` for letter 196 now derives as `Schwarzwald bey Medzibor` without needing a normalisation entry.

**Worth recording as a limit of the tooling.** `Munduhr` is a hapax that none of the methods built so far could reach: it is not close to any anchor name, is not a German word, and sat in a dateline the old whitelist extractor ignored entirely. It took a human reading the page. The same class of error is likely present among the 92 blanks and the odder values in `place_review.md`.

`name_rulings.json` gained a `places_identified` section holding the evidence, so the identification is not re-litigated later.

## Place list: two more identified, and "Unknown" made visible

- **L115** `Bretz den 3ten Aug` -> **Breslau**, on your reading of the page. `Bretz` was a hapax, not close to any anchor, sitting in a dateline - the same shape of error as `Munduhr`.
- **`Peysern` -> `Peisern`** (L28 dateline, L271 prose), normalising to the form the corpus already used at L31. Peisern is the German name for **Pyzdry**, on the Warthe.

**The places list was quietly hiding a third of the corpus.** `build_site_data.py` indexed a letter only `if p:` - so the 92 letters that name no place of writing were dropped from `places.yml` entirely, and the list looked complete when it was not. They are now grouped under **"Unknown"**, sorted last rather than alphabetically among the real places. `places.yml` now carries 28 entries covering all 318 records: Unknown 92, Berlin 54, Breslau 41, Wien 40, Blizanow 17, Kontop 16, Kalisz 10, and so on.

Distinct real places fell 29 -> 27 as `Bretz` merged into Breslau and `Peysern` into Peisern. Backup `...bak12`; all regeneration checks green.

## Michalina Prusimska â€” four surnames merged into one person

She appeared as **three separate people** in the site's people index and the who's-who â€” `Michalina Prusimska` (14 letters), `DÄ…bska (Michalina)` (8), `MiÄ…czyÅ„ska (Michalina)` (5) â€” with letters 242, 266 and 270 counted more than once because she is named differently within a single letter. Merged into one entry: **Michalina Prusimska (DÄ…bska / MiÄ…czyÅ„ska / Moscinska)**, 26 tokens across **18** letters.

The four surnames are one life: born **Prusimska**; married **DÄ…bska**, used consistently 1807â€“1811 and confirmed in the text itself (L28, *"der Frau v DÄ…bska gebohrnen v Pru[simska]"*); remarried late 1814, after which the letters write **Moscinska/Moszynska** â€” the writers' own error for **MiÄ…czyÅ„ska**, not a transcription defect. Letter 266 hedges openly, *"DÄ…bska oder Moscinska"*, exactly at the remarriage; letter 285 states the chain outright: *"gab sie der Tochter des Prussiemski, jezt verehelichte MiÄ…czyÅ„ska zurÃ¼ck."*

**The merge exposed an over-broad regex that had been conflating father and daughter.** The old `prusimska` pattern was bare `Pru[sz]imsk`, which also swept in the adjectival `Prusimskische(n)` Ã—6 â€” *"die Prusimskische Erben"*, *"die Confiscirte Prusimskische GÃ¼ter"*, *"von der Prusimskischen Familie"* â€” references to the family and its estates, not to her. Phase 2 had explicitly established father â‰  daughter, and the site index was quietly undoing that.

Her pattern now requires a feminine **`-a`** ending, which excludes both the adjectival family forms and `Moszynski` (masculine â€” her second husband, a third referent). A separate **`Prusimski family (TrÄ…bczyn estates)`** entry catches those instead, 19 tokens across 12 letters, so nothing is orphaned: L297 names him directly, *"GÃ¼ter nach einen gewiÃŸen **Anton v. Prussiemski**"* â€” Antoni Prusimski. The two patterns were checked for overlap: **zero tokens match both.**

`whos_who.md` collapsed from three entries to one merged plus one family entry, recording the corpus forms (`Prusimska` Ã—11, `DÄ…bska` Ã—10, `Moscinska` Ã—3, `Moszynska` Ã—1, `MiÄ…czyÅ„ska` Ã—1) and why the family is kept apart.

## People index generated rather than hand-curated

The site's `PEOPLE` list was 55 hand-written entries, and it matched **54 of the 807 tokens sitting in person position**. Anyone nobody had thought to add was invisible everywhere on the site â€” not obscure figures either: `Grotowski` Ã—15, `Brzechsta` Ã—29, `Hardenberg` Ã—24, `Sacken` Ã—22, `Amelang` Ã—8, `Schimmelpfennig`, `Struensee`. The same failure as the places whitelist, in a different file.

`name_catalogue.py` now exports its vetted seeds to `name_seeds.json`, and `build_site_data.py` merges them in. **Curated entries stay authoritative** â€” they carry display names, merged identities (Michalina Prusimska's four surnames) and distinctions the statistics cannot see (Hawich vs Honrichs); the export only fills the long tail. `people.yml` went **55 â†’ 103** entries.

Three rounds of filtering were needed first, each a real defect:
- **`Minister` Ã—127 entered as *canon***, because `harvest_canon()` splits `**Graf/Minister Hoym**` from `whos_who.md` into three tokens. `NOT_NAMES` now gates the canon too, not just discovered seeds.
- **`Wien` and `Krotoszyn` typed as people** â€” German `von X` fires identically for `Herr von Triebenfeld` and `von Krotoszin`. The derived place field plus an explicit estate list now settles type.
- **Countries and common words** â€” `PreuÃŸen` 25, `Sachsen` 17, `Italien` 12, `Hard` 43, `Graf` 37, `Beym` 16, `Fond` 15, `Advocat`, `Circa`, `Moratorium` â€” all blocklisted.

Recovered by the pass: Grotowski, Napoleon, **Gneisenau**, Nesselrode, Haugwitz, Massow, BÃ¼low, Dohna, Wartensleben, Blomberg, NÃ¶ldichen, Lipski, Pirch, Struensee, Schimmelpfennig.

**A standing limit worth recording:** this list cannot be complete by construction. It is built from tokens the corpus puts in a recognisable name slot, and 527 of 738 such tokens are hapax. Anyone named once without a title still will not appear.

## `Humboldt`, `GÃ¤rtner`, `Napoleon` standardised

**29 substitutions** (backup `â€¦bak13`, checks green):
- `Humbolt` Ã—11 and `Humbold` Ã—5 â†’ **`Humboldt`**. Neither corpus form was correct â€” this is Wilhelm von Humboldt, Prussian plenipotentiary at Vienna, named beside Hardenberg and Nesselrode (*"Humboldt und auch Nesselrode wolten ihm ihren Monarchen prÃ¦sentiren"*). The 17th instance was `Humbo[?].` standing alone under *"Wien d. 5ten November 1814."* above *"An den Herrn v. Triebenfeld"* â€” **his signature on a letter to Triebenfeld**, so the uncertainty marker resolves too.
- `Gartner` Ã—6 â†’ **`GÃ¤rtner`**, the Geh. Rath.
- `Napolion` Ã—5 â†’ `Napoleon`, `Napolons` Ã—1 â†’ `Napoleons`.

**`GÃ¤rtner` is a surname *and* an occupation.** L303's creditor register lists *"der GÃ¤rtner Nickel"* beside *"der Sattler Hennig"* and *"Major von MÃ¼nchow"* â€” that entry is the gardener, a different referent. Line 4089's `Gartner` has no title and sits in a garbled passage, so it was **left as written**. The people index cannot separate the two, so the display name reads `GÃ¤rtner (Geh. Rath)` to say which is meant, and `name_rulings.json` records it under `context_sensitive`.

`whos_who.md` gained entries for Humboldt, GÃ¤rtner and Napoleon, none of which had one. Â§E is down to **3** open pairs: `Sachsen`/`SachÃŸen`, `Wartemberg`/`WÃ¼rtemberg`, `Bartenstein`/`Brandenstein`.

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

## `Portalis` = `PourtalÃ¨s` â€” merged, with one instance deliberately preserved

Four spellings of one man collapsed into the corpus's own dominant form: `Portalis` Ã—5, `Pourtalles` Ã—3 and `Portales` Ã—1 â†’ **`Pourtales`**, now 15. Backup `â€¦bak15`; checks green.

The identification does not rest on spelling similarity but on biography. Letter 264 describes *"Der reiche Gr[af] **Portalis** mit Barbe in **Neufchatel** erzogen"* â€” raised in NeuchÃ¢tel with Barbe, having sold his English and French estates for millions. Letter 266 describes *"**Pourtales** â€¦ folgt blind seinen Jugend Freund und Schul Cammereden B[arbe]"* â€” the same school friend, the same fortune. NeuchÃ¢tel is the PourtalÃ¨s family seat. One man, under two spellings.

**Line 18917 was excluded from the substitution and must stay excluded.** It reads *"den **Pourtales (nicht Portalis)** wird sehr schnell etworten"* â€” the writer's own note that the name should be Pourtales rather than Portalis. A blanket replace would render it *"Pourtales (nicht Pourtales)"*, destroying the very remark that establishes the identification. Recorded in `name_rulings.json` under `context_sensitive`; the site's pattern matches `Portalis` too, so that one mention still indexes to the right man.

**Canonical form is `Pourtales`, not `PourtalÃ¨s`.** The writer never used the accent, and project policy is root-only correction that does not invent period orthography. The family's proper form appears as the site display name, `PourtalÃ¨s (Pourtales)`.

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

**One failed match ended the search.** A postscript's own date (`die RÃ¼kkunft nach Breslau ist
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

## Phase C â€” English translation

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
make sense of every sentence: `drÃ¼ckte mich schier zu Baden` for `zu Boden` ("crushed me to the
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
`Durchlauchtigster FÃ¼rst`, 197 close `v Triebenfeld`. Where a letter opens mid-flow with no
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
`Sequestration`, `Erbpacht`, `FideicommiÃŸgÃ¼ter`, and the name spellings established for this
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

Verified while writing: letter 7 is signed `Charlotte von Triebenfeld ... ganz unterthÃ¤nigste
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
on a central figure. Also lost: five letters for KÃ¶ckritz, one each for Amelang, PourtalÃ¨s
and GrÃ¤venitz.

A `NAME_ABBREV` table now folds verified abbreviations into the matching patterns. Result:
Hardenberg 31 -> 40, KÃ¶ckritz 29 -> 33, Amelang 31 -> 32, PourtalÃ¨s 12 -> 13, GrÃ¤venitz
2 -> 3, Sacken 21.

**Only abbreviations verified in context were added**, because a wrong expansion invents a
mention that is not in the letter, which is worse than missing one. Four traps were found and
excluded, each checked by reading the passage:

- `Ant:` is **Antwort**, not Anton - "Ant: wir zahlen schon zu viel"
- `Kur:` is **CurlÃ¤ndisch**, not a person - "der Kur: Erben"
- `Ko:` is **Koschentin**, the estate, not KÃ¶ckritz. L2's "In der Ko: Geschichte" is followed
  by PourtalÃ¨s answering that he wants to buy, which settles it
- `Sch:` could be Schlabrendorff, Schenck or Schimmelpfennig; `B:` could be Barbe, Beyme or
  Brzechsta

`Sa:` was admitted only in its title-anchored form. Both corpus instances read "der FÃ¼rstin
Sa:" and "Die FÃ¼rsten Sa:", and Sacken is the only FÃ¼rstin S- in the correspondence; a bare
`Sa:` would not have been safe.

**The translations were inconsistent about the same thing, and that was a prompt fault.** The
system prompt said to reproduce every proper noun exactly as spelled and never normalise a
name, which fought against ordinary comprehension, so the model decided case by case: L239's
"Min Hard:" became "Minister Hardenberg" while L264's "FÃ¼rsten Hard:" stayed "the Prince
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
translation; letter 26 turns out to read **"so viel boshafte GerÃ¼chte ausgestreut wurden"**,
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

The edition was built around one archival holding, Oe 1 BÃ¼ 9454, and it showed: adding a
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

The definitions are drafts: the reference works (Adelung, KrÃ¼nitz, the
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
gulden replacement was read in context first. "Polish gulden", the zÅ‚oty of
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
  at Kalisz", "the PoznaÅ„ government"). A house-form rule in
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
expecting PrÃ¤-; they do now. 108 entries, 14,037 marks in 417 documents.

`glossary_candidates.py --check` is the gate the plan called for, and
regenerate.py runs it after the holdings' descriptions: it fails the build if
a translated holding brings a qualifying word that is neither an entry nor
ruled out, and names it. Tested by removing one ruling: it failed and named
the word; restored, it passed.

## The glossary checked against the reference works (2026-10-02)

With woerterbuchnetz.de, kruenitz.uni-trier.de and pl.wikisource.org now
allowed, 54 of the draft entries were read against KrÃ¼nitz, Adelung, Grimm
and Gloger and set `checked: true`, each with a `source:` naming the entry and
its URL. The glossary page now links the entry name (`source_html`, built by
glossary_build.py); a path into `reference/` is still dropped, and the rest of
the line now shows (the Mencel source's "for the rule of 1795").

Where the work said otherwise, the English and German were corrected:
- Money and measures: Courant is the coin of everyday trade, small change
  apart; the Friedrichsdor stood by law at 5Â¼ Rthl Courant, in trade at five
  in gold with a moving premium, and at six in the royal offices in 1809; the
  Centner was 110 pounds at Berlin but 132 in Silesia (and grain, measured
  by the Scheffel, is dropped from it); the Klafter is six feet by six, as deep as the logs are long; the
  Morgen is a day's or a morning's ploughing; the Hufe is 30 Morgen, and in
  Greater Poland the wÅ‚Ã³ka itself was called Hufe; the Polish gulden is a
  money of account; the legal rate of interest in Prussia was five per cent.
- Land and law: the canon is not "never raised" (KrÃ¼nitz has the hereditary
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
among them, though KrÃ¼nitz was read for each; it has no Dominium); and those the
works online have no entry for: olÄ™drzy, the Duchy of Warsaw's prefects,
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
(OstrorÃ³g-Prusimski), the original owner of the TrÄ…bczyn and Kamionna estates,
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
Oe 1 BÃ¼ 14525), Michalina Prusimska's complaints of 1800 to 1802 (Nr. 3709, as
far as the scans show), the sales of Szetlewek, Kamionna and Kolno and
Pszczew, the Erbet lease and the OleÅ›nica petition, the entail of 1805
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
Antoni Prusimski, noted that KÃ¤hmen had slipped through for Kamionna, and asked
for all names and places in the English to be checked. A names audit compared
every name the translator recorded, German beside English, with the settled
form in `reference/people.yml` and `places.yml`. The transcriptions are not
touched: what the writers wrote stays.

- Registers: the spellings found are now recorded variants, so the termbase
  tells the translator the settled form and the build tags them. Antoni
  Prusimski takes Prussiemski, Prussimski, Prussimsky and Prusimsky (30
  documents, from 29). Kamionna takes KÃ¤hmen and Kamienne, and Kamen, KÃ¤men
  and Kamener only where they name the estate (they are also the verb).
  Kolno takes Kollno. Michalina Prusimska gets a running-text form,
  MiÄ…czyÅ„ska, so the translator no longer prints her catalogue entry inside
  a sentence; her second husband, StanisÅ‚aw MiÄ…czyÅ„ski, gets his own entry
  (Moscinski, MiÄ™czynsky), with a People-page biography. Prince Wilhelm of
  Prussia gets his English form. Some forty other spellings of people and
  places join their entries.
- English: rules in `reference/english_forms.yml` bring the published
  English into line (86 translation files, 31 English summaries): Prusimski;
  MiÄ…czyÅ„ska and MiÄ…czyÅ„ski for Moscinska, Moscinski, MiÄ™czynsky; Kamionna
  for KÃ¤hmen, Kamen, Kamienne, and "Kamionna or Kamionna" made one; Kolno for
  Kulm (31) and Kollno (20); Prince Wilhelm of Prussia for "Prinz Wilhelm
  von PreuÃŸen"; and the other spellings by table (a new `names` lookup in
  english_forms.py). Two one-page corrections: "the peasants of Stoki" is
  Skokum (letter 191, die Skokumer Bauren), and the French letter of 1815
  says "in favour of Madame MiÄ…czyÅ„ska", where the English had printed her
  catalogue entry.
- German summaries: the same forms in `site/_data/summaries_de.yml` and the
  units' checked German summaries (42 places).

Left standing, and listed in NEEDS_CONFIRMATION: the Grand Duchy of Posen,
Betsche below Strehlen, Klein Althammer, PourtalÃ¨s / not Portalis (the
writer's own correction), and the names that need a ruling (Tarmowo or
Tarnowo, WrocÅ‚awek, Schliefen and others).

## The editor's rulings on the names audit (2026-10-03)

Tarnowo, not Tarmowo (the register's `tarmowo` now displays Tarnowo); Ribbeck
for Rybbeck and Rybbek; Kunkel for Kunckel; Dormowe is Dormowo; and in letter
155 the doubtful "Hussaczinski[?]" is Hussarzewski, applied to the
transcription as a recorded ruling (`transcription_decisions.csv`, line
11069), which takes the letters' doubt marks from 252 to 251. Klein Althammer,
from which Hahn wrote letter 189, is Stara KuÅºnia by Bierawa (the gazetteer
GOV, LANAWAJO90CG), the works estate of the entail; the register had excluded
it, and now folds it in. The cathedral chapter "zu Wraclawek" in 14525, 28 is
WÅ‚ocÅ‚awek: a new place in the register, and the English says so. The scan
shows "Wraclawek" where the transcription reads "WrocÅ‚awek"; whether to
correct the transcription is left to the editor. The English and the German
summaries follow (a rule in english_forms.yml; 43 places in the translations,
12 in the English summaries, 25 in the German).

Betsche below Strehlen (letter 119) is left as it is, with the evidence that
it is not Pszczew, for the editor to rule.

BÄ…tkowo (editor, 2026-10-03). The village the contracts and the entail call
Batkowo or Botkow, the village of the WÅ‚ocÅ‚awek cathedral chapter from 1239
until the partition, is BÄ…tkowo in Polish and in the English, Batkowo in
German. The register entry, the English translations (7 documents) and
summaries, the German summaries, the era page and the holdings' About pages
follow; Botkow and Botkowo are folded in. The place stays WÅ‚ocÅ‚awek, as ruled.

Betsche below Strehlen (editor, 2026-10-03). The small estate in letter 119,
divided among Hussite settlers about 1801, lay near Strzelin in Silesia and is
not Pszczew. The Pszczew entry in the register no longer matches it, so the
letter is no longer listed under Pszczew; the English keeps "Betsche".

Wraclawek and Posen (editor, 2026-10-03). The transcription of 14525, 28 now
reads "Wraclawek" and "Wracla-/wek", as the page has them (scans 0121_b,
0122_a1), where it read "WrocÅ‚awek"; the place is still WÅ‚ocÅ‚awek, and the
change is recorded in the holding's transcription_decisions.csv. "Grand Duchy
of Posen" stands in the English of 12765 (14, 27, 28) as the state's English
name. Schliefen / Schlieffen stays open. The 9454 and 14525 letters.json files
are back to their CRLF line endings.

MiÄ…czyÅ„ski / MiÄ…czyÅ„ska (editor, 2026-10-03). Every spelling of the name
(MiÄ™czynsky, MiÄ™czynska, Mieczynski, Miaczynska, Moscinska, Moszynski, ...)
is written MiÄ…czyÅ„ski for StanisÅ‚aw and MiÄ…czyÅ„ska for Michalina in the
English. The English was already so; the register's patterns and the rules in
english_forms.yml now cover the forms with e and Ä™ too, and "Madame
MiÄ™czynsky" in the French letter of 1815 is written Madame MiÄ…czyÅ„ska, so a
new holding is standardised as well. The live site still showed "M. de
MiÄ™czynsky" in 12765, 6 because the names work had not yet been published.

Catchwords said once (editor, 2026-10-03). Every page break in every holding
was read for a catchword the reading text or the English still said twice
("zu || zu", "Salomon Natan || Nathan junior", "Â§. 1. || Â§ 1."). The line-break
pass had dropped those that stand on a line of their own and open the next
page; it could not see one at the end of a full line, one the transcription
misread, or a repeated section number. 59 more are now recorded in a new
`units/<slug>/catchwords.yml` (Oe 1 BÃ¼ 14526: 41, Oe 1 BÃ¼ 9454: 11, the Erbet
record 53/71/0/-/57: 5, Oe 1 BÃ¼ 14525: 2), which `corpus_pages.py` reads with the line-break
decisions: the reading text drops the whole line or only the words named, and
the transcription keeps them. Each entry names its line by number, text and
the next page's first line, so a shifted corpus is found again or stops the
build. The English followed in 39 corrections in english_corrections.yml
(two of them join a word the page break had split: voluntarily, misfortune);
the translator reads the reading text, so a new translation will not need
them. The repeats that the sentence needs stay ("mit Kolno. || Kolno
grentzet", 14525, 13). english_forms.py no longer applies a correction twice
where the words it looks for are part of its own replacement.

Ã‰cus are Reichsthaler (editor, 2026-10-03). The Prince's French letter to
Stein of 1815 (12765, 6) counts in Ã©cus, the French that Prussians wrote for
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
his death no longer says TrÄ…bczyn was sold after 1818. Names follow the
register (Kamionna, ZagÃ³rÃ³w, Pszczew, OleÅ›nica, Konotop, SÅ‚awiÄ™cice, WrocÅ‚aw,
PoznaÅ„, Kalisz), Hohenlohe-Ingelfingen is named as the house style has it, and
the dashes are gone. 54 events, every document link resolving.

Primary sources before Seidel (editor, 2026-10-03). The timeline's
estate claims that rested on Seidel's biography were checked against the
documents. The 1811 proceedings are now told from letters 74a and 74d: the
Invalids' Fund applied on 30 July 1811 to enforce its 50,000 Rthl loan, with
9,375 Rthl of interest unpaid since 1807, and on 1 August the Kammergericht
attached Princess von Sacken's legacy of 80,000 Rthl; the claim that the case
file survives in Berlin is gone. The 1797 entry no longer says ZagÃ³rÃ³w was the
lordship kept after TrÄ…bczyn was lost; Tilsit and the Final Act cite general
history and letter 271 in place of Seidel. Seidel remains a source, a
secondary one: the documents come first and decide where the two disagree, and
a fact from him alone is cited to him (his separation, the house arrest, Jena,
Prenzlau, his death). The rule is in HOHENLOHE_ERA_PLAN.md and the timeline's
header.

Correspondents named in full, with their titles (editor, 2026-10-03). The
From and To line in a document's header showed the names as the holdings
record them, some in German ("Friedrich Ludwig, FÃ¼rst zu
Hohenlohe-Ingelfingen", "Ministerium der auswÃ¤rtigen Angelegenheiten") and
most as a bare surname ("Hardenberg"). A new reference/correspondents.yml
gives each of the 43 recorded forms a name and the person's title at the time
of the documents, in English and German; the header now reads, for example,
"Karl August von Hardenberg, Prussian State Chancellor -> Prince Friedrich
Ludwig of Hohenlohe-Ingelfingen". The lists on Browse and in search show the
name alone, in the page's language. A recorded form with no entry is shown as
it stands and reported by build_site_data.py.

Places of writing in the page's language (editor, 2026-10-03). The place line
under a document's date showed "Wien" on English pages, and "Blizanow" and
"SwiÄ…tniki" without their Polish accents. English pages now use the
register's English form where English has one (render: Vienna, Warsaw), and
German pages the register's name (Wien, Warszawa (Warschau)); "Unknown" is
"Unbekannt" in German. The register gives BlizanÃ³w and ÅšwiÄ…tniki their accents,
with the letters' spellings kept as variants, and St. Petersburg in a dateline
now finds its entry. The English (67 changes in 48 translations, 10 in the
summaries, by a rule in english_forms.yml) and the German summaries follow
("Blizanower GÃ¼ter" stays, a German adjective).

Document navigation stays in its holding (editor, 2026-10-03). The previous
and next links on a document page, in archival and in chronological order,
ran across the whole edition: the last document of one holding led to the
first of the next, and the chronological order moved between holdings by
date. Both orders are now kept per holding (build_site_data.py), so a reader
browsing one holding stays in it; at a holding's first and last document the
arrow is shown disabled. Checked: no navigation link leaves its holding.

A stray full stop in 12765, 8 (editor, 2026-10-03). Page 2, line 212 read
"den man die GÃ¼tter genommen hat. / und der EntschÃ¤diget werden muÃŸ", one
clause cut in two; the English followed ("have been taken. and who must be
compensated"). The full stop is gone from the transcription (ruling in the
holding's transcription_decisions.csv), and so from the reading text, and the
English reads "have been taken and who must be compensated" (a correction in
english_corrections.yml). The corpus dataset was regenerated with it, and
now also carries BlizanÃ³w and ÅšwiÄ…tniki.

Extent gives the pages only (editor, 2026-10-03). A document's details panel
gave its extent as "34 lines across 2 manuscript pages" with "lines 1-34"
beneath; it now gives the number of manuscript pages alone ("2 manuscript
pages", "1 manuscript page"; German "Handschriftenseite(n)"). The line numbers
stay in the transcription view, where a line is cited.

Document headers tidied (editor, 2026-10-03). Every document is now called
"Document 9 Â· Draft": the number first, then the kind, where the header had
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
("Holding: Oe 1 BÃ¼ 9454, Hohenloher Zentralarchiv Neuenstein (HZAN)").

The Szetlewek sale explained (editor, 2026-10-03). "Most of the price goes to
the man who held the farm on pledge" said too little. The timeline and the
era page now say, from the contract (14526, 25), that 8,333 Rthl of the
12,333 went to Ignatz von Radzinski, who had lent money on the farm and held it as
security until he was repaid, and was to vacate it once paid.

ToruÅ„, not Thorn (editor, 2026-10-03). The place register has a new entry,
ToruÅ„ (German Thorn), so the documents that name it are tagged with it: the
two replies of February 1799 sending Hohenlohe-Ingelfingen to the Government
at Thorn for the confiscation judgment (14525, 43, 44), and the 1815 frontier
letters (9454, 246, 266, 271). "Thoren" counts only where it names the town;
in letter 104 it means "fools" and is left alone. The English writes ToruÅ„ (a
rule in english_forms.yml: 4 translations, 2 summaries), as do the timeline,
the era page and the About page of 14525; the German gives ToruÅ„ (Thorn).

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
have Michalina DÄ…bska removed from TrÄ…bczyn; to have the court administration
put on the remaining estates for unpaid interest lifted, the King of Saxony
having granted debtors three years' grace; to remove Honrichs, who had had
himself appointed its administrator and had sold land without authority; to
sue Oppenheimer and Wolff over 72,000 Rthl; to collect the arrears; and to
appear at the Diet in Warsaw, where every landowner had to appear in person or
lose his estates. The era page writes Konotop, not Kontop.

- **Timeline and era page: who was not paying, and what** (editor, 2026-10-03). The
  entries for 1 January 1811 and July 1811, and the matching paragraphs of the Hohenlohe-
  Ingelfingen years page, now say that the colonists holding farms in hereditary lease on the
  ZagÃ³rÃ³w estates paid none of their yearly rent ("interest"), that the tenants of OleÅ›nica,
  Kopojno and Drzewce paid no lease money, and what still fell due (letter 212). The remission
  of a third of the rent is given as Triebenfeld's proposal (letter 215, a Pro Memoria), and the
  eviction as the course he put forward if the estates were to be kept (letter 216).

- **Timeline: Konotop shortened; the 1811 news from Sanitz retitled** (editor, 2026-10-03).
  The Konotop entry gives only the main charges (the full list stays on the era page). The
  entry of 15 August 1811 no longer reads as if the estates were only then to go to Michalina
  DÄ…bska (Prusimska): they were handed over in 1807, and letter 217 reports how that came about
  (her petition to Napoleon, passed on to the Polish governing commission, which ordered it).

- **Timeline: cryptic entries rewritten; a house-style rule against them** (editor,
  2026-10-03). About thirty entries, in English and German, now say who people were
  (Hoym, Beyme, Struensee, Barbe, Zerboni, Princess von Sacken), what offices and procedures
  were (the War and Domains Chambers, the provincial courts, the mortgage books, court
  administration, the entail), and what happened, from the documents: letter 179a is a draft
  petition for a royal loan of 698,000 Rthl, not a survey that "promises" villages; the 1808
  copies show the ZagÃ³rÃ³w court still working after TrÄ…bczyn was taken; the King, not the
  chamber, refused the Pszczew sale in 1805; Erbet's costs were 9 Thaler 18 groschen. Polish
  place names: WitÃ³w, PiotrkÃ³w, Nysa. New section "No cryptic statements" in HOUSE_STYLE.md.

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
  entries under two spellings: Grevenitz (GrÃ¤venitz, "Grev:"), Carl Titz (Tietz, the forest
  inspector who leased Drzewce), Koppe (Koppen, back from Paris in 1808) and Metzig (Melzig,
  written both ways in one passage of letter 41). Each is now one entry, and the English
  uses one spelling (english_forms.yml, person-spellings). The "Born" entry was catching the
  start of BornstÃ¤dt and Bornsted: it is now Dr Ernst Gottlob Born of Frankfurt an der Oder
  alone (two certifications), and BornstÃ¤dt finds all his spellings. Haugt now also finds
  "Haucht" (letter 31). Knoblauch and Knobloch are two men and stay apart.

- **German biographies: Polish place names** (editor's question, 2026-10-04). 79 German
  biographies on the People page used German place names (Kaemen, Betsche, Kalisch, Breslau,
  Koschentin, Wittow and others). They now give the Polish name with the German in brackets
  at its first mention (Kamionna (Kaemen), Pszczew (Betsche)), as the site does elsewhere;
  Warschau and the GroÃŸherzogtum Posen stay as German writes them. The biographies of the
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
  ("Brzezier GÃ¼ter"), now tagged as that estate. The holding's page, the timeline entry and the
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
    December 1800 and its withdrawal), Danckelmann (vice-president at PoznaÅ„, then president
    at Kalisz) and von der Reck (the petition of 1802), in both languages. Danckelmann is
    now also found where his name is broken over a line.
  - Correspondents: the Grand Chancellor Goldbeck, the South Prussian Governments at PoznaÅ„
    and Warsaw, the Superior Appeal Senate of the Kammergericht and Michalina Prusimska.
  - Places: "Ingelfingen" was tagged as a place named in the text wherever a document wrote
    the Prince's name, "Hohenlohe Ingelfingen" (170 of 215 matches); the pattern now finds
    only the town, the principality and the Prince "von Ingelfingen".
  - Timeline: the 1800 entry is retitled "Prusimski's daughter sues for the Brzyce estates".

- **III. HA MdA, III. Nr. 12366 added** (2026-10-04). The foreign ministry's file on Michalina
  MiÄ…czyÅ„ska's claim and on the Polish judgments against Hohenlohe-Ingelfingen's creditors, 1818
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
  the foreign ministry's file on Michalina MiÄ…czyÅ„ska's claim, 1828 to 1832: eleven documents on
  15 pages and the cover, eight in French, two in Polish and one in German. All concern the
  compensation of the Breslau banker Weigel for the mortgage of 30,000 thalers the Polish courts
  struck off TrÄ…bczyn: the answers of Baron Mohrenheim, of the finance commission and of Engel to
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
  the Berlin agent Eysenhardt); "CÃ©sarÃ©vitch" matched to Grand Duke Constantine. Two small
  additions to the build: a by-paragraph ruling can name one document's part of a shared page
  ("8:0009_a2"), and a paragraph break no cue proposes can be written into
  `paragraph_decisions.csv` by hand (cue `hand`). The edition has 458 documents. Not yet
  translated; the summaries have not had the claim check; the German translations beside the two
  Polish letters are not transcribed. See `units/iiihamdaiiinr12367/notes.md`.

- **AGAD 1/174/0/2/73 and 1/174/0/1/6 added** (2026-10-04), the first holdings from the Archiwum
  GÅ‚Ã³wne Akt Dawnych in Warsaw: the papers of July 1807 by which the Governing Commission, the
  provisional Polish government, returned the Prusimski estates to Michalina DÄ…bska. From the
  commission's file of its stay at Dresden (1/174/0/2/73), four documents on five pages: her
  petitions to the commission of 20 and 23 July and to Napoleon of 21 July, and the commission's
  draft resolution of 21 July 1807. From its register of orders and resolutions (1/174/0/1/6),
  two documents on three pages: the order of 12 July to carry out Napoleon's decree for JÃ³zef
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
  New people: MaÅ‚achowski, Åuszczewski, Bischoffwerder; Sanitz, Niemojewski, Hohenlohe and
  Michalina DÄ…bska matched in the forms of 1807; Dresden, Warsaw and Kolno matched in their
  Polish and French forms. The glossary entry for the Prussian court called Regierung no longer
  marks "die preuÃŸische Regierung" or "the Prussian Government": 36 marks gone, in these
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
  Ã©cus and Polish florins are rendered, and that all 459 translations are drafts.

- **APP 53/968/0/-/801 added** (2026-10-05), the second holding from the State Archive in
  PoznaÅ„: sixteen pages from the papers of Albert Breyer, copied about 1930, of three papers on
  the parcelling of the ZagÃ³rÃ³w and TrÄ…bczyn estates. One document, dated 21 March 1806: the
  Prince's general power of attorney for Triebenfeld of 19 February 1805, the consent of the War
  and Domains Chamber at Kalisz of 28 January 1806, and the hereditary lease of 100 Hufen of the
  Drzewce forest to eighteen settlers, whose opening is missing. The seventeen images were
  staged uncropped; the editor's transcription was cut to the pages (page 16 had no mark) and
  the cover's text added from the image. Corrected against the scans: 84 passages, with the
  copies of the power of attorney in APP 53/71/0/-/57 and of the consent in Oe 1 BÃ¼ 14526
  (document 8) as second witnesses. A skipped line and a half of the consent was restored;
  Michael Just's share is 5 Hufen, not 10; the lessee Siemert or Liemert is Liewert; "Petenck"
  is Schenck; the three crosses of the eleven lessees who could not write are given as "xxx".
  Summarised in German and English; holding page in both languages; two timeline entries (28
  January and 21 March 1806) and a third source for the entry of 19 February 1805. Five place
  patterns widened for the copyist's forms (Trompczyn, Marianten, Szedlewek, ÅšwiÄ™cia and ÅšwiÄ™ca,
  NowawieÅ›); the last also matches "NowawieÅ›" in III. HA MdA, III. Nr. 12367, document 7. The
  edition has fourteen holdings and 465 documents. Not yet translated; the summary has not had
  the claim check. See `units/app539680801/notes.md`.

- **APP 53/968/0/-/801 divided into three documents** (2026-10-05, the editor's ruling the
  same day): the power of attorney (document 1, 19 February 1805, Guhrwitz), the consent
  (document 2, 28 January 1806, Kalisz) and the lease contract (document 3, 21 March 1806,
  MariantÃ³w), with a relation from each of the first two to the contract. Three summaries in
  place of one; the holding page cites each paper by its own number; the timeline entries
  point to the right documents; the correction log re-keyed
  (`intake/split_documents.py`). The address `/documents/app539680801/1/` is now the power
  of attorney; the contract is at `/3/`. The editor also confirmed "Dr." before Johann
  Wendel Heilmann and Michael Just's 5 Hufen. New person: Heinrichs, the chamber's
  Commissionsrath and Oeconomie-Commissarius who attests this lease and the AlthÃ¼tte lease
  (Oe 1 BÃ¼ 14526, document 16), kept apart from Martin Honrichs. The edition has 467
  documents.

- **What the rest of the site owed APP 53/968/0/-/801** (2026-10-05). The era essay said the
  crown had licensed the division of TrÄ…bczyn and ZagÃ³rÃ³w the year before the punctation of
  April 1805. Both copies of the consent are dated 28 January 1806, on cabinet orders of
  October and December 1805; the sentence is corrected in both languages and links both
  copies. A short paragraph on the Drzewce lease added to section III (no entry money, four
  free years, on uncleared forest). The holding pages of APP 53/71/0/-/57, Oe 1 BÃ¼ 14526,
  Nr. 3705 and Oe 1 BÃ¼ 9454 name the new holding among their related holdings, in both
  languages. APP 53/71/0/-/57 is no longer described as the only holding from PoznaÅ„.

- **APP 53/968/0/-/801 translated and its summaries claim-checked** (2026-10-05, in session at
  the editor's word). The three documents were translated beside the published English of the
  other copies of the same texts, so the same formula has the same English; where this copy
  differs from them in a word it is followed and the difference flagged. check_translations.py
  raised two rows, neither a fault; uncanonical_names.py nothing in this holding. Seven of the
  copyist's spellings became variants in `reference/places.yml` (Trompczyn, Marianten,
  Mariantow, Szedlewek, ÅšwiÄ™cia, ÅšwiÄ™ca, ÅšwiÄ…tnik). The claim check held 35 statements of the
  three summaries to the documents and weakened two. The English summaries, the holding page
  and a timeline entry now use the termbase's words (demesne farm, Government, Midsummer).
  Status `translated`; every document with text now has an English translation, 462 of 467.

- **I. HA Rep. 162, Nr. 295 added** (2026-10-05), from the file of the Prussian state treasury
  on the 50,000 Rthl registered on ZagÃ³rÃ³w: the cover and eleven pages of copies of 1805, in
  three documents. Triebenfeld's bond to the General Invalids' Fund (Berlin, 28 January 1805),
  which pledges a fifth of the Prince's bond for 250,000 Rthl; the South Prussian Government's
  certificate of its second acknowledgement (Kalisz, 5 March), with the note of its entry in
  the mortgage book; and the mortgage certificate for ZagÃ³rÃ³w (13 March). The editor
  transcribed from the joined page images, line by line. Corrected against the images: 34
  passages; the list of estates in the bond ends "GrÄ…dzyn", not "TrÄ…bczyn"; "Seehandlungs-
  Obligationen", "Koniner Kreise", "Frist". Line ends and paragraphs ruled by hand. Summarised
  in German and English and claim-checked (27 statements, one weakened); translated in session
  (no check rows); holding page in both languages; the timeline entry for the loan, section III
  of the era essay and the pages of Oe 1 BÃ¼ 14525, Oe 1 BÃ¼ 9454 and Nr. 3705 link to it. New
  person: the Regierungsrath v. Lichnowski at Kalisz, kept apart from the creditors of that
  name. Glossary: `rubrik` added, three abbreviations ruled out. The edition has fifteen
  holdings, 470 documents and 1,558 pages; 465 have an English translation. See
  `units/iharep162nr295/notes.md`.

- **I. HA GR, Rep. 7 C, Nr. 1414 added** (2026-10-05), "Aufenthalt des Anton v. Prusimski in
  Venedig": three documents on four pages. An extract in French from dispatch No. 423 of Count
  Cattaneo, the Prussian resident at Venice, of 14 December 1796 (Prusimski, ill and broken by
  his wife's death, has asked for and been given a certificate that he cannot travel), with
  the slip on which the councillor Raumer directs on 8 January 1797 that Hoym and SchrÃ¶tter be
  notified; the department of foreign affairs' draft of 11 January 1797 to Hoym, Schroetter
  and the Grand Chancellor von Goldbeck; SchrÃ¶tter's reply of 29 January. Of seven scans the
  editor wanted four; three openings were cut to the written side. The editor's line-by-line
  transcription was cut to pages, with the department's marks on the papers it received set
  apart as office text. Corrected against the scans: 20 passages; Raumer (for Rammer, Maunes,
  Maurer), Goldbeck as third addressee, Haugwitz and a doubtful Alvensleben as signatories,
  "affatiguÃ©" restored in the extract. Summarised in both languages and claim-checked (19
  statements, two weakened); translated in session, no check rows; holding page in both
  languages; a timeline entry (14 December 1796) and two sentences in section I of the era
  essay; Nr. 3570 and Nr. 3709 link to it. New people: Cattaneo, Raumer, Schroetter and
  Haugwitz, who is now also indexed in the letters of Oe 1 BÃ¼ 9454 that name him. New place:
  Venice. The statement of MiÄ…czyÅ„ska's claim of 1818 (III. HA MdA, III. Nr. 12366, document
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
  champÃªtres" (for "qui font parfois mon pain de nÃ©grÃªtes [?]"), and the line written
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
  "[Londres?]", are left as "[Revâ€¦?]" and "[Pâ€¦?]", what the editor sees of them, and the
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
  1589 for an inspection after a new pond at Åukom flooded the woods of TrÄ…bczyn, now the
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
  TrÄ…mpczyÅ„ski and Åukomski families; the CheÅ‚mski family curated). For the tools: a shared
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
  largest, about sixty words on leaf 709 verso, is the court's finding that CheÅ‚mski raided
  the inn with armed men. The English, which is the editor's, already had the right sense in
  most places and was changed in 32: 24 to add what had been dropped, seven where it had
  followed a misread word, and one where it read the Polish differently (two weeks in the
  tower, not twelve). One paragraph on leaf 680 which the English lacked was translated in
  session. The summary's sentence on CheÅ‚mski's sentence was rewritten and checked (18
  statements). The fonds and the archive's account of the castle court are on the holding's
  page. The folds the scans are cut at were found again, after the first ones proved to cut
  the line ends of left pages, and wait for the editor's approval
  (`review/app53170koningr145/folds/`). The dropped phrases are on a sheet for the editor
  (`review/app53170koningr145/dropped/`). Not published.

- **APP 53/17/0/-/Konin Gr.145 added** (2026-10-06), the first holding of the Prusimski era:
  the decree of the commission that the Polish parliament appointed in 1774 to settle the
  boundary between Antoni Prusimski's TrÄ…bczyn and the CheÅ‚mski brothers' Åukomia. It sat on
  the disputed ground from 13 September 1775 under Ludwik DÄ…mbski, voivode of BrzeÅ›Ä‡
  Kujawski, and its decree was entered there on 23 September 1776 and copied into a court
  book of Konin. One document, 122 pages, Polish with Latin. The 62 scans of openings were
  cut at the fold. The editor's transcription (modern Polish spelling, by paragraph) and the
  editor's own English translation were brought in page by page; the translation was not made
  again. At the editor's word the text had a light check: four of 121 written pages and the
  signatures were read against the scans, 23 readings corrected (one restores six dropped
  words on leaf 673, in both languages), a line of the title page added, and 93 dropped
  accents put right through the text. Summary in both languages, 16 statements checked;
  holding page in both languages; the era is now populated and the story page and the About
  page say so; a timeline entry for 13 September 1775. New person: Ludwik DÄ…mbski. New place:
  BrzeÅ›Ä‡ Kujawski. Three changes to the tools: a document longer than Python's CSV field
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

- Twenty-one holdings from the State Archive in PoznaÅ„ added in one run, 92 documents: the boundary decree of 1775 (Konin Gr.145), six entries of the land court's books of decrees (53/6/0/-/17, -/36, -/40, -/45, -/46, -/47), three of the castle court of Kalisz (Kalisz Gr.414, Gr.424, Gr.425), and the Konin castle court registers Gr.136, Gr.114, Gr.115, Gr.116, Gr.117, Gr.118, Gr.119, Gr.120, Gr.121 and the decree of 1782 in Gr.153. Each entry of a court book is a document. Not published: the editor reviews the folds, the page of changes and `docs/PRUSIMSKI_QUESTIONS.md` first.
- The editor's transcriptions and English translations are kept. Every holding was read against its scans, the short ones whole, four long ones (Konin Gr.117, Gr.118, Gr.153, Gr.119) by the light check, which their pages say. Each correction is logged with its reason, and `review/changes/` lists for the editor what changed and how much it matters.
- Readings that changed what the documents say: PaweÅ‚ Prusimski is Antoni's uncle ("Patrui", not "Patrii"; Konin Gr.117); the surveyor of 1782 is sworn ("jurato", not "jurisdictione"), and the sittings on the ground are "condescensio", not "conditio" (Konin Gr.153); the oath laid on Prusimski in 1783 is that the arrest did not reach his two men ("Arestum non praevenit"; 53/6/0/-/47, read with Konin Gr.119); the wood sold to Tracholz is oak (Konin Gr.120).
- What the holdings established together: the commission of 1775 ended in two decrees, one for each side (Konin Gr.116, Gr.117); the Crown Tribunal decided between them on 23 January 1782 and confirmed it on 17 October 1782, and forty-one mounds were raised from 30 November to 3 December 1782 (Konin Gr.118, Gr.153). The About page, the story page and the era's blurb say so now; they said that the decree of 1775 fixed the boundary.
- `pipeline/intake/courtbook.py` (new): the shared steps of a court-book holding, from cutting the scans to the summaries, driven by one `intake/holding.py` per holding. `pipeline/review/changes_page.py` (new): the page of changes. Dates may be taken from the heading of the court's sitting (`dates: sitting` in rulings.yml). Kinds of document added: report, delivery, protest.
- The translation check no longer takes a chestnut mare ("Equam Castaneam") for a misread "hypocaustum".
- Figures: 564 documents on 1,832 pages in 36 holdings, 1589 to 1832; 86 in Latin; 912 marks of doubt; 559 translated.
- **The editor's second review of the Prusimski-era run (2026-10-07).** At their word the four holdings that had only the light check were read through against the scans: Konin Gr.117 (159 more corrections), Gr.118 (133), Gr.153 (106) and Gr.119 (8). The record of each is `intake/full_check.json`, applied by `holding.py --full` (`courtbook.full_check`). No document is marked as a rough reading any more; the marks of doubt in the edition fell from 912 to 743. What changed the sense: in the Tribunal's decree of 1782 OrÅ‚owski is sentenced to pay Prusimski, not the reverse, the two officers are boundary chamberlains, and words passed over in the ruling on Martin Hunt are restored (Gr.153); in CheÅ‚mski's protests of 1778 "jurto" is an oath, not a jurisdiction, and "pro invalibili" is "invalid" (Gr.117); three lines restored in the protest against the land court of 1782, and Teresa BogdaÅ„ska is the successor of her two late sisters (Gr.118).
- Two entries the editor had photographed were transcribed and translated in session and added as documents: 53/6/0/-/46 entry no. 17 (the land court's decree of 1777 on the debt CheÅ‚mski bought from the merchant Tracholz) and 53/6/0/-/47 entry no. 43 (a hearing on the ground fixed in 1784 for the boundary of Biskupice and ÅomÃ³w, with Prusimski cited).
- Jakub GÃ³rski, boundary chamberlain of InowrocÅ‚aw, has his Polish form in the English; the transcription keeps "Gorski" (the editor). PaweÅ‚ Prusimski as Antoni's uncle, "jurato" and "condescensio" confirmed by the editor.
- The fonds of 53/6 ("KsiÄ™gi sÄ…du ziemskiego w Koninie") and 53/15 ("KsiÄ™gi sÄ…du i urzÄ™du grodzkiego w Kaliszu"), with the archive's description, are on the nine holdings' pages; the Skanoteka watermark is noted on the nine holdings whose photographs carry it.
- The page of changes marks what was written after the editor read it ("New"), and counts it at the top.
- In 53/6/0/-/47, entry no. 26, Prusimski's proxy is "Zeromski" (Wojciech Å»eromski), on the witness of entry no. 43 (the editor, 2026-10-07).
- Entry no. 43 of 53/6/0/-/47, added earlier the same day, was taken out again at the editor's word: it is a suit between SkÃ³rzewski and CheÅ‚mski over the boundary of Biskupice and ÅomÃ³w and not relevant to the project. Its text is kept in the holding (`intake/entry_43.md`), because the reading "Zeromski" in entry no. 26 rests on it.
- Figures: 565 documents on 1,833 pages in 36 holdings; 739 marks of doubt; 560 translated.
- **The spot sheet "Before publishing"** (fourteen rows across the holdings, answered by the editor on 2026-10-07; `docs/PRUSIMSKI_before_publishing.csv` and `..._answers.json`). Readings settled against the page: in 53/6/0/-/46, entry no. 17, "Vitkovien~" and "initorum"; "Laetare" there and "Invocavit" in Konin Gr.117 both stand, so the two documents disagree on the day of the hearing; the search of the 28th of October stands; in Rajewicz's protest (Konin Gr.116) the editor reads "Cumque", and "Citraque", "without his consent", is withdrawn from the text, the English, the summary and the holding's page. Confirmed as built: the closing sentence of 53/6/0/-/47 no. 26, the tower sentence and the paragraph on leaf 680 in Konin Gr.145, the note on leaf 266 verso in Konin Gr.118, the Kinos entry in Konin Gr.120. "Capitaneus" is "Starost" throughout the English of Konin Gr.119.
- **The timeline takes in the Prusimski era** (2026-10-07, at the editor's word): sixteen events from 1589 to 1788, one per matter, each linked to its documents, in English and German. The page had begun at 1794, so the one earlier entry (the commission of 1775) had never been shown, and it still said that the commission fixed the boundary; it is rewritten (the commission ended in two decrees). Years before 1794 appear only where they have documents or an event.
- **The timeline has a band where each era begins** (1589, 1794, 1807); the Prusimski years end and the Hohenlohe-Ingelfingen years begin with Prusimski's flight after the KoÅ›ciuszko Uprising (the editor, 2026-10-07).
- **Oe 1 BÃ¼ 9454, letters 245 and 289: the archive's new scans** (2026-10-07). The images are replaced (289 is now pages 0522_b and 0522_c), the text is corrected against them line by line with the editor's new transcription beside it, the English is revised and the summaries are written again. Letter 245 gains the last line of its first page and is no longer marked as a rough reading; marks of doubt fall from 14 to 6 in 245 and from 13 to 1 in 289 (737 to 717 in the edition). The editor then answered a spot sheet on six words of 245 (2026-10-07): "praedikat", "dringen[?]", "ErrÃ¶then[?]", "aus der B[...] Casse"; two readings stand. On four words of 289 (2026-10-08): "zu Brieg", "Heneberg"; "bitte" and "Circa" stand (719 marks of doubt in the edition). Published at the editor's word on 2026-10-08, with the timeline.
- **The Prusimski-era holdings were published at the editor's word on 2026-10-07**: twenty-one holdings, 93 documents, 1589 to 1788. Figures: 565 documents on 1,833 pages in 36 holdings; 737 marks of doubt; 560 translated.
- **AGAD 1/169/0/1/1745 added** (2026-10-13; not published): six pages of a Prussian table of the villages around Konin, of about 1797, entries 140 to 303, with the houses, churches and Christian and Jewish inhabitants of each place and a total at the foot of every page. There was no transcription: the table was read from the editor's three scans in the working session and is kept in `units/agad1169011745/intake/table.csv`, from which the text, the English version and the editor's checking spreadsheet (`review/agad1169011745/table_check.xlsx`, a picture of each line beside its row) are made. Every line and every page total adds up as read. The site's tables now take a heading of three levels and set off a page's own total (`unitlib.render_table`); the English of a table may translate its heading (`publish_translations.py`). "Kurow Koninsk." and the village "Ostrow" are shut out of the place entries for Konin and OstrÃ³w. Figures with it: 566 documents on 1,839 pages in 37 holdings; 725 marks of doubt; 561 translated. Waiting for the editor's check of the table.

## The summaries of Oe 1 BÃ¼ 14525 and 14526 written again (2026-10-08)

- At the editor's word, in a working session and at no cost: the 74 documents of the two Neuenstein volumes were read whole in their German text and summarised afresh in German, and the English summaries translated from the German. The first summaries had been written by the model from the English translations and never checked. Each statement was then held to its document (212 in Oe 1 BÃ¼ 14525, 182 in 14526; each holding's `intake/claim_check.yml`). Every holding's summaries have now been written from the original language and checked; the edition guide says so in both languages, and the two holdings' pages say how theirs were made.
- Oe 1 BÃ¼ 14525, document 7: the Government at Kalisz attested the copy on 7 July **1801**, not 1804; corrected against the scan (0021_a2) in the transcription and the English. Documents 3 and 4 were checked against the scans: both copies of the grant of 1796 name only Kamionna, Kolno and Brzyce in the deed's text, as transcribed.
- Two dates on the site that are not the documents' own (14525, documents 13 and 21) stay as they are (the editor, 2026-10-09).
- Oe 1 BÃ¼ 14526, document 26: the third party is **Kriede**, not "Reise" (the editor, 2026-10-09; the protocol is signed Jacob Kriede); corrected in the transcription, the English and the summary. Not yet published.

## AGAD 1/169/0/1/1745 checked by the editor and published; the cloud branch merged (2026-10-13)

- **The editor checked the table of villages line by line** on the spreadsheet with a picture of each line: 25 names corrected (most of them a mark on a letter the first reading had missed: KuÅºnica, Åomow, MyÅ¼akow, OÅ›iek, PÄ™poÄ‡in, SÅ‚ugoÄ‡in; and LÄ™ka, SiÄ…szyce, Siekierszyn, Sierszew, "Groi.", "TrÄ…mpczyn."), the six "[?]" taken away, 24 notes of doubt cleared, no figure changed. The list is in `units/agad1169011745/notes.md`. Two periods that went with the "[?]" were put back from the scan ("Leysce.", "LÄ™ka."). "Szyman." is short for Szymanowice (the editor); the text keeps the short form. The folds stand as proposed.
- **A clean spreadsheet of the table, to keep**: `units/agad1169011745/AGAD_1_169_0_1_1745_table.xlsx`, made by `holding.py --archive` from the reading: the table as written, the table in English, and a sheet on the source and the conventions; values only.
- `holding.py --take` now brings back the editor's "Doubt" column too, and `--xlsx` refuses to write over the spreadsheet the editor saved.
- **`claude/peaceful-meitner-snu6qx` merged into `main`**: the summaries of Oe 1 BÃ¼ 14525 and 14526 written again and claim-checked, and the two corrections with them (the section below). The other three cloud branches had nothing that `main` lacked. The two holdings' `summaries_draft.py` were run on the desktop so that its cache holds the new summaries.
- **Published at the editor's word.** Figures: 566 documents on 1,839 pages in 37 holdings; 719 marks of doubt (the new holding has none); 561 translated.

## Two holdings from the State Archive in PoznaÅ„ added (2026-10-13; not published)

- **APP 53/968/0/-/783**: a printed summons in Polish, served on 7/19 October 1860 on Karolina Fridenberg of the Staro-ÅaziÅ„ska colony, by which Count WÅ‚odzimierz MiÄ…czyÅ„ski of TrÄ…bczyn counterclaims before the Civil Tribunal at Kalisz against 97 colonists and asks that Hohenlohe-Ingelfingen's contract of 18 May 1805 with fourteen colonists be held not to bind him. One document on five pages, with the archive's cover. The editor's Polish was read against the scans on every page: 34 corrections and five lines in the court messenger's hand added. The editor's English was a machine's and wrong in substance (the summoning verb, "father" for "husband", "manor" for "court", fourteen holdings for eleven); it is written again from the corrected Polish, and `units/app539680783/intake/changes.yml` lists the differences for the page of changes. Summary in both languages, claim-checked (17 statements, one weakened); a timeline entry and a paragraph in section VIII of the era essay.
- **APP 53/64/0/-/Kalisz Tab.21**: thirteen pages of the register of the hearth tax of the Kalisz voivodeship for the St John's instalment of 1789, 387 entries of the Pyzdry, Kalisz and Konin districts; TrÄ…bczyn is entry 178 (80 zÅ‚oty), with Åazy, Osiny, Nowa WieÅ› and its OlÄ™ders after it, and Åukom entry 106. There was no transcription: the register was read from the scans in the working session (`units/app53640kalisztab21/intake/table.csv`) and waits for the editor's check on a spreadsheet with a picture of each line. The pages have no totals; the sums are held by the rate of the tax instead (a multiple of 3 zÅ‚ 15 gr, or of 2 zÅ‚ 15 gr on leaves 18 to 20). The file named `017v.jpg` is placed as leaf 9 verso, by its receipt numbers.
- **The site**: the document kind "summons"; the timeline runs to 1860 and shows a year after 1832 only if it has a document or an event; a district's name directly above the first entry of a table is a row of the table (`unitlib.table_of`); a glossary entry for the court messenger (woÅºny, ministerialis), which marks 41 documents; Count WÅ‚odzimierz MiÄ…czyÅ„ski and the Zelmer family on the people page; the 1860 print's spellings of Prusimski and Weigel matched; five entries shut out of the register, where they matched village names.
- The archive's descriptions of both fonds are in `reference/sources/`, with working translations.
- Figures with them: 568 documents on 1,857 pages in 39 holdings; 759 marks of doubt; 563 translated; sixteen documents in Polish; the edition now runs from 1589 to 1860.

## The editor's answers on the two PoznaÅ„ holdings worked in (2026-10-14; not published)

- **APP 53/64/0/-/Kalisz Tab.21**: the editor checked the hearth-tax register line by line on the spreadsheet with a picture of each line. 69 names corrected, no figure changed; the twelve figures off the rate of the tax confirmed as read; 13 names keep "[?]" (45 before). Three names the first reading had shortened are written in full on the page (Jerzmanowskiego, BardziÅ„skiego, z MÅ‚ynem). The text, the English (three new forms in the word table), `process.md` and the page brought into line; the clean spreadsheet made (`units/app53640kalisztab21/APP_53_64_0_Kalisz_Tab_21_register.xlsx`). `017v.jpg` is leaf 9 verso (editor). The list of corrections is in the unit's `notes.md`. Publishing the English again also mended its table: the version on file had been published before the heading was settled, without the printed title.
- **APP 53/968/0/-/783**: the folds approved as proposed. Count WÅ‚odzimierz MiÄ…czyÅ„ski was Michalina MiÄ…czyÅ„ska's son (editor): in his biography and on the holding's page.
- **The OlÄ™der colonies of TrÄ…bczyn** (editor): two colonies, first TrÄ…bczyÅ„skie Stare / Nowe OlÄ™dry, later ÅaziÅ„skie Stare / Nowe OlÄ™dry, in several spellings; Åazy is a separate village. The summons' Staro- and Nowo-ÅaziÅ„ska colonies are matched to the two place entries, and Åazy is kept apart from both. A paragraph on this in the pages of both holdings.
- **The tailed sign at the end of a name in the register** is the clerk's sign for an ending such as -skiego (editor): "KiedrowÄ™" (twice), "TrzebiesÅ‚awÄ™" and "SiedliskÄ™" now stand as "Kiedrow:", "TrzebiesÅ‚aw:" and "Siedlisk:", given as a colon like the same sign elsewhere in the register.
- **"Haul. Lazy."** in the table of about 1797 (AGAD 1/169/0/1/1745, no. 150) is probably the ÅaziÅ„skie OlÄ™dry, not the village of Åazy (editor). Recorded; not matched to either colony.
- **A spot sheet for the summons**, "Pen marks on the summons": the six places where the court messenger wrote on the print, each with a picture.
- Figures: 568 documents in 39 holdings; 727 marks of doubt.

## APP 53/968/0/-/669 added: Albert Breyer's notebook of July 1936 (2026-10-14; not published)

- **APP 53/968/0/-/669**: a pencil notebook of 35 pages in German from the papers of Albert Breyer, written in ÅaziÅ„sk and Emilienheim, German settlements of the commune of TrÄ…bczyn, with a log of his photographs at the back. Only the notebook whose scans are in the folder "Notes on ÅaziÅ„sk" (editor); the editor's English notes beside it belong to another notebook of the unit and were not used.
- There was no transcription: read from the scans in session (88 marks of doubt), translated, summarised in both languages and claim-checked (16 statements, two weakened); holding page in both languages. A spot sheet of ten readings, with pictures, for the editor.
- The name list made from the corpus no longer takes a word cut by the line-break mark ("EmilienÂ¬heim" was found as Emilie); nothing else in the edition changed. Neumann, Geheimer Finanzrat Schulze, Holland and Warszawa shut out of this document.
- "geb." ruled out of the glossary (geboren).
- Figures: 569 documents on 1,892 pages in 40 holdings, 1589 to 1936; 815 marks of doubt; 564 translated.

## Glossary: Matura (2026-10-14)

- A glossary entry for the Matura, the school-leaving examination, at the editor's word, in English and German; it marks the word in Breyer's first notebook (page 28). To be checked against the Encyklopedia PWN. Published.

## APP 53/968/0/-/669: the editor's corrections to the first notebook (2026-10-14)

- The editor read the English of Breyer's first notebook against the scans: Grodziec and Ciswica for Smaszew and Czarnica, GrÄ…dzeÅ„, MoraÃŸ, Ed[uard] Zelmer, ChruÅ›ciki, Kinder and Birke in the photo log, and others; the order of some lines; the German of the sayings kept beside the English; the inside back cover read again with the editor and completed (`units/app539680669/intake/editor_corrections.py`).
- Years from 1900 on were shown with a thousands comma ("1,907"): `numerals.py` now takes 1500 to 1999 as years.
- The English naming rule for TrÄ…bczyn no longer rewrites a spelling quoted from the page ('written "TrÄ…pczyn"'), which a run of it had done in two summaries; both kept as they were.
- Figures: 812 marks of doubt.

## APP 53/968/0/-/669: a second notebook added and published (2026-10-14)

- **Document 2**, Breyer's notebook "V. Grodziec Juli 1936", from the editor's raw photos IMG_5192 to IMG_5205: 25 pages read in session (33 marks of doubt), English, summary in both languages claim-checked (15 statements, three weakened), the holding's page and title for two notebooks. The camera's full-size picture inside each raw file was used; the last photo, flagged by the camera as turned, is upright inside the file.
- A spot sheet of 15 readings for the editor. Koppe, KÃ¼ster and StanisÅ‚aw MiÄ…czyÅ„ski shut out of the new document; the glossary's Morgen takes "Mor." after a figure.
- Figures: 570 documents on 1,917 pages in 40 holdings; 828 marks of doubt.
- The editor's answers on the sheet of 15 readings worked in (Brudzewo, Kirschhacker, Swirkhaber, Chocz, Firstgugge and others); 824 marks of doubt. Three rows asked again on a short sheet and answered (Rheinâ€¦, "Die nach ins Posenschen gehen", Dachgugge). Published at the editor's word; 823 marks of doubt.

## Three holdings published (2026-10-14)

- **APP 53/968/0/-/783** (the summons of 1860), **APP 53/64/0/-/Kalisz Tab.21** (the hearth-tax register of 1789) and **APP 53/968/0/-/669** (Albert Breyer's notebook of 1936) published at the editor's word, with the two new eras under working names and the timeline to 1936. Figures: 569 documents on 1,892 pages in 40 holdings, 1589 to 1936; 795 marks of doubt.

## The editor's answers on both spot sheets; two new eras (2026-10-14)

- **APP 53/968/0/-/783**: no. 58 is Marcina Heck, no. 70 Krystofa GrÃ¼nwald (the court messenger's pen over the printed "ja"), the note of costs 47 roubles 21 kopecks; the other pen alterations stand as printed. Text, English, process pages and the page of changes brought into line (`intake/spot_answers.py`).
- **APP 53/968/0/-/669**: seven of ten doubtful readings settled by the editor, three differently from the first reading (Wagelt, Hormann, Neumann L. 1889); WÅ‚odzimierow in the list of the school community. 83 marks of doubt remain.
- **Two new eras** at the editor's word, under working names until the editor names them: "The estate under WÅ‚odzimierz MiÄ…czyÅ„ski" (`wlodzimierz`), the era after Michalina, with the summons of 1860; "The twentieth century" (`twentieth-century`), with Breyer's notebook. Each has its band on the timeline, which now runs to 1936, and its section on the story page, in both languages.
- Figures: 808 marks of doubt.
- **APP 53/968/0/-/669, the second sheet**: 29 of the most uncertain readings put to the editor; 22 changed or settled. StraÅ¼niki is a village (not the name Krainik), Noga a field name (not Kroge), SwiÄ™cer of SwiÄ™cia (not SmiÄ™cer), MÃ¼hle (not MÃ¼ller). 70 marks of doubt remain; 795 in the edition. A third sheet of three readings on Breyer's Sm and Sw: the editor read SwiÄ™cia twice where the first reading had SmiÄ™cia, and St[y?]pin.

## APP 53/968/0/-/716 added, not published (2026-10-14)

- **APP 53/968/0/-/716**, Albert Breyer's notebook "ÅaziÅ„sk, Emilienheim, Ð›Ð¸ÐºÐ²Ð¸Ð´Ð°Ñ†. Ñ‚Ð°Ð±ÐµÐ»ÑŒ", with a loose sheet of 1858, from the editor's raw photos IMG_5159 to IMG_5180: eleven documents by content (the editor's choice), six of them tables. Breyer's Russian copies of the liquidation tables of Emilienheim (28 March 1868), ÅaziÅ„sk (SÅ‚upca, 29 June 1868, 91 holdings, 1,691 Morgen 219 rods, with his pencil of who held each holding in 1875) and Orliny (of Count Albert Taczanowski), and of the servitudes of ÅaziÅ„sk and Orliny; his counts of farmers and Morgen of ÅaziÅ„sk from 1840 to 1935; his German notes of July 1935 and July 1936 on Orlin, JÃ³zefÃ³w, Huta TrÄ…bczyÅ„ska and their people; a list of the farmers of the Orlin Hauland Biskupice; and the Polish list of the hearth tax of Emilienheim, Kopojno, 3/15 December 1858.
- Read from the photos in session (68 marks of doubt), translated, summarised in both languages and claim-checked (83 statements, 16 weakened or cut); holding page in both languages, a timeline entry for 29 June 1868, a paragraph in the story and the era's blurb. Breyer's own total on one page is 6 Morgen more than his figures; the summary says so.
- Tables: a table's title or totals standing on a page of their own now show there, a heading row that is only a title joins the caption, and a single row of column labels is shown as one heading row. Every other table of the edition renders as before. Line breaks in Russian are now decided, a figure ending in a hyphen in a table is no longer taken for a broken word, and tables are left out of the catchword check.
- A spot sheet of 17 readings for the editor. Kl., Wirte and dt. ruled out of the glossary; Kuh and Neumann shut out of the documents where they are not the people of the name list.
- Figures: 581 documents on 1,951 pages in 41 holdings, 1589 to 1936; 880 marks of doubt; 576 translated. Not published.

## Copies take the era of what they copy (2026-10-14)

- **The editor's ruling**: a copy belongs to the time of the document it copies, not to the date of the copy or the holding it is in ("a copy of an 1828 document from 1939 should not belong to the 20th century"). Recorded in `reference/eras.yml`.
- **APP 53/968/0/-/716** brought into line: two documents that held one of Breyer's copies and his own notes together were divided (now thirteen documents). The sheet of 1858, the liquidation tables of 1868, Breyer's extracts of 1870 and 1892 (now dated 26 November 1870) and his copies of the servitudes of ÅaziÅ„sk (dated 1868) and Orliny now stand in the era of WÅ‚odzimierz MiÄ…czyÅ„ski; Breyer's own notes and figures stay in the twentieth century. The story page and both era descriptions follow. No other holding has a copy dated by its copying: APP 53/968/0/-/801 and I. HA Rep. 162 Nr. 295 already carry their originals' dates.
- Figures: 583 documents; 880 marks of doubt; 578 translated. Not published.

## APP 53/968/0/-/716: the editor's answers; Michalina's and WÅ‚odzimierz's dates (2026-10-15)

- The editor answered the spot sheet of 17 readings in Breyer's notebook: 13 settled or changed (the renaming of Emilienheim in 1892, the commune of TrÄ…bczyn in the heading of the ÅaziÅ„sk table, Jesswein among the first farmers of JÃ³zefÃ³w, Maradza, HolÄ™dry Orliny Biskupicki, Skrzydlewski, Tilson, Seling, Polzfu[h?]l, "Bankrott geworden", and most of the heading of the Orlin list). Text, English, four summaries and the holding's pages follow. 55 marks of doubt remain in the notebook, 867 in the edition.
- **Dates from the editor**: Michalina MiÄ…czyÅ„ska, born Prusimska, died on 19 January 1851; her son WÅ‚odzimierz on 20 December 1879, and his nephew WÅ‚adysÅ‚aw MiÄ…czyÅ„ski became heir of TrÄ…bczyn. In the people's notes, the era's description (now 1851 to 1879), the story and the timeline note; the era's band on the timeline now begins at its first document, 1858, and the twentieth century's at 1935.

## APÅ 39/98/0/-/6603 added, not published; the liquidation era (2026-10-15)

- **APÅ 39/98/0/-/6603**, from the State Archive in ÅÃ³dÅº, the first holding from there: the liquidation table of the ÅaziÅ„sk colony, confirmed 8 February 1868 (91 farmsteads, 1,691 Morgen 219 rods, liquidation capital 10,055 roubles 70 kopecks), its copy of 1869 with the servitudes, the inscription of 1884 on fuel and pasture, the certified copies of the inscriptions of 1894 (the servitudes given up to Countess Maria Wielopolska for 393 Morgen 154 rods) and 1897 (the survey of 1896), and the statement of each farmstead's land after the survey. Six documents at the editor's word, three of them tables; the openings where the writing runs across are shown as one page.
- Read from the scans in session (24 marks of doubt), checked by the table's own sums; translated, summarised in both languages and claim-checked (46 statements, two corrected); holding page in both languages.
- **The liquidation era** (`liquidation`, working name) at the editor's word: the enfranchisement of 1864 and the settling of the servitudes, which began under WÅ‚odzimierz MiÄ…czyÅ„ski. The new holding and Breyer's copies of the tables and servitudes in 53/968/0/-/716 stand in it; the story has a section for it, the timeline a band from 1868, an entry for 8 February 1868 (moved from 29 June, the date of Breyer's source) and a new one for 1894.
- The State Archive in ÅÃ³dÅº in the repositories and on the credits page, and the Central Archives of Historical Records, which was missing from the credits. Two new relation kinds, "Copy of" and "Entered in".
- Figures: 589 documents on 1,974 pages in 42 holdings, five archives; 891 marks of doubt; 584 translated. Not published.

## APP 53/968/0/-/716: the editor's answers on the second sheet (2026-10-15)

- 18 of the 47 readings answered and worked in: Ð”Ð¸ÐºÐ³Ð¾Ñ„ÑŠ, Ð”Ð¸ÐºÐ¾Ð½Ñ„ÑŠ, ÐšÐ¸Ð½Ð°ÑÑ‚ÑŠ, ÐžÐ±ÑÑ‚ÑŠ, Ð“Ð¾Ñ‚Ñ‚Ð»Ð¸Ð±ÑŠ, Ð”ÐµÑ‚., "Eingeschrieben jedoch", Ð¦ÐµÐ»ÑŒÐ¼ÐµÑ€ÑŠ Ð“Ð¾Ñ‚Ñ„., Ð¨Ð¼ÐµÑ…ÐµÐ»ÑŒ (Schmechel), and "nur[?]" twice. 46 marks of doubt remain in the notebook, 882 in the edition. The other 30 rows stay on the sheet, with two words the original table of 1869 now settles (Ð¿Ð»Ð°Ñ…Ñ‚Ð°Ð¼Ð¸, Ð½Ð°Ð»Ð¸Ñ‡Ð½Ñ‹Ð¹) put to the editor.

## Breyer's ÅaziÅ„sk table read against the original (2026-10-15)

- At the editor's request, every row of Breyer's copy of the ÅaziÅ„sk liquidation table (APP 53/968/0/-/716, document 4) compared with the original (APÅ 39/98/0/-/6603). Most differences were misreadings of Breyer's hand and are corrected: figures at nos. 11, 12, 20, 44, 51, 52, 60, 61, 65 and 87, the names Ð¡Ð°Ð½Ð¸ÐºÐ¾Ð²ÑÐºÑ–Ð¹, ÐŸÑ€Ð¾Ð¼Ð¸ÑÑ‚ÑŠ, Ð¦ÐµÐ»ÑŒÐ½ÐµÑ€ÑŠ, Ð¨Ñ‚Ð¸Ñ€Ñ†ÐµÐ½Ð±ÐµÐºÐµÑ€ÑŠ and Ð¤ÐµÑ‚Ñ‚ÐµÑ€ÑŠ, and Ð½Ð°Ð»Ð¸Ñ‡Ð½Ñ‹Ð¹ and Ñ‚Ð»Ð°Ñ…Ñ‚Ð°Ð¼Ð¸ in the servitudes. Breyer's own departures from the original stand as he wrote them and are listed in the notes. In the original, no. 43 is ÐœÐ°Ñ‚ÐµÑƒÑˆÑŠ in all three witnesses.
- Marks of doubt: 44 in the notebook, 21 in the original, 877 in the edition.

## Zelmer with m, Breyer's names to the original, the rest of the second sheet (2026-10-15)

- The editor's ruling: Zelmer is always written with m ("there's no Zelner, ever in this project"). Ð¦ÐµÐ»ÑŒÐ¼ÐµÑ€ÑŠ at nos. 37, 50, 53, 65 and 67 in both holdings, in the table, its copy and the statement of APÅ 39/98/0/-/6603 and in Breyer's copy (APP 53/968/0/-/716, document 4); the change to Ð¦ÐµÐ»ÑŒÐ½ÐµÑ€ÑŠ the day before is undone.
- The editor's ruling: names in Breyer's copy of the ÅaziÅ„sk table follow the original's spelling, not Breyer's: ÐœÐµÑ€Ñ†ÑŠ (for ÐœÐµÑ€Ð¶ÑŠ), Ð¡Ð°Ð½Ð¸ÐºÐ¾Ð²ÑÐºÑ–Ð¹ ÐœÐ°Ñ€Ñ†Ð¸Ð½ÑŠ (no. 9), ÐœÐ°Ñ€Ñ†Ð¸Ð½ÑŠ (for ÐœÐ°Ñ€Ñ‚.), ÐšÐ½Ð°Ñ„ÐºÑƒÑÑŠ, Ð¨Ñ‚Ð¸Ñ€Ñ†ÐµÐ½Ð±ÐµÑ…ÐµÑ€ÑŠ, ÐœÐ°Ñ‚ÐµÑƒÑˆÑŠ (no. 43), Ð”Ð°Ð½Ñ–Ð¸Ð»ÑŠ (no. 60), the genitives ÐšÐ¸Ð½Ð°ÑÑ‚Ð° and Ð¢Ð°Ñ€Ð½Ð¾Ð²ÑÐºÐ°Ð³Ð¾, and in the pencil Ð¨ÐµÐ¹Ð½Ñ„Ð¸ÑˆÑŠ and Ð“Ð¸Ñ€ÑˆÑŠ. What Breyer wrote is listed in the holding's notes and on its "How it was made" page. His figures stand as he wrote them.
- The editor's answers on the last 28 rows of the second sheet worked in: Brenda, "schlagen sich", Gottfr., Ð’Ð°Ð½Ð³Ð¾Ð»ÑŒÐ´ÑŠ, Ð¡Ñ‚ÑƒÐ´Ð·ÐµÐ½ÐºÐ°, "1909 9 Nov. hat das aufgehÃ¶rt", "mit d.", Ð’ÐµÐ»ÑŒÐºiÐ¹ Ð±Ð¾Ñ€ÑŠ read without doubt; [Ð‘Ð¾Ð½Ñ†Ð»ÐµÑ€ÑŠ?], [Ð“Ñ€ÐµÐ´ÑŠ?], [â€¦etliâ€¦?], [Solten?], [Zoget.?], [Crist.?] and [Ñ‚Ð¾Ð¿Ð¾Ñ€ÑŠ?] (an axe) changed with their doubt; eleven kept as they were.
- Marks of doubt: 35 in the notebook, 21 in the original, 868 in the edition.

## Breyer's figures to the original; Zelmer in the index (2026-10-15)

- The editor's ruling: the original liquidation table is the authority for the numbers too. Every figure of Breyer's copy (APP 53/968/0/-/716, document 4) compared with APÅ 39/98/0/-/6603; four differed and now follow the original: no. 12 122 rods (read 222), no. 29 188 (read 184), no. 46 38-66 (read 38-61), and nos. 47 and 48 in the original's order. The notes record what was read.
- At the editor's word, the Zelmer family in the people index now also matches Ð¦ÐµÐ»ÑŒÐ¼ÐµÑ€ÑŠ: the table, its copy and the statement of 6603 and Breyer's copy are linked to the family, and its bio names the five holdings of 1868.

## Page edges approved; a spot sheet for the original table (2026-10-15)

- The editor let the folds and page edges of APP 53/968/0/-/716 and APÅ 39/98/0/-/6603 stand ("The page edges look fine").
- All 21 marks of doubt in APÅ 39/98/0/-/6603 put on a spot sheet, "Doubtful readings in the liquidation table of ÅaziÅ„sk": 16 rows, each with a picture, the signatures that recur under three documents asked once.
- The editor's answers worked in: the pencil figure under the table (10055 70), Ð“Ð»ÐµÐ±ÐµÐ»ÑŒ (no. 2 of the copy) and Ð¡Ñ‚ÑƒÑ€Ñ†ÐµÐ½Ð±ÐµÐºÐµÑ€ÑŠ (no. 19 of the copy) read without doubt; the rest, among them all eleven signatures, kept with their doubt. Marks of doubt: 18 in the original, 865 in the edition.

## Published (2026-10-15)

- At the editor's word, APP 53/968/0/-/716 (Breyer's ÅaziÅ„sk notebook) and APÅ 39/98/0/-/6603 (the liquidation table of ÅaziÅ„sk) published together: 589 documents in 42 holdings, 865 marks of doubt, with the new era `liquidation`.

## Oe 1 BÃ¼ 9454, letter 9 (2026-10-15)

- Letter 9, marked "skipped" since the holding was built, added from the editor's transcription: a single leaf in Triebenfeld's hand, holed and with a folded corner, 18 lines with 17 places of lost text and 3 marks of doubt. Read against the scan; where the editor's file and the scan differed the scan decided (Borgen, BÃ¶sewicht, schÃ¤ndlich, weiÃŸ, betreibe ... durch ihn), and those places are on a spot sheet for the editor. Dated to about January 1815 at Vienna, Triebenfeld to the Prince; English and summaries written in session. Not published.
- The editor's answers on the spot sheet worked in: seven readings confirmed, St[aats]. K[anzler]. F[Ã¼rst]. H[ardenberg]. confirmed and expanded, [seie?], [Kedl?] and [weiÃŸ?] marked as doubtful. Four marks of doubt.
- Letter 300 made again from the editor's new crops and transcription: the restored edges give the line starts of page 1 and settle gerÃ¼ffelt, zurÃ¼ck, die Piece, kÃ¶mt, Peterbourg, gÃ¤rstig, Ciszewska and voll; the dateline reads "d 20t Januar", and the archive's pencil note "20. Jan 1816" dates it. Marks of doubt 25 to 18; English revised in session. The edition counts 879. Not published.
- Letters 9 and 300 published at the editor's word (2026-10-15).

## ADWÅ‚ 85: the visitation of the parish of TrÄ…bczyn (2026-10-15)

- A new archive and a new holding: nine pages of the volume of the visitation of the Konin deanery of 1790 and 1791 (Diocesan Archive in WÅ‚ocÅ‚awek, signature 85), the pages the editor's transcript covers. Two documents at the editor's word: the parish of TrÄ…bczyn, and the table of the souls of the parish of ZagÃ³rÃ³w. Era `prusimski-boundary`.
- At the editor's word, the passages of these pages the transcript left out were transcribed in session; every page then read against the scans. A dropped phrase restored (leaf 24: Kalisz 5 miles, Konin 2); the editor's expansions of titles ("Jego WysokoÅ›Ä‡ Magnifici") replaced by the abbreviations as written. All figures of both tables agreed. 12 marks of doubt, on a spot sheet.
- English and summaries written in session; 34 statements claim-checked. Holding page in both languages; timeline entry for 1791; the edition guide, the story page and the era's blurb brought up to 591 documents in 43 holdings and six archives, 891 marks of doubt. The 1788 timeline entry no longer calls itself the last document of the Prusimski years.
- Index: Katarzyna Prusimska (the Chamberlain's wife who enlarged the church), Antoni Prusimski, the TrÄ…mpczyÅ„ski family, seven new people; the parish's places; "po SwiÄ™cie" shut out of SwiÄ™cia and "Komornikow" (cottagers) out of the glossary's komornik. A document type "visitation"; an archive with no website is credited without a link.
- Not published.

## ADWÅ‚ 85: the spot sheet, published (2026-10-16)

- The editor answered the spot sheet "Doubtful readings in the visitation of TrÄ…bczyn": obok, trumnÄ…, BogusÅ‚awskiego, GolinskÄ…, DrÄ™zgi, Illust:, Gralewska, 58 and rozrzÄ…dzonÄ™ settled; Kozierog[?], UÅ‚a[?] and podciorze[?] kept with their doubt (`units/adwl85/intake/spot_answers.py`). 3 marks of doubt remain in the holding, 882 in the edition. BogusÅ‚awski and GoliÅ„ska added to the index.
- The reference stays "ADWÅ‚ 85": the archive's holdings have no series name (editor).
- Published at the editor's word: 591 documents in 43 holdings.

## Kuryer Polski 1754, nr 75: the funeral of PaweÅ‚ Prusimski (2026-10-16)

- The first holding from print and from a library: the report from Kalisz of 5 December 1754 in the Warsaw newspaper Kuryer Polski, no. 75 of 1754 (KÃ³rnik Library of the Polish Academy of Sciences, Cz2271, in the Wielkopolska Digital Library). Read from the editor's image in session, line by line with the printer's letters; one mark of doubt. Translated, summarised, claim-checked (11 statements), holding page in both languages, timeline entry, guide, story page and era blurb brought up to 592 documents in 44 holdings, 883 marks of doubt.
- A new repository `bkpan-kornik` (a library) and document type `newspaper`. ÅÄ™d is LÄ…d (editor): LÄ…d added to the places, which also links the boundary decree of 1775, the Prussian table of about 1797 and six contracts of Oe 1 BÃ¼ 14526. PaweÅ‚, Antoni and Katarzyna Prusimski matched in the print's spelling; the abbot GÅ‚owiecki added.
- Not published.

## Kuryer Polski 1754, nr 75: published (2026-10-16)

- The editor looked at the one doubtful word on the spot sheet and kept "[Cleri?]" as it stands. Published at the editor's word: 592 documents in 44 holdings, 883 marks of doubt.

## Kodeks Dyplomatyczny Wielkopolski: twenty-one medieval entries (2026-10-16)

- A new holding, `kdw`: twenty-one entries of the Kodeks Dyplomatyczny Wielkopolski, 1173 to 1440, from volumes 1, 2, 3, 5, 6, 7, 10 and 11 (volume 8 left out at the editor's word), each entry one document in order of date, given whole from the editor's file and not corrected. Text only, from the Wielkopolska Digital Library's electronic text; each page names its volume and number, linked to the volume.
- The editors' footnote marks are raised and their notes set apart on the site (`units/kdw/footnotes.yml`), without changing the text; both verifications allow for it.
- Estates tagged from the editor's sixteen; new places Szetlew and Adamierz; medieval spellings with their years for thirteen places, shown on the Places page. Thirteen people of TrÄ…bczyn added, each to its document.
- A new era `medieval`, "TrÄ…bczyn in the Middle Ages" (working name): on the timeline from 1173 with six events, on the story page, in the era list. English and summaries written in session; 107 statements claim-checked. Holding page in both languages; the edition guide brought up to 613 documents in 45 holdings, 2,005 pages, 1173 to 1936.
- Years before 1500 no longer get a thousands comma in the reading text and English of this holding (`numerals.YEARS_FROM`); no other holding changed.
- Not published.

## Kodeks Dyplomatyczny Wielkopolski: Imielno, published (2026-10-16)

- Imielno is an estate of focus (editor): a new place, matched also in its medieval form "Chemelino". The gift of the hospital of Gniezno (1243), which lists "Chemelino" among the hospital's villages, is tagged with it, and its summary and the holding page say so (claim check rewritten for that statement). Imielno also links the boundary decree of 1775, the protest of 1778 (Konin Gr.117) and the visitation of 1791.
- Published at the editor's word: 613 documents in 45 holdings, 1173 to 1936.

## The literature: six books, page by page (2026-10-19)

- A new kind of material, kept apart from the archival documents (`docs/LITERATURE_PLAN.md`): books and articles about them, each in its original language and in English, for questions such as whether Triebenfeld inflated the value of his estates. Six works from the editor's folder "Books", copied unchanged into `literature/<slug>/`, the English of all six Claude's (the editor): the Materialien of 1861 (with the black register of the gifted estates), Held's book of 1801, the Neue FeuerbrÃ¤nde of 1807, Paciorkowski's Latin treatise of 1776, Guradze's Der Bauer in Posen of 1898, and Seidel's book of 2018 on Hohenlohe-Ingelfingen.
- Each work has a `work.yml` (title, citation, language, how its pages are marked, an account in English and German) and a `notes.md` (how it came in, how the two files line up, a spot check of the English). `pipeline/literature/build_literature.py` cuts both files at the printed page marks, checks that the passages give back the whole file, and writes `corpus/literature/`: an index and one file per page and language. It runs in `regenerate.py` after the dataset.
- Seidel is under copyright: in the repository for questions but never shown on the site (`visible: false`; the editor, 2026-10-19, knowing that the repository is public). Until now `.gitignore` kept it out.
- Found on the way: Triebenfeld's entry in the black register (Materialien pp. 162-164) is about other estates than TrÄ…bczyn (Piotrow, Lasky and others). Guradze has no page numbers yet (the editor will correct the text); the English of Paciorkowski lacks the mark of p. 27.
- Nothing on the site yet. Not published.

## The literature on the site (2026-10-19, not published)

- "Literature" in the menu (German "Literatur"), after Sources: a list of the five visible works (/literature/, /de/literatur/), and a page for each with the original and the English side by side, passage by passage, each headed by its printed page and with its own anchor so that a page can be cited and linked (for example /literature/materialien1861/#p-162). Footnote markers link to their notes. Made by `pipeline/literature/literature_site.py`, a new step of `regenerate.py`; the plan's section 7 says how.
- Seidel (2018) has no page; `verify_site.py` now fails if its slug or title shows up anywhere in the built site, or if a visible work lacks a page.
- Built and verified on the desktop; not published.
- The book's title is the heading on the list and on each work's page, the citation ("Materialien (1861)") under it (the editor).

## The literature: who and which estates the books name (2026-10-19, not published)

- The edition's index of people and places run over the originals of the five visible works (`pipeline/literature/literature_index.py`, a new step of `regenerate.py`; LITERATURE_PLAN.md, section 8). Every one of the 2,690 hits was read and ruled in `literature/index.yml`: 2,508 stand. The rest are words, measures, regiments and other men of the same name, each with the reason.
- Forms the books print and the edition's patterns miss are added for the literature only: TrÄ…bczyn as "Trombczyn" and "Trobozyn" in the black register, Szetlewek as "Szellewen", Åšwiechocin as "Schwiegoszyn", ÅowyÅ„ as "LÃ¶win", Krotoszyn as "Krotoczyn" and others, the Prince as "Hohenloh".
- On /people/ and /places/, a closed list "In the literature: N passages" under the documents of 35 people and 11 estates, linking to each page of each work that names them (1,174 links in the two languages, each checked to reach its passage). Places that are not estates have no list; their hits are kept in `corpus/literature/mentions.json`.
- Five of the people are Claude's identifications. The editor accepted four on Claude's reading, and Stenger once the evidence was written out for them (2026-10-19). What each rests on:
  - Grevenitz: the books' government councillor (Regierungsrath) von Grevenitz at Posen in the 1790s, given Tarnowo and a go-between in the Gurowski affair (Materialien pp. 127-153; FeuerbrÃ¤nde part 2, pp. 71 and 74, part 3, p. 132), is the edition's Kammergerichtsrat von Grevenitz, Triebenfeld's friend after 1807.
  - StÃ¶ssel: the Baron von StÃ¶ssel who lent Hoym his name to buy a gifted estate (Materialien p. 158) is of the edition's StÃ¶ssel family, Silesian creditors on KoszÄ™cin.
  - NÃ¶ldichen: the NÃ¶ldichen who signs for the General Direction of the Seehandlung in 1794 and 1795 (Held pp. 91 and 94) is the edition's councillor of war NÃ¶ldichen, who valued Krotoszyn, the estate Held's book is about.
  - Wartensleben: General Count Wartensleben at Liegnitz, no. 17 of the black register (FeuerbrÃ¤nde part 2, p. 84; Materialien pp. 165, 212), is listed under the edition's Silesian Counts Wartensleben, father and son, without saying which of them he is.
  - Stenger: the Justizkommissarius Stenger "in Unruhstadt" whose essay of 1798 on the HaulÃ¤nder Guradze cites (chapters IV to VI) is the edition's Criminal Rath Stenger "hier aus Karge" (letter 23 of Oe 1 BÃ¼ 9454, 1809), Triebenfeld's agent for ZagÃ³rÃ³w, TrÄ…bczyn, Pszczew and WitÃ³w: Karge and Unruhstadt are one town, Kargowa (the editor, 2026-10-19).
- Built and verified on the desktop; not published.

## The literature: passages tied by hand to documents (2026-10-19, not published)

- `literature/links.yml`: four links from the black register (the Materialien, pp. 141-171, and the Neue FeuerbrÃ¤nde, parts 2 and 3) to ten documents, each with a sentence in English and German saying what the book says and what the document says (LITERATURE_PLAN.md, section 9). Every figure in a sentence was read in both.
  - The Prince's gift and the exchange for Krotoszyn (I. HA Rep. 7 C Nr. 3570, document 1; Oe 1 BÃ¼ 9454, documents 85, 86, 87, 97, 101). The register says Beyme stopped the exchange; CÃ¶lln said Voss, and the letters bear him out. The register says the Prince gave the cabinet a yield of 50,000 a year; the letters give 41,500 (the Prince) and 40,500 (the King).
  - Triebenfeld's own estates (documents 104, 108, 112): the same valuation (over 700,000) and resale (750,000) in the register and the letters; for his sale to Prince George of Hesse-Darmstadt the register gives 400,000, his letter 280,000.
  - Krotoszyn's lease to FrÃ¼son at 30,100 (documents 85, 86, 101).
  - The other gifts Triebenfeld cites in letter 103 (Bischofswerder, Zastrow, Dolffs and Treskow, "Gen. Ruchts"), beside the register's entries on them. "Ruchts" as RÃ¼chel was Claude's identification; settled the same day (below).
- On the site: under each linked passage a box "In the edition" with the sentence and the documents; on each linked document's page an entry "In the literature" in the box "About this document". `literature_site.py` stops on a link to a passage or document that does not exist; `verify_site.py` checks both sides of every link (140 in the two languages).
- Built and verified on the desktop; not published.

## Letter 103: General RÃ¼chel; the literature published (2026-10-19)

- Oe 1 BÃ¼ 9454, letter 103, page 4: "des Gen. Ruchts" is "des Gen. Ruchels", General RÃ¼chel. The editor agreed with Claude's identification and took "Ruchts" for a misreading; the scan reads "Ruchels". Corrected in the transcription (logged in `transcription_decisions.csv`), in the English ("General RÃ¼chel", by `reference/english_corrections.yml`) and in the link's sentence; the mark of doubt on the word is taken out. RÃ¼chel's entry in `reference/people.yml` now finds the letter. The record is `units/oe1bu9454/intake/scripts/ruechel_103.py`.
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
  - Teodor Å»ychliÅ„ski's *ZÅ‚ota ksiÄ™ga*, vol. 7, pp. 187-188 (the Prusimski) and vol. 13, pp. 219-225 (the MiÄ…czyÅ„ski), read from the photographs in session.
  - Jan PachoÅ„ski's entry on Antoni Prusimski in the *Polski SÅ‚ownik Biograficzny* (1982, editor).
  The English of all six is Claude's, from the original. The machine English in the editor's files was not used (the PSB's was wrong in substance). No German translation of the Polish works was made: an accepted gap (editor).
- The index of people and estates over the eleven visible works: 3,200 hits, every one ruled in `literature/index.yml`; 2,946 stand.
- **Eleven new hand-made links** (`literature/links.yml`; fifteen in all, to 32 documents), every figure read in the book and the document. They tie:
  - Breyer to the lease of 1806 and to Weigel;
  - Å»ychliÅ„ski to the court books on the Prusimski line, to the letters on Michalina's marriage, to the dispatch from Venice and to the summons of 1860;
  - the PSB to the boundary commission, the confiscation, Venice and the restitution of 1807.
- Found while the links were checked, and put to the editor (NEEDS_CONFIRMATION.md, "The literature"):
  - The dispatch from Venice of 14 December 1796 already mourns Prusimski's wife, against Å»ychliÅ„ski's date for her death, 2 September 1797.
  - Å»ychliÅ„ski and the PSB give Michalina's second marriage as 1809, against "about 1814" in the edition's biographies.
  - Å»ychliÅ„ski's account of who held TrÄ…bczyn from 1809 to 1879 differs from the edition's.
  - The lease of 1806 differs from Breyer's account in its date, in the dike clause and on pasture and wood.
  No biography or era of the edition was changed.
- Published at the editor's word the same day, the questions above still open.

## Two eras made one: WÅ‚odzimierz MiÄ…czyÅ„ski's years and the liquidation (2026-10-20, not published)

- At the editor's word, "for better clarity": the era "The estate under WÅ‚odzimierz MiÄ…czyÅ„ski" and the era "The liquidation: the peasants' land and the servitudes" are one, under the working name "The colonists' land and forest rights" (slug `wlodzimierz`). The lawsuit of 1859 over the colonists' rights in the Count's forest and the liquidation that fixed those rights in 1868 and bought them out in 1892 are one story. The era has 14 documents, 1858 to 1897: APÅ 39/98/0/-/6603 and Breyer's copies of the tables in APP 53/968/0/-/716 moved into it.
- Changed with it: the era's ownership line and blurb (`reference/eras.yml`), the timeline (one band at 1858, its note covering both), and the story page in both languages (one section).
- Claude's proposed names for all the eras are put to the editor (NEEDS_CONFIRMATION.md, "The eras"); no other era is changed.

## The documents first: a rule; PaweÅ‚ Prusimski and the privilege of 1746 (2026-10-20, not published)

- **A new rule of the editor's** (2026-10-20): every fact is first checked against the edition's archival documents, before a book or any other source; where they disagree, the edition keeps to the document, and the difference is flagged in NEEDS_CONFIRMATION.md and recorded in the source's `notes.md`. Written into `docs/HOUSE_STYLE.md` ("The documents first"), with pointers in CLAUDE.md, WORKING_NOTES.md and LITERATURE_PLAN.md.
- **Breyer's "Paul von Kolno-PrusiÅ„ski" is PaweÅ‚ Prusimski** (the editor, 2026-10-20). Recorded in `literature/index.yml`, the work's `notes.md` and NEEDS_CONFIRMATION.md.
- **The link from Breyer (1935) on ÅaziÅ„sk Holland** said "the edition has no document of 1746". The corpus had not been searched: the boundary decree of 1775 (Konin Gr.145, p. 76) cites "the rights granted them in 1746", the primary source for the privilege (editor), and the summons of 1860 (APP 53/968/0/-/783) names its grantors, PaweÅ‚ z Kolna PrusiÅ„ski and his wife Katarzyna z RozdraÅ¼ewskich. Both documents are added to the link, and its sentence now says what each says; that the privilege was a hereditary lease is Breyer's account alone.
- For the era of 1851 to 1901, Claude proposes the name "The liquidation: the colonists become owners", from the heading of the ÅaziÅ„sk table of 1868 (NEEDS_CONFIRMATION.md, "The eras"). Not applied: the name is the editor's.
- **What the liquidation did** (the editor, 2026-10-20): the land the colonists farmed became their own, and the demesne farms stayed with the estate. The documents agree: the ÅaziÅ„sk table lists only the peasants' farmsteads and common land, the forest "Studzianka" stays the manor's, and in 1892 the colonists gave up their forest rights for "manor land" from the owner of the estate. The era's account (`reference/eras.yml`) and the story (EN and DE) now say that the manor kept its own land and forest, and that the government paid the former owner for the peasants' dues.

## The editor's voice documented (2026-10-20, docs only)

- From three samples of the editor's writing (the preface and introduction of their book on the TrÄ…bczyn estate, and a statement of purpose), `docs/EDITORS_VOICE.md` records their voice: sentence length (counted), words, openings and closings, evidence, what they do not do, where it differs from HOUSE_STYLE, and a two-paragraph brief. The samples are not kept in the repository. No text on the site was changed; reading the site against the brief is in TODO.md, section 8.
- Corrected and extended at the editor's word the same day: the pronunciations were a rare exception and are out of the brief; the long dashes are the word processor's typography, not the voice, so the house style's rule on dashes is no longer listed as a difference; the tone the editor aims at (a historian and editor of narrative academic history, evidence turned into a story a non-specialist can follow without loss of rigour) and their self-assessments (dry against fluff; framed "side roads") are recorded, and the brief is rewritten to them. A framed side road on the site is a new item in TODO.md.

## The spaced en dash; no signposting (2026-10-20, docs only)

- The editor ruled that an aside takes the spaced en dash ( â€“ ), never the em dash or a hyphen standing in for one; until now the English had no dashes at all. HOUSE_STYLE, "Typography". A range between two figures takes an unspaced en dash (8,000â€“9,000; the editor, the same day); ranges written before have a hyphen.
- A new HOUSE_STYLE section, "No signposting": a sentence about the text instead of the past (announcing, pointing back, listing topics) is not written, except to bring back a topic the reader has not met for a long time (the editor's exception), and then by restating the fact, not by "as mentioned earlier" (Claude's suggestion). Navigational text (the About page's guide, "How it was prepared", lists of contents) is proposed as not signposting, for the editor to confirm. A search of the site's English found no signposts and no dashes, so no published text changes. EDITORS_VOICE.md's brief says both.
- The editor's writing samples are for the analysis of style only: nothing in them is a source for the edition or is set against the documents (the editor, 2026-10-20). Written into WORKING_NOTES ("Working with the editor") and EDITORS_VOICE.md.

## The literature: PachoÅ„ski, MÄ…czak and Szwiec; the list by author (2026-10-20, published)

- The desktop's `main` is brought up to GitHub's (eighteen commits of the cloud sessions: the literature, the eras, line ends LF, house style).
- PachoÅ„ski (1973), "Les Polonais dans la RÃ©publique de Venise", and MÄ…czak (1968), "Export of Grain ... 1550-1650", first built that day as holdings by the desktop session, are moved into the literature (the editor: the Sources page is for primary sources); their holdings, page images and summaries are removed, and the code and data made for literature as holdings are taken out again.
- Szwiec (2009), the catalogue of the regional architecture of the Pyzdry Forest, is added: the Polish text from the Word-printed PDF (`pipeline/literature/szwiec_pdf.py`), Claude's English, and its 80 pages of photographs and maps as pictures. TrÄ…bczyn, WrÄ…bczynek, WrÄ…bczynkowskie Holendry and Orlina are among its villages.
- A work's pages can now show pictures (`figures` in `work.yml`); a work printed in English has one text and no buttons.
- The Literature page lists the works by author (the editor): surname first, the title with the English title in italics under it, where it was published, its language.
- The new works' index hits read and ruled; "Venise" made a default with one exception. The Hohenlohe essay links PachoÅ„ski's note 10 on the literature page. The Licences page says the modern works on the Literature page are outside CC BY.

## The literature: WÄ…sicki (1953) on Prussian colonisation in South Prussia (2026-10-21, published)

- Jan WÄ…sicki, "Kolonizacja niemiecka w okresie Prus PoÅ‚udniowych 1793 â€“ 1806", PrzeglÄ…d Zachodni 1953, no. 9-10, pp. 137-179, at the editor's word: read from the scanned PDF page by page (its OCR not taken over), 101 notes, nine tables in the text; the sideways table of the PoznaÅ„ department's colonies, the plans and a fold-out table of costs as pictures; Claude's English. It names the Hohenlohe estates of ZagÃ³rÃ³w and TrÄ…bczyn and the colonies of 1805 on the Warta. Index hits read and ruled (Frankfurt am Main and the Warsaw domain office as exceptions to older rulings).

## The literature: ChodyÅ‚a (2015) on the OlÄ™der settlements of the Pyzdry Forest (2026-10-21, published)

- Zbigniew ChodyÅ‚a, *Zarys najstarszych dziejÃ³w osad olÄ™derskich w Puszczy Pyzdrskiej 1746 â€“ 1793* (Pyzdry 2015), at the editor's word. The editor's Word conversion has no pages and its note numbers run into the words, so the text is made from the book's PDF in their Books folder (`pipeline/literature/chodyla_pdf.py`), with its 156 printed pages, 369 notes on their pages, three tables as HTML and 39 pages of maps, charters and portraits as pictures, and checked word by word against the Word file. Claude's English, page by page; the tables by `literature/chodyla2015/make_english.py`. The editor's machine English was read and not used.
- The book dates the founding of the TrÄ…bczyÅ„skie Stare OlÄ™dry and the LuÅ›nie OlÄ™dry to 1746 (PaweÅ‚ and Katarzyna Prusimski) from Konin Gr.145, and cites Konin Gr.136, Gr.153, Kalisz Gr.414, the hearth-tax table of 1789, the register of 1796 and the summons of 1860, all in the edition. Two of its details differ from those documents (NEEDS_CONFIRMATION).
- Index hits read and ruled: the Polish case forms of Antoni, PaweÅ‚ and Katarzyna Prusimski added for the literature; "Poniatowskiego" (here the King, not Prince JÃ³zef), "Przespolewski" and "Oppeln" given exceptions to older rulings.
- Six hand-made links from the book to Konin Gr.145 and the summons of 1860 (1746), Konin Gr.136 (1754), Kalisz Gr.414 (1771), Konin Gr.153 (1782), AGAD 1/169/0/1/1745 (the register of 1797) and Kalisz Tab.21 (the hearth tax of 1789). Five differences with the documents are recorded; the edition takes the documents.
- The editor's rule (2026-10-21): a fact or date from a primary document is taken over a literary source's without asking, and the difference is flagged so that it is known. HOUSE_STYLE, "The documents first", point 4; the doc-versus-book questions already in NEEDS_CONFIRMATION (Maryanna DÄ…mbska's death, PaweÅ‚ Prusimski's generation) are marked settled.
- Published at the editor's word, with WÄ…sicki (1953).

## The glossary: grÃ³d, the municipal court (2026-10-21, published)

- A new entry, `grod`, at the editor's word, from the entry GrÃ³d in Arct's *SÅ‚ownik ilustrowany jÄ™zyka polskiego* (1916, vol. 1, p. 405) on Wikisource, which they named, and the State Archive in PoznaÅ„'s description of the Konin court books (`docs/PRUSIMSKI_ERA_PLAN.md`). It explains that the court the edition's English calls the "municipal court" was the starost's court in the grÃ³d, not a town's court: no document in the edition names a town court. Checked (`checked: true`).
- It marks the Polish forms (grÃ³d, grodu, w grodzie, grodzki), the Latin castrensis, "municipal court" in the English and "Burggericht" in the German summaries: 375 marks in 56 documents, every one read in `review/glossary_matches.csv`; none is a place (Grodziec, Grodzisko are kept out).
- **"Castle court" is not the English term** (editor, 2026-10-21): the edition's own prose (holding pages, summaries, timeline, places, the literature's English and its notes) now says "municipal court" for sÄ…d grodzki, as the translations always did (`reference/translation_glossary.yml`), and "municipal court office" for urzÄ…d grodzki: 502 places. Kept: "Burggericht" in the German, and "the domain castle-office of Brieg" in Held (1801), a Prussian domain office, not a grÃ³d. The earlier entries of this changelog keep the old wording as history.
- Arct added to the glossary's reference works (`docs/GLOSSARY_PLAN.md`).
- A second entry, `stawisko`, at the editor's word, from Arct (vol. 2, p. 784: a large boggy pond, or ground taken up by a pond or left after one), with what the documents say of the ground: the boggy, wooded ground on the TrÄ…bczyn-Åukom boundary, disputed from 1728 (Konin Gr.145), its embankment (Gr.114) and the line of 1782 through it (Gr.153). The noun only (editor: "there's a place called Stawisko, and then the noun"): where an act makes the word the ground's name ("na Stawisku zwanym", "stawisko nuncupatum", "called Stawisko", "namens Stawisko") it is not marked. 95 marks in 3 documents, all read. The clerks capitalise most nouns, so a capital is not taken for a name.
- 113 entries, 57 checked.

## The literature: Boniecki (1900), the CheÅ‚mski branch that held Åukomia (2026-10-21, published)

- Adam Boniecki, *Herbarz polski*, part I, vol. 2, "CheÅ‚mscy h. Ostoja", at the editor's word, as a source for the CheÅ‚mski family tree: only the branch that held Åukomia (items 2.976.162-240 of M. J. Minakowski's online edition), from the editor's saved page, by `literature/boniecki1900/make_original.py`. StanisÅ‚aw CheÅ‚mski, Treasurer of Wschowa, his brother Heliodor, their father JÃ³zef and uncle Franciszek, the division of Åukomia about 1700, Ignacy's sale of Åukomia, ÅomÃ³w, Mielno (Imielno) and Bukowe to StanisÅ‚aw in 1766, and StanisÅ‚aw's line to WÅ‚adysÅ‚aw, owner of Åukomia in 1860. Cut at the item numbers (no page breaks online); Claude's English. The saved page is not kept: its header carries the editor's login.
- Read against the documents first: the brothers of 1728 (APP 53/6/0/-/40), of 1775 (Konin Gr.145) and the four estates of 1778 (Konin Gr.117) agree; Heliodor's canonry (CheÅ‚mno in 1775, PoznaÅ„ in Boniecki) and the year of StanisÅ‚aw's title (1778 in the document, 1779 in Boniecki) differ, and the edition follows the documents (NEEDS_CONFIRMATION, "Boniecki (1900)").
- Index rulings for the CheÅ‚mski forms, "Åukomi", and "Mielna" as Imielno in the list of the four estates only. Four hand-made links (`boniecki1900-*`), to 1644, 1728, 1775, 1778 and 1763; the first rests on Claude's reading and waits on the editor. `docs/LITERATURE_PLAN.md`, section 14. The literature has 18 works, 17 on the site.

## The literature: the Encyclopedia of Camps and Ghettos (2012), the Warthegau (2026-10-21, published)

- The USHMM *Encyclopedia of Camps and Ghettos, 1933-1945*, vol. II A (2012), the chapter "Warthegau Region", at the editor's word: only the pages they named, pp. 34-39 (the introduction), 48 (Chocz), 57-59 (Grodziec), 60-61 (Kalisz), 63-64 (Konin), 99-100 (RzgÃ³w), 120-121 (ZagÃ³rÃ³w), for the twentieth-century part of the edition. In English as printed; CC BY-NC-ND 4.0, so no translation and no pictures (their lenders' credits), the captions given.
- Made from the editor's JSTOR PDF by `pipeline/literature/warthegau_pdf.py`: the Polish letters from the accent font, the spaces of no width dropped, line-end hyphens told apart by the space the text layer keeps after a real one, notes linked within each entry, web addresses joined. `--check` compares every letter with the PDF. "BetchatÃ³w" corrected to BeÅ‚chatÃ³w at the editor's word. The PDF is not kept: its page feet carry the download's internet address.
- Index rulings: Koppe and Reinhardt are not the edition's; "KoniÅ„ska", "KoniÅ„skiej" and SÅ‚upca are. No hand-made links yet. The literature has 19 works, 18 on the site.

## The places Grodziec and RzgÃ³w (2026-10-21, published)

- All of 2026-10-21 after ChodyÅ‚a published together at the editor's word: the glossary's grÃ³d and stawisko, "municipal court" throughout, Boniecki (1900), the Encyclopedia of Camps and Ghettos (2012) and the places Grodziec and RzgÃ³w.

- Two places added at the editor's word (`reference/places.yml`, with their map positions in `reference/places_osm.yml`, looked up on OpenStreetMap and read against the sources). **RzgÃ³w** ("Rzgowo" 1261, "Irgouo" 1280, both the RzgÃ³w east of ZagÃ³rÃ³w by the Kodeks editors' note) is found in seven documents and tagged an estate in focus on four that concern it: KDW 4 and 6 (granted with Szetlew and ÅšwiÄ…tniki) and Konin Gr.117, docs 11 and 12 (the pines cut by its subjects in 1779 and its owner Marcin Nosalski's protest). **Grodziec** is found in Breyer's notebooks of 1936 and his notes of 1935; no document is about it, so it is not an estate in focus.
- In the literature, all 122 hits read and ruled (ChodyÅ‚a, Breyer, Szwiec, the Encyclopedia of Camps and Ghettos): every one is the Grodziec near RychwaÅ‚ or the RzgÃ³w near Konin.

## The glossary: komornik, the officer and the lodger (2026-10-21, published)

- At the editor's word, from Gloger's Komornik (the entry already rested on it for the officer). Every use in the documents read: two senses. **The court officer** (komornik graniczny and ziemski, Latin camerarius; Konin Gr.117, Gr.118, Gr.145, Gr.153, Kalisz Gr.425, Oe 1 BÃ¼ 9454 letters 17, 18, 232, 233): the entry `komornik`, now also matching the lower-case Polish, the Latin and the translations' "Boundary Surveyor" and "Land (Court) Chamberlain", 134 marks in 14 documents. **The landless lodger** (Gloger: "chÅ‚opi bezrolni ... za otrzymywanÄ… komorÄ™, ogrÃ³d"): a new entry `komornik-lodger`, marked only in its six documents (ADWÅ‚ 85, Konin Gr.136, Oe 1 BÃ¼ 14525 doc. 23, 14526 doc. 9, 9454 letters 146, 191), 23 marks. Before, the officer's definition was shown in four of those.
- `glossary_build.py` takes `only_in`, the documents an entry is marked in (beside `not_in`). 114 entries, 58 checked.

## The literature: Frost (2007), the nobility of Polandâ€“Lithuania (2026-10-21, published)

- Robert I. Frost, "The Nobility of Polandâ€“Lithuania, 1569â€“1795", ch. 9 of H. M. Scott (ed.), *The European Nobilities in the Seventeenth and Eighteenth Centuries*, vol. II: Northern, Central and Eastern Europe, 2nd ed. (Palgrave Macmillan, 2007), pp. 266-310, from the editor's PDF at their word "only the article by Frost": the volume's Guides to Further Reading (pp. 410-415, with the Polandâ€“Lithuania section) and the Russian chapter's opening page (p. 311) left out, and the guides not to be added at their word ("Don't add the guides from the PDF"). On the site at their word ("Give it a page - I'll need to decide later what gets displayed"); what the page displays is a later decision of theirs (NEEDS_CONFIRMATION).
- The book is under copyright (its imprint: "No reproduction, copy or transmission of this publication may be made without written permission"; "All remaining chapters Â© their respective authors 1995, 2007"). Put in with `visible: false` after the Seidel precedent, then given a page the same day.
- Read spread by spread from the page images at 200 dpi (the scan has no text layer; not OCR), doubtful spots settled at 300 dpi crops; the print's own slips kept as printed and listed in the work's notes. The chapter's notes are endnotes, kept on their printed pages so a note can be cited to its page (no `notes:` in work.yml).
- Index ruling, all pairs read in the sheet: the RadziwiÅ‚Å‚ magnates (28), Hieronim Florian RadziwiÅ‚Å‚'s given name ("Florian", 1) and Augustus II (1, caught by the pattern's bare "f " lookbehind in "of Augustus") are not the edition's; Repnin, the Russian ambassador (p. 299, twice), is ruled to the letters' Prince Repnin (83, 84, 1798), which the editor confirms (2026-10-21: "I'm sure Repnin is the same as the one in the project"; settled in NEEDS_CONFIRMATION). The literature has 20 works, 19 on the site.

## The glossary: kopiec, the boundary mound (2026-10-21, published)

- At the editor's word, from Gloger's "Kopce graniczne", read against the documents first: the decree of 1775 (Konin Gr.145) records the bricks, slag, glass, stones and coals laid where the mounds stood and a glass bottle with the commission's description under one, the corner (naroÅ¼ne) and wall (Å›cienne) mounds and the stakes in the marsh, as Gloger describes them; the line of 1782 (Gr.153) has forty-one wall mounds. Marked in Polish (kopiec), Latin (scopulus), the German summaries (Grenz-, Wand-, Eck-, EndhÃ¼gel) and the English ("mound", always a boundary mound there): 338 marks in 11 documents, all read. 115 entries, 59 checked.

## The glossary: pisarz, the court clerk (2026-10-21, published)

- At the editor's word, from Gloger's "Pisarze". Every use of pisarz and notarius in the documents read: the court's clerk (the land clerk of Kalisz, Ksawery Mikorski, sitting with the judge and sub-judge in 1778 and 1782, Konin Gr.117 and Gr.118; the land clerk of Sieradz and the deputy clerk of Greater Poland at the Tribunal, Gr.153; the land and castle clerks of Gr.145; the customs clerk at Pyzdry, 53/6/0/-/45; a manor's clerk, Gr.118 doc. 27; the clerk of the Civil Tribunal at Kalisz, Nr. 12366 doc. 6) is the new entry `pisarz`, marked only there (38 marks in 8 documents). Not the notary public of the Prussian and Warsaw papers (the entry `notarius`, which no longer marks Gr.153's deputy clerk), nor the surname "Antoni Pisarz" (Kalisz Gr.414), nor the dukes' notarius of the Kodeks.
- `komornik` also matches "Land Court Surveyor" (Gr.145's komornik ziemski). 116 entries, 60 checked.

## Summaries for the works kept off the site; Pinkas Hakehillot (1976) (2026-10-21, published)

- The editor: "For each literary source that you don't publish on the site, include an entry with a detailed summary of its contents." A work with `visible: false` is now listed on the Literature page with a note that it is under copyright, and its page holds only a detailed summary (`summary_en`, `summary_de` in its `work.yml`), none of its text. `build_literature.py` carries the summaries, `literature_site.py` writes the pages and stops on a kept-off work without them, the list and the page show the note and "Read the summary", and `verify_site.py` now checks the summary page and that no stretch of the text (the middle of the longest line of up to 40 passages, in each language) appears in any built file, in place of the old rule that the title appear nowhere.
- **Seidel (2018)**: a summary chapter by chapter (about 1,970 words), written from a reading of the whole book, with what the edition's documents say where it differs: TrÄ…bczyn came by the deed of gift of 9 August 1796 as estates fallen to the crown (Oe 1 BÃ¼ 14525, doc. 1), ZagÃ³rÃ³w by the deed of 19 June 1797 (Rep. 162 Nr. 295, doc. 3), not both in 1796; the colonists' lease of "18 May 1805" can be neither confirmed nor ruled out (APP 801, doc. 3, lacks its beginning).
- **Pinkas Hakehillot (1976)** (`dabrowska1976`): JewishGen's English, by Morris Gradel, of the entries ZagÃ³rÃ³w (p. 103), Pyzdry (pp. 202-203) and Konin (pp. 235-238) of Yad Vashem's encyclopedia, at the editor's word; kept as Seidel (JewishGen's notice forbids copying). `make_original.py` takes the entries from saved copies of the pages, every letter checked. Read against the documents: the entry's 1368 for ZagÃ³rÃ³w's town status against the privilege of 19 November 1407 (KDW, doc. 14), which the edition follows.

## TrÄ…bczyn: the wartime name Drommin (2026-10-21, published)

- At the editor's word: from 1939 to 1945 TrÄ…bczyn was Drommin. The rural commune of TrÄ…bczyn was provisionally renamed Drommin on 20 November 1939, the name confirmed on 18 May 1943, and from 1 April 1940 it formed the Amtsbezirk Drommin, run by an Amtskommissar at Grabina (Rolf Jehke, Territoriale VerÃ¤nderungen in Deutschland und deutsch verwalteten Gebieten 1874-1945, s.v. Amtsbezirk Drommin, https://www.territorial.de/wart//konin/drommin.htm). A new field `renamed` in `reference/places.yml` (name, years, a sentence in each language, the source and its link), carried into `site/_data/estates.yml` and shown on the place's card on the Places page under the medieval spellings, with the source cited. The name is found in no document or work of the edition, so it is not matched.

## APP 53/1455/0/2/21: the copy-book of the privileges of LÄ…d (2026-10-21, published)

- A new holding at the editor's word, `app5314550221`: five pages (13, 14, 25, 26, 66) of the eighteenth-century copy-book "Series privilegiorum monasterii Landensis transcripta ex libro privilegiorum", in the fond Klasztor cystersÃ³w w LÄ…dzie of the State Archive in PoznaÅ„. Six documents, in Latin: the boundary of Makownica (1399); the sale of three mansi of Åukom with the forest Gradziem to LÄ…d (Pyzdry, 21 September 1461); the beginning of King Kazimierz's confirmation of it; King Kazimierz's exchange of Little Wronczyn and the mill at Pyzdry for sixty mansi of the forest Czernietz, where Drzewce was founded (Pyzdry, 18 January 1362); the beginning of his grant of freedom to its colonists; and p. 66 of the compromissory decree of 1761 renewing the mounds between Åukom, ZagÃ³rÃ³w and Drzewce.
- The pages were found by the archive's pencil pagination among the editor's raw photographs and cut from the photographs' previews (`intake/holding.py`); pages 13 and 25 are cut below the end of the entry before, at the editor's word. Read in session (17 marks of doubt), translated, summarised in German and English, claim-checked (70 statements), with its page in both languages, three timeline entries (1362, 1461, 1761) and the German date and relation notes. Eras: `medieval`, and `prusimski-boundary` for the decree of 1761.
- A note in the margin is now a kind of its own (`margin_notes.yml`, "Written in the margin" / "Am Rand geschrieben"), beside text written sideways and the receiving office's notes: `corpus_pages.py`, `build_db.py`, `build_dataset.py`, `build_site_data.py`, `translate.py`, `letter.js`, `i18n.yml`.

## APP 53/1455/0/2/21: GrÄ…dzyÅ„, and p. 15 (2026-10-21, published)

- The editor: "Gradziem is indeed GrÄ…dzyÅ„." The copy's Gradziem, Gradzien and Graziem are matched to GrÄ…dzyÅ„ (`reference/places.yml`), docs 2, 3 and 6 are tagged with it, and the English, the summaries, the holding's page and the timeline say GrÄ…dzyÅ„; the copyist's Latin headings stay as written.
- The editor: "you can add page 15 to finish the king's confirmation." P. 15 (IMG_5223) is added, cut below the end of no. 16. Read whole, no. 16 is King Kazimierz's confirmation at Gniezno, in a year written over and read as 1447, of the contract by which Abbot Maciej bought the same three mansi of Åukomia and the forest of GrÄ…dzyÅ„ from the brothers MikoÅ‚aj, Jan and Warsz of Koscielec: not the confirmation of the sale of 1461, as its heading had been taken to say. Document 3 is dated 8 August 1447, summarised and claim-checked again; its link to doc. 2 is now "supplements"; a timeline entry for 1447. No photograph of p. 27 (editor).

## The literature: Karwowski (1900), the convent at OÅ‚obok (2026-10-21, published)

- At the editor's word: "Klasztor pp. cystersek w OÅ‚oboku" (`literature/karwowski1900/`), from Roczniki Towarzystwa PrzyjaciÃ³Å‚ Nauk PoznaÅ„skiego, T. XXVI (1900), pp. 1-114 â€” only the two paragraphs of p. 87 the editor quoted, with their footnote: the debts Prince Hohenlohe-Ingelfingen left on ZagÃ³rÃ³w, its loss at auction in 1827 to the WrocÅ‚aw banker Karol BogumiÅ‚ Weygel, and the Cistercian Nuns' 40,000 zÅ‚p. lost with it. Read from the WBC digitisation (DjVu id 118639; the files not kept), the image at 300 dpi and word-level zooms, the scan's text layer only as a check. Out of copyright (the author died in 1917). Claude's English. Index ruled; the three identifications it raises wait on the editor (NEEDS_CONFIRMATION, "The literature"). `docs/LITERATURE_PLAN.md`, section 19.

## The literature: Janocki (1779), the Lochowski entry, a sub-item of Paciorkowski (2026-10-21, published)

- At the editor's word: the entry "Stanislaus Lochowski" (LXXVII, printed pp. 159-160) of Jan Daniel Janocki's *Ianociana, sive clarorum atque illustrium Poloniae auctorum Maecenatumque memoriae miscellae*, tomus II (Warsaw and Leipzig 1779), `literature/janocki1779/`, transcribed in session from the editor's PDF (the title page and the two pages; the PDF not kept). It says Lochowski's *Processus iuris limitanei* of 1641 was twice printed again by Marcin Paciorkowski, who, "suppressing the true author Lochowski's name, rashly and insolently claimed the work for himself", under the *Regula processus granicialis* title (1749 and 1760). Claude's English. The entry runs to p. 161; the extract stops at p. 160, where item IV closes whole.
- **The first sub-item** (`docs/LITERATURE_PLAN.md`, section 18): `parent: paciorkowski1776`. The Literature page shows Janocki inside Paciorkowski's section; Paciorkowski's page carries the note (Janocki's words, with a link to the sub-item's page); the sub-item's page links back. `build_literature.py` and `literature_site.py` carry `parent`, `note_en` and `note_de`; the empty `parent` is dropped from the site data (Liquid reads "" as true â€” an empty "Attached to" line appeared on every work page before the drop).
- **The citation of the parent work** is now "Paciorkowski (1776) [= Lochowski 1641]" (`literature/paciorkowski1776/work.yml`), so the corpus passage headers, the page's standfirst and the "In the literature" lists name Lochowski wherever the handbook is cited; the bracket's wording was chosen without the editor and may be reworded. The accounts of Paciorkowski (1776) name the attribution and the conflict with the 1776 title page ("Editio secunda ab ipso authore aucta").
- No new index hits (nothing in the entry matches the edition's people or places); the doubtful reading "Miedzyborze" (the place of Lochowski's subscription) and the transcription wait on the editor (NEEDS_CONFIRMATION, "The literature"). The literature has 22 works, 20 on the site.
- **The plan's section numbers** had gone wrong on the way in: Frost (2007) and Pinkas Hakehillot (1976) were both "section 16", and Karwowski (1900) and Janocki were both "section 17". Renumbered: Pinkas 17, Janocki 18, Karwowski 19, with the cross-references in CLAUDE.md, this file, TODO and `literature_site.py`'s docstring.

## The literature: Minakowska (2026), Wojciech Otto-TrÄ…mpczyÅ„ski's page (2026-10-22, committed; not published)

- The page of Wojciech Otto-TrÄ…mpczyÅ„ski (ID: sw.35437) in Minakowska's database (`literature/minakowska2026ottotrampczynski/`), at the editor's word: the sixteenth-century man of the edition's TrÄ…mpczyÅ„ski family - marriage about 1590 (the database's estimate) to Anna Cerekwicka, the son StanisÅ‚aw, and the descent whose names are the brothers of the decree of 1644's generation. Polish interface, Claude's English. A short page: no biography, no parents, no tree, no siblings.
- **The database's "sw." numbers**: sw.35437 is of the branch of the Teki Dworzaczka regest numbers - the person came into the database from a regest, and the regest of 1614 (KsiÄ™gi grodzkie pyzdrskie, nr 2152, Nr 137: his son's marriage portion of 7,000 zÅ‚ on half the estates) is the page's one source. A fourth kind of number beside the Boniecki (2.976.*) and family-branch (4.285.*) ones.
- **The pipeline fix the work forced** (`pipeline/literature/literature_index.py`): the index dedup dropped an extra pattern's hit whenever an edition pattern of the same slug fullmatched the surface, whether or not it could fire in the record - the edition's `trampczynski` entry carries `only_in`, so its pattern cannot fire in a literature uid, and the work's hits were invisible. The dedup now asks `applies()` first. General, not particular: any future `only_in` person stands the same way.
- **The page** /people/wojciech-otto-trampczynski/ (/de/personen/wojciech-otto-trampczynski/), the second standalone - and the rule's addition: **a standalone block's slug must not be an entry's slug**. The first try keyed the block `trampczynski`, the family entry's own slug, and the page showed the family's heading and bio; the block was renamed and the collision is recorded in `reference/genealogy.yml`.
- The index: 9 hits, all ruled (`--check` clean) - the family yes, "w TrÄ…mpczyÅ„skich Ol." no (the colony's name, ChodyÅ‚a n. 34), "Janem TrÄ…mpczyÅ„skim herbu TopÃ³r" no (Å»ychliÅ„ski p. 187, the OpaliÅ„ski genealogy's man).
- NEEDS_CONFIRMATION gains the regest of 1614 (a possible holding: the Pyzdry books) and the descent's fit with the decree of 1644.

## The literature: Minakowska (2026), StanisÅ‚aw Adam MiÄ…czyÅ„ski's page (2026-10-22, committed; not published)

- The page of StanisÅ‚aw Adam MiÄ…czyÅ„ski (ID: 4.285.278) in Minakowska's database (`literature/minakowska2026miaczynski/`), at the editor's word: the edition's `miaczynski` himself - the second husband of Michalina Prusimska, colonel of the Polish army, adjutant of Prince Poniatowski, member of the Sejm of 1830-31, buried at TrÄ…bczyn, heir of TrÄ…bczyn and Wieniec by the legitymacja of 1838. Polish interface again (the work's language is the saved page's own, section 22), with Claude's English.
- **The marriage act of 17 August 1810** (Warsaw ASC CyrkuÅ‚ IV, act 67/1810, geneteka) against the edition's "about 1814" inferred from the letters of 1815: NEEDS_CONFIRMATION, nothing changed yet - the site shows both, the flag beside the new page's date.
- The page has a **RodzeÅ„stwo section** the first page had not; the standing selection does not bring it in (it stays in the knowledgebase), and `make_original.py` stops there. New marks kept as printed: "hr. [tytuÅ‚] nadany" (a title granted), the Towarzystwo Rolnicze districts as offices, the page's own Wikipedia line, the "(linia: â€¦)" kinship markers inside the status list.
- **The person's page** /people/miaczynski/ (/de/personen/miaczynski/): the first whose genealogy block hangs on an entry of the edition - the people.yml heading and biography, the life line 1780-1845 (stated dates, new in people_bios.yml), the family with the source of every fact, the 5 documents, and the automatic literature box. The wife is linked to her entry (prusimska), the son to his (miaczynski-wlodzimierz).
- **The index: 47 hits, all ruled** (`--check` passes, 0 unruled pairs) - including the four pairs the second page's session had left unruled (Bronisz no, CheÅ‚mska yes, MaÅ‚achowski no, Wieruszowa no). **The two duplicate `MiÄ…czyÅ„ski:` keys of the miaczynski section stood merged**: the second, added for the first Minakowska work, had shadowed the first in YAML and the three zychlinski exceptions were dead from 2026-10-22 until now.
- NEEDS_CONFIRMATION gains the marriage date, PSB t. 20 s. 562, and the page's other printed sources.

## The literature: Minakowska (2026), Helena Zielonacka's page (2026-10-22, committed; not published)

- The page of Helena Zielonacka (ID: 2.976.216) in Minakowska's database (`literature/minakowska2026zielonacka/`), at the editor's word "related to CheÅ‚mski": the CheÅ‚mski line through the wife of the decree of 1728's JÃ³zef Åšcibor-CheÅ‚mski (heir of Åukomia and Åomowo). Saved in the **database's English user interface** - the rule now says the work's language is the saved page's own (`docs/LITERATURE_PLAN.md`, section 22), so this work is `language: en` with no english.md, the one text as MÄ…czak (1968) is; the names, the offices and the regest stay Polish. The database's Boniecki-derived IDs: her 2.976.216 is an entry of the online Boniecki's article 2.976, inside the item range the edition's `boniecki1900` brought in (her marriage is in its passage c04).
- Against the documents: the husband and the family agree with the decree of 1728 (APP 53/6/0/-/40) and Boniecki c04; her sons are the Heliodor and StanisÅ‚aw of the boundary decree of 1775, whose offices carry the same differences Boniecki raised (NEEDS_CONFIRMATION, settled - the documents stand); her children's birth years are the database's estimates and none is shown; the grandchildren's stated years are on her page with the work as their source. The Notes' regest of 1727 (Konin municipal books, her 3,000-zÅ‚p dowry recorded on JÃ³zef's estates, he her guardian as well as her husband) is in the knowledgebase, and whether its holding is to be sought is the editor's (NEEDS_CONFIRMATION).
- **The standalone person page**: /people/helena-zielonacka/ (/de/personen/helena-zielonacka/) is the first for a person of no document of the edition - `standalone: true` in `reference/genealogy.yml`, with its own heading and biography, no documents section, and the literature named by hand (boniecki1900/c04 and the work's marriage passage). The index: 6 hits, all the CheÅ‚mski family entry's, all ruled.
- The first work's notes now record what its dropped status line said (chrome, but a fact about the person), and its grandchildren's "ca 1849" is kept as the rule requires.

## The literature: Minakowska (2026), the Starost's page, and the person pages (2026-10-22, committed; not published)

- The page of Antoni MichaÅ‚ Kazimierz OstrorÃ³g-Prusimski z Kolna h. NaÅ‚Ä™cz (ID: 4.285.619) in M. J. Minakowska's Wielka genealogia Minakowskiej (`literature/minakowska2026prusimski/`), the first of the database's pages the editor means to send, and with it **the standing rule for them** (`docs/LITERATURE_PLAN.md`, section 22): one excerpt work per person, slug `minakowska2026<name>`; the saved page never kept (the editor's login, the visitor's IP); the whole page kept as the knowledgebase (`full.md`, never shown, the Uwagi and their Teki Dworzaczka regest of 1786 included); only the editor's sections shown, **in full detail** (here the biography, the parents, the ancestor tree, the marriage, the children and grandchildren); **the database's estimated dates never taken into the edition's prose** (`docs/EDITORIAL_RULES.md`, the editor's ruling of 2026-10-22); the documents first on every fact.
- **The person pages** (the new site feature, designed with this work): a page per person from the authored `reference/genealogy.yml` - who they are, their life dates, their family with the source of every fact, the documents that name them, the literature that names them - built by `pipeline/build/person_pages.py` (a step of regenerate.py, after the website data and the index), the layout `person`, both languages, linked from the entry on the People page; checked by `verify_site.py`. The pilot: **/people/prusimski/** and /de/personen/prusimski/, with the life-line 1744â€“ca 1806 (the PSB entry's, accepted; the "ca" open, NEEDS_CONFIRMATION), the family (the parents Stefan Prusimski and Wiktoria nÃ©e Malczewska, the marriage to Marianna nÃ©e DÄ…mbska, Michalina with her two husbands and her children and grandchildren, the edition's WÅ‚odzimierz linked), and the sentence on the Uwagi's sources.
- Against the documents: the father and the grandfather agree (the citation of 1782, the decree of 1775); the page's grandmother Teresa nÃ©e ÅoÅ›-GoliÅ„ska is more than the documents say; its header "starosta nieszawskie" is the site's slip (the documents, the page's own Uwagi and the PSB all say Niszczewice); its PSB citation says t. 28 where the edition's copy is t. 27 (NEEDS_CONFIRMATION). The index: 31 hits, all read and ruled - the tree names the Starost's forebears, the grandchildren's list his descendants, and the rulings keep the bare surnames from the wrong persons (`literature/index.yml`).
- Encoding note for the pages of this database: they are ISO-8859-2, not Windows-1250.

## The literature: Kucharski (2023), the noble judiciary (2026-10-22, published)

- Robert Kucharski, "SÄ…downictwo szlacheckie od XV do XVIII wieku", Consilium Iuridicum 1(3-4) 2022, pp. 226-253 (`literature/kucharski2023/`), at the editor's word: the whole article from the journal's own PDF (`pipeline/literature/kucharski_pdf.py`, every page's letters held against the text layer by --check, all 28 pages match), the three pictures not rendered, their captions and "Å¹rÃ³dÅ‚o:" lines as text; Claude's English, page by page, the article's own English abstract and key words standing as printed. CC BY 4.0, so shown whole, and named on the Licences page as the literature's one open-access exception.
- Index hits read and ruled: JÃ³zef Wybicki and the Warsaw of two bibliographical references stood; the municipal court "w BrzeÅ›ciu" of the Matuszewicz story is BrzeÅ›Ä‡ on the Bug, not BrzeÅ›Ä‡ Kujawski - ruled out (NEEDS_CONFIRMATION). No hand-made links yet. `docs/LITERATURE_PLAN.md`, section 20.

## The literature: Mielewczyk (2017), the maps of the villages (2026-10-22, committed; not published)

- Wojciech Mielewczyk, "Zmiany przestrzeni wsi w drugiej poÅ‚owie XIX i na poczÄ…tku XX wieku na przykÅ‚adzie wybranych map ze zbiorÃ³w Muzeum Narodowego Rolnictwa i PrzemysÅ‚u Rolno-SpoÅ¼ywczego w Szreniawie", Z DziejÃ³w Kartografii XXI (2017), pp. 41-57 (`literature/mielewczyk2017/`), at the editor's word with the rulings: visible, the figures skipped, a link to the article provided, the whole article brought in. The link is the open-access copy at maphist.waw.pl (the `scan:` of `work.yml`).
- The text from the annual's PDF (`pipeline/literature/mielewczyk_pdf.py`, --check holds all 17 pages against the text layer); the layer's "fi" ligature with its stray space joined (twelve joins listed); the 19 notes at the foot of their pages; the fourteen figures (Ryc. 1-14) not rendered, their captions as text - on four pages a caption stands between two pieces of one paragraph, and a body line never joins a paragraph of another kind. A paragraph ends even when its last run is a note mark (p. 52, "347 tysiÄ™cy.[^16]"). The article's own slips kept (the caption of Ryc. 6 reads 1866 against the body's 1886; note 4's "t. 3" against Literatura's "t. 2"; Burszta's title "gospodarstwa wojskowego" in Literatura against note 3's "wiejskiego"; the map titles' own spellings; the unfinished year "192â€¦" of the Lisewo entry). Claude's English; the article's own English block of p. 57 stands as printed.
- The article bears on the edition's ground: fig. 4 is a fragment of the map of the estates of TrÄ…bczyn of 1861 with the field of the enfranchised peasants marked, and p. 48 names Kolonia ÅaziÅ„skie and Kolonia Huta on the parcelled lands of the TrÄ…bczyn property (the edition's Staro- and Nowo-ÅaziÅ„ska colonies, which the article does not say). Copyright the Institute's (2017), no open licence stated - shown whole at the editor's word; the Licences page not changed.
- Index hits read and ruled: 17 mentions; the map titles' "Kaliszskoj" and "KoniÅ„skim" ruled to Kalisz and Konin with the reasons written, the minister Poniatowski of 1938 refused to Prince JÃ³zef (an exception added); "Kolonia ÅaziÅ„skie" is not matched by the edition's patterns (they take only the Staro-/Nowo-ÅaziÅ„ska forms) - whether to add a pattern waits on the editor (NEEDS_CONFIRMATION). No hand-made links yet. `docs/LITERATURE_PLAN.md`, section 21. The literature has 25 works, 23 on the site (two summary-only).

## The newspapers: a new section, and Dziennik PoznaÅ„ski R. 79, nr 180 (7 sierpnia 1937) (2026-10-22, committed; not published)

- The editor's ruling: "Let's make a new section for newspaper articles, since it doesn't really fall under archival sources or literature." A third section stands between the Sources (archival) and the Literature (works about the history): `newspapers/`, on the site at /newspapers/ ("Zeitungen" in German), the menu entry between Sources and Literature. Plan, reading method and open questions: `docs/NEWSPAPERS_PLAN.md`.
- The first item (`newspapers/dziennikpoznanski19370807/`): the "Z ZagÃ³rowa" local column of Dziennik PoznaÅ„ski, R. 79, nr 180 (7 August 1937), three anonymous municipal notes closed "(mat)" - the recruitment of some sixty unemployed of ZagÃ³rÃ³w for seasonal farm work in Germany, the moving of the old people's home to a property of the heirs of Ignacy Ciszewski at OleÅ›nica on the road to Konin under deputy mayor Franciszek Åukaszewski, and the paving of the streets with trees to be planted along them. Transcribed line by line as printed ("Â¬" at a word broken at the line's end, the Kuryer Polski convention); Claude's English beside it; era `twentieth-century`. The clipping came as a single JPG in Downloads and is not kept in the repository.
- **No paid run.** The editor asked instead that OCR be installed for the project: Tesseract 5.5.3 (winget `tesseract-ocr.tesseract`) with the Polish models in %LOCALAPPDATA%\Tesseract\tessdata, `pytesseract` installed, and `pipeline/ocr.py` wrapping them (`read()`, `words()`). The text is the agreement of five passes (tessdata_best and the standard model, the page upscaled Ã—3 and Ã—4, psm 6 and 4, the Windows.Media.Ocr engine as a third witness); what they did not settle went to the editor on a stand-alone spot sheet of 13 rows with pictures (`scratch/dp1937_sheet.py`, the queries.py page and saving) and was answered in full the same day: m. ZagÃ³rowa, zapracowanej, odciÄ…Å¼ony ("relieved"), the stray fragment between the notes left out, "starcÃ³w." with its period, Ignacego, **"we wsi i gmina OleÅ›nica" as printed (the grammar's "gminie" refused)**, szosie, OleÅ›nicÄ™, przytuÅ‚kiem, "(mat)" without a period inside, chcÄ…c, the printer's edge fragments ("Pd", "PDZ") left out.
- The site: `pipeline/newspapers/newspapers_site.py` (a step of regenerate.py) writes site/_data/newspapers.yml and one page per item in each language; `_layouts/newspaper.html` shows the item like a work of the literature (one text at a time, the English first); the Newspapers include lists the items by year under their newspaper's name; i18n strings in both languages; verify_site.py checks every visible item's page in both languages and holds a kept-off item (visible: false) to its summary, as it does the literature's. verify_site.py passes whole.
- Open on the editor (NEEDS_CONFIRMATION, "The newspapers"): the clipping's source (its `scan:` stays empty until they say); the rights (anonymous press of 1937 read as public domain by the 70 years from publication - Claude's reading, to be confirmed); whether Kuryer Polski 1754 moves here from the Sources page; whether the index of people and places runs over the items; whether the site carries the clipping itself. Published only at the editor's word.

## The newspapers: Kuryer Polski (1754) moves in; the clipping carried; the index run (2026-10-22, committed; not published)

- The editor's rulings, all worked in the same day: the clipping comes from the blog ZagÃ³rÃ³w w historii (its post of 2 October 2024, "Kolejne wycinki z prasy sprzed lat, cz. 3") - the `source:` of the item, shown on its page; **the rights are approved** ("Assume the rights are approved"); **the site carries the clipping** (`image:` in item.yml, the figure above the texts - the Dziennik clipping converted from its WebP to JPEG, the Kuryer Polski's page a copy of the derivative the document page showed); **Kuryer Polski 1754 moves** from the Sources page into the newspapers; **the people/places index runs over the items**.
- **Kuryer Polski 1754, nr 75** (`newspapers/kuryerpolski1754075/`): the report on the funeral of PaweÅ‚ Prusimski at TrÄ…bczyn, 5 December 1754, is the section's second item. The text, the editor's English, the summaries and the page image come over unchanged in their words; the item is no longer one of the edition's documents (the edition counts 619 documents in 46 holdings), its page is /newspapers/kuryerpolski1754075/ with redirects standing at /documents/kuryerpolski1754075/ and /documents/kuryerpolski1754075/1/, the timeline's event of 1754 links the item's page, and the story's and the KDW holding's links point there. The item's caveat names the English the editor's own, not Claude's (`translation: editor`).
- **The index** (`pipeline/newspapers/newspapers_index.py --check`, a step of regenerate.py): the literature's index machinery run over the items' originals, rulings in `newspapers/index.yml`, every hit read before it was ruled - 18 hits in 14 pairs, all ruled: GÅ‚owiecki, PaweÅ‚, Katarzyna and Antoni Prusimski (the print's PrusiÅ„ski and ÅÄ™dzki forms), Kalisz, Konin, LÄ…d, OleÅ›nica, TrÄ…bczyn, ZagÃ³rÃ³w. The People and Places pages carry a box "In the newspapers" beside the literature's; a person of the newspapers who names no document (GÅ‚owiecki, whose report left the corpus) stands on /people/ all the same, with no documents shown. The OleÅ›nica ruling rests on the item's own geography (the village and commune of that name on the road from ZagÃ³rÃ³w to Konin) and waits for the editor's confirmation (NEEDS_CONFIRMATION). An item's uid in the index is its slug with "-1", so the register's `only_in` filters keep working for the spellings they were written for.
- verify_site.py passes whole: 619 documents character-exact, 2 items with pages in both languages, no broken links (the redirects included).

## The newspapers: Ostdeutscher Beobachter, Jg. 4, Nr. 197 (19. Juli 1942) (2026-10-22, committed; not published)

- The section's third item (`newspapers/ostdeutscherbeobachter19420197/`), given by the editor as a folder with the page image (`1492.jpg`, the WBC object), a markdown file with the German transcription and Claude's English beside it, and the link https://www.wbc.poznan.pl/dlibra/publication/121214/edition/131605/content: the feature "225 Jahre alte deutsche Siedlung im Wartheland" (signed Willi Spatz) on the "purely German settlement" of Lazinsk â€” ÅaziÅ„sk â€” in the Amtsbezirk Drommin. The citation: the Ostdeutscher Beobachter, Organ der NSDAP, VerkÃ¼ndungsblatt des Reichsstatthalters im Reichsgau Wartheland und seiner BehÃ¶rden, Posen, NS-Gauverlag; the paper ran from 1 November 1939 to 1945 as the successor of the Posener Tageblatt.
- The editor's rulings on the direct questions: the English is Claude's (the item's page carries the standing caveat, like the 1937 item's), and **the item is shown whole without the rights flagged** ("Show it, no need to flag the rights") â€” put to the editor because the item is signed, unlike the anonymous 1937 clipping. No OCR, no spot sheet, no paid run: "the transcription is secure", the editor's word, and the text stands as the file gives it (the md's escapes resolved; the article's picture marked "[Abbildung]" with its caption kept as text; the print's line division not kept, the file came with the paragraphs whole).
- **What the item bears on the edition's ground**: the Amtsbezirk Drommin of the article is the wartime name of the rural commune of TrÄ…bczyn (`renamed` in reference/places.yml, 2026-10-21); its Lazinsk is the Åazinsk of Breyer's notebook of July 1936 (APP 53/968/0/-/669), which names the same teacher Mielke ("Lehrer i. Åazinsk: Mielke seit 1925") and Michalinow beside it â€” the article and the notebook, six years apart, witness the same place and the same man. The article's founding date of 1718 stands against the edition's own records (the ÅaziÅ„skie OlÄ™dry from the 1746 foundation, the register and ChodyÅ‚a 2015; the Nowe OlÄ™dry first attested 1776): kept as printed, the difference recorded in the summary (NEEDS_CONFIRMATION, "The newspapers"). The item's judgements are the party paper's own; the account on its page says so.
- The index: two new pairs, read and ruled (`newspapers/index.yml`) â€” "Konin" (the Kreisstadt itself, the article's walk to the Amtsbezirk begins there) and "Schlesien" (the region the fourteen founding families set out from; the article's "Schlesierlande" is matched by no pattern). 20 hits in 3 items, all ruled, 8 links. **"Drommin" and "Lazinsk" are matched by no pattern** â€” whether to add patterns waits on the editor (NEEDS_CONFIRMATION, with the Mielewczyk "Kolonia ÅaziÅ„skie" question).
- Housekeeping: the generated site pages of the Kuryer Polski item (`site/_newspapers/kuryerpolski1754075.md` and its German twin) and the index's corpus record (`corpus/newspapers/mentions.json`), left untracked by the move's commit, are committed here. verify_site.py passes whole: 3 items with pages in both languages, 619 documents character-exact, no broken links. Not published.

## The newspapers: TwojaSÅ‚upca, 6 lipca 2015 ("TrÄ…bczyn Å›wiÄ™towaÅ‚ 775 lat") (2026-10-22, committed; not published)

- The section's fourth item (`newspapers/twojaslupca20150706/`), given by the editor as the address https://twojaslupca.pl/trabczyn-swietowal-775-lat/: the report of the village of TrÄ…bczyn's 775th-anniversary jubilee (the celebration the day before, 5 July 2015; the portal counts from the document of 1240), in TwojaSÅ‚upca, the local news portal of SÅ‚upca â€” the first item of the press from the web, no scan, no OCR: the portal's HTML taken as printed, nothing tidied, its own oddities standing ("WiesÅ‚aw Radniecki Andrzej Kin" without the comma, "Marzena kazimierska" with the small letter, "Anna Siuba" named twice, the spaces after the hyphens, the article's own grammar).
- The editor's rulings on the direct questions: **shown whole** (the article is the press of 2015 and under copyright, unlike the 1937 and 1942 items â€” the rights approved), and **no picture** â€” the article's one photograph stays off the site, its place marked "[Obraz]", the `source:` link pointing to the article. The slug's date stands in the issue's place (`twojaslupca20150706`; `docs/NEWSPAPERS_PLAN.md`, sections 1 and 5). The page's one reader's comment is not part of the article and is not kept. Claude's English; the standing caveat on the page.
- **What the item bears on**: its history paragraph is the edition's own documents' story, each claim matched by the KDW holding â€” the "Trampczin" of 1240 is the KDW's no. 2 (Archbishop Fulko's grant of tithes to LÄ…d, 30 September 1240 (sic), which the article's "a raczej Trampczin" quotes the Latin of); Janek son of Szymon and the count MikoÅ‚aj of LÄ…d are named in the KDW's charter of 27 March 1276 (Duke BolesÅ‚aw the Pious's grant of TrÄ…bczyn to count MikoÅ‚aj, which recites the earlier grantees); "komes Jan i PrzedpeÅ‚k" are the brothers, heirs of TrÄ…bczyn, of the KDW's two judgments of 1346. The jubilee's arithmetic is the article's own (1240 + 775 = 2015). The article names no edition work; the edition keeps to its documents.
- The index: four new pairs read and ruled, one ruled out (`newspapers/index.yml`) â€” "TrÄ…bczyn" and "TrÄ…bczyna" in (the village, the honours' name, the exhibition's title), "Prusimski" in (Antoni Prusimski, the register's Starost, of whom the entry's identity says he took part in the uprising of 1794 â€” the article's context and the register's man agree), "MiÄ…czyÅ„ski" ruled out (the report's heirs-list: WÅ‚odzimierz is the register's other entry, pinned to the summons of 1860; "StanisÅ‚aw hrabia" and "Aleksander" are identified by nothing the edition holds â€” the register's own `not_in` precedent; NEEDS_CONFIRMATION), and the honouree's surname "Wolicki" ruled out of the place Wolica. 35 hits in 4 items, all ruled, 10 links; the TrÄ…bczyn estate's Places entry and the Starost's /people/ entry each gained the item in their "In the newspapers" box. **"LÄ…dzie", "lÄ…dzki" and "Trampczin" are matched by no pattern** â€” whether to extend the register's patterns waits on the editor (NEEDS_CONFIRMATION, "The newspapers").
- Two rendering faults found and fixed while the item went in (WORKING_NOTES, "Two Liquid traps"): the empty `image:` of an item without a picture made the item layout render a broken figure (Liquid counts the empty string as true; the comparison is explicit now), and the Newspapers list page's Language fact was blank for every item (Liquid cannot build the bracket key by concatenation; the include assigns it first). verify_site.py passes whole: 4 items with pages in both languages, 0 kept off the site, 619 documents character-exact, no broken links. Not published.

## The newspapers: the editor's identifications â€” Drommin, Lazinsk, Kolonia ÅaziÅ„skie (2026-10-22, committed; not published)

- The editor's three rulings, put to them with the 1942 item's open questions and answered the same day: **"Drommin = TrÄ…bczyn"** (the article's Amtsbezirk Drommin is the commune of TrÄ…bczyn under its occupation name â€” the register's `renamed` entry confirmed as the identification); **"Lazinsk = German-era name for ÅaziÅ„sk, the colony which went by many name variants"** (the article's Lazinsk is ÅaziÅ„sk, the colony and not a part of one â€” settling the register's open question "whether ÅaziÅ„sk is that name or a part of the colony"; the register records ÅaziÅ„sk as a variant of TrÄ…bczyÅ„skie Stare OlÄ™dry, so the article's Lazinsk is that colony, the 1746 foundation; Breyer's notebook of 1936 distinguishes its Alt and Nowo Åazinsk â€” the Stare and Nowe colonies); **"Kolonia ÅaziÅ„skie is a variant of ÅaziÅ„sk/Lazinsk"** (Mielewczyk's form names the same colony, settling which colony his p. 48 form names).
- Worked in: `reference/places.yml` â€” "Drommin" a matched variant of trabczyn, "Lazinsk" and "Kolonia ÅaziÅ„skie" matched variants of trabczynskie-stare-oledry, the open questions rewritten with the rulings; `newspapers/index.yml` â€” the 1942 item's "Drommin" (1) and "Lazinsk" (6) ruled in; `literature/index.yml` â€” Mielewczyk's "Kolonia ÅaziÅ„skie" ruled yes (the hit his item's index had left unmade). The index over the items: 42 hits in 4 items, all ruled, 11 links; the TrÄ…bczyn estate's Places entry keeps the 1942 item in its "In the newspapers" box. The bare Polish "ÅaziÅ„sk"/"Åaziny" stay `match: false` (their literal would also catch the Nowe colony's "ÅaziÅ„skie", and matching them would bring Breyer's "Åazinsk" of 1936 in â€” NEEDS_CONFIRMATION, the editor's word). The 1942 item's account and summary state the identifications as the editor's rulings; the item's `notes.md` has the block.
- verify_site.py passes whole (4 items with pages in both languages, 619 documents character-exact). Not published.

## The literature: Åukasiewicz (1997), the "Black Register" studied (2026-10-22, committed; not published)

- Dariusz Åukasiewicz, "Nowa analiza â€žCzarnego Rejestru". Studium ÅºrÃ³dÅ‚oznawcze", *Kwartalnik Historyczny* R. CIV (1997), nr 2, pp. 31-62 (`literature/lukasiewicz1997/`), at the editor's word with the rulings: the whole article, visible, the appendix tables as HTML tables. The RCIN digitisation is the `scan:` of `work.yml`.
- The text read from page images (300 dpi, two halves; the four appendix pages printed sideways, read rotated): the PDF's OCR text layer used as a scaffold only and corrected against the images. The register's manuscript in GStAPK (I HA Rep. 7c SÃ¼dpreuÃŸen Nr 14) is the article's own discovery, and its findings correct the register's headline: 48 donataries, 52 donations, 245 estates, nominal value 2 069 550 Thaler, real value 4-7 million (nearer 4) against the title page's 20 million.
- The tables as HTML (Tabela 1's six columns and its number row 1-6 taken from the print's own rules; the print has no serial numbers in the name column - the draft's first pass had added them and they were struck); the table notes as `[^t1-n]`/`[^t4-n]`; the print's slips kept and listed (`notes.md`); the two notes split across page feet keep their split; the journal's own English summary stands as printed with its French-stressed spellings, verified on enlargements. Claude's English page for page.
- Where the article's figures differ from the edition's documents, the documents stand (the Triebenfeld sale: the register's entry and the letters 400,000 to Prince George and 750,000 on, the article 450,000 and "the same year" - his reading of Dorow's printing).
- Index hits read and ruled (the kings yes; Massenbach yes on the article's own n. 24; Niemojewski and Wybicki yes on the confiscation list; Adelheid Simsch refused to the Princess; the donatary GrÃ¤venitz, councillor Schmaling and the Freiherr von der Reck refused with reasons and open in NEEDS_CONFIRMATION, "The literature"; the imprint towns and the titles carrying Berlin refused). Two hand-made links: the Triebenfeld story and Tabela 4's row to the Prince's three letters, and Tabela 1's Hohenlohe row to the five letters of the register's Hohenlohe link. `docs/LITERATURE_PLAN.md`, section 23.

## The newspapers: SÅ‚owo (1892) sells TrÄ…bczyn (2026-10-22, committed; not published)

- SÅ‚owo, R. XI, nr 2 (4 January 1892), p. 3, the "SprzedaÅ¼e dÃ³br" notice
  (`newspapers/slowo18920104/`), at the editor's word: the snippet named, the
  editor's own crop of the column carried on the item's page (`slowo.jpg`),
  the Crispa digitisation as the `source:`.
- The notice's five printed lines transcribed line by line as printed ("Â¬"
  at the two broken words), read by Tesseract (three passes) with word-level
  zooms; five readings ruled on a spot sheet: **za** (no acute), the buyer's
  **WÅ‚adysÅ‚awowa** (the married form), **peckim** (the print is grammatical),
  the figure **150 wÅ‚Ã³k** against the draft's 159, and both digitisation
  artefacts (the streak before the number, the sliver at the crop's foot)
  left out.
- The item is the press witness of TrÄ…bczyn's sale by Count MiÄ…czyÅ„ski to
  Countess WÅ‚adysÅ‚awowa Wielopolska for 225,000 rs. â€” the transfer the
  wlodzimierz era's ownership line records ("by 1892 Countess Maria
  Wielopolska"); the item sits in that era. Open: whether the press's
  "WÅ‚adysÅ‚awowa Wielopolska" and the era's "Countess Maria Wielopolska" name
  one woman (NEEDS_CONFIRMATION, "The newspapers").
- The index run over it: one hit, TrÄ…bczyn, ruled (`newspapers/index.yml`);
  the notice's "hr. MiÄ…czyÅ„skiego" is outside the MiÄ…czyÅ„ski patterns' forms
  (the genitive after "hr."), said in the notes. The "In the newspapers" box
  on TrÄ…bczyn's page on /places/ now carries the item beside the Kuryer
  Polski's. `docs/NEWSPAPERS_PLAN.md`, section 5.

## The place pages: ZagÃ³rÃ³w (2026-10-22, committed; not published)

- The editor's new section (`places/`, `docs/PLACES_PLAN.md`): a page per
  place that has sources of its own, hung on the place's card on the Places
  page and linked from it â€” "Let's add a new source to a place: ZagÃ³rÃ³w.
  This site has a lot of information that should be added under the place
  name, on a separate page for the place." Built like the newspapers'
  machinery, bilingual like the person pages; a place page hangs on an
  estate card, and the build fails loudly if its slug is no estate.
- The first place, ZagÃ³rÃ³w (`zagorowo`): /places/zagorowo/ and
  /de/orte/zagorowo/ (`pipeline/places/place_pages.py`, collection `places`
  and `places_de`, layout `place`, one viewbar for the whole page, the
  "More about the place" line on the card, the checks in verify_site.py).
- The first source, `zagorowpl20220614`: the town's own presentation on
  zagorow.pl ("Miasto i gmina ZagÃ³rÃ³w" â€” historia, poÅ‚oÅ¼enie, atrakcje,
  kultura), a digital flip-book, kept by the Wayback Machine in the capture
  of 14 June 2022 the editor gave. The editor's rulings of the day: the
  source shown whole (Polish as printed, nothing tidied; Claude's English
  beside it, the English first); a new per-place page; **no pictures** â€”
  the page's photographs (the document of 1240, the coat of arms, the
  flag) stay off the site, their places marked "[Obraz]". The viewer's
  furniture is not kept; the page's slips stand and are recorded
  (`places/zagorowo/zagorowpl20220614/notes.md`).
- What it bears on: the quoted fragment names "Zagorowo" among the villages
  of the confirmation of 1261 â€” the form the edition's Places page records
  from the KDW; the box "Historia" names the OlÄ™drzy of the Puszcza
  Pyzdrska; the page names LÄ…d, RzgÃ³w, Drzewce, Imielno and the rest of the
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
  whole where the relevance is dense, cut to paragraphs with "[â€¦]" elsewhere
  (`notes.md` lists the selection and the cuts): the rural colonisation
  (III.1, pp. 39-42, p. 41 naming "Paul von Kolno-Prusinski, Grundherr von
  Trombezyn" and the founding of ÅaziÅ„sk in 1746), the Prussian colonisation
  (VI.1, pp. 89-93, the towns "Konin, ZagÃ¶-rÃ¶w und Kolo"), the schools of
  the Kalisch land (pp. 45, 112), the Grodziec parish contract of 1796
  (p. 94), the parishes Stawiszyn/Prazuchy/Sobiesenki/Åask/Slesin (p. 102),
  the diocese of Kalisch's parish list "ZagÃ¶row mit dem Filial
  Lissewo-Pyzdry, Konin mit dem Filial Maslaki" (p. 123), the churches of
  the region (pp. 165, 166: the ZagÃ³rÃ³w church of 1878-1896; p. 179 Konin
  and MasÅ‚aki), the inter-war parishes (p. 226, the ZagÃ³rÃ³w pastor Alexander
  GroÃŸ 1923-1945), the brethren's circles in ÅaziÅ„sk (pp. 235-236) and the
  statistics of 1938 with the "rein deutsche evangelische Gemeinde Zagorow"
  (p. 256).
- The false friend ruled out in the scan: p. 101's colony "Trombin bei
  Rypin" (the DobrzyÅ„ land) is not TrÄ…bczyn. Nothing tidied: the print's
  slips stand and are recorded in the notes.
- Index hits read and ruled (140 in the work): new forms `Trombezyn`,
  `ZagÃ¶row`/`ZagÃ¶-rÃ¶w`, `Lazinsk` (the editor's Åazinsk ruling of
  2026-10-22) and `Prusinski` (the print drops the Å„); `Brzyczka` refused
  (Reptowski's colony near ÅÃ³dÅº); old rulings sharpened with exceptions
  (SchrÃ¶ttersdorf, the Posen imprints, "Lissewo-Pyzdry", Dembina- and
  Koneck-Holland, and Wielun now taking the town by exception against
  Guradze's field). One hand-made link: p. 41 against the summons of 1860
  and the boundary decree of 1775 â€” Kneifel names the husband alone, the
  documents the couple; the edition follows the documents.
  `docs/LITERATURE_PLAN.md`, section 24. **Published 2026-10-22** at the
  editor's word.

## The literature: Werner (1904), the parish histories of the province of Posen (2026-10-23, committed; not published)

- Albert Werner, *Geschichte der evangelischen Parochien in der Provinz
  Posen*, Ã¼berarbeitet von Johannes Steffani, herausgegeben von dem
  KÃ¶niglichen Consistorium der Provinz Posen (Lissa: Friedrich Ebbecke 1904)
  (`literature/werner1904/`), at the editor's word with the page images of
  the WBC digitisation (publication 34695, edition 51858) in Downloads:
  "only entry 201 about Wreschen is relevant for the project, hence that's
  what's made available here". The excerpt is entry 201, the parish of
  Wreschen (WrzeÅ›nia), printed pp. 422-424, whole, with the book's title
  page as the work's front. Out of copyright; shown whole as far as brought
  in.
- The entry's bearing on the edition: the Wreschen parish originally served
  the German HaulÃ¤nder country around **Peisern (Pyzdry)** and **Zagorowo
  (ZagÃ³rÃ³w)**, and "eine an deutschen HaulÃ¤ndereien reiche Gegend" went from
  it in 1817 when those places came to Russia - the edition's OlÄ™der ground
  and its place `peyserschen-hauland`. The parish's founding by the
  PoniÅ„skis (1758, 1760, the orangery of 1 May 1778, the parish of 1779),
  the churches of 1822 and 1895, the Filial Wilhelmsau of 1892 with its
  Bethaus of the Royal Settlement Commission, and the ten pastors of
  1779-1904. No document, person or settlement of the edition is named: no
  hand-made links.
- **Read by OCR alone** (no transcription existed, and the scans' text layer
  is not in the repository): the lunaroute document converter over the whole
  pages, the bands and the single lines, the passes checked against each
  other (Fraktur Å¿â†’f/j, ktâ†’ft handled by rule; no local Tesseract on the
  editor's machine). The readings a name or fact rests on that the passes
  did not settle are on the editor's spot sheet (`scratch/werner1904_sheet.py`,
  20 rows with crops; answers to `review/werner1904/query_answers.json`).
  Two identifications from outside the page (Orangeriehaus, against the
  Polish accounts of the same gift; the General Superintendent Hesekiel)
  are recorded in the notes and NEEDS_CONFIRMATION.
- Index hits read and ruled: `Peisern`, `Zagorowo` (the print's German form)
  and `RuÃŸland` stand; refused: the title page's and heading's `Posen` (the
  province and the DiÃ¶zese), `Liegnitz` and `Pommern` (pastors' birthplaces),
  and `Sokolnik` (a village of the Wreschen parish, not the edition's Amt
  Sokolnik - open in NEEDS_CONFIRMATION). `docs/LITERATURE_PLAN.md`, section
  25. The literature has 32 works, 30 on the site (two summary-only). The
  spot sheet open; not published.

## 2026-10-22 â€” The newspapers: the three Lidmanowski texts

- **Three new items** (`newspapers/zdrowie1912z10/`, `newspapers/
  jutrzenka1913z8/`, `newspapers/zdrowie1914z6/`), from the editor's file
  "Texts by Dr. Konstanty Lidmanowski, ZagÃ³rÃ³w (1912-1913).md" â€” English
  and Polish together, each with its digitisation link, the transcription
  secure (the editor's word; no OCR, no spot sheet, no page image carried).
  The first items that are articles of learned journals: two in *Zdrowie*
  (the organ of the Warsaw Hygiene Society) â€” the nutrition study of the
  SÅ‚upca powiat, R. XXVIII, z. 10 (1912), pp. 720-725, and the housing
  survey, R. XXX, z. 6 (1914), pp. 432-440 â€” and one in *Jutrzenka* of
  ÅÃ³dÅº (R. 3, nr 8, 24 April 1913, pp. 7-10), the digest of Lidmanowski's
  attire article in the March 1913 *Zdrowie*.
- **The housing survey dated 1914** against the file's name
  ("1912-1913"): Polona's metadata, the issue's table of contents ("Lidma-
  nowski K. Dr. z ZagÃ³rowa. Jak mieszka lud nasz? . . 432") and the
  literature (Boldyrew) agree. The editor's word.
- **The English came with the file** (made by Claude) and was read
  against the Polish and corrected in session â€” eleven artifacts, among
  them a sentence the translation printed twice (the nutrition text's),
  "several dozen rubles" for *kilkanaÅ›cie* (some fifteen), "woolen sailor
  suit" for *ubranie marynarkowe* (a jacket suit), and the like; every
  correction recorded in the item's `notes.md` with the Polish that
  decided it.
- **Rights**: the author, Dr. Konstanty Lidmanowski (30 March 1865,
  SÅ‚upca - 6 January 1943, ZagÃ³rÃ³w; the Polish Wikipedia's article, with
  Kumosa 1992), died 1943, so Polish copyright (life + 70) lapsed in
  2014 â€” all three shown whole at the editor's word. The Jutrzenka digest,
  if anonymous, out of copyright since 1984 either way.
- **A person entry** `lidmanowski` (reference/people.yml, heading
  "Lidmanowski, Konstanty"), the GÅ‚owiecki shape: no documents of the
  edition, the Jutrzenka digest's "dr. Lidmanowski" ruled to him in
  `newspapers/index.yml` (the one text that names him in its body; the
  Zdrowie articles stand on their issue's table of contents).
- **Open in NEEDS_CONFIRMATION**: the Jutrzenka signature (the
  digitisation unreachable from the working session); the life dates
  resting on Wikipedia; SÅ‚upca as a place of the edition (it is in no
  register, so the powiat's name matches no pattern); the 1914 date.
  `docs/NEWSPAPERS_PLAN.md`, section 5. Not published.

## 2026-10-22 â€” The newspapers: the parish's own chronicle of the ZagÃ³rÃ³w filial

- **A new item**, `newspapers/luteraniezagorow/`: the page "ZagÃ³rÃ³w filiaÅ‚
  Parafii Ewangelicko - Augsburskiej w Koninie" on **Luteranie Konin**
  (luteranie.konin.pl/zagorow.html), the Parafia
  Ewangelicko-Augsburska w Koninie's own website â€” headed "WaÅ¼niejsze
  wydarzenia z Å¼ycia Parafii w ZagÃ³rowie", a chronicle in dated entries:
  the Reformation among the monks of LÄ…d in the sixteenth century; the
  evangelicals from Silesia, Pomerania and Prussia, 1720-1817, under the
  care of the incumbent of the evangelical parish at WrzeÅ›nia; the
  incumbents of Grodziec, Konin and Å»ychlin, 1817-1856, and the filial of
  Grodziec founded in ZagÃ³rÃ³w; the parish erected 24 December 1856; the
  plot of 1857, the foundation stone of 8 May 1878, the consecration on
  the first Sunday in Advent 1882; the cantor's house of 1913; the
  rectory of 16 October 1938; the first service after the Second World
  War, 18 July 1954, the Rev. Karol Åšwitalski; the Evangelical Senior
  Citizens' Home consecrated in the former cantor's house by Bishop
  MichaÅ‚ WarczyÅ„ski, 16 June 1995, closed 30 November 2009; the
  electronic clock and bells, 17 August 2008. Given by the editor as a
  website "so I'd group it with newspapers and journals", with their own
  pasted text as first witness. Worked on a **separate branch from main**
  at the editor's word (other work being done there).
- **The page is undated.** No date anywhere on it; the site's footer reads
  "Projekt i wykonanie Â© Walrom 2011" (the site's making), and the page's
  own menus point its top "Archiwum" at archiwum2015.html and its footer
  menu still at archiwum2013.html â€” the page stands as of about 2015. The
  editor's rulings: **no date in the slug** (the plan's rule for a web
  item given a recorded exception, `docs/NEWSPAPERS_PLAN.md` section 1) â€”
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
  the HTML: the twice-standing "KoÅ›ciÃ³Å‚ Ewangelicko-Augsburski w
  ZagÃ³rowie" is the two photographs' alt/title text, not prose;
  "parafiiz GrodÅºca" of a bare fetch is an artifact, the page breaking
  the line after "parafii" (the transcription keeps the break); the page
  pads the broken second lines of the 1856 and 1995 entries with ten
  non-breaking spaces â€” layout, not text, the break kept and the padding
  not; "plebani" (1938) stands as printed, for plebanii; the "(czytaj
  wiÄ™cej)" of the 2009 entry is a link to the site's own page about the
  Dom Seniora, kept as printed.
- **The index run**: 54 hits in 9 items; the item's three new pairs all
  ruled in â€” `zagorowo` "ZagÃ³rÃ³w" (the heading, the bare nominative) and
  `grodziec` "Grodziec"/"GrodÅºca" (the parish of Grodziec, named by its
  place). Not matched by any pattern: "LÄ…du" (the genitive) and the
  Polish region names "ÅšlÄ…ska, Pomorza, Prus" (the register's Schlesien
  pattern is the German word only) â€” the same open question as the 2015
  report's LÄ…d forms (NEEDS_CONFIRMATION, "The newspapers").
- **What it bears on**: Werner (1904), entry 201 â€” the Wreschen
  (WrzeÅ›nia) parish that served ZagÃ³rÃ³w's evangelicals until 1817 is the
  page's "1720 - 1817 ... we WrzeÅ›ni", and the page's Grodziec, Konin and
  Å»ychlin years are the story Werner's entry stops at; Kneifel (1964) â€”
  the church of 1878-1896 (the plot, the foundation stone, the
  consecration) and the diocese list's "ZagÃ¶row mit dem Filial
  Lissewo-Pyzdry". The page names no sources; nothing in it contradicts
  the edition's documents. Not published.
  `docs/NEWSPAPERS_PLAN.md`, section 5;
  `newspapers/luteraniezagorow/notes.md` first.

## 2026-10-22 â€” The literature: SÅ‚owiÅ„ski and PoÅ‚om (2024), "Zerwane ogniwo", and SÅ‚owiÅ„ski (2023) finished

- **A new work**, `literature/slowinskipolom2024/`: the collective volume
  *Zerwane ogniwo. Ewangelicy na ziemi zagÃ³rowskiej* (ZagÃ³rÃ³w: UrzÄ…d
  Miejski w ZagÃ³rowie 2024, edited by MirosÅ‚aw SÅ‚owiÅ„ski and Katarzyna
  PoÅ‚om, ISBN 978-83-969906-0-0), from the editor's checked Polish and
  English Markdown exports of the same day (made from the PDF's text
  layer; the PDF and the .md files not kept in the repository). All 336
  printed pages read: the studies (the parish history, the HaulÃ¤nder
  settlement of 1746-1806, the interwar church, the kantors, the Beutlers,
  the Mielke letters, Breede), the memoirs (Erich Kuhn's among them) and
  the German-era testimonies (*Der Heimatbote*'s note on ÅaziÅ„sk, the
  chronology table, the 1945 inhabitants list of MichalinÃ³w
  TrÄ…bczyÅ„ski/ÅaziÅ„sk/Huta TrÄ…bczyÅ„ska, the forged Reichsstelle document).
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
  and SÅ‚owiÅ„ski 2023): in the repository for questions, `visible: false`,
  the site showing the detailed summary in both languages and none of the
  text (verify_site.py checks - one stretch the two SÅ‚owiÅ„ski summaries
  shared, the Mielke letter's "temples" sentence, shortened in the older
  one so the check stays clean).
- **SÅ‚owiÅ„ski (2023) committed alongside** (the folder had stood untracked):
  its English is the editor's own English .md, not the planned Claude
  translation (`slowinski_md.py --english`; `translation_chunks/` left
  untracked); its year corrected to 2024 where the texts spoke of the
  sister volume (the title page's).
- **What it bears on**: the 1718 founding of ÅaziÅ„sk a third witness (the
  ruling still wanted); the founders of 1746 in yet another form; the
  Mielke dates conflicting (NEEDS_CONFIRMATION). The work is invisible, so
  no index rulings and no hand-made links (the precedent). The literature
  has 34 works, 30 on the site and four summary-only. `docs/LITERATURE_
  PLAN.md`, section 26. Not published.

## 2026-10-22 â€” The newspapers: Echo Tureckie, R. 8, nr 18 (6 maja 1931), nr 379, "ZajÅ›cie w ZagÃ³rowie"

- **A new item**, `newspapers/echotureckie1931018/`: the ZagÃ³rÃ³w edition
  of the Turek weekly Echo Tureckie's report of the clash at the
  recruiting commission of 24 April 1931 â€” the workers' crowd stoning the
  premises when the season's quota ran out, the starosta of SÅ‚upca
  arriving with reinforcements of police, the second storming, the
  dispersal, a dozen or more persons arrested â€” anonymous, no signature
  and no siglum. From the blog **ZAGÃ“RÃ“W-MIEJSCE Z HISTORIÄ„** (the
  editor's word for the title; the same post of 2 October 2024 the 1937
  clipping came from, the file's leading "8." the image's order in the
  post), the rights approved, the clipping carried on the page, the item
  shown whole.
- **Read by four Tesseract passes** â€” the Windows.Media.Ocr engine, the
  plan's third witness, unavailable the day (`winrt` not importable in
  the session's Python) â€” with six rulings on a spot sheet
  (`scratch/et1931_sheet.py`, port 4108): "widowniÄ…" the print's
  line-broken word (the engines' shared "hiÄ…" the print's fractured "Å„"),
  the mark on the k of "rekrutacyjna" not a letter, "kontyngent" against
  the engines' agreed "kontygent" (the print carries the n), the
  right-edge sliver and the final line's leading mark left out, "lokal."
  with its period. This clipping breaks its words **with printed
  hyphens** (the Kuryer Polski and the 1937 clipping broke without), so
  the "Â¬" convention appears nowhere.
- **The editor's rulings of the day**: the paper's title Echo Tureckie
  ("ZagÃ³rÃ³w" the edition's name; the `newspaper:` field carries Echo
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
  â€” the "Z ZagÃ³rowa" column of Dziennik PoznaÅ„ski of 1937 records the
  trade as routine, this item its violence six years earlier; both from
  the same blog post. The item names nobody; the index's hits are
  ZagÃ³rÃ³w's three forms, already ruled. The report's "yesterday" against
  the issue's 6 May is the dispatch's own arithmetic, recorded in the
  summary, corrected nowhere. `docs/NEWSPAPERS_PLAN.md`, section 5;
  `newspapers/echotureckie1931018/notes.md` first.

## The newspapers: Kurjer PoznaÅ„ski, "(Zhitleryzowani koloniÅ›ci)" (2026-10-22, committed; not published)

- The anonymous note in Kurjer PoznaÅ„ski of 12 July 1933 (`newspapers/kurjerpoznanski19330712/`), the eleventh item of the press and the third from the blog ZAGÃ“RÃ“W-MIEJSCE Z HISTORIÄ„ (its post of 24 May 2024, "To i owo, cz. 2"): the German colonists of the rural communes of OleÅ›nica, TrÄ…bczyn and Szymanowice around ZagÃ³rÃ³w, whose colonies once bore German names (Emilienhain, Ludwigslust), who since Hitler's taking power in Germany "as if something turned over in their heads" speak German at the commune office and answer German to a Polish "dzieÅ„ dobry" at school â€” and the closing incident: the school where an Evangelical taught, empty of the colonists' children on the school inspector's visit, the teacher dismissed from his post after it. The citation carries the date only (the clipping gives no issue number): `kurjerpoznanski19330712`.
- **Read by OCR, four passes** (Tesseract best and standard, Ã—3 and Ã—4, psm 6 and 4) with the doubtful places settled at the pixel level first (the ogonek of "TrÄ…bczyn" â€” the print has it and every pass dropped it â€” the Å‚ of "nosiÅ‚y", the Ä™ of "jÄ™zyku" and "uczÄ™szczajÄ…ce", the g of "ewangelik" where two passes read "selik", the period after "NiemcÃ³w", the comma after "Hitlera", the period after "przekrÄ™ciÅ‚o", the â€žâ€¦â€ round "dzieÅ„ dobry"), and four rulings on a spot sheet: the parenthesised lead "(Zhitleryzowani koloniÅ›ci)." with the word set solid (the completive z- on hitleryzowani), "Ludwigslust" (the German form, against the passes' split), the plain "a" of "nie w polskim a niemieckim jÄ™zyku". The print's "kolonje" stands as printed; nothing tidied, 22 lines, the "Â¬" at each break.
- **Shown whole** (`visible: true`): anonymous press of 1933, the rights approved on the 1937 clipping's ruling; the clipping carried on the item page (a genuine JPEG this time, 648 Ã— 573, unlike the Dziennik's WebP in .jpg clothing); the English Claude's, the standing caveat.
- **What it bears on**: the press witness of the colonists' "hitleryzacja" seven years before the 1942 feature's "purely German settlement" of the same population; the print's "Emilienhain" against the documents' "Emilienheim", and the dismissed teacher identified by nothing the edition holds (both NEEDS_CONFIRMATION). `docs/NEWSPAPERS_PLAN.md`, section 5. Not published.

## The register: Ludwigslust (2026-10-22, at the editor's word)

- **Ludwigslust made a place of the edition** (`reference/places.yml`, `ludwigslust`, kind settlement, tier Book-confirmed, `match: 'Ludwigslust\w*'`): the colony of the ZagÃ³rÃ³w lordship's dismemberment â€” named in the edition's own documents (Oe 1 BÃ¼ 9454: letter 24's list "12 Ludwigslust"; letter 177's naming list "Friedrichsfeld, Ludwigslust. = GrÄ…dzyÅ„." and its register of new villages "7. Collonie von 1590 Morgen besezt mit 40 wirthe heiÃŸ Ludwigslust") and in the literature (Breyer 1935 Gaue among the villages keeping their old German names; Breyer 1938's section "Ludwigslust - MaÅ‚y Las" with the refused petition of two colonists to the KÃ¶nigsberg government of August 1816 in the name of 10 families; WÄ…sicki 1953's list of the villages founded on Hohenlohe's estates; SÅ‚owiÅ„ski and PoÅ‚om 2024, "Kolonia Ludwigslust (obecnie MaÅ‚y Las)"). The editor's word came with the Kurjer PoznaÅ„ski item, which names the colony among the German-named colonies around ZagÃ³rÃ³w.
- **The Polish name recorded, not matched**: "MaÅ‚y Las" (SÅ‚owiÅ„ski and PoÅ‚om's "obecnie", Breyer's section title) is a `match: false` variant â€” a common-noun phrase a bare pattern would catch all over the corpus.
- **An open question recorded in the entry**: the naming list and the register of new villages, two enclosures of the one letter (177), do not agree which old ground the colony sat on (the naming list pairs it with GrÄ…dzyÅ„, the register lists it under "bey Kopojno").
- **The literature's six hits ruled** (`literature/index.yml`: breyer1935gaue one, breyer1938 four including the adjective "Ludwigsluster", wasicki1953 one; `--check` passes), and **the item's fourth hit** in `newspapers/index.yml`.
- **The corpus dataset rebuilt on the merged tree** (`pipeline/build/build_dataset.py`, then build_site_data, Jekyll, verify_site all pass): oe1bu9454-177 and oe1bu9454-24 gain their Ludwigslust place mentions (the surfaces stood unlinked, `entity: ""`, since no register entry existed), `corpus/index/place_mentions.json` and the site's `places_named.yml` carry the place; the two letters' pages relinked. The Mielke catch-up in Breyer's notebook (app539680669-1) the parallel session's rebuild had already made (its commit e6ea4f43); the merge carries it once.

## Deliverables produced

`letters.csv` / `letters.json` (database), `von_Triebenfeld_Hohenlohe-Ingelfingen_chronological.txt`, `collation_48_302.md`, `transcription_error_profile.md`, `phase2b_transcription_audit.md`, `currency_normalisation_report.md`, `parsed_dates_review.csv`, `phase2_proper_noun_report.md`.

## 2026-10-23 - The literature: Kraus (2001), chapter III and Anlagen 8 and 10

- **A new work**, `literature/ostensacken2001/`: Gerlinde Kraus,
  *Christiane FÃ¼rstin von der Osten-Sacken: Eine frÃ¼hkapitalistische
  Unternehmerin und ihre Erben wÃ¤hrend der FrÃ¼hindustrialisierung im
  18./19. Jahrhundert* (Stuttgart: Franz Steiner 2001, BeitrÃ¤ge zur
  Unternehmensgeschichte Bd. 10), the biography of the mother of
  Marianne GrÃ¤fin von Hoym, the Prince's wife. Chapter III whole (printed
  pp. 33-42) and, from the appendices, Anlage 8 (the daughter's letter of
  12 October 1811, "Ein Wort des Vertrauens") and Anlage 10 (the mother's
  codicil of 6 November 1807) - the editor's word "Skip what's between"
  keeps Anlage 9 and the first lines of Anlage 11 out, marked with `[.]`
  (the Kneifel convention). Read from the editor's two-up page scans by
  two OCR engines checked against each other (Tesseract 5.5.3 with the
  German traineddata installed for the newspaper work - found on the
  machine though not on PATH - and the lunaroute converter), doubtful
  words read at 3x-6x zoom crops; the readings settled and the print's own
  slips (â€žZransact", the "(1792-1822)" of Hardenberg, "VollblÃ¼tigkeit",
  the codicil's "60/m tausendstel") written out in the work's notes.md.
  Footnote keys page-scoped (`[^p33-1]`, `[^p325-4]`) because the
  chapter's notes 1-43 and the Anlagen's own numbering collide.
- **The copyright ruling**: the book is in copyright (2001, the imprint
  forbids reproduction and translation). Put to the editor with the
  summary-only rule named (section 4 of the plan), they ruled "Full text,
  at my word" - `visible: true`, the third full-text exception (the
  TwojaSÅ‚upca report, Werner's entry).
- **What it bears on**: p. 42 - the prince sold the lordships "Betsche,
  Zogorowo, Trobczyn, Botkowo und Winiec weit unter Wert" to come by
  "baare Mittel", the book's spellings of the edition's ZagÃ³rÃ³w and
  TrÄ…bczyn among them. A hand-made link ties the passage to the royal
  consent of 28 January 1806 to the parcelling of "Zagurowo und Trompczyn"
  (app539680801-2). The new spellings entered as literature-only patterns
  in `literature/index.yml` and ruled; Baildon, Cosmar, Glenk,
  Kircheisen, Emilie, the princes August, Adolph and Alexander, Ã–hringen,
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

## 2026-10-23 - The newspapers: the death notice of WÅ‚odzimierz hr. MiÄ…czyÅ„ski

- **A new item**, `newspapers/dziennikpoznanski18791220/`: the nekrolog in
  the black-bordered box on p. 4 of Dziennik PoznaÅ„ski, R. 21, nr 292 of
  20 December 1879 (the WBC digitisation, sygn. Cz4293 of PAN Biblioteka
  KÃ³rnicka, "domena publiczna") â€” the press witness of the death of Count
  WÅ‚odzimierz MiÄ…czyÅ„ski, "dziedzic majÄ™tnoÅ›ci TrÄ…bczyna w KrÃ³lestwie
  Polskiem", at TrÄ…bczyn on the 18th of December 1879 after long
  sufferings, "opatrzony ss. sakramentami"; the "Ekspedycya zwÅ‚ok" on
  Monday the 22nd, the funeral "nazajutrz"; signed by the grieving nephew,
  WÅ‚adysÅ‚aw hr. MiÄ…czyÅ„ski of PawÅ‚owa. The section's first death notice,
  and the press witness of the event the wlodzimierz era's ownership line
  turns on (it names the nephew who succeeds).
- **Read by Tesseract** at the editor's word (the item's own readings
  ruled in session; the doubtful list in the item's notes.md): the
  microfilm's 300 dpi page defeated the display-capital name line and the
  body's first word ("ZmarÅ‚"), so the issue's DjVu was fetched again from
  the WBC (`/Content/84585/DjVu/0004_0001.djvu`) and rendered at 600 dpi,
  where the same lines read â€” the heading "WÅ‚odzimierz hr. MiÄ…czyÅ„ski,"
  one giant line, then "dziedzic / majÄ™tnoÅ›ci TrÄ…bczyna / w KrÃ³lestwie
  Polskiem," stacked, then the body. Open readings: "Polskiem" (the 600
  dpi crops suggesting "PolskÃ©m"), "Ekspedycya" (against the passes'
  "Eksportac"/"Ekoportacja" shapes; the standard phrase and the descender
  pattern decide), and the funeral day after "nazajutrz" â€” the glyph
  reads as an 8 to every pass but is no digit to the English engine set to
  digits alone, and the sense after a Monday the 22nd allows only the 23rd.
- **The death date stands against the edition's records**: the notice says
  the 18th of December, the editor's ruling of 2026-10-15 (the notebook
  APP 53/968/0/-/716) the 20th â€” and Å»ychliÅ„ski (1891, p. 222) has the
  18th too, the question already open (NEEDS_CONFIRMATION, "The
  literature"). The notice is a period witness on Å»ychliÅ„ski's side; the
  documents first, the ruling the editor's. The item keeps the press's
  date as printed.
- **The index run**: one hit, TrÄ…bczyn, standing under the ruling already
  in `newspapers/index.yml`; no new rulings needed. The Count's own
  mention the register's patterns bring in nowhere (the WÅ‚odzimierz
  entry's `only_in` pin to the summons of 1860; the bare "MiÄ…czyÅ„ski"
  under the 2015 report's standing "no" ruling).
- The image carried on the item's page (the editor's 0004_0001.jpg of the
  WBC download). The item is visible (anonymous press of 1879, public
  domain); committed, not published; publish at the editor's word.


## 2026-10-23 - The gazetteer: the editor's index of places (step 1, the import)

- **The editor's "Place Names.md"** (their own index of the places around
  TrÄ…bczyn and ZagÃ³rÃ³w: 112 entries, 21 cross-references, 119 footnotes)
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
  the foliation checked against five quoted phrases; the LÄ…d copy-book,
  the lease of 1806, Breyer's notebook, the village table of 1797, the
  visitation of 1791, ChodyÅ‚a, Breyer, Szwiec, SÅ‚owiÅ„ski & PoÅ‚om,
  Minakowska, the glossary's "stawisko"). The Kodeks no. 1464 (1362) the
  edition holds as the LÄ…d copy-book's copy, and the footnote links to it.
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
  Prince's lists of 1805-1808 write them; AugustynÃ³w and the lease of 1806;
  the archive of the visitation; the renaming of 1891; four identifications
  with the register). The 1287 of the exchange of WrÄ…bczyn agrees with the
  Kodeks (no. 685 confirms in 1292 an exchange "made five years before").
- **The editor's voice**: the file analysed as a fourth sample, of index
  entries, with a brief of its own (`docs/EDITORS_VOICE.md`); the editor's
  remark on method made a house rule (`docs/HOUSE_STYLE.md`, "No method
  talk").
- The parsing and the scripts were done by a Sonnet sub-agent at the
  editor's word (WORKING_NOTES, "Working with the editor"); its output read
  and the links spot-checked before commit.

## 2026-10-23 - The gazetteer: "Stara Huta OlÄ™dry", a name of two places

- The editor's cross-reference "*Stara Huta OlÄ™dry* â€” See **Huta**" pointed
  to no entry. The edition's sources use the name for both Hutas, and the
  editor ruled it listed as both (2026-10-23): a name item with
  `shared_with` and its sources in each entry. Huta TrÄ…bczyÅ„ska: SÅ‚owiÅ„ski
  (2023), p. 98 (ÅaziÅ„sk Drugi "dawniej ... Holendry Stara Huta"),
  ChodyÅ‚a (2015), p. 84, note 154, the village table of about 1797, entry
  283, and the Prince's papers of 1806 (Oe 1 BÃ¼ 14526, document 8; Oe 1
  BÃ¼ 9454, letter 24), beside Richter 1843's "H. Stara Huta". Huta
  Åukomska: ChodyÅ‚a, pp. 70 and 76, and the 1797 table, entry 281. A third,
  Stara Huta-GrÃ³jeckie OlÄ™dry in Grodziec parish, is not to be confused
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
  map over OpenStreetMap. A pilot (proposed: Åukom 1766) before the rest.
- **The editor chooses the maps** (2026-10-23: "I will be selective with
  them"): the plan, `reference/maps.yml` and the missing list say so; the
  list's maps section is now "Maps cited", not a list of wants.
- The editor agreed the plan's recommendations (2026-10-23): the second
  repository for the tiles, the pilot Åukom 1766, libvips (installed:
  pyvips 3.2.0, libvips 8.18.7). MapWarper's API answers: a map's
  record gives the uploaded image's size, its `gcps` the control points
  (Åukom 1766: five). The map's original is the file of that size (for
  Åukom the PNG, not the JPG), recorded in MAPS_PLAN, section 5.

## 2026-10-23 - The maps: the pilot, Åukom 1766

- At the editor's word ("go ahead with the Åukom map ... Let's only do this
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
- **Åukom 1766**: the editor's north-up PNG (10,280 Ã— 8,523) as the
  original, `view_rotation: 180` (drawn south-up, the editor's word); 502
  tiles, 15.8 MB; five control points, affine RMS 336 m; the warp test
  page. The gazetteer's nine names to find read against the text first:
  MyszakÃ³wek marked absent (the entry says it is not on the map), the stray
  "Stara Huta" item of Huta Åukomska removed, Imielno's *Dezerta Iemielno*
  supplied, Stawisko's *Brod Kaliski* noted as the crossing west of it
  (`maps/lukom1766/notes.md`).
- **The procedure recorded** for the next maps: `docs/ADDING_A_MAP.md`
  (what the editor does, what Claude runs, the traps).
- **The editor's first marks imported** (ten labels, among them MyszakÃ³w,
  which they added). At their word two readings corrected, read on the
  image: *Lomaw* (no Å) and *Dezerta Jemielno* (a J), in the labels, the
  map forms and the entries' text. The inscription *Tres mansi ConventÃ»s
  Landensis* they pointed out added as a label (the abbey of LÄ…d's three
  mansi, the purchase of 1447/1461 in the LÄ…d copy-book; its place in the
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
- **Tres mansi ConventÃ»s Landensis** recorded under GrÄ…dzeÅ„ as its second
  appearance on Åukom 1766, linked to the LÄ…d copy-book's documents of 1447
  and 1461, at the editor's word; label 025 now belongs to GrÄ…dzeÅ„.
- **Padding at both ends** of a band and its crop (the editor's word; a
  Sonnet sub-agent).
- **The final marks on Åukom 1766** imported (the editor's bands, 100 to
  240 pixels): eleven labels, eleven crops whole and upright. The import
  fixed for a second run on the same map: it reuses the gazetteer item
  linked to a label and unlinks labels deleted since (it would have added
  a duplicate for every place).
- **The warp checked by the editor**: the map lands in the right place
  ("This map is very crudely drawn so it's not perfect"). Allmaps handles
  the level-0 static tiles, the pilot's open point.

- **The gazetteer's five new entries entered** at the editor's word
  ("Yes to the gazetteer entries"), 2026-10-26: ÅaziÅ„sk Pierwszy and
  ÅaziÅ„sk Drugi (split from `lazinskie-oledry` at their ruling of the
  day, the combined entry standing as the OlÄ™der settlement before the
  split) and Orlina DuÅ¼a, Stawiszyn and Zbiersk Kolonia, drafted from the
  editor's cemetery survey. The gazetteer's checks pass (117 entries);
  the Places page's tier 1 carries the five; the cemetery pages of Orlina
  DuÅ¼a, Stawiszyn and Zbiersk Kolonia now link their places on the
  Places page's index, and ÅaziÅ„sk Pierwszy's page links its own entry.

## 2026-10-26 â€” The cemeteries: the section planned and built (branch `cemeteries`)

- **The editor's survey of the Evangelical cemeteries** of the
  TrÄ…bczyn/ZagÃ³rÃ³w area and its neighbourhood brought in as a fourth
  section (`cemeteries/`, plan `docs/CEMETERIES_PLAN.md`): ten cemeteries
  visited on one visit in 2023 (the editor's word), each with its page in
  both languages â€” the survey's account of its condition kept as written,
  the headstones as a table (Name / Born / Died / Note), the readings kept
  as the survey has them, nothing tidied, the same table on both pages. No
  person entries behind the names (the editor's word). The asterisked
  numbers beside eight readings are genealogical identifiers for certain
  Zelmers/relations and are kept, in the note column's place and explained
  in one line under the table (the editor's ruling, the second batch of
  the day); the survey's figure references ("Fig. 25" and its neighbours)
  are left off the pages (the editor, the same day). About 200 rows: 5 at
  ÅaziÅ„sk Pierwszy, 11 at Huta ÅaziÅ„ska, 81 at MichalinÃ³w TrÄ…bczyÅ„ski
  (two stones carrying two names, the survey's "&"), 20 at
  WrÄ…bczynkowskie Holendry, 62 at Orlina DuÅ¼a, 10 at Anielewo, 2 at
  Friedrichsfeld, none read at MichalinÃ³w gm. OleÅ›nica, 3 at Stawiszyn,
  8 at Zbiersk Kolonia.
- **The Places page widened** to a general index of places (the editor's
  ruling; `docs/PLACES_PLAN.md`, section 7): tier 1 the places of the
  TrÄ…bczyn/ZagÃ³rÃ³w area â€” the gazetteer's 112 places and the register's
  `area: trabczyn-zagorow` ones (the 27 the gazetteer registers, plus
  SÅ‚upca, Konin and Kalisz) â€” tier 2 the register's remaining 126. The
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
  Friedhof in ÅaziÅ„sk Drugi", Arbeitsgemeinschaft Ostdeutscher
  Familienforscher (JÃ¼rgen Frantz, 31 July 2016), members-only â€” cited
  behind one reading of Huta ÅaziÅ„ska, not held
  (`docs/MISSING_SOURCES.md`). The five new gazetteer entries (ÅaziÅ„sk
  Pierwszy and ÅaziÅ„sk Drugi split from `lazinskie-oledry` at the
  editor's word, and Orlina DuÅ¼a, Stawiszyn and Zbiersk Kolonia) are
  drafted in `scratch/gazetteer_drafts/` and wait on the editor's eye.

## 2026-10-26 - APP 53/21/0/-/Pyzdry Gr.115 added, translated and published (branch app5321pyzdrygr115)

- The holding built: the head of the table of the parish of TrÄ…bczyn on
  page 543 of the Relationes [protocollon] of 1791-1792, the register of the
  grod court and office of Pyzdry (fond "KsiÄ™gi sÄ…du i urzÄ™du grodzkiego w
  Pyzdrach"), from the editor's own transcription, given as a spreadsheet
  export and kept as `intake/table.csv` as received. One document, one page
  (`0543_a`, the editor's own trim of the photographed page), seven rows and
  a heading row: the village of TrÄ…bczyn, the parsonage, NowawieÅ›, Osiny,
  Åazy, "Kuznia MaryantÃ³w" and "Hollendry Luzne Stare i nowe z HutÄ…", each
  with its hearths (dymy rolne) and the two figures the headings call "gara
  zyta" and "gara owcza".
- Only `543_trim.jpg` is used, the editor's word; the spread `542v-543.jpg`
  stays out, and only the table in the page's first half is transcribed.
- The one reading changed at the editor's word, given in chat while they
  were away from the PC: the heading's "Parofie" is "Parafie" (applied by
  the intake script's `--correct`, logged).
- The editor's rulings of the day: "Kuznia MaryantÃ³w" is the Marianton of
  the edition - MariantÃ³w, where the Hohenlohe patrimonial court for
  TrÄ…bczyn sat. `reference/places.yml` (`mariantow`) now also matches
  "MaryantÃ³w", which brings the Prussian table's "Maryantow."
  (agad1169011745, row 175, unmatched before) in as well; 4 hits in 3
  documents, each line read. The TrÄ…bczyn figure (22, where the doubling of
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
  "MaryantÃ³w" (above), the comma-bounded "Åazy" of the table rows (the
  hearth-tax register's entry 180 comes in with it), and "Hollendry Luzne
  Stare i nowe" matched to both OlÄ™der colony entries, as the visitation's
  "OlÄ™dry nowe i stare" already is.
- The editor's closing word of the day, in chat: "No spot sheet is
  necessary - use my transcription, which is correct." The figures stand as
  transcribed (the village's row 21, 22, 84), the "gara" headings stand as
  written, and no dated heading is carried - the document stays undated.
  The sheet built for the holding was removed from the branch unused and
  its server stopped. Open: only whether the Huta of the Hollendry row is a
  distinct place (NEEDS_CONFIRMATION).
- The glossary gate passes (0 candidates); the site verifies clean (628
  documents, text exact, tables checked cell by cell). The edition guide's
  counts corrected (forty-nine holdings) and the PoznaÅ„ bullet extended,
  English and German; the era's blurb names the table. Published at the
  editor's word, 2026-10-26: merged to main with the Szetlewicz holding
  built in parallel (the edition 629 documents in 50 holdings) and pushed.
- Still open (NEEDS_CONFIRMATION): whether the Huta of the Hollendry row is
  a distinct place.

## 2026-10-26 - APP 53/968/0/-/782: Tropiczyner Holl. identified; published

- The editor ruled: "Tropiczyner Holl.", the contract's dateline, is the
  OlÄ™dry on TrÄ…bczyn - the TrÄ…bczyÅ„skie Stare OlÄ™dry, the edition's
  canonical settlement (its later name ÅaziÅ„sk). Recorded in
  reference/places.yml as a matched variant of trabczynskie-stare-oledry
  (it hits the one document only, counted before matching); the place of
  writing override carries the manuscript's form and the build shows the
  canonical name the pattern resolves to. The holding's page names the
  identification, both languages.
- No timeline event (the editor's word): the contract bears on the colony's
  school, not directly on the owner.
- Still open: "Borwiezer Holland"; whether the ruling covers the
  "TrÄ…bczyner HollÃ¤nd" spelling of oe1bu14526-17; "6 gl."; the glossary
  terms (NEEDS_CONFIRMATION).
- Published at the editor's word.

## 2026-10-25 - APP 53/968/0/-/782: the line division ruled

- The editor answered all 7 rows of the holding's spot sheet. Corrections
  applied to the transcription: term 9 breaks after "Ostern" and after
  "Wirt" (not after "Weinachten" and "einem"); term 10 breaks after "und";
  the closing sentence's third line runs "Mann fortzusetzen. Die Sontags
  Schule so wie" (no break after "Sontags"); the board's last line breaks
  before "wir" ("... zu erfÃ¼llen worauf / wir uns Eigen-hÃ¤ndig
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
  forty-eight holdings) and the PoznaÅ„ bullet extended, English and German.
- Open on the editor: the spot sheet; "6 gl." gulden or Groschen; the
  identifications of "Tropiczyner Holl." and "Borwiezer Holland"; glossary
  entries for the single-document terms; a timeline event and the era's
  story (TODO section 36).

## 2026-10-26 - APP 53/20/0/-/PoznaÅ„ Gr.1181 added, translated and published (branch app5320pozgr1181)

- The condescensio decree of 29 March 1784 on the ultimate limitation of the
  Prusimski succession, one Latin document on the editor's fourteen page
  photographs (pp. 161-167v of the relationes protocollon), era
  `prusimski-boundary`. The editor's own transcription, split into pages and
  settled in session before the first build: 108 readings applied, each with
  its witness in `units/app5320pozgr1181/intake/changes_applied.md` (case
  endings where the grammar admits one reading, the register's formulas, and
  forms attested in the sibling units Konin Gr.115-118 and 153; the scribe's
  spellings kept). The dating proven by the weekday formulas: the actum
  Monday after Judica = 29 March 1784; the December terminus 1 December 1783
  (not 1785); "sab~bo" 13 December 1783. 66 readings stand open on the spot
  sheet, published for the editor away from the desktop at
  takaji10.github.io/triebenfeld-spot/sheets/app5320pozgr1181/ (the new
  sheets repository; the crops placed by machine and unchecked - every row
  carries a "wrong line" button). The site builds and verifies clean with
  the unit in place (627 documents in 48 holdings, main untouched).
- The same day, evening: the editor's fresh line-by-line p. 161 came back
  keeping the original doubts, and the 108 completions were withdrawn - the
  editor's word is the source of truth. Five readings settled by that pass
  stand in the corpus (the December year 1783, "videlicet" before the day
  numeral of October 1782, "Mens(is) Junii", "oblatam porrecto", the break
  "camera-/riali", and the full stop after "acclamante."). Lineation of pp.
  161v-167v ruled optional by the editor (the meaning is readable; citation
  can zoom): the pages stand by paragraph as Konin Gr.117 does, p. 161 keeps
  the editor's own lines, and the machine lineation drafts are not built.
- The editor's word to integrate, merge and publish. Translated in session
  (no paid run), page by page under the pipeline's own rules, written to the
  translation cache through translate.py's own save() so the record carries
  the source hash; summaries in both languages; the claim check made in
  session under the --verify rules, 13 statements all supported after three
  corrections of the draft (three daughters, not four; the decree's two
  paternal figures, 154,436 gr 24 1/2 for PaweÅ‚'s scheda at p. 166v and
  154,936 gr 24 1/2 for the captain's own at p. 167, each aright for its own
  scheda; the Nierzychowska ground, quieted 1740 and refused as a load borne
  over, not "not provable as paid"). The checker's two real catches fixed
  (TrÄ…bczyn in the English outside the quoted snippets; "engrossed"
  rewritten "entered at length"), the Latin-source false positives cleared
  in reference/translation_rulings.json with the reason recorded.
- The glossary gate ruled green: Jacobi excluded (the man's name, not the
  feast), Junii excluded (the month's genitive, plain in English), and the
  gulden entry's pattern widened to the bare "fl.", which the Latin of the
  PoznaÅ„ books defeats the figure-before form with ("sex fl. gn[?] 20").
  The literature index: one new ruling (Breyer 1938 p. 17, an estate
  "Brzezno" on the KoÅ‚o-Konin road, yes) and one stale row cleared (the
  szetlewek refusal of "Szetlewo", stale since the szetlew split of the
  relatio holding).
- The index extended: twelve people (Skarbek, ZelisÅ‚awski, the five
  sisters'-heirs parties as family entries, the abbot and prior of LÄ…d, the
  RadoliÅ„skis, Bienicki, the GoliÅ„ski family with the ADWl 85 Golinska
  kept out), seven places (Oporowo with its shares folded in and the map
  link firm at gmina Krzemieniewo - OporÃ³wko and the hamlet KaÅ‚owo-in-
  Oporowo answer the decree's shares OporÃ³wka and KaÅ‚owa, and the 1673 sale
  before the castellany acts of Wschowa fits the region; Prusinowo,
  Wierzbno, Brzezno with the manuscript's "Breczno", Chyby, Jaryszki with
  the map link at gmina KÃ³rnik, Radolin with the family name kept out of
  the pattern), each with its open questions written where the modern
  identification is open, and no map link there.
- The timeline gains the decree of 29 March 1784; the edition guide's
  hand-kept counts corrected in both languages (630 documents, 2,103 pages,
  626 translated, 51 holdings, the PoznaÅ„ archive 24 holdings and 95
  documents, the decree named). origin/main (the Pyzdry Gr.115 holding and
  the Szetlewicz relatio) merged into the branch; the derived files took
  main's side, the four authored conflicts hand-merged, the two JSON caches
  by union. Status translated; the spot sheet stays open, its answers to be
  ruled in when they come.
- Published at the editor's word the same evening: the branch (with the
  cemeteries work and the gazetteer's five new entries merged in as main
  moved) fast-forwarded to main and pushed; the "Build and deploy" run
  40393701490 succeeded and the decree answers on the live site. The
  cemeteries session's worktree sits on the `cemeteries` branch, not main
  - a merge run there fast-forwarded that branch by mistake and was reset
  back; main was moved with `git branch -f` from a fresh fetch (the lesson
  in WORKING_NOTES, "Two sessions, one working copy").
- Two rulings of the publish evening applied at once and republished: the
  scribe's Capitaneus renders starost, not captain (the editor's word; the
  standing rule of Konin Gr.119), in the English, the German, the
  summaries, the holding's pages, the timeline and the story - the
  transcription keeps the manuscript's form; and there is no content past
  167v (the editor's word) - the register ends at the mid-sentence break,
  no next leaf exists, every "continues on the next leaf" sentence was
  withdrawn, and the sheet's tail_167v row came off (the sheet rebuilt and
  republished, 61 rows).
- The starost's seat settled the same evening, in three steps of the
  editor's word: not NieÅ›wieÅ¼ (the session's own misreading, withdrawn);
  then Nieszczewice by the session's first reading of "Nieszczewic e";
  finally NISZCZEWICE by the modern spelling - which is the spelling the
  rest of the edition had carried all along (the register's people entry,
  fifteen sibling holdings, the era essay). The correction ended where it
  began: this holding's renderings now say starost of Niszczewice like
  every other text of the era; the manuscript's Nieszczeviec- stem stands,
  its endings still on the sheet.
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
  Polonisation of German surnames in the gmina ZagÃ³rÃ³w, seven documents on
  ten pages (the folder photograph left out; 0034 carried as "(skipped)",
  shown but not transcribed, at the editor's word). All scans paired.
- The four list sheets read by the machine reader in bands and settled on
  the editor's spot sheet "Readings in Breyer's sheets 1" (30 of 31 rows
  answered 2026-10-25; two rows unanswered, recorded in the holding's
  notes). The prose sheets 0031-0033 are the editor's own transcription,
  kept as typed; their doubtful words recorded in
  `units/app539680545/intake/unresolved.md`.
- Translated in session (intake/translation/, write_cache.py); the check
  clean after it caught the page split of document 5, the edition's WrocÅ‚aw
  for Breslau, and doubt marks the German does not carry.
- Summaries written in both languages in session
  (intake/write_summaries.py) and claim-checked in session
  (intake/claim_check.yml): 33 statements, two corrected in the draft (the
  "Gem. ZagÃ³rÃ³w" line, and where the schools lie).
- The holding's page written in both languages; check_unit_text clean after
  it caught four citations ordered so the years stood past the documents
  that carry them.
- Two shared repairs: the pipeline self-check had failed on main since the
  gazetteer merge (its place-name mapping now carries the file waiver), and
  a stale translation record of kuryerpolski1754075-001 (the item moved to
  the newspapers section) removed by publish_translations.py.
- The edition guide's counts corrected (626 documents, 2,021 pages) and the
  PoznaÅ„ bullet extended, English and German.

## 2026-10-24 - Published

- The editor said "Publish". Main was pushed at 5830d718 after a local
  Jekyll build and `verify_site.py` passed (619 documents character-exact,
  46848 internal links resolve); the "Build and deploy" run succeeded.
- Went live with it: Kneifel (1937), the gazetteer import and the maps'
  first crops.
- The other items this section first named (Kraus, Werner, the Lidmanowski
  texts, SÅ‚owiÅ„ski, the ZagÃ³rÃ³w place page, the newspaper items, Åukasiewicz,
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
  applied ("Judicius" â†’ "Judicio"; "Citti~" read as Citati, the tilde kept).
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
  "Szetlewo z CzÄ™Å›: Jaroszew:" (APP 53/64/0/-/Kalisz Tab.21) moves to
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
  PoznaÅ„ clause extended and the Latin count corrected to a hundred and
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


## 2026-10-26 - Rostworowski (1918), the Dziennik of the Governing Commission (branch rostworowski1918)

- **The 37th work of the literature**: MichaÅ‚ Rostworowski (ed.),
  *MateryaÅ‚y do dziejÃ³w Komisyi RzÄ…dzÄ…cej z r. 1807*, T. 1, *Dziennik
  czynnoÅ›ci Komisyi RzÄ…dzÄ…cej* (KrakÃ³w 1918), the day-by-day journal of the
  Commission that carried the government of the Duchy of Warsaw from
  January 1807, printed from the manuscript a century later. From the SBC
  digitisation (publication 94492, edition 89178; the PDF in Downloads, not
  kept). Out of copyright (print 1918; the editor Rostworowski died 1940);
  shown whole as far as it is brought in.
- **The excerpt** (9 printed pages, the editor's word): the four passages
  that name or bear on Michalina z Prusimskich DÄ…bska, each brought whole -
  sitting 51 of 13 February 1807 (pp. 43-44, the memorial referred to the
  Director of Justice for general rules on the confiscations), sitting 58
  of 18 February (pp. 54-55, the opinion "a matter of a purely political
  character", the resolution to petition the Emperor, the order to the
  Administrative Chambers to watch the estates), sitting 210 at Dresden of
  21 July (pp. 303-304, the Emperor's Wybicki decree of 5 June extended to
  DÄ…mbska, General Niemojewski and Wichrowski), and the Directorium's
  protocol Nr. 3 of 15 July (pp. 321-323, which reports her among the very
  many leaving for Dresden). The editor ruled the whole sitting in each
  case, and for p. 322 - which has no session heading, the later part of
  the volume being the numbered dispatches of the Directorium in ÅubieÅ„ski's
  first person - the whole protocol that contains the passage.
- **The reading**: two witnesses held against each other (the PDF's own
  text layer against a lunaroute OCR pass over the kept pages at 300 dpi);
  the images could not be read directly in the session, so the settlements
  rest on the two witnesses and sense, and six doubtful spots went to the
  served spot sheet (`scratch/rostworowski1918_sheet.py`, port 4110, the
  crops from the PDF's own word positions). **The editor answered the same
  day**: "300/m" and "anzeatycznym" ruled against the transcript's first
  takes (the layer's "SOO/m" and "anzeatyeznym"), X-Å¼Ä™, "Riviera ZaÅ‚uski",
  "Å›ciÄ…gniÄ…nym" and "Kaiena" confirmed as transcribed, and the stray line
  of p. 321 - "Nominowani zostali do konsystorza Luterskiego w PÅ‚ocku.",
  between protocol Nr. 2's signature and the Nr. 3 heading - left open ("I
  have no idea"; NEEDS_CONFIRMATION). No footnote of the print is brought
  in - the three on the kept pages' feet belong by their markers to text
  not brought in.
- **The index**: 23 hits, all ruled. "MaÅ‚achowskiego" stands for the
  President with p. 44 excepted to "no" (there it is the late Director of
  the Treasury, Jan Nepomucen, whose accounts the Commission closed on
  12 February); "Niemojewskiego" and "Wichrowski" stand (the edition's
  precedent men of the decree); "Magnuski" refused (a writer of acts at
  KoÅ›cian, not the Prince's creditor of 1805). A literature-only pattern
  gives the print's modern genitives of Michalina's married surname
  ("Dambskiej", "DÄ…bskiej", the print's own bracket "Dambski[ej]"), which
  the edition's pattern - built on the documents' -kiey forms - misses.
- **Three hand-made links** tie the passages to the AGAD restitution file
  the edition holds (1/174/0/2/73 and 1/174/0/1/6): the February record
  against her letter of 20 July and the draft of 21 July; the decree of
  21 July against the register's resolution in wording near the print's
  ("z PrusiÅ„skich Dambskiey" against "z Prusimskich Dambskiej") and her
  letter of 23 July; the protocol's Dresden report against her three
  letters written at Dresden of 20-23 July.
- **The site built and verified**: 314 hand-made links checked on both
  sides, all documents character-exact. **Published 2026-10-26** at the
  editor's word ("merge into main and publish").

---

## The maps on the site (2026-10-27, branch `maps-site`)

- **Maps in the main navigation** (the editor's request of 2026-10-27): the
  Maps page (/maps/, German /de/karten/) after Places in the header; one
  card per map that is in the edition (`in_project: true` in
  `reference/maps.yml`), by date. A map the gazetteer cites and the edition
  does not hold gets no card (the editor chooses the maps one at a time).
- **The map's viewer page** (/maps/lukom1766/): OpenSeadragon over the
  IIIF tiles of triebenfeld-maps, the map turned by `view_rotation` (the
  lettering upright) with a north-up switch, the editor's eleven marks on
  the map and in a list with the crop of each lettering, the form as the map
  spells it, what the map shows there, the place's page linked, the
  inscription's two documents of the LÄ…d copy-book, the fit's error
  (Â±336 m) shown with it, and the Allmaps warp over OpenStreetMap linked.
  Deep links: /maps/lukom1766/#lukom1766-007 opens the map at the mark.
- **The links both ways** (the editor's request): every place page gains
  "On the maps" - the appearances in date order, for a map in the edition
  the crop and the link to the viewer at the mark, for a map not in the
  edition the form and the short form as a citation; the Places index
  carries "on Åukom 1766" after the kind for the places a map in the
  edition shows. The gazetteer's prose stays as written; the appearance
  marked `absent: true` (MyszakÃ³wek on Åukom 1766) is shown nowhere.
- **The machinery**: `pipeline/maps/map_pages.py` (a step of
  regenerate.py, after the place pages) writes site/_data/maps.yml,
  maps_list.yml, place_maps.yml and the pages site/_maps*/; the place
  pages' intro sentence mentions the maps; verify_site.py gains the maps'
  checks (both pages carry the tiles' address and every mark, every crop is
  in the site, every label a gazetteer entry names exists on its map).
  Åukom 1766 set `in_project: true` - the register's own rule, its page
  now built.
- **The map's page made two-column** (the editor's request of 2026-10-27:
  "make the map viewer much larger ... a narrow left column contains the
  details, and the right column is the map"): the citation and the places
  marked in the narrow left column, the map near the window's full height
  in the right column, where it stays while the list scrolls (on a narrow
  screen the map comes first and the columns stack). A mark now names its
  place on hover - a floating label with the form as the map spells it and
  the place's name where they differ - and clicking a mark takes the
  reader to its row in the list; a row's crop still takes the map to the
  mark, and the deep links still open the map at the mark. The marks are
  keyboard-reachable (role button, Enter or Space acts).

---

## The process explanations taken off the published pages (2026-10-27, the editor's request)

- **The rule**: a sentence on a published page earns its place if it tells
  the reader something about the past, is needed to use the interface at
  that spot, or is a caveat the reader must have. How a page was made or
  why it is arranged the way it is belongs to About the edition and to the
  holdings' "How it was prepared" tabs, not to the page itself.
- **The index pages trimmed** (site/_data/i18n.yml, English and German in
  parallel): the Places page loses "Alphabetical; a place's page is one
  click away" and its German twin, and its lede is one line ("Every place
  the edition records, each with its own page."); the Maps lede loses the
  georeferencing story and keeps "Click a map to read it."; Browse loses
  "Everything filters instantly."; People loses "Open a person's list to
  see those documents, by date or by archival holding."; Timeline loses
  "Click a year to read what it holds."; the Glossary's note now states
  only that each entry names the reference work its definition was checked
  against; Literature and Newspapers lose the "each is introduced with
  what kind of witness it is" clauses. The AI-translation caveats stand
  untouched - they are disclosures, not process.
- **The document pages** (site/_layouts/letter.html): the correspondents'
  "read from the salutation and signature" is gone from every document's
  meta; the Duplicate and Part of entries give the reference alone,
  without "transcribed twice" and "Several documents were bundled under
  one archival number." The per-document condition notes and the
  by-paragraph notices stay: they describe the document in hand.
- **The explanations moved, not lost** (site/reading-this-edition.md): the
  rule for listing a document under an estate is a new "Estates."
  paragraph beside "Places." under "Dates, names and money"; a sentence on
  the maps' georeferencing and photographed names joined "What this
  edition is".
- **The dead strings deleted** after a search showed nothing renders
  them: estates_lede, places_named_lede, places_lede and
  correspondents_note, both languages.
- **Verified and published**: the Jekyll build clean; verify_site.py
  passes - 630 documents character-exact, 67,464 internal links resolve.
  **Published 2026-10-27** at the editor's word ("publish").
- **The navigation cleaned up, the Sources page an overview, the cemeteries
  a subset of Places** (the editor's requests and rulings of 2026-10-27).
  The header carries nine entries now - Story, Browse, Timeline, People,
  Places, Maps, Glossary, Sources, About; Newspapers, Literature and
  Cemeteries left it, their pages remaining at their addresses. **Sources**
  (/sources/, /de/quellen/) is an overview of what the edition is built
  from, four visibly separate sections - Archival material (51 holdings),
  Newspapers (12 items), Literature (39 works), Maps (1) - each with its
  own one-line description and the link to browse it; the holdings' full
  list moved to /sources/archive/ (and /de/quellen/archiv/), the holding
  pages themselves unchanged at /sources/<slug>/. **The cemeteries** hang
  under Places: a section at the foot of the Places page (anchor
  #cemeteries, German #friedhoefe) lists the ten with their grave counts
  and places, and the pages themselves moved to /places/cemeteries/<slug>/
  (German /de/orte/friedhoefe/<slug>/) - the old /cemeteries/ and
  /de/friedhoefe/ addresses redirect page by page
  (`pipeline/cemeteries/cemetery_redirects.py` into
  `site/redirects-static/`; a redirect stub's permalink must keep its
  trailing slash, or Jekyll renders it a flat file the directory URL never
  serves). verify_site.py checks the new paths, the archive list, and the
  overview's four sections.
- **The Browse tab removed and the Eras page introduced** (the editor's
  requests of 2026-10-27). The header carries Story, Eras, Timeline,
  People, Places, Maps, Glossary, Sources, About; the browse page itself
  remains at /documents/ (and /de/dokumente/), reached from the eras page,
  the timeline's year links, the home page and the holding pages. **The
  eras page** (/eras/, German /de/epochen/) shows the six eras that have
  documents - TrÄ…bczyn in the Middle Ages, the TrÄ…bczyn and Åukom boundary
  dispute, the Hohenlohe-Ingelfingen years, the MiÄ…czyÅ„ska restitution,
  the colonists' land and forest rights, the twentieth century - each in
  the editor's own words from reference/eras.yml (the label, the span and
  count of its documents, who held the estate, its description), with a
  link to the era's documents on the browse page (the browse filter reads
  ?era= from the address). verify_site.py checks both pages carry every
  populated era and its link.

## 2026-10-28 - The standfirsts removed - the site stops narrating itself

- **The style ruled off** (the editor, 2026-10-28): text that describes
  what a page contains instead of presenting it - self-narration to the
  reader, restatement of what the heading and list already show,
  explanation of the obvious, and the decorated voice - removed outright.
  In `site/_data/i18n.yml`, both languages, deleted:
  `places_index_lede`, `places_t2_lede`, `gl_lede` and `gl_draft_note`,
  `maps_lede`, `people_lede`, `timeline_lede`, `eras_lede`,
  `sources_lede` and the four `sources_*_lede`, `lit_lede`, `np_lede`,
  `cem_lede`, `places_cem_lede`, and the home cards'
  `card_browse_p`, `card_timeline_p`, `card_people_p`, `card_about_p`
  (21 keys a side). The `<p class="standfirst">` and
  `<p class="src-lede">` elements deleted from the includes with them -
  places, cemeteries, glossary, people, maps, timeline, eras,
  sources-archive, literature, newspapers, sources, and the home cards
  (which keep their titles alone) - and the dead `.gl-note` and
  `.src-lede` CSS rules.
- **Kept where explanation carries what the page cannot show**: the
  Browse line (the full-text search runs over the German, not the
  English) and the Places tier-1 line, reworded so the site names no one
  - "Every place of the neighbourhood, whether or not it is named in the
  documents." German: "Jeder Ort der Gegend, ob in den Dokumenten genannt
  oder nicht." The 2026-10-27 rulings that kept the glossary's tap hint
  and the Glossary note and the Sources one-line descriptions are
  superseded; gone today with the family. The story prose (`home_lede`,
  `home_p1-p3`), the era notes, the view-mode hints, the AI-translation
  caveats and `cem_gid_note` stay - content or disclosure, not
  narration. Descriptions of the material itself (a holding's archive
  description, the Story standfirst, rights, About) are content and
  untouched.
- **The standing rule for site text** (recorded in
  `docs/STANDFIRSTS_PLAN.md`): the site speaks only to its reader about
  the materials; it does not mention the person who made them. Two
  violations found and left for the editor's ruling:
  `np_caveat_editor` ("The English translation is the editor's own." and
  its German twin), and the ten cemetery pages' notes, which open "From
  the editor's survey of the Evangelical cemeteries".
- **Built and verified**: `build_site_data.py`, the Jekyll build and
  `verify_site.py` all clean - 630 documents verified
  character-for-character, 63,056 internal links resolve, tier1 124,
  tier2 179; no deleted string renders anywhere in the built site, and
  the two kept lines render in both languages.

## 2026-10-28 - The voice's two rules recorded (docs only)

- The standfirst ruling and the no-maker ruling worked into
  `docs/HOUSE_STYLE.md`, the file that governs the site's prose: "No
  self-narrating standfirsts" - the four marks of the self-narrating
  text (self-reference; redundancy with the list beneath; explaining the
  obvious; the designed literary voice of dash-appended appositions and
  rhetorical triads), the struck-out examples quoted as NO, the kept
  examples as YES, and the exception, explanation that carries what the
  page cannot show (how the site is used, where its material comes
  from); and "The maker is not named" - the site speaks only to its
  reader about the materials and no page text names the person who made
  them, provenance telling what was done. Both sections cite the
  rulings of 2026-10-28 and `docs/STANDFIRSTS_PLAN.md`. Nothing on the
  site changed today.

## 2026-10-28 - The layout tidied; three literature-index rulings

- All code under `pipeline/` (`unitlib`, `numerals`, `new_unit`,
  `regenerate`, `verify_site` moved from the root; the pages workflow runs
  `python pipeline/verify_site.py`); the generated dataset renamed
  `corpus/` to `dataset/` (a holding's `units/<slug>/corpus.txt` keeps its
  name); finished working files in `docs/archive/`; stray files removed and
  the unreferenced `scratch/` files moved out of the project. The site's
  output unchanged (byte-identical build). WORKING_NOTES, "The layout".
- The editor's rulings on the literature index: GrÄ…dzeÅ„ is the modern name
  of GrÄ…dzyÅ„ (`gradzyn` "GrÄ…dzeÅ„" stands: ChodyÅ‚a 2015, Nazwy miejscowe
  Polski); the project's place is Kolonia Lisewo, not the village of
  Lisewo - the register's pattern for `lisewska-kolonia` no longer matches
  the bare "Lissewo" (Kneifel's and Breyer's filial Lissewo-Pyzdry is the
  village), and ChodyÅ‚a's "Kolonia Lisewo" stands; Breyer's "Rogaler
  (KÃ¶nigsberger) Gesangbuch" is the Rogall hymn-book, not the place Rogal.
- `dataset/` rebuilt: the register's widened GrÄ…dzyÅ„ pattern now marks
  "GrÄ…dzieÅ„" and "GrÄ…dzimia" in ADWÅ‚ 85 doc. 2, Konin Gr.145 and
  APP 53/968/0/-/669 doc. 1. Verified: the Jekyll build and
  `pipeline/verify_site.py` clean (630 documents character-exact, 63,056
  internal links).

## 2026-10-28 - Szczepan Turno; ChodyÅ‚a's facts proposed

- The gazetteer's WrÄ…bczynek and WrÄ…bczynkowskie Holendry name the
  starost of PietrzykÃ³w **Szczepan Turno**, not Turna (the editor: "Turno
  it is"). ChodyÅ‚a p. 49, which both cite, has only the genitive
  "Szczepana Turny"; p. 52 has the nominative. Recorded in GAZETTEER_PLAN,
  section 3, and WORKING_NOTES.
- `docs/CHODYLA_ADDITIONS.md`: ChodyÅ‚a's facts for the place pages,
  traced to the primary sources he cites (HOUSE_STYLE, "The documents
  first", point 7). Not on the site yet; waiting on the editor (TODO,
  section 56).

## 2026-10-29 - The materials' lists as cards with a first page

- The four lists under Sources (archival material, newspapers, literature,
  maps) show each item as a card in the look of the home page's cards: the
  item's first page as a thumbnail on the left (400 px wide, in
  `site/assets/thumbs/`, made by the new `pipeline/build/make_thumbs.py`:
  50 holdings, 7 press items, 5 works, the Åukom map), the whole card one
  link (the title stretched over it; the Janocki sub-item under Paciorkowski
  keeps its own). An item with no image yet (the printed Kodeks, five press
  items, 33 works) shows a blank-page placeholder in the thumb's place
  (`site/_includes/source-thumb.html`), so every card has the same layout.
  The cards run to 90rem wide, the thumb column 7rem.
- Each list has a sort bar (`site/assets/cardsort.js`, shared bar
  `site/_includes/sources-tools.html`): A-Z, the default on every list, and
  by date, the oldest first, undated last. A-Z reads as the literature list
  always did (brackets, accents and the stroke of Å ignored; numbers as
  numbers). The archival list also has a dropdown to filter by archive, with
  a "showing N of 51" count. The bar is hidden without the script (the list
  then keeps the order it was built in) and for a list of fewer than two
  cards (the maps, for now). Six `tools_*` strings, both languages.
- A holding's card on the archival list is titled with the holding's own
  title, no longer its reference: `card_title` in each `unit.yml` (and
  `card_title_de` where the German differs), made from `archive_title`, the
  editor's titles from the scans' folder names, 51 units. A court book has
  the court first ("Konin Municipal Court: Relationes [protocollon]
  1768-1774"; German "Burggericht Konin: ..."), 23 books: municipal court /
  Burggericht for the grod courts of Kalisz, Konin, PoznaÅ„ and Pyzdry, land
  court / Landgericht for the ziemski courts of Konin and Kalisz. The
  reference stands under the title, before the archive's name. Where
  `archive_title` carried a gloss of ours after the archive's own words (six
  Berlin and PoznaÅ„ files) the card takes the archive's words; the old
  "nothing displays it" comments updated. New units get `card_title: TODO`
  from `new_unit.py`; a TODO or an empty value falls back to the reference.
  Sorting A-Z on this list now sorts on these titles. The "Read ..." / "View the map"
  lines are gone, as are the "Read about this holding / Browse its documents"
  links on the archival list and the translation caveat that stood above the
  literature list (the caveat stays on a work's own page).
- The newspapers' and the literature's summaries on the lists are shortened
  to a brief of one or two sentences, newly written in both languages
  (`brief_en`/`brief_de` in each `item.yml` / `work.yml`, 12 + 39); the full
  account stays on the item's own page. A card falls back to the account if
  a brief is missing. The map's thumb is the whole-map level of its tiles
  (322 px, the only whole-map level the tile service serves).
- The generators write `thumb:` and the briefs into the site's data only
  where the file or text is here; `make_thumbs.py` runs in `regenerate.py`
  between the literature build and the literature pages. Six unused strings
  (`sources_read`, `sources_browse`, `np_read`, `lit_read`,
  `lit_read_summary`, `map_view`) replaced by four alt-text strings
  (`alt_holding`, `alt_clipping`, `alt_litpage`, `alt_map`), both languages.
  The shared card rules moved into `style.css` from the four includes.
- Verified: Jekyll build and `pipeline/verify_site.py` clean (630 documents
  character-exact, 62,874 internal links, no hidden-work text leaked by a
  brief). Not published.

## 2026-10-29 - Catalogue titles for eight Prussian files

- The editor's updated archive titles for eight Berlin units (GStA PK: III. HA
  MdA, III. Nr. 12765, 12366, 12367; I. HA GR, Rep. 7 C, Nr. 3709, 3705, 3570,
  1414; I. HA Rep. 162, Nr. 295) now head their cards on the Sources list.
  `card_title_de` is the archive's German, shortened with "[...]" where it runs
  long (the creditors of Nr. 12366 and 12367, the villages and further gifts of
  Nr. 3570, the present owner of Nr. 295); `card_title` is Claude's English
  translation, shown on the English site. The full catalogue title stands as a
  comment above `card_title` in each `unit.yml`; `archive_title` is unchanged.
- Verified: build_site_data, Jekyll build and `pipeline/verify_site.py` clean.
  Not committed, not published.

## 2026-10-29 - Translated titles and the original beneath them, on every holding

- The editor's titles for APP 53/71/0/-/57 (Erbet's hereditary lease) and AGAD
  1/185/0/1/169 (the jurisdictional dispute, Polish) entered; APÅ 39/98/0/-/6603's
  Russian title translated into English and German (the edition's "ÅaziÅ„sk" and
  "TrÄ…bczyn" for the Russian forms).
- Every holding now has an English and a German title (`card_title`,
  `card_title_de`); the 20 Polish, Latin, Russian and German-only ones were
  translated. Under it, in italics, the archive's own title: shortened with
  [...] on the card (`original_title_card`), whole on the holding's page
  (`original_title`), which now also shows the translated title in full
  (`full_title`, `full_title_de`). Not shown where the two are the same (a German
  title on the German site); the three Hohenlohe-archive units
  (Oe 1 BÃ¼ 9454, 14525, 14526) have no original title on record. Court
  books show their title without the court as the original ("Relationes
  [protocollon] ..."). `new_unit.py` template, `build_site_data.py` and the card
  and page templates carry the new keys.
- Open: the translation of "Magd." in the Erbet title is left as the archive's
  abbreviation; the Polish and Latin titles' English were not asked for before
  (the card used the original) and are Claude's.
- Verified: Jekyll build and `pipeline/verify_site.py` clean. Not committed, not
  published.

## 2026-10-29 - Hohenlohe titles; the archive's name

- Oe 1 BÃ¼ 9454, 14525 and 14526 now carry the archive's own German titles
  (editor) as `original_title` and as `card_title_de`; the English titles are
  Claude's translations of them (they replace the descriptive glosses).
- The archive is named **Hohenlohe-Zentralarchiv Neuenstein** (editor), not
  "Hohenloher Zentralarchiv": the four Oe units' `archive:`, the `new_unit.py`
  default, `reference/repositories.yml` (both languages), README, both
  "reading this edition" pages and the units' notes. Quotations (Seidel's
  text, old changelog entries) keep the form they were written in.
- Verified: build and `pipeline/verify_site.py` clean. Not committed, not
  published.

## 2026-10-29 - Types of archival material; Oe 1 U 199's title

- Each holding is classified as a whole by the form of its records
  (`types:` in `unit.yml`, one or two slugs, the dominant first), from the
  eight kinds in `reference/unit_types.yml` (English and German): court
  records, government and administrative files, correspondence, deeds,
  contracts and grants, registers, tables and surveys, church records,
  charters and privileges, researchers' papers. 50 holdings classified (the
  23 court books and the two Konin land-court units court records; 18 with
  two types, e.g. Nr. 3570 deeds + government file, APP 53/71/0/-/57 deed +
  court record, Nr. 12366/12367 and 1414 government file + correspondence).
  Shown as labels on the card and the holding's page, and as a Type filter
  beside the Archive filter on the archival list (`cardsort.js`). The Kodeks
  stays untyped: it is to move to the literature (editor), where there is
  no such type. `build_site_data.py` stops on an unknown type and skips a
  TODO; `new_unit.py` carries `types: [TODO]`.
- Oe 1 U 199 carries the archive's full German title (editor) with a shortened
  card form, and English translations of both.
- Verified: build and `pipeline/verify_site.py` clean. Not committed, not
  published.

## 2026-10-29 - The Kodeks listed with the literature

- The Kodeks Dyplomatyczny Wielkopolski is listed on the Literature page, not
  the archival list (editor: a printed edition, not an archive's records), with
  its structure unchanged: still the holding `kdw` with its 21 documents, its
  address /sources/kdw/, the document browse, the era and the links. `listed_in:
  literature` in `units/kdw/unit.yml`; the archival list, its archive filter and
  the overview's holding count (now 50) leave it out; the Literature list
  carries a card of the same shape (documents, span, the one-sentence title);
  the overview counts it with the works (40); the holding's page links back to
  the Literature list. `verify_site.py` checks the card is on the Literature
  list and not required on the archival one.
- Verified: build and `pipeline/verify_site.py` clean. Not committed, not
  published.

## 2026-10-29 - The map pages simplified

- A map's page (`site/_layouts/map.html`): the "Georeference Â±m" row is gone
  (the fit stays in the data; the overlay and the OpenStreetMap links depend on
  it, readers do not need its error figure); the archive's link is the map's
  reference number in the Holder row, no separate "The map at the archive" line;
  "The places marked on it" is an "Index" ("Register"), an A-Z list of place
  (linked to its page), kind, name as the map spells it (a click takes the map
  to the mark) and an OpenStreetMap link, with no crops of the lettering and no
  count line; the overlay link reads "View map overlay on OpenStreetMap"
  ("KartenÃ¼berlagerung auf OpenStreetMap ansehen").
- The viewer opens the map as drawn. The button (now the site's `vbtn`, so it
  reads in dark mode) says "North up" and turns the map by `view_rotation`,
  then "As drawn"; it is hidden for a map with no rotation. The "+ / âˆ’" hint,
  which did nothing, is removed.
- Verified: build and `pipeline/verify_site.py` clean. Not committed, not
  published.

## 2026-10-29 - The map index as a numbered list

- The index of a map's places is an ordered list with no rules between the
  rows. Each place: its name (the one prominent link, to the place's page), a
  muted line under it (kind, the name as the map spells it, any note), then
  two small chip buttons, "Show on map" (takes the viewer to the mark) and
  "OpenStreetMap"; a document the place is tied to stands as a muted line
  with an arrow. New string `map_locate`, both languages. Not committed, not
  published.
- The map index tightened (same day): one line per place, "Place, kind, name on
  the map" in one size (the name in bold and linked, the map's form in italics,
  no quotes or dots; the editor's note on a mark kept as a tooltip), with short
  chips at the line's end: "Locate", "OSM" and, where a document is tied to the
  place, "Document" (the quote as its tooltip). Strings `map_locate`,
  `map_document`, `map_today` shortened in both languages.
- The inscription "Tres mansi ConventÃ»s Landensis" of Åukom 1766 is its own mark,
  not GrÄ…dzeÅ„ (editor, 2026-10-29): `maps/lukom1766/labels.yml` has `place: null`
  and `new_place` with its own name; the index shows it by that name, unlinked,
  kind "field". Its two references (the king's confirmation of 1447 and the
  privilege of 1461, the LÄ…d copy-book) are kept, now on the label (`refs:`,
  which `map_pages.py` reads when no gazetteer item carries them) and shown as its
  "Document" chips; the item is out of the gazetteer's GrÄ…dzeÅ„ entry, so
  GrÄ…dzeÅ„'s page no longer lists the inscription among its appearances.
- A mark's references stand as a short line under its entry again, introduced by
  "Documents on this inscription:" ("Dokumente zu dieser Inschrift:"), not as
  buttons (the "Tres mansi" inscription: the king's confirmation of 1447 of the
  purchase of three mansi of Åukom; the privilege of 1461). The overlay link
  moved from the side column to the lower right under the map, level with the
  "North up" button. Not committed, not published.
- The marks on the map are centred by OpenSeadragon (`Placement.CENTER`, not
  turned with the map, border-box sizing) instead of a negative margin, which
  drifted off the point at some zoom levels as drawn. The references' lead-in
  now reads "Related:" ("Verwandt:"). Not committed, not published.
- "Locate" centres the mark whatever the view: the viewer zooms without a
  reference point and then pans (zooming about the point left the pan to be
  overridden by the zoom's anchor once the map had been zoomed or dragged). Not
  committed, not published.

## 2026-10-29 - The document page: the particulars in the header

- A document's page (`site/_layouts/letter.html`): the "About this document"
  block no longer stands after the text, to the right of the page views; its
  items (date and how it was dated, holding, extent, people, estates, places,
  the literature, relations to other documents, condition) are in the header
  under the summary, in columns, the long lists across the whole width. The
  correspondents and place rows, which the header already shows, are not said
  twice. The page is one column. The summary runs to 64rem, no longer 62ch.
- The translation tab no longer says "The English translation, page by page."
  (the string removed); only "Not yet translated" remains.
- The date badges read "[date inferred]" and "[date supplied]" ("[Datum
  erschlossen]", "[Datum ergÃ¤nzt]"); the second changed to match the first.
- Verified: build and `pipeline/verify_site.py` clean. Not committed, not
  published.

## 2026-10-29 - The document page, lighter before the content

Worked from the editor's reading of /documents/app5314550221/3/: too much before
the text. The page now runs: a navigation line (the holding's reference, the
archival and the chronological browsers, the archive's name no longer repeated);
"Document 3 Â· Confirmation"; the date with its badge; one line of facts (the
place of writing only where known - no more "Unknown" -, the printed edition's
citation, the number of manuscript pages where there are page images); the
relations; the summary clamped to four lines with a "Read more" button
(`letter.js`; the two summaries differ in length, so the check reruns on a
language change); the people and places named as small tags (the estates in focus
and the other places merged, each once, the first twelve shown, the rest behind
"+N"; people with a dashed outline); then a folded "About this document" (the
holding and archive, how the date was reached where it is not the document's own,
the literature that cites it, a duplicate or parent). Left off the page, kept in
the data: the archival number (it is the document's number), the extent and
condition lines ("5 uncertain readings" and the like), the "date source" line
where the date is the document's own.
- The glossary switch is removed; the marks are always on (`glossary.js`
  ignores the old stored choice).
- A page's "lines a-b" only where the text is matched line by line to the
  manuscript (not for paragraph transcriptions, not for tables, which keep
  their entry range); the note "Transcribed by paragraph..." is said once, above
  the first page, not on every page; a scan's caption is "Open full size", not
  its file name. Strings `summary_more`, `summary_less`, `open_full`, both
  languages.
- Verified: build and `pipeline/verify_site.py` clean. Not committed, not
  published.
- The navigation line slimmed (same day): "â€¹ 53/1455/0/2/21" (the holding) on the
  left, the arrows to the neighbouring documents on the right, with no "Holding"
  and "Archival order" labels; a second pair, "By date" ("Nach Datum"), only
  where the date order differs from the holding's. The page count left the line
  of facts; it is under "About this document" ("Extent"), for documents with
  page images. Not committed, not published.
- The first pair of arrows is labelled "Archival order" again, and a thin
  vertical rule stands between it and the "By date" pair. Not committed, not
  published.

## 2026-10-29 - Helper text off the pages; the texts one width

- Removed (both languages): the hints under a document's tabs ("One line per
  manuscript line, with broken words hyphenated and stray break marks removed.
  Editorial decisions are set out in About the edition.", "The same text with lines
  flowed together into continuous prose."), the note on every page of a paragraph
  transcription ("Transcribed by paragraph, not line by line..." and its printed
  edition twin), the "From the electronic text of a printed edition: there is no
  page image." and "No scan matched to this page." notices, the "as printed" hints
  of the literature, newspaper and place pages, and the newspapers list's caveat.
  Shortened: "Not yet translated." (the tab's note), the translation hints
  ("English translation by Claude."), the translation caveat of the literature and
  newspaper pages, the copyright note ("Under copyright: a summary of the contents
  stands in place of the text."), the cemeteries' identifier note. Rule recorded
  in HOUSE_STYLE.
- A paragraph transcription (`by_paragraph`) is set without line numbers
  (`<ol class="dip" data-para="1">`); a page with no image has no image pane and
  the text takes the width (`.pane-pair.no-scan`); a document with no scans at all
  has no "Hide scans" box.
- The transcription, the reading and the English stand in one width (the
  measure; the transcription's line numbers outside it).
- Verified: build_site_data, Jekyll build and `pipeline/verify_site.py` clean.
  Not committed, not published.

## 2026-10-29 - The site no longer calls itself "the edition"

Scan of the built site: about 1,000 mentions on 294 pages beside the nav and
footer on every page. Changed, in both languages:
- The About page is "About" ("Ãœber") in the nav, the footer and the home card;
  its address is /about/ and /de/ueber/ (the old addresses redirect); its
  headings and sentences no longer say "the edition" (The documents; Citing and
  reusing). The footer reads "630 documents from the TrÄ…bczyn estate, transcribed
  from the originals in archives at ...". The overview's count label is "Size";
  the list label "In the edition" is "In the documents" ("In den Dokumenten").
  The rights page says "the site".
- The prose, 440 sentences from 170 source files (holdings' about/process
  texts, the hand-made links' sentences, the literature and newspaper accounts,
  the people and genealogy notes, the glossary, the timeline, the Hohenlohe page,
  three summaries): the sentences that said only what the site holds or follows
  ("The edition follows the documents", "Where it differs from the edition's
  documents, the notes say so", "The edition has 870 pages" -> "It has 870
  pages") are cut or turned to "it"; "the edition's X" is "the X"; "not in the
  edition" is "not included"; facts kept ("The edition has the decree of ...:
  appointed by ..." -> "The decree of ...: appointed by ..."). Two raw
  repository slugs shown to readers (`boniecki1900`) became "Boniecki (1900)".
  The place pages' footnote link is "The document."; a person source "editor"
  shows as "the editor". The pipeline scripts carry the same changes
  (place_pages.py, person_pages.py), and the dataset's date-basis strings were
  changed in place (the same rules).
- Kept: "edition" meaning a real edition (the printed Kodeks, a source edition, "the
  second edition of 1776", URLs of the digital libraries).
- Rule written into HOUSE_STYLE. Verified: build, `pipeline/verify_site.py`,
  `check_unit_text.py` and the literature index check clean. Not committed, not
  published.
- Not changed, to ask the editor: displayed notes that mention the repository
  itself (NEEDS_CONFIRMATION, `reference/places.yml`, "the editor's ruling") on
  some holding and literature pages, which read as method talk; the
  `cache/summaries-raw*` copies of three summaries (on the editor's machine).

## 2026-10-30 - "How it was prepared" without the repository

- At the editor's word, the method tabs of five holdings rewritten in both
  languages: 53/4/0/-/62, Pyzdry Gr.115, PoznaÅ„ Gr.1181, -/782, and one
  dated ruling in -/716. Out: file names and paths, script names and flags,
  page ids, NEEDS_CONFIRMATION, the spot sheet's address, dated citations of
  rulings, the cost sentences and a tooling story (a check that crashed).
  Kept: what was done, who decided, what is still open. The model is named
  Claude where "the session" stood. Gr.1181 lost its own heading (no other
  tab has one); 53/4/0/-/62's last section is now "Index".
- Two slips in the tabs put right: Pyzdry Gr.115 said "nine corpus lines"
  for a table of a heading row and seven rows (eight lines, as the
  transcription has them); 53/4/0/-/62's list items began with "â€“ " and ran
  together on the page.
- `check_unit_text.py` fails a line begun with an en or em dash and a space.
  HOUSE_STYLE records the ruling. The scan's `method-repo` flags: 55 to 0.
  Verified: build, `pipeline/verify_site.py`, `check_unit_text.py`. Not
  published.

## 2026-10-30: the holding pages tightened (branch `unit-pages-tightening`, not published)

- The holding page's heading is now the translated title of the archival
  unit; the original title stands under it and the reference number beside the
  archive's name. The browser tab names the holding by its title. The
  languages of the documents are one line of the facts (new `languages:` in
  all 51 unit.yml, `reference/languages.yml`).
- "Form and language" removed from 48 holdings, English and German. What
  changes how a document is read (the basis of a date, a part not
  transcribed, original and copy, a kept spelling) moved to the end of
  "Contents"; the old text is in each `notes.md`. The words of the fixes made
  in the process: "Paraphs" heading in -/12765's `about` replaced; "paraph"
  reads "initials" in English where a reader meets it (-/12765, the
  summaries of AGAD 1/174/0/2/73, I. HA GR 7 C 3709's tab).
- "How it was prepared" rewritten for all 51 holdings: only the AI decisions
  that affected the text, written from `prepared:` in unit.yml and
  `reference/prepared.yml` (no more `process.md` / `process_de.md`, whose text
  moved to the notes). The tabs average about a seventh of their old length.
- Verified: `build_site_data.py`, Jekyll build, `verify_site.py` (all checks
  passed), `check_unit_text.py` (0 failures).

## 2026-10-30: the newspaper pages laid out like documents (branch `newspapers-layout`, not published)

- Each of the 12 items has a real title (`title` as printed, `title_en`,
  `title_de`) and an issue line (`issue_en`, `issue_de`); the old long title is
  `long_title`. The page: nav line, newspaper over the title, one line of
  facts, the brief as the summary, the clipping (22 rem, sticky) beside the
  text, English or original by the buttons; no account, no "Published" line, no
  folded details; the translation's caveat shows with the English text. The
  list page's cards match the Sources cards. Verified: build, `verify_site.py`.

## 2026-10-30: KozÅ‚owski 1861, the second map (not published)

- **Brought in at the editor's word** by `docs/ADDING_A_MAP.md`: the plan of
  the TrÄ…bczyn estate drawn in 1861 by Seweryn KozÅ‚owski, APP
  1/402/0/-/536-23, north-up, scale 1:20 000. The original is the archive's
  JPG (15,757 x 12,140), the image the editor georeferenced on MapWarper
  (70818). Tiles in triebenfeld-maps/kozlowski1861 (1,003 files, 43 MB); four
  control points, fit RMS 5.8 m.
- **31 labels** imported from `labels_kozlowski1861_20261030-1620.json`: 25
  linked to gazetteer places (12 new map appearances added), six forest
  districts (okrÄ™g) marked as new places, to be ruled (NEEDS_CONFIRMATION).
  Two entries' coordinates (Czerwonka, Nowa WieÅ›) are 16 and 18 km from their
  marks. `in_project: true`; card, thumbnail and page in both languages;
  Jekyll build and `verify_site.py` pass.
- **Scales**: maps now carry a `scale` (register, map page, "Scale" /
  "MaÃŸstab"), put in as it is known (the editor's word); ADDING_A_MAP says so.
- Tiles' first Pages deployment failed (GitHub 500) and was rebuilt by an
  empty commit; a stale local server held port 8765.
- **Rulings of the editor, same day**: the six okrÄ™g labels are parts of
  their obrÄ™b (appearances of WÅ‚odzimirÃ³w ObrÄ™b and Wielki-BÃ³r ObrÄ™b, not
  new places; one note's "OkrÄ™g" was a slip for ObrÄ™b); the placing on the
  map is accurate, so Czerwonka (the mark's position, precision `from_map`)
  and Nowa WieÅ› (the village's position in `places_osm.yml`) lose their wrong
  coordinates. The labels were imported again from a corrected copy of the
  saved file. Place pages, map pages, build and `verify_site.py` pass.
- **The legend**, at the editor's request: the sheet's *WyjaÅ›nienie KolorÃ³w*
  (lower right) recreated digitally on the map page, a table of the
  fifteen blocks with their grouping headers (Grunta orne, Ogrody, Lasy,
  ÅÄ…ki, Pastwiska, and water), Polish and English (German has its own
  column values). Claude read the Polish from the scan; the values are to
  be checked by the editor. The colours are sampled from the scan (fill,
  the stronger edge strip, the pencil line), and the three patterned
  blocks are drawn with CSS: dots (orchard), blue dashes (wet meadows and
  pastures), the graded pale inset (water). Data `maps/kozlowski1861/
  legend.yml`, built into the page's data by `map_pages.py`, rendered in
  `_layouts/map.html` under the mark index; new i18n keys. A map needs
  nothing: the section shows only where `legend.yml` exists (Åukom 1766
  has none on its sheet). The editor's looks on the day set the blocks to
  the sheet: ten irregular dashes for the wet blocks; then, on the
  editor's word, the orchard as plain dots (no berries, no stems), every
  block the same thin outline â€” water's frame alone built up (the thick
  blue band top and left, a thinner darker line on the other two) â€” the
  squares a little larger, and the caption under the table taken off (no
  explainer text). The editor's colour codes followed (same day): nine of
  the fills given outright â€” Manorial ddcab0, Church c9c4ac, Peasant
  dacea2, Colonists' dcc9a0, Coniferous b6ad98, Deciduous a7aa9b, Copses
  c3b9a0, dry Meadows c9c9b1, Roads and plots under buildings cebb93 â€”
  set as given, the table's other colours still the scan's samples; the
  wet blocks' blue dashes laid further apart so none touch. Verified:
  build, `verify_site.py`; rendered in the headless browser.
- **Published at the editor's word the same day** ("Push and publish"):
  main pushed (2e1213b28..9d73c2131, ten commits, back to the map's
  register entry) and the "Build and deploy" run 41101782292 succeeded on
  it â€” KozÅ‚owski's map, its legend, the corrected places and all of
  today's other rulings went live.

## 2026-10-31: PeÅ‚zucki 1896, the third map, and the labelling page's two conveniences (branch `pelzucki1896`, not published)

- **Named by the editor** ("I want to add a new map to the project"):
  the Szreniawa museum's unit AN-4456, file `4456_full.jpg` â€” the plan of
  the lands that passed into the ownership of the peasants of ÅaziÅ„skie
  Holendry, gmina Tromczyn (TrÄ…bczyn), SÅ‚upca uezd, Kalisz Governorate:
  the map the gazetteer cites as **PeÅ‚zucki 1896** (`glinianki.yml`). The
  unit holds the five sheets of the plan and the editor's mosaic of them;
  asked which image is the map of record, the editor named **the mosaic**
  (`4456_full.jpg`, 21,715 Ã— 14,206) â€” against ADDING_A_MAP's rule that
  the original is the file whose size equals MapWarper's, which the
  procedure now records as the editor's to overrule.
- **Identified from the sheet itself.** The editor's transcriptions in the
  unit (legend, certification texts, explication) give the title
  (ÐŸÐ›ÐÐÐª Ð·ÐµÐ¼ÐµÐ»ÑŒ Ð¿Ð¾ÑÑ‚ÑƒÐ¿Ð¸Ð²ÑˆÐ¸Ñ…ÑŠ Ð²ÑŠ ÑÐ¾Ð±ÑÑ‚Ð²ÐµÐ½Ð½Ð¾ÑÑ‚ÑŒ ÐºÑ€ÐµÑÑ‚ÑŒÑÐ½ÑŠ ÑÐµÐ»ÐµÐ½Ñ–Ñ
  Ð›ÐÐ—Ð˜ÐÐ¡ÐšÐ†Ð• Ð“ÐžÐ›Ð•ÐÐ”Ð Ð«...), the surveyor (Ð“. Ð. ÐŸÐµÐ»Ð·ÑƒÑ†ÐºÑ–Ð¹, 1896, staff land
  surveyor of the 2nd class â€” the surname's reading uncertain,
  NEEDS_CONFIRMATION), the scale (**1:4200 in Russian measure**), the
  certified copy's dates (copy certified at Kalisz 27 March 1898, issued
  with the seal 19 July 1900) and the five sheets (Â«Ð½Ð° Ð¿ÑÑ‚Ð¸ Ð»Ð¸ÑÑ‚Ð°Ñ…ÑŠÂ»).
  The register's entry is filled from them; the English title is the
  folder's own translation, the German Claude's.
- **The MapWarper points were made on sheet 4456-4.jpg** (map 104898,
  "ÅaziÅ„skie Holendry ca. 1896", 7454 Ã— 7392), not on the mosaic: the
  register now carries `mapwarper_image` and `mapwarper_fit:
  [scale, tx, ty]` and `pipeline/maps/mapwarper.py` transforms every
  fetched point into the mosaic's pixels. The fit is found by patch
  correlation in `scratch/map4456/` (not committed); the matcher's three
  wrong takes before it worked are recorded as a lesson (WORKING_NOTES,
  "Correlation matchers: prove them on a self-match first").
- **The labelling page's two conveniences** (the editor's word: "instead
  of filling everything in manually, I want to be able to choose the
  label name, and then you fill in the type of place"; "add the place
  name add section to the top of the column"):
  - choosing a gazetteer place fills the label's type (`shows`) from the
    place's `kind` (a village for a village, water for a stream â€”
    KIND2SHOWS in `label_page.py`); the last step keeps only the form:
    the type shown as filled in, the form field focused, **Enter saves**
    (a type key overrides). The editor's correction the same day: the
    first take saved the label the instant the trace ended, which took
    the moment for typing the form as written on the map away â€” "I need
    to be able to still add 'Form as written on the map'". The type
    choice is what is saved, not the pause;
  - "+ New label" and its form moved to the top of the panel, above the
    To find list. The saved format and the import are unchanged.
- **The texts on the sheet** (the editor's word: "make sure the
  information can be viewed in English, Russian, and German"): the title
  block, the certification texts, the description of adjoining lands
  (ÐžÐ¿Ð¸ÑÐ°Ð½Ñ–Ðµ ÑÐ¼ÐµÐ¶Ð½Ñ‹Ñ…ÑŠ Ð·ÐµÐ¼ÐµÐ»ÑŒ â€” the boundary walk in 20 stretches keyed by
  stamped letters Ðâ€“Ð£, two sections, the uezd groups; added the same day
  at the editor's word from `legend_2_transcription.md` /
  `legend_2_translation_en.md` â€” the letter markers of rows 16â€“18 corrected
  to the editor's revised transcription the same afternoon (ÐŸâ€“Ð, Ð â€“Ð , Ð¡â€“Ð¡;
  the first take's "Ð  [?]" mis-stamp guess withdrawn) â€” and the
  explication (the land-area
  table, basic allotment 870 des. 1454 sq. sazh., additional 197 des.
  2218 sq. sazh., total 1068 des. 1272 sq. sazh.; the arithmetic checked)
  are carried in `maps/pelzucki1896/texts.yml` and shown on the map's
  page â€” the Russian transcription as transcribed, the page's translation
  beside it line by line, the two tables as tables with the original's
  column heads where it has them; the notes explain desyatinas, square
  sazhens and the stamped boundary letters. New i18n keys;
  `map_pages.py` carries `texts` and `title_de`; the German
  standfirst uses the German title where the register has one. A map
  needs nothing: the section shows only where `texts.yml` exists.
- **Tiles cut and published** into triebenfeld-maps/pelzucki1896 (1,624
  files, 60 MB); the register's short entry merged into the full one (the
  duplicate-key trap struck once: the scripts read the shadowing short
  entry and the tiles step stopped until merged). The control points
  fetched from MapWarper 104898 and transformed by the fit; the fit of the
  four transformed points **RMS 2.71 m** (residuals 1.0â€“3.7 m), the
  annotation live, warp.html?map=pelzucki1896 up. The labelling page
  served at http://localhost:8778/pelzucki1896/ (a stale server of an
  earlier session holds 8765); the editor's marks are the next step.
- **The editor's seven marks imported** the same evening
  (`labels_pelzucki1896_20261031-2053.json`): Glinianki, Dziadolina,
  Studzianka, TrÄ…bczyÅ„skie Nowe OlÄ™dry (as **ÐÐ¾Ð²Ñ‹Ðµ Ð“Ð¾Ð»ÐµÐ½Ð´Ñ€Ñ‹**), Noga,
  Grabina â€” and one **new place, Wypalanki** (Ð’Ñ‹Ð¿Ð°Ð»Ñ£Ð½ÐºÐ¸, the felled forest
  of boundary-list row 14; entry to be drafted at the editor's word). New
  map appearances added for Dziadolina, Studzianka, Noga and Grabina;
  positions written (RMS 2.71 m â€” for the marks on the mosaic's northern
  sheets an extrapolation from sheet 4's points: tens of metres, not 2.7).
  **Glinianki**: the mark lands at 52.117 N, 17.905 E, some 13 km from the
  entry's coordinates (52.144, 17.768) â€” the entry's coordinates belong to
  another Glinianki or are wrong (NEEDS_CONFIRMATION; the entry's `maps:`
  item's form, empty until now, set to Glinianki as typed). A correction
  of the session's own note: the "ground extent" first reasoned from was
  sheet 4's warped bbox only; the mosaic reaches further.
- **The boundary walk on the labelling page** (the editor's idea: "I can
  mark the places where the letters occur, and also draw the polylines
  between the letters. But give me the option to skip pairs; it looks
  like T-Y occur in a different location (they're drawn in a sub-map)"):
  where the map's texts carry the adjoining-lands list, the page grows a
  **Boundary walk** section â€” **Mark the letters** steps the stamped
  capitals Ðâ€“Ð£ in list order (edit the letter in the box for a stamp the
  sequence doesn't name; <kbd>S</kbd> leaves one unmarked), **Walk the
  boundary** steps the twenty stretches of the list, each traced from its
  first letter to its last, or skipped (<kbd>S</kbd> or the button) â€” a
  skipped stretch is recorded as skipped, with its description, which is
  the shape of the sub-map's Ð¢â€“Ð£. The import takes the new kinds: a letter
  (a point, cropped like a name), a stretch (a trace, no crop â€” a line is
  not lettering â€” and no gazetteer linking); `labels.yml` carries
  `role: letter` / `role: boundary` with the letter or the from/to/n and
  `skipped:`. On the map page the letters show as a chip row and the
  stretches as a list under "The boundary walk" (German Der Grenzverlauf;
  skipped marked "drawn in the sub-map"), the viewer draws the stretches
  as dashed lines over the map with the from-letter's square at the start,
  and clicking a row or chip takes the map there (a stretch's Locate fits
  the whole line). The point of the walk: the 1896 perimeter of the
  peasants' allotment as a drawable thing for the interactive map, and the
  check of the list's rows 16â€“18 against the stamps.
- **The key (ÐžÐ±ÑŠÑÑÐ½ÐµÐ½Ñ–Ðµ Ð·Ð½Ð°ÐºÐ¾Ð²ÑŠ) on the map page** (the editor's word:
  "Make a legend on the map page similar to the KozÅ‚owski 1861 map"): the
  ten blocks with the editor's own colour codes â€” Buildings 946837,
  Gardens 747969, Arable land c59e74, Meadows ac9e85, Pastures ae9e81,
  Forest brush ab9175, Forest 816c57, Cleared woodland aa9e83 (the light
  blue streaks drawn, the wet pattern with a lighter ink), Unusable land
  c0976d, Water b0978a â€” the labels from the editor's transcription
  (`map_colours_transcription.md`; rows 5 and 6b keep their [?]), the
  English the folder's translation, the German Claude's. The key's
  original text is **Russian**, so the legend data now carries `lang:` and
  `orig:` (the layout falls back to KozÅ‚owski's `pl` fields); the gap row
  between legend groups is emitted only after a group (a flat legend gets
  no stray rules). The buildings block carries the key's own sign (a small
  dark footprint, new CSS pattern). The outline colours are the fills
  darkened (0.85/0.62), the streak ink chosen light blue (#a9c3d2) â€”
  Claude's, to be checked by the editor like the rest of the legend.

## 2026-10-31: "always tag a Zelmer/Celmer/Zellmer" recorded as standing (branch `mentions-robustness`, not published)

- The editor's rule went into the ledger (`EDITORIAL_RULES.md`, "Rulings the
  editor has given, standing until withdrawn") and into the identity of the
  family's entry in `reference/people.yml`. The machinery had honoured it
  since the rulings of 2026-09-11 and 2026-10-15: the entry's `match` covers
  Celmer, Cellmer, Zelmer, Zellmer and the Russian tables' Ð¦ÐµÐ»ÑŒÐ¼ÐµÑ€ÑŠ, with
  inflections, and a curated entry outranks the seed tail everywhere. The
  coverage test found nothing untagged: 28 mention rows over seven documents
  - the liquidation tables of APÅ 39/98/0/-/6603 and Breyer's copy of them,
  document 4 of the 53/968/0/-/716 holding; the delivery protocol of the
  Kalisz Gr.414 holding of 1771; the printed summons of the 53/968/0/-/783
  holding of 1860; Breyer's first notebook, the 53/968/0/-/669 holding.
- Found proving the rule: the five older units whose originals name the
  family (`app53150kaliszgr414`, `app539680783`, `app539680669`,
  `apl399806603`, `app539680716`) produced no `names` marks in their
  translations, so their English pages print the Zelmers with no
  `mentions_english` link. A translation pass would add them; it costs
  money, and waits for the editor's word (TODO 58).
- **Published at the editor's word** ("Push and merge into main"): main
  fast-forwarded and pushed (703b04f50..587412691, both of today's
  commits) and the "Build and deploy" run 41187101304 succeeded on it
  (build 2m23s with verify_site inside, deploy 29s). The home page, the
  People page and the family's card answer on the live site, Cyrillic
  name and all.

## 2026-10-31: MuszyÅ„ska-ZygmaÅ„ska (1947) added to the literature (repository, summary only)

- The Polish transcription and the corrected AI English of *Wielkopolska w
  powstaniu koÅ›ciuszkowskim* (PoznaÅ„ 1947) are in `literature/muszynska1947/`,
  cut into **150 passages**: the front, the five chapters (pp. 7-154) and the
  notes. The bibliography, index and errata are apparatus and are not cut into
  passages (the work's `notes.md`).
- The English was audited whole before it came in: all **411 body paragraphs**
  and **521 notes** read against the Polish, **87 findings** (3 S1, 23 S2,
  61 S3; 68 fixed, 15 source notes, 3 author queries, 1 rejected). This is
  stronger than the literature's usual spot check.
- Kept **`visible: false`**: the book is of 1947 and its rights are not
  established here. The site shows only the detailed summary (`summary_en`,
  `summary_de`); the passages stay in `dataset/literature/` for questions.
  **The editor's word is needed to publish it**; making it visible would also
  require ruling the literature index's hits on its Polish text.
- `pipeline/literature/build_literature.py --quiet` gives 150 passages with
  no page missing from either language; `literature_site.py` writes the
  summary page; `jekyll build` and `verify_site.py` pass (630 documents,
  61,223 internal links). `docs/LITERATURE_PLAN.md` section 30 and
  `docs/NEEDS_CONFIRMATION.md` record it.

## 2026-11-01: MuszyÅ„ska-ZygmaÅ„ska (1947) published in full

- The editor's word: publish it. `visible: true`; the site now carries the
  whole work, English first with a button for the Polish, at
  /literature/muszynska1947/ and /de/literatur/muszynska1947/.
- The literature index was run over its Polish text: **269 hits** found,
  **243 stand**; **26 new pairs (68 hits)** read and ruled in
  `literature/index.yml`; **0 unruled**, `--check` passes. False friends ruled
  out: the Silesian minister Danckelmann, the Prussian general Lichnowski,
  Jacek MaÅ‚achowski, Colonel Pirch of 1794, Kamionna on the Bzura, the
  Silesian OleÅ›nica, the town Åšwiecie, and the surnames Kaliszowski, Åukomski
  and RogaliÅ„ski; Warschauer the historian and the lieutenant Voss.
- `literature_site.py` writes the full pages; `jekyll build` and
  `verify_site.py` pass with the text on the site. The work's `notes.md` and
  `docs/LITERATURE_PLAN.md` Â§30 record the change; the open question in
  `docs/NEEDS_CONFIRMATION.md` is settled.


## 2026-11-01: Dorow (1843), Triebenfeld's memoir, brought in (not published)

- The source found: the editor's PDF of Wilhelm Dorow, *Erlebtes aus den
  Jahren 1813-1820*, part II (Leipzig 1843) - the SBB digitisation (PPN
  167107372X, Bibl. Varnhagen 936, Public Domain Mark), image-only, 245 MB -
  had been downloaded 2026-10-19 with the first literature set and left
  unprocessed; nothing of it had ever entered the repository, the plan or
  the index. It prints, at printed pp. 13-24, the memoir "Pohlen unter
  Friedrich II. und Friedrich Wilhelm II." which the war councillor Peter
  August von Triebenfeld submitted to Dorow in 1813 - the longest thing
  Triebenfeld is known to have written, and in his own words; the
  Materialien (1861, pp. 205-216) reprints it only in extract, and
  Åukasiewicz (1997) retells it. The editor ruled the memoir only, not the
  whole part II.
- The excerpt: the memoir's title leaf and its Goethe motto leaf
  (unnumbered, the volume's pp. 11-12) as the work's front, then printed
  pp. 13-24, ending with Hardenberg's verdict of November 1816; 13 passages
  in both languages. `literature/dorow1843/`, the slug `dorow1843`, kind
  collection, visible (1843, public domain); the scan's pages are not kept
  in the repository.
- Read by OCR: Tesseract 5.5.3 with the `script/Fraktur` model from
  tessdata_best fetched into `%LOCALAPPDATA%\Tesseract\tessdata` (the deu
  model there does not read Fraktur; the install's own tessdata carries
  English only); whole pages at 300 dpi, doubtful lines as 900 dpi bands in
  the Fraktur and deu models. The lunaroute converter (the second engine of
  the Kraus 2001 sitting) could not be reached this session; in its place
  the Materialien's reprint of the same memoir was read line against line
  with `difflib` - its added motto (VollgrÃ¤ff), added pointers, small
  omissions ("auf 6 Jahr"), own slips ("zu werden") and silent
  normalisations are recorded in the work's `notes.md`, and the 1843 print
  stands where they differ.
- Nine readings the passes and the reprint did not settle went to the
  editor's spot sheet (`scratch/dorow1843_sheet.py`, answers to
  `review/dorow1843/query_answers.json`): the 9/5 Procent digit of p. 14
  (the Materialien prints 5 with its own "(?â€”)" pointer), gebauset/gehauset,
  Offizcianten against the print's own whole-word Offizianten of p. 17,
  WÃ¼rkungskreis and bewÃ¼rken against the reprint's Wirkungs- forms, kukken,
  Michelis/Michaelis, and the title leaf's display word and cross-reference.
- The sheet answered the same day (eight of nine rows), the rulings worked
  into `original.md` and the English: **5 Procent** (the Fraktur model's 9
  was its error), **gehauset**, **Officianten**, **WÃ¼rkungskreis**,
  **bewÃ¼rken**, **kukken**, **Michelis** and **Pohlen** stand; the
  cross-reference row was not answered and stays open in NEEDS_CONFIRMATION
  ("The literature"). The work's `notes.md` records the answers and the two
  spellings of Offizianten/Officianten the print itself carries (p. 17 as
  read, p. 15 as ruled).
- The figures: the memoir's own figures are Triebenfeld's (the 10 and the
  volunteered 24 per cent; Prince Karl George of Hessen's circa 230,000
  purchase valued at 800,000; Heymann Ephraim's 200,000 at 5 per cent with
  the 30,000 proxeneticum). The memoir does not print the story of
  Triebenfeld's own estate - that is Åukasiewicz's telling - and
  Åukasiewicz's "35 000" for the valuation commission is not the memoir's
  figure either: the memoir makes the valuation itself cost the prince
  "etwa 3500 Thlr." (p. 22). The register's entry and the letters (400,000
  and 750,000) stand against both (the standing rule).
- The index: 60 hits of the edition's people and places (Hoym 23,
  Schulenburg 10, Berlin 6, Triebenfeld 4, SÃ¼dpreuÃŸen 4), every spelling
  already ruled for the other works; `--check` passes with 0 unruled. One
  hand-made link (`dorow-memoir`): the memoir's two self-identifying
  passages (pp. 18-19) to the same three letters of the Prince that stand
  against Åukasiewicz's telling (oe1bu9454-104, -108, -112); the
  attribution of the memoir is the volume's own and the Materialien's note
  152 spells it out.
- `literature_site.py`, `make_thumbs.py`, `build_site_data.py`, `jekyll
  build` and `verify_site.py` all pass (630 documents character-exact, 326
  hand-made links checked on both sides). `docs/LITERATURE_PLAN.md` Â§31
  records the work. The literature has 41 works, 35 with pages in both
  languages and six summary-only.
- Published at the editor's word ("Publish"): the commit cherry-picked to
  main (21a7d01f7) and pushed; the "Build and deploy" run 41286917735
  succeeded, and /literature/dorow1843/ and /de/literatur/dorow1843/
  answer, the "In the documents" box and its three letters included.

## 2026-11-01: the site fits a phone (the mobile overflow pass)

- The editor reported an overflow on the literature page on mobile. The
  whole built site was checked with a headless browser (puppeteer-core
  driving the machine's Edge, the pages served locally): every page of the
  site except the per-document ones (1,906 pages) and all 631 document
  pages, at 360 px and the previously broken set again at 390 and 320,
  measuring whether anything sticks out past the viewport's right edge.
  **First run: 18 of 58 sample pages overflowed; the full crawl: 54 pages;
  after the fixes: 0 of 1,985 pages.**
- Seven root causes, all in the CSS, one in the map layout:
  - **The materials-list cards** (`.source`): a card's automatic minimum as
    a grid item is its min-content, and the 400px thumb image's intrinsic
    width counted into it - every card refused to shrink below ~432px.
    Fixed with `min-width: 0` on the card and its body
    (`overflow-wrap: anywhere` there too, for the Dean & Hecker card's
    390px licence URL in its Published line).
  - **The literature's "In the documents" links** (`.lit-links-docs a`,
    `.lit-doclinks-pages a`): `white-space: nowrap` made one reference
    ("Oe 1 BÃ¼ 9454, document 108 (22 July 1800)") an unbreakable 350px run;
    the nowrap is gone, the links wrap like text.
  - **The literature's tables** (`.lit-orig/.lit-en/.lit-only table`):
    `display: block; max-width: 100%; overflow-x: auto` - MÄ…czak's
    thirteen-column table now scrolls inside its passage.
  - **The passage jump nav** (`.lit-jump a`): nowrap, and the Minakowska
    works key their passages by whole section headings - one link was
    427px. The links wrap now.
  - **The facts lines** (`.source-facts dd`): `overflow-wrap: anywhere` and
    `min-width: 0` on their flex items - the same licence URL overflowed
    the Dean & Hecker work page, and the map pages' Holder line their
    facts.
  - **The English-only works' text** (`.lit-only`): it lacked the
    `overflow-wrap: anywhere` the other passage containers had - the Dean
    & Hecker notes carry bare URLs 470px wide.
  - **The footnotes** (`.footnotes`, kramdown's endnote blocks): a long
    Wikimapia URL overflowed the Szetlew place page; any token may break
    there now.
  - **The browse filters** (`.filters label`, `.tools-filter select`): a
    select's intrinsic width is its widest option's ("Alexander I, Emperor
    of Russia (48)"), and the label would not shrink; `min-width: 0` on
    both.
  - **The map pages** (their own style block in `_layouts/map.html`): the
    sticky stage's viewer derives a width from its height through
    aspect-ratio (622px on a phone) and overflowed the stacked column by
    46px (`min-width: 0` on the stage); the boundary table
    (`.map-text-table`) scrolls inside its block like the literature's
    tables.
- The check's scripts stand in the session's temp folder
  (`C:/Users/Tersnaus/AppData/Local/Temp/opencode/mobilecheck/`): a crawler
  measuring `scrollWidth` against the viewport and reporting the widest
  offenders, driven over the page list of the built site. To re-run after a
  change: serve `site/_site` (python -m http.server), point the crawler at
  it, rebuild first. `jekyll build` and `verify_site.py` pass.

## 2026-11-01: the literature's call-outs reworked â€” "Related", one note per passage, a gutter column with a toggle (branch `related-callouts`, published at the editor's word)

- The problem, reported by the editor with /literature/materialien1861/ as
  the example: the boxes generated from `literature/links.yml` under the
  heading "In the documents" repeated themselves wherever a link named
  several passages of one work (18 of the 33 links; the worst stamped the
  same box about Bischofswerder, Zastrow, Dolffs and RÃ¼chel under nine pages
  of the Materialien and seven of the FeuerbrÃ¤nde), and each carried the
  link's whole sentence whether or not it bore on the page it stood under.
- **`about:` per-passage notes** (the editor's choices, asked 2026-11-01:
  the heading "Related"/"BezÃ¼ge", the notes inside one link rather than
  split links, the toggle beside the view buttons, on by default; the
  document side keeps "In the literature"): a link with more than one
  passage of a work carries an `about:` entry per passage â€” its own note
  (en, de) and its own documents, a subset of the link's. Every passage of
  such a link must have its note; every document of the link must belong to
  at least one passage; a one-passage link needs no `about:` and may not
  carry one. `literature_site.py` validates all of it and stops on a breach.
- **The passage entries pruned to their documents' reach**: the Treskow and
  Wendessen entries (Materialien pp. 152, 153, 171; FeuerbrÃ¤nde 2-74,
  2-90) leave `register-other-gifts` â€” the letter of 13 March 1799 does not
  touch them. Per-passage notes written for all 18 links that had repeated
  themselves; 72 passage entries now stand where 73 repeated placements
  stood.
- **The gutter column**: from 64rem viewport width the entry stands beside
  the passage (grid `minmax(0, 44rem) 14rem` on `.lit-passage.has-related`,
  the passage's text in a new `lit-main` wrapper); below that it folds under
  the passage text as the box did. The heading is "Related" (`lit_related`
  in i18n), German "BezÃ¼ge"; the toggle button (`.rbtn`, `data-related`
  on the body, `tf-lit-related` in localStorage, default on, `literature.js`)
  hides the column page-wide; without JavaScript it shows.
- Checked with the mobile crawler (its method in WORKING_NOTES) over all 42
  works in both languages at 320/360/390/1024/1280/1920: 504 checks, none
  overflowing; the toggle exercised on every page that carries it.
- **One new link from the rework's reading** â€” `register-donations`: the
  donation dossier I. HA Rep. 7 C Nr. 3570 (Hoym's proposal of 14 July 1796,
  the King's cabinet order of 23 July given at Pyrmont, the deeds of
  9 August 1796) against the register's entries whose deeds and valuations
  it holds (BlÃ¼cher's Duninow, Pontanus's Sieradz, Dolffs's Strzelec with
  the deed date the register prints, Goldbeck's chancery); where they
  disagree the notes say so (the proposal's 120,000 rt for all the Prince's
  items against the register's official 89,250 Thlr.; the proposal's yield
  of 1,500 rt for Duninow against the note's "certainly 6000 thalers").
- **The first sweep of new links** (the works LITERATURE_PLAN section 9
  had queued; every figure read in the book and in the document):
  - `held-krotoszyn` â€” Held (1801), the papers of FrÃ¼son's suit:
    Triebenfeld's administration of Krotoszyn until 1791 at some 17-18,000
    rt a year, FrÃ¼son's nine-year lease at 30,100 from 1 July 1791
    (pp. 12, 54, 79, 129, 173), the composition wrung from FrÃ¼son by
    Triebenfeld and Neumann giving the lease up (p. 34) â€” which the King's
    refusal of 4 December 1798 prices from the government's side: the
    Abstand of 26,000 rt for the Abtretung der Pacht of 1795
    (oe1bu9454-85, -86, -101). Claude's reading; NEEDS_CONFIRMATION.
  - `guradze1898-emancipation` â€” the Duchy of Warsaw's constitution of
    22 July 1807 and the decree of 24 December 1807 abolished hereditary
    subjection; the lease's paragraph 13 had freed its eighteen lessees of
    it two years before (app539680801-3).
  - `paciorkowski1776-boundary` â€” the 1768 constitution's approval rule and
    its rules on boundaries destroyed or privately erected, beside the
    Tribunal's approval of 23 January 1782, the demolition act of
    28 November 1782 and CheÅ‚mski's protest of 1778 (Konin Gr. 153, Konin
    Gr. 117). Claude's reading; NEEDS_CONFIRMATION.
- New in NEEDS_CONFIRMATION: the register's official 89,250 Thlr. against
  the dossier's proposal of 120,000 rt; the Duninow yield (1,500 rt against
  "certainly 6000"); the Konin row's 12,000 (a slip or a row?); Å»ychliÅ„ski
  (1885) writing WÅ‚adysÅ‚aw where the summons of 1860 names WÅ‚odzimierz;
  Held's composition identified with the 1795 Abtretung; the Paciorkowski
  tie as resemblance, not statute.
- Verified: build and `pipeline/verify_site.py` clean (37 links, 40
  documents, 302 link-pairs checked on both sides). Published at the editor's word, 2026-11-01: the two commits cherry-picked onto main (the PeÅ‚zucki 1896 map work beneath the branch left unpublished, the editor's word), the Build and deploy run 41331884277 succeeded.

## 2026-11-01: the connections between documents of different holdings â€” the mechanism, the method, the step in every adding-a-source procedure (branch `related-callouts`, published at the editor's word)

- The editor asked how connections to other documents should be made â€”
  going deeper, across all the documents and not just the literature â€” and
  that the step be part of adding any new source, with the new source's
  connections into existing documents proposed as part of the adding.
- **Built now** (the editor's choice, asked with the plan): the four kinds
  of connection gathered in one standing reference, `docs/CONNECTIONS.md` â€”
  the within-holding relations of `rulings.yml` (they have stood since
  2026-10-03), the new cross-holding connections, the literature's and the
  other sources' links, and the computed index â€” with the method (chains,
  per-entity sweeps, figures as hooks, the era essay as a map; the measure
  of relevance: a document that confirms, corrects, extends or dates what
  the other says) and the Connections step that every adding-a-source
  procedure now carries (NEW_UNIT section 8's table, the newspapers',
  places' and literature's plans).
- **`reference/connections.yml`** â€” each connection names at least two
  documents of different holdings, each participant with its own note in
  English and German: the note THAT document's page shows, so no page
  carries a sentence written for the other side (the per-passage lesson).
  `pipeline/build/connections_site.py` (a step of `regenerate.py`) checks
  it and writes `site/_data/connections.yml`; a document's page shows its
  own note and links to the other participants in the "About this document"
  box, headed "Related"/"BezÃ¼ge" (`doc_related` in i18n);
  `pipeline/verify_site.py` checks every participant's page links every
  other participant, both languages.
- **The first batch, the chains pass** (the editor's choice): four
  connections, eight documents, each resting on links the editor has
  already ruled and carrying no new identification â€” the donation dossier
  against the letter reporting its gift's yields (4-6,000 expected in 1796;
  20,000 reported by March 1799); the lost privilege of 1746 and its two
  witnesses (the decree of 1775, the summons of 1860, which also pleads the
  contract of 18 May 1805); the two registers that count the same villages
  eight years apart (Kalisz Tab. 21's hearth money of 1789, the General
  Directory's houses and people of 1797); the Commission's resolution of
  21 July 1807 kept by two offices (the file's draft, the register's
  protocol). Screenshots checked the box at 1280 and 360 (no overflow;
  document pages are single-URL, the language swapped in-page).
- Verified: build and `pipeline/verify_site.py` clean (8 cross-holding
  connections checked on both sides). Published at the editor's word, 2026-11-01: the two commits cherry-picked onto main (the PeÅ‚zucki 1896 map work beneath the branch left unpublished, the editor's word), the Build and deploy run 41331884277 succeeded.

## 2026-11-01: The KoÅ›ciuszko letter of 3 IX 1798 added as the holding ossol2289 (B. Ossol. rkp. 2289 II)

- The editor ruled the attribution working and asked for the letter to be
  added: the copy of KoÅ›ciuszko's letter of 3 September 1798, written in
  Paris, on page 145 of the PrzyÅ‚Ä™cki copy collection at the Ossolineum
  (scan 0062 of the thirty-scan set). The holding is the first from the
  Ossolineum and opens the new era `insurgency` (working name; the later
  eras' orders bumped; the Eras page renders it from the blurb).
- The transcription is the editor's corrected reading of Claude's
  band-by-band first pass, kept as written: the copyist's orthography, the
  superscript expansions in brackets (Sz[anowny] Ob[ywatel]u, P[aryÅ¼a]),
  the six line-end wraps marked and decided (`linebreak_decisions.csv`,
  all joins, decided by hand - the automatic resolver reads German evidence
  and cannot see Polish). No doubt marks remain.
- Translated in session, no paid run (the single-document path):
  `intake/translation/write_cache.py` writes the English into the
  translation cache with the source_hash, `publish_translations.py`
  publishes it; `check_translations.py` raised 0 rows. The summaries were
  written in both languages and their 10 statements claim-checked
  (`intake/claim_check.yml`), all supported.
- The person entry **Tadeusz KoÅ›ciuszko** added (`people.yml`,
  `people_bios.yml`, `people_headings.yml`; the pattern counted before -
  no document outside ossol2289 names him). The correspondents record
  carries the sender only: the letter never names its addressee, and the
  probable identification with Antoni Prusimski (PSB, pachonski1982) lives
  in the holding's prose as "probably" (NEEDS_CONFIRMATION).
- Intake is selective: only scan 0062 is staged
  (`units/ossol2289/intake/build_pages.py`, TIFF to pages/ as
  `NBO_2289_0145_a.jpg`, relabelled, web derivative and card thumbnail
  made). The other 29 scans stay on disk, read and logged in
  `scratch/ossolineum2289/`, not brought into the edition.
- `merge_corpus`, `build_dataset`, `build_site_data`, `jekyll build` and
  `verify_site.py` pass: 631 documents, text verified character-exact,
  61,688 internal links resolve, 7 eras on the Eras page.

## 2026-11-01: the Prusimski attribution of the ossol2289 letter ruled out for now

- The editor's word: "rule out for now that the letter is not related to
  Prusimski; until something tells us otherwise." The letter keeps its
  place in the edition (holding `ossol2289`), but the addressee is
  treated as not named everywhere: `correspondents.json` carries the
  sender only with the ruling recorded as the recipient's basis; the
  holding's page (about.md/about_de.md) has a new "The addressee"
  section that lays out what was proposed, what stands against it and
  what would reopen it; the summaries (both languages), the era `insurgency`'s
  blurb, the unit.yml title/description and the KoÅ›ciuszko person entry
  (people.yml, people_bios.yml) all drop the "probably Prusimski" wording.
- The grounds, checked in session: PachoÅ„ski's PSB entry cites the
  manuscript in its general source list with no footnote apparatus in the
  file the edition holds (so the citation is attached to no claim), and
  the two phrases the entry quotes for the exchange (Â«Lud i WolnoÅ›Ä‡ to dwa
  filaryâ€¦Â», Â«nie zna go osobiÅ›cieÂ») appear in the copy in neither
  wording. PachoÅ„ski's 1973 Venice article (complete 31-note apparatus,
  read in the literature) cites no Ossolineum manuscript and ends before
  1798 - it contributes context only.
- What would reopen the identification: the printed PSB volume's footnote
  apparatus (t. 27, digitised), an Ossolineum inventory card for
  rkp. 2289/II, or a name at the index level in the codex's own leaves
  (0033-0034 unread to the name level; 0061 unread). Recorded in
  NEEDS_CONFIRMATION and the holding's notes; the "10 Aug." / "13 VIII"
  discrepancy stands on its own.

## 2026-11-01: correction to the attribution ruling - the PSB source list is the whole of it

- The editor: "There's no missing PSB footnote apparatus; I've provided
  the entire article. You got as much info about the Ossolineum source
  that exists." The suggestion that a printed footnote apparatus of PSB
  t. 27 could settle what PachoÅ„ski took from rkp. 2289/II was wrong and
  is struck from the record: a PSB entry carries its sources as a
  general list, with no per-claim notes, and the file the edition holds
  is the entire article. The citation in that list is everything
  PachoÅ„ski gives about the manuscript - what he took from the codex,
  and for which claim, is not recoverable from what he printed.
- Worked into about.md/about_de.md, the holding's notes.md and
  NEEDS_CONFIRMATION. The reopening conditions are now only: an
  Ossolineum catalogue description or inventory card for rkp. 2289/II,
  or a name at the index level in the codex's own leaves (0033-0034,
  0061). The ruling itself (the link to Prusimski ruled out for now)
  is unchanged.

## 2026-11-01: the ossol2289 attribution closed - the evidence exhausted in hand

- The editor: "There is no name in 0033-0034. There is no inventory card
  beyond the link that I shared with you - so this is all that we have."
  The two remaining reopening paths of the previous entries are gone:
  the codex's own index of letters names no addressee for the KoÅ›ciuszko
  letter (the editor's reading of leaves 0033-0034), and the library's
  record for the codex is the catalogue entry the editor shared, which
  describes the contents no further than its title.
- The identification is therefore set aside not pending a look but for
  lack of anything further to look at. Only new evidence - the original
  of the letter surfacing, a second copy elsewhere, or new scholarship -
  could reopen it. Worked into about.md/about_de.md, notes.md,
  correspondents.json, NEEDS_CONFIRMATION and CLAUDE.md; the holding
  itself, its transcription, translation and summaries are unchanged.

## 2026-11-01: the literature cards shortened - `published_card`

- The editor: the cards on the Literature page are too lengthy, "especially
  with the punishing details". The length sat in the published line, which
  reused the work page's full `published:` and had collected excerpt spans,
  reissue and digitisation citations, year-inference notes, licences, ISBNs
  and production credits. Standing rule (LITERATURE_PLAN.md Â§33,
  HOUSE_STYLE "Concision"): a card gives the original imprint or
  first-publication citation and a one- or two-sentence brief; everything
  about how the site holds the work stays on the work's own page.
- New `published_card:` in 24 works' `work.yml` (beside `published:`),
  carried into the site data by `literature_site.py`'s `card_extra()` and
  rendered by `_includes/literature.html` as
  `published_card | default: published`, top-level cards and the sub-item.
  The work pages keep the full line; nothing is cut from the site.
- Five briefs trimmed of the clause naming what the site holds
  (karwowski1900, werner1904, zychlinski1885, zychlinski1891,
  breyer1935gaue), both languages. Card titles carrying excerpt detail
  (dean2012warthegau, zychlinski both, janocki1779, boniecki1900) left for
  the editor's ruling (LITERATURE_PLAN.md Â§33).

## 2026-11-02: the yard analysis and the farm-polygon tool (scratch/map4456, committed by exception)

- The homestead-yard page (yard_map.html, built by build_yard_map.py) grew
  through the marking sessions: number changes on tags, the click-outside
  deselect and the fixed active-farm height (no shifting panel), the L
  all-labels toggle as a Layers button row moved to the sidebar's top, [?]
  uncertain reads accepted in the change field, the note-after-save attach,
  added numbers (A: drag a box round the red number, a click marks the
  spot, Enter -> the tag on the map), and the uncertain-numbers queue —
  the [?] tags walked one at a time with the neighbouring confident tags
  as context, a suggestion from the nearest neighbour, comments, and
  read-is-right/uncertain/use-suggestion marks; fixed entries leave the
  list (64 of 117 left).
- The tag scheme settled: red on semi-transparent white (confident), solid
  yellow (the read carries [?]); purple and the purple review retired —
  the uncertain queue replaces it. The export's red_fixes are baked into
  the page data at build, the build auto-refreshes yards_read.json from
  Downloads and relinks the yards whose tag fix moved.
- yard_analysis.py (new): the yard test per farm — a piece's figure, or a
  subset sum of the pieces, against the statement's buildings-and-gardens
  column; near-sums (a stroke in a read), one-digit slips, exact matches
  on other rows with distances (the forest caution: neighbouring pieces
  of forest carry different numbers), the elimination (a confident figure
  fitting no row), the unread-piece gap. Rulings over 74 farm claims:
  29 confirmed, 7 near-fit, 7 weak, 2 wrong (farms 3 and 4), the rest
  open or untestable. Output: yard_analysis.json.
- The rulings ride the yard page: green solid, light-green near-fit,
  yellow weak, red wrong — each with a why in the sidebar's Ruling box.
- 87 -> 82 corrected at the editor's word: the yard "1. 288" at
  (5329, 6913) is farm 82's (Rogatskii Stanislav) — the buildings figure
  288 exact and the red-82 site 594 px away, closing the farm-15 probe.
- The southwest row re-read at the editor's word: 5, 10, 25, 25, 29 ->
  5, 10, 25, 29, [9?]7 (the 25 that had been corrected away from the OCR's
  29 restored; the last 29 was the catalogue's [8?]9).
- build_farm_polygons.py + farm_polygons.html (new): the farm-polygon
  tool, first stone of the updated vector map — polygons drawn per farm
  (D, vertices, U, Enter, Esc), a clicked tag choosing the farm for the
  next polygon, tags renumberable on the page with the polygons following
  the renumbering, vertex and edge editing (drag a vertex, drag anywhere
  on an edge to insert, click a vertex + Delete, Ctrl+Z undo of 50
  steps), the farms list shaded by the polygon area against the
  statement's row total (green approaching 100%, red past it,
  logarithmically deepening through 2x), the missing-from-the-map box,
  the black-number sites as a layer, the wheel forwarded to the viewer
  over the polygons (a synthetic wheel on the canvas — Firefox's event
  ordering handled), the areas approximate (~0.4 m/px, 28.4 px2/saz).
- The rows without confident tags, the next pass's targets: 88 (German
  Voitsekh) and 90 (Rogovich Martin) — no tags at all; 19, 40, 48, 64,
  89, 94, 96 — only uncertain ones. The parcel-sum plan (the plots' D-S
  labels summed per red cluster against the row totals) named in
  maps/pelzucki1896/notes.md as the road to close them, with the
  measurement-register search at APL 39/98 as the shortcut.
## 2026-11-01: the card titles ruled - `title_card`

- The editor: "I don't need to see page numbers in the title cards." Six
  titles and four English titles carried the page span of what the site
  holds; each got `title_card:` / `title_en_card:` beside its full `title:`
  / `title_en:` (the work's own title alone, e.g. "ZÅ‚ota ksiÄ™ga szlachty
  polskiÃ©j, rocznik VII"), carried into the site data by `card_extra()` and
  rendered by the same `| default:` fallback as `published_card`. The work
  pages keep the full titles (the account there says what is given). The
  Minakowska person IDs stay: the database's identification, not a page
  span. LITERATURE_PLAN.md Â§33 records the ruling.

## 2026-11-04: the faithfulness review - translations, summaries and links held to their sources

- The standing prompt written first (docs/FAITHFULNESS_REVIEW_PROMPT.md): what a review
  agent may assert, the evidence every finding needs (quotation on both sides, or it is
  not a finding), the corpus-then-scan order of ground truth, the settled rulings
  respected, findings by severity (error / likely error / worth checking), proposals in
  the house voice and never applied by the reviewer.
- All 51 holdings reviewed in four passes - summaries (EN+DE), about pairs, translations,
  links: 178 findings (27 errors, 28 likely errors, 123 worth checking), reports and the
  filterable selection sheet under review/faithfulness/ (gitignored, rebuilt by
  make_html.py from the per-unit reports).
- The editor chose 177 findings in the sheet and the approved proposals were applied
  where they carried wording (~150; the conditional ones - none until a reading is
  settled - left as drafted, each logged under review/faithfulness/tmp/impl/):
  translations in the cache and republished (--force; --tag v2 for the four v2-bound
  units), summaries in cache and site/_data in sync (the build cannot carry them - the
  in-session pads have no cache entry), about pairs and the three link files in place.
- Headline corrections: oe1bu14525 Seiner Liebden rendered as direct address in eight
  letters (His Lordship restored) and the Pszczew-or-Pszczew formula in five more
  (Pszczew, called Betsche); oe1bu14526-018 the 7,000-Rthl instalment read as 1,000
  (scan and twin document settle it); app536040 six thousand shingles read as a hundred
  threescore; oe1bu9454-285 the grantee reversed in both summaries - the King granted
  Kamionna to the Prince, not to Prusimski; app5320pozgr1181 Inowrocław and the
  5,500 florins restored; oe1bu9454 about pair missing the majorat's Oppurg;
  ihagrrep7cnr3705 and iharep162nr295 about claims their own deeds contradict;
  iiihamdaiiinr12765 doc 6 ruled to the house form (ecus-reichsthaler) with the
  summaries corrected to match the ruling; the literature links' Zychliński
  three-brothers and Rostworowski signature claims corrected, the connections.yml
  header comment's false NEEDS_CONFIRMATION claim dropped.
- One judgment call recorded: iiihamdaiiinr12367-007's good-groschen proposal trimmed
  to the four bushel prices the corpus actually writes ggr. on; the Rthl conversion
  line reads plain gr. and stands.
- Rebuilt by replaying regenerate.py's steps with the pipeline self-check skipped
  (pre-existing debt, WORKING_NOTES); check_unit_text caught one em dash the fix
  agents had introduced (app536047) and it was set to the spaced en dash; verify_site
  ALL CHECKS PASSED - 631 documents character-exact, 61,579 internal links, 302
  hand-made links and 8 cross-holding connections checked on both sides.
## 2026-11-06: the Pełzucki 1896 map finished on the site - the farm labels, the field numbers, the farm plots, and the settlers' proper names

- The labelling sessions folded into the edition data (scratch/map4456/
  build_farm_labels.py -> pipeline/maps/import_farms.py): maps/pelzucki1896/
  farms.yml now carries 101 labels over 83 of the 97 rows (28 labels beyond
  one per farm - multi-farmstead holdings; the 14 still without a label are
  12, 25, 28, 30, 43, 48, 64, 79, 85, 88, 96 and the common land, the
  headman's plot and the roads - 94, 95, 97),
  maps/pelzucki1896/reds.yml the 407 field numbers (306 corrections or
  moves, 8 additions over the OCR-only pass, none deleted), and
  maps/pelzucki1896/polygons.yml the 44 farm-plot polygons over 29 farms
  (the drawings of 2026-11-02, with the area calibration, ~0.4 m/px).
- The map page (site/_layouts/map.html, site/assets/maps/map-viewer.js)
  grew the layers the editor asked for (2026-11-05), each its own toggle:
  the farm names, on by default (pills № n · name, a click opens the
  farm's table row); the farm plots, on by default (the polygons as one SVG
  overlay whose viewBox is the mosaic's own pixel box, a quiet fill, a
  stroke that keeps its screen width at every zoom, a per-polygon tooltip);
  and the field numbers, off by default.
- The field numbers' pills are grey - the editor's ruling (2026-11-05):
  they are the plan's own finding aids, not highlights, so every one wears
  the same grey on both pages, the unsure readings marked by their [?] and
  a tooltip, never by colour.
- The settlers' proper names (docs/NAME_NORMALISATION_PLAN.md; the editor's
  rulings of 2026-11-05: Gibel not Göbel, Bitner not Büttner, Schönfisch
  not Scheinfisch): every row of farms.yml carries name_norm, name_lang,
  norm_conf and norm_note beside the documentary readings, which stand
  untouched; 62 rows firm, 35 conjectural. The map's pills show the proper
  spelling where it is firm; the settlers' table gains a "Proper spelling"
  column (Richtige Schreibweise), the conjectural rows marked with an
  asterisk and their note as a tooltip. The institutional rows renamed as
  ruled - Village school / Dorfschule, Common cemetery / Gemeindefriedhof,
  Plot of common land / Allmende, The village headman's plot /
  Schulzengrundstück (the German rides along and the pills speak the
  page's language) - and row 97 reads Roads (Wege), not "Under roads".
- Document 6, the liquidation register (apl399806603-006), shows the proper
  names in its translation's name column: the Russian transliterations
  (Konchinskii Iakov) are gone from the English table, the conjectural
  brackets ride along ("[uncertain: Śliwiński] Gottlieb" keeps its
  doubt), the institutions keep their English labels, and the register's 96
  entries all agree with farms.yml (row 97 Roads belongs to the plan, not
  to the register). The diplomatic and reading views keep the manuscript's
  Cyrillic and its transliteration untouched.
  scratch/map4456/apply_doc6_names.py applied it to the published
  translation and the intake alike, and a check proved only the name column
  changed in either file.
- The save server (scratch/map4456/save_server.py) now sends
  Cache-Control: no-store on its state, version and save responses: the
  browser heuristically caches a Last-Modified answer, a reload could then
  serve the pre-save state, and a window could save against a version the
  file had long outgrown. Found by the test battery; the editor's own
  server carried the same latent bug and was restarted with the fix.
- The battery stands at 14 suites / 175 checks, all passing, against a
  sandbox state dir (test_server.py, port 8780, --state-dir test-state),
  the editor's working files hash-proven untouched before and after. The
  suites updated to the imported dataset (the unmarked-farm suites remove
  a farm's label as setup; the red-edit suite resolves its pill by its
  record's own position, not by a reading another parcel repeats; the
  counts read the imported 101).
- Site-wide, a table's column heads stand on a tinted band (--thead in
  site/assets/style.css), the ledger tables' caption on the same band. The
  maps' card thumbnails (pipeline/build/make_thumbs.py) are fetched from
  the tiles' info.json's own smallest whole-map level: the fixed 1/32
  request 404ed for Pełzucki 1896 (679 px wide there, past one tile), which
  is why the map's card went without its picture.
- maps/pelzucki1896/texts.yml: the boundary walk's table gained its Russian
  column heads for the as-drawn view, the explication's German head reads
  Des./Saz. as its English does, and the boundary and explication notes are
  trimmed to what a reader needs (the summation argument left to the
  pipeline's own check).
- Built clean and checked: jekyll build, verify_site ALL CHECKS PASSED
  (631 documents character-exact, 61,775 internal links, no external
  dependencies), and the built site driven in a real browser (26 checks:
  the three layers' defaults, the 44 polygons, the grey pills, the proper
  spellings on both language pages, the proper-spelling column, document
  6's translation table and its untouched Cyrillic).
- Retired at the editor's word (the same day, 2026-11-06): the farm plots
  layer. The polygons she drew over the mosaic proved an unreliable way to
  carry the farm boundaries, and the page shows them no longer -
  maps/pelzucki1896/polygons.yml deleted, the plots toggle, its SVG overlay
  and its styles lifted out of the map layout and viewer, the
  polygons/poly_calibration keys out of map_pages.py and site/_data/
  maps.yml, the map_plots_layer strings out of i18n.yml. The farm names
  and the grey field numbers stand as before (names on, numbers off by
  default); the drawing tool itself remains under scratch/map4456/ as the
  record of the attempt. Verified as the whole map page was: jekyll,
  verify_site ALL CHECKS PASSED (61,775 links), and the real-browser
  checks - the plots button and SVG asserted absent, everything else
  unchanged (22/22).
- The settlers' table re-worked at the editor's word (2026-11-06): one
  Settler column, carrying the proper names alone - the documentary
  transliterations (Gebel Martin) are off the table, the map's pills
  already showed the proper spellings - the institutional rows speaking
  the page's language (Village school / Dorfschule); and the 1868
  statement's Morgen and rods now carry hectares in parentheses
  ("29 M 262 r, 1868 (16.7 ha)"), converted at the mórg nowopolski, the
  Królestwo's official morga of 1819-1849 and the one used in practice to
  the mid-twentieth century (0.5598 ha, 300 square rods - the table's own
  rods run to 295, so the 300-rod mórg is the unit it writes in; the
  Prussian small Morgen of 0.2553 ha is ruled out by the same figures).
  The survey of 1896 measured the holding anew and found it larger
  (5-21% on every row checked), so the hectares convert the 1868 figures
  alone and stand beside the 1896 desyatinas, not against them. The
  conversion is computed per row in pipeline/maps/map_pages.py; the
  Proper spelling header string is retired from i18n.yml.
  A short note under the table says the same in plain language, in the
  reader's language (map_morgen_note in i18n.yml): what the hectares are
  converted at, and that the survey's own figures are the desyatinas.
- The page restructured to the editor's tab plan (2026-11-06): the index
  of places back in the sidebar, close to the top as on the other maps'
  pages, and everything below the map under four tabs - Texts on the
  sheet (the title block and the certification), Adjoining lands (the
  boundary table), The land-area table, Farmsteads - one pane at a time
  on html[data-maptab] set before anything renders, every pane showing
  without JS, the language tabs riding the same bar in the site's button
  style. The land-area table loses the word explication (the editor: it
  confuses) - the tab and the heading read "The land-area table" - and
  gains Morgen and hectares beside the desiatinas: computed per row in
  map_pages.py at one desyatina = 2400 square sazhens of 4.5522 m2
  (about 1.09 ha) and the mórg nowopolski of the farmsteads' table
  (0.5598 ha), the original-language pane keeping the table as written.
  The figures corroborate the conversion independently: the basic
  allotment's 870 des 1454 saz read back as 1,699 M 33 r against the
  1868 statement's own 1,691 M 219 r - the same land within half a
  percent - while the total of 2,085 M 116 r (1,167 ha) carries the
  survey's ~23% growth in the additional allotment. The block's shared
  rendering moved to an include (site/_includes/map-text-block.html);
  a farm Locate from the farmsteads pane still flies the map, and a
  farm focus brings its tab forward first. jekyll and verify_site ALL
  CHECKS PASSED (61,294 links), the real-browser checks re-run (41/41).
- The legend trimmed and the settlers' names re-formed, at the editor's
  word (2026-11-06): the legend's own title ("Explanation of the signs" /
  Erklärung der Zeichen) shows no longer - the section heading and the
  language tabs say what is what, so the legend table needs no language
  column of its own either; and every settler's name now reads given
  name, surname (Jakub Kończyński, Martin Gibel, Karl Benjamin Schwebs),
  the Russian transliterations' surname-first order not carried into the
  display - 82 rows re-formed in farms.yml, the map's pills and document
  6's translation table following (apply_doc6_names.py re-run, 82 names
  synced). The bracketed markers are off the display names too: rows 12
  and 25 read Gottlieb Śliwiński and Szczepan Promins, row 77 Christian
  Haupt - the doubt stays where it belongs, in the conjectural asterisk
  and the row's note; row 12's collation had found all three witnesses
  agreeing, so the display ruling lifts the pending doubt there (its
  norm_note records it), while 25 and 77 keep their asterisks.
- The page restructured to the editor's tab plan (2026-11-06): the index
  of places back in the sidebar, close to the top as on the other maps'
  pages, and everything below the map under four tabs - Texts on the
  sheet (the title block and the certification), Adjoining lands (the
  boundary table), The land-area table, Farmsteads - one pane at a time
  on html[data-maptab] set before anything renders, every pane showing
  without JS, the language tabs riding the same bar in the site's button
  style. The land-area table loses the word explication (the editor: it
  confuses) - the tab and the heading read "The land-area table" - and
  gains Morgen and hectares beside the desiatinas: computed per row in
  map_pages.py at one desyatina = 2400 square sazhens of 4.5522 m2
  (about 1.09 ha) and the mórg nowopolski of the farmsteads' table
  (0.5598 ha), the original-language pane keeping the table as written.
  The figures corroborate the conversion independently: the basic
  allotment's 870 des 1454 saz read back as 1,699 M 33 r against the
  1868 statement's own 1,691 M 219 r - the same land within half a
  percent - while the total of 2,085 M 116 r (1,167 ha) carries the
  survey's ~23% growth in the additional allotment. The block's shared
  rendering moved to an include (site/_includes/map-text-block.html);
  a farm Locate from the farmsteads pane still flies the map, and a
  farm focus brings its tab forward first. jekyll and verify_site ALL
  CHECKS PASSED (61,294 links), the real-browser checks re-run (41/41).
- The map page cleaned up at the editor's word (2026-11-06), to read like
  the other source pages: the prose note under the Farmsteads heading is
  gone (the hectares note stays); "The farmsteads" reads Farmsteads
  (Gehöfte); the Hide linked button is off the site page - the layer
  toggles are all it needs, the working page keeps its switch; the
  language tabs wear the site's own .vbtn button (the pill they wore read
  as a different kind of control); and the index of places moved out of
  the narrow sidebar into a full-width table below the Farmsteads
  (Place / On the sheet / Locate-Today), the sidebar keeping the facts,
  the boundary walk and the legend beside the map. A Locate called from
  the tables below now brings the map into view as it flies (the viewer
  scrolls into view; a farm Locate no longer scrolls the page to the row
  it came from).

## 2026-11-06: the genealogy explorer loads on a project-site deployment

- The explorer hung forever on "Loading the family database …": its built
  shell asked for the bundle at the absolute /genealogy/assets/app.js,
  which only exists when the site is published at a domain root. Published
  as a project site (takaji10.github.io/triebenfeld-letters/), that URL
  fell to the server's HTML 404 page, the browser refused the module
  (Firefox: "disallowed MIME type (text/html)"), and nothing replaced the
  boot screen. The top-bar link and every data fetch already resolved
  relative to the page; the bundle reference alone was absolute.
- The fix (site/genealogy/vite.config.js): base is './', so the built
  shell references ./assets/app.js and ./assets/index.css and the same
  committed build serves under a user site, a project site or any other
  prefix. The committed assets (assets/app.js, index.css, index.html)
  were rebuilt with it.
- verify_site.py's link check resolved every URL against the site root,
  so a document-relative reference read as broken. It now resolves
  ./- and ../-prefixed URLs against the page's own directory - the
  browser's own rule - and passes with the project baseurl as with none.
- The loading page now speaks when the application never arrives
  (shell.html, the source of the built index.html): a plain inline watch
  shows troubleshooting guidance the moment the module script fails to
  load, and after 15 s at the latest - a wrong address, a connection
  problem, a content blocker or browser settings that block scripts -
  with a hard-reload reminder and a link back to the archive home,
  English with German beneath (the visitor's browser language picks the
  lead). The application module stands the watch down the moment it runs
  (window.__zfBooted in src/main.js).
- Inside the application the boot screen gained a progress bar - the
  eight opening files of the database fetch tick it along
  (db.progress in src/lib/db.svelte.js) - and after eight seconds a
  quiet hint that a slow connection or a content blocker can hold the
  database back, in all three interface languages (boot_loading,
  boot_slow in src/lib/i18n.js).
- Built clean and checked: jekyll build and verify_site ALL CHECKS PASSED
  twice over, once with the default baseurl and once with
  /triebenfeld-letters (63,294 internal links each), and the built
  genealogy page and its bundle served and fetched through a local
  server under a nested prefix, the bundle answering text/javascript.
- Found on the live site the same day, once the application finally
  loaded for a visitor: the static boot placeholder survived the mount,
  the "Loading the family database" line sitting above the rendered
  application. Svelte 5's mount() appends to its target - it does not
  replace what is inside (the clear the old shell design leaned on runs
  only in the hydration error path) - so src/main.js now clears #app by
  hand before mounting, and if the mount itself throws it leaves a word
  on the page instead of a blank one. Rebuilt and re-checked the same
  way (both baseurls, ALL CHECKS PASSED).

## 2026-11-06: the genealogy explorer - the Lacho branch finished, the
## media URLs repaired, sorting and IDs on the people lists, the tree on
## the person page

- **The exclusion now removes what it always said it would.** The old
  fixpoint's rule - a child with one kept parent stays - deadlocked
  against itself: a removed sibling's children kept the outsider spouse
  alive (the spouse was the kept parent), and the spouse kept the
  children alive, so the sibling's whole line survived the cut it was
  ruled out of. The published database carried Larry's siblings'
  descendants (I2190-I2192 through their mother I2189, I2202-I2203
  through I2201, I2194 through I2243). prune.py now computes the ruling
  of PLAN.md 4.3 as three passes: the seed (the blood ancestors of the
  roots), the protected line (the roots and their blood descendants -
  the "except through I0005"), and the branch (every blood descendant of
  the seed the walk reaches without passing the protected line); then
  the old fixpoint sweeps the hangers-on, spouses married only into
  removed lines now going regardless of their own natal family (the
  ruling removes the spouse; their parents and siblings married into
  nothing). Measured: 328 people, 245 media, 115 families removed (was
  78/70/19); 4,111 people published (was 4,361). Checked on the real
  data: no protected person is removed, Larry stays, and none of the
  170 blood-removed people has a kept co-parent - the plan's mixed-
  marriage ambiguity never arises in this database. The build's two
  remaining "note mentions an excluded person" items (I0486, I2073) are
  the standing editor's-call class.
- **Every image on the site was broken, shown as "image not
  published".** The manifest's file fields are relative to the media
  repo's media/ directory (the docx entries' originals/ prefix shows the
  convention), but config.yml's media.base lacked the media/ segment, so
  the viewer asked takaji10.github.io/genealogy-media/<hash>.jpg for a
  file that lives at .../media/<hash>.jpg - 404, the img's onerror fired,
  and the viewer fell back to its missing-note. Found on I3131 (Andreas
  Landkammer, his birth record C1796 and death record C0707); every one
  of the 1,698 published items was affected. The base now carries the
  segment (config.yml), the data rebuilt, and the URLs verified against
  the live repo B (200 for the display and thumbnail shapes).
- **The tree route was dead code: it threw on render.** Tree.svelte
  iterated a `links` identifier it never declared - the layout returns
  {nodes, links, ...} but the component never derived it - so
  #/tree/<id> died with a ReferenceError the moment it rendered. Fixed
  (links is a derived of the chart now), and the component gained what
  the fix exposed as missing: the cards carry the person's ID (the cards
  grew a third line), the chart centres on the focus person instead of
  top-aligning, and an embed mode for the person page - the mode pills
  switch a local state and the chevron re-roots the chart locally, both
  without leaving the page, and a plain wheel scroll moves the page
  while Ctrl+wheel zooms (pinch always zooms).
- **The person page shows the tree.** An interactive hourglass chart
  (pedigree and descendants one pill away) sits under the header:
  clicking a card opens that person's page - the move up and down the
  tree - and the chevron re-centers the chart on them in place.
- **IDs are shown wherever people are listed** (the editor's ruling:
  Gramps IDs are the join key of the whole project): the surname page's
  people table gained an ID column, search results and the place pages'
  event tables carry the ID beside the name, the person page's relations
  (parents, siblings, spouses, children) carry it, the header shows the
  person's own ID as a pill, and the tree cards show it under the years.
- **The surname index sorts.** Three orders on the index - by count
  (the old default, ties broken A-Z), A-Z, Z-A - and two on a surname's
  people table (A-Z, Z-A, by display name; the old sort was by given
  name alone). Buttons on the page, labels in all three interface
  languages (sort_az, sort_za, sort_count, siblings new in i18n.js).
- **Parents and siblings on the person page carry life dates** - the
  parents section shows each parent's years beside the ID, the new
  siblings section (the other children of the same parent family) shows
  the same, and the spouses and children under partnerships show theirs.
- Built: data from the 5 NOV 2026 GEDCOM (4,111 people, 1,440 families,
  1,698 media, 1,105 places), app rebuilt, jekyll and verify_site ALL
  CHECKS PASSED with the project baseurl and with none (63,294 internal
  links each), the new data and shards served and fetched through a
  local server, and the tree layout exercised headlessly against the
  new families (I3131's six siblings render, I0005's cut famc renders
  honestly without parents).

## 2026-11-06: the exclusion widened to the ancestors' whole world

- The editor found Trzeciaks, Chikowskis and Klowaks still in the
  database and ruled: everything connected to Larry only through his
  ancestors goes, in all directions. The morning's cut had followed
  blood alone, which left the in-laws' own families standing behind the
  removed spouses - Tatianna Trzeciak (married into the Lechów line)
  was gone but her father and siblings stayed; a branch Rychlicki's
  Klowak-named children stayed where their father link was unrecorded;
  the Roths sat behind a living Lacko in-law. prune.py now partitions
  the database by connectivity instead of running a rule fixpoint: the
  seed (Larry's blood ancestors), the kept world (everything reachable
  from Larry through ANY family link without entering the seed - his
  descendants, their spouses' families, the Zelmer side entire), and
  the removed world (the seed plus everything reachable from it without
  entering the kept set). A person reachable from both worlds stays -
  a branch member who married back into Larry's world belongs to both,
  and in this database there are none. Measured: 418 people, 279 media,
  146 families removed (was 328/245/115); 4,021 people published (was
  4,111). Checked: Trzeciak, Chikowski, Rychlicki, Klowak, Roth, Masluk,
  Ribachuk, McKay, Vogt, Sawuła and Lacho at zero in the published
  index; no one removed by the previous cut comes back; no core
  Zelmer-side surname (Zelmer/Zellmer/Celmer/Cellmer, Flatt, Fengler/
  Fingler, Koss, Strecker, Schmidt) is touched.
- Two [Living] Trzeciak placeholders (I1232, I1235) are an island: a
  husband and wife married to each other with no parents, children or
  events, and no recorded link to any other person - no walk can reach
  them. The config gains exclusion.people, an explicit list for such
  islands, named by the editor's ruling and reported like the rest of
  the cut; build.py and media_build.py pass it so both builds exclude
  the same set.
- Built: data rebuilt (4,021 people, 1,408 families, 1,666 media,
  1,083 places), jekyll and verify_site ALL CHECKS PASSED with the
  project baseurl and with none (63,294 internal links each).

## 2026-11-06: the person page's grey film lifted; the tree re-laid on
## d3-flextree and re-interacted

- **The grey screen over the whole person page was the media viewer's
  dimming halo.** When the editor has drawn a Gramps focus rectangle on
  an image, the viewer dims the photo around it with a box-shadow whose
  spread is 9999px - meant to darken the photograph outside the region,
  but .frame did not clip, so the halo painted a grey film over the
  entire page (the header, the tree, everything; I1751 Anna Hrycyna's
  birth record C1805 was the one seen). It had been latent since the
  viewer was written: until the morning's media-base fix every image
  404ed and no figure ever rendered. .frame now carries
  overflow: hidden, the halo stays inside the photograph where it
  belongs, and the region outline keeps drawing.
- **The tree layout now comes from d3-flextree** (WTFPL, the standard
  tidy-tree algorithm - Reingold-Tilford 1981 in van der Ploeg's 2013
  linear-time form - extended to variable node sizes), bundled locally
  like every dependency: the site keeps its zero-CDN rule. The
  hand-rolled layout it replaces could not keep couples from
  overlapping the neighbouring cards (the same page, Anna Hrycyna's
  hourglass, showed Josephus Zieliński's card across hers). The
  genealogy semantics stay in tree.js: upward, every parent is a node
  of its own so both blood lines walk to their depth; downward, the
  spouse sits beside the person and the children hang beneath the
  couple; the hourglass aligns the two tidy trees on the focus row.
  Limits widened to five generations up, four down.
- **The interaction follows the editor's description**: scroll zooms
  the chart (wheel, and pinch on touch; no more Ctrl-only on the
  embedded chart), drag pans, and clicking a card brings that person
  into view and expands their tree around them - re-rooting in place on
  the person page (local state) and through the URL on the tree route
  (the mode rides along in the query). The corner chevron opens the
  person's page. A hint line under the chart says so, in all three
  interface languages (tree_hint in i18n.js).
- One API trap recorded: d3-flextree's layout function wants hierarchy
  nodes - calling it on raw data wraps them halfway and the nodeSize
  accessor then meets a node without .data. layout.hierarchy(data) then
  layout(tree) is the sequence.
- Checked: a headless layout battery over five people in all three
  modes (check_tree_layout.mjs in site/genealogy) - no card overlaps
  anywhere, every link endpoint lands on a card edge; jekyll and
  verify_site ALL CHECKS PASSED with the project baseurl and with none
  (63,294 internal links each); bundle rebuilt (84.7 KB gzipped).
- **Centring corrected the same day** (the editor: on refresh the tree
  did not sit on its person): the view had been centred on the chart's
  bounding box - the middle of everything drawn, not the person - and
  the transform's base shift was left out of the arithmetic besides.
  The layout now reports the focus card's own centre (focusX/focusY,
  base included) and center() aims there; "fit" keeps using the whole
  box. The battery asserts the focus point lies on the focus card and
  inside the chart for every case.
- **The person page, the places pages and the dates, reworked to the
  editor's remarks of 2026-11-06:**
  - the tree's re-rooting made visible: the new focus card pulses
    (a stroke animation for a second and a half), the chart carries a
    caption naming the centred person with their ID, and the corner
    chevron (which opens the person's page) appears on hover with the
    tooltip "Go to the person's page";
  - round avatars for everyone: a male/female placeholder disc (♀/♂ on
    the tinted field) on every tree card and at the head of the person
    page, replaced by the person's actual photograph where the database
    has one (51 people have a picture: a photo- or portrait-named media
    file, person-level or hanging off a citation - a birth record is a
    document about the person, not a picture of them, so documents do
    not serve as portraits); the tree cards carry the portrait as a
    clipped circle;
  - the person's ID sits beside their name in the header (small
    monospace after the name), not as a badge underneath; the sex is a
    bare symbol with no pill and no label;
  - "Partnerships" reads "Spouses and children" (Ehepartner und
    Kinder / Małżonkowie i dzieci);
  - dates standardised: a new lib/dates.js renders the GEDCOM raw texts
    into the interface language - "13 MAR 1905" becomes March 13, 1905,
    13. März 1905, 13 marca 1905; qualifiers speak ("about 1874" /
    etwa / ok.); ranges join with a dash; anything unrecognised falls
    back to the raw text. Parents, siblings, spouses and children show
    their full formatted life dates (the index now carries the raw
    birth and death texts beside the years), as do the timeline, the
    marriage line and the place pages' event lists;
  - the life events timeline includes the person's marriages, divorces
    and annulments (the editor: everything belongs in the timeline),
    each row naming the spouse - "married March 13, 1905 with X" -
    with the link and the spouse's ID; the place of every event stands
    inline in the row beside the date, as with marriages;
  - the media opens: a click on a thumbnail (or Enter on it) opens the
    full image in a lightbox - dark overlay, the display-size
    derivative, caption, Escape or click to close (the thumbnail had
    been inert since the viewer was written);
  - the Places page gained the map of its geocoded places above the
    list, and A–Z navigation buttons (the letters actually present,
    toggle behaviour, All to clear) beside the text filter;
  - the map gained a layer switch - Map (OpenStreetMap) and Satellite
    (Esri World Imagery), both keyless raster tiles - built into
    MapView, so the Places page, the Place pages and the full map route
    all carry it;
  - the place pages speak: event labels are written out (Marriage, not
    MARR; the tags were the database's codes), family events name the
    couple ("Marriage · Joannes Thomas Zieliński & Catharina Hrycyna")
    with links and IDs instead of "family F1326", and the date column
    shows the formatted full date, not just the year.
- Data rebuilt for it: the index carries the raw life dates and the
  portrait pointers (resolved through the media manifest at build
  time), the person shards the family events with the spouse's id and
  name; 4,021 people, 51 portraits. jekyll and verify_site ALL CHECKS
  PASSED with the project baseurl and with none (63,294 internal links
  each); the date formatter exercised headlessly in all three
  languages; the layout battery passes.

## 2026-11-06: tree cards, avatars and the header, refined

- **Long names no longer cut off** (the editor, on Jan Fryderyk
  Zelmer): the card's name line wraps to two lines when needed - SVG
  text does not wrap, so the words are laid by hand (nameLines in
  Tree.svelte) - and a line that would still overflow is compressed to
  the card's text width with SVG's textLength/lengthAdjust, the
  browser's own fitting; a single unbreakable token (a name written
  without spaces) loses its end to an ellipsis. The card grew its
  lines to make room (name at y 14/27 or 21, years at 40, ID at 52).
- **Clicking a person in the tree now opens their page** (the editor's
  preference): the move through the tree is a navigation, not a
  re-layout - the card flash marks the click for a quarter second
  before the page turns, and the mode pills remain the way to re-root
  the chart in place. The corner chevron (which had opened the same
  page) is retired with its plumbing, the click behaviour being
  identical; the hint line says "Click a person to open their page".
- **The placeholder avatar is a silhouette** - a head-and-shoulders
  figure on the tinted disc, drawn once as an SVG snippet and reused -
  instead of the sex symbol; the sex remains on the card border's
  colour and in the header.
- **The person header gains the life dates after the sex symbol** -
  the same formatted life line the relations show (12 MAR 1879 renders
  as March 12, 1879).
- Also repaired on the way: an encoding round-trip through a
  cp1252-decoded write had mojibake'd Tree.svelte's non-ASCII
  characters (… › and friends); detected by listing the file's
  non-ASCII set and reversed by encode-cp1252/decode-utf-8.
- jekyll and verify_site ALL CHECKS PASSED with the project baseurl
  and with none (63,294 internal links each); the layout battery
  passes; the name-fitting checked over the whole index (the 43-char
  longest name renders as two compressed lines, no overflow).

## 2026-11-06: the People page, the big family tree, and the person
## page's relations re-drawn

- **The Surnames page is now People** (nav label in all three
  languages): the surnames stand as collapsible groups - the row
  carries the name, the count and a turning drop-down arrow, the
  click expands the surname's full list; an expand/collapse-all button
  sits above the table. The list columns are Lastname, Firstname(s);
  ID; gender; birth date; death date (the dates formatted).
- **The search sidebar** stands on the right of the People page:
  name, ID, gender (drop-down), birth-year from/to, birth place with
  autocomplete over the database's places, death-year from/to, death
  place with autocomplete, and the event type as a drop-down. Find
  filters the list and opens every group with hits; Clear resets.
  The event-type filter checks each candidate's person shard (lazy,
  batched) for an event of that tag.
- **The big family tree**: the nav gains "Family tree" and the home
  page a start card, both aimed at the start person I2867 - Boguslaus
  Celmer, the oldest-known Zelmer, named so by the editor - whose
  chart opens in a new "big" mode: fourteen generations up, ten down
  (the embedded chart keeps its small radius; the tree route's mode
  pills gain a ⊞ big view). The layout of I2867's big chart measures
  852 cards over a 117,000-px canvas, laid in 6 ms with zero overlaps;
  scroll zooms, drag pans, and clicking a card opens the person.
- **The person page's relations re-drawn** (the editor's remarks):
  - the "In the tree" section and its embedded chart are gone - the
    header's "In the tree" pill was retired earlier; the person page
    reads as a record now, the tree lives on the Family tree page and
    the tree route;
  - the person's name is no longer bold (font-weight 400);
  - every relation row carries a small round avatar - the person's
    picture, or the silhouette placeholder;
  - parents and siblings are one section, "Parents and siblings"
    (Eltern und Geschwister / Rodzice i rodzeństwo): the parents first,
    the couple's marriage (and divorce/annulment, with dates and
    place) named beneath them, the siblings hanging beneath as
    sub-items on an indented rule; a person with siblings but no
    recorded parents keeps a plain Siblings section;
  - parents and siblings show their birth and death places beside
    their dates (the index now carries bp/dp - 1,599 people with a
    recorded birth place, 925 with a death place; index.json grows
    574 to 759 KB);
  - "Spouses and children" delineated: the spouse stands as its own
    row with avatar, life line and the marriage line, and the children
    hang beneath as sub-items on an indented rule - plainly the
    spouse's, not a flat list.
- **The citation images render at display size**: the media viewer's
  default src was the 400-px thumbnail - the record photographs inside
  the opened citations were pixelated (the editor, 2026-11-06). The
  viewer now shows the display derivative by default (the thumbnail
  remains for the index's portrait pointers); the lightbox and the
  region toggle behave as before.
- **Links in the citations are clickable**: a URL inside the source's
  publication string is rendered as a link on the source title (target
  _blank).
- Also fixed: the silhouette placeholder's shoulders arc is clipped to
  its disc now (a per-card clipPath; the arc is deliberately wider
  than the circle, and unclipped it painted outside the round frame).
- Data rebuilt for the index's new fields; jekyll and verify_site ALL
  CHECKS PASSED with the project baseurl and with none (63,294
  internal links each); the layout battery passes; the big chart
  exercised headlessly (852 nodes, zero overlaps, 6 ms).

## 2026-11-06: the face avatars, the relations as cards, and the People
## page refined

- **The avatars are the editor's region-box crops** (1,077 of them):
  the focus rectangles the editor drew on the media references mark the
  person's head, so the media build now crops the avatar square around
  the box's centre (the box's own extent, a 15% margin, 96 px JPEG,
  content-hash name with the `_a` suffix) and writes avatars.json
  beside the manifest; the site build resolves each person's avatar
  through it - the avatar is the face, not the whole scan. Privacy
  holds: living people and the excluded branch are never cropped. Two
  bugs fixed on the way: the region ids come from data.gramps bare
  (I0001) while the GEDCOM xrefs are wrapped (@I0001@), so the first
  pass found no candidates at all; and the index's avatar assignment
  reused a `row` variable that only existed when a photo had been
  chosen, silently writing 43 of 1,077 avatars into other people's
  rows.
- **The relations are cards, without drawing cards** (the editor's
  wording): avatar left, then two lines - name and ID on the first,
  "born March 12, 1879 · Olesko" and "died August 7, 1875 ·
  Angelówka" on the second (the index's bp/dp places ride beside the
  formatted dates). The parents' marriage/divorce lines carry a bullet
  and stand spaced between the parents and the siblings; the siblings
  hang indented from the parents - the vertical bar is gone everywhere
  (parents/siblings, spouses' children, the partnership rows).
- **The tree is back on the person page** under a "Family tree"
  heading - the editor: removing the pills had removed the chart with
  it; the pills live on the tree route only now, the embedded chart
  shows plain.
- **The People page refined**: group names no longer bold (the
  person-page type scale), the counts quiet in parentheses after the
  name instead of a large badge, the drop-down arrow moved to the
  right edge of the row; sort controls beside Expand all (A-Z, Z-A,
  by count with a high/low toggle on re-click); a small column-head
  row (Last name / First name(s) / ID / ♀♂ / Born / Died) opens with
  each expanded group; the main column holds the site's content width
  (58rem) with the sidebar free beyond it to the right; the
  colspan="5"/six-column mismatch that squeezed the expanded tables
  narrower than the surname rows is fixed (colspan 6).
- **The lightbox shows the derivative at its natural size** - the
  editor zooms into record scans to read them; the 96vw cap that
  shrank a 2000-px scan to a third of its pixels is gone (the overlay
  scrolls), and the citation images render at display size from the
  previous round already.
- **Navigation reshaped** (the editor's remarks): "Family tree"
  renamed Tree and moved to second after Home; the Search page
  removed (People's sidebar covers it - the route still answers for
  old links but no nav item carries it); the Map link removed - the
  Places page's map is the map now, rendered full-bleed (wider than
  the content column, edge to edge) and taller; the tree route's
  main column drops its 58rem cap so the big chart spans the page.
- Data rebuilt (1,077 face avatars in the index); jekyll and
  verify_site ALL CHECKS PASSED with the project baseurl and with
  none; the layout battery passes.

## 2026-11-06: the master tree as a window, the expanding card

- **The tree renders in parts now** (the editor: the whole graph at
  once becomes impossibly wide - I2867's chart measured 852 cards over
  a 117,000-px canvas). The chart is a two-generation window: the
  focus's parents and grandparents above, children and grandchildren
  below - I2867's window is 31 cards. The navigation arrows below the
  chart ("↑ ancestors" / "↓ descendants", shown only when more tree
  exists beyond the window - hasMoreUp/hasMoreDown in tree.js) slide
  the window one generation: the next step renders while the far row
  derenders, the layout recomputed from the new focus. Clicking a card
  no longer navigates (that took the user away from the master view
  unexpectedly); the mode pills on the tree route re-root by URL, and
  the detail panel's "Centre the tree here" re-roots in place.
- **The card expands in place**: a click opens a detail panel over the
  viewport at the card's screen position - avatar, name, ID, born
  date + place, died date + place, the privacy note for the living -
  with two actions: "Go to the person's page →" and "Centre the tree
  here". It closes on its ×, a second click on the card, or when
  another card opens (the panel rides the current transform, so it
  stays on its card while you pan - and is recomputed from the chart
  on any re-layout). The HTML panel sits over the SVG (positioned from
  the chart coordinates through the current pan and zoom), which keeps
  the text selectable and the layout in CSS rather than foreignObject.
- The layout battery now asserts the window radius (no card further
  than the window's rows from the focus) alongside the overlap, link
  and focus checks; the arrow booleans exercised per person (I2867:
  down only - his ancestors stop with him; I0003/I0007/I3131: up).
- jekyll and verify_site ALL CHECKS PASSED with the project baseurl
  and with none (63,294 internal links each).

## 2026-11-06: the avatars corrected to photos only; the person page
## and the tree fixed

- **The avatars were mostly crops of handwriting** (the editor caught
  it: "you appear to have just taken whatever image is in a person's
  folder" - I1706's avatar was a slice of his population register): the
  region boxes on record scans mark where the person's *name sits on
  the form*, not their face, so 1,037 of the 1,077 avatar crops were
  meaningless slivers of documents. The media build now crops an avatar
  only from photo/portrait-named media - a drawn region crops the face
  (40 people), a photo without one centre-crops square on the whole
  picture (12 more, e.g. I0076's obituary photo); everyone else wears
  the silhouette, as it should be. 51 avatars in the rebuilt index;
  repo B republished.
- **The indentation that wasn't**: `ul.people { margin: 0 }` stood
  after `ul.kids { margin-left: 2.4rem }` in the style block and, at
  equal specificity with Svelte's scoping preserved, zeroed the
  sub-groups' indent - the siblings under parents and children under
  spouses had rendered flush. The relation rules now carry two classes
  each (ul.people.kids) so they win on specificity, not order.
- The embedded family tree on the person page grew taller
  (max-height 26rem to 34rem).
- **The alternative names are their own line under the header** - the
  GEDCOM's second NAME records ("birth: Gottlieb Celmer" on I1706)
  had worn pills that read as nonsense; the pill is gone, the line
  quiet beneath the name/ID (altname in Person.svelte), the type word
  kept where the record gives one.
- jekyll and verify_site ALL CHECKS PASSED with the project baseurl
  and with none; the layout battery passes.

## 2026-11-06: the tree page sized, the couple links landing true

- **The Tree page's chart is a window on the page**: 80% of the
  window's width and 80% of the viewport's height, centred (the
  editor's measure); the embedded chart on the person pages keeps its
  own size.
- **Opening a card centres the view on it** - the panel opened at the
  viewport's edge was cut off; the click now also pans so the card
  sits mid-viewport.
- **The expanded card renders inside the chart** (a foreignObject at
  the card's chart coordinates) instead of an HTML overlay positioned
  by the current transform: it pans and zooms with the tree like every
  other piece, which is what the editor asked for. The pointer handler
  stands down for presses inside the panel so its links and buttons
  survive the pointer capture (the Firefox lesson again).
- **The couple links land on the blood person's card** (the editor's
  screenshot: the line into Krystyna Celmer and Bogusław Stark landed
  between the spouses, unreadable as to who married in): the endpoint
  shifts from the block's centre to the blood card's centre by
  (w·CELL − CARD_W)/2 where the node renders a spouse - computed for
  the child side and the parent side of every descendant link, and for
  the focus row's upward links (whose spouse the ancestor tree's own
  nodes do not know about). Verified on I2889: both the link in from
  her parents and the links out to her children start and end at her
  card's centre, x = −91 in chart units.
- jekyll and verify_site ALL CHECKS PASSED with the project baseurl
  and with none; the layout battery passes.

## 2026-11-06: the deploy step given time to breathe

- **The Pages backend slowed and the deploy action's own timeout gave
  up**: the deploy for the tree-page round (cecfe0a5c) failed four
  times in a row at `actions/deploy-pages@v4` - the run, two
  `gh run rerun --failed` attempts, and a fresh empty-commit head -
  each dying with "Timeout reached, aborting!" while polling the
  deployment status. The logs told the story: the first attempts polled
  an *empty* status for five minutes, but the fresh head reached
  `syncing_files` - real progress - and was cancelled by the action's
  5-minute default anyway. The fix was patience: the action's `timeout`
  input now allows 20 minutes (pages.yml), and the next deploy passed.
  Rerunning a failed deploy was the wrong lever here; reading the log
  first found it.
- The tree-page work rode out unchanged on the successful deploy and
  was verified live: 80vw/80vh viewport, foreignObject detail panel,
  the couple-link shift formula, the altname line, the back link, the
  two-classed indentation rules - all present in the served CSS/JS.

## 2026-11-06: the People list on a phone

- **The six-column list scrolls sideways on a narrow screen instead of
  overflowing it**: the table sits in a `.tscroll` wrapper
  (`overflow-x: auto`, momentum scrolling on iOS) - the ID column
  never hides to make it fit, the Gramps id appearing wherever a
  person does being the editor's standing ruling, so the phone pays
  with a swipe rather than the data with its absence.
- **The Tree page's frame height follows the small viewport**
  (`80svh`, the plain `80vh` standing first for older browsers): a
  phone's URL bar collapsing and expanding no longer jitters the chart
  frame, which otherwise breathed every time the bar hid.
- Everything else the mobile audit found was already in place from
  earlier rounds - the correct viewport meta, touch-first tree (drag
  pans, two-finger pinch zooms, taps distinguished from drags by the
  6px travel threshold, `touch-action: none`), the header nav dropping
  to its own row below 640px, the search sidebar stacking under the
  list below 900px, and wrapping flex/auto-fit grids on the person and
  home pages.
- jekyll and verify_site ALL CHECKS PASSED with the project baseurl
  and with none; the layout battery passes.

## 2026-11-07: the empty big tree found and fixed

- **The big tree loaded with nothing in it** (the editor, this
  morning): the chart SVG is sized to the whole layout (the I2867
  window is 8,630×296), and an SVG clips its children to its own box
  by default. The load-time centring translates the focus to the
  middle of the *viewport div* - with the div now 80vh tall, that
  landing point (y≈308) sat below the SVG's own 296px bottom edge, so
  every card was clipped away and the frame showed tan emptiness. The
  old content-sized viewport had accidentally kept the landing point
  inside the box; the explicit height exposed the design's hidden
  assumption. The fix is the standard pan/zoom setup: `overflow:
  visible` on the SVG - the viewport div's `overflow: hidden` is the
  one clip that matters - and the transform is now free to carry cards
  anywhere in the frame (the foreignObject detail panel included, which
  the same clip would have cut when panned below the chart).
- The frame is **70svh** tall now (the plain 70vh standing first for
  older browsers), the editor's measure.
- **Centring on load is guaranteed**: the effect that centres the
  focus retries on the next animation frame when the viewport has no
  layout yet (the data can arrive before the CSS has sized the frame),
  which previously would have silently left the view at the origin.
- Verified with headless Edge screenshots against the local build: the
  tree route shows the hourglass centred on Boguslaus Celmer at
  desktop and phone widths; the person-page embed still centres on its
  person. jekyll and verify_site ALL CHECKS PASSED with the project
  baseurl and with none; the layout battery passes.

## 2026-11-07: the tree page dressed, the fit button honest

- **The page has its title** - "Tree view" (Baumansicht, Widok
  drzewa) above the chart on the tree route; the person-page embed
  keeps its "Family tree" heading.
- **Everything the tree owns is edge-aligned**: title, mode buttons,
  chart frame, navigation arrows and hint text sit in one 80vw column
  (`.treewrap.route`), so the buttons no longer ran past the chart's
  edges - they had spanned the full page width while the frame was
  80vw centred.
- **The fit button fits.** It scaled the chart to the frame but clamped
  the result at the 0.3 interactive-zoom floor - on a wide chart that
  left the chart larger than the frame and the button looked like it
  only centred (the editor's suspicion was right). Fit now computes its
  scale without the floor (the interactive floor drops to 0.05 so the
  fitted scale is not snapped back), and a new **⌖ button returns to
  the focus person at reading size** after a fit. Both carry tooltips.
- jekyll and verify_site ALL CHECKS PASSED with the project baseurl
  and with none; the layout battery passes; verified with a headless
  Edge screenshot of the aligned page.

## 2026-11-07: the branches open on demand

- **The tree no longer sprawls.** The window had rendered every child
  and every grandchild side by side, each married person a full couple
  block - the widest descendant windows in the data measured 21 screen
  widths (I0272 Christina Ubel: 23,437 px), and zooming out to take it
  in made every card unreadable. The editor chose the proposal: the
  chart now shows the ancestors (two generations) and the **children**
  - and the grandchildren wait behind a **"+n" badge** on each child's
  card. Clicking a badge opens that branch in place (the chart re-lays
  out and recentres on the focus); clicking again closes it; and
  **opening a second branch collapses the first** (the editor's
  choice), so the open width is bounded - the widest opened branch in
  the battery measures about five screens, at reading size and
  pannable, against twenty-one at census zoom.
- **A spouse card renders only where the couple's children show** -
  the focus row and open branches; a hidden branch's couple is one
  card, the marriage still documented on the person page.
- **Deeper walking stays possible**: a grandchild in an opened branch
  wears its own +badge, and opening it keeps its ancestors on the path
  open (descendantPath computes the focus-to-leaf chain). The
  navigation arrows keep their roles - up beyond the grandparents,
  down now counting one generation beyond the children row.
- The badges are part of the press-detection scheme (the badge is
  read at pointerdown, acted on at pointerup under the 6px travel
  rule), so a drag never fires one and the Firefox pointer-capture
  lesson applies to them as to the cards.
- The layout battery grew the expansion cases: open a branch, open a
  second (first collapses), open a grandchild's branch beneath an open
  one - no overlaps, no dangling links, the branch really renders, the
  width bounded. All pass; jekyll and verify_site ALL CHECKS PASSED
  with the project baseurl and with none; verified with a headless
  Edge screenshot of I0272's default view fitting one frame.

## 2026-11-07: the badge click keeps the view; the tree moves slowly

- **Expanding or closing a branch no longer moves the viewport** (the
  editor, panned away from the key person, a badge click kept snapping
  the view back): the centring effect had watched the expansion state
  among its keys, so every toggle re-ran the centring. It now watches
  only the focus and the mode - the pan and zoom stay exactly where
  the reader left them; the branch grows or shrinks around the current
  view. (Opening a detail panel still centres on the card - that is a
  deliberate act, not a layout change.)
- **The tree moves in plain sight**: the cards, the marriage lines,
  the links and the open detail panel glide to their new places over
  half a second (CSS transitions on the transform) instead of
  teleporting. The DOM nodes are now keyed by the person (a row letter
  distinguishing the hourglass halves), so a card keeps its element
  across a re-layout and the browser can interpolate; the marriage
  lines became origin-anchored groups (they are always one gap long)
  so they animate the same way; the link paths morph through the CSS
  d property where the browser supports it, standing on their
  attribute where it does not.
- jekyll and verify_site ALL CHECKS PASSED with the project baseurl
  and with none; the layout battery passes; the rendered chart
  verified unchanged with a headless Edge screenshot.

## 2026-11-07: the badge on its own line

- **The +n badge moved out of the card** (the editor: it sat on top of
  the names): it is now its own line **below the card, right-aligned
  to the block's right edge** - under the spouse card when the person
  has one drawn beside them - so no name, year or id ever sits under
  it. It still reads +n to open, − to close, and the press-detection
  treats it as before.

## 2026-11-07: the frozen view kept; the places list organised

- **The badge click now truly keeps the view** (the editor: what is
  under the mouse should still be the button just clicked): freezing
  the transform alone was not enough, because a re-layout recomputes
  the chart's coordinate base (baseX/baseY) and every card's position,
  so the content under a stationary transform shifted. Toggling a
  branch now anchors the clicked badge: its viewport position is
  recorded before the toggle, the recomputed chart is re-read
  synchronously, and the transform is set so the same badge lands
  exactly where it was - the branch grows or shrinks around a frozen
  view, no flash in between.
- **The Places list is separated into letters**: a quiet accent-weighted
  subheader row opens each letter's block inside the table (the same
  pattern as the People page's surname groups).
- **Returning from a place page lands where the reader left**: the
  scroll position is saved when a place is opened (sessionStorage) and
  restored once the list has rendered; the saved position is consumed
  on the return, so a fresh visit from the nav still starts at the
  top. Private modes that refuse storage just land high.
- **The unexplained green dot is gone**: the ◦ pill that marked
  geocoded places carried no meaning a reader could know (the count in
  the toolbar still states how many places are geocoded), so the
  column went with it.
- **The place page gained an "Events" sub-header** (Ereignisse,
  Wydarzenia) before the date list, and the map now has breathing room
  after it (the events table began flush against the map's bottom
  edge).
- jekyll and verify_site ALL CHECKS PASSED with the project baseurl
  and with none; the layout battery passes; all three pages verified
  with headless Edge screenshots.

## 2026-11-07: one slow beat for the whole branch change; the dot explained

- **Newly revealed cards and links now fade in over the same slow beat
  the cards glide on** (the editor: the row underneath/above
  materialised instantly, and the user might get confused): the card
  and link elements are keyed (links now carry their identity - a row
  letter and the parent>child pair - from the layout), so Svelte can
  run enter and exit fades on exactly the elements a branch change
  adds or removes, while the surviving elements keep their glide. The
  whole choreography slowed to 0.8 s, transforms and fades alike.
- **The geolocated mark is back on the Places list, self-explained**:
  a plain round green dot in its own column before the place name (no
  pill), and a legend beside the filter at the top of the page -
  "● = geolocated place" (Ort mit Koordinaten, miejsce zlokalizowane).
- jekyll and verify_site ALL CHECKS PASSED with the project baseurl
  and with none; the layout battery passes; both pages verified with
  headless Edge screenshots.

## 2026-11-07: the surnames in letters

- **The People page's surname list wears the same letter subheaders**
  as the Places list: a quiet accent-weighted row opens each letter's
  block of surname groups. The subheaders appear only in the A-Z
  order - sorted by count or reversed, the letters would interleave
  and the header would lie - so the other orders keep the plain
  flowing list.
- **The Find People sidebar starts below the page's title**: the
  "Surnames" h1 moved outside the two-column layout, so the sidebar
  no longer floated up beside it.
- jekyll and verify_site ALL CHECKS PASSED with the project baseurl
  and with none; the layout battery passes; verified with a headless
  Edge screenshot.

## 2026-11-06: the way home in the explorer's navbar

- The navbar carries a "← Traces in the Sand" link after the app's own
  tabs (accent-weighted, so it reads as a way out, not a section). The
  target is computed from the document URL - two levels up from the
  app's directory - not hard-coded, the same prefix-independence the
  rest of the shell already observes (an absolute path here would have
  been this explorer's first bug once more).
- **The tree's clicks were swallowed by the pan's pointer capture** (the
  editor: clicking others in the tree does nothing). The viewport
  captures the pointer when a press starts - setPointerCapture is what
  keeps a drag tracking outside the viewport - and a captured pointer
  retargets every later pointer event to the viewport. The first fix
  moved the handlers to click - which per the Pointer Events spec is
  retargeted to the capture element as well (it is a compatibility
  mouse event derived from the captured pointerdown/up), so Firefox
  swallowed it too and the editor reported the clicks still dead. The
  working design hangs no interaction on the cards at all: the viewport
  reads, at pointerdown, which card the press landed on (data-pid
  attributes on the card groups, found with closest) and whether it was
  the corner chevron; at pointerup, if the pointer travelled under 6px,
  the recorded card's action runs - re-root-and-centre, or open the
  person page. A drag cancels the press (6px threshold), a second
  finger cancels it (pinch), pointercancel cancels it. Each card now
  carries its own hit rect, so the spouse card is its own click target
  instead of being covered by the couple's shared one.





- The starred readings' note shows at once (2026-11-06, the editor's
  question: the help cursor appeared but the note did nothing): the note
  rode on the browser's native title tooltip, which Windows shows only
  after a second or more of rest - a quick hover read as doing nothing.
  The note is now the page's own tooltip, drawn the moment the pointer
  (or a keyboard focus) reaches the name, and a line under the table
  explains the asterisk itself in both languages: it marks a reading the
  sources leave in doubt, the reasoned-but-unsettled normalisations
  among them. jekyll and verify_site ALL CHECKS PASSED, the browser
  checks re-run (47/47, the hover and the explanation line among them).

- The Pełzucki 1896 plan overlays a satellite image (2026-11-06, the
  editor's ask: "an overlay on a satellite image instead of a vector map,
  and include the farm labels"): scratch/map4456/sat_overlay.html, built
  by build_sat_overlay.py, is the tiles repository's warp test
  (warp.html, the Allmaps warp over OpenStreetMap) with the base changed
  to Esri World Imagery and the 101 farmstead labels of farms.yml laid
  over it - each mark's mosaic pixel carried to lat/lon by the map's own
  order-1 fit (re-derived from georef.yml's control points; the fit block
  carries no coefficients), the fit's RMS 2.71 m standing in the page's
  note. The pills keep the site's farm layer's shape and naming rule
  (the normalised spelling where the editor's reading is firm, the
  transliteration where it is conjectural; the 1896 extent on hover).
  A working page first (this morning's commit); **published at the
  editor's word the same day** ("Publish! Looks great."): the builder
  moved into the pipeline (pipeline/maps/sat_overlay.py <map>; a map
  needs farms.yml, and a rebuild after every import_farms.py bakes the
  marks anew), the page lives in the tiles repository beside the map's
  tiles (pelzucki1896/sat_overlay.html, its annotation fetched
  relatively, the way warp.html does), and the map's page links it
  beside the OSM overlay (map_over_sat in i18n, both languages;
  map_pages.py writes sat_warp when the page exists). The headless check
  (check_sat_overlay.py) now serves the tiles repository and loads the
  page as its Pages will, counting the 101 pills and keeping the
  screenshot; jekyll and verify_site ALL CHECKS PASSED.

## 2026-11-06: twenty maps brought in at once - the bulk batch

- The editor supplied the full list of maps to add ("Treat this as one at a
  time, I'm just providing you with the full list of maps to add. The
  difference is that I'm asking to do the labelling as a bulk exercise at the
  end") - twenty maps through steps 1-5 of docs/ADDING_A_MAP.md on the branch
  `maps-bulk-2026-11`: the register's full entries (nineteen short entries
  filled, two new keys `mapadrogi1890` and `bildplan1944`), the tiles cut into
  triebenfeld-maps, the control points fetched and fitted, the labelling pages
  built for the editor's bulk marking session.
- Rulings taken in chat before the work: the Mapa dróg map whole (the batch's
  exception: the editor marks its labels with the form left empty and the
  Polish standard in its place; Claude's OCR of the marked crops fills the
  Russian as written afterwards); the fotomapa added with its source open;
  the four date questions (Blaeu 1664/1665, Pambo 1801/1803, Hollring
  1804/1805, Krolikow 1800/1800-1815) kept as the register has them and
  flagged for review; Reymann = the Peisern sheet (its own name says ca.
  1850 - flagged); Nowy Trabczyn = 001 only; Zagorow 1841 = the north-up
  rotated image as the map of record, 002 ignored; von Pfau = the full
  sheet, the editor's own _crop.jpg ignored.
- The pipeline grew three ways (docs/ADDING_A_MAP.md carries them): the
  labelling page takes the register's `crop` (the viewer shows the cropped
  image, the marks are stored in the original's pixels; the first cropped
  maps are perthees1798, with the crop computed from the gazetteer's padded
  window through the MapWarper points' affine - scratch/maps_bulk/
  crop_windows.py); mapwarper_fit takes the anisotropic [sx, tx, sy, ty]
  (Richter 1843: the editor's points are on the two trimmed PNGs, whose
  pixel grid is stretched ~1.1% in y against the composite, the fit found by
  FFT patch correlation with a self-match check first - scratch/maps_bulk/
  richter_fit.py; the Sek.-III points (83752) appended by hand as from: hand
  rows, which the re-fetch keeps); tiles.py takes a per-map tile_quality
  (78 for the six largest sets; the viewer alone - the crops are cut from
  the original), which kept triebenfeld-maps at 860 MB inside GitHub Pages'
  1 GB.
- Fits (order 1, RMS): pambo1803 1.4 m, weydner1804 0.0, hollring1804 0.0,
  pelzucki1901 6.3, zagorow1841 23.0, krolikow1800 41.2, slupca1957 37.6,
  trojwiorstowki1914 187.9, perthees1798 314.2, richter1843 423.6 (16
  points, outlier mw759848 at 844 m - flagged). gilly1802's georeferencing
  deferred: the MapWarper upload (83446) matches neither file on J: and BII
  matches neither img_65802 nor the warped tiles at any scale or turn
  (scratch/maps_bulk/gilly_fit.py, gilly_bii_scan.py) - the two files appear
  to be different maps; the editor to say which is the map. messtischblatt
  1940, mapadrogi1890, bildplan1944, ams1962, blaeu1665, vonpfau1770,
  trabczyn1790, zagorowo1799, reymann1834 have no points: they are
  georeferenced from the editor's marks (MAPS_PLAN, section 5).
- NEEDS_CONFIRMATION carries the batch's open questions (the four dates, the
  two proposed short forms, Gilly's files, the Reymann year, the left-out
  second files, the unconfirmed orientations); MISSING_SOURCES carries the
  Bildplan's open source. in_project stays false everywhere until the marks
  are imported (map_pages.py needs labels.yml).
- The same sitting, the editor's rulings by return: the four dates settled
  from the editor's bibliographic references (Blaeu ca. 1664, Pambo 1801
  "after Pambo", Hollring 1805, Królików 1800-1815 — the `year:` fields
  carry them, the slugs and short forms keep the register's years, because
  the gazetteer cites those forms and the parser matches them); Gilly
  georeferenced without MapWarper at the editor's word (the 83446 reference
  was a different version): BII.jpg correlated against the warped tiles of
  MapWarper 63625 (the same cartography, served openly, exact Web-Mercator
  geometry) with a JOINT scale-and-rotation search — BII's meridian is
  tilted ~16 deg, which is why every translation-only search (against 83446,
  against img_65802) had found nothing; 43 synthetic control points,
  affine RMS 132 m, the fit's RMS 165 m (scratch/maps_bulk/gilly63625.py,
  gilly63625_fine.py; georef.yml `from: synthetic`). The batch's labelling
  index (a table of the twenty sheets with links, statuses and the notes to
  address — the Richter mw759848 reminder among them) is built by
  scratch/maps_bulk/build_index.py to review/maps/index.html, served at the
  server root (http://localhost:8780/).
- The warp viewer's base map is switchable (the editor's request of the same
  sitting): OpenStreetMap or Esri World Imagery satellite, the buttons in
  the bar, `?base=satellite` opening on the satellite; the labelling
  index's Overlay column links both (takaji10.github.io/triebenfeld-maps/
  warp.html?map=<key>[&base=satellite]), shown only where a georeference
  exists — the maps without points yet show "with the georef" until their
  marks georeference them.
- The labelling page's editing finished at the editor's two reports of the
  marking session (the name that would not come back; the type that could
  not be changed): Enter commits an existing label's edit and releases it,
  a click on empty map space releases the selection, Esc does the same when
  nothing is in progress; the type the gazetteer filled in is overridden by
  the type buttons now standing in the auto-fill pause (a click keeps the
  pause, the form still to be typed), by a type key pressed in the EMPTY
  form field, and by a type key on a selected saved label — the help carries
  the whole workflow. All 23 sheets rebuilt.
- Polish letters without a layout switch (the editor's request of the same
  sitting): the form and note fields take Right Alt/AltGr + a letter as its
  Polish form (a→ą, c→ć, e→ę, l→ł, n→ń, o→ó, s→ś, x→ź, z→ż, Shift for the
  capital — the Polish-programmer keyboard's own mapping), and a row of
  letter buttons under the form field inserts at the cursor without taking
  the focus. Plain letters always type as themselves (the mapping runs only
  under the held modifier), so a form as written without diacritics stays
  as written. RETIRED the same sitting at the editor's clarification: the
  want was accent-insensitive matching (typing Trabczyn finds Trąbczyn),
  not letter insertion — the buttons and the AltGr mapping are off the
  page.
- **The Drzewce NMP entry re-read from the editor's page image**
  (2026-11-06): the editor's question (is Nazwy miejscowe Polski in the
  edition? — yes: literature/nmpol, the 23 cited entries, visible: false,
  no site page) led to the root cause of the gazetteer's garbled forms —
  the OCR'd citation text itself, whose special characters (ḑ, ž, ṽ, ḱ) had
  defeated the three-witness pass. The editor's page image of vol. 2,
  p. 443 (the locator p. 444 was a page off) settled it: Drzevvyc7a was
  **Drzewycza** (1418, AC II nr 117) and VCe was **Drzewce** (1881,
  SG II 182); the citation text in original.md re-read, english.md's
  summary corrected, the gazetteer's two forms restored with the true
  readings, footnote 16's locator corrected and its note carrying the
  record. The dialect line is Claude's best reading, flagged for the
  editor's confirmation; the other 22 NMP locators may carry the same page
  shift (NEEDS_CONFIRMATION); and the garble-class scan over the
  gazetteer's forms found one more suspect: czarnybrod's "CzanlY Bród"
  (1921), flagged, not corrected.
- **czarnybrod's "CzanlY Bród" settled at the editor's word (2026-11-06):
  Czarny Bród** (1921, Sk II 36). The same garble sat in the edition's own
  NMP citation text (original.md, t. 2, p. 197) — corrected there too,
  with the entry's dialect line
  ("gw. corny brut, - ygo -du, cornobrocKi.") re-read as
  "gw. czorny brut, -ygo -du, czornobrodzki." (the same n/l and dropped
  dz artifacts; **the dialect line is Claude's read, for the editor's
  confirmation against the source when next at hand** — the page image is
  not here).
- **Mapa dróg 1890 marked, OCR'd and georeferenced** (2026-11-06): the
  editor's 37 labels imported (35 gazetteer places and two new places,
  Stara Huta and Świątniki, waiting on the editor's entries); the batch's
  exception worked as agreed — the editor's Polish standards kept verbatim
  in `form_standard:`, Claude's OCR of the crops filling the Russian as
  written into `form:` (25 high, 11 medium, one low flagged: Скукумъ for
  Skokum; the method in maps/mapadrogi1890/notes.md — the crops read by
  Claude directly, the lunaroute converter unable to reach localhost and
  no Russian Tesseract installed), the gazetteer's appearances carrying
  the Russian. The marking exposed that the marked places had no
  `surveyed` coordinates: the plan's section-6 OSM lookups ran (34 places
  confirmed; the two described entries lazinskie-oledry and budy taking
  OSM's matching points, the choices in NEEDS_CONFIRMATION), every written
  coordinate carrying `location.check`; and the fit from the marks alone
  closed at RMS 830 m over 35 points (the class of a schematic roads map;
  three outliers flagged). `in_project: true`; the map's warp is live at
  takaji10.github.io/triebenfeld-maps/warp.html?map=mapadrogi1890. The
  mark-only fit path (georef.yml created empty, the marks as mk-* rows) is
  now written into docs/ADDING_A_MAP.md step 7.
- The evening's rulings and markings (2026-11-06): the editor's two OCR
  corrections (Скукумъ → Скокумъ, Тромчинъ → Тромбчинъ — the б noting the
  two maps' shared transliteration); pelzucki1901 imported (3 labels, the
  Russian forms read — Тромбчинъ, Тромбчинъ Г, Тромбчинъ Ф), fitted at RMS
  42.7 m (one residual flagged: the Trąbczyn mark at 130 m), in_project:
  true; and zagorow1841 re-backed on 001.jpg at the editor's word (the map
  as drawn) — the rotated derivative proved a different version from
  001.jpg (five probes: whole-image template match, patch NCC at the SIFT
  consensus's positions, a rotated-canvas template match, a per-GCP patch
  search over the whole original at all angles and scales, and the SIFT
  lattice's own GCP test landing in white margin), so the MapWarper 75688
  points are off the record, the tiles were re-cut, the stale annotation
  removed, and the map georeferences from the editor's marks alone once
  they mark it. WORKING_NOTES carries the lattice-consensus lesson (SIFT's
  inlier count proves nothing about photometric correspondence; verify with
  patch NCC; suspect the VERSION when rotation is right and phase is
  wrong).

## 2026-11-06: the Łukom 1766 re-backing — the map of record changed to the archive's JPG, and the site's Sources-page icons

- **Łukom 1766's map of record changed to the archive's JPG as drawn**
  (`1_407_0_0_283-29_0001.jpg`, 8,808 × 7,052; the editor's word: use it,
  "not the rotated image"; "if that means I need to redo the labels, I
  can"). The former record — the editor's north-up PNG they had
  georeferenced on MapWarper 75552 — proved a DIFFERENT RASTER, not a
  transform of the JPG: the full probe ladder failed photometric
  verification at every rung (a SIFT full-affine lattice consensus at
  171.2° with patch NCC 0.077, the Zagórów signature; whole-image rot180
  peaks that were the two white margins correlating, content-only 0.088;
  anisotropic rescale 0.066; centred unscaled paste 0.11; a local
  discrepancy grid with 5 weak patches and no consistent offset; the five
  GCP patches swept over all of the JPG at 72 angles × 3 scales with no
  consistent angle or position, all NCC ≤ 0.46; all 8 dihedral
  orientations under 0.09). The eleven marks of 2026-10-23 cannot carry
  over: the PNG-era labels.yml, positions.yml and georef.yml are archived
  in `maps/lukom1766/png-record/`, the register's `mapwarper` field is gone
  (those points are in the PNG's pixels), the eleven crops cut from the PNG
  are deleted, and the gazetteer's lukom1766 appearances had their label
  links cleared (the forms and notes stay — the readings of 2026-10-23
  stand). The register: original → the JPG, orientation south-up kept (the
  map is drawn south-up), `view_rotation` 180 → 0 (the JPG's lettering
  reads upright as drawn; the editor: the page shows the labels right side
  up), `in_project: false` until the re-marking. The tiles re-cut (346
  files, 14.9 MB) and live; georef.json removed; the map will georeference
  from the editor's marks alone (empty georef.yml, the mark-only path like
  zagorow1841) once they mark it; the labelling page serves the JPG
  (10 to find).
- **The sweep's own lesson**: its first run returned NCC 0.000 for every
  GCP because its fft_ncc copy lacked the float32 casts of the working
  version — with uint8 input the img*img integral overflowed, the local
  variance went negative everywhere and the low-variance guard zeroed the
  whole output; the self-match check (a template from the search image
  must return ~1.0) distinguishes a broken correlator from a negative
  result.
- **Maps left the top navbar** (the editor: it is on the Sources page
  already): the nav link and the i18n.yml keys (en, de) removed.
- **The Sources page's four kinds carry vector icons** (the editor's
  request: parchment, newspaper, book, map): a new partial
  `site/_includes/sources-icon.html` draws them in the site's line-icon
  idiom (fill none, stroke currentColor 1.1, round caps and joins, as in
  source-thumb.html); each kind's heading includes it, and the page's
  styles size it. The geometry rendered and checked before committing
  (scratch/maps_bulk/sources_icons_check.html).

## 2026-11-07: the mobile-readiness re-check of the whole site (genealogy excluded)

- **The site is mobile-clean at 390, 360 and 320 px**: all 2,490 built
  pages crawled (puppeteer-core + Edge, 6 in parallel, ~4 minutes per
  width) — zero horizontal overflow at 390 and 360; at 320 exactly one
  defect, the German Pełzucki 1896 map page (15 px). Root cause:
  `.map-tools` (the map toolbar flex row) did not wrap, and the German
  overlay link "Kartenüberlagerung auf OpenStreetMap ansehen" was squeezed
  to its min-content, pushing the row's total min-content past the
  viewport — the English page passed because its text is shorter (the
  2026-11-01 nowrap trap in a new dress: not nowrap on the link, but a
  non-wrapping flex row whose item floor is the longest word). Fix:
  `flex-wrap: wrap` on `.map-tools`; re-crawl clean at all three widths;
  the wrapped toolbar visually checked at 320 (two deliberate lines, the
  link on its own).
- The crawler's three error lines (a navigation race, a null
  documentElement) re-checked individually — all clean at all widths;
  crawler errors are noise to re-run, never findings. The overflow
  report's own offender list pointed at the farm table, but that table's
  wrap clips correctly (a clipped descendant still reports its full
  layout rect); the real extender was found by listing only elements
  outside every clipping container — its right edge matched
  `scrollWidth` exactly. Screenshots of the representative page types at
  390 (home, sources, letter, places, literature, map) show no visual
  defect: the navbar wraps, cards stack, the letter viewer adapts, the
  Sources icons render beside their headings.
- **The check became pipeline** (the editor's word: "New map pages will be
  added in the future, so can you add to whatever pipeline/process to
  ensure that they build correctly for mobile?"):
  `pipeline/mobile_check.py` with `pipeline/mobile_check/crawl.js` lives
  in the repository now (the temp-folder crawler would have died with the
  session). Run after a map's pages are built — `python
  pipeline/mobile_check.py --map <key>` is ADDING_A_MAP step 9 — or with
  `--pages` (list or file) or `--all` (every built page, the genealogy
  section excluded). It starts its own server on a free port, measures at
  390/360/320 in the machine's Edge, retries the two known crawler races
  internally, and names only the elements outside every clipping container
  that push the page past the viewport (the real extenders). Exit 1 on any
  overflow. Proven: the five map pages pass; a planted overflowing
  self-test page fails with exit 1 and the right offender; `--all`
  re-confirmed 0 overflows on 2,490 pages at 320. Needs node on PATH;
  puppeteer-core installs into a persistent cache under the system temp,
  never into the repository.

## 2026-11-07: the Timeline rebuilt — the eras and the timeline are one page, the era pages born, the story page retired

- **The editor's design** (their brief, questions asked first): one Timeline
  page where the eras are introduced — one narrative paragraph each, a Read
  more link to a proper era page with a much more detailed description
  quoting its sources inline — and under each a brief timeline of the events
  relevant to Trąbczyn (primary) and Zagórów (secondary). The timelines
  rebuilt completely: no document counts, no skips between years, 1-2
  compact sources for further reading per event. The story page removed
  (the home page keeps its brief introduction; the nav's first item, renamed
  Introduction, points there). English first, German after approval. Era
  pages at /eras/<slug>/; the eras.yml blurbs rewritten for the page (the
  originals stay in the register).
- **site/_data/timeline.yml rebuilt** from 102 events to 69, a new schema:
  `era` per event (editorial, like the documents'), `when` display date, a
  concise note, and `sources` of text+url linked to the edition's own
  document, literature and newspaper pages. Dropped by the importance rule:
  the Ląd-internal events (1362, 1447, 1461 — the editor's own examples),
  the purely personal, and the procedural sub-steps (their substance lives
  in the era pages). Added: the twentieth century's four events (the 1911
  parceling of Włodzimierow, Breyer's visits of 1935 and 1936, the 1940
  Drommin renaming). The German event notes are gone with the rewrite and
  fall back to English until the German pass.
- **The Timeline page** (timeline.html include rewritten): per era the
  label, the holder line, the intro paragraph (new `intro_en` field in
  reference/eras.yml; German falls back to the editor's blurb_de), the Read
  more link driven by new `page_en`/`page_de` flags, the events
  (era-events.html, shared with the era pages), and the standing link to
  the era's documents on the browse page.
- **Seven era pages** at /eras/<slug>/ (and the German hohenlohe page moved
  to /de/epochen/hohenlohe/): six written new in the story page's narrative
  voice with inline source links and glossary links; the Hohenlohe page
  moved from /hohenlohe/ with its stale pointers fixed and the events block
  added. Each foot carries the era's events and its documents link.
- **Redirects, no plugins**: a `redirect` layout (meta refresh, canonical,
  location.replace); /the-story/ and /de/die-geschichte/ → the home pages,
  /eras/ and /de/epochen/ → the Timeline, /hohenlohe/ and /de/hohenlohe/ →
  the era pages' new addresses. The navbar reordered (Introduction,
  Timeline, Sources, People, Places, Genealogy, Glossary, About) with the
  i18n nav keys updated in both languages; about.md and de/ueber.md point
  at the Timeline; urls.html lost u_story and u_eras.
- **Verified**: build_site_data passes again (it had been failing on main —
  the correspondent entry for Tadeusz Kościuszko, sender of the Ossolineum
  copy collection's letter, was missing from reference/correspondents.yml;
  added with the title the documents and the people bio give);
  gazetteer --check passes; Jekyll builds; verify_site passes (its era
  check retargeted to /timeline/); the mobile check passes on all eleven
  new and redirected pages; the Timeline and an era page checked by eye in
  screenshots.
- **Open**: the German pass (intro paragraphs, six era-page mirrors, the
  events' German fields — the German story page is a redirect meanwhile);
  NEEDS_CONFIRMATION to carry the curation's judgement calls.
  [SETTLED 2026-11-07, the editor's word: the German pass followed their
  approval of the English — see the next section.]

## 2026-11-07: the German pass — the era pages, the Timeline, the events, in German

- **The editor's follow-up** (after their read of the published English:
  "This is looking much better"): Introduction off the top navbar; the eras
  pages for each era (the seven English ones already in place — kept);
  German versions of all the era pages and the timeline; the home page
  updated if necessary; publish. The home page needed nothing: the brand
  link leads home, the cards and the About paragraphs carry it.
- **The events' German fields added to all 69** (when_de, title_de,
  note_de, sources[].text_de — fresh translations of the condensed English
  notes; the old German notes no longer matched). /de/zeitleiste/ renders
  fully German now, intro paragraphs included (intro_de in
  reference/eras.yml for all seven eras, page_de: true so the Read more
  links open the German pages).
- **Six German era pages written** (site/de/epochen/, translations of the
  English ones; links and glossary anchors kept); the German Hohenlohe
  page's stale pointers fixed and its events foot added; the English era
  pages' alt_url restored so the language switch works both ways.
- **The caveat**: the editor does not read German — the German prose is
  machine-authored, follows the site's existing German terminology
  throughout, and awaits a German reader's review (NEEDS_CONFIRMATION).

## 2026-11-11 - AGAD 1/432/0/1/139 added (not published)

Two documents (Erdmann's reports of 1882 on Zagórów and Lissewo-Pyzdry, burnt
leaves of the Warsaw consistory's file), era `wlodzimierz`, slug
`agad14320139`. New: the supplied-text layer (`units/<slug>/supplied.yml`,
`supplied_html()` in `pipeline/build/build_site_data.py`, strings in
`site/_data/i18n.yml`, styles in `site/assets/style.css`): a collapsed panel
under a page's text with proposed wording for lost stretches, grade A or B
only, never in the transcription, translation or summaries. Also fixed: the
Sources page icons were empty SVGs (`include.kind` in `site/_includes/
sources-icon.html`).

## 2026-11-12 - the Trąmpczyński family's person pages and the Teki Dworzaczka (branch `trampczynski-family`, published 2026-11-13 at the editor's word)

- **The editor's family line checked against the documents** (the
  boundary decree of 1775 recites the title deeds 1522-1698): Jan the
  elder and Wojciech are brothers (Wojciech the "stryj" and guardian of
  Jan's sons, 1584-1593); the Jan who married Teresa Prusimska in 1692 is
  Władysław's son, the Jan of the partition of 1693 and the sale of 1698,
  not a grandson; Władysław died before 6 October 1693; his marriage to
  Anna Bojanowska is "by 1663".
- **Literature work `tekidworzaczka`** (Teki Dworzaczka): four regests,
  1614, 1642, 1663, 1692 - three supplied by the editor, one quoted on
  Minakowska's page - each a passage (c01-c04), cited fact by fact.
  Index ruled (Trąmpczyńskiego, Trąmpczyn, Nowawieś).
- **Person pages** (`reference/genealogy.yml`): Jan the elder, Wojciech
  (rewritten), Stanisław, Władysław, Jan, Jan na Kolno Prusimski
  (standalone), Krzysztof Prusimski (on his entry), and the family entry
  `trampczynski` with a list of its members who have pages. Layout: a
  parent or spouse can link to their page (`link:`), a family page lists
  `members:`; a stale `linked` value in the children list fixed.
- **Johann von Prusimski** (the Kolno mortgage certificate, inscription of
  1673) identified as very probably Jan na Kolno Prusimski (Claude,
  NEEDS_CONFIRMATION).
- **Corrected**: Minakowska's 1614 regest misread in the work's notes
  (Anna Słonecka's father is Jan Słonecki; her grandfather Stanisław
  Chwalibowski, pantler of Kalisz); the descent's generations in the
  notes, NEEDS_CONFIRMATION and Wojciech's bio.
- **verify_site.py**: the life-line check skips standalone blocks (they
  have no entry on /people/).
- The literature dataset of `nmpol` rebuilt: its source had changed on
  2026-11-06 (the locator shift) without the passages being regenerated.
- The editor's ruling: "Jan na Kolno Prusimski" in the edition's prose
  (reference/people.yml, the `prusimski` entry's comment).
- **The header's Sources is a dropdown** (the editor's word): All sources,
  Archival material, Newspapers, Literature, Maps, in both languages
  (`site/_layouts/default.html`, `site/assets/nav.js`, styles in
  `site/assets/style.css`, `sources_nav_all` in i18n). A `<details>`, so it
  works without script; the script closes it on an outside click or Escape.
  Checked on desktop and phone width.
- **Plan for a second family tree**, the owners of Trąbczyn, in the Zelmer
  explorer's format: `docs/ESTATE_TREE_PLAN.md` (nothing built).

## 2026-11-12 (afternoon) - the owners' family tree, two trees in the explorer (branch `trampczynski-family`, published 2026-11-13 at the editor's word)

- **/genealogy/ split**: the Zelmer tree moved to /genealogy/zelmer/ (its
  data to `site/genealogy/zelmer/data/`, the pipeline's output path with
  it); the new tree "Owners of Trąbczyn" at /genealogy/trabczyn/; one app
  build, two pages (`scripts/pages.cjs`); /genealogy/ a chooser that
  forwards old hash links to the Zelmer tree. The header's Genealogy is a
  dropdown of the two trees.
- **The tree** (`reference/estate_tree.yml`, schema
  `reference/estate_tree.SCHEMA.md`; built by
  `pipeline/genealogy/build_estate.py` to GEDCOM `site/genealogy/trabczyn/estate.ged`
  and the explorer's JSON): 68 people, 22 families, from the 16th-century
  Otto-Trąmpczyńskis through the Prusimskis to the Miączyński heir who sold
  in 1892; every fact cited (documents first; database dates only when
  exact); places with coordinates from the edition's own files.
- **Teki Dworzaczka c05-c10**: six regests quoted on Minakowska's pages
  (1658, 1671, 1673, 1706 twice, 1720). Settled by them: Władysław
  Otto-Trąmpczyński dead by 1671 (his widow's second marriage to Jan
  Goliński); Jan na Kolno's parents Krzysztof and Teresa Grudzińska;
  Trąbczyn held by Sebastian Prusimski 1700-1720, sold to Krzysztof.
- **Włodzimierz Miączyński died 18 December 1879** (the editor's word):
  changed throughout; the 20th was the death notice's issue date.
- **Maria Wielopolska**, the buyer of 1892, is Maria hr. Plater-Zyberk
  (1857-1909), wife of Władysław hr. Wielopolski (the editor's word); no
  kinship with the families found.
- **The explorer draws remarriages** by the charting standard: the person
  once, spouses in marriage order (two: first left, second right; three or
  more to the right, the marriage lines numbered), each marriage's children
  from its own line. Fixes the Zelmer tree's 43 people with children by two
  or more marriages. **The owner mark**: holders of Trąbczyn (rule `holder`)
  outlined with a key glyph and a legend, in the tree, search, surnames and
  the person page.
- The editor's two charts checked (docs/ESTATE_TREE_PLAN.md, section 8).

## 2026-11-13 - Trąbczyn bought back in 1896 (branch `trampczynski-family`, published 2026-11-13 at the editor's word)

- **Tadeusz Miączyński's repurchase of 1896** (the editor's report of the
  town history sign at Trąbczyn; its primary source not found): recorded
  in `reference/sources/trabczyn_history_sign_1896.md`, entered in the
  owners' tree (Tadeusz a holder, with his parents Witold and Klementyna
  Glińska and his son Władysław Józef) and in the wlodzimierz era's
  ownership line; supported by Breyer's notebook of 1936 ("Graf
  Miączyński" owner about 1911). The act is on MISSING_SOURCES.
- `build_estate.py`: a source kind `report`, for what the editor reports
  and the edition does not hold.

## 2026-11-13 (later) - the marriage of 1810, the year-only dates, Jan Łoś Goliński (branch `trampczynski-family`, published 2026-11-13 at the editor's word)

- **Michalina and Stanisław Adam married in August 1810**: the Geneteka
  index of the Warsaw registers has the civil act (ASC Cyrkuł IV 1810 no.
  67, 17 August) and the church record (St Andrew's 1810 no. 849, 21
  August); Aleksander born 9 January 1810 (ASC Cyrkuł IV births no. 245).
  Żychliński's and the PSB's 1809 are a year early. The bios, the identity
  and the genealogy blocks changed from "about 1814" (documents first).
- **Year-only database dates** stated without a mark of estimate now stand
  in the tree (the editor: "why not?"): Michalina b. 1778, Wiktoria
  Malczewska 1722-1780, Marianna Dąmbska baptised 1763, the marriages of
  1660, 1671 and 1847. Wieniec added with coordinates.
- **Jan Goliński = Jan Łoś Goliński** (the editor): Anna Bojanowska's
  second husband was Teresa Golińska's father; Konstancja Krusińska added
  as Teresa's mother; the person pages say so.

## 2026-11-13 (late) - APŁ 39/98/0/-/1333: the spot sheet and the editor's rulings (branch `trampczynski-family`, published 2026-11-13 with the holding)

- **The spot sheet applied**: "Z najgłębszem uszanowaniem" (163), "gajć"
  (176), "na mylnem przedstawieniu czynu" (88v, the editor's own reading),
  "art 1. 5. 11." (115), "majem" kept (113); the office's note on 88 stands
  as read (the editor unsure). The English follows.
- **Places**: "Łazińsk" matched to the colony (`trabczynskie-stare-oledry`) in
  the colonists' two petitions only, by a new `match_in:` of a place in
  reference/places.yml (pipeline/build/entities.py); the Russian forms of
  Trąbczyn, Nowawies, Marianton, Łazińsk, Osiny, Słupca, Konin and Kalisz
  matched (the index of 1333 and the table of 6603).
- **Daniel and Wilhelm Hohm** said on the holding page to be probably the
  Холмъ of the Łazińsk table of 1868; no person entries for the holding's
  people (the editor).

## 2026-11-13 (evening) - APŁ 39/98/0/-/1333 added: the liquidation-tables file of Trąbczyn, part I (branch `trampczynski-family`, not published)

- **New holding `apl399801333`**, six documents on 30 pages: the file's
  Russian index of 145 papers, 1864-1870 (a table); the plan of Trąbczyn of
  15 May 1865 (an image); Count Włodzimierz Miączyński's petitions of 23 July
  and 10/22 August 1865 against the commissioners' decisions for Krystian
  Lippeldt and for six farmsteads of Nowawies; the Łazińsk colonists'
  petitions of 1867 and 1868 for the forest rights of Hohenlohe's privilege
  of 1805. Era `wlodzimierz`.
- **The index** read in two passes (four Sonnet readers, then eight, two per
  page, settled by Claude); months fixed by the offices' own numbering; the
  editor's rulings: Osiny, the open entries minor.
- **The letters**: the editor's transcription corrected in 29 places where
  the image plainly shows another word (a missing line among them, "O co w
  najgłębszej pokorze błagamy"); folios 114v-115v and the petition no. 59
  transcribed by two readers each; the office's Russian note on folio 88
  set apart; catchwords and one page-crossing join ruled. English,
  summaries (claim-checked, 9 of 87 statements weakened) in session.
- `reference/people.yml`: Włodzimierz Miączyński tagged in this holding
  (`miaczynski-wlodzimierz`, with the index's Cyrillic forms), not Stanisław.
  `reference/glossary.yml`: "Maja" ruled out (the month). `site/_data/i18n.yml`:
  the document kinds petition and plan. Timeline: 1865 and 1867-1868. Era
  paragraph (both languages).
- Open: the spot sheet (seven readings), Łazińsk matching, Hohm/Холмъ,
  people, Russian place names, connections (NEEDS_CONFIRMATION).

## 2026-11-13 (night) - AGAD 1/432/0/1/139: the English made readable (branch `claude/genealogy-navbar-link-order-uro98h`, not published)

- At the editor's word ("easier to read while still following the
  transcription ... keep it light"), the English of Pastor Erdmann's two
  reports of 1882 rewritten: a word broken at the burnt edge whose sense the
  legible part fixes is translated whole ("General Superintendent", not
  "General-Superin[text lost]"); words from the twin report, the form or the
  grammar in square brackets ("[To His] Reverence", "[collected]"); a lost
  figure, name, place, date or negation stays "[text lost]". The German
  transcription is unchanged. 104 marks in the German, 23 in the English;
  the marker-check rows cleared in `reference/translation_rulings.json`.
  The "How it was prepared" tab says so. Asked: whether the two lost
  negations of 0322_a should read "[not]" (NEEDS_CONFIRMATION).
- The Genealogy menu lists "Owners of Trąbczyn" before "The Zelmer family".

## 2026-11-13 (night, later) - AGAD 1/432/0/1/139: the transcription completed in brackets (same branch, not published)

- At the editor's word, the German of both reports completed where no fact is
  added: 61 lines, supplied words in square brackets ("[Sei]ner [Hochwürden
  dem] Herrn General-Superin[tendenten]"), the A and B rows of `supplied.yml`
  and the procedural C rows; the two negations of 0322_a "[nich]t" and
  "[nicht]" and the English "[not]" in both (the editor). A lost figure,
  place or date stays `[...]`; 104 marks before, 40 after
  (`units/agad14320139/intake/supply_text.py`).
- Pipeline: a line ending in a bracketed hyphen ("fo[lgen-]") is a wrap and
  joins to "fo[lgen]den" (`corpus_pages.py`, `resolve_linebreaks.py`,
  `resolve_paragraphs.py`); no other corpus has such a line. Line-break and
  paragraph decisions ruled by hand for the address blocks.
- `docs/EDITORIAL_RULES.md`: the ruling, standing for this holding.

## 2026-11-13 (night, last) - AGAD 1/432/0/1/139: the burn no longer described; published (published 2026-11-13 at the editor's word)

- At the editor's word, the sentences on the leaves' fire damage taken out of
  the holding's title, description, introduction, "How it was prepared", both
  summaries, the timeline note and the era essay (English and German); the
  account stays in `units/agad14320139/notes.md`.
- Published with the readable English, the bracketed completions and the
  Genealogy menu order.
- The Zagórów report's summary (both languages) and the holding's
  introduction now carry its vices and conversions lines (no special vices,
  the reading uncertain; no conversions), resting on the editor's "[not]";
  the claim check records the two statements. Published the same night.

## 2026-11-13 (night) - the homepage rewritten (branch `claude/genealogy-navbar-link-order-uro98h`)

- At the editor's word ("still only talk[s] about the prince ... should read as
  if someone was encountering it for the first time"): the lede and the
  section under it (now "The story in brief" / "Die Geschichte in Kürze") tell
  the whole span, 1173 to the 1930s - the abbey of Ląd and the knights, the
  Prusimskis and the Łukom boundary, the Olęder colonists, the partitions and
  the uprising of 1794, the Hohenlohe-Ingelfingen years, Michalina's
  restitution and the mortgage dispute to 1834, Count Włodzimierz Miączyński
  and the colonists, the reform of 1864, Breyer in the 1930s - and name the
  literature, newspapers, family trees, maps and cemeteries beside the
  documents. Facts taken from the era essays (`reference/eras.yml`). The old
  closing figure (1,414,377 Reichsthaler) dropped with its paragraph.

## 2026-11-14 - name the subject: the homepage written again, and a new house-style rule

- The editor: the writing leans on "this", "that", "those" and on the reader's
  memory across figures and buttons. The homepage written again in both
  languages: each paragraph names its subject, explains the Crown Tribunal,
  the partitions, the Duchy of Warsaw and the colonists' forest rights, and
  no paragraph points back across the figures and buttons.
- The same fault fixed in the era pages: the Hohenlohe-Ingelfingen page's
  opening note (it still said "one of three eras ... not yet published"; there
  are seven) and its first paragraph, the insurgency page's "These are the
  estates", the boundary page's "They were not ended", and the colonists era's
  "They sue him" (both languages).
- `docs/HOUSE_STYLE.md`: new section "Name the subject; do not point back";
  "Concision" now defers to it.
- `docs/HOUSE_STYLE.md`, "Name the subject": the editor's example of what not
  to write ("this is its archive"), the sentence made only of pointers, with
  two more from the holdings' pages; 15 of the 54 holdings' opening
  paragraphs have the "... It is ..." pattern (offered to the editor).

## 2026-11-14 (later) - the holdings' opening paragraphs rewritten; Trąbczyn's owners before 1698

- At the editor's word ("I wouldn't open with these physical descriptions of
  items"): the first paragraph of all 54 holdings' descriptions, in English
  and German, now says what the documents are and why they matter, without
  the counts, archive, volume and languages the page's header already shows,
  and without "It is ..." sentences. The heading "# APP 53/20/0/-/Poznań
  Gr.1181" that repeated the reference inside that holding's description is
  gone. Facts kept from the old openings and the title lines; a few
  corrected on the way (the court order of 1589 is no longer "the earliest
  document in the collection" since the medieval charters came in; the
  summons of 1860 is a counterclaim answering the colonists' suit of 1859).
- The homepage and the boundary era's ownership line: Trąbczyn belonged to
  the Trąmpczyński family until they sold it to Jan Prusimski of Kolno in
  1698 (reference/genealogy.yml); both had said "the Prusimski family from
  1589".
- `docs/HOUSE_STYLE.md`, "A holding's own page": the description does not
  open by repeating the header. The TODO item offered this morning is done.

## 2026-11-14 (evening) - the pages no longer talk about themselves

- At the editor's word ("don't talk about the site/edition/project"):
  self-references removed from reader-facing text in both languages - the
  homepage's lede and closing paragraph, the medieval and restitution era
  pages, the About page (two sentences), the openings of app534062,
  app536017 (and its title line), app53170koningr121, oe1bu9454, adwl85,
  apl399801333 and ossol2289 (with its "session of 1 November" and "waits on
  the editor's rulings"), eight of the literature's Related notes, the
  timeline note of 1818, Dorow (1843)'s account and the Ostdeutscher
  Beobachter's summary. The Licences and privacy page keeps "the website",
  which it needs. `docs/HOUSE_STYLE.md`: new section "The pages do not talk
  about themselves".

## 2026-11-14 (night) - place descriptors checked; the homepage lede rewritten again

- The editor: Konin and Kalisz are cities (the homepage said "towns"; fixed);
  a place named with a descriptor is checked against its recorded kind. New
  `pipeline/review/check_place_descriptors.py` (lists, changes nothing; 40
  descriptors to read) and HOUSE_STYLE, "Check what a place is before you
  call it something".
- The homepage's second sentence no longer says that "people wrote down" who
  owned the estate: the ownership, farming, settlement and lawsuits of the
  estate "were documented" from 1173 to the 1930s. HOUSE_STYLE, "State the
  facts, not the fact that they were written down".

## 2026-11-14 (night, later) - the register's place classes corrected

- At the editor's word ("correct any other issues relating to place names"):
  `reference/places.yml` now says what `kind:` means (what the place is today;
  city is about 50,000 inhabitants or more, or a regional or national
  capital) and 13 places moved from town to city: Konin, Opole, Legnica,
  Częstochowa, Głogów, Zielona Góra, Mysłowice, Włocławek, Jena, Weimar,
  Bayreuth, Fürth, Memel. Open: Ostrów and Neusatz (which place?), Teplitz
  and Emden (about 50,000), Charlottenburg (now a district of Berlin).
- Found and fixed: the Places index and the place pages printed the raw word
  "city" (lowercase, in English also on the German pages) for the 35 cities,
  and "country" and "region" for the 15 of those; labels added in both
  languages.
- `check_place_descriptors.py` no longer lists a colony or settlement that is
  also a village or hamlet.

## 2026-11-14 - Świątniki in the gazetteer; the map viewer retries a failed load (branch `trampczynski-family`, published 2026-11-14 at the editor's word)

- The editor, Mapa dróg 1890 finished: "you need to make a place entry for
  Świątniki". `reference/gazetteer/swiatniki.yml` written on the register's
  `swiatniki` (the village just west of Rzgów, OSM's point, the Kodeks
  editors' note agreeing), the text Claude's, from the edition's documents:
  the *sanctuarii* granted with Rzgów in 1261 and 1280 (KDW 4, 6), one of
  the sixteen church villages granted to the Prince in 1797 (Oe 1 Bü 14525,
  doc. 5), 21 houses and 133 people in the table of about 1797 (entry 274),
  a *Zins Dorf* of Zagórów in the list of 1806 (letter 24), and letters 212
  and 213 of 1811 written there. `reference/gazetteer_sources.yml` gained
  the key `oe1bu14525` and the locators entry 274 and letters 212, 213.
  Label mapadrogi1890-060 linked to the place; Stara Huta stays open.
- `maps/mapadrogi1890/labels.yml` held its labels twice (a stale copy
  before the current one, which won as the later YAML key) and its `map:`
  key lost inside a comment line: the current copy kept alone, the key
  restored. No label changed but 060's link.
- The editor saw "The map tiles did not load (HTTP 503 ...)" on the
  published Mapa dróg 1890 page; the tiles' info.json answered 200 minutes
  later - a passing GitHub Pages error. `site/assets/maps/map-viewer.js`
  now retries the opening three times (after 2, 5 and 10 seconds, saying
  so) and asks for a failed tile again (`tileRetryMax: 3`); only then the
  message, now in the page's language. Checked locally with a page whose
  tile address fails (four tries, then the message) and on the real page
  (opens, 37 marks).
- Rebuilt: site data, place pages, map pages, Jekyll; `gazetteer.py --check`
  and `verify_site.py` pass (639 documents, 69 400 internal links).

## 2026-11-14 (later) - Kolonia Wrąbczyn; the Prince's colonies under their first names on the maps (branch `trampczynski-family`, published 2026-11-14 at the editor's word)

- The editor: the roads map's Колонія Вромбчинъ "is a distinct place that
  is called Kolonia Wrąbczyn. It needs its own place entry." Label
  mapadrogi1890-008 moved from Wrąbczynkowskie Holendry (whose map
  appearance went with it) to the new `reference/gazetteer/kolonia-wrabczyn.yml`:
  one of the Prince's colonies after the hereditary lease of 100 Hufen to
  eighteen settlers (app539680801-3), named by Breyer 1938 p. 21 and Wąsicki
  1953 p. 176, with Chodyła 2015 p. 147 on where its settlers came from;
  placed from the map (`from_map`). Source keys `breyer1938` and
  `wasicki1953` added. The literature index rules Wąsicki's and Chodyła's
  passages away from the village Wrąbczyn (`except`). Seidel's
  "Kolonweiler" is her misquotation of Breyer and is not used. Open: whether
  it is today's Wrąbczyn Górski (NEEDS_CONFIRMATION).
- The editor: a colony the Prince founded that was later renamed shows its
  first name and today's in brackets, so Колонія Адольфсбергъ is not left
  beside an unexplained "Zalesie". The gazetteer's new field `founded_as`
  (GAZETTEER_PLAN) on the eight entries whose text gives the first name;
  `pipeline/maps/map_pages.py` builds the label name from it: "Kolonia
  Adolfsberg (Zalesie)", "Emilienheim (Michalinów Oleśnicki)", "Kolonia
  Ludwigslust (Mały Las)" and so on, on every map's page.
- Rebuilt; gazetteer --check, literature_index --check, verify_site pass
  (69 458 internal links).
- The same day, the editor: "Kolonia Wrąbczyn is today's Wrąbczyn Górski.
  Yes, change the label." The entry, never published, merged into
  `wrabczyn-gorski` (the modern name heads, the editor's two sentences kept,
  `founded_as: Kolonia Wrąbczyn`; the separate entry and its pages removed);
  label mapadrogi1890-008 points there and reads "Kolonia Wrąbczyn
  (Wrąbczyn Górski)", its type changed from unsure to village; the
  literature index's comments follow.

## 2026-11-14 (afternoon) - the map-labelling to-do list keeps itself (branch `trampczynski-family`)

- The editor: remove Pełzucki 1901 and Mapa dróg 1890 from the bulk
  batch's labelling sheet, and the Mapa dróg warning at its top; "When I
  finish with a map and it gets published to the site, let's remove it
  from this to-do list." The sheet's script moved from scratch into the
  pipeline (`pipeline/maps/label_index.py`) and leaves out every map whose
  register entry on origin/main has `in_project: true`; the warning is
  gone, Zagórów 1841's outdated note corrected (001.jpg as drawn), and
  Łukom 1766, waiting for its re-marking, given a row. ADDING_A_MAP step 5
  carries the rule. 19 maps on the list.

## 2026-11-14 (afternoon, later) - the labelling page's step 3 reworked (branch `trampczynski-family`)

- The editor's report on Łukom 1766 (Dezerta Jemielno): after the
  double-click that ends the trace, the cursor jumped into "Form as written
  on the map" and the band keys could not be used; choosing a type other
  than the gazetteer's made the label vanish from the sidebar. The second
  came from a re-render that swapped in a row of type buttons that saved
  at once and moved on to the next place. `pipeline/maps/label_page.py`:
  no field is focused after the trace (or a skipped trace); in step 3 the
  type buttons only choose, and a red **Create** beside **Cancel** (or
  Enter) makes the label, the status line naming what was created; the
  type keys (0-9, -, =, U) removed, with the help and status texts. All
  sheets rebuilt; tested on a separate port (8791) through the trace,
  the band key, "Other" and Create, the test's storage cleared.
- Later the same afternoon, the editor: changing a saved label's form or
  type needs a button that commits it, and the list should show the
  change. The edits to a saved label (form, note, type, band) now wait for
  a red **Save changes** beside **Cancel** (Enter in the form or note
  field does the same), the type buttons sit in the panel and only choose,
  Cancel or Esc puts the label back, and leaving it with changes not saved
  asks; "Change what it shows" is gone. The "To find" list shows a found
  item's saved form and type (before, the gazetteer's form, so an edit
  never showed there); "Other labels" shows the type too. All sheets
  rebuilt; tested on port 8791 (type, choose, save, cancel, leave), the
  test storage cleared.

## 2026-11-14 (evening) - Łukom 1766 marked on the JPG and imported (branch `trampczynski-family`, not published)

- The editor's eleven marks (ten places and the inscription *Tres mansi
  Conventûs Landensis*) imported; the inscription had no `new_place` in the saved
  file, so a copy with it filled in was imported. Mark-only fit RMS 251 m over 4
  points, 11 positions, `in_project: true`, map pages built, gazetteer check and
  verify_site pass (69 562 links). The inscription's note says what it refers to
  (the Ląd convent's farms at Łukom) and it links the 1447 and 1461 charters of
  the Ląd copy-book; the Kodeks decree the editor mentioned was not found in the
  volumes (NEEDS_CONFIRMATION). The mobile check could not start (Edge failed to
  launch in the crawler).
