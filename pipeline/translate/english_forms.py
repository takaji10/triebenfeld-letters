# -*- coding: utf-8 -*-
"""House forms for the English, from reference/english_forms.yml.

    python english_forms.py            # report what would change, write nothing
    python english_forms.py --apply    # rewrite the published English

Imported by publish_translations.py and summarise.py, which apply the rules as
they write, so a re-publish from the cache keeps them. --apply brings the files
already published into line: site/_data/translations/*.yml (the English and,
for a tabulated document, its table) and site/_data/summaries.yml.

Mechanical replacements only; see the file's header for what may go there.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import os, re, sys, argparse, collections
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_RULES = None


def rules():
    global _RULES
    if _RULES is None:
        with open(os.path.join(ROOT, 'reference', 'english_forms.yml'), encoding='utf-8') as f:
            _RULES = [dict(r, _rx=re.compile(r['pattern'])) for r in (yaml.safe_load(f) or {}).get('rules') or []]
    return _RULES


def _word_sub(word, text):
    """A replacement that writes out an abbreviation: keep a full stop only
    where it also ends the sentence."""
    def f(m):
        whole = m.group(0)
        rest = text[m.end():]
        stop = whole.endswith('.') and (not rest.strip() or re.match(r'\s*\n|\s+[A-Z]', rest))
        return m.group(1) + m.group(2) + word + ('.' if stop else '')
    return f


def apply(text, counts=None):
    """The text with every rule applied, in order. Adds to `counts` by rule id."""
    if not text:
        return text
    for r in rules():
        if 'capitalise' in r:
            w = r['capitalise']
            new, n = r['_rx'].subn(lambda m: m.group(0).replace(w, w[0].upper() + w[1:]), text)
        elif 'months' in r:
            new, n = r['_rx'].subn(lambda m: r['months'][m.group(1)], text)
        elif 'word' in r:
            new, n = r['_rx'].subn(_word_sub(r['word'], text), text)
        else:
            new, n = r['_rx'].subn(r['replace'], text)
        if n and counts is not None:
            counts[r['id']] += n
        text = new
    return text


_CORR = None


def corrections():
    global _CORR
    if _CORR is None:
        p = os.path.join(ROOT, 'reference', 'english_corrections.yml')
        _CORR = (yaml.safe_load(open(p, encoding='utf-8')) or {}).get('corrections') or [] if os.path.exists(p) else []
    return _CORR


def apply_page(pad, page, text, counts=None, problems=None):
    """The house forms, then this page's own corrections. A correction whose
    words are not on the page exactly once is not applied, and is reported."""
    text = apply(text, counts)
    for c in corrections():
        if c['pad'] != pad or str(c['page']) != str(page):
            continue
        n = text.count(c['find'])
        if n == 1:
            text = text.replace(c['find'], c['replace'])
            if counts is not None:
                counts['corrections'] += 1
        elif c['replace'] not in text and problems is not None:
            problems.append(f"{pad} p{page}: {c['find']!r} found {n} times - not applied")
    return text


def _dump(path, data):
    # exactly as publish_translations.py writes them
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=100)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    counts, files, samples, problems = collections.Counter(), 0, [], []

    tdir = os.path.join(ROOT, 'site', '_data', 'translations')
    for fn in sorted(os.listdir(tdir)):
        if not fn.endswith('.yml'):
            continue
        p = os.path.join(tdir, fn)
        d = yaml.safe_load(open(p, encoding='utf-8')) or {}
        changed = False
        for seg in d.get('segments') or []:
            for k in ('en', 'html'):
                if seg.get(k):
                    new = (apply_page(fn[:-4], seg.get('page'), seg[k], counts, problems)
                           if k == 'en' else apply(seg[k], counts))
                    if new != seg[k]:
                        if len(samples) < 12 and k == 'en':
                            i = next(i for i, (x, y) in enumerate(zip(seg[k], new)) if x != y)
                            samples.append(f'{fn[:-4]}: ...{seg[k][max(0, i-30):i+25]!r} -> {new[max(0, i-30):i+30]!r}')
                        seg[k] = new
                        changed = True
        if changed:
            files += 1
            if a.apply:
                _dump(p, d)

    sp = os.path.join(ROOT, 'site', '_data', 'summaries.yml')
    raw = open(sp, encoding='utf-8').read()
    s = yaml.safe_load(raw) or {}
    sc = collections.Counter()
    new = {k: apply(v, sc) if isinstance(v, str) else v for k, v in s.items()}
    if sum(sc.values()) and a.apply:
        # exactly as summarise.py writes it, header included
        head = ''.join(l for l in raw.splitlines(True)[:20] if l.startswith('#'))
        with open(sp, 'w', encoding='utf-8', newline='\n') as f:
            f.write(head)
            yaml.safe_dump(new, f, allow_unicode=True, sort_keys=True, width=1000,
                           default_flow_style=False)

    verb = 'changed' if a.apply else 'would change'
    print(f'translations: {verb} {files} file(s): {dict(counts)}')
    print(f'English summaries: {verb} {sum(sc.values())}: {dict(sc)}')
    for x in samples:
        print('  ', x)
    for x in problems:
        print('  !!', x)


if __name__ == '__main__':
    main()
