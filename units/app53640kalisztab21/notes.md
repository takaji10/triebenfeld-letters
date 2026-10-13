# APP 53/64/0/-/Kalisz Tab.21

One document on thirteen pages, with the cover before it: part of the
register of the hearth tax (podymne) collected in the Kalisz voivodeship
for the St John's instalment of 1789, a table. Added on 2026-10-13 at the
editor's request: the table read from the scans in the working session
(there was no transcription), built as a table, summarised in both
languages, given an English version and its page. **Built and committed;
not published, and not yet checked by the editor**: their check is on the
spreadsheet `review/app53640kalisztab21/table_check.xlsx`.

Everything about how the holding was made is in the docstring of
`intake/holding.py`. The reading itself is `intake/table.csv`. The model is
AGAD 1/169/0/1/1745.

## Provenance

Archiwum Państwowe w Poznaniu, fonds 64 (Zbiór tabel podatkowych i
lustracji), unit Kalisz Tab.21, "Podymne z woj. kaliskiego [protocollon]".
The editor gave the reference, the title and the archive's description of
the fonds (`reference/sources/app_zbior_tabel_podatkowych_i_lustracji.md`).
The year 1789 is in the printed title and on the cover.

- **Images.** Fourteen single pages: `000.jpg` the cover; `001.jpg`;
  `007.jpg` to `009.jpg` with their versos; `017v.jpg`; `018.jpg` to
  `020v.jpg`.
- **`017v.jpg` is leaf 9 verso.** Leaf 9 recto ends with entry 75 of the
  Kalisz district and this page has 76 to 107, all places of that district;
  leaf 18 recto begins at entry 58 of another district. A verso has no leaf
  number on it. Page id `0009_b`. **The editor should confirm** against
  their own notes of what they photographed.
- **Pages.** `0000_a` the cover (front matter); `0001_a`; `0007_a`,
  `0007_b`; `0008_a`, `0008_b`; `0009_a`, `0009_b`; `0018_a`, `0018_b`;
  `0019_a`, `0019_b`; `0020_a`, `0020_b` (recto `_a`, verso `_b`). No folds.
- **The cover** has a label in a display hand: "Podymne z Wojewodz: Kalisk:
  Raty Sto Jańsk: 1789. Lib: 24. Hub[?]: 22.", the archive's label "TAB.
  KALISZ 21" and its sticker. "Hub" may be "Kub"; what it stands for is not
  known here.

## The register

A printed form on every page; leaf 1 has the title above it. Columns:
"Kwity. Nro." (printed sideways: the number of the receipt); "Nazwiska
Miast i Wsiow."; "Summa wybrana." and "Summa Delaty.", each in "Złote." and
"Gr:". 387 entries and two district headings:

| Leaves | District | Entries |
|---|---|---|
| 1 | Powiat Pyzdrski | 1 to 29 |
| 7, 7v, 8 | (Pyzdry, continued) | 379 to 448 |
| 8, 8v, 9, 9v | Powiat Kaliski | 1 to 107 |
| 18 to 20v | no heading on these pages: Konin, from the places | 58 to 238 |

The order inside a district is roughly by parish or by estate, not by
alphabet. A village in several hands has a line for each part ("z Części
..."). "Tamże" lines (the parish priest's subjects, the wójt's holding)
belong to the place above.

## How it is written down

- **Empty cells are empty.** The clerk wrote a sum under one heading and
  left the other blank; there are no dashes. The stop after a figure is
  left out.
- **Shortened words keep his colon** ("Pleban:", "Częś:", "Kiedrz:"). Where
  the end of a word runs into the ruled line of the column the note says
  so.
- **Diacritics** only where a mark is on the page.
- **Doubt.** 45 names carry "[?]" or stand as "[Tra…ry?]"; 85 lines have a
  note in `table.csv`. They are in the spreadsheet beside each line.
- **The title** is the caption of the table (the first heading row, over
  the name column); the district headings are rows without a number.

## The check of the figures

No totals, so no sums. The rate is the witness instead: a village's sum is
a multiple of 3 zł 15 gr in the Pyzdry and Kalisz districts and of 2 zł 15
gr on leaves 18 to 20 (`holding.py --look`). Twelve lines are off it: ten
towns (Bnin, Borek, Pyzdry, Środa, "Chorab[?].", Dobrzyca, Iwanowice,
Rychwał, Tuliszków, Władysławów), and two looked at again on the scan and
left as read: the village Dobrzyca (8v, no. 41, 133 zł 15 gr) and the
parish priest's subjects at Iwanowice (9v, no. 94, 24 zł). Why the two
districts' rates differ the register does not say: a thought, not in the
text, is that leaves 18 to 20 are a different class of hearth or a
different instalment; the editor may know.

Two figures were rubbed out by the clerk and entered in the other pair of
columns: nos. 135 (Podbiele) and 147 (Jaroszewice) of the third district.

## Worth knowing from the reading

- **Trąbczyn's group** (leaf 20): 178 Trąpczyn, 80; 179 "Tamże Poddani
  Pleban:", 20; 180 Łazy, 12.15; 181 Osiny, 17.15; 182 Nowa Wies, 12.15;
  183 "Olendry Trąbczynskie", 35. Before it, 176 Folwark Kowalewek and 177
  Folwark Ostrow, 2.15 each; after it, 184 Młyn Drążki, 5. At 2 zł 15 gr a
  hearth that is 32 hearths at Trąbczyn and 14 for its Olęders: a
  calculation, not in the text. The Prussian table of about 1797 has 32
  houses at Trąbczyn.
- **Łukom** (leaf 18v, no. 106): 97.15 as a delata; Lumow and Myszakow, 40
  each, also delata; "Olędry Lusnie" (109), 35, collected.
- **Szetlewo** in four parts (168 to 171: Jaroszewski, Jan Jaroszewski,
  Folwarski, "JP. Zakrzewskiey"), and Szetlewek (172), 55.
- The same names stand in the Prussian table of about 1797 (AGAD
  1/169/0/1/1745): Police wsrzednie, Lekaszyn, Leyszcze, Myszakow and
  others. Two readings there and here support each other ("wsrzednie",
  "Siąszyce").
- **Places the index finds:** Trąbczyn, Łukom, Szetlewek (which also takes
  Szetlewo), Osiny, Pyzdry. Shut out of this document
  (`reference/places.yml`, `people.yml`): Kamionna ("Trzebuchow Kamienne"),
  Amt Sokolnik (the village Sokolniki), Lille ("Folwark Lille[?]"), the
  town Ostrów ("Ostrow"), and the person Broniewski ("Broniszewice"). Nowa
  Wieś and Łazy of the Trąbczyn estate are not matched by the index here
  (their patterns are narrow); the English has "Nowawies" for entry 182.

## What the site needed

`unitlib.table_of` took every row before the first entry as part of the
table's heading. A district's name directly above the first entry is now a
row of the table (a row with only its name cell filled). The other two
tables come out as before.

## Still to do

1. **The editor's check** of the spreadsheet. Their corrections come back
   with `holding.py --take <file> --apply`, then `--write --english
   --cache`, `publish_translations.py`, the summary, `about.md` and
   `intake/claim_check.yml` if a figure or name they cite changed (entries
   106, 109, 143, 172, 178 to 183, 185, 192), the count of names in doubt in
   `process.md` and `process_de.md`, a rebuild, and `--archive` for the
   clean workbook.
2. **The editor's word on `017v.jpg`** (above).
3. **Publishing**, at the editor's word.
4. Not done: modern names for the places; anything in the account of the
   Prusimski years, which waits for the editor's transcriptions.
