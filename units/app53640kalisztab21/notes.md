# APP 53/64/0/-/Kalisz Tab.21

One document on thirteen pages, with the cover before it: part of the
register of the hearth tax (podymne) collected in the Kalisz voivodeship
for the St John's instalment of 1789, a table. Added on 2026-10-13 at the
editor's request: the table read from the scans in the working session
(there was no transcription), built as a table, summarised in both
languages, given an English version and its page. **Checked by the editor
on 2026-10-14** on the spreadsheet `review/app53640kalisztab21/table_check.xlsx`
(below, "The editor's check"), and worked in the same day. **Not
published.**

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
  number on it. Page id `0009_b`. The editor confirmed it (2026-10-14).
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
- **Doubt.** After the editor's check 13 names carry "[?]" (45 before it);
  21 lines have a note in `table.csv` (85 before).
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
different instalment. The editor confirmed all twelve figures against the
scans and took the LOOK marks away (2026-10-14); they could not say why the
figures depart from the rate, and the question stays open.

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
- **The Olęder colonies and Łazy** (editor, 2026-10-14). Two Olęder
  colonies were founded on the Trąbczyn estate, first called Trąbczyńskie
  Stare and Nowe Olędry and later Łazińskie Stare and Nowe Olędry, in
  several spellings. Entry 183, "Olendry Trąbczynskie", names no old or
  new and is not matched to either place entry. Łazy (180) is a distinct
  village, not one of the colonies.
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

## The editor's check (2026-10-14)

The editor read every line of the spreadsheet against the picture beside
it and corrected 69 names; no figure changed. They cleared or changed 70
notes in the "Doubt" column, and deleted the twelve LOOK marks, the figures
being read correctly. Taken back with `holding.py --take <file> --apply`.

The changes that took a letter or a colon off the end of a name were
looked at again on the pictures. "Jerzmanowskiego" (9, 52),
"Bardzińskiego" (18, 67) and "z Młynem" (19, 142) are written in full on
the page: the first reading had them shortened in error. "Przespolewskiego"
(9, 68) runs into the ruled line, and the editor gives it in full; the
line's note says so. "Kiedrowę" (8v, 25 and 26) and "Trzebiesławę" (8,
445) end in a letter with a long tail, first taken as ę. The editor then
saw it as the sign for an ending such as -skiego (2026-10-14): it is the
same tailed sign that ends "Jaroszew:" and "Bągin:", which the register
gives as a colon. So these three, and "Siedliskę" (18, 74; there the
ending is -iem, "z Siedliskiem"), stand as "Kiedrow:", "Trzebiesław:" and
"Siedlisk:", each with a note.

