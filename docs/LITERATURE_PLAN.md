# Plan: the literature

Status: **agreed with the editor 2026-10-19; texts brought in and cut into
passages (`corpus/literature/`); the site pages, the index and the first
links built and published (2026-10-19). The second set of six works
(section 10) built, indexed, linked and published the same day.** When the work is done, the standing parts move into
`DATA_MODEL.md`, `NEW_UNIT.md` and `HOUSE_STYLE.md`, and this file becomes a
record of how it was decided.

The aim (the editor, 2026-10-19): books and articles that help to understand
the archival sources, kept apart from them, so that when every holding is in
the editor can put targeted questions to the whole: "was Triebenfeld falsely
inflating the value of the Trąbczyn estates?", "did the Olęders' customs
shape how they farmed?". The literature is context for those questions. It is
not part of the edition's text and is not edited to its standard.

---

## 1. The works

Supplied by the editor in October 2026 (their folder "Books"), each in its
original language and in English. **The English translations were made by
Claude** (the editor, 2026-10-19).

| Slug | Work | Language | Page marks | On the site |
|---|---|---|---|---|
| `paciorkowski1776` | Marcin Paciorkowski, *Regula processus granicialis campestris Regni Poloniae*, 2nd ed., Częstochowa 1776 | Latin | `[p. N]` | yes |
| `held1801` | [Hans von Held], *Die wahren Jacobiner im preussischen Staate*, 1801 | German | `[p. N]` | yes |
| `feuerbraende1807` | [Friedrich von Cölln], *Neue Feuerbrände*, vol. 1, parts 1-3, Amsterdam and Cölln 1807 | German | `[p. N]` | yes |
| `materialien1861` | [anonymous], *Materialien zur Geschichte polnischer Landestheile unter preussischer Verwaltung*, part 1, Leipzig 1861 | German | `— N —` | yes |
| `guradze1898` | Franz Guradze, *Der Bauer in Posen*, Halle 1898 | German | none yet | yes |
| `seidel2018` | Hans-Joachim Seidel, *Friedrich Ludwig Fürst zu Hohenlohe-Ingelfingen*, Ulm 2018 | German | `[p. N]` | **no** (§4) |

The second set (their folder "Books_2", 2026-10-19; section 10):

| Slug | Work | Language | Page marks | On the site |
|---|---|---|---|---|
| `breyer1935gaue` | Albert Breyer, "Deutsche Gaue in Mittelpolen", 1935, chapters V and VI (Kalisz and Konin) | German | `[p. N]` | yes |
| `breyer1935mutterland` | Albert Breyer, "Ostdeutschland als Mutterland der deutschen Siedlungen in Mittelpolen", 1935 | German | `[p. N]` | yes |
| `breyer1938` | Albert Breyer, "Die deutschen ländlichen Siedlungen des mittelpolnischen Warthebruchs", 1938 | German | `[p. N]` | yes |
| `zychlinski1885` | Teodor Żychliński, *Złota księga szlachty polskiéj*, vol. 7, pp. 187-188 (the Prusimski) | Polish | `[p. N]` | yes |
| `zychlinski1891` | Teodor Żychliński, *Złota księga szlachty polskiéj*, vol. 13, pp. 219-225 (the Miączyński) | Polish | `[p. N]` | yes |
| `pachonski1982` | Jan Pachoński, "Prusimski ... Antoni", *Polski Słownik Biograficzny*, vol. 27, pp. 582-584 | Polish | `\[N\]` | yes |

Found when they were brought in:

