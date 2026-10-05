# -*- coding: utf-8 -*-
"""How the editor's one Markdown transcription became this unit's page files.

    python units/iiihamdaiiinr12367/intake/build_pages.py            # check only
    python units/iiihamdaiiinr12367/intake/build_pages.py --write

A record as much as a tool: it is the one place that says where the text was
cut. The editor's file stays untouched in <raw_dir>. It marks the scans a
piece covers in square brackets ("[0005-0006]"); the text before the first
mark is the cover (0001). Follows units/iiihamdaiiinr12366/intake/build_pages.py.

What happens to it here, all decided against the scans:

  * Each written side is a page: `_a` for a single leaf; scan 0009 is an
    opening, `_a1` its left side and `_a2` its right.
  * The text is cut where the scan turns the page. PAGES names each page and
    the words it begins with; a cut inside a paragraph leaves that paragraph
    as the last line of one page and the first of the next.
  * The piece marked "[0009]" holds two documents on three pages: Weigel's
    reply of 14 October 1830 (0009 left and the top of 0009 right) and Prince
    Lubecki's letter of 27 November 1830 (the foot of 0009 right, and 0010,
    which the file does not mark). A page entry with a document number starts
    that document on that page, at the line beginning with the words given.
  * Markdown is taken off: the backslash escapes, the line-break spaces, and
    the bold and italic marks. The editor's `*` after a word (a reading they
    were unsure of) becomes the edition's `[?]`.

Nothing else is changed here; the readings corrected against the scans are in
corrections.py. The script checks that the page files, read in order with
spaces ignored, are the source text exactly.
"""
import csv
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, ROOT)
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SLUG = 'iiihamdaiiinr12367'

# (the source's mark, document number, [(page id, the words the page begins
# with[, a document that starts on this page and the words it begins with])]).
# The first page of a block begins where the block does. Document 0 is the cover.
PAGES = [
    ('0001', 0, [('0001_a', None)]),
    # Mohrenheim to Schmidt, Warsaw, 26 January / 7 February 1828
    ('0002', 1, [('0002_a', None)]),
    # Mohrenheim to Schmidt, a note, undated
    ('0003', 2, [('0003_a', None)]),
    # Mohrenheim to Schmidt, a note, undated
    ('0004', 3, [('0004_a', None)]),
    # Mohrenheim to Schmidt, Warsaw, 8/20 February 1830
    ('0005-0006', 4, [('0005_a', None),
                      ('0006_a', 'à la décision de')]),
    # To Schmidt, Warsaw, 29 September 1830
    ('0007', 5, [('0007_a', None)]),
    # Copy: Lubecki to Weigel, Warsaw, 22 September 1830, Polish
    ('0008', 6, [('0008_a', None)]),
    # Copy: Weigel to Lubecki, Breslau, 14 October 1830, German; then
    # copy: Lubecki to Weigel, Warsaw, 27 November 1830, Polish
    ('0009', 7, [('0009_a1', None),
                 ('0009_a2', 'Hierdurch hat sich', 8, 'Nro. 77775'),
                 ('0010_a', 'Jakkolwiek WWPan')]),
    # Fuhrmann to Schmidt, Warsaw, 2/14 December 1831
    ('0011-0012', 9, [('0011_a', None),
                      ('0012_a', 'circonstances j’ai fait')]),
    # Copy: Engel to Schmidt, Warsaw, 1/13 March 1832
    ('0013', 10, [('0013_a', None)]),
    # Fuhrmann to Schmidt, Warsaw, 8/20 March 1832
    ('0014', 11, [('0014_a', None)]),
]

MARK = re.compile(r'^\\\[(\d{4}(?:-\d{4})?)\\\]$')


def plain(line):
    """One Markdown line as corpus text."""
    line = line.strip()
    line = line.replace('\\*', '\x00')          # the editor's doubt mark
    line = line.replace('*', '')                # bold and italic
    line = re.sub(r'\\(.)', r'\1', line)        # the other escapes
    return line.replace('\x00', '[?]').strip()


