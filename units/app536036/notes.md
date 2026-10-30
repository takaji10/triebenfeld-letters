# 53/6/0/-/36 (APP)

Two documents on two pages: two default judgments of the sitting of 1644 in
a book of decrees of the land court at Konin, Jerzy Chełmski against the
Trąmpczyński brothers and their mother, for notches cut in his wood at Łukom
and for timber felled there. Latin. Added on 2026-10-06 from the editor's
scan, transcription and English translation, in the second Prusimski-era
batch (`docs/PRUSIMSKI_ERA_PLAN.md`). Status `translated`. Built and verified
locally, **not published**; the editor reviewed the folds on 2026-10-07 (`intake/folds.json`).

## Provenance

Archiwum Państwowe w Poznaniu, fonds 53/6, unit 36: a volume the editor's
folder calls "Decreta [inducta] 1641-1644". The name of the fonds as the
archive gives it is not known here; the court is named from the text.

- **Scan.** One, `53_6_0_-_36_91328209.jpg`: an opening, leaf 641 verso and
  leaf 642 recto.
- **Pages.** `intake/build_pages.py --crop` cuts it at the fold (x 1803) into
  `0642_a1` and `0642_a2`, named after the leaf on the right, whole pages.
  Other entries stand on both pages and are not transcribed.
- **Leaf 612**, with the heading of the sitting, is transcribed by the editor
  but has no scan. Not a page; quoted in `about.md`; the ground of the date.

## Transcription and check (2026-10-06)

The editor's file had 18 marks of doubt in 317 words. All of it read against
the scan: 14 passages corrected (`intake/corrections.py`, logged). **The
other entries on the opening are the key**: they are default judgments in
the same set words and settle nearly everything. What changes the sense:

- The heading is "Con[tuma]ces", not "Conces[sionis]"; the entries below are
  headed "Contumax".
- "juridice clamatos et non comparentes ... in paena contumaciae admittente
  judicio eodem judicialiter condemnavit" (was "clamant et non Comparendum
  ... Admittendam ... Jud[icatum?] Cond[o]navit").
- "per immissionem Subditorum" (was "Subactorum"): their subjects.
- "Dominam Reformatoriam et Advitalem" (was "Reform[atricem] et
  Aduct[ricem]"): the widow's dower and life interest.
- "Quod sibi ... fundo intacto pensat" (was "eundem siti ... in [t?]acto").
- "educto officio Succamerali eadem signa luitis paenis annihilent".
- "personaliter stans ... palam Recognovit se Citationem ratione
  praemissorum editam Feria secunda proxime praeterita in Curia Citatorum".

Left as the editor has them: "filiis" (the scan may have "filios"),
"Koelmarek" (it may be "Kaczmarek"), "tanq[uam]". One doubt kept:
"a[ssignatis?]".

## The documents

Two, one for each entry (the editor's ruling of 2026-10-06). Page `0642_a2`
carries the end of 1 and all of 2. `doc_type: decree`, Latin, place Konin,
estates lukomia and trabczyn. Dated by the sitting, year only (`rulings.yml`,
`dates: sitting:`): it opened on the Monday after the octave of Corpus
Christi 1644, 6 June.

The editor's outline called the first a "concession"; it is a default
judgment. The boundary decree of 1775 (Konin Gr.145) cites suits of 1644
between the same families at Pyzdry over notches and mounds; whether these
two entries are among the ones it cites has not been worked out.

## Translation (2026-10-06)

The editor's English, revised (`intake/translation/build_docs.py`): its
notes had marked every doubtful word, and with the doubts settled most
sentences changed. `FIXES` has each passage as it stood and as it stands.
Kept: the editor's terms (General Royal Messenger, the Honest, the Worthy,
Sub-chamberlain, "on this side or beyond"). Two of 26 notes kept. The
glossary's "administratrix" and "conductrix" rested on the misread words.

check_translations.py: 2 rows, none a fault.

## Summaries and claim check (2026-10-06)

Two summaries, German first (`intake/summaries_draft.py`), 13 statements, all
supported (`intake/claim_check.yml`).

## Authorities (2026-10-06)

- The Chełmski family is now a curated entry in `reference/people.yml`
  (key `chemski`, the one the name catalogue had made): it finds the Polish
  and Latin forms (Chełmskiego, Chełmscy, Chełmsky), which the catalogue's
  pattern did not. This raises its count in Konin Gr.145.
- New: the Trąmpczyński family (`trampczynski`), matched only in these two
  documents, because "Trąpczyński" is also the adjective of the place.
- Places matched: Trąbczyn, Łukom. Not indexed: Karmin, Słończyce, the
  messengers.

## Still to do

- Publishing, at the editor's word. (The folds are the editor's: reviewed on
  the fold page on 2026-10-07, 1 scan(s), 1 of them turned; saved in
  `intake/folds.json` and the pages cut again from it.)
- The editor's look at the revised English.

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

The first entry begins a third of the way down leaf 641 verso, under its heading, and ends with one line at the top of leaf 642 recto. The second follows it there in eight lines. The rest of both pages belongs to other entries, which are not transcribed. The Latin is heavily abbreviated; square brackets in the transcription show letters that were supplied. 

The entries have no date of their own. The heading of the sitting stands on leaf 612, which the editor transcribed but which is not among the scans: "Actum in Terminis Terrestribus Particularibus Coninensibus feria Secunda post Octavas Festi Sacratissimi Corporis Christi proxima Anno Domini Millesimo Sexcentesimo Quadragesimo Quarta in Conin Celebratis". That is: done at the particular land court terms of Konin, held at Konin, on the Monday after the octave of Corpus Christi 1644, which was 6 June. The year of the documents is taken from this heading.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Scans

The archive supplied one image, which shows two facing pages of the bound volume. It was cut at the fold into two pages. Both are kept whole, although other entries stand on them above and below these two.

### Transcription

The editor transcribed the two entries and supplied them by paragraph, not line by line, with many marks of doubt: the hand is small and abbreviates nearly every word. The editor also transcribed the heading of the court's sitting from leaf 612. That leaf is not among the images, so the heading is quoted in the description of this holding and is not included.

### Check against the scan

An AI model (Claude) read both entries word for word against the scan and corrected fourteen passages. The other entries on the same two pages are judgments of the same kind in the same set words, and they settled nearly every doubt. Three corrections change what the entries are taken to be. The heading reads "Contumaces", in default, and not "Concessionis". The closing words are those of a default judgment: the defendants, called and not appearing, are condemned in the penalty of contumacy. And it was the Trąmpczyńskis' subjects, not agents, who were sent into the wood. One mark of doubt remains, and in three places the editor's reading stands because the scan does not decide. Each change is logged with its reason.

### Division and dating

Each entry is a document. Neither has a date of its own. Their year is taken from the heading of the sitting they belong to, which opened on 6 June 1644; the day of these judgments within the sitting is not known.

### Translation

The English is the editor's own translation. It had been made from the first reading of the Latin, and its notes marked each place where that reading was in doubt. It was revised wherever the corrected Latin required it, which is in most sentences; the editor's terms and wording are kept where the Latin under them did not change. Two of the editor's twenty-six notes are kept. The others discussed readings that are now settled. An automatic check compared the terms of the two texts.

### Summaries

The summaries were written in German from the corrected Latin and translated into English. Each of their thirteen statements was then checked against its document. All held.
