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
  (`docs/archive/PRUSIMSKI_QUESTIONS.md`); `about.md` and `process.md` say so, and
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
- Publishing, at the editor's word. (The folds are the editor's: reviewed on
  the fold page on 2026-10-07, 3 scan(s), 3 of them turned; saved in
  `intake/folds.json` and the pages cut again from it.)

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

The entry fills leaves 121 to 123. **Its middle is not transcribed**: after the malthouse, a third of the way down leaf 121 verso, the scans have a numbered description of the village houses, one by one, which runs over the whole of leaf 122 to the top of leaf 122 verso. That part is in neither the transcription nor the translation, and leaf 122 is not shown. The text takes up again at "Wieś Nowa". The Polish is the building language of the time and is given as the editor transcribed it. The Latin record at the end is abbreviated; the transcription fills the abbreviations out.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The archive supplied three images: one single page and two images of two facing pages each, which were cut at the fold. One of the five pages, leaf 122 recto, carries none of the transcribed text and is not shown.

### Transcription

The editor transcribed the entry and supplied it by paragraph, not line by line. The transcription leaves out the description of the village houses in the middle of the entry: the rest of leaf 121 verso after the malthouse, all of leaf 122, and the top of leaf 122 verso.

### Check against the scans

An AI model (Claude) read against the scans the heading, the count of people on leaf 122 verso and the whole of leaf 123, and corrected sixteen readings. The description of the manor buildings on leaf 121 and at the top of leaf 121 verso, about 540 words, was not compared. Corrections that change the sense: an unknown word, "zelaga", is "żelaza", ironware; two figures in the count are 8, not 6; the woods reach "above Szetlewek", the neighbouring estate; and the gap left before the messenger's name holds his office. Each change is logged with its reason.

### Division and dating

The entry is one document. It is dated 12 July 1754, the day the report was entered at Konin; the inspection itself was made on 9 July.

### Translation

The English is the editor's own translation and was not made again. It was changed in six places where the text had been corrected. The editor's notes on terms are kept as translator's notes; three that commented on readings since corrected are left out. A line in square brackets marks the place of the part that is not transcribed.

### Summary

The summary was written in German from the Polish and Latin and translated into English. Each of its ten statements was then checked against the document. All held.
