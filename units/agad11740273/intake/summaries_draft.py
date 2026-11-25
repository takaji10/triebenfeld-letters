# -*- coding: utf-8 -*-
"""The summaries of AGAD 1/174/0/2/73, written in the working session.

    python units/agad11740273/intake/summaries_draft.py

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
SLUG = 'agad11740273'
REF = 'AGAD 1/174/0/2/73'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

S = {
 1: ('Entwurf eines Beschlusses der Regierungskommission, in Dresden gefasst, in polnischer Sprache. Die Sache der Michalina Dąbska, geborene Prusimska, die die Rückgabe ihrer unter der früheren Regierung konfiszierten und anderen übergebenen Erbgüter verlangt, ist der Kommission vom Kaiser überwiesen worden. Die Kommission nimmt sich die Gerechtigkeit zum Vorbild, die der Kaiser ihrem Mitglied Wybicki durch das in Finckenstein erlassene Dekret vom Juni erwiesen hat, und dehnt dieses Urteil auf den Fall der Michalina Dąbska, des Generals Niemojewski und Wichrowskis aus: Die von der früheren preußischen Regierung konfiszierten Erbgüter dieser Personen sollen an ihre wahren Eigentümer zurückfallen. Der Entwurf ist an mehreren Stellen verbessert und trägt die Paraphe des Präsidenten Małachowski.',
     'At Dresden on 21 July 1807 the Governing Commission, the provisional Polish government Napoleon had set up, resolved to extend to Michalina Dąbska, born Prusimska, the justice Napoleon had done its member Józef Wybicki by his decree of June given at Finckenstein. Dąbska asked for the return of her hereditary estates, which Prussia had confiscated and given to others, and the Emperor had referred her case to the commission. The commission applied the judgment for Wybicki also to General Niemojewski and to Wichrowski: the hereditary estates of these persons, confiscated by the former Prussian government, were to return to their true owners. The commission\'s president, Stanisław Małachowski, initialled the draft.'),
 2: ('Michalina Dąbska, geborene Prusimska, schreibt in Dresden an die Regierungskommission, in polnischer Sprache. Sie habe schon zweimal um die Rückgabe der Güter gebeten, die ihrem Vater zugunsten der preußischen Generale Fürst Hohenlohe, Bischoffswerder und Sanitz konfisziert wurden: Trąbczyn im Departement Kalisz sowie Kamionna, Kolno, Pawłowo, Pawłówko und ein Magazin in einem Ort, der „Wrocławek“ geschrieben ist, im Departement Poznań. Eine Antwort habe sie noch nicht erhalten. Da sie wisse, dass Wybicki seine ebenso konfiszierten Güter vom Kaiser zurückerhalten hat, bittet sie die Kommission, sich für sie zu verwenden und ihr Gelegenheit zu geben, ein gleiches Urteil zu erlangen. Die Kommission vermerkt die Vorlage am 21. Juli.',
     'Michalina Dąbska, born Prusimska, writes at Dresden to the Governing Commission, in Polish. She has twice asked for the return of the estates confiscated from her father for the benefit of the Prussian generals Prince Hohenlohe, Bischoffswerder and Sanitz: Trąbczyn in the department of Kalisz, and Kamionna, Kolno, Pawłowo, Pawłówko and a storehouse at a place written “Wrocławek” in the department of Poznań. She has had no answer. Knowing that Wybicki has had his estates, confiscated like hers, given back by the Emperor, she asks the commission to intercede for her and to give her the means of obtaining the same judgment. The commission notes the petition as presented on 21 July.'),
 3: ('Michalina Dąbska, geborene Prusimska, bittet in Dresden den Kaiser Napoleon auf Französisch. Sie habe ihm ihre Beschwerden und Hoffnungen schon über die polnische Regierung vorlegen lassen, bisher aber nichts von einem Dekret erfahren, das sie wieder in die Güter einsetzt, die zugunsten der preußischen Generale Fürst Hohenlohe, Bischoffswerder und Sanitz konfisziert wurden. Sie sei überzeugt, dass ihr dieselbe Gerechtigkeit zuteilwerde, die den Grafen Wybicki in seine Besitzungen wieder eingesetzt hat, und bittet den Kaiser, sie ihr nicht zu verweigern. Nach dem Vermerk der Kommission wurde die Bittschrift am 21. Juli 1807 in einer außerordentlichen Sitzung in Dresden vom Fürsten, dem Kriegsdirektor, auf Befehl des Kaisers vorgelegt; der Vermerk trägt die Paraphe des Präsidenten Małachowski, an den das Blatt auf der Rückseite adressiert ist.',
     "On 21 July 1807 at Dresden Michalina Dąbska, born Prusimska, daughter of the Starost Antoni Prusimski, petitioned Emperor Napoleon for the return of her father's confiscated estates. She had already had her complaints and hopes laid before him through the Polish government, but had so far heard nothing of a decree restoring her to the estates that were confiscated for the benefit of the Prussian generals Prince Hohenlohe, Bischoffswerder and Sanitz. She was persuaded that the same justice that restored Count Wybicki to his possessions would be done to her, and begged the Emperor not to refuse it. By Napoleon's order Prince Józef Poniatowski, the Governing Commission's Director of War, presented the petition to the commission at an extraordinary session at Dresden the same day; the commission's president, Małachowski, initialled the note."),
 4: ('Michalina Dąbska, geborene Prusimska, schreibt in Dresden erneut an die Regierungskommission, in polnischer Sprache. Das Dekret des Kaisers vom 5. Juni, das Wybicki die von der preußischen Regierung konfiszierten und vergebenen Güter zurückgab, sei zum Grundsatz und Muster genommen worden, um den Personen, die im Dekret der Kommission vom 21. Juli genannt sind, gleiche Gerechtigkeit zu erweisen. Sie zweifle nicht, dass die Kommission ihren Beschluss ebenso ausführen lasse wie für Wybicki und die Direktion der inneren Angelegenheiten anweise, den Verwaltungskammern die Einweisung in die Güter zu befehlen. Die Kommission vermerkt die Vorlage am 23. Juli 1807 und legt das Schreiben zu den Akten.',
     "On 23 July 1807 at Dresden Michalina Dąbska, born Prusimska, daughter of the Starost Antoni Prusimski, wrote again to the Governing Commission, the provisional Polish government Napoleon had set up. The Emperor's decree of 5 June, which gave back to Józef Wybicki the estates confiscated and disposed of by the Prussian government, had been taken as the principle and pattern for doing equal justice to the persons named in the commission's resolution of 21 July. She did not doubt that the commission would have its resolution carried out in the same way as for Wybicki, and asked it to direct the Directorate of Internal Affairs to order the administrative chambers to put her in possession of the estates. The commission noted the petition as presented the same day."),
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