The English word table needed three new forms for corrected names (nos.
94, 142 and 437 of their districts); every other line came out of it
unchanged. "Przespolewskiego" (9, 68) is now found by the index as the
Przespolewski of Oe 1 Bü 9454 and 14525. That entry is a surname with no
forename (in 14525 Jacob von Przespolewski protests over a bond of
Prusimski's); whether the owner of the part of Gutów in 1789 is the same
man is not known, and the link is by the name only.

| Leaf | No. | First reading | The editor |
|---|---|---|---|
| 1 | 10 | Folwark [Tra…ry?] | Folwark Trafary |
| 1 | 11 | Folwark Sztrząski[?] | Folwark Sztrząski |
| 1 | 12 | Folwark Lille[?] | Folwark Lille |
| 1 | 14 | Folwark Pyżyce | Folwark Pyzyce |
| 1 | 22 | Folwark Bieczewo[?] | Folwark Bieczewo |
| 1 | 25 | Wies Bozęciczki | Wies Bozęciezki |
| 1 | 27 | Folwark Mycielinek[?] | Folwark Mycielinek |
| 7 | 380 | Gutkowo[?] | Gułkowo |
| 7 | 387 | Gałęzowo Część do Duchowny[?] | Gałęzowo Część do Dziekany |
| 7 | 393 | Luberz[?] | Łuberz |
| 7 | 406 | Szabłki[?] Części OO. Franciszkan: | Srabki Części OO. Franciszkan: |
| 7 | 408 | Woytostwo Włoczewskie[?] | Woytostwo Właczewskie[?] |
| 7v | 409 | Usięcino[?] | Usięcino |
| 7v | 413 | Witerzi[?] | Witerczi[?] |
| 7v | 437 | Adamierz z Pustk: Młynem[?] | Adamierz z Pustk[owie?]: Młynem |
| 7v | 438 | Miasto Sroda | Miasto Szroda |
| 8 | 442 | Zdzienica[?] | Zdrzenica |
| 8 | 443 | Woytostwo Zdziennickie[?] | Woytostwo Zdrziennickie |
| 8 | 445 | Dzierzawa Trzebiesławsk: | Dzierzawa Trzebiesławę |
| 8 | 11 | Pawłowo wielki | Pawłow wielki |
| 8v | 21 | Strzałkow | Sztrzałkow |
| 8v | 25 | Czachory Część Anto: Kiedrz: | Czachory Część Anto: Kiedrowę |
| 8v | 26 | z Części w Gołuchowie Kiedrz: | z Części w Gołuchowie Kiedrowę |
| 8v | 34 | Krowica wielka y Pustki[?] | Krowica wielka y Pinki[?] |
| 8v | 36 | Tursko[?] | Junikow[?] |
| 8v | 38 | Fałęcice[?] | Fałęcice |
| 8v | 40 | Miasteczko Chorab[?]. | Miasteczko Chorab. |
| 9 | 50 | Gorzuchy z Części Sieroszews: | Gorzuchy z Części Sieroszew: |
| 9 | 52 | z Części Mi: Jerzmanowskieg: | z Części Mi: Jerzmanowskiego |
| 9 | 65 | z Części Brzeskiego[?] | z Części Przciekiego[?] |
| 9 | 67 | Gazewo[?] | Gazewo |
| 9 | 68 | Gutow Część Przespolews: | Gutow Część Przespolewskiego |
| 9 | 70 | z Części Kożuchow[?] | z Części Kosiekich |
| 9 | 71 | Gać Moskowia[?] | Gać Moskomia |
| 9v | 76 | Zamęzcie[?] | Zamoscie[?] |
| 9v | 80 | Janiszow[?] | Jaruntow |
| 9v | 89 | Pokrzykow[?] | Poklękow[?] |
| 9v | 93 | Miasteczko Jwanowice | Miasteczko Iwanowice |
| 9v | 94 | Tamże poddanych Pleb: | Tamże poddanych Pleban: |
| 9v | 100 | Część Niniewa[?] | Część Niniowa |
| 18 | 65 | Jaroszewice Małe z Częś: Krzyz: | Jaroszewice Mokre z Częś: hurczew: |
| 18 | 67 | z Części JP. Bardzińskieg: | z Części JP. Bardzińskiego |
| 18 | 74 | Kuznica z Dąmbrową y Kieliską[?] | Kuznica z Dąmbrową y Siedliskę |
| 18 | 75 | Sączky[?] | Sacały[?] |
| 18 | 79 | Kęszewy z Ciołkiem y Dzią[?] | Kęszewy z Ciołkiem y Dryią |
| 18v | 96 | z Części Krzeczkowskiego[?] | z Części Krzeczkowskiego |
| 19 | 128 | Police wsrzednie[?] | Police wesrednie[?] |
| 19 | 131 | Pętowo[?] | Perłowo |
| 19 | 138 | Modłabiena[?] | Modłabiena |
| 19 | 141 | Zaskoze[?] | Zastroze |
| 19 | 142 | Pustkowie Grądy z Młyne: | Pustkowie Grądy z Młynem |
| 19v | 145 | Młyn Kuczimia[?] | Młyn Rudzimia |
| 19v | 148 | Bikorzew[?] | Piskoszew |
| 19v | 153 | Rozięcice[?] z Częś: Bernar: Bąg: | Racięcice[?] z Częś: Bernar: Bągin: |
| 19v | 154 | z Części Tomasza Bąg: | z Części Tomasza Bągin: |
| 19v | 157 | Łuczywno z Częś: Ber: Bąg: | Łuczywno z Częś: Ber: Bągin: |
| 19v | 158 | Łuczywno z Częś: J: Bąg: | Łuczywno z Częś: J: Bągin: |
| 19v | 161 | Smolniki z Częś: Toma: Bąg: | Smolniki z Częś: Toma: Bągin: |
| 19v | 164 | Pycewo[?] | Sycewo |
| 19v | 168 | Szetlewo z Częś: Jaroszews: | Szetlewo z Częś: Jaroszew: |
| 19v | 169 | z Części Jana Jaroszews: | z Części Jana Jaroszew: |
| 19v | 173 | Szawłowice[?] | Szawłowice |
| 20 | 191 | Trzebuchow Kamienne | Trzebuchowo Kamienne |
| 20 | 200 | Tamże Poddani Pleba: | Tamże Poddani Pleban: |
| 20v | 209 | Wilany[?] | Wilany |
| 20v | 218 | Kotunia | Kotonia |
| 20v | 223 | Wola Rozostowa[?] | Wola Rozostawa |
| 20v | 225 | Kliwany[?] | Klwany |
| 20v | 230 | Wardęzyn major z Częś: Węs: | Wardęzyn major z Częś: Węgie: |

## What the site needed

`unitlib.table_of` took every row before the first entry as part of the
table's heading. A district's name directly above the first entry is now a
row of the table (a row with only its name cell filled). The other two
tables come out as before.

## Still to do

1. Done 2026-10-14: the editor's check worked in, the English, the page
   files and `process.md` brought into line, the clean workbook made
   (`APP_53_64_0_Kalisz_Tab_21_register.xlsx` in this folder). No entry the
   summary or `claim_check.yml` cites was changed, so neither was touched.
2. **Publishing**, at the editor's word.
3. Not done: modern names for the places; anything in the account of the
   Prusimski years, which waits for the editor's transcriptions.
