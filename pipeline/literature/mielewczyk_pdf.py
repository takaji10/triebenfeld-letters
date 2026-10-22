# -*- coding: utf-8 -*-
"""
Mielewczyk (2017): the journal's PDF to literature/mielewczyk2017/original.md
(2026-10-22).

    python pipeline/literature/mielewczyk_pdf.py <the PDF> [--report] [--check]

The PDF ("ZDK_21_041-057.pdf" in the editor's Downloads folder) is the printed
article as the annual set it (Z Dziejów Kartografii, tom XXI, 2017, s. 41-57,
Instytut Historii Nauki PAN; the open-access copy stands at
http://www.maphist.waw.pl/wp-content/uploads/2020/05/ZDK_21_041-057.pdf). Its
text layer is the article's text. The whole article is brought in (the
editor's word of 2026-10-22); the fourteen figures (Ryc. 1-14) are not
rendered (the editor's word), their captions stay, being text.

What this script does to the text layer, and nothing else:
- each page is opened with "[p. N]", N the printed page read from the page's
  foot (PDF page 1 is p. 41). The running head (the author or the title, y <=
  60; on p. 1 the journal's own block) and the foot (the printed page number,
  y > 620) are left out;
- the lines of a paragraph are joined. A paragraph begins at a line indented
  by the article's indent (x >= 84) when the line before ends a sentence, or
  after a heading, a caption, the front matter or the bibliography; or at a
  line after a short one that ends a sentence (the text is justified, so a
  short line that ends a sentence ends a paragraph; the article sets its
  first paragraph flush, without the indent, and marks them so). A line is
  never a paragraph's end when it ends in a word divided at the line's end.
  A paragraph runs on over a page's end and over the pages that carry only
  figures. Every break the script decided without an indent to show it is
  listed by --report;
- a word divided at the end of a line is joined again. A hyphen is kept where
  the joined form is a compound the article prints elsewhere within a line,
  or where a number or a capital stands at the break. Every break the script
  decided without seeing the word elsewhere is listed by --report;
- the ligature glyph "ﬁ" stands for "fi" of one word, and the space the layer
  keeps after it is the setting's, not the word's ("Kartograﬁ i" =
  "Kartografii", "graﬁ cznie" = "graficznie", "ﬁ elds" = "fields"): the space
  is taken out and every such join is listed by --report;
- headings become "# ...": the Polish title and the English title (14-point,
  their lines joined), the section headings 1 to 3 and their subsections 1.1
  to 1.2, and Literatura and Źródła kartograficzne (12-point). The author's
  name (13-point) and his affiliation and e-mail (9-point, centred) are
  paragraphs, not headings;
- the front matter and the English summary ("Zarys treści:", "Słowa
  kluczowe:", "Summary:", "Keywords:") are paragraphs; their bold labels are
  set in **bold** as the print sets them;
- the notes are at the foot of each page, numbered through the article (1 to
  19). A note's raised number in the text becomes "[^n]" set against the word
  it follows (the layer's spaces there are the setting's, not the text's),
  and the note "[^n]: ..." at the end of its page. The raised marks run 1 to
  19 in order; the script checks this;
- the captions of the figures (Ryc. 1-14, 9-point, the journal's condensed
  sans) are text, in their place, each caption its own paragraph (a caption's
  second line joined, a divided word joined again);
- the entries of Literatura and of Źródła kartograficzne are unnumbered:
  each begins at the left margin (x < 75), its run-over lines are indented
  (x >= 75) and joined to it. The text is otherwise unchanged, its slips
  included (the caption of Ryc. 6 reads 1866 where the body reads 1886; the
  note 4 reads "t. 3" where Literatura reads "t. 2"; Literatura reads
  "gospodarstwa wojskowego" for Burszta's title where note 3 reads
  "wiejskiego"; "Terra Pisdrensis dawnej i dziś" in Literatura, "dawniej i
  dziś" in note 6; the map titles' own spellings, "Płan Kolonii",
  "Kaliszskoj Gubiernii", "Jeometry Gotzkejn", the repeated scale "20 000" of
  the Grabienice entry, the unfinished year "192…" of the Lisewo entry).

With --check the script rebuilds, from its own reading of the text layer, the
stream of letters each page carries (the raised marks, the note numbers, the
head, the foot and the layout's spaces left out) and asserts that the same
stream, read back out of original.md, is unchanged.
"""
import io
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'literature', 'mielewczyk2017', 'original.md')

