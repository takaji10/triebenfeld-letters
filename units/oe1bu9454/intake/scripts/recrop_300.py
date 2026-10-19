# -*- coding: utf-8 -*-
"""Oe 1 Bü 9454, letter 300: the editor's new crops and new transcription (2026-10-15).

    python units/oe1bu9454/intake/scripts/recrop_300.py            # check only
    python units/oe1bu9454/intake/scripts/recrop_300.py --write    # once
    python units/oe1bu9454/intake/scripts/recrop_300.py --reading  # once, after: the reading record

Images. Letter 300's two pages had been cut badly from scans 0537 and 0538: the
first page lost its torn lower left and its right edge, the second its right edge
lower down, so that line starts and ends were missing. The editor cropped both
pages again ("Oe 1_Bü 9454_0537.jpg", "Oe 1_Bü 9454_0538.jpg" in their Downloads
folder) and these replace the processed images 0537_b and 0538_a; the page ids
stay. The old images go to processed/_superseded/, as for letters 245 and 289.

Text. Made line by line, as for 245 and 289, from the text that stood in the
corpus (which had had every correcting pass), the editor's new transcription and
the new crops read through enlarged; where they differ the scan decided. The top
of each page was torn in the original, so the new crops add nothing there; they
restore the line starts of page 1 from "rufen" down and the end of page 2's lines.
  - Read anew from the restored edges: rufen, werden, wegen, entwarf, dem Fürsten,
    weigerte, der F. Rad[ziwiłł]:, Bemerkungen zurück (was "merkungen zuvöd").
  - Corrected against the scan: in Gosztiszyn (was "im"; the place is Gostyszyn,
    letter 298), [...]ni kömt d 22 (was "[...]sei könte"), gerüffelt (was
    "gerichtfelt"), G. H. Posens (was "G L."), seinem, die Piece (was "Prese[?]"),
    werden (line 10, was "worden"), soglei[...] (was "so gleich[...]"), Ha[...]
    (was "Hau[...]"), Peterbourg (twice; was "Petersburg"), gärstig (was
    "gänztig"), Ciszewska (was "Cziszewska"), kömt (was "könne"), und at the end of
    "Schreiben," (was "[...]"), voll (was "woll"), and the dashes and stops the scan
    shows. "Sachen —" is no longer followed by "[...]": nothing is lost there.
  - Supplied in brackets where only the formula's end survives the tear:
    [Durchlauch]tigster Fürst, [Gnädigster] Fürst und Herr!, [Ew]r Durchlaucht.
  - Doubtful: [wüste?] (was "wirten"; the editor: "Wüste"), [gegen?] at the end of
    the Constantin line (the letters at the edge; was "ge[...]").
  - Dateline: "d 20t Januar"; the year is torn away. "2[9?] Januar 1816" is gone.
    The archive's pencil note at the foot of page 1, "20. Jan 1816", now visible on
    the new crop, is added there as letter 289's pencil date was, and dates the
    letter (rulings.yml, dates.read).
  Kept from the corpus where the scan does not decide against it: Organication (his
  spelling), als den pp Fürsten, dem gehörigen, mehrere, diensten, aufopfar¬,
  Gr Furst, Pohln[ische], Schlawenschitz (the settled spelling).
"""
import io
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.dirname(os.path.dirname(UNIT))
RAW = r'J:\Documents\Archive\Genealogy\References\Hohenlohe-Zentralarchiv Neuenstein\Oe 1_Bü 9454\processed'
NEW = r'C:\Users\Tersnaus\Downloads'

