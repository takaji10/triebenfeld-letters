# Currency Normalisation Report

Currency in this corpus is written a dozen different ways. The aim was to make it queryable without altering anything whose meaning is uncertain.

## The monetary system

Prussia/Brandenburg to 1821: **1 Reichsthaler = 24 Groschen; 1 Groschen = 12 Pfennig.** So a valid Groschen value is 0–23 and a valid Pfennig value is 0–11. The corpus obeys this exactly:

- Every Groschen value found: `6, 6, 10, 12, 14×6, 16, 16, 18, 18` — none exceeds 23 ✓
- Every Pfennig value found: `4, 11, 11, 11, 11, 11` — none exceeds 11 ✓

Because the system checks out, **position is a reliable guide** — which is what makes the `d` problem solvable at all.

## What was changed

| Change | Count |
|---|---|
| `/m` expanded to thousands (`112/m` → `112000`) | 125 |
| Reichsthaler family → `Rthl` (`rt`, `rt.`, `r.`, `rtl.`, `rth`, `rthl`, `R.`, `t.`) | 1,272 |
| `d` resolved to `Rthl` (value ≥ 12) | 131 |
| `#` → `Ducaten` | 19 |
| **Total** | **1,547** |

## What was deliberately NOT changed

| Left alone | Count | Why |
|---|---|---|
| `d` in Pfennig position | 6 | `d` = *denarius* is the **correct** historical abbreviation for Pfennig — the same convention behind British pre-decimal pence. `14 g. 11 d.` is right as transcribed, not an error. |
| `d` in date contexts | 6 | `d.` also abbreviates *den/der*. `1808 d. 14t Febr` is a date, not a sum. |
| `t`/`r` that were ordinal day markers | 14 | `14t Febr` is "14ten Februar". A first pass turned these into `14 Rthl Febr` — caught in dry run, now guarded. |
| `d` genuinely ambiguous (≤ 11, no Groschen) | 12 → **0** | Reviewed and resolved by hand (see `NEEDS_CONFIRMATION.md` §B): 10 were Reichsthaler, 1 was Groschen, and 1 (`2.d Preſectio`) wasn't currency at all — it was a garbled rendering of *Podprefect*, corrected to `Pod Prefecta`. One further case, `6. d.`, turned out to be a corrupted `64/m` and was expanded to `64000`. |

## Why `d` could be resolved at all

The decisive evidence: **46 distinct sums appear written both ways** in the corpus.

| Sum | as `d` | as Reichsthaler |
|---|---|---|
| 6000 | 3× | 39× |
| 112000 | 2× | 13× |
| 100000 | 2× | 20× |
| 50000 | 2× | 19× |

The 112,000 advance — the central financial thread of the whole correspondence — is written `112000 rt` in one letter and `112000 d` in another. Same sum, same context, two notations. That settles it: large-number `d` is Reichsthaler, and the `Rthl` form is overwhelmingly dominant, so `d` is the minority form.

**One correction to the original hypothesis:** `d` as Pfennig is *not* a transcription error. It is the standard historical abbreviation and has been preserved.

## Method note

This ran as a **dry run first**, which caught two real bugs before anything was written:

1. `14t Febr` was being converted to `14 Rthl Febr` — the bare `t` in the Reichsthaler family was matching ordinal day markers.
2. Two genuine currency values (`21000 d.`, `27000 d`) were wrongly skipped as dates, because a preceding *den/am* looked date-like. The guard now only treats a number as day-sized if it is ≤ 31.

Both were fixed and the guards are explicit in the code. Line count was preserved throughout; a backup of the pre-change file is at `..._cleaned.txt.bak3`.

## Addendum — a bug found later, and its fix

While reading letter 72 in full for the letter-splitting work, one line stood out: `Warschau den 5 Rthl Maerz 1812` — a date reading as if it contained a currency amount. Tracing it back: the month-detection regex used by the `d`-resolution date-guard had a character-class bug. `m[äae]r[zc]` matches **one** character from {ä, a, e} — it can match "März" or "Marz" or "Merz", but **not** "Maerz" (the two-letter "ae" digraph spelling), because a character class can't match a two-character sequence. So wherever the source used that spelling, the guard silently failed to recognize it as a date context.

**Scope, checked systematically rather than assumed:** re-scanned every one of the 164 bare-`t`/`r` → `Rthl` conversions logged during the original run, filtered to day-sized values (≤31, since ordinal day markers like "5t" for "5ten" are the only plausible confusion — real currency sums in this corpus are essentially always either much larger or explicitly followed by a real unit), and read each in its original context. Found **23 total** miscoverted ordinal-day references — 1 from the `Maerz`-spelling bug specifically, and 22 more from a related, broader gap: the guard only checked for a following month *name*, not for the equally common `d. M.` ("dieses Monats" / "of this month") construction, which doesn't name a month at all (e.g. `den 15t d. M.` = "on the 15th of this month").

All 23 reverted to their original ordinal-day reading. Two of those lines had *also* legitimately converted a real currency figure elsewhere on the same line (L1185: `...6 rt` → `6 Rthl`; L6195: `...8000 Rt.` → `8000 Rthl`) — both re-applied after the revert so nothing real was lost. Full list of affected lines available on request; none required guessing, every one was verified against the pre-normalization backup before touching it.
