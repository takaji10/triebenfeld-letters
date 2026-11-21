# Rusiński 1947 — English translation plan and ruleset

Source of truth: `original.md` (the finished transcription; ~67,300
words incl. the annexes). Target deliverable: `english.md` in this
folder, same structure, translated 1:1 against the source blocks.

## 0. Invariants — what must NOT change

These make the translation checkable by script; every item has an
automated check in the QA battery (§7).

1. **Numbers are sacrosanct.** Every digit sequence in the source
   must appear in the target with the same digits (after the
   separator conversion of §4). No rounding, no "about", no silently
   repaired arithmetic. The known print-internal discrepancies
   (Δ1/Δ9/Δ12 column sums; p. 23's 15.831 vs 15.840; the b-RAZEM
   484/538 pixel question in ANEKS I) travel into the translation
   exactly as the print has them — flagged in the transcription
   notes, not "fixed" in translation.
2. **Page structure is sacrosanct.** `[p. N]` markers and the annex
   `<!-- annex sheet NNNN -->` markers survive verbatim; every page
   block translates to one block; footnotes stay under their page
   (the per-page note rule), same note counts per page (691 refs /
   685 defs, incl. the 5 legitimate ditto refs).
3. **Source sigla never translate.** AW., Rel. Posn., Rel. Cost.,
   Decr. Posn., Inscr. Valc., Dom. P., Kl., Tp./Tod. 89/90, MP, MG,
   MGd, VO, AGH, AM., Szk., Kat., Q, Verz/1800, TW etc. stay
   letter-for-letter. The abbreviations key (front matter) gets a
   translated rendering of the *expansions*, sigla untouched.
4. **Proper names keep Polish spelling.** Personal names (Bniński,
   Miaskowski, Czernkowski…), settlement names (Ol. Karpicko,
   Radoszkowskie Ol., Folsztyn as printed), estates, rivers, offices.
   No Germanization, no Anglicization, no diacritic stripping. First
   mention may add nothing; the print's own forms ("Ol.", "Olędry")
   are part of the name and are handled by the glossary, not renamed.
5. **Quoted archival text stays in the original language.** See §6.
6. **Tables translate cell content only** — structure, columns,
   dashes, note refs ([^61-1] etc.) stay as-is; numbers under rule 1.

## 1. Scope and staging

Work proceeds block-by-block (each `[p. N]` block is one unit), in
this order, with a battery run after each stage:

| Stage | Content | ~words |
|---|---|---|
| T1 | Front matter (title pages, TOC, abbreviations, preface, intro) | 2,700 |
| T2 | Ch. I–II + TABELA I (pp. 1–26) | 9,700 |
| T3 | Ch. II–III (pp. 27–54) | 11,700 |
| T4 | Ch. IV (pp. 55–88) | 14,300 |
| T5 | Ch. IV–V (pp. 89–122) | 14,100 |
| T6 | ANEKS II–III (printed sources, pp. 145–150) | 4,000 |
| T7 | ANEKS I (pp. 123–144, tables + notes) | 10,800 |
| T8 | Plates/captions (p. 157 f.) | 40 |

Rationale: T1–T5 establish the terminology while the prose is still
fresh; the annex tables (T7) are the most mechanical and come last,
after the glossary has hardened. ANEKS I note: the transcription
carries the pixel-reconciled draft tables (column-sum deltas
documented in notes.md); if the editor's edited `aneks_i.xlsx`
arrives, fold it in and re-run the transcription battery BEFORE T7
starts.

## 2. Terminology glossary (the working core)

Fixed renderings, applied mechanically; the glossary grows during
T1–T2 and freezes at the end of T2. Stemming forms are handled by
rule (Polish is inflected; English renderings get natural inflection).

