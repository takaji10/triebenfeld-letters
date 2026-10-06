# -*- coding: utf-8 -*-
"""The summary of APP 53/17/0/-/Konin Gr.145, written in the working session.

    python units/app53170koningr145/intake/summaries_draft.py

The holding is one document. Its summary was written in German on 2026-10-06
from the editor's English translation and their outline of the record, with
the Polish beside it for the passages quoted in the claim check; the English
is a translation of the German. After every page had been read against its
scan, the sentence on Stanisław Chełmski's sentence was rewritten: the
finding on the raid on the inn had been missing from the Polish. It was
claim-checked in the same session (claim_check.yml beside this file), as read_letters.py --verify checks, not by
the paid run. This script writes the records summarise.py would have written
(units/<slug>/summaries_de.yml, cache/summaries-raw-de/, cache/summaries-raw/).
The lines in site/_data/summaries.yml and summaries_de.yml were put in by
hand. Follows units/ihagrrep7cnr1414/intake/summaries_draft.py.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
SLUG = 'app53170koningr145'
REF = 'APP 53/17/0/-/Konin Gr.145'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

S = {
 1: ("Dekret einer Grenzkommission, am 23. September 1776 in die Burggerichtsakten von Brześć Kujawski eingetragen und nach einem Auszug daraus in das Gerichtsbuch von Konin übernommen. Die Kommission war durch einen Beschluss des Reichstags eingesetzt, der am 1. Juni 1774 in Warschau zu den Akten gegeben wurde, um den seit Jahrzehnten geführten Grenzstreit zwischen Trąbczyn, dem Gut des Antoni Prusimski, Starost von Niszczewice, und Łukomia, dem Gut der Brüder Chełmski, endgültig zu entscheiden. Sie trat am 13. September 1775 unter dem Vorsitz von Ludwik Dąmbski, Woiwode von Brześć Kujawski, im Wald auf dem strittigen Grund zusammen. Ein Streit darüber, welcher Kommissar die Feder führen solle, spaltete das Gericht; ein Vergleich, den es den Parteien vorschlug, kam nicht zustande, und es verhandelte geteilt weiter. Prusimski führte das Gericht seine Grenzlinie entlang, an Wegen, Grenzhügeln, eingekerbten Bäumen, Waldstücken und einem Teichgrund vorbei, und berief sich auf Urkunden und beeidete Zeugenverhöre. Das Gericht prüfte auch die Linie Chełmskis, erkannte Prusimskis Grenzlinie als die bessere an, ließ zwischen Trąbczyn und Łukomia und zwischen Trąbczyn und Biskupice neue Grenzhügel aufwerfen und legte Prusimski auf, sie auf dem letzten Hügel mit sechs Zeugen zu beschwören. Stanisław Chełmski wurde wegen der Übergriffe auf Trąbczyner Grund und wegen eines bewaffneten Überfalls auf das Wirtshaus an der Landstraße, bei dem in das Haus geschossen und es angezündet wurde, zu zwei Wochen Turmhaft in Konin und zu Bußen an Prusimski verurteilt, dazu zu 8.000 polnischen Gulden für gefälltes Holz und andere Schäden. Die Fortsetzung der Grenze gegen Biskupice wurde auf den 21. Mai 1776 vertagt. Sechs Kommissare und der Kalischer Grenzvermesser Wojciech Czarnecki, der die Hügel aufwarf, unterzeichnen.",
     "The decree of a boundary commission, entered in the castle court records at Brześć Kujawski on 23 September 1776 and copied from an extract of them into the court book of Konin. The commission was appointed by an act of parliament, recorded at Warsaw on 1 June 1774, to decide once and for all the boundary dispute, decades old, between Trąbczyn, the estate of Antoni Prusimski, Starost of Niszczewice, and Łukomia, the estate of the Chełmski brothers. It met on 13 September 1775, in the forest on the disputed ground, under Ludwik Dąmbski, voivode of Brześć Kujawski. A quarrel over which commissioner should hold the pen split the court; a settlement it proposed to the parties was not reached, and it went on sitting divided. Prusimski led the court along his boundary line, past roads, boundary mounds, blazed trees, woods and a pond-ground, and relied on documents and sworn examinations of witnesses. The court also examined Chełmski's line, found Prusimski's boundary line the better, had new boundary mounds raised between Trąbczyn and Łukomia and between Trąbczyn and Biskupice, and required Prusimski to swear to it on the last mound with six witnesses. Stanisław Chełmski, for his encroachments on Trąbczyn ground and for an armed raid on the inn on the highway, in which shots were fired into the house and it was set alight, was sentenced to two weeks in the tower at Konin and to penalties payable to Prusimski, and besides to 8,000 Polish złoty for felled timber and other damage. The rest of the boundary with Biskupice was adjourned to 21 May 1776. Six commissioners sign, and with them Wojciech Czarnecki, the boundary surveyor of Kalisz, who raised the mounds."),
}


def main():
    with open(os.path.join(UNIT_DIR, 'summaries_de.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# German summary of {REF}, written in the working session from the\n'
                "# editor's English translation and outline, with the Polish beside it\n"
                '# (intake/summaries_draft.py, 2026-10-06).\n'
                '# Claim-checked in session on 2026-10-06 (intake/claim_check.yml).\n'
                '# A finding aid, not part of the edition text.\n')
        for n, (de, _en) in sorted(S.items()):
            f.write(f'{SLUG}-{n:03d}: {json.dumps(de, ensure_ascii=False)}\n')
    for lang, sub, i in (('de', 'summaries-raw-de', 0), ('en', 'summaries-raw', 1)):
        d = os.path.join(ROOT, 'cache', sub)
        os.makedirs(d, exist_ok=True)
        for n, pair in S.items():
            pad = f'{SLUG}-{n:03d}'
            json.dump({'letter': str(n), 'pad': pad, 'summary': pair[i],
                       'model': 'in-session, 2026-10-06; claim-checked in session',
                       'usage': {'input': 0, 'output': 0, 'cache_read': 0}},
                      open(os.path.join(d, pad + '.json'), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
    print(len(S), 'summary written, German and English')


if __name__ == '__main__':
    main()
