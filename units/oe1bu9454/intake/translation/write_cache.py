# -*- coding: utf-8 -*-
"""Write the in-session English of single letters of Oe 1 Bü 9454 into the translation cache.

    python units/oe1bu9454/intake/translation/write_cache.py 245,289

Letters 245 and 289 were given new scans and a corrected text on 2026-10-07
(intake/scripts/rescan_245_289.py). Their English, from the paid run of this
holding, was revised in a Claude Code session to follow the corrected German;
each doc<N>.yml beside this file holds the pages in the shape of the
submit_translation tool. This writes them with translate.py's own save(),
into the holding's published generation of the cache (tag v2), so the record
carries the source_hash of the text as it now stands; check_translations.py
and publish_translations.py (both with --tag v2) read it from there. cache/
is not in the repository: these files are the record.
"""
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
TAG = 'v2'
os.chdir(ROOT)
want = sys.argv[1].split(',') if len(sys.argv) > 1 else sys.exit('name the letters, e.g. 245,289')
sys.argv = ['translate.py', '--unit', 'oe1bu9454']
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'translate'))
import translate as T  # noqa: E402

recs = {str(r['letter_id']): r for r in T.load_letters()}
for lid in want:
    p = os.path.join(HERE, f'doc{lid}.yml')
    payload = yaml.safe_load(open(p, encoding='utf-8'))
    n = len(payload['pages'])
    if n != len(recs[lid]['pages']):
        raise SystemExit(f"letter {lid}: {n} pages, the corpus has {len(recs[lid]['pages'])}")
    T.save(recs[lid], payload, {'input': 0, 'output': 0}, TAG, {'model': 'claude-code-session'})
    print(f'wrote {T.out_path(lid, TAG)} ({n} pages)')
