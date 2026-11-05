# -*- coding: utf-8 -*-
"""Paragraph assembly from the MARKED lines (marked_lines.json).

Same rules as paragraphs.py (indent + gap + sentence boundary), but the
lines carry the [^p-n] labels; a label riding a hyphenated line-end word
travels with the joined word (the label is stripped from the fragment
and re-attached to the joined result).
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
LABEL = re.compile(r'\[\^[^\]]+\]')


def assemble_marked(n):
    data = json.load(open(os.path.join(OCR, 'marked_lines.json'),
                          encoding='utf-8'))
    lines = data[n]['lines']
    if not lines:
        return []
    lefts = sorted(l['text'] and _first_x(n, l) for l in lines)
    # geometry from the unmarked TSV (paragraphs.page_lines)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from paragraphs import page_lines
    geo = {g['top']: g for g in page_lines(n)}
    body = [l for l in lines if l['top'] in geo]
    if not body:
        return []
    lefts = sorted(g['left'] for g in geo.values())
    col_left = lefts[len(lefts) // 3]
    tops = [g['top'] for g in body]
    pitch = min(b - a for a, b in zip(tops, tops[1:]) if b - a > 20) \
        if len(tops) > 1 else 90
    paras = []
    cur = []
    prev = None
    for l in body:
        g = geo[l['top']]
        newpar = False
        if prev is not None:
            gap = l['top'] - prev['top']
            indent = g['left'] - col_left
            first_char = l['text'].lstrip()[:1]
            prev_end = prev['text'].rstrip()[-1:]
            if (indent >= 40 and gap >= pitch * 1.25
                    and not prev['text'].rstrip().endswith('-')
                    and (prev_end in '.!?;:' or first_char.isupper())):
                newpar = True
        if newpar and cur:
            paras.append(cur)
            cur = []
        cur.append(l)
        prev = l
    if cur:
        paras.append(cur)
    out = []
    for p in paras:
        words = []
        for i, l in enumerate(p):
            t = l['text'].strip()
            if i > 0 and words and words[-1].endswith('-'):
                # carry any label parked on the hyphen fragment
                label = ''
                m = LABEL.search(words[-1])
                if m:
                    label = m.group(0)
                    words[-1] = words[-1].replace(label, '')
                first, _, rest = t.partition(' ')
                joined = words[-1][:-1] + first
                if label and LABEL.search(first):
                    # the next fragment carries its own label
                    words.append(joined)
                elif label:
                    words.append(joined + label)
                else:
                    words.append(joined)
                words.extend(rest.split() if rest else [])
            else:
                words.extend(t.split())
        out.append(' '.join(words))
    return out


def _first_x(n, l):
    return 0


def main():
    for n in sys.argv[1:]:
        for p in assemble_marked(n):
            print()
            print(p[:400])


if __name__ == '__main__':
    main()
