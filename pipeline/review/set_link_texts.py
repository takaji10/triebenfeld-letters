"""Write new sentences into literature/links.yml (the voice review,
docs/VOICE_REVIEW_PLAN.md): for each link id in the batch file, its `en` and
`de` (either), replacing the link's own folded block. The old sentences stay
in git.

Usage: python pipeline/review/set_link_texts.py <batch.yml> [--dry]
"""
import os, re, sys, textwrap
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, 'literature', 'links.yml')


def main():
    batch = yaml.safe_load(open(sys.argv[1], encoding='utf-8'))
    lines = open(P, encoding='utf-8', newline='').read().split('\n')
    done = set()
    i, cur = 0, None
    while i < len(lines):
        m = re.match(r'^- id: (\S+)', lines[i])
        if m:
            cur = m.group(1)
        m = re.match(r'^  (en|de): ', lines[i])
        if m and cur in batch and batch[cur].get(m.group(1)):
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or lines[j].startswith('    ')):
                j += 1
            while j > i + 1 and not lines[j - 1].strip():
                j -= 1
            body = textwrap.wrap(' '.join(batch[cur][m.group(1)].split()), 76,
                                 break_long_words=False, break_on_hyphens=False)
            lines[i:j] = [f'  {m.group(1)}: >-'] + ['    ' + b for b in body]
            done.add((cur, m.group(1)))
            i += len(body) + 1
            continue
        i += 1
    want = {(k, l) for k, v in batch.items() for l in ('en', 'de') if v.get(l)}
    if want - done:
        raise SystemExit(f'not found: {sorted(want - done)}')
    text = '\n'.join(lines)
    yaml.safe_load(text)
    if '--dry' not in sys.argv:
        open(P, 'w', encoding='utf-8', newline='').write(text)
    print(len(done), 'sentences set')


if __name__ == '__main__':
    main()
