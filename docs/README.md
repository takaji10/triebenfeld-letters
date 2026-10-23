# What is in docs/

Two kinds of file, mixed together in one directory because the reports are
referenced from the changelog by path and moving them would break entries that
were true when they were written.

## Standing reference — the ones to read

| | |
|---|---|
| [DATA_MODEL.md](DATA_MODEL.md) | What is authored, what is generated, and the identifiers. Start here. |
| [EDITORIAL_RULES.md](EDITORIAL_RULES.md) | What may be corrected without asking, what never is, and the editor's standing rulings. |
| [NEW_UNIT.md](NEW_UNIT.md) | Taking a new holding from scans to published pages. |
| [HOUSE_STYLE.md](HOUSE_STYLE.md) | How everything written about the documents is written. The editor's standing rulings on prose. |
| [EDITORS_VOICE.md](EDITORS_VOICE.md) | The editor's own voice, from four samples of their writing (the fourth, index entries, with a brief of its own): an analysis and a two-paragraph brief, for a later reading of the site's prose. Where it differs from HOUSE_STYLE, the house style stands until the editor rules. |
| [DEPLOY.md](DEPLOY.md) | How the site is hosted and what blocks a deploy. |
| [NEEDS_CONFIRMATION.md](NEEDS_CONFIRMATION.md) | Open questions, still live. |
| [TODO.md](TODO.md) | The next steps, in order, and which of them wait on the editor. |
| [WORKING_NOTES.md](WORKING_NOTES.md) | How the editor works, the mistakes already made once, and the traps in the tools. The shared copy of what a desktop session keeps in memory, so a cloud session has it too. |
| [HOHENLOHE_ERA_PLAN.md](HOHENLOHE_ERA_PLAN.md) | The Hohenlohe-Ingelfingen years page: what goes in, its sections and their sources, and what a new holding changes. |
| [PRUSIMSKI_ERA_PLAN.md](PRUSIMSKI_ERA_PLAN.md) | The Prusimski era: the court books from Poznań still to add, how each is added, the spelling question, thoughts on the glossary. What the editor has decided and what waits on them. |
| [GLOSSARY_PLAN.md](GLOSSARY_PLAN.md) | The glossary page and the definitions in the documents: planned, not built. |
| [LITERATURE_PLAN.md](LITERATURE_PLAN.md) | The books and articles about the sources (`literature/`): kept apart from the archival documents, original and English page by page, for questions; which are shown on the site and how. |
| [NEWSPAPERS_PLAN.md](NEWSPAPERS_PLAN.md) | The items from the press (`newspapers/`): neither holdings nor literature, the editor's own section; how an item is read (OCR in the project), what is shown and what is open. |
| [PLACES_PLAN.md](PLACES_PLAN.md) | The place pages (`places/`): a page per place that has sources of its own, hung on its card on the Places page; how a source is brought in and shown. |
| [GAZETTEER_PLAN.md](GAZETTEER_PLAN.md) | The gazetteer (`reference/gazetteer/`): the editor's index of the places around Trąbczyn and Zagórów, its footnotes linked to the edition, the old maps (the labelling page, georeferencing), the dataset and the interactive map; the steps in order. |
| [MISSING_SOURCES.md](MISSING_SOURCES.md) | The running list of sources the edition cites and does not yet hold, for the editor to bring in; the gazetteer's part made by `pipeline/gazetteer/gazetteer.py --missing`. |
| [CHANGELOG.md](CHANGELOG.md) | What changed and why, in order. |

## Reports — a record of how something was settled

Each was written once, to answer one question, and is kept because the decision
it reached is still in force. None of them describes the current state of the
project.

| | |
|---|---|
| [collation_48_302.md](collation_48_302.md) | Two transcriptions of one letter, compared line by line. The basis for what the duplicate pairs are worth. |
| [currency_normalisation_report.md](currency_normalisation_report.md) | That the corpus obeys 1 Rthl = 24 g = 12 d exactly, which is what let inconsistent sums be resolved. |
| [transcription_error_profile.md](transcription_error_profile.md) | What machine transcription of Kurrent gets wrong, and how often. |
| [phase2_proper_noun_report.md](phase2_proper_noun_report.md) | The first pass over names. |
| [phase2b_transcription_audit.md](phase2b_transcription_audit.md) | The audit that followed it. |
| [name_decisions.md](name_decisions.md) | Which spelling was chosen for which name, with the reasoning. |
| [narrative_overview.md](narrative_overview.md) | A first-pass chapter skeleton of the correspondence. Its own header calls the connective narrative a draft to verify, not settled fact. |

Elsewhere: `reference/` holds the authorities the pipeline reads (people,
places, the termbase); `units/<slug>/` holds each holding's transcription and
its editorial rulings. Both are tracked and both are authored by hand.
