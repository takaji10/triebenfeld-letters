# -*- coding: utf-8 -*-
"""Build maps/pelzucki1896/reds.yml from the editor's red readings."""
import io
import json
import re
import sys

import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

r = json.load(io.open('scratch/map4456/reds_all.json', encoding='utf-8'))
y = json.load(io.open('scratch/map4456/yards_read.json', encoding='utf-8'))

marks = []
for x in r['answered']:
    marks.append({'x': x['x'], 'y': x['y'], 'text': (x.get('text') or '').strip(),
                  'unsure': bool(x.get('unsure'))})
for x in r['added']:
    marks.append({'x': x['x'], 'y': x['y'], 'text': (x.get('text') or '').strip(),
                  'unsure': bool(x.get('unsure'))})


def near(a, b, tol=24):
    return abs(a['x'] - b['x']) <= tol and abs(a['y'] - b['y']) <= tol


for x in y['red_added']:
    if any(near(x, m) for m in marks):
        continue
    marks.append({'x': x['x'], 'y': x['y'], 'text': str(x.get('n', '')).strip(),
                  'unsure': '[' in str(x.get('n', ''))})

fx = y['red_fixes']
applied = 0
for m in marks:
    k = str(m['x']) + ',' + str(m['y'])
    if k in fx:
        m['text'] = str(fx[k]).strip()
        m['unsure'] = m['unsure'] or '[' in m['text']
        applied += 1


def kind(t):
    if re.fullmatch(r'\d+', t):
        return 'num'
    if '-' not in t and re.fullmatch(r'[\d\[\]\?]+', t) and re.search(r'\d', t):
        return 'unsure'
    return None


kept, dropped = [], []
for m in marks:
    k = kind(m['text'])
    if not k:
        dropped.append(m['text'])
        continue
    v = int(re.sub(r'[^\d]', '', m['text']))
    if not (1 <= v <= 97):
        dropped.append(m['text'])
        continue
    kept.append({'n': m['text'] if k == 'unsure' else v,
                 'x': m['x'], 'y': m['y'],
                 'unsure': True if k == 'unsure' else m['unsure']})

print('catalogue:', len(marks), '| fixes applied:', applied,
      '| kept as row numbers:', len(kept),
      '| unsure:', sum(1 for m in kept if m['unsure']),
      '| dropped:', len(dropped), sorted(set(dropped))[:10])

HDR = '''# The red numbers of the plan, the statement's row numbers on each parcel
# (map pelzucki1896).
#
# The red system read by the editor: red n marks a parcel of statement row n
# of the 1896 survey (APL 39/98/0/-/6603-6, the farmsteads' statement) - the
# mapping proved by clustering (maps/pelzucki1896/notes.md, "The red system
# settled"). The readings are the red map's export of 2026-11-01
# (scratch/map4456/reds_all.json: the red sheet's answers and the marks added
# on the map) with the yard session's additions (red_added) and the later
# corrections by position (red_fixes, %d applied). A mark whose reading is
# uncertain carries it as written - 3[7?] is 37, one digit doubtful - and
# shows unsure. The area readings (D-S) and fragments are not row numbers
# and are not here; the readings outside the rows 1..97 (%s) are left
# out. Positions are in the pixels of the mosaic (reference/maps.yml).
map: pelzucki1896
marks:
''' % (applied, ', '.join(sorted(set(dropped))[:6]) or 'none')

with io.open('maps/pelzucki1896/reds.yml', 'w', encoding='utf-8', newline='\n') as f:
    f.write(HDR)
    yaml.safe_dump(kept, f, allow_unicode=True, default_flow_style=False,
                   sort_keys=False, width=100)

d = yaml.safe_load(io.open('maps/pelzucki1896/reds.yml', encoding='utf-8'))
print('written reds.yml:', len(d['marks']))
