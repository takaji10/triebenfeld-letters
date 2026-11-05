# -*- coding: utf-8 -*-
"""Put the editor's proper names into document 6's English table.

    python scratch/map4456/apply_doc6_names.py

The liquidation register (apl399806603-006) prints the settlers' names as
Russian transliterations (Konchinskii Iakov). The editor's normalisation of
the 1896 plan's names (maps/pelzucki1896/farms.yml, name_norm; docs/
NAME_NORMALISATION_PLAN.md) is the proper reading, and the translation's
name column now carries it - firm and conjectural alike, the conjectural
brackets riding along. The diplomatic and reading views keep the
manuscript's Cyrillic and its transliteration untouched.

Two files change, each rewritten with its generator's own conventions
(yaml.safe_dump, width 100 - publish_translations.py writes the site file
the same way, so the shape stays canonical):
  site/_data/translations/apl399806603-006.yml  (what the page shows:
      each segment's en CSV, and the built html table beside it)
  units/apl399806603/intake/translation/doc6.yml  (the intake, kept in
      step so the reading survives beside its source)

The table's entry rows are 1-96 in this document; row 97 (Roads) belongs
to the 1896 plan, not to the register. The institutional rows (92-95)
already read as their English labels and stay as they are.
"""
import html
import io
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import name_norm  # noqa: E402  (for INSTITUTIONS; it also wraps stdout)

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass

PAD = 'apl399806603-006'
FILES = [
    os.path.join(ROOT, 'site', '_data', 'translations', PAD + '.yml'),
    os.path.join(ROOT, 'units', 'apl399806603', 'intake', 'translation',
                 'doc6.yml'),
]

# a numbered CSV row in the en block: the entry number, then the name up
# to the next comma (the shape unitlib.table_of reads)
ROW_RE = re.compile(r'(?m)^(\d{1,2}),([^,\n]*)(,.*)$')
# a built table cell: the entry number immediately followed by the name cell
CELL_RE = re.compile(
    r'<td class="no">(\d{1,2})</td><td class="name">([^<]*)</td>')


def display_names():
    """{row n: proper name for the translation's name column}."""
    f = yaml.safe_load(io.open(os.path.join(ROOT, 'maps', 'pelzucki1896',
                                            'farms.yml'), encoding='utf-8'))
    out = {}
    for s in f['settlers']:
        n = s['n']
        if n in name_norm.INSTITUTIONS:
            out[n] = s.get('name')      # the English label, already proper
        else:
            out[n] = s.get('name_norm')
    # the settler names must carry no comma and no quote, or the CSV's
    # shape breaks; the institutions' labels may (the headman's plot)
    for n, v in out.items():
        if n in name_norm.INSTITUTIONS:
            continue
        assert v and ',' not in v and "'" not in v and '"' not in v, (n, v)
    return out


def fix_en_csv(en, names):
    done = []

    def one(m):
        no, name, rest = int(m.group(1)), m.group(2), m.group(3)
        new = names.get(no)
        if new is None or new == name:
            return m.group(0)
        done.append(no)
        return '%d,%s%s' % (no, new, rest)

    return ROW_RE.sub(one, en), done


def fix_html(htm, names):
    done = []

    def one(m):
        no, old = int(m.group(1)), m.group(2)
        new = names.get(no)
        if new is None:
            return m.group(0)
        esc = html.escape(new, quote=False)
        if esc == old:
            return m.group(0)
        done.append(no)
        return '<td class="no">%d</td><td class="name">%s</td>' % (no, esc)

    return CELL_RE.sub(one, htm), done


def dump(d):
    return yaml.safe_dump(d, allow_unicode=True, default_flow_style=False,
                          sort_keys=False, width=100)


def main():
    names = display_names()
    for path in FILES:
        d = yaml.safe_load(io.open(path, encoding='utf-8'))
        n_csv = n_html = 0
        for s in (d.get('segments') or d.get('pages') or []):
            if s.get('en'):
                s['en'], done = fix_en_csv(s['en'], names)
                n_csv += len(done)
            if s.get('html'):
                s['html'], done = fix_html(s['html'], names)
                n_html += len(done)
        with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(dump(d))
        # the file must still read back with the names in place
        chk = yaml.safe_load(io.open(path, encoding='utf-8'))
        assert (chk.get('segments') or chk.get('pages')), path
        print('%s: %d CSV names, %d html cells' % (
            os.path.relpath(path, ROOT), n_csv, n_html))
    print('done - proper names in the translation of', PAD)


if __name__ == '__main__':
    main()
