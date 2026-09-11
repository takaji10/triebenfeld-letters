# -*- coding: utf-8 -*-
"""
The queryable dataset: per-document files and standing indexes.

corpus/letters.json is a single array of every document in the project. To ask
what one holding says about Trąbczyn between 1804 and 1806 you have to load all
of it and rebuild the joins by hand. This writes the same content in a shape you
can scope a question against before opening anything:

    corpus/index/documents.json     the manifest - one compact row per document
    corpus/index/people.json        entity -> every mention, with its location
    corpus/index/places.json        place  -> the documents written there
    corpus/index/dates.json         year and month -> uids
    corpus/index/relations.json     document -> document, with the kind of link
    corpus/index/uncertainties.json every surviving marker, with its context
    corpus/documents/<uid>.json     one document, whole
    corpus/text/<uid>.txt           the same as plain text, for grepping

index/documents.json is the entry point: it carries only the fields worth
narrowing on, so an agent reaches a working set without opening a document file.

Nothing here is authored. Every value comes from corpus/letters.json, which is
itself derived from the units' corpus.txt, so a rebuild reproduces the lot.
letters.json is left in place: the site and the verifier still read it.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import io, sys, os, json, re
from collections import defaultdict, Counter
from entities import load_people, load_places, mentions
import unitlib
import yaml


def load_translations():
    """Published English, keyed by pad.

    It lives in site/_data/translations/ because that is where the website
    reads it, but it is not a site artefact: it is part of the edition. Kept
    out of the dataset it was searchable by nothing except the website.
    """
    d = os.path.join(ROOT, 'site', '_data', 'translations')
    out = {}
    if not os.path.isdir(d):
        return out
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.yml'):
            continue
        with open(os.path.join(d, fn), encoding='utf-8') as f:
            y = yaml.safe_load(f) or {}
        out[fn[:-4]] = y
    return out


def load_summaries():
    """English and German summaries, keyed by pad."""
    out = {}
    for lang, fn in (('en', 'summaries.yml'), ('de', 'summaries_de.yml')):
        p = os.path.join(ROOT, 'site', '_data', fn)
        if not os.path.isfile(p):
            continue
        with open(p, encoding='utf-8') as f:
            out[lang] = yaml.safe_load(f) or {}
    return out

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORPUS = os.path.join(ROOT, 'corpus')
INDEX = os.path.join(CORPUS, 'index')
DOCS = os.path.join(CORPUS, 'documents')
TEXT = os.path.join(CORPUS, 'text')

# Every marker the transcription uses to admit doubt or damage.
MARKER = re.compile(r'\[[^\]]*(?:\?|\.\.\.)[^\]]*\]')


def write_json(path, obj):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, sort_keys=False)


def main():
    for d in (INDEX, DOCS, TEXT):
        os.makedirs(d, exist_ok=True)
    with open(os.path.join(CORPUS, 'letters.json'), encoding='utf-8') as f:
        recs = json.load(f)
    people = load_people()
    canon = load_places()
    trans = load_translations()
    summaries = load_summaries()
    print(f'{len(recs)} documents, {len(people)} people in the authority')

    manifest, people_idx, place_idx = [], defaultdict(list), defaultdict(list)
    date_idx, rel_idx, unc_idx = defaultdict(list), [], []
    n_mentions = 0
    _REPO_OF = {u.slug: (u.get('repository') or '') for u in unitlib.load_units()}

    for r in recs:
        uid = r['uid']
        ms = mentions(r, people)
        n_mentions += len(ms)
        place = canon.get(r['place'], r['place']) or 'Unknown'

        # --- the document, whole -------------------------------------------
        tr = trans.get(r['pad']) or {}
        segs = tr.get('segments') or []
        en = '\n\n'.join((x.get('en') or '').strip() for x in segs
                         if (x.get('en') or '').strip())
        sum_en = (summaries.get('en', {}) or {}).get(r['pad']) or ''
        sum_de = (summaries.get('de', {}) or {}).get(r['pad']) or ''

        # Who and where the ENGLISH names, tied to the same entity slugs as the
        # German. Without this the translation is a flat string: a reader of the
        # English cannot be shown who a passage is about, and the dataset cannot
        # be asked the question either - the forms differ (Wien -> Vienna), so
        # grepping the English is not a substitute.
        en_mentions, en_names = [], []
        for seg in segs:
            for n in (seg.get('names') or []):
                de_form = (n.get('de') or '').strip()
                en_form = (n.get('en') or '').strip()
                if not en_form:
                    continue
                hit = next((m for m in ms if m['surface'] == de_form
                            or m['display'] == de_form), None)
                en_mentions.append({
                    'entity': hit['entity'] if hit else '',
                    'display': hit['display'] if hit else en_form,
                    'kind': (hit or {}).get('kind') or n.get('kind') or '',
                    'surface_de': de_form, 'surface_en': en_form,
                    'page': seg.get('page'),
                })
                en_names.append(en_form)

        doc = dict(r)
        doc['mentions'] = ms
        doc['mentions_english'] = en_mentions
        doc['place_canonical'] = place
        doc['translation_status'] = tr.get('status') or 'untranslated'
        doc['translation'] = segs
        doc['text_english'] = en
        doc['summary_en'] = sum_en
        doc['summary_de'] = sum_de
        write_json(os.path.join(DOCS, uid + '.json'), doc)

        # --- the plain-text mirror -----------------------------------------
        # Without a full-text index, grep is the search; grepping JSON gives
        # hits nobody can read. This gives a hit that can be quoted and cited.
        head = [f'# {uid}  {r["letter_id"]}  {r.get("doc_type") or "document"}',
                f'# {r.get("date_iso") or "undated"}  {place or ""}'.rstrip(),
                f'# {r["permalink"]}', '']
        # German first, then the summary and the English under their own
        # headings, so a grep hit says which language it was found in.
        body = ['\n'.join(head), r['text']]
        if sum_en:
            body.append('\n--- SUMMARY (English) ---\n' + sum_en)
        if en:
            body.append('\n--- ENGLISH TRANSLATION (%s) ---\n%s'
                        % (doc['translation_status'], en))
        with open(os.path.join(TEXT, uid + '.txt'), 'w',
                  encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(body) + '\n')

        # --- indexes --------------------------------------------------------
        marks = MARKER.findall(r['text'])
        manifest.append({
            'uid': uid, 'unit': r['unit'], 'letter_id': r['letter_id'],
            'doc_type': r.get('doc_type') or '', 'language': r.get('language') or 'de',
            # era and themes travel with the document; repository is a property
            # of the holding, joined from the unit record rather than repeated
            # on every row of build_db's flat table.
            'era': r.get('era') or '', 'themes': r.get('themes') or [],
            'repository': _REPO_OF.get(r['unit'], ''),
            'date_iso': r.get('date_iso') or '', 'date_precision': r.get('date_precision') or '',
            'date_source': r.get('date_source') or '', 'place': place,
            'n_pages': len(r.get('pages') or []), 'n_lines': r.get('n_lines') or 0,
            'uncertainty_count': len(marks), 'has_damage': bool(r.get('has_damage')),
            'mentions': len({m['entity'] for m in ms}),
            'translation_status': doc['translation_status'],
            'has_summary': bool(sum_en),
            'title': f'{(r.get("doc_type") or "document").replace("_", " ")} {r["letter_id"]}',
            'path': f'documents/{uid}.json', 'text_path': f'text/{uid}.txt',
            'permalink': r['permalink'],
        })
        for m in en_mentions:
            if m['entity']:
                people_idx[m['entity']].append({
                    'uid': uid, 'surface': m['surface_en'], 'page': m['page'],
                    'page_id': '', 'line': 0, 'language': 'en',
                })
        for m in ms:
            # Both numbers. `line` is the unit-absolute one every tool and every
            # transcription decision is keyed to; `doc_line` is what the site
            # shows, numbered from 1 in each document. The published page
            # carries only the second, so this index is where a citation in one
            # scheme is turned into the other.
            people_idx[m['entity']].append({
                'uid': uid, 'surface': m['surface'], 'page': m['page'],
                'page_id': m['page_id'], 'line': m['line'],
                'doc_line': m.get('doc_line'),
            })
        place_idx[place].append(uid)
        if r.get('date_iso'):
            date_idx[r['date_iso'][:4]].append(uid)
        for rel in (r.get('relations') or []):
            rel_idx.append({'from': uid, 'kind': rel.get('kind', ''),
                            'to': f'{r["unit"]}-{rel.get("target", "")}',
                            'note': rel.get('note', '')})
        if r.get('duplicate_of'):
            rel_idx.append({'from': uid, 'kind': 'duplicate_of',
                            'to': f'{r["unit"]}-{r["duplicate_of"]}', 'note': ''})
        # every surviving marker, with the line it sits on
        for p in (r.get('pages') or []):
            for i, line in enumerate(p['diplomatic'].split('\n')):
                for mk in MARKER.findall(line):
                    unc_idx.append({
                        'uid': uid, 'marker': mk, 'page': p['page'],
                        'page_id': p.get('page_id', ''), 'line': p['line_start'] + i,
                        'doc_line': p['doc_line_start'] + i,
                        'context': line.strip()[:120],
                    })

    disp = {slug: d for slug, d, _ in people}
    write_json(os.path.join(INDEX, 'documents.json'), manifest)
    write_json(os.path.join(INDEX, 'people.json'),
               [{'entity': k, 'display': disp.get(k, k), 'count': len(v),
                 'documents': sorted({m['uid'] for m in v}), 'mentions': v}
                for k, v in sorted(people_idx.items(), key=lambda kv: -len(kv[1]))])
    write_json(os.path.join(INDEX, 'places.json'),
               [{'place': k, 'count': len(v), 'documents': v}
                for k, v in sorted(place_idx.items(),
                                   key=lambda kv: (kv[0] == 'Unknown', -len(kv[1])))])
    write_json(os.path.join(INDEX, 'dates.json'),
               [{'year': k, 'count': len(v), 'documents': sorted(v)}
                for k, v in sorted(date_idx.items())])
    write_json(os.path.join(INDEX, 'relations.json'), rel_idx)
    write_json(os.path.join(INDEX, 'uncertainties.json'), unc_idx)

    # The manifest's uncertainty_count must equal the rows in the uncertainty
    # index, or one of the two is lying about where the evidence is weak.
    a = sum(d['uncertainty_count'] for d in manifest)
    b = len(unc_idx)
    print(f'  documents/  {len(manifest)} files')
    print(f'  text/       {len(manifest)} files')
    print(f'  people      {len(people_idx)} entities, {n_mentions} mentions')
    print(f'  places      {len(place_idx)}')
    print(f'  dates       {len(date_idx)} years')
    print(f'  relations   {len(rel_idx)}')
    print(f'  uncertainty {b} markers')
    print(f'VERIFY manifest uncertainty total == index rows : {a == b} ({a} vs {b})')
    assert a == b, 'uncertainty counts disagree'
    missing = [d['uid'] for d in manifest
               if not os.path.isfile(os.path.join(CORPUS, d['path']))]
    print(f'VERIFY every manifest row has its document file  : {not missing}')
    assert not missing
    uids = {d['uid'] for d in manifest}
    bad = [r for r in rel_idx if r['to'] not in uids]
    print(f'VERIFY every relation names a document that exists: {not bad}'
          + (f'  {bad[:3]}' if bad else ''))


if __name__ == '__main__':
    main()
