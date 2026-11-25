# Places, people and the glossary: plan (2026-11-24)

The editor's list of 2026-11-24 for the Places page and the place entries,
the People page and person pages, and the Glossary; then the work still
outstanding from the site overhaul (docs/SITE_OVERHAUL_PLAN.md, Phase 6).
Who does each step follows CLAUDE.md, "Sub-agents first": a script, then
Haiku (mechanical, with a machine check), then Sonnet (code to a spec,
reading, flagging, claim checks), and Opus, the main session, for the specs,
every identification, every ruling put to the editor and every sentence a
reader sees. English only; the German follows later, all at once (the
editor's word).

## What was found while planning

- **The "broken" links are a prefix bug.** The place entries' footnotes are
  written as plain Markdown links (`/documents/kdw/11/`) inside a raw block,
  so they bypass `relative_url` and miss the live site's `/triebenfeld-letters`
  prefix. The documents exist. Fix at the generator
  (`pipeline/places/place_pages.py`), and add a verify_site check that no
  built page carries a root-relative link without the prefix (the current
  check runs with an empty baseurl and cannot see it).
- **Słownik geograficzny and Nazwy miejscowe Polski** citations show no link
  because those works had no page until today. Both are now shown in full
  (`slownik`, `nmpol`); each citation can link to its entry on the work page.
  No new literature entry is needed.
- **Coordinates.** 106 gazetteer places carry `lat`/`lon`, rounded to about a
  kilometre; the places of the register outside the gazetteer (Berlin,
  Wrocław, Dresden ...) carry none.
- **Antoni Prusimski's death.** The edition's life-line is "1744–ca 1806"
  (PSB, accepted 2026-10-22, the "ca" left open). The documents say more:
  he was alive at Dresden in April and May 1803 (Nr. 3132), and the
  Prussian note of 1819 (Nr. 12366, doc. 3) gives his death as 1803. By the
  rule "the documents first" the date should be "d. 1803 or later" with the
  difference flagged; see step P6.

## Part A. The Places page (first)

| Step | What | Who |
|---|---|---|
| A1 | **Coordinates for every mappable place.** Coordinates stored in `reference/places.yml` (`lat`, `lon`, `precision`), taken first from the gazetteer, then from the georeferenced maps' marks, then (with the editor's yes, a network fetch) from Wikidata/GeoNames for the rest. A script `pipeline/places/coords.py --check` fails the build when a place is added or removed and the coordinates or the derived data are stale; it runs in regenerate.py and in verify_site. | script by Sonnet; Opus checks every identification of a Wikidata match |
| A2 | **Search bar on the Places page**: the standard component (`browse.html`, kind `places`) with a text box and a "Near" control: a place picker plus 5, 10, 20, 50, 100 km, distances computed in the browser from the stored coordinates (haversine); unmapped places are listed as "no position" and left out of a distance search. | Sonnet to spec |
| A3 | **Order**: both sections (the Trąbczyn and Zagórów area; other places) kept alphabetical by the generator, whatever order places are added in, with A–Z/Z–A per section; a check in verify_site that the built lists are sorted. | script + Sonnet |
| A4 | **The map**: one large map (Leaflet, already used on the map pages) with OpenStreetMap and a satellite layer (the tile sources the site already uses), a marker per mapped place; filters for "Trąbczyn and Zagórów area" and "Other places", and per type of place. | Sonnet |
| A5 | **Marker set by type**: one standard icon set (town, village, colony/Olęder settlement, demesne farm, mill/inn/forge, church/parish, forest/ground, estate, city, region) in the site's line style, light and dark; a legend that switches each set on and off. Opus draws up the mapping from `kind:`; the editor sees the set before it ships. | Sonnet draws, Opus maps |
| A6 | **Listings**: "Place — type" or "Place — see Place"; the map citations ("on Kozłowski 1861 ...") leave the list; the two "see" lines of Stara Huta Olędry joined ("see Huta Łukomska and Huta Trąbczyńska"); the descriptor "Every place of the neighbourhood ..." removed. | script |
| A7 | **Cemeteries**: alphabetical, descriptors removed; "Michalinów gm. Oleśnica" renamed "Michalinów Oleśnicki" (title only; the survey's own text stays as written). | script |

## Part B. Individual place entries

| Step | What | Who |
|---|---|---|
| B1 | **Map in the header**: larger, OpenStreetMap with a satellite switch, placed after the line that says where the place lies. | Sonnet |
| B2 | **Citations**: the citation itself becomes the link ("Ibid No. 1363." linked), the "The document." links go; several documents for one citation each get their own number-link. Słownik and Nazwy citations link to their entries. The prefix bug fixed (above). | script in place_pages.py |
| B3 | **Section order and names**: "References on maps (n)" with a "Show" expander, above "References in documents (n)" (a subheader, expander "Show"); the footnotes under a subheader "Citations". | Sonnet |
| B4 | **Footnote jumps**: clicking a note or its ↩ scrolls the target to the middle of the screen and highlights it briefly (both ways), on place, literature and document pages alike (one small script). | Sonnet |
| B5 | **Units of measurement**: a rule in HOUSE_STYLE, "Units": an old unit keeps its own name, in the form the glossary heads it, italic where foreign (*Morgen*, *Hufe*, *łan*, *włóka*, *grzywna*), never a Polish or German inflected form in English prose ("morgi" becomes *Morgen*, "grzywny" *grzywna*s), and links to its glossary entry. A lint finds the inflected forms site-wide; the editor's own texts (gazetteer, survey) are asked about before any change. | Opus rule, script lint |
| B6 | **Pronunciation**: for Polish place names, IPA made from the spelling by a rule script (Polish spelling is close to phonemic; stress on the penult), shown small after the name; German names only where a reliable source gives it. Opus checks every output; a sample goes to the editor first. | script, Opus |

## Part C. The People page and person pages

| Step | What | Who |
|---|---|---|
| C1 | **Who matters.** Opus scores every person by documents, eras, and their part in the story, and proposes a "relevant" list (expected 25 to 40). The editor approves the list before it is built. | Opus |
| C2 | **Eras for people**: each person placed in the eras of the documents that name them (a person in two eras shows in both). | script |
| C3 | **Three views**: by era (default; relevant people first, "Show the others" at the end of each era), A–Z/Z–A, by mentions. | Sonnet |
| C4 | **Bios rewritten** (all 320) to the rules: no restated name, context for every claim ("the claim for compensation" says whose and against whom), no document talk ("only the initial ... can be read"), names in their standard form (Prince Hohenlohe-Ingelfingen; von Triebenfeld). A Sonnet reader flags; Opus rewrites; facts added from the person's documents only. | Sonnet flags, Opus writes |
| C5 | **Chełmski split** into the individuals (Stanisław Ścibor Chełmski of Łukom at the centre; Jerzy, Franciszek, Józef ...), with their documents re-tagged and checked. | Opus, script re-tag |
| C6 | **Person pages for the relevant people**: a longer biography with citations, on the existing pattern (`reference/genealogy.yml`, `person_pages.py`); "Their page" becomes "Read more". | Opus writes; Sonnet claim-checks |
| C7 | **Life dates**: for each relevant person, birth and death dates looked for in the documents first, then the literature; inferred dates cited on the person page; differences flagged in NEEDS_CONFIRMATION (Prusimski first, above). | Sonnet searches, Opus rules |
| C8 | **References**: "References in documents (n)" and "References in literature (n)" as subheaders, each with a "Show" expander. | Sonnet |

## Part D. The Glossary

| Step | What | Who |
|---|---|---|
| D1 | **Language labels**: say only what is true and useful. A word used in its own language form gets that language ("French: *Cabinets-Ordre*"); a borrowed form gets the borrowing language and its source ("German *Competenz*, from Latin *competentia*"). Opus reviews all 120. | Opus |
| D2 | **References**: "References in documents (n)" with "Show", as elsewhere. | Sonnet |
| D3 | **Sources**: the "to be checked against ..." notes leave the page; a checked entry ends with one line "Reference: <link>". | script |
| D4 | **Categories** ("Law and administration" ...): remove, unless the editor wants them as a filter (they serve no reader purpose as labels). | the editor's word |
| D5 | **Relevance**: entries like "humble servant", "I remain until death", "Rubrik" moved to `excluded:` with a reason, after the editor sees the list of such entries. | Opus proposes, the editor rules |
| D6 | **Prose to the rules** ("the documents name him by it", "In the letters they survey estates"): every definition read and rewritten. | Opus |

## Part E. Then the outstanding work

1. The Zagórów place page (the edition's own prose) to the rules.
2. The ~600 document summaries, holding by holding (prose_lint and a Sonnet
   reader flag; Opus rewrites; a Sonnet claim check; `set_summaries.py`).
3. The literature's title pages when the editor sends them.

## Order

A1 (coordinates and the prefix fix) → B2, B3 (references, which also fix the
links) → A6, A7, A3 (listings) → A2, A4, A5 (search and map) → B1, B4 →
C1 (the relevant list, to the editor) → C2, C3, C8 → C4, C5 → C6, C7 →
D1–D6 → B5, B6 → E. Each part ends with build, verify_site, screenshots,
CHANGELOG, and is published at the editor's word.

## The editor's answers (2026-11-24)

1. **Coordinates** for places outside the gazetteer: fetched from Wikidata,
   each match checked by Claude (the host may need allowing in the cloud
   environment).
2. **Pronunciation**: IPA generated from the Polish spelling by rule, each
   checked by Claude, a sample shown to the editor first; German names only
   where a source gives it.
3. **Glossary categories**: removed.
4. The "relevant people" list goes to the editor for approval before the
   People page is rebuilt. **Approved 2026-11-25** ("Looks good").
5. (2026-11-25) The pronunciation sample accepted; shown on the place pages.
6. (2026-11-25) The glossary's courtesy styles, closing formulas and
   document furniture moved to `excluded:`, but *locus sigilli* kept, since
   "L. S." stands in the English translations.
7. (2026-11-25) Claude's place identifications accepted "on first glance".
8. (2026-11-25) The grzywna: "marks" was not used consistently, so the
   original unit stays, *grzywna*/*grzywny*, with a glossary entry
   (HOUSE_STYLE, "Units of measurement and money").

## C1. The relevant people: proposal (for the editor's approval)

Chosen by their part in the story of the estate, not by mentions alone (the
Hohenlohe letters name hundreds of creditors and officials once or twice).
Each gets a full person page (C6) and shows first in their era (C3). Those
marked * already have a page.

- **Middle Ages**: Count Mikołaj, treasurer of Ląd, to whom Trąbczyn was
  given in 1276; Jan and Przedpełk of Trąbczyn, the heirs of 1346.
- **The boundary dispute**: Antoni Prusimski*; Paweł Prusimski;
  Katarzyna Prusimska, born Rozdrażewska; Krzysztof Prusimski*; Stanisław
  Ścibor Chełmski*; the Otto-Trąmpczyński family* (Wojciech/Albertus of
  1589 and his kin); Ludwik Dąmbski, president of the commission of 1775.
- **The insurgency**: Antoni Prusimski*; Tadeusz Kościuszko; Xaver Jezierski.
- **The Hohenlohe years**: Prince Friedrich Ludwig of Hohenlohe-Ingelfingen;
  Peter Friedrich von Triebenfeld; Johann Wilhelm Glenck; Michalina
  Prusimska; Karl Leopold von Köckritz; Count Hoym; Otto Karl Friedrich von
  Voss; Karl August von Hardenberg; Hawich; Martin Honrichs; Joseph Zerboni
  di Sposetti.
- **The restitution**: Michalina Miączyńska; Stanisław Miączyński*; Carl
  Ferdinand Weigel; Prince Franciszek Ksawery Drucki-Lubecki.
- **The colonists' rights**: Count Włodzimierz Miączyński; the Zelmer family;
  Pastor E. Erdmann.
- **The twentieth century**: the teacher Mielke of Łazińsk.

Not proposed, though often named: the Prince's many creditors and bankers
(Cosmar, van der Lahr, Stössel, Oppenheimer, Schlabrendorff ...), clerks and
messengers (Schenck, Hecker, Szepczyński ...), and kings and ministers who
appear only in passing (Napoleon, the Prussian kings, Haugwitz, Goldbeck),
who stay on the People page with their short entries.
