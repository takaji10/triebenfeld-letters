# Needs Confirmation

**The one place to look for anything still awaiting your ruling.** Everything
settled has moved to `CHANGELOG.md`; nothing listed here has been changed in the
corpus. Counts re-measured 2026-09-03.

`name_catalogue.md` is now an **outstanding-work list**: every ruling you give is
recorded in `name_rulings.json`, and rebuilding the catalogue suppresses it. So
nothing you have already decided is ever put to you a second time. Add rulings
there (or tell me and I will), never remove them.

> **Corpus line numbers shift** whenever lines are added or removed. They were
> re-derived 2026-09-03 after the letter-number strip. If a reference here does
> not match, search for the token rather than trusting the number.

| § | What | Count | Where to work |
|---|---|---|---|
| A | Source discrepancy, letters 48/302 | 1 | needs the physical copies |
| B | The transcriber's own uncertainty markers | 141 | `scan_review.html` |
| C | Damaged page blocks | 2 letters | `scan_review.html` |
| D | Name variants proposed, not yet ruled | 167 | `name_catalogue.md` §Proposed corrections |
| E | Two names, one entity or two? | 3 | `name_catalogue.md` §Established names… |
| F | Names withheld as ambiguous | 5 | `name_catalogue.md` §Withheld |
| G | Specific names investigated, awaiting you | 6 | `name_decisions.md` §Still open |
| I | **Names with no identification** | **482** | `name_review.csv` (fill column 3) |

---

## §A. Source discrepancy — needs the original manuscripts

Both copies are internally consistent, so this is the *copyist's* error, not the
transcription's. Cannot be resolved from the text.

| Where | Letter 48 | Letter 302 | Need |
|---|---|---|---|
| Registered claims figure | `23000 Rthl` | `32000 Rthl` | which physical copy is right |

## §B. The transcriber's own uncertainty markers — 141

Places where the transcriber recorded doubt rather than guessing. Start with the
**46 `[word?]` guesses** — each is a short flagged string, so cheapest to check —
then the **95 bare `[?]`**. Every one has a scan beside it via `page_scan_map.csv`.

## §C. Damaged page blocks — letters 247 and 248

Text genuinely missing, recoverable only from the originals. Flagged in
`letters.csv` under `has_damage`.

## §D. Name variants proposed but not ruled — 167

In `name_catalogue.md` under **Proposed corrections**, with letter, page and the
scan filename on every row.

**86 are tier A** (anchored on a name from `whos_who.md`) and **89 are tier B**
(a seed the script discovered statistically). Start with tier A — the heaviest are
`Schenck` (7 variants), `Schöler` (5), and `Schlawenschitz`, `Warschau`,
`Cabanis`, `Kunckel`, `Göschel` (4 each).

> **Read these with suspicion.** Of the ~25 you checked, about 20 were wrong.
> The failures were *all* in the statistically-discovered seeds (`Pforte`→`Pferd`,
> `Schriften`→`Schritte`, `Coeln`→`Cosel`); every fix anchored on a name from
> `whos_who.md` held up. Each entry is labelled **tier A — settled canon** or
> **tier B — discovered**. Work tier A first; treat tier B as a list of places to
> look, not corrections to approve.

## §E. Two established names — one entity, or two? — 3

Both spellings are common, so neither looks like a slip, and the variant matching
never compares them. Never auto-merged: this is the shape of the mistake nearly
made with `Hawich`/`Honrichs`.

| Name A | Name B | Note |
|---|---|---|
| `Sachsen` ×18 | `Sachßen` ×10 | ß/s variant, or two spellings of the same |
| `Wartemberg` ×3 | `Würtemberg` ×14 | |
| `Bartenstein` ×3 | `Brandenstein` ×6 | probably genuinely distinct places |

## §F. Withheld as ambiguous — 5

In `name_catalogue.md` under **Withheld**. Each sits equally close to two
different names; merging on a coin-flip is how two real people become one.

## §G. Investigated, awaiting your eye — 6

Full evidence in `name_decisions.md` under **Still open**.

