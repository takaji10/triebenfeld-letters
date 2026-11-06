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
    # real Markdown tables (the editor's ruling): per-column cells from
    # annex_md.json (pixel-classified dash/empty cells + cleaned OCR
    # text); furniture rows (the series-c title, the b-series totals
    # line) as plain lines outside the tables
    amd_path = os.path.join(OCR, 'annex_md.json')
    amd = json.load(open(amd_path, encoding='utf-8')) \
        if os.path.isfile(amd_path) else None
    # the series-c OCR noise cells (0158 row 9's Nazwa/Parafia are the
    # one bad multi-line cell pair) - the strip's row text is
    # print-verified for this row; substituted at compose time
    NOISE_FIX = {
        ('0158', 9): ['Trojanowskie Olędry ⁹', 'Mur. Goślina',
                      'razem z Głębockiem a na miejscu Trzcianki',
                      'las', '—', 'AW. B. 1037', '5 VIII 1788',
                      '—', '—', '—'],
    }
    if amd:
        for n in amd:
            for r in amd[n]['rows']:
                fix = NOISE_FIX.get((n, r['num']))
                if fix:
                    r['cells'] = [r['cells'][0]] + fix
    # the annex tables' footnote apparatus (annex_notes.py: the print's
    # superscript refs in the Nazwa cells and the note blocks below the
    # sheets' tables; blocks numbered from 1, a ref resolves to the
    # nearest block below its own sheet)
    import annex_notes
    import annex_fixes
    if amd:
        nf = annex_fixes.apply(amd)
        print('annex_fixes applied:', nf)
    # the c-series totals rows: real table rows in the print (the
    # values pixel-verified; the leading '4.' of the Ludn figures sits
    # tight to the column rule and was lost in the first reads)
    C_TOTALS = {
        'u0': ['Razem z poprzedn.', '—', '—', '—', '—', '—', '—', '—',
               '2.178', '38', '4.514'],
        'u2': ['Ogółem', '—', '—', '—', '—', '—', '—', '—',
               '2.216', '38', '4.514'],
    }
    parts.append('[p. 123]\n\nANEKS I\n')
    HEAD = ('Lp. | Nazwa osady w okresie rozbiorów | Ówczesna parafia | '
            'Nazwa dzisiejsza | Rok założ. osady | Charakter terenu '
            'przed założ. osady | Przywilej lub wzmianka — sygn. źródła | '
            'data | L. dymów wg Tp. 89 lub 90 | dymów oblicz. '
            'szacunkowo | Ludn. osad wg Tołł.')
    SEP = ' | '.join(['---'] * 11)
    for n in [f'{i:04d}' for i in range(139, 160)]:
        parts.append(f'\n<!-- annex sheet {n} -->\n')
        if amd and n in amd:
            sh = amd[n]
            # the print's order: rows and furniture interleaved by
            # y (0159: rows 10-11, the totals line, the sub-table
            # title, then sub-rows 1-4 - two tables on one sheet)
            items = ([{'kind': 'row', 'y': r['y'][0], 'r': r}
                      for r in sh['rows']]
                     + [{'kind': 'furn', 'y': f['y'][0], 'f': f}
                        for f in sh['furniture']])
            items.sort(key=lambda x: x['y'])
            page = label(n)
            nums = sorted(r['num'] for r in sh['rows'])
            last_num = nums[-1] if nums else None

            def flush(table):
                if table:
                    parts.append(HEAD)
                    parts.append(SEP)
                    parts.extend(table)
                    parts.append('')
                    return []
                return table

            table = []
            for it in items:
                if it['kind'] == 'furn':
                    f = it['f']
                    if f['key'] in C_TOTALS:
                        # the print's totals row belongs to the table
                        # it follows (no header of its own)
                        cells = ['**%s**' % C_TOTALS[f['key']][0]] + \
                            C_TOTALS[f['key']][1:]
                        table.append('| ' + ' | '.join(cells) + ' |')
                        continue
                    table = flush(table)
                    if f['key'] == 'u1':
                        parts.append('**%s**\n' % f['text'].strip())
                    else:
                        parts.append('*%s*\n' % f['text'].strip())
                    continue
                r = it['r']
                cells = [c if c.strip() else ' '
                         for c in r['cells'][1:]]
                ref = annex_notes.REFS.get((n, r['num']))
                if ref:
                    note_num, ref_page, junk = ref
                    naz = cells[0]
                    if junk and naz.rstrip().endswith(junk):
                        naz = naz.rstrip()[:-len(junk)].rstrip()
                    else:
                        # fall back to a targeted strip of the common
                        # artifacts the superscript left behind
                        naz = re.sub(r'\s*[!?„”"$Ś9⁹*]+$', '', naz)
                    cells[0] = naz + f'[^{ref_page}-{note_num}]'
                table.append(f"| {r['num']} | " + ' | '.join(cells)
                             + ' |')
                if n in annex_notes.RAZEM and r['num'] == last_num:
                    # the series' totals row prints after the last
                    # numbered row (0146: after r111; 0157: after r156)
                    rz = annex_notes.RAZEM[n]
                    cells = ['**%s**' % rz['cells'][0]] + rz['cells'][1:]
                    if rz.get('ref'):
                        nn_, pg_ = rz['ref']
                        cells[0] += f'[^{pg_}-{nn_}]'
                    table.append('| ' + ' | '.join(cells) + ' |')
            table = flush(table)
            # the sheet's note block (the print sets it below the
            # sheet's table)
            for num, ntext in annex_notes.NOTES.get(n, []):
                parts.append(f'[^{page}-{num}]: {ntext}')
            if annex_notes.NOTES.get(n):
                parts.append('')
        else:
            # fallback: the raw-row rendering
            rows = json.load(open(os.path.join(OCR, 'annex_table.json'),
                                  encoding='utf-8'))[n]['rows']
            for num in sorted(int(k) for k in rows if k.isdigit()):
                raw = rows[str(num)].get('raw') or ''
                parts.append(f"{num}. {raw}  ")
        parts.append('')
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
    # the strip's systemic lowercase-l -> capital-I artifact (editor
    # ruling): 'Kl.' (Klassifikationsanschlaege) read as 'KI.', 'Ol.'
    # (Olendry) as 'OI.'/'OIL' - restore the print's sigla everywhere
    # (word-boundary guarded; single-letter Roman numerals untouched)
    for pat, rep in ((r'(?<![A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż])KI\.', 'Kl.'),
                     (r'(?<![A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż])OIL\b', 'Ol.'),
                     (r'(?<![A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż])OI\.', 'Ol.')):
        n = len(re.findall(pat, text))
        text = re.sub(pat, rep, text)
        print('normalize %s -> %s: %d' % (pat, rep, n))
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    print('written', os.path.abspath(OUT), len(text), 'chars')


if __name__ == '__main__':
    main()
