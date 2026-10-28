# Plan: the maps on the site

Status: **planned 2026-10-27, on the branch `maps-site` from `main`**, at the
editor's request ("A link to a page of maps is missing from the main
navigation"; "upon clicking the card you can see a map viewer along with any
relevant details of the map"; "create links between place names in the place
names list and place names identified on a map"). It works `docs/MAPS_PLAN.md`
section 7 ("On the site") into the parts to build and the order to build them;
the design and the reasons stay there, and the procedure for bringing one map
in stays in `docs/ADDING_A_MAP.md`.

---

## 1. What there is to start from

- **The register** (`reference/maps.yml`): every map the gazetteer cites,
  keyed by slug, each with `cited_as` (the editor's short form, "Łukom 1766"),
  its year and kind; `in_project: false` until the map is brought in. One map
  is in: **Łukom 1766** (`lukom1766`), the pilot, its full entry written, its
  tiles published in the second repository (triebenfeld-maps,
  takaji10.github.io/triebenfeld-maps/lukom1766/info.json), its Allmaps warp
  checked by the editor. Its `in_project` still reads false — the register's
  own comment says it turns true "once its tiles are published and its page
  built", and the page is this work.
- **The pilot's marks** (`maps/lukom1766/`): `labels.yml` — eleven labels,
  ten of them a place of the gazetteer and one the inscription *Tres mansi
  Conventûs Landensis*; `positions.yml` — the ground position (lat/lon) of
  every marked point, from the fit; `georef.yml`, `notes.md`.
- **The crops**: the picture of each name's lettering, cut by the import into
  `site/assets/maps/crops/lukom1766/` (eleven small JPEGs, already in the
  edition's site).
- **The gazetteer** (`reference/gazetteer/`, 121 entries): each entry's
  `maps:` list is the appearances of the place on the maps — the form as the
  map spells it, a note, and for the marked appearances the label's id and
  sometimes `refs` to the edition's documents (the inscription's two
  documents of the Ląd copy-book, for one). An appearance can be
  `absent: true` (Myszakówek, judged not to be on Łukom 1766): those are
  records of a check, not appearances, and nothing on the site links them.
- **OpenSeadragon is already in the project** (`pipeline/maps/vendor/`, for
  the labelling page): the viewer takes its copy from there, no outside
  dependency.
- **Nothing of the maps is on the site yet**: no nav entry, no `u_maps` in
  `site/_includes/urls.html`, no map checks in `pipeline/verify_site.py`.
- **The workflow builds Jekyll only** (`.github/workflows/pages.yml`): the
  Python build steps are not run there, so every generated file the site
  reads is committed — `site/_data/*.yml` and the generated pages are, and
  the maps' will be too. `pipeline/verify_site.py` makes no external requests, so its
  checks read the repository, not the tiles' host.

## 2. The pages

Two new pages, both languages, built the way the newspapers and the places
were built (a collection per language, one layout, the texts from
`site/_data/`):

- **`/maps/`** (`/de/karten/`): **the list of maps by date, one card per map
  that is in the edition** (`in_project: true`). The card carries the short
  form as its title ("Łukom 1766"), the maker and the kind, the count of the
  places marked on it ("ten places of the gazetteer marked"), and links the
  map's viewer page. A map the gazetteer cites and the edition does not hold
  gets **no card** — the editor chooses which maps come in, one at a time
  (MAPS_PLAN, "The editor chooses the maps"); until one is brought in it
  stays a citation on the place pages and a line of `docs/MISSING_SOURCES.md`.
  With only the pilot in, the page opens with one card; every map added here
  after (`docs/ADDING_A_MAP.md`) gets its card from the build without further
  work.
- **`/maps/<map>/`** (`/de/karten/<map>/`): the map's page, the viewer with
  the details (section 3).

The nav: **`Maps` after `Places`** in the header of `default.html` (places
and maps are neighbours of one subject), German **Karten** — `nav.maps` in
both blocks of `site/_data/i18n.yml`, and `u_maps` in `urls.html`, as every
section's URL is.

## 3. The map's page: the viewer and the details

Layout `map.html` (like `place.html`: one layout, both languages, the texts
from the data). **Two columns** (the editor, 2026-10-27: "make the map
viewer much larger. Maybe a two column view where a narrow left column
contains the details, and the right column is the map"): the details in the
narrow left column, the map large in the right column — near the full
height of the window, and kept in place while the left column scrolls
(sticky; on a narrow screen the map comes first and the columns stack).
On it:

- **The viewer**: OpenSeadragon over the map's IIIF level-0 tiles
  (`tiles:` in the register), full width. The page's script:
  - turns the map by the register's `view_rotation` (Łukom 1766 by 180°, so
    the lettering reads upright and the map stands as its maker drew it,
    south at top), with a control to show it north-up as scanned;
  - draws every label as a mark at its point (the points are in the pixels
    of the original, MAPS_PLAN section 2; the build writes them adjusted for
    the map's `crop`, which for Łukom 1766 is none), so the marks survive a
    new crop or a better scan;
  - a mark and a row of the list point at each other: **hovering a mark
    names the place** (a floating label — the form as the map spells it,
    with the place's name where they differ), and **clicking a mark takes
    the reader to its row in the list** (the editor, 2026-10-27); a row's
    crop takes the map to the mark; the address
    `/maps/lukom1766/#lukom1766-007` opens the viewer at that mark
    (MAPS_PLAN, section 7);
  - a mark is a link to the place's page.
- **The details**, in the left column:
  - **The map itself**: title (Polish and English), maker, year, kind, scale
    if the register has it, holder and reference ("AGAD 1/407/0/-/283, sheet
    29"), and the link to the holding (`url:`) — the citation of the map,
    which a reader needs before anything else.
  - **The places marked on it**: one row per label, in reading order of the
    map — the crop of the lettering (the small JPEG), the form as the map
    spells it (*Grądzeń* → *Grądzien*), what the map shows there (`shows:`
    village, folwark, inscription...), the editor's note where one stands,
    and the place's name linked to its place page. A label that is an
    inscription (`new_place`, no place of the gazetteer) is shown as one,
    with the documents its appearance belongs to — the gazetteer item's
    `refs`, which for the *Tres mansi* inscription are the two documents of
    the Ląd copy-book.
  - **Over OpenStreetMap**: a link to
    takaji10.github.io/triebenfeld-maps/warp.html?map=<map> — the Allmaps
    warp the editor has checked — until the interactive map `/map/` is built
    (MAPS_PLAN, section 8, step 6; not this work).
- Each label whose place has a position (`positions.yml`) shows it — a
  "today" link per row, to OpenStreetMap's marker — where the fit is good
  enough to name it; the fit's RMS stands with the list, so a reader knows
  how much to trust it (Łukom 1766: 336 m, a loose fit of five points).

## 4. The place-side links (the new links the editor asked for)

The gazetteer already records, per place, which maps show it and in what
form. What is missing is the link on the site, in both directions. The
directions:

- **A place page shows its maps** (`pipeline/places/place_pages.py`, the
  generated body): a section **"On the maps"** under the dated forms, the
  appearances in date order of the maps — for a map in the edition, the crop
  of the place's lettering, the form as the map spells it, and the link to
  the map's viewer opened at the mark (`/maps/lukom1766/#lukom1766-007`);
  for a map the edition does not hold, the form and the map's short form as
  a plain citation, as the gazetteer's text has it today. The appearances
  marked `absent:` are not shown.
- **The Places index carries the maps too** (`site/_includes/places.html`):
  a row whose place appears on a map in the edition gains the map's short
  form after its kind — "— on [Łukom 1766]" — linked to the viewer. This is
  the literal link the editor asked for, from the place names list to the
  maps; the index stays a plain two-tier alphabetical list otherwise
  (PLACES_PLAN, section 8).
- **The viewer's marks and list link back** to the place pages (section 3).

The prose of the gazetteer ("*Grądzeń* (Łukom 1766)") is **kept as written**
— the links are carried by the section under the text, not by rewriting the
editor's sentences. MAPS_PLAN section 7 once said the "(Gilly 1802)" of an
entry should link to the map; whether the inline citations are linked too is
put to the editor (section 8 below), as a second step if wanted: the build
wraps each `cited_as` short form of an in-project map in the entry's text
with the link, leaving the words as they are.

## 5. The build

One new script, **`pipeline/maps/map_pages.py`** (the pattern of
`pipeline/places/place_pages.py`), which reads `reference/maps.yml`,
`maps/<map>/labels.yml` and `positions.yml`, and the gazetteer, and writes:

- `site/_data/maps_list.yml` — the cards' rows: slug, cited_as, year, kind,
  maker, title, the count of places marked, the tiles URL;
- `site/_data/maps.yml` — per map in the edition: its labels (id, form,
  place, shows, note, the crop's path, the point adjusted for the crop, the
  ground position), its description fields, its refs;
- `site/_data/place_maps.yml` — per place of the gazetteer: its appearances,
  the map's year and `in_project` joined in, `absent:` items dropped;
- the two list pages (`site/maps.md`, `site/de/karten.md` — small,
  hand-written, like `places.html`) and the generated map pages
  `site/_maps/<map>.md`, `site/_maps_de/<map>.md`, one per in-project map,
  front matter carrying the map's slug.

With it:

- `site/_config.yml`: the collections `maps` and `maps_de` (output, each
  file's own permalink), after the newspapers';
- `reference/maps.yml`: **`lukom1766` set `in_project: true`** when its page
  stands — the register's own rule;
- the generated files committed, as the place pages' are.

## 6. The checks (`pipeline/verify_site.py`)

- every in-project map's page exists in both languages and names its tiles
  URL, which matches the register's `tiles:` (a path check on the string,
  no request);
- every label on a map page has its crop file under
  `site/assets/maps/crops/<map>/` and its place in the gazetteer;
- every label id named in a gazetteer entry's `maps:` exists in that map's
  `labels.yml`, and every map named there exists in `reference/maps.yml`;
- every place page's "On the maps" links resolve (the built HTML's hrefs
  checked against the site's own pages, as the other checks do).

## 7. The steps in order

1. The branch (`maps-site`, from `main`, this worktree — the main checkout
   carries another session's work).
2. The build script and the data files (section 5), run once, the outputs
   inspected against `maps/lukom1766/` by hand.
3. The list page and the nav (`nav.maps`, `u_maps`, the header), both
   languages.
4. The `map` layout and the viewer script (OpenSeadragon from
   `pipeline/maps/vendor/` into `site/assets/`), the marks, the deep links,
   the details.
5. The place side: the "On the maps" section in `place_pages.py`, the index
   markers in `places.html`.
6. `lukom1766` to `in_project: true`; the map's `notes.md` updated; the
   changelog.
7. The checks of section 6 into `pipeline/verify_site.py`; a local Jekyll build;
   `pipeline/verify_site.py` clean; `/maps/`, `/maps/lukom1766/`, a place page and
   the index looked at.
8. Commit on `maps-site`. **Publishing stays the editor's word** (CLAUDE.md,
   "Branch and publishing"): fast-forward `main`, push, confirm the
   "Build and deploy" run.

## 8. Questions for the editor

- **The nav's place**: after Places, before Cemeteries — agreed?
- **Cards with thumbnails?** A card can carry a small view of the map cut
  from the tiles' top-level image, or stand as text only. Proposed: text
  only to start, a thumbnail when a second map arrives.
- **The index markers**: the Places index carrying "on Łukom 1766" after the
  kind, or the links living on the place pages alone (PLACES_PLAN's plain
  index kept bare)?
- **The inline citations**: the "(Łukom 1766)" of the gazetteer's prose
  linked as well (MAPS_PLAN, section 7), or the sections under the text
  enough?
- **The German section name**: Karten (proposed).
