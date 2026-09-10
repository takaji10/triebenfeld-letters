# -*- coding: utf-8 -*-
"""
Rebuild everything from the transcriptions, in dependency order.

    python regenerate.py                     every transcribed unit
    python regenerate.py --unit oe1bu9454    one unit, then re-merge
    python regenerate.py --site              also build and verify the website

Editing a unit's corpus.txt shifts its line numbers, which invalidates that
unit's line-break decisions (they are keyed by line number), which changes the
page structure, which changes the scan mapping. So the per-unit order below is
not optional.

Nothing here writes to a corpus.txt or to the images: both are read-only inputs.
"""
import io
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))

# run once per unit, in this order
PER_UNIT = [
    ('pipeline/build/resolve_linebreaks.py', 'line-break decisions',
     're-derived because line numbers move when the corpus is edited'),
    ('pipeline/build/build_db.py', 'database, pages and reading copy',
     'corpus/units/<slug>/ - letters, pages, reading and chronological text'),
    ('pipeline/build/match_scans.py', 'scan mapping and reviewer',
     'page_scan_map.csv / scan_inventory.md / scan_review.html'),
]

# then once for the whole corpus
MERGED = [
    ('pipeline/build/merge_corpus.py', 'merge units',
     'corpus/letters.json and friends, every unit together'),
    # The dataset is built first: it writes the per-document files, and the
    # website and the verifier both read those rather than the merged array.
    ('pipeline/build/build_dataset.py', 'queryable dataset',
     'corpus/index/ and corpus/documents/ - what a research agent reads'),
    ('pipeline/build/build_site_data.py', 'website data',
     'site/_letters/ and the search index'),
]

# after the mapping is rebuilt: the label in each scan filename is derived from
# it, so it goes stale whenever pages move. Reporting is enough here - renaming
# is left as a deliberate act (relabel_scans.py --apply).
POST_UNIT = [('pipeline/build/relabel_scans.py', 'scan filename labels',
              'checks the -L<letter>_<page> labels still match the mapping')]

KEEP = ('documents/', 'text/', 'people ', 'places ', 'dates ', 'relations ',
        'uncertainty ', 'pages:', 'records:', 'VERIFY', 'transcript pages', 'images assigned',
        'images unassigned', 'accounting', 'no image used twice',
        'capture order', 'pages with no image', 'decisions:', 'confidence:',
        'captures ', 'wrote ', 'letter pages checked', 'manuscript pages',
        'archival lines exact', 'VERIFIED', 'MISMATCH', 'WARNING',
        'labels to update', 'nothing to do', 'merged:', 'skipped ', 'documents',
        'FAIL', 'ALL CHECKS', 'internal links', 'external resources')


def run(script, label, detail, unit=None):
    print(f'\n=== {label}{" - " + unit if unit else ""} ===')
    print(f'    {detail}')
    t = time.time()
    cmd = [sys.executable, '-u', os.path.join(ROOT, script)]
    if unit:
        cmd += ['--unit', unit]
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    out = (p.stdout or '') + (p.stderr or '')
    for line in out.splitlines():
        if any(k in line for k in KEEP):
            print('   ', line.strip())
    if p.returncode != 0:
        print(f'\n!! {script} failed (exit {p.returncode}). Full output:\n')
        print(out)
        sys.exit(p.returncode)
    print(f'    done in {time.time() - t:.0f}s')


def transcribed(u):
    """A unit with no text yet is scaffolding, not an error."""
    try:
        return os.path.getsize(u.corpus_path) > 0
    except OSError:
        return False


def main():
    only = unitlib.unit_arg()
    units = unitlib.load_units(only)

    ready = [u for u in units if transcribed(u)]
    waiting = [u for u in units if not transcribed(u)]
    for u in waiting:
        print(f'skipping {u.slug}: units/{u.slug}/corpus.txt is empty '
              f'(status: {u.get("status", "draft")})')
    if not ready:
        raise SystemExit('no transcribed unit to build')

    print('Regenerating: ' + ', '.join(u.slug for u in ready))
    # The pipeline's own checks run first: both mistakes they look for are
    # invisible until the output is wrong, and by then a build has already
    # written the wrong thing everywhere.
    run('pipeline/check_pipeline.py', 'pipeline self-check',
        'no holding named in code, no record keyed by the archive number')
    for u in ready:
        for script, label, detail in PER_UNIT:
            run(script, label, detail, unit=u.slug)

    for script, label, detail in MERGED:
        run(script, label, detail)

    for u in ready:
        for script, label, detail in POST_UNIT:
            run(script, label, detail, unit=u.slug)

    if '--site' in sys.argv:
        print('\n=== website ===')
        p = subprocess.run(['bundle', 'exec', 'jekyll', 'build'],
                           cwd=os.path.join(ROOT, 'site'), capture_output=True,
                           text=True, encoding='utf-8', errors='replace', shell=True)
        if p.returncode != 0:
            print((p.stdout or '') + (p.stderr or ''))
            sys.exit(p.returncode)
        print('    jekyll build ok')
        run('verify_site.py', 'website verification',
            'text fidelity and link integrity')

    print('\nAll done.')
    print('Review sheets are in review/<slug>/; open scan_review.html to check pairings.')


if __name__ == '__main__':
    main()
