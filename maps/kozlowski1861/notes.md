# Kozłowski 1861 (`kozlowski1861`)

The collective plan of the Trąbczyn estate of 1861, APP 1/402/0/-/536-23
(Archiwum Państwowe w Poznaniu), drawn by the sworn surveyor Seweryn
Kozłowski, first class, for Count Włodzimierz Miączyński. The second map
brought into the edition, at the editor's word (2026-10-30), by
`docs/ADDING_A_MAP.md`.

Title: *Plan zbiorowy dóbr Trąbczyna z przyległosciami dziedzicznych Jaśnie
Wielmożnego Włodzimierza Hrabi Miączyńskiego w Gubernii Warszawskiej Powiecie
Konińskim położonych Powierzył r 1861 i zrysował Seweryn Kozłowski Geometra
Klassy I* (the archive's catalogue form: "Plan zbiorowy dóbr Trąbczyn w
powiecie konińskim").

## The image

- **The original is the archive's JPG** (15,757 x 12,140 pixels, 28.7 MB) on
  J:, which is also the image georeferenced on MapWarper (70818, "Trąbczyn
  Estate, 1861"; the same size), so every control point and mark is in its
  pixels.
- **Drawn north-up** (the lettering reads upright; `view_rotation: 0`). The
  whole sheet is tiled, with no crop: 1,003 files, 43.4 MB, in
  triebenfeld-maps/kozlowski1861/. The scan includes the archive's colour
  chart and grey background at the right and bottom edges.
- The sheet is folded in fifteen panels (the creases show). It carries a
  title cartouche, a compass rose, the legend *Wyjaśnienie Kolorów*
  and a scale bar (*Podziałka Nowo Polska*), **1:20 000** (confirmed by the
  editor, 2026-10-30; the register's `scale`).
- **The legend is in the edition** (`legend.yml`, built onto the map page by
  `map_pages.py`, 2026-10-30, at the editor's request): the fifteen blocks
  under their five grouping headers, with water and "drogi i place pod
  zabudowaniami" standing outside the groups as on the sheet; the Polish as
  written, read by Claude from the scan, and an English column, to be
  checked by the editor. The colours: nine `fill`s are the editor's
  codes, given 2026-10-30 (manorial, church, peasant, colonists',
  coniferous, deciduous, copses, dry meadows, roads and plots under
  buildings), the rest the scan's (fill, pencil line and every block's
  coloured edge strip sampled; in the render the edge
  strip is used for water's frame alone — at the editor's word it is the
  one block with a thicker border, a thinner darker line on its weaker
  sides). The three patterned blocks (orchard's plain dots, the wet
  meadows' and pastures' blue dashes, water's graded pale inset) are
  drawn with the page's CSS; the squares render 3.9 × 1.8 rem, and there
  is no caption under the table (no explainer text on the site). Łukom
  1766 has no legend on its sheet: the section shows only where a map
  has `legend.yml`.

## The georeference

- **Four control points** from the editor's MapWarper georeference
  (`georef.yml`, read on 2026-10-30).
- **The affine fit** (georef.py): RMS 5.8 m; residuals 0.4 to 8.9 m. A tight
  fit, as befits a surveyor's plan of 1861.
- `georef.json` in triebenfeld-maps/kozlowski1861/ is the Allmaps annotation;
  .../warp.html?map=kozlowski1861 lays the map over OpenStreetMap.

## What the gazetteer says is on it

The gazetteer cites this map as *Kozłowski 1861* for many of its places;
the labelling page's "To find" list held 13 of them (the entries whose map
appearances are parsed from the short form).

## The editor's marks (2026-10-30)

- **31 labels** (`labels_kozlowski1861_20261030-1620.json`), all 13 names to
  find among them. 25 are linked to places of the gazetteer (13 existing map
  appearances, 12 added: Szetlewek, Stanisławów, Porąbki, Nowa Wieś, Osiny,
  Przybysław, Łazy, Trąbczyn, Huta, Włodzimirów, Maryantów, Grabina); six
  are forest districts (*okręg*: Osiny, Grabina, Garbinck, Studzienka,
  Wypalanki, Noga) marked as new places, to be ruled. Two more are Łazinskie
  [Kolonie] and [Kolonia] (Michalinów), both Olęder settlements.
- **The crops** were looked at together: all 31 whole and upright, the
  lettering not cut.
- **The fit again**: no marked place has surveyed coordinates, so the four
  MapWarper points stay the control set (RMS 5.8 m) and every mark gets a
  position (`positions.yml`). Against the gazetteer's coordinates, ten
  identified places land within 40 to 480 m (Kolonia 919 m); Czerwonka and
  Nowa Wieś land 15.9 and 18.5 km away, which points to the entries'
  coordinates (NEEDS_CONFIRMATION, "The gazetteer").
- **On the site** (2026-10-30): `in_project: true`, the card and its
  thumbnail, /maps/kozlowski1861/ and /de/karten/kozlowski1861/, the place
  pages' "On the maps". Archive link:
  https://www.szukajwarchiwach.gov.pl/en/jednostka/-/jednostka/24675961.

## Rulings (2026-10-30, the editor)

- **The okręg are part of the obręb**: the six labels are appearances of
  Włodzimirów Obręb (Osiny, Grabina, Garbinck) and Wielki-Bór Obręb
  (Studzienka, Wypalanki, Noga), not places of their own. The saved file
  was copied with that change, `labels_kozlowski1861_20261030-1620-okreg.json`
  (the editor's file kept), and imported again; the gazetteer items carry
  the note "A district (okręg) of the precinct". *Noga Okręg*'s note read
  "Wielki-Bór Okręg", a slip for Obręb (corrected).
- **The marks' placing is accurate**: the entries' coordinates for Czerwonka
  and Nowa Wieś (16 and 18 km off) were wrong. Czerwonka now has the mark's
  position (52.116603, 17.957974; precision `from_map`); Nowa Wieś the
  position of the village in `reference/places_osm.yml` (52.14177, 17.93662;
  a third of a kilometre from the mark).

## Still to do

- The ten empty map forms in the gazetteer entries (the labels carry them).
- Not pushed: the site is published only at the editor's word.
