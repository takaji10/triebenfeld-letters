# -*- coding: utf-8 -*-
"""Draft the English corrections for the date moves (docs/DATE_ORDER_PLAN.md,
Method 5). Run BEFORE the German is moved and rebuilt: it reads the German
paragraphs as they stand in dataset/units/<slug>/letters.json.

    python pipeline/review/date_order_english.py --unit oe1bu9454

For every entry of units/<slug>/intake/date_order.yml that has no English
correction yet:

- the German page's paragraphs are mapped one to one onto the English page's
  (the edition's label lines left out); a page where the counts differ is
  listed for drafting by hand;
- if every date line lies in paragraphs that hold nothing but date lines, the
  English paragraphs at those places are the date: they are taken out, joined
  by a space (", " after a place that stood on a line of its own; the editor,
  2026-11-23), and put after the paragraph that ends with the anchor line;
- anything else (the date shares a paragraph with other words) is listed for
  drafting by hand.

Every draft is checked: `find` occurs once on the published page, the words
of `find` and `replace` are the same (commas aside), and the replacement has
as many paragraphs as the find, less the joined ones. Writes
review/date_order/english_<slug>.yml (drafts) and lists the rest.
"""
import collections
import io
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import unitlib  # noqa: E402
import date_order  # noqa: E402

LABELS = {'[Written by the receiving office:]', '[Written in the margin:]', '[Written in another hand:]',
          '[The document continues:]'}


def paragraphs_with_spans(text):
    """[(start, end, text)] of the blank-line separated paragraphs of text."""
    out, pos = [], 0
    for m in re.finditer(r'\n\s*\n', text):
        out.append((pos, m.start(), text[pos:m.start()]))
        pos = m.end()
    out.append((pos, len(text), text[pos:]))
    return [(a, z, t) for a, z, t in out if t.strip()]


def words(s):
    return collections.Counter(w.strip(',') for w in s.split() if w.strip(','))


def german_paragraph_of(page, abs_line):
    """Index of the German paragraph holding abs_line, by para_lines; None if unsure."""
    dip = page['diplomatic'].split('\n')
    if page['line_end'] - page['line_start'] + 1 != len(dip):
        return None
    k = abs_line - page['line_start']
    if not 0 <= k < len(dip):
        return None
    pl = sorted(page.get('para_lines') or [])
    idx = sum(1 for x in pl if x <= k) - (1 if 0 in pl else 0)
    if not page.get('continues_previous') and 0 not in pl:
        pass
    return idx


