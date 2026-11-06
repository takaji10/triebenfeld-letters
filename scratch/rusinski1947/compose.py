# -*- coding: utf-8 -*-
"""Compose original.md for Rusinski 1947 - the working draft.

Structure:
  - front matter (title page, imprint, contents, Wykaz skrotow) from
    front_matter.md (composed separately; included as a literal here);
  - the body pages [p. 1]..[p. 122] from the marked paragraphs;
  - the footnote definitions after each page's body, page-prefixed;
  - ANEKS I as HTML tables from annex_table.json (tier A/B rows parsed
    into the nine columns; tier C rows kept as raw cell text pending the
    spot sheet);
  - ANEKS II (pp. 145-150) and III (pp. 151-156) as prose;
  - the four plates recorded.
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', 'literature', 'rusinski1947',
                   'original.md')

BODY = [f'{i:04d}' for i in range(16, 138)]
ANEX2 = [f'{i:04d}' for i in range(160, 166)]
ANEX3 = [f'{i:04d}' for i in range(166, 172)]


def label(n):
    return str(int(n) - 15)


def main():
    spath = os.path.join(OCR, 'structure4.json')
    if not os.path.isfile(spath):
        spath = os.path.join(OCR, 'structure2.json')
    if not os.path.isfile(spath):
        spath = os.path.join(OCR, 'structure.json')
    struct = json.load(open(spath, encoding='utf-8'))
    sys.path.insert(0, HERE)
    from paragraphs2 import assemble_marked
    import readability
    # the pct/fraction token map (pct_frac.py's 5x-verified decisions):
    # applied to body AND note texts (the earlier fix pass reached only
    # the body lines; the note layer carried the same artifacts)
    tokmap = {}
    pf = os.path.join(OCR, 'pct_frac.json')
    if os.path.isfile(pf):
        for k, v in json.load(open(pf, encoding='utf-8')).items():
            if v.get('resolved') and v.get('print') not in (None, 'MARKER') \
                    and v['print'] != v['tok']:
                key = v['tok'].strip('.,;:!?»”"()')
                tokmap[key] = v['print']
    # MANUAL supplement: percent tokens the queue missed or misclassed,
    # each verified by the read-through's cross-references (p. 13's 75%
    # confirmed by p. 31's "do 25%", p. 14's one-third confirmed by the
    # 832/550 arithmetic, the p. 34 range by the chapter's subject)
    tokmap.update({
        '5%/': '5%', '10%/': '10%', '36%/': '36%', '20%/': '20%',
        '13.6%%': '13.6%', '750/y': '75%', '!/': '⅓',
        '35—38?/': '35—38%',
    })

    def fix_toks(text):
        out = []
        for tok in text.split(' '):
            core = tok.strip('.,;:!?»”"()')
            if core in tokmap:
                out.append(tok.replace(core, tokmap[core]))
            else:
                out.append(tok)
        return ' '.join(out)
    parts = []

    # ---- front matter -------------------------------------------------
    fm = os.path.join(HERE, 'front_matter.md')
    if os.path.isfile(fm):
        parts.append(open(fm, encoding='utf-8').read().strip())
    # ---- body ---------------------------------------------------------
    # paragraphs collected per page first: the readability pass + the
    # cross-page hyphen join (a word hyphenated over the leaf: p. 32
    # 'Element nie-' -> p. 33 'miecki...') run before assembly
    page_paras = {}
    for n in BODY + ANEX2 + ANEX3:
        page_paras[n] = [fix_toks(readability.apply(p))
                         for p in assemble_marked(n)]
        for note in struct[n]['notes']:
            note['text'] = fix_toks(readability.apply(note['text']))
    order = BODY + ANEX2 + ANEX3
    LABEL_RE = re.compile(r'\[\^[^\]]+\]')
    TERM = ('.', '!', '?', '…', '”', '»', ':', ';')
    for a, b in zip(order, order[1:]):
        pa, pb = page_paras[a], page_paras[b]
        while pa and not pa[-1].strip():
            pa.pop()
        while pb and not pb[0].strip():
            pb.pop(0)
        if not pa or not pb:
            continue
        tail = pa[-1].rstrip()
        tail_txt = LABEL_RE.sub(' ', tail).rstrip()
        head = pb[0].lstrip()
        joined = None
        if tail_txt.endswith('-'):
            toks = tail.split()
            # the fragment = the last token that is not a parked label;
            # labels parked after it belong to the joined word
            fi = len(toks) - 1
            parked = []
            while fi >= 0 and LABEL_RE.fullmatch(toks[fi]):
                parked.insert(0, toks[fi])
                fi -= 1
            frag_w = toks[fi] if fi >= 0 else ''
            base = LABEL_RE.sub('', frag_w).rstrip('-')
            m = LABEL_RE.search(frag_w)
            lab = m.group(0) if m else ''
            # the fragment must be a plausible word-half (lowercase
            # letters): rejects sliver junk ('Ooz————') and digits
            if base and re.fullmatch(r'[a-ząćęłńóśźż]+', base) \
                    and len(base) >= 2 and head[:1].islower():
                bw = head.split(' ', 1)
                first = base + bw[0]
                rest = bw[1] if len(bw) > 1 else ''
                joined = first + lab
                if parked:
                    joined += ' ' + ' '.join(parked)
                if rest:
                    joined += ' ' + rest
                page_paras[a] = pa[:-1] + \
                    ([' '.join(toks[:fi])] if fi > 0 else [])
                page_paras[b] = [joined] + pb[1:]
                continue
        elif not tail_txt.endswith(TERM) and head[:1].islower() \
                and not head.startswith('„') and not head.startswith('«'):
            # plain mid-sentence page break: the print's paragraph
            # simply continues over the leaf - the whole paragraph
            # moves to page B (intact, labels included)
            page_paras[a] = pa[:-1]
            page_paras[b] = [tail + ' ' + head] + pb[1:]
            continue
    for n in BODY:
        parts.append(f'[p. {label(n)}]\n')
        parts.append('\n\n'.join(page_paras[n]))
        notes = []
        for note in struct[n]['notes']:
            notes.append(f"[^{label(n)}-{note['num']}]: {note['text']}")
        if notes:
            parts.append('\n'.join(notes))
    # ---- ANEKS I tables (printed pp. 123-144) ---------------------------
    # rendered as the print-faithful raw row text (the editor-reviewed
    # format); the per-column parse (annex_cells.json + RULES_SHEET.html)
    # is available for a future cell-table rendering on the editor's
    # word - the dash-cells OCR as junk ('Sz=—=—') that would take
    # hundreds of spot answers to certify
    parts.append('[p. 123]\n\nANEKS I\n')
    at = json.load(open(os.path.join(OCR, 'annex_table.json'),
                        encoding='utf-8'))
    for n in [f'{i:04d}' for i in range(139, 160)]:
        rows = at[n]['rows']
        parts.append(f'\n<!-- annex sheet {n}, tier mix -->\n')
        unnum = [(rows[k].get('y', [10 ** 9])[0], k)
                 for k in rows if not k.isdigit()]
        for num in sorted(int(k) for k in rows if k.isdigit()):
            r = rows[str(num)]
            if r['tier'] in ('A', 'B') and r.get('cells'):
                cells = r['cells']
                cells = [c for c in cells if c.strip()]
                cells[0] = re.sub(r'^\|?\s*' + str(num) + r'\s*\|?\s*',
                                  '', cells[0])
                parts.append(f"{num}. " + ' | '.join(cells) + '  ')
            else:
                raw = r.get('raw') or ' '.join(r.get('cells', []))
                parts.append(f"{num}. {raw}  ")
        for _, k in sorted(unnum):
            raw = rows[k].get('raw') or ''
            parts.append(f"{raw}  ")
    # ---- ANEKS II and III (printed sources, pp. 145-150, 151-156) -------
    for group in (ANEX2, ANEX3):
        for n in group:
            parts.append(f'[p. {label(n)}]\n')
            parts.append('\n\n'.join(page_paras[n]))
            notes = []
            for note in struct[n]['notes']:
                notes.append(f"[^{label(n)}-{note['num']}]: {note['text']}")
            if notes:
                parts.append('\n'.join(notes))
    # ---- the plates -----------------------------------------------------
    parts.append("""
[p. 157]

Plany osad (the settlement plans, eight plates) and the Mapa: image
plates, not transcribed (the editor's ruling). Scans tom5_0172-tom5_0175;
tom5_0174's caption reads "3. Nowe al. Wielkokrobielewskie Olędry.
Przykład osady rozrzuconej. Fotografia mapy nr 113 z r. 1830."
""")
    text = '\n\n'.join(parts) + '\n'
    # the print sets its markers tight to the word ('lata³,'): remove
    # the space the token replacement leaves before a label
    text = re.sub(r' +(\[\^)', r'\1', text)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    print('written', os.path.abspath(OUT), len(text), 'chars')


if __name__ == '__main__':
    main()
