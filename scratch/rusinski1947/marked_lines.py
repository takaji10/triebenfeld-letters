# -*- coding: utf-8 -*-
"""Insert the reconstructed markers into the page's body LINES, then
assemble the paragraphs from the marked lines (the order that keeps the
labels: a marker riding a hyphenated line-end word travels with the
joined word).

marked_lines.json: per page {'lines': [(top, text)], 'head_tops': [...]}
- the body lines (structure.json), the running head dropped, each text
with [^<page>-<n>] labels inserted after the nth matching token.
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'


def strip_tail(tok):
    m = re.match(r'^(?P<base>[^\W\d_][\wąćęłńóśźż.\-]*?)[*?]*\d{1,2}[*?]?'
                 r'[.,;:»”"]?$', tok, re.UNICODE)
    return m.group('base') if m else None


def insert_marks(line_text, marks):
    """Insert the labels into one line. A standalone mark's digit token
    IS the superscript: it is replaced by the label. A glued mark rides
    a host word: the token's digit/artifact tail is stripped and the
    label follows the base."""
    if not marks:
        return line_text
    words = line_text.split(' ')
    out = []
    used = set()
    for w in words:
        placed = False
        for mi, mk in enumerate(marks):
            if mi in used:
                continue
            tok = mk.get('tok', '')
            kind = mk.get('kind', '')
            want = strip_tail(tok) or tok.rstrip('0123456789*?.,;:')
            base = w.rstrip('.,;:!?»”"')
            if kind == 'standalone' and w.rstrip('.,;:') == tok \
                    .rstrip('.,;:'):
                out.append(f"[^{mk['label']}]")
                used.add(mi)
                placed = True
                break
            if kind != 'standalone' and want and base == want:
                tail = w[len(base):]
                out.append(f"{want}[^{mk['label']}]{tail}")
                used.add(mi)
                placed = True
                break
            if kind != 'standalone' and tok != base and base == tok:
                # the token itself glued ('Ujskich1'): strip the tail
                out.append(f"{want}[^{mk['label']}]"
                           + w[len(base):])
                used.add(mi)
                placed = True
                break
        if not placed:
            out.append(w)
    # any unmatched markers: at the line's end, in order
    for mi, mk in enumerate(marks):
        if mi not in used:
            out.append(f"[^{mk['label']}]")
    return ' '.join(out)


def main():
    struct = json.load(open(os.path.join(OCR, 'structure.json'),
                            encoding='utf-8'))
    markers = json.load(open(os.path.join(OCR, 'markers.json'),
                             encoding='utf-8'))
    out = {}
    for n, page in struct.items():
        marks_by_top = {}
        for mk in markers.get(n, []):
            marks_by_top.setdefault(mk['top'], []).append(mk)
        lines = []
        note_top = min((x['top'] for x in page['notes']), default=None)
        for ln in page['lines']:
            if note_top is not None and ln['top'] >= note_top:
                continue
            t = ln['text'].strip()
            # drop the running head (a lone page number)
            if re.fullmatch(r'[\d.,IVX]{1,5}[.,]?', t):
                continue
            marks = marks_by_top.get(ln['top'], [])
            t2 = insert_marks(t, marks)
            lines.append({'top': ln['top'], 'text': t2})
        out[n] = {'lines': lines}
    with open(os.path.join(OCR, 'marked_lines.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    placed = sum(len(v) for v in markers.values())
    print('pages:', len(out), 'labels placed:', placed)


if __name__ == '__main__':
    main()
