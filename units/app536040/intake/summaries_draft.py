# -*- coding: utf-8 -*-
"""The summary of APP 53/6/0/-/40, written in the working session.

    python units/app536040/intake/summaries_draft.py

One document, read whole against the scans on 2026-10-07 and summarised in
German from the corrected Latin; the English is a translation of the German.
Claim-checked in the same session (claim_check.yml beside this file), as
read_letters.py --verify checks, not by the paid run.
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

SLUG = 'app536040'
REF = 'APP 53/6/0/-/40'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

S = {
 1: ('Dekret des Landgerichts in Konin aus der Sitzung, die am Montag nach Septuagesima 1728 begann, überschrieben „Decretum Locationis“. Die Brüder Franciszek und Józef Ścibor Chełmski, Erbherren von Łukom und Łomowo, haben Krzysztof Prusimski als Hauptbeklagten, seinen Sohn Antoni, sechs namentlich genannte adlige Dienstleute und ungenannte Untertanen von Trąbczyn geladen; die Klage war schon zur Sitzung nach Trinitatis 1727 erhoben und damals nicht entschieden worden. Sie werfen Prusimski vor, er habe ohne Rücksicht auf nachbarliche Freundschaft hundert Schock Schindeln, die auf ihrem Grund gefertigt worden waren, samt einer Hütte verbrennen lassen, wobei Kinder, die in der Hütte lebten, beinahe verbrannt wären; er habe vier Arbeitsochsen, die für die Glashütte gehalten wurden, bei einem bewaffneten Überfall wegnehmen lassen und Józef Chełmski nach dem Leben getrachtet; und er habe, während die Kläger am Krontribunal in Piotrków waren, seinen Sohn, die Dienstleute und Untertanen bewaffnet auf Grund geschickt, der seit alters zu Łukom gehöre, und dort Heu in nicht geringer Zahl von Fuhren wegnehmen lassen. Beide Seiten erscheinen vor Gericht. Das Gericht befindet, dass ein vereidigter Kommissar der Woiwodschaften Posen und Kalisz, Wojciech Biskupski, auf den beide sich geeinigt haben, mit je zwei Freunden beider Seiten am Montag nach dem Sonntag Misericordia auf den strittigen Grund gehen muss; sie sollen über das Eigentum am Grund, die Gewalttaten und die Schäden alte, kundige Zeugen unter Eid vernehmen und alle Ansprüche entscheiden. Berufung ist nur gegen das Endurteil zulässig. Beide Parteien haben eine Buße von vierzehn polnischen Mark zu zahlen, halb an die Gegenseite und halb an das Gericht; wer dem Dekret nicht nachkommt, verfällt der Verbannung.',
     'A decree of the land court at Konin, of the sitting that opened on the Monday after Septuagesima 1728, headed "Decretum Locationis". The brothers Franciszek and Józef Ścibor Chełmski, heirs of Łukom and Łomowo, have cited Krzysztof Prusimski as principal defendant, his son Antoni, six noblemen in his service, who are named, and unnamed subjects of Trąbczyn; the suit had been brought at the sitting after Trinity 1727 and was not decided then. They charge that Prusimski, with no regard for neighbourly friendship, had a hundred threescore of shingles made on their ground burned together with a hut, so that children living in the hut were nearly burned; that he had four working oxen kept for the glassworks taken in an armed raid, and plotted against Józef Chełmski\'s life; and that, while the plaintiffs were at the Crown Tribunal at Piotrków, he sent his son, the retainers and the subjects in arms onto ground that belongs to Łukom from of old, and had hay taken there in no small number of cartloads. Both sides appear before the court. The court finds that a sworn commissioner of the provinces of Poznań and Kalisz, Wojciech Biskupski, on whom both have agreed, with two friends of each side, must go onto the disputed ground on the Monday after Misericordia Sunday; they are to examine old and knowledgeable witnesses on oath about the ownership of the ground, the acts of violence and the damage, and to decide all the claims. Appeal lies only from the final sentence. Both parties are to pay a penalty of fourteen Polish marks, half to the other side and half to the court; whoever does not comply with the decree falls under banishment.'),
}


def main():
    courtbook.write_summaries(ROOT, UNIT_DIR, SLUG, REF, S,
                              'written in the working session from the corrected Latin\n# (intake/summaries_draft.py, 2026-10-07).')


if __name__ == '__main__':
    main()
