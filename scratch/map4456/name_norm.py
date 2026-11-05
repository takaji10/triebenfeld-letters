# -*- coding: utf-8 -*-
"""The normalisation draft for the Pełzucki 1896 names (plan:
docs/NAME_NORMALISATION_PLAN.md).

Builds, from farms.yml + the four witnesses (the 1868 table, the 1869
copy, Breyer's copy, the 1896 statement):

- scratch/map4456/name_norm_draft.json - the proposed name_norm,
  name_lang, norm_conf and note for all 97 rows, for the editor to rule
  on;
- scratch/map4456/name_norm_sheet.html - the review sheet (served by
  save_server.py, like the labelling page).

The documentary fields (name, name_1868) are never rewritten here; the
normalisation is a proposal beside them. The editor's rulings already
made (2026-11-05, in conversation) are applied as firm: Gibel (not
Göbel), Bitner (not Büttner).
"""
import csv
import glob
import io
import json
import os
import sys
from datetime import date

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DOCS = os.path.join(ROOT, 'dataset', 'documents')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8',
                              errors='replace')

# ---- the editor's rulings already made -------------------------------------
RULINGS = {
    2: 'Gibel, not Göbel — seen in other records (editor, 2026-11-05)',
    54: 'Bitner, not Büttner — seen in other records (editor, 2026-11-05)',
    81: 'Schönfisch, not Scheinfisch (editor, 2026-11-05)',
}

# the institutional rows: the label in each language. The English is the
# display name the table has carried; the Polish is the proper local form;
# the German the editor asked for (2026-11-05). Row 97 reads simpler:
# Roads, not Under roads.
INSTITUTIONS = {
    92: dict(en='Village school', pl='Szkoła wiejska', de='Dorfschule'),
    93: dict(en='Common cemetery', pl='Cmentarz wspólny',
             de='Gemeindefriedhof'),
    94: dict(en='Plot of common land', pl='Działka gruntów wspólnych',
             de='Allmende'),
    95: dict(en="The village headman's plot", pl='Działka sołtysa',
             de='Schulzengrundstück'),
    97: dict(en='Roads', pl='Drogi', de='Wege',
             note='Подъ дорогами, under the roads — shown simply as Roads'),
}

# ---- the four witnesses ----------------------------------------------------
def rows_of(uid):
    doc = json.load(open(os.path.join(DOCS, uid + '.json'), encoding='utf-8'))
    return doc['text_english']


def parse(text):
    out = {}
    for row in csv.reader(io.StringIO(text)):
        if row and row[0].strip().isdigit():
            n = int(row[0])
            if 1 <= n <= 97:
                out[n] = row[1].strip()
    return out


def breyer():
    text = rows_of('app539680716-4')
    brows = []
    for row in csv.reader(io.StringIO(text)):
        cells = [c.strip() for c in row]
        if not any(cells):
            continue
        if cells[0].isdigit():
            brows.append((int(cells[0]), cells[1]))
        elif len(cells) > 2 and cells[2].isdigit():
            brows.append((None, cells[1]))
        elif brows and any(cells):
            n, nm = brows[-1]
            brows[-1] = (n, nm + ' ' + ' '.join(c for c in cells if c))
    out = {}
    for n, nm in brows:
        if n and 1 <= n <= 97:
            out[n] = nm.split(' — ')[0].strip()
    return out


A = parse(rows_of('apl399806603-1'))
B = parse(rows_of('apl399806603-2'))
D = parse(rows_of('apl399806603-6'))
C = breyer()

