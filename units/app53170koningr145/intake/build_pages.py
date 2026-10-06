# -*- coding: utf-8 -*-
"""How the scans and the editor's transcription of APP 53/17/0/-/Konin Gr.145
became this unit's page images, page files and corpus.

    python units/app53170koningr145/intake/build_pages.py            # check only
    python units/app53170koningr145/intake/build_pages.py --crop     # cut the page images
    python units/app53170koningr145/intake/build_pages.py --write    # write page files and corpus.txt

A record as much as a tool: it is the one place that says which image is which
page and where the text was cut.

The images. Sixty-two scans from the archive, 654.jpg to 715.jpg, each an
opening of the bound court book. The scan is named after the leaf on its right:
scan 673 shows leaf 672 verso on the left and leaf 673 recto on the right. Each
is cut at the fold (FOLDS, the darkest column near the middle of the opening,
found by a script and checked on contact sheets, 2026-10-06) into
<scan>_a1.jpg, the left page, and <scan>_a2.jpg, the right page, in
raw_dir/processed/. Scan numbers are written with four digits there, as in the
other holdings.

Which pages are the document. The entry begins on leaf 654 recto, its title
page (0654_a2), and ends on leaf 715 recto (0715_a2): 122 pages. Two halves are
cut but left out of the edition (SKIP): 0654_a1, which is the end of another
entry of the book, and 0655_a1, leaf 654 verso, which is blank and crossed
through.

The text. The editor's file marks each page by its leaf, "[655]" for the recto
and "[655v]" for the verso. Leaf N recto is page <N>_a2; leaf N verso is page
<N+1>_a1. The title page has no mark: its text stands before "[655]". The text
is by paragraph, not by line. Markdown is taken off: the escapes before square
brackets, and the asterisks the editor put round Latin words. Nothing else is
changed here; what was corrected against the scans is in corrections.py. The
script checks that the page files, read in order with spaces ignored, are the
source text exactly.

The file's heading, its line "ff. 654-715", and "Languages: Polish and Latin"
are the editor's and are not part of the text. Nor is the one footnote, an
English rendering of the Latin record of the Warsaw court on leaf 656; it and
its mark in the text are left out.
"""
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes-oblatae [protocollon] 1776 (53.17.0.-.Konin Gr.145)"
PROCESSED = os.path.join(RAW, 'processed')
FIRST, LAST = 654, 715
SKIP = {'0654_a1', '0655_a1'}

# x of the fold on each scan, in pixels from the left.
FOLDS = {
    654: 2488, 655: 2572, 656: 2592, 657: 2608, 658: 2616, 659: 2624, 660: 2504, 661: 2528,
    662: 2780, 663: 2548, 664: 2492, 665: 2648, 666: 2652, 667: 2528, 668: 2640, 669: 2696,
    670: 2452, 671: 2436, 672: 2388, 673: 2460, 674: 2492, 675: 2444, 676: 2456, 677: 2460,
    678: 2484, 679: 2464, 680: 2464, 681: 2424, 682: 2436, 683: 2540, 684: 2484, 685: 2460,
    686: 2556, 687: 2444, 688: 2480, 689: 2512, 690: 2464, 691: 2500, 692: 2524, 693: 2488,
    694: 2512, 695: 2536, 696: 2496, 697: 2520, 698: 2544, 699: 2512, 700: 2540, 701: 2520,
    702: 2484, 703: 2496, 704: 2524, 705: 2476, 706: 2576, 707: 2740, 708: 2548, 709: 2572,
    710: 2576, 711: 2512, 712: 2552, 713: 2520, 714: 2616, 715: 2548,
}

HEADER_DROP = (
    '# Relationes-oblatae [protocollon] 1776 - Polish Original',
    '* ff. 654-715 (53/17/0/-/Konin Gr.145)*',
    'Languages: Polish and Latin',
)


def page_id(leaf):
    """'655' -> '0655_a2'; '655v' -> '0656_a1'."""
    if leaf.endswith('v'):
        return '%04d_a1' % (int(leaf[:-1]) + 1)
    return '%04d_a2' % int(leaf)


def page_ids():
    ids = []
    for n in range(FIRST, LAST + 1):
        for half in ('a1', 'a2'):
            pid = '%04d_%s' % (n, half)
            if pid not in SKIP:
                ids.append(pid)
    return ids


def plain(text):
    """Markdown off: escapes before brackets and full stops, asterisks round Latin."""
    text = re.sub(r'\\([\[\]\.\-\*_#~])', r'\1', text)
    return text.replace('*', '')


def read_source():
    f = glob.glob(os.path.join(glob.escape(RAW), '*Polish Original.md'))
    assert len(f) == 1, f
    s = io.open(f[0], encoding='utf-8-sig').read().replace('\r\n', '\n')
    # The editor's one footnote, an English rendering of a Latin passage: not text of the page.
    s = re.sub(r'(?m)^\\?\[\^\d+\\?\]:.*\n?', '', s)
    s = re.sub(r'\\?\[\^\d+\\?\]', '', s)
    parts =re.split(r'\n\\\[(\d+v?)\\\]\n', s)
    head, leaves, texts = parts[0], parts[1::2], parts[2::2]
    head_lines = [l for l in head.split('\n') if l.strip() and l.strip() not in HEADER_DROP]
    pages = [('0654_a2', head_lines)]
    for leaf, text in zip(leaves, texts):
        pages.append((page_id(leaf), [l for l in text.split('\n') if l.strip()]))
    pages = [(pid, [re.sub(r'\s+', ' ', plain(l)).strip() for l in lines]) for pid, lines in pages]
    # the check: nothing lost, nothing added
    src = plain(s)
    for d in HEADER_DROP:
        src = src.replace(plain(d), '', 1)
    src = re.sub(r'\n\[(\d+v?)\]\n', '\n', src)
    got = ''.join(''.join(lines) for _, lines in pages)
    assert re.sub(r'\s+', '', src) == re.sub(r'\s+', '', got), 'page files do not add up to the source text'
    return pages


def crop():
    from PIL import Image
    os.makedirs(PROCESSED, exist_ok=True)
    for n in range(FIRST, LAST + 1):
        im = Image.open(os.path.join(RAW, '%d.jpg' % n)).convert('RGB')
        x = FOLDS[n]
        for half, box in (('a1', (0, 0, x, im.height)), ('a2', (x, 0, im.width, im.height))):
            im.crop(box).save(os.path.join(PROCESSED, '%04d_%s.jpg' % (n, half)), quality=92)
    print('cut', (LAST - FIRST + 1) * 2, 'page images into', PROCESSED)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    pages = read_source()
    want = [p for p in page_ids()]
    have = [pid for pid, _ in pages]
    assert have == want, ('pages out of step', [p for p in want if p not in have][:5], [p for p in have if p not in want][:5])
    words = sum(len(' '.join(lines).split()) for _, lines in pages)
    print(len(pages), 'pages,', sum(len(l) for _, l in pages), 'paragraphs,', words, 'words; source text reproduced exactly')
    if '--crop' in sys.argv:
        crop()
    if '--write' in sys.argv:
        tdir = os.path.join(UNIT_DIR, 'transcriptions')
        os.makedirs(tdir, exist_ok=True)
        for pid, lines in pages:
            io.open(os.path.join(tdir, pid + '.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
        out = ['[DOC 1]']
        for pid, lines in pages:
            out.append('[PAGE %s]' % pid)
            out.extend(lines)
        io.open(os.path.join(UNIT_DIR, 'corpus.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
        print('wrote', len(pages), 'page files and corpus.txt')


if __name__ == '__main__':
    main()
