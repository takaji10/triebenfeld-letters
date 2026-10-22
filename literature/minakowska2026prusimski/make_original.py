# -*- coding: utf-8 -*-
"""Make original.md and full.md of minakowska2026prusimski from the editor's
saved page.

The source is the editor's file "Antoni Michał Kazimierz Ostroróg-Prusimski
z Kolna h. Nałęcz (M.J. Minakowska, Genealogia potomków Sejmu Wielkiego).htm"
(Downloads, 2026-10-22): person 4.285.619 of M. J. Minakowska's Wielka
genealogia Minakowskiej (https://www.sejm-wielki.pl/b/4.285.619), the page
itself citing "wydanie z 22.10.2026". The page is not kept in the repository:
its header carries the editor's login, and its footer the visitor's IP
address.

The page is written in ISO-8859-2 (latin2). Two files are made:

  full.md      the knowledgebase (docs/LITERATURE_PLAN.md, section 22): the
               whole page in reading order - the biography, Rodzice, the
               ancestor tree, Śluby i dzieci, the mother's other marriages
               (Inne małżeństwa i dzieci matki), Stryjowie lub wujowie oraz
               ciotki, i kuzynki, Najbliżsi sławni ludzie, and Uwagi with the
               page's own source list and the Teki Dworzaczka regest of 1786.
               Tracked, never shown on the site.
  original.md  what the work is (the editor, 2026-10-22: "his biographical
               details, parents, weddings, and children"): the same page up
               to the mother's other marriages, shown on the site.

What the script does to the page's text:

  - the site's chrome is dropped: the koligacja form, the ranking line, the
    "All sources" and "Add or correct" links, the tree-view links, the page's
    advertisement for the author's book, the footer's navigation links and
    the footer itself. The page's own "Cytuj:" line ends full.md;
  - the ancestor tree's connector cells ("&", "|") and Sosa numbers ("8 | 9")
    are dropped inside the tree only: they are the table's furniture. The
    couples are father then mother, four couples to a row of the page's
    table, which the linear text does not show;
  - a line that is a dates token ("?1710-", "ca 1763-", "1778-1851"), a year
    in brackets ("(1775)"), a bare comma, a "(linia: ...)" kinship line, or
    "artykuł w Nekrologii" is joined to the line before it: on the page these
    run on inside one entry, the break is the link tag's;
  - nothing else is changed. The page's own spellings stand, including its
    lowercase opening of the heading "śluby i dzieci" (the site's own
    character slip, notes.md) and the site's province tags in brackets
    ("[str]", "[bku]"), which are not expanded;
  - the gender icons are pictures and are dropped; the names carry the
    gender in Polish;
  - two headings are added, and are not the page's: "# Przodkowie" before the
    ancestor tree, and "# Wnuki" where the grandchildren's list begins.

Usage: python literature/minakowska2026prusimski/make_original.py "<saved page>.htm"
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
    ('Najbliższa rodzina uczestnika', None),
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
]

# A line that runs on inside the entry before it: joined with a space,
# except a line that begins with the comma of the site's lists, which is
# joined without one.
JOINS = [
    re.compile(r'^,'),
    re.compile(r'^\(linia: '),
    re.compile(r'^\(\d{4}[^)]*\)$'),
    re.compile(r'^(ca )?\??\d{4}([/-](\??\d{4})?)*[-/]?$'),
    re.compile(r'^artykuł w Nekrologii$'),
]

# A dates token that has run on into other words ("?1710- dzieci"): the
# whole line joins the one before it.
JOINS_RUNON = re.compile(r'^(ca )?\?\d{4}[-/][^\s]*\s+\S')

# The ancestor tree's furniture, dropped inside the tree only.
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
    # a font tag sat before the comma: "i dzieci , wnuki" is printed
    # "i dzieci, wnuki"
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
                 if x.startswith('Antoni Michał Kazimierz')
                 and 'M.J. Minakowska' not in x)
    assert lines[start + 1] == '(ID: 4.285.619)', lines[start + 1]
    lines[start] += ' (ID: 4.285.619)'
    # The sections, by their headings.
    h3 = [i for i, x in enumerate(lines) if x.startswith('@@H3 ')]
    sluby = next(i for i in h3 if lines[i].startswith('@@H3 \u015bluby'))
    inne = next(i for i in h3 if lines[i].startswith('@@H3 Inne ma'))
    cytaj = next(i for i, x in enumerate(lines) if x.startswith('Cytuj:'))
    # The ancestor tree runs from its first row label to the heading of the
    # marriages.
    tree_start = next(i for i, x in enumerate(lines) if x == 'pradziadkowie')
    tree_end = sluby

    def assemble(stop):
        """From the person's line to `stop`, chrome dropped, the inline
        lines joined, the tree's furniture dropped inside the tree."""
        out = []
        i = start
        while i < stop:
            if i == start + 1:
                i += 1            # the "(ID: ...)" line, already joined
                continue
            x = lines[i]
            if is_chrome(x) or (tree_start <= i < tree_end
                                and TREE_FURNITURE.match(x)):
                i += 1
                continue
            if out and (any(rx.match(x) for rx in JOINS) or JOINS_RUNON.match(x)):
                sep = '' if x.startswith(',') else ' '
                out[-1] += sep + x
            else:
                out.append(x)
            # A line that runs on to the next, on the page and broken here
            # by a link tag: the entry's colon, the "&" before a spouse, the
            # comma of the site's office and kinship lists. The next line is
            # taken even when it would have been joined anyway.
            while out and (out[-1].endswith(':') or out[-1].endswith(' &')
                           or out[-1].endswith(',') or out[-1] == '&'):
                j = i + 1
                if j >= stop:
                    break
                y = lines[j]
                if j == start + 1 or is_chrome(y) or \
                        (tree_start <= j < tree_end and TREE_FURNITURE.match(y)):
                    break
                sep = '' if y.startswith(',') else ' '
                out[-1] += sep + y
                i = j
            i += 1
        return out

    full = assemble(cytaj + 1)
    body = assemble(inne)

    # The two added headings.
    with_headings = []
    for x in body:
        if x == 'pradziadkowie':
            with_headings += ['# Przodkowie', '']
        if x == 'dzieci' and any('Stanisław Adam' in y for y in with_headings[-6:]) \
                and not any(y == '# Wnuki' for y in with_headings):
            with_headings += ['# Wnuki', '']
        with_headings.append(x)
    body = with_headings

    # The headings become markdown, one level: the page's own ("## Rodzice"
    # from its h3) and the two added ones alike.
    def headings(rows):
        return ['# ' + x[5:] if x.startswith('@@H3 ') else x for x in rows]

    with open(os.path.join(HERE, 'original.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(headings(body)).rstrip('\n') + '\n')
    with open(os.path.join(HERE, 'full.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(headings(full)).rstrip('\n') + '\n')


if __name__ == '__main__':
    main()
