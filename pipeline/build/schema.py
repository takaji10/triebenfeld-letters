# -*- coding: utf-8 -*-
"""The column lists the flat per-unit tables are written with.

Here, and not in build_db.py, because merge_corpus.py concatenates those tables
across holdings and has to know it is looking at the same shape. It used to take
the header from whichever unit it read first and write every other unit's rows
underneath it:

    header = header or h
    rows.extend(rd)

which is correct exactly as long as no two units ever disagree. Adding a field
and rebuilding one unit - `python regenerate.py --unit oe1bu9454` - leaves the
other unit's letters.csv on disk with the old columns, and the merge then writes
one holding's `text` under another holding's `is_missing`. No error, no warning,
and the damage is only visible if you happen to read the merged file.

So both sides import the list from here, and merge_corpus asserts the header it
reads against it. That turns "a schema change needs a full regenerate, not
--unit" from a procedure someone has to remember into one the build enforces.
"""

# One row per document. Pages are nested and so live only in letters.json.
DOCUMENT_FLAT_FIELDS = [
    'unit', 'uid', 'pad', 'permalink', 'letter_id', 'seq_archival',
    'parent_letter', 'doc_type', 'date_iso', 'date_precision', 'date_source',
    'date_display', 'date_inferred_from', 'year', 'month', 'day', 'place',
    'sender', 'recipient', 'line_start', 'line_end', 'uncertainty_count',
    'has_damage', 'duplicate_of', 'is_missing', 'n_lines', 'n_pages',
    'era',
    'text', 'text_reading',
]

# One row per manuscript page, for scan matching.
PAGE_FLAT_FIELDS = [
    'letter_id', 'page', 'line_start', 'line_end', 'n_lines', 'scan', 'reading',
]

FIELDS_BY_TABLE = {
    'letters.csv': DOCUMENT_FLAT_FIELDS,
    'pages.csv': PAGE_FLAT_FIELDS,
}
