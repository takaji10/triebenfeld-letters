# -*- coding: utf-8 -*-
"""The editor's answers to the spot sheet of 2026-10-05, applied.

    python units/iharep162nr295/intake/spot_answers.py            # check only
    python units/iharep162nr295/intake/spot_answers.py --write    # once

Five readings were put to the editor against the page images
(open_queries.csv beside this file; the answers are in
review/iharep162nr295/query_answers.json, copied here as ANSWERS). Four stand
as transcribed; one figure changes. The change is made in corpus.txt and the
page file, logged in transcription_decisions.csv, and carried into the row of
paragraph_decisions.csv that is found by that line.
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
SLUG = 'iharep162nr295'

# key: (document, page image, as transcribed, the editor's answer)
ANSWERS = {
    'q01': (1, '0004_a', 'nachstehende', 'nachstehende'),
    'q02': (2, '0007_a', '3 gg.', '2 gg.'),
    'q03': (2, '0006_a', 'missarien', 'missarien'),
    'q04': (3, '0009_a', 'Kalischscher', 'Kalischscher'),
    'q05': (1, '0003_a', 'ihm', 'ihm'),
}
OLD, NEW = 'T. u. S. 2 rt. 3 gg.', 'T. u. S. 2 rt. 2 gg.'
PAGE_FILE = '0007_I_HA_Rep_162_Nr_295_0007_a.txt'


def swap(path, enc='utf-8'):
    s = io.open(path, encoding=enc, newline='').read()
    if s.count(OLD) != 1:
        sys.exit(f'{path}: found {s.count(OLD)} time(s)')
    return s.replace(OLD, NEW)


def main():
    write = '--write' in sys.argv
    cp = os.path.join(UNIT_DIR, 'corpus.txt')
    tp = os.path.join(UNIT_DIR, 'transcriptions', PAGE_FILE)
    pp = os.path.join(UNIT_DIR, 'paragraph_decisions.csv')
    new = {p: swap(p) for p in (cp, tp)}
    new[pp] = swap(pp, 'utf-8-sig')
    line = io.open(cp, encoding='utf-8').read().split('\n').index(OLD) + 1
    print(f'{sum(1 for v in ANSWERS.values() if v[2] != v[3])} of {len(ANSWERS)} answers change the text; corpus line {line}')
    if not write:
        return
    for p, s in new.items():
        io.open(p, 'w', encoding='utf-8-sig' if p == pp else 'utf-8', newline='').write(s)
    with io.open(os.path.join(UNIT_DIR, 'transcription_decisions.csv'), 'a', encoding='utf-8', newline='') as f:
        csv.writer(f).writerow(['spot-q02', f'{SLUG}-002', 3, '3 gg.', '2 gg.', f'@{line} {OLD} -> {NEW}',
                                'read on the page image by the editor, spot sheet of 2026-10-05: '
                                'the second figure of the fee note is a 2, like the first'])
    print('written and logged')


if __name__ == '__main__':
    main()
