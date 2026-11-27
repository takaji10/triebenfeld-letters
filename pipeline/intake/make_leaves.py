# -*- coding: utf-8 -*-
"""The leaf or page number of each manuscript page, as the transcription files give it.

    python pipeline/intake/make_leaves.py            # check: what would be written
    python pipeline/intake/make_leaves.py --write    # units/<slug>/leaves.yml

The editor, 2026-11-27: the court records' page numbers ("[p. 585v]") are to stand in the transcriptions
and translations, as they stand in the editor's transcription files ("\\[172v\\]"). The holdings' intake
scripts recorded them when the pages were cut, as a LEAF dict ({page id: '172 verso'}); this collects
them into units/<slug>/leaves.yml ({page id: '172v'}), which build_site_data.py reads to set "[p. 172v]"
at the head of each page's text, in every view. Descriptions that are not numbers ('the cover', 'a blank
verso') give no mark. Three holdings number their pages by a rule rather than a dict (RULES below).
A holding's leaves.yml, once written, is the record: correct it by hand if the editor corrects a leaf.
"""
import ast
import csv
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def norm(v):
    v = str(v).strip()
    m = re.fullmatch(r'(?:leaf |p\. |page |fol\. )?(\d+)([rv]?)(?: (recto|verso))?(?: \(.*\))?', v)
    if not m:
        return None
    return m.group(1) + ('v' if m.group(2) == 'v' or m.group(3) == 'verso' else '')


def literal_leaf(slug):
    """The LEAF dict of a holding's intake scripts, where it is written out as a literal."""
    out = {}
    for p in sorted(glob.glob(os.path.join(ROOT, 'units', slug, 'intake', '*.py'))):
        tree = ast.parse(io.open(p, encoding='utf-8').read())
        consts = {}
        for node in tree.body:
            if not (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)):
                continue
            name, val = node.targets[0].id, node.value
            if isinstance(val, ast.Dict):
                try:
                    consts[name] = ast.literal_eval(val)
                except ValueError:
                    continue
                if name == 'LEAF':
                    out.update(consts[name])
            elif name == 'LEAF' and isinstance(val, ast.DictComp):
                it = val.generators[0].iter       # {..}.items() or NAME.items()
                if isinstance(it, ast.Call) and isinstance(it.func, ast.Attribute):
                    base = it.func.value
                    if isinstance(base, ast.Dict):          # {_p(k): v for k, v in {'0002_a2': 'fol. 1r'}.items()}
                        out.update(ast.literal_eval(base))
                    elif isinstance(base, ast.Name) and base.id in consts:   # {v: 'page ' + k for k, v in PAGE_ID.items()}
                        out.update({v: 'page ' + k for k, v in consts[base.id].items()})
    return out


def page_ids(slug):
    p = os.path.join(ROOT, 'dataset', 'units', slug, 'pages.csv')
    if not os.path.exists(p):
        return []
    ids = []
    for r in csv.DictReader(io.open(p, encoding='utf-8-sig')):
        m = re.search(r'_(\d{3,4}_[ab]\d?)-L', r['scan'])
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    return ids


def rule_145(pid):          # build_pages.py: '655' -> '0655_a2'; '655v' -> '0656_a1'
    n, side = pid.split('_')
    return str(int(n)) if side == 'a2' else '%dv' % (int(n) - 1) if side == 'a1' else None


def rule_paged(pid):        # one photograph per page side: _a the recto (or the page), _b the verso
    n, side = pid.split('_')
    return str(int(n)) + ('v' if side == 'b' else '')


RULES = {
    'app53170koningr145': rule_145,      # leaf N recto is page N_a2, leaf N verso page N+1_a1
    'app5320pozgr1181': rule_paged,      # pp. 161-167v: 0161_a is 161, 0161_b is 161v
    'app534062': rule_paged,             # manuscript page 222 (scan 231 of the archive's unit)
    'app5321pyzdrygr115': rule_paged,    # page 543 of the Relationes of 1791-1792
}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    write = '--write' in sys.argv
    for d in sorted(glob.glob(os.path.join(ROOT, 'units', '*', ''))):
        slug = os.path.basename(os.path.dirname(d))
        ids = page_ids(slug)
        if not ids:
            continue
        if slug in RULES:
            got = {pid: RULES[slug](pid) for pid in ids}
        else:
            lit = literal_leaf(slug)
            if not lit:
                continue
            got = {pid: norm(lit[pid]) for pid in ids if pid in lit}
        got = {k: v for k, v in got.items() if v}
        if not got:
            continue
        miss = [pid for pid in ids if pid not in got]
        print('%-22s %3d of %3d pages numbered%s' % (slug, len(got), len(ids),
                                                    ('; none for ' + ' '.join(miss)) if miss else ''))
        if write:
            body = ''.join("%s: '%s'\n" % (k, got[k]) for k in ids if k in got)
            io.open(os.path.join(ROOT, 'units', slug, 'leaves.yml'), 'w', encoding='utf-8', newline='\n').write(
                '# The leaf (or page) number of each page of this holding, as the transcription files give it:\n'
                '# shown as "[p. N]" at the head of each page\'s text (pipeline/intake/make_leaves.py, the editor,\n'
                '# 2026-11-27). The record: correct a number here by hand.\n' + body)


if __name__ == '__main__':
    main()
