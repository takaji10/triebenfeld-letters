# -*- coding: utf-8 -*-
"""
Chodyła (2015): the book's PDF to literature/chodyla2015/original.md and its
page pictures (2026-10-21).

    python pipeline/literature/chodyla_pdf.py <the PDF> [--figures] [--report]

The PDF ("Zarys najstarszych dziejów osad olederskich w Puszczy Pyzdrskiej
1746 – 1793 (Chodyła, 2015).pdf" in the editor's Books folder) is the printed
book as set in InDesign, so its text layer is the book's text, not a reading of
an image. The editor's Word file of the same text (".docx.md") has lost the
pages, the raised note numbers and the italics of the book titles; it is used
to check this one word by word (literature/chodyla2015/notes.md).

What this script does to the text layer, and nothing else:
- each page is opened with "[p. N]" (the printed page is the PDF's page).
  Pages 1 and 3 (the title page and "Pyzdry 2015") stand before the first
  mark, as the work's front. Page 2 holds only a decoration; page 4, the
  table of contents, is left out (the editor ruled so for Pachoński's book).
  The page number at the foot of each page is left out;
- the lines of a paragraph are joined. A paragraph begins after a heading,
  where the type size changes, at a line beginning in bold (a term of the
  glossary), at an item of the list of illustrations ("4." and a tab), after
  a short line that ends a sentence (the glossary and the list have no
  indents; a line short only because it runs beside a picture and ends in a
  note mark does not count), and at a line indented by the book's indent (12
  to 24 points) after a line that ends a sentence or is short. Text set round
  a portrait starts further in and is not a new paragraph; nor is the second
  line of a numbered point whose first line hangs ("5)" or "3)" and a tab);
  nor a line after a word divided at a line's end. The large initial letter
  of a chapter is set before the rest of its word;
- a word divided at the end of a line is joined again. A hyphen is kept
  where the joined form is a compound the book prints elsewhere within a line
  ("społeczno-zawodowej"), or a first part in -o the book prints with a
  hyphen ("funkcjonalno-"), where a number or a capital stands at the break
  ("1939-Kraków", "Dzierzbińskie-Zamęty"), and where the next line repeats the
  hyphen, as Polish typesetting does ("Wrocław-" / "-Warszawa"). A word
  divided over two pages is given whole on the first (pages holding only a
  picture may stand between). Every break the script decided without seeing
  the word elsewhere is listed by --report;
- headings (19-point bold) become "# ...";
- the notes are at the foot of each page, numbered through the book (1 to
  369). A note's raised number in the text becomes "[^n]" and the note
  "[^n]: ..." at the end of its page; a note that runs on to the next page is
  given whole on the page where it begins. A raised figure is a note mark
  only in the order of the notes; any other ("km²") becomes its raised
  character. Two marks are printed in the text's own type (FLAT_MARKS, notes
  25 and 366) and are set by hand. Everything in small type below the first
  note of a page is the notes' (note 12 holds a title set a size larger);
- italic becomes *...*, bold **...**. Spaces, tabs and no-break spaces become
  one space, and a space is put where the page leaves a gap between two spans
  and gives none; the ligatures "ﬁ" and "ﬂ" (set with a space after them)
  become "fi" and "fl". A few letters are set at 0.1 point and do not show in
  print ("B|ü|sching", p. 45): they are the words' letters and are kept; one
  stray, " ű" after a printed "fü" (p. 17), is left out. The words inside the
  sponsors' logos (p. 155) are left out. The text is otherwise unchanged, its
  slips included;
- the ruled tables (Tab. 1 to 3) are read cell by cell (PyMuPDF's
  find_tables) and written as HTML tables, a cell spanning columns or rows
  with colspan or rowspan, italic as <i>. A word belongs to the cell it
  begins in (a wide number runs over into the next; "1 177" is two cells'
  figures in one span); a header set sideways is read left to right. Each
  page's part of a table is given under that page;
- the captions of the illustrations are text, after the text of their page
  (a caption beside a portrait would otherwise fall into the paragraph).
With --figures it renders every page that holds an illustration (maps,
documents, portraits; not the decorations, the signatures or the sponsors'
logos) at 1100 pixels wide into site/assets/literature/chodyla2015/<page>.jpg,
and prints the `figures` list for work.yml.
"""
import io
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'literature', 'chodyla2015', 'original.md')
FIG = os.path.join(ROOT, 'site', 'assets', 'literature', 'chodyla2015')
FRONT = (1, 3)
SKIP = {2, 4}
# pages with an illustration; the others with pictures hold decorations (2),
# signatures (7, 8) or logos (154-156)
FIGURES = [22, 23, 24, 25, 26, 27, 29, 30, 32, 35, 36, 37, 38, 41, 42, 43, 44,
           46, 47, 48, 50, 51, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 67, 68,
           69, 71, 72, 73, 122]
