# -*- coding: utf-8 -*-
"""How the scans and the editor's transcription of APP 53/968/0/-/801 became
this unit's page images and page files.

    python units/app539680801/intake/build_pages.py            # check only
    python units/app539680801/intake/build_pages.py --copy     # copy the page images
    python units/app539680801/intake/build_pages.py --write    # write the page files

A record as much as a tool: it is the one place that says which image is which
page and where the text was cut. Follows
units/agad11740273/intake/build_pages.py.

The images. Seventeen images from the archive, Image00035.jpg to
Image00051.jpg: the cover of the unit and sixteen written pages, which carry
the numbers 1 to 16 in red pencil. Each is one page and needs no cropping, so
each is copied unchanged into raw_dir/processed/ as <capture>_a.jpg, as for
APP 53/71/0/-/57. Page ids follow the images: page 1 is 0036_a, page 16 is
0051_a.

The marks. The editor's file marks the pages "[01]" to "[15]", the red
numbers. It has no mark "[16]": the text of page 16 follows that of page 15,
and is cut off here at "Friedrich Siering", the first signature on page 16.

The text. It is by paragraph, not by line. Markdown is taken off (escapes;
the link the editor put on the name of the chamber). One paragraph break
inside a sentence is closed (JOIN): the source breaks "der Flächen." from
"Inhalt von 100 Hufen", which the page writes as one word, "Flächen-Inhalt".
Nothing else is changed here; readings corrected against the scans are in
corrections.py. The script checks that the page files, read in order with
spaces ignored, are the source text exactly.

The cover. The transcription has no text for it. COVER is what stands on it,
read from the image: the stamp of the fonds, the archivist's title and date in
square brackets, and the archive's stamp with fonds and number. It is front
matter, before the document.
"""
import csv
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, ROOT)
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SLUG = 'app539680801'

# image -> page id
IMAGES = [(f'Image{n:05d}.jpg', f'{n:04d}_a') for n in range(35, 52)]

COVER = ('0035_a', [
    'Spuścizna Alberta Breyera',
    '[Odpisy dokumentów w sprawie parcelacji majątków Zagórowo, Wittow i Trąpczyn z lat 1805-1806]',
    '[1930?]',
    'Archiwum Państwowe w Poznaniu',
    'Zespół: Spuśc. A. Breyera',
    'Sygn. 801',
])

# the source's mark -> [(page id, the words the page begins with)]
PAGES = [(f'{n:02d}', [(f'{35 + n:04d}_a', None)]) for n in range(1, 15)]
PAGES.append(('15', [('0050_a', None), ('0051_a', 'Friedrich Siering')]))

# (mark, how the line begins): joined to the line before it with a space.
JOIN = [('07', 'Inhalt von 100 Hufen')]

MARK = re.compile(r'^\\\[(\d{2})\\\]$')


def plain(line):
    """One Markdown line as corpus text."""
    line = line.strip()
    line = re.sub(r'\[([^\]]*)\]\(https?://[^)]*\)', r'\1', line)   # a link: its text
    line = re.sub(r'\\(.)', r'\1', line)                            # the escapes
    return line.strip()


def blocks(path):
    """{mark: [lines]} in source order."""
    out, cur = {}, None
    with open(path, encoding='utf-8-sig') as f:
        for raw in f.read().split('\n'):
            raw = raw.rstrip('\r')
            m = MARK.match(raw.strip())
            if m:
                cur = m.group(1)
                out[cur] = []
            elif raw.strip():
                if cur is None:
                    sys.exit('text before the first mark: ' + raw[:40])
                out[cur].append(plain(raw))
    return out


def squeeze(lines):
    return re.sub(r'\s+', '', ''.join(lines))


def copy_images(unit):
    pdir = os.path.join(unit.raw_dir, 'processed')
    os.makedirs(pdir, exist_ok=True)
    for src, pid in IMAGES:
        shutil.copy2(os.path.join(unit.raw_dir, src), os.path.join(pdir, pid + '.jpg'))
        print(f'  {src} -> processed/{pid}.jpg')


def main():
    unit = unitlib.one_unit(SLUG)
    if '--copy' in sys.argv:
        copy_images(unit)
        return
    write = '--write' in sys.argv
    mds = [f for f in os.listdir(unit.raw_dir) if f.lower().endswith('.md')]
    if len(mds) != 1:
        sys.exit(f'expected one .md in {unit.raw_dir}, found {len(mds)}')
    src = blocks(os.path.join(unit.raw_dir, mds[0]))

    if list(src) != [b for b, _ in PAGES]:
        sys.exit(f'NOT WRITTEN\nsource marks {list(src)} do not match PAGES')

    pages, problems = [COVER], []
    for mark, plist in PAGES:
        lines = list(src[mark])
        whole = squeeze(lines)
        for jmark, head in JOIN:
            if jmark != mark:
                continue
            hit = [i for i, l in enumerate(lines) if l.startswith(head)]
            if len(hit) != 1 or hit[0] == 0:
                problems.append(f'{mark}: joined line "{head}" found {len(hit)} time(s)')
                continue
            lines[hit[0] - 1] += ' ' + lines.pop(hit[0])
        if squeeze(lines) != whole:
            problems.append(f'{mark}: a join changed the text')

        cut = len(lines)
        if len(plist) == 2:
            hit = [i for i, l in enumerate(lines) if l.startswith(plist[1][1])]
            if len(hit) != 1:
                problems.append(f'{plist[1][0]}: "{plist[1][1]}" found {len(hit)} time(s)')
            else:
                cut = hit[0]
        parts = [lines[:cut]] + ([lines[cut:]] if len(plist) == 2 else [])
        for (pid, _), part in zip(plist, parts):
            if not part:
                problems.append(f'{pid}: no text')
            pages.append((pid, part))
        if squeeze(sum(parts, [])) != whole:
            problems.append(f'{mark}: the pages do not add up to the source text')

    if [p for p, _ in pages] != [p for _, p in IMAGES]:
        problems.append('the pages and the images do not match')
    if problems:
        sys.exit('NOT WRITTEN\n' + '\n'.join(problems))
    print(f'{len(src)} marks -> {len(pages)} pages (the cover and 16), one document; '
          f'the pages add up to the source text')
    for pid, part in pages:
        print(f'  {pid:<8} {len(part):>3} lines  {part[0][:40]!r} ... {part[-1][-40:]!r}')
    if not write:
        return

    tdir = os.path.join(UNIT_DIR, 'transcriptions')
    os.makedirs(tdir, exist_ok=True)
    for pid, part in pages:
        with open(os.path.join(tdir, pid + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(part) + '\n')

    rdir = unitlib.review_dir(unit.slug)
    os.makedirs(rdir, exist_ok=True)
    for d in (rdir, HERE):
        with open(os.path.join(d, 'document_boundaries.csv'), 'w', encoding='utf-8',
                  newline='') as f:
            w = csv.writer(f)
            w.writerow(['letter_id', 'first_page', 'first_line'])
            w.writerow([1, '0036_a', 1])
    print('wrote transcriptions/ and document_boundaries.csv')


if __name__ == '__main__':
    main()
