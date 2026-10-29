# -*- coding: utf-8 -*-
"""
The sources lists' pictures: one thumbnail per card of the four lists.

The materials lists (the archival holdings, the newspapers, the literature,
the maps) show each item as a card with a picture of the thing itself, a
first page. The thumbs are reduced to 400px wide and kept in
site/assets/thumbs/ under kind-prefixed names, so the four kinds of item
cannot collide:

  holding-<slug>.jpg   a holding's first page, from the scan derivative of
                       the first document in the holding's archival order
                       (the same first page the holding's own list shows)
  np-<slug>.jpg        a press item's first clipping page, from the item's
                       picture in site/assets/newspapers/<slug>/
  lit-<slug>.jpg       a work's first imaged page, from its figures
                       (dataset/literature/index.json)
  map-<key>.jpg        a map's whole face, fetched from its published
                       tiles' lowest whole-map level (scale 1/32; the tile
                       service has no other whole-map level)

The generators write `thumb:` into the site's data only when the file is
here, so the pages never show an image the site does not carry. Re-running
skips what is already current (the source's stamp against the thumb's), so
it is cheap to call after the lists change. Runs in pipeline/regenerate.py
after the literature is built and before the site's pages are generated.

    python pipeline/build/make_thumbs.py           # make what's missing
    python pipeline/build/make_thumbs.py --force   # rebuild everything
    python pipeline/build/make_thumbs.py --prune   # also delete orphans
"""
import io, os, re, sys, time, json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unitlib
import yaml
from PIL import Image
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
THUMBS = os.path.join(ROOT, 'site', 'assets', 'thumbs')
SCANS = os.path.join(ROOT, 'site', 'assets', 'scans')
NP_ASSETS = os.path.join(ROOT, 'site', 'assets', 'newspapers')
LIT_ASSETS = os.path.join(ROOT, 'site', 'assets', 'literature')
MAPS_YML = os.path.join(ROOT, 'reference', 'maps.yml')

WIDTH = 400
QUALITY = 80

FORCE = '--force' in sys.argv
PRUNE = '--prune' in sys.argv


def reduce_to_thumb(src, dst):
    """One file's thumb: open, downscale to WIDTH, save beside the others."""
    with Image.open(src) as im:
        # draft() lets the JPEG decoder downscale while reading - much faster
        # than decoding at full size and resizing afterwards.
        im.draft('RGB', (WIDTH * 2, WIDTH * 2))
        im = im.convert('RGB')
        im.thumbnail((WIDTH, WIDTH * 4), Image.LANCZOS)
        im.save(dst, 'JPEG', quality=QUALITY, optimize=True, progressive=True)


def make(src, dst, expected):
    """Make one thumb if wanted: returns 'made' or 'current'."""
    expected.add(os.path.basename(dst))
    if not FORCE and os.path.isfile(dst) \
            and os.path.getmtime(dst) >= os.path.getmtime(src):
        return 'current'
    reduce_to_thumb(src, dst)
    return 'made'


def first_page_scan():
    """unit slug -> the first page's scan file, in the holdings' own order.

    The same reading the units.yml row and the holding's own list stand on:
    the first document of the archival order, and the lowest numbered page
    of it whose scan is mapped."""
    out = {}
    def num_of(lid):
        return int(re.match(r'(\d+)', lid).group(1))
    for r in unitlib.load_documents(ROOT):
        for p in (r.get('pages') or []):
            if p.get('scan'):
                key = (num_of(r['letter_id']), p['page'])
                cur = out.get(r['unit'])
                if cur is None or key < cur[0]:
                    out[r['unit']] = (key, p['scan'])
    return {slug: fp[1] for slug, fp in out.items()}


def holdings(expected):
    made = 0
    count = 0
    for slug, scan in sorted(first_page_scan().items()):
        src = os.path.join(SCANS, scan)
        if not os.path.isfile(src):
            print(f'holding {slug}: scan derivative {scan} missing, no thumb')
            continue
        count += 1
        dst = os.path.join(THUMBS, f'holding-{slug}.jpg')
        if make(src, dst, expected) == 'made':
            made += 1
    return made, count


