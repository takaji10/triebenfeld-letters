# -*- coding: utf-8 -*-
"""Merge documents that were split, and renumber the holding (docs/DOCUMENT_MERGE_PLAN.md;
the editor, 2026-11-23).

    python pipeline/review/merge_documents.py --unit <slug>            # dry run: the plan and every check
    python pipeline/review/merge_documents.py --unit <slug> --write    # carry it out

units/<slug>/intake/merges.yml:

    merges:
    - main: '1'
      parts:
      - {doc: '2', as: voice}       # written on the same sheet in another hand: a second voice
      - {doc: '3', as: enclosure}   # sent with the letter: its pages follow, no box
    - main: '21'
      parts:
      - {doc: '22', as: follows}    # a second text on the same page in the same hand: follows

The main document keeps its place; the parts are taken into it; then the
holding's documents are numbered 1, 2, 3 ... again in their order (the editor:
"re-number in the case where you combine"). Not for Oe 1 Bü 9454, whose
numbers are the archive's (refused).

Everything keyed by document number is rewritten from the old to the new
number: corpus.txt, the set-apart blocks, the decision sheets, rulings.yml
(checked by parsing: the rewritten file must equal the expected data),
reading.json, the summaries (the published files and the caches), the English
(the published files and the translation cache), the corrections file, the
date-order record, and the links in every holding's about.md, the era pages
and the timeline. The merged documents' summaries are written by hand
(`summaries:` in merges.yml, en and de) - the tool refuses to write without
them. Prose that names a document number in words is reported, not changed.
"""
import collections
import copy
import csv
import glob
import io
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
import unitlib  # noqa: E402

NL = chr(10)
SET_APART = ('office_notes.yml', 'margin_notes.yml', 'hand_notes.yml', 'sideways.yml')
LABEL_HAND = '[Written in another hand:]'
LABEL_SKIP = set()   # (part, page) whose voice joins the block before it on the same page


def pad_of(slug, letter):
    return '%s-%03d' % (slug, int(letter)) if letter.isdigit() else '%s-%s' % (slug, letter)


# ---- the corpus -------------------------------------------------------------

def parse_corpus(text):
    """(head lines, [(id, [(page_id, [lines])])]) - blank lines kept with the page they follow."""
    head, docs, cur, page = [], [], None, None
    for t in text.split(NL):
        s = t.strip()
        m = re.match(r'\[DOC (\S+)\]$', s)
        if m:
            cur = (m.group(1), [])
            docs.append(cur)
            page = None
            continue
        m = re.match(r'\[PAGE (\S+)\]$', s)
        if m and cur is not None:
            page = (m.group(1), [])
            cur[1].append(page)
            continue
        if cur is None:
            head.append(t)
        elif page is None:
            page = ('', [])
            cur[1].append(page)
            page[1].append(t)
        else:
            page[1].append(t)
    return head, docs


def strip_trailing_blank(lines):
    while lines and not lines[-1].strip():
        lines = lines[:-1]
    return lines


def build(docs, merges):
    """(new docs, id map old->new, voice blocks, follow starts, page map for parts)."""
    by_id = {d: pages for d, pages in docs}
    part_of = {}
    for mg in merges:
        for p in mg['parts']:
            part_of[str(p['doc'])] = (str(mg['main']), p['as'])
    new_docs, idmap, voices, follows, pagemap = [], {}, [], [], {}
    n = 0
    for d, pages in docs:
        if d in part_of:
            continue
        n += 1
        new_id = str(n)
        idmap[d] = new_id
        acc = [(pid, list(lines)) for pid, lines in pages]
        pagemap[d] = {i + 1: i + 1 for i in range(len(pages))}
        mg = next((m for m in merges if str(m['main']) == d), None)
        for p in (mg['parts'] if mg else []):
            pd, kind = str(p['doc']), p['as']
            idmap[pd] = new_id
            pagemap[pd] = {}
            for i, (pid, lines) in enumerate(by_id[pd], 1):
                content = [x for x in strip_trailing_blank(lines)]
                if acc and acc[-1][0] == pid:
                    acc[-1] = (pid, strip_trailing_blank(acc[-1][1]) + content)
                    pagemap[pd][i] = len(acc)
                else:
                    acc.append((pid, content))
                    pagemap[pd][i] = len(acc)
                firsts = [x for x in content if x.strip()]
                if kind == 'voice' and firsts:
                    n_lines = len([x for x in content if x.strip()])
                    prev = voices[-1] if voices else None
                    if prev and prev['letter'] == new_id and prev['page'] == pid and prev.get('_end') == len(acc):
                        # a voice directly after another on the same page: one block, one label
                        # (Nr. 12765, page 0012_a2: two drafts; a block's first line must be unique)
                        prev['lines'] += n_lines
                        LABEL_SKIP.add((pd, i))
                    else:
                        voices.append({'letter': new_id, 'page': pid, 'first': firsts[0].strip(),
                                       'lines': n_lines, '_end': len(acc)})
                if kind == 'follows' and firsts and i == 1:
                    follows.append((new_id, firsts[0].strip()))
        new_docs.append((new_id, acc))
    return new_docs, idmap, voices, follows, pagemap


