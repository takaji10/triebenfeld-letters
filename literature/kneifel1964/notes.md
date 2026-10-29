# Kneifel (1964): the church history, the excerpt

Eduard Kneifel, *Geschichte der Evangelisch-Augsburgischen Kirche in Polen*,
Selbstverlag des Verfassers, Niedermarschacht über Winsen/Luhe 1964 (printed
by Karl Müller, Roth bei Nürnberg). Added 2026-10-22 at the editor's word:
"Add this literary source to the project ... Use the two .md files for the
German and English transcriptions/translations. Be careful not to go too deep
into this text: don't call out new people/estates/etc. unless it's something
related to Trąbczyn/Zagórów areas. This is a large text, so surely large
parts of it will also not be relevant to the project. Don't labour intensively
over it."

The editor's choices of the day, asked before the work began: the excerpt
carries **the place-named pages and the two colonisation sections** that set
them (not only the place-named pages); the work is **shown on the site**
(visible), the modern work's copyright named (below); **only the excerpt
scripts and the cut pages are committed**, not the two source files.

## The source

The editor's folder on their machine:
`J:\Documents\Archive\Genealogy\References\Books\History of the
Evangelical-Augsburg Church in Poland (DE) (Kneifel, 1964)` — a PDF of the
book (333 PDF pages, not kept), a photograph (1939PLP2.jpg, not kept), and
two Markdown files: the German transcription "…(complete, with page numbers,
GFM footnotes).md" (UTF-8, 1,174,670 characters, printed pages [7] to [319]
marked on their own lines, the footnotes in GFM form `[^p41-4]`, the
definition of each note at the foot of its own page) and the English
translation "…(EN)…md", which pairs it page for page (the same 313 page
marks, the same notes numbered per page). The two files agree page for page
throughout the excerpt; `build_literature.py` reported no missing pages and
no length warning.

The title page reads: EDUARD KNEIFEL / Geschichte / der /
Evangelisch=Augsburgischen / Kirche / in Polen; the imprint page "Selbstverlag
des Verfassers 2091 Niedermarschacht über Winsen/Luhe / Druck: Karl Müller ·
Druckerei und Verlag · Roth bei Nürnberg". The book runs: Vorwort (with the
author's own life, pp. 7-10), Einleitung (11), chapters I-XVI to the
Zusammenfassung, a Literaturnachweis, a Personenregister and Bildtafeln.

## What is brought in, and why

Scanned first: every page of the German file was searched for the edition's
ground (Trąbczyn, Zagórów, Łazińsk, the colonies, the neighbouring parishes
and towns). The book is a general church history; the relevant material is
scattered. The excerpt, 21 printed pages:

- **pp. 39-42**, the section "Die ländliche Kolonisation" (III.1): the rural
  colonisation of central Poland from 1550, its second rise after 1725, and
  p. 41 the passage on the Kalisch land that names the Starost and Łazińsk;
  p. 42 kept only to the section's five concluding points, before "Die
  städtische Einwanderung".
- **pp. 89-93**, the section "Die preußische Kolonisation in Mittelpolen"
  (VI.1): the Prussian colonisation of 1793-1806, its figures and colonies;
  p. 92 names the towns "Konin, Zagö-röw und Kolo"; p. 93 carries the
  section's close and the opening of VI.2 (the schools of the Kalisch land,
  among them Grodziec).
- **p. 45**, the German schools of the Kalisch land to 1795:
  Władysławów-Rosterschütz 1740, …, Orlina, Łazińsk; and the Kantorat system.
- **p. 94**, the Grodziec parish contract of 12.-14. July 1796 (the
  Holländer villages include Orlina) and the founding of Babiak.
- **p. 102**, the parishes Stawiszyn, Prazuchy, Sobiesenki, Łask and Slesin
  (its preaching-place Butter-Holl = Masłaki; the Konin congregation's
  church bought 1824, the parish of 1826).
- **p. 112**, the schools of the 1840s: "im Bezirk Zagörow sieben", Orlina
  Wielka and Łazińsk with their school lands.
- **p. 123**, the parishes of the diocese of Kalisch, "Zagörow mit dem
  Filial Lissewo-Pyzdry, Konin mit dem Filial Maslaki" (kept from the
  paragraph on the dioceses' division to the end of the Kalisch list).
- **p. 165**, the churches of the region's parishes: Władysławów 1872,
  Stawiszyn 1875/76, Grodziec 1846-1866, the filial Masłaki 1888.
- **p. 166**, the church of Zagórów: foundation stone 8 May 1878, dedicated
  1st Advent Sunday 1882, a parsonage bought 1896; the Koło church 1882/83
  (kept from the foundation stone to the Władysławow filial's church of
  1861).
- **p. 179**, the parish of Konin in the first decade of the 20th century
  and the filial Masłaki's quashed church project (Masłaki or Kleczew).
- **p. 226**, the inter-war parishes: Konin's pastor Robert Badke 1928-1939,
  Masłaki made a parish, and "Von 1923 bis 1945 war in Zagörow Pastor
  Alexander Groß tätig …" (kept to that sentence).
