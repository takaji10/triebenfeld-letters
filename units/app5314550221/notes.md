# APP 53/1455/0/2/21

Six documents on five pages of an eighteenth-century copy-book of the
privileges of the Cistercian abbey of Ląd, "Series privilegiorum monasterii
Landensis transcripta ex libro privilegiorum", in the fond Klasztor
cystersów w Lądzie (53/1455) of the State Archive in Poznań. The pages are
13, 14, 25, 26 and 66, the editor's choice (2026-10-21: "only pages 25-26,
13-14, and 66 are relevant - they contain copies of privilege documents").
The privileges copied are of 1362, 1399 and 1461, and a court decree of
1761. Added 2026-10-21: read from the photographs in session, translated,
summarised, claim-checked, with its page, three timeline entries and the
German notes. **Not published.**

Everything about how the holding was made is in the docstrings of
`intake/holding.py` (the photographs and the crops) and `intake/text.py`
(how the text is written, what is left out).

## Provenance

The editor's folder (the unit's `raw_dir`) has 34 photographs, IMG_5217 to
IMG_5251: the box with the archive's label (IMG_5217), the cover (5218), then
the pages, one to a photograph and turned on its side, as Canon raw files
(.CR2), and IMG_5239 as a .jpg. The photographs are not every page: after
p. 38 they jump to p. 53. The editor gave the fond and the archive's
description of it (kept in `unit.yml`, under `fonds`).

The editor's own five cropped .jpg files in the folder are not the pages
chosen: IMG_5220a and b are pp. 5 and 6, IMG_5225a is pp. 18 and 19 (an
opening), IMG_5225b p. 20, IMG_5239 p. 54. The pages were found by the
archive's pencil pagination, at the top outer corner of each page, beside an
older number in red crayon and a crossed-out one (p. 25, for instance, has
"25", red "26" and "13" struck through). The edition goes by the pencil
numbers.

## The trims

At the editor's word ("make sure to trim any text on those pages that are
parts of other sections from previous/earlier pages"):
- p. 13 is cut below the end of no. 13 (a privilege of 1400, Słupca), at the
  heading of no. 14;
- p. 25 is cut below the end of no. 24 (dated at Konin, 1365, with the note
  of its entry at Konin in 1740), at the heading of no. 25;
- p. 66 lies wholly inside no. 46 (it begins on p. 63, under the heading
  "Cessio Fundi certi in Haereditate Bonorum Lukom circa parietem Bonorum
  Drzewce jacentis ... per Decretum Compromissoriale subsecuta", entered at
  Kalisz castle on the Monday after Cantate 1761). Cutting what belongs to an
  earlier section would have left nothing, so the page is given whole: the
  editor chose that page.
- Two entries begin on the chosen pages and run on to pages not chosen:
  no. 16 (p. 14 to p. 15, IMG_5223) and no. 26 (p. 26 to p. 27, the facing
  page of IMG_5227, which shows only a strip of it). They are documents 3
  and 5, given as far as these pages go. **Offered to the editor**: p. 15
  (photographed) to finish no. 16; p. 27 would need a photograph.

## The margin note

p. 14, right margin, beside "cum Sylva Chmielniki et cum Sylva Lome": "Et cum
Sylva Lomy a limitibus", with a stroke towards the text, in a lighter hand
than the copyist's, perhaps another. It is document 2's last paragraph of
the page and is set apart under "Written in the margin" (`margin_notes.yml`,
a kind added to the pipeline for it: `pipeline/build/corpus_pages.py`,
`SET_APART`).

## Readings

Seventeen words read with doubt, all names or words of the Latin the
photographs do not settle: in doc. 1 "suffragio", "gadibus", "Odsuć"
(underlined, a Polish word), "postmo" (across a line, perhaps "postmodo"),
the witnesses' "Czaten", "Siemenci", "Retch", "Vito"; in doc. 2 "Barlyus" and
"Wardzch" (the third brother, written two ways), "Stenis" (in the list of
lands, perhaps for "stawis"), "Gavisso"; in doc. 4 "est" in the heading
(blotted) and "Bechovien.", "transmitti"; in doc. 6 "attendentique",
"Bylczynski". Doc. 1 has "videal" for "valeat" or "videatur", kept as
written. The copy writes "Kominensi" for Koninensi (doc. 2); the English
says Konin.

## Against the documents and the other holdings

- **Drzewce.** The copyist's heading of no. 25 says Drzewce was founded in
  the forest given in 1362. The Kodeks has the abbey's village "in Nouo
  Sagorowo, alias Drzewycz" in 1411 (`kdw`, doc. 15) and its farm in
  Drzewcza in 1418 (doc. 18). They agree.
- **Gradziem / Gradzien** is a forest beside Łukom, Huta and Drzewce. Whether
  it is the Grądzyń of the edition's estates list (reference/places.yml,
  `gradzyn`; Rep. 162 Nr. 295, the bond of 1805) is not settled: not
  matched, in NEEDS_CONFIRMATION.
- **Little Wronczyn** ("parvum Wronczyno") is the edition's Wrąbczynek (the
  Kodeks: 1173 "parvum Vronchin", 1377 "Parvum Wronczino"); tagged
  `wrabczynek`. The English says Little Wronczyn, as the Kodeks English says
  Great Wronczyn.

## Checks

`check_translations.py` raises two rows, both the German termbase's
"Dominium" catching the Latin "dominio" (ownership), the known noise of a
Latin holding (WORKING_NOTES). `publish_translations.py` deleted
`site/_data/translations/pachonski1973-001.yml`, a stale file of a holding
that became literature on 2026-10-20; it was restored, not this holding's
business (WORKING_NOTES).

## Damage

None recorded. The paper is whole on the five pages.
