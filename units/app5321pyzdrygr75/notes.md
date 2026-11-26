# 53/21/0/-/Pyzdry Gr.75 (APP)

One document on two pages: entry no. 39 of the register "Inscriptiones
[protocollon] 1768-1781" of the municipal court and office of Pyzdry, on leaf 19
recto and verso - the declaration of the merchant Jan Tracholz of Witkowo
(written Traholtz) transferring to Stanisław Chełmski his claims against the
late Paweł Prusimski. Added 2026-11-26 on the branch
`claude/vigilant-johnson-jxb4hz`; status `translated`; **published 2026-11-26** (run 267 of "Build and deploy").
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
  `reference/people.yml`): 9 documents now; the "Trachultz" of Gr.120 is Tracholz (the editor, 2026-11-26). The Pyzdry clerk writes **Traholtz**
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
whole pages, was discarded for the same reason). Claude's findings went to the editor
on a spot sheet (`intake/spot_sheet.html`, made by `intake/spot_sheet.py`), and the
editor's answers of the same day were applied. The result, in `holding.py` ROWS and
`transcription_decisions.csv` (13 rows):

**Corrections from the page, standing:**
1. "Manifestatione Recedendo e[dem?]ce~" is **"Manifeste Recedendo &c[etera]"**.
2. **Omission**: after "Imperialium" the page has **"Grossorum Tredecim, [?]icorum sex per
   olim Magnificum"**: 13 groschen and, it seems, 6 pfennigs after the 1,053 imperials. The editor
   reads "sex"; the word before it they could not settle (Ferricorum? Fenicorum? Fersicorum?);
   Claude takes **"Fenicorum[?]"** (the pfennig: imperials, groschen, pfennigs; r/n are minim
   confusions). The English says "6 pfennigs" with a doubt mark.
3. "ea positam" is **"expositam"**; "manuali his ac Regestris" is **"manualibus ac"**, with
   "Regestris" moved to the head of leaf 19 verso; "actas" is **"Actaq[ue]"**; the docket's "Super"
   is "Sup[er]".

**The editor's rulings of 2026-11-26 on the spot sheet, applied:**
- "Borram" is **"Borrarum"** (D1); there is **no "[i?]" after "erogatam"** (D2); "ea praedictis" is
  **"ex praedictis"** (D4); "se[?]rsivo" is the editor's best reading (L3); **"Auscuk[Auszug]" stays**.
- **Claude's "hasce" and "hac ... recog~tione" were wrong** and are put back to the editor's "hisce"
  and "haec sua personali recog~tioni" (A6, A8); and A4: **"proque sisc[e?] ac commodo"** (the editor's
  reading, the doubt mark moved to the letter; Claude's "usuq[ue]" is withdrawn).
- **The passage on the two inserted lines (D5, D6)** is the editor's new reading: "...se referentibus et
  hasce summas enucleatibus un[s?][u?][o?]n provisionibus ab ejsdem summis capitalibus provenientibus
  ac[u?]um process[ae?] juris per Recognoscentem successoribus Prusimscianis instituto cessit
  contulit...": one sentence, the words "provisionibus ... provenientibus" and "ac cum processu juris
  per Recognoscentem ... instituto" at the cross before "cessit", and nothing after "libere accedente".
  Claude's check: it reads as one sentence ("una cum" for "un[...]n"; "per" is the preposition: the
  process instituted **by the acknowledger** against the Prusimski successors, which is why the
  summaries and the English now say so).
- Not clear or not sure, left as written: D3 "iure[?]" (Claude's "aere" not taken up), D7 "Da[m/s?]" and
  the flourish, D8 "in Per", L1 "[ordine?]", L2 "Stru[i]um" (the editor sees "struum", knows it is Struium).
- Not answered, left as Claude changed them: A1 "Manifeste", A3 "expositam", A5 "manualibus ac" and the
  place of "Regestris", A7 "Actaq[ue]", A9 "Sup[er]".

Struck out, not transcribed (ruling of 2026-10-05, restated by the editor 2026-11-26: "don't include
the struck out words in the transcription"): "per" after "elaboratis"; about three words after
"Prusimski pro" ("usu seu conversione"); "sibi" before "hasce" on the verso.

**Abbreviations.** The editor ruled (2026-11-26, TODO t904) that the tilde forms are expanded in square
brackets where certain: "recog~tioni" is now "recog[ni]tioni"; "alisculi~" is an unresolved word and
stands. The editor's other transcription is unchanged.

**The English and doubt.** The rule of 2026-11-22 (EDITORIAL_RULES, "An unread word in the English"):
the English never carries the original's letters; where the passage fixes the sense it gives the sense
with `[?]` after it, where it does not, `[...]`. So "6 pfennigs[?]", "a separate[?] register", "by his own
right[?]", "together[?] with", "with[?] the legal process", and `[...]` for "[ordine?]", "sisc[e?]",
"alisculi~", "Da[m/s?]" and the flourish. (The first draft of this English used the older
"[uncertain: ...]" form; withdrawn.)

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