- **`blackregister.txt` is not a separate work.** It is pages 140 to 171 of
  the Materialien, word for word: the black register, the list of the Crown
  and church estates given away in 1794-1798 (printed, the Materialien says,
  from a manuscript in Held's papers), with Triebenfeld's entry (16/38) on
  pages 162-164. It is not brought in twice.
- **Triebenfeld's entry in the black register is not about Trąbczyn**: it
  lists Piotrow, Koscielna Wies, Glogowa, Krzywo Sondowo and the lordship of
  Lasky, with their value at the gift, the Kalisz valuation of 1797 and the
  sale prices of 1801. It bears on how such estates were valued, not on
  Trąbczyn's value itself.
- **The Paciorkowski file named "(French)" is the Latin original.**
- **Guradze is of 1898**, not 1918 as the file name had it (the editor; the
  preface is dated "Halle a. S., im Frühjahr 1898"). The archive.org copy
  (`derbauerinposen00guragoog`, digitised by Google from the University of
  California, 108 pages) says the work appeared in the *Zeitschrift der
  historischen Gesellschaft für die Provinz Posen*. The editor's text has no
  page numbers; the editor will correct it and add them later. A way to do
  it: archive.org's page-by-page OCR (`_djvu.xml`) gives the first words of
  every printed page, which can be found in the editor's text.

## 2. What the literature is, and what it is not

- **Each work is brought in whole, as the editor supplied it, and never
  tidied**: the same rule as a transcription (`EDITORIAL_RULES.md`). A
  slip in the editor's text is noted, not corrected, unless the editor
  corrects the file.
- **It is not a holding.** No scans, no marks of doubt, no line-by-line
  review, no spot sheets. It never counts in the edition's figures
  (documents, pages, marks of doubt), never appears in the document lists,
  the browse page or the timeline. A newspaper item or a printed edition of
  a single charter about the estate is still a holding (Kuryer Polski, the
  Kodeks): the test is whether it is a document *of* the estate's history or
  a work *about* that history or its setting.
- **Each work says what kind of witness it is.** Held (1801) and Cölln
  (1807) were pamphleteers on opposite sides of the quarrel over the gifted
  estates; the Materialien (1861) is an anonymous, openly polemical
  collection; Guradze (1898) a scholarly study; Seidel (2018) a modern
  biography; Paciorkowski (1776) a practitioner's handbook. An answer to a
  question says "Held alleged in 1801 that...", never "the literature
  says". The work's `work.yml` carries a short account of its author, its
  purpose and how far to trust it, in both languages.
- **The English is Claude's.** It is not checked whole. When a work comes
  in, a few pages are read against the original and the result is noted in
  its `notes.md`. Any passage an answer rests on is read against the
  original before it is quoted. The work's page says who made the English.

## 3. Where it lives

```
literature/<slug>/
  work.yml        bibliography, kind, language, page-mark form, visibility,
                  the account of the work (EN and DE), who made the English
  original.md     the editor's file, unchanged (git may change its line
  english.md      endings, nothing else)
  notes.md        how it came in, the alignment, the spot check of the English
corpus/literature/
  index.json      every work (bibliography, account, visible) and its
                  passages (key, part, page, line and length per language)
  <slug>/<key>.<lang>.txt   one passage in one language (la, de or en)
```

`pipeline/literature/build_literature.py` cuts each work into passages at its
printed page marks, pairs the original's page with the English's, and
reports any page found in one and not the other. What stands before the
first numbered page is the passage `front` (the two languages differ there:
Held has five unnumbered pages in one and seven in the other); an unnumbered
page later in the book is keyed by the page before it (`257-u1`). Where page
numbers begin again in each part (the Neue Feuerbrände) the key carries the
part (`3-133`). A notes section gathered at the end (the Materialien's
"Anmerkungen") is the passage `notes`. A work with no page marks (Guradze,
for now) is cut by chapter. The script checks that each file is put back
together exactly from its passages. Each passage file opens with comment lines naming the
work, the page and the citation form, like `corpus/text/`, so a search hit can
be cited from the file it was found in.

## 4. Seidel (2018): in the repository, not on the site

The book is under copyright, and its imprint forbids copying, translating or
electronic use without the author's consent. The repository is public. Claude
put three choices to the editor (a git-ignored folder, a separate private
repository, or the public repository with no page) and said that committing it
publishes it in the copyright sense, whatever the site shows. **The editor
chose the public repository with no page** (2026-10-19), because the book
matters for context. So:

- `work.yml` has `visible: false`. The site build skips such a work entirely:
  no page, no passage, no hit in the search index, no "In the literature"
  line on a person's page, nothing under `site/`.
- Its passages are written to `corpus/literature/` like the others, for
  questions.
- A later choice the editor may make: list it on the Literature page by its
  bibliographic details alone.

## 5. On the site

- **"Literature" in the menu** (the editor, 2026-10-19), "Literatur" in
  German, after Sources. The page lists the visible works, each with its
  account. **The book's title is the heading** on the list and on the
  work's page, the citation ("Materialien (1861)") under it (the editor,
  2026-10-19); the browser tab keeps the short citation.
