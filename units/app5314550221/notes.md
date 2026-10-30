# APP 53/1455/0/2/21

Six documents on six pages of an eighteenth-century copy-book of the
privileges of the Cistercian abbey of Ląd, "Series privilegiorum monasterii
Landensis transcripta ex libro privilegiorum", in the fond Klasztor
cystersów w Lądzie (53/1455) of the State Archive in Poznań. The pages are
13, 14, 25, 26 and 66, the editor's choice (2026-10-21: "only pages 25-26,
13-14, and 66 are relevant - they contain copies of privilege documents"),
and p. 15, added the same day to finish no. 16 ("you can add page 15 to
finish the king's confirmation"). The privileges copied are of 1362, 1399,
1447 and 1461, and a court decree of 1761. Added 2026-10-21: read from the photographs in session, translated,
summarised, claim-checked, with its page, three timeline entries and the
German notes. **Published 2026-10-21** at the editor's word.

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
  and 5. p. 15 was added at the editor's word (2026-10-21) and is cut below
  the end of no. 16, above the heading of no. 17 ("Privilegium donationis
  2dae partis Wrabczyno"), not in the edition. There is no photograph of
  p. 27 (the editor), so no. 26 stays a beginning, undated.

## No. 16 is not the confirmation of the sale of 1461

Read whole with p. 15, no. 16 is King Kazimierz's confirmation, at Gniezno
on the Tuesday before St Lawrence, of the contract by which Abbot Maciej
bought the three mansi in "Villa Lukomia" and the forest "Graziem" from the
brothers Mikołaj, Jan and Warsz ("Warschio") of Koscielec and their stepson.
The year is written over ("1.4" and two inked figures); a later hand wrote
1447 in pencil in the margin, and the witnesses fit 1447: Bishop Andrzej
(Bniński, of Poznań), Łukasz of Górka, voivode of Poznań, Przedbor of
Koniecpol, castellan of Sandomierz, the chancellor Jan of Koniecpol. Dated 8
August 1447 (`rulings.yml`, inferred, with the basis). So the abbey bought
the land under Abbot Maciej by 1447, and in 1461 (no. 15) the brothers and
their nephews resigned it to Abbot Cornelius before the general captain. The
first relation, "confirms" doc. 2, was taken from the heading before p. 15
was read, and is replaced by "supplements". In no. 15 the third brother,
read "Barlyus" and "Wardzch", may be this Warsz; the readings stand as
read, with their doubt.

## The margin note

p. 14, right margin, beside "cum Sylva Chmielniki et cum Sylva Lome": "Et cum
Sylva Lomy a limitibus", with a stroke towards the text, in a lighter hand
than the copyist's, perhaps another. It is document 2's last paragraph of
the page and is set apart under "Written in the margin" (`margin_notes.yml`,
a kind added to the pipeline for it: `pipeline/build/corpus_pages.py`,
`SET_APART`).

## Readings

Twenty-two words read with doubt, all names or words of the Latin the
photographs do not settle: in doc. 3, on p. 15, "Casanis", the year "1447",
"Rasko", "Dobrogosto", "Tczenaczmy"; in doc. 1 "suffragio", "gadibus", "Odsuć"
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
- **Gradziem / Gradzien / Graziem** is Grądzyń (the editor, 2026-10-21):
  matched to `gradzyn` in reference/places.yml, tagged on docs 2, 3 and 6,
  and Grądzyń in the English, the summaries and the holding's page. The
  copyist's headings ("Privilegium Gradziem Ruchowia", "Confirmatio Gradziem
  Regis Casimiri") stay as he wrote them.
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

## Form and language (taken off the public page, 2026-10-30)

The editor ruled the section too descriptive: the languages went to the header, and what changes how a document is read stays in "Contents". The old text:

Latin, copied in the eighteenth century in one clear hand, with the copyist's spelling and abbreviations; Polish words stand in it as the originals had them ("kopce", "niwa", "sep", "naraz", "powos"). Each privilege has a heading in larger letters and its number beside it; the copyist marks the start of each with an "x" in the margin and ends each page with a catchword. Later hands have written page numbers in pencil and red crayon at the top of the pages, and the years of the privileges in pencil in the margin.

## How it was prepared (the public text before 2026-10-30)

The editor ruled the tab too detailed: it now tells only what an AI decided that affected the text (`prepared:` in unit.yml). The full account, kept here:

### Images

The editor photographed the volume in the archive, the cover and its pages, one page to a photograph, with a camera that saved raw files. They chose six pages: 13, 14, 25, 26 and 66, and then 15, by the archive's pagination in pencil at the top outer corner of each page. Which photograph is which page was read off those numbers. Each page was taken from the full-size picture inside the raw file, turned upright and cut to the page. Pages 13 and 25 begin with the end of a privilege copied on the page before; at the editor's word the picture and the text begin below it, at the heading of the first privilege that starts on the page. Page 15 was added to finish the king's confirmation of 1447, which begins at the foot of page 14; it is cut below its end, above the next entry. Page 66 lies wholly inside a long entry and is given whole.

### Transcription

There was no earlier transcription. An AI model (Claude) read the pages from the photographs, enlarged, in the working session. The text keeps the copyist's spelling, writes out his common abbreviations, as is done with Latin, and leaves names and adjectives he cuts short with a stop as he wrote them. Words he struck out are not transcribed. The note in the margin of page 14 is transcribed and set apart. Page numbers, the years written later in pencil in the margins, and the copyist's marks are not transcribed. Twenty-two words and names are read with doubt and marked so.

### Dating

Each document is a copy and takes the date of what it copies. Documents 1, 2 and 4 are dated by their own dating clauses, given by feasts, and the day of the month is counted from them. Document 3 is dated the same way, but the copyist wrote its year over: it is read as 1447, which a later hand wrote in the margin and the offices of its witnesses bear out. Document 5 is a beginning that stops before its date, and is left undated. Document 6 names only "the Friday after Misericordia Sunday"; the year, 1761, is in the heading of the entry on page 63, which is not included.

### Summary and translation

The summaries were written in German from the Latin and translated into English; each of their 80 statements was then checked against the text, and nothing in them rests on a word read with doubt. The English translation was made in the same session. Christian names are given in their Polish form; surnames and the names of places not identified stand as written.
