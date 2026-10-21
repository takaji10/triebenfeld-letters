# -*- coding: utf-8 -*-
"""Make literature/dean2012warthegau/original.md from the editor's PDF.

The PDF is the JSTOR download of the chapter "Warthegau Region (Reichsgau
Wartheland)" of The United States Holocaust Memorial Museum Encyclopedia of
Camps and Ghettos, 1933-1945, vol. II, part A (Indiana University Press,
2012), CC BY-NC-ND 4.0, in the editor's Downloads folder
("WARTHEGAUREGIONREICHSGAU-2012.pdf", 2026-10-21). Only the pages the editor
named are taken (PDF pages 3-8, 17, 26-28, 29-30, 32-33, 68-69, 89-90); the
printed page is the PDF page + 31. The PDF is not kept in the repository:
every page's foot names the address it was downloaded from.

What is done to the text layer, and why:

- Running heads, page feet and the JSTOR line are left out; pictures too
  (their credits are the lenders', not the book's licence). A caption is
  given as text after the text of its page.
- Each page is read left column, then right; the chapter's title and its
  first gazetteer line run across both columns and come first.
- Polish letters: the typesetting takes them from an accent font that
  stores each under its plain letter ("Łódz" is "Łód" and an accent-font
  "z"). ACCENT maps them back (ź, ń, ą, ę, ć, ś, ż, Ż, Ś, Ń). An accent-font
  letter not in the table stops the script. The print's own slips stay
  ("Łódż" once, in a note).
- Spaces: the text layer has spaces of no width after every hyphen and
  dash, in the "fi" and "fl" ligatures and before many words ("there  were").
  A space that starts where the next letter starts, or inside the letter
  before it, is dropped; a real space always leaves a gap.
- Hyphens at a line's end: the layer keeps a (zero-width) space after a
  real hyphen ("mid-", "good-", "SS-") and none after a break ("Ko-nin").
  So a hyphen followed by a space stays and the lines are joined without
  one; one without is a break, and the word is joined. A word broken over
  two included, consecutive pages is joined on the first.
- Paragraphs: a block whose first line is indented begins a paragraph;
  one that is not continues the paragraph before it (a column or page
  break). A block indented as a whole is a quotation (">"). Headings,
  NOTES, SOURCES, the gazetteer line and the author's name begin their own.
- Notes: superscript numbers become [^n], and each note of a NOTES list
  [^n]: (a new note where a line begins with the next number). The site
  links a marker to the first note of its number after it. Where an entry
  begins on these pages but its notes are on a page not taken (Ciechocinek,
  Sanniki, Zduńska Wola), its markers stay plain (<sup>n</sup>), so that
  none links to another entry's note.
- Web addresses: the print breaks them at dots and slashes and across
  lines; inside an address beginning "www" the spaces are dropped.
- CORRECTIONS: words the text layer has wrong, put right at the editor's
  word, each listed with its reason ("Betchatów" is Bełchatów).
- Italic as *...*, bold (SOURCES, the entry headings' run-ins) as **...**;
  the chapter's title "#", an entry's heading "##".

Usage: python pipeline/literature/warthegau_pdf.py <the PDF> [--check]
"""
import os
import re
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'literature', 'dean2012warthegau', 'original.md')

PAGES = [3, 4, 5, 6, 7, 8, 17, 26, 27, 28, 29, 30, 32, 33, 68, 69, 89, 90]
OFFSET = 31                      # printed page = PDF page + 31
TOP, FOOT = 56, 745              # running heads above, page feet below
MID = 286                        # the gutter between the columns
# Words the text layer has wrong, corrected at the editor's word; each must
# be found exactly once.
CORRECTIONS = [
    ('Betchatów', 'Bełchatów', 'the editor, 2026-10-21: "Betchatów should be '
     'Bełchatów" (p. 34, the list of the ghettos of Kreis Lask)'),
]
ACCENT = {'a': 'ą', 'c': 'ć', 'e': 'ę', 'n': 'ń', 's': 'ś', 'z': 'ź',
          '{': 'ż', 'Y': 'Ż', 'S': 'Ś', 'N': 'Ń',
          '-': '-', 'Ł': 'Ł', 'ł': 'ł'}