- **One page per work**: the account, who made the English, the contents,
  and the text page by page, each page headed by its printed number so it
  can be cited ("Materialien, p. 162"). **One text at a time, the English
  first, with a button for the original** (the editor, 2026-10-19: as a
  reader switches the views of a document; the two texts side by side
  were "not ideal").
- **Links into the edition**, built up in this order:
  1. the existing index of people, places and estates run over the passages;
     every hit read before it goes live (the index has matched wrongly
     before on a new kind of text: WORKING_NOTES, "Polish text and
     German-made patterns"). A person's or place's page then has a separate
     box, "In the literature", listing the passages that name them;
  2. links written by hand: a passage tied to a document or a holding, with
     a sentence saying why (`literature/links.yml`). The first: the black
     register's entry on Triebenfeld as the Feuerbrände printed it (part 2,
     pp. 83-84), Cölln's remark on it (part 3, pp. 133-134) and the reprint
     of 1861 (pp. 162-164), tied to the Prince's correspondence on his
     estates;
  3. the glossary may cite a passage as its `source:` (Guradze on peasant
     tenure, Paciorkowski on the boundary procedure).
- **The timeline**: perhaps later, selectively (the editor, 2026-10-19). Not
  in this plan.

## 6. Order of work

1. Bring all six works in; build the passages; report the alignment. *(done
   2026-10-19; what was found is in each work's `notes.md`)*
2. The site pages, tried first with the Materialien; then the other visible
   works. *(done and published 2026-10-19: section 7)*
3. The index of people and places over the passages, read hit by hit.
   *(done and published 2026-10-19: section 8)*
4. The hand-made links, beginning with the black register. *(the black
   register done and published 2026-10-19: section 9)*
5. Guradze's page numbers, when the editor has corrected the text.
6. Perhaps: the black register as a table (recipient, estates, district,
   value at the gift, later valuation, sale price), which bears directly on
   the question of inflated values.

## 7. How the site pages are made (2026-10-19)

- `pipeline/literature/literature_site.py` (a step of regenerate.py, after
  build_literature.py) reads `corpus/literature/` and writes
  `site/_data/literature.yml` (the list page) and one page per visible work
  in each language: `site/_literature/<slug>.md` (/literature/<slug>/) and
  `site/_literature_de/<slug>.md` (/de/literatur/<slug>/). All three are
  generated; never edit them by hand. A work with `visible: false` gets
  nothing under `site/`.
- The page: the work's facts and account (`work.yml`), a warning that the
  English is Claude's and the original decides, a list of pages to jump
  to, then every passage as a section with an anchor `#p-<key>` (for
  example `/literature/materialien1861/#p-162`). Each section holds both
  texts; the buttons above the first page ("English", and the original's
  language) show one of them, the English first, and the choice is kept
  between works (`site/assets/literature.js`, localStorage `tf-lit-view`).
  Without the script both stand one under the other. A passage that
  has no English (Paciorkowski p. 27) says so.
- Only the rendering is changed, never the words: footnote markers become
  links to their notes, headings sit two levels down, a "|" outside a table
  and a name printed as asterisks ("v. ****d") are escaped, and a line
  break inside a paragraph is kept. The script's docstring says why.
- `verify_site.py` checks that each visible work has its two pages and that
  neither the slug nor the title of a hidden work appears anywhere in the
  built site. The timeline's citations "Seidel 2018, ch. ..." are allowed:
  they cite the book and give none of its text.

## 8. How the index is made (2026-10-19)

- `pipeline/literature/literature_index.py --check` (a step of
  regenerate.py, after literature_site.py) runs the edition's own patterns
  for people and places (`pipeline/build/entities.py`) over the originals
  of the visible works. The English is not searched (the original decides,
  and every hit would count twice), and neither is Seidel.
- **Every hit was read before it was ruled** (Claude, 2026-10-19). The
  rulings are in `literature/index.yml`, one per name and spelling found:
  yes, no with the reason, or a default with the passages that take the
  other answer. The first run found 2,690 hits in 240 pairs; 2,508 stand.
  Most of the rejected ones are words ("Sommer" the season, "Gärtner" the
  cottager, "Kuh" the cow), other men of the same name (Danckelmann the
  Silesian minister, Raumer the historian, the regiments Grevenitz and
  Zastrow), or measures ("Berliner" and "Breslauer" bushels).
- The books print some names in forms the edition's patterns miss: the
  black register gives Trąbczyn as "Trombczyn" and "Trobozyn", Feuerbrände
  writes "Hohenloh". These are added for the literature only, under
  `patterns:` in the same file, and ruled like the others. Without them
  Trąbczyn had no hit at all.
- `--check` fails on a hit with no ruling (a new work, or Guradze's text
  corrected) and on a ruling that names a passage where its spelling is no
  longer found, so nothing unread reaches the site. `--sheet` writes every
  hit in context to `review/literature/mentions.md` for reading.
- Where a name in a book is Claude's identification and not the book's
  own statement, the comment at its ruling says so. The editor accepted
  the first five (2026-10-19): Grevenitz, Stössel, Nöldichen and
  Wartensleben on Claude's reading, Stenger once the evidence was written
  out (Karge and Unruhstadt are one town). The editor cannot check such a
  thing in the German: write out what the identification rests on (the
  book's words, the edition's document, the place) so they can judge it
  without reading either.
- **On the site**: a person's entry on /people/ and an estate's on /places/
  has a closed list, "In the literature: N passages", under its documents:
  each work's citation, then a link to every page that names them
  (`site/_includes/lit-mentions.html`, from
  `site/_data/literature_mentions.yml`). 35 people and 11 estates have one.
  Places that are not estates have no list (the Places page shows the
  estates only); their hits stay in `corpus/literature/mentions.json` for
  questions.

## 9. How the hand-made links are made (2026-10-19)

- `literature/links.yml`: each link names passages (`<work>/<key>`),
  documents (their uids) and a sentence in English and German saying why
  they belong together. The sentence is read on both sides, so it names the
  book, the document and what each says; every figure in it was read in
  both (Claude, 2026-10-19). Where they disagree it says so, and the
  difference is flagged in NEEDS_CONFIRMATION and recorded in the work's
  `notes.md` (the editor's rule of 2026-10-20: the documents first,
  `docs/HOUSE_STYLE.md`).
- `literature_site.py` checks every link (the passage exists, its work is
  shown, the document exists) and stops if one fails. Under each linked
  passage it puts a box, "In the edition", with the sentence and a link to
  each document ("Oe 1 Bü 9454, document 85 (4 December 1798)"); it writes
  `site/_data/literature_links.yml`, from which a document's page has an
  entry "In the literature" in the box "About this document": the sentence
  and the pages by work, in the reader's language. `verify_site.py` checks
  both sides of every link.
- **The first four links, the black register** (26 passages, 10
  documents):
  1. *The Prince's gift and the exchange for Krotoszyn*: the register's
     entries on the Prince (Materialien pp. 145-146, 159; Feuerbrände 2-69,
     2-80) and Cölln's correction (3-132), with the gift of 1796
     (I. HA Rep. 7 C Nr. 3570, document 1), the King's refusal of December
     1798 and the Prince's answers (Oe 1 Bü 9454, documents 85, 86, 87, 97,
     101). The register says the Prince himself put the yield at 50,000 a
     year; his letter to the King of December 1798 gives 41,500, the King's
     40,500.
  2. *Triebenfeld's own estates*: his entry (Materialien pp. 162-163;
     Feuerbrände 2-83, 2-84) and Cölln's remark (3-134), with his letters
     of 1799 to 1801 (documents 104, 108, 112). The same valuation (over
     700,000) and resale (750,000) in both; for his own sale to Prince
     George the register gives 400,000, his letter 280,000.
  3. *Krotoszyn*: the "black book" quoted in the Materialien (p. 163) on
     Triebenfeld's administration and Früson's lease at 30,100, with the
     letters that give the same rent (documents 85, 86, 101).
  4. *The other gifts*: the entries on Bischofswerder, Treskow, Zastrow,
     Rüchel and Dolffs, with Triebenfeld's letter of 13 March 1799
     (document 103), which sets the Prince's gift beside the same ones.
     The letter's general was read "Ruchts"; Claude took him for Rüchel,
     the editor agreed, and the scan reads "Ruchels" (2026-10-19; the
     transcription corrected by
     `units/oe1bu9454/intake/scripts/ruechel_103.py`).
