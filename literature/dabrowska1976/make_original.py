# -*- coding: utf-8 -*-
"""Make original.md of dabrowska1976 from saved copies of JewishGen's pages.

The work: three entries of Pinkas Hakehillot Polin, vol. I (Yad Vashem), in
JewishGen's English translation by Morris Gradel, each a page the editor
named (2026-10-21; fetched that day):

  p. 103       Zagórów  https://www.jewishgen.org/Yizkor/pinkas_poland/pol1_00103a.html
  pp. 202-203  Pyzdry   https://www.jewishgen.org/Yizkor/pinkas_poland/pol1_00202.html
  pp. 235-238  Konin    https://www.jewishgen.org/Yizkor/pinkas_poland/pol1_00235.html

JewishGen's notice: "This material may not be copied, sold or bartered
without JewishGen, Inc.'s permission". The editor ruled (2026-10-21): kept as
Seidel (2018), in the repository with no page on the site (work.yml,
visible: false); the saved pages are not kept.

What is taken from each page: the entry, from its page reference ("{Page
103}", "{Page 202}", "(pages 235-238)") to its end, before the site's links:
heading, translator's line, tables, section headings, paragraphs, the Konin
photograph's caption and the translator's notes, as given (the "Z" for
Zagórów, "Andaks" for the Endeks, the translation's spellings and
slips). Left out: JewishGen's acknowledgements and disclaimer above each
entry (quoted in notes.md), the images and the site's links. Each page
reference becomes the edition's page mark ("[p. 202-203]"); the HTML's runs
of spaces and its hard line ends inside a paragraph become single spaces.
Headings: the entry's title "##", a section "###".

Usage: python literature/dabrowska1976/make_original.py <dir with the saved pages>
       (page_00103a.html, page_00202.html, page_00235.html)
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = [  # saved file, where the entry begins, its page mark
    ('page_00103a.html', '{Page 103}', '103'),
    ('page_00202.html', '{Page 202}', '202-203'),
    ('page_00235.html', '(pages 235-238)', '235-238'),
]


def inline(fragment):
    """Bold, italic and underline as Markdown; other tags dropped."""
    t = re.sub(r'(?is)<(b|strong|u)>(.*?)</\1>', lambda m: '**' + m.group(2).strip() + '**', fragment)
    t = re.sub(r'(?is)<(i|em)>(.*?)</\1>', lambda m: '*' + m.group(2).strip() + '*' if m.group(2).strip() else '', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t).replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', t).strip()


def table(m):
    rows = []
    for tr in re.findall(r'(?is)<tr>(.*?)</tr>', m.group(1)):
        cells = [inline(re.sub(r'(?i)<br\s*/?>', ' ', c)).replace('**', '')
                 for c in re.findall(r'(?is)<td[^>]*>(.*?)</td>', tr)]
        rows.append(cells)
    out = ['| ' + ' | '.join(rows[0]) + ' |', '|' + '---|' * len(rows[0])]
    out += ['| ' + ' | '.join(r) + ' |' for r in rows[1:]]
    return '\n\n' + '\n'.join(out) + '\n\n'


def convert(raw, start, mark):
    body = raw[raw.index(start) + len(start):raw.index('Yizkor Book Project', raw.index(start))]
    body = re.sub(r'(?is)<img[^>]*>|<a [^>]*>|</a>|<hr[^>]*>|</?center>', ' ', body)
    # the title and the district
    body = re.sub(r'(?is)<font size="?\+2"?>(.*?)</font>', lambda m: '\n\n## ' + inline(m.group(1)) + '\n\n', body)
    body = re.sub(r'(?is)<font size="?\+1"?>(.*?)</font>', lambda m: '\n\n' + inline(m.group(1)) + '\n\n', body)
    body = re.sub(r'(?is)<table[^>]*>(.*?)</table>', table, body)

    def h4(m):
        parts = [inline(p) for p in re.split(r'(?i)<p>', m.group(1)) if inline(p)]
        out = []
        for p in parts:
            if p.startswith('Translated by'):
                out.append('*' + p + '*')
            elif p.startswith('**'):
                out.append(p)
            else:
                out.append('### ' + p)
        return '\n\n' + '\n\n'.join(out) + '\n\n'
    body = re.sub(r'(?is)<h4[^>]*>(.*?)</h4>', h4, body)
    # paragraphs: <p>, </p> and <br> break; inside, lines join
    paras = re.split(r'(?i)</?p>|<br\s*/?>|\n\s*\n', body)
    out = []
    for p in paras:
        if p.strip().startswith(('|', '##', '###')):
            out.append(p.strip())
            continue
        t = inline(p)
        if t and t != '**':
            out.append(t)
    # a markdown table or heading kept by the split above may still carry
    # following text on its lines: give each its own block
    blocks = []
    for b in out:
        blocks += [x.strip() for x in re.split(r'\n\s*\n', b) if x.strip()]
    return '[p. ' + mark + ']\n\n' + '\n\n'.join(blocks) + '\n'


def main():
    d = sys.argv[1]
    parts = []
    for fn, start, mark in PAGES:
        raw = open(os.path.join(d, fn), 'rb').read().decode('utf-8')
        parts.append(convert(raw, start, mark))
    with open(os.path.join(HERE, 'original.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(parts))
    print('wrote original.md:', len(parts), 'entries')


if __name__ == '__main__':
    main()
