# Notes — APP 53/20/0/-/Poznań Gr.1181

Read this first when working on this holding.

## What it is

One entry, in Latin, of the relationes protocollon of the castellany court of
Poznań: the decree of the condescensio held **on the Trąbczyn grounds**
("in Fundo Bonorum Villae Trąmpczyn Curiaque ibidem sita") on **Monday after
Judica Sunday, 29 March 1784**, on the ultimate limitation (ultimariae
limitatio) of the succession the sterile brothers **Antoni and Paweł
Prusimski** left. The parties: Antoni in Kolno Prusimski, starost of
Niszczewice, against the heirs of the sisters (the Zakrzewski, Tomicki,
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

**Lineation ruled optional (the editor, 2026-10-26).** Asked whether laying
out the remaining pages was worth doing, the editor reasoned that the meaning
is already readable and any passage to be cited can be zoomed into later -
and they are right: nothing in the pipeline needs the lines, and the sibling
Konin Gr.117 is published by paragraph with the standing notice "Transcribed
by paragraph, not line by line". So pp. 161v-167v stand by paragraph
(rulings.yml `by_paragraph`), the notice shows on the site, and lineation
remains available if a passage ever needs line-level citation. The session's
measured failure at machine lineation (below) is moot for the corpus but
recorded as the answer to "how easy would it be".

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
- **The entry stops mid-sentence** at the foot of p. 167v ("... Relictam
  viduam"). The editor ruled (2026-10-26, in chat): **there is no content
  past 167v** — the register ends there; the entry stops because the volume
  ends, and no next leaf exists to ask for. The spot sheet's `tail_167v`
  row was settled by this and taken off the sheet.
- **The register heading "4ta Martii"** carries no year in the transcription.
  The volume is labelled 1786, but the actum is 1784 and the narrative runs
  to "anno immediate elapso 1783"; whether the heading carries a year and
  which is on the spot sheet (`heading_year`). Until it is settled the date
  span of the unit is written 1784-1786.
- **The office is the starost, of Niszczewice** (the editor, 2026-10-26,
  in chat: "it is not captain, it is starost", and, on the place, "It
  should be Nieszczewic e" corrected to "Niszczewice" - the modern
  spelling, the one the rest of the edition already carried). The scribe's
  *Capitaneus Nieszczeviec-* is the Latin of starosta of Niszczewice; the
  English and German render "starost of Niszczewice" throughout, as in the
  editor's other translations (Konin Gr.119). The transcription keeps the
  manuscript's Capitaneo/Capitanei and the Nieszczeviec- stem; the endings
  stay on the sheet (`pr_nieszwiez`). The session's first evening reading
  ("Nieśwież") was the session's own misreading and is withdrawn.

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
- **People pages**: Antoni Prusimski's career (starost of Niszczewice, knight
  of St Stanisław) and the family's 1740 division are already in
  `reference/genealogy.yml` from other sources; the entry's own recital of
  the division is a new document-side witness.

## Open

- The spot sheet (all sections). The holding is integrated and translated
  with the doubts standing as written; when the answers come they are ruled
  into the text and the affected pages rebuilt.
- The fond's own name in the archive's inventory (unit.yml `fonds` left
  unwritten until the editor supplies it, as for Konin Gr.117).

## The integration (2026-10-26, same day, second sitting)

The editor's word: integrate, commit, merge into main, publish. Done in
session, no paid run:

- **Translation** in session, page by page, under the pipeline's own rules;
  written to the translation cache through `translate.py`'s own `save()` by
  `intake/translation/write_cache.py` (the cache is not in the repository;
  the script is the record). Published to the site data with
  `publish_translations.py`. The checker's rows: one real catch (the
  English had the manuscript's "Trąmpczyn" where the edition prints
  "Trąbczyn" — fixed outside the [written ...] brackets) and one real
  forbidden rendering ("engrossed", a German-Ausfertigung rule — rewritten
  "entered at length"); the rest were Latin-source false positives, cleared
  in `reference/translation_rulings.json` with the reason recorded there.
- **Summaries** in both languages, inserted into `site/_data/summaries.yml`
  and `summaries_de.yml` by `intake/write_summaries.py` (the script is the
  record). **Claim check** in `intake/claim_check.yml`, hand-made under the
  `--verify` rules: 13 statements, all supported after three corrections of
  the draft — the three daughters (not four), the two paternal figures
  (Paweł's scheda 154,436 gr 24½ at p. 166v and the starost's own 154,936
  gr 24½ at p. 167, each right for its own scheda; the draft had carried
  only 154,936), the Nierzychowska ground (quieted 1740, refused as a load
  borne over, not "not provable as paid"), and the manuscript's own
  "filiastro[?]" for the bracket. The decree's arithmetic was verified by
  computing it (98,379 gr 5 = 130,594 gr 5 − 32,215; ÷6 = 16,396 gr 15
  2½ solidi, the solidus the third of the groschen; 170,833 gr 10 and
  171,333 gr 10 less 16,396 gr 15 2½ solidi = 154,436 and 154,936 gr 24½);
  the weekday formulas all fit the years the decree gives them.
