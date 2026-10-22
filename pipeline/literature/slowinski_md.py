# -*- coding: utf-8 -*-
"""
Słowiński (2023): the editor's checked Markdown of "Przeżyć tę jedną zimę"
to literature/slowinski2023/original.md (2026-10-22).

    python pipeline/literature/slowinski_md.py <the checked .md> <the PDF>
                                               [--english] [--report] [--check]

With --english the same treatment is given the book's English .md and the
result written literature/slowinski2023/english.md (2026-10-22; the work's
second text, which build_literature.py cuts like the original). The
paragraph-move step finds paragraphs by their letters in the PDF's Polish
layer, so it finds nothing in the English and moves nothing: the paragraph
the Polish .md had beside its picture stands in the English .md beside it
too, and is set right by hand where --check reports the page.

The editor's .md of the book is the checked export of 2026-10-22
(docs/WORKING_NOTES.md, "Two of Słowiński's books checked against their
PDFs"): made again from the PDF's text layer with PyMuPDF, the editor's first
export kept only as a witness. The PDF ("Przeżyć tę jedną zimę.pdf", Konin
2023, the editor's Downloads folder) is the book as printed; it is not kept in
the repository, and neither is the .md.

What this script does to the checked .md, and nothing else:

- The .md carries its page marks in the form "<!-- s. N [PDF M] -->", N the
  printed page, M the PDF page; the marks stand on their own lines and, where
  the book's text runs over a page's end mid-sentence, also inside a line. The
  script splits every line at an inline mark, so each printed page keeps its
  own words; a mark opens its page's run of text.
- The .md names its pictures in lines beginning "![", pointing at an images
  folder that was not supplied; the pictures are in the PDF and are not
  rendered (the editor's word of 2026-10-22, as for Mielewczyk 2017): the
  picture lines are dropped, their captions stay, being text.
- The .md repeats a page's mark beside its pictures (the export set the
  pictures in their places with the page's mark around them, after the page's
  text had already run on). Page marks never run backwards in a book: a mark
  whose printed page is not greater than the page now open is a placement
  mark, and is dropped with the pictures around it.
- The .md's unnumbered pages (the cover, the imprint, the epigraph page, the
  table of contents) carry the mark "s. ?"; the script writes them
  "s. unnumbered", the form the passage builder (build_literary.py) knows.
  The unnumbered pages before the first numbered one are the passage "front".
- The notes of the print stand at the foot of their pages. The .md gathered
  them at the very end, after a "---" divider, each note (and each piece of a
  note that runs over a page's foot) under a mark repeating the page of its
  reference in the text. The script takes the notes back to their pages: the
  note, or the piece of it, is set at the foot of that page's run of text, as
  the print sets it. A note's raised mark in the text keeps its [^n] form.
- Nothing else is changed: the headings, the epigraphs in ">", the ornaments
  "◼", the print's slips, the book's own way of setting the letters' dates.

With --check the script rebuilds, from its own reading of the PDF's text
layer, the stream of letters each PDF page carries (whitespace, hyphens and
dashes, the marks of the markdown and the layout's signs left out; the
look-alike letters the layer carries written as the book prints them) and
asserts that the same stream, read back out of the original.md it wrote, is
unchanged page by page.
"""
import io
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'literature', 'slowinski2023', 'original.md')
OUT_EN = os.path.join(ROOT, 'literature', 'slowinski2023', 'english.md')

MARK = re.compile(r'<!-- s\. (\S+) \[PDF (\d+)\] -->')
IMAGE = re.compile(r'^!\[')
COMMENT = re.compile(r'^<!--(?!\d)[^>]+-->\s*$')
DIVIDER = re.compile(r'^---\s*$')


def read_lines(path):
    with open(path, encoding='utf-8') as f:
        return f.read().replace('\r\n', '\n').split('\n')