# ---- the given names, by target language -----------------------------------
# The surname's language chooses the table (a mixed row like Runga
# Voitsekh is German surname + Polish given name, normalised per element).
GIVEN = {
    'de': {
        'Iakov': 'Jakob', 'Martin': 'Martin', 'Karl': 'Karl',
        'Daniil': 'Daniel', 'Gotlib': 'Gottlieb', 'Kristiian': 'Christian',
        'Vilgelm': 'Wilhelm', 'Frants': 'Franz', 'Ian': 'Johann',
        'Kristof': 'Christoph', 'Iulian': 'Julian', 'Avgust': 'August',
        'Osip': 'Joseph', 'Voitsekh': 'Wojciech', 'Gotfrid': 'Gottfried',
        'Petr': 'Peter', 'Veniiamin': 'Benjamin', 'Mateush': 'Matthäus',
        'Friderik': 'Friedrich', 'Emanuil': 'Emanuel', 'Morits': 'Moritz',
        'Genrikh': 'Heinrich', 'Andrei': 'Andreas', 'Anton': 'Anton',
        'Liudvik': 'Ludwig', 'Mikhail': 'Michael', 'Samuil': 'Samuel',
        'Ivan': 'Johann', 'Stanislav': 'Stanislaus', 'Shchepan': 'Stephan',
        'Foma': 'Thomas', 'Martsin': 'Martin',
    },
    'pl': {
        'Iakov': 'Jakub', 'Martin': 'Marcin', 'Karl': 'Karol',
        'Daniil': 'Daniel', 'Gotlib': 'Gottlieb', 'Kristiian': 'Chrystian',
        'Vilgelm': 'Wilhelm', 'Frants': 'Franciszek', 'Ian': 'Jan',
        'Kristof': 'Krzysztof', 'Iulian': 'Julian', 'Avgust': 'August',
        'Osip': 'Józef', 'Voitsekh': 'Wojciech', 'Gotfrid': 'Gottfried',
        'Petr': 'Piotr', 'Veniiamin': 'Beniamin', 'Mateush': 'Mateusz',
        'Friderik': 'Fryderyk', 'Emanuil': 'Emanuel', 'Morits': 'Moritz',
        'Genrikh': 'Henryk', 'Andrei': 'Andrzej', 'Anton': 'Antoni',
        'Liudvik': 'Ludwik', 'Mikhail': 'Michał', 'Samuil': 'Samuel',
        'Ivan': 'Jan', 'Stanislav': 'Stanisław', 'Shchepan': 'Szczepan',
        'Foma': 'Tomasz', 'Martsin': 'Marcin',
    },
}
# Ivan/Ian: the Russian clerk's Иван covers Jan, Iwan and Johann alike;
# the surname's language decides, and the note says so when it does.

