# -*- coding: utf-8 -*-
"""
"Zerwane ogniwo": the checked Markdown of the collective volume to
literature/slowinskipolom2024/original.md and english.md (2026-10-22).

    python pipeline/literature/slowinskipolom_md.py <the checked .md> <the PDF>
                                                    [--english] [--report] [--check]

Without --english the Polish .md is treated and original.md written; with it
the English .md and english.md. The volume: "Zerwane ogniwo. Ewangelicy na
ziemi zagórowskiej", a collective work edited by Mirosław Słowiński and
Katarzyna Połom, Zagórów 2024 (the Municipal Office in Zagórów); the checked
.md files and the PDF ("Zerwane ogniwo.pdf", the editor's Downloads folder)
are the exports of 2026-10-22 (docs/WORKING_NOTES.md, "Two of Słowiński's
books checked against their PDFs" - the same session's method, the same
rulings: the look-alike letters ß/ä written as printed, the cover's OGNIWO
written whole). The PDF and the .md files are not kept in the repository.

What this script does to the checked .md, and nothing else (the twin of
pipeline/literature/slowinski_md.py, which made Słowiński 2023 the same way):

- The .md carries its page marks in the form "<!-- s. N [PDF M] -->", N the
  printed page, M the PDF page; the marks stand on their own lines and, where
  the book's text runs over a page's end mid-sentence, also inside a line
  (one of them the export broke over two lines in the English; repaired in
  the .md first, the repair recorded in the work's notes.md). The script
  splits every line at an inline mark, so each printed page keeps its own
  words; a mark opens its page's run of text.
- The .md names its pictures in lines beginning "![", pointing at an images
  folder beside it ("Zerwane ogniwo - images", not kept in the repository);
  the pictures are in the PDF and are not rendered (the editor's word of
  2026-10-22, as for Słowiński 2023 and Mielewczyk 2017): the picture lines
  are dropped, their captions stay, being text.
- The .md repeats a page's mark beside its pictures (the export set the
  pictures in their places with the page's mark around them, after the
  page's text had already run on). Page marks never run backwards in a book:
  a mark whose printed page is not greater than the page now open is a
  placement mark, and is dropped with the pictures around it.
- The .md's own comments ("<!-- caption -->", "<!-- byline -->", the cover's
  note) are dropped, being chrome.
- The .md's unnumbered pages carry the mark "s. ?"; the script writes them
  "s. unnumbered", the form the passage builder (build_literature.py) knows.
  The unnumbered pages before the first numbered one are the passage "front".
- The notes of the print stand at the foot of their pages. The .md gathered
  them at the very end, after a "---" divider, each note (and each piece of
  a note that runs over a page's foot) under a mark repeating the page of
  its reference in the text. The script takes the notes back to their pages:
  the note, or the piece of it, is set at the foot of that page's run of
  text, as the print sets it. A note's raised mark in the text keeps its
  [^n] form.
- Nothing else is changed: the headings (the parts' "##", the chapters'
  "###"), the TOC's "◆", the print's slips.

With --check the script rebuilds, from its own reading of the PDF's text
layer, the stream of letters each PDF page carries (whitespace, hyphens and
dashes, the marks of the markdown and the layout's signs left out; the
look-alike letters the layer carries written as the book prints them) and
asserts that the same stream, read back out of the file it wrote, is
unchanged page by page. The print's folio stands in the band of the page's
bottom seventy points (the book's pages are 566.9 points high, the folio
about y 513); a page with none (a picture page) is simply not stripped.

For the English the letters cannot be held to the Polish layer; instead the
marks of the English are held to the marks of the original.md (the English
.md mirrors the Polish one mark for mark, and the Polish one is held to the
PDF by the letter check).
"""
import io
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'literature', 'slowinskipolom2024', 'original.md')
OUT_EN = os.path.join(ROOT, 'literature', 'slowinskipolom2024', 'english.md')

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
    the page now open, the mark opens the next.

    The export sets a picture plate's captions in a block of their own,
    after the running text has already flowed past the plate: the block
    opens with the plate's own mark again and closes with the mark of the
    page the text had reached - which may be a greater number still (the
    plate sits mid-page between two marks set inline). So any mark whose
    page has been opened before is a **return**, of whatever number: the
    lines that follow it (the pictures' captions, the text's continuation)
    belong to the page it names, and the script switches to that page's
    object. Words around such a returned mark are an error, reported. The
    unnumbered pages' marks always open a page of their own (they never
    return), so that the front's unnumbered pages stay apart."""
    pages, cur, by_label = [], None, {}
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
            returning = (cur is not None and label in by_label
                         and label.isdigit())
            if returning:
                if head.strip() or tail.strip():
                    report.append(f'line {i}: WORDS ROUND A RETURNED MARK '
                                  f's. {label}: {head!r} / {tail!r}')
                head, tail = '', tail
                cur = by_label[label]
                continue
            if cur is not None and head.strip():
                cur[2].append(head)
            cur = [label, int(pdf), []]
            pages.append(cur)
            if label not in by_label:
                by_label[label] = cur
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
    # page in the print: the PDF's own text says where it is (the Polish only;
    # in the English the step is skipped - an English line cannot be looked
    # for in the Polish layer, and the one hit it finds is a false one: the
    # imprint's "Dr Zbigniew Chodyła" matched the German summary's credit.
    # The English's captions keep the export's placement, in the spread
    # cases a page off the print; recorded in the work's notes.md)
    import fitz
    doc = fitz.open(pdf_path)
    if not OUT.endswith('english.md'):
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
# the export's markup for what the print's layer does not carry as letters:
# the <br> tags of its table cells (the print breaks the line) and the
# circled numerals of the captions (the print's glyphs are private-use
# characters the letter stream does not carry)
md_markup = re.compile(r'<br\s*/?>|[\u2460-\u24ff\u3251-\u325f\u32b1-\u32bf]')


