# -*- coding: utf-8 -*-
"""Insert the summaries of APP 53/20/0/-/Poznań Gr.1181 into
site/_data/summaries.yml and site/_data/summaries_de.yml. Written in
session 2026-10-26 (from the session's English of the document); run once.
"""
import io

EN = '''app5320pozgr1181-001: The decree of the condescensio held at the grounds of Trąbczyn, at the manor there, on Monday after Judica Sunday, 29 March 1784, by the castellany offices of Greater Poland sitting on the ultimate limitation of the succession the sterile brothers Antoni and Paweł Prusimski left. The parties: Antoni in Kolno Prusimski, captain of Nieśwież, knight of the Order of St Stanisław, against the heirs of the sisters - the Zakrzewski, Tomicki, Taczanowski, Kołaczkowski and Tworowicz parties - with the abbot and convent of Ląd cited over the reproduction of the quietation of 3,500 Hungarian ducats and of the jewels and silver of the Prusimski house lodged in the convent's treasury. After the sworn bringing of the documents (completed December 1783), the decree recites the suit's whole documentary history: the tribunal's decree of 8 October 1782 [the scribe writes the 8th, the Monday after St Francis of that year was the 7th]; the fraternal division of 1740 with its three schedas and their loads, from the wadion of 1700 and the death of Ludwik at Kamionna in 1708 to the dowry provisions and quietations of the three daughters; the maternal Golinski estates (Oporowo with Oporówka and Kałowo, Prusinowo, Szetlewek) with their arendas and their church inscriptions back to 1616. The court's own determinations: the clean maternal fortune of 98,379 florins groschen 5 Polish divided among six capits, three brothers and three sisters, at 16,396 florins groschen 15 and 2 1/2 solidi each; the clean paternal fortunes adjudged to the captain as the brother's son [written "filiaster"], Paweł's scheda at 154,436 florins groschen 24 1/2 Polish and his own at 154,936 florins groschen 24 1/2, each after the deduction of the maternal portion; the widow Nierzychowska's 30,000, though quieted in 1740, and Puchalski's 10,000, presumed pacified, not judged as borne over, so that nothing out of them can come to the female sex; the Radoliński successors' claim of 43,000 florins Polish on Trąbczyn - its letter of 1736 disputed as not in Andrzej Radoliński's hand, the cause remanded to Gniezno and undecided since 1777, the 18,000 enumerated left standing as the original sum with the load removed, pending the final decision in the competent forum. The last page opens the question of what the brothers alienated beyond the division: Katarzyna née Rozdrażewska, widow of Paweł, and her 40,000 florins Polish inscribed in 1745 on Peczyska and Dubno; the condescensio term at Grab of 3 June 1782 with Ludwik Bogdański, chamberlain of Kalisz, and Teresa née Rozdrażewska; and at the naming of Ewa de Maniewska Potocka, widow of Joachim Potocki, the entry breaks off mid-sentence.
'''

DE = '''app5320pozgr1181-001: Das Dekret der Kondeszension, gehalten auf dem Grund von Trąbczyn, im dortigen Gutshaus, am Montag nach Judika, dem 29. März 1784, durch die Kastellaneiämter Großpolens über die ultimative Limitation der Erbschaft der kinderlos verstorbenen Brüder Antoni und Paweł Prusimski. Die Parteien: Antoni in Kolno Prusimski, Kapitän von Nieśwież, Ritter des St.-Stanislaus-Ordens, gegen die Erben der Schwestern - die Parteien Zakrzewski, Tomicki, Taczanowski, Kołaczkowski und Tworowicz - mit dem Abt und Konvent von Ląd, zitiert wegen der Reproduktion der Quittung über 3500 ungarische Dukaten und der Juwelen und des Silbers des Prusimski-Hauses, im Schatz des Konvents niedergelegt. Nach dem beeidigten Einbringen der Urkunden (vollendet Dezember 1783) rezitiert das Dekret die ganze Urkundengeschichte des Rechtsstreits: das Tribunalsdekret vom 8. Oktober 1782 [der Schreiber schreibt den 8., der Montag nach dem Franziskusfest jenes Jahres war der 7.]; die brüderliche Teilung von 1740 mit ihren drei Lotschechten und ihren Lasten, vom Wadium von 1700 und dem Tod Ludwiks in Kamionna 1708 bis zu den Mitgiftbestimmungen und Quittungen der drei Töchter; die mütterlichen Golinski-Güter (Oporowo mit Oporówka und Kałowo, Prusinowo, Szetlewek) mit ihren Pachten und ihren Kircheneintragungen bis zurück zu 1616. Die eigenen Feststellungen des Gerichts: die reine mütterliche Vermögensmasse von 98 379 Florin Groschen 5 polnisch, geteilt unter sechs Kapitalien, drei Brüder und drei Schwestern, zu je 16 396 Florin Groschen 15 und 2 1/2 Solidi; die reinen väterlichen Vermögensmassen, dem Kapitän als dem Sohn des Bruders [geschrieben "filiaster"] zugesprochen, die Lotschecht Pawełs zu 154.436 Florin Groschen 24½ polnisch und seine eigene zu 154.936 Florin Groschen 24½, jede nach dem Abzug des mütterlichen Anteils; die 30 000 der Witwe Nierzychowska, obgleich 1740 quittiert, und die 10 000 Puchalskis, als bezahlt vermutet, nicht als übergetragen geurteilt, so dass daraus für den weiblichen Stand nichts herauskommen kann; die Forderung der Nachfolger Radolińskis von 43 000 Florin polnisch auf Trąbczyn - deren Schrift von 1736 als nicht von der Hand Andrzej Radolińskis bestritten, die Sache an Gniezno verwiesen und seit 1777 unentschieden, die 18 000 aufgezahlten als ursprüngliche Summe mit aufgehobener Last stehengelassen, bis zur endgültigen Entscheidung am zuständigen Gericht. Die letzte Seite eröffnet die Frage, was die Brüder über die Teilung hinaus veräußert haben: Katarzyna geb. Rozdrażewska, Witwe Pawełs, und ihre 40 000 Florin polnisch, 1745 auf Peczyska und Dubno eingetragen; der Kondeszensionstermin zu Grab vom 3. Juni 1782 mit Ludwik Bogdański, Kämmerer von Kalisz, und Teresa geb. Rozdrażewska; und bei der Nennung von Ewa de Maniewska Potocka, Witwe des Joachim Potocki, bricht der Eintrag mitten im Satz ab.
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
    assert 'app5320pozgr1181-' not in s, path + ': entries already there'
    i = s.index('app539680782-001:')
    io.open(path, 'w', encoding='utf-8', newline='\n').write(
        s[:i] + emit(block) + s[i:])
    print('wrote', path)