| Item | State |
|---|---|
| `Märck` (line 2827) | you are checking. `Märkische Landschafts-Obligationen` is a real instrument, so `Märck.` may be a correct abbreviation |
| `Holländer` → `Hauländer` | **RESOLVED 2026-09-03** during the translation pass. Two senses, cleanly separable by context, and the corpus glosses the term itself: L216 *"die **Hauländer oder Collonisten**"*. Decisively, **L207 p1 uses both spellings on one page for the same people** — *"Pol Bauren und **Holländer**"* in the body and *"denen Bauen und **Hauländern**"* in the NB below it — so in estate contexts the two are one word. L101's *"1 **Holländer Hufe** … von den Besitzern zweyer **Holländer**"* is the same tenure sense under the other spelling. The military `Holländer` (539, L10, L286) and `Holland` the country are a different word and stay. |
| `Schlawen` ×6 | used exactly as a place; plausibly short for `Schlawenschitz`, but a writer may simply abbreviate |
| `Stege` (L180) | "Pochammer nach Stege" reads as a place. `Steegemann` does not occur in the corpus at all |
| `Wünster` ×3 | a person (`Hofrath Wünster`), spelled identically 3×. Left alone; belongs in the who's-who |
| `Franckfurten` (L277) | "Franckfurten u Main" = Frankfurt am Main. Root-only gives `Frankfurten` |

## §H. Canonical merges — APPLIED 2026-09-03

All seven applied, plus `Sakken` → `Sacken`. 64 substitutions, backup
`…cleaned.txt.bak7`, all regeneration checks green. Recorded in
`name_rulings.json` so they are never re-proposed.

**Locked, never to be re-proposed:** `Wrąbczyn` is a separate place from
`Trąbczyn`. `Swięcier` is a legitimate inflection of `Swięcia`. The adjectival
forms `Kalischen`, `Kalischer`, `Kaliszer` are correct German derivations of
`Kalisz` and were deliberately left alone — merging them would produce
non-German.

## §I. Names the edition uses but does not identify — 490

**Work through `name_review.csv`** — three columns: the name, where it occurs
(letter and page), and a blank third column for you. Write the corrected
spelling, or `OK` to confirm the current reading and retire the row. Then
`python name_review_sheet.py --read` reports what you filled in and `--read
--apply` writes it to the corpus. Rewriting the sheet preserves your answers, so
it can be regenerated as new names surface.

`unidentified_names.md` is the same material as a readable report, with a line of
context and the scan filename per row. Generated by `unidentified_names.py`. `whos_who.md` covers ~76 name tokens; the
corpus contains far more, and the gap is not obscure — `Grotowski`, `Lignowski`
and `Garczynski` each appear a dozen times with no entry at all.

| Tier | Count | What |
|---|---|---|
| §1 | 58 | **Recurring people, unidentified.** Most tractable — each recurs, so context accumulates across letters. Start here. |
| §2 | 8 | Type ambiguous — no clear person-or-place cue either way. |
| §3 | 59 | Minor places: estates, villages, small towns. Obvious cities excluded. |
| §4 | 365 | The long tail — in a name slot but occurring once or twice, so no statistical method can confirm them. |

Every row carries the letters, a context line, and the scan filename.

**Expect a proportion of §4 to be misreadings rather than unknown people** —
`Munduhr` and `Bretz` both looked exactly like this before they were read off
the page. Three are already visible: `Tastrow` (×2) is almost certainly
`Zastrow`; `Cöln` (×2) is the `Coeln` already ruled on; `Briechffa` is a
`Brzechsta` variant.

---

## Not open — recorded so it is not raised again

- `spelling_audit.md` §Checked and kept — 40 candidates rejected with reasons.
- `name_decisions.md` §Rejected — 16 proposals you overruled.
- `name_decisions.md` §Dropped as seeds — `Werthe`, `Wirth`, `Brieten`,
  `Bedeutung`, `Eines`, `Inneres` are not names.
- Scan-based re-transcription: **abandoned.** The scans are ~162 DPI (median
  1339×1644), roughly half the archival minimum, and both Opus 5 and Sonnet 5
  produced text materially worse than the existing transcription — inventing
  `Slawick` for `Hawich`, `Perz-Fructor` for `Ober-Inspektor`. Evidence in
  `retranscription-opus/`, `retranscription-sonnet/`, scored by
  `compare_pilot.py`. Revisit only if higher-resolution scans become available.
