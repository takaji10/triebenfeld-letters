# Werner (1904): the parish history, entry 201 Wreschen

Albert Werner, *Geschichte der evangelischen Parochien in der Provinz Posen*,
verfaßt von Albert Werner, früher Pastor in Tremessen, überarbeitet von
Johannes Steffani, Diakonus an der St. Petrikirche in Posen, herausgegeben von
dem Königlichen Consistorium der Provinz Posen (Lissa: Friedrich Ebbecke,
1904). Added 2026-10-23 at the editor's word: the pages of the WBC
digitisation are in Downloads
(`51858_Geschichte_der_evangelischen_Parochien_in_der_Prov`: scans 001,
434-436), "only entry 201 about Wreschen is relevant for the project, hence
that's what's made available here".

## The source

The digitisation of the Wielkopolska Digital Library (WBC), publication 34695,
edition 51858, https://www.wbc.poznan.pl/dlibra/publication/34695/edition/51858/content
(the editor's page). The four page images are **not** kept in the repository
(raw scans); the WBC page is recorded in `work.yml` (`scan:`). The WBC's own
metadata page gave the bibliographic facts: DC.creator "Werner Albert",
contributors "Steffani Johannes (ueberarbeitet)" and "Koeniglichen
Konsistorium der Provinz Posen (hrsg.)", publisher "Ebbeckes Friedrich, Lissa",
DC.date 1904, language "ger", rights "Biblioteka Uniwersytecka w Poznaniu".

The four images: 001 the title page, 434-436 printed pp. 422, 423 and 424
(the running numbers read at the page heads). Entry 201 fills them whole: it
begins at the head of p. 422 and ends on p. 424 with "...worauf Martin Sänger
hierher geschickt wurde.", below which the page is blank; entry 202 begins on
p. 425, which was not supplied. The entries are numbered through the book
(201 is the number of Wreschen) and grouped by "Diözese" - here "Diözese
Posen I.", the church district - of the evangelical church province of Posen.

## The text

No transcription existed: every line was read from the page images. The
reading was done by OCR of the images (the whole pages, then the pages cut
into bands, then into single lines at 3x), the passes checked against each
other, doubtful words re-read at 5x-6x zooms; the *lunaroute* document
converter was the OCR engine, **not** a local Tesseract (none is installed on
this machine). Fraktur's long s (ſ) comes through as "f" or "j" throughout
("Reftor" for Rektor, "jondern" for sondern, "jüdpreußischer" for
südpreußischer), "kt" as "ft", and proper names were read against that
knowledge; each doubtful word went to the editor on the spot sheet
(`scratch/werner1904_sheet.py`, answers in `review/werner1904/query_answers.json`).

- **The print's "="** (the Fraktur hyphen) is transcribed as a plain hyphen:
  "Pfarrer- und Kantorwohnung", "Gustav-Adolf-Verein", "Ober-Kirchenrat" (the
  print: "Pfarrer= und Kantor=", "Gustav=Adolf=Berein", "Ober=Kirchenrat").
  Line-end hyphens are joined within a paragraph, as in Karwowski (1900);
  no word is broken at a page break here.
- **"Orangeriehaus"** - the OCR reads "Drangeriehaus" (Fraktur O read as D).
  The Polish literature on the same gift confirms the building: the
  evangelical congregation of Września received Adam Poniński's palace
  orangery in 1778 (pl. Wikipedia "Zbór ewangelicko-augsburski we Wrześni";
  the zabytek.pl entry on the church: the orangery of 1 May 1778, with the
  two houses for the pastor and the cantor and the field). This is Claude's
  identification of the word, not the OCR's.
- **"Hesekiel"** - the OCR reads "Hejefiel/Hejcfiel" throughout. The General
  Superintendent of Posen from 1886 was Johannes Hesekiel (1835-1918), who
  dedicated churches in the province in these years; this is Claude's
  identification (external sources), the page says only "D. Hesekiel".
- **"Zusammenkünfte"** - one OCR pass read "Aufkommenfünfte"; the sentence
  ("religiöse Zusammenkünfte zu halten", the leave of 1758) settles it.
- **"südpreußischer Zeit"** - OCR "jüdpreußischer"; the Ŀ-forms of Fraktur.
  South Prussia held the country 1793-1806, which fits "erst zu südpreußischer
  Zeit vollständig geordnet" (the parochial relations first fully ordered then).
- **"Tischdorf"** - OCR "Tijchdorf"; ſch = sch.
- **"Rektor/Konrektor/Generalsubstitut/Pfarrverweser/Diakonus/Hilfsprediger"** -
  the Fraktur kt and ſ of the OCR passes ("Reftor", "Generaljublstitut",
  "Pfarrverweifer", "Diafonus", "Hülfprediger"). "Hilfsprediger" is written in
  the post-1901 spelling; whether the print still has the old "Hülfs-" form
  (both occur in 1904 prints) was not decided - the word's letters carry no
  fact.
- **"Konsistorium in Lissa"** - OCR "Nonfisttorium in Lüffa/Liffa". Lissa
  (Leszno), where Friedrich Ebbecke printed the book.
- **"Schwerzen"** (pastor 4 was rector there) - read twice the same; the
  village is Schwerin an der Warthe? not settled; as read.
- The paragraphing follows the print's blocks as the OCR blocks showed them:
  the sentence on the Filial Wilhelmsau continues the paragraph of the
  villages ("Szamarzewo mit 1821 Parochianen. Das dazu gehörige ..."), and
  the closing "Mit dem 1. Mai 1894" stands after item 10 as its own
  paragraph. Item 6 runs across the page break (p. 423 to 424), as printed.
- The title page (001) is brought in as the work's front. Its "Diakonus an
  der St. Petrikirche in Posen" was OCR'd "in Polen"; St. Petri is the church
  in Posen (the epigraph "2. Cor. 6, 9" and the imprint "Lissa i. P." stand
  as read).

## The spot sheet (the editor to answer)

`scratch/werner1904_sheet.py` serves the readings a name or figure rests on
and that the passes did not settle, each with its crop from the page image:
the heading's "Diözese"/"Diöcese", the Prince's title (read
"Kronschätzmeister"), "Orangeriehaus", "1. Juni" against "1. Juli" for the
Filial Wilhelmsau of 1892, the pastors Krause, Heise, Schent, the parishes
Piesske, Ciele, Gogolin, and the village list's hard names (Guttowy,
Raczanowo, Ossowo, Piary, Zafutowo, Racławki). Everything else in the entry
the passes agreed on.

