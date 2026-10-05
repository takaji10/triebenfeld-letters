# I. HA GR, Rep. 7 C, Nr. 1414 (GStA PK)

Three documents on four pages, December 1796 to March 1797: how the news that
Antoni Prusimski was at Venice, ill and asking for a certificate that he
could not travel, went from the Prussian resident there through the
department of foreign affairs to the ministers for the new Polish provinces.
Added on 2026-10-05: scans cropped, the editor's text cut to pages,
corrected, summarised, translated and claim-checked, with its place on the
site. Status `translated`.

## Provenance

Geheimes Staatsarchiv Preußischer Kulturbesitz, Berlin, I. HA Geheimer Rat,
Rep. 7 C Südpreußen, Nr. 1414; the archive's title is "Aufenthalt des Anton
v. Prusimski in Venedig", dated 1797. Older marks at the foot of the first
page: "R. 7. C. 6. P. 27." with "Fasz. 5" in blue pencil, struck through, and
the stamp "Deutsches Zentralarchiv".

- **Scans.** Seven. The editor wanted 0002 to 0005 (2026-10-05). 0001 is the
  modern folder with the archive's label; 0006 is a blank opening with the
  archive's slip "Es folgen leere Seiten, die nicht aufgenommen wurden"; 0007
  is a blank leaf. None of the three is staged, and there is no front matter.
- **Pages.** 0002 is one page, copied whole (`0002_a`). 0003, 0004 and 0005
  are openings with a blank left side; the editor asked for the blank pages
  to be cut away. `intake/build_pages.py --crop` cuts each to the written
  side (`_a2`) by a box placed on a gridded view. On 0003 the box is the
  slip, which is smaller than the leaf under it. The first boxes for 0004 and
  0005 cut the line ends at the right; they were widened to the edge of the
  page.

## Transcription

The editor's four files (one per scan, line by line) are in
`<raw_dir>/txt/`. `intake/build_pages.py --write` made
`transcriptions/I_HA_Rep_7_C_Nr_1414_<page id>.txt` from them and checks that
every source line is used once. Only the order changes: the department's
marks on the extract (0004) and on Schrötter's letter (0005) go to the end of
their page and are listed in `office_notes.yml`, with the whole of the slip
(0003). The draft (0002) keeps the editor's order.

Paragraphs were set by hand where the cues failed
(`paragraph_decisions.csv`: five rows ruled, eight breaks added with cue
`hand`).

## The documents

| Document | Pages | What it is | Date, place |
|---|---|---|---|
| 1 | 0002_a | Draft of the department of foreign affairs to Hoym, "et in simili" to Schroetter, and by an added line to the Grand Chancellor von Goldbeck; "Gr. in triplo md."; two ministers' signatures; "d 12. sämmtl. zur Post" | 11 January 1797, Berlin |
| 2 | 0003_a2, 0004_a2 | The slip with Raumer's direction of 8 January 1797 ("A. 10. ... Notif. 1. Hoym 2. Schrötter"), then the extract in French from Cattaneo's dispatch No. 423, routed "Hr von Raumer", presented 2 January 1797, "vide Journal A. No. 10." | 14 December 1796, Venice |
| 3 | 0005_a2 | Schrötter to the department, with its marks: "N 5 d 11 Jan", presented 8 February 1797, "Februar B. No 709.", "Ad acta 16 Mart 97 Raumer" | 29 January 1797, Berlin |

Numbered as the pages lie in the file. In order of time: 2 (the dispatch and
its receipt), the slip, 1, 3. Relations: 1 transmits 2; 3 answers 1. Document
1 is `draft`; 2 and 3 are letters; 2 is French. Senders and recipients are in
`correspondents.json`, each with its reason, and in
`reference/correspondents.yml`.

The division was not put to the editor. The slip could be a document of its
own; it is six lines and is the office's writing about the extract, so it
stays with it.

## Corrections (2026-10-05)

20 passages, each read on the scan: `intake/corrections.py`, logged in
`transcription_decisions.csv`. What was left is in `intake/unresolved.md`.

- **Raumer.** "Hr von Raumer" stands in Latin script at the head of the
  extract; the same name signs the slip and the "Ad acta" on Schrötter's
  letter. The transcription had "Rammer", "Maunes[?]" and "Maurer[?]". Taken
  to be Karl Georg von Raumer (1753-1833) of the department of foreign
  affairs; the papers give only the surname, and the identification is from
  memory of the literature, not checked against a reference work.
- **Goldbeck.** "in simuli[?] des / R[?]. G[?]. Goldbeim[?] / Erfolg." is "in
  simili des / H. G[roß]K[anzlers] v. Goldbeck / Excell.": a third addressee,
  added in a large hurried hand. "Gr. in triplo md." (three fair copies)
  agrees.
- **The signatures under the draft.** "Keuglig[?]" is Haugwitz. "Au[?]" is
  given as "[Alvensleben?]": a tall A and a run of minims; Alvensleben was the
  minister who signed with Haugwitz in 1797. No other signature of his is in
  the edition to compare.
- **Office marks.** "zur Inh:" is "zur Post."; "Februar 13." is "Februar B.",
  the journal letter; "16 Ma[r?] 97" is "16 Mart 97"; "Jan[?]" on the slip is
  January.
- **Text.** "aus die Ehre" is "uns die Ehre"; "1792" at the end of the draft
  is "1797"; "Fuhl[?] u" and "E[?]" are abbreviations of Freiherr; in the
  extract "affatigué" was added at the head of a line and "accublement" is
  "accablement".

## Summaries, translation, claim check (2026-10-05)

German summaries written in the session, the English translated from them
(`intake/summaries_draft.py`); 19 statements checked, two weakened
(`intake/claim_check.yml`). Translated in session
(`intake/translation/doc<N>.yml`, `write_cache.py`); status `translated`,
`published_tag: ""`. check_translations.py: no row, after "Schroetter" was
given in the settled form Schrötter. uncanonical_names.py: nothing in this
holding. "Anton Prusimski" and "Antoine Prusimski" stand as the pages have
them. Office notes are under "[Written by the receiving office:]".

## Authorities (2026-10-05)

New people: Cattaneo, Raumer, Schroetter (rendered Schrötter), Haugwitz.
Haugwitz is also named in Oe 1 Bü 9454 (letters 75, 79, 98 and others, 1798
onward), where he was not indexed before; every line the new pattern matches
was read, and all are the minister. Goldbeck (the Grand Chancellor) gained
this holding's document 1 in his `only_in` list. Matched without change:
Hoym, Prusimski. New place: Venice (`venedig`, matching Venedig and Venise).
Alvensleben is not indexed: the reading is doubtful.

## The site (2026-10-05)

`about.md` and `process.md` in both languages; a timeline entry for 14
December 1796; two sentences in section I of the era essay, in both
languages; the holding pages of Nr. 3570 and Nr. 3709 name this holding.
The era is `hohenlohe` (section I of the essay). `docs/HOHENLOHE_ERA_PLAN.md`
had left open whether it belongs to the boundary era instead; it does not:
the papers are of 1796 and 1797 and concern Prusimski after the
confiscation.

## Still to do

- The editor's eye on three identifications: Raumer, Goldbeck, and the first
  signature under the draft (`intake/unresolved.md`).
- The English has not been read against the scans.
