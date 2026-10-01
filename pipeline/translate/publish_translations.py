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

import unitlib
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


def english_table(tbl_de, segs):
    """The English of a tabulated document as a table, page by page, or None.

    The translator returns each page as CSV in the shape it was given. That is
    only shown as a table if it kept the shape: the same rows on every page
    and, outside the name column, the same cells. Otherwise the pages are
    published as plain text, which looks wrong but puts no sum against the
    wrong entry.
    """
    try:
        tbl = unitlib.table_of({int(s['page']): [ln for ln in s['en'].splitlines()
                                                 if ln.strip()]
                                for s in segs})
    except (StopIteration, ValueError):
        return None

    def figures(t):
        rows = t['head'][1:] + [r for pg in sorted(t['pages']) for r in t['pages'][pg]] + t['foot']
        return [[c.strip() for k, c in enumerate(r) if k != 1] for r in rows]

    if ({pg: len(r) for pg, r in tbl['pages'].items()}
            != {pg: len(r) for pg, r in tbl_de['pages'].items()}
            or figures(tbl) != figures(tbl_de)):
        return None
    return {pg: unitlib.render_table(tbl, pg) for pg in tbl['pages']}


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
    a.unit = unitlib.resolve_unit(a.unit)
    unitlib.check_translation_tag(a.unit, a.tag, 'publish from')
    # review sheets belong to their unit, not to the project
    globals()['SHEET'] = os.path.join(unitlib.review_dir(a.unit), 'translation_review.csv')

    src = os.path.join(ROOT, 'cache', 'translation-raw' + (f'-{a.tag}' if a.tag else ''))
    if not os.path.isdir(src):
        sys.exit(f'no translations at {src} - run translate.py first')

    # The block list only blocks anything if it describes the translations about
    # to be published. Publish before running check_translations.py and the sheet
    # is a report on a previous generation: the run says "0 skipped", every
    # blocking check is silently void, and three documents went to the site
    # carrying renderings the termbase forbids. The order is step 5 before step 6
    # in docs/NEW_UNIT.md, and it is no longer a thing to remember.
    if not a.force:
        newest = max((os.path.getmtime(os.path.join(src, f))
                      for f in os.listdir(src) if f.endswith('.json')),
                     default=0)
        if not os.path.isfile(SHEET):
            sys.exit(f'no review sheet at {SHEET}\n'
                     f'Run: python pipeline/translate/check_translations.py '
                     f'--unit {a.unit}'
                     + (f' --tag {a.tag}' if a.tag else '')
                     + '\n(or --force to publish with no blocking checks at all)')
        if os.path.getmtime(SHEET) < newest:
            sys.exit('the review sheet is older than the translations it would '
                     'have to block:\n'
                     f'  {SHEET}\n'
                     f'Re-run: python pipeline/translate/check_translations.py '
                     f'--unit {a.unit}'
                     + (f' --tag {a.tag}' if a.tag else ''))

    held, held_letters = (set(), set()) if a.force else blocked_pages()
    if not a.list:
        os.makedirs(DEST, exist_ok=True)

    # Documents the editor laid out as tables get an English table as well.
    tables = {r['pad']: t
              for u in unitlib.load_units() if u.slug == a.unit
              for lid, t in unitlib.load_tables(u).items()
              for r in unitlib.records_by_pad(ROOT).values()
              if r['unit'] == u.slug and str(r['letter_id']) == lid}

    published = kept = skipped = 0
    for fn in unitlib.scope_to_unit(sorted(os.listdir(src)), a.unit):
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
                # names and numbers travel with the text. They were dropped
                # here, so the English reached the site and the dataset as a
                # flat string: nothing could tag a person in the translation,
                # and the forms differ from the German (Wien -> Vienna), so
                # grep could not stand in for it either.
                seg = {'page': p['page'], 'en': en}
                pairs = [n for n in (p.get('names') or []) if isinstance(n, dict)]
                if pairs:
                    seg['names'] = pairs
                if p.get('numbers'):
                    seg['numbers'] = p['numbers']
                segs.append(seg)
        if not segs:
            print(f'  {pad}: nothing publishable ({dropped} page(s) held back)')
            skipped += 1
            continue

        if pad in tables:
            shown = english_table(tables[pad], segs) if not dropped else None
            if shown:
                for seg in segs:
                    seg['html'] = shown[int(seg['page'])]
            else:
                print(f'  !! {pad}: the English did not keep the rows and figures '
                      f'of the table - published as plain text')

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
    # The generation just published, written back rather than left to be
    # remembered: every tool defaults to the untagged cache, so a holding that
    # does not say which generation it was published from will be checked
    # against an abandoned one sooner or later. It already was.
    if not a.list and published:
        unitlib.record_published_tag(a.unit, a.tag)
    if held and not a.force:
        print(f'{len(held)} page(s) held back by a blocking check - see '
              f'translation_review.csv, then re-run after ruling on them')
    # Writing is not enough: a document that stops existing leaves its
    # translation behind, and a stale file here is a page the site will publish
    # for a record the corpus no longer has. Merging 30-32 into one left exactly
    # that, twice, and nothing noticed until someone counted the files.
    if not a.list:
        live = set(unitlib.records_by_pad(ROOT))
        orphans = sorted(f for f in os.listdir(DEST)
                         if f.endswith('.yml') and f[:-4] not in live)
        for f in orphans:
            os.remove(os.path.join(DEST, f))
        if orphans:
            print(f'removed {len(orphans)} translation(s) whose document no longer '
                  f'exists: {", ".join(x[:-4] for x in orphans)}')
        print(f'wrote into {DEST}')


if __name__ == '__main__':
    main()
