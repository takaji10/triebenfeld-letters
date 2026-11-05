# -*- coding: utf-8 -*-
"""Round-trip test of the red corrections through the import, without a
browser: a synthetic red_labels_latest.json (two corrections, one to a firm
number, one back to an unsure reading) -> import_farms.py -> reds.yml."""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SAVE = 'scratch/map4456/test-state/red_labels_latest.json'
os.makedirs('scratch/map4456/test-state', exist_ok=True)
YML = 'maps/pelzucki1896/reds.yml'
had_yml = os.path.isfile(YML)
bak = tempfile.mktemp(suffix='.yml')
if had_yml:
    shutil.copy(YML, bak)
had_save = os.path.isfile(SAVE)
if had_save:
    shutil.copy(SAVE, bak + '.save')
try:
    r = yaml.safe_load(io.open(YML, encoding='utf-8'))
    marks = r['marks']
    first = next(m for m in marks if m.get('unsure'))
    plain = next(m for m in marks if not m.get('unsure'))
    saved = [{'n': x['n'], 'x': x['x'], 'y': x['y']} for x in marks]
    # correction 1: the unsure 4[5?] read firm as 45
    for x in saved:
        if x['x'] == first['x'] and x['y'] == first['y']:
            x['n'] = '45'
    # correction 2: a firm reading gains a doubt
    for x in saved:
        if x['x'] == plain['x'] and x['y'] == plain['y']:
            x['n'] = str(plain['n']) + '[?]'
    json.dump(saved, io.open(SAVE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    p = subprocess.run([sys.executable, 'pipeline/maps/import_farms.py', SAVE],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(p.stdout)
    if p.returncode != 0:
        print('STDERR:', p.stderr[-400:])
    d = yaml.safe_load(io.open(YML, encoding='utf-8'))
    f1 = next(m for m in d['marks'] if m['x'] == first['x'] and m['y'] == first['y'])
    f2 = next(m for m in d['marks'] if m['x'] == plain['x'] and m['y'] == plain['y'])
    print('correction 1:', f1)
    print('correction 2:', f2)
    ok1 = f1['n'] == '45' and not f1['unsure']
    ok2 = f2['n'] == str(plain['n']) + '[?]' and f2['unsure']
    print('firm read lands:', 'PASS' if ok1 else 'FAIL')
    print('doubt lands:', 'PASS' if ok2 else 'FAIL')
    print('mark count kept:', 'PASS' if len(d['marks']) == len(marks) else 'FAIL')
finally:
    if had_yml:
        shutil.copy(bak, YML)
    elif os.path.isfile(YML):
        os.remove(YML)
    if had_save:
        shutil.copy(bak + '.save', SAVE)
    elif os.path.isfile(SAVE):
        os.remove(SAVE)
    print('reds.yml and the working file restored')