def draft(unit, ent, rec, en_pages, corpus):
    letter = str(ent['letter'])
    date = [str(x) for x in ent['date']]
    docs = dict(date_order.documents_from(corpus))
    lines = docs[letter]
    texts = [t for _, _, t in lines]
    s = next(i for i in range(len(texts)) if texts[i:i + len(date)] == date)
    e = s + len(date) - 1
    a = next(j for j in range(e + 1, len(texts)) if texts[j] == str(ent['after']))
    page_id = lines[s][1]
    page = next((p for p in rec['pages'] if p.get('page_id') == page_id), None)
    if page is None:
        return None, 'the page %s is not in the dataset' % page_id
    gp = page['paragraphs']
    # the computed paragraph count must be the build's
    pl = sorted(page.get('para_lines') or [])
    if len(pl) + (0 if 0 in pl else 1) != len(gp) or page.get('office_lines') or page.get('margin_lines') \
            or page.get('hand_lines') or page.get('sideways_lines'):
        return None, 'the German page has set-apart text or paragraphs that para_lines does not account for'
    di = [german_paragraph_of(page, lines[k][0]) for k in range(s, e + 1)]
    ai = german_paragraph_of(page, lines[a][0])
    if None in di or ai is None:
        return None, 'a line could not be placed in its German paragraph'
    for k, i in zip(range(s, e + 1), di):
        if texts[k].strip() not in gp[i]:
            return None, 'the date line "%s" is not in German paragraph %d' % (texts[k], i)
    # paragraphs holding nothing but date lines
    page_lines = page['diplomatic'].split('\n')
    members = collections.defaultdict(list)
    for k in range(len(page_lines)):
        members[german_paragraph_of(page, page['line_start'] + k)].append(page['line_start'] + k)
    date_abs = {lines[k][0] for k in range(s, e + 1)}
    dparas = sorted(set(di))
    if any(set(members[i]) - date_abs for i in dparas):
        return None, 'the date shares a German paragraph with other words'
    # the anchor must end its paragraph
    if members[ai][-1] != lines[a][0]:
        return None, 'the anchor line does not end its German paragraph'
    seg = en_pages.get(page['page'])
    if not seg:
        return None, 'no English page %s' % page['page']
    en = seg
    ep = [x for x in paragraphs_with_spans(en) if x[2].strip() not in LABELS]
    if len(ep) != len(gp):
        return None, 'German %d paragraphs, English %d' % (len(gp), len(ep))
    if dparas != list(range(dparas[0], dparas[-1] + 1)) or ai <= dparas[-1]:
        return None, 'the date paragraphs are not consecutive before the anchor'
    first, last = dparas[0], ai
    span = en[ep[first][0]:ep[last][1]]
    if any(x.strip() in LABELS for x in re.split(r'\n\s*\n', span)):
        return None, 'a label line inside the span'
    dtexts = [re.sub(r'\s+', ' ', ep[i][2]).strip() for i in dparas]
    # a place on a line of its own: the first date line has no figure and is not
    # "den ..." ("Trąbczyn", "Frankfurth a/d O.")
    place_alone = len(date) > 1 and not re.search(r'\d', texts[s]) and \
        not re.match(r'\s*(den|d\.?|die|le|dnia)\b', texts[s], re.I)
    joined = dtexts[0]
    for k, t in enumerate(dtexts[1:], 1):
        sep = ', ' if (k == 1 and place_alone and not joined.endswith(',')) else ' '
        joined += sep + t
    rest = [en[ep[i][0]:ep[i][1]] for i in range(dparas[-1] + 1, last + 1)]
    new = '\n\n'.join(rest + [joined])
    find = span
    if en.count(find) != 1:
        return None, 'the English span occurs %d times on the page' % en.count(find)
    if words(find) != words(new):
        return None, 'the words differ (internal check)'
    return {'pad': rec['pad'], 'page': page['page'], 'find': find, 'replace': new,
            'why': '%s: the date after the signature' % ' / '.join(
                [texts[k] for k in range(e + 1, a + 1)] + [' '.join(date)])}, None


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    slug = unitlib.unit_arg()
    unit = unitlib.one_unit(slug)
    spec = date_order._yaml(os.path.join(unit.dir, 'intake', 'date_order.yml'))
    recs = {str(r['letter_id']): r for r in
            json.load(io.open(os.path.join(ROOT, 'dataset', 'units', slug, 'letters.json'), encoding='utf-8'))}
    corpus = io.open(unit.corpus_path, encoding='utf-8', newline='').read().split('\n')
    have = {(c['pad'], c['page']) for c in yaml.safe_load(io.open(os.path.join(ROOT, 'reference',
                                                                              'english_corrections.yml'),
                                                                  encoding='utf-8'))['corrections']
            if 'the date after the signature' in str(c.get('why', ''))}
    drafts, manual = [], []
    for ent in spec.get('moves') or []:
        rec = recs[str(ent['letter'])]
        tp = os.path.join(ROOT, 'site', '_data', 'translations', rec['pad'] + '.yml')
        segs = (yaml.safe_load(io.open(tp, encoding='utf-8')) or {}).get('segments') or []
        en_pages = {s['page']: s.get('en') or '' for s in segs}
        if any(p == rec['pad'] for p, _ in have):
            continue
        try:
            d, why = draft(unit, ent, rec, en_pages, corpus)
        except StopIteration:
            d, why = None, 'the date or anchor is not found as the entry has them (already moved?)'
        if d:
            drafts.append(d)
        else:
            manual.append({'letter': str(ent['letter']), 'pad': rec['pad'], 'why': why})
    out = os.path.join(ROOT, 'review', 'date_order', 'english_%s.yml' % slug)
    with io.open(out, 'w', encoding='utf-8', newline='\n') as f:
        yaml.safe_dump({'drafts': drafts, 'manual': manual}, f, allow_unicode=True, sort_keys=False, width=1000)
    print('%s: %d drafted, %d by hand -> %s' % (slug, len(drafts), len(manual), os.path.relpath(out, ROOT)))
    for m in manual:
        print('  by hand: %s %s' % (m['letter'], m['why']))


if __name__ == '__main__':
    main()