P1 = '''300
[Durchlauch]tigster Fürst
[Gnädigster] Fürst und Herr!
[...]halte ich die Nachricht daß in Gosztiszyn ein
[...]schlag abgegeben ist — kein Schreiben ist aber
[...]werde es morgen abhohlen laßen und dan den
[...]Gebrauch davon machen —
[...]ni kömt d 22 nach Posen zurück — Er ward nach Berlin ge¬
rufen um verabschiedet oder wenigstens derbe gerüffelt zu
werden — die Sache war — Es solte von beyden ein Gutachten
wegen Organication des G. H. Posens eingereicht werden — Zerboni
entwarf das mit seinem Secretaire Schmidt und sandte es am Ende
dem Fürsten Radziwiłł zur mit Unterschrift zu — Radziwiłł ver¬
weigerte leztere, weil es das Gegentheil von dem war was
der König selbst dem Fürsten gesagt und zu Ihm befohlen hatte —
der F. Rad[ziwiłł]: sandte also dem Zerboni die Piece mit dem gehörigen
Bemerkungen zurück — Zerboni darüber entrüstet, sagte —
Es ist den Teufel als den pp Fürsten gelegen — Es bedarf seiner
Unterschrift nicht — Ich bin hier regierender Herr —
20. Jan 1816'''
P2 = '''Dies ward dem Fürsten Radziwiłł soglei[...]
im höchsten Grad aigrirt gieng sogleich mit[...]
Gemahlin folgte ihm, und beide beste[...]
der König ließ den Fürsten Ha[...]
"[wüste?] wohl daß d[...]
der p. ist ein un[...]"
Z[erboni] ward sofort nach Berlin[...]
unbekandt — Es heißt Klew[...]
aber die Geld Männer als Stag[...]
ich gehe Behutsam mit meine Sachen —
zu Peterbourg soll es gärstig aussehen —[...]
Senat sollen die Pohln[ische] Constitution, welche der[...]
schönem Ciszewska unterzeichnet hat gänzlich verworfen haben —
Man sagt die Pohlen hätte sich darauf durch eine geheime De¬
putation beym Kayser erklärt daß sie ihm sogleich mit mehrere
hundert tausend Mann zu diensten stehen und alles aufopfar¬
würden um die Constitution aufrecht zu erhalten —
Dies soll dort bekannt worden sein und nun ist der Satan ganz los
Gr Furst Constantin ist wie auf Windes Flügeln nach Peterbourg [gegen?]
Wann mein nach Schlawenschitz gesandter Bothen zurück kömt
Dann gehe ich nach Betsche, und bin ich dort fertig nach Berlin
um das Entschädigungs-Geschäft zu betreiben.
In der Haupt Sache beziehe ich mich auf mein lezteres Schreiben, und
ersterbe Ehrfurchts voll
[Ew]r Durchlaucht
Blizanow
d 20t Januar
ganz unterthäniger Diener
v Triebenfeld'''
PAGES = [('0537_b', P1, '0853_Oe 1_Bue 9454_0537_b.txt', 'Oe 1_Bü 9454_0537.jpg', 'Oe 1_Bü 9454_0537_b.jpg',
          'Oe_1_Bu_9454_0537_b-L300_01.jpg'),
         ('0538_a', P2, '0854_Oe 1_Bue 9454_0538_a.txt', 'Oe 1_Bü 9454_0538.jpg', 'Oe 1_Bü 9454_0538_a.jpg',
          'Oe_1_Bu_9454_0538_a-L300_02.jpg')]
DATE_OLD = '    "247": [1814, 10, 28, "day"]'
DATE_NEW = ('    "300": [1816, 1, 20, "day"]   # "d 20t Januar", the year torn away; the archive\'s pencil note on page 1 '
            'reads "20. Jan 1816" (new crop, 2026-10-15)\n')