TABLE_PAGES = set(range(12, 16)) | set(range(89, 92)) | set(range(97, 104))
RAISE = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
SPACE_CHARS = ' \t\u00a0'
SPACES = re.compile(r'[ \t\u00a0\u2009\u202f]+')
UPPER = 'A-ZĄĆĘŁŃÓŚŹŻÄÖÜ'
LOWER = 'a-ząćęłńóśźżäöüé'

REPORT = []
LAST = [0]          # the last note mark set: marks run 1 to 369 through the book
# two note marks are printed in the text's own type, not raised (pp. 18, 147)
FLAT_MARKS = {18: ('z 1789 r. 25 tabele', 'z 1789 r.[^25] tabele', 25),
              147: ('mieszkańców 366.', 'mieszkańców[^366].', 366)}


def lig(t):
    return t.replace('ﬁ ', 'fi').replace('ﬂ ', 'fl').replace('ﬁ', 'fi').replace('ﬂ', 'fl')


class Run:
    __slots__ = ('text', 'it', 'bold', 'sup')

    def __init__(self, text, it=False, bold=False, sup=False):
        self.text, self.it, self.bold, self.sup = text, it, bold, sup


LOGO_FONTS = ('Calibri', 'CanalLight')     # the words inside the sponsors' logos (p. 155)


def span_runs(spans):
    """A line's spans as runs; where the page leaves a gap between two spans
    and gives no space ("4 132" in a table), a space is put in."""
    out, prev = [], None
    for s in sorted(spans, key=lambda s: s['bbox'][0]):
        if any(f in s['font'] for f in LOGO_FONTS):
            continue
        t = lig(s['text'].replace('\u00ad', ''))
        if not t:
            continue
        # letters set at 0.1 point do not show in print but are the words'
        # letters ("B|ü|sching", p. 45) and are kept; one, " ű" after a
        # printed "fü" (p. 17), is a stray and is left out
        if s['size'] < 1 and t.startswith(' '):
            continue
        sup = bool(s['flags'] & 1) and s['size'] < 8
        if (prev is not None and out and s['bbox'][0] - prev['bbox'][2] > 1.5 and not sup
                and not out[-1].text.endswith((' ', '\u00a0', '\t')) and not t.startswith((' ', '\u00a0', '\t'))):
            out[-1].text += ' '
        out.append(Run(t, 'It' in s['font'], 'Bold' in s['font'] or 'Semibold' in s['font'], sup))
        prev = s
    return out


