# -*- coding: utf-8 -*-
"""Check the descriptors written before place names against how the place is classed.

    python pipeline/review/check_place_descriptors.py

The editor, 2026-11-14, after the homepage called Konin and Kalisz "towns":
a place named with a descriptor ("the town of X", "the village of X", "the
cities of X and Y") is checked against its kind in reference/places.yml or
reference/gazetteer/<slug>.yml before the sentence is written (HOUSE_STYLE,
"Check what a place is before you call it something").

Reads the authored prose that readers see (page texts, descriptions, summaries,
timeline notes, era essays) and lists every descriptor that does not match the
place's recorded kind. It changes nothing; a person reads the list. A place
with no recorded kind is not listed. The register's kinds are uneven (Konin is
a "town", Częstochowa a "town"): a mismatch is a question, not always an error. Two kinds of mismatch are
right and stay: a descriptor correct for the period written about ("its
village of Zagórów" before the town charter of 1407), and a place the sources
call one thing and the register another (the "town" of Kamionna of the charter
of 1796, an estate in the register). Read each against the sentence.
"""
import glob, io, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# descriptor word -> the kinds of the register that it is allowed to name.
# "estate of X" and "manor of X" are left out: they name a landholding that
# carries the place's name (the estate of Zagórów), not what the place is.
CLASS = {
    'city': {'city'}, 'cities': {'city'}, 'town': {'town'}, 'towns': {'town'},
    'village': {'village'}, 'villages': {'village'},
    'hamlet': {'hamlet'}, 'hamlets': {'hamlet'},
    # a colony or a settlement may be a village or a hamlet as well
    'colony': {'settlement', 'oleder-settlement', 'colony', 'village', 'hamlet'},
    'colonies': {'settlement', 'oleder-settlement', 'colony', 'village', 'hamlet'},
    'settlement': {'settlement', 'oleder-settlement', 'colony', 'village', 'hamlet'},
    'settlements': {'settlement', 'oleder-settlement', 'colony', 'village', 'hamlet'},
}
# German "Stadt" names a city or a town, so either record fits it
DE = {'Stadt': {'city', 'town'}, 'Städte': {'city', 'town'}, 'Städten': {'city', 'town'},
      'Dorf': {'village'}, 'Dörfer': {'village'}, 'Dorfes': {'village'},
      'Weiler': {'hamlet', 'village'}}


def kinds():
    """name (lower case) -> set of recorded kinds."""
    out = {}
    def add(name, kind):
        if name and kind:
            out.setdefault(name.lower(), set()).add(str(kind))
    pl = yaml.safe_load(open('reference/places.yml', encoding='utf-8'))
    for v in (pl.get('places', pl) or {}).values():
        if isinstance(v, dict):
            for key in ('display', 'german'):
                add(v.get(key), v.get('kind'))
    for f in glob.glob('reference/gazetteer/*.yml'):
        d = yaml.safe_load(open(f, encoding='utf-8'))
        if isinstance(d, dict):
            add(d.get('heading'), d.get('kind'))
            for a in d.get('aliases') or []:
                add(str(a).split(',')[0], d.get('kind'))
    return out


def values(x, where=''):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from values(v, f'{where}.{k}')
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from values(v, f'{where}.{i}')
    elif isinstance(x, str):
        yield where, x


def texts():
    ymls = ['site/_data/i18n.yml', 'site/_data/timeline.yml', 'site/_data/summaries.yml',
            'site/_data/summaries_de.yml', 'reference/eras.yml', 'reference/people_bios.yml',
            'reference/genealogy.yml', 'literature/links.yml']
    ymls += glob.glob('units/*/unit.yml') + glob.glob('literature/*/work.yml')
    for f in ymls:
        try:
            d = yaml.safe_load(open(f, encoding='utf-8'))
        except Exception:
            continue
        for where, v in values(d):
            yield f + where, v
    mds = (glob.glob('units/*/about*.md') + glob.glob('site/*.md') + glob.glob('site/de/*.md')
           + glob.glob('site/eras/*.md') + glob.glob('site/de/epochen/*.md'))
    for f in mds:
        s = open(f, encoding='utf-8').read()
        s = re.sub(r'<!--.*?-->|\{%.*?%\}|\{\{.*?\}\}', '', s, flags=re.S)
        yield f, s


NAME = r"[A-ZŁŚŻŹĆŃÓ][\w'’.-]*(?: (?:am|an der|nad|pod) [A-ZŁŚŻŹĆŃÓ]\w+)?"
EN = re.compile(r'\b(' + '|'.join(CLASS) + r') of (' + NAME + r'(?:,? (?:and|und) ' + NAME + r')*)')
DEP = re.compile(r'\b(' + '|'.join(DE) + r') (' + NAME + r'(?:,? (?:und) ' + NAME + r')*)')


def main():
    known = kinds()
    seen, bad = set(), []
    for where, s in texts():
        for rx, table in ((EN, None), (DEP, DE)):
            for m in rx.finditer(s):
                word = m.group(1)
                allowed = CLASS[word] if table is None else table[word]
                names = re.split(r',? (?:and|und) ', m.group(2))
                if not word.endswith('s') and word not in ('Städte', 'Städten', 'Dörfer'):
                    names = names[:1]       # "the town of X and Y": only X is the town
                for name in names:
                    name = name.strip().rstrip('.,;')
                    have = known.get(name.lower())
                    if not have or have & allowed:
                        continue
                    key = (word, name, where.split('.')[0])
                    if key in seen:
                        continue
                    seen.add(key)
                    bad.append((where, word, name, sorted(have), s[max(0, m.start() - 40):m.end() + 20].replace('\n', ' ')))
    for where, word, name, have, ctx in sorted(bad):
        print(f'{where}: "{word} ... {name}" but {name} is recorded as {", ".join(have)}\n    ...{ctx}...')
    print(f'\n{len(bad)} descriptor(s) to read against the register')


if __name__ == '__main__':
    main()