# ---- the rows: surname form, language, confidence, note --------------------
# sur: the proposed surname (or the whole norm for the institutional rows,
# marked with sur=None). alts: the alternatives the note mentions.
ROWS = {
    1: dict(sur='Kończyński', lang='pl', conf='conjectural',
            alts='Konchiński',
            note='Кончинскій: the stem could be Kończyn- or Koncin-'),
    2: dict(sur='Gibel', lang='de', conf='firm',
            note='editor\'s ruling 2026-11-05: Gibel in other records '
                 '(not Göbel)'),
    3: dict(sur='Mertz', lang='de', conf='conjectural', alts='Merz'),
    4: dict(sur='Holm', lang='de', conf='firm'),
    5: dict(sur='Mertz', lang='de', conf='conjectural', alts='Merz'),
    6: dict(sur='Hirsch', lang='de', conf='conjectural',
            alts='Giersz (Polish)'),
    7: dict(sur='Kinast', lang='de', conf='firm'),
    8: dict(sur='Strzyżykowski', lang='pl', conf='conjectural',
            alts='Strzyżowski',
            note='from strzyżyk (the wren) or the place Strzyżów'),
    9: dict(sur='Sanikowski', lang='pl', conf='conjectural',
            alts='Sannikowski'),
    10: dict(sur='Marek', lang='pl', conf='firm',
             note='the surname is Polish as spelt; Breyer\'s 1875 pencil '
                  'note: a Merz farmed it'),
    11: dict(sur='Grünwald', lang='de', conf='firm'),
    12: dict(sur='Śliwiński', lang='pl', conf='firm',
             note='collation: the 1868, 1869 and Breyer readings agree '
                  'plainly - the 1896 uncertainty can be lifted (ruling '
                  'pending)'),
    13: dict(sur='Steinbart', lang='de', conf='conjectural',
             alts='Steinbord, Steinbardt'),
    14: dict(sur='Holm', lang='de', conf='firm'),
    15: dict(sur='Falk', lang='de', conf='firm'),
    16: dict(sur='Mertz', lang='de', conf='conjectural', alts='Merz'),
    17: dict(sur='Mertz', lang='de', conf='conjectural', alts='Merz'),
    18: dict(sur='Sanikowski', lang='pl', conf='conjectural',
             alts='Sannikowski'),
    19: dict(sur='Stürzenbecker', lang='de', conf='conjectural',
             note='the three Russian spellings (Sturtsenbekher, '
                  'Shtirtsenbeker, Stirtsenbeker) all point here; a '
                  'documented Olęder surname - confirm'),
    20: dict(sur='Sanikowski', lang='pl', conf='conjectural',
             alts='Sannikowski'),
    21: dict(sur='Goske', lang='de', conf='firm',
             norm='heirs of Karl Goske',
             note='the heirs rows reorder to the given name first, as '
                  'their own languages write them'),
    22: dict(sur='Bludziński', lang='pl', conf='firm'),
    23: dict(sur='Śmigelski', lang='pl', conf='firm'),
    24: dict(sur='Rogacki', lang='pl', conf='firm',
             norm='heirs of Piotr Rogacki'),
    25: dict(sur=None, lang='pl', conf='conjectural',
             norm='[uncertain: Promins] Szczepan',
             note='all four witnesses hesitate on the same word '
                  '(Promist/Promins) - stays uncertain'),
    26: dict(sur='Runge', lang='de', conf='firm',
             note='the given name is Polish (Wojciech) - normalised per '
                  'element'),
    27: dict(sur='Runge', lang='de', conf='firm',
             norm='heirs of Gottfried Runge'),
    28: dict(sur='Falkenberg', lang='de', conf='firm'),
    29: dict(sur='Goske', lang='de', conf='conjectural',
             note='Goska → Goske: the 1868 genitive (Госкѣ) spells it '
                  'with e'),
    30: dict(sur='Schulz', lang='de', conf='firm'),
    31: dict(sur='Knafkus', lang='de', conf='conjectural',
             alts='Knaufkus'),
    32: dict(sur='Runge', lang='de', conf='firm',
             norm='heirs of Wojciech Runge',
             note='Рунги is the genitive of Runge'),
    33: dict(sur='Runge', lang='de', conf='firm',
             norm='heirs of Gottfried Runge'),
    34: dict(sur='Runge', lang='de', conf='firm'),
    35: dict(sur='Kitke', lang='de', conf='conjectural', alts='Kietke'),
    36: dict(sur='Friedenberg', lang='de', conf='firm'),
    37: dict(sur='Zellmer', lang='de', conf='firm', alts='Zöllmer'),
    38: dict(sur='Malinowski', lang='pl', conf='firm'),
    39: dict(sur='Haupt', lang='de', conf='firm',
             note='1868 reads Haupt Franz Christian - the 1896 clerk '
                  'dropped the middle name'),
    40: dict(sur='Schwebs', lang='de', conf='conjectural', alts='Schwabs'),
    41: dict(sur='Stürzenbecker', lang='de', conf='conjectural',
             note='as farm 19'),
    42: dict(sur='Betke', lang='de', conf='firm',
             norm='heirs of Christian Betke'),
    43: dict(sur='Kinast', lang='de', conf='firm'),
    44: dict(sur='Rasch', lang='de', conf='firm',
             note='1868 reads Rasch Friedrich Ivan - the 1896 clerk '
                  'dropped Ivan (Johann)'),
    45: dict(sur='Banzert', lang='de', conf='conjectural',
             alts='Bandzert, Bansert'),
    46: dict(sur='Kuhn', lang='de', conf='conjectural',
             alts='Kühn, Kun'),
    47: dict(sur='Zeer', lang='de', conf='conjectural', alts='Seher'),
    48: dict(sur='Banzert', lang='de', conf='conjectural',
             alts='Bandzert, Bansert'),
    49: dict(sur='Mertz', lang='de', conf='conjectural', alts='Merz'),
    50: dict(sur='Zellmer', lang='de', conf='firm', alts='Zöllmer'),
    51: dict(sur='Gibel', lang='de', conf='firm',
             note='editor\'s ruling 2026-11-05: Gibel in other records '
                  '(not Göbel)'),
    52: dict(sur='Śmigelski', lang='pl', conf='firm'),
    53: dict(sur='Zellmer', lang='de', conf='firm', alts='Zöllmer',
             norm='heirs of Daniel Zellmer'),
    54: dict(sur='Bitner', lang='de', conf='firm',
             note='editor\'s ruling 2026-11-05: Bitner in other records '
                  '(not Büttner)'),
    55: dict(sur='Rittamer', lang='de', conf='conjectural',
             alts='Rytamer, Riedamer'),
    56: dict(sur='Przystański', lang='pl', conf='conjectural',
             alts='Przystalski, Przytański',
             note='прж renders the Polish prz-'),
    57: dict(sur='Bartel', lang='de', conf='firm'),
    58: dict(sur='Goske', lang='de', conf='firm',
             note='the given name is Polish'),
    59: dict(sur='Hintz', lang='de', conf='conjectural',
             alts='Hinz, Ginz',
             note='cf. Hintz in Breyer\'s tables of the neighbouring '
                  'colonies (APP 716, doc 5160)'),
    60: dict(sur='Stark', lang='de', conf='firm'),
    61: dict(sur='Kinast', lang='de', conf='firm',
             note='the given name is Polish'),
    62: dict(sur='Kussmann', lang='de', conf='conjectural',
             alts='Kusman, Kußmann'),
    63: dict(sur='Kinast', lang='de', conf='firm',
             norm='heirs of Wojciech Kinast',
             note='the given name is Polish'),
    64: dict(sur='Gehrke', lang='de', conf='firm'),
    65: dict(sur='Zellmer', lang='de', conf='firm', alts='Zöllmer'),
    66: dict(sur='Stark', lang='de', conf='firm'),
    67: dict(sur='Zellmer', lang='de', conf='firm', alts='Zöllmer'),
    68: dict(sur='Liepelt', lang='de', conf='firm'),
    69: dict(sur='Gotter', lang='de', conf='firm'),
    70: dict(sur='Moritz', lang='de', conf='firm',
             note='the surname here is Moritz (Морицъ), the given name '
                  'Gottfried'),
    71: dict(sur='Obst', lang='de', conf='firm'),
    72: dict(sur='Reich', lang='de', conf='firm'),
    73: dict(sur='Schwebs', lang='de', conf='conjectural',
             alts='Schwabs'),
    74: dict(sur='Haupt', lang='de', conf='firm'),
    75: dict(sur='Haupt', lang='de', conf='firm',
             note='1868 reads Haupt Gottfried Christian - the middle '
                  'name distinguishes him from the Christian Haupt of '
                  'farm 76 (father and son); the 1896 clerk dropped it'),
    76: dict(sur='Haupt', lang='de', conf='firm',
             note='1868 reads Khaupt Kristiian Kristiianov = Christian, '
                  'son of Christian - the patronymic is what tells him '
                  'from farm 75; the 1896 clerk dropped it'),
    77: dict(sur=None, lang='de', conf='conjectural',
             norm='Haupt Christian [conflict]',
             note='CONFLICT: the 1896 statement (the map\'s own source) '
                  'reads Gebel Kristiian, but the 1868 table, the 1869 '
                  'copy and Breyer all read Khaupt Gotfridov Kristiian '
                  '(Haupt, Gottfried\'s son). Rule: clerk\'s error, or '
                  'the farm changed hands (docs 4-5)?'),
    78: dict(sur='Zielczak', lang='pl', conf='conjectural',
             alts='Zelczak, Selczak'),
    79: dict(sur='Szczepiński', lang='pl', conf='firm'),
    80: dict(sur='Vogel', lang='de', conf='firm'),
    81: dict(sur='Schönfisch', lang='de', conf='firm',
             note='editor\'s ruling 2026-11-05: Schönfisch, not '
                  'Scheinfisch'),
    82: dict(sur='Rogacki', lang='pl', conf='firm'),
    83: dict(sur='Fetter', lang='de', conf='conjectural', alts='Vetter'),
    84: dict(sur='Stürzenbecker', lang='de', conf='conjectural',
             norm='heirs of Johann Stürzenbecker',
             note='1868 names the deceased: Ivan (Johann); the 1896 '
                  'clerk dropped the given name - restored here from '
                  'the 1868 witness'),
    85: dict(sur='Kinast', lang='de', conf='firm'),
    86: dict(sur='Haupt', lang='de', conf='firm'),
    87: dict(sur='Haupt', lang='de', conf='firm'),
    88: dict(sur='Hermann', lang='de', conf='conjectural',
             note='Германъ as surname → Hermann; the given name is '
                  'Polish (Wojciech)'),
    89: dict(sur='Tarnowski', lang='pl', conf='firm',
             norm='heirs of Michał Tarnowski'),
    90: dict(sur='Rogowicz', lang='pl', conf='conjectural',
             alts='Rogowitz'),
    91: dict(sur='Marylski', lang='pl', conf='firm'),
    92: dict(sur=None, lang='pl', conf='firm', norm='Szkoła wiejska',
             note='the village school'),
    93: dict(sur=None, lang='pl', conf='firm', norm='Cmentarz wspólny',
             note='the common cemetery'),
    94: dict(sur=None, lang='pl', conf='conjectural',
             norm='Działka gruntów wspólnych',
             note='the communal-land plot; the Polish wording is '
                  'editorial'),
    95: dict(sur=None, lang='pl', conf='firm', norm='Działka sołtysa',
             note='the village headman\'s plot'),
    96: dict(sur='Reich', lang='de', conf='firm',
             note='the 1896 columns are dotted (..) and the name '
                  'duplicates farm 72 - the same man\'s second plot, or '
                  'a clerical repetition; check the scan'),
    97: dict(sur=None, lang='pl', conf='firm', norm='Drogi',
             note='Подъ дорогами, under the roads - shown simply as '
                  'Roads'),
}


