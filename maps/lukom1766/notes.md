# Łukom 1766 (`lukom1766`)

The plan of the Łukom estate of 1766, AGAD 1/407/0/-/283, sheet 29
(https://www.szukajwarchiwach.gov.pl/en/jednostka/-/jednostka/17930967), the
first map brought into the edition: the pilot of `docs/MAPS_PLAN.md`, at the
editor's word (2026-10-23: "go ahead with the Łukom map, and make sure the
process is recorded so I can easily add more maps in the future. Let's only
do this one map for now"). The procedure it settled is
`docs/ADDING_A_MAP.md`.

## The image

- **The map of record changed to the archive's JPG as drawn**
  (2026-11-06, the editor's word: use `1_407_0_0_283-29_0001.jpg`, "not the
  rotated image"). Its lettering reads upright, so `view_rotation: 0` and the
  viewer's north-up button carries the turn (the editor: "the map will be
  turned upside down and rotated [for the georeferencing], but for the
  purposes of the map page itself, it will be shown with the labels right
  side up"). The tiles were re-cut on it (346 files, 14.9 MB), the stale
  `georef.json` removed, `in_project: false` until the re-marking.
- **The former record, the editor's north-up PNG (10,280 × 8,523), is a
  DIFFERENT RASTER, not a rotated copy**: no rotation, mirror, scale or
  affine carries the marks across. The probes (2026-11-06,
  `scratch/maps_bulk/lukom_*.py`): SIFT full-affine locked a lattice (5,652
  "inliers", rotation 171.2°) with zero photometric agreement — patch NCC
  0.077, the Zagórów signature; whole-image rot180 matches peaked 0.43 but
  that was the two white margins correlating (content-only 0.088);
  anisotropic rescale 0.066; centred unscaled paste 0.11; a local
  discrepancy grid matched only 5 weak patches with no consistent offset;
  the five MapWarper GCP patches swept over all of the JPG at 72 angles ×
  3 scales gave no consistent angle or position (three near 180–190° at
  scattered places, two at 0/10° — one pair on the *same* pixel at
  different angles), all NCC ≤ 0.46; and all 8 dihedral orientations of the
  JPG against the PNG sit under 0.09. The PNG-era files (labels.yml,
  positions.yml, georef.yml — the eleven marks of 2026-10-23, the MapWarper
  75552 points) are archived in `png-record/`; the register's `mapwarper`
  field is gone (those points are in the PNG's pixels). The *readings* and
  the gazetteer decisions of 2026-10-23 stand — they live in the gazetteer,
  not in the labels file — and the map is re-marked on the JPG (the
  editor's offer: "If that means I need to redo the labels, I can").
- **Drawn with south at the top** (the editor, 2026-10-23: "it was drawn
  upside-down, with south facing up - so to show it correctly on the globe,
  it needs to be shown with the labels upside-down. The PNG has the map
  rotated to have north at the top").
- **The former original, the editor's north-up PNG** (10,280 × 8,523
  pixels), was the image georeferenced on MapWarper (75552). The JPG beside
  it on J: (8,808 × 7,052) is the archive's download as drawn, and
  "(Rotated).jpg" (8,386 × 6,748) another copy; neither matched MapWarper's
  control points [2026-11-06: the JPG is now the map of record — see above].

## The georeference

[2026-11-06: this section describes the PNG era, archived in `png-record/`;
the JPG is placed from the editor's marks alone — empty `georef.yml`,
`mk-*` rows only, like zagorow1841 — once they re-mark.]

- **Five control points** from the editor's MapWarper georeference
  (`georef.yml`, read from MapWarper's API on 2026-10-23; MapWarper's own
  errors 175 to 574 pixels).
- **The affine fit** (georef.py): RMS 336 m; residuals 99 to 594 m; none
  over three times the RMS. A loose placement: the map is a manuscript estate
  plan, and five points are few. It tightens when the extant places have
  coordinates and the editor's marks join the points
  (`docs/ADDING_A_MAP.md`, step 7).
- `georef.json` in triebenfeld-maps/lukom1766/ is the Allmaps annotation;
  https://takaji10.github.io/triebenfeld-maps/warp.html?map=lukom1766 lays
  the map over OpenStreetMap (Leaflet 1.9.4, @allmaps/leaflet
  1.0.0-beta.54). **Checked by the editor** (2026-10-23): "Generally, yes,
  it lands at the right spot. This map is very crudely drawn so it's not
  perfect." Allmaps warps level-0 static tiles, so the plan's fallback
  (warped tiles of our own) is not needed.

## What the gazetteer says is on it

Nine names to find (the labelling page's list), from the entries' map
appearances, read against the entries' text on 2026-10-23 before the page
was made. The import's first pass had three wrong, put right by hand:

- **Myszakówek** is **not** on the map ("however, it does not appear on
  Łukom 1766"): its item is kept with `absent: true`, and the page and the
  import skip absent items.
- **Huta Łukomska**: the map has *Huta*; the second item, "Stara Huta",
  came from the sentence "(then known as *Stara Huta*) ... as it was
  included on Łukom 1766" and was removed.
- **Imielno**: the form *Dezerta Iemielno* (the entry: "Łukom 1766 showed
  this place as *Dezerta Iemielno*"), which the import had missed because
  the form follows the map's name.
- **Stawisko**: the map's *Brod Kaliski* is the swamp crossing west of
  Stawisko, not Stawisko itself; the item's note says so.

The others: Budy (*Budy do Huty*), Grądzeń (*Grązien*), Łomów (*Lomaw*, corrected below),
Łukom (*Lukom*), Rosciszewo (*Rosciszew*), Studzianka (*Studzienka*).

## The editor's marks (2026-10-23)

- **Ten labels** saved by the editor (`labels_lukom1766_20261023-2021.json`):
  the nine names to find and **Myszaków**, which they added (the gazetteer
  had no item for it on this map; one was added with the form *Myszaków*).
- **Two readings corrected** at the editor's word ("Łomaw ... is a
  misreading of what's on the map"; their own message has "Dezerta
  Jemielno"), read by Claude on the image: **Lomaw** (a plain L with a
  flourish, no stroke) and **Dezerta Jemielno** (the J with its
  descender). Corrected in the labels, the gazetteer's map forms, and the
  entries' text of Łomów and Imielno (the editor's file in
  `reference/gazetteer/source/` keeps what they wrote).
- **The inscription *Tres mansi Conventûs Landensis*** ("three mansi of
  the Convent of Ląd") beside Dezerta Jemielno, which the editor pointed
  out: added as label 025 (`new_place`, shows `field`), traced by Claude
  from the image in three lines reading upward, no symbol. It is the
  abbey's land of the purchase in the Ląd copy-book: three mansi of Łukom
  with the forest of Grądzyń, confirmed in 1447 and resigned in 1461 (APP
  53/1455/0/2/21, documents 3 and 2), the *Pustkowie Grądziem* of the
  Grądzeń entry ("included three farms in Łukom ... and the meadow above
  Imielno"). Recorded under **Grądzeń** as a second appearance on this map,
  linked to the two documents, at the editor's word (2026-10-23: "the
  latter decision"): land of a holding, not a settlement, so no entry of
  its own.
- **Two-line names** (Dezerta / Jemielno) were traced as a zig-zag; the page
  and the crop now take a trace's return against the reading direction as a
  line break (or the key L), the crop's direction from the first line.
- **The bands**: every label kept the default band of 60 pixels, while the
  lettering runs to 100-200 (Grązien's capitals, Dezerta): their crops cut
  the letters' tops. The page's help now says to cover the letters, `[`
  and `]` step by 20, and a finished label's band is changed by selecting
  it. Waiting on the editor's bands; then the import again. The band now
  stands on the traced baseline (the editor's word, 2026-10-23): `height`
  above it, 35% of that below for descenders.
- The fit gives every marked point a position (`positions.yml`), at the
  fit's 336 m.

- **The final marks** (`labels_lukom1766_20261023-2050.json`, 2026-10-23):
  the editor started from the corrected file, set every band to its
  letters (100 to 240 pixels) and checked the inscription; imported, all
  eleven crops whole and upright (Grązien across its wide spacing, the
  three lines of the inscription, the bent "Budy do Huty"). A second import
  reuses the gazetteer items already linked to its labels and unlinks
  labels deleted since (it added duplicates before; fixed in session).

## Still to do

- The map's viewer page on the site, and the crops on the place pages, are
  **built** (2026-10-27, `docs/MAPS_SITE_PLAN.md`): /maps/lukom1766/ and
  /de/karten/lukom1766/, the Maps page's card, the place pages' "On the
  maps", the Places index's "on Łukom 1766". `in_project` turned true.
  The place pages regenerated (their intro mentions the maps).
- The map's position (positions.yml) rides the fit's 336 m: the "today"
  links on the viewer page show it as it stands. The fit tightens when the
  extant places' coordinates join the control points (ADDING_A_MAP, step 7)
  - then the pages are built again.
- The editor's next marks, and the next map at their choice, by
  `docs/ADDING_A_MAP.md`; each new map gets its card and its page from
  `pipeline/maps/map_pages.py`.

## Re-marked on the JPG and imported (2026-11-14)

The editor's eleven marks on the archive's JPG (`labels_lukom1766_20261114-1219.json`):
ten places of the gazetteer and the inscription *Tres mansi Conventûs Landensis*.
The saved file had no `new_place` on the inscription (label lukom1766-024), so the
import was run from a copy with it filled in (the saved file in Downloads is
untouched). Mark-only fit: four marks have coordinates and joined the fit (RMS
251 m, the class of a 1766 estate plan); the other places are placed by their
labels. `in_project: true`.

**The inscription** is no place entry (the editor's word, 2026-11-14): it marks an
area of farms the Cistercian convent of Ląd held at Łukom. Its note says so and it
links the two charters it rests on, the king's confirmation of 1447 and the
privilege of 1461 (the Ląd copy-book, `app5314550221` documents 3 and 2). The editor
asked for a link to a decree of the Kodeks Dyplomatyczny Wielkopolski: the edition's
Kodeks entries (21) do not carry the three mansi, and a search of the eight volumes
on J: for Łukom and Grądzień with mansi or Ląd found no such entry (only the 1240
tithes, kdw 2, which names Łukom without mansi). Asked of the editor
(NEEDS_CONFIRMATION).
