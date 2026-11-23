# -*- coding: utf-8 -*-
"""Undo a restamp that hid an older change (2026-11-23).

    python pipeline/review/date_order_unstamp.py --unit oe1bu9454 --letters 1,2,3 --rev <commit>

For each letter: the cached translation's source_hash is set to the hash of the
German as it stood at <commit> (before the move), so translate.py --stale lists
the letter again for the change it was listed for before; the move itself
(which changed no word) is not what it reports. Use only for letters that were
on the stale list before the move.
"""
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
import unitlib  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    slug = unitlib.unit_arg()
    unit = unitlib.one_unit(slug)
    letters = sys.argv[sys.argv.index('--letters') + 1].split(',')
    rev = sys.argv[sys.argv.index('--rev') + 1]
    saved = sys.argv[:]
    sys.argv = ['translate.py', '--unit', slug]
    sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'translate'))
    import translate
    sys.argv = saved
    old = json.loads(subprocess.run(['git', 'show', '%s:dataset/units/%s/letters.json' % (rev, slug)],
                                    cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout)
    old = {str(r['letter_id']): r for r in old}
    tag = str(unit.get('published_tag') or '') or None
    n = 0
    for lid in letters:
        p = translate.out_path(lid, tag)
        d = json.load(io.open(p, encoding='utf-8'))
        d['source_hash'] = translate.source_hash(old[lid])
        d['source_note'] = ('2026-11-23: on the stale list before the date was moved; the hash is that of the '
                            'German before the move (%s), so the older change stays listed' % rev)
        with io.open(p, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        n += 1
    print('%d letter(s) set back to stale' % n)


if __name__ == '__main__':
    main()
