# Plan: the gazetteer

Status: **agreed with the editor 2026-10-23**; step 1 done (the import), the
rest to come in the order of section 8. Nothing of it is on the site yet.

The editor, 2026-10-23, giving their file "Place Names.md": "my own
compilation of as full of an index as I could possibly assemble of place
names from the Trąbczyn and Zagórów area. They are the main focus for the
project ... The point is to supplement the existing place name database with
this one." The index is "to share the history of a place, name variations,
significant (or, in the case of non-recent times, any) dates related to the
place, and other relevant information. Eventually I will add GPS data to it.
I will want the places to become a queryable dataset within the project."
Later, once the outstanding sources are in, Claude is to go through the
edition and add what the editor's index lacks (section 8, step 7).

The editor's rulings of 2026-10-23 (Claude's four recommendations, accepted):

- **The modern name heads an entry** (Augustynów, Mały Las, Grądzeń); the
  register's older spellings stand as names of the place. The register's
  slugs stay, so no address on the site changes (`ludwigslust` is the slug
  of Mały Las, `gradzyn` of Grądzeń, `augustinow` of Augustynów).
- **The editor's text is kept as they wrote it**, credited to them, not
  rewritten to the house style. It is a sample of their voice for short
  entries in index style (`docs/EDITORS_VOICE.md`, "Index entries").
- **Every place gets a page**, however short its entry.
- **The work is on its own branch** (`gazetteer`).

And, 2026-10-23: **a running list of missing sources**
(`docs/MISSING_SOURCES.md`); the maps' and sources' rights are left to the
end of the project ("for now just assume the rights aren't an issue").

---

## 1. What the gazetteer is, beside what exists

- **The register** (`reference/places.yml`) is the edition's authority on a
  place's identity: its display form, the pattern that finds it in the
  documents, its variants, what it must not be confused with. It has 203
  places, most of them far away (Berlin, Venice, Breslau). It stays the
  authority on identity and matching.
- **The gazetteer** (`reference/gazetteer/<slug>.yml`) is the editor's
  index of the Trąbczyn and Zagórów area: 112 places, each with its history,
  its names, its dates, its sources and its appearances on the old maps. A
  gazetteer entry names its register slug in `register:` where the place is
  already in the register (27 of them); the others are new to the edition.
