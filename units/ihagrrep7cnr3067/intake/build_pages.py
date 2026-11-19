# -*- coding: utf-8 -*-
"""How the scans and the editor's transcriptions of I. HA GR, Rep. 7 C, Nr. 3067
became this unit's page images and page files.

    python units/ihagrrep7cnr3067/intake/build_pages.py            # check only
    python units/ihagrrep7cnr3067/intake/build_pages.py --crop     # cut the page images
    python units/ihagrrep7cnr3067/intake/build_pages.py --write    # write the page files

A record as much as a tool: it is the one place that says which part of which
scan is a page, which source line went where, and which readings were
corrected against the scans. Follows units/ihagrrep7cnr1414/intake/build_pages.py.

The scans. The editor gave four (2026-11-19), 0005 to 0008. 0005 and 0007 are
single pages the editor had already cut to the leaf and are copied whole
(`_a`). 0006 and 0008 are openings, cut at the fold (`_a1` the left side,
`_a2` the right) with the scale bar left off; CROPS gives each box in pixels
(left, top, right, bottom), the fold placed on the binding thread.

The text. The editor's four files in <raw_dir>, one per scan, line by line.
SPEC says, for each page, which source lines it takes. On 0006 the left side
ends with the catchword "die", repeated at the head of the right side; the
king's own hand begins on the right side below Goldbeck's date and
signature (document 2, first_line 10). On 0008 the second side repeats the
table's column heads.

CORRECTIONS are the readings changed against the scans after two Sonnet
readers and Claude checked every line (notes.md, "The transcription
checked"). The script checks that every source line is used exactly once and
that every correction finds its text exactly once.
"""
import csv
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'pipeline'))
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SLUG = 'ihagrrep7cnr3067'
PREFIX = 'I_HA_Rep_7_C_Nr_3067_'

# scan -> (page id, box or None for the whole scan)
CROPS = [
    ('0005', '0005_a', None),                          # the promemoria, first side
    ('0006', '0006_a1', (0, 0, 2635, 4376)),           # the promemoria continued
    ('0006', '0006_a2', (2635, 0, 5140, 4376)),        # its end, Goldbeck; the king's hand
    ('0007', '0007_a', None),                          # the list's title
    ('0008', '0008_a1', (0, 0, 2620, 4380)),           # the list, A, B and C 1-9
    ('0008', '0008_a2', (2620, 0, 5150, 4380)),        # the list, C 10-26
]

# page id -> (document number or None to continue, first line on the page of
# that document, [(first line, last line), ...] of the source file)
SPEC = [
    ('0005_a', 1, 1, [(1, 44)]),
    ('0006_a1', None, None, [(1, 41)]),
    ('0006_a2', 2, 10, [(42, 62)]),
    ('0007_a', 3, 1, [(1, 5)]),
    ('0008_a1', None, None, [(1, 84)]),
    ('0008_a2', None, None, [(85, 194)]),
]

# (page id, old, new, reason). Filled from the check against the scans.
CORRECTIONS = [
    # The promemoria (document 1)
    ('0005_a', 'nach der Strenge der Gesetze\n', 'nach der Strenge der Gesetze,\n',
     'the comma at the line end (readers 2 and Claude)'),
    ('0005_a', 'Verfügungen aus\n', 'Verfügungen aus¬\n',
     'the line-end hyphen of "ausnehmend" (reader 2 and Claude)'),
    ('0005_a', 'Mnewski', 'Mniewski', 'the page has M-n-i-e-w-s-k-i (reader 2 and Claude)'),
    ('0005_a', 'Straf E[w?][r?][m?]¬', 'Straf Exem¬',
     '"Exem-" / "pel": the letters read by readers 1 and 2 and Claude; "ein Strafexempel statuiren" is the fixed formula'),
    ('0005_a', '49 zufürtzerer', '49 zu kürtzerer',
     'a k and a space (readers 1 and 2 and Claude); "fürtzerer" is no word, and the lines below have "zu langwieriger", "zu lebenswieriger"'),
    ('0006_a1', 'größtintheils', 'größtentheils',
     'the same word in the same hand six lines below (reader 2 and Claude)'),
    ('0006_a1', 'schon aus\n', 'schon aus¬\n',
     'the line-end hyphen of "ausgestanden" (reader 2 and Claude)'),
    ('0006_a1', 'Arrest-Zeitgantz', 'Arrest-Zeit gantz',
     'two words, "Arrest-Zeit" and the adverb "gantz"; the sentence reads only so'),
    ('0006_a1', 'ge¬\ngeldet haben', 'ge¬\nmeldet haben',
     '"ge- / meldet": all three readings'),
    ('0006_a2', 'Vorschläge zu entriren.\n', 'Vorschläge zu entriren\n',
     'no full stop on the page (readers 1 and 2)'),
    ('0006_a2', 'Grafen von Höym', 'Grafen von Hoym',
     'no umlaut on the page (readers 1 and 2), the minister\'s settled form'),
    # The King's decision (document 2)
    ('0006_a2', 'Nach genauer Betrachtung', 'Nach genauer Untersuchung[?]',
     'no B: the word opens with a looped capital and runs "-nter-s-uchung" (reader 1 and Claude; reader 2 "Erwegung"); kept doubtful'),
    ('0006_a2', 'finde binnen der', 'finde keinen der',
     'the looped k of the hand; "finde keinen der Condemnirten einer Minderung der Strafe würdig" is the one reading of the sentence (Claude; reader 2 also no "binnen")'),
    ('0006_a2', 'der straffe strafen\n', 'der strafen\n',
     'two words on the line are struck through (readers 1 and 2); struck-out text is not transcribed (EDITORIAL_RULES, 2026-10-05)'),
    ('0006_a2', 'zu erkennen[?]', 'zu erlegung[?]',
     'the g with its descender; "zu erlegung derselben angehalten" is the one reading (Claude); kept doubtful'),
    ('0006_a2', 'mäßigen am[e?]st', 'mäßigen arest',
     'a-r-e-s-t (readers 1 and 2 and Claude): "zu dem Verhältniß mäßigen Arest gebracht"'),
    # The list (document 3)
    ('0008_a1', 'Weiler sich als', 'Weil er sich als',
     'two words, as "Weil er" in every other entry (readers 3 and 4, Claude)'),
    ('0008_a1', 'Beförderung des\n', 'Beförderung der\n',
     '"der Insurrektion" (readers 3 and 4, Claude)'),
    ('0008_a1', 'Weiler bey der Flucht', 'Weil er bey der Flucht', 'two words, as above'),
    ('0008_a2', 'Weiler dem Ueberfall', 'Weil er dem Ueberfall', 'two words, as above'),
    ('0008_a2', 'Dziewanowski\nAusgleicher Ursach', 'Dziewanowski\nAus gleicher Ursach',
     'three words with clear gaps (readers 3 and 4, Claude)'),
    ('0008_a2', 'Maruczewski\nAusgleicher Ursach', 'Maruczewski\nAus gleicher Ursach', 'as above'),
    ('0008_a2', 'verdächtig ist.\n4 Jahre\nDecember 1795', 'verdächtig ist.\n4 Jahre\nDezember 1795',
     'with z, as the entries below it (reader 4 and Claude)'),
    ('0008_a2', 'Insurrektion\n4 Jahre\nNovember 1796', 'Insurrektion\n4 Jahr\nNovember 1796',
     '"4 Jahr", no e (reader 3 and Claude)'),
]


