# -*- coding: utf-8 -*-
"""The paragraph breaks of I. HA GR, Rep. 7 C, Nr. 421, set by hand (Claude, 2026-11-21).

    python units/ihagrrep7cnr421/intake/paragraphs.py     # after a build has written paragraph_decisions.csv

The resolver's first pass was read row by row against the pages and set by
these principles, as for Nr. 3132 (WORKING_NOTES: "A list of rows to rule on is
not a deliverable"):
- the salutation, the dateline, the body, each signature and the address block
  begin paragraphs; a heading of several lines ("Klage des Stanisl. von Chełmski
  auf Łukom bei Peysern ./. den Starosten ... ex Chirographo"; "auf das
  Vorstellen ... in Sachen seiner ./. Prusimski") runs together as one;
- a signature and what belongs to it run together ("Antoni Prusimski / S. N.
  Mpp", "Jakub Bieńkowski / przytomny Przyiaciół");
- the office's block in the margin of document 1 ends before the petition's
  salutation; a copy's heading "Copia" stands apart from the text;
- a line that continues a sentence runs on.
Each row is written with cue `hand` and confidence `held`, so that
resolve_paragraphs.py keeps it. Rows are found by document and the line's own
text (the start of it), not by corpus line number.
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
PATH = os.path.join(UNIT_DIR, 'paragraph_decisions.csv')

# (document, start of the line, decision)
RULES = [
    ('1', 'Allerdurchläuchtigstr Großmächtigstr', 'break'),   # after the office's block
    ('1', 'werde der von Pru', 'run'),
    ('1', 'nicht beruhigen kann,', 'run'),
    ('1', 'confiscirten Vermö', 'run'),
    ('1', 'sollen, daß jedoch', 'run'),
    ('2', 'auf das Vorstellen des v Chełmski', 'break'),
    ('2', 'seiner ./. Prusimski:', 'run'),
    ('2', 'von Chełmski ./. Prusimski.', 'run'),
    ('2', 'dem[?] K[r?]. R. Mondro.', 'run'),
    ('3', 'für den Stanislaus von Chełmski,', 'run'),
    ('3', 'v. Prusimski.)', 'run'),
    ('3', 'c. lediglich sein Bewenden', 'run'),
    ('4', 'den Fiscum wegen', 'run'),
    ('4', 'M[?]. mit selbigen', 'run'),
    ('4', '12,000. ## einge', 'run'),
    ('4', 'Allerhöchst dieselben wie', 'run'),
    ('4', 'sollte.', 'run'),
    ('5', 'Bereits unter dem 9ten Octbr.', 'break'),
    ('5', 'Allerhöchstdieselben wiederholenlich', 'run'),
    ('6', 'Łukom bei Peysern', 'run'),
    ('6', './.', 'run'),
    ('6', 'den Starosten', 'run'),
    ('6', 'Anton v Prusimski', 'run'),
    ('6', 'auf Trąmpczyn', 'run'),
    ('6', 'wegen 12000 #.', 'run'),
    ('6', 'ex Chirographo.', 'run'),
    ('6', 'Term. instr. anzusagen', 'run'),
    ('6', 'Nizey wyrazony Blankiet', 'break'),
    ('6', 'S[tarosta]. N[ieszczewicki]. Mpp', 'run'),
    ('6', 'przytomny Przyiaciół', 'run'),
    ('7', 'c. Fiscum betr:)', 'run'),
]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    rows = list(csv.DictReader(io.open(PATH, encoding='utf-8-sig')))
    fields = list(rows[0].keys())
    used = set()
    for r in rows:
        for k, (doc, start, dec) in enumerate(RULES):
            if r['letter'] == doc and r['context'].startswith(start):
                r['decision'], r['confidence'], r['cue'] = dec, 'held', 'hand'
                used.add(k)
    missing = [RULES[k] for k in range(len(RULES)) if k not in used]
    for m in missing:
        print('not found:', m)
    with io.open(PATH, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    left = sum(1 for r in rows if r['confidence'] == 'review')
    print(len(used), 'of', len(RULES), 'rules applied;', left, 'rows left for review')
    if missing:
        sys.exit(1)


if __name__ == '__main__':
    main()
