# -*- coding: utf-8 -*-
"""The tools of the Latin audit (docs/LATIN_AUDIT_PLAN.md).

    python pipeline/review/latin_audit.py scope               # the documents in scope, counted
    python pipeline/review/latin_audit.py manifest            # reference/latin_audit/manifest.json
    python pipeline/review/latin_audit.py tildes              # reference/latin_audit/tildes.json
    python pipeline/review/latin_audit.py refs                # reference/latin_audit/references.json
    python pipeline/review/latin_audit.py strips <slug> [--web]
    python pipeline/review/latin_audit.py texts <slug>        # each page's text, numbered, for the readers
    python pipeline/review/latin_audit.py crop <slug> <band file> <x0,y0,x1,y1 fractions> <name>
    python pipeline/review/latin_audit.py apply <slug> [--write] [--file <name in intake/>]
    python pipeline/review/latin_audit.py impact <slug>       # what else a holding's applied audit touches
    python pipeline/review/latin_audit.py sheet               # the one spot sheet, from questions.csv
    python pipeline/review/latin_audit.py serve [--read]      # the same with buttons; answers saved at once

In scope: every document whose language (dataset/letters.json) includes Latin, the Kodeks left out
(printed text, never corrected).

`strips` cuts each page into overlapping bands for the readers, into review/latin_audit/<slug>/strips/.
It takes the page from the editor's original scans: <raw>/processed/<scan> (where the holding's
cutting step has put the pages, turned and cut at the editor's folds), else <raw>/<scan>. <raw> is the
holding's `raw_dir` (unit.yml) or `RAW` (intake/holding.py). Only with --web does it fall back to the
site's 1,100-pixel copy, and it says so for every page.

`apply` puts the settled rows of units/<slug>/intake/latin_audit.json into corpus.txt:
    {"ROWS":   [[page id, old, new, why], ...],     corrections the page proves
     "EXPAND": [[page id, old, new, why], ...]}     certain tilde expansions (EDITORIAL_RULES)
Each `old` must stand exactly once on its page. Nothing is written if any row fails. Every applied row
is logged in the holding's transcription_decisions.csv (as courtbook.correct does), with the source
"Latin audit, read on the scan" or "Latin audit, expansion". Run it once; a second run finds nothing.
"""
import csv
import glob
import hashlib
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'reference', 'latin_audit')
REVIEW = os.path.join(ROOT, 'review', 'latin_audit')
DOUBT = re.compile(r'\[[^\]\[]*\?\]|\[(?:\.\.\.|…)\]')
TILDE = re.compile(r'\S*~\S*')


def _letters():
    return json.load(io.open(os.path.join(ROOT, 'dataset', 'letters.json'), encoding='utf-8'))


def in_scope():
    return [l for l in _letters() if 'la' in (l.get('language') or '').split(',') and l['unit'] != 'kdw']


def _yaml(path):
    import yaml
    return yaml.safe_load(io.open(path, encoding='utf-8')) or {}


def raw_dir(slug):
    """Where the editor's original scans of a holding are, as the holding records it."""
    u = _yaml(os.path.join(ROOT, 'units', slug, 'unit.yml'))
    r = (u.get('scans') or {}).get('raw_dir')
    if r:
        return r
    for p in glob.glob(os.path.join(ROOT, 'units', slug, 'intake', '*.py')):
        m = re.search(r'^RAW\s*=\s*r?["\']([^"\']+)["\']', io.open(p, encoding='utf-8').read(), re.M)
        if m:
            return m.group(1)
    return None


def scan_keys(slug):
    """{web image name: the scan's own name} from the holding's scan_rename_map.json."""
    p = os.path.join(ROOT, 'units', slug, 'scan_rename_map.json')
    if not os.path.exists(p):
        return {}
    return {v: k for k, v in json.load(io.open(p, encoding='utf-8-sig')).items()}