| PL | EN (fixed) | Note |
|---|---|---|
| olędrzy, osady olęderskie | the Olęders, Olęder settlements | keep the ethnic term (from nl. * Hollander*); "Hollanders" misleads; "Hauländer" is the German term, only in German-context quotes. First use: "the Olęders (Olęder settlers; German *Hauländer*)" in T1 |
| olędry (pl. tantum, the settlements) | an Olęder settlement / the Olędras (settlement name) | settlement *names* like "Ol. Nowe Dwory" render per §5 |
| huba | huba (Hufe, hide) | keep + gloss at first use; "full huba / half huba" for pełna/półhuba |
| dym | hearth (dym) | the fiscal unit; "hearth" with the Polish in brackets at first use; "dymy" lists in tables → "hearths" |
| włóka | włóka (Włóka ≈ 16.8 ha? no —) | keep + gloss: "włóka (c. 17–19 ha, local measure)" — exact gloss from the book's own data (TABELA: 30-morgowa włóka); use the book's figures, not ours |
| morg | morg (Morgen) | keep |
| łokieć, pręt | ell, rod | the TABELA II note's chełmiński ell figures stay numeric |
| tynf | tymf (tynf) | the debased coin; keep "tymf" (English numismatic form), gloss at first use |
| talar, dukat, złoty (zł), grosz (gr), szeląg | thaler, ducat, złoty (zł), grosz (gr), szeląg | currency symbols zł/gr stay as symbols |
| czynsz | rent (cash rent) | context-checked; never "custom" |
| powinności | obligations / dues | by context: robocizny = labour dues |
| robocizna | labour due(s) | |
| szarwark | corvée (szarwark) | |
| chałupnik, komornik, zagrodnik | cottager, lodger, smallholder | chałupnik=cottage-dweller w/o land; komornik=lodger; fixed per first-use table |
| sołtys, ławnik, wójt | village headman (sołtys), lay assessor (ławnik), reeve/vogt (wójt) | |
| dziedzic, pan | the lord / the estate owner | "dziedzic" = the proprietor; never "heir" blindly |
| folwark | manor farm (folwark) | |
| grunta | land(s) | |
| serwituty | servitudes (rights of use) | |
| wolnizna | free period (wolnizna) | the rent-free years |
| lokacja, lokować | locatio / to locate (settle) | "locate" in the settlement-history sense |
| przywilej | charter (przywilej) | settlement charters; "privilege" avoided except in quote-glosses |
| wilkierz | wilkierz (village by-law) | |
| oblaty | enrolments (oblaty) | the register copies |
| księgi grodzkie / ziemskie | the grod (castle-court) books / the land-court books | gloss at first use |
| starostwo, królewszczyzny | royal domain (starostwo), royal estates | |
| majętność | estate (majętność) | the private complexes: "the Wieleń estate" |
| przymus mlewa | milling monopoly (przymus mlewa) | |
| propinacja | propination (the liquor monopoly) | |
| karczma, karczmarz | inn, innkeeper | |
| gwara/ustalenie "okolica" | the Okolica (settlement form) | keep as a settlement-type term |
| klucz | (estate) complex / klucz | context |
| dym pospolity | hearth tax | |
| pogłówne | poll tax | |
| hyberna / subsidium charitativum | hyberna (winter levy), the charitable subsidy | |
| kanon, kwatera | canon (tax unit), quarter (kwatera) | context-checked in ch. V |

Prohibited-varying: the same Polish term must map to the same English
term everywhere (checked by script, §7).

## 3. Sigla, citations, cross-references

- Sigla as-is (invariant 3). The front-matter abbreviations list is
  translated around them.
- "s. 39" (page refs) → "p. 39"; "s. 84, przyp. 258" → "p. 84, n.
  258" (the print's own global note numbering — kept as printed, not
  renumbered to our per-page labels).
- "w. XVII" → "the 17th c."; "w. XVI/XVIII" likewise; "1. połowa
  XVIII" → "first half of the 18th c."; decades "latach
  osiemdziesiątych w. XVIII" → "the 1780s".
- Archival units: "fol. 302", "vol. III", "nr 638", "r. 1790"
  → "fol. 302", "vol. III", "no. 638", "of 1790".

## 4. Numbers, dates, measures — the mechanical rules

1. **Thousand/decimal separators flip** (Polish → English
   convention): `13.737 dymów` → `13,737 hearths`; `6,05 osób` →
   `6.05 persons`; `16.303` → `16,303`; decimals keep their digits
   (`1,97 g.` → `1.97 g`). Applied by script, then human-checked on
   the fraction pages (pp. 24–25, 61–64, 99, 107–109).
2. **Fractions stay as printed glyphs**: 20½, ⅑, ½, 2⅚ — the
   transcription's unicode fractions carry over unchanged.
3. **"zł 20 gr" patterns**: `88 zł 20 gr` → `88 zł 20 gr` (symbols
   kept, order kept).
4. **Dates**: `w r. 1690` → `in 1690`; `r. 1663—74` → `1663–74`;
   `23 X 1778` → `23 October 1778`; `10 TX 1777` stays as the
   archival citation form (sigla-adjacent); `za czasów Augusta III`
   → "under Augustus III" (ruler names anglicized: Fryderyk Wielki →
   Frederick the Great, etc.).
5. **Measures**: conversions NEVER added inline. If a conversion
   gloss is wanted, it goes in a translator's note (decision D4).
6. **"około", "w przybliżeniu"** → "about/approximately" — allowed,
   but never attached to numbers that the print states exactly.

## 5. Names and settlement naming convention

- "Ol." = *olędry* in settlement names: keep the abbreviation form
  but gloss once in T1: e.g. "Ol. Karpicko (the Karpicko Olęder
  settlement)" on first mention; thereafter the source's own usage
  maps as: "Ol. X" → "Ol. X" (unchanged, treat as proper name) —
  EXCEPT where the sentence grammar needs English, then "the Olęder
  settlement of X".
