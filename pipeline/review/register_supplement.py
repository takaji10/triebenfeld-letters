# -*- coding: utf-8 -*-
"""Fill the Consistency Register's Hohenlohe-era gap from the corpus itself.

    python register_supplement.py                  # report to the terminal
    python register_supplement.py --write          # write the markdown

Consistency_Register.md is the book's authority on names, and it says plainly
what it is missing. Under "What this register still needs":

    A review run covering the Hohenlohe-Ingelfingen and 19th-century sections.
    The persons, places, and archival references for 1796-1861 are listed
    provisionally above but have never been through a review pass, so no
    first-appearance locations, spelling-variant trails, or conflict flags
    exist for them.

That is precisely what corpus/index/people.json and places.json already hold
and nothing reads: every observed surface form, with the document, page and
absolute line it stands on. The register needs it written out; the edition
needs no new judgement to write it. So this generates it.

What it does NOT do is edit the register. Consistency_Register.md is a curated
scholarly document with resolutions, open questions and prose that no generator
should overwrite, so the output is a separate file for the editor to merge -
and it says which entries are new against the register's own provisional list,
so the merge is a reading job rather than a diffing one.

Identity is authored, in reference/people.yml and reference/places.yml.
Appearances are counted, here. Nothing below decides who anyone is.
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, os, sys, json, argparse
from collections import OrderedDict

import unitlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'build'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

INDEX = os.path.join(ROOT, 'corpus', 'index')
OUT = os.path.join(ROOT, 'Consistency_Register_Supplement.md')
REGISTER = os.path.join(ROOT, 'Consistency_Register.md')


def index(name):
    p = os.path.join(INDEX, name)
    return json.load(io.open(p, encoding='utf-8')) if os.path.isfile(p) else []


def doc_order():
    """{uid: (date_iso, unit, position)} - how to say which appearance is first.

    Date first, because that is what "first appearance" means to a reader. But
    an undated document sorts last rather than first: an empty date string would
    otherwise win every comparison and put the least-known document at the head
    of every entity's trail.
    """
    out = {}
    for i, r in enumerate(index('documents.json')):
        uid = r.get('uid') or ''
        out[uid] = (r.get('date_iso') or '9999-99-99', r.get('unit') or '', i)
    return out


def trail(entry, order):
    """Every spelling of one entity, with where each was seen.

    Grouped by surface rather than by document, because the question the
    register asks is "how is this name spelled across the corpus", and the
    answer is a short list even for an entity appearing in three hundred
    documents.
    """
    seen = OrderedDict()
    for m in entry.get('mentions') or []:
        s = seen.setdefault(m.get('surface') or '', [])
        s.append(m)
    rows = []
    for surface, ms in seen.items():
        ms = sorted(ms, key=lambda m: order.get(m.get('uid'), ('9999', '', 0)))
        rows.append({'surface': surface, 'count': len(ms), 'first': ms[0],
                     'documents': sorted({m.get('uid') for m in ms})})
    rows.sort(key=lambda r: (-r['count'], r['surface']))
    return rows


def cite(m, dates):
    uid = m.get('uid') or '?'
    d = dates.get(uid, ('', '', 0))[0]
    when = f", {d[:4]}" if d and not d.startswith('9999') else ''
    return f"{uid}{when}, p. {m.get('page')} (line {m.get('line')})"


def known_to_register():
    """Names the register already mentions, however briefly.

    A substring test, deliberately crude. Its only job is to mark an entry as
    NEW or as an expansion of something provisional, and a false "already
    known" is the safer error: it leaves the editor reading rather than
    trusting a claim of novelty.
    """
    if not os.path.isfile(REGISTER):
        return ''
    return io.open(REGISTER, encoding='utf-8').read()


def section(title, entries, order, dates, register, kind):
    out = [f'## {kind}', '']
    for e in entries:
        rows = trail(e, order)
        if not rows:
            continue
        display = e.get('display') or e.get('entity')
        new = '' if display.split()[-1] in register else '  **NEW to the register.**'
        out.append(f"### {display}  <!-- {e['entity']} -->")
        out.append('')
        out.append(f"- **{len(e.get('documents') or [])} document(s)**, "
                   f"{e.get('count', 0)} mention(s).{new}")
        first = rows[0]['first']
        best = min(rows, key=lambda r: order.get(r['first'].get('uid'),
                                                 ('9999', '', 0)))
        out.append(f"- **First appearance:** {cite(best['first'], dates)}, "
                   f"as *{best['surface']}*.")
        if len(rows) == 1:
            out.append(f"- **Spellings encountered:** one only, *{rows[0]['surface']}* "
                       f"({rows[0]['count']}x).")
        else:
            out.append('- **Spellings encountered:**')
            for r in rows:
                out.append(f"    - *{r['surface']}* — {r['count']}x, first at "
                           f"{cite(r['first'], dates)}")
        out.append('')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true', help='write the markdown file')
    ap.add_argument('--min-documents', type=int, default=1,
                    help='skip entities appearing in fewer documents than this')
    a = ap.parse_args()

    holdings = ', '.join(u.get('ref') or u.slug for u in unitlib.load_units()
                         if (u.get('status') or '') != 'draft')
    order = doc_order()
    register = known_to_register()
    people = [e for e in index('people.json')
              if len(e.get('documents') or []) >= a.min_documents]
    places = [e for e in index('places.json')
              if isinstance(e, dict) and e.get('mentions')]

    people.sort(key=lambda e: -(e.get('count') or 0))
    body = ['# Consistency Register — Hohenlohe-era supplement', '',
            '*Generated by `pipeline/review/register_supplement.py` from '
            '`corpus/index/`. Identity is authored in `reference/people.yml` and '
            '`reference/places.yml`; everything below is counted from the '
            'transcriptions and is regenerated, so edit those files rather than '
            'this one.*', '',
            'This answers item 1 of the register\'s own "What this register still '
            'needs": the persons of 1796–1861 had no first-appearance locations '
            'and no spelling-variant trails. Each entry below gives the canonical '
            'display name, every surface form the corpus actually carries, and '
            'the document, page and line each was first seen at, so an entry can '
            'be checked against the manuscript rather than taken on trust.', '',
            f'Holdings covered: {holdings}.',
            '', '---', '']
    body += section('Persons', people, order, order, register, 'Persons')
    if not places:
        body += [
            '---', '',
            '## Places', '',
            'Not yet available. `corpus/index/places.json` currently records where a',
            'document was WRITTEN, from its dateline, and not which places a document',
            'names - so the estate at the centre of a holding is indexed a handful of',
            'times rather than in the hundreds. `entities.place_mentions()`',
            'exists and reference/places.yml carries the patterns; the pass that writes',
            'those mentions into the index is the remaining step, after which this',
            'section fills itself the way Persons above does.', '']
    if places:
        body += ['---', ''] + section('Places', places, order, order, register, 'Places')

    text = '\n'.join(body).rstrip() + '\n'
    named = sum(1 for e in people if len(e.get('documents') or []) >= a.min_documents)
    multi = sum(1 for e in people if len(trail(e, order)) > 1)
    print(f'{named} person entries, {multi} with more than one spelling')
    print(f'{len(places)} place entries with mentions in the body text')
    if not a.write:
        print(f'\n(report only - re-run with --write to produce {os.path.basename(OUT)})')
        return
    io.open(OUT, 'w', encoding='utf-8').write(text)
    print(f'\nwrote {OUT}')
    print('Merge by hand into Consistency_Register.md - it carries resolutions '
          'and open questions no generator should overwrite.')


if __name__ == '__main__':
    main()
