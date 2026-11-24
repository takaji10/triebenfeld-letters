# Where the English reader-facing prose is authored

Inventory made 2026-11-24 by reading the layouts in `site/_layouts` and
`site/_includes` and the build scripts. Edit the **source** column; everything
under `site/_data`, `site/_holdings*`, `site/_maps*`, `site/_literature*`,
`site/_newspapers*`, `site/_people*`, `site/_places*`, `site/_cemeteries*`,
`dataset/` and `site/_site` is generated, except where marked "authored".

| # | Category | Source (path pattern) | English prose fields / files | Texts | Turned into site data by |
|---|----------|-----------------------|------------------------------|-------|--------------------------|
| 1a | Holding: "About" tab | `units/<slug>/about.md` (German: `about_de.md`) | whole file, Markdown; `[[41]]` cites a document, `[[unit:slug]]` a holding, `<!-- context -->` marks an uncited paragraph | 57 | `pipeline/build/unit_pages.py` writes `site/_holdings/<slug>.md`; layout `unit.html` |
| 1b | Holding: header lines | `units/<slug>/unit.yml` | `card_title` (card and `<h1>`), `full_title` (11 only; sub-heading), `title` (the standfirst under the heading, and on the Sources card), `short_title` (30; tab title only), `original_title` is source language | 57 each (`full_title` 11, `short_title` 30) | `pipeline/build/build_site_data.py` writes `site/_data/units.yml` |
| 1c | Holding: "Method" tab | `units/<slug>/unit.yml` `prepared:` (items are keys of `reference/prepared.yml` `sentences:` or inline `{en, de}`) and `reference/prepared.yml` | `sentences.<key>.en`, `headings`, inline `en:` | 57 holdings; 13 shared sentences | `unit_pages.py` (`prepared_text`), same page file |
| 1d | Not shown | `unit.yml` `description`, `archive_title`, `translation_note`, `notes.md` | `description` goes into `units.yml` but no layout prints it; the rest is working notes | 57 | not shown, ignore for house style |
| 2 | Document summaries | **`site/_data/summaries.yml`** (flat map `pad: text`, pad = `<slug>-<doc>`; German `summaries_de.yml` beside it, also `units/<slug>/summaries_de.yml`) | the value, one line | 649 | **Authored, not generated**, despite its header: `summarise.py --build` once assembled it from `cache/summaries-raw/` (not in repo); today changes go through `pipeline/review/set_summaries.py <batch.yml>` (also rewrites the unit's `intake/summaries_draft.py`/`english*.py`). `build_site_data.py` copies it into the search index; `letter.html` reads `site.data.summaries[page.pad]`; `build_dataset.py` copies into `dataset/` |
| 2b | Document translations (not prose about documents, listed for completeness) | `site/_data/translations/<pad>.yml` `segments[].en`; fixes in `reference/english_forms.yml`, `reference/english_corrections.yml` | the translation | 648 | `publish_translations.py`; never hand-edit alone |
| 3a | Literature | `literature/<slug>/work.yml` | `account_en` (work page), `brief_en` (card), `summary_en` (7 works kept off the site; their page shows only this), `note_en` (1), `title_en`, `title_en_card`, `published`, `published_card`; `english.md` is the translation of the work, not prose about it | 43 works (`account_en` 43, `brief_en` 43, `summary_en` 7) | `pipeline/literature/literature_site.py` -> `site/_data/literature.yml`, `site/_literature/` |
| 3b | Newspapers | `newspapers/<slug>/item.yml` | `account_en`, `brief_en`, `summary_en` (all 12 have one), `title_en`, `issue_en`; `english.md` is the translation | 12 items | `pipeline/newspapers/newspapers_site.py` -> `site/_data/newspapers.yml` |
| 3c | Maps | `reference/maps.yml` (`title_en`, `kind` slugs; no account/brief prose); `maps/<slug>/legend.yml` (`en:` on title, groups, items), `maps/<slug>/texts.yml` (`blocks[].names.en`, `margin.en`, translations of the sheet's text); `maps/<slug>/notes.md` is working notes | 23 `title_en`; legends 2; texts 1 (pelzucki1896) | `pipeline/maps/map_pages.py` -> `site/_data/maps.yml`, `maps_list.yml`, `site/_maps/` |
| 3d | Cemeteries | `cemeteries/<slug>/cemetery.yml` | `account_en` (the survey's account, kept as written), `title`, `graves`; `headstones.yml` tables | 10 | `pipeline/cemeteries/cemetery_pages.py` -> `site/_data/cemeteries*.yml`, `site/_cemeteries/` |
| 3e | Place-page sources | `places/<place>/place.yml`; `places/<place>/<source>/{source.yml,english.md,original.md}` | `standfirst_en`, `intro_en`; source's own English | 1 place, 1 source | `pipeline/places/place_pages.py` -> `site/_places/`, `site/_data/places_pages.yml` |
| 4a | Eras (cards, timeline, story) | `reference/eras.yml` | `label_en`, `intro_en`, `blurb_en`, `ownership_en` | 7 eras | `build_site_data.py` -> `site/_data/eras.yml`; `timeline.html` shows `ownership_en`, `intro_en` (else `blurb_en`) |
| 4b | Era pages, story, about | `site/eras/<era>.md` (German `site/de/epochen/`), `site/the-story.md`, `site/about.md`, `site/hohenlohe.md` | whole file | 7 era pages (1,000 lines), about 240 lines | **Authored in place** (no script writes them; `verify_site.py` checks) |
| 4c | Place cards and pages | `reference/gazetteer/*.yml` (one per place; the editor's text kept as written), `reference/places.yml`, `reference/place_tiers.yml`; shared: `reference/shared_pages.yml`, `reference/site_notes_de.yml` | gazetteer entry text (en/de), `places.yml` descriptors | about 112 places | `pipeline/gazetteer/gazetteer.py`, `build_site_data.py` -> `site/_data/places*.yml`, `site/_places/` |
| 4d | People | `reference/people_bios.yml` (`bio`, `life`; slug keyed), `reference/people_headings.yml` (`en`), `reference/people.yml` (matching rules, not prose) | `bio` | 320 bios, 44 headings | `build_site_data.py` (BIOS) -> `site/_data/people.yml`; `pipeline/build/person_pages.py` |
| 4e | Person pages (genealogy) | `reference/genealogy.yml` `people.<slug>`: `heading`, `bio`, `notes`, `life` (standalone ones: `standalone: true`); `reference/estate_tree.yml` | `bio`, `heading`, `notes` | 12 persons (7 standalone with `bio`) | `pipeline/build/person_pages.py` -> `site/_people/`; `pipeline/genealogy/build_estate.py` |
| 4f | Glossary | `reference/glossary.yml` | `head_en`, `short_en`, `long_en` | 120 | `glossary_build.py` -> `site/_data/glossary.yml` |
| 4g | Connections, timeline | `reference/connections.yml` (sentence per link), `site/_data/timeline.yml` (authored) | `why`-type sentences | 11 / n | `connections_site.py` |

## Generated English (edit at the source)

- `site/_data/units.yml`, `eras.yml`, `literature.yml`, `newspapers.yml`,
  `maps.yml`, `people.yml`, `places*.yml`, `glossary.yml`, `cemeteries*.yml`,
  `connections.yml`, `literature_links.yml`, `*_mentions.yml`, `stats.yml`:
  generated by `build_site_data.py` and the section scripts.
- `site/_holdings*/`, `site/_literature*/`, `site/_newspapers*/`, `site/_maps*/`,
  `site/_people*/`, `site/_places*/`, `site/_cemeteries*/`: generated pages.
- `dataset/` and `site/_data/translations/`: generated from units and caches.
- The one trap: `site/_data/summaries.yml` is *edited* (via `set_summaries.py`),
  although it says "Generated by summarise.py".

Not edited by anyone for house style: German twins (`*_de`, `about_de.md`,
`summaries_de.yml`), `notes.md`, `rulings.yml`, translations of documents.
