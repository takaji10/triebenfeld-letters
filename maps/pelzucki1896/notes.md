# Pełzucki 1896 — the plan of the Łazińskie Holendry peasant lands

The sixth map in the edition (docs/ADDING_A_MAP.md), named by the editor on
2026-10-31: the file `4456_full.jpg` in the Szreniawa museum's AN-4456 unit on
J:. Brought in with the labelling page's two new conveniences (below).

## What the map is

The plan of the lands that passed into the ownership of the peasants of the
village **Łazińskie Holendry** (the edition's `lazinskie-oledry`, the Olęder
settlement south of Łazy), gmina Tromczyn (Trąbczyn), Słupca uezd, Kalisz
Governorate. Drawn in 1896 by the staff land surveyor of the 2nd class
**Г. А. Пелзуцкій** (G. A. Pełzucki — the surname's reading is marked
uncertain in the transcription, NEEDS_CONFIRMATION); scale **1:4200 in
Russian measure**, from the sheet's own line «Масштабъ русской мѣры 1:4200».
The sheet the museum holds is the **certified copy**: examined and passed
(copy certified at Kalisz, 27 March 1898), issued with the official seal to
the village's peasants on **19 July 1900** under Article 1465 of the
Establishment Committee's decree.

This is the map the gazetteer cites as **Pełzucki 1896** (the appearance of
Glinianki, `reference/gazetteer/glinianki.yml`); its short form stays. The
plan appears in Mielewczyk's 2017 study of the Szreniawa museum's village
maps (`literature/mielewczyk2017`), which names Pełzucki among the surveyors
of the museum's holdings.

## The images of the unit AN-4456