- "Holendry X" (the older settlement names, e.g. Holendry
  Nadziejewskie) stay as names: "the Holendry Nadziejewskie".
- Personal names with titles: "pan" in quotes/archival text stays
  period ("Sir" is prohibited; use "the lord" or leave per §6).
- German institutional names in Prussian-period passages keep the
  German with an English gloss on first use (Amt Podstolitz,
  Netzdistrikt).

## 6. Quotations policy

The book quotes three registers: (a) 17th–18th-c. Polish archival
Polish (charters, wilkierze, manifesty), (b) German (petitions,
rescripts), (c) Latin tags (in assistentia, ad fiscum, competenti
domini sui).

- **(a) Archival Polish quotes**: translate into English INSIDE the
  running text/notes, and keep the original Polish verbatim in the
  SAME note following the translation, introduced as
  `[orig. …]`. Exception: quotes the print itself already summarizes
  or paraphrases translate without the original.
  *Alternative (simpler, less scholarly): translate all quotes, drop
  originals except where the print discusses the wording itself.*
  → decision D1.
- **(b) German quotes**: same rule as (a) (decision D1 covers both).
  The heavily degraded p. 97 petition keeps its "quote, corrected
  against nothing" status: translate with `[sic]`-marking preserved.
- **(c) Latin tags**: keep Latin, add a bracketed English gloss on
  first use only (`in assistentia [in the assistance of]`).
- Quotation marks: Polish „…” → English “…”; the transcription's
  „” glyphs convert mechanically.
- The print's own editorial insertions inside quotes ([...], (sic))
  stay as-is.

## 7. QA battery for the translation (scripts, per stage)

1. `tr_closure.py` — port of fn_closure: per-page ref/def sets must
   match original.md's sets 1:1 (labels unchanged).
2. `tr_numbers.py` — extract every digit-sequence (incl. fractions)
   from source and target per page; apply the separator rule; any
   mismatch = FAIL. This is the single strongest guarantee.
3. `tr_glossary.py` — glossary conformance: each PL stem maps to its
   fixed EN rendering; flag variant renderings.
4. `tr_sigla.py` — sigla inventory from source must appear in target
   unmodified, same counts.
5. `tr_names.py` — settlement/person name inventory (regex-built
   from the source) present in target.
6. `tr_structure.py` — page markers, sheet markers, table row
   counts, note counts per page identical.
7. Final read-through pass (human) with the notes.md traps list in
   hand (the p. 85/86 split, the note-overflow notes 38-3/116-5, the
   pp. 24–25 ladders).

## 8. Style register

- Scholarly but readable modern English; long Polish periodic
  sentences may be split — meaning-preserving, never re-ordered
  argumentatively. Technical-historical register of e.g. English
  agrarian-history writing (Meitzen/English Hufe-literature tone).
- Tense: present for the print's descriptions of sources ("the
  charter provides…"), past for historical events — mirroring the
  Polish where it does so.
- No contractions in the analytical text; quotes translate into
  period-plain diction, not fake archaism.
- Em-dashes/en-dashes per the print's ranges; Polish "tj.", "tzn.",
  "por.", "m.in.", "itd.", "nast." → "i.e.", "i.e.", "cf.", "among
  others", "etc.", "ff.".
- "dawne województwo poznańskie" → "the former Poznań voivodeship";
  administrative names (powiat) → "county (powiat)" first use, then
  "county".
- Editorial "[sic]" items in the transcription (e.g. "Tp. 72 [sic;
  TKS. 72]") stay exactly as bracketed.

## 9. Decisions (editor, 2026-11-07)

- **D1. Quotes:** default applied — Polish archival quotes translate
  only (originals dropped except where the print discusses the
  wording); the German petition keeps original + translation.
- **D2. English variety:** **British** spelling and conventions.
- **D3. "Olęder" terminology:** **keep "Olęder(s)"** as the ethnic
  term (first-use gloss in T1).
- **D4. Conversions:** default applied — metric/measure glosses at
  first use, from the book's own figures.
- **D5. Numeric discrepancies:** default applied — silent carry-over
  as in the transcription (documented in notes.md).
- **D6. ANEKS I:** **SKIP** — the annex tables (pp. 123–144) are NOT
  translated; `english.md` carries a bracketed translator's note at
  the ANEKS I position ("[ANEKS I: tables not translated in this
  edition]"), and stage T7 is dropped. ANEKS II–III (printed
  sources) still translate (T6).

## 10. Effort and product

~67,300 words; T1–T8 above. Products per stage: the translated
blocks appended to `english.md` + the stage's QA report; at the end:
`english.md`, `translation_log.md` (decisions + glossary v-final),
and the seven-script battery all green.
