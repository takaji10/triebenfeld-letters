"""Write new accounts and briefs into literature/<slug>/work.yml, and keep what
they drop in the work's notes.md (the voice review, docs/VOICE_REVIEW_PLAN.md).

The texts come from a batch file (YAML): for each slug, account_en,
account_de, brief_en, brief_de (any of them), and `why`, the sentences of the
old account that said why the work is on the site - the editor's ruling of
2026-10-29: that reasoning belongs in the notes, not on the page. `why` is
appended to notes.md under "## Why it is here", with the date; the old
account itself stays in git.

Usage: python pipeline/review/set_work_texts.py <batch.yml> [--dry] [--newspapers]
(--newspapers: the slugs are items of newspapers/, item.yml)
"""
import os, re, sys, textwrap
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KEYS = ('account_en', 'account_de', 'brief_en', 'brief_de')


def set_block(text, key, value):
    """Replace the top-level `key:` of a YAML text with a folded block."""
    lines = text.split('\n')
    for i, ln in enumerate(lines):
        if re.match(rf'^{key}:', ln):
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or lines[j].startswith((' ', '\t'))):
                j += 1
            while j > i + 1 and not lines[j - 1].strip():
                j -= 1
            body = textwrap.wrap(' '.join(value.split()), width=76, break_long_words=False, break_on_hyphens=False)
            lines[i:j] = [f'{key}: >-'] + ['  ' + b for b in body]
            return '\n'.join(lines)
    raise SystemExit(f'no top-level {key}:')


def main():
    batch = yaml.safe_load(open(sys.argv[1], encoding='utf-8'))
    dry = '--dry' in sys.argv
    for slug, v in batch.items():
        section, fname = ('newspapers', 'item.yml') if '--newspapers' in sys.argv else ('literature', 'work.yml')
        p = os.path.join(ROOT, section, slug, fname)
        t = open(p, encoding='utf-8', newline='').read()
        for k in KEYS:
            if v.get(k):
                t = set_block(t, k, v[k])
        yaml.safe_load(t)   # still YAML
        if not dry:
            open(p, 'w', encoding='utf-8', newline='').write(t)
        if v.get('why'):
            n = os.path.join(ROOT, section, slug, 'notes.md')
            add = ('\n## Why it is here\n\n'
                   'Kept from the work\'s account, which said it on the page until the '
                   'voice review of 2026-10-29 (the editor: the reasoning for why a work '
                   'is relevant is for the notes, not the reader):\n\n'
                   + '\n'.join('> ' + ln for ln in textwrap.wrap(' '.join(v['why'].split()), 76)) + '\n')
            if not dry:
                with open(n, 'a', encoding='utf-8', newline='\n') as f:
                    f.write(add)
        print('set', slug)


if __name__ == '__main__':
    main()