def blocks(path):
    """{mark: [lines]} in source order; the text before the first mark is 0001."""
    out, cur = {'0001': []}, '0001'
    with open(path, encoding='utf-8-sig') as f:
        for raw in f.read().split('\n'):
            raw = raw.rstrip('\r')
            m = MARK.match(raw.strip())
            if m:
                cur = m.group(1)
                out[cur] = []
            elif raw.strip():
                out[cur].append(plain(raw))
    return out


def squeeze(lines):
    return re.sub(r'\s+', '', ''.join(lines))


def main():
    write = '--write' in sys.argv
    unit = unitlib.one_unit(SLUG)
    mds = [f for f in os.listdir(unit.raw_dir) if f.lower().endswith('.md')]
    if len(mds) != 1:
        sys.exit(f'expected one .md in {unit.raw_dir}, found {len(mds)}')
    src = blocks(os.path.join(unit.raw_dir, mds[0]))

    if list(src) != [b for b, _, _ in PAGES]:
        sys.exit(f'NOT WRITTEN\nsource marks {list(src)} do not match PAGES')

    pages, bounds, problems = [], [], []
    for mark, doc, plist in PAGES:
        lines = list(src[mark])

        # Cut at each page's opening words, searching on from the last cut.
        cuts = [(0, 0)]                          # (line index, offset in line)
        for entry in plist[1:]:
            pid, head = entry[0], entry[1]
            li, off = cuts[-1]
            found = None
            for i in range(li, len(lines)):
                j = lines[i].find(head, off if i == li else 0)
                if j >= 0:
                    found = (i, j)
                    break
            if not found:
                problems.append(f'{pid}: "{head}" not found after the previous cut')
                found = cuts[-1]
            cuts.append(found)
        cuts.append((len(lines), 0))

        got = []
        bounds.append((doc, plist[0][0], 1))
        for n, entry in enumerate(plist):
            pid = entry[0]
            (i0, o0), (i1, o1) = cuts[n], cuts[n + 1]
            part = []
            for i in range(i0, min(i1 + 1, len(lines))):
                a = o0 if i == i0 else 0
                b = o1 if i == i1 else len(lines[i])
                if lines[i][a:b].strip():
                    part.append(lines[i][a:b].strip())
            if not part:
                problems.append(f'{pid}: no text')
            if len(entry) == 4:                  # a document starts on this page
                hit = [k for k, l in enumerate(part) if l.startswith(entry[3])]
                if len(hit) != 1:
                    problems.append(f'{pid}: "{entry[3]}" begins {len(hit)} line(s)')
                else:
                    bounds.append((entry[2], pid, hit[0] + 1))
            pages.append((pid, part))
            got.extend(part)
        if squeeze(got) != squeeze(lines):
            problems.append(f'{mark}: the pages do not add up to the source text')

    if problems:
        sys.exit('NOT WRITTEN\n' + '\n'.join(problems))
    print(f'{len(src)} pieces -> {len(pages)} pages, {len(bounds) - 1} documents and '
          f'the cover; the pages add up to the source text')
    for pid, part in pages:
        print(f'  {pid:<8} {len(part):>3} lines  {part[0][:40]!r} ... {part[-1][-40:]!r}')
    if not write:
        return

    tdir = os.path.join(UNIT_DIR, 'transcriptions')
    os.makedirs(tdir, exist_ok=True)
    for pid, part in pages:
        with open(os.path.join(tdir, pid + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(part) + '\n')

    # review/ is not in the repository, so the sheet is kept here too.
    rdir = unitlib.review_dir(unit.slug)
    os.makedirs(rdir, exist_ok=True)
    for d in (rdir, HERE):
        with open(os.path.join(d, 'document_boundaries.csv'), 'w', encoding='utf-8',
                  newline='') as f:
            w = csv.writer(f)
            w.writerow(['letter_id', 'first_page', 'first_line'])
            w.writerows(b for b in bounds if b[0])
    print('wrote transcriptions/ and document_boundaries.csv')


if __name__ == '__main__':
    main()