def norm_of(n, name):
    r = ROWS[n]
    if r.get('norm'):
        return r['norm']
    # an uncertain reading carries its doubt into the norm: '[uncertain:
    # Slivinskii] Gotlib' -> '[uncertain: Śliwiński] Gottlieb'
    lead = ''
    body = name
    if body.startswith('[uncertain:'):
        inner, _, body = body[len('[uncertain:'):].partition(']')
        # the doubt carries into the norm around the surname alone: the
        # given name is not in doubt. '[uncertain: Slivinskii] Gotlib'
        # -> '[uncertain: Śliwiński] Gottlieb'
        gmap = GIVEN[r['lang']]
        parts = [gmap.get(g.rstrip('.'), g)
                 for g in body.strip().split()]
        return '[uncertain: ' + r['sur'] + '] ' + ' '.join(parts)
    return _norm_parts(r, None, body)


def _norm_parts(r, force_sur, body):
    gmap = GIVEN[r['lang']]
    toks = body.split()
    sur = force_sur if force_sur is not None else r['sur']
    givens = toks[1:] if force_sur is None else toks
    parts = [sur]
    for g in givens:
        g2 = g.rstrip('.')
        if g2 in gmap:
            parts.append(gmap[g2])
        else:
            parts.append(g)   # unknown given name: left as transcribed
    return ' '.join(parts)


