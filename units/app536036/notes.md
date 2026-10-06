# 53/6/0/-/36 (APP)

Two documents on two pages: two default judgments of the sitting of 1644 in
a book of decrees of the land court at Konin, Jerzy Chełmski against the
Trąmpczyński brothers and their mother, for notches cut in his wood at Łukom
and for timber felled there. Latin. Added on 2026-10-06 from the editor's
scan, transcription and English translation, in the second Prusimski-era
batch (`docs/PRUSIMSKI_ERA_PLAN.md`). Status `translated`. Built and verified
locally, **not published: the editor approves the fold first**
(`review/app536036/folds/`).

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

- The editor's approval of the fold, then publishing at their word.
- The editor's look at the revised English.
