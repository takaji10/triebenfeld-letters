# -*- coding: utf-8 -*-
"""Insert the summaries of APP 53/968/0/-/782 into site/_data/summaries.yml
and site/_data/summaries_de.yml. Written in session 2026-10-25; run once.
"""
import io

EN = '''app539680782-001: The contract of 14 March 1820 between the village board of Tropiczyner Holland and the school teacher Samuel Adolph of Borwiezer Holland. The board had put him to the test and took a liking to him [the manuscript reads "an ihm einen gefallen fragen"], and contracts with him and issues him the appointment. Ten numbered terms follow: free dwelling; to the school three Morgen of land and some meadow, which he may use without payment, the land tilled by the community; from the community five Viertel of grain and a half Viertel of seed, which he must carry at his going; school money of 3 Groschen for a child learning from the a b c to reading and 6 Groschen for writing and reckoning; a present of 1 St. from every child that is confirmed; term 7 standing with its number and nothing after it; burial fees of 7 Böhm 3 Groschen for an old corpse and 1 St. for a child; at the high feasts of Christmas, Easter and Whitsun an Opfertorium [an offering] from every Wirt of 6 gl.; and a New Year's round, New Year 6 Groschen Polish and Green Thursday 3 Groschen Polish. The teacher binds himself on this contract to continue his office as an honest man, the Sunday school as well as the children's teaching; the board issues the contract for one year and binds itself to fulfil its side faithfully, and the three sign: Johann George Lindner, village mayor; Christoph Rimpel, assessor; Samuel Gellert, gerichten [as written].
'''

DE = '''app539680782-001: Der Kontrakt vom 14. März 1820 zwischen der Gemeinde von Tropiczyner Holland und dem Schul Lehrer Samuel Adolph aus Borwiezer Holland. Die Gemeinde hatte ihn zur Probe gestellt und Gefallen an ihm gefunden [das Manuskript liest sich "an ihm einen gefallen fragen"], kontraktiert sich mit ihm und stellt ihm die Vocation aus. Es folgen zehn nummerierte Punkte: freie Wohnung; zu der Schule drei Morgen Land und etwas Wiese, das er ohne Entgelt gebrauchen kann, vom Ackerland die Gemeinde bestellt; von der Gemeinde fünf Viertel Korn und ein halb Viertel aus Saat, die er beim Abzug zu fahren hat; Schulgeld von 3 Groschen für ein Kind, das vom a b c bis zum Lesen lernt, und 6 Groschen für Schreiben und Rechnen; ein Präsent von 1 St. von jedem eingesegneten Kind; Punkt 7 mit seiner Nummer und nichts dahinter; Begräbnißgebühren von 7 Böhm 3 Groschen für eine alte Leiche und 1 St. für ein Kind; an den hohen Festtagen von Weihnachten, Ostern und Pfingsten ein Opfertorium [eine Gabe] von jedem Wirt von 6 gl.; und ein Neujahrsumgang, Neujahr 6 Groschen polnisch und Grüner Donnerstag 3 Groschen polnisch. Der Lehrer verobligiert sich auf diesen Kontrakt, sein Amt als ein rechtschaffener Mann fortzusetzen, die Sonntags Schule so wie auch Kinder Lehre; die Gemeinde stellt den Kontrakt auf ein Jahr und verobligiert sich, ihre Seite treulich zu erfüllen, und die drei unterschreiben: Johann George Lindner, Schulze; Christoph Rimpel, Beisitzer; Samuel Gellert, gerichten [wie geschrieben].
'''

def quote(v):
    """One entry as a single-quoted YAML scalar (colons, apostrophes safe)."""
    return "'" + v.replace("'", "''") + "'"


def emit(block):
    out = []
    for line in block.splitlines():
        if not line.strip():
            continue
        key, val = line.split(': ', 1)
        out.append(key + ': ' + quote(val))
    return '\n'.join(out) + '\n'


for path, block in (('site/_data/summaries.yml', EN),
                    ('site/_data/summaries_de.yml', DE)):
    s = io.open(path, encoding='utf-8').read()
    i = s.index('app539680545-001:')
    assert 'app539680782-' not in s, path + ': entries already there'
    io.open(path, 'w', encoding='utf-8', newline='\n').write(
        s[:i] + emit(block) + s[i:])
    print('wrote', path)
