# -*- coding: utf-8 -*-
"""Harvest the Latin court books for the reading guide (docs/COURT_RECORDS_GUIDE_PLAN.md).

    python3 pipeline/guide/harvest.py

Writes, into reference/guide/ (data for the guide, every row pointing to its document):
  abbreviations.yml  every tilde form of the Latin court-book documents, with each occurrence's
                     context (six words either side) and the document; `expansion` is left empty
                     for the occurrence to be expanded by its case, then checked
  difficult.yml      the readings the checks changed (transcription_decisions.csv) and the graded
                     changes (intake/changes.yml): what was written, what the page has, and why;
                     `lang` is the document's language (la, pl ...), so the Latin part of the guide
                     and the Polish part each take their own (the editor, 2026-11-26)
  formulas.yml       the opening and the closing words of every Latin document, by kind (doc_type)
Only documents whose language is Latin (rulings.yml documents.language, or the holding's first
language) are taken. Free; no model.
"""
import csv, glob, io, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'reference', 'guide')
COURT = re.compile(r'protocollon|inducta|Relation|Inscript|Decret|Resign|Oblat', re.I)


def units():
    for path in sorted(glob.glob(os.path.join(ROOT, 'units', '*', 'unit.yml'))):
        u = yaml.safe_load(io.open(path, encoding='utf-8'))
        if COURT.search(str(u.get('archive_title', ''))) and 'la' in (u.get('languages') or []):
            yield u['slug'], u


def languages(slug, unit):
    """{document number: language} for every document of the holding."""
    rul = yaml.safe_load(io.open(os.path.join(ROOT, 'units', slug, 'rulings.yml'), encoding='utf-8')) or {}
    lang = (rul.get('documents') or {}).get('language') or {}
    first = (unit.get('languages') or ['la'])[0]
    nums = re.findall(r'(?m)^\[DOC (\S+)\]$', io.open(os.path.join(ROOT, 'units', slug, 'corpus.txt'), encoding='utf-8').read())
    return {n: lang.get(n, first) for n in nums}


def docs(slug, unit):
    rul = yaml.safe_load(io.open(os.path.join(ROOT, 'units', slug, 'rulings.yml'), encoding='utf-8')) or {}
    d = rul.get('documents') or {}
    lang, kind = d.get('language') or {}, d.get('doc_type') or {}
    first = (unit.get('languages') or ['la'])[0]
    cur, out = None, {}
    for line in io.open(os.path.join(ROOT, 'units', slug, 'corpus.txt'), encoding='utf-8').read().split('\n'):
        m = re.match(r'^\[DOC (\S+)\]$', line)
        if m:
            cur = m.group(1); out[cur] = []; continue
        if line.startswith('[PAGE') or cur is None or not line.strip():
            continue
        out[cur].append(line)
    for n, lines in out.items():
        if lang.get(n, first) == 'la':
            yield n, kind.get(n, 'letter'), ' '.join(lines)


def main():
    os.makedirs(OUT, exist_ok=True)
    abbr, forms, diff = {}, {}, []
    for slug, unit in units():
        for n, kind, text in docs(slug, unit):
            uid = '%s-%s' % (slug, n)
            words = text.split()
            for i, w in enumerate(words):
                if '~' in w:
                    tok = re.sub(r'^[^\w\[]+|[^\w~\]?]+$', '', w)
                    abbr.setdefault(tok, []).append({'doc': uid, 'kind': kind,
                        'context': ' '.join(words[max(0, i - 6):i]) + ' [[' + w + ']] ' + ' '.join(words[i + 1:i + 7]),
                        'expansion': ''})
            forms.setdefault(kind, []).append({'doc': uid, 'opening': ' '.join(words[:40]), 'closing': ' '.join(words[-30:])})
        langs = languages(slug, unit)
        p = os.path.join(ROOT, 'units', slug, 'transcription_decisions.csv')
        if os.path.isfile(p):
            for r in csv.DictReader(io.open(p, encoding='utf-8-sig')):
                n = r['pad'].rsplit('-', 1)[-1].lstrip('0') or '0'
                diff.append({'doc': r['pad'], 'lang': langs.get(n, '?'), 'was': r['transcribed'], 'now': r['proposed'],
                             'why': r['why'], 'source': 'check'})
        p = os.path.join(ROOT, 'units', slug, 'intake', 'changes.yml')
        if os.path.isfile(p):
            data = yaml.safe_load(io.open(p, encoding='utf-8')) or {}
            for r in (data.get('changes') or []) if isinstance(data, dict) else data:
                if isinstance(r, dict):
                    one = set(langs.values())
                    diff.append({'doc': slug, 'lang': one.pop() if len(one) == 1 else 'holding: ' + '/'.join(sorted(one)),
                                 'was': str(r.get('was', '')), 'now': str(r.get('now', '')),
                                 'why': str(r.get('what', '')), 'grade': r.get('importance', ''), 'source': 'changes'})
    rows = [{'form': k, 'count': len(v), 'occurrences': v} for k, v in sorted(abbr.items(), key=lambda kv: (-len(kv[1]), kv[0]))]
    for name, data in (('abbreviations.yml', rows), ('formulas.yml', forms), ('difficult.yml', diff)):
        with io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=110)
    print('%d tilde forms (%d occurrences), %d kinds of entry (%d documents), %d logged changes'
          % (len(rows), sum(r['count'] for r in rows), len(forms), sum(len(v) for v in forms.values()), len(diff)))


if __name__ == '__main__':
    main()
