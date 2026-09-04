# -*- coding: utf-8 -*-
"""
Match the scanned page images in pages/ to the transcribed pages.

Each image is one manuscript page. Blank pages (blank versos, unused spread
halves) were deliberately deleted before this ran, so gaps in the filename
sequence are expected and are NOT treated as errors.

Filename grammar:  Oe 1_Bü 9454_NNNN_<crop><half>.jpg
    NNNN     the camera capture
    crop     a = leftmost document in the capture, b = next, ...
    half     1 = left page of an opened spread, 2 = right page (absent if not split)

Outputs
    scan_inventory.md    what is in pages/, and where the transcript looks over-segmented
    page_scan_map.csv    the proposed mapping, one row per transcript page - hand-editable
    scan_review.html     standalone visual reviewer (open it directly, reads pages/ in place)

Nothing here modifies the corpus, the database, or the images.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, csv, json
from collections import defaultdict, Counter
import unitlib
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UNIT = unitlib.one_unit(unitlib.unit_arg())
os.makedirs(os.path.join(ROOT, 'review', UNIT.slug), exist_ok=True)
PAGES_DIR = os.path.join(ROOT, 'pages')
# Filenames were renamed to be ASCII and self-describing:
#   Oe_1_Bu_9454_0343_a1-L179a_04.jpg
#   <signature>_<capture>_<crop><half>-<L{letter}_{page}|front|notext|notapage>
# The trailing part is a convenience label; the capture and crop still carry the
# archival identity, and scan_rename_map.json records the original names.
FN = re.compile(r'^(Oe_1_Bu_9454)_(\d{4})_([a-h])(\d?)(?:-[^.]*)?\.jpg$')

# Letter 303, the liquidation register, was originally assumed to be from a
# separate source. The scans show otherwise: the trailing captures of the
# Büschel are its own pages, so it takes images like any other document.
NOT_IN_BUESCHEL = set()


def letter_key(lid):
    m = re.match(r'(\d+)([a-z]*)', lid)
    return (int(m.group(1)), m.group(2))


# A short block that is only a dateline, a signature or a salutation is almost
# certainly not a new manuscript page - it is the transcriber setting that
# element off with a blank line. These are the main source of over-segmentation.
SIG_RE = re.compile(r'\b(Diener|Knecht|Triebenfeld|ersterbe|gehorsamst\w*|unterth[äa]nig\w*)\b', re.I)
DATE_RE = re.compile(r'\b(1[78]\d\d)\b')
PLACE_RE = re.compile(r'\b(Berlin|Breslau|Wien|Kontop|Glogau|Posen|Kalisz|Peysern|'
                      r'Trąbczyn|Zagorow\w*|Blizanow|Warschau|Öhringen|Neisse|Betsche|'
                      r'Schlawensch\w*|Dresden|Erfurt|Paris|Küstrin)\b', re.I)
SALUT_RE = re.compile(r'(Gnädigster|Durchlauchtigster|Hochfürstliche|Hochwohlgeboren)', re.I)


def page_hint(page):
    """Why this short page probably isn't a real page break - or '' if it looks fine."""
    if page['n_lines'] > 3:
        return ''
    t = ' '.join(page['diplomatic'].split())
    if not t or t in ('(missing)', '(skipped)'):
        return ''
    if SIG_RE.search(t) and len(t) < 90:
        return 'signature block'
    if DATE_RE.search(t) and (PLACE_RE.search(t) or re.search(r'\bd(en)?\.?\s*\d', t)):
        return 'dateline'
    if SALUT_RE.search(t) and len(t) < 70:
        return 'salutation'
    if len(t) < 40:
        return 'very short block'
    return ''


DECISIONS_FILE = os.path.join(UNIT.dir, 'scan_decisions.json')


def load_decisions():
    """
    Durable, hand-checked decisions about the images themselves, exported from
    the reviewer. Keeping them here rather than in browser storage means they
    survive regeneration - and means the reviewer opens on the corrected state
    instead of resetting to naive folder order every time.

      front_matter   belongs to no letter (the series title page)
      dropped        not a manuscript page at all
      image_no_text  a real page with no transcribed text - either the transcript
                     is missing it, or it was deliberately left untranscribed
      image_order    the corrected reading sequence, when it isn't folder order
      notes          per-image reason, so an intentional omission is never later
                     mistaken for a gap to be filled
      pairs          "letter/page" -> image, established by looking at the scans.
                     This is authoritative: it beats anything derived here.
      gaps           "letter/page" entries confirmed to have no scan
    """
    d = {'front_matter': [], 'dropped': [], 'image_no_text': [], 'image_order': [],
         'notes': {}, 'pairs': {}, 'gaps': []}
    if os.path.isfile(DECISIONS_FILE):
        with open(DECISIONS_FILE, encoding='utf-8') as f:
            d.update(json.load(f))
    return d


def load_captures():
    """[(capture_no, [filename, ...]), ...] in physical order."""
    by_num = defaultdict(list)
    unparsed = []
    for f in sorted(os.listdir(PAGES_DIR)):
        if not f.lower().endswith('.jpg'):
            continue
        m = FN.match(f)
        if not m:
            unparsed.append(f)
            continue
        by_num[int(m.group(2))].append((m.group(3), m.group(4) or '', f))
    caps = []
    for n in sorted(by_num):
        items = sorted(by_num[n], key=lambda t: (t[0], t[1]))
        caps.append((n, [t[2] for t in items]))
    return caps, unparsed


def align(letters, caps):
    """
    Assign a contiguous run of captures to each letter, minimising the total
    difference between images received and pages transcribed.

    Captures are atomic: a capture's crops belong to one document, so a capture
    is never split between two letters.
    """
    N, M = len(letters), len(caps)
    csum = [0] * (M + 1)
    for j, (_, imgs) in enumerate(caps):
        csum[j + 1] = csum[j] + len(imgs)

    INF = float('inf')
    dp = [[INF] * (M + 1) for _ in range(N + 1)]
    back = [[0] * (M + 1) for _ in range(N + 1)]
    dp[0][0] = 0

    for i in range(1, N + 1):
        want = letters[i - 1]['n_pages']
        skip = letters[i - 1]['_skip']
        # A letter never needs more captures than it has pages (a capture yields
        # at least one image), so the search window stays small.
        span = 0 if skip else want + 4
        for j in range(M + 1):
            best, bk = INF, j
            lo = j if skip else max(0, j - span)
            for k in range(lo, j + 1):
                if dp[i - 1][k] == INF:
                    continue
                got = csum[j] - csum[k]
                if skip and got:
                    continue
                cost = dp[i - 1][k] + abs(got - (0 if skip else want))
                # nudge away from leaving a real letter with no images at all
                if not skip and got == 0:
                    cost += 2
                if cost < best:
                    best, bk = cost, k
            dp[i][j] = best
            back[i][j] = bk

    j = M
    spans = [None] * N
    for i in range(N, 0, -1):
        k = back[i][j]
        spans[i - 1] = (k, j)
        j = k
    return spans, dp[N][M]


