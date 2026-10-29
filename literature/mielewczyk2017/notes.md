# Mielewczyk (2017): notes

Wojciech Mielewczyk, "Zmiany przestrzeni wsi w drugiej połowie XIX i na
początku XX wieku na przykładzie wybranych map ze zbiorów Muzeum Narodowego
Rolnictwa i Przemysłu Rolno-Spożywczego w Szreniawie", *Z Dziejów Kartografii*,
tom XXI, 2017, pp. 41-57; Zespół Historii Kartografii - Instytut Historii
Nauki PAN imienia Ludwika i Aleksandra Birkenmajerów. The open-access copy
stands at
http://www.maphist.waw.pl/wp-content/uploads/2020/05/ZDK_21_041-057.pdf
(the `scan:` of `work.yml`). The author is a curator of the museum whose
collection the article surveys (its address and e-mail stand on the title
page); the edition's **title_en** is the one given with the work by the
editor, not the article's own English title of p. 57, which is kept as
printed in both texts.

## How it came in (2026-10-22)

The editor: "I want to add a new literary source to the project - the PDF is
located in the Downloads folder and is called ZDK_21_041-057.pdf", with the
bibliographic facts (author, title, English title, volume, pages, the
maphist.waw.pl address). Asked, they ruled (2026-10-22): **the article is
visible, the figures are skipped, a link to the article is provided
somewhere, and the whole article is brought in.**

- The link to the article: the open-access copy at maphist.waw.pl is the
  `scan:` of `work.yml`, which `literature_site.py` shows on the work's page
  (like Kucharski's link to the journal's page). No other link was added.
- The PDF is the annual's own setting, 17 PDF pages, printed pp. 41-57, with
  a clean text layer. `original.md` is made from it by
  `pipeline/literature/mielewczyk_pdf.py` (its docstring lists every rule), so
  that every passage can be cited by its printed page:

      python pipeline/literature/mielewczyk_pdf.py "<Downloads>/ZDK_21_041-057.pdf" [--report] [--check]

- **`--check` holds every page against the text layer**: for each page the
  script rebuilds the stream of letters the layer carries (the running head,
  the printed page number, the layout's spaces, the raised note marks and the
  note numbers left out) and asserts the same stream, read back out of
  `original.md`, is unchanged. All 17 pages match. The 19 raised note marks
  were read in the order 1 to 19.
- The figures (Ryc. 1-14, one or two to a page on pp. 43-53) are not rendered
  (the editor's word); their captions stay, being text. On four pages the
  caption stands between two pieces of one paragraph (pp. 43, 45, 49 and 51),
  and the pieces are kept apart, as the print sets them.
- The PDF is **not kept in the repository**. It is the editor's file; the
  open-access copy stands on the Zespół Historii Kartografii's page (the
  `scan:` of `work.yml`).
- Copyright: **© 2017 Instytut Historii Nauki PAN** (the imprint of every
  page); no open licence is stated. The editor ruled the article visible
  none the less, whole, with the link to the open-access copy. It is not an
  open licence like Kucharski's CC BY 4.0, so the Licences page
  (site/rights.md, site/de/rechte.md) was **not** changed.

## The text

Never tidied (`docs/EDITORIAL_RULES.md`). What the script does is in its
docstring; among the things found in making it:

- **The pages.** PDF page 1 is p. 41; the printed page number stands alone at
  the foot (y > 620) in the annual's display face; the running head (the
  author or the shortened title, y <= 60) is left out. On pp. 3, 5, 9, 10, 11
  and 13 (pp. 43, 45, 49, 50, 51 and 53) the body text is only a few lines or
  none, the rest of the page being taken by the figures; the body of p. 49's
  paragraph runs over the two figure-only pages 50 to 51 and is joined again
  there.
- **The ligature glyph.** The layer renders "fi" as one glyph and leaves a
  space after it ("Kartograﬁ i", "graﬁ cznie", "inten- syﬁ kacji", in the
  English summary "ﬁ elds", "signiﬁ cant"): the space is the setting's, not
  the word's, and is taken out (every join listed by --report; twelve of
  them, each asserted by --check).
- **The paragraphs.** The body is justified; the first paragraph of the
  article (and the front matter's second paragraph) is set with the indent
  (x >= 84), the later ones flush, so a paragraph's end is known only by the
  short last line that ends a sentence. The script's rules and their report
  follow `kucharski_pdf.py`. A body line never joins a paragraph of another
  kind (a caption, the front matter, a note, a bibliography entry), which the
  figure pages make necessary (p. 43's caption stands between the two pieces
  of the paragraph "W drugiej połowie XIX w. ... 410 spółek" and
  "wodnych, z których ...").
- **The note mark [^16]** stands at its paragraph's end (p. 52, after
  "347 tysięcy."), so the last run of the paragraph is the mark and not the
  sentence; the script's "did the paragraph end in a sentence" looks past the
  raised runs, and the print's two paragraphs ("... 347 tysięcy.[^16]" and
  "Ustawa o komasacji ...") stand apart as printed.