def chars_of(line):
    """The line's characters as (char, x0, x1, style), accents mapped."""
    out = []
    for s in line['spans']:
        f, size = s['font'], s['size']
        style = ''
        if 'Ital' in f:
            style = 'i'
        if 'Bold' in f:
            style = 'b'
        if size < 7 and 'Janson' in f:
            style = 'sup'
        for c in s['chars']:
            ch = c['c']
            if 'Accent' in f:
                if ch not in ACCENT:
                    raise SystemExit(f'accent-font letter {ch!r} not in ACCENT')
                ch = ACCENT[ch]
            ch = {'ﬁ': 'fi', 'ﬂ': 'fl'}.get(ch, ch)
            out.append([ch, c['bbox'][0], c['bbox'][2], style])
    # drop the spaces of no width
    keep = []
    for i, c in enumerate(out):
        if c[0] == ' ':
            nxt = out[i + 1] if i + 1 < len(out) else None
            prv = keep[-1] if keep else None
            if nxt is None or prv is None:
                keep.append(c)
                continue
            # spurious: after a space, a hyphen, a dash or an opening
            # bracket or quote, or starting inside the letter before; a real
            # space before a kerned capital ("Poylishe Yidn") may start where
            # the capital does, so the next letter alone does not decide
            # A space at a hyphenation point inside a word ("or ga nized",
            # "house holds") starts where the next letter starts; a real space
            # ends about where the next letter starts, even before a kerned
            # capital. So a space whose next letter begins in its first half
            # is spurious.
            if (prv[0] in ' -–—(“‘[/' or c[1] < prv[2] - 0.6
                    or nxt[1] - c[1] < 0.5 * (c[2] - c[1])):
                continue
        keep.append(c)
    return keep


def kind(line, size, font):
    if 'Eurostile' in font:
        if 'Bold' in font and size >= 14:
            return 'title'
        if 'Bold' in font and size >= 12:
            return 'heading'
        if 'Bold' in font and size >= 9.9:
            return 'notes'
        if size < 8.5:
            return 'caption'
        if 'Bold' not in font:
            return 'signature'
    return 'body'


def page_items(page):
    """Lines of a page in reading order, grouped by block."""
    items = []
    for b in page.get_text('rawdict')['blocks']:
        if b['type'] != 0:
            continue
        lines = [l for l in b['lines'] if TOP <= l['bbox'][1] < FOOT]
        if not lines:
            continue
        x0 = min(l['bbox'][0] for l in lines)
        x1 = max(l['bbox'][2] for l in lines)
        full = x0 < MID and x1 > MID + 20
        col = 0 if full else (1 if x0 < MID else 2)
        items.append({'col': col, 'y': lines[0]['bbox'][1], 'lines': lines,
                      'left': 42 if col < 2 else 291})
    items.sort(key=lambda it: (it['col'], it['y']))
    return items


class Para:
    def __init__(self, kind):
        self.kind = kind          # body, quote, title, heading, notes, note, caption, signature, gaz
        self.chars = []           # [ch, style]
        self.num = None           # a note's number
        self.hyphen_end = False

    def add_line(self, cs, trailing_space):
        text = ''.join(c[0] for c in cs).rstrip()
        cs = cs[:len(cs) - (len(''.join(c[0] for c in cs)) - len(text))] if text else []
        # strip by characters (an 'fi' ligature char is two letters)
        while cs and cs[-1][0] == ' ':
            cs.pop()
        while cs and cs[0][0] == ' ':
            cs.pop(0)
        if not cs:
            return
        if self.chars:
            last = self.chars[-1][0]
            if self.hyphen_end:                     # a break: join the word
                self.chars.pop()
            elif last in '–—' or (last == '-' and self._real):
                pass                                # a dash, or a real hyphen: closed up
            else:
                self.chars.append([' ', self.chars[-1][1]])
        self.chars += [[c[0], c[3]] for c in cs]
        self._real = trailing_space
        self.hyphen_end = cs[-1][0] == '-' and not trailing_space

    _real = False


URL = re.compile(r'www(?: ?\.[\w/-]+| [\w-]*/[\w/.-]*)+')


def fix_urls(t):
    """The print breaks a web address at its dots and slashes, and across
    lines without a hyphen ("www .chgs .umn .edu/ histo ries/"): inside an
    address beginning "www", the spaces are dropped."""
    def one(m):
        return m.group(0).replace(' ', '')
    prev = None
    while prev != t:
        prev = t
        t = URL.sub(one, t)
        t = re.sub(r'(www\S*/) (?=\w)', r'\1', t)          # "edu/ histo"
        t = re.sub(r'(www\S*\w) \.(?=\s|$)', r'\1.', t)   # "pits.htm ."
    return t


