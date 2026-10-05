# -*- coding: utf-8 -*-
"""APP 53/968/0/-/801 divided into three documents (editor, 2026-10-05).

    python units/app539680801/intake/split_documents.py            # check only
    python units/app539680801/intake/split_documents.py --write    # once

The holding was first built as one document, a deed package, and published
so. The editor then ruled that the three papers are three documents:

    1  the general power of attorney (pages 0036 to 0038)
    2  the consent of the chamber    (pages 0039 to 0041)
    3  the lease contract            (pages 0042 to 0051)

This script records how that was done. It puts [DOC 2] and [DOC 3] into
corpus.txt, rewrites the two copies of document_boundaries.csv, and re-keys
transcription_decisions.csv: each logged correction keeps its key and its
text and takes the document, the page within that document and the corpus
line it now has. corrections.py ran before the division and names every
correction under document 1; it is a record of what was changed and is not
to be run again.
"""
import csv
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, ROOT)
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SLUG = 'app539680801'
STARTS = {'0036_a': 1, '0039_a': 2, '0042_a': 3}      # first page -> document


def main():
    write = '--write' in sys.argv
    cp = os.path.join(UNIT_DIR, 'corpus.txt')
    old = io.open(cp, encoding='utf-8').read().split('\n')
    if sum(1 for l in old if l.startswith('[DOC ')) != 1:
        sys.exit('corpus.txt is not one document: already divided?')

    # the new corpus, and for every old line number its new place
    new, place = [], {}
    doc, page_in_doc = None, 0
    for i, l in enumerate(old):
        m = re.match(r'\[PAGE (\S+)\]', l)
        if l.startswith('[DOC '):
            continue
        if m and m.group(1) in STARTS:
            doc, page_in_doc = STARTS[m.group(1)], 0
            new.append(f'[DOC {doc}]')
        if m:
            page_in_doc += 1
        new.append(l)
        place[i + 1] = (doc, page_in_doc, len(new))
    if [l for l in new if not l.startswith('[DOC ')] != [l for l in old if not l.startswith('[DOC ')]:
        sys.exit('the text changed')

    dp = os.path.join(UNIT_DIR, 'transcription_decisions.csv')
    rows = list(csv.reader(io.open(dp, encoding='utf-8-sig', newline='')))
    head, rows = rows[0], rows[1:]
    out, count = [], {1: 0, 2: 0, 3: 0}
    for key, pad, page, a, b, decision, why in rows:
        m = re.match(r'@(\d+) ', decision)
        d, p, line = place[int(m.group(1))]
        if b not in new[line - 1]:
            sys.exit(f'{key}: the corrected text is not on line {line}')
        out.append([key, f'{SLUG}-{d:03d}', p, a, b, f'@{line} ' + decision[m.end():], why])
        count[d] += 1
    print(f'{len(new) - len(old) + 1} markers added; corrections by document: {count}')
    if not write:
        return

    io.open(cp, 'w', encoding='utf-8', newline='\n').write('\n'.join(new))
    with io.open(dp, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(head)
        w.writerows(out)
    for d in (unitlib.review_dir(SLUG), HERE):
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'document_boundaries.csv'), 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            w.writerow(['letter_id', 'first_page', 'first_line'])
            for page, n in STARTS.items():
                w.writerow([n, page, 1])
    print('written')


if __name__ == '__main__':
    main()
