# -*- coding: utf-8 -*-
"""
Chodyła (2015): the tables of english.md, made from the Polish ones.

    python literature/chodyla2015/make_english.py

english.md is Claude's English, written page by page from original.md
(notes.md). Its tables (Tab. 1, pp. 12-15; Tab. 2, pp. 89-91; Tab. 3a-c,
pp. 97-103) stand there as the marker "<!-- TABLE -->"; this script puts in
place of each marker the Polish table of the same page, in the same order,
with its words in English: the headers and remarks whole (CELLS), the names
by a few word rules (WORDS: "albo" is "or", a modern district's adjective is
the district's name). Figures, the names of places and the print's slips
("d0", "[ ]") are left as printed; "Chłocy" is given as "Boys [Chłocy, sic]". Run once; a marker that is
already replaced is not there to be found again.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

CELLS = {
    # Tab. 1
    'Lp.': 'No.',
    'Nazwy: powiatów, osad, parafii, gmin – historyczne i współczesne':
        'Names of districts, settlements, parishes, communes – historical and present',
    'Pyzdrski': 'Pyzdry', 'Koniński': 'Konin', 'Kaliski': 'Kalisz',
    'Dzisiejsze': 'Present', 'powiaty i gminy': 'districts and communes',
    'Parafie': 'Parishes',
    # Tab. 2
    'L.p.': 'No.',
    'Nazw osad według powiatów': 'Names of settlements by district',
    'Liczba i rodzaje dymów': 'Number and kinds of hearths',
    'Browary': 'Breweries', 'Karczmy': 'Inns', 'Chałupy': 'Cottages',
    'o 1 gospodarzu': 'with 1 farmer', 'o 2 gospodarzach': 'with 2 farmers',
    'ogrodowe': 'garden (smallholders\')',
    'ogrodowe bez gruntu i ogrodu': 'garden, without land and garden',
    'dymy rzemieślnicze i fabryczne': 'craftsmen\'s and manufacturing hearths',
    'razem wg tabel dymów lub szacunkowo[]': 'total by the tables of hearths, or estimated []',
    'dymy samorolne 1791 wg Tab. i szacunkowo[]': 'self-tilling hearths 1791 by the Tab., and estimated []',
    'Powiat pyzdrski': 'District of Pyzdry', 'Powiat koniński': 'District of Konin',
    'Powiat kaliski': 'District of Kalisz',
    'Razem': 'Total', 'Razem w trzech powiatach': 'Total in the three districts',
    # Tab. 3a and 3b
    'Nazwy osad alfabetycznie': 'Names of settlements in alphabetical order',
    'Liczebność mieszkańców według': 'Number of inhabitants by',
    'wg płci i wieku': 'by sex and age',
    'wg kategorii społeczno–zawodowych': 'by social and occupational category',
    'Ogółem, takze szac. wg liczby dymów[ ] z uwzględnienim płci iwyznania; także w 1791 r.':
        'Total, also estimated by the number of hearths [ ], with sex and confession; also in 1791',
    'Ogółem, także szac. wg liczby dymów[ ] z uwzględnienim płci':
        'Total, also estimated by the number of hearths [ ], with sex',
    'Gospodarze rolnicy': 'Farmers', 'Czynszownicy, chałupnicy': 'Rent-payers, cottagers',
    'Komornicy': 'Lodgers', 'Rzemieślnicy': 'Craftsmen',
    'Karczmarze, szynkarze': 'Innkeepers, tapsters', 'Czeladź, służący': 'Farm servants, servants',
    'Luźni za robotą': 'Luźni (hired workers)', 'Inni': 'Others',
    'Mężczyźni': 'Men', 'Synowie do l. 15 od l. 15': 'Sons: under 15; 15 and over',
    'Białogłowy': 'Women', 'Córki': 'Daughters',
    'prawdopodobnie razem z Lisewem dla którego wykazano 238 mieszkańców (126 M. i 112 Ż.)':
        'probably together with Lisewo, for which 238 inhabitants were recorded (126 M. and 112 Ż.)',
    '177 (89 M.,88 Ż.) w 1791 r. 111 kat. (40 M., 47 K., 10 Ch, ,14 Dz.) 50 M. 61 Ż.':
        '177 (89 M.,88 Ż.) in 1791 111 Cath. (40 M., 47 K., 10 Ch, ,14 Dz.) 50 M. 61 Ż.',
    '132 (73+ M.,59 Z) w 1791 r. 99 samych dysydentów (37 M., 35 K., 13 Ch., 14 Dz.) 50 M. 49 Z.':
        '132 (73+ M.,59 Z) in 1791 99 dissenters only (37 M., 35 K., 13 Ch., 14 Dz.) 50 M. 49 Z.',
    # Tab. 3c
    'Nazwy osad alfabetycznie wg powiatów pyzdrskiego, konińskiego i kaliskiego':
        'Names of settlements in alphabetical order by the districts of Pyzdry, Konin and Kalisz',
    'Liczebność mieszkańców': 'Number of inhabitants',
    'według wyznania płci i wieku': 'by confession, sex and age',
    'Ogółem, także szac. wg liczby dymów[ ] z uwzględnienim płci i wyznania':
        'Total, also estimated by the number of hearths [ ], with sex and confession',
    'Katolicy': 'Catholics', 'Dysydenci': 'Dissenters', 'Kobiety': 'Women',
    'Kobie-ty': 'Wo-men', 'Chłocy': 'Boys [Chłocy, sic]', 'Chłopcy': 'Boys', 'Dziewczęta': 'Girls',
    'prawdopodobnie razem z Trąbczyńskimi Nw. i St. Ol.':
        'probably together with the Trąbczyńskie Nw. and St. Ol.',
}

# the modern districts named in Tab. 1 by their adjectives
DISTRICTS = {'słupecki': 'Słupca', 'pleszewski': 'Pleszew', 'kaliski': 'Kalisz',
             'wrzesiński': 'Września', 'koniński': 'Konin', 'turecki': 'Turek'}
WORDS = [
    (r'\balbo\b', 'or'), (r'\bal\.', 'or'), (r'\bwzględnie\b', 'or'), (r'\blub\b', 'or'),
    (r'\bi\b', 'and'), (r'\bczęść\b', 'part of'), (r'\(część\)', '(part)'),
    (r'\bczęść Kolonii\b', 'part of Kolonia'), (r'\bos\. and kol\.', 'settlement and colony'),
    (r'\bz Olędrami\b', 'with the Olędry'),
]


def english_cell(inner):
    """The English of one cell's inner HTML."""
    m = re.fullmatch(r'(<b>)?(.*?)(</b>)?', inner, re.S)
    pre, text, post = m.group(1) or '', m.group(2), m.group(3) or ''
    if text in CELLS:
        return pre + CELLS[text] + post
    out = text
    for rx, rep in WORDS:
        out = re.sub(rx, rep, out)
    for adj, name in DISTRICTS.items():
        out = re.sub(rf'\b{adj}\b', name, out)
    return pre + out + post


