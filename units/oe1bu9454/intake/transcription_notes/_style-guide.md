# Transcription Style Guide (draft — pending pilot review)

Diplomatic transcription: preserve original spelling, capitalization, and line breaks as written. Do not modernize orthography or punctuation.

## Frontmatter schema

```yaml
---
source_image: "Oe 1_Bü 9454_00NN.jpg"
crop_images: ["Oe 1_Bü 9454_00NN_a.jpg", "Oe 1_Bü 9454_00NN_b.jpg"]
date_original: "as written in the source, e.g. Wien d. 12ten Febr. 1815"
date_iso: "1815-02-12"          # null if undeterminable
place: "Wien"                     # null if not stated
sender: "..."                     # null if undeterminable
recipient: "..."                  # null if undeterminable
document_type: "Konzept"          # one of: Konzept (draft), Reinschrift (fair copy), unknown
archival_page_number: null        # the number penciled in the corner, if visible
has_table_or_figures: false
needs_review: false                # true if any [?] flags or arithmetic mismatch present
---
```

## Line and paragraph structure

- Each manuscript line becomes its own line in the Markdown body, ending with two trailing spaces (Markdown hard break), so the transcription's line breaks mirror the original.
- A blank line marks a paragraph break only where the manuscript itself shows one (new indented paragraph), not just a page-internal line wrap.

## Markup conventions

| Phenomenon | Convention | Example |
|---|---|---|
| Struck-through / deleted text | `~~text~~` | `~~Cosman~~` |
| Interlinear/marginal insertion by the author | `[+text+]` | `[+wieder+]` |
| Abbreviation, silently expanded | abbreviation as written, expansion in brackets immediately after | `Ew. [Euer]` |
| Uncertain reading | word or phrase followed by `[?]` | `Kalisch[?]` |
| Illegible passage | `[illegible]`, or `[illegible: ~N words]` if extent is estimable | `[illegible: ~3 words]` |
| Latin (or other non-German) insertions | rendered in *italics* to mark the language switch | *ex nexu* |
| Numbers/sums | see dedicated convention below — always treated as lower-confidence by default |

## Numbers and tables (high-risk — see plan for rationale)

- Reproduce any columnar/tabular material in the source as an actual Markdown table, not flattened into prose.
- Preserve the period's number formatting (e.g. `112000 fl`) rather than normalizing punctuation.
- Flag every transcribed number with `[?]` unless it is read with full confidence — numbers get more scrutiny than surrounding prose by default.
- If a document states a sum/total, verify it against itemized figures where possible. A mismatch is a strong signal of a misread digit; flag `needs_review: true` in frontmatter and note the discrepancy inline rather than silently reconciling it.

## Archival page numbers vs. dates

Some fair-copy pages carry a small penciled sequence number in the top corner (e.g. "2") — this is the archive's own pagination, distinct from the date written in the body/foot of the letter. Capture it as `archival_page_number` in frontmatter; do not confuse it with a date or folio citation.

## Open items to confirm during pilot review

- Confirm the insertion/deletion markup reads cleanly once the user sees real examples.
- Confirm whether superscript abbreviation letters (e.g. a raised "t" in "12ten") should be rendered plain or with `<sup>t</sup>`.
- Confirm date normalization rules for `date_iso` when the year is implied but not explicit on a given page.
