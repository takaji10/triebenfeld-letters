# -*- coding: utf-8 -*-
"""Write the editor's English of APP 53/6/0/-/36 into the translation cache.

    python units/app536036/intake/translation/write_cache.py

The English is the editor's own translation, made before the holding came into
the edition; build_docs.py beside this file cut it to the edition's pages
(doc<N>.yml, in the shape of translate.py's submit_translation tool). This
writes it with translate.py's own save(), so the cache record carries the
source_hash of the Latin it belongs to; check_translations.py and
publish_translations.py read it from there. cache/ is not in the repository:
doc<N>.yml and build_docs.py are the record.
"""
import os, sys
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
os.chdir(ROOT)
want = sys.argv[1].split(',') if len(sys.argv) > 1 else None
sys.argv = ['translate.py', '--unit', 'app536036']
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
           {'model': 'editor'})
    print(f'wrote {T.out_path(lid)} ({n} pages)')
