# -*- coding: utf-8 -*-
"""
Assemble corpus.txt from one-file-per-page transcriptions.

    python pipeline/intake/import_pages.py --unit oe1bu14526 \
        --boundaries review/oe1bu14526/document_boundaries.csv
    python pipeline/intake/import_pages.py --unit oe1bu14526 --pages-only
    python pipeline/intake/import_pages.py --unit oe1bu14526 --list

Where a source arrives with its transcriptions already matched to its scans,
that pairing is evidence and should be written down, not reconstructed later by
walking two lists in parallel and hoping they stay in step. So each page's text
is preceded by a marker naming the manuscript page it was read from:

    [DOC 7]
    [PAGE 0011_a1]
    Gremcholz hat der Herr Kaufer fuer sein ganzes
    ...
    [PAGE 0011_a2]
    ...

The page id is the capture and crop from the image filename. It is the page's
archival identity and never changes; the -L<doc>_<page> label a file may pick up
later is derived from the mapping and is deliberately not part of it.

The boundaries file says where each document starts. Columns:

    letter_id    the archival number this document takes
    first_page   page id it opens on            e.g. 0009_b
    first_line   1-based line within that page, when a document starts partway
                 down one. Optional, defaults to 1.

Any other columns are ignored, so the same sheet can carry doc_type, dates and
notes for the editor's use. Pages before the first document become front matter,
which is what the title page of a volume is.

corpus.txt is the canonical hand-edited input everywhere else in the project, so
this refuses to overwrite a non-empty one without --force. It is meant to run
once.
"""
import argparse
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def page_id_of(filename, strip):
    """'0016_Oe 1_Bue 14526_0011_a1.txt' -> '0011_a1'."""
    stem = os.path.splitext(filename)[0]
    if strip and strip in stem:
        stem = stem.split(strip, 1)[1]
    return stem


def load_sources(unit):
    """[(page_id, [line, ...]), ...] in filename order."""
    d = unit.transcriptions_dir
    if not d:
        raise SystemExit(f'{unit.slug}: unit.yml declares no transcriptions: block')
    if not os.path.isdir(d):
        raise SystemExit(f'{unit.slug}: no transcriptions directory at {d}')
    ext = os.path.splitext(unit.transcriptions_glob)[1] or '.txt'
    names = sorted(f for f in os.listdir(d) if f.lower().endswith(ext))
    if not names:
        raise SystemExit(f'{unit.slug}: no {ext} files in {d}')

    out, seen = [], {}
    for n in names:
        pid = page_id_of(n, unit.page_id_strip)
        if pid in seen:
            raise SystemExit(f'{unit.slug}: two files claim page {pid!r}: '
                             f'{seen[pid]} and {n}')
        seen[pid] = n
        with open(os.path.join(d, n), encoding='utf-8') as f:
            text = f.read()
        lines = [l.rstrip('\r') for l in text.split('\n')]
        while lines and not lines[-1].strip():
            lines.pop()
        out.append((pid, lines))
    return out


def load_boundaries(path, known):
    """[(letter_id, first_page, first_line), ...] in source order."""
    with open(path, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit(f'{path}: no rows')
    need = {'letter_id', 'first_page'}
    missing = need - set(rows[0])
    if missing:
        raise SystemExit(f'{path}: missing column(s): {sorted(missing)}')

    order = {pid: i for i, pid in enumerate(known)}
    out = []
    for r in rows:
        lid = (r['letter_id'] or '').strip()
        pid = (r['first_page'] or '').strip()
        if not lid or not pid:
            continue
        if pid not in order:
            raise SystemExit(f'{path}: document {lid} opens on page {pid!r}, '
                             f'which is not among the transcriptions')
        line = (r.get('first_line') or '1').strip() or '1'
        out.append((lid, pid, int(line)))

    dupes = [l for l in {x[0] for x in out} if sum(1 for y in out if y[0] == l) > 1]
    if dupes:
        raise SystemExit(f'{path}: document number used twice: {sorted(dupes)[:5]}')
    out.sort(key=lambda t: (order[t[1]], t[2]))
    return out


def assemble(sources, bounds):
    """The corpus text, plus a count of documents and pages emitted."""
    # start-of-document markers, keyed by where they fall
    starts = {}
    for lid, pid, line in bounds:
        starts.setdefault((pid, line), []).append(lid)

    out = []
    n_pages = 0
    for pid, lines in sources:
        # A page can carry the end of one document and the start of the next, so
        # every split point on this page is handled in order and the page id is
        # repeated for each part. Both parts really were read off this image.
        cuts = sorted(k[1] for k in starts if k[0] == pid)
        segments = []
        prev = 1
        for c in cuts:
            if c > prev:
                segments.append((prev, lines[prev - 1:c - 1]))
            prev = c
        segments.append((prev, lines[prev - 1:]))

        for start_line, seg in segments:
            for lid in starts.get((pid, start_line), []):
                out.append(f'[DOC {lid}]')
            if not [l for l in seg if l.strip()]:
                continue
            out.append(f'[PAGE {pid}]')
            out.extend(seg)
            n_pages += 1
    return '\n'.join(out) + '\n', len(bounds), n_pages


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--boundaries', metavar='PATH', help='CSV saying where each document starts')
    ap.add_argument('--pages-only', action='store_true',
                    help='no document tags; every page in one undivided run')
    ap.add_argument('--list', action='store_true',
                    help='print the page ids in order and stop')
    ap.add_argument('--force', action='store_true', help='overwrite a non-empty corpus.txt')
    ap.add_argument('--dry-run', action='store_true', help='report only; write nothing')
    a = ap.parse_args()

    unit = unitlib.one_unit(a.unit)
    sources = load_sources(unit)
    print(f'{unit.slug}: {len(sources)} transcription file(s)')

    if a.list:
        for pid, lines in sources:
            head = next((l for l in lines if l.strip()), '')
            print(f'  {pid:12s} {len(lines):3d} lines  {head[:64]}')
        return

    if a.boundaries:
        path = a.boundaries if os.path.isabs(a.boundaries) else os.path.join(ROOT, a.boundaries)
        bounds = load_boundaries(path, [p for p, _ in sources])
    elif a.pages_only:
        bounds = []
    else:
        raise SystemExit('pass --boundaries PATH, or --pages-only to import '
                         'the pages before the documents have been settled')

    text, n_docs, n_pages = assemble(sources, bounds)

    # Nothing may be lost in the crossing. The corpus must hold every non-blank
    # line of every source file, in order, and nothing else.
    src_lines = [l.strip() for _, ls in sources for l in ls if l.strip()]
    got = [l.strip() for l in text.split('\n')
           if l.strip() and not l.startswith(('[DOC ', '[PAGE '))]
    if src_lines != got:
        raise SystemExit(f'import would not be lossless: {len(src_lines)} source '
                         f'lines vs {len(got)} in the corpus - refusing to write')

    print(f'  documents : {n_docs}')
    print(f'  pages     : {n_pages}')
    print(f'  lines     : {len(src_lines)} carried across, none lost')

    out = unit.corpus_path
    if os.path.isfile(out) and os.path.getsize(out) > 0 and not a.force:
        raise SystemExit(f'{out} is not empty. It is the canonical transcription '
                         f'and is hand-edited from here on - pass --force only if '
                         f'you really mean to replace it.')
    if a.dry_run:
        print('\ndry run - nothing was written')
        return
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print(f'\nwrote {out}')
    print(f'next: python regenerate.py --unit {unit.slug}')


if __name__ == '__main__':
    main()
