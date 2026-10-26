# -*- coding: utf-8 -*-
"""The before/after check of the table_of extension for a table with no entry
number column (APP 53/21/0/-/Pyzdry Gr.115, 2026-10-26).

Mistake 9 of docs/NEW_UNIT.md: before shared code is changed, the "before" is
taken from the pristine version and diffed against the new output. This runs
both over every document that rulings.yml lists under `tables:` in every unit
and asserts the two agree exactly. The extension only fires where no row has a
number in its first cell, which no existing table has - so every difference it
prints is a defect of the change, and a clean run is the proof the change is
safe to build on.

    python pipeline/review/verify_table_of_diff.py
"""
import csv
import importlib.util
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
import unitlib as NEW            # the worktree's changed version
import yaml

# the pristine version, from HEAD, under another name
pristine_src = subprocess.run(
    ['git', '-C', ROOT, 'show', 'HEAD:unitlib.py'],
    capture_output=True, text=True, encoding='utf-8', check=True).stdout
p = os.path.join(os.environ.get('TEMP', os.path.join(ROOT, 'scratch')),
                 'unitlib_pristine_tableof.py')
with io.open(p, 'w', encoding='utf-8', newline='\n') as f:
    f.write(pristine_src)
spec = importlib.util.spec_from_file_location('unitlib_pristine', p)
OLD = importlib.util.module_from_spec(spec)
spec.loader.exec_module(OLD)

UNITS = os.path.join(ROOT, 'units')
n_docs = n_units = 0
for slug in sorted(os.listdir(UNITS)):
    d = os.path.join(UNITS, slug)
    rulings_path = os.path.join(d, 'rulings.yml')
    corpus_path = os.path.join(d, 'corpus.txt')
    if not os.path.isfile(rulings_path) or not os.path.isfile(corpus_path):
        continue
    if slug == 'app5321pyzdrygr115':
        continue        # the holding the extension is for: no behaviour before it
    rulings = yaml.safe_load(io.open(rulings_path, encoding='utf-8')) or {}
    tables = ((rulings.get('documents') or {}).get('tables')) or []
    if not tables:
        continue
    n_units += 1
    wanted = {str(t) for t in tables}
    doc_pages, lid = {}, None
    for line in io.open(corpus_path, encoding='utf-8').read().split('\n'):
        m = re.match(r'^\[DOC (\d+)\]$', line)
        if m:
            lid = m.group(1) if m.group(1) in wanted else None
            if lid:
                doc_pages[lid] = []
            continue
        if lid is None:
            continue
        if line.startswith('[PAGE '):
            doc_pages[lid].append([])
        elif line.strip() and doc_pages[lid]:
            doc_pages[lid][-1].append(line)
    for lid, plines in doc_pages.items():
        page_lines = {i: ls for i, ls in enumerate(plines, 1) if ls}
        a, b = OLD.table_of(page_lines), NEW.table_of(page_lines)
        n_docs += 1
        if a != b:
            print(f'DIFFERS: {slug} doc {lid}')
            for k in a:
                if a.get(k) != b.get(k):
                    print(f'  {k}:')
                    print(f'    old: {a.get(k)!r}'[:400])
                    print(f'    new: {b.get(k)!r}'[:400])
            sys.exit(1)
        # and the rendering of every page of the table, old against new
        for pg in NEW.table_page_numbers(b):
            ra, rb = OLD.render_table(a, pg), NEW.render_table(b, pg)
            if ra != rb:
                print(f'DIFFERS (render): {slug} doc {lid} page {pg}')
                for i in range(min(len(ra), len(rb))):
                    if ra[i] != rb[i]:
                        print(f'   old: {ra[i:i + 200]!r}')
                        print(f'   new: {rb[i:i + 200]!r}')
                        break
                sys.exit(1)

# and the new table over the numberless table itself, as a smoke test
import csv as _csv
rows = ['Parofie,Nazwiska Miast WsiÃ³w FolwarkÃ³w,Dymy rolne,gara zyta,gara owcza',
        'TrÄ…bczyn,Wies TrÄ…bczyn,21,22,84',
        ',Plebania,4,8,16',
        ',Kuznia MaryantÃ³w,1,2,4']
parsed = [next(_csv.reader([r])) for r in rows]
t = NEW.table_of({1: rows})
assert t['head'] == parsed[:1], t['head']
assert t['pages'][1] == parsed[1:], t['pages']
assert t['foot'] == [] and t['caption'] == ''
print(f'{n_docs} table documents in {n_units} units: old and new agree; '
      f'the numberless table sorts into head + {len(t["pages"][1])} rows')
