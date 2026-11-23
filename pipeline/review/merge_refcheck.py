# -*- coding: utf-8 -*-
"""Check every changed line of the shared files (registers, era pages, timeline,
other holdings' descriptions) against the merge maps (docs/DOCUMENT_MERGE_PLAN.md).

    python pipeline/review/merge_refcheck.py --units a,b,c [--rev HEAD]

For each changed line: the old line's document addresses and keys, mapped through
the maps, must be the new line's (a key named twice in a list kept once), and
the rest of the line must be the same apart from a link's shown number.
"""
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    units = sys.argv[sys.argv.index('--units') + 1].split(',')
    rev = sys.argv[sys.argv.index('--rev') + 1] if '--rev' in sys.argv else 'HEAD'
    maps = {u: json.load(io.open(os.path.join(ROOT, 'units', u, 'intake', 'merge_map.json'),
                                 encoding='utf-8'))['idmap'] for u in units}
    changed = subprocess.run(['git', 'diff', '--name-only', rev, '--'], cwd=ROOT, capture_output=True,
                             text=True, encoding='utf-8').stdout.split()
    files = [f for f in changed if (f.startswith(('reference/', 'site/eras/', 'site/de/epochen/', 'literature/',
                                                   'newspapers/', 'places/')) or f == 'site/_data/timeline.yml'
                                    or (f.startswith('units/') and f.endswith(('about.md', 'about_de.md'))))
             and not f.endswith('english_corrections.yml')]
    alt = '|'.join(re.escape(u) for u in units)
    addr = re.compile(r'/documents/(%s)/(\w+)/' % alt)
    keyp = re.compile(r'(?<![\w/-])(%s)-(\w+)\b' % alt)
    bad = n = 0
    for f in files:
        old = subprocess.run(['git', 'show', '%s:%s' % (rev, f)], cwd=ROOT, capture_output=True, text=True,
                             encoding='utf-8').stdout.split('\n')
        new = io.open(os.path.join(ROOT, f), encoding='utf-8').read().split('\n')
        if len(old) != len(new):
            print('!! %s: the number of lines changed' % f)
            bad += 1
            continue
        for a, b in zip(old, new):
            if a == b:
                continue
            n += 1
            exp = [(u, maps[u].get(d, d)) for u, d in addr.findall(a)]
            got = addr.findall(b)
            ek, gk = [], [(u, d) for u, d in keyp.findall(b) if not d.startswith('0')]
            for u, d in keyp.findall(a):
                if d.startswith('0'):
                    continue
                y = (u, maps[u].get(d, d))
                if y not in ek or '[' not in a:
                    ek.append(y)
            if exp != got:
                bad += 1
                print('!! addresses %s: %s -> %s' % (f, exp, got))
            if sorted(set(ek)) != sorted(set(gk)):
                bad += 1
                print('!! keys %s: %s -> %s' % (f, ek, gk))
            ra = re.sub(r'\[(\D*)\d+\]\(', '[N](', keyp.sub('K', addr.sub('A', a)))
            rb = re.sub(r'\[(\D*)\d+\]\(', '[N](', keyp.sub('K', addr.sub('A', b)))
            ra, rb = re.sub(r'(K, )+K', 'K', ra), re.sub(r'(K, )+K', 'K', rb)
            if ra != rb:
                bad += 1
                print('!! text %s: %s' % (f, a[:120]))
    print('%d changed line(s) in %d file(s), %d problem(s)' % (n, len(files), bad))


if __name__ == '__main__':
    main()
