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
    spath = os.path.join(OCR, 'structure4.json')
    if not os.path.isfile(spath):
        spath = os.path.join(OCR, 'structure2.json')
    if not os.path.isfile(spath):
        spath = os.path.join(OCR, 'structure.json')
    struct = json.load(open(spath, encoding='utf-8'))
    markers = json.load(open(os.path.join(OCR, 'markers.json'),
                             encoding='utf-8'))
    # the pct/fraction resolutions (pct_frac.py): a box-addressed token
    # replacement, via the page TSV's word at that box
    fixes = {}
    pf = os.path.join(OCR, 'pct_frac.json')
    if os.path.isfile(pf):
        for k, v in json.load(open(pf, encoding='utf-8')).items():
            if not v.get('resolved') or v.get('print') in (None, 'MARKER'):
                continue
            scan, l, t = k.split('_')
            fixes.setdefault(scan, []).append((int(l), int(t), v['print']))
    out = {}
    for n, page in struct.items():
        note_top = min((x['top'] for x in page['notes']), default=None)
        # markers ride body lines; match by PROXIMITY (the markers' tops
        # come from the v1 lineation, the lines from the rebuilt one -
        # exact equality survived only by coincidence, which had
        # collapsed label placement to 45). Note-region marker
        # candidates (the notes' own leading digits) are not body
        # markers.
        marks_all = [mk for mk in markers.get(n, [])
                     if note_top is None or mk['top'] < note_top - 40]
        marks_by_top = {}
        for mk in marks_all:
            # the closest rebuilt line above/at the marker's top
            best = None
            bd = 10 ** 9
            for ln in page['lines']:
                if ln['top'] >= note_top:
                    continue
                d = abs(ln['top'] - mk['top'])
                if d < bd:
                    bd, best = d, ln
            if best is not None and bd <= 60:
                marks_by_top.setdefault(best['top'], []).append(mk)
        # this page's fix tokens: (left, top) -> print form; the
        # affected line is the TSV word's own line (top within 30)
        fix_by_linetop = {}
        if n in fixes:
            d = json.load(open(os.path.join(OCR, n + '.json'),
                               encoding='utf-8'))
            for x in d['words']:
                for (l, t, pr) in fixes[n]:
                    if x[0] == l and x[1] == t:
                        lt = None
                        for top in {w[1] for w in d['words']
                                    if w[5].strip()}:
                            if abs(top - t) < 30 and (lt is None
                                                      or abs(top - t)
                                                      < abs(lt - t)):
                                lt = top
                        if lt is not None:
                            fix_by_linetop.setdefault(lt, []).append(
                                (x[5].strip(), pr))
        lines = []
        for ln in page['lines']:
            if note_top is not None and ln['top'] >= note_top:
                continue
            t = ln['text'].strip()
            # drop the running head (a lone page number)
            if re.fullmatch(r'[\d.,IVX]{1,5}[.,]?', t):
                continue
            for (old, pr) in fix_by_linetop.get(ln['top'], []):
                if old in t:
                    t = t.replace(old, pr, 1)
            marks = marks_by_top.get(ln['top'], [])
            t2 = insert_marks(t, marks)
            lines.append({'top': ln['top'], 'left': ln.get('left'),
                          'text': t2})
        out[n] = {'lines': lines}
    with open(os.path.join(OCR, 'marked_lines.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    placed = sum(len(v) for v in markers.values())
    print('pages:', len(out), 'labels placed:', placed,
          'pct fixes:', sum(len(v) for v in fixes.values()))


if __name__ == '__main__':
    main()
