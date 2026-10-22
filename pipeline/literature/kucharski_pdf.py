# -*- coding: utf-8 -*-
"""
Kucharski (2023): the journal's PDF to literature/kucharski2023/original.md
(2026-10-22).

    python pipeline/literature/kucharski_pdf.py <the PDF> [--report] [--check]

The PDF ("12+Robert+Kucharski.pdf" in the editor's Downloads folder) is the
printed article as the journal set it (Consilium Iuridicum 1(3-4) 2022,
pp. 226-253, DOI 10.52097/ci.5671, CC BY 4.0). Its text layer is the article's
text. The whole article is brought in (the editor's word of 2026-10-22); the
three pictures (Ryc. 1-3) are not rendered (the editor's word), their captions
and "Źródło:" lines stay, being text.

What this script does to the text layer, and nothing else:
- each page is opened with "[p. N]", N the printed page read from the page's
  foot (PDF page 1 is p. 226). The running head (the author or the title,
  y < 130) and the foot (the journal's name and the page number, y > 670) are
  left out;
- the lines of a paragraph are joined. A paragraph begins at a line indented
  by the article's indent (x >= 130) when the line before ends a sentence, or
  after a heading, a caption, a "Źródło:" line or a list; or at a line after a
  short one that ends a sentence (the text is justified, so a short line that
  ends a sentence ends a paragraph; the article sets its later paragraphs
  flush, without the indent, and marks them so). A line is never a paragraph's
  end when it ends in a word divided at the line's end. A paragraph runs on
  over a page's end. Every break the script decided without an indent to show
  it is listed by --report;
- a word divided at the end of a line is joined again. A hyphen is kept where
  the joined form is a compound the article prints elsewhere within a line, or
  where a number or a capital stands at the break. Every break the script
  decided without seeing the word elsewhere is listed by --report;
- headings become "# ...": the title and the English title (15.5-point, their
  two lines joined), VARIA (16-point), the section headings 1 to 4 and their
  subsections 3.1 to 3.7, and Streszczenie, Słowa kluczowe, Bibliografia,
  Abstract and Key words (11- and 12-point). The byline ("Robert Kucharski",
  12-point with the raised note 1) is a paragraph, not a heading;
- the notes are at the foot of each page, numbered through the article (1 to
  45). A note's raised number in the text becomes "[^n]" set against the word
  it follows (the layer's spaces there are the setting's, not the text's), and
  the note "[^n]: ..." at the end of its page. The raised marks run 1 to 45 in
  order; the script checks this;
- the author names in the notes are printed letterspaced ("K u c h a r s k i"):
  the spaces are the setting's, not the word's, and are taken out (every such
  join is listed by --report). Italics become *...*. The dash glyph of the
  Symbol font (F02D) is the article's "–"; on the ORCID line of note 1 it is
  the hyphen of 0000-0002-2279-9496 and is set so;
- the list items (the seven lines of pp. 240-241 that the print begins with an
  en-dash) keep their dash and stand each as its own paragraph, their run-on
  lines joined;
- the captions of the three pictures and their "Źródło:" lines are text, in
  their place;
- the numbered entries of the Bibliografia are kept with their numbers
  ("1. Balzer O., ..."), the numbers escaped ("1\\.") so that Markdown does
  not take them for a list. The text is otherwise unchanged, its slips
  included (the Bibliografia prints Kutrzeba's book twice, items 15 and 16).

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
OUT = os.path.join(ROOT, 'literature', 'kucharski2023', 'original.md')

SPACE_CHARS = ' \t\u00a0'
SPACES = re.compile(r'[ \t\u00a0\u2009\u202f]+')
UPPER = 'A-ZĄĆĘŁŃÓŚŹŻ'
LOWER = 'a-ząćęłńóśźż'
DASH = '\uf02d'                    # the Symbol font's dash glyph
ORCID = '0000\u20130002\u20132279\u20139496'
SENT_END = re.compile(r'[.!?\u2026]["”»\)\]]*\s*$')
BIB_NUM = re.compile(r'^(\d+)\.\s*(.*)$')

REPORT = []
MARKS = []                         # the note marks, in the order met
SEEN = Counter()                   # every word the article prints within a line


class Run:
    __slots__ = ('text', 'it', 'sup')

    def __init__(self, text, it=False, sup=False):
        self.text, self.it, self.sup = text, it, sup


def unspaced(t):
    """A letterspaced word ("K u c h a r s k i"): the single letters separated
    by single spaces are one word - but only where the joined form is a word
    the article prints elsewhere within a line, so an initial left loose by
    the setting ("M B o r u c k i", note 36) keeps its spaces."""
    toks = t.split(' ')
    out, run = [], []

    def flush():
        if len(run) >= 3:
            cand = ''.join(run)
            if cand.strip(',.').lower() in SEEN:
                REPORT.append('letterspaced name joined: ' + cand)
                out.append(cand)
            else:
                out.extend(run)
        else:
            out.extend(run)
        run.clear()
    for tok in toks:
        stripped = tok.rstrip(',')
        tail = tok[len(stripped):]
        if stripped and len(stripped) == 1 and stripped.isalpha() and not tail:
            run.append(stripped)
            continue
        if run and tail and len(stripped) == 1 and stripped.isalpha():
            run.append(stripped + tail)          # the last letter with its point
            flush()
            continue
        flush()
        out.append(tok)
    flush()
    return ' '.join(out)


def span_runs(spans):
    """A line's spans as runs; where the page leaves a gap between two spans
    and gives no space, a space is put in. A letterspaced span is joined."""
    out, prev = [], None
    for s in spans:
        t = s['text'].replace(DASH, '\u2013').replace('\u00ad', '')
        t = unspaced(t) if ' ' in t else t
        if not t:
            continue
        sup = bool(s['flags'] & 1) and s['size'] < 9
        if (prev is not None and out and s['bbox'][0] - prev['bbox'][2] > 1.5 and not sup
                and not out[-1].text.endswith(SPACE_CHARS) and not t.startswith(SPACE_CHARS)):
            out[-1].text += ' '
        out.append(Run(t, 'Italic' in s['font'], sup))
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
            rows.append({'y': round(l['bbox'][1]), 'x0': round(l['bbox'][0]),
                         'x1': round(l['bbox'][2]),
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
        b = [Run(rt, first.it, first.sup)] + list(b[1:])
        return a + b
    if lt.endswith('\u2013') and not last.sup:
        # an en-dash at the line's end: a range divided ("(1454–" / "1772)")
        rt = first.text.lstrip(' ')
        right = re.match(r'\d+', rt)
        if right and lt[len(lt.rstrip(' ')) - 2].isdigit():
            last.text = lt.rstrip(' ')
            b = [Run(rt, first.it, first.sup)] + list(b[1:])
            return a + b
    if not last.text.endswith(' ') and not first.text.startswith(' '):
        last.text = last.text + ' '
    return a + list(b)


def render(runs):
    """Runs to Markdown: italics *...*; raised runs turned into note marks,
    set against the word before them."""
    out = []
    for r in runs:
        if out and out[-1].sup and r.sup:
            out[-1] = Run(out[-1].text + r.text, sup=True)
        elif out and not r.sup and not out[-1].sup and out[-1].it == r.it:
            out[-1] = Run(out[-1].text + r.text, r.it)
        else:
            out.append(Run(r.text, r.it, r.sup))
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
        if not r.it or not t.strip():
            text += t
            continue
        lead = t[:len(t) - len(t.lstrip(' '))]
        trail = t[len(t.rstrip(' ')):]
        text += lead + '*' + t.strip(' ') + '*' + trail
    return SPACES.sub(' ', text).strip()


def fmt_para(text):
    # a paragraph beginning "12." would be taken for a numbered list
    text = re.sub(r'^(\d+)\.(?=\s)', r'\1\\.', text)
    text = re.sub(r'^([-+*])(?=\s)', r'\\\1', text)
    return text


def main():
    import fitz
    pdf = sys.argv[1]
    doc = fitz.open(pdf)

    # every word the article prints within a line, for the hyphen decisions
    SEEN.clear()
    for page in doc:
        for line in page.get_text().split('\n'):
            line = line.replace(DASH, '\u2013')
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
                if l['bbox'][1] > 670:
                    t = ''.join(s['text'] for s in l['spans']).strip()
                    if t.isdigit():
                        printed = int(t)
        assert printed == n + 225, f'PDF page {n}: printed page {printed}'
        rows = [r for r in rows_of(page) if 130 < r['y'] <= 670]
        right = max((r['x1'] for r in rows if r['size'] >= 10.5), default=0)
        pages.append((printed, rows, right))

    # the state of the text runs over the pages: a paragraph goes on
    para = None           # the runs of the paragraph being gathered
    kind = 'p'            # p, list, bib, cap
    prev = None           # the previous body row, for the break rules
    bib = False           # in the Bibliografia's entries
    blocks_of = []        # per page: [(kind, payload)]

    def short(r):
        return r['x1'] < right - 20

    def ended():
        if para is None or not para:
            return False
        return bool(SENT_END.search(para[-1].text.rstrip()))

    def starts_paragraph(r):
        if para is None:
            return True
        if para[-1].text.rstrip().endswith('-') and not r['runs'][0].sup:
            return False     # a word divided at the line's end
        if prev is not None and short(prev) and ended():
            if r['x0'] < 130:
                REPORT.append(f'p. {printed}: paragraph begins flush: '
                              + r['runs'][0].text[:40])
            return True
        if r['x0'] >= 130:
            return ended()
        return False

    for printed, rows, right in pages:
        blocks = []
        blocks_of.append(blocks)
        note_open = None       # [n, runs] the note being gathered

        def close():
            nonlocal para, kind
            if para is not None:
                blocks.append((kind, para))
                para = None
                kind = 'p'

        for r in rows:
            runs, size, y = r['runs'], r['size'], r['y']
            text0 = runs[0].text.lstrip() if runs else ''
            # the notes: small type, but the "Źródło:" lines of the pictures
            if size < 10 and not text0.startswith('Źródło'):
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
                    rest = SPACES.sub(' ', ''.join(s['text'] for s in r['spans']))
                    rest = re.sub(r'^\s*\d+\s+', '', rest).strip()
                    rest = unspaced(rest)
                    note_open = [num, [Run(rest, 'Italic' in r['spans'][-1]['font'])]]
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
            # the heading: bold, 11 points and more, without a raised mark
            # (the byline carries note 1)
            if size >= 11 and any('Bold' in s['font'] for s in r['spans']) \
                    and not any(x.sup for x in runs):
                close()
                txt = SPACES.sub(' ', ''.join(
                    s['text'].replace(DASH, '\u2013') for s in r['spans'])).strip()
                if blocks and blocks[-1][0] == 'h' and y - HLAST[0] <= 25 \
                        and abs(HLAST[1] - size) < 1:
                    blocks[-1][1].append(txt)     # a title's second line
                else:
                    blocks.append(('h', [txt]))
                HLAST[:] = [y, size]
                bib = (txt == 'Bibliografia')
                prev = None
                continue
            # a list item: the print's en-dash of the Symbol font
            if size >= 10.5 and r['x0'] < 130 and 'Symbol' in r['spans'][0]['font'] \
                    and len(r['spans'][0]['text'].strip()) <= 1:
                close()
                para = [Run('\u2013 ', runs[0].it)] + list(runs[1:])
                kind = 'list'
                prev = r
                continue
            if text0.startswith('Ryc.'):
                close()
                para, kind = list(runs), 'cap'
                prev = r
                continue
            if text0.startswith('Źródło'):
                close()
                para, kind = list(runs), 'cap'
                prev = None
                continue
            if bib:
                m = BIB_NUM.match(text0) if r['x0'] < 130 else None
                if m:
                    close()
                    para, kind = list(runs), 'bib'
                    prev = r
                    continue
                if para is None or kind != 'bib':
                    REPORT.append(f'p. {printed}: a bibliography line with no entry: '
                                  + text0[:40])
                    close()
                    para, kind = list(runs), 'bib'
                else:
                    para = join_runs(para, runs, printed)
                prev = r
                continue
            if starts_paragraph(r):
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
        last = next((b for b in reversed(blocks) if b[0] in ('p', 'list')), None)
        if not last:
            continue
        runs = last[1]
        lt = runs[-1].text.rstrip(' ')
        m = re.search(rf'([{UPPER}{LOWER}]+)-$', lt)
        if not m:
            continue
        left = m.group(1)
        nxt = next((b for b in blocks_of[i + 1] if b[0] in ('p', 'list')), None)
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
                text = render(runs)
                if ORCID in text:
                    text = text.replace(ORCID, ORCID.replace('\u2013', '-'))
                parts.append(f'[^{n}]: ' + text)
            else:
                text = render(payload)
                parts.append(fmt_para(text))
        rendered.append((printed, parts))

    doc_text = '\n'.join(
        '\n\n'.join([f'[p. {printed}]'] + [p for p in parts if p.strip()]) + '\n'
        for printed, parts in rendered)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(doc_text)
    print('wrote', OUT, '-', len(MARKS), 'note marks, expected 45')
    if MARKS != list(range(1, 46)):
        print('NOTE MARKS OUT OF ORDER:', MARKS)
    if '--report' in sys.argv:
        print('\n--- report ---')
        for line in REPORT:
            print(line)
    if '--check' in sys.argv:
        check(doc)


HLAST = [0, 0]         # the last heading's y and size, for joining a title's lines


CARRIES = []           # [(page index, left, right)] words given whole on the page before


def norm(t):
    """The stream of letters a text carries: layout's spaces, hyphens, the
    marks and the Markdown's signs all out."""
    t = re.sub(r'^\[\^\d+\]:\s*', '', t, flags=re.M)   # a note line's prefix
    t = re.sub(r'\[\^\d+\]', '', t)                    # a mark in the text
    t = re.sub(r'^\[p\. \d+\]$', '', t, flags=re.M)
    t = re.sub(r'^#+\s*', '', t, flags=re.M)
    t = t.replace('*', '').replace('\\.', '.')
    t = t.replace('\u2013', '').replace(DASH, '')
    t = re.sub(r'[-\s]', '', t)
    return t


