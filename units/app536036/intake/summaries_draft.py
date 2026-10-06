# -*- coding: utf-8 -*-
"""The summaries of APP 53/6/0/-/36, written in the working session.

    python units/app536036/intake/summaries_draft.py

Two documents. Each was read whole against the scan on 2026-10-06 and
summarised in German from the corrected Latin; the English is a translation
of the German. They were claim-checked in the same session (claim_check.yml
beside this file), as read_letters.py --verify checks, not by the paid run.
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

SLUG = 'app536036'
REF = 'APP 53/6/0/-/36'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

S = {
 1: ('Versäumnisurteil des Landgerichts in Konin aus dessen Sitzung von 1644, überschrieben „Contumaces“. Jerzy Chełmski hat als Kläger die Brüder Marcin, Wojciech, Władysław und Andrzej Trąmpczyński, Söhne des verstorbenen Stanisław, und dessen Witwe Anna von Słończyce geladen, die an seinem Nachlass ihr Leibgedinge und ein lebenslanges Nutzungsrecht hat. Er wirft ihnen vor, sie hätten ihre Untertanen in seinen eigenen Wald beim Dorf Łukom geschickt und dort etwa achtzig Kerben nach Art von Grenzzeichen in Bäume schlagen lassen, um einen großen Teil seines Grundes ihrem eigenen zuzuschlagen. Den Schaden setzt er, den Grund selbst nicht gerechnet, auf tausend polnische Mark und ebenso viel Schadenersatz an und verlangt, dass die Zeichen nach Hinzuziehung des Unterkämmereramts getilgt werden. Die Beklagten wurden durch den Gerichtsboten Mikołaj Jaworowski von Karmin aufgerufen und erschienen im ersten Termin nicht; der Kläger verurteilte sie mit Zulassung des Gerichts in die Strafe des Ungehorsams. Der Gerichtsbote Bartłomiej Koelmarek von Łukom erklärt, er habe die Ladung am vergangenen Montag im Hof der Geladenen im Dorf Trąbczyn in Gegenwart des Gesindes niedergelegt.',
     'A judgment by default of the land court at Konin, of its sitting of 1644, headed "Contumaces". Jerzy Chełmski, as plaintiff, has cited the brothers Marcin, Wojciech, Władysław and Andrzej Trąmpczyński, sons of the late Stanisław, and his widow Anna of Słończyce, who holds her dower and a life interest in what he left. He charges that they sent their subjects into his own woodland by the village of Łukom and had about eighty notches cut into trees there in the manner of boundary marks, so as to add a great part of his ground to their own. He reckons the harm, leaving the ground itself aside, at a thousand Polish marks and as much again in damages, and demands that the marks be annulled once the sub-chamberlain\'s office has been brought out. The defendants were called by the court messenger Mikołaj Jaworowski of Karmin and did not appear at the first term; the plaintiff condemned them, with the court\'s leave, in the penalty of contumacy. The court messenger Bartłomiej Koelmarek of Łukom declares that he laid the citation on the Monday before at the manor of the cited in the village of Trąbczyn, in the presence of the household.'),
 2: ('Zweites Versäumnisurteil derselben Sitzung von 1644, gegen dieselben Beklagten und mit denselben Worten wie das erste. Jerzy Chełmski wirft den Trąmpczyński vor, sie hätten in den Wäldern, die zum Dorf und Gut Łukom gehören, vor kurzem etwa hundert zum Bauen taugliche Bäume, vor allem Kiefern, und etwa dreihundert Fuhren Brennholz schlagen lassen und nach Belieben verwendet. Den Schaden setzt er, den Grund selbst nicht gerechnet, auf dreihundert polnische Mark an. Für das Übrige verweist der Eintrag auf den vorangehenden.',
     'A second judgment by default of the same sitting of 1644, against the same defendants and in the same words as the first. Jerzy Chełmski charges that the Trąmpczyńskis lately had about a hundred trees fit for building, chiefly pines, and about three hundred cartloads of firewood felled in the woods belonging to the village and estate of Łukom, and used them as they pleased. He reckons the harm, leaving the ground itself aside, at three hundred Polish marks. For the rest the entry refers to the one before it.'),
}


def main():
    courtbook.write_summaries(ROOT, UNIT_DIR, SLUG, REF, S,
                              'written in the working session from the corrected Latin\n# (intake/summaries_draft.py, 2026-10-06).')


if __name__ == '__main__':
    main()
