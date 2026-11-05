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
            if mk.get('out'):
                # audit-authored replacement: the token is replaced
                # wholesale ('out' carries '{label}'); tok may match as
                # a substring (fused tokens '17732,' via '1773')
                if w == tok or (tok and tok in w):
                    out.append(mk['out'].replace('{label}',
                                                 mk['label']))
                    used.add(mi)
                    placed = True
                    break
                continue
            want = strip_tail(tok) or tok.rstrip('0123456789*?.,;:')
            base = w.rstrip('.,;:!?»”"')
            if kind == 'standalone' and w.rstrip('.,;:') == tok \
                    .rstrip('.,;:'):
                punct = w[len(w.rstrip('.,;:')):]
                if mk.get('num_ctx'):
                    # number-context placement: KEEP the digit (it may
                    # be a real number, not the marker - 'co 4
                    # tygodnie') and set the label after it
                    out.append(w + f"[^{mk['label']}]")
                else:
                    out.append(f"[^{mk['label']}]" + punct)
                used.add(mi)
                placed = True
                break
            if kind == 'artifact' and \
                    re.fullmatch(r'[*?$§£|?]+[.,;:»”"]?', w):
                # an isolated artifact glyph the models produced for the
                # print's inline marker ('*', '$', '?.', '£.') - the
                # word must BE the glyph (an untested match ate prose)
                punct = w[len(w.rstrip('.,;:')):]
                out.append(f"[^{mk['label']}]" + punct)
                used.add(mi)
                placed = True
                break
            if kind != 'standalone':
                # the print's glued marker: the structure word carries
                # the digit tail ('Maasa4', 'zezwalał1,') or lost it
                # ('osadniczej' for lp 'osadniczej1'). The word base
                # must EQUAL want - a mere prefix ('ini' vs
                # 'iniciatywy') must never match (it ate words).
                wb = re.sub(r'[\d*?]+$', '', w.rstrip('.,;:!?»”"'))
                if wb and wb != w and wb == want and \
                        re.search(r'[\d*?]', w):
                    tailp = w[len(wb):]
                    tailp = re.sub(r'^[\d*?]+', '', tailp)
                    out.append(f"{wb}[^{mk['label']}]{tailp}")
                    used.add(mi)
                    placed = True
                    break
                if wb == want and wb == w and want != tok and \
                        re.search(r'[\d*?]', tok):
                    # the structure read lost the marker digit: keep the
                    # word, append the label after it
                    out.append(f"{w}[^{mk['label']}]")
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
        tops = [x['top'] for x in page['notes'] if x['top'] is not None]
        note_top = min(tops) if tops else None
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
        # affected line = the nearest REBUILT line (within 45px) - the
        # old bucket-top lookup matched nothing after the lineation
        # change, so the 92 pct/fraction fixes silently never landed
        fix_by_linetop = {}
        if n in fixes:
            d = json.load(open(os.path.join(OCR, n + '.json'),
                               encoding='utf-8'))
            box_word = {(x[0], x[1]): x[5].strip() for x in d['words']
                        if x[5].strip()}
            for (l, t, pr) in fixes[n]:
                tok = box_word.get((l, t))
                if not tok:
                    continue
                best = None
                bd = 10 ** 9
                for ln in page['lines']:
                    dd = abs(ln['top'] - t)
                    if dd < bd:
                        bd, best = dd, ln
                if best is not None and bd <= 45:
                    fix_by_linetop.setdefault(best['top'], []).append(
                        (tok, pr))
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
