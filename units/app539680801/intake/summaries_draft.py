# -*- coding: utf-8 -*-
"""The summaries of APP 53/968/0/-/801, written in the working session.

    python units/app539680801/intake/summaries_draft.py

Each document was read whole against its scans on 2026-10-05 and summarised in
German; the English is a translation of the German. They have NOT had the
claim check (read_letters.py --verify, paid, or its in-session equivalent).
First written as one summary, when the holding was one document; rewritten as
three when the editor divided it the same day. This script writes the records
summarise.py would have written (units/<slug>/summaries_de.yml,
cache/summaries-raw-de/, cache/summaries-raw/). Follows
units/agad1174016/intake/summaries_draft.py.
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
 1: ('Abschrift der Generalvollmacht des Fürsten zu Hohenlohe-Ingelfingen für den Kriegs- und Forstrat von Triebenfeld, ausgestellt im Guhrwitzer Justizamt bei Breslau am 19. Februar 1805. Triebenfeld darf den Fürsten in allen Angelegenheiten seiner Güter Zagórów, Witów und Trąbczyn im Kalischer Departement vertreten, sie mögen Parzellierung, Verkauf, Verpachtung oder Verpfändung betreffen: bei der Kammer und der Regierung in Kalisch Anträge stellen, sich mit den Pächtern auseinandersetzen, Gelder zahlen und empfangen und den Beamten der Güter Befehle erteilen und sie suspendieren. Der Fürst verspricht, alles zu genehmigen und ihm die Kosten zu erstatten. Das Justizamt bezeugt am selben Tag seine Unterschrift; das Patrimonialgericht auf Trąbczyn beglaubigt die Abschrift am 21. März 1806.',
     "A copy of the general power of attorney of the Prince of Hohenlohe-Ingelfingen for the War and Forest Councillor von Triebenfeld, given at the Guhrwitz justice office near Wrocław on 19 February 1805. Triebenfeld may act for the Prince in all matters of his estates of Zagórów, Witów and Trąbczyn in the Kalisz department, whether parcelling, sale, lease or mortgage: apply to the Chamber and to the provincial court at Kalisz, settle with the lessees, pay and receive money, and give orders to the officials of the estates and suspend them. The Prince promises to approve everything and to repay his costs. The justice office attests his signature the same day; the patrimonial court on Trąbczyn certifies the copy on 21 March 1806."),
 2: ('Abschrift des Konsenses, den die Südpreußische Kriegs- und Domänenkammer in Kalisch am 28. Januar 1806 im Namen des Königs erteilt, auf Kabinettsordres vom 22. Oktober und 7. Dezember des Vorjahres. Der Fürst zu Hohenlohe-Ingelfingen darf die Vorwerke Drzewce, Kopojno, Świątniki, Święcia und Broniki der Herrschaft Zagórów sowie Nowa Wieś, Przybysław, Stara Huta und einen Teil von Trąbczyn parzellieren, Oleśnica und Szetlewek vererbpachten und die Dienste aller Untertanen in einen festen Geldzins verwandeln; einen Teil von Trąbczyn, die Grundstücke in Mariantów und einen Teil des Forstes behält er zurück. Vier Bedingungen: Die Entschädigung der Untertanen für ihre Hütungs- und Holzungsrechte ist festzusetzen; keine Bauernstelle darf eingehen; die staatlichen Abgaben bleiben und werden im Hypothekenbuch gesichert; die Holzungsrechte des Klosters Ląd und des Domänenamts Ratyń werden gewahrt.',
     "A copy of the consent that the South Prussian War and Domains Chamber at Kalisz gives in the King's name on 28 January 1806, on cabinet orders of 22 October and 7 December of the year before. The Prince of Hohenlohe-Ingelfingen may parcel out the manor farms of Drzewce, Kopojno, Świątniki, Święcia and Broniki in the lordship of Zagórów and of Nowa Wieś, Przybysław, Stara Huta and part of Trąbczyn, let Oleśnica and Szetlewek in hereditary lease, and turn the services of all his subjects into a fixed money rent; he keeps back part of Trąbczyn, the land at Mariantów and a part of the forest. Four conditions: the compensation of the subjects for their rights of pasture and wood is to be fixed; no peasant holding may lapse; the state's taxes remain and are secured in the mortgage book; the wood rights of the abbey of Ląd and of the domain office of Ratyń are protected."),
 3: ('Abschrift eines Erbpachtvertrags, dessen Anfang fehlt. Der Fürst zu Hohenlohe-Ingelfingen überlässt durch seinen Generalbevollmächtigten von Triebenfeld achtzehn namentlich genannten Einsassen 100 Magdeburger Hufen Wald seines Gutes Drzewce auf ewige Zeiten; sechzehn nehmen je 5 Hufen, zwei je 10. Einkaufsgeld wird nicht gezahlt, weil das Land erst zu roden ist; dafür gelten vier Freijahre bis Weihnachten 1808. Danach beträgt der Erbzins 30 Reichstaler je Hufe, zusammen 3000 Reichstaler jährlich, zahlbar zu Johanni und zu Weihnachten; die Hälfte ist ablösbar. Bei jedem Verkauf fällt der zehnte Groschen an die Herrschaft. Die Erbpächter sind frei von Erbuntertänigkeit und Hofdiensten, unterstehen aber der Gerichtsbarkeit der Herrschaft, müssen Bier und Branntwein von ihr nehmen und haften solidarisch. Die Gemeinde erhält 21 Morgen zinsfrei für Schullehrer, Schulzen und Kirchhof. Elf der achtzehn unterzeichnen mit drei Kreuzen. Das Patrimonialgericht fertigt den Vertrag in Mariantów am 21. März 1806 aus.',
     "A copy of a hereditary-lease contract whose beginning is missing. Through his plenipotentiary von Triebenfeld the Prince of Hohenlohe-Ingelfingen lets 100 Magdeburg Hufen of forest of his estate of Drzewce to eighteen named settlers for ever; sixteen take 5 Hufen each and two take 10. No entry money is paid, because the land has still to be cleared; four rent-free years are allowed instead, until Christmas 1808. After that the hereditary rent is 30 Reichsthaler a Hufe, 3000 Reichsthaler a year in all, payable at St John's Day and at Christmas; half of it can be redeemed. At every sale a tenth of the price goes to the lordship. The lessees are free of hereditary subjection and labour service but remain under the lordship's court, must buy their beer and spirits from it, and are jointly liable. The community receives 21 Morgen free of rent for a schoolmaster, a village mayor and a churchyard. Eleven of the eighteen sign with three crosses. The patrimonial court engrosses the contract at Mariantów on 21 March 1806."),
}


def main():
    with open(os.path.join(UNIT_DIR, 'summaries_de.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# German summaries of {REF}, written in the working session from a\n'
                '# reading of each document against its scans (intake/summaries_draft.py, 2026-10-05).\n'
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
    print(len(S), 'summaries written, German and English')


if __name__ == '__main__':
    main()
