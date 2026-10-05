# -*- coding: utf-8 -*-
"""How the scans and the editor's transcription of AGAD 1/174/0/2/73 became
this unit's page images and page files.

    python units/agad11740273/intake/build_pages.py            # check only
    python units/agad11740273/intake/build_pages.py --crop     # cut the page images
    python units/agad11740273/intake/build_pages.py --write    # write the page files

A record as much as a tool: it is the one place that says which half of which
image is a page, and where the text was cut. Follows
units/iiihamdaiiinr12366/intake/build_pages.py.

The images. The editor has five images of the file (05, 06, 07, 08, 047; the
five long-named files in the folder are the same images again). Each shows an
opening, of which one side is wanted (editor, 2026-10-04: "cropped to remove
the unrelated pages"). CROPS gives that side as a box in pixels: `_a1` is the
left side of the opening, `_a2` the right. The other side is blank, or belongs
to another matter.

The marks. The editor's file marks the pieces "[05]", "[07]", "[08]" and
"[047]". The first three are the pencil leaf numbers written on the pages, not
the image names: leaf 5 is on image 05, leaf 7 on image 06, leaf 8 on image 07
with its back on image 08. "[047]" is image 047, whose leaf is numbered 51.
Page ids follow the images, as everywhere in the edition.

The text. It is by paragraph, not by line. Markdown is taken off (escapes;
`*` after a word would become `[?]`). Two kinds of line are moved, as the
scans have them (MOVES):

  * What the commission's office wrote on a petition (the received note
    "Presentatum ...") goes to the end of that petition's page and is listed
    in office_notes.yml (docs/NEW_UNIT.md, "A file the office wrote on").
  * The address of the French petition stands on the back of its leaf, so it
    is the text of page 0008_a1.

Nothing else is changed here; readings corrected against the scans are in
corrections.py. The script checks that the page files, read in order with
spaces ignored, are the source text exactly, apart from the moved lines.
"""
import csv
import glob
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, ROOT)
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SLUG = 'agad11740273'

# image -> (page id, box: left, top, right, bottom). Placed on a contact sheet
# of the eight pages of the two AGAD holdings, 2026-10-04.
CROPS = [
    ('05.jpg',  '0005_a2', (1740, 110, 3470, 2760)),   # leaf 5: the draft resolution
    ('06.jpg',  '0006_a2', (1750, 60, 3480, 2760)),    # leaf 7: the Polish petition
    ('07.jpg',  '0007_a2', (1750, 60, 3480, 2760)),    # leaf 8: the French petition
    ('08.jpg',  '0008_a1', (60, 60, 1800, 2760)),      # leaf 8, back: its address
    ('047.jpg', '0047_a2', (1790, 40, 3480, 2740)),    # the petition of 23 July
]

# (the source's mark, document number or None to continue the document before,
#  [(page id, the words the page begins with)]).
PAGES = [
    # Draft: resolution of the Governing Commission, Dresden, 21 July 1807
    ('05', 1, [('0005_a2', None)]),
    # Michalina Dąbska to the Governing Commission, Dresden, 20 July 1807
    ('07', 2, [('0006_a2', None)]),
    # Michalina Dąbska to Napoleon, Dresden, 21 July 1807; the address on the back
    ('08', 3, [('0007_a2', None),
               ('0008_a1', 'Jaśnie Wielmożnemu Jegomości')]),
    # Michalina Dąbska to the Governing Commission, Dresden, 23 July 1807
    ('047', 4, [('0047_a2', None)]),
]

# (mark, how the line begins, 'end'): taken from where the transcription has
# it and set after the block's last line. Applied in this order.
MOVES = [
    ('07', 'Presentatum 21. Julii', 'end'),
    ('08', 'Presentatum 21. Lipca', 'end'),
    ('08', 'Jaśnie Wielmożnemu Jegomości', 'end'),
    ('047', 'Presentatum 23. Lipca', 'end'),
]

MARK = re.compile(r'^\\\[(\d{2,4}(?:-\d{2,4})?)\\\]$')


def plain(line):
    """One Markdown line as corpus text."""
    line = line.strip()
    line = line.replace('\\*', '\x00')          # the editor's doubt mark
    line = line.replace('*', '')                # bold and italic
    line = re.sub(r'\\(.)', r'\1', line)        # the other escapes
    return line.replace('\x00', '[?]').strip()


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


def crop(unit):
    from PIL import Image
    pdir = os.path.join(unit.raw_dir, 'processed')
    os.makedirs(pdir, exist_ok=True)
    manifest = {}
    for src, pid, box in CROPS:
        im = Image.open(os.path.join(unit.raw_dir, src)).convert('RGB')
        out = pid + '.jpg'
        im.crop(box).save(os.path.join(pdir, out), quality=97)
        manifest[src] = [{'file': out, 'bbox_original': list(box),
                          'size': [box[2] - box[0], box[3] - box[1]],
                          'fold_confidence': 'manual'}]
        print(f'  {src} -> processed/{out}  {box}')
    with open(os.path.join(pdir, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)


def main():
    unit = unitlib.one_unit(SLUG)
    if '--crop' in sys.argv:
        crop(unit)
        return
    write = '--write' in sys.argv
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
        for bmark, head, _where in MOVES:
            if bmark != mark:
                continue
            hit = [i for i, l in enumerate(lines) if l.startswith(head)]
            if len(hit) != 1:
                problems.append(f'{mark}: moved line "{head}" found {len(hit)} time(s)')
                continue
            lines.append(lines.pop(hit[0]))
        if sorted(lines) != before:
            problems.append(f'{mark}: a move changed the lines')

        cuts = [(0, 0)]
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
        if doc is not None:
            bounds.append((doc, plist[0][0], 1))

    if problems:
        sys.exit('NOT WRITTEN\n' + '\n'.join(problems))
    print(f'{len(src)} pieces -> {len(pages)} pages, {len(bounds)} documents; '
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
            w.writerows(bounds)
    print('wrote transcriptions/ and document_boundaries.csv')


if __name__ == '__main__':
    main()
