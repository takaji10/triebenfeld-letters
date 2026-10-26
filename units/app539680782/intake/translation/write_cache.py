# -*- coding: utf-8 -*-
"""Write the in-session English of APP 53/968/0/-/782 into the translation cache.

    python units/app539680782/intake/translation/write_cache.py [1,2,...]

The document was translated in a Claude Code session (2026-10-25) under the
rules translate.py gives its translator: its system prompt, termbase and
canonical names, generated for this unit, and the editor's word that no paid
run be spent on a single two-page document. The contract keeps every name and
place as written (the translation_note's rule); the money and measure
abbreviations follow the edition's standing forms (gr. and gl. after a figure
render Groschen by reference/english_forms.yml - see NEEDS_CONFIRMATION on
whether "6 gl." is gulden in this document); the garbled stretches are kept or
bracketed, never guessed. doc1.yml holds the pages in the shape of the
submit_translation tool. This writes them with translate.py's own save(), so
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
sys.argv = ['translate.py', '--unit', 'app539680782']
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