def source(raw_dir):
    out = {}
    for f in sorted(os.listdir(raw_dir)):
        if not f.endswith('.txt'):
            continue
        scan = os.path.splitext(f)[0].rsplit('_', 1)[1]
        out[scan] = io.open(os.path.join(raw_dir, f), encoding='utf-8-sig').read() \
            .replace('\r\n', '\n').rstrip('\n').split('\n')
    return out


def crop(unit):
    from PIL import Image
    pdir = os.path.join(unit.raw_dir, 'processed')
    os.makedirs(pdir, exist_ok=True)
    manifest = {}
    for scan, pid, box in CROPS:
        src = PREFIX + scan + '.jpg'
        im = Image.open(os.path.join(unit.raw_dir, src)).convert('RGB')
        box = box or (0, 0) + im.size
        out = PREFIX + pid + '.jpg'
        im.crop(box).save(os.path.join(pdir, out), quality=95)
        manifest.setdefault(src, []).append({'file': out, 'bbox_original': list(box),
                                             'size': [box[2] - box[0], box[3] - box[1]],
                                             'fold_confidence': 'manual'})
        print(f'  {src} -> processed/{out}  {box}')
    with open(os.path.join(pdir, 'manifest.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)


def main():
    unit = unitlib.one_unit(SLUG)
    if '--crop' in sys.argv:
        crop(unit)
        return
    src = source(unit.raw_dir)
    pages, bounds, problems = [], [], []
    used_by_scan = {}
    for pid, doc, first, ranges in SPEC:
        scan = pid.split('_')[0]
        lines = []
        for a, b in ranges:
            lines.extend(src[scan][a - 1:b])
            used_by_scan.setdefault(scan, []).extend(range(a, b + 1))
        if any(not l.strip() for l in lines):
            problems.append(f'{pid}: a blank line')
        pages.append([pid, lines])
        if doc:
            bounds.append((doc, pid, first))
    for scan, used in used_by_scan.items():
        if sorted(used) != list(range(1, len(src[scan]) + 1)):
            problems.append(f'{scan}: the source has {len(src[scan])} lines, SPEC uses {len(used)}')
    if sorted(src) != sorted(used_by_scan):
        problems.append('the source files and SPEC do not name the same scans')
    by_pid = {p[0]: p for p in pages}
    for pid, old, new, why in CORRECTIONS:
        text = '\n'.join(by_pid[pid][1])
        n = text.count(old)
        if n != 1:
            problems.append(f'{pid}: {old!r} found {n} times')
            continue
        by_pid[pid][1] = text.replace(old, new).split('\n')
    if problems:
        sys.exit('NOT WRITTEN\n' + '\n'.join(problems))
    print(f'{len(src)} source files -> {len(pages)} pages, {len(bounds)} documents, '
          f'{len(CORRECTIONS)} corrections; every source line placed exactly once')
    for pid, lines in pages:
        print(f'  {pid:<8} {len(lines):>3} lines  {lines[0][:36]!r} ... {lines[-1][-30:]!r}')
    if '--write' not in sys.argv:
        return
    tdir = os.path.join(UNIT_DIR, 'transcriptions')
    os.makedirs(tdir, exist_ok=True)
    for pid, lines in pages:
        with open(os.path.join(tdir, PREFIX + pid + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines) + '\n')
    rdir = unitlib.review_dir(unit.slug)
    os.makedirs(rdir, exist_ok=True)
    for d in (rdir, HERE):
        with open(os.path.join(d, 'document_boundaries.csv'), 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(['letter_id', 'first_page', 'first_line'])
            w.writerows(bounds)
    print('wrote transcriptions/ and document_boundaries.csv')


if __name__ == '__main__':
    main()
