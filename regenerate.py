# -*- coding: utf-8 -*-
"""
Rebuild everything from the canonical corpus, in dependency order.

Run this after editing von_Triebenfeld_Hohenlohe-Ingelfingen_cleaned.txt:

    python3 regenerate.py            # everything except the Jekyll build
    python3 regenerate.py --site     # also rebuild and verify the website

Editing the corpus shifts line numbers, which invalidates the line-break
decisions (they are keyed by line number), which changes the page structure,
which changes the scan mapping. So the order below is not optional.

Nothing here touches the corpus or the images - both are read-only inputs.
"""
import io, sys, os, subprocess, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))

STEPS = [
    ('pipeline/build/resolve_linebreaks.py', 'line-break decisions',
     're-derived because line numbers move when the corpus is edited'),
    ('pipeline/build/build_db.py', 'database, pages and reading copy',
     'letters.csv / letters.json / pages.csv / reading + chronological text'),
    ('pipeline/build/match_scans.py', 'scan mapping and reviewer',
     'page_scan_map.csv / scan_inventory.md / scan_review.html'),
    ('pipeline/build/build_site_data.py', 'website data',
     'site/_letters/ and the search index'),
]

# Run after the mapping is rebuilt: the label in each scan filename is derived
# from it, so it goes stale whenever pages move. Reporting is enough here -
# renaming is left as a deliberate act (relabel_scans.py --apply).
POST = [('pipeline/build/relabel_scans.py', 'scan filename labels',
         'checks the -L<letter>_<page> labels still match the mapping')]

KEEP = ('pages:', 'records:', 'VERIFY', 'transcript pages', 'images assigned',
        'images unassigned', 'accounting', 'no image used twice',
        'capture order', 'pages with no image', 'decisions:', 'confidence:',
        'captures ', 'wrote ', 'letter pages checked', 'manuscript pages',
        'archival lines exact', 'VERIFIED', 'MISMATCH', 'WARNING', 'labels to update', 'nothing to do',
        'FAIL', 'ALL CHECKS', 'internal links', 'external resources')


def run(script, label, detail):
    print(f'\n=== {label} ===')
    print(f'    {detail}')
    t = time.time()
    p = subprocess.run([sys.executable, '-u', os.path.join(ROOT, script)],
                       cwd=ROOT, capture_output=True, text=True,
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


def main():
    print('Regenerating from von_Triebenfeld_Hohenlohe-Ingelfingen_cleaned.txt')
    for script, label, detail in STEPS:
        run(script, label, detail)
    for script, label, detail in POST:
        run(script, label, detail)

    if '--site' in sys.argv:
        print('\n=== website ===')
        p = subprocess.run(['bundle', 'exec', 'jekyll', 'build'],
                           cwd=os.path.join(ROOT, 'site'), capture_output=True,
                           text=True, encoding='utf-8', errors='replace', shell=True)
        if p.returncode != 0:
            print((p.stdout or '') + (p.stderr or ''))
            sys.exit(p.returncode)
        print('    jekyll build ok')
        run('verify_site.py', 'website verification', 'text fidelity and link integrity')

    print('\nAll done. Reload scan_review.html in the browser.')
    print('Your anchors, front-matter marks and dropped images are kept;')
    print('page-level decisions reset when the page structure changes, and the')
    print('reviewer shows a banner saying so.')


if __name__ == '__main__':
    main()
