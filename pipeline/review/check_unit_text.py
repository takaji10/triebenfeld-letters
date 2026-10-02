# -*- coding: utf-8 -*-
"""
Hold each holding's description to the documents it cites.

Reads  : units/<slug>/about.md, process.md (and their _de counterparts)
         corpus/documents/ via unitlib.load_documents()
Writes : review/<slug>/unit_text_check.md

A description is written by hand from the summaries and the reading, and a
long one is exactly where a figure gets carried over wrongly. So:

  FAIL  a citation [[n]] that names no document of the holding
  FAIL  a year, a day or a sum that none of the cited documents has (in its
        text, its English, its summaries, its reading notes or its date)
  FAIL  a paragraph of about.md that cites nothing and is not marked as
        context (<!-- context -->)
  FAIL  an em or en dash in English prose (docs/HOUSE_STYLE.md)
  note  a capitalised word found neither in the cited documents nor in the
        authorities: usually an ordinary word, sometimes a name got wrong

A citation covers the sentences since the citation before it in the same
paragraph. Failures stop regenerate.py; notes are for whoever wrote the text.

    python pipeline/review/check_unit_text.py [--unit <slug>]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__))), 'build'))

import io, os, re, sys, json, unicodedata
import unitlib
from unit_pages import CITE, CONTEXT
from entities import load_people, place_authority

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NUM = re.compile(r'(?<![\w.,])\d[\d.,]*\d(?![\w])|(?<![\w.,])\d(?![\w.,]*\d)')
NAME = re.compile(r"\b[A-ZÄÖÜĄĆĘŁŃÓŚŹŻ][\w'’-]{2,}")
# Capitalised words that are not names of anything in a document.
COMMON = set('''the this that these those there then they their what when where
which who why how and but for from with without after before since until while
his her its one two three four five six seven eight nine ten each every both all
some most many much any not nor only also still here january february march
april may june july august september october november december french german
polish latin english rthl groschen prince king emperor tsar count duke baron
minister ministry chancellor state general major colonel councillor'''.split())


def fold(s):
    s = unicodedata.normalize('NFKD', s.replace('ß', 'ss').replace('ł', 'l').replace('Ł', 'L'))
    return ''.join(c for c in s if not unicodedata.combining(c)).lower()


def digits(s):
    """Thousands separators out, so 55,000 and 55.000 and 55000 are one figure."""
    return re.sub(r'(?<=\d)[.,](?=\d{3}(?!\d))', '', s)


def haystack(rec):
    parts = [rec.get('text') or '', rec.get('text_english') or '',
             rec.get('summary_en') or '', rec.get('summary_de') or '',
             json.dumps(rec.get('reading') or {}, ensure_ascii=False),
             rec.get('date_iso') or '', str(rec.get('year') or ''),
             str(rec.get('day') or ''), rec.get('sender') or '',
             rec.get('recipient') or '', rec.get('place') or '']
    parts += [m.get('display', '') for m in (rec.get('mentions') or [])
              + (rec.get('place_mentions') or [])]
    return digits('\n'.join(parts))


def paragraphs(text):
    text = re.sub(r'<!--(?!\s*context\s*-->).*?-->', '', text, flags=re.S)
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]


def check(unit, recs, authority):
    by_id = {r['letter_id']: r for r in recs}
    fails, notes = [], []
    unit_dir = os.path.join(ROOT, 'units', unit.slug)
    for name in ('about.md', 'process.md', 'about_de.md', 'process_de.md'):
        p = os.path.join(unit_dir, name)
        if not os.path.exists(p):
            continue
        text = open(p, encoding='utf-8').read()
        english = not name.endswith('_de.md')
        about = name.startswith('about')
        for para in paragraphs(text):
            head = ' '.join(para.split())[:60]
            if para.startswith('#'):
                continue
            if english and re.search(r'[–—]', para):
                fails.append(f'{name}: a dash in "{head}..."')
            ids = [i.strip() for m in CITE.finditer(para) for i in m.group(1).split(',')]
            for i in ids:
                if i not in by_id:
                    fails.append(f'{name}: [[{i}]] is not a document of this holding ("{head}...")')
            if not about:
                continue
            if CONTEXT in para:
                continue
            if not ids:
                fails.append(f'{name}: no document cited and not marked as context: "{head}..."')
                continue
            # each stretch of prose, with the citation that closes it
            pos = 0
            for m in CITE.finditer(para):
                seg = para[pos:m.start()]
                pos = m.end()
                cited = [by_id[i.strip()] for i in m.group(1).split(',') if i.strip() in by_id]
                hay = '\n'.join(haystack(r) for r in cited)
                hay_f = fold(hay)
                for n in NUM.findall(digits(seg)):
                    if not re.search(r'(?<!\d)' + re.escape(n) + r'(?!\d)', hay):
                        fails.append(f'{name}: {n} is not in the documents cited '
                                     f'[{m.group(1)}]: "...{" ".join(seg.split())[-70:]}"')
                # German capitalises every noun, so this note only works in English.
                for w in (NAME.findall(seg) if english else []):
                    f = fold(w.rstrip("'’s") if w.endswith(("'s", '’s')) else w)
                    if f in COMMON or f in hay_f or f in authority:
                        continue
                    notes.append(f'{name}: "{w}" is not in the documents cited [{m.group(1)}]')
            tail = para[pos:].replace(CONTEXT, '')
            for n in NUM.findall(digits(tail)):
                fails.append(f'{name}: {n} stands after the last citation of its '
                             f'paragraph: "...{" ".join(tail.split())[-70:]}"')
    return fails, notes


def main():
    units = unitlib.load_units(unitlib.unit_arg())
    docs = unitlib.load_documents()
    authority = set()
    for _slug, disp, _rx in list(load_people()) + list(place_authority()):
        authority.update(fold(w) for w in re.findall(r"[\w'’-]{3,}", disp))
    bad = 0
    for u in units:
        recs = [r for r in docs if r['unit'] == u.slug]
        if not recs:
            continue
        fails, notes = check(u, recs, authority)
        out = unitlib.review_dir(u.slug)
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, 'unit_text_check.md'), 'w', encoding='utf-8',
                  newline='\n') as f:
            f.write(f'# {u["ref"]}: the description held to its documents\n\n')
            f.write(f'## Failures ({len(fails)})\n\n' + ''.join(f'- {x}\n' for x in fails))
            f.write(f'\n## Words to look at ({len(notes)})\n\n'
                    + ''.join(f'- {x}\n' for x in sorted(set(notes))))
        has = [n for n in ('about.md', 'process.md')
               if os.path.exists(os.path.join(ROOT, 'units', u.slug, n))]
        print(f'    {u.slug}: {", ".join(has) or "no text yet"}; '
              f'{len(fails)} failures, {len(set(notes))} words to look at')
        for x in fails:
            print('      FAIL ' + x)
        bad += len(fails)
    if bad:
        sys.exit(f'{bad} statements do not hold against the documents they cite')


if __name__ == '__main__':
    main()
