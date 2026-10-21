# Encyclopedia of Camps and Ghettos (2012): the Warthegau, the pages taken

*The United States Holocaust Memorial Museum Encyclopedia of Camps and
Ghettos, 1933-1945*, vol. II: *Ghettos in German-Occupied Eastern Europe*,
part A, ed. Martin Dean and Mel Hecker (Bloomington: Indiana University
Press, 2012), the chapter "Warthegau Region (Reichsgau Wartheland)". Added
2026-10-21 at the editor's word, for the twentieth-century part of the
edition. JSTOR: https://www.jstor.org/stable/j.ctt2050wk1.11.

## Licence

The book is licensed **CC BY-NC-ND 4.0** (its JSTOR cover page): it may be
shared, in whole or in part, for no commercial end, with the credit; it may
not be adapted. So the text is given as printed, in English only: no German
translation is made, and nothing is rewritten. The credit is the work's
`published` line (authors, book, editors, publisher, licence). The pictures
are left out: each carries its lender's credit ("COURTESY OF NARA", "OF
IPN"), and the book's licence may not cover them. Their captions are text
of the book and are given.

## The source

The editor's PDF "WARTHEGAUREGIONREICHSGAU-2012.pdf" (Downloads), 99 pages:
JSTOR's cover page, then the chapter, printed pp. 33-129. The PDF is **not**
kept in the repository: the foot of every page names the internet address
it was downloaded from and the time. `pipeline/literature/warthegau_pdf.py`
makes `original.md` from it; its docstring says everything it does.

## What is taken (the editor, 2026-10-21)

"Only pages (going by the document page count) of 3-8, 17 (Chocz), 26-28
(Grodziec), 29-30 (Kalisz), 32-33 (Konin), 68-69 (Rzgów), 89-90 (Zagórów)
are relevant for the 20th century part of the project - how much each part
is relevant remains to be seen."

The printed page is the PDF page + 31:

| PDF | Printed | What |
|---|---|---|
| 3-8 | 34-39 | the chapter's introduction (Joseph Robert White and Martin Dean), with its notes |
| 17 | 48 | the end of Bugaj, **Chocz** (Jolanta Kraemer), the start of Ciechocinek |
| 26-28 | 57-59 | the notes of Grabów, **Grodziec** (Jolanta Kraemer), the start of Izbica Kujawska |
| 29-30 | 60-61 | the end of Izbica Kujawska, **Kalisz** (Martin Dean) |
| 32-33 | 63-64 | the end of Koło, **Konin** (Jolanta Kraemer) |
| 68-69 | 99-100 | the end of Radziejów, **Rzgów** (Jolanta Kraemer), the start of Sanniki |
| 89-90 | 120-121 | the end of Włocławek, **Zagórów** (Evelyn Zegenhagen and Martin Dean), the start of Zduńska Wola |

Whole pages are taken, so the ends and beginnings of the neighbouring
entries stand with them. Each named entry lies wholly within its pages.
PDF p. 9 (printed p. 40) is blank.

## The text layer, and what was done

- **Polish letters** come from an accent font that stores each under its
  plain letter: mapped back (`ACCENT`). The print's own slip "Łódż" (once,
  in a note) stays.
- **Spaces of no width** after hyphens and dashes, in the "fi"/"fl"
  ligatures, before words and at hyphenation points inside words ("or ga
  nized", "house holds") are dropped by their position; a real space ends
  where the next letter begins.
- **Line-end hyphens**: the text layer keeps a space after a real hyphen
  (all 14: "so-called", "mid-July", "SS-Sonderkommando") and none after a
  break (291): the one kept, the other joined.
- **Web addresses**, broken by the print at dots and slashes, are joined.
- **Notes**: markers link to their entry's notes. Ciechocinek (p. 48),
  Sanniki (p. 100) and Zduńska Wola (p. 121) begin here with their notes on
  pages not taken; a marker of theirs would be plain, and none occurs.
- **Corrected at the editor's word**: "Betchatów" is Bełchatów (p. 34, the
  ghettos of Kreis Lask; `CORRECTIONS` in the script).
- Kept as the text layer has them: "Gerndarmeriekreis" (p. 61, a note
  quoting a German title), the space in "(or lack thereof )" and
  "(Kulmhof )".
- `--check` compares every letter of the pages with the PDF's own; they
  agree (two words broken over a page end are moved to the first page).

## For the edition

- The German names: Grodziec "Grossdorf", Zagórów "Hinterberg", Rzgów,
  Konin "Landkreis Konin", Kalisz "Kalisch".
- The "hamlet ghettos" of Kreis Konin (Grodziec, Rzgów, Zagórów), July 1940
  to March 1941; the murder of the Zagórów ghetto in the Kazimierz Biskupi
  Forest, autumn 1941.
- Grodziec and Rzgów were added to the edition's places at the editor's
  word (2026-10-21, `reference/places.yml`), so the index finds them here
  and in the other works. Rzgów is an estate in focus (the Kodeks entries of
  1261 and 1280 and the dispute of 1779 in Konin Gr.117 concern it) and its
  list of the literature shows on the Places page; Grodziec is not (no
  document is about it: Breyer's notebook "V. Grodziec Juli 1936" has the
  name on its cover and is about Łazińsk), so its hits stay in the index
  for questions. Chocz is not a place of the edition. Offered: links once
  the editor says which parts bear on the edition.
- No hand-made links yet: the edition's documents of the twentieth century
  are Breyer's notebooks of 1936, before the events of these pages.