def rows_of(page, exclude=()):
    """Lines in reading order: dict(x0, y, x1, size, runs). Lines whose middle
    lies in one of the rectangles `exclude` (the tables) are left out."""
    rows = []
    for b in page.get_text('dict')['blocks']:
        if b['type'] != 0:
            continue
        for l in b['lines']:
            spans = [s for s in l['spans'] if s['text'].strip(' \t\u00a0')]
            if not spans:
                continue
            x0, y0, x1, y1 = l['bbox']
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            if any(r[0] <= cx <= r[2] and r[1] <= cy <= r[3] for r in exclude):
                continue
            # the size of the line's first letters: a note may hold a title
            # set a size larger (notes 12 and 48)
            body = [s for s in spans if s['size'] > 1 and not s['flags'] & 1]
            size = (body or [s for s in spans if s['size'] > 1] or spans)[0]['size']
            rows.append({'x0': x0, 'y': round(y0), 'x1': x1, 'size': round(size, 1),
                         'spans': l['spans']})
    rows.sort(key=lambda r: (r['y'], r['x0']))
    merged = []
    for r in rows:
        m = merged[-1] if merged else None
        if m and abs(m['y'] - r['y']) <= 3 and abs(m['size'] - r['size']) < 1 and r['x0'] > m['x0']:
            m['x1'] = max(m['x1'], r['x1'])
            m['spans'] = m['spans'] + r['spans']
        else:
            merged.append(r)
    for m in merged:
        m['runs'] = span_runs(m['spans'])
    return merged


# ---------------------------------------------------------------- words

def words_inside(doc):
    """Every word and hyphenated compound that stands within a line."""
    seen = Counter()
    for page in doc:
        for line in page.get_text().split('\n'):
            line = lig(line).replace('\u00a0', ' ')
            for w in re.findall(rf'[{UPPER}{LOWER}A-Za-z]+(?:-[{UPPER}{LOWER}A-Za-z]+)*', line):
                seen[w.lower()] += 1
    return seen


SEEN = Counter()


def compound(left, right):
    """A compound adjective of the book's kind ("funkcjonalno-gospodarczej",
    "emfiteutyczno-wieczystego") divided at its hyphen: the book prints the
    same first part with a hyphen elsewhere, before the same beginning, or the
    first part is a long one in -o and the second a word of its own."""
    head = (left + '-' + right[:3]).lower()
    if any(w.startswith(head) for w in SEEN):
        return True
    if not left.endswith('o'):
        return False
    if len(left) >= 4 and any(w.startswith(left.lower() + '-') for w in SEEN):
        return True
    return left.endswith(('no', 'ko')) and len(left) >= 8 and len(right) >= 6


def join_runs(a, b, where):
    """Append the runs of line b to the runs a, joining a divided word."""
    if not a:
        return list(b)
    if not b:
        return a
    last = a[-1]
    first = b[0]
    lt = last.text.rstrip(' ')
    if lt.endswith('-') and not last.sup:
        left = re.search(rf'([{UPPER}{LOWER}A-Za-z0-9]*)-$', lt).group(1)
        rt = first.text.lstrip(' ')
        right = re.match(rf'[{UPPER}{LOWER}A-Za-z0-9]*', rt).group(0)
        if rt.startswith('-'):
            how = 'repeat'
        elif not left or not right or left[-1].isdigit() or right[0].isdigit() or right[0].isupper():
            how = 'keep'
        elif SEEN[(left + '-' + right).lower()] or compound(left, right):
            how = 'keep'
        elif SEEN[(left + right).lower()]:
            how = 'join'
        else:
            how = 'join'
            REPORT.append(f'{where}: {left}-|{right} -> {left}{right}')
        if how == 'join':
            last.text = lt[:-1]
        elif how == 'keep':
            last.text = lt
        else:
            last.text = lt
            rest = rt[1:]
            b = [Run(rest, first.it, first.bold, first.sup)] + list(b[1:])
            return a + b
        b = [Run(rt, first.it, first.bold, first.sup)] + list(b[1:])
        return a + b
    if not last.text.endswith(' ') and not first.text.startswith(' '):
        last.text = last.text + ' '
    return a + list(b)


