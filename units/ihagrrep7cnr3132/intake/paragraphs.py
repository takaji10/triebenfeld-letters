# -*- coding: utf-8 -*-
"""The paragraph breaks of I. HA GR, Rep. 7 C, Nr. 3132, set by hand (Claude, 2026-11-20).

    python units/ihagrrep7cnr3132/intake/paragraphs.py     # after a build has written paragraph_decisions.csv

The resolver's first pass was read row by row against the pages and set by
these principles, not put to the editor (WORKING_NOTES: "A list of rows to
rule on is not a deliverable"):
- each docket line at the head of a letter (number, "pr." date, date) is its
  own paragraph, and the body begins a new one;
- the dateline, each signature line and the address block begin paragraphs;
  the lines of one address ("An / des Königlichen ... / Excellenz") run
  together, as do two signatures written side by side (Goldbeck Haugwitz);
- in the office's slip each numbered instruction begins a paragraph, and the
  lines of one instruction run together;
- a line that continues a sentence runs on.
Each row is written with cue `hand` and confidence `held`, so that
resolve_paragraphs.py keeps it. Rows are found by document and the line's
own text (the start of it), not by corpus line number.
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
    ('1', 'Excellenz', 'run'),
    ('2', 'Nachdem die Regierung zu Posen', 'break'),
    ('2', 'des Königln. würkl.', 'run'),
    ('3', 'Jezierski', 'run'),
    ('3', 'Im völligen Einverständnis', 'break'),
    ('3', 'Berlin d 29 Apr', 'break'),
    ('4', 'Nachdem auf unsern', 'break'),
    ('4', 'des Königl. würkl.', 'run'),
    ('4', 'Excellenz', 'run'),
    ('4', 'Sr Exc v. Goldbeck depart', 'run'),
    ('4', '3. 4. notificirt', 'run'),
    ('4', 'v. Voss zur Mit', 'run'),
    ('5', 'Ew. Königl. Majestät haben', 'break'),
    ('5', 'welches wir jedoch', 'break'),
    ('5', 'Sr Königl: Majestät.', 'run'),
    ('6', 'die Staatsminister Großkanzler', 'run'),
    ('6', 'v. Goldbeck und Grafen', 'run'),
    ('7', 'Haugwitz', 'run'),
    ('7', 'die SüdPreußl. Regierung', 'run'),
    ('7', 'zu Posen', 'run'),
    ('8', 'v. Prusiemski und dem Xaver', 'run'),
    ('8', 'Haugwitz', 'run'),
    ('8', 'v. Prusiemski und den Xaver', 'run'),
    ('9', 'Da Sr. Königl. Majestät', 'break'),
    ('11', 'die Kammer', 'run'),
    ('11', 'zu Posen.', 'run'),
    ('11', 'zur gefälligen Mitzeichnung', 'break'),
    ('11', 'In der abschriftlichen Anlage', 'break'),
    ('11', 'Berlin den 30. May 1803.', 'break'),
    ('11', 'Haugwitz', 'run'),
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
    print(len(used), 'of', len(RULES), 'rules applied')


if __name__ == '__main__':
    main()
