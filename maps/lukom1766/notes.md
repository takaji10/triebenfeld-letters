# Łukom 1766 (`lukom1766`)

The plan of the Łukom estate of 1766, AGAD 1/407/0/-/283, sheet 29
(https://www.szukajwarchiwach.gov.pl/en/jednostka/-/jednostka/17930967), the
first map brought into the edition: the pilot of `docs/MAPS_PLAN.md`, at the
editor's word (2026-10-23: "go ahead with the Łukom map, and make sure the
process is recorded so I can easily add more maps in the future. Let's only
do this one map for now"). The procedure it settled is
`docs/ADDING_A_MAP.md`.

## The image

- **Drawn with south at the top** (the editor, 2026-10-23: "it was drawn
  upside-down, with south facing up - so to show it correctly on the globe,
  it needs to be shown with the labels upside-down. The PNG has the map
  rotated to have north at the top").
- **The original is the editor's north-up PNG** (10,280 × 8,523 pixels),
  the image they georeferenced on MapWarper (75552). The JPG beside it on J:
  (8,808 × 7,052) is the archive's download as drawn, and
  "(Rotated).jpg" (8,386 × 6,748) another copy; neither matches MapWarper's
  control points. Every mark is in the PNG's pixels.
- `view_rotation: 180` in `reference/maps.yml`: the labelling page opens the
  map turned so the lettering reads upright. The editor traces each name in
  reading order, and the crop comes out upright whatever the turn.
- The whole sheet is tiled (no crop): 502 tiles, 15.8 MB, in
  triebenfeld-maps/lukom1766/, info.json id
  https://takaji10.github.io/triebenfeld-maps/lukom1766.

## The georeference

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
  1.0.0-beta.54).

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

- Whether the warp test page shows the map in the right place (not yet
  opened in a browser: the editor's eye, or a later session's).
- The map's viewer page on the site, and the crops on the place pages, wait
  for the gazetteer's place pages (GAZETTEER_PLAN, step 3).
