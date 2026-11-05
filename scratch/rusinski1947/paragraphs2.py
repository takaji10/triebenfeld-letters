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
    # geometry from the lines themselves (the rebuilt lineation's own
    # 'left'): the old paragraphs.page_lines table had the v1 tops, and
    # filtering the rebuilt lines by those keys dropped most of the
    # body (the 415k -> 137k collapse)
    kept = [l for l in lines if l.get('left') is not None]
    if not kept:
        return []
    lefts = sorted(l['left'] for l in kept)
    col_left = lefts[len(lefts) // 3]
    body = kept
    tops = [l['top'] for l in body]
    pitch = min(b - a for a, b in zip(tops, tops[1:]) if b - a > 20) \
        if len(tops) > 1 else 90
    paras = []
    cur = []
    prev = None
    for l in body:
        newpar = False
        if prev is not None:
            gap = l['top'] - prev['top']
            indent = l['left'] - col_left
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
                # carry any label parked on the hyphen fragment, join
                # the fragment with the next line's first word - the
                # joined word REPLACES the fragment (appending kept both
                # 'zna-' and 'znanej' in the text)
                frag = words[-1]
                m = LABEL.search(frag)
                label = m.group(0) if m else ''
                base = LABEL.sub('', frag)
                first, _, rest = t.partition(' ')
                joined = base[:-1] + first
                words[-1] = joined + label
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
