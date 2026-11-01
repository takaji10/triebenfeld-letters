# -*- coding: utf-8 -*-
"""Stage the scan of B. Ossol. rkp. 2289 II, page 145, into pages/.

The holding's scans are thirty TIFFs of the digitised manuscript (leaves
0033-0062, files NBO-2289--<nnnn>.tif, 1990x3150, greyscale), downloaded by
the editor into Downloads/Ossolineum/. Intake is selective: the one document
transcribed so far is the copy of Kościuszko's letter of 3 September 1798,
which stands on manuscript page 145 - scan 0062 of the set (the editor,
2026-11-01). This converts that one TIFF into pages/ under the unit's
staged name, NBO_2289_0145_a.jpg (the page id 0145_a is the manuscript's
own pagination), and records the provenance in scan_rename_map.json. The
remaining 29 scans stay on disk, unscreened into the edition.

The conversion is a copy in spirit: the greyscale TIFF becomes a JPEG of
the same pixel size, nothing cropped, nothing sharpened. make_scan_derivatives.py
makes the web-sized copy from it.

Run:  py -3 units/ossol2289/intake/build_pages.py
"""
import json
import os
import shutil
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))), 'pipeline'))
import unitlib

UNIT = unitlib.one_unit('ossol2289')
ROOT = unitlib.ROOT

src = os.path.join(UNIT.raw_dir, 'NBO-2289--0062.tif')
staged = 'NBO_2289_0145_a.jpg'
dst = os.path.join(ROOT, 'pages', staged)

os.makedirs(os.path.dirname(dst), exist_ok=True)
if not os.path.isfile(dst):
    with Image.open(src) as im:
        im = im.convert('L')
        im.save(dst, 'JPEG', quality=92)
    print('converted', os.path.basename(src), '->', staged, Image.open(dst).size)
else:
    print('already there', staged)

# The provenance record, in the shape stage_pages.py writes it: original
# name -> staged name. The unit is staged by hand (this script), so the map
# is written here and merged with whatever stage_pages may later record.
map_path = os.path.join(UNIT.dir, 'scan_rename_map.json')
rename = {}
if os.path.isfile(map_path):
    with open(map_path, encoding='utf-8') as f:
        rename = json.load(f)
rename.setdefault('NBO-2289--0062.tif', staged)
with open(map_path, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(dict(sorted(rename.items())), f, ensure_ascii=False, indent=1)
    f.write('\n')
print('rename map:', rename)
