# -*- coding: utf-8 -*-
"""
Crop staged page images by the boxes recorded in a holding's
intake/crops.json (the editor, 2026-11-24: "The following holdings need some
cropping of their pages").

crops.json maps a page image's file name to its box, as fractions of the
uncropped image (left, top, right, bottom), and the size of the uncropped
1100-px derivative it was drawn on:

    {"I_HA_Rep_7_C_Nr_3705_0002_a-L1_01.jpg":
        {"box": [0.478, 0, 1, 1], "from_size": [1100, 896]}}

The file is the record. It is applied to the derivative in site/assets/scans
only while that image still has its uncropped size (so a second run changes
nothing), and make_scan_derivatives.py applies the same boxes when it makes
the derivative again from the original in pages/ on the desktop, so a rebuild
keeps the crop. The originals in pages/ are never cut.

The boxes are drawn on the fold page's box mode (pipeline/intake/fold_page.py)
or set by a script; `python pipeline/intake/apply_crops.py <slug> [<file>]`
copies a saved crops_<slug>.json into the holding first, when given one.

    python pipeline/intake/apply_crops.py <slug>            # apply
    python pipeline/intake/apply_crops.py <slug> saved.json # copy, then apply
    python pipeline/intake/apply_crops.py --all             # every holding
"""
import json, os, shutil, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCANS = os.path.join(ROOT, 'site', 'assets', 'scans')


def load(slug):
    p = os.path.join(ROOT, 'units', slug, 'intake', 'crops.json')
    if not os.path.isfile(p):
        return {}
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def all_crops():
    """Every holding's boxes, keyed by image name (for make_scan_derivatives)."""
    out = {}
    udir = os.path.join(ROOT, 'units')
    for slug in sorted(os.listdir(udir)):
        out.update(load(slug))
    return out


def box_px(entry, size):
    w, h = size
    l, t, r, b = entry['box']
    return (round(l * w), round(t * h), round(r * w), round(b * h))


def crop_image(im, entry):
    return im.crop(box_px(entry, im.size))


def apply(slug):
    crops = load(slug)
    done = same = missing = 0
    for name, entry in crops.items():
        p = os.path.join(SCANS, name)
        if not os.path.isfile(p):
            print(f'  missing: {name}')
            missing += 1
            continue
        with Image.open(p) as im:
            if list(im.size) != list(entry['from_size']):
                same += 1
                continue
            out = crop_image(im.convert('RGB'), entry)
        out.save(p, 'JPEG', quality=78, optimize=True, progressive=True)
        print(f'  cropped: {name} -> {out.size[0]}x{out.size[1]}')
        done += 1
    print(f'{slug}: {done} cropped, {same} already cropped, {missing} missing')
    return missing == 0


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    if argv[0] == '--all':
        ok = all(apply(s) for s in sorted(os.listdir(os.path.join(ROOT, 'units')))
                 if load(s))
        return 0 if ok else 1
    slug = argv[0]
    if len(argv) > 1:
        dst = os.path.join(ROOT, 'units', slug, 'intake', 'crops.json')
        with open(argv[1], encoding='utf-8') as f:
            data = json.load(f)
        with open(dst, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
            f.write('\n')
    return 0 if apply(slug) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
