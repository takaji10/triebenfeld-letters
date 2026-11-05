# -*- coding: utf-8 -*-
"""Paragraph assembly for tom5's body text (the compose step's core).

The literature's original.md is flowing prose (the Lukasiewicz 1997
precedent): the print's line breaks are removed, hyphenated words joined
('wojewódz-' + 'twa' -> 'województwa'), paragraphs kept as the print has
them. A new paragraph starts where the print indents: the line's first
word sits right of the column's left edge by roughly an indent, and the
vertical gap above it is larger than the line pitch.

Inputs: the per-page JSONs (TSV words for geometry), structure.json for
the line/note split. Output (test mode): the assembled paragraphs of the
pages named on the command line, printed for inspection.
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'


def page_lines(n):
    """Lines with x-geometry: [(top, left0, text)] from the TSV, reading
    order; the running head dropped; the footnote block excluded."""
    d = json.load(open(os.path.join(OCR, n + '.json'), encoding='utf-8'))
    ws = [(x[1], x[0], x[5].strip()) for x in d['words'] if x[5].strip()]
    ws.sort()
    lines = []
    for top, left, word in ws:
        if lines and abs(lines[-1][0] - top) < 30:
            lines[-1][2].append((left, word))
            lines[-1][3] = max(lines[-1][3], left)
        else:
            lines.append([top, left, [(left, word)], left])
    out = []
    for top, l0, parts, lmax in lines:
        parts.sort()
        out.append({'top': top, 'left': l0, 'right': lmax,
                    'text': ' '.join(w for _, w in parts)})
    return out


def assemble(n):
    """The page's body paragraphs: dehyphenated, indent-detected."""
    lines = page_lines(n)
    if not lines:
        return []
    body = list(lines)
    # the running head: drop leading lines that are only a page number
    while body and re.fullmatch(r'[\d.,IVX]{1,5}[.,]?', body[0]['text'].strip()):
        body.pop(0)
    # column geometry: the modal left edge and the line pitch
    lefts = sorted(l['left'] for l in body)
    col_left = lefts[len(lefts) // 3]
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
            prev_end = prev['text'].rstrip()[-1:] if prev['text'].strip() else ''
            # a new paragraph: the print indents its first line (~40-60px),
            # the previous line does not hyphenate into it, and a sentence
            # boundary (or a capital opening) agrees
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
    # dehyphenate and join
    out = []
    for p in paras:
        words = []
        for i, l in enumerate(p):
            t = l['text'].strip()
            if i > 0 and words and words[-1].endswith('-'):
                # join the hyphenated word with the line's first word
                first, _, rest = t.partition(' ')
                words[-1] = words[-1][:-1] + first
                words.extend(rest.split() if rest else [])
            else:
                words.extend(t.split())
        out.append(' '.join(words))
    return out


def main():
    for n in sys.argv[1:]:
        print(f'===== {n} =====')
        for p in assemble(n):
            print()
            print(p)


if __name__ == '__main__':
    main()
