# Plan: the maps

Status: **agreed 2026-10-23; the pilot (Łukom 1766) built and checked by
the editor the same day** (Allmaps warps the static tiles: no warped tiles
of our own needed); its pages on the site wait for the place pages. The
checklist for each map is `docs/ADDING_A_MAP.md`. It
works out section 6 of `docs/GAZETTEER_PLAN.md` ("The maps") into the parts
to build and the order to build them in.

The editor, 2026-10-23: "The point of doing this is to create an easy way
for you to refer to maps in the project, and therefore create a useable data
source, but also to eventually make an interactive map on the site using
OpenStreetMap or similar." And on marking a map: "some places will not be
labeled in a rectilinear way ... I'd also need to say what it is, which could
be difficult ... and then also, some places won't be found on maps, so they
won't have GPS, just vague descriptions of where they were." Rights are left
to the end of the project ("for now just assume the rights aren't an
issue").

**The editor chooses the maps** (2026-10-23: "I don't want to add all of
these maps - I will be selective with them"). No map comes into the
edition because it is cited or because it is in the folder: each is brought
in at the editor's word, one at a time. A map the gazetteer cites and the
edition does not hold stays a citation (and on the missing list, as cited,
not as wanted).

---

## 1. What there is to start from

- **Maps on the editor's drive** (`J:\...\References\Maps`, 12 GB with
  other regions), some of the 27 the gazetteer cites among them, for the
  editor to choose from:
  the Łukom estate plan of 1766 (AGAD 1/407/0/-/283, sheet 29), the
  *Supplement à la grande Carte de la Pologne* of 1770, Perthées' Kalisz
  voivodeship of 1798 and his parish sketch of 1790, Gilly's *Special Karte
  von Südpreussen* (1802-03), the boundary maps of 1800-1804 (AGAD
  1/402/0/-), Colberg (1827), Reymann (1834), the Zagórów boundary map of
  1841 (APŁ 39/98/0/-/9856), Richter's topographic map of the Kingdom
  (1843), the Trąbczyn estate plans of 1860 and 1861, the Nowy Trąbczyn
  survey of 1901 (APŁ 39/98/0/-/10091), the Messtischblätter of 1940-44,
  the Wartheland maps, Słupca 1957, the Army Map Service's Pyzdry 1962.
- **Sixteen maps there are already georeferenced** by the editor on MapWarper
  (mapwarper.net), each with a `.kml` beside the image that names its
  MapWarper number: Łukom 1766 (75552), Perthées 1798 (83433), Gilly
  (83446; South Prussia 63625), the boundary maps of 1800-1804 (71123,
  75553, 75568, 75589), Zagórów 1841 (75688), Richter 1843 (83751, 83752),
  the Trąbczyn estate 1860 (70818), Nowy Trąbczyn 1901 (75703), the
  Szreniawa map of the Łazińskie Holendry (104898), the 1940 comparison
  (70591), Schubert 1914 (83432), Słupca 1957 (64085). Each carries the
  editor's control points (a pixel on the map tied to a point on the
  ground). They are the start of the georeferencing, not to be redone.