def page_folios(doc):
    """{pdf page (1-based): the printed number the print sets at its foot} -
    the digit-only block in the bottom band of the page (the book's folio
    stands about y 513 of a 566.9-point page)."""
    out = {}
    for pno in range(doc.page_count):
        h = doc[pno].rect.height
        for b in doc[pno].get_text('blocks'):
            t = b[4].strip()
            if b[1] > h - 70 and t.isdigit() and len(t) <= 3:
                out[pno + 1] = t
    return out


def check(md_path, pdf_path, report):
    """The letters of every PDF page against the letters the file written
    carries for it (the marks name the PDF page), compared page by page as
    multisets - the form of the check WORKING_NOTES records for these books
    ("the letters equal page by page"). Left out of the print's side: the
    folio block at the foot (the printed page number) and the running heads
    at the top (the author's name on the left pages, the section's title on
    the right ones - the export leaves them out); left out of the .md's
    side: the [^n] markers, which stand for the print's asterisks.

    The print's layout sets a picture page's captions round its pictures;
    the export lays them out in a line, so the order of the letters differs
    where captions stand - a multiset holds the captions to their page
    without holding them to an order the print does not have.

    A word the print divides over a page's end is given whole on one page
    (the .md's rule): the pages concerned are reconciled before a difference
    is called one. The cover's and the half-title's clock-face O is written
    OGNIWO (the editor's ruling): a page whose only difference is one O more
    on the .md's side is reported, not counted.

    For the English (OUT the english.md) the letters cannot be held to the
    Polish layer; instead the marks of the English are held to the marks of
    the original.md (the English .md mirrors the Polish one mark for mark,
    and the Polish one is held to the PDF by the letter check)."""
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
    folios = page_folios(doc)
    # the running heads: every block in the top band of the page (the
    # author's name, the section titles, the Kurzfassung's, the
    # acknowledgements' and the tables of contents' own) - the export leaves
    # them out, and no real heading of this book stands that high; if one
    # did, its page would show the text the .md carries and the check would
    # name it
    heads = {}
    for pno in range(doc.page_count):
        for b in doc[pno].get_text('blocks'):
            if b[3] < 45.5:
                t = ' '.join(b[4].split())
                if t:
                    heads[t] = heads.get(t, 0) + 1
    for t, n in sorted(heads.items(), key=lambda kv: -kv[1]):
        report.append(f'head stripped ({n}x): {t!r}')
    by_pdf, cur = {}, None
    for line in read_lines(OUT):
        m = MARK.match(line)
        if m:
            cur = int(m.group(2))
            by_pdf.setdefault(cur, [])
            continue
        if IMAGE.match(line):
            report.append(f'{os.path.basename(OUT)} still carries a picture '
                          f'line: {line[:60]!r}')
            continue
        if cur is not None:
            by_pdf[cur].append(line)
    wants, gots = [], []
    for pno in range(doc.page_count):
        blocks, h = [], doc[pno].rect.height
        for b in doc[pno].get_text('blocks'):
            t = ' '.join(b[4].split())
            if not t:
                continue
            if b[3] < 45.5 and t in heads:
                continue
            if b[1] > h - 70 and t.isdigit() and len(t) <= 3:
                continue
            blocks.append(b[4])
        wants.append(letters('\n'.join(blocks)))
        gots.append(letters(md_markup.sub('', NOTE_MARK.sub(
            '', '\n'.join(by_pdf.get(pno + 1, []))))))
    from collections import Counter
    bad = 0
    done = set()
    head_letters = {''.join(sorted(letters(t))) for t in heads}
    allow_want, allow_got = Counter(), Counter()   # accepted differences
    for p in range(doc.page_count):
        if p in done:
            continue
        extra_got = Counter(gots[p]) - Counter(wants[p])
        extra_want = Counter(wants[p]) - Counter(gots[p])
        if not extra_got and not extra_want:
            continue
        # the clock-face O of the title (the editor's ruling: OGNIWO)
        if extra_got == Counter({'O': 1}) and not extra_want:
            report.append(f'PDF page {p + 1}: the .md has one O more - the '
                          f'clock-face O of the title, written OGNIWO (the '
                          f"editor's ruling)")
            allow_got += extra_got
            done.add(p)
            continue
        # the print's own repeat of a section title (the tables of contents
        # carry theirs twice; the export has it once - and one letter of the
        # repeated title may stand as a private-use glyph the layer does not
        # carry)
        if extra_want and not extra_got:
            bare = ''.join(sorted(extra_want.elements()))
            hit = bare in head_letters or any(
                sum((Counter(h) - extra_want).values()) == 1
                for h in head_letters)
            if hit:
                report.append(f'PDF page {p + 1}: the print carries a heading '
                              f'twice where the .md has it once')
                allow_want += extra_want
                done.add(p)
                continue
        # a word divided over the page's end, or a spread's captions the
        # export set under one mark: reconciled with the page after
        matched = False
        for q in (p + 1, p + 2):
            if q >= doc.page_count:
                break
            q_want = Counter(wants[q]) - Counter(gots[q])
            q_got = Counter(gots[q]) - Counter(wants[q])
            if extra_got and extra_got == q_want:
                frag = ''.join(sorted(extra_got.elements()))
                if len(frag) <= 12:
                    why = ("the word divided over the page's end, given "
                           'whole on the first page, as the .md sets it')
                else:
                    why = ("the spread's captions the export set under one "
                           'mark, here the first page of the two')
                report.append(f'PDF pages {p + 1}/{q + 1}: {why}')
                done.update((p, q))
                matched = True
                break
            if extra_want and extra_want == q_got:
                frag = ''.join(sorted(extra_want.elements()))
                if len(frag) <= 12:
                    why = ("the word divided over the page's end, given "
                           'whole on the second page, as the .md sets it')
                else:
                    why = ("the spread's captions the export set under one "
                           'mark, here the second page of the two')
                report.append(f'PDF pages {p + 1}/{q + 1}: {why}')
                done.update((p, q))
                matched = True
                break
        if matched:
            continue
        bad += 1
        def show(c):
            return ''.join(sorted(c.elements()))[:60] if c else '-'
        report.append(f'PDF page {p + 1}: the print has {show(extra_want)} '
                      f'the .md has not; the .md has {show(extra_got)} the '
                      f'print has not')
    # nothing lost overall (the accepted allowances excepted)
    total_want, total_got = Counter(), Counter()
    for p in range(doc.page_count):
        total_want += Counter(wants[p])
        total_got += Counter(gots[p])
    if total_got - total_want != allow_got \
            or total_want - total_got != allow_want:
        bad += 1
        report.append('the letters of the print and of the .md are not the '
                      'same overall (the accepted allowances excepted)')
    missing = [p for p in by_pdf if p > doc.page_count]
    if missing:
        report.append(f'{os.path.basename(OUT)} names PDF pages the PDF has '
                      f'not: {missing}')
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
