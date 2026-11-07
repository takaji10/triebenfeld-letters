# Translation log — Rusiński 1947

Decisions applied (see `translation_plan.md` §9): British (D2),
"Olęder(s)" retained (D3), ANEKS I skipped (D6); defaults for D1/D4/D5.

## T1 — front matter (DONE)

Scope: title page, printer's imprint, table of contents, the list of
abbreviations (A. Sources with translated expansions + call marks
verbatim; B. Literature copied verbatim — citations keep their
original languages). Translator's preamble added at the top of
`english.md` stating all conventions.

Checker `tr_t1.py` (kept for re-runs): per-block label sequence,
per-block digit-multiset equality (separator-insensitive), 37-siglum
inventory equality, 19 call marks, bibliography verbatim-identity.

Findings fixed during the check:
- glosses initially repeated years already carried by the retained
  Polish source titles (Tod. 89 / Tołł. / Tp. 75 / Tp. 89,90 /
  Lustr. pruska 1664 / MP) — gloss years dropped, titles keep them;
- the print's truncated year form `1917—8` must NOT be expanded
  (generalizes to: preserve the print's number formatting quirks);
- checker-side: sigla must be matched on word boundaries and counted
  from `[p. I]` onward (the translator's note's example sigla would
  otherwise pollute the counts); call marks matched
  whitespace-tolerantly (a wrap inside a call mark is legitimate).

Rule amendments for the later stages (from these findings):
- R-N1: a gloss may not repeat a numeral already present in the
  retained original text it glosses;
- R-N2: the print's number-form quirks (truncated years like
  1917—8, idem forms) carry over as printed.

Next: T2 (introductory remarks, pp. 1–11, and Chapter I–II pp. 12–26
incl. TABELA I).
