# -*- coding: utf-8 -*-
"""Collate two independent translations, and report only where they disagree
about MEANING.

    python translate.py --rerun-flagged --tag B --batch   # make the second witness
    python translate.py --collect --tag B
    python collate_translations.py                        # then compare

Structure follows collate_witnesses.py, which does the same job for the two
transcription witnesses: produce independently, compare afterwards, never merge
automatically.

Why this is scoped to flagged spans instead of the whole corpus. Two fluent
translations of the same paragraph differ almost everywhere - word order,
register, which clause leads. Diffing them wholesale would bury the handful of
real disagreements under thousands of paraphrases, and a report nobody can read
is worse than no report. So the comparison runs only where a witness already
said it was unsure, and asks a narrower question than "do these differ?":

    do the two readings fall on opposite sides of a known meaning split?

Each rare pair in translation_glossary.yml carries two keyword `poles`. If the
two witnesses land in different poles - one says "dismissal", the other says
"order to pay" - that is a real divergence and goes in the report. If they land
in the same pole, or in neither, they are two ways of saying one thing and are
discarded. The output feeds translation_review.csv as `divergence` rows.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, os, re, sys, json, argparse

import yaml
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'review', 'translation_divergence.json')
REPORT = os.path.join(ROOT, 'review', 'translation_divergence.md')


def pole_of(text, poles):
    """Which side of the split this English lands on, or None if neither."""
    t = (text or '').lower()
    hits = {name: sum(1 for w in words if w.lower() in t)
            for name, words in poles.items()}
    best = max(hits, key=hits.get) if hits else None
    return best if best and hits[best] > 0 else None


def norm(s):
    return re.sub(r'\W+', ' ', (s or '')).strip().lower()


def overlap(a, b):
    """Do two German spans refer to the same place in the text?"""
    wa, wb = set(norm(a).split()), set(norm(b).split())
    if not wa or not wb:
        return False
    return len(wa & wb) / min(len(wa), len(wb)) >= 0.5


def load_witness(tag):
    """Load a witness, skipping any letter whose result came back malformed.

    A batch occasionally returns a tool input whose `pages` is a truncated JSON
    string rather than an array. One unusable file should not stop the
    comparison of the other twenty-five, so it is reported and skipped."""
    d = os.path.join(ROOT, 'cache', 'translation-raw' + (f'-{tag}' if tag else ''))
    out, skipped = {}, []
    if not os.path.isdir(d):
        return out
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.json') or fn.startswith('_'):
            continue
        rec = json.load(open(os.path.join(d, fn), encoding='utf-8'))
        pages = rec.get('pages')
        if not isinstance(pages, list) or not all(isinstance(p, dict) for p in pages):
            skipped.append(str(rec.get('letter')))
            continue
        out[str(rec.get('letter'))] = rec
    if skipped:
        print(f'  skipped {len(skipped)} malformed witness file(s): '
              + ', '.join('L' + x for x in skipped))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--a', default=None, help='tag of the first witness (default: none)')
    ap.add_argument('--b', default='B', help='tag of the second witness')
    args = ap.parse_args()

    A, B = load_witness(args.a), load_witness(args.b)
    if not B:
        sys.exit(f'no second witness - run: python translate.py --rerun-flagged '
                 f'--tag {args.b}')
    glossary = yaml.safe_load(open(os.path.join(ROOT, 'reference', 'translation_glossary.yml'),
                                   encoding='utf-8'))
    pairs = glossary['rare_pairs']

    rows, compared, same_pole, no_pole = [], 0, 0, 0
    for lid, b in B.items():
        a = A.get(lid)
        if not a:
            continue
        bp = {p.get('page'): p for p in b.get('pages', [])}
        for pa in a.get('pages', []):
            pb = bp.get(pa.get('page'))
            if not pb:
                continue
            for fa in pa.get('flagged') or []:
                fb = next((x for x in (pb.get('flagged') or [])
                           if overlap(fa.get('de'), x.get('de'))), None)
                if not fb:
                    continue
                compared += 1
                # which split, if any, does this span sit on?
                poles = None
                for e in pairs:
                    if re.search(e['pattern'], fa.get('de') or '', re.I):
                        poles = e['poles']
                        break
                if not poles:
                    continue
                ra, rb = pole_of(fa.get('rendered_as'), poles), \
                    pole_of(fb.get('rendered_as'), poles)
                if ra is None or rb is None:
                    no_pole += 1
                    continue
                if ra == rb:
                    same_pole += 1
                    continue
                rows.append({
                    'letter': lid, 'pad': a.get('pad', lid), 'page': pa.get('page'),
                    'kind': 'divergence',
                    'german': (fa.get('de') or '')[:90],
                    'english': f"A: {(fa.get('rendered_as') or '')[:60]}",
                    'note': f"B: {(fb.get('rendered_as') or '')[:60]} | the two "
                            f"witnesses read this on opposite sides of the split "
                            f"({ra} vs {rb})",
                })

    json.dump(rows, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    lines = ['# Translation divergence report', '',
             f'{len(B)} letter(s) have a second witness. {compared} flagged span(s) '
             f'appear in both.', '',
             f'- **{len(rows)}** disagree about meaning and are listed below',
             f'- {same_pole} agree on meaning despite differing wording',
             f'- {no_pole} could not be placed on either side of the split', '']
    if rows:
        lines += ['| letter | page | German | witness A | witness B |', '|---|---|---|---|---|']
        for r in rows:
            b_txt = r['note'].split(' | ')[0][3:]
            lines.append(f"| L{r['letter']} | {r['page']} | {r['german'][:50]} | "
                         f"{r['english'][3:][:50]} | {b_txt[:50]} |")
    else:
        lines.append('No meaning-level disagreements found.')
    lines += ['', 'Wording differences are deliberately not reported: two fluent '
                  'translations differ almost everywhere, and listing that would bury '
                  'the real disagreements.', '']
    open(REPORT, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')

    print(f'{compared} flagged span(s) in both witnesses')
    print(f'  {len(rows)} meaning-level divergence(s)')
    print(f'  {same_pole} agree on meaning, {no_pole} unplaceable')
    print(f'\nwrote {OUT}\nwrote {REPORT}')
    print('re-run check_translations.py to fold these into translation_review.csv')


if __name__ == '__main__':
    main()
