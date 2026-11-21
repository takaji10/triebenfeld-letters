# -*- coding: utf-8 -*-
"""The line ends of I. HA GR, Rep. 7 C, Nr. 421 the resolver split and Claude
joined by hand (2026-11-21): words broken at the line end with "¬" whose joined
form the resolver found in neither the corpus nor DWDS (old spellings, Latin,
Polish, a name). Two stay split, being two words with a stray mark: "allen¬ /
persönlichen" and "einer¬ / wider" (Mondro's "mit einer wider den Fiscum
angestellten Klage", as the clean copy writes it).

    python units/ihagrrep7cnr421/intake/linebreaks.py

Run after resolve_linebreaks.py; the rows are written `held`, so later runs
keep them (resolve_linebreaks carries a held row over by its two halves and
context).
"""
import csv
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(os.path.dirname(HERE), 'linebreak_decisions.csv')

# (head, tail): one word broken at the line end.
JOIN = {
    ('Ur', 'tel'), ('dies', 'fällige'), ('Perso', 'nalklagen'), ('Par', 'teyen'),
    ('De', 'signa'), ('Prin', 'zipien'), ('Re', 'visions'), ('Aller', 'höch'),
    ('Hau', 'länder'), ('Mier', 'zewo'), ('b', 'redet'), ('Ter', 'mino'),
    ('l', 'lich'), ('hab', 'h'), ('sub', 'stantiirt'), ('one', 'goż'),
    ('za', 'latwi'), ('wy', 'rażone'), ('kal', 'kulacyi'),
}
REASON = 'hand: a word broken at the line end (Claude, 2026-11-21)'


def main():
    rows = list(csv.DictReader(io.open(CSV, encoding='utf-8-sig', newline='')))
    cols = list(rows[0].keys())
    n = 0
    seen = set()
    for r in rows:
        k = (r['head'], r['tail'])
        if k in JOIN and r['mark'] == '¬':
            seen.add(k)
            if r['decision'] != 'join' or r['confidence'] != 'held':
                r['decision'], r['confidence'], r['reason'] = 'join', 'held', REASON
                n += 1
    missing = JOIN - seen
    if missing:
        raise SystemExit('not found: %s' % sorted(missing))
    with io.open(CSV, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    print('%d row(s) set to join by hand' % n)


if __name__ == '__main__':
    main()
