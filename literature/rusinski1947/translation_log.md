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


## T2–T6 — the body, annexes II–III and plates (DONE)

Method: five parallel translation passes (one per stage), each working
block-by-block from `original.md` under the full ruleset brief
(terminology table, mechanical number rules, sigla/citation rules,
quotes policy, British register). Parts assembled in order into
`english.md` by `tr_assemble.py`; the ANEKS-I zone replaced by the
bracketed not-translated note (D6) at `[p. 123]`.

Verification (`tr_full.py`, the standing battery):
- label sequence 135/135; **footnote refs 0 diffs; defs 0 diffs**
  (label multisets per page, incl. the ditto refs);
- per-page digit multisets 0 diffs (after separator normalization,
  decade-form tolerance and a split/merge reconciler);
- per-page fraction-glyph multisets 0 diffs; zł/gr token counts 0 diffs;
- siglum inventory equal (garble-tolerant patterns: ĄW., A.M, Rel.
  Posn, K]., 'T'ol.);
- table regions identical (rows/cols: p. 26 6×4, p. 61 34×5,
  p. 64 13×6, p. 66 10×5).

Adjudicated deviations, encoded as the checker's whitelist (each
traceable to an agent report or a pixel check):
- **Fraction-garble normalizations** (pp. 67–79, 98–114): the print's
  OCR-mangled fraction forms ('71/,' '11/2' '*/.') rendered as glyph
  fractions (7½, 1½, ¼ …), corroborated where possible by context
  (e.g. def 76-1 'pół huby'; fn 98-4's 27¼→31¾);
- **def 69-1** (Folsztyn hearth lists): reconstructed so the printed
  totals (27; 27½) tally — flagged as conjectural in the agent report;
- **Junk-marker drops** ('1'=i, '7'=Z, the garbled '20' of p. 148,
  the '(Hb gr)' garble rendered by sense): the superscript-note
  markers that the OCR printed as bare digits;
- **ANEKS III clause numbers 2–9 and 26 restored** (pp. 152, 154):
  the print numbers its clauses; the OCR lost those numerals — the
  reconstruction follows the print's own sequence;
- **p. 58 def 58-5**: the print reads '1 złotego 15 groszy'
  (pixel-verified: I + złotego + 1 + 5groszy); the OCR had split
  '15' into '1'+'5' and garbled 'Z reguły' as '7. reguły';
- **p. 17's stray '|' noise line** dropped (no content, no digits).

Agent-flagged items carried into the text as printed (for the final
human pass): the bare superscript digits that ARE the print's marker
positions (kept, e.g. 'hamry 1 kuźnice'); the print's own errors
('Ol. Róża (founded 1024)' [1624], '97.5557', '1 : 57,6001'); garbled
bibliographic strings inside citations kept verbatim; the p. 97
German petition reproduced verbatim with bracketed English; the p. 110
lost rye figure left as '[—]'/'?' placeholder rather than invented.

Sanity passes after the battery: zero leftover Polish sentences in
the covered zone; Americanisms swept (one 'organize' → 'organise');
the ANEKS-I note and plates note in place.

Remaining for the final human pass (not blockers):
- the bracketed conjectures the agents marked ([?], '[—]', sense
  renderings of garbled quote tails) — an editor's eye on ~20 spots;
- optional: reconcile the fraction normalizations against pixels one
  by one (currently context-corroborated only);
- 'złotys/złoty' plural style could be unified to 'zł' symbols.

DELIVERABLE STATE: `english.md` = complete translation of everything
except the ANEKS I tables (D6). ~447 kB; the battery is ALL PASS.