def apply():
    """Write the approved normalisation into farms.yml: name_norm,
    name_lang, norm_conf, norm_note per settler; the institutional rows
    also get name_de and keep their English display name (row 97 reads
    Roads now). The marks list passes through untouched."""
    yml = os.path.join(ROOT, 'maps', 'pelzucki1896', 'farms.yml')
    text = io.open(yml, encoding='utf-8').read()
    d = yaml.safe_load(text)
    n_set = 0
    for s in d['settlers']:
        n = s['n']
        r = ROWS.get(n)
        if r is None:
            continue
        name = s.get('name') or ''
        inst = n in INSTITUTIONS
        if inst:
            ie = INSTITUTIONS[n]
            s['name'] = ie['en']
            s['name_norm'] = ie['pl']
            s['name_de'] = ie['de']
            s['name_lang'] = 'pl'
            s['norm_note'] = ie.get('note', '')
            s['norm_conf'] = 'firm' if n != 94 else 'conjectural'
            s['institution'] = True
        else:
            s['name_norm'] = norm_of(n, name)
            s['name_lang'] = r['lang']
            s['norm_conf'] = r['conf']
            note = r.get('note', '')
            if r.get('alts'):
                note = (note + ' ' if note else '') + \
                    '(also possible: ' + r['alts'] + ')'
            if note:
                s['norm_note'] = note
        if n in RULINGS:
            s['norm_note'] = RULINGS[n]
            s['norm_conf'] = 'firm'
        n_set += 1
    header = text.split('\nsettlers:', 1)[0]
    if not header.endswith('\n'):
        header += '\n'
    with open(yml, 'w', encoding='utf-8', newline='\n') as f:
        f.write(header)
        yaml.safe_dump({'settlers': d['settlers'], 'marks': d['marks']},
                       f, allow_unicode=True, default_flow_style=False,
                       sort_keys=False, width=100)
    print('applied normalisation to %d settlers -> %s' % (n_set, yml))


