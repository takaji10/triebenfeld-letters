# I. HA GR, Rep. 7 C, Nr. 3709 (GStA PK)

Fifteen documents on 19 pages, plus the cover as front matter, 1800-1802: the
file on Michalina Prusimska's lawsuit against the Prince of
Hohenlohe-Ingelfingen for the Brzyce estates. Scans added 2026-10-01;
transcribed, divided, corrected and summarised on 2026-10-04. Not yet
translated.

## Provenance

Geheimes Staatsarchiv Preußischer Kulturbesitz, Berlin, I. HA Geheimer Rat,
Rep. 7 C Südpreußen, Nr. 3709. The cover reads "Acta betr. die Beschwerden der
Michalina von Prusimska in Sachen wider den Fürsten von Hohenlohe Ingelfingen"
and gives the span "den 18ten Juny 1800" to "den 29 Januar 1802". 22 scans:
0001 the cover, the rest openings photographed flat. Left out on the editor's
instruction, as blank: 0006 and 0022. The other 20 were copied into
raw_dir/processed/ as <capture>_a.jpg.

**Pages (editor, 2026-10-01).** An opening with one blank side is cut at the
fold to its written side; an opening with writing on both sides is NOT cut and
stays one page. This differs from Nr. 12765, where such openings were split.
- kept the right (`_a2`): 0002, 0003, 0004, 0005, 0007, 0011, 0012, 0014, 0016,
  0017, 0018, 0020
- kept the left (`_a1`): 0015, 0019, 0021
- whole (`_a`): 0008, 0009, 0010, 0013, and the cover 0001
The editor placed the fold on eight of the fifteen; the other seven were cut
at the proposed line, which the editor left in place. The blank halves are in
`processed/_blank_halves/`.

## Transcription

The editor's files, one per scan (a Transkribus export, supplied 2026-10-04),
are copied to `<raw_dir>/transcription/` and stay untouched.
`intake/build_pages.py` turned them into `transcriptions/<page id>.txt`,
`office_notes.yml` and `review/<slug>/document_boundaries.csv`, and records
which source line went where. It was run once; corpus.txt has been corrected
since, so do not run it with `--write` again. The page files in
`transcriptions/` are the text as imported, before correction.

- **The French petition (document 15)** stands in the editor's own second
  reading, given on 2026-10-04 in paragraphs and set on the line breaks of the
  first transcription (`review/<slug>/rulings_corrections.py`, FRENCH). "Sire."
  and "de Votre Majesté.", which the second reading left out, stand on lines of
  their own on the page and were kept.
  At the editor's request that reading was then checked against the scan and
  sixteen words corrected, each logged with its reason
  (`review/<slug>/rulings_french.tsv`): in this hand n and u are one shape
  (eu, bonté twice, ans, point, daignatez), the final s is a large loop (remis,
  des, longtems), and the long s lacks the f's cross-stroke (sais, serai, Lois);
  also recourir, suplier, "Il y a", "à Posen". Her verb endings in -tez stand.
- The opening 0010 shows the end of the Prince's letter on the left and, on
  the right, the decree that is transcribed from scan 0011. The decree is not
  repeated on page 0010.
- Marks on the scans that the transcription does not have, and that were not
  added: "Süd-Pr." at the head of the drafts, the numbers "5021. B. 2786." at
  the foot of document 1, the paraph beside "ex officio" on the rescripts, the
  struck-out passages of document 14.

## Office text

The file keeps incoming letters with the receiving office's work written on
them (see `docs/GOVERNMENT_FILES.md`).

- **Shorter marks by the receiving office** are listed in `office_notes.yml`
  and shown under "Written by the receiving office", at the end of their
  document's part of the page. Five blocks: on documents 1 and 3 (the date at
  the head, "ad acta" with the paraph, the mark and numbers at the foot), 5
  (date received, journal number), 12 (the decree of 31 December for the
  answer, journal number) and 15 (the Cabinet's remittal to Minister von der
  Reck, the received mark, his decree of 29 January 1802).
- The decree on document 12 and the minister's decree on document 15 are
  directions for an answer, not the answer itself, so they are office text and
  not documents of their own. The decree of 7 December (document 7) is on a
  sheet of its own and is a document.
- A draft's own registry marks (dispatch notes, clerks' signatures, "im Bureau
  zu mundiren", the paraph) are part of the draft and are not marked.

## The documents