- **The place pages** (`places/<slug>/`, `docs/PLACES_PLAN.md`) carry the
  sources brought in for one place (Zagórów's town presentation). A place
  with both has one page: the gazetteer entry first, its sources below.

## 2. The files

```
reference/gazetteer/source/place_names_2026-10-23.md   the editor's file, verbatim
reference/gazetteer/<slug>.yml        one place: the editor's text, its kind and
                                      location, its names, its map appearances,
                                      its footnotes resolved, open points
reference/gazetteer_sources.yml       every work the footnotes cite, and where
                                      it is in the edition (or that it is not)
reference/maps.yml                    every map the entries cite
pipeline/gazetteer/import_place_names.py   the import of 2026-10-23 (a record:
                                      the YAML is edited by hand from here on)
pipeline/gazetteer/gazetteer.py       --check (the links, the keys, the slugs)
                                      --missing (docs/MISSING_SOURCES.md)
```

An entry's fields, in order: `slug`, `heading`, `register`, `status`
(`extant` where the editor's heading is bold, `historical` where italic),
`kind` and `kind_text`, `location` (section 5), `text_en` (the editor's
words), `names`, `aliases` (the editor's "See" headings that point here),
`maps`, `footnotes` (each with its `refs`: a source key, a locator, a link
or none), `review` (what is still to settle). The German text (`text_de`)
is added in step 3.

**The editor's "See" lines are not kept as entries.** They become names of
the place they point to, and the A–Z list on the site makes the cross-
references from the names, so a new name never needs a "See" line by hand.

## 3. The text

The editor's text is shown as written, with only the marks of the export
removed (`\[`, `\.`, "km2"). Each footnote becomes a link where its source is
in the edition: a document's page (a leaf of the boundary decree of 1775
opens at that leaf), a page of a book, a glossary entry. A footnote whose
source is not in the edition stays a plain citation, and the source goes on
the missing list.

**No method talk on a place's page** (the editor, 2026-10-23: "I never
explain to the reader what I'm doing or how (like this project tends to
over-do)"). A place page has no paragraph on what the page gathers or how it
was made; the facts begin at once. The one line of credit ("Entry by
<editor>") is the only thing that is not about the place. The German is
Claude's, written to the same voice.

**Where the editor's text and the documents differ**, the text is not
changed: the difference goes into `docs/NEEDS_CONFIRMATION.md` ("The
gazetteer"), and the editor rules (HOUSE_STYLE, "The documents first"). The
editor's file is content for the site, not only a style sample, so its facts
are checked like any other source's (the rule of WORKING_NOTES on style
samples does not apply to it).

## 4. The sources and the missing list

`reference/gazetteer_sources.yml` holds every work the footnotes cite. Each
key says how a locator becomes a link: by Kodeks volume and number, by a
court book's leaf, by a table, by a page of a book, or not at all. Of 119
footnotes, 76 link to the edition at the import (79 of their 126
references). The other 43 cite the parish registers of Trąbczyn and
Zagórów, the *Słownik geograficzny*, Perthées' parish descriptions of
1796, three court-book passages, a mortgage file, and ten Kodeks entries
the holding lacks. The entries name 27 maps, 179 times; none of them is in
the edition yet.

`docs/MISSING_SOURCES.md` is the running list. Its gazetteer part is made by
`gazetteer.py --missing`; a part kept by hand lists what the rest of the
project waits on. When a source comes in, its key is pointed at it and the
script is run again: the footnotes become links and the line leaves the list.

## 5. Where a place is

Four degrees, in `location.precision`, because many of the places were never
on a map and some cannot be placed at all:

| precision | what it means | on the interactive map |
|---|---|---|
| `surveyed` | coordinates of the place today (OpenStreetMap, or the editor's GPS) | a pin |
| `from_map` | placed by a mark on a georeferenced old map (section 6) | a pin of another kind, with the map named and its error |
| `described` | only the editor's words: "south of Łazy", "belonging to Łomów" | no pin: named in the popup of the place it is described from |
| `unknown` | "Location unknown" | no pin: listed apart |

`location.text`, `relation`, `relative_to` and `belongs_to` hold the
editor's own description from the first sentence of the entry; they stay
when coordinates are added, as the record of what the sources say.

## 6. The maps

The parts to build and their order are in `docs/MAPS_PLAN.md` (2026-10-23).
The editor chooses which maps come in, one at a time ("I will be selective
with them"). What follows is the design of the marking.

**What the mark is for**: two things, which are not at the same spot on an
old map. (a) The **place itself**: the village's dot, the church, the mill,
the middle of a forest. That point is what the interactive map and the
georeferencing need. (b) The **lettering**: the name as the map spells it,
which is what a reader wants to see and what a citation points to. The
lettering usually sits beside the symbol, often slanted or curved along a
road or river.

**The labelling page** (built like the fold page, `pipeline/intake/
fold_page.py`: one map at a time, zoom and pan, keyboard, a Save button that
gives a file to bring in):

1. **The list to find.** The page opens a map with the labels the
   gazetteer already records for it ("Gilly 1802: Grondzyn – Grądzeń;
   Bukower Hol. – Bukowe; Stara Huta – Huta Łukomska ..."). The editor picks
   one; nothing has to be typed. A label not on the list: type the form as
   written and pick the place by any of its names, or mark it "new place".
2. **Click the place.** One click on the symbol. Where the map shows no
   symbol (a forest's name across the trees), skip it.
3. **Trace the lettering.** Click at the start of the word, at each bend,
   and double-click at its end: two clicks for straight text at any slant,
   three to five for a curve. The page draws a band of adjustable height
   along the line; that band is the crop shown on the site. It is quicker
   than a box round a curved word, and it fits one. Where speed matters
   more, the lettering can be skipped and the page cuts a square round the
   point.
4. **What it is.** A short list of what the map shows there, with keys:
   village, Olęder settlement, folwark or manor, tavern, water mill,
   windmill, forest, field or meadow, water, road or crossing, church,
   other, **unsure**. It defaults to the place's kind; "unsure" is a full
   answer and never blocks the save. The editor's own notes ("with a
   windmill", "appeared as a folwark") stay as the appearance's note.

Each saved mark is one map appearance: `{map, form, point, trace, shows}`,
kept in `maps/<map>/labels.yml`, and the gazetteer's `maps:` list is filled
from it.

**OCR is not used on the maps.** Map lettering is curved, spaced out over
hachures and symbols, and in many hands and typefaces; the editor knows
which label is which place, and the list to find already holds most forms.

**Georeferencing comes from the marks.** When the places that exist today
have coordinates (section 5), every point the editor clicked on a map for
such a place is a control point: with four or more per map the map can be
laid over OpenStreetMap. Then the points clicked for the vanished places on
that map (Rosciszewo, Lusnie Olędry, Bieganszczyzna) give their coordinates
(`from_map`), with an error from the fit.

**On the site**: a viewer for each map (zoom and pan), and on each place's
page a strip of the crops of its lettering, map by map in date order: how the
name looked on von Pfau, on Gilly, on Reymann. A crop opens the map at that
mark. The editor's "(Gilly 1802)" in the text links to the mark.

**The images**: the large scans are cut into tiles for the viewer; the
originals stay off the repository, like the archive scans. Each map's full
description (title, maker, scale, holder, reference) goes into
`reference/maps.yml` when it is brought in.

## 7. The dataset and the interactive map

- **Downloads**: the whole gazetteer as JSON and CSV from the site, and, once
  there are coordinates, as GeoJSON in the Linked Places format (the format
  of the World Historical Gazetteer, for sharing historical gazetteers).
- **A search page**: by any name or spelling, by kind, by period (first
  mention, last map), by whether the place still exists, by source, by map.
- **The interactive map**: Leaflet over OpenStreetMap, the places by their
  precision (section 5), the old maps as layers once georeferenced, each pin
  opening the place's entry.

## 8. The steps

1. **The import** (done 2026-10-23): the editor's file in the repository,
   112 entries as YAML, the footnotes resolved, the sources and maps listed,
   the check, the missing list.
2. **Claude's reading of the import**: the names and map appearances read
   against the text, the identifications with the register settled (the
   points in NEEDS_CONFIRMATION, "The gazetteer"), the differences from the
   documents listed.
3. **The pages**: a page per place, English and German, the footnotes
   linked, the names over time, the map appearances, the documents,
   literature and newspapers that mention the place (from the indexes that
   exist); the A–Z list of every name on the Places page; Zagórów's page
   with its entry above its sources. The new places go into the register
   (display and variants; no matching yet). Checks in `verify_site.py`.
4. **The dataset**: the downloads and the search page.
5. **The maps** (`docs/MAPS_PLAN.md`): the labelling page, a pilot map,
   then the maps the editor chooses.
6. **The interactive map**, once coordinates are in.
7. **The index and the enhancement pass** (at the editor's word, once the
   outstanding sources are in): patterns to find the new places in the
   documents, every hit read and ruled. Many of the names are common words
   (Budy, Huta, Noga, Grabina, Posada, Laski, Wygoda, Królestwo, Cygany,
   Las), so each pattern is narrow and its hits are read before it stands.
   Then Claude adds to each entry what the edition says that it lacks, with
   footnotes, marked as Claude's addition.
