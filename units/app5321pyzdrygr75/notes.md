# 53/21/0/-/Pyzdry Gr.75 (APP)

One document on two pages: entry no. 39 of the register "Inscriptiones
[protocollon] 1768-1781" of the grod court and office of Pyzdry, on leaf 19
recto and verso - the declaration of the merchant Jan Tracholz of Witkowo
(written Traholtz) transferring to Stanisław Chełmski his claims against the
late Paweł Prusimski. Added 2026-11-26 on the branch
`claude/vigilant-johnson-jxb4hz`; status `translated`; **not published**.
Latin with a Polish closing formula ("ręką trzymaną") and docket. Read
`intake/holding.py`'s docstring first.

## Provenance and rulings of the editor (2026-11-26)

- **The volume.** Pyzdry Gr.75 is "Inscriptiones [protocollon] 1768-1781"
  (szukajwarchiwach.gov.pl, jednostka 984716). The folder "Relationes
  [protocollon] 1768-1771" was a second copy of the same volume and is deleted
  on the editor's machine; the old question (TODO t009) is closed. The files the
  editor sent are still named "Relationes ... 1768-1771" (the old folder's name).
- **No cropping.** The two images are single pages: leaf 19 recto = page
  `0019_a`, leaf 19 verso = `0019_b`. The cloud session received them as images
  of 1185 x 2000 pixels and made the site's copies (1100 wide) directly
  (`holding.py --scans`); the editor's originals stay on the J drive, so
  `make_scan_derivatives.py` must not be run with `--prune` on this holding.
  `page_scan_map.csv` and `scan_rename_map.json` were written by hand
  (`match_scans.py` needs the raw scans).
- **The editor's Latin is used and checked; their English is a guide.** Both
  are kept as received in `intake/editor_latin.md` and `intake/editor_english.md`.
  The English of the edition is Claude's own, in session, no paid run.
- **Tracholz.** A person entry at the editor's word (`tracholz`,
  `reference/people.yml`): 9 documents now. The Pyzdry clerk writes **Traholtz**
  (no c); the pattern is `Trac?h[ou]lt?z`.
- **Connections.** The editor named it a default step: connection
  `tracholz-transfer-and-chelmski-suit` (six documents: this entry, the Konin
  decree 53/6/0/-/46 doc. 2, Konin Gr.117 docs 3 and 8, Gr.118 doc. 14, Gr.120
  doc. 2); a timeline event of 7 September 1768; a paragraph in the era essay.
- **Entry no. 17 of 53/6/0/-/46 needs no fresh transcription:** it is already
  document 2 of that holding (editor, 2026-11-26).

## The check against the images

Done 2026-11-26 from enlarged strips (Claude), with a second reader working from
the editor's text as a table of differences (Sonnet) and two blind readers
(Sonnet; the verso reader read the signature and the heading well, the recto
reader gave a weak reading and was not relied on - the first blind pass, from
whole pages, was discarded for the same reason). Nine corrections (ten rows, the page break being two), in
`holding.py` ROWS and `transcription_decisions.csv`:

1. "Manifestatione Recedendo e[dem?]ce~" is **"Manifeste Recedendo &c[etera]"**
   (the page: "Mnfte Recedendo &ce Recognovit").
2. **Omission**: after "Imperialium" the page has **"Grossorum Tredecim,
   Fericorum[?] sc[ilicet] per olim Magnificum"** - 13 groschen after the 1,053
   imperials; "Fericorum" is doubtful and not used in the English or summaries.
3. "ea positam" is **"expositam"** (the line ends "ex-").
4. "proque sisce[?]" is **"proq[ue] usuq[ue]"**.
5. "manuali his ac Regestris" is **"manualibus ac"**, and "Regestris" moves to
   the head of leaf 19 verso (the page ends at the torn corner).
6. "hisce summas" is **"hasce summas"** (accusative, and "hasce" two lines below).
7. "actas praesenti" is **"Actaq[ue] praesenti"**.
8. "haec sua personali recog~tioni" is **"hac sua personali recog~tione"**
   (ablative absolute with "accedente").
9. The docket's "Super" is "Sup[er]".

Struck out, not transcribed (ruling of 2026-10-05): "per" after "elaboratis";
about three words after "Prusimski pro" ("usu seu conversione"); "sibi" before
"hasce" on the verso.

**Left as the editor has them and put to the editor** (TODO t903): "Borram" (the
page may read "Borrarum"); "erogatam [i?]" (a smear); "iure suo proprio" (the page
may read "aere": from his own money); "ea praedictis" ("ex"?); "Da[m/s?]"; the
docket's "in Per" (perhaps "inter"); the first word of the interlinear line above
line 10 of the verso; the first word of the verso ("Regestris"); and the **placing
of the two inserted lines**: the interlinear "... ab ejusdem summis capitalibus
provenientibus &" carries a cross that matches a cross in line 10 before "cessit"
(the editor has it at the end of the entry), and the foot line "Recognoscentem
successoribus Prusimscianis instituto" carries a cross that matches the cross after
"per[tinente]" at the end of the signature line (the editor has it before "cessit").
Both placings change the English only in order of clauses.

**Abbreviations.** The editor's "~" forms stand; the letters supplied in the ten
corrections are bracketed by the ruling of 2026-11-22. Whether to carry the bracket
rule over to the editor's tilde forms is asked (TODO t904).

## What the entry says, and does not

- "Borris et sylvis" (pine forest) here, against "silvae Quercineae" in the protest
  of 1778 (Konin Gr.117, doc. 3: a contract of 1744 for oak timber) and "pine forest"
  in the decree of 1777: the documents differ on the wood; the transfer names no year
  for the contract.
- The entry has no date on its pages; the sitting heading beneath it on leaf 19 verso
  (Friday 9 September 1768, held outside the town after the enemy's burning of Pyzdry
  on 11 June) heads the entries from no. 40 on. The date 7 September 1768 is from the
  Konin decree of 1777 (53/6/0/-/46, doc. 2: "Feria 4ta in Vigilia Festi Nativitatis
  BMV 1768"), inferred in `rulings.yml`.
- "Fericorum", "Klapek", "Rynek", "Auscuk": left as written; Klapek and Rynek are not
  identified.
- "Witkoviensi" is read Witkowo (Claude's identification, as in 53/6/0/-/46).

## Method

Check against the images: Claude and Sonnet readers (above). Translation and
summaries: Claude, in session, no paid run; claim check in session
(`intake/claim_check.yml`; "Kiefernstämme" cut to "Bäume aus den Kiefernwäldern",
the 1,513 florins weakened to "partly ... partly"). The glossary gate passes (no
candidates). Two rows of `reference/translation_rulings.json` are Claude's own, for the
editor to confirm: "Dominium" (here dominion, not manorial lordship) and the marker count
of "fun[d?]u[m?]".

## Still to do

- The editor's rulings on TODO t903 and t904.
- Publication, at the editor's word.
