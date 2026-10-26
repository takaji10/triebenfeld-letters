# -*- coding: utf-8 -*-
"""Write the in-session English of APP 53/4/0/-/62 into the translation cache.

    python units/app534062/intake/translation/write_cache.py [1,2,...]

The document was translated in a Claude Code session (2026-10-26) under the
rules translate.py gives its translator: its system prompt, termbase and
canonical names, generated for this unit, and the editor's word that no paid
run be spent on a single-page document (the path of app539680782). The
translation keeps the entry's order and its doubtful words bracketed, never
guessed; the names follow the edition's rule that the English uses the Polish
form of a person's name (Sebastianus -> Sebastian) and the place its
canonical form (Szetlewo -> Szetlew). doc1.yml holds the page in the shape of
the submit_translation tool. This writes it with translate.py's own save(), so
the cache record carries the source_hash of the text translated, exactly as a
paid run would; check_translations.py and publish_translations.py read it from
there. cache/ is not in the repository: this file is the record.
"""
import os, sys
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
os.chdir(ROOT)
want = sys.argv[1].split(',') if len(sys.argv) > 1 else None
sys.argv = ['translate.py', '--unit', 'app534062']
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
