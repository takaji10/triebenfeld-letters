# -*- coding: utf-8 -*-
"""How the editor's one Markdown transcription became this unit's page files.

    python units/iiihamdaiiinr12366/intake/build_pages.py            # check only
    python units/iiihamdaiiinr12366/intake/build_pages.py --write

A record as much as a tool: it is the one place that says where the text was
cut. The editor's file stays untouched in <raw_dir>. It is written by
paragraph, not by line, and marks the scans a piece covers in square brackets
("[0003-0009]"); the text before the first mark is the cover (0001).

What happens to it here, all decided against the scans:

  * Each written side is a page. A single leaf is `_a`; of an opening, `_a1` is
    the left side and `_a2` the right. Scans 0004 and 0005 are the same opening
    photographed twice, because a slip bound into the gutter hides part of
    either side: the left page is taken from 0004, the right from 0005
    (editor, 2026-10-04).
  * The text is cut where the scan turns the page. PAGES names each page and
    the words it begins with; a cut inside a paragraph leaves that paragraph
    as the last line of one page and the first of the next. One cut falls
    inside a word as transcribed: "spodobniemogą" is "spodob" at the foot of
    0021 right and "niemogą." at the head of 0022 left.
  * A dateline or address the transcription sets at the head of a piece but
    the scribe wrote at its end stands on the page where it is written (MOVES).
  * Markdown is taken off: the backslash escapes, the line-break spaces, and
    the bold and italic marks. The editor's `*` after a word (a reading they
    were unsure of) becomes the edition's `[?]`.

Nothing else is changed. The script checks that the page files, read in order
with spaces ignored, are the source text exactly, apart from the moved lines.
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

SLUG = 'iiihamdaiiinr12366'

# (the source's mark, document number, [(page id, the words the page begins with)]).
# The first page of a block begins where the block does. Document 0 is the cover.
PAGES = [
    ('0001', 0, [('0001_a', None)]),
    # Alopeus to Bernstorff, Berlin, 20 January 1819
    ('0002', 1, [('0002_a', None)]),
    # Copy: the report on Miączyńska's claim, Warsaw, 29 April 1818
    ('0003-0009', 2, [('0003_a', None),
                      ('0004_a1', '1. Kamienno'),
                      ('0005_a2', 'maladie et de la mort'),
                      ('0006_a1', 'dont ils avaient été privés'),
                      ('0006_a2', 'être renvoyé devant'),
                      ('0007_a1', 'disposa des susdit'),
                      ('0007_a2', 'avait été fait, si'),
                      ('0008_a1', 'jugea[?] convenable'),
                      ('0008_a2', 'les créanciers régleront'),
                      ('0009_a', 'de la tutelle de Mme.')]),
    # Draft reply to Alopeus, Berlin, 11 May 1819
    ('0010-0011', 3, [('0010_a', None),
                      ('0011_a', 'Posen, elle')]),
    # Copy: Tarczewski, Warsaw, 16 November 1819
    ('0012', 4, [('0012_a', None)]),
    # Copy: Schöler to Nesselrode, St Petersburg, 10 February 1827
    ('0013-0016', 5, [('0013_a', None),
                      ('0014_a1', 'contracta une dette'),
                      ('0014_a2', '1. Que l'),
                      ('0015_a1', 'Neuf mois'),
                      ('0015_a2', 'tenir aux lois'),
                      ('0016_a1', 'traités existans'),
                      ('0016_a2', 'Kalisz, soit annul')]),
    # Certified extract: judgment of the Kalisz tribunal, 30 July 1827, Polish
    ('0017-0025', 6, [('0017_a', None),
                      ('0018_a1', 'zamieszkałemi Powodaniu'),
                      ('0018_a2', '2. Maryą Anną'),
                      ('0019_a1', 'Instancyi Wojewodztwa Kaliskiego'),
                      ('0019_a2', 'nie iest usprawiedliwione'),
                      ('0020_a1', 'rozbiorem Kraju'),
                      ('0020_a2', 'zostawszy, przeszły'),
                      ('0021_a1', 'ze więc z tych'),
                      ('0021_a2', 'lezy oznaczenie'),
                      ('0022_a1', 'niemogą.'),
                      ('0022_a2', 'ani przywiedziony'),
                      ('0023_a1', 'do swey własnisci'),
                      ('0023_a2', 'Wierzytelnosci iego'),
                      ('0024_a1', 'następuiące Summy'),
                      ('0024_a2', 'Instytutu Edukacyinego'),
                      ('0025_a', 'Za zgodnosc')]),
]

# (the source's mark, how the line begins, where it goes). The line is taken
# from the head of its block and set where it stands on the scan:
#   'end'         after the block's last line
#   'before-last' before the block's last line (a date above the signature)
MOVES = [
    ('0003-0009', 'Varsovie le 29 avril 1818', 'end'),
    ('0013-0016', 'St. Peterburg le 10', 'before-last'),
    ('0013-0016', 'A S. E. Mr. le Comte de', 'end'),
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
        before = sorted(lines)
        for bmark, head, where in MOVES:
            if bmark != mark:
                continue
            hit = [i for i, l in enumerate(lines) if l.startswith(head)]
            if len(hit) != 1:
                problems.append(f'{mark}: moved line "{head}" found {len(hit)} time(s)')
                continue
            l = lines.pop(hit[0])
            lines.insert(len(lines) - 1 if where == 'before-last' else len(lines), l)
        if sorted(lines) != before:
            problems.append(f'{mark}: a move changed the lines')

        # Cut at each page's opening words, searching on from the last cut.
        cuts = [(0, 0)]                          # (line index, offset in line)
        for pid, head in plist[1:]:
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
        for n, (pid, _) in enumerate(plist):
            (i0, o0), (i1, o1) = cuts[n], cuts[n + 1]
            part = []
            for i in range(i0, min(i1 + 1, len(lines))):
                a = o0 if i == i0 else 0
                b = o1 if i == i1 else len(lines[i])
                if lines[i][a:b].strip():
                    part.append(lines[i][a:b].strip())
            if not part:
                problems.append(f'{pid}: no text')
            pages.append((pid, part))
            got.extend(part)
        if squeeze(got) != squeeze(lines):
            problems.append(f'{mark}: the pages do not add up to the source text')
        bounds.append((doc, plist[0][0], 1))

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
