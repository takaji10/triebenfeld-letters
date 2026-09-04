# Transcription Audit — von Triebenfeld / Hohenlohe-Ingelfingen Correspondence

Phase 2b. Because the underlying transcription was produced by AI rather than a human paleographer, this pass was deliberately scoped as an **audit, not a rewrite**. AI transcription carries a failure mode a human misreading doesn't: where handwriting is faint or damaged, a generative model can fill the gap with fluent, plausible text that corresponds to nothing on the page. Guessing at what a garbled passage "should" say would repeat exactly that operation, and stacking a second guess on a possible first one launders it into something that merely *looks* more confident.

So: things that could be proven were fixed; things that could only be guessed were flagged for you to check against the original scans.

---

## Part 1 — Fixes applied (23 tokens)

Every one was individually verified in context before applying. All are the same class of narrow, single-character letter-confusion correction used in the proper-noun pass, applied to non-name vocabulary.

**The honorific `Durchlaucht`** (the corpus's most repeated word, 1,393 uses) had accumulated 18 corrupted variants, all unambiguous in context:

| Fixed | → | Lines |
|---|---|---|
| `Durchlacht`, `Durchlaut`, `durchlaut`, `Durchlautt`, `Durchlaugt`, `Durchlauß`, `Durchlauft` ×3, `Durchlauf`, `Durchlau` ×2, `Durchlängt` | `Durchlaucht` | 361, 1220, 1928, 2186, 2419, 3307, 8291, 15033, 16048, 16855, 18207, 18276, 18297, 18918, 21818 |
| `Durchlauch tigster`, `Durchlauch ligster` (spurious mid-word space) | `Durchlauchtigster` | 18102, 18550 |
| `Hochfürstg` ×2, `Hochfürstlg` | `Hochfürstl` | 8476, 10246, 10277 |
| `unnd` → `und`; `Ewir` → `Ewr`; `Ihnem` → `Ihnen` | | 1046, 17471, 15415 |

Verified: line count unchanged, word count −2 (exactly the two space-joins).

### What was rejected, and why it matters

An automated scan proposed **108** candidate word-level fixes. Hand-verification rejected **85 of them** — a 79% false-positive rate that is itself the most useful result in this section. The rejects fell into three groups:

- **Real German words** the corpus uses correctly: `bieder` (upright — *not* `wieder`), `bar` (cash — *not* `war`), `nimmer`, `keinem`, `Dienern`, `Ministern`, `warm`, `nit`, `dein`, `vorm`. Also `pas` (French — there is at least one French letter in the corpus) and `Contracti` (Latin, alongside the corpus's other Latin legal terms).
- **Line-wrap fragments that were already correct**: `dner` is the tail of `verschie|dner`; `dine` is the tail of `Lombar|dine` (the surname Lombardini); `dens` is the tail of `Ver|dens`. "Fixing" any of these would have corrupted correct text.
- **Genuinely ambiguous**: `nich` maps equally to `ich` and `mich`; `ach` to both `nach` and `auch`.

The practical takeaway: **the transcription's error rate on ordinary vocabulary is very low.** Nearly everything that looks wrong to a naive matcher is either correct period German or a line-wrap artifact. That is reassuring about the source, and it is why a broad "clean up the prose" pass would have done more harm than good.

---

## Part 2 — Recommended fix, not applied (your call)

**Line 1625 — a provable numeric error, with two independent proofs.**

The corpus contains the same estate-revenue table twice: once summarised (letter 24, L1623–1638) and once itemised (letter 179, L13028–13058). Both tables are **internally arithmetically perfect**:

| | Table A (letter 24) | Table B (letter 179) |
|---|---|---|
| Tit. I.1 | 5752 | 5752 |
| Tit. I.2 | 16781 | 16781 |
| Tit. II | 3500 | 2000 + 1500 = **3500** ✓ |
| Tit. III | 13357 | 3000+1500+150+2125+1800+4560+222 = **13357** ✓ |
| Tit. IV (brickworks) | 857 | 870 |
| **Stated total** | **40247** ✓ | **40260** ✓ |

Every subtotal in the itemised version reproduces the summary version's aggregate exactly. This validates the transcription of roughly twenty separate figures — strong evidence the numbers came through accurately.

It also isolates one error. Line 1625 reads `5752 d. 14 g. 4 d.` But every other line item is a whole Reichsthaler, so the fractional part of Table A's own total (`14 g 11 d`) must come entirely from this item. Table A therefore contradicts itself, and Table B independently reads `14 g. 11 d.`

> **Recommended:** L1625 `14 g. 4 d.` → `14 g. 11 d.` — proven by the table's own arithmetic *and* by the duplicate.

I have not applied this. It is a financial figure in a financial corpus, and numbers are where you would most want the final say. Say the word and it takes a second.

*(The 857 vs 870 brickworks difference is **not** an error — each table is self-consistent with its own total, so these are two genuinely different valuations, taken at different dates.)*

---

## Part 3 — Structural findings (these change how the database should be built)

### 3.1 The letter numbering is NOT chronological

This is the single most important finding for the database design. Sorting by letter number does **not** give you chronological order. Reconstructing each letter's date from its signature block (282 of 301 letters have one) shows the archive is **two sequences bound together**:

| Block | Letters | Period |
|---|---|---|
| **Block 1** | 1–74 | 1806–1815 (internally jumbled: 1815 → 1812 → 1806 → 1808 → 1809 → 1810 → 1812) |
| **Block 2** | 75–301 | 1798 → 1816, cleanly ascending |

Letter 75 jumps back seventeen years, from 1811 to 1798. Within Block 2 the numbering is a genuinely reliable chronological proxy; within Block 1 it is not.

**Implication:** the database needs a real `date` field parsed from each letter's signature block, and queries about chronology must use that field, never the letter number.

### 3.2 Letters bundled under a single number

Eight letters contain two or more complete signature-and-date blocks, meaning more than one letter is filed under one number. Letter 118 is confirmed by inspection: it holds a letter dated **10 Feb 1804** and another dated **29 March 1804**, each separately signed.

| Letter | Signature blocks | Date lines |
|---|---|---|
| 31, 269 | 2 | 2 |
| 50, 72, 118 | 3 | 2–4 |
| 265 | 5 | 2 |
| 179 | 2 | 4 |
| 74 | 10 (a legal instrument quoting parties) | 4 |

Letters 31, 50, 72, 118, 265 and 269 are the strong candidates for splitting into separate database records. Letter 74 is likely a false positive — it is a court document that names parties repeatedly rather than a bundle.

### 3.3 Letter 48 and the final unnumbered letter are the SAME letter, transcribed twice

Both give the identical account of thirteen powers of attorney granted to Justizbürgermeister Hawich — same structure, same enumeration, same content. They are two transcriptions of the same document from different copies.

**This is unexpectedly valuable: it is a free accuracy benchmark.** Two independent transcriptions of one document let you measure quality directly, and where they disagree, one is usually demonstrably right:

| Letter 48 (L3666+) | Final letter (L21779+) | Which is right |
|---|---|---|
| `Ober Inspector Hertes` | `Ober-Inspektor Hecker` | **Hecker** — the estate inspector named ~30× elsewhere |
| `Traperiner Gütern` | `Trąbczyner Güter` | **Trąbczyner** — confirmed real place |
| `Juden Oppenheimer et Wolff` | `Süden Oppenheimer et Wolf` | **Juden** — Oppenheimer & Wolff, a Jewish banking house named elsewhere |
| `Dqbska` | `Döbske` | Both corrupt — cf. `Dąbska` used elsewhere |
| `Viertens` (fourth) | `mertens` | **Viertens** — the enumeration runs erstens…dreyzehentens |
| `Hawich` | `Habik` | cf. the Hawich/Habick cluster already standardised |

Neither copy dominates: each is right where the other is wrong. Worth reading side by side if this letter matters to your research — between the two you can recover a better text than either provides alone.

**Also note:** the final letter is one of the two unnumbered letters identified back in Phase 1. Its content is now identified.

### 3.4 Damaged page edges — 5 blocks, ~42 lines

The 56 `[...]` markers are not scattered word-level doubt. Forty-two fall in five runs of consecutive lines, each cut consistently on **one side only** — a physical damage or scan-crop signature, not transcription uncertainty:

| Lines | Extent | Edge lost |
|---|---|---|
| 18126–18133 | 8 lines | right |
| 18161–18171 | 6 lines | left |
| 20950–20961 | 11 lines | right |
| 21684–21689 | 6 lines | left |
| 21702–21713 | 11 lines | right |

These passages have text genuinely missing from the source and can never be recovered from the transcription alone — only from the original, if the margin survives. The remaining 14 `[...]` are isolated one-off gaps.

---

## Part 4 — Flagged for your review (not fixed)

### 4.1 Transcription's own uncertainty markers: 224 total

The transcription flagged its own doubt in four ways. **These are the highest-value passages to check against the originals**, because they are the transcription process's own admission of low confidence — exactly where the hallucination risk is concentrated.

| Marker | Count | Meaning |
|---|---|---|
| `[?]` | 96 | Illegible, no reading offered |
| `[...]` | 56 | Omitted/unreadable span (42 = the damaged edges above) |
| `[xyz?]` | 49 | A reading offered, but flagged uncertain |
| Other `[...]` | 23 | Editorial expansions (`P[ro] M[emoria]`, `[Locus Sigilli]`) — benign |

The 49 flagged-guess markers are the most efficient starting point: each is a specific short string the transcriber doubted, so checking one is a quick glance rather than a re-reading. They include several proper nouns already touched in Phase 2 — `[Schenck?]` (L2853), `[ritz?]` (L16316, in the Köckritz cluster), `[Breslau?]`, `[Potsdam?]`, `[Werleben?]`.

### 4.2 Date outliers worth confirming

Letters whose signature date breaks their neighbours' run — either a misread date, or a genuinely misfiled letter:

| Letter | Date reads | Neighbours | Note |
|---|---|---|---|
| **109** | 31 Jan **1805** | 1799 / 1801 | Six years out of place |
| **254** | 2 May **1809** | 1814 | Five years out of place |
| **186** | bare `1810.` | 1806 | No month/day; bare year on its own line |
| 232 | 16 June 1811 | 1812 | Minor |

*(Letters 101, 247 and 248 initially flagged as outliers but cleared on inspection — the odd years are references in the body text, e.g. "eine Cabinets Ordre vom 4ten Marz 1795", not the letters' own dates. Letter 101 simply has no signature date.)*

### 4.3 Garbled passages — flagged, deliberately not "fixed"

These are where a reading would have been a guess. Listed for scan-checking, with no proposed correction:

`Einzdurchlaucht` (L984) · `fardurchlaucht` (L15227) · `Bestandurchlaucht` (L16035) — glued/garbled honorifics where the first element is unrecoverable.
`durchlängt` (L5250) — a standalone word on its own line between unrelated content.
`mirn` (L10359) · `unun` (L14180) · `habnen` (L20530) — non-words in passages too broken for the surrounding text to disambiguate.
`durchlaus` (L2984, "nehme ich durchlaus nichts") — probably `durchaus`, but that is a different word rather than a letter-shape slip, so it wants confirming.

---

## Summary

- **23 fixes applied**, each individually context-verified.
- **85 of 108** automated candidates rejected on inspection — the transcription's ordinary-vocabulary accuracy is high, and most apparent errors are line-wrap artifacts or real words.
- **1 numeric fix recommended** with arithmetic proof, awaiting your approval.
- **4 structural findings** that affect database design: non-chronological numbering, bundled letters, a duplicated letter, and damaged page blocks.
- **224 uncertainty markers** catalogued and prioritised for scan-checking.

The corpus text itself is now in good shape. The remaining work is verification against originals — which needs the scans, not more processing.
