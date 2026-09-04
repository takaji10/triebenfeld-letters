# -*- coding: utf-8 -*-
"""Move finished translations into the site, and nowhere else.

    python publish_translations.py             # publish what passes
    python publish_translations.py --force     # publish held-back pages too
    python publish_translations.py --list      # show status, write nothing

Writes site/_data/translations/<pad>.yml, which is the one place the site reads
translations from and the one place build_site_data.py promises never to touch
(build_site_data.py:12-13). Nothing here goes near letters.json, letters.csv,
pages.csv, site/_letters/ or the corpus, so no verification in regenerate.py can
be disturbed by anything this script does.

Two safeguards worth knowing about:

  * A page that failed a blocking check - an unflagged rare-pair occurrence, or
    a segment count that does not match the manuscript - is held back rather
    than published. Those failures mean something is wrong that a reader of the
    English could not possibly detect, which is exactly the case for not showing
    it to them.

  * A letter already marked `reviewed` is never demoted back to `draft`. Re-run
    the model as often as you like; it cannot silently undo work you have signed
    off. Advancing to `reviewed` is done by translation_review.py once every row
    for that letter carries a ruling, not by this script.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, os, re, sys, csv, json, argparse

import yaml
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEST = os.path.join(ROOT, 'site', '_data', 'translations')
SHEET = os.path.join(ROOT, 'review', 'translation_review.csv')

BLOCKING = {'rare-pair', 'structure'}


def blocked_pages():
    """What a blocking check refused: (pad, page) pairs, plus whole letters.

    A `structure` failure - the segment count not matching the manuscript - is
    not a per-page problem. It means the returned pages cannot be trusted to be
    the pages they claim to be, so the whole letter is held rather than
    publishing a subset under page numbers that may not line up.
    """
    pages, letters = set(), set()
    if not os.path.isfile(SHEET):
        return pages, letters
    with open(SHEET, encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f):
            if r['kind'] not in BLOCKING or (r.get('ruling') or '').strip():
                continue
            if r['kind'] == 'structure':
                letters.add(r['pad'])
            else:
                pages.add((r['pad'], str(r['page'])))
    return pages, letters


def existing_status(path):
    if not os.path.isfile(path):
        return None
    try:
        return (yaml.safe_load(open(path, encoding='utf-8')) or {}).get('status')
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--tag', default=None)
    a = ap.parse_args()

    src = os.path.join(ROOT, 'cache', 'translation-raw' + (f'-{a.tag}' if a.tag else ''))
    if not os.path.isdir(src):
        sys.exit(f'no translations at {src} - run translate.py first')

    held, held_letters = (set(), set()) if a.force else blocked_pages()
    if not a.list:
        os.makedirs(DEST, exist_ok=True)

    published = kept = skipped = 0
    for fn in sorted(os.listdir(src)):
        if not fn.endswith('.json') or fn.startswith('_'):
            continue
        d = json.load(open(os.path.join(src, fn), encoding='utf-8'))
        # The cache filename is the pad. The 'pad' recorded inside the file
        # predates unit namespacing and can be stale, so it is not trusted.
        pad = fn[:-5]
        dest = os.path.join(DEST, pad + '.yml')

        if pad in held_letters:
            print(f'  {pad}: held back entirely - segment count does not match the '
                  f'manuscript')
            skipped += 1
            continue

        was = existing_status(dest)
        if was == 'reviewed':
            print(f'  {pad}: already reviewed - left alone')
            kept += 1
            continue

        segs, dropped = [], 0
        for p in d.get('pages', []):
            if (pad, str(p.get('page'))) in held:
                dropped += 1
                continue
            en = (p.get('en') or '').strip()
            if en:
                segs.append({'page': p['page'], 'en': en})
        if not segs:
            print(f'  {pad}: nothing publishable ({dropped} page(s) held back)')
            skipped += 1
            continue

        if a.list:
            print(f'  {pad}: {len(segs)} page(s) ready'
                  + (f', {dropped} held back' if dropped else ''))
            published += 1
            continue

        with open(dest, 'w', encoding='utf-8', newline='\n') as f:
            yaml.safe_dump({'status': 'draft', 'segments': segs}, f,
                           allow_unicode=True, sort_keys=False, width=100)
        published += 1
        if dropped:
            print(f'  {pad}: published {len(segs)} page(s), {dropped} held back')

    verb = 'ready' if a.list else 'published'
    print(f'\n{published} letter(s) {verb}, {kept} already reviewed, {skipped} skipped')
    if held and not a.force:
        print(f'{len(held)} page(s) held back by a blocking check - see '
              f'translation_review.csv, then re-run after ruling on them')
    if not a.list:
        print(f'wrote into {DEST}')


if __name__ == '__main__':
    main()
