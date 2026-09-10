# -*- coding: utf-8 -*-
"""
Scaffold a new archival unit.

    python new_unit.py oe1bu14525 --ref "Oe 1 Bü 14525" \
        --scans "C:/Users/Tersnaus/Downloads/Oe 1_Bue 14525"

Creates units/<slug>/ with unit.yml, an empty corpus.txt, an empty rulings.yml
and a notes.md to fill in. Nothing else in the project is touched; the pipeline
picks the unit up on the next run.

With --ref alone the slug is derived from it, so this also works:

    python new_unit.py --ref "Oe 1 U 199" --scans ".../Oe 1_U 199"
"""
import argparse
import io
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def guess_glob(scans_dir):
    """The filename pattern the images share, e.g. 'Oe 1_Bü 14525_*.jpg'.

    Archive exports are numbered <prefix>_NNNN.<ext>, so the prefix is whatever
    precedes the last underscore. Guessing beats making the user work it out,
    and unit.yml is there to correct it when the guess is wrong.
    """
    if not os.path.isdir(scans_dir):
        return None, None
    stems = Counter()
    exts = Counter()
    for fn in os.listdir(scans_dir):
        base, ext = os.path.splitext(fn)
        if ext.lower() not in ('.jpg', '.jpeg', '.png', '.tif', '.tiff', '.pdf'):
            continue
        exts[ext.lower()] += 1
        if '_' in base:
            stems[base.rsplit('_', 1)[0]] += 1
    if not stems:
        return None, (exts.most_common(1)[0][0] if exts else None)
    prefix, _ = stems.most_common(1)[0]
    ext = exts.most_common(1)[0][0]
    return f'{prefix}_*{ext}', ext


UNIT_YML = '''# One archival unit. Everything the pipeline needs to know about where this
# material came from and how its files are named.

slug: {slug}
ref: {ref}
archive: {archive}
title: >-
  TODO: what this unit contains, in a line or two.
date_span: TODO
status: draft              # draft | transcribed | translated | published

# Raw scans live outside the project. crop_scans.py reads from raw_dir and
# writes single pages into raw_dir/processed/.
scans:
  raw_dir: {raw_dir}
  raw_glob: {raw_glob}

  # Web derivatives are copied into site/assets/scans/ under an ASCII-safe
  # prefix, because source names carry spaces and umlauts. Later stages parse
  # this prefix, so it must not change once the unit is published.
  ascii_prefix: {ascii_prefix}

# The transcription. Documents are delimited by [DOC N] on its own line.
corpus: corpus.txt

# For the reader: shown on this unit's provenance page.
description: >-
  TODO: a sentence for the reader.
'''

RULINGS_YML = '''# Editorial rulings for {ref}.
#
# Keyed by the archive's own document number, which is what letter_id stays.
# Nothing here is derived: each entry is a decision taken against evidence and
# recorded so a rebuild reproduces it. Start empty and fill in from the review
# sheets in review/ as you work through them.

places:
  # Place of writing, where the dateline is absent, illegible or misleading.
  # A trailing [?] marks a reading that is probable rather than settled.
  #   "12": Berlin
  overrides: {{}}

dates:
  # [year, month, day, precision]; null where that element is unknown.
  #   "3": [1815, 2, 9, "day"]
  supplied: {{}}

  # Taken from the document's own duplicate.
  twin: {{}}

  # [year, month, day, precision, basis]; the basis is shown to the reader.
  inferred: {{}}

  # Undated and left so.
  no_date: []

documents:
  # Anything that is not an ordinary letter, e.g. "register".
  doc_type: {{}}

  # Same document, transcribed twice.
  duplicate_of: {{}}

  # Why a sub-record exists, shown on the document.
  split_note: {{}}

damage:
  # Damage is read from the text's own [...] markers. List document numbers
  # here only for damage the transcription does not mark.
  letters: []
'''

NOTES_MD = '''# {ref}

TODO: how many documents, how many pages, what date span.

## Provenance

{archive}. TODO: how many archival scans, how they were photographed, and what
the cropping produced.

## Transcription

TODO: how the text was produced, and what that means for reading it.

## Quirks worth knowing

TODO: numbering that is not chronological, bundled numbers, duplicates,
languages other than German, archival numbers with no surviving text.

## Damage

TODO, or "none recorded".
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('slug', nargs='?', help='short id, e.g. oe1bu14525; derived from --ref if omitted')
    ap.add_argument('--ref', required=True, help='archival reference, e.g. "Oe 1 Bü 14525"')
    ap.add_argument('--scans', default='', help='directory holding the raw scans')
    ap.add_argument('--archive', default='Hohenloher Zentralarchiv Neuenstein (HZAN)')
    a = ap.parse_args()

    slug = a.slug or unitlib.slugify(a.ref)
    if not slug.isalnum():
        raise SystemExit(f'slug must be alphanumeric: {slug!r}')

    dest = os.path.join(unitlib.UNITS_DIR, slug)
    if os.path.exists(dest):
        raise SystemExit(f'{dest} already exists')

    raw_glob, ext = guess_glob(a.scans)
    if a.scans and not os.path.isdir(a.scans):
        print(f'  note: {a.scans} does not exist yet; fix scans.raw_dir when it does')
    if raw_glob is None:
        raw_glob = 'TODO_*.jpg'
    elif ext == '.pdf':
        print('  note: this unit is PDFs. Export them to JPGs into the same')
        print('        folder before running crop_scans.py, and fix raw_glob.')

    os.makedirs(dest)
    fields = dict(slug=slug, ref=a.ref, archive=a.archive,
                  raw_dir=a.scans or 'TODO',
                  raw_glob=raw_glob,
                  ascii_prefix=unitlib.slugify(a.ref) if not a.scans else
                  raw_glob.rsplit('_*', 1)[0].replace(' ', '_')
                  .replace('ü', 'u').replace('ö', 'o').replace('ä', 'a'))
    write = {
        'unit.yml': UNIT_YML.format(**fields),
        'rulings.yml': RULINGS_YML.format(ref=a.ref),
        'notes.md': NOTES_MD.format(ref=a.ref, archive=a.archive),
        'corpus.txt': '',
    }
    for name, body in write.items():
        with open(os.path.join(dest, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(body)

    print(f'  created units/{slug}/')
    for name in write:
        print(f'    {name}')
    print()
    print('  Next:')
    print(f'    1. fill in the TODOs in units/{slug}/unit.yml')
    print(f'    2. python pipeline/intake/crop_scans.py --unit {slug}')
    print(f'    3. python pipeline/intake/split_spreads.py --unit {slug} --auto')
    print(f'    4. transcribe, and save to units/{slug}/corpus.txt')
    print(f'    5. python regenerate.py --unit {slug}')


if __name__ == '__main__':
    main()