- Next, when the editor wants them: Held's book on Krotoszyn (he was there
  in the 1790s) against the same letters, and the passages on the
  Olęders and the boundary procedure (Guradze, Paciorkowski) against the
  holdings they bear on.

## 10. The second set (Books_2, 2026-10-19)

The editor's rulings (2026-10-19):
- The PSB entry is dated 1982 ("1982 is fine to use").
- **Unless the editor says otherwise, every English in their files is a
  machine's.** So each was read against the original, and the English on
  the site is Claude's, written from the original (the PSB file's machine
  English was wrong in substance: `literature/pachonski1982/notes.md`).
- Dennerlein's forewords to her reissues of Breyer are left out.
- Of "Deutsche Gaue in Mittelpolen" only the chapters on Kalisz and Konin
  (V and VI) are brought in.
- Vol. 7 of the Złota księga begins with Krzysztof Prusimski on p. 187; the
  print's "wrzysztof" is kept as printed.
- **A work opens on the English** (section 5).
- **No German translation is made** of a work that lacks one: the site's
  German page of such a work has the original and the English, and that is
  an accepted gap.

How each came in is in its `notes.md`, with the command that made its
`original.md` where one did:
- The three Breyer articles are Dennerlein's digital reissues
  (UpstreamVistula.org, PDF). `pipeline/literature/upstream_pdf.py` makes
  `original.md` from the PDF's text layer (its docstring lists every
  rule: headings, spaced type, footnotes, tables, pages printed on their
  side). They are cited by the reissue's pages.
