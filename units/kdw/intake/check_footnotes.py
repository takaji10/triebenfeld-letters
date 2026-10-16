# -*- coding: utf-8 -*-
"""Check units/kdw/footnotes.yml against the corpus.

    python units/kdw/intake/check_footnotes.py

Every marker's piece of text (braces taken out) occurs exactly once in its
document; every note's beginning begins exactly one line of it; every marker
has a note and every note a marker, but for those listed under `unmatched`.
Labels may be ranges ("5-6", "b-c"): a range note answers each label in it,
and a range marker is answered by the range note.
"""
import io
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(HERE)


def docs():
    out, cur = {}, None
    for line in io.open(os.path.join(UNIT, 'corpus.txt'), encoding='utf-8').read().split('\n'):
        m = re.match(r'^\[DOC (\S+)\]$', line)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur and line.strip() and not line.startswith('[PAGE '):
            out[cur].append(line)
    return out


def label(piece):
    m = re.search(r'\{([^}]*)\}', piece)
    assert m, piece
    return m.group(1), piece.replace('{', '').replace('}', '')


def expand(lab):
    lab = lab.rstrip(')')
    m = re.match(r'^(\w+)-(\w+)$', lab)
    if not m:
        return {lab}
    a, b = m.groups()
    if a.isdigit() and b.isdigit():
        return {str(i) for i in range(int(a), int(b) + 1)}
    return {chr(c) for c in range(ord(a), ord(b) + 1)}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    spec = yaml.safe_load(io.open(os.path.join(UNIT, 'footnotes.yml'), encoding='utf-8'))
    text = docs()
    bad = 0
    for lid, d in spec.items():
        lines = text[str(lid)]
        whole = '\n'.join(lines)
        mk, nt = set(), set()
        for piece in d.get('markers') or []:
            lab, raw = label(piece)
            n = whole.count(raw)
            if n != 1:
                print('doc %s: marker %r found %d times' % (lid, piece, n))
                bad += 1
            mk |= expand(lab)
        for piece in d.get('notes') or []:
            lab, raw = label(piece)
            n = sum(1 for l in lines if l.startswith(raw))
            if n != 1:
                print('doc %s: note %r begins %d lines' % (lid, piece, n))
                bad += 1
            nt |= expand(lab)
        unmatched = {str(k) for k in (d.get('unmatched') or {})}
        for lab in sorted((mk ^ nt) - unmatched):
            print('doc %s: %s has %s' % (lid, lab, 'no note' if lab in mk else 'no marker'))
            bad += 1
    print('footnotes:', sum(len(d.get('markers') or []) for d in spec.values()), 'markers,',
          sum(len(d.get('notes') or []) for d in spec.values()), 'notes,', bad, 'problems')
    return bad


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