def main():
    if '--apply' in sys.argv:
        apply()
        return
    y = yaml.safe_load(io.open(
        os.path.join(ROOT, 'maps', 'pelzucki1896', 'farms.yml'),
        encoding='utf-8'))
    rows = []
    for s in y['settlers']:
        n = s['n']
        r = ROWS[n]
        name = s.get('name') or ''
        norm = r.get('norm') or norm_of(n, name)
        w = []
        for key, src in (('1868', A), ('1869', B), ('1896', D),
                         ('Breyer', C)):
            v = src.get(n)
            if v:
                w.append('%s: %s' % (key, v))
        divergent = len({A.get(n), B.get(n), D.get(n)}) > 1
        rows.append({
            'n': n,
            'name': name,
            'name_1868': s.get('name_1868'),
            'witnesses': w,
            'divergent': divergent,
            'norm': norm,
            'lang': r['lang'],
            'conf': r['conf'],
            'note': r.get('note', ''),
        })
    n_firm = sum(1 for r in rows if r['conf'] == 'firm')
    n_conj = sum(1 for r in rows if r['conf'] == 'conjectural')
    n_div = sum(1 for r in rows if r['divergent'])
    out = {
        'generated': date.today().isoformat(),
        'rulings_applied': RULINGS,
        'counts': {'rows': len(rows), 'firm': n_firm,
                   'conjectural': n_conj, 'divergent_witnesses': n_div},
        'rows': rows,
    }
    p = os.path.join(HERE, 'name_norm_draft.json')
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('draft: %d rows (%d firm, %d conjectural, %d divergent) -> %s'
          % (len(rows), n_firm, n_conj, n_div, p))
    sheet(rows, out)


def sheet(rows, out):
    html = SHEET_TMPL.replace('__DATA__', json.dumps(out, ensure_ascii=False)
                              .replace('<', '\\u003c'))
    p = os.path.join(HERE, 'name_norm_sheet.html')
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('sheet: %s' % p)