def render(head, new_docs):
    out = list(head)
    for d, pages in new_docs:
        out.append('[DOC %s]' % d)
        for pid, lines in pages:
            if pid:
                out.append('[PAGE %s]' % pid)
            out.extend(lines)
    return NL.join(out)


def check_corpus(old_docs, new_docs):
    problems = []
    lines = lambda docs: sorted(x for _, pages in docs for _, ls in pages for x in ls if x.strip())
    if lines(old_docs) != lines(new_docs):
        problems.append('the text lines differ (not a pure merge)')
    seen = collections.Counter(pid for _, pages in new_docs for pid, _ in pages if pid)
    twice = [p for p, c in seen.items() if c > 1]
    if twice:
        problems.append('pages still under two documents: %s' % twice)
    return problems


# ---- rulings.yml, rewritten line by line and checked by parsing -----------------

def expected_rulings(r, idmap, parts):
    r = copy.deepcopy(r)

    def mapk(d):
        out = {}
        for k, v in (d or {}).items():
            k = str(k)
            if k in parts:
                continue
            out[idmap.get(k, k)] = v
        return out
    pl = r.get('places') or {}
    if 'overrides' in pl:
        pl['overrides'] = mapk(pl['overrides'])
    dt = r.get('dates') or {}
    for sec in ('read', 'supplied', 'twin', 'inferred'):
        if isinstance(dt.get(sec), dict):
            dt[sec] = mapk(dt[sec])
    if isinstance(dt.get('no_date'), list):
        dt['no_date'] = [idmap.get(str(x), str(x)) for x in dt['no_date'] if str(x) not in parts]
    docs = r.get('documents') or {}
    for sec in ('doc_type', 'language', 'split_note'):
        if isinstance(docs.get(sec), dict):
            docs[sec] = mapk(docs[sec])
    if isinstance(docs.get('duplicate_of'), dict):
        docs['duplicate_of'] = {idmap.get(str(k), str(k)): idmap.get(str(v), str(v))
                                for k, v in docs['duplicate_of'].items()}
    if isinstance(docs.get('relations'), dict):
        rel = {}
        for k, lst in docs['relations'].items():
            nk = idmap.get(str(k), str(k))
            keep = []
            for x in lst:
                nt = idmap.get(str(x['target']), str(x['target']))
                if nt == nk:
                    continue          # a relation inside the merged document
                y = dict(x)
                y['target'] = nt
                keep.append(y)
            if keep:
                rel.setdefault(nk, []).extend(keep)
        docs['relations'] = rel
    if isinstance(docs.get('estates'), dict):
        est = {}
        for k, v in docs['estates'].items():
            nk = idmap.get(str(k), str(k))
            cur = est.setdefault(nk, [])
            for e in v:
                if e not in cur:
                    cur.append(e)
        docs['estates'] = est
    for sec in ('damage', 'rough'):
        if isinstance((r.get(sec) or {}).get('letters'), list):
            seen = []
            for x in r[sec]['letters']:
                y = idmap.get(str(x), str(x))
                if y not in seen:
                    seen.append(y)
            r[sec]['letters'] = seen
    return r


