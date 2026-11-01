# -*- coding: utf-8 -*-
"""Insert the summaries of B. Ossol. rkp. 2289 II into site/_data/summaries.yml
and site/_data/summaries_de.yml. Written in session 2026-11-01; run once.
"""
import io

EN = '''ossol2289-001: The copy of Kościuszko's letter of 3 September 1798, written in Paris, to an émigré correspondent who had written to him from Dresden in August of that year - the letter stands in a collection of copies, "Listy, dokumenty i wiersze z lat 1697-1798", made mostly by Stanisław Przyłęcki (B. Ossol. rkp. 2289 II, page 145 of the codex). Kościuszko answers that he read the expressions of goodwill with the same courtesy as in the letters that had reached him in America; he regrets that events did not let him meet the writer in London, and would have liked to know him in person. He will stand by every Pole of a truly Republican soul who fought with him against the enemies of the country, and in the time to come, on the principles the writer's letter mentions, the ways of common defence and the nation's true happiness will be founded. For now care must be taken not to expose, through premature steps while happier events are awaited, the men of goodwill to the persecutions of the enemies. He asks the writer to keep the letter, and promises to preserve his friendship. The letter never names its addressee ("Obywatelu!" is all); the probable identification with Antoni Prusimski rests on Pachoński's entry in the Polish Biographical Dictionary, whose sources cite this very manuscript - its "grzeczna odpowiedź", polite reply, of which the entry says Kościuszko answered the émigré's letter of August 1798 politely, expressing regret that he did not know him in person, only from correspondence.
'''

DE = '''ossol2289-001: Die Abschrift von Kościuszkos Brief vom 3. September 1798, geschrieben in Paris, an einen emigrierten Korrespondenten, der ihm im August desselben Jahres aus Dresden geschrieben hatte - der Brief steht in einer Sammlung von Abschriften, "Listy, dokumenty i wiersze z lat 1697-1798", überwiegend von Stanisław Przyłęcki geschrieben (B. Ossol. rkp. 2289 II, Seite 145 des Sammelbands). Kościuszko antwortet, er habe die Worte des Wohlwollens mit derselben Höflichkeit gelesen wie in den Briefen, die ihn in Amerika erreicht hatten; er bedauert, dass ihn die Umstände nicht hatten in London zu ihm kommen lassen, und hätte den Schreiben gern persönlich kennengelernt. Er wird zu jedem Polen von wahrhaft republikanischer Seele, das mit ihm gegen die Feinde des Landes gekämpft hat, ungetrennt stehen, und in der künftigen Zeit werden auf den Grundsätzen, deren der Brief des Schreibers gedenkt, die Wege der allgemeinen Verteidigung und das wahre Glück der Nation gegründet werden. Vorläufig müsse darauf gesehen werden, die Männer des Wohlwollens nicht durch voreilige Schritte, während günstigere Ereignisse erwartet werden, den Verfolgungen der Feinde auszusetzen. Er bittet den Schreiber, den Brief für sich zu behalten, und verspricht, seine Freundschaft zu bewahren. Der Brief nennt seinen Adressaten nirgends ("Obywatelu!" ist alles); die wahrscheinliche Identifizierung mit Antoni Prusimski ruht auf Pachońskis Artikel im Polnischen Biografischen Wörterbuch, dessen Quellen genau diese Handschrift nennen - seine "grzeczna odpowiedź", die höfliche Antwort, von der der Artikel sagt, Kościuszko habe dem Emigranten auf dessen Brief vom August 1798 höflich geantwortet mit dem Bedauern, ihn nicht persönlich zu kennen, sondern nur aus der Korrespondenz.
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
    assert 'ossol2289-' not in s, path + ': entries already there'
    io.open(path, 'w', encoding='utf-8', newline='\n').write(
        s[:i] + emit(block) + s[i:])
    print('wrote', path)