SHEET_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Name normalisation — Pełzucki 1896 (review sheet)</title>
<style>
body { margin: 0; font: 14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #171614; color: #e8e3da; }
header { padding: .6rem 1rem; border-bottom: 1px solid #38342e; }
h1 { font-size: 1rem; margin: 0 0 .25rem; font-weight: 600; }
.hint { color: #8b847a; font-size: .8rem; }
.hint b { color: #b3aca1; }
#tools { position: sticky; top: 0; z-index: 5; display: flex; gap: .4rem; padding: .5rem 1rem; background: #171614; border-bottom: 1px solid #38342e; }
button { font: inherit; font-size: .8rem; background: #24211d; color: #e8e3da; border: 1px solid #38342e; border-radius: 4px; padding: .3rem .7rem; cursor: pointer; }
button[aria-pressed="true"] { background: #8a6d3b; border-color: #8a6d3b; }
table { border-collapse: collapse; width: 100%; font-size: .85rem; }
th, td { padding: .3rem .5rem; text-align: left; vertical-align: top; border-bottom: 1px solid #2b2823; }
th { position: sticky; top: 2.6rem; background: #24211d; font-size: .72rem; text-transform: uppercase; letter-spacing: .06em; color: #8b847a; }
td.num, th.num { text-align: right; white-space: nowrap; }
tr.conj td { background: rgba(138, 109, 59, .12); }
tr.conflict td { background: rgba(168, 66, 47, .18); }
.norm { font-weight: 600; }
.conf-firm { color: #7da06b; }
.conf-conjectural { color: #d8a53e; }
.wit { color: #8b847a; font-size: .74rem; white-space: pre-line; }
.note { color: #b3aca1; font-size: .78rem; max-width: 26rem; }
.flag { display: inline-block; background: #7a1f14; color: #ffd9cf; border-radius: 3px; padding: 0 .3rem; font-size: .68rem; margin-left: .3rem; }
</style>
</head>
<body>
<header>
  <h1>Name normalisation — Pełzucki 1896 (review sheet)</h1>
  <div class="hint">The documentary transliteration is <b>never rewritten</b>; this sheet proposes the proper Polish/German rendering beside it. Amber rows are <b>conjectural</b> (the note carries the alternatives — confirm or correct); red rows carry a <b>conflict between the witnesses</b> and need a ruling. The decisions live in <b>scratch/map4456/name_norm_draft.json</b> — edit it directly or tell Claude the changes. The editor's rulings already applied: <b>Gibel</b> (not Göbel), <b>Bitner</b> (not Büttner).</div>
</header>
<div id="tools">
  <button data-f="all" aria-pressed="true">All 97</button>
  <button data-f="conj">Conjectural</button>
  <button data-f="conf">Conflicts</button>
  <button data-f="div">Witnesses differ</button>
</div>
<table>
<thead><tr>
<th class="num">№</th><th>As transcribed</th><th>The four witnesses</th>
<th>Proposed proper spelling</th><th>Lang</th><th>Conf.</th><th>Note</th>
</tr></thead>
<tbody id="tb"></tbody>
</table>
<script>
const DATA = __DATA__;
const tb = document.getElementById('tb');
function row(r) {
  const tr = document.createElement('tr');
  tr.className = (r.conf === 'conjectural' ? 'conj ' : '') +
    (r.norm.includes('conflict') ? 'conflict' : '');
  const wit = r.divergent ? r.witnesses.join('\\n') : '';
  tr.innerHTML =
    '<td class="num">' + r.n + '</td>' +
    '<td>' + esc(r.name) + (r.name_1868 && r.name_1868 !== r.name ?
      ' <span class="wit">(1868: ' + esc(r.name_1868) + ')</span>' : '') +
    '</td>' +
    '<td class="wit">' + esc(wit) + '</td>' +
    '<td class="norm">' + esc(r.norm) +
      (r.conf === 'conjectural' ? '<span class="flag">?</span>' : '') +
    '</td>' +
    '<td>' + r.lang + '</td>' +
    '<td class="conf-' + r.conf + '">' + r.conf + '</td>' +
    '<td class="note">' + esc(r.note) + '</td>';
  return tr;
}
function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
}
function show(f) {
  tb.innerHTML = '';
  DATA.rows.forEach(r => {
    if (f === 'conj' && r.conf !== 'conjectural') return;
    if (f === 'conf' && !r.norm.includes('conflict')) return;
    if (f === 'div' && !r.divergent) return;
    tb.appendChild(row(r));
  });
}
document.querySelectorAll('#tools button').forEach(b => {
  b.addEventListener('click', () => {
    document.querySelectorAll('#tools button').forEach(x =>
      x.setAttribute('aria-pressed', 'false'));
    b.setAttribute('aria-pressed', 'true');
    show(b.dataset.f);
  });
});
show('all');
</script>
</body>
</html>
"""

if __name__ == '__main__':
    main()
