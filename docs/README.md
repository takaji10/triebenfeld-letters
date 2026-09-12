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
| [DEPLOY.md](DEPLOY.md) | How the site is hosted and what blocks a deploy. |
| [NEEDS_CONFIRMATION.md](NEEDS_CONFIRMATION.md) | Open questions, still live. |
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
