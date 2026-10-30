# 53/6/0/-/40 (APP)

One document on five pages: the "Decretum Locationis" of the land court at
Konin, 26 January 1728, Franciszek and Józef Ścibor Chełmski against
Krzysztof Prusimski, his son Antoni and their people, sending a commissioner
onto the disputed ground. Latin. Added on 2026-10-07 in the second
Prusimski-era batch. Status `translated`. Built and verified locally, **not published**; the editor reviewed the folds on 2026-10-07 (`intake/folds.json`).

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

- Publishing, at the editor's word. (The folds are the editor's: reviewed on
  the fold page on 2026-10-07, 4 scan(s), 4 of them turned; saved in
  `intake/folds.json` and the pages cut again from it.)
- The editor's look at the changes to their English.

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

The heading of the sitting stands at the top of leaf 368. The entry begins a quarter of the way down leaf 372, under its own heading, fills leaves 372 verso and 373, and ends in nine lines on leaf 373 verso. Other entries stand on the first, second and last of these pages and are not transcribed. The Latin is abbreviated in the manner of the court books; the transcription fills the abbreviations out. A clause left out by the clerk and added at the foot of leaf 372 with a mark is given where the mark places it.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The archive supplied five images: three single pages, one image of two facing pages, and the label on the cover of the volume. The image of two pages was cut at the fold; the single pages are used as they are; the label is not a page. All five pages are kept whole, although other entries stand on three of them.

### Transcription

The editor transcribed the heading of the sitting and the entry and supplied them by paragraph, not line by line, with the clerk's abbreviations filled out and eleven marks of doubt.

### Check against the scans

An AI model (Claude) read all five pages word for word against the scans and corrected 29 readings. Ten of the eleven doubts are settled; one stays. Most corrections are small. Those that change the sense: the sons are cited "with their parents, the servants and subjects with their lords", a set phrase, where the first reading had a decree. The shingles burned were "a hundred sixties", six thousand; the hay was taken "in no small number of cartloads", and its loss caused "the loss of livestock". The court, "deciding" the plaintiffs' cause, finds one thing, that a commissioner must go onto the ground. Each change is logged with its reason.

### Division and dating

The entry is one document, with the heading of its sitting as its first page. The heading gives the day: the Monday after Septuagesima Sunday 1728, which was 26 January.

### Translation

The English is the editor's own translation and was not made again. It was changed in sixteen places where the Latin had been corrected. The editor's notes and glossary are not used here. An automatic check compared the terms of the two texts.

### Summary

The summary was written in German from the corrected Latin and translated into English. Each of its twelve statements was then checked against the document. One was weakened, because the word for what was done with the hay is not surely read; the rest held.
