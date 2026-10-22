# Kucharski (2023): notes

Robert Kucharski, "Sądownictwo szlacheckie od XV do XVIII wieku",
*Consilium Iuridicum*, vol. 1, no. 3-4 (2022), pp. 226-253, DOI
10.52097/ci.5671; published 10 October 2023 by Academicon, open access, CC BY
4.0. The journal's own citation reads "Kucharski, R. (2023)" while the issue
is dated 2022; the editor chose the citation's year, and the slug follows it.
The author is a public prosecutor of the District Prosecution Service in
Częstochowa (the article's own note 1, with his ORCID 0000-0002-2279-9496),
who has published a series of historical studies of the Polish courts in the
same journal ("Geneza sądów polskich" 2022, "Trybunał Koronny" 2023, the
Księstwo Warszawskie series 2023-2024).

## How it came in (2026-10-22)

The editor: "I want to add a new literary source - 12+Robert+Kucharski.pdf in
the Downloads folder. 'Sądownictwo szlacheckie od XV do XVIII wieku' by
Robert Kucharski. Info on the article is available here:
https://ojs.academicon.pl/ci/article/view/5671." Asked, they ruled:
the slug `kucharski2023` (the journal's citation year), the whole article, and
the pictures skipped.

- The PDF is the article as the journal set it, 28 PDF pages, printed
  pp. 226-253, with a clean text layer. `original.md` is made from it by
  `pipeline/literature/kucharski_pdf.py` (its docstring lists every rule), so
  that every passage can be cited by its printed page:

      python pipeline/literature/kucharski_pdf.py "<Downloads>/12+Robert+Kucharski.pdf" [--report] [--check]

- **`--check` holds every page against the text layer**: for each page the
  script rebuilds the stream of letters the layer carries (the running head,
  the foot, the layout's spaces, the raised note marks and the note numbers
  left out) and asserts the same stream, read back out of `original.md`, is
  unchanged. All 28 pages match. The 45 raised note marks were read in the
  order 1 to 45.
- The pictures (Ryc. 1 on p. 229, Ryc. 2 on p. 237, Ryc. 3 on p. 247) are not
  rendered (the editor's word); their captions ("Ryc. N. ...", italic) and the
  "Źródło:" lines stand in the text, in their place.
- The PDF is **not kept in the repository**. It is the editor's file; the
  open-access copy stands on the journal's page (the `scan:` of `work.yml`).
- Copyright: **CC BY 4.0**, so the work is `visible: true` and shown whole.
  The Licences page (site/rights.md, site/de/rechte.md) names it as the
  literature's one open-access exception.

## The text

Never tidied (`docs/EDITORIAL_RULES.md`). What the script does is in its
docstring; among the things found in making it:

- **The paragraphs.** The article sets its paragraphs flush (no blank line,
  no indent between them) and marks a paragraph's end only by the short last
  line of a justified text; the first paragraph after a heading, a picture's
  caption or a list carries the article's indent (x 133). The script joins a
  paragraph's lines and breaks a new paragraph at an indented line that ends
  a sentence before, or after a short line that ends a sentence; a word
  divided at a line's end is never a paragraph's end. Paragraphs break at the
  pages' ends (their notes stand between the two pieces), as in
  `chodyla_pdf.py`.
- **A word divided over two pages is given whole on the first** (six of
  them: sądowych pp. 231-232, orzekania pp. 233-234, odmawiał pp. 235-236,
  przymiotu pp. 236-237, zaświadczenia pp. 239-240, takich pp. 246-247).
- **The notes** are at the foot of each page, numbered through the article
  (1 to 45); a note's raised mark in the text becomes `[^n]` against the word
  it follows, the note `[^n]: ...` at the end of its page. None runs over a
  page's end.
- **The author names in the notes are printed letterspaced** ("K u c h a r s
  k i"): the spaces are the setting's, not the word's, and are taken out where
  the joined word is one the article prints elsewhere within a line
  (Kucharski, Zarański, Schulz, Wybicki, Kutrzeba, Naworski, Góralski,
  Bardach, Leśnodorski, Pietrzak, Pawlikowski, Sawicki, Kaczmarczyk,
  Dąbkowski, Hube, Siedlecki, Balzer, Kulecki, Borucki, Zaleski, Makiła,
  Duklan, Matuszewicz, Koźmian, Łoziński, Turska, Wasylewski, Chodorowski,
  Rafacz). **Note 36 keeps "M B o r u c k i" as printed**: the initial's
  point is missing in the setting, and "Mborucki" is no word the article
  prints, so the letterspaced run is not joined.
- **The dash glyph of the Symbol font** (F02D, the layer's substitute for a
  dash with no code of its own) is the article's "–"; on the ORCID line of
  note 1 it is the hyphen of 0000-0002-2279-9496 and is set so.
- **The article's own slips are kept**, among them: "ale zdarzało się także,
  iż w razie potrzeby." (p. 231, the sentence breaks off), "skald" for
  "skład" (p. 231), "w XVII wieku... które nie zbierają się" for the sejmiks'
  fall, though p. 233 dates the same fall "W XVII wieku sądy ziemskie weszły
  w okres stagnacji" (the article repeats itself, p. 232 and p. 233),
  "ścignie" for "ściganie" (p. 234), "ku egzekucji" for "przy braku
  egzekucji" read as printed (p. 245), note 14's stray closing quotation mark
  after "Geneza sądów polskich”, note 20's "s. 151, t. II, s. 151" (the same
  page twice), note 2's "Warszawa 2022, Collegium Iuridicum 2022" (both), and
  the **Bibliografia prints Kutrzeba's book twice** (items 15 and 16). The
  key words' list is set in the genitive in places ("podkomorskich,
  miejskich") and repeats "sędzia", "zabójca"... as the print has them.

## The English

Claude's (2026-10-22), page by page from `original.md`, with the same pages,
paragraphs and notes. The headings are translated; VARIA (the journal's
section label) stands. Quotations are given in English; the bibliography of
the notes and of the Bibliografia keeps the Polish titles, with an English
rendering in square brackets.

- **The article's own English abstract and key words (pp. 252-253) stand as
  printed** - they are the author's, published by the journal, and are not
  retranslated. They differ from the Polish in detail (the Polish "wielość
  typów sądów" becomes "a multitude of types of judgments"; "sędzia" of the
  key words becomes "magistrate"); the English of pp. 226-227 is Claude's
  translation of the Polish, and the two stand apart as the article prints
  them.
- Terms: *sąd ziemski* land court, *sąd grodzki* municipal court (the
  edition's own usage, and the article's "municipal court" in its English key
  words), *sąd podkomorski* the podkomorzy's court, *podkomorzy* podkomorzy
  (the chamberlain), *podsędek* sub-judge, *pisarz* scribe, *woźny* usher,
  *instygator* instygator (the public prosecutor of the estate order), the
  article's own "instigator" kept only in its key words of pp. 252-253,
  *asesor* assessor, *sędziowie społeczni* lay judges, *starosta* starost,
  *sejmik* sejmik, *nagana sędziego* the judge's reprimand, *apelacja*
  appeal, *rozprawa zaoczna* default hearing, *kocz* kocz (a court fee),
  *pamiętne* pamiętne (the reprimand's fee), *roczki powiatowe* the district
  sessions, *skrutynium* skrutynium (the official inquiry), *mocja*, *gravamen*,
  *male obtentum* as set, *wieża dolna/górna* the lower/the upper tower,
  *grzywna* fine, *grzywna* (the money) mark, *łokieć* ell, *zajazd* armed
  raid, *banita/banicja* outlaw/banishment, *gołota* the landless nobility,
  *posesjonat/posesor* landholder, *królewszczyzna* royal domain, *oprawca*
  oprawca (the headsman-official; the article's own explanation is carried),
  *wiecowe* the wiec courts, *sądy ziemiańskie* of the Four-Year Sejm the
  noble courts (distinguished from the abolished land courts in the sentence
  itself).
- The italics follow the print: the abstract, the key words and the captions
  whole; in the body *sui generis*, *male obtentum*, *infamis*, *Volumina
  Legum* (p. 242); in the notes *dignitates*, *officia*, *op. cit.*

## How it bears on the edition

The article is a general survey, not a study of the edition's ground: it
cites no court book and names no person or place of the edition's estates.
What it gives the edition is the setting of the books it holds (the land and
municipal books of Konin and Kalisz): the kinds of court that kept them, the
officers who wrote and kept them, the course of a process in them, the force
of an entry ("wieczność ksiąg", pp. 240-241) and the practice of the roczki
sessions, the summons and the default ruling - the machinery behind the
documents transcribed in `units/`. Where a question needs it, a passage of
the article can be cited against a holding's reading.

**The index** (`literature/index.yml`): every hit read and ruled. Five hits
stood, all already ruled from the other works: Józef Wybicki (quoted on
p. 230, in note 6 and in the Bibliografia, item 32 - the edition's senator
and voivode, the ruling made for Pachoński 1973), and the Warszawa of two
bibliographical references (notes 5 and 26, the Schulz edition). One false
friend ruled out: **"Brześć"** (p. 246) - the municipal court "w Brześciu" of
the story of Wacław Matuszewicz is Brześć on the Bug (Brest), in the district
of Łuck, told from the memoirs of the Matuszewicze; not the edition's
Brześć Kujawski. Recorded in `docs/NEEDS_CONFIRMATION.md`.

**Hand-made links** (`literature/links.yml`): none yet. Nothing in the
article names the edition's people, estates or holdings; if the editor wants
one - say, the article's pages on the kancelaria and the wieczność of the
books (pp. 239-241) against the court books themselves - the passage and the
holding are to be read on both sides first (HOUSE_STYLE, "The documents
first").

## Open

- Published with the merge to `main` (2026-10-22).
- The Licences page (site/rights.md, site/de/rechte.md) now names the
  article's CC BY 4.0 as the literature's one open-access exception.
- The Brześć ruling is Claude's identification (NEEDS_CONFIRMATION).
