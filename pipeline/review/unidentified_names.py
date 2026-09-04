# -*- coding: utf-8 -*-
"""Every name in the corpus that has no identification yet.

`whos_who.md` covers ~76 name tokens. The corpus contains far more, and the
difference is not obscure: recurring correspondents like Grotowski, Lignowski
and Garczynski appear a dozen times each with no entry at all.

Three tiers, in the order they are worth your time:

  §1 recurring people   seeded, no who's-who entry, 2+ occurrences. Tractable:
                        they recur, so context accumulates across letters.
  §2 ambiguous          the corpus gives no clear person/place cue either way.
  §3 minor places       excludes the obvious cities; small estates and villages
                        where the identification is genuinely open.
  §4 the long tail      tokens in an unambiguous name slot that occur once or
                        twice and never became seeds. 527 of the 738 name-slot
                        tokens are hapax, so this is where most unknowns live -
                        and where no automated method can help.

Every row carries the letters it appears in, a context line, and the scan
filename, so each can be checked against the manuscript directly.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, csv, json, unicodedata
from collections import Counter, defaultdict

# Reuse the blocklist and stemmer the catalogue already vets names against,
# rather than keeping a second copy that can drift out of step.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# name_catalogue already installs a UTF-8 stdout wrapper on import; wrapping a
# second time closes the first one's buffer out from under us.
from name_catalogue import NOT_NAMES, stem
import unitlib
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UNIT = unitlib.one_unit(unitlib.unit_arg())
OUT = os.path.join(ROOT, 'review', 'unidentified_names.md')

# Cities that need no identifying - listing them would only bury the real work.
OBVIOUS = set('''Berlin Breslau Wien Paris Warschau Dresden Königsberg Posen
Prag Petersburg London Frankfurt Leipzig München Hamburg Stuttgart Weimar
Erfurt Magdeburg Potsdam Memel Glogau Brieg Neisse Küstrin Kalisz Preußen
Südpreußen Schlesien Pommern Sachsen Rußland Frankreich Österreich Pohlen
Polen Italien Böhmen Hessen Bayern Hannover Westphalen Holland Curland
Schweiz Elbe Oder Warthe Weichsel Rhein Donau'''.split())


def fold(s):
    s = unicodedata.normalize('NFKD', s.lower().replace('ſ', 's').replace('ß', 'ss'))
    return ''.join(c for c in s if not unicodedata.combining(c))


def whos_who_names():
    p = os.path.join(ROOT, 'reference', 'whos_who.md')
    out = set()
    if not os.path.isfile(p):
        return out
    for m in re.finditer(r'\*\*([^*]+)\*\*', open(p, encoding='utf-8').read()):
        for part in re.split(r'\s*/\s*|\s*,\s*', m.group(1)):
            part = re.sub(r'\([^)]*\)', '', part).strip()
            for tok in re.findall(r'[^\W\d_]{4,}', part):
                if tok[:1].isupper():
                    out.add(fold(tok))
    return out


NAME_SLOT = re.compile(
    r'(?:\bv\.?\s+|\bvon\s+|\bHerrn?\s+|\bH\.\s*|\bHl\.\s*|\bdH\.?\s*|\bdHl\.?\s*'
    r'|\bGraf(?:en)?\s+|\bGräfin\s+|\bBaron\s+|\bFrau\s+|\bMinister\s+'
    r'|\bGeneral\s+|\bGen\.?\s+|\bObrist(?:en)?\s+|\bRath\s+|\bDoctor\s+'
    r'|\bPr[äa]fect\s+|\bJustiz\s+|\bAmtmann\s+|\bPastor\s+|\bMajor\s+)'
    r'([A-ZÄÖÜ][^\W\d_]{3,})', re.UNICODE)


def main():
    recs = json.load(open(os.path.join(ROOT, 'corpus', 'letters.json'), encoding='utf-8'))
    scans = {}
    mp = os.path.join(UNIT.dir, 'page_scan_map.csv')
    if os.path.isfile(mp):
        for r in csv.DictReader(open(mp, encoding='utf-8-sig')):
            scans[(r['letter'], r['page'])] = r.get('image', '')

    where = defaultdict(list)
    letters_of = defaultdict(set)
    slot = Counter()
    slot_letters = defaultdict(set)
    slot_where = defaultdict(list)
    for r in recs:
        lid = str(r['letter_id'])
        for p in r['pages']:
            pg = str(p['page'])
            for line in (p.get('transcription') or p['diplomatic']).split('\n'):
                for m in NAME_SLOT.finditer(line):
                    tok = m.group(1)
                    slot[tok] += 1
                    slot_letters[tok].add(lid)
                    if len(slot_where[tok]) < 3:
                        slot_where[tok].append((lid, pg, line.strip()))
                for tok in re.findall(r'[^\W\d_]{4,}', line):
                    if tok[:1].isupper():
                        letters_of[tok].add(lid)
                        if len(where[tok]) < 3:
                            where[tok].append((lid, pg, line.strip()))

    known = whos_who_names()
    seeds = {}
    sp = os.path.join(ROOT, 'reference', 'name_seeds.json')
    if os.path.isfile(sp):
        seeds = {e['name']: e for e in json.load(open(sp, encoding='utf-8'))}

    def row(name, n, slot_only=False):
        w = (slot_where if slot_only else where).get(name, []) or where.get(name, [])
        src = slot_letters if slot_only else letters_of
        lt = sorted(src.get(name, []), key=lambda x: (len(x), x))
        ctx = w[0][2][:90].replace('|', '/') if w else ''
        scan = scans.get((w[0][0], w[0][1]), '') if w else ''
        return (f"| `{name}` | {n} | {', '.join(lt[:10])}"
                f"{' …' if len(lt) > 10 else ''} | {ctx} | `{scan}` |")

    L = []
    A = L.append
    A('# Unidentified names\n')
    A("Names occurring in the corpus with no entry in `whos_who.md`. Nothing here "
      "is a proposed correction — these are people and places the edition names "
      "but does not yet identify.\n")
    A('Every row gives the letters it appears in, a line of context, and the scan '
      'behind that page, so each can be checked against the manuscript.\n')

    unident = [(nm, e) for nm, e in seeds.items() if fold(nm) not in known]
    people = sorted([x for x in unident if x[1]['kind'] == 'person'],
                    key=lambda x: -x[1]['count'])
    unk = sorted([x for x in unident if x[1]['kind'] == 'unknown'],
                 key=lambda x: -x[1]['count'])
    places = sorted([x for x in unident if x[1]['kind'] == 'place'
                     and x[0] not in OBVIOUS], key=lambda x: -x[1]['count'])

    hdr = '| Name | × | Letters | Context | Scan |\n|---|---|---|---|---|'

    A(f'\n## §1. Recurring people, unidentified — {len(people)}\n')
    A('The most tractable: each recurs, so context accumulates across letters.\n')
    A(hdr)
    for nm, e in people:
        A(row(nm, e['count']))

    A(f'\n## §2. Type ambiguous — {len(unk)}\n')
    A('The corpus gives no clear person-or-place cue either way.\n')
    A(hdr)
    for nm, e in unk:
        A(row(nm, e['count']))

    A(f'\n## §3. Minor places — {len(places)}\n')
    A('Estates, villages and small towns. Obvious cities (Berlin, Wien, Paris …) '
      'are excluded — listing them would bury the real work.\n')
    A(hdr)
    for nm, e in places:
        A(row(nm, e['count']))

    seed_stems = {fold(stem(nm)) for nm in seeds}
    tail = [(t, n) for t, n in slot.items()
            if t not in seeds and fold(t) not in known and n <= 2
            and t not in NOT_NAMES and stem(t) not in NOT_NAMES
            # an inflection of a name already listed is not a new unknown
            and fold(stem(t)) not in seed_stems
            # a token that is common across the corpus is a word, not a hapax name
            and len(letters_of.get(t, ())) <= 4]
    tail.sort(key=lambda x: (-x[1], x[0]))
    A(f'\n## §4. The long tail — {len(tail)}\n')
    A('Tokens the corpus puts in an unambiguous name slot ("Herr v. X", '
      '"Major X") but which occur only once or twice, so no statistical method '
      'can confirm them. **This is where most unknowns live.** Expect a '
      'proportion to be misreadings rather than real names — `Munduhr` and '
      '`Bretz` both looked like this before they were read off the page.\n')
    A(hdr)
    for t, n in tail:
        A(row(t, n, slot_only=True))

    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print(f'§1 recurring people   {len(people)}')
    print(f'§2 type ambiguous     {len(unk)}')
    print(f'§3 minor places       {len(places)}')
    print(f'§4 long tail          {len(tail)}')
    print(f'\nwrote {OUT}')


if __name__ == '__main__':
    main()