SPACE_CHARS = ' \t\u00a0'
SPACES = re.compile(r'[ \t\u00a0\u2009\u202f]+')
UPPER = 'A-ZĄĆĘŁŃÓŚŹŻ'
LOWER = 'a-ząćęłńóśźż'
LIG = '\ufb01'                     # the layer's "fi" ligature, always of one word
SENT_END = re.compile(r'[.!?\u2026]["”»\)\]]*\s*$')
BOLD_LABELS = ('Zarys treści', 'Słowa kluczowe', 'Summary', 'Keywords')

REPORT = []
MARKS = []                         # the note marks, in the order met
SEEN = Counter()                   # every word the article prints within a line


class Run:
    __slots__ = ('text', 'it', 'sup', 'b')

    def __init__(self, text, it=False, sup=False, b=False):
        self.text, self.it, self.sup, self.b = text, it, sup, b


def deligature(t):
    """The "ﬁ" ligature is one word's "fi"; the space the layer keeps after it
    is the setting's. Every join is listed, so a real "fi i" would be seen."""
    t = t.replace(LIG, 'fi')
    out = []
    for m in re.finditer(r'fi (?=[%s])' % LOWER, t):
        out.append(t[max(0, m.start() - 12):m.end() + 12])
    if out:
        REPORT.append('ligature space taken out: ' + ' | '.join(out))
    return re.sub(r'fi ([%s])' % LOWER, r'fi\1', t)


def span_runs(spans):
    """A line's spans as runs; where the page leaves a gap between two spans
    and gives no space, a space is put in."""
    out, prev = [], None
    for s in spans:
        t = deligature(s['text'])
        if not t.strip(SPACE_CHARS):
            continue
        sup = bool(s['flags'] & 1) and s['size'] < 9
        if (prev is not None and out and s['bbox'][0] - prev['bbox'][2] > 1.5 and not sup
                and not out[-1].text.endswith(SPACE_CHARS) and not t.startswith(SPACE_CHARS)):
            out[-1].text += ' '
        out.append(Run(t, 'Italic' in s['font'], sup, 'Bold' in s['font']))
        prev = s
    return out


def rows_of(page):
    """Lines in reading order: dict(y, x0, x1, size, runs, spans). Lines that
    stand beside each other on one baseline are merged."""
    rows = []
    for b in page.get_text('dict')['blocks']:
        if b['type'] != 0:
            continue
        for l in b['lines']:
            spans = [s for s in l['spans'] if s['text'].strip(SPACE_CHARS)]
            if not spans:
                continue
            rows.append({'y': round(l['bbox'][1]), 'x0': round(l['bbox'][0], 1),
                         'x1': round(l['bbox'][2], 1),
                         'size': max(round(s['size'], 1) for s in spans),
                         'spans': spans})
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
            how = 'keep'
        elif left.isdigit() and right.isdigit():
            how = 'join'                 # a numeric range divided at the line's end
        elif not left or not right or left[-1].isdigit() or right[0].isdigit() or right[0].isupper():
            how = 'keep'
        elif SEEN[(left + '-' + right).lower()]:
            how = 'keep'
        elif SEEN[(left + right).lower()]:
            how = 'join'
        else:
            how = 'join'
            REPORT.append(f'p. {where}: {left}-|{right} -> {left}{right}')
        if how == 'join':
            last.text = lt[:-1]
        else:
            last.text = lt
        b = [Run(rt, first.it, first.sup, first.b)] + list(b[1:])
        return a + b
    if not last.text.endswith(' ') and not first.text.startswith(' '):
        last.text = last.text + ' '
    return a + list(b)


def render(runs):
    """Runs to Markdown: italics *...*, bold **...**; raised runs turned into
    note marks, set against the word before them."""
    out = []
    for r in runs:
        if out and out[-1].sup and r.sup:
            out[-1] = Run(out[-1].text + r.text, sup=True)
        elif out and not r.sup and not out[-1].sup and out[-1].it == r.it \
                and out[-1].b == r.b:
            out[-1] = Run(out[-1].text + r.text, r.it, b=r.b)
        else:
            out.append(Run(r.text, r.it, r.sup, r.b))
    text = ''
    for r in out:
        t = SPACES.sub(' ', r.text)
        if not t.strip():
            continue
        if r.sup:
            digits = re.search(r'\d+', t)
            if digits:
                n = int(digits.group(0))
                MARKS.append(n)
                pre, post = t[:digits.start()], t[digits.end():]
                text = text.rstrip(' ') + f'[^{n}]' + post.lstrip(' ')
            else:
                text += t
            continue
        if not (r.it or r.b) or not t.strip():
            text += t
            continue
        lead = t[:len(t) - len(t.lstrip(' '))]
        trail = t[len(t.rstrip(' ')):]
        inner = t.strip(' ')
        if r.it:
            text += lead + '*' + inner + '*' + trail
        else:
            text += lead + '**' + inner + '**' + trail
    return SPACES.sub(' ', text).strip()