- Żychliński's two extracts are photographs. Vol. 7's had no text, and vol.
  13's text layer is unusable; both were rendered with PyMuPDF and read in
  session, and `original.md` was written by hand.
- The PSB entry is the Polish half of the editor's file, unchanged.

The index (section 8) was run over the six and every hit ruled: 3,200 hits
in the eleven visible works, 2,946 standing. Claude's identifications not yet
accepted are listed in `docs/NEEDS_CONFIRMATION.md` ("The literature").

**Eleven hand-made links** (section 9), every figure read in the book and
the document (`literature/links.yml`, after the comment "The books of the
second set"):
- Breyer (1938) on the lease of 1806 (APP 53/968/0/-/801, documents 2 and
  3) and on Weigel (Oe 1 Bü 9454, letters 220 and 284);
- Breyer (1935a) on Łazińsk Holland (Konin Gr.136, the inspection of 1754);
- Żychliński (1885) on the line from Krzysztof to the Starost (Konin Gr.145,
  Gr.118 document 23, Gr.136, 53/6/0/-/40);
- Żychliński (1891) on Michalina's marriage (five letters of Oe 1 Bü 9454),
  her mother's death (Nr. 1414, document 2) and Włodzimierz (the summons of
  1860, APP 53/968/0/-/783);
- Pachoński (1982) on the boundary commission (Konin Gr.145), the
  confiscation (Nr. 3570), Venice (Nr. 1414) and the restitution of 1807
  (the two AGAD holdings).

