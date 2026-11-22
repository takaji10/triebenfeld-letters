# -*- coding: utf-8 -*-
"""Bring the layout editor's export home (docs/ENGLISH_EDITOR_PLAN.md, 2026-11-22).

    python pipeline/translate/import_layout.py <english_layout_YYYY-MM-DD.json>           # check only
    python pipeline/translate/import_layout.py <file> --write                            # write

The export (site/assets/layout-editor.js, "Export") holds:

- english: per page of a document, the editor's layout of the English. It is
  accepted only if its words are the page's words as published now
  (english_layout.norm); it goes into reference/english_layout/<pad>.yml and is
  attached to site/_data/translations/<pad>.yml at once (and at every publish).
- german: per document, the lines where the reading text's paragraphs begin or
  run on, and the lines set apart as a second voice. A break becomes a held
  row of the holding's paragraph_decisions.csv (cue `hand` where no cue
  proposed one); a voice becomes a block of the holding's office_notes.yml,
  margin_notes.yml or hand_notes.yml ("none" takes the lines out of any block).
  The document line numbers of the export are mapped to the corpus through
  dataset/units/<slug>/letters.json, so the dataset must be the one the site
  was built from.

After --write: rebuild the holdings named (python pipeline/regenerate.py --unit
<slug>; a holding's own intake/paragraphs.py may restate a decision - read its
rules), then the site, and verify.
"""
import csv
import io
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import english_layout  # noqa: E402
import english_forms   # noqa: E402

FILES = {'office': 'office_notes.yml', 'margin': 'margin_notes.yml', 'hand': 'hand_notes.yml'}
COLS = ['letter', 'line', 'decision', 'confidence', 'cue', 'ratio', 'prev_len', 'page_measure',
        'prev_line', 'context']


def english(entries, write, report):
    by_pad = {}
    for e in entries:
        by_pad.setdefault(e['pad'], []).append(e)
    for pad, es in sorted(by_pad.items()):
        tp = os.path.join(ROOT, 'site', '_data', 'translations', pad + '.yml')
        if not os.path.isfile(tp):
            report.append(f'!! {pad}: no published English')
            continue
        data = yaml.safe_load(io.open(tp, encoding='utf-8')) or {}
        segs = {str(s.get('page')): s for s in data.get('segments') or []}
        pages = english_layout.load(pad)
        took = 0
        for e in es:
            seg = segs.get(str(e['page']))
            if not seg or not seg.get('en'):
                report.append(f'!! {pad} p{e["page"]}: no such page in the English')
                continue
            bad = english_layout.check(e['layout'])
            if bad:
                report.append(f'!! {pad} p{e["page"]}: the layout is malformed: {bad[:3]}')
                continue
            if english_layout.norm(english_layout.layout_text(e['layout'])) != english_layout.norm(seg['en']):
                report.append(f'!! {pad} p{e["page"]}: the English has changed since the layout was made '
                              f'- not taken; lay the page out again')
                continue
            pages[str(e['page'])] = {'page': int(e['page']), 'fingerprint': english_layout.fingerprint(seg['en']),
                                     'layout': e['layout']}
            took += 1
        report.append(f'{pad}: {took} of {len(es)} English page(s) taken')
        if write and took:
            english_layout.save(pad, pages)
            if english_layout.attach(pad, data.get('segments') or [], report):
                english_forms._dump(tp, data)


def corpus_map(unit, letter):
    """(corpus lines, {doc line: (absolute line, page_id)}) for one document."""
    lines = io.open(os.path.join(ROOT, 'units', unit, 'corpus.txt'), encoding='utf-8').read().split('\n')
    recs = json.load(io.open(os.path.join(ROOT, 'dataset', 'units', unit, 'letters.json'), encoding='utf-8'))
    rec = next((r for r in recs if str(r.get('letter_id')) == str(letter)), None)
    out = {}
    for p in (rec or {}).get('pages') or []:
        for d in range(p['doc_line_start'], p['doc_line_end'] + 1):
            out[d] = (p['line_start'] + d - p['doc_line_start'], p.get('page_id') or '')
    return lines, out