def render(runs, notes, html=False):
    """Runs to Markdown (or HTML for a table cell)."""
    # merge raised figures and turn them into note marks
    out = []
    for r in runs:
        if out and out[-1].sup and r.sup:
            out[-1] = Run(out[-1].text + r.text, sup=True)
        elif out and not r.sup and not out[-1].sup and (out[-1].it, out[-1].bold) == (r.it, r.bold):
            out[-1] = Run(out[-1].text + r.text, r.it, r.bold)
        else:
            out.append(Run(r.text, r.it, r.bold, r.sup))
    text = ''
    for r in out:
        t = SPACES.sub(' ', r.text)
        if r.sup and not t.strip():
            text += ' '
            continue
        if r.sup:
            # a raised mark may carry a raised quotation mark before it ("”297")
            m = re.match(r'(\D*)(\d*)(.*)$', t.strip())
            pre, k, post = m.groups()
            text += pre
            if k and k in notes and LAST[0] < int(k) <= LAST[0] + 3:
                text = text.rstrip(' ') + f'[^{k}]'
                LAST[0] = int(k)
            elif k:
                text += k.translate(RAISE)
            text += post
            continue
        if not (r.it or r.bold) or not t.strip():
            text += t
            continue
        lead = t[:len(t) - len(t.lstrip(' '))]
        trail = t[len(t.rstrip(' ')):]
        core = t.strip(' ')
        if html:
            core = f'<i>{core}</i>' if r.it else f'<b>{core}</b>'
        else:
            mark = '*' if r.it else '**'
            core = f'{mark}{core}{mark}'
        text += lead + core + trail
    return SPACES.sub(' ', text).strip()


# ---------------------------------------------------------------- tables

def span_words(s):
    """A span cut into its words, each a span of its own with its own bounds:
    a table's cell border may fall between two words of one span ("1 177",
    the column Inni and the total, p. 97)."""
    out, cur = [], []
    for ch in s['chars'] + [None]:
        if ch is None or ch['c'] in SPACE_CHARS:
            if cur:
                out.append(cur)
                cur = []
            if ch is not None and out:
                out[-1].append(ch)          # the space stays with its word
        else:
            cur.append(ch)
    pieces = []
    for w in out:
        x0 = min(c['bbox'][0] for c in w)
        x1 = max(c['bbox'][2] for c in w)
        pieces.append({'text': ''.join(c['c'] for c in w), 'font': s['font'],
                       'size': s['size'], 'flags': s['flags'],
                       'bbox': (x0, s['bbox'][1], x1, s['bbox'][3])})
    return pieces


def table_html(page, t, notes, where):
    """One table as HTML rows, with colspan and rowspan from the cells' bounds."""
    xs = sorted({round(c[0]) for c in t.cells} | {round(c[2]) for c in t.cells})
    ys = sorted({round(c[1]) for c in t.cells} | {round(c[3]) for c in t.cells})

    def near(v, grid):
        return min(range(len(grid)), key=lambda i: abs(grid[i] - v))
    lines = []
    for b in page.get_text('rawdict')['blocks']:
        if b['type'] != 0:
            continue
        for l in b['lines']:
            l = dict(l)
            l['spans'] = [w for s in l['spans'] for w in span_words(s)]
            lines.append(l)
    rows_html = []
    taken = set()
    grid = {}
    for c in t.cells:
        r0, r1 = near(c[1], ys), near(c[3], ys)
        c0, c1 = near(c[0], xs), near(c[2], xs)
        grid[(r0, c0)] = (r1, c1, c)
    for ri in range(len(ys) - 1):
        cells = []
        for ci in range(len(xs) - 1):
            if (ri, ci) in taken:
                continue
            if (ri, ci) not in grid:
                continue
            r1, c1, c = grid[(ri, ci)]
            for a in range(ri, r1):
                for bb in range(ci, c1):
                    taken.add((a, bb))
            # the cell's lines, joined
            inside = []
            for l in lines:
                x0, y0, x1, y1 = l['bbox']
                cy = (y0 + y1) / 2
                if not c[1] - 1 <= cy <= c[3] + 1:
                    continue
                if abs(l['dir'][1]) > 0.5:             # set sideways (headers):
                    if c[0] - 1 <= (x0 + x1) / 2 <= c[2] + 1:
                        spans = [s for s in l['spans'] if s['text'].strip(SPACE_CHARS)]
                        if spans:                     # read left to right
                            inside.append((round(x0), -y1, span_runs(spans)))
                    continue
                # a word belongs to the cell it begins in: the PDF may set a
                # wide number and the name beside it as one line ("10.-11.")
                spans = [s for s in l['spans'] if s['text'].strip(SPACE_CHARS)
                         and c[0] - 1 <= s['bbox'][0] + 1 < c[2]]
                if spans:
                    inside.append((round(y0), spans[0]['bbox'][0], span_runs(spans)))
            inside.sort(key=lambda z: (z[0], z[1]))
            runs, prev_y = [], None
            for y, x, rr in inside:
                if prev_y is not None and abs(y - prev_y) <= 2:
                    runs = runs + [Run(' ')] + rr
                else:
                    runs = join_runs(runs, rr, where)
                prev_y = y
            txt = render(runs, notes, html=True)
            attrs = ''
            if c1 - ci > 1:
                attrs += f' colspan="{c1 - ci}"'
            if r1 - ri > 1:
                attrs += f' rowspan="{r1 - ri}"'
            cells.append(f'<td{attrs}>{txt}</td>')
        if cells:
            rows_html.append('<tr>' + ''.join(cells) + '</tr>')
    return '<table><tbody>\n' + '\n'.join(rows_html) + '\n</tbody></table>'