def main():
    with open(os.path.join(ROOT, 'corpus', 'units', UNIT.slug, 'letters.json'), encoding='utf-8') as f:
        recs = json.load(f)
    recs.sort(key=lambda r: letter_key(r['letter_id']))
    for r in recs:
        r['_skip'] = bool(r['is_missing']) or r['letter_id'] in NOT_IN_BUESCHEL

    caps, unparsed = load_captures()
    n_imgs = sum(len(i) for _, i in caps)
    n_pages = sum(r['n_pages'] for r in recs)
    print(f'captures {len(caps)}  images {n_imgs}  transcript pages {n_pages}')
    if unparsed:
        print(f'  WARNING: {len(unparsed)} filenames did not parse: {unparsed[:5]}')

    # Straight sequential pairing: transcript page 1 to image 1, and so on, both
    # in their own natural order. No grouping is guessed at - every image and
    # every page is shown exactly where it falls, and corrections are made by
    # anchoring in the reviewer. (The per-letter fit analysis still appears in
    # scan_inventory.md as diagnostics, but it no longer drives the mapping.)
    spans, cost = align(recs, caps)
    print(f'per-letter fit (diagnostic only): total mismatch {cost}')

    # ---- build the row model -------------------------------------------------
    # A uniform model the reviewer can re-flow trivially: an ordered list of page
    # slots, an ordered list of images, plus the gaps and drops that pair them.
    dec = load_decisions()
    present = {f for _, fl in caps for f in fl}
    folder_order = [f for _, fl in caps for f in fl]

    # Corrected reading order, if one has been recorded; files that have since
    # been deleted drop out, and any new file is appended at its folder position.
    if dec['image_order']:
        kept = [f for f in dec['image_order'] if f in present]
        seen = set(kept)
        for f in folder_order:
            if f not in seen:
                kept.append(f)
                seen.add(f)
        folder_order = kept

    excluded = set(dec['front_matter']) | set(dec['dropped'])
    notext = [f for f in dec['image_no_text'] if f in present]
    all_imgs = [f for f in folder_order if f not in excluded and f not in set(notext)]
    if excluded or notext:
        print(f'  decisions applied: {len(dec["front_matter"])} front matter, '
              f'{len(dec["dropped"])} dropped, {len(notext)} without text, '
              f'{"custom" if dec["image_order"] else "folder"} order')

    per_letter = [(r, [f for _, fl in caps[k:j] for f in fl], caps[k:j])
                  for r, (k, j) in zip(recs, spans)]

    # Every transcript page, in order.
    slots = []
    for r in recs:
        note = ''
        if r['letter_id'] in NOT_IN_BUESCHEL:
            note = 'register - not part of this Büschel'
        elif r['is_missing']:
            note = 'missing/skipped in the archive - no document to scan'
        for pi, p in enumerate(r['pages']):
            slots.append((r, p, pi, note))

    # The pairing established by looking at the scans wins. Anything it doesn't
    # cover (pages added since the review) falls back to sequential fill from
    # whatever images that review left unused, in order.
    #
    # Deliberately NOT inferred here: which pages have no scan. An archival
    # number recorded as missing can still have a physical page behind it -
    # letter 9 does - so assuming otherwise silently shifts every later pairing.
    pairs = {k: v for k, v in dec['pairs'].items() if v in present}
    gaps = set(dec['gaps'])
    spoken_for = set(pairs.values())
    spare = [f for f in all_imgs if f not in spoken_for]

    rows = []
    si = 0
    for (r, p, pi, note) in slots:
        key = f"{r['letter_id']}/{p['page']}"
        if key in pairs:
            img, status = pairs[key], 'reviewed'
        elif key in gaps:
            img, status = '', 'gap'
        else:
            img = spare[si] if si < len(spare) else ''
            status = 'auto' if img else 'gap'
            if img:
                si += 1
        rows.append({
            'letter': r['letter_id'], 'page': p['page'],
            'line_start': p['line_start'], 'line_end': p['line_end'],
            'n_lines': p['n_lines'],
            'image': img,
            'status': status,
            'confidence': 'ok' if status == 'reviewed' else 'check',
            'note': note,
            'hint': page_hint(p) if pi > 0 else '',
            'text': p['diplomatic'],
        })
    # Any images past the end of the transcript still get a row of their own, so
    # nothing in the folder is ever invisible.
    for img in spare[si:]:
        rows.append({
            'letter': '', 'page': '', 'line_start': '', 'line_end': '', 'n_lines': '',
            'image': img, 'status': 'beyond_last_page', 'confidence': 'check',
            'note': 'more images than transcribed pages', 'hint': '', 'text': '',
        })
    # Images set aside by a recorded decision - kept visible, never dropped from
    # the record.
    for img, st, note in (
            [(f, 'front_matter', 'not part of any letter') for f in dec['front_matter']]
            + [(f, 'dropped', 'not a manuscript page') for f in dec['dropped']]
            + [(f, 'image_no_text', 'no transcribed text') for f in notext]):
        if img in present:
            rows.append({
                'letter': '0' if st == 'front_matter' else '', 'page': '',
                'line_start': '', 'line_end': '', 'n_lines': '', 'image': img,
                'status': st, 'confidence': 'n/a',
                'note': dec['notes'].get(img, note), 'hint': '', 'text': '',
            })
    unused = []

    write_map(rows, unused)
    write_inventory(caps, recs, per_letter, unparsed, unused)
    write_reviewer(rows, recs)
    verify(rows, present, folder_order, recs)


def write_map(rows, unused):
    cols = ['letter', 'page', 'line_start', 'line_end', 'n_lines',
            'image', 'status', 'confidence', 'note']
    path = os.path.join(UNIT.dir, 'page_scan_map.csv')
    # Excel holds an exclusive lock on an open file. That shouldn't stop the rest
    # of the run - the reviewer matters more than this table.
    try:
        open(path, 'a').close()
    except PermissionError:
        print(f'  SKIPPED page_scan_map.csv - the file is open in another program '
              f'(close it and re-run to refresh it)')
        return
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow(r)
        for img in unused:
            w.writerow({'letter': '', 'page': '', 'image': img,
                        'status': 'unassigned', 'confidence': 'check',
                        'note': 'image not matched to any transcribed page'})
    print(f'wrote page_scan_map.csv ({len(rows)} page rows, {len(unused)} unassigned images)')