def check(doc):
    """Every page's letters, as the layer carries them, against original.md -
    the body and the notes apart, since a word given whole on the page before
    crosses from one body to the next."""
    want_body, want_notes = [], []
    for n, page in enumerate(doc, 1):
        body, notes = [], []
        for b in page.get_text('dict')['blocks']:
            if b['type'] != 0:
                continue
            for l in b['lines']:
                y = l['bbox'][1]
                if y <= 130 or y > 670:
                    continue
                spans = sorted(l['spans'], key=lambda s: s['bbox'][0])
                stream = notes if (max(round(s['size'], 1) for s in spans) < 10
                                   and not ''.join(s['text'] for s in spans).lstrip()
                                   .startswith('Źródło')) else body
                for s in spans:
                    if bool(s['flags'] & 1) and s['size'] < 9:
                        continue             # a raised note mark
                    if round(s['size'], 1) <= 6.5:
                        continue             # a note's number
                    stream.append(s['text'].replace(DASH, '\u2013'))
        want_body.append(norm(''.join(body)))
        want_notes.append(norm(''.join(notes)))
    for i, left, right in CARRIES:
        want_body[i] += right                 # the word given whole on p. i
        want_body[i + 1] = want_body[i + 1][len(right):]
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
            print(f'CHECK p. {i + 226} ({what}): differs at offset {j}:')
            print('  layer :', w[max(0, j - 40):j + 40])
            print('  output:', g[max(0, j - 40):j + 40])
    print('CHECK:', 'all 28 pages match' if not bad else f'{bad} checks differ')


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
