# -*- coding: utf-8 -*-
"""The summary of APP 53/6/0/-/17, written in the working session.

    python units/app536017/intake/summaries_draft.py

One document, read whole against the scans on 2026-10-07 and summarised in
German from the Latin as read again; the English is a translation of the
German. Claim-checked in the same session (claim_check.yml beside this
file), as read_letters.py --verify checks, not by the paid run.
courtbook.write_summaries writes every place a summary is kept.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'app536017'
REF = 'APP 53/6/0/-/17'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

S = {
 1: ('Eintrag des Landgerichts in Konin von 1589, überschrieben damit, dass Łukomski eine Besichtigung durchzuführen hat. Albertus Trąmpczyński Otha hat als Kläger Thomas Łukomski zum zweiten Mal geladen, nachdem dieser beim ersten Mal ausgeblieben war. Er wirft ihm vor, er habe in diesem Jahr mit anderen Nachbarn im Gut des Dorfes Łukom einen Teich angelegt und durch zu starkes Aufstauen des Wassers eine große Menge Wald, Kiefernwald, unfruchtbare Weide und Wiesen in den Gütern der Dörfer Trąbczyn, Nowa Wieś und Osiny überschwemmt; ein polnischer Satz nennt Eichen, Buchen und Eschen, die zum Bauen und für Bienenbeuten taugten und durch die Überschwemmung abgestorben seien. Den Schaden schätzt der Kläger auf zehntausend ungarische Goldgulden und ebenso viel Schadenersatz. Das Gericht ordnet auf Antrag des Beklagten eine gerichtliche Besichtigung an und gibt einen Gerichtsboten bei, den der Beklagte wählt und bezahlt; er soll sehen, an welchem Ort und auf wessen Grund das Unrecht geschehen ist und ob es geschehen ist. Der Beklagte hat die Besichtigung binnen sechs Wochen am strittigen Ort durchzuführen, beide Parteien müssen anwesend sein, und bei den nächsten Gerichtsterminen in Konin haben sie einen letzten Termin, um das Ergebnis vor Gericht zu hören.',
     'An entry of the land court at Konin of 1589, headed with the words that Łukomski is to carry out an inspection. Albertus Trąmpczyński Otha, as plaintiff, has cited Thomas Łukomski for the second time, after he failed to appear the first time. He charges that Łukomski, with other neighbours, built a pond this year in the estate of the village of Łukom and, by holding back too much water, flooded a great quantity of woodland, pine forest, barren pasture and meadow in the estates of the villages of Trąbczyn, Nowa Wieś and Osiny; a sentence in Polish names oak, beech and ash, fit for building and for bee-trees, killed by the flooding. The plaintiff values the harm at ten thousand Hungarian gold florins and as much again in damages. At the defendant\'s request the court orders a judicial inspection and adds a court messenger, whom the defendant chooses and pays; he is to see in what place and on whose ground the wrong was done, and whether it was done. The defendant must carry out the inspection within six weeks at the place in dispute, both parties must be present, and at the next court terms at Konin they have a final term to hear the outcome before the court.'),
}


def main():
    courtbook.write_summaries(ROOT, UNIT_DIR, SLUG, REF, S,
                              'written in the working session from the Latin as read again\n# (intake/summaries_draft.py, 2026-10-07).')


if __name__ == '__main__':
    main()