Each work's `notes.md` says which planned links were not written and why
(for one, the Łazińsk tables of 1868 do not name the estate's owner).

Found in the checking: **the dispatch from Venice of 14 December 1796
already speaks of the death of Prusimski's wife**, against Żychliński's
"2 September 1797". And the lease of 1806 differs from Breyer's account
in three points: the date, the dike clause, and pasture and wood.

## 11. Three more works (2026-10-20)

| Slug | Work | Language | Page marks | On the site |
|---|---|---|---|---|
| `pachonski1973` | Jan Pachoński, "Les Polonais dans la République de Venise (1794-1797)", in *Italia, Venezia e Polonia tra illuminismo e romanticismo*, Florence 1973, pp. 237-256 | French | `[p. N]` | yes |
| `maczak1968` | Antoni Mączak, "Export of Grain and the Problem of Distribution of National Income in the Years 1550-1650", *Acta Poloniae Historica* 18, 1968, pp. 75-98 | English | `[p. N]` | yes |
| `szwiec2009` | Piotr Szwiec, *Katalog architektury regionalnej dla obszaru „Puszczy Pyzdrskiej”*, Pyzdry and Poznań 2009 | Polish | `[p. N]` | yes |

- **Pachoński and Mączak were first built as holdings** (`units/`), by a
  desktop session that had not fetched the cloud's work and did not know the
  literature existed. The editor: "Literature definitely has its own page!
  Don't touch the Sources page, that's for primary-source material from
  archives." Both were moved here the same day; their texts and English were
  carried over unchanged in their words (each work's `notes.md`).
- **The list page, by author** (the editor, 2026-10-20): the works in the
  order of their authors' surnames (`author_sort`), each with the author
  (surname, first name), the title as printed and the English title in
  italics under it, where it was published, and its language. The "Author"
  line and the short citation are no longer shown in the list.
- **Pictures** (`figures` in `work.yml`): Pachoński's map (p. 246), Mączak's
  map (p. 81) and chart (p. 97), and Szwiec's 80 pages of photographs and maps,
  each above its page's text.
- **A work printed in English** (Mączak): no `english.md`, one text, no
  buttons.
- Szwiec's catalogue was made from its Word-printed PDF by
  `pipeline/literature/szwiec_pdf.py`; its English by
  `literature/szwiec2009/make_english.py`. Its captions name no village, so
  no photograph is tied to Trąbczyn, though Trąbczyn, Wrąbczynek,
  Wrąbczynkowskie Holendry and Orlina are among the villages it studied.
- The index: the new hits were read and ruled (`literature/index.yml`); the
  ruling "Venise: no", made for a title in the PSB, had to become a default
  with that one exception, or it would have dropped every Venice in
  Pachoński (1973).

## 12. Wąsicki (1953) (2026-10-21)

| Slug | Work | Language | Page marks | On the site |
|---|---|---|---|---|
| `wasicki1953` | Jan Wąsicki, "Kolonizacja niemiecka w okresie Prus Południowych 1793 – 1806", *Przegląd Zachodni* 1953, no. 9-10, pp. 137-179 | Polish | `[p. N]` | yes |

From the editor's scanned PDF; its OCR was not taken over, every page was
read from the images (`literature/wasicki1953/notes.md`). The Poznań
department's table of colonies (pp. 162-167, printed sideways), the plans and
the fold-out table of costs are shown as pictures. It names the Hohenlohe
estates of Zagórów and Trąbczyn and the colonies founded there in 1805 (pp.
174-176, from Breyer 1938): a hand-made link to APP 53/968/0/-/801, document
3 (the lease of 1806), is the obvious next one, once the figures are read on
both sides.

## 13. Chodyła (2015) (2026-10-21)

| Slug | Work | Language | Page marks | On the site |
|---|---|---|---|---|
| `chodyla2015` | Zbigniew Chodyła, *Zarys najstarszych dziejów osad olęderskich w Puszczy Pyzdrskiej 1746 – 1793*, Pyzdry 2015 | Polish | `[p. N]` | yes |

The editor gave a Word conversion of the book (".docx.md") and a machine
English. The book's own PDF, in their Books folder, was used instead for the
text: it has the printed pages, the notes at the foot of each page and the
25 illustrations. `pipeline/literature/chodyla_pdf.py` makes `original.md`
from its text layer, and the result was checked word by word against the
editor's file. The machine English was read and not used: the English is
Claude's, page by page (`literature/chodyla2015/notes.md`).

The book is about the edition's own ground: the founding of the Trąbczyńskie
Stare Olędry and the Luśnie Olędry by Paweł and Katarzyna Prusimski in 1746,
Łazy, the Trąbczyńskie Nowe Olędry, and 55 other Olęder settlements of the
Pyzdry Forest to 1793, from the court books the edition holds (Konin Gr.145,
Gr.136, Gr.153, Kalisz Gr.414, the summons of 1860). Five of its details
differ from the edition's documents (the owner in 1860, the date of the
sitting of 1782, the wood Lusina in 1754, the hearths of 1789, the date of
the register of 1797). The edition takes the documents (the editor's rule of
2026-10-21) and NEEDS_CONFIRMATION records each. Six hand-made links
(`chodyla2015-*`). Published 2026-10-21 at the editor's word, with Wąsicki
(section 12).

## 14. Boniecki (1900) (2026-10-21)

| Slug | Work | Language | Page marks | On the site |
|---|---|---|---|---|
| `boniecki1900` | Adam Boniecki, *Herbarz polski*, part I, vol. 2, Warsaw [1900], "Chełmscy h. Ostoja" (from p. 364), the branch that held Łukomia | Polish | none: cut at headings (`chapter`) | yes |

The editor gave a saved page of M. J. Minakowski's online edition of
Boniecki (article 2.976), "a source for the family tree of the Chełmski
family", and asked for only the part on Stanisław Chełmski, his brother
Heliodor, the transfers of Łukom, and Łukom, Bukowe, Łomów and Imielno
("Mielna" there). So the work is an excerpt, like Żychliński (1891):
`literature/boniecki1900/make_original.py` takes items 2.976.162-240 of the
running text, joins each paragraph's lines, marks what it leaves out "[…]"
and heads each part with the item numbers; the saved page is not kept (its
header carries the editor's login). The English is Claude's.

What the documents say first: the brothers of 1728 (APP 53/6/0/-/40), the
brothers of 1775 (Konin Gr.145) and the four estates of 1778 (Konin Gr.117)
agree with Boniecki; Heliodor's canonry and the year of Stanisław's title
differ, and the edition follows the documents (NEEDS_CONFIRMATION,
"Boniecki (1900)"). Four hand-made links (`boniecki1900-*`). Published
2026-10-21 at the editor's word.

## 15. Encyclopedia of Camps and Ghettos (2012), the Warthegau (2026-10-21)

| Slug | Work | Language | Page marks | On the site |
|---|---|---|---|---|
| `dean2012warthegau` | *The USHMM Encyclopedia of Camps and Ghettos, 1933-1945*, vol. II A, ed. Martin Dean and Mel Hecker, Indiana University Press 2012: the chapter "Warthegau Region", pp. 34-39, 48, 57-61, 63-64, 99-100, 120-121 | English | `[p. N]` | yes |

The editor gave the JSTOR download of the chapter and named the pages for
the twentieth-century part of the edition: the introduction and the entries
on Chocz, Grodziec, Kalisz, Konin, Rzgów and Zagórów (the hamlet ghettos of
Kreis Konin, 1940-1941). `pipeline/literature/warthegau_pdf.py` reads the
text layer (an accent font for the Polish letters, spaces of no width,
hyphens told apart by the space the layer keeps after a real one) and
checks every letter against the PDF. The book is CC BY-NC-ND 4.0: shown in
English as printed, no translation, pictures left out (their lenders'
credits), captions given. The PDF is not kept (its feet carry the
download's internet address). "Betchatów" is Bełchatów (editor). No links
yet; how much bears on the edition is the editor's to say. Published
2026-10-21 at the editor's word.

## 16. Frost (2007), the nobility of Poland–Lithuania (2026-10-21)

| Slug | Work | Language | Page marks | On the site |
|---|---|---|---|---|
| `frost2007` | Robert I. Frost, "The Nobility of Poland–Lithuania, 1569–1795", ch. 9 of H. M. Scott (ed.), *The European Nobilities in the Seventeenth and Eighteenth Centuries*, vol. II: Northern, Central and Eastern Europe, 2nd ed., Palgrave Macmillan 2007, pp. 266-310 | English | `[p. N]` | yes (given a page at the editor's word; what it displays is a later choice) |

The editor's PDF (a scan with no text layer) holds, beside the Frost
chapter, the volume's Guides to Further Reading (pp. 410-415, with the
Poland-Lithuania section pp. 411-415) and the opening page of the
Russian-nobility chapter (p. 311). Only Frost's article was transcribed, at
the editor's word ("only the article by Frost"); what was left out is
described in `literature/frost2007/notes.md`, and the guides are not to be
added (the editor: "Don't add the guides from the PDF", 2026-10-21). The
book is under copyright (its imprint forbids reproduction without written
permission; the chapters (c) their authors 1995, 2007): put in with
`visible: false` after section 4, then given a page at the editor's word
the same day ("Give it a page - I'll need to decide later what gets
displayed"); what the page displays is a later choice of theirs
(NEEDS_CONFIRMATION). Read spread by spread from page images at
200 dpi, doubtful spots at 300 dpi; not OCR. The chapter's notes are
endnotes, kept on their printed pages so a note can be cited (no `notes:`
in work.yml). The passage index reads it now that it has a page; its four
new pairs are ruled (the Radziwiłł magnates, Hieronim Florian's given
name and Augustus II are not the edition's; Repnin the Russian ambassador
is ruled to the letters' Prince Repnin on Claude's reading, waiting on
the editor).