def main():
    import fitz
    pdf = sys.argv[1]
    doc = fitz.open(pdf)

    # every word the article prints within a line, for the hyphen decisions
    SEEN.clear()
    for page in doc:
        for line in page.get_text().split('\n'):
            line = deligature(line)
            for w in re.findall(rf'[{UPPER}{LOWER}A-Za-z]+(?:-[{UPPER}{LOWER}A-Za-z]+)*', line):
                SEEN[w.lower()] += 1

    pages = []
    for n, page in enumerate(doc, 1):
        # the printed page number, from the foot
        printed = None
        for b in page.get_text('dict')['blocks']:
            if b['type'] != 0:
                continue
            for l in b['lines']:
                if l['bbox'][1] > 620:
                    t = ''.join(s['text'] for s in l['spans']).strip()
                    if t.isdigit():
                        printed = int(t)
        assert printed == n + 40, f'PDF page {n}: printed page {printed}'
        rows = [r for r in rows_of(page) if 60 < r['y'] <= 620]
        right = max((r['x1'] for r in rows if r['size'] >= 10.5
                     and 'TimesNewRoman' in r['spans'][0]['font']), default=0)
        pages.append((printed, rows, right))

    # the state of the text runs over the pages: a paragraph goes on
    para = None           # the runs of the paragraph being gathered
    kind = 'p'            # p, small, bib, cap
    prev = None           # the previous body row, for the break rules
    bib = False           # in the Literatura / Źródła kartograficzne entries
    blocks_of = []        # per page: [(kind, payload)]

    def short(r):
        return r['x1'] < right - 20

    def ended():
        if para is None or not para:
            return False
        for run in reversed(para):
            if not run.sup:
                return bool(SENT_END.search(run.text.rstrip()))
        return False

    def starts_paragraph(r):
        if para is None:
            return True
        if para[-1].text.rstrip().endswith('-') and not r['runs'][0].sup:
            return False     # a word divided at the line's end
        if prev is not None and short(prev) and ended():
            return True
        if r['x0'] >= 84:
            return ended()
        return False

    for printed, rows, right in pages:
        blocks = []
        blocks_of.append(blocks)
        note_open = None       # [n, runs] the note being gathered
        # an entry whose run-over lines crossed the page: the page before ended
        # in a bibliography block, still open
        prev_blocks = blocks_of[-2] if len(blocks_of) > 1 else None
        carry_reported = False

        def close():
            nonlocal para, kind
            if para is not None:
                blocks.append((kind, para))
                para = None
                kind = 'p'

        for r in rows:
            runs, size, y = r['runs'], r['size'], r['y']
            text0 = runs[0].text.lstrip() if runs else ''
            fonts = [s['font'] for s in r['spans']]
            # the notes: 8-point Times
            if size < 9 and 'TimesNewRoman' in ' '.join(fonts):
                close()
                num = None
                for s in r['spans']:
                    if round(s['size'], 1) <= 6.5:
                        m = re.match(r'\s*(\d+)', s['text'])
                        if m:
                            num = int(m.group(1))
                            break
                if num is not None:
                    if note_open is not None:
                        blocks.append(('note', note_open))
                    # the note's first line: its runs without the number's span
                    note_spans = [s for s in r['spans'] if round(s['size'], 1) > 6.5]
                    note_open = [num, span_runs(note_spans) if note_spans else []]
                else:
                    if note_open is None:
                        raise SystemExit(
                            f'p. {printed}: a note line with no note: {text0!r}')
                    note_open[1] = join_runs(note_open[1], runs, printed)
                prev = None
                continue
            if note_open is not None:
                blocks.append(('note', note_open))
                note_open = None
            # the title: 14-point, the annual's display face
            if size >= 13.5:
                close()
                txt = SPACES.sub(' ', ''.join(
                    deligature(s['text']) for s in r['spans'])).strip()
                if blocks and blocks[-1][0] == 'h' and y - HLAST[0] <= 25:
                    blocks[-1][1].append(txt)     # a title's next line
                else:
                    blocks.append(('h', [txt]))
                HLAST[:] = [y, size]
                bib = False
                prev = None
                continue
            # the author: 13-point
            if size >= 12.5:
                close()
                para, kind = list(runs), 'p'
                prev = None
                continue
            # the captions of the figures: the condensed sans, 9-point
            if size < 10.5 and any('Swis' in f for f in fonts):
                if para is not None and kind == 'cap' and prev is not None \
                        and y - prev['y'] <= 15:
                    para = join_runs(para, runs, printed)
                else:
                    close()
                    para, kind = list(runs), 'cap'
                prev = r
                continue
            # the front matter and the English summary: 9-point Times
            if size < 10.5:
                label = text0.startswith(BOLD_LABELS) or text0.startswith('Muzeum') \
                    or text0.startswith('E-mail:')
                if label or para is None or kind != 'small' \
                        or (prev is not None and y - prev['y'] > 16) \
                        or (r['x0'] >= 80 and ended()):
                    close()
                    para, kind = list(runs), 'small'
                else:
                    para = join_runs(para, runs, printed)
                prev = r
                continue
            # a heading: the display face, 11 points and more, without a mark
            if size >= 10.5 and any('ZapfHumnstEU-Bold' in f for f in fonts) \
                    and not any(x.sup for x in runs):
                close()
                txt = SPACES.sub(' ', ''.join(
                    deligature(s['text']) for s in r['spans'])).strip()
                if blocks and blocks[-1][0] == 'h' and y - HLAST[0] <= 25:
                    blocks[-1][1].append(txt)     # a title's next line
                else:
                    blocks.append(('h', [txt]))
                HLAST[:] = [y, size]
                bib = (txt in ('Literatura', 'Źródła kartograficzne'))
                prev = None
                continue
            if bib:
                # an entry begins at the left margin; its run-over lines stand in
                if r['x0'] < 75:
                    close()
                    para, kind = list(runs), 'bib'
                elif para is not None and kind == 'bib':
                    para = join_runs(para, runs, printed)
                elif para is None and prev_blocks and prev_blocks[-1][0] == 'bib':
                    # the entry's run-over lines crossed the page: they join it
                    joined = join_runs(prev_blocks[-1][1], runs, printed)
                    prev_blocks[-1] = ('bib', joined)
                    BIB_CARRIES.append((printed - 1 - 41,
                                        ''.join(s['text'] for s in r['spans'])))
                    if not carry_reported:
                        REPORT.append(f'pp. {printed - 1}-{printed}: the entry\'s '
                                      'run-over lines joined across the pages')
                        carry_reported = True
                else:
                    close()
                    para, kind = list(runs), 'bib'
                prev = r
                continue
            if kind != 'p' or starts_paragraph(r):
                close()
                para, kind = list(runs), 'p'
            else:
                if para is None:
                    REPORT.append(f'p. {printed}: a body line with no paragraph: '
                                  + text0[:40])
                    para, kind = list(runs), 'p'
                else:
                    para = join_runs(para, runs, printed)
            prev = r
        close()
        if note_open is not None:
            blocks.append(('note', note_open))
            note_open = None

    # a word divided over two pages is given whole on the first: the page's
    # last paragraph ends in the word's first half, the next page's first
    # paragraph begins with the second (chodyla_pdf.py's rule)
    for i, (printed, blocks) in enumerate(zip([p for p, _, _ in pages], blocks_of[:-1])):
        last = next((b for b in reversed(blocks) if b[0] in ('p', 'small')), None)
        if not last:
            continue
        runs = last[1]
        lt = runs[-1].text.rstrip(' ')
        m = re.search(rf'([{UPPER}{LOWER}]+)-$', lt)
        if not m:
            continue
        left = m.group(1)
        nxt = next((b for b in blocks_of[i + 1] if b[0] in ('p', 'small')), None)
        if not nxt:
            continue
        first = nxt[1][0]
        w = re.match(rf'[{UPPER}{LOWER}]+', first.text)
        if not w or not w.group(0)[:1].islower():
            continue
        right = w.group(0)
        keep = bool(SEEN[(left + '-' + right).lower()])
        runs[-1].text = lt[:m.start(1)] + left + ('-' if keep else '') + right
        rest = first.text[len(right):].lstrip(' ')
        if rest:
            first.text = rest
        else:
            nxt[1].pop(0)
            if not nxt[1]:
                blocks_of[i + 1].remove(nxt)
        REPORT.append(f'pp. {printed}-{printed + 1}: {left}-|{right} -> '
                      f'{left}{"-" if keep else ""}{right}, whole on p. {printed}')
        CARRIES.append((i, left, right))

    rendered = []
    for printed, blocks in zip([p for p, _, _ in pages], blocks_of):
        parts = []
        for kind_, payload in blocks:
            if kind_ == 'h':
                parts.append('# ' + ' '.join(payload))
            elif kind_ == 'note':
                n, runs = payload
                parts.append(f'[^{n}]: ' + render(runs))
            else:
                parts.append(render(payload))
        rendered.append((printed, parts))

    doc_text = '\n'.join(
        '\n\n'.join([f'[p. {printed}]'] + [p for p in parts if p.strip()]) + '\n'
        for printed, parts in rendered)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(doc_text)
    print('wrote', OUT, '-', len(MARKS), 'note marks, expected 19')
    if MARKS != list(range(1, 20)):
        print('NOTE MARKS OUT OF ORDER:', MARKS)
    if '--report' in sys.argv:
        print('\n--- report ---')
        for line in REPORT:
            print(line)
    if '--check' in sys.argv:
        check(doc)