def write_inventory(caps, recs, per_letter, unparsed, unused):
    comp = Counter()
    pruned = defaultdict(list)
    for n, files in caps:
        parts = sorted(FN.match(f).group(3) + (FN.match(f).group(4) or '') for f in files)
        comp[tuple(parts)] += 1
        s = set(parts)
        for crop in {p[0] for p in parts}:
            halves = {p[1:] for p in parts if p[0] == crop}
            if '2' in halves and '1' not in halves:
                pruned['left half of a spread removed'].append(f'{n:04d}_{crop}1')
            if '1' in halves and '2' not in halves:
                pruned['right half of a spread removed'].append(f'{n:04d}_{crop}2')
        if 'b' in s and 'a' not in s and not any(p.startswith('a') for p in parts):
            pruned['first document in the capture removed'].append(f'{n:04d}_a')

    MEANING = {
        ('a1', 'a2'): 'spread split into two pages, both kept',
        ('a', 'b'): 'two documents in the capture, both kept',
        ('a',): 'single document, not a spread',
        ('b',): 'the _a crop was blank and removed',
        ('a1',): 'the right half was blank and removed',
        ('a2',): 'the left half was blank and removed',
        ('a', 'b2'): 'horizontal split; _b1 removed',
        ('a1', 'a2', 'b'): 'spread plus a second document',
    }

    L = []
    A = L.append
    A('# Scan inventory\n')
    A(f'`pages/` holds **{sum(len(i) for _, i in caps)} images** across '
      f'**{len(caps)} captures** (0001–{caps[-1][0]:04d}), against '
      f'**{sum(r["n_pages"] for r in recs)} transcribed pages**.\n')
    A('Each image is one manuscript page. Blank pages were deleted before this ran, '
      'so gaps in the filename sequence are deliberate and are recorded below as '
      'pruning, not as damage.\n')
    if unparsed:
        A(f'\n**{len(unparsed)} filenames did not parse** and were ignored: '
          + ', '.join(f'`{x}`' for x in unparsed[:10]) + '\n')

    A('\n## What each capture yielded\n')
    A('| Composition | Captures | Meaning |\n|---|---|---|')
    for k, v in comp.most_common():
        A(f'| `{"` + `".join(k)}` | {v} | {MEANING.get(k, "")} |')

    A('\n## Pruned counterparts\n')
    A('Expected, not errors — these are the blanks you removed. Listed so the record '
      'exists and nothing here is later mistaken for a missing scan.\n')
    for kind in sorted(pruned):
        names = pruned[kind]
        A(f'\n**{kind}** — {len(names)}\n')
        A('> ' + ', '.join(f'`{n}`' for n in names[:60])
          + (f' … and {len(names) - 60} more' if len(names) > 60 else ''))

    # ---- the strongest evidence: short blocks that aren't pages ----
    hits = []
    for r in recs:
        for p in r['pages'][1:]:
            h = page_hint(p)
            if h:
                hits.append((r['letter_id'], p, h))
    A('\n\n## Short blocks that are almost certainly not page breaks\n')
    A(f'**{len(hits)} of them**, against a shortfall of '
      f'{sum(r["n_pages"] for r in recs) - sum(len(i) for _, i in caps)} pages — so this '
      'very likely accounts for the whole discrepancy.\n')
    A('These are datelines, signatures and salutations that the transcriber set off with '
      'a blank line. Phase 1 read every blank line as a page break, which turned each of '
      'these into its own "page". They are the first thing to check in the reviewer: '
      '**merge into previous page** is almost always the right call, and the real fix is '
      'to remove the blank line from the corpus.\n')
    A('| Letter | Page | Lines | Looks like | Blank line at | Content |\n'
      '|---|---|---|---|---|---|')
    for lid, p, h in hits:
        txt = ' '.join(p['diplomatic'].split())[:64]
        A(f'| {lid} | {p["page"]} | {p["n_lines"]} | {h} | {p["line_start"] - 1} | '
          f'{txt.replace("|", "\\|")} |')

    # ---- over-segmentation suspects ----
    A('\n\n## Where the transcript claims more pages than there are images\n')
    A('The likeliest cause is over-segmentation: our page breaks come from blank lines '
      'in the transcript, and some of those are probably paragraph breaks rather than '
      'page breaks. Each row lists the blank-line positions inside the letter so a '
      'suspect break can be checked against the text directly. **Fixing one means '
      'editing the corpus** (removing a blank line), not the mapping.\n')
    with open(unitlib.one_unit(unitlib.unit_arg()).corpus_path,
              encoding='utf-8') as f:
        corpus = f.read().split('\n')
    sus = []
    for r, imgs, _ in per_letter:
        if r['_skip']:
            continue
        d = r['n_pages'] - len(imgs)
        if d > 0:
            blanks = [str(p['line_start'] - 1) for p in r['pages'][1:]]
            sus.append((d, r['letter_id'], r['n_pages'], len(imgs), blanks))
    sus.sort(key=lambda t: (-t[0], letter_key(t[1])))
    A(f'\n{len(sus)} letters affected, {sum(d for d, *_ in sus)} pages in total.\n')
    A('| Letter | Transcript pages | Images | Excess | Blank lines inside the letter |\n'
      '|---|---|---|---|---|')
    for d, lid, np_, ni, blanks in sus:
        A(f'| {lid} | {np_} | {ni} | +{d} | ' +
          (', '.join(blanks[:12]) + (' …' if len(blanks) > 12 else '') if blanks else '—')
          + ' |')

    if unused:
        A('\n## Images not matched to any page\n')
        A('> ' + ', '.join(f'`{u}`' for u in unused[:60]))

    with open(os.path.join(ROOT, 'review', UNIT.slug, 'scan_inventory.md'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print('wrote scan_inventory.md')


def write_reviewer(rows, recs):
    data = [{
        'l': r['letter'], 'p': r['page'], 'ls': r['line_start'], 'le': r['line_end'],
        'img': r['image'], 'st': r['status'], 'cf': r['confidence'],
        'nt': r['note'], 'hn': r.get('hint', ''), 'tx': r['text'],
    } for r in rows]
    letters = []
    seen = set()
    for r in rows:
        if r['letter'] not in seen:
            seen.add(r['letter'])
            letters.append(r['letter'])

    # Fingerprint of the page structure, so the reviewer can tell when the corpus
    # has moved underneath decisions saved in a previous session.
    import hashlib
    stamp = hashlib.sha1(
        '|'.join(f"{r['letter']}:{r['page']}:{r['line_start']}:{r['line_end']}"
                 for r in rows).encode('utf-8')).hexdigest()[:12]

    html = TEMPLATE.replace('/*DATA*/', json.dumps(data, ensure_ascii=False)) \
                   .replace('/*LETTERS*/', json.dumps(letters, ensure_ascii=False)) \
                   .replace('/*STAMP*/', json.dumps(stamp))                    .replace('/*SEED*/', json.dumps(load_decisions(), ensure_ascii=False))
    path = os.path.join(ROOT, 'review', UNIT.slug, 'scan_review.html')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print(f'wrote scan_review.html ({os.path.getsize(path)/1024/1024:.1f} MB)')


def verify(rows, present, expected_order, recs):
    """
    present        every file in pages/
    expected_order the sequence the mapping is supposed to follow (folder order,
                   or the corrected order if one has been recorded)
    """
    print('\n--- verification ---')
    seen = [r['image'] for r in rows if r['image']]
    dupes = [k for k, v in Counter(seen).items() if v > 1]
    page_rows = [r for r in rows if r['page'] != '']
    paired = [r['image'] for r in rows if r['image'] and r['page'] != '']

    print(f'transcript pages covered : {len(page_rows)} '
          f'(expected {sum(r["n_pages"] for r in recs)})')
    print(f'images paired to a page  : {len(paired)}')
    print(f'images set aside         : {len(seen) - len(paired)} '
          f'(front matter, dropped, no text, past the last page)')
    missing = present - set(seen)
    print(f'every image accounted for: {not missing}'
          + (f'  MISSING: {sorted(missing)[:3]}' if missing else ''))
    print(f'no image used twice      : {not dupes}')

    # The mapping must follow the intended sequence - folder order, or the
    # corrected order if one was recorded. Only the images actually in the
    # sequence are checked: front matter, drops and no-text images are listed
    # after it by design, so their position carries no meaning.
    ASIDE = {'front_matter', 'dropped', 'image_no_text'}
    pos = {f: i for i, f in enumerate(expected_order)}
    order_ok, last = True, -1
    for r in rows:
        if not r['image'] or r['status'] in ASIDE:
            continue
        p = pos.get(r['image'], -1)
        if p < last:
            order_ok = False
            break
        last = p
    print(f'follows intended order   : {order_ok}')
    gaps = sum(1 for r in page_rows if r['status'] == 'gap')
    print(f'pages with no image      : {gaps}')

    assert not dupes, f'image assigned more than once: {dupes[:5]}'
    assert not missing, f'image missing from the mapping: {sorted(missing)[:5]}'
    assert len(page_rows) == sum(r['n_pages'] for r in recs), 'page coverage mismatch'
    assert order_ok, 'mapping does not follow the intended image sequence'


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Scan review &middot; Triebenfeld</title>
<style>
:root{--ink:#1c1a17;--soft:#55504a;--faint:#857e75;--paper:#fbf9f5;--paper2:#f2eee6;
--rule:#ded7ca;--accent:#7a3b2e;--ok:#3f6b42;--warn:#8a4b1a;
--serif:Iowan Old Style,Palatino Linotype,Georgia,serif;
--sans:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:15px}
header{position:sticky;top:0;z-index:5;background:var(--paper2);border-bottom:1px solid var(--rule);
padding:.7rem 1rem;display:flex;flex-wrap:wrap;gap:.6rem 1.2rem;align-items:center}
h1{font-size:1rem;margin:0 1rem 0 0;font-family:var(--serif)}
.stat{font-size:.8rem;color:var(--faint)}
.stat b{color:var(--ink)}
button,select{font:inherit;font-size:.82rem;padding:.3rem .6rem;border:1px solid var(--rule);
border-radius:3px;background:var(--paper);color:var(--ink);cursor:pointer}
button:hover{border-color:var(--accent)}
button.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
label.chk{font-size:.82rem;color:var(--soft);cursor:pointer;display:flex;gap:.3rem;align-items:center}
.row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:1rem;
padding:1rem;border-bottom:1px solid var(--rule);align-items:start}
.row.flag{background:#fff8ee}
.row.done{opacity:.55}
.meta{font-size:.75rem;color:var(--faint);margin-bottom:.4rem;display:flex;flex-wrap:wrap;gap:.5rem}
.pill{border:1px solid var(--rule);border-radius:999px;padding:.05rem .5rem}
.pill.gap{color:var(--warn);border-color:var(--warn)}
.pill.ok{color:var(--ok);border-color:var(--ok)}
.pill.hint{color:#fff;background:var(--accent);border-color:var(--accent)}
.pill.anch{color:#fff;background:#46618a;border-color:#46618a}
.row.hinted{background:#fdf1ec}
.row.anchored{box-shadow:inset 4px 0 0 #46618a}
.imghead{border:1px solid var(--rule);border-bottom:0;background:var(--paper2);
padding:.45rem .55rem;display:flex;flex-wrap:wrap;gap:.4rem .7rem;align-items:center}
.imghead .fname{margin:0;flex:1 1 100%;font-size:.7rem;color:var(--faint);word-break:break-all}
.anchor{display:flex;gap:.35rem;align-items:center;font-size:.78rem;color:var(--soft)}
.anchor input{font:inherit;font-size:.8rem;width:4.5rem;padding:.25rem .4rem;
border:1px solid var(--rule);border-radius:3px;background:var(--paper)}
.anchor input:focus{outline:2px solid #46618a;outline-offset:-1px}
.anchor .hintxt{color:var(--faint);font-size:.72rem}
.moves{display:flex;gap:.3rem;align-items:center;font-size:.72rem;color:var(--faint)}
.moves button{font-size:.72rem;padding:.15rem .4rem}
.reordered .imghead{background:#eef2f7;border-color:#46618a}
.pill.front{color:#fff;background:#5c6b4a;border-color:#5c6b4a}
.pill.new{color:#fff;background:#7a6220;border-color:#7a6220}
.row.newlet{box-shadow:inset 4px 0 0 #7a6220}
#newlet{padding:.8rem 1rem;background:#faf5e6;border-bottom:1px solid var(--rule)}
#newlet h2{margin:0 0 .4rem;font-size:.8rem;text-transform:uppercase;
letter-spacing:.06em;color:var(--soft)}
#newlet p{margin:0 0 .5rem;font-size:.8rem;color:var(--soft);max-width:52rem}
#newlet table{border-collapse:collapse;font-size:.8rem}
#newlet td,#newlet th{border-bottom:1px solid var(--rule);padding:.3rem .6rem;text-align:left}
pre{font-family:var(--serif);font-size:.92rem;line-height:1.55;white-space:pre-wrap;
margin:0;max-height:60vh;overflow:auto}
.imgwrap{position:relative;min-height:120px}
img{width:100%;height:auto;border:1px solid var(--rule);background:#fff;display:block}
.noimg{color:var(--warn);font-size:.85rem;padding:1rem;border:1px dashed var(--warn);text-align:center}
.acts{display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.5rem}
.acts button{font-size:.75rem}
.fname{font-size:.7rem;color:var(--faint);margin-top:.3rem;word-break:break-all}
#empty{padding:3rem 1rem;text-align:center;color:var(--faint)}
#conflict{margin:0;padding:.7rem 1rem;background:#fdecea;color:var(--warn);
border-bottom:1px solid var(--warn);font-size:.85rem}
#filterbar{margin:0;padding:.55rem 1rem;background:#eef2f7;color:#33506f;
border-bottom:1px solid var(--rule);font-size:.83rem}
#filterbar button{margin-left:.5rem}
#orderbar{margin:0;padding:.55rem 1rem;background:#eef2f7;color:#33506f;
border-bottom:1px solid var(--rule);font-size:.83rem}
#orderbar button{margin-left:.5rem}
#front{padding:.8rem 1rem;background:#f0f3ec;border-bottom:1px solid var(--rule)}
#front h2{margin:0 0 .5rem;font-size:.8rem;text-transform:uppercase;
letter-spacing:.06em;color:var(--soft)}
#front .fitems{display:flex;flex-wrap:wrap;gap:.8rem}
#front figure{margin:0;width:150px}
#front img{width:100%;border:1px solid var(--rule)}
#front figcaption{font-size:.68rem;color:var(--faint);word-break:break-all;margin:.2rem 0}
</style></head><body>
<header>
  <h1>Scan review</h1>
  <span class="stat"><b id="s-pages">0</b> pages &middot; <b id="s-img">0</b> matched &middot;
    <b id="s-gap">0</b> gaps &middot; <b id="s-drop">0</b> dropped &middot;
    <b id="s-merge">0</b> merges &middot; <b id="s-anch">0</b> anchors &middot;
    <b id="s-front">0</b> front matter &middot;
    <b id="s-notext">0</b> images w/o text &middot;
    <b id="s-new">0</b> new letters &middot;
    <b id="s-left">0</b> images left over</span>
  <select id="jump"><option value="">Jump to letter…</option></select>
  <label class="chk"><input type="checkbox" id="onlyflag"> only uncertain</label>
  <label class="chk"><input type="checkbox" id="hidedone"> hide confirmed</label>
  <button id="download" class="primary">Download review_export.csv</button>
  <button id="copy">Copy as CSV</button>
  <button id="reset">Reset</button>
</header>
<div id="conflict" hidden></div>
<div id="filterbar" hidden></div>
<div id="orderbar" hidden></div>
<div id="newlet" hidden></div>
<div id="front" hidden></div>
<div id="list"></div>
<div id="empty" hidden>Nothing to show with these filters.</div>
<script>
const DATA = /*DATA*/;
const LETTERS = /*LETTERS*/;
const STAMP = /*STAMP*/;          // fingerprint of the page structure this file was built from
const SEED  = /*SEED*/;           // decisions already recorded in scan_decisions.json
const KEY = 'tf-scan-review';

// State: which page slots are gaps, which images are dropped, which pages merge
// into the previous one, which rows you've confirmed, and any anchors you've set.
// An anchor pins one image to the FIRST page of a letter; everything after it
// re-flows to follow. Keyed by filename so it survives re-alignment.
// `front` holds images that belong to no letter at all - the series title page
// and anything like it. They leave the sequence entirely, so everything after
// shifts up, but they stay recorded rather than being thrown away as blanks.
// `newlet` records letters the scans reveal that the transcript doesn't have -
// e.g. transcript letter 1 turns out to be two documents, 1 and 1a. These are
// proposals, not anchors: the corpus has no pages for them until its text is
// split, which is a separate step.
// `merge` folds a page into the one before it, `mergen` into the one after.
// Both mean the same thing for the mapping - this slot is not a page of its own -
// but they imply different corpus edits: remove the blank line before it, or
// the blank line after it.
// `order` is an explicit image sequence, used when the folder order is not the
// reading order (a capture photographed out of sequence, halves of a spread
// split across two captures, and so on). Null until you move something.
// The four ways an image and a page can fail to line up, kept distinct because
// they mean different things:
//   gap    - a transcribed page with no image (the scan is missing)
//   notext - a real manuscript page with no transcribed text (the TRANSCRIPT is
//            missing a page); the image keeps its place and shifts the rest
//   drop   - not a page at all; leaves the sequence entirely
//   front  - front matter, belongs to no letter; leaves the sequence
let S = {gap:{}, drop:{}, notext:{}, merge:{}, mergen:{}, ok:{}, anchor:{},
         front:{}, newlet:{}, order:null};
// Decisions are stored against the page structure they were made on. If the
// corpus has been edited since, page-keyed decisions (gaps, merges, confirms)
// no longer point at the same pages - and merges in particular will already
// have been applied to the corpus, so replaying them would double-count.
// Anchors and front matter are keyed by filename and stay valid either way.
let STALE = false;
try {
  const saved = JSON.parse(localStorage.getItem(KEY) || '{}');
  if (saved.stamp && saved.stamp !== STAMP) {
    STALE = true;
    S = Object.assign(S, {anchor: saved.anchor || {}, front: saved.front || {},
                          newlet: saved.newlet || {}, drop: saved.drop || {},
                          notext: saved.notext || {}, order: saved.order || null});
  } else {
    S = Object.assign(S, saved);
  }
} catch(e){}

// First visit in this browser: start from the decisions already on disk rather
// than from nothing, so the reviewer reflects work that has been committed.
if (!Object.keys(S.front).length && !Object.keys(S.drop).length
    && !Object.keys(S.notext).length && !S.order){
  (SEED.front_matter  || []).forEach(f => S.front[f]  = 1);
  (SEED.dropped       || []).forEach(f => S.drop[f]   = 1);
  (SEED.image_no_text || []).forEach(f => S.notext[f] = 1);
  if ((SEED.image_order || []).length) S.order = SEED.image_order;
}
const save = () => {
  try { localStorage.setItem(KEY, JSON.stringify(Object.assign({stamp: STAMP}, S))); }
  catch(e){}
};

const pageRows  = DATA.filter(d => d.p !== '');
const baseImgs  = DATA.filter(d => d.img).map(d => d.img);

/* Re-flow: walk the page slots and the image list together, skipping merged
   pages, gapped pages and dropped images. One fix near the top therefore
   shifts everything after it, which is the whole point.

   Anchors override the running position: when we arrive at the first page of a
   letter that has an anchor, the image pointer jumps to the anchored image, and
   everything after follows on in sequence. That is what lets you jump around,
   state a known fact ("this image is letter 47"), and have the rest fall in. */
/* The working image sequence: your explicit order if you've set one, otherwise
   the folder order.

   Images get deleted from pages/ between sessions, so the stored order is
   reconciled rather than discarded: files that no longer exist drop out, and
   files that have appeared are slotted in next to their folder neighbour. Your
   reordering therefore survives edits to the folder instead of silently
   reverting. */
let ORDER_ADJUSTED = 0;

function imageOrder(){
  if (!Array.isArray(S.order) || !S.order.length) return baseImgs;

  const known = new Set(baseImgs);
  const kept = S.order.filter(f => known.has(f));
  const removed = S.order.length - kept.length;

  const inKept = new Set(kept);
  const added = baseImgs.filter(f => !inKept.has(f));
  for (const f of added){
    // insert next to the nearest preceding folder neighbour we still have
    let anchorAt = -1;
    for (let k = baseImgs.indexOf(f) - 1; k >= 0; k--){
      const j = kept.indexOf(baseImgs[k]);
      if (j >= 0) { anchorAt = j; break; }
    }
    kept.splice(anchorAt + 1, 0, f);
    inKept.add(f);
  }

  ORDER_ADJUSTED = removed + added.length;
  if (ORDER_ADJUSTED) S.order = kept;      // keep the reconciled version
  return kept;
}

/* Move an image one place earlier or later in the visible sequence. Positions
   are swapped in the full order, so dropped and front-matter images keep their
   place and nothing is lost. */
function moveImage(file, dir){
  const order = imageOrder().slice();
  const visible = order.filter(f => !S.drop[f] && !S.front[f]);
  const vi = visible.indexOf(file);
  const target = visible[vi + dir];
  if (vi < 0 || target === undefined) return;      // already at the end
  const i = order.indexOf(file), j = order.indexOf(target);
  order[i] = target; order[j] = file;
  S.order = order; save(); render();
}

function reflow(){
  const imgs = imageOrder().filter(f => !S.drop[f] && !S.front[f]);
  const pos  = new Map(imgs.map((f, n) => [f, n]));

  // letter -> anchored image (a letter can only start in one place)
  const anchorFor = {};
  for (const [file, letter] of Object.entries(S.anchor)){
    if (pos.has(file)) anchorFor[letter] = file;
  }

  let i = 0;
  const out = [], used = new Set(), conflicts = [];
  for (const p of pageRows){
    const id = p.l + '/' + p.p;
    if (p.p === 1 && anchorFor[p.l] !== undefined){
      const target = pos.get(anchorFor[p.l]);
      if (target < i) conflicts.push(p.l);   // would need to reuse an image
      i = target;
    }
    // Images marked as having no transcribed text stand alone, consuming no
    // page slot, so everything after them shifts to stay aligned.
    while (i < imgs.length && S.notext[imgs[i]]){
      used.add(imgs[i]);
      out.push({p:null, img:imgs[i], notext:true});
      i++;
    }
    if (S.merge[id])  { out.push({p, img:'', merged:'prev'}); continue; }
    if (S.mergen[id]) { out.push({p, img:'', merged:'next'}); continue; }
    if (S.gap[id])    { out.push({p, img:'', gap:true}); continue; }
    const f = imgs[i++] || '';
    if (f) used.add(f);
    out.push({p, img:f, anchored: p.p === 1 && anchorFor[p.l] === f});
  }
  // Images past the last transcript page still get a row, so nothing in the
  // folder is ever silently omitted from the review.
  for (const f of imgs.slice(i)){
    used.add(f);
    out.push({p:null, img:f, tail:true, notext: !!S.notext[f]});
  }
  return {out, leftover: imgs.filter(f => !used.has(f)), conflicts};
}

function render(){
  const {out, leftover, conflicts} = reflow();
  const onlyflag = document.getElementById('onlyflag').checked;
  const hidedone = document.getElementById('hidedone').checked;
  const list = document.getElementById('list');
  let html = '', shown = 0;

  for (const r of out){
    if (r.notext || r.tail){           // an image standing on its own
      shown++;
      const why = r.notext
        ? '<span class="pill gap">marked: no text for this image</span>'
        : '<span class="pill gap">image past the last transcribed page</span>';
      const note = (SEED.notes || {})[r.img];
      const body = r.notext
        ? (note ? esc(note) + ' &mdash; recorded, nothing outstanding.'
                : 'Marked as having no transcribed text, so it takes no page slot and '
                  + 'everything after it has shifted. The transcript is missing this page.')
        : 'There is no transcribed page left for this image &mdash; either the transcript '
          + 'is missing a page, or this image is not a letter page.';
      html += '<div class="row flag"><div><div class="meta">'
        + '<b>No transcript page</b> ' + why + '</div><pre>' + body + '</pre>'
        + '<div class="acts">'
        + '<button data-kind="notext" data-arg="'+esc(r.img)+'">'
        + (r.notext ? 'Undo &mdash; this image does have text' : 'No text for this image')
        + '</button>'
        + '<button data-kind="drop" data-arg="'+esc(r.img)+'">Not a page &mdash; drop it</button>'
        + '</div></div>'
        + '<div class="imgwrap">' + imgHead(r.img, '')
        + '<img loading="lazy" src="pages/'+encodeURIComponent(r.img)+'"></div></div>';
      continue;
    }
    const p = r.p, id = p.l + '/' + p.p;
    const done = !!S.ok[id];
    const flag = !r.img || r.merged || r.gap || p.cf === 'check' || p.hn;
    if (onlyflag && !flag) continue;
    if (hidedone && done) continue;
    shown++;
    const cls = 'row' + (p.hn ? ' hinted' : flag ? ' flag' : '')
              + (done ? ' done' : '') + (r.anchored ? ' anchored' : '')
              + (r.img && S.newlet[r.img] ? ' newlet' : '');
    const pill = r.merged ? '<span class="pill gap">merged into '
                            + (r.merged === 'next' ? 'next' : 'previous') + ' page</span>'
              : r.gap     ? '<span class="pill gap">no image</span>'
              : !r.img    ? '<span class="pill gap">no image left</span>'
              : done      ? '<span class="pill ok">confirmed</span>' : '';
    const apill = r.anchored ? '<span class="pill anch">anchored</span>' : '';
    html += '<div class="'+cls+'" id="r-'+id.replace('/','-')+'">'
      + '<div><div class="meta"><b>Letter '+p.l+'</b> &middot; page '+p.p
      + ' <span class="pill">lines '+p.ls+'&ndash;'+p.le+'</span> '+pill+apill
      + (p.nt ? ' <span class="pill">'+p.nt+'</span>' : '')
      + (p.hn ? ' <span class="pill hint">likely a '+esc(p.hn)
                +', not a page &mdash; merge?</span>' : '')
      + '</div><pre>'+esc(p.tx)+'</pre>'
      + '<div class="acts">'
      + btn(id,'ok', done?'Unconfirm':'Confirm')
      + btn(id,'gap', S.gap[id]?'Un-gap':'No image for this page')
      + btn(id,'merge', S.merge[id]?'Un-merge':'Merge into previous page')
      + btn(id,'mergen', S.mergen[id]?'Un-merge':'Merge into next page')
      + (r.img ? '<button data-kind="notext" data-arg="'+esc(r.img)+'">'
                 + 'No text for this image</button>' : '')
      + (r.img ? btn(id,'drop','Not a page — drop this image', r.img) : '')
      + '</div></div>'
      + '<div class="imgwrap">'
      + (r.img ? imgHead(r.img, p.l)
                 + '<img loading="lazy" src="pages/'+encodeURIComponent(r.img)+'">'
               : '<div class="noimg">'
                 + (r.merged ? 'merged into the ' + (r.merged === 'next' ? 'next' : 'previous')
                               + ' page &mdash; remove the blank line '
                               + (r.merged === 'next' ? 'after line ' + p.le
                                                      : 'before line ' + p.ls)
                   : r.gap ? 'marked as having no image' : 'no image available')
                 + '</div>')
      + '</div></div>';
  }
  // Rebuilding the list would otherwise throw you back to the top on every
  // click, which is unusable when working down 900 rows.
  const y = window.scrollY;
  list.innerHTML = html;

  // Where each image currently sits, so a proposal can say what it displaces.
  const reflowIndex = new Map(
    out.filter(r => r.img).map(r => [r.img, {l: r.p.l, p: r.p.p}]));

  // Proposed new letters: collected in one place, since each one is a corpus
  // edit (split the text, then the pages and dates re-derive themselves).
  const nl = baseImgs.filter(f => S.newlet[f]);
  const ne = document.getElementById('newlet');
  ne.hidden = nl.length === 0;
  if(nl.length){
    const rowFor = f => (reflowIndex.get(f) || {});
    ne.innerHTML = '<h2>Proposed new letters ('+nl.length+')</h2>'
      + '<p>The scans show a document the transcript does not have as its own letter. '
      + 'These cannot be anchored yet &mdash; the corpus has no pages for them until the '
      + 'text is split. Export this list and the split can be applied to the corpus, after '
      + 'which the dates and page structure re-derive automatically.</p>'
      + '<table><tr><th>New letter</th><th>Starts at image</th>'
      + '<th>Currently sits in</th><th></th></tr>'
      + nl.map(f => {
          const r = rowFor(f);
          return '<tr><td><b>'+esc(S.newlet[f])+'</b></td><td>'+esc(f)+'</td>'
            + '<td>'+(r.l ? 'letter '+esc(r.l)+', page '+esc(r.p) : '&mdash;')+'</td>'
            + '<td><button data-kind="unanchor" data-arg="'+esc(f)+'">Clear</button></td></tr>';
        }).join('') + '</table>';
  }

  // Front matter leaves the sequence, so it needs somewhere to live or it would
  // simply vanish and could never be undone.
  const fm = baseImgs.filter(f => S.front[f]);
  const fe = document.getElementById('front');
  fe.hidden = fm.length === 0;
  if(fm.length){
    fe.innerHTML = '<h2>Front matter &mdash; not part of any letter ('+fm.length+')</h2>'
      + '<div class="fitems">' + fm.map(f =>
          '<figure><img loading="lazy" src="pages/'+encodeURIComponent(f)+'">'
          + '<figcaption>'+esc(f)+'</figcaption>'
          + '<button data-kind="unanchor" data-arg="'+esc(f)+'">Put back</button></figure>'
        ).join('') + '</div>';
  }

  window.scrollTo(0, y);
  document.getElementById('empty').hidden = shown > 0;

  // A filter silently hiding rows makes the image sequence look like it skips.
  // Say so loudly whenever anything is hidden.
  const total = out.length;
  const fb = document.getElementById('filterbar');
  if (shown < total){
    fb.hidden = false;
    fb.innerHTML = 'Showing <b>'+shown+'</b> of <b>'+total+'</b> rows — '
      + (total - shown) + ' hidden by a filter, so the image sequence will look '
      + 'like it skips. <button id="showall">Show everything</button>';
    document.getElementById('showall').addEventListener('click', () => {
      document.getElementById('onlyflag').checked = false;
      document.getElementById('hidedone').checked = false;
      render();
    });
  } else fb.hidden = true;

  // A custom image order silently changes what pairs with what - say so, and
  // make it undoable without wiping the rest of the review.
  const ob = document.getElementById('orderbar');
  const cur = imageOrder();
  const moved = cur === baseImgs ? 0 : cur.reduce((n,f,k) => n + (f !== baseImgs[k] ? 1 : 0), 0);
  if (moved){
    ob.hidden = false;
    ob.innerHTML = 'Custom image order in use &mdash; <b>' + moved
      + '</b> image(s) no longer in folder order. '
      + (ORDER_ADJUSTED
          ? '<b>' + ORDER_ADJUSTED + '</b> file(s) were added to or removed from '
            + '<code>pages/</code> since you set it; your order was kept and adjusted '
            + 'around them. '
          : '')
      + '<button id="resetorder">Restore folder order</button>';
    document.getElementById('resetorder').addEventListener('click', () => {
      S.order = null; save(); render();
    });
  } else ob.hidden = true;
  document.getElementById('s-pages').textContent = pageRows.length;
  document.getElementById('s-img').textContent   = out.filter(r=>r.img).length;
  document.getElementById('s-gap').textContent   = Object.keys(S.gap).length;
  document.getElementById('s-drop').textContent  = Object.keys(S.drop).length;
  document.getElementById('s-merge').textContent =
    Object.keys(S.merge).length + Object.keys(S.mergen).length;
  document.getElementById('s-anch').textContent  = Object.keys(S.anchor).length;
  document.getElementById('s-front').textContent = Object.keys(S.front).length;
  document.getElementById('s-notext').textContent = Object.keys(S.notext).length;
  document.getElementById('s-new').textContent   = Object.keys(S.newlet).length;
  document.getElementById('s-left').textContent  = leftover.length;
  const warn = document.getElementById('conflict');
  if(conflicts.length){
    warn.hidden = false;
    warn.textContent = 'Anchors out of order at letter ' + conflicts.join(', ')
      + ' — an earlier anchor already used images past this point, so the sequence '
      + 'runs backwards here. Check those anchors.';
  } else warn.hidden = true;
  window.__leftover = leftover;
}

function imgHead(file, placeholder){
  return '<div class="imghead">'
    + '<div class="fname">'+esc(file)+'</div>'
    + '<div class="moves">Order:'
    + '<button data-kind="moveup" data-arg="'+esc(file)+'" title="one place earlier">'
    + '&uarr; earlier</button>'
    + '<button data-kind="movedown" data-arg="'+esc(file)+'" title="one place later">'
    + '&darr; later</button></div>'
    + '<div class="anchor"><label>This image is letter'
    + ' <input type="text" inputmode="numeric" data-anchor="'+esc(file)+'"'
    + ' value="'+esc(S.anchor[file] || S.newlet[file] || '')
    + '" placeholder="'+esc(placeholder)+'"></label>'
    + '<button data-kind="setanchor" data-arg="'+esc(file)+'">Submit</button>'
    + (S.anchor[file] || S.newlet[file]
        ? '<button data-kind="unanchor" data-arg="'+esc(file)+'">Clear</button>' : '')
    + (S.newlet[file]
        ? '<span class="pill new">new letter '+esc(S.newlet[file])
          + ' &mdash; needs the corpus split first</span>'
        : '<span class="hintxt">pins to page&nbsp;1; the rest re-flow'
          + ' &middot; <b>0</b> = front matter'
          + ' &middot; a new ID (<b>1a</b>) proposes a split</span>')
    + '</div></div>';
}

function btn(id,kind,label,arg){
  return '<button data-id="'+id+'" data-kind="'+kind+'"'
       + (arg?' data-arg="'+esc(arg)+'"':'') + '>'+label+'</button>';
}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;')
  .replace(/>/g,'&gt;').replace(/"/g,'&quot;');}

// '0' is reserved: it means "this image is not part of any letter" (the series
// title page and similar front matter).
const VALID = new Set(pageRows.map(p => p.l));
const FRONT_MATTER = '0';
const ID_RE = /^\d+[a-z]{0,2}$/;   // 1, 1a, 302b - the project's archival form

document.addEventListener('click', e => {
  const b = e.target.closest('button[data-kind]');
  if(!b) return;
  const id = b.dataset.id, kind = b.dataset.kind;
  if(kind==='setanchor'){
    const inp = document.querySelector('input[data-anchor="'+CSS.escape(b.dataset.arg)+'"]');
    if(inp) commitAnchor(inp);
    return;
  }
  if(kind==='notext'){ const f=b.dataset.arg; S.notext[f] ? delete S.notext[f] : S.notext[f]=1;
                       save(); render(); return; }
  if(kind==='moveup'){   moveImage(b.dataset.arg, -1); return; }
  if(kind==='movedown'){ moveImage(b.dataset.arg,  1); return; }
  if(kind==='drop'){ const f=b.dataset.arg; S.drop[f] ? delete S.drop[f] : S.drop[f]=1; }
  else if(kind==='unanchor'){
    delete S.anchor[b.dataset.arg];
    delete S.front[b.dataset.arg];
    delete S.newlet[b.dataset.arg];
  }
  else { S[kind][id] ? delete S[kind][id] : S[kind][id]=1; }
  save(); render();
});

// Typing a letter number against an image anchors it there. Committed on Enter
// or blur, so the list doesn't re-flow under you mid-keystroke.
function commitAnchor(inp){
  const file = inp.dataset.anchor;
  const v = inp.value.trim();
  if(!v){
    if(S.anchor[file] || S.front[file]){
      delete S.anchor[file]; delete S.front[file]; save(); render();
    }
    return;
  }
  if(v === FRONT_MATTER){
    inp.setCustomValidity('');
    if(S.front[file]) return;
    delete S.anchor[file]; S.front[file] = 1; save(); render(); return;
  }
  if(!VALID.has(v)){
    // Not a letter we have - but if it's a well-formed archival ID, treat it as
    // a NEW letter the scans have revealed (e.g. letter 1 is really 1 + 1a).
    // It cannot be anchored yet: the corpus has no pages for it until the text
    // is split, so it is recorded as a proposal instead.
    if(ID_RE.test(v)){
      inp.setCustomValidity('');
      if(S.newlet[file] === v) return;
      // A new sub-lettered ID should extend an archival number we actually have
      // (1 -> 1a). If the base number is unknown it is more likely a typo, so
      // ask rather than quietly recording it.
      const base = v.match(/^\d+/)[0];
      if(!VALID.has(base) && !confirm(
          'There is no letter ' + base + ' in the corpus.\n\n'
          + 'Record "' + v + '" as a new letter anyway?')){
        inp.value = S.anchor[file] || S.newlet[file] || '';
        return;
      }
      delete S.anchor[file]; delete S.front[file];
      S.newlet[file] = v; save(); render(); return;
    }
    inp.setCustomValidity('"' + v + '" is not a letter ID. Use a number, '
      + 'optionally with a letter (1a), or 0 for front matter.');
    inp.reportValidity();
    return;
  }
  inp.setCustomValidity('');
  if(S.anchor[file] === v && !S.front[file] && !S.newlet[file]) return;
  delete S.front[file]; delete S.newlet[file];
  S.anchor[file] = v; save(); render();
}
document.addEventListener('keydown', e => {
  if(e.key === 'Enter' && e.target.dataset && e.target.dataset.anchor){
    e.preventDefault(); commitAnchor(e.target); e.target.blur();
  }
});
document.addEventListener('blur', e => {
  if(e.target.dataset && e.target.dataset.anchor) commitAnchor(e.target);
}, true);
['onlyflag','hidedone'].forEach(k =>
  document.getElementById(k).addEventListener('change', render));

document.getElementById('jump').addEventListener('change', e => {
  const el = document.querySelector('[id^="r-'+e.target.value+'-"]');
  if(el) el.scrollIntoView({behavior:'smooth', block:'start'});
});

document.getElementById('reset').addEventListener('click', () => {
  if(!confirm('Discard all review decisions, including anchors and front matter?')) return;
  S = {gap:{},drop:{},notext:{},merge:{},mergen:{},ok:{},anchor:{},front:{},newlet:{},order:null};
  save(); render();
});

/* Build the export. Beyond the mapping it carries the image-level decisions -
   custom order, no-text, front matter, drops - because those live only in this
   browser until they are written to disk. */
function buildCsv(){
  const {out, leftover} = reflow();
  const rows = [['letter','page','line_start','line_end','image','status','anchored',
                 'new_letter','note']];
  for(const r of out){
    if(!r.p){                                    // image with no transcript page
      rows.push(['','','','',r.img,
                 r.notext ? 'image_no_text' : 'beyond_last_page','','',
                 r.notext ? 'transcript is missing this page' : '']);
      continue;
    }
    const p=r.p, id=p.l+'/'+p.p;
    const st = r.merged ? (r.merged === 'next' ? 'merge_into_next' : 'merge_into_previous')
             : r.gap    ? 'gap'
             : !r.img   ? 'gap'
             : S.ok[id] ? 'confirmed' : 'auto';
    const nlv = r.img ? (S.newlet[r.img] || '') : '';
    rows.push([p.l,p.p,p.ls,p.le,r.img,
               nlv ? 'starts_new_letter' : st,
               r.anchored?'yes':'', nlv, p.nt||'']);
  }
  for(const f of baseImgs.filter(f => S.front[f]))
    rows.push(['0','','','',f,'front_matter','','','not part of any letter']);
  for(const f of baseImgs.filter(f => S.drop[f]))
    rows.push(['','','','',f,'dropped','','','marked as not a page']);
  for(const f of leftover) rows.push(['','','','',f,'unassigned','','','']);

  // The working image sequence, so a custom order is not stranded in this
  // browser. Recorded as its own rows, in order, after the mapping.
  const order = imageOrder();
  if (order !== baseImgs){
    order.forEach((f, n) => rows.push(['','','','',f,'image_order',String(n+1),'',
                                       'position in the corrected image sequence']));
  }
  return rows.map(r => r.map(c => {
    c = String(c==null?'':c);
    return /[",\n]/.test(c) ? '"'+c.replace(/"/g,'""')+'"' : c;
  }).join(',')).join('\n');
}

document.getElementById('download').addEventListener('click', () => {
  const csv = buildCsv();
  const blob = new Blob(['﻿'+csv], {type:'text/csv;charset=utf-8'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'review_export.csv';
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
});

document.getElementById('copy').addEventListener('click', () => {
  const csv = buildCsv();
  navigator.clipboard.writeText(csv).then(
    () => alert('Copied. Paste it into review_export.csv in the project folder.'),
    () => { const w=window.open(); w.document.write('<pre>'+esc(csv)+'</pre>'); });
});

LETTERS.forEach(l => {
  const o=document.createElement('option'); o.value=l; o.textContent='Letter '+l;
  document.getElementById('jump').appendChild(o);
});

if (STALE) {
  const b = document.getElementById('conflict');
  b.hidden = false;
  b.textContent = 'The corpus has been edited since your last session, so the pages have '
    + 'changed. Your page-level decisions (gaps, merges, confirmations) were dropped — '
    + 'merges you had marked are already applied in the corpus, so replaying them would '
    + 'double-count. Anchors, front matter and dropped images were kept.';
  save();
}
render();
</script></body></html>
"""


if __name__ == '__main__':
    main()