| No. | Pages | What it is |
|---|---|---|
| front | 0001 | The file's cover |
| 1 | 0002 | Report of the Government at Poznań to the King, 18 June 1800 |
| 2 | 0003 | Copy: cabinet order to that Government, Charlottenburg, 14 June 1800 (enclosed in 1) |
| 3 | 0004 | Report of the Government at Poznań, 10 July 1800 |
| 4 | 0005 | Copy: cabinet order, Charlottenburg, 1 July 1800 (enclosed in 3) |
| 5 | 0007-0008 | The Prince to the Grand Chancellor, Wrocław, 30 Nov 1800: the petition |
| 6 | 0008-0010 | The Prince to the Grand Chancellor, same day: covering letter |
| 7 | 0011 | Decree "ex officio", Berlin, 7 Dec 1800 |
| 8 | 0012 | Draft rescript to the Government at Poznań, 7 Dec 1800 |
| 9 | 0012-0013 | Draft rescript to the Government at Warsaw, 7 Dec 1800 |
| 10 | 0013 | Draft rescript to the Ober-Appellations-Senat of the Kammergericht, 7 Dec 1800 |
| 11 | 0014-0015 | Draft to the Prince, Berlin, 7 Dec 1800 |
| 12 | 0016 | Report of the Government at Poznań, 18 Dec 1800: judgment already given on the 9th |
| 13 | 0017 | Draft rescript to the Government at Warsaw, 31 Dec 1800 |
| 14 | 0018-0019 | Draft to the Prince, Berlin, 31 Dec 1800 (rough) |
| 15 | 0020-0021 | Prusimska to the King, Dresden, 22 Jan 1802, French |

