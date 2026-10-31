# -*- coding: utf-8 -*-
"""
The documents that carry no tagged people, as a sheet the editor works through.

    python pipeline/review/zero_mentions.py          # write the sheet + CSV
    python pipeline/review/zero_mentions.py --lines 15   # at least this long
    python pipeline/review/zero_mentions.py --unit oe1bu9454
    python pipeline/review/zero_mentions.py --quiet  # for the rebuild

The person authority is German-corpus-shaped: curated patterns in
reference/people.yml, a statistical long tail (name_seeds.json) under them.
Latin, Polish and Russian naming runs through it thin to none - a medieval
charter can name its donor and king in forms no pattern reaches - and a
holding taken in without a name ruling lands in the dataset with tags for
no one. The cost of that is invisible: the document is published, the site
verifies clean, and every question of "who appears here" quietly answers
with nothing.

What no script can settle is whether the blank is a real blank or a missing
entry; that is the editor's call, against the page. What this sheet does is
gather the blanks in one place, with the evidence for calling each either
way:

  - where the document is, its date, kind, language, size, correspondents;
  - a lead list: tokens sitting in name position - after von / zu or an
    honorific, or ending -schen, where estates and family names live - that
    no authority pattern matches. A document whose leads are the words of
    officialese is plausibly empty; one with leads like "Adolph" or
    "Zbyszewski" is not.

Nothing here matches anything new and nothing is applied. The editor's
rulings live in `reference/zero_mention_rulings.json` ({uid: note}, the
translation_rulings.json shape); a ruled row moves to the sheet's ruled
section, out of the working list and the CSV, and is not raised again.

`pipeline/regenerate.py` runs this as a report after the dataset is rebuilt,
so a new holding's blanks appear in it on the next build without anyone
remembering to look. It deliberately does not gate: a genuinely empty
record is a perfectly fine thing to be.
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_os.path.dirname(_HERE))
_sys.path.insert(0, _os.path.join(_ROOT, 'pipeline', 'build'))
_sys.path.insert(0, _ROOT)

import io, sys, os, re, csv, json, argparse
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = _ROOT
INDEX = os.path.join(ROOT, 'dataset', 'index', 'documents.json')
SHEET = os.path.join(ROOT, 'review', 'zero_mentions.md')
CSVP = os.path.join(ROOT, 'review', 'zero_mentions.csv')
RULINGS = os.path.join(ROOT, 'reference', 'zero_mention_rulings.json')

COLUMNS = ['uid', 'unit', 'letter_id', 'date', 'date_precision', 'date_source',
           'place', 'doc_type', 'language', 'pages', 'lines', 'sender',
           'recipient', 'candidates', 'permalink', 'decision', 'note']

# Ordinary words a capital can open, and the officialese nouns of this
# corpus. The cues put a token *after* von / zu / an honorific or the
# -schen ending; what survives that, and the authorities, is a lead. What
# this list keeps out is the nouns those cues still catch in a deed
# ("von der Provision" the share, "Copie des Indyculs" the papers).
_STOPWORDS = frozenset("""
Adieu Alles Auch Auf Aus Bei Damit Danach Dann Das Der Des Die Dies Diese
Dieser Dir Durch Eine Einen Eines Einer Er Es Euer Ew Gen Gnädig Hab Ich Ihn
Ihnen Ihr Ihre Im In Je Jetzt Kein Keine Man Mit Morgen Nach Naemlich Nie
Noch Nun Nur Ob Oder Ohne Puncto Schon Sehr Sein Seine Sich Sie Sind So
Sonst Und Uns Unter Von Vor Was Wer Wie Wir Wird Wirst Wo Wollen Wurde
Nämlich Naemlich Am An Befehl Contract Extract Original Provision
Provisionis Quittung Rescript Register Registre Verzeichniss Copie Copy
Erben Witwe Wittwe Collega Diener Begleitschreiben Manifest Deklaration
Unknown Datum Befehle Jan Febr Februar Mär Marz März Apr April Mai Juni
Jul Juli Augt Sep Sept Okt Nov Dez Decr Montag Dienstag Mittwoch
Donnerstag Freitag Samstag Sonnabend Sonntag Kopie Concept Konzept
Abschrift Hauß Haeuser Kirchen Christen Geschlecht Geschlechts Menschen
Graeber Grab Dörfer Doerfer Kurow Jahre Jahr Hochwohlgebohrnen Herrn
""".split())

# Despaced join (von=dre) and despaced abbreviations (v., vo) want the same
# separators the corpus uses: one run of spaces, dashes or equals. Python's
# re has no branch reset, so each alternative carries its own capturing
# group and candidates() reads m.group(m.lastindex) - the branch that fired.
_TOKEN = r'([A-ZÄÖÜ][a-zäöüßżźćńłóś]{2,})'
_SEP = r'\s*[-=]\s*|\s+'
# Python's re has no branch reset, so every alternative carries its own
# capturing group and candidates() reads m.group(m.lastindex), the branch
# that fired.
_CUE = re.compile(
    r'\bv[.=]\w*' + _SEP + _TOKEN +
    r'|\bvon\b' + _SEP + _TOKEN +
    r'|\bzu\b' + _SEP + _TOKEN +
    r'|\bHerrn?\b' + _SEP + _TOKEN +
    r'|\bFrau(?:en)?\b' + _SEP + _TOKEN +
    r'|\bPastor\b' + _SEP + _TOKEN +
    r'|\bCapitain\b' + _SEP + _TOKEN +
    r'|\bMajor\b' + _SEP + _TOKEN +
    r'|\bLeutnant\b' + _SEP + _TOKEN +
    r'|\bRath\b' + _SEP + _TOKEN +
    r'|\bAmtmann\b' + _SEP + _TOKEN +
    r'|\bKantor\b' + _SEP + _TOKEN +
    r'|\bLehrer\b' + _SEP + _TOKEN +
    r'|\bSchulze\b' + _SEP + _TOKEN +
    r'|\bKuhhirte?n\b' + _SEP + _TOKEN +
    r'|\bSch[öo]ltze\b' + _SEP + _TOKEN +
    r'|\bBürgermeister\b' + _SEP + _TOKEN +
    r'|\bKaufmann\b' + _SEP + _TOKEN +
    r'|\bNotar\b' + _SEP + _TOKEN)
_SCHEN = re.compile(r'\b([A-ZÄÖÜ][a-zäöüßżźćńłóś]{3,})schen\b')


def load_rulings():
    if os.path.isfile(RULINGS):
        with open(RULINGS, encoding='utf-8') as f:
            return json.load(f) or {}
    return {}


def _read_text(rec):
    # text_path is dataset-relative ("text/<uid>.txt"), as the manifest
    # writes it (docs/DATA_MODEL.md, the index's field table).
    tp = (rec.get('text_path') or '').lstrip('/')
    p = tp if tp.startswith(ROOT) else os.path.join(ROOT, 'dataset', tp)
    if tp and os.path.isfile(p):
        with open(p, encoding='utf-8') as f:
            return f.read(), p
    return '', p


def candidates(text, authority):
    """Unmatched name-position tokens, in document order, capped at 12.

    The cap is deliberate: a holding of legal formulas can carry hundreds
    of capitalised leads, and the sheet wants a taste of the row to point
    at the page, not the row's whole burden. The document itself is one
    permalink away.
    """
    out = []
    # The .txt files open with four '#' header lines (uid, date and place,
    # permalink) whose words are not the document's; the candidates come
    # from the text proper.
    flat = '\n'.join(ln for ln in text.split('\n')
                     if not ln.startswith('#')).replace('ſ', 's')
    for m in list(_CUE.finditer(flat)) + list(_SCHEN.finditer(flat)):
        tok = m.group(m.lastindex or 1)
        if len(out) >= 12 or tok in _STOPWORDS:
            continue
        for _slug, _d, rx in authority:
            if rx.search(tok):
                break
        else:
            out.append(tok)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit')
    ap.add_argument('--lines', type=int, default=15,
                    help='report documents of at least this many lines')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()

    import entities
    authority = entities.load_people() + entities.place_authority()

    with open(INDEX, encoding='utf-8') as f:
        docs = json.load(f)
    if a.unit:
        docs = [r for r in docs if r['unit'] == a.unit]

    rulings = load_rulings()
    rows = []
    for r in docs:
        if r.get('mentions', 0) or (r.get('n_lines') or 0) < a.lines:
            continue
        text, tpath = _read_text(r)
        heads = [ln for ln in text.split('\n')
                 if ln.strip() and not ln.startswith('#')]
        rows.append({'rec': r, 'tpath': tpath,
                     'first': ' '.join(heads[0].split()) if heads else '',
                     'candidates': candidates(text, authority)})

    ruled = [x for x in rows if x['rec']['uid'] in rulings]
    open_rows = [x for x in rows if x['rec']['uid'] not in rulings]
    open_rows.sort(key=lambda x: -(x['rec'].get('n_lines') or 0))
    by_place = Counter(x['rec'].get('place') or 'Unknown' for x in open_rows)

    with open(SHEET, 'w', encoding='utf-8', newline='\n') as f:
        w = f.write
        w('# The documents that carry no tagged people\n\n')
        w('Generated by `pipeline/review/zero_mentions.py` (run by '
          '`pipeline/regenerate.py`\nafter the dataset is rebuilt). '
          '%d documents unruled, %d ruled, of %d built;\nreported where no '
          'person matches a document of at least %d lines.\n\n'
          % (len(open_rows), len(ruled), len(docs), a.lines))
        w('Most common places of writing among the unruled: %s.\n\n'
          % ', '.join('%s (%d)' % (p, n) for p, n in by_place.most_common(8)))
        w('To rule a row: enter it in `reference/zero_mention_rulings.json`\n'
          'as `"<uid>": "<why no one is tagged, or what you did>"`. The row\n'
          'leaves the working list here and from the CSV. The "unmatched in\n'
          'name position" line is a heuristic lead list, not a claim: the\n'
          'tokens the cues and the -schen forms found, minus the stopwords\n'
          'and anything an authority pattern covers. Read against the scan.\n')
        for x in open_rows:
            r = x['rec']
            sender = r.get('sender') or ''
            recipient = r.get('recipient') or ''
            corr = ('%s -> %s' % (sender, recipient) if sender and recipient
                    else (('sender %s, recipient not identified' % sender)
                          if sender else
                          (('recipient %s, sender not identified' % recipient)
                           if recipient else 'no correspondents recorded')))
            w('\n## %s\n\n' % r['uid'])
            w('- %s, %s (%s), place of writing %s · %s\n'
              '- %d pages, %d lines · correspondents: %s\n'
              % (r['doc_type'],
                 r.get('date_iso') or 'undated',
                 r.get('date_source') or 'no date source',
                 r.get('place') or 'Unknown',
                 r.get('language') or 'de',
                 r.get('n_pages'), r.get('n_lines'), corr))
            if x['candidates']:
                w('- unmatched in name position: %s\n'
                  % ', '.join(x['candidates']))
            if x['first']:
                w('- first line: "%s"\n' % x['first'][:220])
            w('- text: %s · page: %s\n'
              % (os.path.relpath(x['tpath'], ROOT), r['permalink']))

        if ruled:
            w('\n## Already ruled\n\n')
            for x in sorted(ruled, key=lambda x: x['rec']['uid']):
                w('- %s: %s\n' % (x['rec']['uid'], rulings[x['rec']['uid']]))

    with open(CSVP, 'w', encoding='utf-8', newline='\n') as f:
        wr = csv.DictWriter(f, COLUMNS, lineterminator='\n')
        wr.writeheader()
        for x in open_rows:
            r = x['rec']
            wr.writerow({'uid': r['uid'], 'unit': r['unit'],
                         'letter_id': r['letter_id'],
                         'date': r.get('date_iso') or '',
                         'date_precision': r.get('date_precision') or '',
                         'date_source': r.get('date_source') or '',
                         'place': r.get('place') or '',
                         'doc_type': r['doc_type'],
                         'language': r.get('language') or 'de',
                         'pages': r.get('n_pages'), 'lines': r.get('n_lines'),
                         'sender': r.get('sender') or '',
                         'recipient': r.get('recipient') or '',
                         'candidates': ' | '.join(x['candidates']),
                         'permalink': r['permalink'],
                         'decision': '', 'note': ''})

    if not a.quiet:
        print('zero mentions: %d unruled, %d ruled (sheet %s)'
              % (len(open_rows), len(ruled), os.path.relpath(SHEET, ROOT)))


if __name__ == '__main__':
    main()
