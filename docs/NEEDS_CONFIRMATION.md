# Needs confirmation

Questions still open, gathered from the holdings' notes, rulings and the
reference registers (2026-10-02). When one is settled, record the decision
where it belongs (`units/<slug>/rulings.yml`, `reference/`, the unit's
`notes.md`, the changelog) and take it off this list. Nothing here is a
reason to change the text without the editor.

The `review/<slug>/` files named below are generated and not in the
repository; they are on the working machine.

## Waiting on material

- **I. HA GR, Rep. 7 C, Nr. 3709** is in the edition as scans only. It waits
  for the editor's transcriptions. Then: divide it into one document per
  letter, set the office's writing apart (as in III. HA MdA, III Nr. 12765;
  see `docs/GOVERNMENT_FILES.md`), read, translate and summarise.
- **Rescans, Oe 1 Bü 9454**: letter 245 (both pages) and letter 289 page 1,
  requested in `review/oe1bu9454/rescan_request_final.md`. The trial reading
  of 245 (`review/oe1bu9454/trial_245.csv`, 101 rows) waits for them.
- **Two eras are named and empty** (`reference/eras.yml`): the
  Trąbczyn–Łukom boundary dispute (c. 1589–1788) and the
  Prusimska/Miączyńska restitution (1807 onward).

## Readings, Oe 1 Bü 9454

The editor could not settle these from the page (2026-09-28). They stay as
written until there is a witness or a better scan.

- Abbreviations and names: H. C. R. R. N Weigelts (64; the editor sees
  perhaps H. C. K. K. N.), H. R. R. Falz (207; Regierungs Rath not supported),
  H. z. M. v. Kirche[?] (8; perhaps Kircheisen), Gl. Listog[?] (56; perhaps
  L'Estocq), B. R. Glenck, Gen. B. at Jena (20), der bidere B (288).
- Unread words: Lottom[?], Stache[?], Ternuis[?], Rewen[?]; thenigtes (144).
- Places read tentatively, still marked: Neasal[?] (66; perhaps Neusalz,
  named in the same letter), Neufallen[?], Sa[?]en.
- **Rough transcriptions.** 13 letters are still largely an uncorrected
  machine reading, and their pages say so: 17, 21, 33, 36, 38, 46, 114, 138,
  161, 176, 217, 245, 296 (`rulings.yml`, `rough`). Take a letter off when it
  has been re-read.
- **Correspondents not known.** No signature or address to go on: 14, 20,
  72, 101, 109, 122, 132, 135, 150, 179a, 186, 202, 207, 224, 257, 285.
  Recorded in `correspondents.json`; do not rerun `derive_correspondents.py`.
- 252 `[?]` marks remain in the transcription: names, figures and garbled
  phrases that need the page.

## Readings, the other holdings

- Words left as written for want of a witness, one list per holding, in
  `review/<slug>/unresolved.md`: Oe 1 Bü 9454, III. HA MdA, III Nr. 12765,
  I. HA GR, Rep. 7 C, Nr. 3705, Oe 1 U 199, 53/71/0/-/57.
- **Oe 1 Bü 14526**: 5 of the 158 unmarked suspicions are open
  (`unmarked_suspicions_review.csv`).
- **III. HA MdA, III Nr. 12765**: 94 readings proposed by the translator, none
  applied, most the same words as in `unresolved.md`. About a dozen chancery
  formulas ("erwiedere ich auf", "Zurückgabe der Beilagen", "geehrtesten",
  "behalte mir vor") would be worth a spot sheet if the drafts are to be
  improved; applying any makes those documents' English stale.

## Identifications

People (`reference/people.yml`, `open_questions`):

- Kaleschke / Koleschke, the actuarius of the Stillfried court: neither
  spelling is asserted.
- Michaelis: the merchant and the Hof Fiscal may be one man or two.
- Prinz George: which house he belongs to is not stated in the letters.
- Settlers doubled between a German deed and a Polish protocol (as Celmer and
  Zelmer): not checked beyond the known case.

Places (`reference/places.yml`, `open_questions`):

- Harbultowitz, among the estates of the majorat in Oe 1 U 199: not
  identified.
- In Oe 1 Bü 9454: Neustadt (which one is not clear), Wilhelmsruh (a manor by
  Breslau, no Polish name found), Petersdorf (too common a name to place).
- Szetlewek and Szeklejówek: a tentative identification, not matched.
- Santomist (9454, letter 179) taken to be Zielomyśl: probable, not certain.
- Olisnice in the consistency register: the same place as Olesnica, or a
  separate settlement.
- Guhrwitz (Górzyce): Stillfried's ownership in 1805 is unconfirmed.
- Łazińsk / Łaziny: whether they name Trąbczyńskie Stare Olędry or a part of it.
- The Peyserschen Hauland: one settlement, or the district's colonies taken
  together.
- To split when the documents arrive: Łukomskie Olędry (two places under one
  name) and Trombschino-Hauland (now matched to Trąbczyn).

## Translations

All 421 English translations are machine drafts (`status: draft` in
`site/_data/translations/`); none has been read against the manuscript. Each
holding's `review/<slug>/translation_review.csv` lists the rows to rule on.
The six documents without English have no text to translate: Nr. 3709, and
in Oe 1 Bü 9454 the skipped number 9 and the missing 121, 181, 225, 293.

## Before the site is shared widely

- **Scan rights.** Confirm with each archive (HZAN Neuenstein, GStA PK,
  Poznań) that its images may be published, and in what form of credit. The
  Licences, credits and privacy page (`site/rights.md`) credits each one and
  claims no permission; once an archive grants it, say so there.
- **The holder's name.** The licences and that page name `takaji10`. To use a
  full name, change `site/_data/rights.yml` and `LICENSE` together.
