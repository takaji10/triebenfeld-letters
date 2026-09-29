# -*- coding: utf-8 -*-
"""Print letters with both line numbers.

    python pipeline/review/show_letter.py --unit oe1bu9454 215 72e

Each line is printed as

    <corpus line> | <letter line> | text

The corpus line is what fix_sheet.py and apply_transcription_fixes.py take.
The letter line is the number the site shows beside the text, and the one to
use when pointing the editor at a passage. [DOC] and [PAGE] markers and blank
lines have no letter line.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, os, re, sys, argparse
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', required=True)
    ap.add_argument('letters', nargs='+')
    a = ap.parse_args()
    u = unitlib.one_unit(a.unit)
    want = set(a.letters)
    cur = None; n = 0
    for i, l in enumerate(open(os.path.join(u.dir, 'corpus.txt'), encoding='utf-8').read().split('\n'), 1):
        m = re.match(r'\[DOC (\S+)\]', l)
        if m:
            cur = m.group(1); n = 0
        s = l.strip()
        if s and not s.startswith('[DOC ') and not s.startswith('[PAGE '):
            n += 1; ll = str(n)
        else:
            ll = ''
        if cur in want:
            print(f'{i:5}|{ll:>3}| {l}')


if __name__ == '__main__':
    main()
