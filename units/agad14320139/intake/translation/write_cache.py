# -*- coding: utf-8 -*-
"""Write the in-session English of AGAD 1/432/0/1/139 into the translation cache.

    python units/agad14320139/intake/translation/write_cache.py [1,2]

Translated in a Claude Code session (2026-11-11) under translate.py's rules,
no paid run; build_docs.py makes doc1.yml and doc2.yml (every lost stretch
"[text lost]", nothing completed, the reconstruction layer never used). This
writes them with translate.py's own save(), so the cache record carries the
source_hash of the German translated, as a paid run's would.
"""
import os, sys
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
os.chdir(ROOT)
want = sys.argv[1].split(',') if len(sys.argv) > 1 else None
sys.argv = ['translate.py', '--unit', 'agad14320139']
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'translate'))
import translate as T

recs = {str(r['letter_id']): r for r in T.load_letters()}
for lid in sorted(recs, key=int):
    if want and lid not in want:
        continue
    p = os.path.join(HERE, f'doc{lid}.yml')
    if not os.path.isfile(p):
        continue
    payload = yaml.safe_load(open(p, encoding='utf-8'))
    n = len(payload['pages'])
    if n != len(recs[lid]['pages']):
        raise SystemExit(f'document {lid}: {n} pages, the corpus has '
                         f"{len(recs[lid]['pages'])}")
    T.save(recs[lid], payload, {'input': 0, 'output': 0}, None,
           {'model': 'claude-code-session'})
    print(f'wrote {T.out_path(lid)} ({n} pages)')
