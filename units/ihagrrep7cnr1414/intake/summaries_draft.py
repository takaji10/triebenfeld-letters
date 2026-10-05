# -*- coding: utf-8 -*-
"""The summaries of I. HA GR, Rep. 7 C, Nr. 1414, written in the working session.

    python units/ihagrrep7cnr1414/intake/summaries_draft.py

Each document was read whole against its scan on 2026-10-05 and summarised in
German; the English is a translation of the German. They were claim-checked in
the same session (claim_check.yml beside this file), as read_letters.py
--verify checks, not by the paid run. This script writes the records
summarise.py would have written (units/<slug>/summaries_de.yml,
cache/summaries-raw-de/, cache/summaries-raw/). Follows
units/iharep162nr295/intake/summaries_draft.py.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
SLUG = 'ihagrrep7cnr1414'
REF = 'I. HA GR, Rep. 7 C, Nr. 1414'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

S = {
 1: ('Konzept eines Schreibens des Departements der auswärtigen Angelegenheiten, Berlin, 11. Januar 1797, an den Minister Graf von Hoym und gleichlautend an den Minister Freiherr von Schroetter; eine größere Hand fügt den Großkanzler von Goldbeck hinzu, und drei Reinschriften werden angeordnet. Das Departement teilt in Abschrift mit, was der königliche Resident in Venedig, Graf von Cattaneo, auf Verlangen des Anton Prusimski berichtet hat, eines Eingesessenen der von der ehemaligen Republik Polen erworbenen Provinzen, der sich gegenwärtig in Venedig aufhält. Von den beiden Unterschriften ist die zweite die des Ministers Haugwitz. Am 12. gingen alle Schreiben zur Post.',
     "Draft of a letter of the Department of Foreign Affairs, Berlin, 11 January 1797, to the minister Count von Hoym and in the same words to the minister Baron von Schroetter; a larger hand adds the Grand Chancellor von Goldbeck, and three fair copies are ordered. The department communicates in copy what the royal resident at Venice, Count von Cattaneo, has reported at the request of Anton Prusimski, a resident of the provinces acquired from the former Republic of Poland, who is at present staying at Venice. Of the two signatures the second is that of the minister Haugwitz. On the 12th all the letters went to the post."),
 2: ('Auszug aus der Depesche Nr. 423 des Grafen Cattaneo, Venedig, 14. Dezember 1796, in französischer Sprache. Der polnische Edelmann Antoine Prusimski ist bei ihm erschienen, in wirklich zerrütteter Gesundheit und durch den Tod seiner Frau fast bis zur Stumpfheit getroffen, und hat um ein Attest über seine traurige Lage und darüber gebeten, dass er gegenwärtig und in dieser Jahreszeit nicht reisen könne. Cattaneo glaubte es ihm nicht verweigern zu können: Wer schon erschöpft sei, wenn er von einem Haus ins andere gehe, könne nicht von einem Land ins andere reisen. Das Departement erhielt den Auszug am 2. Januar 1797 und leitete ihn dem Herrn von Raumer zu; dieser verfügte am 8. Januar, Hoym und Schrötter zu benachrichtigen.',
     "Extract from dispatch No. 423 of Count Cattaneo, Venice, 14 December 1796, in French. The Polish gentleman Antoine Prusimski came to him in truly ruined health and dulled almost to stupor by the death of his wife, and asked for a certificate of his sad situation and that he could not travel at present and in that season. Cattaneo did not think he could refuse it: a man who is exhausted by going from one house to another cannot travel from one country to another. The department received the extract on 2 January 1797 and routed it to Mr von Raumer, who directed on 8 January that Hoym and Schrötter be notified."),
 3: ('Schrötter dankt dem Departement der auswärtigen Angelegenheiten für die Nachricht vom 11. des Monats über Anton Prusimski, der in der neuen Erwerbung von Polen ansässig ist und sich gegenwärtig in Venedig aufhält. Er hat davon dem Staatsminister Graf von Hoym weiter Nachricht gegeben, weil nicht feststeht, ob Prusimski in Neuostpreußen oder in Südpreußen ansässig ist. Berlin, 29. Januar 1797. Das Departement erhielt das Schreiben am 8. Februar und legte es am 16. März zu den Akten.',
     "Schrötter thanks the Department of Foreign Affairs for the news of the 11th of the month about Anton Prusimski, who is settled in the new acquisition from Poland and is at present staying at Venice. He has passed it on to the Minister of State Count von Hoym, because it is not established whether Prusimski is settled in New East Prussia or in South Prussia. Berlin, 29 January 1797. The department received the letter on 8 February and put it with the files on 16 March."),
}


def main():
    with open(os.path.join(UNIT_DIR, 'summaries_de.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# German summaries of {REF}, written in the working session from a\n'
                '# reading of each document against its scan (intake/summaries_draft.py, 2026-10-05).\n'
                '# Claim-checked in session on 2026-10-05 (intake/claim_check.yml).\n'
                '# A finding aid, not part of the edition text. Published\n'
                '# through summarise.py --build --lang de.\n')
        for n, (de, _en) in sorted(S.items()):
            f.write(f'{SLUG}-{n:03d}: {json.dumps(de, ensure_ascii=False)}\n')
    for lang, sub, i in (('de', 'summaries-raw-de', 0), ('en', 'summaries-raw', 1)):
        d = os.path.join(ROOT, 'cache', sub)
        os.makedirs(d, exist_ok=True)
        for n, pair in S.items():
            pad = f'{SLUG}-{n:03d}'
            json.dump({'letter': str(n), 'pad': pad, 'summary': pair[i],
                       'model': 'in-session, 2026-10-05; claim-checked in session',
                       'usage': {'input': 0, 'output': 0, 'cache_read': 0}},
                      open(os.path.join(d, pad + '.json'), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
    print(len(S), 'summaries written, German and English')


if __name__ == '__main__':
    main()