- **The notes** are at the foot of each page, numbered through the article
  (1 to 19); a note's raised mark in the text becomes `[^n]`, the note
  `[^n]: ...` at the end of its page. The number's span (6.4-point) is
  dropped from the note's first line; where a note's number is followed by a
  run of only spaces (note 2: "2 |  S. Borowski"), the number's span is
  dropped by its size and the run's spaces are kept, so no space is lost
  ("Rolnictwo, w: Dzieje ...", not "Rolnictwo,w:"). Note 18 is italic whole.
- **The article's own slips are kept**, among them:
  - the caption of Ryc. 6 reads "z 1866 r." where the body reads "z roku 1886"
    (p. 47); the map's own entry (p. 56) dates the plan checked against 1866
    and the copy 1869, so the caption's date is not a slip of the body's;
  - note 4 cites "Studia nad dziejami Wielkopolski, t. 3: 1890–1914", while
    Literatura reads "t. 2: 1890–1914" (p. 55) for the same work;
  - Literatura reads "Zarys historii **gospodarstwa wojskowego** w Polsce"
    for Burszta's chapter, where note 3 reads "gospodarstwa **wiejskiego**"
    (the standard work is *Zarys historii gospodarstwa wiejskiego w Polsce*);
  - Literatura reads "Terra Pisdrensis **dawnej i dziś**", note 6
    "Terra Pisdrensis **dawniej i dziś**";
  - the entries of Źródła kartograficzne keep the maps' own spellings
    ("Heinamann", "Rektificirt", "Wiederkopirt", "Płan Kolonii",
    "Kaliszskoj Gubiernii", "sostawliennago", "Czastwym", "Jeometry
    Gotzkejn"), the Grabienice entry repeats its scale ("na podziałkę
    1:20 000 ... 20 000"), and the Lisewo entry's year of the survey is
    unfinished in the print ("w roku 192…");
  - the front matter's "w Narodowym Muzeum Rolnictwa" (p. 41) against the
    body's "Muzeum Narodowe Rolnictwa" (the museum's name is
    *Muzeum Narodowe Rolnictwa i Przemysłu Rolno-Spożywczego*);
  - the article sets "¼ ogółu" (p. 42) and "⅓" (p. 51) as single glyphs;
  - the English summary of p. 57 is the author's own, ungrammatical in
    places ("in polish villages became fundamental socio-economic changes"),
    and stands as printed in both texts.

## The English

Claude's (2026-10-22), page by page from `original.md`, with the same pages,
paragraphs and notes. The headings are translated; the article's own English
block of p. 57 (the title, the summary, the key words) stands as printed,
being the author's, and is not retranslated; its author's line and the
museum's name are rendered ("The National Museum of Agriculture and
Agricultural-Food Industry, Szreniawa").

- Terms: *separacja* separation (the separating of the peasants' lands from
  the manorial ones), *uwłaszczenie* enfranchisement, *ukaz uwłaszczeniowy*
  the enfranchisement ukase, *serwituty* servitudes, *komisja osadnicza*
  the Settlement Commission, *kolonizacja* colonisation, *kolonia* colony
  (the names Kolonia X kept as the villages' names), *melioracja*
  melioration, *rowy odwadniające* drainage ditches, *dreny* drains,
  *spółki wodne / melioracyjne* the water / melioration companies,
  *karczunek* the clearing of forests, *Nowiny* the Nowiny (the place of a
  cut-down forest, the name left as the maps give it), *komasacja /
  scalenie* consolidation / the merging of lands, *szachownica* the
  chessboard (of fields), *parcelacja / rozparcelowany* parcellation /
  parcelled, *Bank Włościański* the Peasants' Bank, *kółka rolnicze* the
  agricultural circles, *miedze* balks, *gubernia* governorate,
  *gmina, powiat, voivodeship* the commune, the powiat, the voivodeship,
  *sygn.* shelfmark, *rękopiśmienna* manuscript.
- The italics follow the print: the front matter's labels and the English
  summary's are bold; the map titles in Źródła kartograficzne whole (with
  their non-italic tails as the print sets them); in the notes and in
  Literatura the titles of the works.
- **The Polish titles of the notes and of Literatura are kept, with an
  English rendering in square brackets** (kucharski2023's rule). The
  fourteen map titles of Źródła kartograficzne are quotations of the maps'
  own titles (German, Russian-transliterated and Polish of the time) and
  stand as printed, each with a bracketed English rendering; the Polish
  descriptive tails after them (the scale, the measures, "rękopiśmienna",
  "sygn.") are translated. Where the print's slip would mislead, the
  bracketed rendering says so (Burszta's "wojskowego"; Jakóbczyk's "t. 2"
  against note 4's "t. 3"; the Grabienice entry's repeated "20 000").

## How it bears on the edition

The article is about the edition's own ground for the 19th century: **fig. 4
is a fragment of the map of the estates of Trąbczyn of 1861** (1:15 000,
shelfmark AN 489/5, drawn 1886 by Kar. Kubicki from Józef Kozłowski's plans
of 1861, p. 56) with the field of the enfranchised peasants marked - the map
of the Russian partition's enfranchisement, made after the ukase of 1864 (the
article's example, p. 45); and p. 48 names **Kolonia Łazińskie and Kolonia
Huta among the new villages founded on the parcelled lands of the Trąbczyn
property** - the edition's Staro- and Nowo-Łazińska colonies (the estate's
two Olęder colonies, APP 53/968/0/-/783), though the article does not say so
and does not date the parcellation. The rest of the article is the general
setting of the nineteenth-century documents: the enfranchisement and
separation in the Prussian partition, the Settlement Commission's
parcellation, the melioration, the consolidation - the era of the summons of
1860 (APP 53/968/0/-/783) and the liquidation tables (APŁ 39/98/0/-/6603,
APP 53/968/0/-/716).