def english_table(html):
    return re.sub(r'(<td[^>]*>)(.*?)(</td>)',
                  lambda m: m.group(1) + english_cell(m.group(2)) + m.group(3), html, flags=re.S)


def by_page(text):
    parts = re.split(r'^\[p\. ([^\]]+)\]$', text, flags=re.M)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def main():
    orig = io.open(os.path.join(HERE, 'original.md'), encoding='utf-8').read()
    path = os.path.join(HERE, 'english.md')
    eng = io.open(path, encoding='utf-8').read()
    tables = {k: re.findall(r'<table>.*?</table>', v, re.S) for k, v in by_page(orig).items()}
    parts = re.split(r'^(\[p\. [^\]]+\])$', eng, flags=re.M)
    done = 0
    for i in range(1, len(parts), 2):
        key = parts[i][4:-1]
        want = list(tables.get(key, []))
        body = parts[i + 1]
        n = body.count('<!-- TABLE -->')
        if n and n != len(want):
            sys.exit(f'p. {key}: {n} markers, {len(want)} tables')
        for t in want[:n]:
            body = body.replace('<!-- TABLE -->', english_table(t), 1)
            done += 1
        parts[i + 1] = body
    io.open(path, 'w', encoding='utf-8', newline='\n').write(''.join(parts))
    print('tables put in:', done)


if __name__ == '__main__':
    main()