def pages_of(lines, report):
    """[(printed, pdf, [lines])] in the .md's own order, marks and pictures
    left out. A mark inside a line splits it: the words before it belong to
    the page now open, the mark opens the next."""
    pages, cur = [], None
    for i, line in enumerate(lines, 1):
        if IMAGE.match(line):
            report.append(f'line {i}: picture dropped')
            continue
        ms = list(MARK.finditer(line))
        if not ms:
            if COMMENT.match(line):
                report.append(f'line {i}: the .md\'s own comment dropped '
                              f'({line.strip()})')
                continue
            if cur is not None:
                cur[2].append(line)
            continue
        head = line[:ms[0].start()]
        for j, m in enumerate(ms):
            tail = line[m.end():ms[j + 1].start() if j + 1 < len(ms) else len(line)]
            printed, pdf = m.group(1), m.group(2)
            label = 'unnumbered' if printed == '?' else printed
            first = (cur is None or not cur[0].isdigit()
                     or not label.isdigit() or int(label) > int(cur[0]))
            if cur is not None and not first:
                report.append(f'line {i}: placement mark s. {printed} dropped')
                if head.strip() or tail.strip():
                    report.append(f'line {i}: WORDS ROUND A PLACEMENT MARK: '
                                  f'{head!r} / {tail!r}')
                head, tail = '', tail
                continue
            if cur is not None and head.strip():
                cur[2].append(head)
            cur = [label, int(pdf), []]
            pages.append(cur)
            head = tail
        if cur is not None and head.strip():
            cur[2].append(head)
    return pages


def run(md_path, pdf_path, report):
    lines = read_lines(md_path)
    # the notes are everything after the last --- divider
    divs = [i for i, l in enumerate(lines) if DIVIDER.match(l)]
    if not divs:
        raise SystemExit('no --- divider found: where the notes begin')
    div = divs[-1]
    body, tail = lines[:div], lines[div + 1:]
    pages = pages_of(body, report)
    # the notes: each piece under its mark goes to the foot of that page
    notes = pages_of(tail, report)
    by_label = {}
    for p in pages:
        by_label.setdefault(p[0], p)
    for label, pdf, note_lines in notes:
        page = by_label.get(label)
        if page is None:
            report.append(f'NOTE on s. {label}: no such page in the body')
            continue
        page[2].extend([''] + note_lines)
    # a paragraph the .md set beside its picture may stand on the neighbouring
    # page in the print: the PDF's own text says where it is
    import fitz
    doc = fitz.open(pdf_path)
    layer_letters = [letters(doc[p].get_text()) for p in range(doc.page_count)]
    for label, pdf, pls in list(pages):
        for li, line in enumerate(pls):
            bare = letters(NOTE_MARK.sub('', line))
            if len(bare) < 12:
                continue
            found = [n + 1 for n, t in enumerate(layer_letters) if bare in t]
            if len(found) == 1 and found[0] != pdf:
                target = next((p for p in pages if p[1] == found[0]), None)
                if target is not None:
                    report.append(
                        f's. {label}: the paragraph beginning '
                        f'{line.strip()[:50]!r} is printed on the page of '
                        f'PDF {found[0]} (the .md set it beside its picture): '
                        f'moved there')
                    target[2].extend([''] + [line])
                    pls[li:li + 1] = []
                    break
    # every page's mark is written once, in the .md's own form
    out = []
    for label, pdf, pls in pages:
        out.append(f'<!-- s. {label} [PDF {pdf}] -->')
        out.extend(pls)
    text = '\n'.join(out).rstrip('\n') + '\n'
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    return pages


def letters(s):
    """The stream of letters a text carries: everything that is not a letter
    or a digit taken out, the look-alike letters written as the book prints
    them, the ligatures their letters."""
    s = unicodedata.normalize('NFKC', s)
    for a, b in (('\u03b2', '\u00df'), ('\u04d3', '\u00e4'), ('\u0456', 'i')):
        s = s.replace(a, b)
    return ''.join(c for c in s if c.isalnum())


