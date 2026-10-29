# Boniecki (1900): the Chełmski family, the branch that held Łukomia

Adam Boniecki, *Herbarz polski*, part I, vol. 2, Warsaw [1900], the article
"Chełmscy h. Ostoja" from p. 364. Added 2026-10-21 at the editor's word, as
"a source for the family tree of the Chełmski family".

## The source

The editor's saved page of M. J. Minakowski's online edition of Boniecki,
article 2.976 (https://wielcy.pl/wgm/boniecki/en/art/2/976.xml), in their
Downloads folder: "New Boniecki - Genealogy of Polish-Lithuanian Elites —
Chełmscy h. Ostoja.htm". The page is **not** kept in the repository: its
header carries the editor's login. `make_original.py` makes `original.md`
from it and says what it does.

The online edition gives Boniecki's text twice: as a pedigree, one person to
an item (2.976.1 to 2.976.274), and as the "Running text". The running text
is used. It gives the article's first page (364) and no page breaks, so the
work is cut at headings, one passage per part, and each heading is the
online edition's item numbers (c01 = 2.976.162-176, and so on). The
headings are the edition's; the text under them is Boniecki's as the online
edition gives it, its paragraph mark ¶ kept, nothing corrected. The year of
vol. 2 is the one usually given; it was not read off a title page.

## What is brought in (the editor, 2026-10-21)

"Only a very small part is [useful]: the part talking about Stanisław
Chełmski and references to Łukom/Bukowe/Łomów/Imielno (Mielna in this
document) ... events related to Stanisław Chełmski, especially with history
of estate transfers related to Trąbczyn/Łukom - we also want to include
info about Stanisław's brother, Heliodor. So don't include everything."

So: the branch that held Łukomia, from the point where Boniecki says the
pedigree breaks off (2.976.162) to Stanisław's great-grandsons (2.976.240):

- c01 (162-176): the old pedigree that makes Jerzy, of the province of
  Kalisz, the father of Krzysztof Ścibor and Andrzej Ścibor, which Boniecki
  doubts.
- c02 (177-182): Krzysztof Ścibor, owner of part of Łukomia; his widow's
  protest of 1703 that Andrzej held all of it.
- c03 (183, 196-198, 209-210): his son Adam and grandson Ignacy, only so far
  as to say who Ignacy was, and Ignacy's sale of 1766. Left out, marked
  "[…]": Adam's and Ignacy's marriages, Śladków, the Popiels' protest.
- c04 (211-220): Andrzej Ścibor, his sons Franciszek and Józef, his
  daughters, the Tribunal's judgment of 1748 on Łukomia.
- c05 (221-225): Józef's children Katarzyna, Heliodor and Stanisław; the
  boundary commission of 1755 for their estate of "Tyszakowa" in the
  district of Konin; Heliodor's offices.
- c06 (226-240): Stanisław and his line to Władysław, owner of Łukomia in
  1860, and his sons born 1863 and 1867.

Not brought in: everything before 2.976.162 (the family near Kraków from
1304), Adam's line beyond what is said above, and 2.976.241-274 (Samuel and
others of the seventeenth century, not shown to be of this branch). Item
2.976.199 is empty in the online edition (the name of Morsztynowa's husband,
in the sale of Śladków); it is in a part left out.

## Words and names

- "Mielno" ("Mielna") is the edition's Imielno (the editor). The index
  finds it only in the list "Łukomia, Łomowa, Mielna i Bukowa"
  (`literature/index.yml`, patterns).
- "brat ze stryjecznych": a cousin on the father's side. By Boniecki's own
  tree Ignacy and Stanisław were second cousins: their grandfathers
  Krzysztof and Andrzej were brothers. The English says "cousin on his
  father's side".
- "gród" is the municipal court (the edition's term); "skarbnik wschowski"
  Treasurer of Wschowa, as in the documents; "chorąży chorągwi pancernej"
  ensign of an armoured company; "oboźny" Camp Master.
- "(Sig. 27 f. 349 )Heliodor": so in the online edition, the reference and
  the next sentence run together. Kept in `original.md`; the English puts a
  full stop.
- "Tyszakowa" (genitive, Tyszaków or Tyszakowo) and "Jadamiesz" are not
  identified; neither is a place of the edition.
- The Władysław Chełmski of c06, owner of Łukomia, married 1860, is not
  Władysław Miączyński, heir of Trąbczyn after 1879.

## Against the documents (the documents first)

What the edition's documents say, and where they agree or differ:

- **Jerzy, 1644.** The land court's judgment of 1644 (APP 53/6/0/-/36) has
  Jerzy Chełmski suing the Trąmpczyński brothers over "his own wood by the
  village of Łukom". It fits the old pedigree Boniecki doubts (c01); the
  document does not say whose father he was. Claude's reading.
- **Franciszek and Józef, 1728.** The decree of 1728 (APP 53/6/0/-/40) names
  "Franciscus et Josephus Ścibor Chełmscy", heirs of Łukom and Łomowo: the
  sons of Andrzej in Boniecki (c04). Agrees.
- **Heliodor, 1775.** The boundary decree (Konin Gr.145) calls him "Canon of
  Chełmno" ("Kanonikowi Chełmińskiemu" in the editor's transcription);
  Boniecki has him parish priest of Jaksice in 1757 and canon of Poznań in
  1765 (c05). A difference: the edition follows the decree for 1775. The
  offices may be of different years.
- **Stanisław's title.** Konin Gr.117, doc. 4 (April 1778) already calls him
  "Thesaurarius Vschovensis", Treasurer of Wschowa; Boniecki gives the title
  under 1779 (c06). A difference of a year; the edition follows the
  document.
- **The four estates.** The same protest of 1778 has him heir of "Łukomia,
  Łomova, Imielno et Bukowo", the four estates Ignacy sold him in 1766 (c03).
  Agrees.
- **Before 1766.** Stanisław Ścibor Chełmski was already at law with
  Katarzyna Prusimska in 1761-1763 (APP 53/6/0/-/45). Not a difference:
  Boniecki's 1766 is the purchase of Ignacy's share.

All are in `docs/NEEDS_CONFIRMATION.md`, "Boniecki (1900)", settled by the
rule.

## Links

Four hand-made links (`literature/links.yml`, `boniecki1900-*`): Jerzy to
1644, Franciszek and Józef to 1728, Heliodor and Stanisław to 1775, the
estates and the title to 1778 and 1763.

## Why it is here

Kept from the work's account, which said it on the page until the voice review of 2026-10-29 (the editor: the reasoning for why a work is relevant is for the notes, not the reader):

> Boniecki says himself that the pedigree breaks off just before this branch.
