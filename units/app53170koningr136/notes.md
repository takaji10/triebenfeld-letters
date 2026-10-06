# 53/17/0/-/Konin Gr.136 (APP)

One document on four pages: the inspection of the Trąbczyn estate of 9 July
1754 for the widow Katarzyna Prusimska, with the court messenger's report of
12 July. Polish with Latin. Added on 2026-10-07 in the second Prusimski-era
batch. Status `translated`. Built and verified locally, **not published**.

Everything about how it was made is in the docstring of `intake/holding.py`
(one script for all the steps: `courtbook.holding_main`).

## What is not in it

- **The middle of the entry**: the numbered, house-by-house description of
  the villages (rest of leaf 121 verso, all of leaf 122, top of leaf 122
  verso) is in neither the editor's transcription nor their English. Built
  without it at the editor's instruction to hold questions for the end
  (`docs/PRUSIMSKI_QUESTIONS.md`); `about.md` and `process.md` say so, and
  the English has a line in square brackets at the place. Leaf 122 recto
  (`0122_a2`) is cut and set apart.
- **Not compared with the scans**: the manor buildings on leaf 121 and the
  malthouse on leaf 121 verso (about 540 words).

## The check

16 readings corrected (`ROWS` in `intake/holding.py`, logged): "żelaza" for
"zelaga"; 8 for 6 twice; "Szetlejowkiem"; in the Latin record "Ministerialis
Regni Generalis" in the gap the editor left, "notus sanus existens",
"Generosis", "personaliter ... tum ... tum". Left as the editor has them:
"Szeptycki [Szepczyński]" (the bracket is the editor's), "Hatew",
"advitalitialis".

## People

- Paweł Prusimski: new entry `prusimski-pawel`, this document only. The
  record calls him the King's chamberlain and heir of Trąbczyn, "non pridem
  vita functi". How he stands to Krzysztof (1728) and to the Starost is not
  said in the documents here.
- Katarzyna Prusimska's entry takes this document; the entries of Michalina
  and of the Starost are shut out of it.
- New kind of document: `report` (a messenger's relatio), labelled in
  `site/_data/i18n.yml`.

## Still to do

- The editor's answer on the untranscribed middle.
- The editor's approval of the folds, then publishing at their word.
