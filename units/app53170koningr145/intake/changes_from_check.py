# -*- coding: utf-8 -*-
"""Write changes.yml for APP 53/17/0/-/Konin Gr.145 from the record of the full check.

    python units/app53170koningr145/intake/changes_from_check.py

changes.yml is what pipeline/review/changes_page.py reads to make the
editor's page of changes across the Prusimski-era holdings ("a page showing
dropped phrases and their importance, since I need to update some writing
outside of the project": the editor, 2026-10-07). For this holding it is not
written by hand: it is made from full_check_rows.py (every dropped phrase,
and the misread words in the court's own rulings) and
translation/fixes_full.py (what changed in the English), so it says what
those files say. The fuller sheet for this holding alone is dropped_sheet.py.
"""
import io
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'translation'))
import dropped_sheet as D  # noqa: E402
import full_check_rows as F  # noqa: E402
from fixes_full import FIXES_FULL  # noqa: E402

GRADE = {'court': 'significant', 'fact': 'fact', 'formula': 'wording'}


def main():
    order = D.ids()
    dropped = [r for r in F.ROWS if r['kind'] == 'dropped']
    en_dropped = [x for x in FIXES_FULL if x[3].startswith('dropped') or x[3].startswith('a paragraph')]
    en_other = [x for x in FIXES_FULL if x not in en_dropped]
    need = [r for r in dropped if not any(r['page'] == k[0] and r['new'].split().count(k[1]) for k in D.ENGLISH_HAD_IT)]
    fix_of = {id(r): x for r, x in zip(need, en_dropped)}
    out = []

    def where(pid):
        return 'leaf %s, page %d of 122' % (D.leaf(pid), order.index(pid) + 1)

    e = D.EARLIER
    out.append({'importance': GRADE[e['weight']], 'kind': 'dropped phrase', 'where': 'leaf %s, page %d of 122' % (e['leaf'], e['page']),
                'what': e['note'], 'was': '(six Polish words missing)', 'now': 'las cały Lusnie zajmujących i zabierających',
                'english_now': 'occupying and taking in the whole Lusnia woodland'})
    for r in dropped:
        x = fix_of.get(id(r))
        item = {'importance': GRADE[r['weight']], 'kind': 'dropped phrase', 'where': where(r['page']),
                'what': D.html.unescape(D.note(r['note'])), 'was': r['old'], 'now': r['new']}
        if x is None:
            item['english_now'] = 'The English already had it. Not changed.'
        elif x[3].startswith('a paragraph'):
            item['english_was'] = '(the English had no paragraph for this passage)'
            item['english_now'] = x[1].split('\n\n')[2]
        else:
            item['english_was'], item['english_now'] = x[0], x[1]
        out.append(item)
    for r in F.ROWS:
        if r['kind'] == 'misread' and r['weight'] == 'court':
            out.append({'importance': 'significant', 'kind': 'misread word in a ruling', 'where': where(r['page']),
                        'what': D.html.unescape(D.note(r['note'])), 'was': r['old'], 'now': r['new']})
    for old, new, lf, why in en_other:
        out.append({'importance': 'fact', 'kind': 'English changed', 'where': 'leaf ' + lf, 'what': why,
                    'english_was': old, 'english_now': new})
    doc = {'unit': 'APP 53/17/0/-/Konin Gr.145: the boundary decree of 1775', 'changes': out}
    head = ('# Made by changes_from_check.py from the record of the full check. Do not edit by hand.\n'
            '# importance: significant | fact | wording.\n\n')
    with io.open(os.path.join(HERE, 'changes.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(head)
        yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, width=110)
    print('wrote changes.yml:', len(out), 'entries')


if __name__ == '__main__':
    main()
