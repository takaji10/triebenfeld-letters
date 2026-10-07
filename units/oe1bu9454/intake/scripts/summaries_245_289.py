# -*- coding: utf-8 -*-
"""Oe 1 Bü 9454, letters 245 and 289: the summaries and the reading record after the new scans (2026-10-07).

    python units/oe1bu9454/intake/scripts/summaries_245_289.py            # check only
    python units/oe1bu9454/intake/scripts/summaries_245_289.py --write    # once

Both summaries were written again in the working session from the German as
corrected (rescan_245_289.py), in German first and then in English, within
the holding's limit of about eighty words, and each statement was held to
the letter: CLAIMS gives, for every statement, words of the letter that
carry it. The script finds those words, records the lines in reading.json
(as the paid reading did), and writes the summaries where they are kept:
summaries_de.yml here, and the two cache files that summarise.py --build
assembles into site/_data/summaries.yml and summaries_de.yml.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.dirname(os.path.dirname(UNIT))

DE = {
 '245': 'Eingabe Triebenfelds an Staats Kanzler Hardenberg für den notleidenden Fürsten Hohenlohe. Medizinalrat Cosmar habe sich als '
        'Testamentsvollstrecker der Fürstin Sacken in die Majoratsgüter Sławięcice, Lasowice und Oppurg (79500 Rthl Ertrag) eingenistet, gestützt '
        'auf einen Transact von 1811, den die Sterbende nur mit drei Kreuzen zeichnete; er ziehe alle Einkünfte ein und lege keine Rechnung. Die '
        'Curischen Erben wollen für 426000 Rthl 112000 nehmen. Erbeten werden ein Vorschuss von 112000 Rthl, Aufhebung des Transacts, Cosmars '
        'Entfernung und ein Bericht des Oberlandesgerichts Brzeg. Triebenfeld bietet 60000 Rthl Kaution.',
 '289': 'Triebenfeld bittet Albrecht, beim König einen kategorischen Bescheid zur Forderung der Curischen Erben zu erwirken. Die Schuld beträgt '
        '300/m Rthl, mit Zinsen 426/m Rthl, und der verstorbene König hat sie als Selbstschuldner unterschrieben. Zahlt der König, soll die '
        'Cosmarische Administration der Majoratsgüter aufgehoben werden; der Fürst habe in vier Jahren statt 96/m nur 2500 Rthl erhalten. Sagt er '
        'sich los, will Triebenfeld mit den Erben vergleichen, die zuvor circa 112/m Rthl annehmen wollten, und bittet um einen königlichen '
        'Vorschuss dafür. Cosmar legt keine Rechnung.',
}
EN = {
 '245': 'Petition by Triebenfeld to State Chancellor Hardenberg on behalf of the distressed Prince Hohenlohe. It says the Councillor of Medicine '
        'Cosmar, as executor of the will of Princess Sacken, has lodged himself in the entailed estates of Sławięcice, Lasowice and Oppurg (79500 '
        'Rthl in yield), relying on a settlement of 1811 that the dying Princess signed only with three crosses; that he draws all the revenues '
        'and submits no account; and that the Curland heirs will take 112000 for 426000 Rthl. Requested are an advance of 112000 Rthl, annulment '
        'of the settlement, Cosmar\'s removal and a report from the High Court of Appeal in Brzeg. Triebenfeld offers 60000 Rthl as security.',
 '289': 'Triebenfeld asks Albrecht to obtain a categorical decision from the King on the claim of the Curische heirs. He says the debt amounts '
        'to 300/m Rthl, 426/m Rthl with interest, and that the late King signed it as principal debtor. If the King pays, Cosmar\'s '
        'administration of the entailed estates should be lifted; the Prince, he says, has received only 2500 Rthl in four years instead of '
        '96/m. If he disclaims it, Triebenfeld wants to reach a settlement with the heirs, who earlier were willing to accept about 112/m Rthl, '
        'and he asks for a royal advance for that purpose. He says Cosmar submits no account.',
}
# statement of the German summary -> words of the letter that carry it
CLAIMS = {
 '245': [
  ('Eingabe Triebenfelds an Staats Kanzler Hardenberg für den notleidenden Fürsten Hohenlohe',
   ['(des Fürsten Staats Kanzler v. Hardenberg)', 'die drükendeste Noth des Fürsten zu schildern', 'v Triebenfeld']),
  ('Medizinalrat Cosmar habe sich als Testamentsvollstrecker der Fürstin Sacken in die Majoratsgüter Sławięcice, Lasowice und Oppurg (79500 Rthl '
   'Ertrag) eingenistet',
   ['betragen die Schlawenschitzer, Lassowitzer und', 'weiß dennoch 79500 rttlr Ertrag gewähren', 'einzunisten gewußt', 'Er heißt Testa: Executor']),
  ('gestützt auf einen Transact von 1811, den die Sterbende nur mit drei Kreuzen zeichnete',
   ['da sie in den lezten Zügen lag', 'nur mit 3 Xen unterzeichnete', 'In den mehrerwehnten Transact von 1811']),
  ('er ziehe alle Einkünfte ein und lege keine Rechnung',
   ['alle Revenuen einzieht und Niemanden davon einen Heller giebt', 'auch keine rechnung']),
  ('Die Curischen Erben wollen für 426000 Rthl 112000 nehmen', ['für die ganze Forderung von 426000 rt. — 112000 nehmen']),
  ('Erbeten werden ein Vorschuss von 112000 Rthl, Aufhebung des Transacts, Cosmars Entfernung',
   ['einen Vorschuß von 112/m rt zur Bezahlung', 'verdienten maßen aufheben', 'Cosmar aber von allem aus scheiden']),
  ('und ein Bericht des Oberlandesgerichts Brzeg', ['einen Bericht des Ober Land Gerichts zu Brieg']),
  ('Triebenfeld bietet 60000 Rthl Kaution', ['mit einer Caution von 60000 rt. hafte']),
 ],
 '289': [
  ('Triebenfeld bittet Albrecht, beim König einen kategorischen Bescheid zur Forderung der Curischen Erben zu erwirken',
   ['um allerhöchste Gnädigste Categorischen', 'gorische Erklärung des Monarchen', 'an des Hr. Cabinets Rath Albrecht']),
  ('Die Schuld beträgt 300/m Rthl, mit Zinsen 426/m Rthl, und der verstorbene König hat sie als Selbstschuldner unterschrieben',
   ['eine Forderung von 300/m rt. haben', 'von des höchst Seel. Königs Majestaet als selbst Schuldner unterschrieben', 'mit den Intressen 426/m rt. beträgt']),
  ('Zahlt der König, soll die Cosmarische Administration der Majoratsgüter aufgehoben werden',
   ['Im ersten Fall würde ich unterthänigst bitten', '"daß die Cosmarische Administration sofort aufgehoben und von']),
  ('der Fürst habe in vier Jahren statt 96/m nur 2500 Rthl erhalten', ['sollen den der Fürst hat seit', '4 Jahren statt 96/m rt nur 2500 rt']),
  ('Sagt er sich los, will Triebenfeld mit den Erben vergleichen, die zuvor circa 112/m Rthl annehmen wollten',
   ['Im 2ten Falle aber würde ich allergehorsamst bitten', 'los sagten, wornach ich dann den Vergleich mit zuversicht', 'nach welchen leztere Circa 112/m rt. zufrieden sein']),
  ('und bittet um einen königlichen Vorschuss dafür', ['allergnädigst vorzuschießen, befehlen mögten']),
  ('Cosmar legt keine Rechnung', ['wenig oder nichts legt keine Rechnung']),
 ],
}
NOTES = {
 '245': 'Read again in the working session on 2026-10-07 from the text corrected against the archive\'s new scans. A petition from Triebenfeld '
        'at Vienna (20 October 1814) to State Chancellor Hardenberg for Prince Hohenlohe, against the Medicinalrath Cosmar, executor of the '
        'late Princess Sacken: the entailed estates Schlawenschitz, Lassowitz and Oppurg (worth over 2 million Rthl, yield 79500 Rthl) and the '
        'Transact of 1811. The claim of the Curische Erben, 426000 Rthl, guaranteed by the King, is settled at 112000. It asks for an advance of '
        '112/m, the annulment of the Transact, the removal of Cosmar and a report from the OLG Brieg. Nothing on Trąbczyn. The text is now '
        'legible throughout; six places are lost or in doubt.',
 '289': 'Read again in the working session on 2026-10-07 from the text corrected against the archive\'s new scans. Triebenfeld at Vienna (5 May '
        '1815) to Cabinets Rath Albrecht on the claim of the Curische Erben against Prince Hohenlohe: 300/m rt, with interest 426/m rt. The '
        'late King signed as principal debtor; the King disclaimed it, then at Vienna promised the heiresses to have it laid before him at '
        'Berlin, and the heirs withdrew from the settlement at about 112/m rt. Triebenfeld asks for a categorical decision. Trąbczyn is not '
        'mentioned.',
}
DOUBT = {
 '245': [('allersubmiße[...]', 'the end of the word is torn away'), ('geschied[en?]', 'the end of the line is at the edge'),
         ('gekrän[...]', 'the end of the line is lost'), ('praeciat', 'the letters as read; the term is not identified'),
         ('Exc. [...]', 'a small word is torn away'), ('Intresse v[?]', 'the torn end of the line'),
         ('unterschrieb[...]', 'the end of the line is lost'), ('Praeciat', 'the same term as on page 1')],
 '289': [('Heneberg[?]', 'the name is not surely read'), ('zu bring', 'perhaps "zu Brieg"'), ('bitte', 'perhaps "litte"'),
         ('Circa', 'perhaps "mit"')],
}


def letter_lines(corpus, doc):
    """[(letter line number, text)] of one document, numbered as the site numbers them."""
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


def main():
    write = '--write' in sys.argv
    sys.stdout.reconfigure(encoding='utf-8')
    corpus = io.open(os.path.join(UNIT, 'corpus.txt'), encoding='utf-8').read().split('\n')
    rp = os.path.join(UNIT, 'reading.json')
    raw = io.open(rp, encoding='utf-8', newline='').read()
    reading = json.loads(raw)
    sp = os.path.join(UNIT, 'summaries_de.yml')
    sde = io.open(sp, encoding='utf-8', newline='').read()
    for doc in ('245', '289'):
        ll = letter_lines(corpus, doc)
        # every statement of the summary is one of the claims, in order, and nothing else
        left = DE[doc]
        for st, _ in CLAIMS[doc]:
            assert st in left, (doc, st)
            left = left.replace(st, '', 1)
        assert not re.sub(r'[\s.;,]', '', left), (doc, left)
        claims = []
        for st, words in CLAIMS[doc]:
            lines = []
            for w in words:
                hit = [n for n, l in ll if w in l]
                assert len(hit) >= 1, (doc, w)
                lines.append(hit[0])
            claims.append({'statement': st, 'lines': sorted(set(lines))})
        doubt = []
        for w, note in DOUBT[doc]:
            hit = [n for n, l in ll if w in l]
            assert hit, (doc, w)
            doubt.append({'line': hit[0], 'word': w, 'note': note})
        print(doc, len(DE[doc].split()), 'words (German),', len(EN[doc].split()), '(English);', len(claims), 'statements, all found in the letter')
        key = 'oe1bu9454-' + doc
        old = reading[key]
        reading[key] = {'letter': doc, 'legibility': 'legible', 'notes': NOTES[doc], 'claims': claims, 'doubtful_words': doubt,
                        'read_against': 'session 2026-10-07 (intake/scripts/summaries_245_289.py)'}
        assert set(old) >= {'letter', 'claims'}, old.keys()
        m = re.search(r'(?m)^%s: .*$' % re.escape(key), sde)
        assert m, key
        if write:
            sde = sde[:m.start()] + '%s: %s' % (key, DE[doc]) + sde[m.end():]
            for sub, text in (('summaries-raw', EN[doc]), ('summaries-raw-de', DE[doc])):
                p = os.path.join(ROOT, 'cache', sub, key + '.json')
                d = json.load(io.open(p, encoding='utf-8'))
                d['summary'] = text
                d['model'] = 'claude-code-session'
                json.dump(d, io.open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    if write:
        io.open(sp, 'w', encoding='utf-8', newline='').write(sde)
        indent = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)
        out = json.dumps(reading, ensure_ascii=False, indent=indent)
        if '\r\n' in raw:
            out = out.replace('\n', '\r\n')
        io.open(rp, 'w', encoding='utf-8', newline='').write(out + ('\r\n' if raw.endswith('\r\n') else '\n' if raw.endswith('\n') else ''))
        print('written')


if __name__ == '__main__':
    main()
