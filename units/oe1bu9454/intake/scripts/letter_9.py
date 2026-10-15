# -*- coding: utf-8 -*-
"""Oe 1 Bü 9454, letter 9: the editor's transcription worked in (2026-10-15).

    python units/oe1bu9454/intake/scripts/letter_9.py            # check only
    python units/oe1bu9454/intake/scripts/letter_9.py --write    # once

Letter 9 stood in the holding as "(skipped)": the page map called it missing in
the archive, though the scan (0015_b, the right half of scan 0015; the left
half is a blank leaf) shows a single leaf in Triebenfeld's hand, with a large
hole through its left middle and its top right corner folded over. On
2026-10-15 the editor supplied a transcription of it.

Text. Made line by line from the editor's transcription and the scan, read
through enlarged; where they differ, the scan decided. "[...]" marks text lost
in the hole or under the fold, as the editor wrote it and as this holding marks
damage. The editor's hyphens used as dashes are "—"; their "s" is kept (no ſ),
as in their transcription of 245 and 289. Beugelin is written Beguelin, the
settled form (new_text_checklist.md, 4). Read otherwise than the editor's file,
from the scan (each is on the spot sheet "Letter 9", spot_9.py):
  line 2  betreibe ich durch ihn (editor: betreiben ich durch ihm);
  line 4  [säh?] (editor: seie); "gerne säh ich dem Patron[...] / Gesicht";
  line 6  [St. K. F. H.?] (editor: St. K. F. A[?].): the fourth letter is a
          Kurrent H; Staats Kanzler Fürst Hardenberg would fit, not expanded;
  line 7  weiß ich das wie und wo (editor: aus ich);
  line 9  wenn nur erst (editor: wann);
  line 11 Eben so gl[...] (editor: Eben so [...]): "gl" stands before the hole;
  line 12 [vorgerübene?]: the editor's letters, kept with a mark of doubt, as no
          word is found in them ("morgen reisen" is offered on the sheet);
  line 14 zum Borgen nehmen (editor: Bergen): the vowel is a round o, and letter
          8 has "ich lebe blos von erborgten Gelde";
  line 16 davon läuft der Bösewicht hat mich schändlich geärgert (editor: daran
          läuft der Böse wirft hat mich schrecklich geärgert);
  line 17 Streiche without the editor's mark of doubt.
Three marks of doubt, none of them the editor's [?] (which were on Streiche and
A[?]).

Date, place, writer. No date, place or signature survives; the leaf begins
mid-sentence. Dated to about January 1815 at Vienna: like letter 265a (8 January
1815) it waits only for the advance of 112/m Rthl to be granted ("accordir[t]"),
after the Transact of 1811 ("Über die [...] 1811 ist schon alles einig"); letter
8 (December 1814) still asks for a written promise of the 112/m; Beguelin and
Barbe, Koschentin, the children's distress and his living on borrowed money are
the business of the Vienna letters of that winter (8, 13). Writer Triebenfeld,
to the Prince, by his hand and business, as letters 8 and 13.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.dirname(os.path.dirname(UNIT))
KEY = 'oe1bu9454-009'

TEXT = '''9
der Geheime Etats Rath von Beguelin, arbeitet durch Barbes Vermittelung[...]
für [...] die Koschentiner Sache betreibe ich durch ihn — Aber der sehr[...]
Kedl [...] hat ihm gesagt, daß er die ganze Herrschaft[...]
schentin [...] haben könne — gerne [säh?] ich dem Patron[...]
Gesicht [...] mir doch durch wenn und was Sie dar[...]
für [...] [St. K. F. H.?] was anzubringen ist, auch, wie[...]
mit da [...] weiß ich das wie und wo, so mache ich hier
alles mög[...]
Über die [...] 1811 ist schon alles einig, wenn nur erst die 112/m
rt. accordir[...]
Eben so gl[...] [...]derung des halben Gehalts — Sobald nur etwas
Luft ist, werde ich [vorgerübene?] Meine Kinder helfen Ewr Durchlaucht ja mit 100 rt.
Kümmerlich und eingezogen muß ich hier leben in 6-7 Tägen muß ich schon wieder
meine Zuflucht zum Borgen nehmen —
Meinen krummen Bedienten laßen Ewr Durchlaucht dorten ja beobachten, daß er nicht
davon läuft der Bösewicht hat mich schändlich geärgert, aber außerdem hier
viel schlechte Streiche gemacht —'''
PAGE_FILE = '0021_Oe 1_Bue 9454_0015_b.txt'

DATE = ('    "9": [1815, 1, null, "inferred", "about January 1815, at Vienna: like letter 265a (8 Jan 1815) it waits only '
        'for the advance of 112/m Rthl to be granted, after the Transact of 1811; Beguelin, Barbe and the Koschentin '
        'business are those of the Vienna letters of that winter (8, 13). A single damaged leaf; its beginning, date and '
        'signature are lost"]')
CORR = {'basis': 'ruling 2026-10-15: his hand and business: the Vienna mission (Beguelin, Barbe, the 112/m), his children, '
                 'living on borrowed money; a single leaf, beginning and signature lost',
        'confidence': 'high', 'recipient': 'Friedrich Ludwig, Fürst zu Hohenlohe-Ingelfingen', 'sender': 'von Triebenfeld'}

DE = ('Bruchstück eines Briefes Triebenfelds an den Fürsten, ein einzelnes beschädigtes Blatt ohne Anfang. Der Geheime '
      'Etatsrat Beguelin arbeite durch Barbes Vermittlung, und durch ihn betreibe Triebenfeld die Koschentiner Sache. Es '
      'sei schon alles einig, wenn nur erst die 112/m Rthl bewilligt würden. Der Fürst möge seinen Kindern mit 100 Rthl '
      'helfen; Triebenfeld lebe kümmerlich und müsse in 6-7 Tagen wieder borgen. Sein Diener dort solle beobachtet '
      'werden, damit er nicht davonlaufe; er habe ihn geärgert.')
EN = ('Fragment of a letter from Triebenfeld to the Prince, a single damaged leaf without its beginning. He says the Privy '
      'Councillor of State Beguelin is working through Barbe\'s mediation, and that through him he is pursuing the Koschentin '
      'business. Everything is already agreed, he says, if only the 112/m Rthl are granted first. He asks the Prince to help '
      'his children with 100 Rthl; he says he lives meagrely and must borrow again in 6-7 days. His servant there should be '
      'watched so that he does not run away; he says the man has angered him.')
# statement of the German summary -> words of the letter that carry it
CLAIMS = [
    ('Bruchstück eines Briefes Triebenfelds an den Fürsten, ein einzelnes beschädigtes Blatt ohne Anfang',
     ['der Geheime Etats Rath von Beguelin', 'Ewr Durchlaucht dorten']),
    ('Der Geheime Etatsrat Beguelin arbeite durch Barbes Vermittlung',
     ['der Geheime Etats Rath von Beguelin, arbeitet durch Barbes Vermittelung']),
    ('und durch ihn betreibe Triebenfeld die Koschentiner Sache', ['die Koschentiner Sache betreibe ich durch ihn']),
    ('Es sei schon alles einig, wenn nur erst die 112/m Rthl bewilligt würden',
     ['ist schon alles einig, wenn nur erst die 112/m', 'rt. accordir[...]']),
    ('Der Fürst möge seinen Kindern mit 100 Rthl helfen', ['Meine Kinder helfen Ewr Durchlaucht ja mit 100 rt.']),
    ('Triebenfeld lebe kümmerlich und müsse in 6-7 Tagen wieder borgen',
     ['Kümmerlich und eingezogen muß ich hier leben in 6-7 Tägen', 'meine Zuflucht zum Borgen nehmen']),
    ('Sein Diener dort solle beobachtet werden, damit er nicht davonlaufe',
     ['Meinen krummen Bedienten laßen Ewr Durchlaucht dorten ja beobachten, daß er nicht', 'davon läuft']),
    ('er habe ihn geärgert', ['hat mich schändlich geärgert']),
]
NOTES = ('Read in the working session on 2026-10-15 from the editor\'s transcription and the scan. A single leaf in '
         'Triebenfeld\'s hand to the Prince, without beginning, date or signature, holed in its left middle and folded at the '
         'top right corner, so that many lines are broken. Vienna, about January 1815: Beguelin works through Barbe and '
         'through him the Koschentin business is pursued; everything is agreed if only the 112/m Rthl are granted (the '
         'Transact of 1811); the half salary; 100 Rthl for his children; he lives on borrowing; his servant, who has run up '
         'tricks, is to be watched. Nothing on Trąbczyn.')
DOUBT = [('[säh?]', 'the vowel is not clear; the sense would be "gerne säh ich dem Patron [ins] Gesicht"'),
         ('[St. K. F. H.?]', 'four initials; perhaps Staats Kanzler Fürst Hardenberg'),
         ('[vorgerübene?]', 'the letters as the editor read them; no word is found in them')]


def letter_lines(corpus, doc):
    out, on, n = [], False, 0
    for l in corpus:
        s = l.strip()
        if s.startswith('[DOC '):
            on = s == '[DOC %s]' % doc
            n = 0
        elif on and s and not s.startswith('[PAGE '):
            n += 1
            out.append((n, l))
    return out


def sub_once(s, old, new, what):
    assert s.count(old) == 1, (what, s.count(old))
    return s.replace(old, new)


def main():
    write = '--write' in sys.argv
    sys.stdout.reconfigure(encoding='utf-8')
    # --- the text
    cp = os.path.join(UNIT, 'corpus.txt')
    lines = io.open(cp, encoding='utf-8').read().split('\n')
    i = lines.index('[PAGE 0015_b]')
    assert lines[i - 1] == '[DOC 9]' and lines[i + 1] == '(skipped)' and lines[i + 2] == '[DOC 10]', lines[i - 1:i + 3]
    new_lines = lines[:i + 1] + TEXT.split('\n') + lines[i + 2:]
    pf = os.path.join(UNIT, 'transcriptions', PAGE_FILE)
    assert io.open(pf, encoding='utf-8').read().strip() == '(skipped)'
    # --- summary claims are all in the letter
    ll = letter_lines(new_lines, '9')
    left = DE
    for st, _ in CLAIMS:
        assert st in left, st
        left = left.replace(st, '', 1)
    assert not re.sub(r'[\s.;,]', '', left), left
    claims = []
    for st, words in CLAIMS:
        hits = []
        for w in words:
            h = [n for n, l in ll if w in l]
            assert h, w
            hits.append(h[0])
        claims.append({'statement': st, 'lines': sorted(set(hits))})
    doubt = []
    for w, note in DOUBT:
        h = [n for n, l in ll if w in l]
        assert h, w
        doubt.append({'line': h[0], 'word': w, 'note': note})
    print('letter 9: %d lines; summary %d words (German), %d (English); %d statements, all found; %d marks of doubt'
          % (len(ll), len(DE.split()), len(EN.split()), len(claims), len(doubt)))
    # --- rulings.yml
    rp = os.path.join(UNIT, 'rulings.yml')
    ru = io.open(rp, encoding='utf-8', newline='').read()
    ru = sub_once(ru, 'no_date: ["121", "181", "225", "293", "303", "9"]', 'no_date: ["121", "181", "225", "293", "303"]', 'no_date')
    ru = sub_once(ru, '    "254": [1814, 11, null, "inferred",', DATE + '\n    "254": [1814, 11, null, "inferred",', 'inferred')
    ru = sub_once(ru, '    "8": "Wien[?]"\n', '    "8": "Wien[?]"\n    "9": "Wien[?]"\n', 'place')
    ru = sub_once(ru, '    "9": []\n', '    "9": [koschentin, oppurg, schlawenschitz, lassowitz]\n', 'estates')
    # --- correspondents.json
    cjp = os.path.join(UNIT, 'correspondents.json')
    craw = io.open(cjp, encoding='utf-8', newline='').read()
    cj = json.loads(craw)
    assert cj['9']['basis'] == 'unmatched', cj['9']
    cj['9'] = CORR
    # --- page_scan_map.csv: the note that called the letter missing
    mp = os.path.join(UNIT, 'page_scan_map.csv')
    mraw = io.open(mp, encoding='utf-8', newline='').read()
    mraw = sub_once(mraw, ',declared,ok,missing/skipped in the archive - no document to scan', ',declared,ok,', 'scan map')
    # --- reading.json
    rdp = os.path.join(UNIT, 'reading.json')
    rraw = io.open(rdp, encoding='utf-8', newline='').read()
    reading = json.loads(rraw)
    assert KEY not in reading
    entry = {'letter': '9', 'legibility': 'legible', 'notes': NOTES, 'claims': claims, 'doubtful_words': doubt,
             'read_against': 'session 2026-10-15 (intake/scripts/letter_9.py)'}
    reading = dict(kv for k, v in reading.items()
                   for kv in ([(k, v), (KEY, entry)] if k == 'oe1bu9454-008' else [(k, v)]))
    assert KEY in reading
    # --- summaries_de.yml (after letter 8)
    sp = os.path.join(UNIT, 'summaries_de.yml')
    sde = io.open(sp, encoding='utf-8', newline='').read()
    m = re.search(r'(?m)^oe1bu9454-008: .*\n', sde)
    assert m and KEY + ':' not in sde
    sde = sde[:m.end()] + '%s: %s\n' % (KEY, DE) + sde[m.end():]
    # --- the site's summaries (by hand, as for 245 and 289: summarise.py --build from this cache would revert others)
    site = {}
    for name, text in (('summaries.yml', EN), ('summaries_de.yml', DE)):
        p = os.path.join(ROOT, 'site', '_data', name)
        s = io.open(p, encoding='utf-8', newline='').read()
        m = re.search(r'(?m)^oe1bu9454-008: .*\n', s)
        assert m and KEY + ':' not in s, name
        val = text if ':' not in text and "'" not in text else "'" + text.replace("'", "''") + "'"
        site[p] = s[:m.end()] + '%s: %s\n' % (KEY, val) + s[m.end():]
    if write:
        io.open(cp, 'w', encoding='utf-8', newline='\n').write('\n'.join(new_lines))
        io.open(pf, 'w', encoding='utf-8', newline='\n').write(TEXT + '\n')
        io.open(rp, 'w', encoding='utf-8', newline='').write(ru)
        io.open(cjp, 'w', encoding='utf-8', newline='\n').write(json.dumps(cj, ensure_ascii=False, indent=2, sort_keys=True)
                                                                  + ('\n' if craw.endswith('\n') else ''))
        io.open(mp, 'w', encoding='utf-8', newline='').write(mraw)
        indent = 1 if rraw.startswith('{\n "') else (2 if rraw.startswith('{\n  "') else None)
        out = json.dumps(reading, ensure_ascii=False, indent=indent)
        if '\r\n' in rraw:
            out = out.replace('\n', '\r\n')
        io.open(rdp, 'w', encoding='utf-8', newline='').write(out + ('\r\n' if rraw.endswith('\r\n') else '\n' if rraw.endswith('\n') else ''))
        io.open(sp, 'w', encoding='utf-8', newline='').write(sde)
        for p, s in site.items():
            io.open(p, 'w', encoding='utf-8', newline='').write(s)
        for sub, text in (('summaries-raw', EN), ('summaries-raw-de', DE)):
            p = os.path.join(ROOT, 'cache', sub, KEY + '.json')
            assert not os.path.exists(p), p
            json.dump({'letter': '9', 'pad': KEY, 'summary': text, 'model': 'claude-code-session',
                       'usage': {'input': 0, 'output': 0}},
                      io.open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
        print('written')


if __name__ == '__main__':
    main()