def rewrite_rulings(raw, idmap, parts):
    """The rulings text with every document number rewritten. Returns new text."""
    out, section, sub, skip_indent = [], None, None, None
    rel_key_new = None
    lines = raw.split(NL)
    i = 0
    est_seen = {}
    rel_keys_written = set()
    while i < len(lines):
        t = lines[i]
        i += 1
        if skip_indent is not None:
            ind = len(t) - len(t.lstrip())
            if t.strip() and ind <= skip_indent:
                skip_indent = None
            else:
                continue
        m = re.match(r'^(\w[\w_]*):', t)
        if m:
            section, sub = m.group(1), None
            out.append(t)
            continue
        m = re.match(r'^  (\w[\w_]*):', t)
        if m:
            sub = m.group(1)
            # inline lists: letters: ["5", "9"], no_date: [...]
            if '[' in t and sub in ('letters', 'no_date'):
                def repl(mm):
                    return '"%s"' % idmap.get(mm.group(1), mm.group(1))
                vals = re.findall(r'"([^"]+)"', t.split(':', 1)[1].split('#')[0])
                newvals = []
                for v in vals:
                    if sub == 'no_date' and v in parts:
                        continue
                    nv = idmap.get(v, v)
                    if nv not in newvals:
                        newvals.append(nv)
                pre = t.split('[', 1)[0]
                comment = ('  #' + t.split('#', 1)[1]) if '#' in t.split(']')[-1] else ''
                out.append(pre + '[' + ', '.join('"%s"' % v for v in newvals) + ']' + comment)
                continue
            out.append(t)
            continue
        m = re.match(r'^(\s{4})"([^"]+)":(.*)$', t)
        if m and section in ('places', 'dates', 'documents'):
            ind, k, rest = m.groups()
            nk = idmap.get(k, k)
            if sub == 'relations':
                # a block: key line, then "- kind/target/note" lines more indented
                block = [t]
                while i < len(lines) and (not lines[i].strip() or len(lines[i]) - len(lines[i].lstrip()) > 4):
                    block.append(lines[i])
                    i += 1
                items, curr = [], None
                for b in block[1:]:
                    if re.match(r'^\s{6}- ', b):
                        curr = [b]
                        items.append(curr)
                    elif curr is not None:
                        curr.append(b)
                kept = []
                for it in items:
                    txt = NL.join(it)
                    mt = re.search(r'target:\s*"([^"]+)"', txt)
                    nt = idmap.get(mt.group(1), mt.group(1)) if mt else None
                    if nt == nk:
                        continue
                    if mt:
                        txt = txt.replace(mt.group(0), 'target: "%s"' % nt)
                    kept.append(txt)
                if kept:
                    if nk in rel_keys_written:
                        out.append(NL.join(kept))       # appended under the key already written
                    else:
                        out.append('%s"%s":' % (ind, nk))
                        out.append(NL.join(kept))
                        rel_keys_written.add(nk)
                continue
            if sub == 'estates':
                vals = re.findall(r'[\w-]+', rest.split('#')[0])
                if nk in est_seen:
                    pos, cur = est_seen[nk]
                    for v in vals:
                        if v not in cur:
                            cur.append(v)
                    out[pos] = '%s"%s": [%s]' % (ind, nk, ', '.join(cur))
                    continue
                est_seen[nk] = (len(out), list(vals))
                out.append('%s"%s": [%s]%s' % (ind, nk, ', '.join(vals),
                                               ('  #' + rest.split('#', 1)[1]) if '#' in rest else ''))
                continue
            if k in parts and sub in ('overrides', 'read', 'supplied', 'twin', 'inferred', 'doc_type',
                                      'language', 'split_note'):
                continue
            if sub == 'duplicate_of':
                rest = re.sub(r'"([^"]+)"', lambda mm: '"%s"' % idmap.get(mm.group(1), mm.group(1)), rest, count=1)
            out.append('%s"%s":%s' % (ind, nk, rest))
            continue
        out.append(t)
    return NL.join(out)


