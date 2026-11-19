# -*- coding: utf-8 -*-
"""The English of the list of the condemned as a table, row for row the shape
of the German (intake/table.csv, build_pages.py TABLE), written into pages 5
and 6 of doc1.yml (the list was document 3 until the editor made the file one
document, 2026-11-19; PAGES below keep the list's own page numbers 2 and 3; its title page,
page 4 of the document, is text since the same day and not written here). 2026-11-19, when the list became a table; the words are those
of the line-by-line English it replaces.

    python units/ihagrrep7cnr3067/intake/translation/doc3_table.py
"""
import csv
import io
import os

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = ['Number', 'Names', 'Nature of the crime', 'Length of the sentence', 'Its beginning']
SAME = 'For especially active participation in the insurrection'

PAGES = {
    2: [
        HEAD,
        ['', 'A. Death sentence.', '', '', ''],
        ['1,', 'Franz von Wittwicki,', "Because at the attack on the town of Włocławek they led "
         "the canons' servants against the military, and also murdered an officer and an "
         'excise official.', '', ''],
        ['2,', 'Andreas Retznowski,', '', '', ''],
        ['', 'B. Lifelong fortress imprisonment.', '', '', ''],
        ['1,', 'Joseph von Stockowski,', 'Because he was general of the insurgents of Wieluń, '
         'led them against the royal troops, robbed magazines and plundered treasuries.', '', ''],
        ['2,', 'Joseph Nowicki,', 'Was sentenced to the gallows, because he was especially '
         'active in the seizure of the artillery transport at Włocławek and mortally injured '
         'several people in it; but has been pardoned by His Royal Majesty.', '', ''],
        ['3,', 'Joseph Sobolewski,', 'Because after the dissolution of the insurrection he '
         'joined a band of robbers and helped in murders of soldiers and travellers.', '', ''],
        ['', 'C. Long fortress imprisonment', '', '', ''],
        ['1,', 'Johann Thiele', "Because he showed himself especially active as secretary at "
         "the insurgents' Commission of Order and War", '4 years', 'February 1795'],
        ['2,', 'Nicolaus von Psarski', SAME, '8 years', 'March 1795'],
        ['3,', 'Johann von Pistrzkowski', 'The same', '8 years', 'March 1795'],
        ['4,', 'Johann von Dobski', 'The same', '10 years', 'March 1795'],
        ['5,', 'Provost von Chicomski', 'For abuse of his spiritual office to promote the '
         'insurrection', '10 years', 'July 1795'],
        ['6,', 'Vincent von Magnuski', 'Because he probably finished off a dragoon who was '
         'already wounded.', '4 years', 'August 1795'],
        ['7,', 'Casimir von Pratzmowski', 'For especially active participation in the '
         'insurrection and highway robbery committed', '15 years', 'August 1795'],
        ['8,', 'Johann von Dobrski', 'Because, during his flight from the insurgents, he '
         'mortally wounded a hussar who wanted to examine him', '10 years', 'August 1795'],
        ['9,', 'Joseph von Psarski', SAME, '6 years', 'September 1795'],
    ],
    3: [
        HEAD[:4] + ['Its beginning.'],
        ['10,', 'Lorenz von Masowiecki', 'Because he took part in the attack on the town of '
         'Rypin by the insurgents', '4 years', 'October 1795'],
        ['11,', 'Dominic v. Dziewanowski', 'For the same reason', '4 years', 'October 1795'],
        ['12,', 'von Ryczewski', 'Because after the dissolution of the insurrection he joined '
         'a band of robbers and took part in various robberies.', '15 years', 'October 1795'],
        ['13,', 'von Maruczewski', 'For the same reason', '8 years', 'October 1795'],
        ['14,', 'Komornick von Wardenski', 'Because he is strongly suspected of having known '
         'of the insurrection beforehand.', '4 years', 'December 1795'],
        ['15,', 'Casimir von Lenartowicz', 'For especially active participation', '6 years',
         'December 1795'],
        ['16,', 'Felix von Krettkowski', 'Because, though not entirely of his own free will, '
         'he became general of the insurgents of Łęczyca', '6 years -', 'December 1795'],
        ['17,', 'Valentin von Zaburowski', 'For especially active participation', '4 years',
         'December 1795'],
        ['18,', 'Stephan von Pilchowski', 'The same, and for plundering committed.', '8 years',
         'January 1796'],
        ['19,', 'Paul von Skorzewski', 'General of the insurgents of Kalisz', '6 years',
         'January 1796'],
        ['20,', 'Samuel Czimay', 'Because they took an active part in the attack on the '
         'garrison at Włocławek.', '4 years', 'March 1796'],
        ['21,', 'Szekus Ruba', '', '4 years', ''],
        ['22,', 'Johann Michalleck', 'For participation in the insurrection and plundering '
         'committed', '4 years', 'May 1796'],
        ['23,', 'Cajetan von Smolinski', 'For abuse of his spiritual office to promote the '
         'insurgents.', '4 years', 'May 1796'],
        ['24,', 'Friedrich Jacob v. Psarski', 'Because he was president of the confederation '
         'of Wieluń and and Ostrzewo.', '10 years', 'May 1796'],
        ['25,', 'Constantin v. Mielewski', 'For participation in the insurrection and '
         'suspicion of the murder of a Jew', '7 years', 'June 1796'],
        ['26,', 'Chrisolog v. Rogoczynski', 'For particularly active participation in the '
         'insurrection', '4 years', 'November 1796'],
    ],
}


def csv_text(rows):
    buf = io.StringIO()
    csv.writer(buf, lineterminator='\n').writerows(rows)
    return buf.getvalue().rstrip('\n')


def block(dumper, data):
    style = '|' if '\n' in data else None
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style=style)


yaml.SafeDumper.add_representer(str, block)


def main():
    p = os.path.join(HERE, 'doc1.yml')
    d = yaml.safe_load(io.open(p, encoding='utf-8'))
    for pg in d['pages']:
        if pg['page'] < 5:
            continue
        pg['en'] = csv_text(PAGES[pg['page'] - 3])
        for f in pg.get('flagged') or []:
            f['de'] = f['de'].replace('Krieg¬ Commission', 'Krieg¬Commission')
            f['de'] = f['de'].replace('Wielun und / und Ostrzewo', 'Wielun und und Ostrzewo')
            f['rendered_as'] = f['rendered_as'].replace('Wieluń and / and Ostrzewo',
                                                        'Wieluń and and Ostrzewo')
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        yaml.safe_dump(d, f, allow_unicode=True, sort_keys=False, width=100)
    print('wrote', p)


if __name__ == '__main__':
    main()