HLAST = [0, 0]         # the last heading's y and size, for joining a title's lines

CARRIES = []           # [(page index, left, right)] words given whole on the page before

BIB_CARRIES = []       # [(page index, raw)] entry lines joined across the pages


def norm(t):
    """The stream of letters a text carries: layout's spaces, hyphens, the
    marks and the Markdown's signs all out."""
    t = re.sub(r'^\[\^\d+\]:\s*', '', t, flags=re.M)   # a note line's prefix
    t = re.sub(r'\[\^\d+\]', '', t)                    # a mark in the text
    t = re.sub(r'^\[p\. \d+\]$', '', t, flags=re.M)
    t = re.sub(r'^#+\s*', '', t, flags=re.M)
    t = t.replace('*', '').replace('**', '')
    t = t.replace(LIG, 'fi')
    t = re.sub(r'[-\s]', '', t)
    return t


def check(doc):
    """Every page's letters, as the layer carries them, against original.md -
    the body and the notes apart, since a word given whole on the page before
    crosses from one body to the next."""
    want_body, want_notes = [], []
    for n, page in enumerate(doc, 1):
        body, notes = [], []
        lines = []
        for b in page.get_text('dict')['blocks']:
            if b['type'] != 0:
                continue
            for l in b['lines']:
                if 60 < l['bbox'][1] <= 620:
                    lines.append(l)
        lines.sort(key=lambda l: (round(l['bbox'][1]), round(l['bbox'][0])))
        for l in lines:
            spans = sorted(l['spans'], key=lambda s: s['bbox'][0])
            size = max(round(s['size'], 1) for s in spans)
            stream = notes if (size < 9 and any('TimesNewRoman' in s['font'] for s in spans)) \
                else body
            for s in spans:
                if bool(s['flags'] & 1) and s['size'] < 9:
                    continue             # a raised note mark
                if round(s['size'], 1) <= 6.5:
                    continue             # a note's number
                stream.append(s['text'])
        want_body.append(norm(''.join(body)))
        want_notes.append(norm(''.join(notes)))
    for i, left, right in CARRIES:
        want_body[i] += right                 # the word given whole on p. i
        want_body[i + 1] = want_body[i + 1][len(right):]
    for i, raw in BIB_CARRIES:
        s = norm(raw)                         # the entry's run-over lines, joined
        want_body[i] += s                     # to the entry on the page before
        want_body[i + 1] = want_body[i + 1][len(s):]
    text = io.open(OUT, encoding='utf-8').read()
    parts = re.split(r'^\[p\. \d+\]$', text, flags=re.M)[1:]
    got_body, got_notes = [], []
    for p in parts:
        body, notes = [], []
        for line in p.split('\n'):
            (notes if re.match(r'^\[\^\d+\]: ', line) else body).append(line)
        got_body.append(norm('\n'.join(body)))
        got_notes.append(norm('\n'.join(notes)))
    if len(want_body) != len(got_body):
        print(f'CHECK: {len(want_body)} pages in the PDF, {len(got_body)} in original.md')
        return
    bad = 0
    for i, (wb, wn, gb, gn) in enumerate(zip(want_body, want_notes, got_body, got_notes)):
        for what, w, g in (('body', wb, gb), ('notes', wn, gn)):
            if w == g:
                continue
            bad += 1
            j = next((k for k in range(min(len(w), len(g))) if w[k] != g[k]),
                     min(len(w), len(g)))
            print(f'CHECK p. {i + 41} ({what}): differs at offset {j}:')
            print('  layer :', w[max(0, j - 40):j + 40])
            print('  output:', g[max(0, j - 40):j + 40])
    print('CHECK:', 'all 17 pages match' if not bad else f'{bad} checks differ')


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
