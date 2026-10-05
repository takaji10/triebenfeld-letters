# -*- coding: utf-8 -*-
"""The summary of APP 53/968/0/-/801, written in the working session.

    python units/app539680801/intake/summaries_draft.py

The document was read whole against its scans on 2026-10-05 and summarised in
German; the English is a translation of the German. It has NOT had the claim
check (read_letters.py --verify, paid, or its in-session equivalent). This
script writes the records summarise.py would have written
(units/<slug>/summaries_de.yml, cache/summaries-raw-de/, cache/summaries-raw/).
Follows units/agad1174016/intake/summaries_draft.py.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
SLUG = 'app539680801'
REF = 'APP 53/968/0/-/801'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

S = {
 1: ('Abschrift dreier zusammengehöriger Stücke von 1805 und 1806. Erstens die Generalvollmacht des Fürsten zu Hohenlohe-Ingelfingen für den Kriegs- und Forstrat von Triebenfeld, ausgestellt im Guhrwitzer Justizamt bei Breslau am 19. Februar 1805, für alle Angelegenheiten seiner Güter Zagórów, Witów und Trąbczyn; das Patrimonialgericht auf Trąbczyn beglaubigt die Abschrift am 21. März 1806. Zweitens der Konsens der Kriegs- und Domänenkammer in Kalisch vom 28. Januar 1806: Der Fürst darf Vorwerke der Herrschaften Zagórów und Trąbczyn parzellieren, Oleśnica und Szetlewek vererbpachten und die Dienste der Untertanen in Geldzins verwandeln, unter vier Bedingungen. Drittens der Erbpachtvertrag, dessen Anfang fehlt: Der Fürst überlässt durch Triebenfeld achtzehn namentlich genannten Einsassen 100 Magdeburger Hufen Wald des Gutes Drzewce auf ewige Zeiten, ohne Einkaufsgeld und mit vier Freijahren bis Weihnachten 1808, danach gegen 30 Reichstaler Erbzins je Hufe, zusammen 3000 Reichstaler jährlich; die Hälfte des Zinses ist ablösbar. Das Gericht fertigt den Vertrag in Mariantów am 21. März 1806 aus.',
     'A copy of three papers of 1805 and 1806 that belong together. First, the general power of attorney of the Prince of Hohenlohe-Ingelfingen for the War and Forest Councillor von Triebenfeld, given at the Guhrwitz justice office near Wrocław on 19 February 1805, for all business of his estates of Zagórów, Witów and Trąbczyn; the patrimonial court on Trąbczyn certifies the copy on 21 March 1806. Second, the consent of the War and Domains Chamber at Kalisz of 28 January 1806: the Prince may parcel out manor farms of the lordships of Zagórów and Trąbczyn, let Oleśnica and Szetlewek in hereditary lease and turn his subjects\' services into a money rent, on four conditions. Third, the hereditary-lease contract, whose beginning is missing: through Triebenfeld the Prince lets 100 Magdeburg Hufen of forest of the Drzewce estate to eighteen named settlers for ever, without entry money and with four rent-free years until Christmas 1808, then at a hereditary rent of 30 Reichsthaler a Hufe, 3000 Reichsthaler a year in all; half the rent can be redeemed. The court engrosses the contract at Mariantów on 21 March 1806.'),
}


def main():
    with open(os.path.join(UNIT_DIR, 'summaries_de.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# German summary of {REF}, written in the working session from a\n'
                '# reading of the document against its scans (intake/summaries_draft.py, 2026-10-05).\n'
                '# Not claim-checked. A finding aid, not part of the edition text. Published\n'
                '# through summarise.py --build --lang de.\n')
        for n, (de, _en) in sorted(S.items()):
            f.write(f'{SLUG}-{n:03d}: {json.dumps(de, ensure_ascii=False)}\n')
    for lang, sub, i in (('de', 'summaries-raw-de', 0), ('en', 'summaries-raw', 1)):
        d = os.path.join(ROOT, 'cache', sub)
        os.makedirs(d, exist_ok=True)
        for n, pair in S.items():
            pad = f'{SLUG}-{n:03d}'
            json.dump({'letter': str(n), 'pad': pad, 'summary': pair[i],
                       'model': 'in-session, 2026-10-05; not claim-checked',
                       'usage': {'input': 0, 'output': 0, 'cache_read': 0}},
                      open(os.path.join(d, pad + '.json'), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
    print(len(S), 'summary written, German and English')


if __name__ == '__main__':
    main()