def web_images(slug):
    """{(document number, page): web image name} from page_scan_map.csv."""
    out = {}
    p = os.path.join(ROOT, 'units', slug, 'page_scan_map.csv')
    with io.open(p, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r.get('page'):
                out[(r['letter'], int(r['page']))] = r['image']
    return out


def cmd_scope():
    rows = {}
    for l in in_scope():
        r = rows.setdefault(l['unit'], [0, 0, 0, 0, 0])
        r[0] += 1
        for p in l['pages']:
            t = p.get('diplomatic') or ''
            r[1] += 1
            r[2] += len(t.split())
            r[3] += len(TILDE.findall(t))
            r[4] += len(DOUBT.findall(t))
    tot = [0] * 5
    print('| Holding | Docs | Pages | Words | ~ forms | Marks of doubt |')
    for u, r in sorted(rows.items()):
        print('| %s | %d | %d | %d | %d | %d |' % ((u,) + tuple(r)))
        tot = [a + b for a, b in zip(tot, r)]
    print('| total %d holdings | %d | %d | %d | %d | %d |' % ((len(rows),) + tuple(tot)))


def cmd_manifest():
    units = {}
    for l in in_scope():
        slug = l['unit']
        if slug not in units:
            u = _yaml(os.path.join(ROOT, 'units', slug, 'unit.yml'))
            units[slug] = {'ref': u.get('reference') or u.get('ref') or u.get('title'), 'raw': raw_dir(slug),
                           'folds': os.path.exists(os.path.join(ROOT, 'units', slug, 'intake', 'folds.json')),
                           'pages': [], '_web': web_images(slug), '_keys': scan_keys(slug)}
        m = units[slug]
        for p in l['pages']:
            web = m['_web'].get((l['letter_id'], p['page']))
            t = p.get('diplomatic') or ''
            m['pages'].append({'uid': l['uid'], 'page': p['page'], 'page_id': p['page_id'], 'web': web,
                               'scan': m['_keys'].get(web), 'lines': len(t.split('\n')),
                               'tildes': len(TILDE.findall(t)),
                               'doubts': [d for d in DOUBT.findall(t)]})
    missing = []
    for slug, m in units.items():
        del m['_web'], m['_keys']
        if not m['raw']:
            missing.append(slug + ': no raw folder recorded')
        missing += ['%s %s p.%s: no scan name' % (slug, p['uid'], p['page']) for p in m['pages'] if not p['scan']]
    os.makedirs(OUT, exist_ok=True)
    io.open(os.path.join(OUT, 'manifest.json'), 'w', encoding='utf-8', newline='\n').write(
        json.dumps(units, ensure_ascii=False, indent=1) + '\n')
    print('manifest:', len(units), 'holdings,', sum(len(m['pages']) for m in units.values()), 'pages')
    for x in missing:
        print('  !', x)


def bracket(written, full):
    """The written form with its tilde replaced by the supplied letters in brackets (EDITORIAL_RULES,
    2026-11-27): Calissien~ + Calissiensibus -> Calissien[sibus]; Cond~nis + Condescensionis ->
    Cond[escensio]nis; a doubled consonant that the full word does not continue is written once:
    Citt~ + Citationes -> Cit[ationes]. Returns (bracketed, number of gaps) or (None, 0) where the
    written letters are not the full word's letters in order (ott~ for olim, JMcum~): settled by hand.
    A form with more than one gap (vn~tis -> v[e]n[ien]tis) is returned too; its form waits on the
    editor (plan, section 3)."""
    m = re.match(r'^(\(?)(.*?)([.,;:)\]]*)$', written)
    lead, w, tail = m.group(1), m.group(2), m.group(3)
    if w.count('~') != 1 or full.endswith('?') or ' ' in full:
        return None, 0
    a, b = w.split('~')
    if b and not full.lower().endswith(b.lower()):
        return None, 0
    head, fh = a, full[:len(full) - len(b)] if b else full
    out, j, gaps = [], 0, 0
    i = 0
    while i < len(head):
        ch = head[i]
        if i + 1 < len(head) and head[i + 1] == ch and ch.lower() not in 'aeiouy' and \
                j < len(fh) and fh[j].lower() == ch.lower() and not (j + 1 < len(fh) and fh[j + 1].lower() == ch.lower()):
            i += 1                       # the clerk's doubled consonant, written once
            continue
        k = j
        while k < len(fh) and fh[k].lower() != ch.lower():
            k += 1
        if k == len(fh) or (i == 0 and k != 0):
            return None, 0
        if k > j:
            out.append('[' + fh[j:k] + ']')
            gaps += 1
        out.append(fh[k] if fh[k] == ch else ch)
        j = k + 1
        i += 1
    if j < len(fh):
        out.append('[' + fh[j:] + ']')
        gaps += 1
    if not gaps:
        return None, 0
    fwd = (lead + ''.join(out) + b + tail, gaps)
    back = _from_end(head, fh)
    if back and gaps >= 3 and back[1] < gaps:   # three or more gaps: the alignment with fewer (Condsnis~: Cond[escen]s[io]nis)
        return lead + back[0] + b + tail, back[1]
    return fwd


def _from_end(head, fh):
    """The letters of `head` matched in `fh` from the end backwards: (bracketed, gaps) or None."""
    out, j, i = [], len(fh), len(head) - 1
    gaps = 0
    while i >= 0:
        ch = head[i]
        if i > 0 and head[i - 1] == ch and ch.lower() not in 'aeiouy' and fh[:j].lower().count(ch.lower()) < 2:
            i -= 1
            continue
        k = j - 1
        while k >= 0 and fh[k].lower() != ch.lower():
            k -= 1
        if k < 0 or (i == 0 and k != 0):
            return None
        if k + 1 < j:
            out.append('[' + fh[k + 1:j] + ']')
            gaps += 1
        out.append(ch)
        j = k
        i -= 1
    return ''.join(reversed(out)), gaps


def _draft():
    """The guide's draft expansions (reference/guide/abbreviations_expanded.yml), by document and the
    words around the form."""
    d = _yaml(os.path.join(ROOT, 'reference', 'guide', 'abbreviations_expanded.yml'))
    out = {}
    for f in d.get('forms') or []:
        for o in f.get('occurrences') or []:
            ctx = o.get('context') or ''
            m = re.search(r'(\S*)\s*\[\[(.+?)\]\]\s*(\S*)', ctx)
            if not m:
                continue
            out.setdefault((o['doc'], m.group(2)), []).append(
                {'before': m.group(1), 'after': m.group(3), 'expansion': str(o.get('expansion') or ''),
                 'sure': str(o.get('sure')), 'reason': o.get('case_reason') or ''})
    return out


def cmd_tildes():
    draft = _draft()
    occ, n_draft = [], 0
    for l in in_scope():
        for p in l['pages']:
            lines = (p.get('diplomatic') or '').split('\n')
            words = [(i, w) for i, ln in enumerate(lines) for w in ln.split()]
            for k, (i, w) in enumerate(words):
                if '~' not in w:
                    continue
                before = words[k - 1][1] if k else ''
                after = words[k + 1][1] if k + 1 < len(words) else ''
                cands = draft.get((l['uid'], w.rstrip('.,;:')), []) + draft.get((l['uid'], w), [])
                hit = next((c for c in cands if c['before'] == before), None) or \
                    next((c for c in cands if c['after'] == after), None)
                e = {'uid': l['uid'], 'page_id': p['page_id'], 'line': i + 1, 'form': w,
                     'word': sum(1 for ii, _ in words[:k] if ii == i),
                     'context': ' '.join(x for _, x in words[max(0, k - 12):k]) + ' [[' + w + ']] ' +
                                ' '.join(x for _, x in words[k + 1:k + 13])}
                if hit:
                    n_draft += 1
                    br, gaps = bracket(w, hit['expansion']) if hit['expansion'] else (None, 0)
                    e.update({'draft': hit['expansion'], 'draft_sure': hit['sure'], 'draft_reason': hit['reason'],
                              'bracketed': br, 'gaps': gaps})
                occ.append(e)
    os.makedirs(OUT, exist_ok=True)
    io.open(os.path.join(OUT, 'tildes.json'), 'w', encoding='utf-8', newline='\n').write(
        json.dumps(occ, ensure_ascii=False, indent=1) + '\n')
    print(len(occ), 'tilde forms;', n_draft, 'with a draft expansion;',
          sum(1 for e in occ if e.get('draft') and not e.get('bracketed')), 'drafts that do not bracket')


# Authored texts that may rest on a document; generated copies (site/_holdings, _places, _people,
# assets, translations) are left out: they are rebuilt from these.
AUTHORED = ['units/*/about.md', 'units/*/about_de.md', 'units/*/notes.md', 'site/eras/*.md',
            'site/de/epochen/*.md', 'site/guide/**/*.md', 'site/_data/timeline.yml', 'reference/connections.yml',
            'reference/genealogy.yml', 'reference/people_bios*.yml', 'reference/estate_tree.yml',
            'reference/site_notes_de.yml', 'reference/english_corrections.yml', 'literature/links.yml',
            'literature/*/notes.md', 'newspapers/*/notes.md', 'places/**/*.md', 'docs/NEEDS_CONFIRMATION.md',
            'site/*.md', 'site/de/*.md']


def cmd_refs():
    docs = {l['uid']: l for l in in_scope()}
    slugs = sorted({l['unit'] for l in docs.values()}, key=len, reverse=True)
    pat = re.compile(r'(?:/documents/|\b)(%s)(?:/|-0*)(\w+?)(?=[/\s"\'),.\]:;]|$)' % '|'.join(map(re.escape, slugs)))
    refs = {}
    files = sorted({f for g in AUTHORED for f in glob.glob(os.path.join(ROOT, g), recursive=True)})
    for f in files:
        rel = os.path.relpath(f, ROOT).replace(os.sep, '/')
        own = re.match(r'units/([^/]+)/about(?:_de)?\.md$', rel)
        for i, line in enumerate(io.open(f, encoding='utf-8').read().split('\n'), 1):
            found = {'%s-%s' % m.groups() for m in pat.finditer(line)}
            if own:
                found |= {'%s-%s' % (own.group(1), n) for n in re.findall(r'\[\[(\w+)\]\]', line)}
            for uid in found & set(docs):
                refs.setdefault(uid, []).append({'file': rel, 'line': i, 'text': line.strip()[:200]})
    os.makedirs(OUT, exist_ok=True)
    io.open(os.path.join(OUT, 'references.json'), 'w', encoding='utf-8', newline='\n').write(
        json.dumps(refs, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
    print(len(files), 'authored files read;', len(refs), 'of', len(docs), 'documents cited;',
          sum(len(v) for v in refs.values()), 'citing lines')


def cmd_strips(slug, web=False):
    from PIL import Image
    man = json.load(io.open(os.path.join(OUT, 'manifest.json'), encoding='utf-8'))[slug]
    raw = man['raw']
    out = os.path.join(REVIEW, slug, 'strips')
    os.makedirs(out, exist_ok=True)
    seen, problems = set(), []
    for p in man['pages']:
        if p['page_id'] in seen:
            continue
        seen.add(p['page_id'])
        src = None
        for c in ([os.path.join(raw, 'processed', p['scan']), os.path.join(raw, p['scan'])] if raw and p['scan'] else []):
            if os.path.isfile(c):
                src = c
                break
        if not src:
            if not web:
                problems.append('%s: no original scan found (%s) - run the holding\'s cutting step, or --web'
                                % (p['page_id'], p['scan']))
                continue
            src = os.path.join(ROOT, 'site', 'assets', 'scans', p['web'])
            problems.append('%s: the web copy, not the original' % p['page_id'])
        im = Image.open(src).convert('RGB')
        w, h = im.size
        n = 8                                             # a court-book page holds 25-40 lines: 4-5 in a band
        step = h / n
        pad = int(step * 0.25)                            # a quarter band of overlap above and below
        for k in range(n):
            top, bot = max(0, int(k * step) - pad), min(h, int((k + 1) * step) + pad)
            band = im.crop((0, top, w, bot))
            if w > 2400:
                band = band.resize((2400, int(band.size[1] * 2400 / w)))
            band.save(os.path.join(out, '%s_s%02d.jpg' % (p['page_id'], k + 1)), quality=90)
        im.resize((1200, int(h * 1200 / w))).save(os.path.join(out, '%s_whole.jpg' % p['page_id']), quality=85)
    print(len(seen), 'pages cut into', out)
    for x in problems:
        print('  !', x)


def cmd_texts(slug):
    """Each page's transcription as numbered lines, for the readers' briefs:
    review/latin_audit/<slug>/pages/<page id>.txt. The [DOC n] markers are kept, unnumbered, where a page
    holds more than one entry; the line numbers are the ones the readers report and Claude settles by."""
    _, lines = _corpus(slug)
    out = os.path.join(REVIEW, slug, 'pages')
    os.makedirs(out, exist_ok=True)
    pages, cur, doc = {}, None, None
    for ln in lines:
        if ln.startswith('[DOC '):
            doc = ln
            continue
        m = re.match(r'^\[PAGE (\S+)\]$', ln)
        if m:
            cur = m.group(1)
            pages.setdefault(cur, []).append(doc)
            continue
        if cur:
            pages[cur].append(ln)
    for pid, body in pages.items():
        n, txt = 0, []
        for ln in body:
            if ln is None:
                continue
            if ln.startswith('[DOC '):
                txt.append(ln)
            elif ln.strip():
                n += 1
                txt.append('%d\t%s' % (n, ln))
        io.open(os.path.join(out, pid + '.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(txt) + '\n')
    print(len(pages), 'pages written to', out)


def cmd_crop(slug, strip, box, name):
    """A tight cut of a band, for Claude's settling and for the spot sheet: box = x0,y0,x1,y1 as fractions
    of the band; written to review/latin_audit/crops/<slug>_<name>.jpg (the sheet's folder)."""
    from PIL import Image
    im = Image.open(os.path.join(REVIEW, slug, 'strips', strip))
    w, h = im.size
    x0, y0, x1, y1 = [float(v) for v in box.split(',')]
    c = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    if c.size[0] < 1400:
        c = c.resize((1400, int(c.size[1] * 1400 / c.size[0])))
    out = os.path.join(REVIEW, 'crops')
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, '%s_%s.jpg' % (slug, name))
    c.save(p, quality=90)
    print(p)


def _corpus(slug):
    path = os.path.join(ROOT, 'units', slug, 'corpus.txt')
    return path, io.open(path, encoding='utf-8').read().split('\n')


def cmd_apply(slug, write=False, name='latin_audit.json'):
    rec = json.load(io.open(os.path.join(ROOT, 'units', slug, 'intake', name), encoding='utf-8'))
    path, lines = _corpus(slug)
    pad_of = {}
    for l in in_scope() + [x for x in _letters() if x['unit'] == slug]:
        for p in l['pages']:
            pad_of.setdefault(p['page_id'], (l['pad'], p['page']))
    spans, cur = {}, None                     # page id -> [line indexes]
    for i, ln in enumerate(lines):
        m = re.match(r'^\[PAGE (\S+)\]$', ln)
        if m:
            cur = m.group(1)
            continue
        if ln.startswith('[DOC '):
            continue
        if cur:
            spans.setdefault(cur, []).append(i)
    log, bad = [], []
    for kind, source in (('ROWS', 'Latin audit, read on the scan'), ('EXPAND', 'Latin audit, expansion')):
        for pid, old, new, why in rec.get(kind, []):
            hits = [i for i in spans.get(pid, []) if old in lines[i]]
            if sum(lines[i].count(old) for i in hits) != 1:
                bad.append('%s %s: found %d time(s): %r' % (kind, pid, sum(lines[i].count(old) for i in hits), old[:70]))
                continue
            lines[hits[0]] = lines[hits[0]].replace(old, new)
            pad, page = pad_of.get(pid, ('%s-?' % slug, '?'))
            key = hashlib.md5(('%s|%s|%s' % (pid, old, new)).encode()).hexdigest()[:8]
            log.append([key, pad, page, old, new, '%s: %s -> %s' % (pid, old[:60], new[:60]), '%s: %s' % (source, why)])
    print(len(rec.get('ROWS', [])), 'corrections,', len(rec.get('EXPAND', [])), 'expansions;', len(bad), 'do not apply')
    for b in bad:
        print('  ', b)
    if bad or not write:
        return
    io.open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    dpath = os.path.join(ROOT, 'units', slug, 'transcription_decisions.csv')
    new_file = not os.path.exists(dpath)
    with io.open(dpath, 'a', encoding='utf-8-sig' if new_file else 'utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        if new_file:
            w.writerow(['key', 'pad', 'page', 'transcribed', 'proposed', 'decision', 'why'])
        w.writerows(log)
    print('written and logged')


def cmd_impact(slug):
    """For each row of the holding's latin_audit.json: the document, and every authored text that cites
    it (references.json), with the lines that contain the old word - the list section 5 of the plan works
    through. Expansions alone are listed only by count: they change no fact."""
    rec = json.load(io.open(os.path.join(ROOT, 'units', slug, 'intake', 'latin_audit.json'), encoding='utf-8'))
    refs = json.load(io.open(os.path.join(OUT, 'references.json'), encoding='utf-8'))
    uid_of = {}
    for l in in_scope():
        for p in l['pages']:
            uid_of.setdefault(p['page_id'], []).append(l['uid'])
    out = ['# Impact of the Latin audit: %s' % slug, '',
           '%d corrections, %d expansions (the expansions change no fact and are not listed).' %
           (len(rec.get('ROWS', [])), len(rec.get('EXPAND', []))), '']
    for pid, old, new, why in rec.get('ROWS', []):
        uids = uid_of.get(pid, [])
        out.append('## %s: %s -> %s' % (pid, old, new))
        out.append('Why: %s. Documents: %s. Check its English, both summaries and the claim check.' %
                   (why, ', '.join(uids)))
        words = [w for w in re.findall(r'\w{4,}', old) if w not in new]
        for uid in uids:
            for r in refs.get(uid, []):
                mark = ' **(has "%s")**' % '/'.join(words) if any(w.lower() in r['text'].lower() for w in words) else ''
                out.append('- `%s:%d`%s %s' % (r['file'], r['line'], mark, r['text']))
        out.append('')
    os.makedirs(os.path.join(REVIEW, slug), exist_ok=True)
    p = os.path.join(REVIEW, slug, 'impact.md')
    io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('written', p)


def cmd_sheet():
    """review/latin_audit/questions.csv (holding, page_id, uid, crop, transcribed, question, options) -> the
    spot sheet review/latin_audit/sheet.html: a card per question, the crop as a CSS background (no
    script: WORKING_NOTES, the Gr.75 sheet), grouped by holding; the editor answers by number in chat."""
    import html
    rows = list(csv.DictReader(io.open(os.path.join(REVIEW, 'questions.csv'), encoding='utf-8-sig')))
    css = ('body{font:16px/1.45 Georgia,serif;max-width:60rem;margin:2rem auto;padding:0 1rem;color:#222;background:#fff}'
           '.c{border:1px solid #ccc;border-radius:6px;padding:1rem;margin:1rem 0}'
           '.im{width:100%;height:14rem;background-size:contain;background-repeat:no-repeat;background-position:left center;'
           'border:1px solid #eee;margin:.5rem 0}h2{margin-top:2.5rem}code{background:#f4f4f4;padding:0 .2em}')
    out = ['<!doctype html><meta charset="utf-8"><title>Latin audit spot sheet</title><style>%s</style>' % css,
           '<h1>The Latin audit: questions for the editor</h1>',
           '<p>%d questions. Answer by number in the chat, e.g. "12: as transcribed; 13: pro".</p>' % len(rows)]
    import base64
    from PIL import Image

    def data_uri(rel):
        """The crop inside the file (the app's viewer loads no separate files and runs no script)."""
        p = os.path.join(REVIEW, rel)
        if not rel or not os.path.isfile(p):
            return ''
        im = Image.open(p).convert('RGB')
        if im.size[0] > 1400:
            im = im.resize((1400, int(im.size[1] * 1400 / im.size[0])))
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=72)
        return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode('ascii')

    cur = None
    for k, r in enumerate(rows, 1):
        if r['holding'] != cur:
            cur = r['holding']
            out.append('<h2>%s</h2>' % html.escape(cur))
        r = dict(r, crop=data_uri(r['crop']))
        out.append('<div class="c"><b>%d.</b> %s, page %s<div class="im" style="background-image:url(\'%s\')"></div>'
                   '<p>Transcribed: <code>%s</code></p><p>%s</p><p>Options: %s</p></div>' % (
                       k, html.escape(r['uid']), html.escape(r['page_id']), html.escape(r['crop']),
                       html.escape(r['transcribed']), html.escape(r['question']), html.escape(r['options'])))
    p = os.path.join(REVIEW, 'sheet.html')
    io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('written', p, '-', len(rows), 'questions')


def _qkey(r):
    return hashlib.md5(('%s|%s|%s|%s' % (r['holding'], r['page_id'], r['transcribed'], r['question'][:80]))
                       .encode('utf-8')).hexdigest()[:10]


def _row_slug(r):
    """The holding a question belongs to: from its uid (slug-n), else from its crop's file name."""
    for cand in (r.get('uid', '').rsplit('-', 1)[0], r.get('uid', ''),
                 os.path.basename(r.get('crop', '')).split('_')[0]):
        if cand and os.path.isdir(os.path.join(ROOT, 'units', cand)):
            return cand
    return ''


def _page_file(slug, page_id):
    """The whole page for the editor (the editor, 2026-11-27: whole pages, not Claude's crops): the
    original scan as cut at the folds (<raw>/processed/<scan>), else the original, else the strips' copy."""
    man = json.load(io.open(os.path.join(OUT, 'manifest.json'), encoding='utf-8')).get(slug)
    if not man or not re.match(r'^[\w.-]+$', page_id):
        return None
    scan = next((p['scan'] for p in man['pages'] if p['page_id'] == page_id), None)
    for c in ([os.path.join(man['raw'], 'processed', scan), os.path.join(man['raw'], scan)] if man.get('raw') and scan else []):
        if os.path.isfile(c):
            return c
    c = os.path.join(REVIEW, slug, 'strips', page_id + '_whole.jpg')
    return c if os.path.isfile(c) else None


_PAGES = {}


def _page_text(slug, page_id):
    """The page's text as the corpus now stands (after the audit's corrections), one string."""
    if slug not in _PAGES:
        pages, cur = {}, None
        for ln in _corpus(slug)[1]:
            m = re.match(r'^\[PAGE (\S+)\]$', ln)
            if m:
                cur = m.group(1)
                continue
            if ln.startswith('[DOC ') or not cur:
                continue
            pages.setdefault(cur, []).append(ln.strip())
        _PAGES[slug] = {k: ' '.join(x for x in v if x) for k, v in pages.items()}
    return _PAGES[slug].get(page_id, '')


def _context_html(slug, page_id, transcribed, width=160):
    """The editor (2026-11-27): the card quotes the text around the place, with the place highlighted.
    Each piece of `transcribed` (split at "...") is looked up in the page's current text; the quotation runs
    `width` characters before the first piece and after the last, cut at word boundaries."""
    import html
    text = _page_text(slug, page_id) if slug else ''
    parts = [re.sub(r'^\(.*?\)\s*', '', p).strip(' .,') for p in re.split(r'\s*\.\.\.\s*|\s*…\s*', transcribed)]
    parts = [p for p in parts if len(p) > 2]
    spans = []
    for p in parts:
        i = text.find(p)
        if i < 0 and len(p.split()) > 2:                # the first words, if the whole piece has moved
            p = ' '.join(p.split()[:3])
            i = text.find(p)
        if i >= 0:
            spans.append((i, i + len(p)))
    if not spans:
        return '<code>%s</code> <small>(not found in the present text of the page)</small>' % html.escape(transcribed)
    spans.sort()
    a, b = max(0, spans[0][0] - width), min(len(text), spans[-1][1] + width)
    a = text.rfind(' ', 0, a) + 1 if a > 0 else 0
    sp = text.find(' ', b)
    b = sp if sp > 0 else len(text)
    out, pos = [], a
    for s, e in spans:
        if s < pos:
            continue
        out.append(html.escape(text[pos:s]) + '<mark>' + html.escape(text[s:e]) + '</mark>')
        pos = e
    out.append(html.escape(text[pos:b]))
    return '<code>%s%s%s</code>' % ('… ' if a > 0 else '', ''.join(out), ' …' if b < len(text) else '')


def _big_crop(slug, page_id, band):
    """A larger crop for the editor (2026-11-27: "Keep your crops and the links, just make the crops larger"):
    the question's band with the band above and below, about three eighths of the page, from the original
    scan, at 1600 pixels wide. JPEG bytes, or None."""
    from PIL import Image
    p = _page_file(slug, page_id)
    if not p:
        return None
    im = Image.open(p).convert('RGB')
    w, h = im.size
    k = min(8, max(1, int(band)))
    top, bot = max(0, int((k - 2) * h / 8 - h / 32)), min(h, int((k + 1) * h / 8 + h / 32))
    c = im.crop((0, top, w, bot))
    if c.size[0] > 1600:
        c = c.resize((1600, int(c.size[1] * 1600 / c.size[0])))
    buf = io.BytesIO()
    c.save(buf, 'JPEG', quality=82)
    return buf.getvalue()


def cmd_serve(port=4102, read=False):
    """The spot sheet with buttons, as queries.py serves its sheets: every answer is saved at once to
    review/latin_audit/answers.json. `--read` prints the answers. The page needs this program running
    (it is opened in the browser at the address it prints, not as a file)."""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import html
    rows = list(csv.DictReader(io.open(os.path.join(REVIEW, 'questions.csv'), encoding='utf-8-sig')))
    store = os.path.join(REVIEW, 'answers.json')
    answers = json.load(io.open(store, encoding='utf-8')) if os.path.exists(store) else {}
    if read:
        done = [(k, r) for k, r in enumerate(rows, 1) if answers.get(_qkey(r), {}).get('reading')]
        print('%d of %d answered' % (len(done), len(rows)))
        for k, r in done:
            x = answers[_qkey(r)]
            got = {'__other__': 'other: %s' % (x.get('other') or '(not given)'),
                   '__unsure__': "can't tell"}.get(x['reading'], x['reading'])
            print('  %d. %s %s: %s -> %s%s' % (k, r['holding'], r['page_id'], r['transcribed'][:60], got,
                                               '  [%s]' % x['note'] if x.get('note') else ''))
        return

    def page():
        css = (':root{--bg:#fbfaf7;--fg:#222;--mute:#666;--line:#ddd;--ok:#2a6b2a;--card:#fff;--link:#1f5fa8;--visited:#6a3d9a;--mark:#ffe08a;--markfg:#000}'
               '@media (prefers-color-scheme:dark){:root{--bg:#1b1a18;--fg:#e8e6e1;--mute:#9a968e;--line:#3a3834;--ok:#7fc27f;--card:#242320;--link:#8cc4ff;--visited:#c9a6ff;--mark:#8a6400;--markfg:#fff}}'
               'body{font:16px/1.5 Georgia,serif;max-width:60rem;margin:2em auto;padding:0 16px;background:var(--bg);color:var(--fg)}'
               '.row{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:12px 14px;margin:14px 0}'
               '.row.done{border-left:5px solid var(--ok)}img{max-width:100%;border:1px solid var(--line);margin:.5em 0}'
               'code{font-family:ui-monospace,Consolas,monospace;font-size:14px;overflow-wrap:anywhere}'
               'button{font:inherit;padding:4px 12px;margin:0 6px 6px 0;cursor:pointer;border-radius:4px;border:1px solid var(--line);'
               'background:var(--bg);color:var(--fg);text-align:left}button.on{background:var(--fg);color:var(--bg)}'
               'input{font:inherit;width:100%;box-sizing:border-box;margin-top:4px;padding:4px 6px;background:var(--bg);color:var(--fg);'
               'border:1px solid var(--line)}#status{position:sticky;top:0;background:var(--bg);padding:6px 0;color:var(--mute)}h2{margin-top:2.2rem}a{color:var(--link)}a:visited{color:var(--visited)}mark{background:var(--mark);color:var(--markfg);padding:0 2px;border-radius:2px}')
        out = ['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
               '<title>Latin audit questions</title><style>%s</style>' % css,
               '<h1>The Latin audit: %d questions</h1>' % len(rows),
               '<p>Each card shows the place on the page, what the transcription has, and the question. Pick an answer, '
               'or type it under "Something else". "Can\'t tell" is a fine answer. Answers save as you go.</p>',
               '<div id="status"></div>']
        cur = None
        for k, r in enumerate(rows, 1):
            if r['holding'] != cur:
                cur = r['holding']
                out.append('<h2>%s</h2>' % html.escape(cur))
            key = _qkey(r)
            a = answers.get(key, {})
            opts = [o.strip() for o in r['options'].split('|') if o.strip()]
            btns = ''.join('<button data-v="%s">%s</button>' % (html.escape(o, True), html.escape(o)) for o in opts)
            btns += '<button data-v="__unsure__">Can\'t tell</button><button data-v="__other__">Something else</button>'
            slug = _row_slug(r)
            img = ''
            if slug and r['page_id']:
                cu = '/crop/%s/%s/%s' % (slug, html.escape(r['page_id']), html.escape(r.get('band') or '4'))
                img = ('<a href="%s" target="_blank"><img src="%s" alt="part of the page" loading="lazy"></a>'
                       '<p><a href="/page/%s/%s" target="_blank">Open the whole page (%s) in a new tab</a></p>'
                       % (cu, cu, slug, html.escape(r['page_id']), html.escape(r['page_id'])))
            out.append('<div class="row" data-key="%s" data-v="%s"><b>%d.</b> <small>%s, page %s</small>%s'
                       '<p>Transcribed: %s</p><p>%s</p><div>%s</div>'
                       '<input placeholder="Something else: type the reading" value="%s" %s>'
                       '<input placeholder="Note (optional)" value="%s"></div>' % (
                           key, html.escape(a.get('reading', ''), True), k, html.escape(r['uid']), html.escape(r['page_id']),
                           img, _context_html(slug, r['page_id'], r.get('find') or r['transcribed']), html.escape(r['question']), btns,
                           html.escape(a.get('other', ''), True), '' if a.get('reading') == '__other__' else 'hidden',
                           html.escape(a.get('note', ''), True)))
        out.append('''<script>
const st=document.getElementById('status');
function count(){const r=document.querySelectorAll('.row'),d=[...r].filter(x=>x.dataset.v).length;st.textContent=d+' of '+r.length+' answered';}
async function save(row){
  const [other,note]=row.querySelectorAll('input');
  const body={key:row.dataset.key,reading:row.dataset.v||'',other:other.value,note:note.value};
  try{const r=await fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      if(!r.ok)throw 0;count();}catch(e){st.textContent='Not saved - is latin_audit.py serve still running?';}
}
document.querySelectorAll('.row').forEach(row=>{
  const bs=[...row.querySelectorAll('button')],[other,note]=row.querySelectorAll('input');
  function set(v){row.dataset.v=v;row.classList.toggle('done',!!v);
    bs.forEach(b=>b.classList.toggle('on',b.dataset.v===v));other.hidden=v!=='__other__';if(v==='__other__')other.focus();}
  if(row.dataset.v)set(row.dataset.v);
  bs.forEach(b=>b.onclick=()=>{set(b.dataset.v);save(row);});
  let t;[other,note].forEach(i=>i.oninput=()=>{clearTimeout(t);t=setTimeout(()=>save(row),400);});
});
count();
</script></html>''')
        return '\n'.join(out)

    class H(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_GET(self):
            if self.path.startswith('/crop/'):
                parts = self.path.split('/')[2:5]
                b = _big_crop(*parts) if len(parts) == 3 and parts[2].isdigit() else None
                if not b:
                    self.send_error(404)
                    return
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(b)
                return
            if self.path.startswith('/page/'):
                p = _page_file(*self.path.split('/')[2:4])
                if not p:
                    self.send_error(404)
                    return
                self.send_response(200)
                self.send_header('Content-Type', 'image/png' if p.lower().endswith('.png') else 'image/jpeg')
                self.end_headers()
                self.wfile.write(open(p, 'rb').read())
                return
            if self.path.startswith('/img/'):
                p = os.path.join(REVIEW, 'crops', os.path.basename(self.path))
                if not os.path.isfile(p):
                    self.send_error(404)
                    return
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(open(p, 'rb').read())
                return
            body = page().encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            d = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            answers[d['key']] = {'reading': d.get('reading', ''), 'other': d.get('other', ''), 'note': d.get('note', '')}
            with io.open(store, 'w', encoding='utf-8', newline='\n') as f:
                json.dump(answers, f, ensure_ascii=False, indent=1)
            self.send_response(204)
            self.end_headers()

    print('the Latin audit questions at http://127.0.0.1:%d/  -  answers go to %s' % (port, store))
    HTTPServer(('127.0.0.1', port), H).serve_forever()


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == 'scope':
        cmd_scope()
    elif a[0] == 'manifest':
        cmd_manifest()
    elif a[0] == 'tildes':
        cmd_tildes()
    elif a[0] == 'refs':
        cmd_refs()
    elif a[0] == 'strips':
        cmd_strips(a[1], '--web' in a)
    elif a[0] == 'crop':
        cmd_crop(a[1], a[2], a[3], a[4])
    elif a[0] == 'texts':
        cmd_texts(a[1])
    elif a[0] == 'apply':
        cmd_apply(a[1], '--write' in a, a[a.index('--file') + 1] if '--file' in a else 'latin_audit.json')
    elif a[0] == 'impact':
        cmd_impact(a[1])
    elif a[0] == 'sheet':
        cmd_sheet()
    elif a[0] == 'serve':
        cmd_serve(int(a[a.index('--port') + 1]) if '--port' in a else 4102, '--read' in a)
    else:
        sys.exit(__doc__)