NOTE_MARK = re.compile(r'\[\^\d+\]')


def page_folios(doc):
    """{pdf page (1-based): the printed number the print sets at its foot} -
    the digit-only block in the folio band (y0 >= 540)."""
    out = {}
    for pno in range(doc.page_count):
        for b in doc[pno].get_text('blocks'):
            t = b[4].strip()
            if b[1] >= 540 and t.isdigit() and len(t) <= 3:
                out[pno + 1] = t
    return out


def check(md_path, pdf_path, report):
    """The letters of every PDF page against the letters the original.md
    carries for it (the marks name the PDF page). The folio block the layer
    carries at the foot (the printed page number) is left out; a word the
    print divides over a page's end is given whole on the first page (the
    .md's rule), so the check gives its tail back to the page that begins
    with it before it compares.

    For the English (OUT the english.md) the letters cannot be held to the
    Polish layer; instead the marks of the English are held to the marks of
    the original.md: the English .md mirrors the Polish one mark for mark,
    and the Polish one is held to the PDF by the letter check."""
    import fitz
    doc = fitz.open(pdf_path)
    if OUT.endswith('english.md'):
        ref = os.path.join(os.path.dirname(OUT), 'original.md')
        want = [(m.group(1), int(m.group(2)))
                for m in MARK.finditer('\n'.join(read_lines(ref)))]
        got = [(m.group(1), int(m.group(2)))
               for m in MARK.finditer('\n'.join(read_lines(OUT)))]
        if want != got:
            report.append('the English marks are not the original.md\'s')
            for i in range(min(len(want), len(got))):
                if want[i] != got[i]:
                    report.append(f'  first differing mark {i}: '
                                  f'original {want[i]} english {got[i]}')
                    break
            if len(want) != len(got):
                report.append(f'  {len(want)} marks against {len(got)}')
        else:
            report.append(f"the English's {len(got)} marks are the "
                          f"original.md's, in order")
        return 0
    doc = fitz.open(pdf_path)
    folios = page_folios(doc)
    by_pdf, cur = {}, None
    for line in read_lines(OUT):
        m = MARK.match(line)
        if m:
            cur = int(m.group(2))
            by_pdf.setdefault(cur, [])
            continue
        if IMAGE.match(line):
            report.append(f'original.md still carries a picture line: {line[:60]!r}')
            continue
        if cur is not None:
            by_pdf[cur].append(line)
    bad = 0
    wants, gots = [], []
    for pno in range(doc.page_count):
        layer = doc[pno].get_text()
        folio = folios.get(pno + 1)
        if folio:
            layer = re.sub(rf'(?m)^\s*{folio}\s*$', '', layer)
        wants.append(letters(layer))
        gots.append(letters(NOTE_MARK.sub('', '\n'.join(by_pdf.get(pno + 1, [])))))
    bad = 0
    wants, gots = [], []
    for pno in range(doc.page_count):
        layer = doc[pno].get_text()
        folio = folios.get(pno + 1)
        if folio:
            layer = re.sub(rf'(?m)^\s*{folio}\s*$', '', layer)
        wants.append(letters(layer))
        gots.append(letters(NOTE_MARK.sub('', '\n'.join(by_pdf.get(pno + 1, [])))))
    from collections import Counter
    full_want, full_got = ''.join(wants), ''.join(gots)
    if Counter(full_want) != Counter(full_got):
        bad += 1
        report.append('the letters of the print and of the .md are not the '
                      'same overall')
    cumw, cumg = [], []
    n = 0
    for w in wants:
        cumw.append(n)
        n += len(w)
    cumw.append(n)
    n = 0
    for g in gots:
        cumg.append(n)
        n += len(g)
    cumg.append(n)

    def page_of(pos, cum):
        for p in range(doc.page_count):
            if cum[p] <= pos < cum[p + 1]:
                return p
        return doc.page_count - 1

    WINDOW = 24
    pending = []          # boundary fragments the .md carries early
    i = j = 0
    while i < len(full_want) or j < len(full_got):
        if i < len(full_want) and j < len(full_got) \
                and full_want[i] == full_got[j]:
            i += 1
            j += 1
            continue
        # the .md may carry a short run the print divides over the page's end
        frag = None
        for win in (WINDOW, 12, 8):
            sync = next((k for k in range(1, 13)
                         if full_want[i:i + win]
                         == full_got[j + k:j + k + win]), None)
            if sync:
                frag = full_got[j:j + sync]
                break
        if frag:
            p = page_of(j, cumg)
            rest = ''.join(wants[p + 1:])
            if rest.startswith(frag):
                report.append(f'PDF pages {p + 1}/{p + 2}: the word divided '
                              f"over the page's end ({frag!r}) given whole on "
                              f'the first page, as the .md sets it')
                pending.append(frag)
                j += len(frag)
                continue
        # the layer may carry a short run the .md has set on an earlier page
        # (the other half of such a division)
        sync = next((k for k in range(1, 13)
                     if full_want[i + k:i + k + WINDOW] == full_got[j:j + WINDOW]),
                    None)
        if sync:
            run = full_want[i:i + sync]
            hit = next((f for f in pending if Counter(f) == Counter(run)), None)
            if hit:
                pending.remove(hit)
                i += sync
                continue
            bad += 1
            p = page_of(j, cumg)
            report.append(f'PDF page {p + 1}: the print\'s letters '
                          f'{run[:60]!r} the .md does not carry (at {i})')
            i += sync
            continue
        # a real difference: resync at the next common window
        p = page_of(j, cumg)
        step = next(((di, dj) for di in range(1, 2000) for dj in range(0, 200)
                     if full_want[i + di:i + di + WINDOW]
                     == full_got[j + dj:j + dj + WINDOW]), None)
        if step is None:
            bad += 1
            report.append(f'PDF page {p + 1}: the print ...{full_want[i:i + 60]!r} '
                          f'against the .md ...{full_got[j:j + 60]!r} (at {i}); '
                          f'no resync found, the rest is not checked letter '
                          f'by letter')
            break
        di, dj = step
        rw, rg = full_want[i:i + di], full_got[j:j + dj]
        if Counter(rw) == Counter(rg):
            report.append(f'PDF page {p + 1}: the letters the same, their '
                          f"order not: the print ...{rw[:50]!r} against the "
                          f".md ...{rg[:50]!r}")
        elif not (set(Counter(rw)) <= set(Counter(full_got[cumg[p]:j]))
                  and all(Counter(rw)[c] <= Counter(full_got[cumg[p]:j])[c]
                          for c in Counter(rw))):
            bad += 1
            report.append(f'PDF page {p + 1}: the print ...{rw[:60]!r} '
                          f'against the .md ...{rg[:60]!r} (at {i})')
        else:
            report.append(f'PDF page {p + 1}: the letters of ...{rw[:50]!r} '
                          f'stand earlier on the same page of the .md (the '
                          f"print's order read differently)")
        i += di
        j += dj
    missing = [p for p in by_pdf if p > doc.page_count]
    if missing:
        report.append(f'original.md names PDF pages the PDF has not: {missing}')
    return bad


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    report = '--report' in sys.argv
    checking = '--check' in sys.argv
    english = '--english' in sys.argv
    if len(args) != 2:
        print(__doc__)
        return 2
    md_path, pdf_path = args
    if english:
        globals()['OUT'] = OUT_EN
    rep = []
    if not checking:
        run(md_path, pdf_path, rep)
    bad = check(md_path, pdf_path, rep)
    for line in rep:
        print(line)
    print(f"{'--check: ' if checking else ''}{len(rep)} report line(s), "
          f"{bad} PDF page(s) differ")
    return 1 if (bad or any('WORDS AFTER' in r or 'no such page' in r for r in rep)) else 0


if __name__ == '__main__':
    sys.exit(main())
