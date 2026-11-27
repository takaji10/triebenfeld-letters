# -*- coding: utf-8 -*-
"""Set a translation cache record's English from the published site file, before an edit is republished.

    python pipeline/translate/cache_from_site.py <uid> [<uid> ...] [--head]

Why: the faithfulness review of 2026-11-04 corrected the English in the cache and in
site/_data/translations/, not in the holdings' intake/translation/doc<N>.yml nor in the court books'
holding.py FIXES. Saving the cache again from doc<N>.yml (write_cache.py, courtbook.save_cache,
holding.py --cache) and republishing quietly undoes those corrections (WORKING_NOTES, "Republishing
English after the faithfulness review"). So: save the cache (it carries the current source_hash), run
this to put the live English back into it (--head takes the file as committed, not as in the working
tree), apply the new edits to the cache's pages, then check_translations.py and publish_translations.py,
and read `git diff --word-diff` of the site file: it must show the new edits and nothing else.

<uid> is the site file's name, e.g. app53170koningr118-014. The cache is cache/translation-raw/<uid>.json
(or translation-raw-v2/ for the units bound to the v2 tag).
"""
import io
import json
import os
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = sys.argv[1:]
    head = '--head' in args
    uids = [a for a in args if not a.startswith('--')]
    for uid in uids:
        rel = 'site/_data/translations/%s.yml' % uid
        if head:
            text = subprocess.run(['git', 'show', 'HEAD:' + rel], cwd=ROOT, capture_output=True, text=True,
                                  encoding='utf-8', check=True).stdout
        else:
            text = io.open(os.path.join(ROOT, rel), encoding='utf-8').read()
        segs = yaml.safe_load(text)['segments']
        for d in ('translation-raw', 'translation-raw-v2'):
            cp = os.path.join(ROOT, 'cache', d, uid + '.json')
            if os.path.exists(cp):
                break
        else:
            sys.exit('%s: no cache record (an in-session holding without one: fix the site file directly)' % uid)
        rec = json.load(io.open(cp, encoding='utf-8'))
        assert len(rec['pages']) == len(segs), '%s: %d cached pages, %d on the site' % (uid, len(rec['pages']), len(segs))
        n = 0
        for p, s in zip(rec['pages'], segs):
            if p['en'] != s['en']:
                p['en'] = s['en']
                n += 1
        io.open(cp, 'w', encoding='utf-8', newline='\n').write(json.dumps(rec, ensure_ascii=False, indent=1))
        print('%s: %d page(s) taken from the site' % (uid, n))


if __name__ == '__main__':
    main()
