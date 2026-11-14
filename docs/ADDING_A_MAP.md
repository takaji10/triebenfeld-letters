# Adding a map

The procedure for bringing one old map into the edition, worked out on the
first, the Łukom estate plan of 1766 (`lukom1766`, 2026-10-23). The design
and the reasons are in `docs/MAPS_PLAN.md`; this is the checklist. The
editor chooses which maps come in, one at a time.

Two repositories take part: this one (the register, the marks, the scripts,
the site) and **triebenfeld-maps** (`C:\Users\Tersnaus\Downloads\
triebenfeld-maps`, published at https://takaji10.github.io/triebenfeld-maps/),
which holds only the image tiles and the georeference of each map, because
this repository is too large to take them. The scripts find it beside this
one (or where the environment variable `TRIEBENFELD_MAPS` points).

## What the editor does

1. **Names the map** to Claude: the editor's short form ("Gilly 1802"), and
   the file on J: if it is not plain which. If the map is on MapWarper, the
   `.kml` beside the image names its number; say so if it is not.
2. **Says how it is drawn** if it is unusual: drawn with south at the top
   (Łukom 1766), a sketch not to scale, a sheet of a larger map. **Says
   which image is the map of record** when a unit holds more than one
   (Pełzucki 1896: the five sheets and the editor's mosaic of them; the
   mosaic was named, and it is the original in the register).
3. **Marks it** on the labelling page Claude opens (below): for each name,
   click the place's symbol, trace the baseline of the lettering (the line the letters stand on) in
   reading order, press the
   key for what the map shows. A name on two lines: trace the first line,
   then click the start of the second and go on (or press L before clicking
   the second line's start). **Save** gives a file
   (`labels_<map>_<date>.json`) in the Downloads folder; tell Claude its name.
   Work is kept in the browser between sittings, and a saved file can be
   loaded again to go on. **Where the map's texts carry the
   adjoining-lands list, the page also has the boundary walk**: mark the
   stamped letters of the list, then walk its stretches — each traced
   from its first letter to its last, or skipped (<kbd>S</kbd>; a stretch
   drawn in a sub-map is skipped, recorded as skipped with its
   description).
4. **Rules** on what Claude asks afterwards: a form typed differently from
   the gazetteer's, a new place, a control point that does not fit.

## What Claude does

`<map>` is the map's key in `reference/maps.yml` (`lukom1766`).

1. **The register.** Fill the map's entry in `reference/maps.yml`: title
   (and title_en), maker, **scale** (as printed, "1:20 000", from the scale
   bar or the editor; left out when not known, never guessed), holder,
   reference, url; `original` (the file on
   J:, **forward slashes**), `width` and `height`; `crop` (null for the
   whole map, else `[left, top, width, height]` round the gazetteer's area in
   the original's pixels); `orientation` and `view_rotation` (the turn that
   makes the lettering read upright: 180 for a south-up map shown north-up);
   `mapwarper` (the number) and `tiles`. **If the map is on MapWarper, the
   original is the file whose size equals MapWarper's** (`https://
   mapwarper.net/api/v1/maps/<n>`, its width and height): the control
   points are in that image's pixels. For Łukom 1766 that is the PNG the
   editor turned north-up, not the JPG beside it.
2. **The tiles.** `python pipeline/maps/tiles.py <map>`: cuts the original
   (or its crop) into IIIF level-0 tiles in triebenfeld-maps/<map>/. Large
   maps need libvips (installed: `pip install pyvips[binary]`).
3. **The control points.** `python pipeline/maps/mapwarper.py <map>` reads
   the editor's MapWarper points into `maps/<map>/georef.yml` (a map not on
   MapWarper skips this and is placed from the marks in step 7). Then
   `python pipeline/maps/georef.py <map>`: fits them, reports each point's
   error in metres, and writes `triebenfeld-maps/<map>/georef.json`, the
   annotation Allmaps warps the map by. **A georeference made on another
   image than the map of record** (the editor's points for Pełzucki 1896
   are in sheet 4456-4.jpg's pixels, the map of record the mosaic): the
   register names it in `mapwarper_image` and gives
   `mapwarper_fit: [scale, tx, ty]`, the mapping of that image's pixels
   into the original's; mapwarper.py applies it to every point it fetches.
   When the georeferenced image's pixel grid is stretched against the
   original's (the two trimmed PNGs of Richter 1843 against the editor's
   composite), the fit is the anisotropic `[sx, tx, sy, ty]`. Find the fit
   by patch correlation (scratch/map4456/, scratch/maps_bulk/, the method
   in maps/pelzucki1896/notes.md), and check the matcher on a self-match
   before trusting any of its scores. A second georeferenced image whose
   points the pipeline cannot fetch (Richter's Sek. III, MapWarper 83752,
   against one register entry) is appended to georef.yml by hand as
   `from: hand` rows, which the re-fetch keeps.
4. **Publish the tiles.** Commit and push triebenfeld-maps; wait for its
   Pages build; check `https://takaji10.github.io/triebenfeld-maps/<map>/
   info.json` loads and `.../warp.html?map=<map>` lays the map over
   OpenStreetMap. **A large set can carry `tile_quality: 78` in its register
   entry** (tiles.py's default is 85): the tiles feed the viewer alone, and
   the label crops are always cut from the original — the second
   repository has to stay inside GitHub Pages' 1 GB (the bulk batch of
   2026-11-06 put it at 860 MB).
5. **The labelling page.** `python pipeline/maps/label_page.py <map>`, then
   serve it: `python -m http.server 8765 --directory review/maps` and give
   the editor http://localhost:8765/<map>/. The page lists the names the
   gazetteer already records for this map ("To find"). **The to-do list of
   maps to mark** is `python pipeline/maps/label_index.py`
   (review/maps/index.html, served on port 8780 by the `map-labelling`
   configuration of .claude/launch.json): a new map gets a row in its
   `ORDER`, and a map leaves the list by itself once the register on
   origin/main has `in_project: true` for it (the editor, 2026-11-14) -
   run it after every publish that carries a map.
6. **The marks.** `python pipeline/maps/import_labels.py <map>
   <saved file>`: checks the file, writes `maps/<map>/labels.yml`, cuts the
   crops of the lettering into `site/assets/maps/crops/<map>/`, and links
   each label to its place's map appearance in the gazetteer. Put what it
   reports (forms that differ, new places) to the editor.
7. **The fit again.** `python pipeline/maps/georef.py <map>`: the marks of
   places that have coordinates join the control points, and every marked
   place gets a position (`maps/<map>/positions.yml`). A point flagged as a
   misfit is a question for the editor, not a correction. A map not on
   MapWarper has no georef.yml yet: create it empty (the header comment,
   `gcps: []`) and the marks fit alone — the mk-* rows are the only control
   points (mapadrogi1890, 2026-11-06). That needs the marked places'
   coordinates: a mark whose gazetteer place has no `surveyed` point joins
   nothing, so the plan's section-6 OSM lookups (GAZETTEER_PLAN) run first,
   every written coordinate carrying `location.check` with what the lookup
   found.
8. **Record.** `maps/<map>/notes.md` (what came in, how it is drawn, what
   was settled); set `in_project: true`; `python pipeline/gazetteer/
   gazetteer.py --missing` (the map leaves the list of maps cited);
   NEEDS_CONFIRMATION, TODO, the changelog. Commit both repositories.
9. **The mobile check.** After the map's pages are built (map_pages.py,
   then Jekyll): `python pipeline/mobile_check.py --map <map>` — the map's
   en and de pages measured at 390/360/320 px in the machine's Edge
   (needs node on PATH; puppeteer-core installs itself into the system
   temp, never the repository). Exit 1 names the elements outside every
   clipping container that push the page past the viewport: a map page
   that overflows on a phone is a build defect — fix it (the known shapes:
   `min-width: 0` on a grid/flex item, `flex-wrap: wrap` on a toolbar
   whose link text is data, a wide table inside `overflow-x: auto`),
   rebuild, re-run. The first pass found exactly this on the German
   Pełzucki 1896 page (2026-11-07); `--all` checks the whole built site
   (the genealogy section excluded) in about four minutes per width.

The mechanical steps (2, 3, 6, 7) can be run by a Sonnet sub-agent with this
file as its brief; reading the fit and the reports stays with the main
session (WORKING_NOTES, "Working with the editor").

## Traps found on the first map

- **Backslashes.** A Windows path written into a file through this shell's
  heredoc lost a backslash and gained a control character ("\1" in
  "...29)\1_407..."). Write paths with forward slashes.
- **A cropped map is labelled on the crop.** The labelling page takes the
  register's `crop`: the viewer shows the cropped image, the marks are stored
  in the original's pixels (the page converts at its edges; the saved file is
  in original pixels, as the import and the register want). The crop's
  `[left, top, width, height]` is in original pixels round the gazetteer's
  area, padded — computed for a regional sheet from the MapWarper points'
  affine (the method in scratch/maps_bulk/crop_windows.py, 2026-11-06).
- **The band must cover the letters.** The traced line is the baseline; the
  band stands on it: `height` pixels above it (the letters' height) and 35%
  of that below it for descenders, and 40% of the height beyond each end. The picture of a name is cut along the
  band; on Łukom 1766 every label kept the default 60 pixels while the
  lettering ran to 100-200, and the crops lost the letters' tops.
  Look at a few crops after the import (they are small JPEGs) before going
  on.
- **Two-line names** are traced line after line; the return to the next
  line's start is taken as a break (or the key L). A trace that zig-zags
  across one line of text would be split wrongly.
- **Writing that is not a place** (an inscription, a note on the map:
  *Tres mansi Conventûs Landensis*) is marked as a new label with its text
  as `new_place`; where it goes in the gazetteer is the editor's call.
- **After Claude changes the marks** (a corrected form, an added label),
  the page is made again from `labels.yml`, and the editor presses "Start
  from the saved file" before going on, or their browser's older copy
  comes back with the next save.
- **Importing again is safe**: the import reuses the gazetteer item already
  linked to a label and unlinks the labels deleted since. Run it on each
  new save.
- **The port and the host.** Another server may already hold 8765 (a
  stale one from an earlier session did, and answered Firefox on IPv4 with a
  reset; 8766 is `review_server.py`). Check with `Get-NetTCPConnection
  -LocalPort <port> -State Listen` and serve with `--bind 127.0.0.1` on a free
  port (8777 worked). The page keeps its work in the browser per port.
- **Pages can fail.** The tiles' first deployment failed with a GitHub 500
  and a re-run stayed queued; an empty commit to triebenfeld-maps started a
  new build. Until `.../<map>/info.json` loads, the labelling page has no
  map.
- **The saved file.** Look in Downloads for `labels_<map>_<date>.json`
  after the editor says they saved; one searched before the save finished
  found nothing.
- **The uploaded file, not the scan.** MapWarper's points are in the pixels
  of the image uploaded there; any other copy (another size, another turn)
  puts every point in the wrong place. Compare the sizes first.
- **A duplicate key in maps.yml is silent.** A second key of the same name
  shadows the first (the trap recorded for literature/index.yml, met again
  when the short `pelzucki1896` entry was not merged into the new one: the
  scripts read `original: null` and the tiles step stopped, though the file
  looked right). When a map already in the register is brought in, merge
  into the existing entry.
- **The texts on the sheet.** A map whose sheet carries texts worth showing
  (a title block, certification texts, an explication) gets them in
  `maps/<map>/texts.yml` — the transcription and its translations, read by
  map_pages.py and rendered by the map layout's "Texts on the sheet"
  section; the page's language carries its own translation, the Russian
  stands as transcribed (Pełzucki 1896, the pattern).
- **The labelling page's type from the gazetteer** (the editor's word,
  2026-10-31): choosing a place fills the label's type from the place's
  `kind`, and the last step keeps only the form — the type is shown as
  filled in, the form field focused; **Enter saves**, a type key overrides
  the gazetteer's answer. The form as written on the map is typed at this
  pause (the editor's word, when the first take saved the label at once
  and took the typing moment away: "I need to be able to still add 'Form
  as written on the map'"). The place-name form stands at the top of
  the panel. No editor action needed; the import and the saved format are
  unchanged.