def render(p, linked):
    out, cur = [], ''
    i = 0
    cs = p.chars
    while i < len(cs):
        ch, st = cs[i]
        if st == 'sup' and ch.isdigit():
            j = i
            while j < len(cs) and cs[j][1] == 'sup' and cs[j][0].isdigit():
                j += 1
            n = ''.join(c[0] for c in cs[i:j])
            out.append(('', f'[^{n}]' if linked else f'<sup>{n}</sup>'))
            i = j
            continue
        if st == 'sup':
            st = ''
        out.append((st, ch))
        i += 1
    # wrap runs of italic or bold, spaces kept outside the marks
    text, k = '', 0
    while k < len(out):
        st = out[k][0]
        j = k
        while j < len(out) and out[j][0] == st:
            j += 1
        run = ''.join(c for _, c in out[k:j])
        if st in ('i', 'b') and run.strip():
            mark = '*' if st == 'i' else '**'
            # an italic that begins inside a word ("Z*agłada*": the text
            # layer sets the first letter roman) takes in the whole word
            m = re.search(r'\w+$', text)
            if m and not run[0].isspace():
                text, run = text[:m.start()], m.group(0) + run
            lead = run[:len(run) - len(run.lstrip())]
            tail = run[len(run.rstrip()):]
            text += lead + mark + run.strip() + mark + tail
        else:
            text += run
        k = j
    text = re.sub(r'(?<=\S)  +(?=\S)', ' ', text)   # where an italic run met a space
    return fix_urls(text)


def build(doc):
    pages = []            # (printed page, [Para])
    segment = []          # the paragraphs of the current entry (marker links)
    segments = []
    prev_pdf = None
    in_notes, last_num = False, 0     # a notes list may run on to the next page
    for pno in PAGES:
        page = doc[pno - 1]
        if prev_pdf is not None and pno != prev_pdf + 1:
            segments.append(segment)
            segment = []
            in_notes, last_num = False, 0
        paras, captions = [], []
        cur = None
        for it in page_items(page):
            first = it['lines'][0]
            s0 = next((s for s in first['spans']
                       if ''.join(c['c'] for c in s['chars']).strip()), first['spans'][0])
            k = kind(first, s0['size'], s0['font'])
            if k == 'caption':
                cap = Para('caption')
                for l in it['lines']:
                    cs = chars_of(l)
                    cap.add_line(cs, bool(cs) and cs[-1][0] == ' ')
                captions.append(cap)
                continue
            if k in ('title', 'heading'):
                if k == 'heading':
                    segments.append(segment)
                    segment = []
                cur = Para(k)
                for l in it['lines']:
                    cs = chars_of(l)
                    cur.add_line(cs, True)
                paras.append(cur)
                segment.append(cur)
                in_notes = False
                cur = None
                continue
            if k == 'notes':
                cur = Para('notes')
                cur.add_line(chars_of(first), True)
                paras.append(cur)
                segment.append(cur)
                in_notes, last_num = True, 0
                cur = None
                rest = it['lines'][1:]
                if not rest:
                    continue
                it = dict(it, lines=rest)
                first = rest[0]
            if k == 'signature':
                cur = Para('signature')
                for l in it['lines']:
                    cur.add_line(chars_of(l), True)
                paras.append(cur)
                segment.append(cur)
                cur = None
                in_notes = False
                continue
            text0 = ''.join(c[0] for c in chars_of(first)).strip()
            if text0.startswith('SOURCES'):
                in_notes = False
            if in_notes:
                for l in it['lines']:
                    cs = chars_of(l)
                    t = ''.join(c[0] for c in cs)
                    if not t.strip():
                        continue
                    m = re.match(r'\s*(\d{1,3})\.\s', t)
                    if m and int(m.group(1)) == last_num + 1:
                        cur = Para('note')
                        cur.num = last_num = int(m.group(1))
                        taken = 0          # drop the number, by letters
                        while cs and taken < m.end():
                            taken += len(cs[0][0])
                            cs = cs[1:]
                        cur.add_line(cs, bool(cs) and cs[-1][0] == ' ')
                        paras.append(cur)
                        segment.append(cur)
                    else:
                        if cur is None or cur.kind not in ('note', 'notecont'):
                            cur = Para('notecont')   # a note run on from the page before
                            paras.append(cur)
                            segment.append(cur)
                        cur.add_line(cs, bool(cs) and cs[-1][0] == ' ')
                continue
            indent = first['bbox'][0] - it['left']
            whole = min(l['bbox'][0] for l in it['lines']) - it['left']
            italic_gaz = text0.startswith('Pre-')
            new = (cur is None or indent > 6 or text0.startswith('SOURCES')
                   or italic_gaz or (cur.kind not in ('body', 'quote')))
            if whole > 14 and len(it['lines']) > 1:
                cur = Para('quote')
                paras.append(cur)
                segment.append(cur)
            elif new:
                cur = Para('gaz' if italic_gaz else 'body')
                paras.append(cur)
                segment.append(cur)
            for l in it['lines']:
                cs = chars_of(l)
                cur.add_line(cs, bool(cs) and cs[-1][0] == ' ')
            if cur.kind == 'quote':
                cur = None
        pages.append([pno + OFFSET, pno, paras, captions])
        prev_pdf = pno
    segments.append(segment)
    # an entry's markers link only where its notes are among these pages
    linked = {}
    for seg in segments:
        has = any(p.kind == 'notes' for p in seg)
        for p in seg:
            linked[id(p)] = has
    return pages, linked


