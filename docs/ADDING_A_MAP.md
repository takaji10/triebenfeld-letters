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
   (Łukom 1766), a sketch not to scale, a sheet of a larger map.
3. **Marks it** on the labelling page Claude opens (below): for each name,
   click the place's symbol, trace the baseline of the lettering (the line the letters stand on) in
   reading order, press the
   key for what the map shows. A name on two lines: trace the first line,
   then click the start of the second and go on (or press L before clicking
   the second line's start). **Save** gives a file
   (`labels_<map>_<date>.json`) in the Downloads folder; tell Claude its name.
   Work is kept in the browser between sittings, and a saved file can be
   loaded again to go on.
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
   annotation Allmaps warps the map by.
4. **Publish the tiles.** Commit and push triebenfeld-maps; wait for its
   Pages build; check `https://takaji10.github.io/triebenfeld-maps/<map>/
   info.json` loads and `.../warp.html?map=<map>` lays the map over
   OpenStreetMap.
5. **The labelling page.** `python pipeline/maps/label_page.py <map>`, then
   serve it: `python -m http.server 8765 --directory review/maps` and give
   the editor http://localhost:8765/<map>/. The page lists the names the
   gazetteer already records for this map ("To find").
6. **The marks.** `python pipeline/maps/import_labels.py <map>
   <saved file>`: checks the file, writes `maps/<map>/labels.yml`, cuts the
   crops of the lettering into `site/assets/maps/crops/<map>/`, and links
   each label to its place's map appearance in the gazetteer. Put what it
   reports (forms that differ, new places) to the editor.
7. **The fit again.** `python pipeline/maps/georef.py <map>`: the marks of
   places that have coordinates join the control points, and every marked
   place gets a position (`maps/<map>/positions.yml`). A point flagged as a
   misfit is a question for the editor, not a correction.
8. **Record.** `maps/<map>/notes.md` (what came in, how it is drawn, what
   was settled); set `in_project: true`; `python pipeline/gazetteer/
   gazetteer.py --missing` (the map leaves the list of maps cited);
   NEEDS_CONFIRMATION, TODO, the changelog. Commit both repositories.

The mechanical steps (2, 3, 6, 7) can be run by a Sonnet sub-agent with this
file as its brief; reading the fit and the reports stays with the main
session (WORKING_NOTES, "Working with the editor").

## Traps found on the first map

- **Backslashes.** A Windows path written into a file through this shell's
  heredoc lost a backslash and gained a control character ("\1" in
  "...29)\1_407..."). Write paths with forward slashes.
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