- **Glossary gate**: `Jacobi` excluded (the man's name, not the feast);
  `Junii` excluded (the month's genitive, plain in English); `fl.` covered
  by widening the gulden entry's pattern to the bare "fl." (the Latin
  writes the figures in words — "sex fl. gn[?] 20" — which defeated the
  figure-before-fl form). The literature index needed one new ruling
  (Breyer 1938 p. 17, an estate "Brzezno" on the Koło-Konin road, ruled
  yes) and one stale row cleared (the szetlewek refusal of "Szetlewo",
  stale since the szetlew split of the relatio holding, merged from main
  the same day).
- **People**: twelve entries added (`intake/add_people.py` is the record):
  Skarbek (castellan of Uniejów — the scribe's "Junivladislaviensi" read
  by its sense, kept doubtful in the translation), Zelisławski, and the
  family entries of the five sisters'-heirs parties, the abbot and prior
  of Ląd, the Radolińskis, Bienicki, and the Goliński family (the ADWl 85
  "Golinska" excluded from it). Bios appended to `people_bios.yml`.
- **Places**: seven entries added to `reference/places.yml` — Oporowo
  (with the shares Oporówka and Kałowa folded into its pattern; map link
  firm: Oporowo, gmina Krzemieniewo, pow. leszczyński — Oporówko and the
  hamlet Kałowo-in-Oporowo answer the decree's shares, and the 1673 sale
  before the castellany acts of Wschowa fits the region), Prusinowo,
  Wierzbno, Brzezno (the manuscript's "Breczno" folded in), Chyby, Jaryszki
  (map link: gmina Kórnik), Radolin (pattern keeps the family name out).
  No map link where the identification is open, and the open questions are
  written on the entries. The hearth-tax register and the Kalisz table
  already carry "Radolina" and "Dorf Prusinowa" — their mentions now
  resolve.
- **Timeline**: the decree of 29 March 1784 as an estate event, with refs
  and the German fields.
- **The site's hand-kept counts** corrected in the edition guide (both
  languages): 630 documents, 2,103 pages, 626 translated, 51 holdings,
  24/95 for the Poznań archive, and the decree named there.
- **Merged origin/main** (the Pyzdry Gr.115 holding and the Szetlewicz
  relatio) into the branch; derived files took main's side, the four
  authored conflicts (CHANGELOG, TODO, dwds_cache, translation_rulings)
  hand-merged, the two JSON caches by union.
- Status `translated`. Publishing (the merge to main and the push) is the
  editor's word given in this sitting; the spot sheet stays open, its
  answers to be ruled in when they come.
- **Two rulings of the publish evening** (2026-10-26, in chat), applied at
  once and republished: the scribe's *Capitaneus* renders **starost**, not
  captain (the standing rule; Konin Gr.119), in the English, the German,
  the summaries, the holding's pages, the timeline and the story; and
  **there is no content past 167v** — the register ends at the mid-sentence
  break, no next leaf exists, and every "continues on the next leaf"
  sentence was withdrawn. The sheet's `tail_167v` row came off and the
  sheet was rebuilt and republished (61 rows now).

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

The scans are the editor's own photographs of the fourteen pages (161 to
167v in the archive's pagination), one page per photograph, taken from the
volume of the relationes protocollon in the State Archive in Poznań. The
transcription is the editor's own, made from the photographs: a Latin text
of one continuous entry, typed page by page and, for p. 161, laid out in
the manuscript's own lines.

The editor's text was carried over as written. Claude had first completed
108 doubtful case endings by grammar. When the editor's fresh line-by-line
typing of p. 161 arrived the same day and kept the original doubts, the
completions were withdrawn, and the editor's text stands throughout. The
five readings the fresh typing settled (the December year 1783,
"videlicet" before the day numeral of the decree of October 1782, "Mensis"
before Junii, "oblatam porrecto", the break "camera-/riali") are the
editor's own readings, and everything else stands with its doubt mark as
they typed it.

The pages were cut from the photographs at the archive's pagination and
paired with the transcription; the holding is one document. Pp. 161v-167v
are presented by paragraph, each page's text beside that page's scan, as
the sibling registers of the same suit are; p. 161 is line by line, as the
editor typed it. The line division of the remaining pages is left open:
machine layouts tried for them put the line ends 2-4 words away from the
editor's own on p. 161, and were not used.

Some thirty doubtful readings remain, names, words and figures the
transcription marks with [?]. They are with the editor; where the editor
settles one, the text will be corrected.

The English was translated from the editor's transcription in a working
session under the same rules as the other holdings. The summaries in both
languages were written with it, and each of their statements was checked
against the document.
