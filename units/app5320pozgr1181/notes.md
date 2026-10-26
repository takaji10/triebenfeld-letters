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

The editor's own Latin transcription, one Markdown file (14 pages, 161 to
167v), split into per-page files by `intake/split_and_settle.py` and settled
in session on 2026-10-26 **before** the first build, so nothing was built
twice.

- **108 readings applied** (see `intake/changes_applied.md` for the table with
  the witness of each). The rules followed are the standing ones: a reading
  changes only where the grammar admits one reading, a fixed formula of the
  register, an unflagged form elsewhere in the same entry, or a form attested
  in the sibling units settles it; the scribe's spellings are kept (dicidenda,
  oblatuata, octuigentorum, "Paturna", "fp"); his grammar is not tidied.
- **The scribe's office forms in -ida** are confirmed by the sibling units and
  kept: "Castellanida" (161), as "Dapiferidae Podlachiae" in Konin Gr.118 and
  "Thesaurarida" in Gr.117. "Subdapifinda[?]" (161) is proposed as
  "Subdapiferida" on the spot sheet.
- **Dates proven in session** (all from the entry's own formulas and the
  calendar, not from looking at the images - the session could not see them;
  the letters themselves are confirmed on the spot sheet):
  - The actum: Monday after Judica Sunday = **29 March 1784** (Judica fell on
    Sunday 28 March 1784). The year "Octuagesimo Quarto" in the editor's
    transcription is consistent with this and stands unless the sheet says
    otherwise.
  - The December terminus "anno immediate elapso 178[5?]": the formula
    "Monday after St Andrew, i.e. 1 December" fits **1783** (30 November 1783
    was a Sunday) and not 1785 (a Wednesday). The digit itself is still to be
    read (spot sheet, `dec_year`); if the page says 5, the scribe slipped and
    the transcription keeps 1785.
  - "sub~bo post Festum Immaculate Conceptionis" = **Saturday 13 December
    1783** (the Saturday after 8 December), read "sab~bo" - supported by the
    same word written "sab~bo"/"sabbo~" twice later in the entry (sheet row
    `p_sabbo` confirms the letter).
  - "die decima sexta" of "Feria secunda post Dominicam Sanctae Trinitatis" =
    **16 June 1783** (Trinity Sunday was 15 June).
  - The decree of 8 October 1782 ("die 8ua Mensis 8bris") against the
    Monday-after-St-Francis formula of the same sentence (4 October 1782 was
    a Friday; the Monday is 7 October) - open on the spot sheet.
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
