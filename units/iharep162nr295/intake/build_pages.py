# -*- coding: utf-8 -*-
"""How the editor's photographs of GStA PK, I. HA Rep. 162, Nr. 295 became
this unit's page images.

    python units/iharep162nr295/intake/build_pages.py            # check only
    python units/iharep162nr295/intake/build_pages.py --crop     # make the page images

A record as much as a tool: it is the one place that says which photographs
make up which page, where the two were joined and where the page was cut out.
Follows units/agad11740273/intake/build_pages.py.

The photographs. 23 images taken on 28 July 2023 with a telephone held over
the file. The first is the cover. The other 22 are eleven pages, each taken
twice: once over the top of the page and once over the bottom, so that the two
overlap by half a page and more, and the same lines of writing stand in both.
Fed to a transcription tool as they are, every page would give those lines
twice.

The page images. Each pair is joined into one image of the whole page:

  * The bottom photograph is laid on the top one by a projective transformation
    (`coeffs` in stitch.json), found from several hundred points that the two
    share; `check` gives how many, and how far they lie apart after the
    transformation (about 1.5 pixels in the middle, under 3 for 95 in 100).
    The top photograph is left as it was taken.
  * The two are joined along a seam (`seam`) that runs through the gap between
    two lines of writing, inside the part both photographs show. Above it the
    page is the top photograph, below it the bottom one, so no line of
    writing is doubled or lost, and none is pieced together from the two. The
    seam was searched for as the path across the page that touches the least
    ink in either photograph (`check`, `seam_near_ink`: the share of its
    length that comes near any, the tail of a letter at most); over 12 pixels
    the one image fades into the other.
  * The bottom photograph is brightened or darkened to match the top one along
    the seam, because the light fell differently on the two (`gain_r`,
    `gain_g`, `gain_b`: a factor for the middle of each of 24 equal columns
    across the width, measured on the bare paper beside the seam).
  * CROPS then cuts the page out of the joined image: left, top, right, bottom
    in pixels of the top photograph. Placed on a gridded contact sheet,
    2026-10-05. The cut is at the fold, so the page opposite is not in the
    image. The fold does not run straight down the photographs, so on 0008_a
    and 0010_a the cut takes a strip of blank margin with it, to keep out the
    line ends of the page before.

The numbers in stitch.json were found by find_stitch.py, beside this file,
which needs OpenCV. They are applied here with Pillow alone, so the page
images can be made again without it.

Page ids. `0001_a` is the cover; `0002_a` to `0012_a` are the eleven pages in
the order they were photographed, which is the order of the file. The pages
carry no leaf numbers in the photographs.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, ROOT)
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SLUG = 'iharep162nr295'
PREFIX = 'I_HA_Rep_162_Nr_295_'
COVER = 'PXL_20230728_101209718.jpg'
FEATHER = 6          # Gaussian radius of the fade across the seam, in pixels

# page id -> box (left, top, right, bottom) cut out of the joined image; for
# the cover, out of its one photograph.
CROPS = {
    '0001_a': (200, 90, 2720, 3990),     # the cover
    '0002_a': (62, 500, 3010, 5200),      # "Abschrift": the bond, Berlin, 28 January 1805
    '0003_a': (0, 500, 2880, 5000),
    '0004_a': (130, 440, 2850, 4900),    # its end; "Actum Berlin, den 28. Januar 1805"
    '0005_a': (0, 540, 2890, 5300),      # "Wir Friedrich Wilhelm ..."
    '0006_a': (125, 430, 2880, 5080),    # "Actum Kalisch, den 27. Februar 1805"
    '0007_a': (0, 300, 2850, 4800),      # the entry in the mortgage book
    '0008_a': (225, 600, 3010, 5200),    # its end; the mortgage certificate begins
    '0009_a': (0, 440, 2730, 4950),
    '0010_a': (170, 360, 2840, 4900),
    '0011_a': (35, 400, 2700, 5200),
    '0012_a': (0, 250, 2900, 5080),      # its end, Kalisch, 13 March 1805; the next begins
}


def join(raw_dir, rec):
    """The whole page: the top photograph, and below the seam the bottom one."""
    from PIL import Image, ImageDraw, ImageFilter, ImageMath
    w, h = rec['canvas']
    top = Image.open(os.path.join(raw_dir, rec['top'])).convert('RGB')
    bottom = Image.open(os.path.join(raw_dir, rec['bottom'])).convert('RGB')
    if top.size[0] != w:
        sys.exit(f"{rec['top']}: {top.size[0]} pixels wide, stitch.json expects {w}")

    laid = bottom.transform((w, h), Image.Transform.PERSPECTIVE, rec['coeffs'],
                            Image.Resampling.BICUBIC)

    # the gain: one value per column of the page, run smoothly into the next
    bands = []
    for band, key in zip(laid.split(), ('gain_r', 'gain_g', 'gain_b')):
        gain = Image.new('F', (len(rec[key]), 1))
        gain.putdata(rec[key])
        gain = gain.resize((w, h), Image.Resampling.BILINEAR)
        bands.append(ImageMath.lambda_eval(
            lambda a: a['convert'](a['float'](a['c']) * a['g'] + 0.5, 'L'), c=band, g=gain))
    laid = Image.merge('RGB', bands)

    below = Image.new('L', (w, h), 0)
    ImageDraw.Draw(below).polygon([tuple(p) for p in rec['seam']] + [(w, h), (0, h)], fill=255)
    below = below.filter(ImageFilter.GaussianBlur(FEATHER))

    page = Image.new('RGB', (w, h))
    page.paste(top, (0, 0))
    return Image.composite(laid, page, below)


def main():
    unit = unitlib.one_unit(SLUG)
    with open(os.path.join(HERE, 'stitch.json'), encoding='utf-8') as f:
        stitch = json.load(f)
    if sorted(stitch) != sorted(p for p in CROPS if p != '0001_a'):
        sys.exit('stitch.json and CROPS do not name the same pages')

    used = [COVER] + [stitch[p][k] for p in sorted(stitch) for k in ('top', 'bottom')]
    have = sorted(f for f in os.listdir(unit.raw_dir) if f.startswith('PXL_'))
    missing = [f for f in used if f not in have]
    if missing:
        sys.exit(f'not in {unit.raw_dir}: {missing}')
    print(f'{len(have)} photographs, {len(used)} used -> {len(CROPS)} pages')
    for pid in sorted(CROPS):
        src = COVER if pid == '0001_a' else f"{stitch[pid]['top']} + {stitch[pid]['bottom']}"
        box = CROPS[pid]
        print(f'  {pid}  {box[2] - box[0]} x {box[3] - box[1]}  {src}')
    if '--crop' not in sys.argv:
        return

    from PIL import Image
    pdir = os.path.join(unit.raw_dir, 'processed')
    os.makedirs(pdir, exist_ok=True)
    manifest = {}
    for pid in sorted(CROPS):
        box = CROPS[pid]
        if pid == '0001_a':
            im = Image.open(os.path.join(unit.raw_dir, COVER)).convert('RGB')
            sources = [COVER]
        else:
            im = join(unit.raw_dir, stitch[pid])
            sources = [stitch[pid]['top'], stitch[pid]['bottom']]
        out = PREFIX + pid + '.jpg'
        im.crop(box).save(os.path.join(pdir, out), quality=95)
        manifest[out] = {'sources': sources, 'bbox_joined': list(box),
                         'size': [box[2] - box[0], box[3] - box[1]]}
        print(f'  wrote processed/{out}')
    with open(os.path.join(pdir, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
