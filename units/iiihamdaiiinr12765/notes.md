# III. HA MdA, III Nr. 12765 (GStA PK)

Thirty documents on 48 pages, plus the cover as front matter, 1814-1820: the
Prussian foreign ministry's file on the Prince of Hohenlohe's claim to be
compensated for the Trąbczyn estates. Imported, read, summarised and translated
on 2026-10-01.

## Provenance

Geheimes Staatsarchiv Preußischer Kulturbesitz, Berlin, III. HA Ministerium der
auswärtigen Angelegenheiten, III Nr. 12765 (older marks on the cover: AA. III
Rep. 8 Nr. 4096; R. XI n. 175 a 2). 46 scans, each an opening of the file
photographed flat; the cover (0001) is a single page.

- **Blank, left out** (no transcription; two carry the archive's slip "Es folgen
  leere Seiten"): 0002, 0009, 0017, 0024, 0034, 0035, 0038, 0045, 0046.
- **Pages.** Only a written side of an opening is a page. `_a1` is the left
  side, `_a2` the right. The editor places the fold on every opening
  (`review_folds.py`); unwritten halves go to `processed/_blank_halves/`.
  - both sides written: 0008, 0012, 0013, 0019, 0022, 0023, 0027, 0029, 0040,
    0041, 0042
  - left only: 0014, 0031, 0043
  - right only: the other 22 openings
- The ruler and dark border are left on the images.

## Transcription

The editor's files, one per scan, stay in `<raw_dir>/transcription/`.
`intake/build_pages.py` turned them into `transcriptions/<page id>.txt`,
`office_notes.yml` and `review/<slug>/document_boundaries.csv`, and records
which source line went where. It was run once; corpus.txt has been corrected
since, so do not run it with `--write` again.

- The source marks the change of side with a blank line on six scans. On five
  more (0019, 0022, 0023, 0027, 0029) both sides are written with no blank
  line; where the text crosses the fold was read off the scan.
- **By paragraph, not by line** (rulings.yml `pages: by_paragraph:`): the
  French pages 0007, 0008, 0010, 0016, 0039-0041 and the left of 0042. Each
  corpus line is a paragraph of the manuscript; the site says so on the page.
- The received mark at the head of several letters ("C. 558 pr. 31. Dec.
  1814", "C. 1527 pr. 24 Mai 1815") is on the scan but not in the
  transcription, and was not added.

## Office text

The file keeps incoming letters with the ministry's work written on them.

- **A reply drafted on the page is its own document** (2, on Triebenfeld's
  letter 1; 9 and 10 beside the end of the Prince's letter 8).
- **Shorter marks by the receiving office** are listed in `office_notes.yml`
  and shown under "Written by the receiving office". They stand at the end of
  their document's part of the page (editor, 2026-10-01), wherever they are on
  the sheet. Nine blocks: on documents 1, 4, 6, 14, 19, 23, 25, 27, 30. The
  longest is the opinion written down the margin of Zerboni's report (14).
- A draft's own registry marks (journal number, "mund.", "abg.", paraphs) are
  part of the draft and are not marked.
- In document 2 the two paraphs the source gives after the salutation of
  letter 1 were moved under the draft, where they stand on the page.

## The documents

| No. | Pages | What it is |
|---|---|---|
| front | 0001 | The file's cover |
| 1 | 0003 | Triebenfeld to Hardenberg, Vienna, 25 Oct 1814 |
| 2 | 0003 | Draft reply to Triebenfeld, Vienna, 25 Nov 1814, written beneath 1 |
| 3 | 0004 | Copy: Hardenberg to Triebenfeld, Paris, 14 May 1814 (enclosed in 1) |
| 4 | 0005 | Triebenfeld to Hardenberg, Vienna, 2 March 1815 |
| 5 | 0006 | Draft reply to Triebenfeld, Vienna, 17 March 1815 |
| 6 | 0007-0008 | The Prince to Stein, Sławięcice, 12 April 1815, French |
| 7 | 0010 | Draft reply to the Prince, Vienna, May 1815, French |
| 8 | 0011-0012 | The Prince to Hardenberg, Sławięcice, 12 May 1815 |
| 9 | 0012 | Draft reply to the Prince, Vienna, 6 June 1815 |
| 10 | 0012-0013 | Draft to Zerboni, Vienna, 6 June 1815, asking for a report |
| 11 | 0013-0014 | Earlier draft reply to the Prince, May 1815, cancelled ("cessat") |
| 12 | 0015 | Fair copy of 11, not sent |
| 13 | 0016 | Fair copy of 7, French |
| 14 | 0018-0019 | Zerboni's report to Hardenberg, Poznań, 2 Nov 1815 |
| 15 | 0020 | Decree on the report, 20 April 1816 |
| 16 | 0021-0022 | Draft to the Prince, Berlin, 20 April 1816 |
| 17 | 0022-0023 | Draft instruction to Schöler at St Petersburg, 29 April 1816 |
| 18 | 0025 | Registry note, 3 and 5 May 1816 |
| 19 | 0026-0027 | The widow von Brehmer to Hardenberg, Sommerfeld, 26 April 1816 |
| 20 | 0028-0029 | Minute: resolution for her and a further instruction to Schöler, June 1816 |
| 21 | 0030 | Draft to the widow von Brehmer, Berlin, 22 June 1816 |
| 22 | 0030-0031 | Draft to Schöler, Berlin, 22 June 1816 |
| 23 | 0032 | The widow von Brehmer to the ministry, Sommerfeld, 25 July 1816 |
| 24 | 0033 | Draft to her, Berlin, 10 Aug 1816 |
| 25 | 0036 | Schöler to the ministry, St Petersburg, 23 Nov 1816: the refusal |
| 26 | 0037 | Draft to the Prince, Berlin, 22 Dec 1816 |
| 27 | 0039-0041 | Note of the Russian envoy Alopeus to Ancillon, Berlin, 31 Jan 1820, French |
| 28 | 0041-0042 | Copy: Prince Zajączek's report to the Tsar, Warsaw, 4 June 1819, French |
| 29 | 0042-0043 | Draft to Minister von Schuckmann, Berlin, 13 May 1820 |
| 30 | 0044 | Schuckmann to the ministry, Berlin, 19 May 1820 |

Dates are the documents' own datelines (`dates.read` where the parser could not
reach them). Senders and recipients are in `correspondents.json`, each with its
reason. 12 and 13 are recorded as duplicates of 11 and 7.

**Links to 9454.** No letter here is also in 9454. The widow von Brehmer's
5,000 rt is entry 66 of the creditors' register (9454 document 303), and the
Seehausen debt is named in 9454 letters 24, 179a and 191. Triebenfeld's letters
from Vienna in 9454 (286, 288, 290, 6) report the same business to the Prince.

## Corrections (2026-10-01)

Twelve, each with a witness, in `transcription_decisions.csv`:
Staegemann -> Stägemann (twice); Küsler -> Küster; "M. S. S.[?]" -> "Ns. S. D.";
[?]tlope[?] -> Alopeus; Schuermann and Scheuermann[?] -> Schuckmann; "[18]16" ->
"[18]20" under the letter of May 1820; Schoder -> Schoeler; Szettleiver ->
Szettlewek; Sagen -> Eugen.

The ministry's drafts are in a hurried chancery hand and are badly read; nine
are marked `rough` in rulings.yml (5, 9, 10, 15, 16, 20, 22, 26, 29).

## The correction pass (2026-10-01)

193 words corrected (187 from the list, 2 at line ends, 4 edited directly), each with
its witness, listed with reasons in
`review/<slug>/rulings_corrections.py` and logged in
`transcription_decisions.csv`. What counted as a witness here:

- **The file's own twins.** Draft 11 against its fair copy 12; the French
  draft 7 against its fair copy 13; the minute 20 against the drafts 21, 22 and
  24 written from it in the same words; decree 15 against draft 17; draft 29
  against Schuckmann's answer 30, which repeats its phrases; draft 10 against
  Zerboni's report 14.
- A fixed formula (the closings, "anheim geben", "nach Lage der Umstände",
  "vorzulegen"), a non-word one slip from the only word that fits, or a
  sentence with one reading.
- Approved patterns: Ewr/Ew. before Durchlaucht (four times).
- Line ends: `¬` on words broken at a line end, and eight line-break decisions
  held by hand where the resolver took one word for two.

Four changes span more than one word and were edited directly: the cover's
"Besetzungen" -> "Besitzungen" (L8, as at L1037); "un venable" -> "convenable"
(L154, the word is broken over a line in the manuscript); "im mittelbar" ->
"unmittelbar" (L510); "du Sa Majesté" -> "de Sa Majesté" (L945).

**The editor's check (2026-10-01).** A random spot sheet of 20 of the 173
corrections that can be checked on the page: all 20 correct. Eight changes where
one real word replaced another (komme -> Konin, sich -> lieh, Südpreuß ->
Einspruch, Gesellschaft -> Gesandschaft, Euern -> Innern, immer -> einer, fund ->
sind, Hochhaltung -> Hochachtung): all eight confirmed. Of nine words left as
written, the editor read six on the scan, now applied: Uebereinkunft (L38),
Erfolg (L512), ingrossirten (L637), ersehen (L889), Note (L909) and the treaty
year 1815 for "1813" (L1001). Three the editor could not tell and they stand:
"Wort" (L37), "en[?]ire" (L173), "Magistel" (L271).

Left alone: the writers' own spelling and grammar, figures and dates, the
French and Polish forms of names in French text (Trąpczin, Prussiemski), and
every passage too garbled to have a witness. Those are listed in
`review/<slug>/unresolved.md`.

## Signatures and paraphs

Read on the scans against the file's own names and the offices held.

| As transcribed | Where | Reading | Standing |
|---|---|---|---|
| Küsler | 1, office note | Küster, of the Chancellor's chancery at Vienna | applied |
| [?]tlope[?] | 27 | Alopeus, the Russian envoy at Berlin | applied |
| Scheuermann[?] | 30 | Schuckmann, minister of the interior | applied |
| Fr. von Schöler | 25 | as read: the envoy at St Petersburg | confirmed |
| Ns. S. D., N. S. D., M. S. S.[?] | 5, 9, 10, 11, 16 | not a name: "Namens Seiner Durchlaucht", in His Serene Highness's name | applied |
| M. v. Z. M. Y[?]S., M. d. a. A[?]. HS., M. v. St[?]. 3[?] S. | 22, 24, 26 | not a name: "M. d. a. A. 3te S.", the ministry and its third section, written out on 17 | applied (editor, q08: 3te S.) |
| [H?], Hy[?], [Hy?], H[?], H., Hoym[?] (1814-16) | 2, 4, 5, 11, 16, 17, 26 | Hbg: Hardenberg's paraph, each time with the day and month | applied (editor, q01, on 5; the rest by comparison, hand 1) |
| [V?], [?]. (1814-15) | 2, 5 | Stg.: Stägemann's paraph | applied (editor, q02, on 5; the same mark on 2) |
| Hoym, Hoym[?] with a date (1816-20) | 22, 24, 29, 30 | Hoffm.: an official Hoffmann, probably the counsellor Johann Gottfried Hoffmann. Not Minister Hoym, who died in 1807 | applied (editor, q03, on 22; the same mark on the others) |
| Ba[?] | 29 | Bal[an]: the editor reads Bal, and after the comparison confirmed the hand as Balan | applied (q09, confirmed) |
| B. standing alone, St., H[?]. | 20, 22, 23, 24, 26 | B[alan].: the two-stroke initial that closes the decrees and initials the drafts; written out Bal on 29, so Balan | "St." and "H[?]." changed to B. by comparison, hand 4; the editor confirmed hand 4 is Balan |
| B. before a date | 20, 23, 25, 30 | not a name: Berlin, as in "B. 18. Juny 16." | as read |
| Stein[?], 7 May 1816 | 19, office note | Stgm: Stägemann (the editor: "Htgm, Hgm, Stgm?"). Not Jordan, as I first guessed | applied by comparison, hand 2 |
| [Unterschrift] | 14, office note | Stg.: the same hand (the editor saw it matches 19) | applied by comparison, hand 2 |
| Bever, Strenger | 18 | registry clerks; Bever also signs in Rep. 7 C Nr. 3570 | as read |

The editor answered the questions on 2026-10-01 (`review/<slug>/open_queries.csv`,
answers in `query_answers.json`). Thirteen lines changed, logged in
`transcription_decisions.csv`, except the three closing-formula lines, which were
edited directly because they change several words at once: "M. v. Z. M. Y[?]S.",
"M. d. a. A[?]. HS." and "M. v. St[?]. 3[?] S." all now read "M. d. a. A. 3te S.".

**The comparison (2026-10-01).** The editor could not tell four marks alone, so
every paraph in the file was cropped and laid side by side:
`review/<slug>/signatures/index.html`, built by `intake/signature_sheet.py`.
They sort into four hands, and each unread mark falls into one:

1. A tall initial with a day and month: Hardenberg (the editor's Hbg.). Ten
   times, on every draft written in his name from 1814 to 1816, and on neither
   draft of 1820.
2. "St" in one stroke, then g: Stägemann (the editor's Stg.). Beside
   Hardenberg's at Vienna, and under both marginal opinions of 1816.
3. Hoffm and a date, 1816 and 1820.
4. Two tall strokes joined, once written out "Bal": Balan, the official the
   papers were assigned to. It follows the place and date of each decree.

Eight more lines were changed on that evidence, each logged with its reason.
The editor looked at the sheet and agreed with all four hands, with Alopeus,
and with "B." before a date being Berlin (2026-10-01). The paraphs are therefore
expanded in brackets in the text: H[arden]b[er]g, St[ä]g[emann] and
St[ä]g[e]m[ann], Hoffm[ann], B[alan], and B[erlin] before a date. No "Hoym"
remains in this unit. Decrees 15 and 20 are recorded as Balan's and the registry
note 18 as Bever's. Two of Balan's paraphs are on the scans but not in the
transcription (under decree 15 and at the right of document 30) and were not
added. The general lessons are in `docs/GOVERNMENT_FILES.md`.

## The reading (2026-10-01)

Every document was read whole and the reading written to `reading.json`
(`intake/reading_record.py` holds it in editable form): notes in English on who
writes to whom about what, legibility, 113 statements each tied to its lines,
and 99 words still suspected of being misread. It was made in the working
session, not by the paid `read_letters.py` run, so it has not had that tool's
second, independent check of each statement; the line references and every
figure were checked by script. German summaries are still to be written from it.

Worth knowing from the reading:
- **Triebenfeld was dead by 13 April 1816.** Stägemann's opinion in the margin
  of Zerboni's report calls him "der verstorben v Triebenfeld" and says Leixner
  "auch" has died. His last letter in 9454 is of 31 January 1816 (letter 301).
- The Prince is "verstorben" in the papers of 1820; his heirs make the claim.
- Zerboni thought the claim nearly worthless (Trąbczyn run down and loaded
  with debt), and the ministry passed it to St Petersburg only as a matter of
  grace, "without pressing it"; the draft to the Prince says it was supported.
- The transcription left out words the scans have. In document 6 the clause
  with the sum the Prince paid to redeem the estates was added at the editor's
  wish (2026-10-01): "et 6000 écus de fraix, de payer une somme de 55000 écus".
  The figure is read on the scan and proved by the letter's own sum: 55000 and
  6000 are "ces deux sommes ensemble 61,000". Still not added: in document 7
  "mais je l'engage à attendre", in document 17 a struck-out passage about
  Sokolnik.

**Metadata and authorities (2026-10-01).** Sender, recipient, date, place,
language, type, relations and estates in focus are set for all thirty documents
(rulings.yml, correspondents.json). People and places named are tagged from the
authorities; added for this unit: people Stein, Schöler, Balan, Küster, Alopeus,
Ancillon, Zajączek, von Brehmer, Seehausen, Eugen von Württemberg, Hoffmann,
Sobolewski, Strenger, with identities for Zastrow and Simon and the Tsar's and
Miączyńska's forms in this file; places Sommerfeld, Boleslawice, Nowawies, Łazy,
and the spellings Brzyze, Osziny, Miedzeris. In document 19 "Michaelis" was
corrected to "Michaline" from the scan: it had tagged the merchant Michaelis.
Themes are the editor's to assign and none is set.

**German summaries (2026-10-01).** Drafted from the reading
(`intake/summaries_draft.py`), then checked by the paid second call
(`read_letters.py --verify`, 30 checks, $1.22), which may only cut or weaken.
`summaries_de.yml` holds the checked text. It changed eight summaries:
- the kind of paper was cut where the text itself does not state it ("Entwurf"
  in 2, "Reinschrift" in 12 and 13); the page still shows the type;
- a name the text does not spell out was cut (Stein in 9, where the line is
  garbled; Hardenberg in 15, where the text has only "S. Durchlaucht");
- a promise was weakened to what is written (11: it would be a pleasure to find
  an occasion; 21: should the Emperor declare himself inclined);
- 23: the direction on the widow's letter was cut to its legible part.
Fifteen statements in `reading.json` carry the check's verdict and reason. Two
of mine it caught were corrected: in 27 it is the envoy, not the Emperor, who
asks the ministry to inform the petitioners; in 14 the King is "inclined" to
compensate the donees, no more. The English summaries are still to be made, by
translating these.

## Translation and English summaries (2026-10-01)

- **Translation:** all 30 documents, tag v2, run live (at most $4.25 by the
  tool's readout). The mechanical check blocks nothing. The translator was
  given each document's reading notes and doubtful words, and a label line
  before office text, which the English carries as "[Written by the receiving
  office:]" (`translate.py`, OFFICE_MARK).
- **Edited in the cache, not re-translated:** Balan's title where it came out
  wrong ("Decree: Mr Privy Councillor Balan" -> "Assigned to: Councillor of
  Legation Balan"; "Councillor of the High Court" -> "Councillor of Legation");
  the widow's style ("the widow of Colonel von Brehmer"); "Grand Duchy of
  Posen" kept as the name of the state (document 28 had Poznań).
  `uncanonical_names.py` still reports that phrase twice; it stands.
- **English summaries:** translated from the checked German ones
  (`summarise.py --from-german`, $0.55).
- **The translator's proposals for the German** (`transcription_fixes.py`): 94
  open, nearly all the same words already listed in `unresolved.md`, with the
  same readings. They rest on sense or on chancery formulas, in the rough
  drafts; none was applied. A dozen formula readings ("erwiedere ich auf",
  "Zurückgabe der Beilagen", "geehrtesten", "behalte mir vor") would be worth
  a spot sheet if the editor wants the drafts improved; applying them makes
  those documents' English stale.

## Still to do

- The editor's fold lines, then `split_spreads.py --apply-folds`, moving the
  unwritten halves aside, `stage_pages.py`, `relabel_scans.py --apply`,
  `make_scan_derivatives.py`, `regenerate.py` twice and `--site`.
- The words logged in `review/<slug>/unresolved.md`, should the editor want
  to read any of them on the scan.
