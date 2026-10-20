# -*- coding: utf-8 -*-
"""
Szwiec (2009): the catalogue's PDF to literature/szwiec2009/original.md and
its page pictures (2026-10-20).

    python pipeline/literature/szwiec_pdf.py <the PDF> [--figures]

The PDF was printed from Word ("Kat_Archi_region_Pyzdry.doc"), so its text
layer is the author's text, not a reading of an image. What this script does to
it, and nothing else:
- each page is opened with "[p. N]" (the printed page numbers are the PDF's);
  pages 2 and 3 (title page and credits) stand before the first mark, as the
  work's front. Pages 1 and 5 are blank; page 4, the table of contents, is
  left out (the editor ruled so for Pachoński's book);
- the running head ("KATALOG ARCHITEKTURY REGIONALNEJ ..." with the page
  number, or the page number with "dr Piotr Szwiec") is left out;
- the pieces of a line are joined, with a space where the PDF leaves a gap
  and gives none ("1.5. Sposób", "obiektów drewnianych"); the lines of a
  paragraph are joined. A paragraph begins at an indented line, at a change
  between bold and plain, at a numbered heading, or after a gap. The
  bibliography (pp. 96-100) is set with hanging indents: there an entry
  begins at its number "[n]", a list at its heading;
- the small type holds the photographs' captions and the notes. A note is a
  small line beginning with a number that is raised in the text above it;
  its mark becomes "[^n]" and the note "[^n]: ...". Any other raised figure
  becomes its raised character (the degrees of "45⁰"). A caption begins with
  its number ("16. Budynek mieszkalny ...") and runs on over the next small
  line close under it;
- Word's hyphen (U+2010) becomes "-"; the text is otherwise unchanged, its
  slips included.
With --figures it renders every page that holds photographs or maps (all but
page 3, whose pictures are the sponsors' logos) at 1100 pixels wide into
site/assets/literature/szwiec2009/<page>.jpg, and prints the `figures` list
for work.yml.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'literature', 'szwiec2009', 'original.md')
FIG = os.path.join(ROOT, 'site', 'assets', 'literature', 'szwiec2009')
FRONT = (2, 3)
SKIP = {1, 4, 5}
LOGOS = {3}
BIBLIOGRAPHY = range(96, 101)   # pp. 96-100, the bibliography
RAISE = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
INDENT = 122         # a body line starting this far in begins a paragraph
NBSP = ' '


def clean(t):
    return re.sub(r'[  ]+', ' ', t.replace('‐', '-')).strip()


def lines_of(page):
    """[(x0, y, x1, size, bold, [(text, sup)])] in reading order."""
    d = page.get_text('dict')
    rows = []
    for b in d['blocks']:
        if b['type'] != 0:
            continue
        for l in b['lines']:
            spans = [s for s in l['spans'] if s['text'].strip(' ' + NBSP)]
            if not spans:
                continue
            rows.append([l['bbox'][0], round(l['bbox'][1]), l['bbox'][2],
                         max(s['size'] for s in spans),
                         all(s['flags'] & 16 for s in spans),
                         [(s['text'], bool(s['flags'] & 1), s['bbox'][0], s['bbox'][2]) for s in spans]])
    rows.sort(key=lambda r: (r[1], r[0]))
    merged = []
    for r in rows:
        if merged and abs(merged[-1][1] - r[1]) <= 2 and r[3] == merged[-1][3]:
            m = merged[-1]
            m[2] = max(m[2], r[2])
            m[4] = m[4] and r[4]
            m[5] = m[5] + r[5]
        else:
            merged.append(r)
    for m in merged:
        pieces = sorted(m[5], key=lambda x: x[2])
        out = []
        for i, (t, sup, x0, x1) in enumerate(pieces):
            gap = x0 - pieces[i - 1][3] if i else 0
            if (out and gap > 1.2 and not sup and not out[-1][0].endswith((' ', NBSP))
                    and not t.startswith((' ', NBSP))):
                out.append((' ', False))
            out.append((t, sup))
        m[5] = out
    return merged


def is_head(r, n):
    t = clean(''.join(x for x, _ in r[5]))
    return r[1] < 95 and (t.startswith('KATALOG ARCHITEKTURY') or t.endswith('dr Piotr Szwiec')
                          or t == str(n))


def page_text(page, n):
    rows = [r for r in lines_of(page) if not is_head(r, n)]
    body = [r for r in rows if r[3] >= 9]
    small = [r for r in rows if r[3] < 9]
    marks = {t.strip() for r in body for t, sup in r[5] if sup and t.strip().isdigit()}

    def note_no(r):
        m = re.match(r'(\d+)', clean(''.join(x for x, _ in r[5])))
        return m.group(1) if m and m.group(1) in marks else None
    numbers = {note_no(r) for r in small} - {None}

    def text(r):
        out = ''
        for t, sup in r[5]:
            if sup and t.strip() in numbers:
                out += f'[^{t.strip()}]'
            elif sup and t.strip().isdigit():
                out += t.strip().translate(RAISE)
            else:
                out += t
        return re.sub(r'\s+\[\^', '[^', clean(out))

    paras, prev = [], None
    for r in body:
        t = text(r)
        if not t:
            continue
        if n in BIBLIOGRAPHY:
            # hanging indents: an entry begins at its number "[n]", a list at its heading
            starts = (prev is None or re.match(r'\[\d+\]', t) or not re.match(r'\[\d+\]', paras[-1])
                      or r[1] - prev[1] > 25)
        else:
            # a gap ends a paragraph only after a full stop: text also runs on round a photograph
            end = paras[-1].endswith(('.', ':', '!', '?', '”', ')')) if paras else True
            starts = (prev is None or r[0] >= INDENT or (r[4] != prev[4] and end)
                      or (r[1] - prev[1] > 25 and end)
                      or (r[4] and re.match(r'\d+(\.\d+)*\.\s?\S', t)))
        if starts:
            # a heading's number and its words stand apart on the page ("1.2. Zebranie")
            paras.append(re.sub(r'^(\d+(?:\.\d+)*\.)(?=[A-ZĄĆĘŁŃÓŚŹŻ])', r'\1 ', t))
        else:
            paras[-1] += ' ' + t
        prev = r
    notes, caps, prev, in_note = [], [], None, False
    for r in small:
        t = text(r)
        if not t:
            continue
        k = note_no(r)
        if k and not any(k == x for x, _ in notes):
            notes.append([k, re.sub(r'^\d+\.?\s*', '', t)])
            in_note = True
        elif in_note and notes:
            notes[-1][1] += (' ' if prev[2] >= 400 else '\n') + t
        elif caps and prev is not None and r[1] - prev[1] < 15 and not re.match(r'\d+\.\s', t):
            caps[-1] += ' ' + t
        else:
            caps.append(t)
            in_note = False
        prev = r
    return paras + caps + [f'[^{k}]: {v}' for k, v in notes]


def main():
    import fitz
    doc = fitz.open(sys.argv[1])
    blocks = []
    for n, page in enumerate(doc, 1):
        if n in SKIP:
            continue
        paras = page_text(page, n)
        head = '' if n in FRONT else f'[p. {n}]\n\n'
        blocks.append(head + '\n\n'.join(paras) + '\n')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(blocks))
    print('wrote', OUT)
    if '--figures' in sys.argv:
        from PIL import Image
        os.makedirs(FIG, exist_ok=True)
        figs = []
        for n, page in enumerate(doc, 1):
            if n in SKIP or n in LOGOS or not page.get_images():
                continue
            zoom = 1100 / page.rect.width
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
            im.save(os.path.join(FIG, f'{n}.jpg'), quality=82, optimize=True)
            figs.append(n)
        print('figures:', ' '.join(f'"{n}": "{n}.jpg"' for n in figs))


if __name__ == '__main__':
    main()
