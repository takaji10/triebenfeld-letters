# -*- coding: utf-8 -*-
"""Make original.md and full.md of minakowska2026zielonacka from the editor's
saved page.

The source is the editor's file "Helena Zielonacka (M.J. Minakowska, Wielka
Genealogia Minakowskiego) - Wielka Genealogia Minakowskiej - M.J.
Minakowska.htm" (Downloads, 2026-10-22): person 2.976.216 of M. J.
Minakowska's Wielka genealogia Minakowskiej
(https://www.sejm-wielki.pl/b/2.976.216), the page itself citing "wydanie z
22.10.2026". The page is not kept in the repository: its header carries the
editor's login, its footer the visitor's IP address.

The page is written in ISO-8859-2 and is the database's **English** user
interface - the database renders its pages in the reader's language, so a
saved page of it may be in English where the first of these works
(minakowska2026prusimski) was in Polish. The work's language is therefore
`en`: the page as saved is what the site shows, with no English beside it.
The names, the offices and the source lines stay Polish whatever the
interface, and the Teki Dworzaczka regest of 1727 in the Uwagi is Polish.

Two files are made (docs/LITERATURE_PLAN.md, section 22):

  full.md      the knowledgebase: the whole page in reading order - the
               biography, Parents, the ancestor tree, Spouses and children,
               Siblings, the mother's other marriages (twice over, one per
               husband), Uncles and aunts, the nearest PSB persons, and
               Notes with the page's own sources (Boniecki's Herbarz, t. II
               s. 364, and the Teki Dworzaczka regest of 1727). Tracked,
               never shown on the site.
  original.md  what the work is (the editor's standing selection, section
               22: the biography, the parents, the weddings, the children):
               the same page up to "Siblings, nephews and nieces", shown on
               the site.

What the script does to the page's text:

  - the site's chrome is dropped: the koligacja form, the membership-status
    line ("Not belonging to the Genealogy of descendants of the Great
    Sejm"), the ranking line, the "All sources" and "Add or correct" links,
    the tree-view links, the footer's navigation (the graves map, the
    ancestry and descendants trees, the cousins, the shortest-path links
    and the poets named there) and the footer itself. The page's own
    "Cytuj:" line ends full.md. The dropped status line is recorded in
    notes.md;
  - the ancestor tree's connector cells ("&", "|") and Sosa numbers
    ("8 | 9") are dropped inside the tree only. The couples stand father
    then mother, four couples to a row of the page's table, which the
    linear text does not show; unknown ancestors stand as the page's "?";
  - a line that is a dates token ("?1730-", "?1760-/1806"), a year in
    brackets ("(1765)"), a bare comma, a Polish office ("kanonik [poz]
    Poznań"), "an article in the Nekrologia" or a "(line: ...)" kinship
    line is joined to the line before it, the office with a comma: on the
    page these run on inside one entry, the break is the link tag's;
  - a line that ends on a link tag's break - the marriage's "Married about
    1720 to", the "&" before a spouse, a comma, a colon - takes the next
    line, even when the next would have been joined anyway;
  - nothing else is changed. The page's own spellings stand, including its
    "«Scibor»" name-part marker and the province tags in brackets ("[poz]",
    "[san]"), which are not expanded.

Usage: python literature/minakowska2026zielonacka/make_original.py "<saved page>.htm"
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# The site's chrome, dropped from both files: the line begins with it, or,
# where a second string is given, carries it anywhere.
CHROME = [
    ('Genealogy Map Album', None),
    ('M.J. Minakowska: Minakowska', None),
    ('justin@takaji.ca', None),
    ('Alphabetic and subject indexes', None),
    ('Name Surname:', None),
    ('Koligacja (szukanie pokrewieństwa', None),
    ('n.p. ', None),
    ('Not belonging to the Genealogy', None),
    ('Ranking WGM', None),
    ('All sources for this person', None),
    ('Add or correct dates and places', None),
    ('Ancestry: tree', None),
    ('tree "', None),
    ('Mapa grobów rodzinnych', None),
    ('Ancestry - Tree', None),
    ('Descendants - Tree', None),
    ('Cousins', None),
    ('Next sibling', None),
    ('Shortest path with', None),
    ('M. Rej,', None),
    ('J. Kochanowski,', None),
    ('J.A. Morsztyn,', None),
    ('I. Krasicki,', None),
    ('Z. Krasiński,', None),
    ('A. Fredro,', None),
    ('C.K. Norwid,', None),
    ('I. Czartoryska,', None),
    ('A. Wielopolski,', None),
    ('A. Boniecki,', None),
    ('«Bór»,', None),
    ('«Hubal»,', None),
    ('kard. Sapieha,', None),
    ('MJM', None),
    ('Cytuj:', None),
    ('©', None),
    ('IP:', None),
    ('', 'bardzo proszę'),
]

# A Polish office or status standing on a line of its own: joined to the
# line before it, with a comma.
OFFICES = re.compile(
    r'^(kanonik|skarbnik|cześnik|podczaszy|stolnik|łowczy|chorąży|kasztelan'
    r'|miecznik|pisarz|podstarości|podwojewodzi|rotmistrz|starosta|sędzia'
    r'|burgrabia|regens|podkomorzy|senator|bohater)\b')

# A line that runs on inside the entry before it: joined with a space,
# except a line that begins with the comma of the site's lists, which is
# joined without one.
JOINS = [
    re.compile(r'^,'),
    re.compile(r'^\(line: '),
    re.compile(r'^\(\d{4}[^)]*\)'),
    re.compile(r'^(ca )?\??\d{4}([/-](\??\d{4})?)*[-/]?$'),
    re.compile(r'^an article in the Nekrologia$'),
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
    # a font tag sat before the comma: "with , the" is printed "with, the"
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
                 if x == 'Helena Zielonacka' and '(ID' not in x)
    assert lines[start + 1] == '(ID: 2.976.216)', lines[start + 1]
    lines[start] += ' (ID: 2.976.216)'
    # The sections, by their headings.
    h3 = [i for i, x in enumerate(lines) if x.startswith('@@H3 ')]
    parents = next(i for i in h3 if lines[i] == '@@H3 Parents')
    spouses = next(i for i in h3 if lines[i].startswith('@@H3 Spouses and children'))
    siblings = next(i for i in h3 if lines[i].startswith('@@H3 Siblings'))
    cytaj = next(i for i, x in enumerate(lines) if x.startswith('Cytuj:'))
    # The ancestor tree runs from its first row label to the heading of the
    # marriages.
    tree_start = next(i for i, x in enumerate(lines) if x == 'the great-grandparents')
    tree_end = spouses

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
            if out and (any(rx.match(x) for rx in JOINS) or JOINS_RUNON.match(x)
                        or OFFICES.match(x)):
                sep = ', ' if OFFICES.match(x) else ('' if x.startswith(',') else ' ')
                out[-1] += sep + x
            else:
                out.append(x)
            # A line that runs on to the next, on the page and broken here
            # by a link tag: the marriage's "Married about 1720 to", the "&"
            # before a spouse, the comma of the site's lists. The next line
            # is taken even when it would have been joined anyway.
            while out and (out[-1].endswith(':') or out[-1].endswith(' &')
                           or out[-1].endswith(',') or out[-1].endswith(' to')
                           or out[-1] == '&'):
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
    body = assemble(siblings)

    # The headings become markdown, one level: the page's own (its h3) and
    # none added - this page's one marriages heading covers the
    # grandchildren, so the "# Wnuki" the first work's script needed is not
    # needed here.
    def headings(rows):
        return ['# ' + x[5:] if x.startswith('@@H3 ') else x for x in rows]

    with open(os.path.join(HERE, 'original.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(headings(body)).rstrip('\n') + '\n')
    with open(os.path.join(HERE, 'full.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(headings(full)).rstrip('\n') + '\n')


if __name__ == '__main__':
    main()
