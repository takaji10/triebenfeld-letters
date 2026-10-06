# 53/6/0/-/40 (APP)

One document on five pages: the "Decretum Locationis" of the land court at
Konin, 26 January 1728, Franciszek and Józef Ścibor Chełmski against
Krzysztof Prusimski, his son Antoni and their people, sending a commissioner
onto the disputed ground. Latin. Added on 2026-10-07 in the second
Prusimski-era batch. Status `translated`. Built and verified locally, **not
published: the editor approves or moves the fold first**
(`review/app536040/folds/`).

## Provenance and pages

Archiwum Państwowe w Poznaniu, fonds 53/6, unit 40: "Decreta [inducta]
1722-1780". The cover label in the folder (`Image00001.jpg`) reads "Z. KONIN
43", the volume's older number; it is not a page and is not used.

- `368.jpg`, `372.jpg`, `373v.jpg`: single pages, copied whole as `0368_a2`,
  `0372_a2`, `0374_a1` (leaf N recto is `<N>_a2`, leaf N verso `<N+1>_a1`).
- `372v-373.jpg`: an opening, cut at the fold (x 2650, a first proposal;
  the automatic finder was unsure here) into `0373_a1` and `0373_a2`.
- Other entries stand on leaves 368, 372 and 373 verso; not transcribed.

## Check (2026-10-07)

All five pages read against the scans: 29 readings corrected
(`intake/corrections.py`, logged). The hand is clear and the editor's text
was close. What changes the sense is listed in `process.md`. One doubt kept:
"devehi[?]". Left as the editor has them: "filiis quibus" (the small word
after "filiis" is not surely "quibus"), "Zdzęnicki", "ac aliorum actorum"
(so written, where "citatorum" would be expected), and spellings.

## The document

One document; the heading of the sitting (leaf 368) is its first page.
`doc_type: decree`, Latin, place Konin, estates lukomia and trabczyn. Dated
by the sitting, to the day: Monday after Septuagesima 1728 = 26 January
(`rulings.yml`).

**The decree of 1775 cites it** (Konin Gr.145, English pages 31, 75, 109,
121): "the Konin land court decree ... on Monday after the Sunday
Septuagesime in 1728, concerning that same stawisko ... with a field session
assigned to the ground", and "the second [inquiry] conducted in 1728 by the
Kalisz land court authority". The stawisko is not named in this decree; it
speaks only of ground belonging to Łukom.

The field hearing was set for the Monday after Misericordia Sunday, 12 April
1728.

## People

- **Krzysztof Prusimski and the elder Antoni**: new entry
  `prusimski-krzysztof`, matched as "Prusimski" in this document only; the
  Starost's entry (`prusimski`) is shut out of it. The decree of 1775 calls
  Krzysztof the Starost's grandfather and the elder Antoni his uncle. The
  editor's register adds Paweł Prusimski between them (from Konin Gr.136).
- The Chełmski family entry takes Franciszek and Józef.
- Not indexed: Wojciech Biskupski the commissioner, Konstanty Marszyński,
  the six retainers.

## Translation, summary

- English: the editor's, 16 changes (`intake/translation/build_docs.py`).
  The "[T.N.n]" marks and their notes are left out.
- Summary: German first, 12 statements; one weakened in the claim check
  (the hay "taken", not "carried off to Trąbczyn").
- check_translations.py: 2 rows, none a fault.

## Still to do

- The editor's approval of the fold, then publishing at their word.
- The editor's look at the changes to their English.