Dates and places are the documents' own datelines, all set in `rulings.yml`.
Senders and recipients are in `correspondents.json`, each with its reason.
Types: 2 and 4 are `royal_rescript` (the King's cabinet orders, in copies), 7
is `note`, the six outgoing papers are `draft`, the rest letters. Document 5
is marked damaged (torn edge), 14 rough.

**The estate.** "Brzezier Güter" is tagged as Brzyce (`places.yml`, variant
"Brzezier"). The proof is in Nr. 12765, document 4: the grant included "das
Dorf Brzyze nebst Zubehör in Cujawien", and the Prince held everything "außer
Brzyze, welches die Tochter des Prusimski ... als mütterliches Erbteil
vindizirte". This file is that suit. All fifteen documents have Brzyce as the
estate in focus.

**People.** No new entries. Goldbeck gains his paraph and these documents
(`only_in`); Danckelmann's pattern now takes "Danckelman", as he signs, and
his identity says he was president at Poznań and moved to Kalisz in 1800
(document 11); von der Reck's pattern takes "v. d. Reck". The councillors of
the Poznań government who sign the reports are not in `people.yml`.

## Corrections (2026-10-04)

57 words in the German, each with its witness, in `review/<slug>/rulings_corrections.py`
(55) and `rulings_lineends*.tsv` (2), and 16 in the French (above), logged in `transcription_decisions.csv`.
What counted as a witness:

- **The file's own twins.** The decree of 7 December (7) against the three
  rescripts written from it in the same words (8, 9, 10) and the letter to the
  Prince (11); the Poznań government's three signature lists (1, 3, 12); its
  report 12 against the decree written on it and draft 13.
- A fixed formula ("ersterben in devotester Treue", "Angesichts dieses",
  "verfehlen wir nicht", "zu erklären geruhen"), a form that is no word and is
  one slip from the only word that fits, or a sentence with one reading.
- One clerk's hand (documents 8 to 10) is read with ß for ſt and s for t:
  meißen, Misglieder, Schwebes, benachrichtiges.

Five edits change more than one word and were made directly (DIRECT in the
same script): "mit G[o?]egu[?][g/y?] anfangen seyn" -> "mit Bezug auf unsern"
(document 3, the formula of reference, clear on the scan); "pur" -> "zur";
"Freyheit nach / in dem mein" -> "Freyheit neh¬ / me, mein" (document 6);
"nun dir." -> "mundiren." (document 14).

Six line-end joins are held by hand in `linebreak_decisions.csv`
(ange¬meßene, Zwey¬fel, Cammer¬gerichts, höchst¬denenselben, been¬digter,
Appel¬lations).

Left alone: the writers' own spelling and grammar, figures and dates, the
torn line ends of document 5, the garbled margin of document 14, and the
editor's French. Those are listed in `review/<slug>/unresolved.md`.

## Signatures and paraphs

Every paraph and signature was cropped and laid side by side before any was
read: `review/<slug>/signatures/index.html`, built by
`intake/signature_sheet.py`.

| As transcribed | Where | Reading | Standing |
|---|---|---|---|
| G[?], Gu[?], Gunz[?], Q[?]nz[?] | 1, 3, 7, 10, 11, 12, 13, 14 | one hand: the Grand Chancellor's paraph, expanded G[oldbeck] | applied; rests on the office, not on the letters of the mark. For the editor to confirm on the sheet |
| ferner, H[...] | 1, 3 | Hering, as on 12 | applied |
| Darmenberg, Dannenberg[?] | 1, 3, 12 | Dannenberg | applied |
| [?]oening | 1 | Hoening, as on 12 | applied |
| Schwolner[?], Khroener[?] | 9, 13 | Schroener, a chancery clerk | applied |
| Leuoher[?] / Leuo[hirt?] / Leewhert[?] | 1, 3, 12 | Leuchert | applied, by the state handbook |
| Seih[?] / S[...] / Beimk[?] | 1, 3, 12 | Richter | applied, by the state handbook |
| Sühring[?] / Vühring[?] | 3, 12 | Dühring (the handbook prints Düring and Döhring) | applied |
| Merzow[?] | 3 | Herford (v. Herford) | applied, by the state handbook |
| v Tischer | 1, 3 | v Fischer | applied, by the state handbook |
| Bamg[...]t, Bamuzut[?] | 9, 13 | a chancery clerk, perhaps Baumgart | as transcribed |
| H[?]B[?], h qu[?] B, H qm B. | 1, 3, 5 | a mark of the receiving office beside the journal number | not read, as transcribed |
| Reck | 15 | Minister von der Reck, named in the Cabinet's remittal above | as read |

The identification of Goldbeck: the Prince addresses documents 5 and 6 to
the "Groß Canzler"; the answer (11) is in the first person and bears the
paraph; the same paraph closes the decrees and the rescripts issued "Ad
mandatum". Heinrich Julius von Goldbeck was Grand Chancellor from 1795. The
mark begins with a G; its other letters cannot be told apart.

**The Poznań councillors (2026-10-04, at the editor's request).** The names
left unsettled by the three lists alone were settled against the court's entry
in the *Handbuch über den Königlich Preußischen Hof und Staat* for 1800 and
1801 (`reference/sources/handbuch_1800_1801_regierung_posen.md`): eleven lines
changed, logged in `transcription_decisions.csv`
(`review/<slug>/rulings_signatures.tsv`). Every signature under the three
reports is now a councillor the handbook names. The handbook also shows that
Danckelmann was vice-president, under a first president von Steudener who does
not sign here, and that von Götze had the post by 1801. Only the machine-read
text of the handbook was used; "Richter" rests on the 1801 volume and the
shape of the signature, since the 1800 list is garbled at one name.

## Summaries (2026-10-04)

German summaries were written in the session from a reading of each document
against its scan, and the English translated from them
(`intake/summaries_draft.py`, which writes `summaries_de.yml` and the cache
records `summarise.py --build` publishes). **They have not had the paid claim
check** (`read_letters.py --verify`), and there is no `reading.json`.

`site/_data/summaries_de.yml` was not rebuilt from the local cache: the
committed file carries name corrections made in the cloud that the cache on
this machine does not have, and a rebuild would have undone them in 46 lines.
The fifteen new lines were inserted into the committed file instead.

Worth knowing from the reading:
- The suit is for Brzyce only, the mother's estate, not for the father's
  confiscated lands. Prusimska is a minor and sues through a guardian, with
  the Poznań guardianship board directing the suit.
- The Prince's defence (document 6): her father, still alive, had a lifetime
  right in his late wife's property, and that right fell to the fisc with his
  confiscated property, so it came to the Prince.
- The Grand Chancellor moved the case to Warsaw at the Prince's request on 7
  December 1800; Poznań had the order on the 16th and had given judgment on
  the 9th. **The file does not say who won.** Nr. 12765 (document 4) says she
  recovered Brzyce.
- By January 1802 the appeal was with the Kammergericht in Berlin, and
  Prusimska was writing from Dresden.

**For a session without `review/`** (it is not in the repository): copies of
`unresolved.md`, `rulings_corrections.py` and the `rulings_*.tsv` sheets are in
`units/ihagrrep7cnr3709/intake/`, as they stood on 2026-10-04. The signatures
sheet is rebuilt by `intake/signature_sheet.py` and needs the page images.

## Still to do

- Translation into English (paid; pilot not needed, the same kind of source
  as Nr. 12765). `unit.yml` carries the description and translation note.
- The claim check of the German summaries (paid), if the editor wants it.
- The editor's eye on the signatures sheet and on `unresolved.md`.
- Glossary candidates once translated (`glossary_candidates.py --unit`).
