# -*- coding: utf-8 -*-
"""Insert the summaries of APP 53/4/0/-/62 into site/_data/summaries.yml
and site/_data/summaries_de.yml. Written in session 2026-10-26; run once.
"""
import io

EN = '''app534062-001: The report of the court messenger Sebastian Szetlewicz of Szetlewko (Szetlewek), an entry at the foot of page 222 of the relation and citation book of the land court at Kalisz for 1726-1727, of the sitting of 1727. He reports to the court that he had carried a citation to the estate of the village of Szetlew, to the residence of the party cited, and, on the Thursday next past, had laid and left it there on the table in the heated room, before the cited party's "Conte~" [as written; a word not fully read, perhaps a household member]. The entry gives neither the case nor the parties; the report's opening formula does not fully parse as transcribed, and the entry closes with the phrase "of which, the present report". The holding was added for the messenger's name - it shows a Szetlewicz family living at Szetlewek in the 1720s, over fifty years before the messenger Mathias Matuszkiewicz "de villa Szetlewek" reports in the Konin register.
'''

DE = '''app534062-001: Der Bericht des Gerichtsboten Sebastian Szetlewicz von Szetlewko (Szetlewek), ein Eintrag am Fuß von Seite 222 des Relations- und Zitationsbuchs des Landgerichts in Kalisz für 1726-1727, von der Sitzung des Jahres 1727. Er trägt dem Gericht vor, dass er eine Ladung zum Gut des Dorfes Szetlew, an die Wohnung des Geladenen gebracht und am vorvergangenen Donnerstag dort auf dem Tisch im beheizten Raum niedergelegt und zurückgelassen hat, vor dem „Conte~“ [wie geschrieben; ein nicht sicher gelesenes Wort, vielleicht ein Haushaltsangehöriger] des Geladenen. Der Eintrag nennt weder die Sache noch die Parteien; die Eingangsformel des Berichts ergibt sich in der Abschrift nicht ganz, und der Eintrag schließt mit der Wendung „of which, the present report“. Die Holding wurde um des Namens des Boten willen aufgenommen - er zeigt eine Familie Szetlewicz, die in den 1720er Jahren in Szetlewek wohnte, über fünfzig Jahre bevor der Bote Mathias Matuszkiewicz „de villa Szetlewek“ im Koniner Register berichtet.
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
    i = s.index('app536017-001:')
    assert 'app534062-' not in s, path + ': entries already there'
    io.open(path, 'w', encoding='utf-8', newline='\n').write(
        s[:i] + emit(block) + s[i:])
    print('wrote', path)
