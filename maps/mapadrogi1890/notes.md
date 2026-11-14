# Mapa dróg 1890 — the roads map of the Słupca poviat

The twenty-first map in the edition and one of the bulk batch of 2026-11-06
(docs/ADDING_A_MAP.md; the register's entry in `reference/maps.yml`). The
Russian-language map of the roads of the Słupca poviat, ca. 1890 (the
editor's date), AGAD 1/402/0/-/491-93. The whole map is in (the editor's
word); no MapWarper georeference — the map is placed from the editor's marks
alone.

## The labels and the batch's exception

The editor marked **37 labels** (35 gazetteer places — Pyzdry included in
the re-save — and two new places, **Stara Huta** and **Świątniki**, whose
entries wait on the editor's ruling, NEEDS_CONFIRMATION). Świątniki has
its gazetteer entry since 2026-11-14 at the editor's word
(`reference/gazetteer/swiatniki.yml`, label mapadrogi1890-060 linked);
Stara Huta is still open. Колонія Вромбчинъ (label mapadrogi1890-008),
first linked to Wrąbczynkowskie Holendry, is Kolonia Wrąbczyn, a place of
its own and today's Wrąbczyn Górski (the editor, 2026-11-14;
`reference/gazetteer/wrabczyn-gorski.yml`); its type changed from unsure to
village at the editor's word.
The Prince's renamed colonies show their first name with today's in
brackets on this map's page, "Kolonia Adolfsberg (Zalesie)" (`founded_as`
in the gazetteer). The map is
Russian, so this map is the batch's exception, agreed in advance: the editor
marked each label with the **Polish standard form** in the form field and
left the as-written form to Claude's OCR.

The OCR (2026-11-06): the crops of the lettering
(`site/assets/maps/crops/mapadrogi1890/`, cut by the import) were **read by
Claude directly** — pre-reform Russian Cyrillic; the lunaroute converter
cannot reach a localhost URL and takes no file path, and no Russian
Tesseract model is installed — each reading cross-checked against the
editor's Polish standard and against the transliteration conventions
witnessed on the Pełzucki 1896 plan's own title (Тромчинъ for Trąbczyn,
Лазинскіе for Łazińskie). The readings stand in `labels.yml` as:

- `form:` — the Russian **as written on the map** (what every other map's
  form field holds; the gazetteer's map appearances carry it too);
- `form_standard:` — the editor's Polish reading, kept verbatim;
- `form_map_conf:` — high / medium / low. The one low reading was settled
  by the editor (2026-11-06): Скукумъ read again as **Скокумъ** (Skokum);
  and Тромчинъ corrected to **Тромбчинъ** (Trąbczyn) at the editor's word.

Two readings worth noting: Trąbczyn is Тромбчинъ on this map (the editor's
correction of Claude's Тромчинъ, 2026-11-06 — the б of the Polish b
transliterated where the 1896 plan's title has Тромчинъ; the two maps
transliterate differently), and the German-named colonies keep their
German names in Russian transliteration (Эмилиенгейм, Колонія Адольфсбергъ,
Колонія Людвигслюстъ, Колонія Софиенталь, Колонія Фридрихсфельдъ,
Колонія Ингельфингенъ).

## The georeferencing

From the marks alone (MAPS_PLAN, section 5): `georef.yml` was created empty
and the 35 marked places with coordinates joined as mk-* control points.
The coordinates come from the gazetteer — where this map's marking exposed
that the marked places had no `surveyed` coordinates, the plan's section-6
lookups ran (scratch/maps_bulk/osm_check.py, osm_check2.py): **34 places
confirmed on OpenStreetMap** (Nominatim, 2026-11-06), 29 against their
entries' own `identified` points, 3 confirmed to the meter under corrected
queries (Wrąbczynkowskie Holendry, Wrąbczynek, Pyzdry), 2 described entries
taking OSM's matching point (Łazińskie Olędry — the modern Łazińsk Drugi's,
2.7 km south of Łazy as the entry says; Budy — the hamlet in Grądzeń, as the
entry says). Every written coordinate carries `location.check` with the
found string; the editor's own GPS replaces any of them.

The fit: **order 1, RMS 830 m** over 35 points — the class of a schematic
roads map, distances along roads not to scale. Residuals worth the editor's
eye (a misfit is a question, not a correction): mk-mapadrogi1890-034
(Olędry Michalinówo, 2.9 km), mk-mapadrogi1890-038 (Łazińskie Olędry,
1.4 km) — both at the map's east edge — and mk-mapadrogi1890-008 (Kolonia
Wrąbczyn, 2.4 km, whose trace carried a doubled point in the saved file).

## Where it stands

Steps 1-7 of docs/ADDING_A_MAP.md done; the OCR's readings are Claude's and
the flagged one waits on the editor; `in_project: true` and the site page
built at the import. Open (NEEDS_CONFIRMATION carries the list): the two new
places; the low-confidence reading; the fit's outliers; the whole set of
readings at the editor's eye where a crop is doubtful.
