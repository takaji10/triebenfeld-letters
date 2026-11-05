# -*- coding: utf-8 -*-
"""Apply the reconstructed footnote markers to the body paragraphs.

Input: markers.json (markers2.py), the paragraphs (paragraphs.assemble),
the notes (structure.json). For each page, the markers in reading order
are inserted into the paragraph text after the token they ride ('after'
token = the word the superscript follows), as [^<page>-<n>] labels.

The 'after' token is matched by occurrence counting (the tok may recur);
the marker lands right after that occurrence. Tokens like 'Ujskich1'
carry the marker INSIDE them - the trailing digits are stripped when a
marker rides them ('Ujskich1' -> 'Ujskich[^p-1]').

Output: marked_text.json: per page, the paragraphs with labels inserted.
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'


def strip_tail(tok):
    """The token without its marker tail, if it has one."""
    m = re.match(r'^(?P<base>[^\W\d_][\wąćęłńóśźż.\-]*?)[*?]*\d{1,2}[*?]?'
                 r'[.,;:»”"]?$', tok, re.UNICODE)
    return m.group('base') if m else tok


def apply(paras, marks):
    """Insert the labels into the paragraphs at their tokens."""
    if not marks:
        return paras
    # flatten the paragraphs to tokens with a map back
    out = []
    seq = []          # (para_idx, word_idx, tok)
    for pi, p in enumerate(paras):
        words = p.split(' ')
        for wi, w in enumerate(words):
            seq.append((pi, wi, w))
    used = set()
    for mk in marks:
        tok = mk['after']
        want = strip_tail(tok)
        # find the nth unused occurrence of this token (or its
        # stripped form) at or after the marker's line
        hits = [i for i, (pi, wi, w) in enumerate(seq)
                if (w == tok or w.rstrip('.,;:!?') == tok
                    or strip_tail(w) == want) and i not in used]
        if not hits:
            continue
        i = hits[0]
        used.add(i)
        pi, wi, w = seq[i]
        repl = want + f"[^{mk['label']}]" + \
            (w[len(want):] if w.startswith(want) and len(w) > len(want)
             else '')
        # keep any punctuation the token carried after the stripped base
        tail = w[len(want):]
        repl = want + f"[^{mk['label']}]{tail}"
        seq[i] = (pi, wi, repl)
    # rebuild
    new = [list(p.split(' ')) for p in paras]
    for pi, wi, w in seq:
        new[pi][wi] = w
    return [' '.join(ws) for ws in new]


def main():
    markers = json.load(open(os.path.join(OCR, 'markers.json'),
                             encoding='utf-8'))
    struct = json.load(open(os.path.join(OCR, 'structure.json'),
                            encoding='utf-8'))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from paragraphs import assemble
    out = {}
    for n, marks in markers.items():
        paras = assemble(n)
        out[n] = apply(paras, marks)
        if marks:
            print(n, 'markers:', len(marks), '->',
                  sum(p.count('[^') for p in out[n]))
    with open(os.path.join(OCR, 'marked_text.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)


if __name__ == '__main__':
    main()
