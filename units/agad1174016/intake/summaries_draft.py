# -*- coding: utf-8 -*-
"""The summaries of AGAD 1/174/0/1/6, written in the working session.

    python units/agad1174016/intake/summaries_draft.py

Each document was read whole against its scan on 2026-10-04 and summarised in
German; the English is a translation of the German. They were claim-checked in
session on 2026-10-05 (claim_check.yml beside this file), as read_letters.py
--verify checks, not by the paid run: all supported.
This script writes the records summarise.py would have written
(units/<slug>/summaries_de.yml, cache/summaries-raw-de/, cache/summaries-raw/),
so that `summarise.py --build` publishes them. Follows
units/iiihamdaiiinr12367/intake/summaries_draft.py.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
SLUG = 'agad1174016'
REF = 'AGAD 1/174/0/1/6'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

S = {
 1: ('Eintrag im Register der Regierungskommission, in polnischer Sprache: eine Anordnung an den Direktor der inneren Angelegenheiten, in Warschau in der Sitzung vom 12. Juli 1807 ergangen. Die Kommission übersendet ihm in beglaubigter Abschrift das Dekret des Kaisers der Franzosen und Königs von Italien, am 5. Juni in Finckenstein erlassen, das ihrem Mitglied Wybicki den Besitz der Güter Manieczki, Przylepki, Boreczek und Esterpol zurückgibt, die im Departement Poznań sequestriert waren und über die die preußische Regierung verfügt hatte, und das der provisorischen polnischen Regierung die Ausführung aufträgt. Der Direktor soll das Dekret unverzüglich ausführen: der Verwaltungskammer des Departements Poznań befehlen, die Güter für Wybicki zu übergeben, und ihn ohne Verzug in den Besitz einweisen lassen. Unter dem Eintrag stehen die Namen des Präsidenten Stanisław Małachowski und des Generalsekretärs Jan Łuszczewski.',
     'An entry in the register of the Governing Commission, in Polish: an order to the Director of Internal Affairs, given at Warsaw at the session of 12 July 1807. The commission sends him a certified copy of the decree of the Emperor of the French and King of Italy, given at Finckenstein on 5 June, which returns to its member Wybicki the possession of the estates of Manieczki, Przylepki, Boreczek and Esterpol, sequestrated in the department of Poznań and disposed of by the Prussian government, and charges the provisional Polish government with carrying it out. The director is to carry out the decree without delay: to order the administrative chamber of the department of Poznań to hand the estates over for Wybicki, and to have him put in possession at once. Under the entry stand the names of the president, Stanisław Małachowski, and the secretary general, Jan Łuszczewski.'),
 2: ('Eintrag im Register der Regierungskommission, in polnischer Sprache, mit dem das Verzeichnis der Beschlüsse beginnt, die die Kommission während ihres Aufenthalts in Dresden gefasst hat. Der Beschluss vom 21. Juli 1807 stellt die von der preußischen Regierung konfiszierten Erbgüter der Michalina Dąbska, des Generals Niemojewski und Wichrowskis unter das Urteil, das der Kaiser zugunsten Wybickis erlassen hat. Die Sache der Michalina Dąbska, geborene Prusimska, sei der Kommission vom Kaiser überwiesen worden; nach dem Vorbild des in Finckenstein erlassenen Dekrets vom 5. Juni dehnt die Kommission das Urteil auf die drei Fälle aus, damit die Güter an ihre wahren Eigentümer zurückfallen. Unter dem Eintrag stehen die Namen des Präsidenten Stanisław Małachowski und des Generalsekretärs Jan Łuszczewski.',
     'An entry in the register of the Governing Commission, in Polish, which opens the record of the resolutions the commission took during its stay at Dresden. The resolution of 21 July 1807 brings the hereditary estates of Michalina Dąbska, General Niemojewski and Wichrowski, confiscated by the Prussian government, under the judgment the Emperor gave in favour of Wybicki. The case of Michalina Dąbska, born Prusimska, has been referred to the commission by the Emperor; following the decree of 5 June given at Finckenstein, the commission extends the judgment to the three cases, so that the estates return to their true owners. Under the entry stand the names of the president, Stanisław Małachowski, and the secretary general, Jan Łuszczewski.'),
}


def main():
    with open(os.path.join(UNIT_DIR, 'summaries_de.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# German summaries of {REF}, written in the working session from a\n'
                '# reading of each document against its scan (intake/summaries_draft.py, 2026-10-04).\n'
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
                       'model': 'in-session, 2026-10-04; claim-checked in session 2026-10-05',
                       'usage': {'input': 0, 'output': 0, 'cache_read': 0}},
                      open(os.path.join(d, pad + '.json'), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
    print(len(S), 'summaries written, German and English')


if __name__ == '__main__':
    main()
