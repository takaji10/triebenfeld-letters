# -*- coding: utf-8 -*-
"""APP 53/968/0/-/716: the editor's raw photos IMG_5159 to IMG_5180, made into images of the paper.

    python units/app539680716/intake/photos.py

The editor photographed the unit on a table in April 2023 as Canon raw files
(.CR2). No raw converter is installed: each CR2 carries the camera's
full-size JPEG (5184 x 3456), which is taken out of the file (the largest
embedded JPEG that opens; the helper is that of 53/968/0/-/669) and cut to
the paper by BOXES into PHOTOS under the unit's folder. All 22 photos carry
the orientation flag 1 (upright).

- IMG_5159 shows three things side by side: the archive's title page, the
  notebook's cover and the loose sheet. Only the title page is taken from it
  (editor, 2026-10-14); the other two are photographed again (5160 to 5162).
- IMG_5160 shows the loose sheet of 1858 lying sideways, its front; it is
  turned 90 degrees anticlockwise (TURN). IMG_5161 shows its back, upright.
- IMG_5168 and IMG_5169 are the same opening, photographed twice; 5169 is
  used and 5168 left out (holding.py says which).
Boxes were found by the saturation of the wood against the paper and checked
by eye, with a margin.
"""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

def preview(path):
    """The camera's full-size JPEG in a CR2: the helper of 53/968/0/-/669, loaded by its path (both files are photos.py)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'photos669', os.path.join(ROOT, 'units', 'app539680669', 'intake', 'photos.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.preview(path)

RAW = (r"J:\Documents\Archive\Genealogy\References\Poznań State Archives"
       r"\Łazińsk [woj. poznańskie][Emalienheim] - [notatki różnej treści, zestawienia] (53.968.0.-.716)")
PHOTOS = 'photos'

# (left, top, right, bottom) in the camera's full-size JPEG, margin included.
BOXES = {
    5159: (380, 800, 2090, 2700),
    5160: (600, 420, 4250, 2900),
    5161: (1400, 760, 5184, 3456),
    5162: (1550, 560, 3450, 3100),
    5163: (620, 630, 3910, 3020),
    5164: (870, 540, 4200, 3040),
    5165: (880, 590, 4160, 3030),
    5166: (880, 540, 4100, 2950),
    5167: (910, 630, 4140, 3040),
    5168: (930, 650, 4100, 3040),
    5169: (970, 620, 4130, 2970),
    5170: (1010, 600, 4180, 2960),
    5171: (920, 730, 4190, 3160),
    5172: (910, 650, 4140, 3060),
    5173: (990, 590, 4240, 3000),
    5174: (890, 540, 4190, 2970),
    5175: (940, 500, 4240, 2940),
    5176: (980, 520, 4280, 2940),
    5177: (990, 540, 4300, 2970),
    5178: (920, 580, 4290, 3040),
    5179: (950, 580, 4320, 3040),
    5180: (1000, 640, 3090, 3100),
}
# degrees anticlockwise, applied after the cut
TURN = {5160: 90}


def main():
    out = os.path.join(RAW, PHOTOS)
    os.makedirs(out, exist_ok=True)
    for n, box in sorted(BOXES.items()):
        im = preview(os.path.join(RAW, 'IMG_%d.CR2' % n)).convert('RGB')
        assert im.size == (5184, 3456), im.size
        im = im.crop(box)
        if n in TURN:
            im = im.rotate(TURN[n], expand=True)
        im.save(os.path.join(out, 'IMG_%d.jpg' % n), quality=93)
    print(len(BOXES), 'photos cut to the paper in', out)


if __name__ == '__main__':
    main()
