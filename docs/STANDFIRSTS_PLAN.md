# The standfirsts — what they were, what stands, what went

Ruled by the editor, 2026-10-28. The completion of the preamble work of
2026-10-27 (see the changelog's that day's entries and this pass).

## What the style was

The site's section pages opened with a prose paragraph between the heading
and the content - a standfirst, as journalism calls it. Its four marks:

1. **Self-narration.** The text talked about the page, not the world:
   "Every place the edition records, each with its own page."
2. **Redundancy.** It restated what the heading and the list beneath
   already demonstrate - how many, in which documents, what kind.
3. **Explaining the obvious.** "each with its own page", "tap one to see
   what it means."
4. **A designed literary voice.** Dash-appended appositions and rhetorical
   triads ("its villages, hamlets and colonies, the market towns and seats
   around them").

The reference the editor gave for the wanted style renders no such text:
headings, lists, images; the structure explains itself.

## The standing rule

> The site speaks only to its reader about the materials. It does not
> mention the person who made them.

An explanation survives on a page only where it carries what the page
cannot show: how to use the site, or what the material is. Anything that
describes the page itself is removed.

## What stands (kept, 2026-10-28)

- **`browse_lede`** - the one line that says the full-text search runs
  over the German text. Unchanged.
- **`places_t1_lede`** - reworded away from the editor:
  English "Every place of the neighbourhood, whether or not it is named
  in the documents."; German "Jeder Ort der Gegend, ob in den Dokumenten
  genannt oder nicht."
- The home story (`home_lede`, `home_p1`-`home_p3`), the era notes of the
  timeline (`tl_era_note_*`), the view-mode hints (`hint_*`), the
  AI-translation caveats (`lit_caveat`, `np_caveat`), the cemetery
  bracket-number note (`cem_gid_note`), the glossary's German tags in the
  marks - all content or disclosure, not narration.
- The reading pages' standfirsts on the material itself: a holding's
  archive description, the Story page, rights, About.

## What went (deleted, 2026-10-28)

Both languages, keys in `site/_data/i18n.yml` and their render sites in
`site/_includes/`: `places_index_lede`, `places_t2_lede`, `gl_lede`,
`gl_draft_note`, `maps_lede`, `people_lede` (with the trailing
About-the-edition link; the footer links About twice already),
`timeline_lede`, `eras_lede`, `sources_lede`, `sources_arch_lede`,
`sources_np_lede`, `sources_lit_lede`, `sources_maps_lede` (the four
`sources_*_go` links stay under their headings), `lit_lede`, `np_lede`,
`cem_lede`, `places_cem_lede`, `card_browse_p`, `card_timeline_p`,
`card_people_p`, `card_about_p` - 21 keys a side. Dead CSS deleted:
`.gl-note` (assets/style.css), `.src-lede` (sources.html's inline style).

## Settled (the editor, 2026-10-28)

- `np_caveat_editor` now reads "The English translation is the one
  supplied with the transcription." (German: "Die englische Übersetzung
  ist die mit der Transkription gelieferte."); the key name stays.
- The ten cemetery pages' notes now open "From the survey of the
  Evangelical cemeteries" (`cemeteries/*/notes.md`); the rendered pages
  never carried the phrase.

## Worked

`build_site_data.py` (630 documents, archival lines exact), the Jekyll
build, and `verify_site.py` (63,056 internal links, no external
dependencies) all clean. In the built site, no deleted string appears
anywhere; the two kept lines render in both languages; the `.standfirst`
class remains only on texts about the material itself.
