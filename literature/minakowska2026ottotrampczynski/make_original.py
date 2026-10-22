# -*- coding: utf-8 -*-
"""Make original.md and full.md of minakowska2026ottotrampczynski from the
editor's saved page.

The source is the editor's file "Wojciech Otto-Trampczynski (M.J. Minakowska,
Genealogia potomkow Sejmu Wielkiego).htm" (Downloads, 2026-10-22): person
sw.35437 of M. J. Minakowska's database
(https://www.sejm-wielki.pl/b/sw.35437), the page itself citing "wydanie z
22.10.2026". The page is not kept in the repository: its header carries the
editor's login, and its footer the visitor's IP address.

The page is written in ISO-8859-2 (latin2) and is the database's Polish user
interface, as the first and third of these works were; the work's language
is therefore `pl`, with the English beside it. A short page: the subject is
of the sixteenth century, the database gives him no biography, no parents,
no ancestor tree and no siblings - only the marriage and the descent, the
nearest PSB persons, and the Uwagi, whose one line is the Teki Dworzaczka
regest of the Konin-region record of 1614 that names him and his son
Stanisław. Two files are made (docs/LITERATURE_PLAN.md, section 22):

  full.md      the knowledgebase: the whole page in reading order - the
               biographical line, Śluby i dzieci, wnuki, i do prawnuków,
               Najbliżsi sławni ludzie, and Uwagi with the Teki Dworzaczka
               regest of 1614 (Księgi grodzkie pyzdrskie, cz. 1, nr 2152,
               Nr 137: Stanisław Trąmpczyński, son of Wojciech Otha
               Trąmpczyński, pledges half the estates to Jan Słonecki for
               7,000 zł as the dowry of Anna Słonecka, marrying - the
               record of the wedding the page dates about 1590). Tracked,
               never shown on the site.
  original.md  what the work is (the editor's standing selection, section
               22: the biography, the parents, the weddings, the children):
               the same page up to the nearest PSB persons - here the
               biographical line and the marriage with the children and
               grandchildren - shown on the site.

What the script does to the page's text:

  - the site's chrome is dropped: the koligacja form, the membership-status
    line ("Dalszy związek rodzinny z potomkami Sejmu Wielkiego"), the
    ranking line, the "All sources" and "Add or correct" links, the page's
    advertisement for the author's book (this page carries it inside the
    marriages section), the footer's navigation links and the footer
    itself. The page's own "Cytuj:" line ends full.md. The dropped status
    line is recorded in notes.md;
  - there is no ancestor tree on this page: the person of the sixteenth
    century has no known parents in the database, so the "# Przodkowie"
    heading the first and third works' scripts add is not added here, and
    the tree's furniture rules are kept but do nothing;
  - a line that is a dates token ("?1570-", "?1630-1662/"), a year in
    brackets, a bare comma, or "(linia: ...)" is joined to the line before
    it: on the page these run on inside one entry, the break is the link
    tag's;
  - a line that ends on a link tag's break - the marriage's "ślub: około
    1590):", the "&" before a spouse, the comma of the site's lists - takes
    the next line, even when the next would have been joined anyway;
  - nothing else is changed. The page's own spellings stand, including its
    lowercase opening of the heading "śluby i dzieci" (the site's own
    character slip, notes.md) and the regest's "Otha" (the record's own
    form of Otto);
  - the gender icons are pictures and are dropped; the names carry the
    gender in Polish.

Usage: python literature/minakowska2026ottotrampczynski/make_original.py "<saved page>.htm"
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# The site's chrome, dropped from both files: the line begins with it, or,
# where a second string is given, carries it anywhere.
CHROME = [
    ('Koligacja (szukanie pokrewieństwa', None),
    ('n.p. ', None),
    ('Dalszy związek rodzinny', None),
    ('Ranking WGM', None),
    ('All sources for this person', None),
    ('Add or correct dates and places', None),
    ('Przodkowie: drzewo', None),
    ('drzewo "', None),
    ('O autorce serwisu', None),
    ('Autorką i twórczynią', None),
    ('Kobiecość', None),
    ('216 stron', None),
    ('Poznaj książkę', None),
    ('Mapa grobów rodzinnych', None),
    ('Kalendarzyk Rodzinny tej osoby', None),
    ('Przodkowie - Drzewo', None),
    ('Potomkowie - Drzewo', None),
    ('Kuzyni', None),
    ('Następny brat lub siostra', None),
    ('Związek z M.J. Minakowsk', None),
    ('Baza danych na stronach', None),
    ('Baza jest uzupełniana', None),
    ('Serwisowi Sejm-Wielki.pl patronuje', None),
    ('Znani:', None),
    ('politycy:', None),
    ('uczeni (', None),
    ('©', None),
    ('IP:', None),
    ('', 'bardzo proszę'),
    ('', 'wyrażona liczba ogniw'),
    ('', 'wersja pełna'),
]

# A line that runs on inside the entry before it: joined with a space,
# except a line that begins with the comma of the site's lists, which is
# joined without one.
JOINS = [
    re.compile(r'^,'),
    re.compile(r'^\(linia: '),
    re.compile(r'^\(\d{4}[^)]*\)$'),
    re.compile(r'^(ca )?\??\d{4}([/-](\??\d{4})?)*[-/]?(\.\.\d{4})?$'),
    re.compile(r'^artykuł w Nekrologii$'),
]

# A dates token that has run on into other words ("?1710- dzieci"): the
# whole line joins the one before it.
JOINS_RUNON = re.compile(r'^(ca )?\?\d{4}[-/][^\s]*\s+\S')

# The ancestor tree's furniture, dropped inside the tree only. This page
# has no tree; the rules are kept for the shape of the two other scripts.
TREE_FURNITURE = re.compile(r'^&$|^\|$|^\d+$|^\d+ \| \d+$')


def flatten(path):
    """The page's text as lines, its headings marked '@@H3 '."""
    s = open(path, encoding='iso8859-2').read()
    s = re.sub(r'(?is)<script.*?</script>', '', s)
    s = re.sub(r'(?is)<style.*?</style>', '', s)
    s = re.sub(r'(?is)<!--.*?-->', '', s)

    def h3(m):
        t = html.unescape(re.sub(r'<[^>]+>', ' ', m.group(1)))
        return '\n@@H3 ' + ' '.join(t.split()) + '\n'

    s = re.sub(r'(?is)<h3[^>]*>(.*?)</h3>', h3, s)
    s = re.sub(r'(?i)<img[^>]*>', '', s)
    s = re.sub(r'(?i)<br\s*/?>|</(p|div|li|h\d|tr|ul|ol|table|tbody|td|center|form)>', '\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    s = s.replace('\u00a0', ' ')
    # a font tag sat before the comma: "dzieci , wnuki" is printed
    # "dzieci, wnuki"
    s = s.replace(' ,', ',')
    out = []
    for x in s.split('\n'):
        x = ' '.join(x.split())
        if x:
            out.append(x)
    return out


def is_chrome(x):
    for a, b in CHROME:
        if a and x.startswith(a):
            return True
        if b and b in x:
            return True
    return False


def main():
    lines = flatten(sys.argv[1])
    # The work begins at the page's heading of the person: the name line,
    # with the "(ID: ...)" line joined to it.
    start = next(i for i, x in enumerate(lines)
                 if x.startswith('Wojciech Otto-Trąmpczyński')
                 and 'M.J. Minakowska' not in x)
    assert lines[start + 1] == '(ID: sw.35437)', lines[start + 1]
    lines[start] += ' (ID: sw.35437)'
    # The sections, by their headings.
    h3 = [i for i, x in enumerate(lines) if x.startswith('@@H3 ')]
    sluby = next(i for i in h3 if lines[i].startswith('@@H3 \u015bluby'))
    slawni = next(i for i in h3 if lines[i].startswith('@@H3 Najbliżsi'))
    cytaj = next(i for i, x in enumerate(lines) if x.startswith('Cytuj:'))

    def assemble(stop):
        """From the person's line to `stop`, chrome dropped, the inline
        lines joined."""
        out = []
        i = start
        while i < stop:
            if i == start + 1:
                i += 1            # the "(ID: ...)" line, already joined
                continue
            x = lines[i]
            if is_chrome(x):
                i += 1
                continue
            if out and (any(rx.match(x) for rx in JOINS) or JOINS_RUNON.match(x)):
                sep = '' if x.startswith(',') else ' '
                out[-1] += sep + x
            else:
                out.append(x)
            # A line that runs on to the next, on the page and broken here
            # by a link tag: the marriage's colon, the "&" before a spouse,
            # the comma of the site's lists. The next line is taken even
            # when it would have been joined anyway.
            while out and (out[-1].endswith(':') or out[-1].endswith(' &')
                           or out[-1].endswith(',') or out[-1] == '&'):
                j = i + 1
                if j >= stop:
                    break
                y = lines[j]
                if j == start + 1 or is_chrome(y):
                    break
                sep = '' if y.startswith(',') else ' '
                out[-1] += sep + y
                i = j
            i += 1
        return out

    full = assemble(cytaj + 1)
    body = assemble(slawni)

    # The headings become markdown, one level: the page's own ("## Śluby i
    # dzieci" from its h3). No heading is added: there is no ancestor tree
    # on this page, and the grandchildren run inside the one marriages
    # heading as on the second page.
    def headings(rows):
        return ['# ' + x[5:] if x.startswith('@@H3 ') else x for x in rows]

    with open(os.path.join(HERE, 'original.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(headings(body)).rstrip('\n') + '\n')
    with open(os.path.join(HERE, 'full.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(headings(full)).rstrip('\n') + '\n')


if __name__ == '__main__':
    main()