def newspapers(expected):
    made = 0
    count = 0
    for slug in sorted(os.listdir(os.path.join(ROOT, 'newspapers'))):
        item_p = os.path.join(ROOT, 'newspapers', slug, 'item.yml')
        if not os.path.isfile(item_p):
            continue
        with open(item_p, encoding='utf-8') as f:
            it = yaml.safe_load(f)
        img = (it or {}).get('image')
        src = os.path.join(NP_ASSETS, slug, img or '')
        if not img or not os.path.isfile(src):
            continue
        count += 1
        dst = os.path.join(THUMBS, f'np-{slug}.jpg')
        if make(src, dst, expected) == 'made':
            made += 1
    return made, count


def literature(expected):
    made = 0
    count = 0
    with open(os.path.join(ROOT, 'dataset', 'literature', 'index.json'),
              encoding='utf-8') as f:
        works = json.load(f)
    for w in works:
        figs = w.get('figures') or {}
        if not figs:
            continue
        # the work's first numbered page of those that have a picture,
        # imaged or not
        src = None
        for key in sorted(figs, key=lambda k: int(re.match(r'\d+', k).group())
                          if re.match(r'\d+', k) else 10 ** 9):
            candidate = os.path.join(LIT_ASSETS, w['slug'], figs[key])
            if os.path.isfile(candidate):
                src = candidate
                break
        if src is None:
            continue
        count += 1
        dst = os.path.join(THUMBS, f"lit-{w['slug']}.jpg")
        if make(src, dst, expected) == 'made':
            made += 1
    return made, count


def maps(expected):
    """The maps' whole faces, fetched from the tiles' lowest whole-map level.

    The static IIIF of the tiles' site serves the whole map only at the
    scale factors' own sizes: at 1/32 the map is its least whole map, a few
    hundred px wide (lukom1766: 322x267) - wide enough for a card, and it
    is fetched as the tiles are, so no new picture is made of the map."""
    made = 0
    count = 0
    with open(MAPS_YML, encoding='utf-8') as f:
        reg = yaml.safe_load(f)
    for key, m in (reg.get('maps') or {}).items():
        if not m.get('in_project') or not m.get('tiles'):
            continue
        base = m['tiles'].rsplit('/info.json', 1)[0]
        w = -(-m['width'] // 32)
        h = -(-m['height'] // 32)
        url = f'{base}/full/{w},{h}/0/default.jpg'
        r = requests.get(url, timeout=60)
        if r.status_code != 200 or 'jpeg' not in r.headers.get('content-type', ''):
            print(f'map {key}: the tiles served no whole map ({r.status_code}), no thumb')
            continue
        count += 1
        dst = os.path.join(THUMBS, f'map-{key}.jpg')
        expected.add(os.path.basename(dst))
        if not FORCE and os.path.isfile(dst):
            pass
        else:
            with open(dst, 'wb') as fb:
                fb.write(r.content)
            made += 1
    return made, count


def main():
    os.makedirs(THUMBS, exist_ok=True)
    expected = set()
    t0 = time.time()
    parts = [('holdings', holdings), ('newspapers', newspapers),
             ('literature', literature), ('maps', maps)]
    for name, fn in parts:
        made, count = fn(expected)
        print(f'thumbs {name:10s} {made} made, {count - made} already current (of {count})')

    orphans = [f for f in os.listdir(THUMBS)
               if f.lower().endswith('.jpg') and f not in expected]
    if orphans:
        if PRUNE:
            for f in orphans:
                os.remove(os.path.join(THUMBS, f))
            print(f'pruned {len(orphans)} thumb(s) with no item: {orphans[:3]}')
        else:
            print(f'NOTE: {len(orphans)} thumb(s) have no item '
                  f'(run with --prune to remove): {orphans[:3]}')

    print(f'thumbs in {time.time() - t0:.0f}s')


if __name__ == '__main__':
    main()
