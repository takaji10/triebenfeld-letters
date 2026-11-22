# -*- coding: utf-8 -*-
"""The editor's layout of the English (docs/ENGLISH_EDITOR_PLAN.md, 2026-11-22).

The editor lays out a page's English on the site (`?edit` on a document's
address): paragraph breaks, line breaks, indentation, alignment, italic, and
the voices set apart. The export comes home through import_layout.py into
`reference/english_layout/<pad>.yml`; every publish attaches it to the page as
the segment's `layout`, beside the plain `en`, which stays as it is for the
dataset, the search and the checks. site/assets/letter.js shows the layout
where there is one.

A page's layout:

    [ {"p": PARA} | {"box": "office"|"margin"|"hand", "ps": [PARA, ...]} , ... ]
    PARA = {"r": [[text, ""|"i"], ...], "i": 0-3, "a": "l"|"c"|"r"}

`r` holds the runs ("i" italic); a "\\n" inside a run's text is a line break;
`i` the indentation steps; `a` the alignment (left by default).

A layout is attached only if its words are the page's words: both reduced to
their letters and digits, lower case, the label lines of the plain text left
out (`norm`). If the English has changed since (a correction, a new
translation), the layout is not attached, and the publish reports it.
"""
import io
import os
import unicodedata

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR = os.path.join(ROOT, 'reference', 'english_layout')

LABELS = {'[Written by the receiving office:]': 'office', '[Written in the margin:]': 'margin',
          '[Written in another hand:]': 'hand'}
CONTINUES = '[The document continues:]'
KINDS = ('office', 'margin', 'hand')


def norm(text):
    """The letters and digits of a text, lower case, without the label lines."""
    paras = [p.strip() for p in text.replace('\r\n', '\n').split('\n\n')]
    keep = ' '.join(p for p in paras if p not in LABELS and p != CONTINUES)
    keep = unicodedata.normalize('NFC', keep).lower()
    return ''.join(ch for ch in keep if unicodedata.category(ch)[0] in 'LN')


def fingerprint(text):
    """FNV-1a (32 bit) over the code points of norm(text); the same in the editor."""
    h = 0x811c9dc5
    for ch in norm(text):
        h ^= ord(ch)
        h = (h * 0x01000193) & 0xffffffff
    return '%08x' % h


def paras_of(layout):
    for item in layout or []:
        if 'p' in item:
            yield item['p']
        else:
            for p in item.get('ps') or []:
                yield p


def layout_text(layout):
    return '\n\n'.join(''.join(r[0] for r in p.get('r') or []) for p in paras_of(layout))


def check(layout):
    """Problems with the shape of a layout (empty list if none)."""
    out = []
    if not isinstance(layout, list):
        return ['not a list']
    for k, item in enumerate(layout):
        if not isinstance(item, dict) or not (('p' in item) ^ ('box' in item)):
            out.append(f'item {k}: neither a paragraph nor a box')
            continue
        if 'box' in item and item['box'] not in KINDS:
            out.append(f'item {k}: unknown box {item["box"]!r}')
        for p in ([item['p']] if 'p' in item else item.get('ps') or []):
            if not isinstance(p, dict) or not isinstance(p.get('r'), list):
                out.append(f'item {k}: a paragraph without runs')
                continue
            if p.get('i', 0) not in (0, 1, 2, 3):
                out.append(f'item {k}: indentation {p.get("i")!r}')
            if p.get('a', 'l') not in ('l', 'c', 'r'):
                out.append(f'item {k}: alignment {p.get("a")!r}')
            for r in p['r']:
                if (not isinstance(r, list) or len(r) != 2 or not isinstance(r[0], str)
                        or r[1] not in ('', 'i')):
                    out.append(f'item {k}: a run {r!r}')
    return out


def load(pad):
    """{page (str): {'layout': [...], 'fingerprint': ...}} from the pad's file."""
    p = os.path.join(DIR, pad + '.yml')
    if not os.path.isfile(p):
        return {}
    d = yaml.safe_load(io.open(p, encoding='utf-8')) or {}
    return {str(x['page']): x for x in d.get('pages') or []}


def save(pad, pages):
    os.makedirs(DIR, exist_ok=True)
    rows = [pages[k] for k in sorted(pages, key=lambda s: (len(s), s))]
    with io.open(os.path.join(DIR, pad + '.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# The editor\'s layout of this document\'s English (pipeline/translate/english_layout.py;\n'
                '# written by import_layout.py from the editor\'s export: do not edit by hand).\n')
        yaml.safe_dump({'pad': pad, 'pages': rows}, f, allow_unicode=True, sort_keys=False, width=100)


def attach(pad, segs, problems=None):
    """Put each page's layout into its segment as `layout` where its words are the
    page's; drop a stale one. Returns True if any segment changed."""
    lay = load(pad)
    changed = False
    for seg in segs:
        old = seg.get('layout')
        new = None
        entry = lay.get(str(seg.get('page')))
        if entry and seg.get('en') and not seg.get('html'):
            if norm(layout_text(entry['layout'])) == norm(seg['en']) and not check(entry['layout']):
                new = entry['layout']
            elif problems is not None:
                problems.append(f'{pad} p{seg.get("page")}: the layout no longer fits the English '
                                f'(the words have changed since it was made) - not shown')
        if new is None and 'layout' in seg:
            del seg['layout']
            changed = True
        elif new is not None and new != old:
            seg['layout'] = new
            changed = True
    return changed
