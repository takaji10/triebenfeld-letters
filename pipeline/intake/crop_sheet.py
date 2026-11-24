# -*- coding: utf-8 -*-
"""
The crop page for one or more holdings: the fold page's box mode
(fold_page.render(boxes=True)) over every staged page image of the holdings
given, the pictures embedded so that the one HTML file works anywhere.

    python pipeline/intake/crop_sheet.py <slug> [<slug> ...] [--out PATH]

Images: units/<slug>/page_scan_map.csv, column `image` (front matter rows
too), the files in site/assets/scans/; ordered by holding, then file name.
Default --out: review/crops/index.html.

A box already recorded in units/<slug>/intake/crops.json is prefilled when
the image on disk still has the size it was drawn on; when the image is
smaller (the crop has been applied) it is labelled "already cropped" and
not prefilled. The saved file is grouped, {slug: {file: {box, from_size}}};
apply it with `python pipeline/intake/apply_crops.py --grouped saved.json`.
"""
import base64, csv, io, json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fold_page

ROOT = os.path.dirname(os.path.dirname(HERE))
SCANS = os.path.join(ROOT, 'site', 'assets', 'scans')


def images(slug):
    p = os.path.join(ROOT, 'units', slug, 'page_scan_map.csv')
    with open(p, encoding='utf-8-sig', newline='') as f:
        names = {r['image'] for r in csv.DictReader(f) if r.get('image')}
    return sorted(names)


def items_for(slug):
    cp = os.path.join(ROOT, 'units', slug, 'intake', 'crops.json')
    crops = {}
    if os.path.isfile(cp):
        with open(cp, encoding='utf-8') as f:
            crops = json.load(f)
    out = []
    for name in images(slug):
        p = os.path.join(SCANS, name)
        if not os.path.isfile(p):
            print(f'  missing: {slug} {name}')
            continue
        with Image.open(p) as im:
            w, h = im.size
        with open(p, 'rb') as f:
            src = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('ascii')
        item = {'slug': slug, 'file': name, 'src': src, 'w': w, 'h': h, 'label': f'{slug}  {name}'}
        c = crops.get(name)
        if c:
            if [w, h] == list(c['from_size']):
                item['box'] = c['box']
            else:
                item['label'] += '  (already cropped)'
        out.append(item)
    return out


def main(argv):
    out = os.path.join(ROOT, 'review', 'crops', 'index.html')
    if '--out' in argv:
        k = argv.index('--out')
        out = argv[k + 1]
        argv = argv[:k] + argv[k + 2:]
    if not argv:
        print(__doc__)
        return 1
    items = []
    for slug in argv:
        items += items_for(slug)
    save = f'crops_{argv[0]}.json' if len(argv) == 1 else 'crops_grouped.json'
    html = fold_page.render(', '.join(argv), items, save=save, key='crops:' + ','.join(argv),
                            boxes=True, grouped=len(argv) > 1)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print(f'{out}: {len(items)} images, {os.path.getsize(out) // 1024} KB')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