def german(entries, write, report):
    for e in entries:
        unit, letter = e['unit'], str(e['letter'])
        udir = os.path.join(ROOT, 'units', unit)
        try:
            lines, where = corpus_map(unit, letter)
        except (OSError, ValueError) as x:
            report.append(f'!! {unit} {letter}: {x}')
            continue
        # paragraph starts
        dp = os.path.join(udir, 'paragraph_decisions.csv')
        rows = list(csv.DictReader(io.open(dp, encoding='utf-8-sig'))) if os.path.isfile(dp) else []
        changed = 0
        for b in e.get('breaks') or []:
            hit = where.get(int(b['doc_line']))
            if not hit:
                report.append(f'!! {unit} {letter}: document line {b["doc_line"]} not found')
                continue
            ab, _ = hit
            t = lines[ab - 1].strip()
            if b.get('text') and english_layout.norm(b['text'])[:20] not in english_layout.norm(t):
                report.append(f'!! {unit} {letter} line {b["doc_line"]}: the page showed "{b["text"][:40]}", '
                              f'the corpus has "{t[:40]}" - not taken (the text has moved since the export)')
                continue
            ctx = t[:70]
            prev = lines[ab - 2].strip()[:60] if ab >= 2 else ''
            row = next((r for r in rows if r['letter'] == letter and r['context'] == ctx), None)
            if row:
                row['decision'], row['confidence'] = b['decision'], 'held'
            else:
                rows.append({'letter': letter, 'line': str(ab), 'decision': b['decision'], 'confidence': 'held',
                             'cue': 'hand', 'ratio': '0', 'prev_len': '0', 'page_measure': '0',
                             'prev_line': prev, 'context': ctx})
            changed += 1
        if write and changed:
            with io.open(dp, 'w', encoding='utf-8-sig', newline='') as f:
                w = csv.DictWriter(f, fieldnames=COLS, lineterminator='\n', extrasaction='ignore')
                w.writeheader()
                w.writerows(rows)
        # voices
        voiced = 0
        for v in e.get('voices') or []:
            a, z = where.get(int(v['from'])), where.get(int(v['to']))
            if not a or not z or a[1] != z[1]:
                report.append(f'!! {unit} {letter}: the lines {v["from"]}-{v["to"]} are not on one page')
                continue
            first, n, page_id = lines[a[0] - 1].strip(), z[0] - a[0] + 1, a[1]
            span = set(range(a[0], z[0] + 1))
            for kind, fn in FILES.items():
                path = os.path.join(udir, fn)
                if not os.path.isfile(path):
                    continue
                raw = io.open(path, encoding='utf-8').read()
                d = yaml.safe_load(raw) or {}
                keep, touched = [], False
                for blk in d.get('blocks') or []:
                    if str(blk.get('letter')) == letter and blk.get('page') == page_id:
                        try:
                            s = next(k for k in range(a[0] - 200, z[0] + 200)
                                     if 0 < k <= len(lines) and lines[k - 1].strip() == str(blk['first']).strip())
                        except StopIteration:
                            s = None
                        if s is not None and span & set(range(s, s + int(blk['lines']))):
                            # keep the parts of the old block outside the new range
                            end = s + int(blk['lines']) - 1
                            parts = [(s, a[0] - 1), (z[0] + 1, end)]
                            for p0, p1 in parts:
                                if p1 >= p0:
                                    keep.append({'letter': letter, 'page': page_id,
                                                 'first': lines[p0 - 1].strip(), 'lines': p1 - p0 + 1})
                            report.append(f'  {unit} {letter}: block "{str(blk["first"])[:30]}" in {fn} cut to '
                                          f'what lies outside lines {v["from"]}-{v["to"]}')
                            touched = True
                            continue
                    keep.append(blk)
                if write and touched:
                    write_blocks(path, raw, keep)
            if v['kind'] in FILES:
                path = os.path.join(udir, FILES[v['kind']])
                raw = io.open(path, encoding='utf-8').read() if os.path.isfile(path) else ''
                d = yaml.safe_load(raw) or {} if raw else {}
                blocks = d.get('blocks') or []
                blocks.append({'letter': letter, 'page': page_id, 'first': first, 'lines': n})
                if write:
                    write_blocks(path, raw, blocks, kind=v['kind'])
            voiced += 1
        report.append(f'{unit} {letter}: {changed} paragraph decision(s), {voiced} voice(s)')


def write_blocks(path, raw, blocks, kind=None):
    head = ''.join(l for l in raw.splitlines(True) if l.startswith('#')) if raw else (
        f'# Set apart on the site ({kind}; pipeline/build/corpus_pages.py, SET_APART). Written by\n'
        f'# pipeline/translate/import_layout.py from the editor\'s layout export.\n'
        f'#   first: the block\'s first line exactly as it stands in corpus.txt\n'
        f'#   lines: how many lines the block has\n')
    body = yaml.safe_dump({'blocks': [{'letter': str(b['letter']), 'page': b['page'], 'first': b['first'],
                                       'lines': int(b['lines'])} for b in blocks]},
                          allow_unicode=True, sort_keys=False, width=1000)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(head + body)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    write = '--write' in sys.argv
    if not args:
        sys.exit(__doc__)
    data = json.load(io.open(args[0], encoding='utf-8'))
    if data.get('kind') != 'triebenfeld-layout':
        sys.exit('not a layout export')
    report = []
    english(data.get('english') or [], write, report)
    german(data.get('german') or [], write, report)
    for x in report:
        print(x)
    print('written' if write else '(check only; --write to write)')


if __name__ == '__main__':
    main()
