# I. HA GR, Rep. 7 C, Nr. 3132

The Prussian ministers' file of February to June 1803 on the petition of
Antoni Prusimski, the former Starost, and the canon Xaver Jezierski, both at
Dresden, to be allowed home to South Prussia: eleven documents, the cover as
front matter. Added 2026-11-20 at the editor's word, branch
`trampczynski-family`; not yet published.

The archive's title, as the editor gave it: "Gesuch des v. Prusinski und des
Jesierski wegen Erlaubnis zur Rückkehr nach Südpreußen". The cover reads
"Acta betr das Gesuch des v. Prusimski und des Jezierski um Erlaubniß zur
Rückkehr in ihr Vaterland", "No. 5", "Südpr.", "den 19 Februar 1803".

## Provenance

GStA PK. The editor gave "I. HA Rep. 7 C, Nr. 3132"; written with GR, as the
siblings (the archive's label on the cover has "I. HA Geheimer Rat, Rep. 7 C
Südpreußen"). Slug `ihagrrep7cnr3132`.

Eighteen scans (Downloads\74344_Lacko\I_HA_Rep_7_C_Nr_3132), with the
editor's transcriptions of fifteen in `txt/`. 0003, 0017 and 0018 have no
transcription and are left out, unlooked-at (the editor: "leave them out. No
need to look at them"). 0001 is the cover; the rest are openings of the
file photographed whole, cut at the fold by `intake/holding.py --crop`
(courtbook.cut), the folds found by courtbook.find_fold and the page edges
set by eye to leave off the ruler; the editor checked them on the fold page
(`holding.py --sheet` -> `review/ihagrrep7cnr3132/folds/index.html`; their
saved file goes in with `python pipeline/intake/courtbook.py folds
ihagrrep7cnr3132 <file>`). The editor adjusted the folds of 0013 to 0016
and saved them (2026-11-20; `intake/folds.json`, applied with that command).
Eleven sides are blank or the archive's slip and are not staged (SKIP).
Since 2026-11-20 they are not cut out at all (the editor: "remove the blank
pages from the set"; `courtbook.cut(..., keep_skipped=False)`), and
`processed/_not_staged/` is empty. Pages: 0001_a, 0002_a2 (fol. 1r), 0004_a2 (2r),
0005_a2 (3r), 0006_a1 (3v), 0007_a2 (4r), 0008_a2 (5r), 0009_a1, 0009_a2
(5v, 6r), 0010_a1 (6v), 0011_a2 (7r), 0012_a2 (8r), 0013_a1 (8v), 0013_a2
and 0014_a1 (the small slip bound in as fol. 9, recto and verso), 0014_a2
(10r), 0015_a1 (10v), 0016_a2 (11r).

## The documents

**Eleven** (the editor, 2026-11-20, asked before the cut, as WORKING_NOTES
says since Nr. 3067; Claude had proposed twelve, the slip its own document;
the editor: "11: slip with no. 4").

| Doc | Pages | What it is | Date, place |
|---|---|---|---|
| 1 | 0002_a2 | Goldbeck to Haugwitz: the petition referred; the rescript to Poznań for the files | 19 Feb. 1803, Berlin |
| 2 | 0004_a2 | Goldbeck to Haugwitz: the files in 6 volumes, the draft report | 22 Apr. 1803, Berlin |
| 3 | 0005_a2, 0006_a1 | Haugwitz's draft reply: the report signed, his reservation on the confiscation | 29 Apr. 1803, Berlin |
| 4 | 0007_a2, 0013_a2, 0014_a1 | Goldbeck to Haugwitz: the cabinet order, the drafts; with the office's slip | 11 May 1803, Berlin |
| 5 | 0008_a2 to 0010_a1 | Copy of the joint report to the King | 30 Apr. 1803, Berlin |
| 6 | 0011_a2 | Copy of the cabinet order | 10 May 1803, Potsdam |
| 7 | 0012_a2 (lines 1-19) | Copy of the rescript to the South Prussian Government at Poznań | 11 May 1803, Berlin |
| 8 | 0012_a2 (from line 20), 0013_a1 | The resolution to the two at Dresden, below the copy of 7 | 11 May 1803, Berlin |
| 9 | 0014_a2 (lines 1-27) | Draft to Voss: the notificatorium to countersign | 30 May 1803, Berlin |
| 10 | 0014_a2 (from line 28), 0015_a1 | Haugwitz's draft reply to Goldbeck | 30 May 1803, Berlin |
| 11 | 0016_a2 | Draft rescript to the Chamber at Poznań: the oath of allegiance | 30 May 1803, Berlin |

**The slip is out of the file's order.** It stands bound between 8v and 10r;
it carries "Cito / 1261", the registry number of document 4 ("B Nº 1261" at
the head of 4r, not transcribed). `holding.py` writes corpus.txt itself
(DOCS), with the slip's two sides after 4r, not `import_pages.py`, which
keeps the order of the page files; `scan_decisions.json` (`image_order`)
gives match_scans the same reading order, without which its check "follows
intended order" fails. Both sides are listed in `office_notes.yml`, with the
note of 3 May at the foot of document 3.

Types: letters 1, 2, 4; drafts 3, 9, 10, 11 (the layout: text down the right
half, address and dispatch notes in the left, GOVERNMENT_FILES); report 5;
`royal_rescript` 6, 7, 8 (as the cabinet orders of Nr. 3709 and the
resolution of Oe 1 Bü 14525, 43). Relations: 3 answers 2, 4 transmits 5 and
6, 6 answers 5, 10 answers 4.

## The transcription checked

The transcription is the editor's: a recognition model's reading,
corrected, with [?] where they were unsure. At the editor's word ("try to
resolve any uncertainties ... use Sonnet agents for lower-effort tasks")
four Sonnet readers checked it against the page images in overlapping
strips: reader 1 the clean letters and copies (cover, docs 1, 2, 4, 6-8),
reader 2 the copy of the report, readers 3 and 4 independently the drafts
and the slip (reader 3 read the slip, reader 4 the left column of 0005_a2
and the margin of 0006_a1, from the image before the text). Claude settled
the disagreements on enlarged crops: the slip whole, "Huldigungseid" (the
editor's "Huldigungs und" on 0015_a1: the "und" is "eid" with a dotted i),
"Bericht" (reader 4's "Entwurf" is wrong; the editor's word stands), "gegen
sie", "einer mäßigen", "9jährige Verbannung". Where the readers contradicted
each other and the editor's word was possible, the editor's stands
(WORKING_NOTES, from Nr. 3067).

55 corrections, each with its witness, in `intake/holding.py`
(CORRECTIONS). Among them: "Straßen" -> "Starosten", "urtheilt" ->
"ertheilt", "Bewunden" -> "Bewenden", "Verbauung" -> "Verbannung",
"Gjährige[?]" -> "9jährige" (the cabinet order's "neunjährige"), "Aldels",
"eiter", "Theilmann", "Confiscationsartel" -> "Confiscations Urtel", "ergab /
genen" -> "ergan- / genen", "Keinschrift" -> "Reinschrift", "und, /
änderlich" -> "unab- / änderlich", the margin note of 0006_a1 ("Die mir
geneigtest Communicirten Acta füge ich mit Danksagung hier wieder bey"),
"re- / fehle" -> "ver- / fehle", "stüge" -> "füge", "fl[?]. Nun" -> "Et.
Min.", "bestohlen" -> "befehlen", "hier p" -> "Sind p", and the slip:
"Acta / 26" -> "Cito / 1261", "Frf." -> "Sr Exc", "Woll[?]heit[?]" -> "v.
Voss zur Mit-", "Haldgass[?] und Leisten" -> "Huldigungseid leisten". Three
on Claude's witness alone, on the spot sheet for the editor's eye:
"mitzuziehnen" -> "mitzuzeichnen" (document 2's formula), "sagen sie" ->
"gegen sie" (the one reading of the sentence; the crop shows "gegen"),
"[U?]. A. B." -> "U. A. H." (the formula "Unser allergnädigster Herr").
The signatures "[Haugwitz?]" are "Haug[witz]": "Haug" read, the rest from
the writer (as "A[lvensleben]" in Nr. 1414). A line the editor wrote for the
flourish between documents 7 and 8 ("–") is left out (OMIT).

Moved: on 0005_a2 the office note "d. 3ten May. ins: cum 2 vol: Actor:
pLch:" now stands before the catchword "eine" (the line-break pass looks at
the page's last line for a catchword; WORKING_NOTES).

Not transcribed, as in the editor's text: the registry numbers "B Nº 501",
"B Nº 1010", "B Nº 1261" at the head of 1r, 2r and 4r; the stamped folio
numbers; the pencil numbers 147, 415, 416; the "+" marks before "Nachdem";
the diagonal strokes in the margins; on 0002_a2 the brace of "(factum)";
on 0004_a2 the margin note "6 Vol: Act: / Conc: zum Bericht"; on 0005_a2 the
margin notes "Abg. d. 30 ejd." (reader 4) and "Retenta Cop."; on 0007_a2 the
large "Acto" in the middle of the page; struck words on 0005_a2 and 0014_a2.

**The spot sheet** (`intake/spot_sheet_html.py` ->
`review/ihagrrep7cnr3132/spot_sheet.html`, one self-contained page): 14
readings and 4 decisions (the Jezierski entry, the three connections).
Answered by the editor on 2026-11-20 and applied through CORRECTIONS (each
reason names its question): confirmed "mitzuzeichnen" (q1), "gegen sie"
(q7), "U. A. H." (q8) and "geschehen sey anhero" (q12); the editor's own
readings kept in q2, q6, q9 and q14; given "des [sub?] lit." (q3), "An v
Prusiemski" (q4), "hinzufügen zu müssen" (q5), "Sr." (q10) and "Graf
Haug[witz]" (q13); q11 unread by both. The English and the summary of
document 4 follow ("v. Voss for co- Count Haug[witz]").

Line ends: eight words broken with "¬" that the resolver split set to
`join` by hand (Prusimski, beigehend, meiner, Euwer, Officianten,
characterisirt, eingeschafften, abschriftl). Paragraphs: set by
`intake/paragraphs.py` on stated principles (30 rows held).

## Translation and summaries

Translated in session (2026-11-20), no paid run:
`intake/translation/english.py` writes doc1-11.yml, `write_cache.py` puts
them in the cache; check_translations raised one forbidden rendering
("engrossed" for "mundiren lassen", now "had the fair copy made"), then
nothing. Summaries in session (`intake/write_summaries.py`), claim-checked
by a Sonnet reader (`intake/claim_check.yml`: 96 statements, 85 supported,
10 overstated, 1 unsupported; all eleven taken: the slip's writer and the
number 1261 not stated, "probably" for the misattached copy, "not closely
examined", the resolution not headed "Abschrift", "[loyal?]", document 9
unsigned, the office notes quoted not interpreted). "Draft" for 3, 9, 10, 11
is kept: the edition's type, from the layout.

The English writes Prusimski for the clerks' Prusiemski, Pawłów for
"Pawlower Güter" (the form of the Sanitz entry, from Nr. 3570), Smiłowice,
Kuyavia, Włocławek; "Neustadt" (Jezierski's parish) stays as written.

## Index

- Goldbeck: `only_in` extended to documents 1-8 and 10. Haugwitz, Voss,
  Hohenlohe, Sanitz matched as they were. Friedrich Wilhelm III: issuer of
  6, 7 and 11 (`issued_in`; his `issuer_match` takes "Friedrich Wilhelm p.").
- Bischoffwerder: the report's one-f "Bischofswerder" matched only in "von
  Bischofswerder geschenkt": the one-f form stands 40 times in the
  literature, not ruled (NEEDS_CONFIRMATION); his identity now names this
  report among the donees.
- Jezierski: a new entry `jezierski` (kept at the editor's word, spot sheet
  d1), and matched in Nr. 3067 too: "Jetzierski" among Goldbeck's fled
  ringleaders of 1797 (the editor: "Use info from 3067 to build the person
  entry for Jezierski, tag him in 3067 as well"). The identity tells the
  1797 mention; Nr. 3067's English reads "Jetzierski [Jezierski]".
- Prusimski: a sentence on 1803 in his identity.
- Places: Trąbczyn matches "Trampczyner" (a `match: true` variant; a broad
  Tr[ąa]mpczyn pattern would have caught the Trąmpczyński family). Neustadt
  shut out of document 5 (`not_in`): Jezierski's parish, a Nowe Miasto not
  identified, not the register's town. Smiłowice and Pawłów are not places
  of the register (offered, NEEDS_CONFIRMATION).
- Glossary: "May", "König.", "Et." ruled out under `excluded:`.

## Connections and the timeline

Three cross-holding connections (spot sheet d2-d4; d3 and d4 kept by the
editor, d2 open: they asked what it means, explained in chat 2026-11-20):
`prusimski-wife-italy` (1414-2, 12366-2), `prusimski-estates-three-donees`
(agad11740273-2), `goldbeck-confiscation-stands` (3067-1). Timeline: "Prusimski
allowed home", 10 May 1803, era `insurgency` (as the Venice event of the
Prussian file Nr. 1414). Paragraphs added to /eras/insurgency/ and to
section I of /eras/hohenlohe/, both languages.

## Era

`hohenlohe`, as Nr. 1414 and Nr. 3067 (the editor left it to Claude: "You
should also assign an era").

## Damage

None recorded.