# ---------------------------------------------------------------- pages

def note_start(r):
    t = ''.join(s['text'] for s in r['spans'])
    m = re.match(r'\s*(\d+)\t', t)
    return m.group(1) if m else None


def page_items(page, n, notes_all, pending):
    """The page's paragraphs, tables and notes as Markdown blocks."""
    tables = []
    if n in TABLE_PAGES:
        tables = [t for t in page.find_tables().tables]
    rects = [t.bbox for t in tables]
    rows = [r for r in rows_of(page, rects)
            if not (r['size'] == 11.0 and r['y'] > 630)]          # page number
    # the notes: from the first line that opens a note, every line in small
    # type below it (a note may hold a title set larger, note 12), and lines
    # of a note run on from the page before
    first = min((r['y'] for r in rows if r['size'] == 8.5 and note_start(r)), default=10 ** 6)
    small = [r for r in rows if r['size'] == 8.5 or (r['y'] >= first and r['size'] < 10)]
    body = [r for r in rows if r not in small]
    # captions stand beside or under their picture: given after the text
    captions = [r for r in body if r['size'] == 8.0]
    body = [r for r in body if r['size'] != 8.0]
    where = f'p. {n}'
    # left margin and right edge of the text block
    lefts = [r['x0'] for r in body if r['size'] == 10.5]
    left = min(lefts) if lefts else min((r['x0'] for r in body), default=0)
    right = max((r['x1'] for r in body if r['size'] in (10.5, 9.0, 8.0)), default=0)

    items = []      # (y, kind, payload)
    for t in tables:
        items.append((t.bbox[1], 'table', t))
    for r in body:
        items.append((r['y'], 'row', r))
    items.sort(key=lambda z: (z[0], 0 if z[1] == 'table' else 1, z[2]['x0'] if z[1] == 'row' else 0))

    blocks, para, prev, drop = [], None, None, ''
    lines_in = []
    hanging = False     # the paragraph is a numbered point whose first line hangs ("3)")
    heading = None

    def close():
        nonlocal para
        if para is not None:
            blocks.append(('p', para))
            para = None

    for y, kind, r in items:
        if kind == 'table':
            close()
            if heading:
                blocks.append(('h', heading)); heading = None
            blocks.append(('t', r))
            prev = None
            continue
        size = r['size']
        if size >= 40:                       # the large initial
            drop = ''.join(s['text'] for s in r['spans']).strip()
            continue
        if size >= 18 and all('Bold' in s['font'] for s in r['spans'] if s['text'].strip()):
            close()
            txt = SPACES.sub(' ', ''.join(lig(s['text']) for s in r['spans'])).strip()
            heading = (heading + ' ' + txt) if heading else txt
            prev = r
            continue
        if heading:
            blocks.append(('h', heading)); heading = None
            prev = None
        runs = r['runs']
        if drop:
            runs = [Run(drop)] + runs
            drop = ''
        starts = para is None or prev is None
        if not starts:
            short = prev['x1'] < right - 20
            # the line before ends a sentence (a note mark counts as an end)
            full = [x for x in para if x.text.strip()] if para else []
            ended = bool(full) and (full[-1].sup or bool(
                re.search(r'[.:!?”)]\s*$', full[-1].text)))
            if abs(size - prev['size']) >= 0.5:
                starts = True
            elif (size >= 10 and 12 <= r['x0'] - prev['x0'] <= 24 and (short or ended)
                  and not (hanging and len(lines_in) == 1)):
                starts = True                # indented first line (text set
                                             # round a picture starts further
                                             # in; a numbered point hangs: its
                                             # first line stands out, "5)")
            elif re.match(r'\s*\d+\.\t', ''.join(sp['text'] for sp in r['spans'])):
                starts = True                # an item of the list of illustrations
            elif r['runs'] and r['runs'][0].bold and not prev['runs'][-1].bold:
                starts = True
            elif short and ended and not full[-1].sup:    # text beside a picture runs short
                starts = True
            elif r['y'] - prev['y'] > prev['size'] * 2.2:
                starts = True
            # a word divided at the line's end is never a paragraph's end
            head = ''.join(x.text for x in runs).lstrip()
            if (starts and para and re.search(rf'[{UPPER}{LOWER}]-\s*$', para[-1].text)
                    and head[:1].islower()):
                starts = False
        if starts:
            close()
            para = list(runs)
            lines_in = [r]
            hanging = bool(re.match(r'\s*\d+\)\t', ''.join(sp['text'] for sp in r['spans'])))
        else:
            para = join_runs(para, runs, where)
            lines_in.append(r)
        prev = r
    close()
    if heading:
        blocks.append(('h', heading))
    # captions: a caption begins with its number and a tab ("4. (1) Fragmenty")
    cap, prev = None, None
    for r in captions:
        t0 = ''.join(s['text'] for s in r['spans'])
        if cap is None or re.match(r'\s*\d+\.\t', t0) or r['y'] - prev['y'] > 16:
            if cap:
                blocks.append(('c', cap))
            cap = list(r['runs'])
        else:
            cap = join_runs(cap, r['runs'], where)
        prev = r
    if cap:
        blocks.append(('c', cap))

    # notes
    notes_here = []
    for r in small:
        k = note_start(r)
        runs = r['runs']
        if k:
            # drop the number and the tab
            t0 = runs[0].text
            m = re.match(r'\s*\d+\t\s*', t0)
            runs = [Run(t0[m.end():], runs[0].it, runs[0].bold)] + runs[1:]
            note = [k, runs]
            notes_here.append(note)
            pending[0] = note
        else:
            target = pending[0]
            if target is None:
                REPORT.append(f'{where}: a note line with no note: {"".join(x.text for x in runs)[:60]}')
                continue
            target[1] = join_runs(target[1], runs, where)
    return blocks, notes_here