## The figures

All read the same in every pass: 1758, 1760, 1 May 1778, 1779, 1817, 1822,
1883 (500 Mark), 27 September 1895, 67500 Mark, 3000/1000/1000/14000 Mark and
1158.05 Mark, 9 November 1879, 1821 parishioners, 1 June 1892, 3 June 1892,
336 Evangelicals, the pastors' years (1779, 1783, 1787, 1795, 1818, 1819,
1835, 1848, 24 December 1849, 41 years old, 1850, 1856, 1857, 1858, 1865,
1867, 1873, 1883, 1884, 1 May 1894, 1895) and the deaths (15 November 1818,
18 April 1835, 24 December 1849).

## What it bears on

The entry is the Wreschen parish's history; the edition's ground is touched
at the German Hauländer country around **Peisern (Pyzdry)** and **Zagorowo
(Zagórów)**, lost to the parish in 1817 when those places came to Russia -
Congress Poland's border ran there. The edition holds the place
`peyserschen-hauland` (its open question, one settlement or the colonies
collectively, is not touched by this entry) and the town of Zagórów. The
eighteenth-century part of the story (the leave of 1758, the privilege of
1778, the parish of 1779) is the time of the edition's Starost and of the
Olęder colonies of the Pyzdry Forest, but the entry names none of the
edition's people or settlements: no hand-made links were written.

Against the edition's own knowledge: the entry says the parish originally
served that Hauländer country; the edition's documents show German settlers
in the Peisern country (the Peyserschen Hauland is named in the letters,
corpus line 20244) and the Zagórów parishes of the region (Breyer 1935a
"Gaue", p. 129, names the church books of the evangelical congregations of
Grodziec, Stawiszyn and Zagórów). No contradiction found.

## The English

Claude's, page for page, from the German. The place names keep the print's
forms (Wreschen, Peisern, Zagorowo, Miloslaw); the Polish forms the print
itself gives in brackets stand as printed ("poln. Września oder Wrzesno").
"(f. d.)" is the print's "siehe dort" - translated "(see there)". The title
of Schramm's publication is kept in German with a translation in brackets.
The book title's "Parochien" is "parishes" throughout (the parishes of the
church province, not the Polish parafie of the civil division).

## Copyright

Printed 1904; author and reviser long dead. Out of copyright, hence
`visible: true`. Digitisation and rights at the WBC: Biblioteka Uniwersytecka
w Poznaniu.