- **The sizes**: from 4,590 × 5,319 pixels (the parish sketch, 7.5 MB) to
  42,457 × 33,200 (Gilly's sheet, 1.4 billion pixels, 361 MB). The area
  of the gazetteer is a small part of the regional maps, all of the estate
  maps.
- **The machine**: Python with PIL and numpy; no GDAL, no libvips.
- **The repository is large already**: 854 MB packed, the built site 700
  MB, nearly all of it the scans (GitHub advises a repository under 1 GB,
  and a Pages site may not pass 1 GB). The map images cannot go into it.

## 2. The architecture

```
J:\...\Maps\<folder>\<image>        the originals (never copied whole)
        │  prepare.py: crop to the area, cut into tiles
        ▼
triebenfeld-maps (a second repository, its own GitHub Pages site)
  <map>/info.json, <map>/<tiles>    IIIF level-0 static tiles, one set per map
        │
        ├── the labelling page (local, like the fold page) ──► maps/<map>/labels.yml
        ├── georef.py: control points ──────────────────────► maps/<map>/georef.yml
        │                                                      (+ a georeference annotation)
        ▼
the edition's site
  /maps/<map>/      the map in a zoomable viewer, the marks on it
  /places/<slug>/   the strip of crops of the place's name, map by map
  /map/             Leaflet over OpenStreetMap: the gazetteer's places and
                    the old maps as layers, warped in the browser
```

**The originals stay on the editor's drive**, as the archive scans do;
`reference/maps.yml` records each map's file, its size and its
description.

**The tiles live in a second repository** (`triebenfeld-maps`, published by
its own GitHub Pages at takaji10.github.io/triebenfeld-maps/), so the
edition's repository and site keep their size. Each map is cropped to the
area the gazetteer covers before it is tiled: an estate map whole, a sheet
of Gilly or Richter only round Zagórów and Trąbczyn. A cropped map is some
5 to 40 MB of tiles, so even a generous selection stays well inside the
second site's 1 GB. Free, and the same way of publishing as the edition.

**The tiles are IIIF** (the International Image Interoperability Framework,
the standard libraries and archives serve their images in), "level 0":
plain files, no image server. Every viewer reads them (OpenSeadragon,
Leaflet), and so does **Allmaps** (allmaps.org), the open-source tool that
warps a IIIF map onto OpenStreetMap in the browser from its control points.
With Allmaps the edition keeps **one** set of tiles per map and needs no
warped copy: the warp is computed as the page is viewed. Allmaps' handling
of level-0 static tiles is to be confirmed in the pilot; the fallback is
warped tiles made by our own script (numpy, from the same control points).

**Every mark is in the pixels of the original image**, never of a crop or a
tile, so that a new crop or a better scan does not move it.
`reference/maps.yml` records the original's width and height, and the build
stops if they change.

## 3. The data

```
reference/maps.yml              the register: per map its short form ("Gilly
                                1802"), title, maker, date, scale, holder and
                                reference, the file on J:, its size in pixels,
                                the crop (in original pixels), the MapWarper
                                number, kind, whether it is in the edition
maps/<map>/labels.yml           the editor's marks (section 4)
maps/<map>/georef.yml           the control points and the fit (section 5)
maps/<map>/notes.md             how it came in, what was settled
```

A **label** (one mark):

```yaml
- id: gilly1802-017
  place: gradzyn                # gazetteer slug, or null with new_place: "..."
  form: "Grondzyn"              # the lettering as the map spells it
  point: [20311, 14882]         # the place's symbol, original pixels; null if none
  trace: [[20240, 14830], [20398, 14826]]   # along the lettering
  height: 38                    # the band's height in pixels
  shows: village                # what the map shows there, or unsure
  note: null                    # the editor's words ("with a windmill")
```

The gazetteer's `maps:` list (section 2 of GAZETTEER_PLAN) is then filled
from the labels: the form, the point and the crop for each appearance.

## 4. The labelling page

Built like the fold page (`pipeline/intake/fold_page.py`): a plain HTML page
on the editor's machine, served with `python -m http.server` as the spot
sheets are, keeping its work in the browser as it goes, with a Save button
that gives a file to bring in. The viewer is OpenSeadragon (a copy in the
project, no outside dependency), reading the map's tiles.

1. **The list to find**: the labels the gazetteer already records for this
   map, with the place each belongs to ("Grondzyn – Grądzeń"). The editor
   picks one; the form is filled in. A label not on the list: type it, and
   pick the place by any of its names, or "new place".
2. **Click the place**: one click on its symbol. "No symbol" for a name
   with nothing under it (a forest, a field).
3. **Trace the lettering**: click its start, each bend, double-click its
   end. Two clicks for straight text at any slant, three to five for a curve;
   the mouse wheel with shift sets the band's height. "Skip" leaves only the
   point, and a square round it is the crop.
4. **What it is**: one key from a short list (village, Olęder settlement,
   folwark or manor, tavern, water mill, windmill, forest, field or meadow,
   water, road or crossing, church, other, **unsure**), defaulting to the
   place's kind. A note field for the rest.
5. Arrow keys move between labels; a mark can be dragged or deleted; the
   marks already made show on the map.

`python pipeline/maps/import_labels.py <map> <saved file>` takes the saved
file into `maps/<map>/labels.yml`, cuts the crops (the band straightened, as
small JPEGs, which do go into the edition's site: a few hundred of a few
kilobytes each), and fills the gazetteer's map appearances. As with the
folds, the saved file is the editor's and wins.

## 5. Georeferencing

- **Control points from MapWarper**, read from its API (tried 2026-10-23):
  `https://mapwarper.net/api/v1/maps/<n>` gives the map's title, its
  source, its bounding box and **the width and height of the image the
  editor uploaded**; `.../api/v1/maps/<n>/gcps` gives the points as JSON
  (pixel x, y; lat, lon; MapWarper's error). The page `/maps/<n>/gcps.csv`
  answers with HTML, not CSV. Łukom 1766 (75552) has five points, with
  errors of 175 to 574 pixels: enough to place the map, and the marks add
  more. Saved to `maps/<map>/georef.yml`.
- **The original is the file uploaded to MapWarper.** MapWarper's points
  are in the pixels of the uploaded image, which is not always the file a
  reader would take: for Łukom 1766 it is the PNG (10,280 × 8,523), not the
  JPG beside it (8,808 × 7,052) or the rotated copy (8,386 × 6,748). The
  file whose size equals the API's width and height is the map's original
  in `reference/maps.yml`, and the marks are made on it.
- **Control points from the marks**: once the places that exist today have
  coordinates, every point the editor clicked on a map for such a place is
  a control point too. The maps not on MapWarper are georeferenced by the
  marking alone, with no separate step.
- **The fit**: `pipeline/maps/georef.py` fits the points (a polynomial for a
  surveyed map, a thin-plate spline for a sketch), reports each point's
  error, flags the outliers (a misidentified place shows as one), and writes
  the georeference annotation that Allmaps reads.
- **Coordinates for the vanished places**: the point clicked for a place
  with no coordinates today (Rosciszewo, Lusnie Olędry, Bieganszczyzna) is
  carried through the fit, and the place gets a `from_map` location with the
  map named and the fit's error (GAZETTEER_PLAN, section 5). Where several
  maps place it, all are kept, and the one with the smallest error leads.

## 6. Coordinates for the places that exist today

The interactive map and the automatic georeferencing need them first. Claude
looks each extant place up on OpenStreetMap (as `reference/places_osm.yml`
was made in October), checks the match against the editor's description
("south of Łazy") and writes `location.lat/lon` with `precision: surveyed`.
The editor's own GPS replaces any of them later. Places described only, or
unknown, get no coordinates (GAZETTEER_PLAN, section 5).

## 7. On the site

- **/maps/**: the list of maps by date, each with its description and the
  places marked on it.
- **/maps/<map>/**: the map in OpenSeadragon, the marks drawn on it; a
  mark's link (`#gilly1802-017`) opens the map at that label. The editor's
  "(Gilly 1802)" in an entry links to it.
- **On a place's page**: the strip of crops of its name, map by map in date
  order.
- **/map/**: Leaflet over OpenStreetMap; the places by precision (a pin for
  `surveyed`, another for `from_map`, none for `described` and `unknown`,
  which are named in the popups of their neighbours and listed apart); the
  old maps as layers that can be faded in, warped by Allmaps.
- **The data**: the labels and coordinates go into the gazetteer's downloads
  (JSON, CSV, and GeoJSON in the Linked Places format; GAZETTEER_PLAN,
  section 7).
- `verify_site.py`: every label's place exists, every crop exists, every
  map page loads its tiles' info.json, every map named in an entry exists.

## 8. The steps

Who does what: the mechanical scripts (tiling, import, crops, exports) go to
a Sonnet sub-agent with a written spec; the labelling page's design, the
fits and the identifications stay with Claude in the main session; the
marking and the rulings are the editor's.

1. **Decisions** (the editor, 2026-10-23: "I agree with your
   recommendations"): the second repository for the tiles; the pilot map,
   Łukom 1766; libvips installed (pyvips 3.2.0 with libvips 8.18.7, `pip
   install pyvips[binary]`); the MapWarper points read from its API.
2. **The register of maps**: for each map the editor chooses, its entry in
   `reference/maps.yml` filled in (title, maker, holder, reference, file,
   size, MapWarper number) from the folder, the `.url` and `.kml` files and
   the image; where it is not plain which file a short form of the editor's
   means ("Kozłowski 1861": the collective plan of the Trąbczyn estate,
   AGAD 1/402/0/-/536, sheet 23, or the estate plan of 1860?), Claude asks.
   The maps not chosen keep their short entry, as the gazetteer's citations
   need.
3. **Coordinates for the extant places** (section 6).
4. **The pilot, one map end to end**, the editor's choice; proposed
   **Łukom 1766**, the estate
   plan (8,808 × 7,052 pixels, already on MapWarper, ten places of the
   gazetteer): tiles in the second repository, the labelling page, the
   editor marks it, the import and crops, the MapWarper points, the warp in
   Allmaps, its viewer page and the crops on the place pages. The pilot
   settles the page's handling and Allmaps' with static tiles before the
   rest is built on them.
5. **The maps the editor chooses**, one at a time at their word, each
   through steps 2 and 4. For the choosing, how many of the gazetteer's
   places each cited map shows: Gilly 1802 and Richter 1843 (29 each), von
   Pfau 1770 (15), Perthées 1798, Reymann 1834 and Kozłowski 1861 (13
   each), Messtischblatt 1940 (11), the rest fewer (`docs/MISSING_SOURCES.md`,
   "Maps").
6. **The interactive map** (/map/), when the pilot's warp works and the
   coordinates are in.