def fmt_para(text):
    # a paragraph beginning "12." would be taken for a numbered list
    text = re.sub(r'^(\d+)\.(?=\s)', r'\1\\.', text)
    text = re.sub(r'^([-+*])(?=\s)', r'\\\1', text)
    return text


def main():
    import fitz
    doc = fitz.open(sys.argv[1])
    SEEN.update(words_inside(doc))
    # the note numbers: every number that begins a note line
    notes_all = set()
    for n, page in enumerate(doc, 1):
        for r in rows_of(page):
            if r['size'] == 8.5:
                k = note_start(r)
                if k:
                    notes_all.add(k)
    pending = [None]
    pages = []
    for n, page in enumerate(doc, 1):
        if n in SKIP:
            continue
        blocks, notes_here = page_items(page, n, notes_all, pending)
        pages.append((n, blocks, notes_here))
    # notes are rendered after all pages are read, since a note may run on
    rendered = []
    for n, blocks, notes_here in pages:
        parts = []
        for kind, payload in blocks:
            if kind == 'h':
                parts.append(['h', '# ' + payload])
            elif kind == 't':
                parts.append(['t', table_html(doc[n - 1], payload, notes_all, f'p. {n}')])
            else:
                para = render(payload, notes_all)
                if n in FLAT_MARKS and FLAT_MARKS[n][0] in para:
                    old, new, k = FLAT_MARKS[n]
                    para = para.replace(old, new)
                    LAST[0] = max(LAST[0], k)
                parts.append([kind, para])
        for k, runs in notes_here:
            parts.append(['n', f'[^{k}]: ' + render(runs, notes_all)])
        rendered.append((n, parts))
    # a word divided over two pages is given whole on the first
    # (pages holding only an illustration and its caption may stand between)
    for i, (n, a) in enumerate(rendered):
        last = [p for p in a if p[0] == 'p']
        if not last or not re.search(rf'[{UPPER}{LOWER}]-\**$', last[-1][1]):
            continue
        for m, b in rendered[i + 1:]:
            if any(p[0] == 'p' for p in b):
                break
        else:
            continue
        b = [p for p in b if p[0] != 'c']
        if b[0][0] != 'p':
            continue
        first = b[0][1]
        word = re.match(r'\S+', first).group(0)
        m1 = re.search(rf'([{UPPER}{LOWER}]+)-(\**)$', last[-1][1])
        left, star = m1.group(1), m1.group(2)
        m2 = re.match(rf'(\**)([{UPPER}{LOWER}]*)', word)
        lead, right = m2.group(1), m2.group(2)
        if not right or not right[0].islower():
            continue
        keep = SEEN[(left + '-' + right).lower()] or compound(left, right)
        base = last[-1][1][:m1.end(1)] + ('-' if keep else '')
        if star and lead == star:            # an italic word: one run, not two
            last[-1][1] = base + word[len(lead):]
        else:
            last[-1][1] = base + star + word
        b[0][1] = first[len(word):].lstrip()
        REPORT.append(f'pp. {n}-{m}: {left}-|{right} -> {left}{"-" if keep else ""}{right}, on p. {n}')
    # an italic run that crosses a page end is closed on the first page and
    # opened again on the next, so that each page's Markdown stands alone
    for (n, a), (m, b) in zip(rendered, rendered[1:]):
        last = [p for p in a if p[0] == 'p']
        nxt = [p for p in b if p[0] == 'p']
        if last and nxt and len(re.findall(r'(?<!\*)\*(?!\*)', last[-1][1])) % 2:
            last[-1][1] += '*'
            nxt[0][1] = '*' + nxt[0][1]
            REPORT.append(f'pp. {n}-{m}: italic carried over the page end')
    out, front = [], []
    for n, parts in rendered:
        text = '\n\n'.join(fmt_para(t) if k in 'pc' else t for k, t in parts if t.strip())
        if n in FRONT:
            front.append(text)
        else:
            out.append(f'[p. {n}]\n\n{text}\n' if text else f'[p. {n}]\n')
    doc_text = '\n\n'.join(front) + '\n\n' + '\n'.join(out)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(doc_text)
    print('wrote', OUT, len(notes_all), 'notes')
    if '--report' in sys.argv:
        for line in REPORT:
            print(line)
    if '--figures' in sys.argv:
        from PIL import Image
        os.makedirs(FIG, exist_ok=True)
        for n in FIGURES:
            page = doc[n - 1]
            zoom = 1100 / page.rect.width
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
            im.save(os.path.join(FIG, f'{n}.jpg'), quality=82, optimize=True)
        print('figures:', ' '.join(f'"{n}": "{n}.jpg"' for n in FIGURES))


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
