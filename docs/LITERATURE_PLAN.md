# Plan: the literature

Status: **agreed with the editor 2026-10-19; texts brought in and cut into
passages (`corpus/literature/`); the site pages built (2026-10-19), not
yet published.** When the work is done, the standing parts move into
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
  and the text page by page, original and English side by side, each page
  headed by its printed number so it can be cited ("Materialien, p. 162").
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
   works. *(done 2026-10-19, not published: section 7)*
3. The index of people and places over the passages, read hit by hit.
   *(done 2026-10-19, not published: section 8)*
4. The hand-made links, beginning with the black register.
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
  example `/literature/materialien1861/#p-162`), original on the left and
  English on the right (one above the other on a phone). A passage that
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
