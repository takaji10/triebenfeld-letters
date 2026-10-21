# -*- coding: utf-8 -*-
"""Make original.md of boniecki1900 from the editor's saved page.

The source is the editor's file "New Boniecki - Genealogy of Polish-Lithuanian
Elites — Chełmscy h. Ostoja.htm" (Downloads, 2026-10-21): article 2.976 of
M. J. Minakowski's online edition of Boniecki's Herbarz polski
(https://wielcy.pl/wgm/boniecki/en/art/2/976.xml). The page is not kept in the
repository: its header carries the editor's login.

Only the branch of the family that held Łukom is taken (editor, 2026-10-21:
Stanisław Chełmski, his brother Heliodor, and the passages on Łukom, Bukowe,
Łomów and Imielno, "Mielno" here). The text is the page's "Running text",
copied as given: the online edition's paragraph mark ¶ kept, nothing
corrected ("(Sig. 27 f. 349 )Heliodor" stands as it is). What this script
does to it:

  - it joins the lines of a paragraph with a space: the online edition breaks
    the running text at each person it links, the print does not;
  - it heads each part with the online edition's item numbers ("# 2.976.177-
    182"), so that each can be found on the site; the headings are the
    edition's, not Boniecki's;
  - it marks what is left out of a paragraph with "[…]".

Usage: python literature/boniecki1900/make_original.py "<saved page>.htm"
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (heading, [(first words of the first line, first words of the last line,
#   cut the last line after these words or None)])
PARTS = [
    ('2.976.162-176', [('¶ W tem miejscu urywa się', 'Jerzego.', None)]),
    ('2.976.177-182', [('¶ Krzysztof Ścibor, zeznał', 'Pozostała po nim wdowa', None)]),
    ('2.976.183, 196-198, 209-210', [
        ('¶ Syn jego Adam Scibor', '¶ Syn jego Adam Scibor', 'chorąży chorągwi pancernej,'),
        ('¶ Ignacy,', 'cześnikiem rożańskim, właściciel', 'cześnikiem rożańskim,'),
        ('Ignacy część swoją na dobrach', 'bratu swemu ze stryjecznych', None),
    ]),
    ('2.976.211-220', [('¶ Andrzej Scibor Chełmski podpisał', 'za Janem Czarnockim', None)]),
    ('2.976.221-225', [('Józef', 'W 1755 r. wyznaczoną', None)]),
    ('2.976.226-240', [('Stanisław, skarbnik wschowski', 'i Zygmunt, urodzony', None)]),
]


def running_text(path):
    s = open(path, encoding='utf-8', errors='strict').read()
    s = re.sub(r'(?is)<(script|style).*?</\1>', '', s)
    s = re.sub(r'(?i)<br\s*/?>|</p>|</div>|</li>|</h\d>|</tr>', '\n', s)
    t = html.unescape(re.sub(r'<[^>]+>', '', s))
    t = re.sub(r'[ \t]+', ' ', t)
    lines = [x.strip() for x in t.split('\n') if x.strip()]
    start = max(i for i, x in enumerate(lines) if x == 'Running text')
    return lines[start + 1:]


def find(lines, words, after):
    hits = [i for i in range(after, len(lines)) if lines[i].startswith(words)]
    assert hits, words
    return hits[0]


def paragraphs(chunk):
    """Join a run of lines into paragraphs, a new one at each ¶."""
    out = []
    for x in chunk:
        if x.startswith('¶') or not out:
            out.append(x)
        else:
            out[-1] += ' ' + x
    return out


def main():
    lines = running_text(sys.argv[1])
    pos = find(lines, '¶ W tem miejscu urywa się', 0)
    body = ['**Chełmscy h. Ostoja**', '']
    for head, runs in PARTS:
        body += ['# ' + head, '']
        for first, last, cut in runs:
            a = find(lines, first, pos)
            b = find(lines, last, a)
            chunk = lines[a:b + 1]
            if cut:
                k = chunk[-1].index(cut) + len(cut)
                chunk[-1] = chunk[-1][:k] + ' […]'
            pos = b + 1
            body += [p for para in paragraphs(chunk) for p in (para, '')]
    with open(os.path.join(HERE, 'original.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(body).rstrip('\n') + '\n')


if __name__ == '__main__':
    main()
