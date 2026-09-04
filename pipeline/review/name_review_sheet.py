# -*- coding: utf-8 -*-
"""Build the three-column review sheet for unidentified names, and read it back.

    python name_review_sheet.py            # write name_review.csv (blank col 3)
    python name_review_sheet.py --read     # summarise what has been filled in
    python name_review_sheet.py --read --apply    # apply the filled-in rows

Column 3 (`correct_form`) is yours. Leave it blank to skip a row. Write the
corrected spelling to change it, or `OK` to confirm the current reading is right
so it is never raised again.

Rows are in alphabetical order (umlauts folded, so Ö sorts with O).

Rewriting the sheet preserves anything already filled in, so it can be
regenerated after new names appear without losing your work.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, csv, json, unicodedata, shutil
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from name_catalogue import NOT_NAMES, stem
import unitlib
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHEET = os.path.join(ROOT, 'review', 'name_review.csv')
CORPUS = unitlib.one_unit(unitlib.unit_arg()).corpus_path

OBVIOUS = set('''Berlin Breslau Wien Paris Warschau Dresden Königsberg Posen
Prag Petersburg London Frankfurt Leipzig München Hamburg Erfurt Magdeburg
Potsdam Memel Glogau Brieg Neisse Küstrin Kalisz Preußen Südpreußen Schlesien
Pommern Sachsen Rußland Frankreich Österreich Pohlen Polen Italien Böhmen
Hessen Bayern Hannover Westphalen Holland Curland Schweiz'''.split())

NAME_SLOT = re.compile(
    r'(?:\bv\.?\s+|\bvon\s+|\bHerrn?\s+|\bH\.\s*|\bHl\.\s*|\bdH\.?\s*|\bdHl\.?\s*'
    r'|\bGraf(?:en)?\s+|\bGräfin\s+|\bBaron\s+|\bFrau\s+|\bMinister\s+'
    r'|\bGeneral\s+|\bGen\.?\s+|\bObrist(?:en)?\s+|\bRath\s+|\bDoctor\s+'
    r'|\bPr[äa]fect\s+|\bJustiz\s+|\bAmtmann\s+|\bPastor\s+|\bMajor\s+)'
    r'([A-ZÄÖÜ][^\W\d_]{3,})', re.UNICODE)


def fold(s):
    s = unicodedata.normalize('NFKD', s.lower().replace('ſ', 's').replace('ß', 'ss'))
    return ''.join(c for c in s if not unicodedata.combining(c))


def known_names():
    """Every name already settled, from all four places a decision can live.

    Filtering on whos_who.md alone was not enough: most rulings never produce a
    who's-who entry, so the sheet was still asking about Amelang, Brzechsta,
    Hardenberg, Trąbczyn, Kontop and the rest of the agreed canon.
    """
    out = set()

    # 1. who's-who: bolded names in the tables
    p = os.path.join(ROOT, 'reference', 'whos_who.md')
    if os.path.isfile(p):
        for m in re.finditer(r'\*\*([^*]+)\*\*', open(p, encoding='utf-8').read()):
            for part in re.split(r'\s*/\s*|\s*,\s*', m.group(1)):
                for tok in re.findall(r'[^\W\d_]{4,}', re.sub(r'\([^)]*\)', '', part)):
                    if tok[:1].isupper():
                        out.add(fold(tok))

    # 2. every ruling given so far
    p = os.path.join(ROOT, 'reference', 'name_rulings.json')
    if os.path.isfile(p):
        r = json.load(open(p, encoding='utf-8'))
        for pair in r.get('settled_pairs', []) + r.get('locked_apart', []):
            for nm in pair:
                out.add(fold(nm))          # both sides: canonical AND absorbed
        for key in ('places_identified', 'context_sensitive', 'reclassify'):
            for nm in r.get(key, {}):
                for tok in re.findall(r'[^\W\d_]{3,}', nm):
                    out.add(fold(tok))
        for nm in r.get('keep_derivations', []) + r.get('applied', []) \
                + r.get('rejected', []) + r.get('drop_seeds', []) \
                + r.get('tracked_elsewhere', []):
            out.add(fold(nm))

    # 3. the project canon hard-coded in name_catalogue.py
    p = os.path.join(ROOT, 'pipeline/review', 'name_catalogue.py')
    if os.path.isfile(p):
        m = re.search(r'EXTRA_SEEDS = """(.*?)"""', open(p, encoding='utf-8').read(), re.S)
        if m:
            out.update(fold(t) for t in m.group(1).split())

    # 4. every place the edition has already derived from a dateline, plus the
    #    estate list name_catalogue uses. These are settled geography, not
    #    questions - Kontop, Blizanow, Betsche and the rest were still being
    #    asked about because they appear in neither whos_who nor the rulings.
    p = os.path.join(ROOT, 'corpus', 'letters.json')
    if os.path.isfile(p):
        for r in json.load(open(p, encoding='utf-8')):
            for tok in re.findall(r'[^\W\d_]{3,}', r.get('place') or ''):
                out.add(fold(tok))
    p = os.path.join(ROOT, 'pipeline/review', 'name_catalogue.py')
    if os.path.isfile(p):
        m = re.search(r"known_places = set\('''(.*?)'''", open(p, encoding='utf-8').read(), re.S)
        if m:
            out.update(fold(t) for t in m.group(1).split())

    # 5. names the site already gives a curated display entry
    p = os.path.join(ROOT, 'pipeline/build', 'build_site_data.py')
    if os.path.isfile(p):
        src = open(p, encoding='utf-8').read()
        block = re.search(r'^PEOPLE = \[.*?^\]', src, re.S | re.M)
        if block:
            for disp in re.findall(r"\(\s*'[a-z0-9_-]+',\s*'([^']+)'", block.group(0)):
                for tok in re.findall(r'[^\W\d_]{4,}', disp):
                    if tok[:1].isupper():
                        out.add(fold(tok))
    return out


def gather():
    recs = json.load(open(os.path.join(ROOT, 'corpus', 'letters.json'), encoding='utf-8'))
    seeds = {}
    sp = os.path.join(ROOT, 'reference', 'name_seeds.json')
    if os.path.isfile(sp):
        seeds = {e['name']: e for e in json.load(open(sp, encoding='utf-8'))}
    known = known_names()

    where, slot_where = defaultdict(list), defaultdict(list)
    total, slot_total = defaultdict(int), defaultdict(int)
    for r in recs:
        lid = str(r['letter_id'])
        for p in r['pages']:
            pg = str(p['page'])
            for line in (p.get('transcription') or p['diplomatic']).split('\n'):
                for m in NAME_SLOT.finditer(line):
                    t = m.group(1)
                    slot_total[t] += 1
                    if (lid, pg) not in slot_where[t]:
                        slot_where[t].append((lid, pg))
                for t in re.findall(r'[^\W\d_]{4,}', line):
                    if t[:1].isupper():
                        total[t] += 1
                        if (lid, pg) not in where[t]:
                            where[t].append((lid, pg))

    rows = []
    seed_stems = {fold(stem(n)) for n in seeds}
    for nm, e in seeds.items():
        # settled anywhere - who's-who, a ruling, the canon, a site entry -
        # or an inflection of something settled
        if (fold(nm) in known or fold(stem(nm)) in known or nm in OBVIOUS
                or e['source'] == 'canon'):
            continue
        rows.append((nm, e['count'], where.get(nm, []), e['kind']))
    for t, n in slot_total.items():
        if (t in seeds or fold(t) in known or fold(stem(t)) in known
                or n > 2 or t in NOT_NAMES
                or stem(t) in NOT_NAMES or fold(stem(t)) in seed_stems
                or len(where.get(t, ())) > 4):
            continue
        rows.append((t, n, slot_where.get(t, []), 'rare'))
    # Alphabetical, folded so that ä/ö/ü/ß sort with their base letters rather
    # than after z, and case is ignored.
    rows.sort(key=lambda r: (fold(r[0]), r[0]))
    return rows


def write_sheet():
    prior = {}
    if os.path.isfile(SHEET):
        with open(SHEET, encoding='utf-8-sig', newline='') as f:
            for r in csv.DictReader(f):
                if r.get('correct_form', '').strip():
                    prior[r['name']] = r['correct_form'].strip()
        shutil.copy2(SHEET, SHEET + '.bak')
    rows = gather()
    with open(SHEET, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['name', 'occurs_in', 'correct_form'])
        for nm, n, locs, kind in rows:
            loc = '; '.join(f'L{a} p{b}' for a, b in locs[:4])
            if len(locs) > 4:
                loc += f' (+{len(locs) - 4} more)'
            w.writerow([nm, loc, prior.get(nm, '')])
    print(f'wrote {SHEET}  -  {len(rows)} rows'
          + (f', {len(prior)} previous answers preserved' if prior else ''))
    print('Fill column 3 with the corrected spelling, or OK to confirm as-is.')


def read_sheet(apply_it):
    if not os.path.isfile(SHEET):
        sys.exit(f'no sheet at {SHEET} - run without --read first')
    filled, confirmed = [], []
    with open(SHEET, encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f):
            v = (r.get('correct_form') or '').strip()
            if not v:
                continue
            (confirmed if v.upper() == 'OK' else filled).append((r['name'], v, r['occurs_in']))
    print(f'{len(filled)} correction(s), {len(confirmed)} confirmed as-is')
    for nm, v, loc in filled:
        print(f'   {nm:<22} -> {v:<22} {loc}')
    if not apply_it:
        print('\n(reporting only - add --apply to write them to the corpus)')
        return
    if not filled:
        print('nothing to apply'); return

    lines = open(CORPUS, encoding='utf-8').read().split('\n')
    changed = 0
    for nm, v, _ in filled:
        pat = re.compile(r'(?<![^\W\d_])' + re.escape(nm) + r'(?![^\W\d_])')
        for i, l in enumerate(lines):
            new = pat.sub(v, l)
            if new != l:
                changed += len(pat.findall(l))
                lines[i] = new
    bak = CORPUS + '.bak_review'
    shutil.copy2(CORPUS, bak)
    open(CORPUS, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print(f'\napplied {changed} substitution(s)\nbackup at {bak}')
    print('now run:  python regenerate.py')


if __name__ == '__main__':
    if '--read' in sys.argv:
        read_sheet('--apply' in sys.argv)
    else:
        write_sheet()