def main():
    write = '--write' in sys.argv
    sys.stdout.reconfigure(encoding='utf-8')
    cp = os.path.join(UNIT, 'corpus.txt')
    lines = io.open(cp, encoding='utf-8').read().split('\n')
    for pid, text, txt, new_img, old_img, staged in PAGES:
        new = text.split('\n')
        i = lines.index('[PAGE %s]' % pid)
        j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith(('[PAGE ', '[DOC ')))
        d = max(k for k in range(i) if lines[k].startswith('[DOC '))
        assert lines[d] == '[DOC 300]', lines[d]
        old = lines[i + 1:j]
        print('page %s: %d lines were there, %d now; %d unchanged' % (pid, len(old), len(new), sum(1 for a in new if a in old)))
        assert os.path.isfile(os.path.join(NEW, new_img)) and os.path.isfile(os.path.join(RAW, old_img))
        assert os.path.isfile(os.path.join(UNIT, 'transcriptions', txt))
        if write:
            lines[i + 1:j] = new
            io.open(os.path.join(UNIT, 'transcriptions', txt), 'w', encoding='utf-8', newline='\n').write(text + '\n')
            sup = os.path.join(RAW, '_superseded')
            os.makedirs(sup, exist_ok=True)
            shutil.move(os.path.join(RAW, old_img), os.path.join(sup, old_img))
            shutil.copyfile(os.path.join(NEW, new_img), os.path.join(RAW, old_img))
            shutil.copyfile(os.path.join(NEW, new_img), os.path.join(ROOT, 'pages', staged))
            web = os.path.join(ROOT, 'site', 'assets', 'scans', staged)
            if os.path.isfile(web):
                os.remove(web)                      # made again by make_scan_derivatives.py
    rp = os.path.join(UNIT, 'rulings.yml')
    ru = io.open(rp, encoding='utf-8', newline='').read()
    k = ru.index(DATE_OLD)
    k = ru.index('\n', k) + 1
    assert '"300": [1816' not in ru
    ru = ru[:k] + DATE_NEW + ru[k:]
    if write:
        io.open(cp, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
        io.open(rp, 'w', encoding='utf-8', newline='').write(ru)
        print('written')


if __name__ == '__main__' and '--reading' not in sys.argv:
    main()


def reading_record():
    """The reading record of letter 300 (reading.json), run once after main(): page 1 gained a line (the pencil
    date), so every claim line below line 19 moves by one; the doubtful words the scan has settled (gerichtfelt,
    zuvöd, gänztig, Cziszewska, könne, Ehrfurchts woll) come off, and the new doubts go on; the first claim's
    "overstated" note is resolved, as "G. H. Posens" is now read."""
    import json
    write = '--reading' in sys.argv
    rdp = os.path.join(UNIT, 'reading.json')
    rraw = io.open(rdp, encoding='utf-8', newline='').read()
    reading = json.loads(rraw)
    r = reading['oe1bu9454-300']
    assert any(w['word'] == 'gerichtfelt' for w in r['doubtful_words']), 'already done'
    for c in r['claims']:
        c['lines'] = [n + 1 if n > 19 else n for n in c['lines']]
        c.pop('check', None)
        c.pop('why', None)
    lines = (P1 + '\n' + P2).split('\n')
    doubt = []
    for w, note in [('Gosztiszyn', 'The writer spells it Gostyszyn elsewhere (doc 298); a recorded variant of the place.'),
                    ('Organication', "Organisation; the writer's own spelling."),
                    ('[wüste?]', 'the first word of the quoted line; the old reading had "wirten"'),
                    ('aufopfar¬', "Probably 'aufopfern'."),
                    ('[gegen?]', 'the letters at the edge after "Peterbourg"; the old reading had "ge[...]"')]:
        hit = [n for n, l in enumerate(lines, 1) if w in l]
        assert len(hit) == 1, w
        doubt.append({'line': hit[0], 'word': w, 'note': note})
    r['doubtful_words'] = doubt
    r['read_against'] = (r.get('read_against', '') + '; text made again from the new crops, 2026-10-15 '
                         '(intake/scripts/recrop_300.py)').lstrip('; ')
    for c in r['claims']:
        print(c)
    if write:
        indent = 1 if rraw.startswith('{\n "') else (2 if rraw.startswith('{\n  "') else None)
        out = json.dumps(reading, ensure_ascii=False, indent=indent)
        if '\r\n' in rraw:
            out = out.replace('\n', '\r\n')
        io.open(rdp, 'w', encoding='utf-8', newline='').write(
            out + ('\r\n' if rraw.endswith('\r\n') else '\n' if rraw.endswith('\n') else ''))
        print('reading record written')


if __name__ == '__main__' and '--reading' in sys.argv:
    reading_record()