# ---- csv, blocks, json ---------------------------------------------------------

def remap_csv(path, col, fn):
    if not os.path.isfile(path):
        return None
    raw = io.open(path, encoding='utf-8-sig', newline='').read()
    rows = list(csv.DictReader(io.StringIO(raw)))
    fields = list(csv.DictReader(io.StringIO(raw)).fieldnames or [])
    for r in rows:
        if r.get(col) not in (None, ''):
            r[col] = fn(r[col])
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator='\n', extrasaction='ignore')
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue(), rows


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    slug = unitlib.unit_arg()
    if slug == 'oe1bu9454':
        sys.exit('Oe 1 Bü 9454 keeps the archive\'s numbers: not merged or renumbered (the editor, 2026-11-23)')
    unit = unitlib.one_unit(slug)
    write = '--write' in sys.argv
    spec = yaml.safe_load(io.open(os.path.join(unit.dir, 'intake', 'merges.yml'), encoding='utf-8'))
    merges = spec['merges']
    corpus_raw = io.open(unit.corpus_path, encoding='utf-8', newline='').read()
    head, docs = parse_corpus(corpus_raw)
    new_docs, idmap, voices, follows, pagemap = build(docs, merges)
    parts = {str(p['doc']) for m in merges for p in m['parts']}
    problems = check_corpus(docs, new_docs)
    new_corpus = render(head, new_docs)
    old_pad = lambda d: pad_of(slug, d)
    print('%s: %d documents -> %d' % (slug, len(docs), len(new_docs)))
    renum = {k: v for k, v in idmap.items() if k != v}
    print('  renumbered: ' + ', '.join('%s->%s' % kv for kv in idmap.items() if kv[0] != kv[1]))
    for mg in merges:
        print('  merged into %s: %s' % (idmap[str(mg['main'])], ', '.join(
            '%s (%s)' % (p['doc'], p['as']) for p in mg['parts'])))
    writes = {}       # path -> new text
    removes = set()   # paths to delete
    reports = []

    # corpus
    writes[unit.corpus_path] = new_corpus

    # set-apart blocks: renumber, and the voices of the merged parts
    for fn in SET_APART:
        p = os.path.join(unit.dir, fn)
        exists = os.path.isfile(p)
        raw = io.open(p, encoding='utf-8').read() if exists else ''
        d = yaml.safe_load(raw) or {} if raw else {}
        blocks = d.get('blocks') or []
        for b in blocks:
            b['letter'] = idmap.get(str(b['letter']), str(b['letter']))
        if fn == 'hand_notes.yml':
            blocks += voices
        if not exists and not (fn == 'hand_notes.yml' and voices):
            continue
        head_c = ''.join(l for l in raw.splitlines(True) if l.startswith('#')) if raw else (
            '# A second voice in another hand (pipeline/build/corpus_pages.py, SET_APART).\n'
            '#   first: the block\'s first line exactly as it stands in corpus.txt\n'
            '#   lines: how many lines the block has\n')
        body = yaml.safe_dump({'blocks': [{'letter': str(b['letter']), 'page': str(b['page']), 'first': b['first'],
                                           'lines': int(b['lines'])} for b in blocks]},
                              allow_unicode=True, sort_keys=False, width=1000)
        writes[p] = head_c + body

    # decision sheets
    for fn, col in (('paragraph_decisions.csv', 'letter'), ('linebreak_decisions.csv', 'letter'),
                    ('page_scan_map.csv', 'letter')):
        res = remap_csv(os.path.join(unit.dir, fn), col, lambda v: idmap.get(v, v))
        if res:
            text, rows = res
            if fn == 'paragraph_decisions.csv':
                # the text that follows on a shared page begins a paragraph
                for nid, first in follows + [(v['letter'], v['first']) for v in voices]:
                    ctx = first[:70]
                    hit = [r for r in rows if r['letter'] == nid and r['context'] == ctx]
                    if hit:
                        hit[0].update({'decision': 'break', 'confidence': 'held', 'cue': 'hand'})
                    else:
                        rows.append({'letter': nid, 'line': '0', 'decision': 'break', 'confidence': 'held',
                                     'cue': 'hand', 'ratio': '0', 'prev_len': '0', 'page_measure': '0',
                                     'prev_line': '', 'context': ctx})
                buf = io.StringIO()
                w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator='\n', extrasaction='ignore')
                w.writeheader()
                w.writerows(rows)
                text = buf.getvalue()
            writes[os.path.join(unit.dir, fn)] = text
    res = remap_csv(os.path.join(unit.dir, 'transcription_decisions.csv'), 'pad',
                    lambda v: pad_of(slug, idmap[v.rsplit('-', 1)[1].lstrip('0') or '0'])
                    if v.startswith(slug + '-') and (v.rsplit('-', 1)[1].lstrip('0') or '0') in idmap else v)
    if res:
        writes[os.path.join(unit.dir, 'transcription_decisions.csv')] = res[0]

    # rulings
    rp = os.path.join(unit.dir, 'rulings.yml')
    rraw = io.open(rp, encoding='utf-8').read()
    rnew = rewrite_rulings(rraw, idmap, parts)
    exp = expected_rulings(yaml.safe_load(rraw), idmap, parts)
    got = yaml.safe_load(rnew)
    if exp != got:
        for k in exp:
            if exp[k] != got.get(k):
                problems.append('rulings.yml: section %s does not come out as expected' % k)
    for k in parts:
        r0 = yaml.safe_load(rraw)
        for sec, sub in (('places', 'overrides'), ('dates', 'read'), ('documents', 'doc_type')):
            v = ((r0.get(sec) or {}).get(sub) or {}).get(k)
            if v is not None:
                reports.append('rulings of the merged-in document %s, dropped: %s.%s = %r' % (k, sec, sub, v))
    writes[rp] = rnew

    # correspondents.json (keyed by number): the main document's sender and
    # recipient stand; a merged-in part's are dropped and reported
    cj = os.path.join(unit.dir, 'correspondents.json')
    if os.path.isfile(cj):
        cd = json.load(io.open(cj, encoding='utf-8'))
        new_cd = {}
        for k, v in cd.items():
            if k in parts:
                reports.append('correspondents of the merged-in document %s, dropped: %s -> %s' % (
                    k, v.get('sender'), v.get('recipient')))
                continue
            new_cd[idmap.get(k, k)] = v
        writes[cj] = json.dumps(dict(sorted(new_cd.items(), key=lambda kv: (len(kv[0]), kv[0]))),
                                ensure_ascii=False, indent=2) + NL

    # reading.json (pad keys)
    jp = os.path.join(unit.dir, 'reading.json')
    if os.path.isfile(jp):
        rd = json.load(io.open(jp, encoding='utf-8'))
        new_rd = {}
        for k, v in rd.items():
            d = k.rsplit('-', 1)[1].lstrip('0') or '0'
            nd = idmap.get(d, d)
            nk = pad_of(slug, nd)
            v = dict(v)
            v['letter'] = nd
            if nk in new_rd:
                new_rd[nk]['notes'] = (new_rd[nk].get('notes', '') + ' ' + v.get('notes', '')).strip()
            else:
                new_rd[nk] = v
        writes[jp] = json.dumps(new_rd, ensure_ascii=False, indent=1) + NL

    # summaries: written by hand for the merged documents
    summ = spec.get('summaries') or {}
    for mg in merges:
        nid = idmap[str(mg['main'])]
        if not (summ.get(str(mg['main'])) or {}).get('en') or not (summ.get(str(mg['main'])) or {}).get('de'):
            problems.append('no summaries (en, de) given for the merged document %s (old %s)' % (nid, mg['main']))
    for sp in (os.path.join(ROOT, 'site', '_data', 'summaries.yml'), os.path.join(ROOT, 'site', '_data', 'summaries_de.yml'),
               os.path.join(unit.dir, 'summaries_de.yml')):
        if not os.path.isfile(sp):
            continue
        lang = 'de' if sp.endswith('_de.yml') else 'en'
        raw = io.open(sp, encoding='utf-8').read()
        data = yaml.safe_load(raw) or {}
        headc = ''.join(l for l in raw.splitlines(True)[:20] if l.startswith('#'))
        new = {}
        for k, v in data.items():
            if not str(k).startswith(slug + '-'):
                new[k] = v
                continue
            d = k.rsplit('-', 1)[1].lstrip('0') or '0'
            if d in parts:
                continue
            nk = pad_of(slug, idmap.get(d, d))
            mg = next((m for m in merges if str(m['main']) == d), None)
            new[nk] = (summ.get(d) or {}).get(lang, v) if mg else v
        writes[sp] = headc + yaml.safe_dump(new, allow_unicode=True, sort_keys=True, width=1000,
                                            default_flow_style=False)

    # caches and published English, by file
    tag = str(unit.get('published_tag') or '')
    cdirs = {'translation': os.path.join(ROOT, 'cache', 'translation-raw' + ('-' + tag if tag else '')),
             'sum_en': os.path.join(ROOT, 'cache', 'summaries-raw'),
             'sum_de': os.path.join(ROOT, 'cache', 'summaries-raw-de'),
             'reading': os.path.join(ROOT, 'cache', 'reading-' + slug)}
    tdir = os.path.join(ROOT, 'site', '_data', 'translations')
    for d, _ in docs:
        removes.add(os.path.join(tdir, old_pad(d) + '.yml'))
        for c in cdirs.values():
            removes.add(os.path.join(c, old_pad(d) + '.json'))
    for nd, _ in new_docs:
        olds = [d for d, n in idmap.items() if n == nd]
        main_old = next(d for d in olds if d not in parts)
        ordered = [main_old] + [str(p['doc']) for m in merges if str(m['main']) == main_old for p in m['parts']]
        kinds = {str(p['doc']): p['as'] for m in merges for p in m['parts']}
        # published English
        segs_out = {}
        tp_old = [os.path.join(tdir, old_pad(d) + '.yml') for d in ordered]
        if all(os.path.isfile(p) for p in tp_old):
            base = yaml.safe_load(io.open(tp_old[0], encoding='utf-8'))
            for d, p in zip(ordered, tp_old):
                data = yaml.safe_load(io.open(p, encoding='utf-8'))
                for s in data.get('segments') or []:
                    np_ = pagemap[d][int(s['page'])]
                    en = s.get('en') or ''
                    if d != main_old and kinds[d] == 'voice' and (d, int(s['page'])) not in LABEL_SKIP:
                        en = LABEL_HAND + '\n\n' + en
                    if np_ in segs_out:
                        prev = segs_out[np_]
                        prev['en'] = prev['en'].rstrip() + '\n\n' + en
                        for key in ('names', 'numbers'):
                            if s.get(key):
                                prev.setdefault(key, [])
                                prev[key] = prev[key] + [x for x in s[key] if x not in prev[key]]
                    else:
                        s2 = dict(s)
                        s2['page'] = np_
                        s2['en'] = en
                        segs_out[np_] = s2
            base['segments'] = [segs_out[k] for k in sorted(segs_out)]
            writes[os.path.join(tdir, pad_of(slug, nd) + '.yml')] = yaml.safe_dump(
                base, allow_unicode=True, sort_keys=False, width=100)
        elif any(os.path.isfile(p) for p in tp_old):
            problems.append('document %s: some parts have published English and some not' % nd)
        # translation cache
        cp = [os.path.join(cdirs['translation'], old_pad(d) + '.json') for d in ordered]
        if all(os.path.isfile(p) for p in cp):
            base = json.load(io.open(cp[0], encoding='utf-8'))
            pages = {}
            stale_parts = []
            for d, p in zip(ordered, cp):
                c = json.load(io.open(p, encoding='utf-8'))
                for pg in c.get('pages') or []:
                    np_ = pagemap[d][int(pg['page'])]
                    en = pg.get('en') or ''
                    if d != main_old and kinds[d] == 'voice' and (d, int(pg['page'])) not in LABEL_SKIP:
                        en = LABEL_HAND + '\n\n' + en
                    if np_ in pages:
                        pages[np_]['en'] = pages[np_]['en'].rstrip() + '\n\n' + en
                    else:
                        pg2 = dict(pg)
                        pg2['page'] = np_
                        pg2['en'] = en
                        pages[np_] = pg2
            base['letter'], base['pad'] = nd, pad_of(slug, nd)
            base['pages'] = [pages[k] for k in sorted(pages)]
            base['n_pages'] = len(pages)
            if len(ordered) > 1:
                base['source_note'] = 'merged 2026-11-23 from %s (docs/DOCUMENT_MERGE_PLAN.md)' % ', '.join(
                    old_pad(d) for d in ordered)
                base['source_hash'] = 'merged-' + base.get('source_hash', '')   # restamped after the rebuild
            writes[os.path.join(cdirs['translation'], pad_of(slug, nd) + '.json')] = json.dumps(
                base, ensure_ascii=False, indent=1)
        # summary and reading caches: the main's file under the new number
        for key in ('sum_en', 'sum_de', 'reading'):
            p0 = os.path.join(cdirs[key], old_pad(main_old) + '.json')
            if os.path.isfile(p0):
                c = json.load(io.open(p0, encoding='utf-8'))
                c['letter'], c['pad'] = nd, pad_of(slug, nd)
                if len(ordered) > 1 and key in ('sum_en', 'sum_de'):
                    c['summary'] = summ[main_old]['en' if key == 'sum_en' else 'de']
                    c['model'] = 'written in session (merge, 2026-11-23)'
                writes[os.path.join(cdirs[key], pad_of(slug, nd) + '.json')] = json.dumps(c, ensure_ascii=False,
                                                                                           indent=1)
    # the dataset's per-document files of numbers that no longer exist: the
    # dataset build writes the documents there are and never prunes (Nr. 12765
    # kept stale 25-30 until removed by hand, 2026-11-23)
    gone = [d for d, _ in docs if d not in {nd for nd, _ in new_docs}]
    for d in gone:
        removes.add(os.path.join(ROOT, 'dataset', 'documents', '%s-%s.json' % (slug, d)))
        removes.add(os.path.join(ROOT, 'dataset', 'text', '%s-%s.txt' % (slug, d)))
    removes -= set(writes)

    # corrections: pad and page
    cpath = os.path.join(ROOT, 'reference', 'english_corrections.yml')
    craw = io.open(cpath, encoding='utf-8').read()

    def fix_corr(m):
        d = m.group(2).lstrip('0') or '0'
        if d not in idmap:
            return m.group(0)
        np_ = pagemap[d][int(m.group(3))]
        return 'pad: %s, page: %d' % (pad_of(slug, idmap[d]), np_)
    cnew = re.sub(r'pad: (%s)-(\w+), page: (\d+)' % re.escape(slug), fix_corr, craw)
    if cnew != craw:
        writes[cpath] = cnew

    # date-order record
    dp = os.path.join(unit.dir, 'intake', 'date_order.yml')
    if os.path.isfile(dp):
        draw = io.open(dp, encoding='utf-8').read()
        writes[dp] = re.sub(r"letter: '([^']+)'", lambda m: "letter: '%s'" % idmap.get(m.group(1), m.group(1)), draw)

    # links in prose: /documents/<slug>/<n>/ everywhere authored
    link_files = (glob.glob(os.path.join(ROOT, 'units', '*', 'about*.md')) +
                  glob.glob(os.path.join(ROOT, 'site', 'eras', '*.md')) +
                  glob.glob(os.path.join(ROOT, 'site', 'de', 'epochen', '*.md')) +
                  [os.path.join(ROOT, 'site', '_data', 'timeline.yml'), os.path.join(ROOT, 'reference', 'connections.yml'),
                   os.path.join(ROOT, 'literature', 'links.yml')])
    pat = re.compile(r"(/documents/%s/)(\w+)(/)" % re.escape(slug))
    for p in link_files:
        if not os.path.isfile(p):
            continue
        raw = writes.get(p) or io.open(p, encoding='utf-8').read()
        if not pat.search(raw):
            continue
        # one pass: a cite link (<a href="{{ '/documents/slug/N/' | relative_url }}">N</a>)
        # gets its address and its shown number mapped together; any other
        # address is mapped alone. Never twice.
        cite = (r"""<a href="\{\{ '/documents/%s/(\w+)/' \| relative_url \}\}">(\w+)</a>""" % re.escape(slug))
        both = re.compile('%s|%s' % (cite, pat.pattern))

        def one_pass(m):
            if m.group(1) is not None:       # a cite link
                n_old, shown = m.group(1), m.group(2)
                n_new = idmap.get(n_old, n_old)
                shown_new = n_new if shown == n_old else shown
                return m.group(0).replace("/%s/' |" % n_old, "/%s/' |" % n_new, 1).replace(
                    '">%s</a>' % shown, '">%s</a>' % shown_new)
            return m.group(3) + idmap.get(m.group(4), m.group(4)) + m.group(5)
        new = both.sub(one_pass, raw)
        # a cite list that now names one document twice: [<a>1</a>, <a>1</a>] -> [<a>1</a>]
        one = r"""<a href="\{\{ '/documents/%s/(\w+)/' \| relative_url \}\}">\w+</a>""" % re.escape(slug)
        new = re.sub(r'(%s)(, (%s))+' % (one, one), lambda m: dedupe_cites(m.group(0)), new)
        if new != raw:
            writes[p] = new
    # the holding's own descriptions cite documents as [[4]] or [[1, 3, 4]]
    for p in (os.path.join(unit.dir, 'about.md'), os.path.join(unit.dir, 'about_de.md')):
        if os.path.isfile(p):
            raw = writes.get(p) or io.open(p, encoding='utf-8').read()
            new = remap_cites(raw, idmap)
            if new != raw:
                writes[p] = new
    # prose naming documents in words: reported
    for p in link_files + [os.path.join(unit.dir, 'unit.yml'), os.path.join(unit.dir, 'notes.md')]:
        if os.path.isfile(p) and os.path.basename(os.path.dirname(p)) == slug:
            for n, line in enumerate(io.open(p, encoding='utf-8'), 1):
                if re.search(r'\b(documents?|Dokument\w*|Nr\.|nos?\.)\s+\d', line):
                    reports.append('words naming a number, read by hand: %s:%d: %s' % (
                        os.path.relpath(p, ROOT), n, line.strip()[:110]))

    print()
    for r in reports:
        print('  report: ' + r)
    for pr in problems:
        print('  !! ' + pr)
    print('  files to write: %d; to remove: %d' % (len(writes), len([p for p in removes if os.path.isfile(p)])))
    if problems:
        sys.exit('refused: nothing written')
    if write:
        for p in removes:
            if os.path.isfile(p):
                os.remove(p)
        for p, txt in writes.items():
            with io.open(p, 'w', encoding='utf-8', newline='\n') as f:
                f.write(txt if txt.endswith(NL) else txt + NL)
        json.dump({'idmap': idmap, 'pagemap': pagemap}, io.open(os.path.join(unit.dir, 'intake', 'merge_map.json'),
                                                                'w', encoding='utf-8', newline='\n'), indent=1)
        print('written; the map is in intake/merge_map.json')


def remap_cites(text, idmap):
    """[[4]] / [[1, 3, 4]] citations (check_unit_text.py's form) mapped; a number named twice once."""
    def one(m):
        nums = [x.strip() for x in m.group(1).split(',')]
        if not all(re.match(r'^\w+$', x) for x in nums):
            return m.group(0)
        out = []
        for x in nums:
            y = idmap.get(x, x)
            if y not in out:
                out.append(y)
        return '[[' + ', '.join(out) + ']]'
    return re.sub(r'\[\[((?:\w+)(?:\s*,\s*\w+)*)\]\]', one, text)


def dedupe_cites(s):
    items = re.findall(r"""<a href="\{\{ '/documents/[^/]+/(\w+)/' \| relative_url \}\}">\w+</a>""", s)
    full = re.findall(r"""<a href="[^"]+">\w+</a>""", s)
    out, seen = [], set()
    for k, f in zip(items, full):
        if k in seen:
            continue
        seen.add(k)
        out.append(f)
    return ', '.join(out)


if __name__ == '__main__':
    main()
