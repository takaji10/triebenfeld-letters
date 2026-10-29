# Frost (2007): notes

Robert I. Frost, "The Nobility of Poland–Lithuania, 1569–1795", chapter 9 of
H. M. Scott (ed.), *The European Nobilities in the Seventeenth and Eighteenth
Centuries*, Volume II: Northern, Central and Eastern Europe, 2nd edition,
London: Palgrave Macmillan, 2007, pp. 266-310 (ISBN 978-1-4039-3375-1
hardback). First published by Longman in 1995; the 2nd edition of 2007 is the
one the editor sent.

## How it came in (2026-10-21)

The editor supplied the PDF
(`The_Nobility_of_Poland_Lithuania_1569_17.pdf`) and asked that the source be
added following the literature procedure: "I don't want to add the article
'The Russian Nobility in the Seventeenth and Eighteenth Centuries' in the
file - it's not relevant. Only the article by Frost."

## What the PDF holds

28 spreads of two printed pages each, a scan with no text layer:

- spreads 1-2: front matter (title pages, copyright page, contents p. v);
- spreads 3-25: the Frost chapter, pp. 266-310, with p. 311, the opening
  page of chapter 10 (Isabel de Madariaga, "The Russian Nobility in the
  Seventeenth and Eighteenth Centuries"), at the end of the chunk;
- spreads 26-28: the volume's Guides to Further Reading, pp. 410-415: the
  tail of the Hungary section (p. 410), the Poland-Lithuania section
  (pp. 411-415) and the first lines of the Russia section (p. 415).

Only the Frost chapter (pp. 266-310) was transcribed. The Russian chapter
stays out at the editor's word. The Poland-Lithuania section of the Guides
(pp. 411-415) — a guide to further reading on the chapter's whole subject —
is not part of Frost's article either; asked, the editor said no
(2026-10-21): "Don't add the guides from the PDF."

## On the site (2026-10-21)

The book is under copyright (its imprint: "No reproduction, copy or
transmission of this publication may be made without written permission";
"All remaining chapters © their respective authors 1995, 2007"), so the
work went in with `visible: false` after the Seidel precedent
(LITERATURE_PLAN.md, section 4). The same day the editor gave it a page:
"Give it a page - I'll need to decide later what gets displayed" — so
`visible: true` now, and what the page displays is a later decision of
theirs, open in `docs/NEEDS_CONFIRMATION.md`; for now the page shows the
text as the build makes it for every visible work.

## The text

Read spread by spread from page images at 200 dpi (the PDF has no text
layer; no OCR tool was at hand), doubtful spots re-read at 300 dpi crops;
not OCR.

- By paragraph; running heads and printed page numbers left out (the page
  marks give the numbers); italics not marked.
- The chapter's notes are endnotes: the marks `[^n]` stand in the body
  (pp. 266-302), their definitions follow the heading "Notes" on
  pp. 303-310, so that a note keeps the page of its definition. No
  `notes:` in work.yml: with it the page marks inside the notes would be
  dropped.
- Block quotations (the epigraph, Starowolski, Kromer, Trepka's entries,
  Moryson, Connor, Kołłątaj) as "> " lines.
- Paragraphs running over a page end are cut by the page mark, and the
  word at the break is completed on the next page's first line (as in
  Mączak 1968).
- The print's slips kept: "Žyigimantas Kestutaitis" (twice, p. 272, for
  Žygimantas); "shliahta" (p. 268, Kromer's rendering) and "shliaikhtich"
  (p. 271); "Konopczynski" (p. 292 — p. 293 prints "Koniecpolski" for the
  same man); "come and catle" in the Moryson quote (p. 280, for "corn and
  cattle"); "Polish Peoples Republic" without apostrophe (pp. 287, 303);
  "Private wars..." with a capital after a colon (p. 284); "(Liber
  Chamorum")" with a closing quote and no opening one (n. 23, p. 305);
  "litevskiego" (n. 13) and "cyrnik" (n. 10); "Pzenikanie" for
  "Przenikanie" (nn. 39-40); "at, 35–6" (n. 84) and "(2nd edn., Warsaw,
  1924,)" (n. 55), both as printed.
- Settled at 300 dpi where the first reading was doubtful: "Gabriel
  Podoski" (p. 299), "Gedymin" (p. 271), "clientes" (pp. 297, 300),
  "Dzieje Wielkopolski" (n. 94), "1 połowy" and "Materiały" (n. 82),
  "Myślenice" (p. 277).
- In the small type of the notes the stroke of ł does not always show at
  200 dpi; the doubtful ones were checked at 300 dpi (Materiały, n. 82).

## No English

The article is printed in English (`language: en`): there is no english.md,
and its page shows the one text without buttons.

## How it bears on the edition

It names neither Trąbczyn, nor the Olęders, nor Konin. Its nearest ties to
the edition: the studies of the Kalisz district (the Pośpiech land market,
nn. 42, 78, 92 — pp. 282, 295, 309); Great Poland throughout (Dworzaczek's
comparison of Little and Great Poland incomes, p. 288; the middling
nobility's share of the land, p. 295; the 775 new settlements of 1721-1793,
p. 296); and nobles of Great Poland serving in the Prussian army by the
mid-eighteenth century (p. 285). It ends with the partitions that made the
edition's estates Prussian, and the noble society it describes is the one
that had owned and ruled them.

## Literature index

The passage index is built from the visible works only (literature_index.
py), and reads this work now that it has a page. Its four new pairs were
read in the sheet and ruled on 2026-10-21: the Radziwiłł magnates and the
family name plainly plural are not Prince Antoni; "Florian" is the given
name of Hieronim Florian Radziwiłł, not Florian Gelanski; "Augustus" is
Augustus II, King of Poland and Elector of Saxony (caught by the edition's
pattern under "o**f** Augustus"), not Fürst August; and Repnin, the Russian
ambassador of p. 299, is ruled to the letters' Prince Repnin (83, 84,
1798): the same man, the editor confirms (2026-10-21: "I'm sure Repnin is
the same as the one in the project").

## Why it is here

Kept from the work's account, which said it on the page until the voice review of 2026-10-29 (the editor: the reasoning for why a work is relevant is for the notes, not the reader):

> Background to the noble society that owned and ruled the estates: it names
> neither Trąbczyn nor the Olęders, but draws its evidence heavily from Great
> Poland, among other things from the study of the Kalisz district land market
> (Pośpiech) showing the middle nobility buying out portions and holding its
> own between 1580 and 1655, and from the 775 new settlements raised in Great
> Poland between 1721 and 1793.
