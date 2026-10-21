# -*- coding: utf-8 -*-
"""APP 53/1455/0/2/21: from the editor's photographs to the edition.

    python units/app5314550221/intake/holding.py            # check only
    ... --crop        cut the five pages out of the photographs into raw_dir/processed/
    ... --write       page files and corpus.txt from intake/text.py
    ... --english     write translation/doc<N>.yml from intake/english.py
    ... --cache       put them into the translation cache
    ... --summaries   write the summaries S everywhere they are kept

This file is the record of what was done to this holding (2026-10-21). Apart
from --crop, the steps are those of courtbook.holding_main
(pipeline/intake/courtbook.py).

The unit is a copy-book of the privileges of the Cistercian abbey of Ląd,
"Series privilegiorum monasterii Landensis transcripta ex libro
privilegiorum", in the fond Klasztor cystersów w Lądzie (53/1455) of the
State Archive in Poznań. The editor photographed the cover and the pages
with a camera, IMG_5217 to IMG_5251 (Canon raw files, .CR2; IMG_5239 as a
.jpg), and gave the pages to edit (2026-10-21): pages 13-14, 25-26 and 66,
by the archive's pagination in pencil at the top outer corner of each page
(not the older numbers in red crayon beside it). Page 15 was added the
same day to finish the king's confirmation, no. 16, and is cut below its end.
Which photograph is which page was read off those numbers: p. 13 is
IMG_5221, p. 14 IMG_5222, p. 15 IMG_5223, p. 25
IMG_5226, p. 26 IMG_5227, p. 66 IMG_5245. Each photograph shows one page
whole, turned on its side, with a strip of the facing page. The editor's
own cropped .jpg files in the folder (IMG_5220a and b, IMG_5225a and b,
IMG_5239) are other pages (pp. 5, 6, 18-20 and 54) and are not used.

No raw converter is installed here: the page is taken from the full-size
JPEG preview inside each .CR2 (5184 x 3456; units/app539680669/intake/
photos.py, preview()), turned upright and cut to the box in BOXES, in pixels
of the upright picture. The top of p. 13 and the top of p. 25 belong to
entries that begin on earlier pages, and the box starts below them, at the
heading of the first privilege that begins on the page (the editor: "trim
any text on those pages that are parts of other sections from previous/
earlier pages"). What is left out is said in intake/text.py.

The text was read from these pictures, enlarged, in session (intake/
text.py); the English is intake/english.py.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
sys.path.insert(0, os.path.join(ROOT, 'units', 'app539680669', 'intake'))
sys.path.insert(0, HERE)
import courtbook  # noqa: E402
import text  # noqa: E402

SLUG = 'app5314550221'
REF = 'APP 53/1455/0/2/21'
RAW = (r"J:\Documents\Archive\Genealogy\References\Poznań State Archives"
       r"\Series privilegiorium monasterii Landensis transcripta ex libro privilegiorum (53.1455.0.2.21)")

# page id: (photograph, degrees to turn it counter-clockwise, box (left, top, right, bottom)
# in the upright picture). Top of 0013_a and 0025_a: below the end of the entry before.
BOXES = {
    '0013_a': ('IMG_5221.CR2', 90, (330, 1455, 3110, 4795)),
    '0014_a': ('IMG_5222.CR2', 90, (240, 444, 2700, 4722)),
    # p. 15, added at the editor's word to finish no. 16: cut below its end,
    # above the heading of no. 17, which is not in the edition
    '0015_a': ('IMG_5223.CR2', -90, (640, 820, 2950, 3135)),
    '0025_a': ('IMG_5226.CR2', -90, (380, 1507, 2650, 4537)),
    '0026_a': ('IMG_5227.CR2', -90, (480, 722, 2790, 4444)),
    '0066_a': ('IMG_5245.CR2', -90, (555, 444, 2905, 4370)),
}
LEAF = {'0013_a': 'p. 13', '0014_a': 'p. 14', '0015_a': 'p. 15', '0025_a': 'p. 25', '0026_a': 'p. 26', '0066_a': 'p. 66'}
SCANS = []          # the photographs are raw files: --crop below cuts them, not courtbook.cut
DOCS = text.DOCS
ROWS = []           # the text was read whole from the photographs: text.py is the record


def crop():
    from photos import preview
    out = os.path.join(RAW, 'processed')
    os.makedirs(out, exist_ok=True)
    for pid, (name, turn, box) in sorted(BOXES.items()):
        im = preview(os.path.join(RAW, name)).convert('RGB').rotate(turn, expand=True)
        im.crop(box).save(os.path.join(out, pid + '.jpg'), quality=92)
        print('cut', pid, 'from', name)


def read_source():
    return dict(text.TEXT)


def english():
    import english as E
    return {n: [E.ENGLISH[(n, pid)] for pid in ids] for n, ids in DOCS}


def _summaries():
    try:
        import english as E
        return E.S, E.HOW
    except ImportError:
        return {}, ''


S, HOW = _summaries()

if __name__ == '__main__':
    if '--crop' in sys.argv:
        crop()
        sys.argv.remove('--crop')
    courtbook.holding_main(globals())