**The index** (`literature/index.yml`): every hit read and ruled (2026-10-22).
The runs of the index over the article found 17 mentions, all ruled:

- **Trąbczyn** - three stands under the standing "Trąbczyn: yes": p. 45 (the
  map of the dóbr Trąbczyn with the field of the enfranchised peasants
  marked), p. 48 (the Kolonia Łazińskie and Kolonia Huta founded on the
  parcelled dobrach majątku Trąbczyn) and p. 56 (the map's own title in
  Źródła kartograficzne);
- **Zagórów** - three stands under the standing "Zagórów: yes" (the town,
  its commune and the places named after it): the gmina of Trąbczyn (pp. 45,
  48) and of Zabłocie (p. 46), not the town's own history;
- **Pyzdry** - three stands under the standing "Pyzdry: yes": the commune of
  Lisewo (p. 54, "gm. Pyzdry") and the place of publication "Poznań–Pyzdry"
  of the author's own 2014 study (p. 42, note 6; Literatura, p. 55);
- **Rzgów** - one stand (p. 48): "gm. Rzgów", the commune of Grabienice -
  the same commune already ruled yes for Chodyła (2015) and Szwiec (2009)
  ("koniński Rzgów"); Rzgów is an estate of the edition, so its page gains
  the mention;
- **Poznań (Posen)** - three stands, the province in the titles of note 1
  and of Literatura's Jackowski entry and in the Przecław map's title
  "Regierungsbezirk Posen" (pp. 42, 55);
- **Kalisz** - one stand, ruled: "Kaliszskoj Gubiernii", the Kalisz
  Governorate, in the Izydorek map's own title (p. 56) - the Governorate
  named from the town ("Kaliszskoj: yes", with the reason written);
- **Konin** - one stand, ruled: "Powiecie Konińskim", the Konin district, in
  the Grabienice map's own title (p. 56) - a statement of geography, unlike
  the "Koniński" refused for Chodyła's headings ("Konińskim: yes", with the
  reason written);
- **Poniatowski** - one refusal, ruled: Juliusz Poniatowski, the Minister of
  Agriculture and Land Reforms, in the citation of his speech of 1938 (p. 52,
  note 18), not the edition's Prince Józef - an exception added to the
  standing default;
- **No hits**: the article's "Kolonia Łazińskie" (p. 48) is not matched, for
  the edition's patterns match only the summons' "Staro-/Nowo-Łazińska"
  forms, and the article does not say which of the two colonies it names;
  likewise "powiatu pyzdrskiego" (the lowercase adjective, pp. 42, 55) and
  the article's other villages (Grabienice, Umień, Kromolice...) have no
  pattern. Not added: a literature pattern for "Łazińskie" would have to say
  which colony, and the article does not (NEEDS_CONFIRMATION).

**Hand-made links** (`literature/links.yml`): none written. The obvious
candidates, the article's pp. 45 and 48 against the edition's
nineteenth-century holdings (the summons of 1860, the liquidation tables),
wait on both sides being read whole (HOUSE_STYLE, "The documents first"):
the article says only that the map of 1861 shows the field of the
enfranchised peasants and that the two colonies were founded on the
parcelled lands, and says nothing of the estate's owners or dates that a
link's sentence could read.

## Open

- **Committed on `main` (2026-10-22, commits 1c2a43c3 and after); not
  pushed, not published.** The merge to the live site waits on the
  editor's word (the standing rule: publish only when the editor says so).
- Whether a literature pattern for the colonies' later name ("Kolonia
  Łazińskie", p. 48) should be added - the article does not say which of the
  two colonies it names (NEEDS_CONFIRMATION).
- The copyright is the Institute's and no open licence is stated; the
  editor ruled the article visible whole, and this note records the ruling,
  but the Licences page does not name the article (it is not an open
  licence); if the editor wants it named there, that is still to do.

## Why it is here

Kept from the work's account, which said it on the page until the voice review of 2026-10-29 (the editor: the reasoning for why a work is relevant is for the notes, not the reader):

> It rests on the standard economic histories and on the author's own studies
> of the Szreniawa collection; it says nothing of the Trąbczyn map's
> particulars beyond its scale and shelfmark.