- **pp. 235-236**, the brethren's circles of Łazińsk: the Hahnsche
  Gemeinschaft "In Lazinsk, in der Gemeinde Zagörow" (p. 235, to the page's
  end) and the Lazinsker Brüderkreis (p. 236, to "verloren die „Brüder" an
  Boden."). The sentence runs across the page break; each page keeps its
  own half, as the print has it.
- **p. 256**, the statistics of 1938: "die rein deutsche evangelische
  Gemeinde Zagorow" (not counted in the diocese's figures), the diocese of
  Kalisch's figures corrected from the author's own book of 1937 on the
  parishes of the Kalisch diocese (its Zagórów Kirchspiel, 3,800 souls in
  1934).

Left out: everything else, above all the chapters on the Reformation, the
oppression and toleration, the general superintendents, the wars, and the
regions east and south (Lublin, Volhynia, Silesia, Łódź), whose places are
not the edition's. One false friend checked and ruled out: p. 101 names a
colony "Trombin in der Nähe von Rypin" (the Dobrzyń land) — not Trąbczyn;
p. 41's "Trombezyn" is the estate.

## The text

The German transcription is taken over as the editor's file has it, nothing
tidied: the print's slips stand ("Prazuehy" for Prazuchy, "Arheit" p. 236,
"Golonisten" p. 90, the mangled quotation marks „…"66" and the broken words
at the page breaks, "des18. / Jahrhunderts", "Zagö-röw"), as do the notes'
own slips (p. 40 n. 8, p. 90 n. 2). A page kept whole keeps its footnotes
whole; a page kept in part keeps the notes its kept text points to and drops
the rest (p. 166's note 8 and p. 236's note 68 belong to the left-out text).
The page marks of the source ([N]) are rewritten to the edition's form
([p. N]).

## The English

The English is the pairing translation the editor's file carries; it was
made by Claude when the book was taken in (the standing rule for the editor's
Books, docs/LITERATURE_PLAN.md, section 1). It is not checked whole: the
spot check is this excerpt, every page of which was read in both languages
while the cuts were laid and the boundaries found (the reading found no
unfaithfulness in the excerpt; the translation carries the source's slips
with it — "Zagör" for Zagörow on p. 226, "years-lo" broken mid-word on
p. 42). The work's page says who made the English.

## Copyright

The book is in copyright (published 1964; the author did not long survive
it). Put to the editor before anything was shown; they chose the visible
excerpt. The Licences page names no work individually and was not changed
(the precedent of Mielewczyk 2017 and Łukasiewicz 1997).

## The index

`literature_index.py --check` and `--sheet`: 140 hits in the work, every one
read. New rulings in `literature/index.yml`: `Trombezyn` (the print's
spelling of Trąbczyn, p. 41), `Zagörow` and the print's broken "Zagö-röw"
(the literature-only pattern `Zagö-?r[öo]w`, beside the edition's own o/ó
forms already ruled), `Lazinsk` under the Trąbczyńskie Stare Olędry (the
editor's ruling of 2026-10-22: Łazinsk is the colony, its German-era name),
`Prusinski` under Paweł Prusimski (the print drops the Polish ń), and
`Brzyczka` ruled out (A. Reptowski's colony near Łódź, p. 41, not the
edition's Brzyce). Old rulings read against the new hits, four sharpened:
Schrötter excepts the colony Schröttersdorf (p. 91), Posen excepts the three
imprint pages (89, 90, 94), Pyzdry excepts the filial's compound name
"Lissewo-Pyzdry" (p. 123), Holland excepts the colonies "Dembina-Holland"
and "Koneck-Holland" (p. 40), and Wielun now takes the town by exception
(pp. 102, 123, 165) against Guradze's field. Hits that stand under existing
rulings as read: Napoleon, Schroetter (p. 90, the minister), the diocese
list's towns and provinces, Grimm ruled out again (Pastor Grimm of
Stawiszyn, p. 93, is not the letters' Grimm).

## The link

One hand-made link, `kneifel1964-lazinsk` in `literature/links.yml`: p. 41
(Łazińsk founded 1746 by the lord of "Trombezyn") against the summons of
1860 (APP 53/968/0/-/783, document 1, which names "Paweł z Kolna Prusiński"
with his wife Katarzyna as the grantors of the Hollanders' privilege of
1746) and the boundary decree of 1775 (Konin Gr. 145, which attests the
rights granted in 1746). Read in both before it was written; where Kneifel
names the husband alone, the documents name the couple, and the edition
follows the documents.

## Why it is here

Kept from the work's account, which said it on the page until the voice review of 2026-10-29 (the editor: the reasoning for why a work is relevant is for the notes, not the reader):

> Only the pages that bear on the area are brought in: besides the founding of
> Łazińsk, the German schools of the Kalisch land (Władysławów-Rosterschütz
> 1740, Łazińsk, Orlina), the Grodziec parish contract of 1796, the parishes
> of the diocese of Kalisch (Zagórów with the filial Lisewo-Pyzdry, Konin with
> the filial Masłaki), the Zagórów church of 1878-1896 and its pastors to
> 1945, the brethren's circles in Łazińsk, and the statistics of 1938. A self-
> published work of a German-Lutheran standpoint; the Warsaw consistorial
> archive, its chief source, had burned in 1939.