def write(pages, linked):
    lines = []
    for idx, (printed, pdf, paras, captions) in enumerate(pages):
        # a word broken over two consecutive pages: joined on the first
        nxt = pages[idx + 1] if idx + 1 < len(pages) else None
        if paras and paras[-1].hyphen_end and nxt and nxt[1] == pdf + 1 and nxt[2]:
            p, q = paras[-1], nxt[2][0]
            w = 0
            while w < len(q.chars) and q.chars[w][0] != ' ':
                w += 1
            p.chars.pop()
            p.chars += q.chars[:w]
            q.chars = q.chars[w + 1:]
            p.hyphen_end = False
        lines += [f'[p. {printed}]', '']
        for p in paras:
            t = render(p, linked.get(id(p), False))
            if not t.strip():
                continue
            if p.kind == 'title':
                t = '# ' + t.replace('**', '')
            elif p.kind == 'heading':
                t = '## ' + t.replace('**', '')
            elif p.kind == 'notes':
                t = '**' + t.replace('**', '') + '**'
            elif p.kind == 'note':
                t = f'[^{p.num}]: ' + t if linked.get(id(p), False) else f'{p.num}. ' + t
            elif p.kind == 'quote':
                t = '> ' + t
            lines += [t, '']
        for c in captions:
            t = render(c, False)
            if t.strip():
                lines += [t, '']
    text = '\n'.join(lines).rstrip('\n') + '\n'
    for old, new, why in CORRECTIONS:
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    return text


def check(doc, text):
    """Every letter of the pages taken, against the PDF's own (spaces,
    hyphens, marks and note numbers aside). A word broken over two pages is
    moved to the first, so a page and the next may differ by that word; the
    whole must agree."""
    from collections import Counter
    keep = re.compile('[^A-Za-zÀ-žŁłąćęńśźżĄĆĘŃŚŹŻ]')
    parts = re.split(r'^\[p\. (\d+)\]\s*$', text, flags=re.M)
    got = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}
    total_a, total_g = Counter(), Counter()
    for pno in PAGES:
        raw = ''
        for b in doc[pno - 1].get_text('rawdict')['blocks']:
            if b['type'] != 0:
                continue
            for l in b['lines']:
                if TOP <= l['bbox'][1] < FOOT:
                    raw += ''.join(c[0] for c in chars_of(l)) + ' '
        for old, new, why in CORRECTIONS:          # the editor's corrections
            raw = raw.replace(old, new)
        a = Counter(keep.sub('', raw))
        g = Counter(keep.sub('', re.sub(r'<sup>\d+</sup>|\[\^\d+\]:?', '', got[pno + OFFSET])))
        total_a += a
        total_g += g
        if a != g:
            moved = ''.join(sorted((g - a).elements())) or ''.join(sorted((a - g).elements()))
            print(f'p. {pno + OFFSET}: a word moved across the page end ({moved})')
    ok = total_a == total_g
    print('check:', 'all letters agree' if ok else
          f'differ: missing {dict(total_a - total_g)}, extra {dict(total_g - total_a)}')
    return 0 if ok else 1


def main():
    doc = fitz.open(sys.argv[1])
    pages, linked = build(doc)
    text = write(pages, linked)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print(f'wrote {OUT}: {len(pages)} pages')
    if '--check' in sys.argv:
        sys.exit(1 if check(doc, text) else 0)


if __name__ == '__main__':
    main()
