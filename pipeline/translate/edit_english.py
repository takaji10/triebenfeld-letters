# -*- coding: utf-8 -*-
"""Edit the published English of documents, on top of the live text, and republish.

    python pipeline/translate/edit_english.py <edits.json>            # check: shows what would change
    python pipeline/translate/edit_english.py <edits.json> --write    # cache, check, publish

<edits.json>: {"<uid>": [["old words", "new words"], ...], ...}, uid as the site file is named
(app53170koningr121-001). Each old must stand exactly once in the document's English; it is matched
across line wraps (any run of white space), and the new words go in with single spaces.

The base is site/_data/translations/<uid>.yml as committed (HEAD), never the holding's doc<N>.yml:
the faithfulness review of 2026-11-04 corrected the English in the cache and the site only, and a
republish from doc<N>.yml undoes it (WORKING_NOTES, "Republishing English after the faithfulness
review"). The cache record is written with the current source hash (the corrected transcription), then
check_translations.py and publish_translations.py run for each holding touched. Afterwards read
`git diff --word-diff` of the site files: the edits and nothing else. The holding's doc<N>.yml or
holding.py FIXES are not changed: record the edit in the holding's notes.
"""
import io
import json
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def apply(texts, edits, uid):
    bad = []
    for old, new in edits:
        pat = r'\s+'.join(re.escape(w) for w in old.split())
        hits = [(i, len(re.findall(pat, t))) for i, t in enumerate(texts) if re.search(pat, t)]
        if len(hits) != 1 or hits[0][1] != 1:
            bad.append('%s: %d page(s) with %r' % (uid, len(hits), old[:70]))
            continue
        i = hits[0][0]
        nn = ' '.join(new.split())
        texts[i] = re.sub(pat, lambda m: nn, texts[i])
    return bad


def main():
    path = sys.argv[1]
    write = '--write' in sys.argv
    only = sys.argv[sys.argv.index('--slug') + 1] if '--slug' in sys.argv else None
    if not only:
        sys.stdout.reconfigure(encoding='utf-8')
    edits = json.load(io.open(path, encoding='utf-8'))
    if only:
        edits = {u: e for u, e in edits.items() if u.rsplit('-', 1)[0] == only}
    os.chdir(ROOT)
    sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'translate'))
    bad, plan = [], {}
    for uid, ed in edits.items():
        rel = 'site/_data/translations/%s.yml' % uid
        head = subprocess.run(['git', 'show', 'HEAD:' + rel], capture_output=True, text=True, encoding='utf-8', check=True)
        segs = yaml.safe_load(head.stdout)['segments']
        texts = [s['en'] for s in segs]
        bad += apply(texts, ed, uid)
        plan[uid] = texts
    for b in bad:
        print('NOT FOUND ONCE:', b)
    print('%d document(s), %d edit(s), %d not applied' % (len(edits), sum(len(v) for v in edits.values()), len(bad)))
    if bad or not write:
        return
    units = sorted({uid.rsplit('-', 1)[0] for uid in plan})
    if not only:                      # one process per holding: translate.py rewraps stdout on import
        for slug in units:
            subprocess.run([sys.executable, os.path.abspath(__file__), path, '--write', '--slug', slug], check=True,
                           env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        return
    for slug in units:
        argv, sys.argv = sys.argv, ['translate.py', '--unit', slug]
        import translate as T
        sys.argv = argv
        recs = {str(r['letter_id']): r for r in T.load_letters()}
        for uid, texts in plan.items():
            if uid.rsplit('-', 1)[0] != slug:
                continue
            letter = str(int(uid.rsplit('-', 1)[1]))
            rec = recs[letter]
            cp = None
            for d in ('translation-raw', 'translation-raw-v2'):
                p = os.path.join(ROOT, 'cache', d, uid + '.json')
                if os.path.exists(p):
                    cp = p
                    break
            if cp:
                out = json.load(io.open(cp, encoding='utf-8'))
                assert len(out['pages']) == len(texts), uid
                for pg, t in zip(out['pages'], texts):
                    pg['en'] = t
                out['source_hash'] = T.source_hash(rec)
                io.open(cp, 'w', encoding='utf-8', newline='\n').write(json.dumps(out, ensure_ascii=False, indent=1))
            else:
                T.save(rec, {'pages': [{'page': i + 1, 'confidence': 'high', 'marker_count': 0, 'en': t}
                                       for i, t in enumerate(texts)]},
                       {'input': 0, 'output': 0}, None, {'model': 'editor'})
            print('cached', uid)
        subprocess.run([sys.executable, 'pipeline/translate/check_translations.py', '--unit', slug],
                       stdout=subprocess.DEVNULL, check=True)
        r = subprocess.run([sys.executable, 'pipeline/translate/publish_translations.py', '--unit', slug],
                           capture_output=True, text=True, encoding='utf-8')
        print(slug, (r.stdout.strip().splitlines() or [''])[-2:], r.stderr.strip()[-300:])


if __name__ == '__main__':
    main()
