# Notes — APP 53/20/0/-/Poznań Gr.1181

Read this first when working on this holding.

## What it is

One entry, in Latin, of the relationes protocollon of the castellany court of
Poznań: the decree of the condescensio held **on the Trąbczyn grounds**
("in Fundo Bonorum Villae Trąmpczyn Curiaque ibidem sita") on **Monday after
Judica Sunday, 29 March 1784**, on the ultimate limitation (ultimariae
limitatio) of the succession the sterile brothers **Antoni and Paweł
Prusimski** left. The parties: Antoni in Kolno Prusimski, captain of
Nieśwież, against the heirs of the sisters (the Zakrzewski, Tomicki,
Taczanowski, Kołaczkowski and Tworowicz parties), with the abbot and convent
of **Ląd** summoned over the quietation of 3,500 ducats and the silver lodged
in the convent's treasury. The decree recites the whole documentary history
of the suit: the Piotrków decrees of 1782 and the comportation of documents
of December 1783, the fraternal division of **1740** with its three schedas
and their sums, the maternal Golinski goods (Oporowo with Oporówka and
Kałowo, Prusinowo, Szetlewek) with their contracts and loads back to 1616,
and the loads on the paternal estates (Trąbczyn, Nowa Wieś, Łazy, Osiny,
Wierzbno, Brzezno, Kamionna, Kolno, Pawłowo, Zernik, Chyby).

The entry is the direct continuation of the lawsuit the sibling holdings
carry: Konin Gr.115-121 and 145, 153 (the boundary suit and the
condescensiones of 1775-1782) and the Kalisz Gr.414/425. Its era is
`prusimski-boundary`.

## The transcription

The editor's own Latin transcription. On 2026-10-26 (evening) the editor
began laying it into the manuscript's lines - p. 161 is done, in their own
layout, and stands in the corpus as they typed it (`intake/lay_lines.py`
carries it in verbatim and verifies no word was lost). The fresh pass
settled five readings, all on p. 161: the December year is **1783**; the
decree day reads "**videlicet** 8ua Mensis 8bris" (the scribe's 8 stands
against the 7 the Monday-after-St-Francis formula computes for 1782 -
recorded as the scribe's slip or his own reckoning); "**Mens(is)**
Junii" (the old "[??] sui" was one garbled word); "**oblatam**
porrecto"; "**camera-/riali**" (the break as they typed it; the joined
form is for the linebreak decisions, not assumed). A full stop after
"acclamante." is also theirs.

The 108 readings the morning session had applied (case completions,
formulas) were **withdrawn** the same day: the editor's fresh
transcription keeps the original doubts, and their word is the source of
truth. They wait in `intake/split_and_settle.py` with the witness of each;
the spot sheet's two principle rows (pr_nieszwiez, pr_changes) rule
whether they go back in.

**Lineation of pp. 161v-167v waits on the editor.** The session measured
itself against the editor's p. 161 ground truth and cannot do it
unsupervised: char-wrap lands within +-1 word at 3 of 8 boundaries
(drifting 2-4 words), and three line-detector attempts counted 22, 24,
39, 41 and 50 lines against the true 38 (the hand's lines touch; the
spacing is not uniform). Machine drafts, clearly marked, are in
`intake/lineation_draft/` as a typing aid only; nothing of them is built.
The other pages stand in the corpus one paragraph per page until the
editor's layouts arrive.

- **Dates** (from the entry's own formulas, checked against the calendar;
  the letters confirmed by the editor's fresh pass where they re-read
  them):
  - The actum: Monday after Judica Sunday = **29 March 1784** (Judica fell
    on Sunday 28 March 1784). The year "Octuagesimo Quarto" in the
    transcription is consistent with this and stands unless the sheet says
    otherwise.
  - The December terminus is **1 December 1783** (the editor's reading;
    the weekday formula agrees: 30 November 1783 was a Sunday, 1785's was
    a Wednesday).
  - "sub~bo post Festum Immaculate Conceptionis" = the Saturday after the
    feast, 13 December 1783, if sub~bo is sabbato - the editor's spelling
    stands as written; the reading is interpretation, not correction.
  - "die decima sexta Mensis Junii" = 16 June 1783 (Trinity Sunday was
    15 June) - the day formula now fits the calendar exactly.
- **The entry breaks off mid-sentence** at the foot of p. 167v ("... Relictam
  viduam"). The continuation is on the next leaf, not among the scans
  (spot sheet, `tail_167v`).
- **The register heading "4ta Martii"** carries no year in the transcription.
  The volume is labelled 1786, but the actum is 1784 and the narrative runs
  to "anno immediate elapso 1783"; whether the heading carries a year and
  which is on the spot sheet (`heading_year`). Until it is settled the date
  span of the unit is written 1784-1786.

## The spot sheet

`units/app5320pozgr1181/intake/spot_rows.py` defines the rows;
`intake/make_sheet.py` builds the page with a picture of each row's line
(`review/app5320pozgr1181/sheet/`). The sheet is published at a public
address (the editor is away from this machine); the editor's answers come
back pasted into the chat, are recorded here, and are applied by a follow-up
of `split_and_settle.py` (the PROPOSED list) or by hand for the rows whose
reading they settle.

## What the entry gives the rest of the edition (to do after the sheet)

- **Index**: the new persons (the Zakrzewskis, Tomickis, Taczanowskis,
  Kołaczkowskis, Tworowiczes, Skarbek, Zelisławski, Łaszkowski, Zeromski,
  the Radolińskis, Kęszyckis, Obarzankowskis, Dziembowskis, Zaleskis,
  Nierzychowskis, Puchalskis, Raczyskis, Pomorskis, Kowalskis, Urbanowskis,
  Zielonacki, Białoskorski, Trąmpczyńskis, Obierunskis, Parys, Poninski,
  Rozdrażewskis, Maniewska Potocka, Bogdański, Florkiewicz, Flottowa...),
  ruled after the sheet settles the doubtful names. Szepczyński, Prusimski,
  Rozdrażewska, Trąmpczyński, Kiełczewski, Strzałkowski are already in the
  register.
- **Places**: the estates of the 1740 division not yet in the register
  (Oporowo, Prusinowo, Wierzbno, Brzezno, Podbiele, Świątniki, Jaryszki,
  Kanin, Pawłowo, Zernik, Chyby, Drzęczew, Huta, the Goraj and Krobielewko
  borras) - variants ruled, cards as the editor decides.
- **Glossary**: the Latin court terms (condescensio, ultimariae limitatio,
  comportatio, quietatio, complanatio, scheda, vadium, arenda, reversale,
  indiction) - the gate will list them once the holding is translated.
- **Timeline**: the 1740 division and the 1784 decree are candidates; both
  are already documented from other holdings - rule after the sheet.
- **People pages**: Antoni Prusimski's career (captain of Nieśwież, knight
  of St Stanisław) and the family's 1740 division are already in
  `reference/genealogy.yml` from other sources; the entry's own recital of
  the division is a new document-side witness.

## Open

- The spot sheet (all sections).
- The fond's own name in the archive's inventory (unit.yml `fonds` left
  unwritten until the editor supplies it, as for Konin Gr.117).
- The English translation (in session, after the sheet's answers).
