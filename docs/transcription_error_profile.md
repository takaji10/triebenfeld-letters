# Transcription Error Profile
### Derived empirically from the letter 48 ↔ 302 twin

Letters 48 and 302 are the same document transcribed twice from two physical copies — the only place in this corpus where a second witness exists. Their **104 divergences over ~630 words** are therefore a measured sample of how this transcription actually fails, rather than a guess about it. This profile is the working reference for reading the other 300 letters, where no second witness exists to catch anything.

**Headline: neither witness dominates.** Letter 48 is right about as often as letter 302, and each is wrong exactly where the other is right. No single transcription pass of this corpus should be treated as authoritative.

---

## The rules

### ① Numeric corruption — most serious, and effectively undetectable alone

| | Letter 48 | Letter 302 | Truth |
|---|---|---|---|
| Obligation | `25000 rt` | `250000 Rt` | **250000** (confirmed) |
| Registered claims | `23000 rt` | `32000 Rthl` | **unresolved** |

An order-of-magnitude error and a digit transposition in a single letter. **No financial figure in this corpus is trustworthy on its own.** The only figures we can positively vouch for are those in the estate-revenue table, and only because its arithmetic cross-checks internally (every subtotal in the itemised version reproduces the summary version exactly).

*Practical consequence:* treat any single-sourced figure as provisional. Where a figure matters to a conclusion, look for an arithmetic or cross-letter check before relying on it.

### ② A real word beats a non-word

Where the two witnesses disagree and one reading is a valid German word while the other is not, **the real word is almost certainly correct.**

| Real word | Non-word | Correct |
|---|---|---|
| `Reichstag` (48) | `Kreſstag` (302) | Reichstag ✓ |
| `Viertens` (48) | `mertens` (302) | Viertens ✓ |
| `Sechstens` (48) | `Fochstens` (302) | Sechstens ✓ |
| `Rest` (48) | `Kest` (302) | Rest ✓ |
| `Aufhebung` (48) | `Austhabung` (302) | Aufhebung ✓ |
| `Trąbczyner` (302) | `Traperiner` (48) | Trąbczyner ✓ |

Six for six, and it points at both witnesses rather than favouring one.

> **Note on a discarded rule.** An earlier draft proposed the opposite: that a *famous* term appearing in a mundane context is a hallucination red flag, reasoning that `Reichs Tag` had been inflated from an obscure `Kreistag`. That was wrong — Reichstag is correct. The rule was built from a single example and had the direction backwards; applied at scale it would have "corrected" correct readings into invented obscure ones. Recorded here because a plausible-sounding rule that fails is worth remembering.

**Limit:** where *both* readings are real words (`Juden`/`Süden`, `nach`/`noch`), the rule is silent and only context decides.

### ③ Ordinal series are a free self-check

Both witnesses garble the enumeration, but in different places:

- 48 → ordinals present: **1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12**
- 302 → ordinals present: **1, 2, 3, 8, 9, 12, 13**

**Together they reconstruct the complete 1–13 series that neither has alone** — and 302's `stünftens` supplies the *Fünftens* that 48 mangles into `suustens`. A gap in an ordinal run is machine-detectable and, once detected, usually certain.

*Implemented:* a corpus-wide ordinal scan is part of the toolset. It finds only two runs (this letter's two copies), because long enumerations are rare here — but where one occurs it is free verification.

### ④ Proper nouns are the least reliable category

`Hertes`/`Hecker` · `Traperiner`/`Trąbczyner` · `Niederwiecki`/`Niedzewiecki` · `Schench`/`Schenk` · `Lahrschen`/`Larischen`.

Most alarming: **48 reads `Heinrich` where 302 reads `Howich`** — the name is *Hawich*, and 48 corrupted it into an entirely ordinary German given name. A wrong name that looks completely normal cannot be caught by inspection.

*Practical consequence:* rare spellings of names deserve automatic suspicion. A scan for rare tokens close to an established name found **~220 candidates**, including residual variants of names already standardised — e.g. six further `Köckritz` forms (`Köckrich`, `Koekritz`, `Kockeitz`, `Köcheritz`, `Köchriz`, `Köclwitz`) and several `Triebenfeld` corruptions (`Trinbenfeld`, `Priebenfeld`, `Frebenfeld`, `Sorebenfeld`). See `NEEDS_CONFIRMATION.md` §I.

### ⑤ Function-word flips reverse meaning — the irreducible risk

`die **Ab**weisung` (dismissal) vs `der **An**weisung` (instruction) — opposite legal meanings, one letter apart. *(Abweisung is correct here.)* Also `exmittirt`/`committirt` — different legal acts — and `nach`/`noch`, `als`/`da`, `wie`/`wir`, `vor`/`von`.

These are undetectable without a second witness, because both readings are fluent and grammatical.

*Practical consequence:* a research conclusion resting on a single small function word is provisional. This is the class the corpus simply cannot protect you from.

### ⑥ Silent omission

Letter 302 **drops the date line entirely** (`Kontop den 7ten Marz 1809`). Letter 48 drops content 302 preserves elsewhere.

*Practical consequence:* **absence of a date is not evidence that a letter was undated.** This directly affects the 19 letters with no parseable date.

---

## Three sources of divergence, not two

A difference between the two witnesses can arise at three points, and they have different implications:

1. **Transcription error** — the AI misread the page. *(e.g. `25000` for `250000`.)* A defect to be corrected.
2. **Scribal error** — the human copyist erred when producing the second physical copy. *(e.g. `23000`/`32000`, where both transcriptions faithfully render their respective pages.)* **This is a genuine historical datum about the archive, not noise.** It should be recorded as "both readings attested", never silently resolved.
3. **Legitimate variation** — orthographic differences between the two copies.

Category 2 is easy to miss and important: it means some divergences are unresolvable *in principle* from the transcription, no matter how carefully it is read.

## The harmless majority (~35%)

`ß`/`ss`/`z`, `-irt`/`-iert`, word-division (`aus gestellt`/`ausgestellt`), `Ewr`/`Ew`/`Ewer`, capitalisation. This is variation within the period's own writing tradition, not error — and it confirms the decision not to "smooth" the German. Normalising it would destroy real evidence about the two copies while fixing nothing.
