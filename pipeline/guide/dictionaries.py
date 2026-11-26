# -*- coding: utf-8 -*-
"""Word lists for the reading guide (docs/COURT_RECORDS_GUIDE_PLAN.md, "Dictionaries").

    python3 pipeline/guide/dictionaries.py

Writes reference/guide/places_found.yml from the Latin court-book documents:
  matched     every place of reference/places.yml whose pattern finds it in the Latin, with each
              surface form as written (Coninen~, Coninensibus, Trąmpczyn ...), its count and documents
  candidates  the place-like words no pattern finds: Latin place adjectives (-ensis, -iensis and
              their cases, and the abbreviated -en~ / -ien~ / -ven~), with count, documents and a
              context, for Claude to identify (Nieszczevicen~ = of Niszczewice)
The identifications and the Polish and modern names are written by hand into
reference/guide/places_latin.yml, which the guide's dictionary is built from. Free; no model.
"""
import io, os, re, sys
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import harvest  # noqa: E402

ADJ = re.compile(r"\b[A-ZŁŚŻ][\w~]*?(?:i?ens(?:is|i|em|ium|ibus|e|es)|i?en~|ven~|vien~|ens~)(?![\w~])")


def main():
    places = yaml.safe_load(io.open(os.path.join(ROOT, 'reference', 'places.yml'), encoding='utf-8'))['places']
    pats = {}
    for slug, p in places.items():
        if p.get('match'):
            try:
                pats[slug] = re.compile(r'(?<![\w~])(?:%s)' % p['match'])
            except re.error:
                pass
    matched, cand, taken = {}, {}, set()
    for slug, unit in harvest.units():
        for n, kind, text in harvest.docs(slug, unit):
            uid = '%s-%s' % (slug, n)
            for ps, rx in pats.items():
                for m in rx.finditer(text):
                    form = m.group(0)
                    taken.add((uid, m.start()))
                    e = matched.setdefault(ps, {'place': places[ps].get('display', ps), 'forms': {}})
                    f = e['forms'].setdefault(form, {'count': 0, 'docs': []})
                    f['count'] += 1
                    if uid not in f['docs']:
                        f['docs'].append(uid)
            for m in ADJ.finditer(text):
                if any((uid, s) in taken for s in range(m.start() - 2, m.start() + 3)):
                    continue
                w = m.group(0)
                c = cand.setdefault(w, {'count': 0, 'docs': [], 'context': ''})
                c['count'] += 1
                if uid not in c['docs']:
                    c['docs'].append(uid)
                if not c['context']:
                    c['context'] = text[max(0, m.start() - 60):m.end() + 40]
    out = {'matched': {k: {'place': v['place'],
                           'forms': [{'form': f, **d} for f, d in sorted(v['forms'].items(), key=lambda x: -x[1]['count'])]}
                       for k, v in sorted(matched.items())},
           'candidates': [{'form': w, **d} for w, d in sorted(cand.items(), key=lambda x: (-x[1]['count'], x[0]))]}
    with io.open(os.path.join(ROOT, 'reference', 'guide', 'places_found.yml'), 'w', encoding='utf-8', newline='\n') as f:
        yaml.safe_dump(out, f, allow_unicode=True, sort_keys=False, width=110)
    print('%d places of the register found in the Latin, %d surface forms; %d place-like words unmatched'
          % (len(matched), sum(len(v['forms']) for v in matched.values()), len(cand)))


if __name__ == '__main__':
    main()