- `4456-1.jpg` … `4456-5.jpg` — the five sheets of the plan (the title
  block's «на пяти листахъ» agrees). Sheet 1 carries the title block, the
  certification texts and the explication.
- `4456_full.jpg` — the five sheets assembled by the editor into one mosaic
  (the sheets are pieces of one map and overlap at their edges). **The
  mosaic is the map of record** (the editor's word, 2026-10-31), 21715 ×
  14206.
- `legend.jpg`, `legend_2.jpg`, `eksplikatsia.jpg`, `written_text.jpg` —
  detail photographs of sheet 1's title block, description of adjoining
  lands, explication and certification texts, transcribed in the unit's
  `*_transcription.md` / `*_translation_en.md` files. The transcriptions
  and their English are the editor's; the German on the map's page is
  Claude's, made against the English.
- `4456-1.psd`, `TIF/`, `JPG/` — the editor's working copies and the
  half-sheet scans; not used by the pipeline.

## The texts on the sheet (on the page in Russian, English and German)

The page shows the three texts in the original Russian with the translation
under (the English page the English, the German page the German):

- the **title block** (cartouche): the title, the surveyor, the five sheets,
  the magnetic needle's deviation of 7°30′ west of the true meridian, the
  survey of 1896; signed by the surveyor and by the Commissioner for Peasant
  Affairs of the Słupca uezd;
- the **certification texts**: the original plan examined and passed
  (Межевой Ревизоръ, Непремѣнный Членъ, За Предсѣдателя, Межевой Техникъ);
  the copy certified at Kalisz, 27 March 1898; the copy issued 19 July 1900
  under Article 1465 of the Establishment Committee's decree; the scale
  line;
- the **description of adjoining lands** (Описаніе смежныхъ земель, the
  unit's `legend_2.jpg`, transcribed in `legend_2_transcription.md`): the
  boundary walk round the plan's perimeter in 20 stretches keyed by stamped
  letters (А–У), in two sections (Участокъ № 1 and № 2) and three uezd
  groups — Słupca uezd, then Konin (Biskupice, Czarnybród), then Słupca
  again. The neighbours: the manor farm Włodzimirów and the forests,
  homestead and parcels of the Trąbczyn estate, the peasants of Osiny,
  Michalinów and Huta, the felled forests Maradz and Wypalanki, the forest
  of Łukom, Stawisko. Rows 1–15 run one letter to the next; rows 16–18 are
  П–А, Р–Р and С–С (the editor's ruling of the stamps); rows 19 and 20
  close the loop;
- the **explication** (Экспликація), the land-area table: the basic allotment
  870 desyatinas 1454 square sazhens (842+28), the additional allotment 197
  desyatinas 2218 square sazhens (192+5), the total 1068 desyatinas 1272
  square sazhens; one desyatina is 2400 square sazhens (about 1.09 ha), one
  square sazhen about 4.55 m². The figures sum correctly, which supports the
  digit readings.

Carried in `texts.yml`, rendered by the `map` layout's "Texts on the sheet"
section (docs/MAPS_SITE_PLAN.md, section 3).

## The georeferencing

The editor's MapWarper points (map **104898**, "Łazińskie Holendry ca.
1896") were made on the **single sheet `4456-4.jpg`** (7454 × 7392), not on
the mosaic: `mapwarper_image` names the sheet and `mapwarper_fit`
**[1.0025, 7033, 6910]** in `reference/maps.yml` moves the fetched points
into the mosaic's pixels (pipeline/maps/mapwarper.py). The fit was found by
patch correlation in `scratch/map4456/` — see "The mosaic fit" below. The
check that the transformation is right is the ground itself: the four
transformed points fit at **RMS 2.71 m** (residuals 1.0–3.7 m; Kozłowski
1861 fits at 5.8 m, Łukom 1766 at 336 m). Tiles published
(triebenfeld-maps/pelzucki1896, 1,624 files, 60 MB), the Allmaps warp live
at warp.html?map=pelzucki1896.

## The labelling page's new conveniences (the editor's word, 2026-10-31)

- **The type of place fills itself in**: choosing a gazetteer place for a
  label sets the label's `shows` from the place's `kind` in the gazetteer
  (a village for a village, water for a stream; the mapping is KIND2SHOWS in
  pipeline/maps/label_page.py). The last step keeps only the form: the
  type shown as filled in, the **form field focused** — type the form as
  written on the map, press **Enter**, and the label saves and moves to
  the next place (a type key overrides the gazetteer's answer). A type the
  editor chose by hand is never overwritten; kinds the gazetteer holds
  that no button covers (mounds, locale, unknown…) keep the full step with
  its buttons.
- **The place-name section moved to the top**: "+ New label" and its form
  stand above the To find list (the form's position in the panel follows the
  list).
- **The boundary walk** (the editor's idea, 2026-10-31): "Mark the
  letters" steps the stamped capitals А–У of the adjoining-lands list —
  click each stamp on the map (edit the letter in the box for a stamp the
  sequence doesn't name; <kbd>S</kbd> leaves one unmarked) — and "Walk the
  boundary" steps the twenty stretches, each traced from its first letter
  to its last, or **skipped** (<kbd>S</kbd>): the shape for the Т–У pair,
  which is drawn in the sub-map. The import takes the new kinds (`role:
  letter` / `role: boundary`; a letter cropped like a name, a stretch not
  cropped and not linked to the gazetteer); on the map page the letters
  show as chips, the stretches as a list, and the viewer draws the drawn
  stretches as dashed lines over the map. The point: the 1896 perimeter of
  the peasants' allotment as a drawable thing for the interactive map, and
  the check of the list's rows 16–18 (П–А, Р–Р, С–С) against the stamps.

## The key on the map page

The plan's own key, «Объясненіе знаковъ», is on the page as a legend like
Kozłowski 1861's (`legend.yml`, built by map_pages.py): ten blocks with the
editor's colour codes of 2026-10-31, the labels from the unit's
`map_colours_transcription.md` (rows 5 and 6b keep their [?]), the English
the folder's translation, the German Claude's. The original text is
Russian — the legend data carries `lang: ru` and `orig:` fields (the
layout falls back to Kozłowski's `pl`), the buildings block carries the
key's own building sign, and the cleared woodland's light blue streaks are
drawn. The outline colours are the fills darkened, the streak ink chosen
light blue: Claude's, to be checked by the editor like the rest.

## Open (NEEDS_CONFIRMATION carries the list)

- The surveyor's surname (Пелзуцкій / Пелзуцкимъ) and the commissioner's
  (Жемчужинъ or Жемчугинъ) are uncertain readings of the transcription; the
  register records the Polish form Pełzucki from the editor's short form.
- The date "27" of the 1898 certification is a best reading.
- The mosaic's fit (below) is approximate where a sheet's edge sits inside
  its neighbour's overlap; the marks are made on the mosaic, so the fit's
  error rides on every label's pixel.

## The mosaic fit (scratch/map4456/, not committed)

The five sheets sit in the mosaic at a common scale, matched by
zero-normalized patch correlation (the matcher proved on a self-match
first: the first three takes of the fit had the numerator's
mean-subtraction and the local sums' conjugate wrong, and every "match"
was noise — WORKING_NOTES, "Correlation matchers"). Sheets 1, 2 and 5
locked at scale 1.000 (scores 0.97–0.997), sheet 3 at 1.015 and sheet 4 at
**1.0025** (nine patches, corners within ±35 px ≈ ±14 m on the ground).
The layout is the 3×2 grid the thumb suggests — top row sheets 1, 2 (and
an empty third cell), bottom row 5, 4, 3 — with ~400–500 px overlaps at
the sheet edges. Sheet 4's `[scale, tx, ty]` = [1.0025, 7033, 6910] is
what `mapwarper_fit` carries.

## The numbers on the map against the liquidation tables (2026-11-01, Claude's read)

The editor asked whether the map's numbers (black and red, all over the
sheets) align with the Łazińsk liquidation tables (APŁ 39/98/0/-/6603). A
first session located the red ink (`scratch/map4456/red_scan.py`, dozens of
clusters over every sheet) and stopped on an unrecoverable error; this pass
finished the question with OCR. Tesseract failed on the cursive figures
(whole-tile masking drowns it in linework; isolated crops read scribbles);
EasyOCR 1.7 on CPU read them. The pass: a detection stage over all 77 tiles
(long map strokes stripped, digit-sized blobs grouped into candidate boxes,
7,343 after dedup), then recognition on each candidate's colour crop only —
`scratch/map4456/numbers_easy2.py` — giving 860 numeric tokens
(`numbers_easy2.json`/`.csv`), **836 red and 24 black**.

What the tokens show:

- **The explication reads back off the mosaic.** Four of its six sazhen
  figures — 219, 1454, 1883, 335 — stand where the table sits on sheet 1
  (x≈5,200–5,400, y≈900–1,600), confidences 0.48–1.00; 1,235 and 1,272 were
  not captured. The title block's year 1896 reads twice at conf 0.91–0.96.
  A check on known ground truth: the OCR reaches the sheet's own tables.
- **The red figures are areas in desiatinas and sazhens, written as stacked
  pairs** — desiatinas above sazhens. The stacked-pair test
  (`spatial_test2.py`) matches two stacks against the survey statement's
  row-columns exactly (doc 6, the statement each farmstead's land after the
  survey): **(4, 1684) = row 84's total** (the heirs of Shtirtsenbekera,
  4 des 1684 saz), with the farmstead's pasture desiatinas (2) read beside
  it; and (0, 219), which proved to be the explication's own 842/219, not
  row 21's unusable. Control mean for the test 0.02 (p≈0.0025).
- **Token level runs above chance but modestly.** 22 of the 69 tokens
  carrying a figure ≥ 100 hit a statement value; the permutation control
  (same tokens, digits shuffled) gives 12.4, p = 0.0025
  (`perm_test2.py`). The margin is small because one wrong digit kills a
  match and the statement's sazhen values are dense (423 distinct values in
  100–2,399).

The reading: the map's red numbers are the 1896 survey's **per-parcel**
areas in des/saz — the same survey whose figures the 1897 inscription
entered in the liquidation table (doc 5) and whose per-**farmstead** totals
the statement (doc 6) gives. A farmstead's holding is made of several
parcels, so the statement's rows do not repeat verbatim on the map; the
alignment is in the system of figures and the totals, and a full row-by-row
proof wants every parcel figure read and summed per farmstead. The common
cemetery (row 93, 2 des 282 saz) shows its desiatinas (2) read at
(9,653, 8,966), the sazhens not captured. What the black figures are stands
open here — the section "The black numbers and the farm locations" reads
them as the farmstead numbers, and the section "The numbers' grammar" after
it carries the editor's correction of that reading.
Whether some red numbers along the perimeter are the boundary stretches'
lengths stands open.

Files: `scratch/map4456/numbers_easy2.{json,csv}` (all tokens),
`numbers_hits.json` (the strict statement hits), `numbers_overlay.py` (the
tokens drawn on a downscaled mosaic, temp), `cemetery_probe.py`,
`anchor_check.py`. Not committed, like the rest of `scratch/map4456/`.

## The black numbers and the farm locations (2026-11-01, Claude's read)

The editor's follow-up: can the numbers point to where a specific Olęder's
farm stood? They can. A second OCR pass dedicated to the dark ink (the
first pass's threshold was catching the forest fill; the black ink is dark
brown, luminance 62–96 in the strokes — `black_probe.py`) over all tiles:
`dark_harvest.py`, 2,284 candidates, 688 tokens (`numbers_black.json`),
349 of them clean at conf ≥ 0.4.

**The black numbers are the farmstead numbers of the liquidation table.**
269 of the 349 clean tokens read 1–97 — the statement's numbering — and two
sites are proved by the red figures beside them:

- **Farm 11, Grunvald Kristof** (Грунвальдъ): black **11** at
  17.95456 E, 52.09687 N, conf 0.78, with red **454** 30 px away — row 11's
  unusable (0 des 454 saz), a value unique to row 11 in the whole statement.
- **Farm 78, Želchak Foma** (Цельхакъ): black **78** at 17.87796 E,
  52.10876 N, conf 0.97, with red **888** 351 px away (row 78's meadow,
  0 des 888 saz, unique) and red **936** 226 px away (row 79's arable,
  2 des 936 saz, unique) — a farm-78/79 boundary with both sides marked.
- (and farm 84, the heirs of Shtirtsenbekera, from the earlier stack: parcel
  at 17.88197 E, 52.11131 N, its total 4 des 1684 saz read in place.)

So the map's system is: **black = the farm's number (the row's number in
the tables), red = that parcel's area in des/saz**. A number recurs because
every parcel of a farm carries it — farm 11 three times, farm 50 twice. The
holder's name comes from the statement (doc 6): read the black number, look
up the row, and the Olęder is named.

Flagged for the editor's eye (candidates, no red support yet — the red OCR
is the limiting factor, ~69 usable multi-digit tokens):

- **Farm 50, Tselmer Genrikh (Цельнеръ — the Zelmer family)**: four black
  sites clustered at 17.877–17.892 E, 52.096–52.102 N (the 49/50 pair sits
  728 px apart on one latitude; rows 49 Merts Avgust and 50 Tselmer side by
  side). The statement gives Tselmer 20 des 416 saz in all.
- **Row 92, the village school**: black 92 at 17.90982 E, 52.09999 N, not
  far from the common cemetery (row 93; the gazetteer's `lazinsk-pierwszy`
  point 17.91139, 52.10333) — plausible neighbours, no red support nearby.

The full locator is `farm_locations.csv`/`.json` (183 sites: number, holder,
position, lat/lon, support), the drawing `black_overlay.py` (supported sites
green, candidates blue, temp). A full parcel-by-parcel proof — sum each
farm's red parcels against its row — wants a better read of the red
desiatinas (most sit below the OCR's confidence now).

## The tables linked into one list of the Olęders (2026-11-01, Claude's read)

The farm numbers join every table that names them;
`link_tables.py` builds the joined row set —
`oleders_linked.csv`/`.json` (97 rows: number, the 1868 name and dues, the
1869 copy's name, Breyer's 1868 Morgen/rods and his pencil note of who held
the farm in 1875, the 1894 land given for the servitudes, the 1896 name and
total, the map sites):

- **APŁ 39/98/0/-/6603-1** (the 1868 table): names 1–97, the dues.
- **APŁ 39/98/0/-/6603-2** (the 1869 copy): the same names, another hand.
- **APP 53/968/0/-/716-4** (Breyer's copy): the 1868 extents in Morgen/rods
  and, after a dash, his pencil note of the 1875 holder — 56 of 97 rows
  carry one (the cemetery's among them: "Gotfr. Khaupt 8-179"). His part-I
  numbering follows the draft column (1–90, 86 twice) and was aligned to
  doc 1's rows by order, verified against the draft column exactly.
- **APŁ 39/98/0/-/6603-4** (the 1894 inscription): nos. 1–7, 9–13, 15–46,
  48–58, 60, 62, 64, 65, 67–74, 76–91, 96 — 4 Morgen; 8, 14, 59, 61, 63,
  66, 75 — 6 Morgen; 47 — 5.
- **APŁ 39/98/0/-/6603-6** (the 1896 statement): names 1–96 and the areas
  (row 97's roads stand in the closing "Unusable land" line, 12 des 741
  saz).
- **The map**: the black-number sites of `farm_locations.json`.

What the join shows:

- **One true change of holder: no. 77, Khaupt Gotfridov Kristiian (1868)
  → Gebel Kristiian (1896)** — the change the statement's summary notes.
  The other 18 differing names are orthography (Martsin/Martin,
  Daniil/Daniel), dropped patronymics (39, 44, 75, 76), or the statement's
  own order (90). Both spellings stand in the table.
- **Five Zelmer rows**: 37 Tselmer Gotfrid (1875 Shults Frid.), 50 Tselmer
  Genrikh, 53 the heirs of Tselmera Daniila (1875 Avg. Shmigel), 65 Tselmer
  Mikhail (1875 Gotf.), 67 Tselmer Avgust.
- **The 1875 pencil notes** name who held 56 farms seventeen years after
  the tables were drawn — widow for 78, Shults Frid. for 37, Avg. Shmigel
  for 53, and so on; the column is raw Breyer, abbreviations and all.
- **46 of the 97 rows have black-number sites on the map** (149 sites after
  the information-block reads were removed; two supported by the red
  figures — farms 11 and 78).

Open: the 1896 statement's row 96 (Reikh) carries ".." cells the parse
reads as 0; the cemetery's 1868 area (2 des 282 saz) against the 1896
re-measurement (1 des 1320 saz) is the tables' own correction at work. The
CSV's `changed` column marks every differing pair; the editor rules which
are true changes and which are the transliteration's drift.

The working page that shows this list on the map:
`oleders_map.html` (built by `build_oleders_page.py` from
`oleders_linked.json` and `farm_locations.json`), served from the
repository root at localhost:8779 — the site's own viewer
(`site/assets/maps/`) over the published tiles, the 183 black-number sites
as marks (proved ones green), the linked table as the list, a row's Locate
chip taking the map to its site and a mark's click opening the row. The
liquidation holding's notes (`units/apl399806603/notes.md`) carry the
cross-reference. The page is working material, not an edition page.

## The numbers' grammar (the editor's field observations, 2026-11-01)

The editor, reading the drawn map by eye, distinguishes these kinds of
numbers — and the first kind overturns the "black = the farm's number"
reading of the previous section:

- **Black parcel labels, two lines: «n // D-S»** — the editor's examples:
  "3 // 1-662", "1 // 3-311", "2 // 1-414", "3 // 1-2088", and single-line
  "1-1294". The dash separates **desiatinas from sazhens**: 1-662 is
  1 des 662 saz. The leading small number is the parcel's number — and the
  editor's second observation settles its sense: **it never rises above
  about 8** (1, 2, 3, 4 scattered over the map, no high numbers), so it is
  a **parcel index within the farm** — farm no. 12's fields carry 1, 2, 3
  as their labels — not the farm's number in the tables.
- **The red numbers are single, low figures without a hyphen** (the
  editor's third observation, on the corrected red set — and the data
  agrees: 182 of the region's 388 red tokens read 0–9, 3×34 and 4×41 the
  commonest, only 4 doubtful tokens reach 1000–2399). The area figures
  belong to the **black** system (208 tokens ≥100 in the region, the
  proved 1684 among them), so the earlier reading of the red as stacked
  des/saz area pairs is withdrawn — the farm-84 stack stands as read, but
  it is not the red system's general form. What the red low numbers are
  stands open: candidates are the parcel indexes (the black labels'
  leads), a land-kind index, or desiatina counts; the red sheet's single
  value field plus the editor's note of what each number sits beside is
  to decide it. The pre-ink-fix refutations (red-as-farm-number by
  scatter) are void — they ran on misfiled tokens.
- **A classification bug the editor's observations exposed:** the ink of a
  token was judged by the mean redness of its box — which measures the
  background wash, so black labels on red-ochre parcels were filed as red.
  Re-classified by the ink pixels themselves (`fix_ink.py`), 423 of 860
  "red" tokens flip to black and 262 of 688 "black" to red: the corrected
  split is red 675, black 873 (in the editor's region 388 red, 722 black).
  The n // D-S labels being black, as the editor saw, now matches the data.
- **Black figures at the edges of shapes, sometimes hyphen-prefixed** —
  likely line lengths (the boundary stretches' measures) or the sazhen
  half of a label whose desiatina half sits on the line above.
- **Red numbers** — the second area system (the stacked des/saz pairs the
  OCR pass found; see the section above).
- **Angle measures in circles ("86°")** — the traverse's angles at the
  turning points; not land data, to be excluded by the ring.

The sheet's own texts give no key to the numbers (the legend covers the
colours alone, `map_colours_transcription.md`), so the grammar stands on
such field observations and on the checksums.

**How the relevant numbers are to be found (the plan, at the editor's
question "which settler owned which plot"):** the chain is parcel → farm →
statement row → holder. The parcel labels «n // D-S» are the survey's own
per-parcel record; parcels of one farm lie contiguous and their areas must
sum to the farm's row total in the statement (doc 6) — the explication's
grand total (1,068 des 1,272 saz) closes the check. So: read every
D-S label inside the region, group the labels by contiguity, sum each
group, and the groups whose sums match statement rows identify the farms;
the row gives the holder, the leading numbers anchor the group at its
homestead. The red system and the black system then cross-check each other.

The tool for the region: **`draw_region.html`** (`build_draw_region.py`) —
the full mosaic in the site's viewer; a click lays a vertex of the polyline,
Close (or Enter) closes the polygon, and every one of the 1,548 OCR'd
numbers then shows solid inside the region and faded outside it, with
counts by ink — the over-catch the editor expects becomes visible. Undo
vertex / Clear to redraw, Export downloads `region_polygon.json` (mosaic
pixels; the editor drew the region 2026-11-01, 56 vertices, saved in
`scratch/map4456/region_polygon.json`: 388 red, 722 black tokens inside).
The reading sheets built on it (`build_reading_sheets.py`, one template,
both served from localhost:8779):

- **`red_sheet.html`** — the editor's word, "start with recognising the
  red numbers": **269 cards**, each a red ink cluster in the region,
  fields upper (the desiatinas of a stacked pair) and lower (the sazhens;
  a single-line figure goes in lower alone), verdicts Save (Enter) /
  **Unsure** (Ctrl+Enter, empty allowed) / Not a number / Skip (Esc), the
  cluster box adjustable as on the spot sheet (drag inside to move, an
  edge for that edge, a corner for both, no grab marks), Hide box (H) from
  anywhere, Export → `reds_read.json`. The red system is the one that
  proved farm 84 (its stack 4/1684 = the row's total exactly), so its
  readings feed the sum test directly: contiguous red stacks summed per
  group against the statement's row totals name the farms.
- **`label_sheet.html`** — the black parcel labels, 387 cards, fields lead
  (the small n above the area, 1..12 per the editor's observation) and
  area (D-S); the same interaction (the earlier build's box was a fixed
  reference marker — pointer-events none, the H key bound to one field —
  which the editor rightly found broken; both sheets now share the
  spot-sheet interaction), Export → `labels_read.json`.

## The red system settled: red = the statement's row number (2026-11-01)

The editor read the red numbers by eye (`red_map.html`, built by
`build_red_map.py`, v12 — the map with the answered values as labels, new
labels added by dragging a rectangle in draw mode, answered labels fixed by
selecting and re-dragging; the click-to-select that six builds of
interception could not deliver was delivered by the pointer-event
interception of v11 plus a Firefox diagnosis the page's own independent
diagnostic block made possible). The catalogue:
`scratch/map4456/reds_all.json` — 437 readings (103 from the sheet, 334
added on the map), 33 boxes fixed by re-dragging, 166 marks rejected as
not-a-number, no card left unanswered.

**The answer: the red numbers are the statement's row numbers, written on
each parcel of the farm.** The evidence (`analyze_reds.py`,
`red_evidence.py`):

- **The sites of one value cluster.** 84 values appear twice or more; 61 of
  them cluster below the permutation control's 25th percentile (4,783 px —
  the control draws the same counts from the same 396 positions at
  random): P ≥ 61 of 84 at p = 0.25 is 7 × 10⁻²⁰. Red 71's two sites sit
  77 px apart, red 68's two 334 px, red 14's three within 749 px. The
  earlier refutation (red 78 scattered across the map) was an artifact of
  the misfiled OCR tokens and is withdrawn.
- **The spread matches the farms' shapes.** A farm's parcels are not a
  point: spreads of 2,000–5,000 px for values with 4–12 sites are the
  signature of a dispersed holding, and the tightest values (2–3 sites
  within 500–1,000 px) are small farms.
- **The special rows behave as themselves.** Red 92 (the school) twice
  within 381 px; red 97 (the roads) 28 times spread over the whole plan —
  roads and unusable strips run everywhere, and row 97 is exactly
  "Under roads". Red 94 (the common land) once. The cemetery (93) and
  Reikh's farm (96) were not captured; 88 and 90 also missing.

The counts per value are the first map of the farms' parcel counts: red 4
twelve times, red 3 nine times, red 23 and 47 nine times — against the
statement's rows of the same numbers. 10 values seen once, 4 never.

**What carries the ownership chain the rest of the way** is the areas: each
farm's parcels must sum to its row's total in the statement. The editor's
correction of the day: **the D-S labels they read are in red ink** — the
areas are not the black system's alone, and the ink colour is not the
system's dividing line. The 27 red D-S readings in the catalogue
(`red_ds_exact.py`, `red_ds_nearmiss.py`):

- **No statement cell matches any of them exactly** — the earlier claim of
  15 exact matches was a rounding artifact (an error of 239 sazhens printed
  as "off 0.0 des") and is retracted. The nearest row totals lie 15–240
  sazhens away: within a digit's misread for eight of them (8-2070 is 15
  sazhens from row 25's total, 5-150 is 72 from row 38's, 26-1860 is 62
  from row 47's), but none exact.
- **They sit inside clusters of one repeated red value** (11-2380 among
  four red 53s, 3-765 among three red 76s and two red 72s, 35-1590 among
  three red 14s) — the likeliest reading: **a red D-S label is the area of
  the parcel-pieces the neighbouring red-n cluster marks**, a *part* of a
  farm's holding (a detached piece), whose parts and pieces together
  should sum to the row total. The sum test cannot run yet: 27 labels
  against 96 farms is too sparse, which is why the black label sheet (the
  parcel areas, 387 cards) remains the next reading pass.
- **They divide into a west/core group (12) and an east group (15)** — and
  the east group sits where the adjoining-lands list puts the parcels that
  are *not* Łazińsk's: the Trąbczyn estate's parcel (row 17, Р–Р) and
  Michalinów's additional allotment (row 18, С–С) lie inside the plan's
  boundary and carry no row in the statement. Several D-S labels there
  (13-1350 and 3-765 at the far east edge, 87-857) may belong to those
  neighbours' lands — their areas would be red, in des/saz, and absent
  from every table here by right.

So the system, as it now stands: **red n = the parcels of statement row n**
(clustering proved; the sum test pending), red D-S = parcel-piece areas in
des/saz (some on Łazińsk's parcels, some possibly on the neighbours'
inside the plan), black n // D-S = the parcel labels' second system, the
circled degrees the traverse. The one step left to close the chain
arithmetically is the black label sheet's readings.

## The farm-13 test: the black grammar read on the ground (2026-11-01)

The editor read every figure around three red-13 sites (farm 13,
Shteinbord Iulian, statement row 13: 11 des 103 saz; buildings 0/594,
arable 5/2144, meadow 1/2104, pasture 2/2058, unusable 0/393) and the
numbers check (`farm13_check.py`). The editor's three kinds, confirmed:

- **Black «n. figure» — the plot number and its piece's area.** The lead
  decimal figure is **the plot's number within the farm** — the editor's
  own hypothesis — and one plot's number repeats on each of its scattered
  pieces (strip farming): farm 13 shows plot 1 once, plot 2 twice, plot 3
  four times, plot 4 five times. The lead never runs high because a farm
  here has only a handful of plots.
- **The areas**: D-S pairs (1-1584), sazhen-only after the plot lead
  (1926, 198), hyphen-prefixed (-684 — a piece whose plot lead is not in
  the same crop or is written apart) and bare smalls.
- **The unled smalls** (-52, 47, 20, -26, -112, 108, 18) are the farm's
  **unusable bits — the tracks and ditches**: together 383 sazhens against
  the statement's unusable 0/393 (off 10, within a digit misread).

The checks:

- **Plot 1 = 594 = the buildings column 0/594 EXACTLY** — plot 1 is the
  homestead yard, and its figure is the table's own buildings figure.
- **Plots identified**: 2 = 2/1990, 3 = 2/1360, 4 = 2/2280 (pieces as
  read; the leads do *not* correspond to the table's land-kind columns —
  tested and rejected: no kind total equals a lead's sum).
- **The identified total is 8 des 1807 saz of the row's 11/103 (79%)**;
  the missing 5,496 saz sit on parcels outside the three 700-px crops —
  an excellent fill for a partial sweep, and no contradiction.
- **Two single-digit candidates for a second look**: 2-194 (plot 3) fits
  the pasture column 2/2058 exactly if read **2-186** (4,986 + the -72 =
  5,058); and -766 (plot 3, if the arable grouping 1-1802 + 1-1584 +
  1-188 + 1926 + -684 + -766 = 14,150 against arable 14,144 is real)
  would be exact as **-760**. Both within one stroke of the reading.

The grammar of the whole map is now:

| Mark | Sense | Evidence |
|---|---|---|
| red n (1..97) | the parcels of statement row n | clustering, P = 7×10⁻²⁰; row 97 = the roads, 28× |
| black n. area | plot n of that farm, this piece's area | plot 1 = buildings exact; pieces repeat the plot's number |
| black -n / bare n (small) | the farm's tracks and ditches | 383 vs the row's unusable 393 |
| red D-S | an area of a detached piece (farm or a neighbour inside the plan) | the neighbourhood test |
| circled ° | the traverse's angles | — |

What remains to name every farm with arithmetic certainty is the same read
across the other 90-odd farms: the plots' pieces, summed per red-n group,
checked against the row totals — farm 13's pattern says the checks will
close. The re-check of the two digit candidates and the full sweep can go
into the black label sheet's pass.

## The yard test (the editor's confirmation method, 2026-11-01)

The editor proposed confirming a red-n = row-n mapping by the farm's
**buildings** figure: the yard is one parcel under the lead 1., and the
statement's buildings column records it separately. The arithmetic holds
(`buildings_discrimination.py`): 66 distinct buildings values over 96 rows,
54 rows in the 200–700 saz yard band of which 26 unique in the band; the
odds of a wrong (farm, yard) pair agreeing by chance ≈ 2%. The method,
refined: **the yard is a single piece** (farm 13's 1. = 594 = buildings
exactly; a `1.` with two pieces means one of them isn't the yard), and
**ten rows carry buildings 0** (12, 25, 45, 71, 80, 85, 93, 94, 95, 96 —
no yard figure in the statement; for those the test is vacuous).

The editor's two probes (`yard_test.py`):

- **Farm 9, "1. 144"** — row 9's buildings are **exactly 144**
  (Sanikovskii Martin). Exact to the sazhen. Confirmed outright.
- **Farm 15, "1. -288"** — the editor corrects the analysis: **-288 was a
  clean read**, and the editor flags uncertainty with brackets and a
  question mark ([29?] and the like), as the catalogue's 135 uncertain
  readings show; no misread may be assumed to make a number agree. Row
  15's buildings are 297, not 288 — and **288 is exactly the buildings
  figure of rows 38, 39 and 82** (Malinovskii Petr, Khaupt Kristiian,
  Rogatskii Stanislav). The map says which: the read stands at (5244,
  7700), and **red-82's site (5121, 7299) is 419 px away** — inside the
  same field block — while red-38's nearest site is 1,800+ px off and
  red-39's 1,100+. The likeliest reading is therefore that the yard of
  **farm 82 (Rogatskii Stanislav)** was read, its red number 82 standing
  419 px from the mark — the figure and the red number disagreeing by one
  farm. Farm 15's own yard (297) has not been read yet. The probe
  confirmed the *method* (the yard pins the farm) and showed its edge:
  when the yard figure and the red n disagree, the disagreement is data —
  either the mark belongs to a neighbouring farm's parcel or the yard is
  another farm's, and the map's geometry (419 px, not 4,000) says which
  neighbour is the candidate. Farm 15's mapping is **not** confirmed by
  this read; it awaits its own yard.

The caution from farm 87 stands: the yard check wants the farm's *smallest
single* n. figure; a `1.` with a large piece beside it (288 + 1-50 = 2,738
is no yard) means a mixed read — the sweep's protocol is to find the
smallest 1. figure first, then the full sum.

## The homestead anchors (the editor's plan, 2026-11-01)

The editor marks each farm's yard parcel on the map and links it to the
farm's red number: **`yard_map.html`** (`build_yard_map.py`, served from
localhost:8779). The page carries the red catalogue as faint dashed tags
(toggleable) so the yard's farm is visible at the mark; a yard is added by
dragging a rectangle around the black 1. figure in draw mode and typing the
farm number and the area as written (uncertainty in [..?]); labels edit and
delete as on the red map; Export → `yards_read.json`.

What the pairs decide (`buildings_discrimination.py` holds the odds): a
yard figure equal to its row's buildings column **confirms** the red n =
row n mapping (≈2% collision odds, removed by the position); a
disagreement **names the row the figure belongs to** — and the distance
from the mark to that row's red sites says whether the red n there is
misread or the yard is the neighbour's. Farm 15's probe demonstrated the
disagreement branch: -288 (clean) at (5244, 7700) names row 38/39/82, and
red-82's site 419 px away makes **82 the candidate** — farm 15's own yard
(297) still unfound. Corrections to the transcriptions move only on this
kind of evidence: an exact column match at a plausible distance, never an
assumed misread.

The editor offered to read the numbers by eye; two working pages answer
(claude's build, `scratch/map4456/`, served from the repository root at
localhost:8779):

- **`spot_sheet.html`** (`build_spot_sheet.py`, v4): 271 cards, each a
  full-resolution crop of the mosaic (250 px square, shown enlarged ×1.3)
  where the OCR read a number **in the drawn portion of the map**, with the
  machine's reading in a box — 147
  black farm numbers (conf 0.45–0.9), 89 red multi-digit areas at every
  confidence (a wrong match is worse than a missing one) and 35 dark
  figures over 97 (possible red-stack halves the dark mask caught). The
  information blocks are excluded already: the title + certification block,
  the explication and the legend + adjoining-lands list sit in zones fixed
  from the ASCII density art of sheet 1 (`ascii_sheet1.py`,
  `classify_drawn.py`; the zones validated against the known points — the
  proved farms 78, 84, 11 outside them, the explication's own figures
  inside). 302 tokens were auto-classified "not a number" that way
  (`numbers_auto.json`: 140 in the blocks, 171 below conf 0.45, 15 digit
  fragments), and near-duplicates (one figure read twice) merged. The
  overlay **box is the editor's to adjust** (v3, the editor's word after
  card 1: the box covered "195" where the sheet draws "95"): drag inside it
  to move, a corner to resize; the adjusted box is saved with the verdict
  in mosaic pixels (`box`, `box_adjusted` in the export) and sharpens the
  site's position and the calibration both; **Hide box** (<kbd>H</kbd>) shows
  the crop bare, the setting staying until toggled back; the box has no
  grab marks — the drag mode follows the pointer (v4, the editor's word:
  drag any edge to move that edge alone, a corner for both at once, the
  cursor showing which). Verdicts: Enter
  confirms, a
  typed correction saves as corrected, **Ctrl+N or the grey button =
  "not a number"** (a line fragment, a letter), Ctrl+Enter = cannot read,
  Esc skips; progress persists in the browser (localStorage, key
  `p1896-spot-v2`, kept from v2 so earlier answers carry over) and Export
  downloads `numbers_spot.json` at any point, partial work included.
- **`annotate_numbers.html`** (`build_annotate_page.py`): the free page.
  A click on the mosaic drops a pending mark, the number typed in the side
  panel (ink chosen: black farm number, red area) attaches on Enter;
  annotations persist (key `p1896-annot-v1`) and export as
  `numbers_annot.json` in mosaic pixels. The first pass's 149 farm sites
  (the drawn-portion set; the info-block reads removed) show as dashed
  circles behind a toggle; the panel lists the farms no black number was
  read for — where a reading helps most.

The two exports feed the next steps: the spot sheet's confirmed readings
calibrate the OCR (which digits it confuses, then a re-read), the free
annotations fill the unlocated farms and the red stacks' desiatina halves,
and together they make the parcel-sum proof — every farm's red parcels
summed against its statement row.

## Where it stands (2026-10-31)

Steps 1–5 of docs/ADDING_A_MAP.md done: register, tiles, control points
(fetched, transformed, fitted at RMS 2.71 m), tiles published, the
labelling page built and served at http://localhost:8778/pelzucki1896/
(a stale server holds 8765; 8778 is this session's). Waiting on the
editor's marks; then the import, the fit again with the marks, the page
(`in_project: true` then), the build and the checks.

## The homestead yards and the farm-number rulings (2026-11-02, the editor's marking sessions)

The yard page (`yard_map.html`, v7) carried three marking passes — the
yards (100 pieces, 74 farm claims), the red numbers' corrections
(119 fixes in the export's `red_fixes`, baked into the page at build),
and the uncertain-numbers queue (117 `[?]` tags walked with neighbour
context; 64 left). `yard_analysis.py` runs the yard test per farm — the
piece figures (or subset sums) against the statement's
buildings-and-gardens column — and the verdicts colour the page:
green solid (29), light-green near-fit (7), yellow weak (7), red wrong
(3 and 4). The highlights:

- **87 -> 82** (the editor's word): the 288 yard at (5329, 6913) is farm
  82's — the figure exact and red-82's site 594 px away. Farm 15's probe
  closed.
- **The southwest row** 5, 10, 25, 25, 29 -> 5, 10, 25, **29, [9?]7**:
  the second 25 was the OCR's own 29 (the earlier correction withdrawn),
  the last 29 was the catalogue's [8?]9, now [9?]7 — canonically the
  roads row 97, plausible at the corner.
- **11** stands confirmed by its unique 454 beside the black 11; its
  yard read 8640 is the garden plot (buildings+garden as one figure,
  864 unique to row 11) plus an artifact stroke.
- **No tags at all**: 88 (German Voitsekh) and 90 (Rogovich Martin);
  **only uncertain tags**: 19, 40, 48, 64, 89, 94, 96. 88's black site
  (19978, 12189) sits among 72/73/71/77 tags in the east block — the
  polygon pass will corner it.

The farm-polygon tool (`farm_polygons.html`, built by
`build_farm_polygons.py`) is the first stone of the updated vector map:
polygons per farm, the clicked tag choosing the farm, tag renumbering
with the polygons following, vertex/edge editing with Ctrl+Z, the farms
list shaded by polygon area against the row total (the areas approximate,
~0.4 m/px), the missing-rows box, export as farm_polygons.json.

**The road to close the rest**: the parcel-sum test — the black «n. D-S»
parcel labels read on the label sheet, grouped by their red clusters,
summed per group and matched against the 96 row totals — which would
also name 88, 90, 96 by elimination. The shortcut to check first: the
1896 survey's rejestr pomiarowy (the measurement register the 1881 rules
require with every measurement), in APŁ 39/98 (Urząd Gubernialny
Kaliski do Spraw Włościańskich — the liquidation tables' own fonds,
sygn. 6603 among them), per-village files with attached registers and
plans. A Grundbuch in the Galician sense never existed for the
Kingdom's villages; the register, the hipoteka entry (built on the
liquidation table), and the gmina records are the equivalents.
