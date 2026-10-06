# -*- coding: utf-8 -*-
"""The summary of APP 53/6/0/-/45, written in the working session.

    python units/app536045/intake/summaries_draft.py

The holding is one document. It was read whole against its scan on 2026-10-06
and summarised in German from the corrected Latin; the English is a
translation of the German. It was claim-checked in the same session
(claim_check.yml beside this file), as read_letters.py --verify checks, not by
the paid run. This script writes the records summarise.py would have written
(units/<slug>/summaries_de.yml, cache/summaries-raw-de/, cache/summaries-raw/)
and puts the holding's lines into site/_data/summaries.yml and
summaries_de.yml, replacing its own lines only.
"""
import io
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
SLUG = 'app536045'
REF = 'APP 53/6/0/-/45'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

S = {
 1: ('Dekret des Landgerichts in Konin aus dessen Sitzung von 1763 im Streit zwischen der Witwe Katarzyna Prusimska, geborene Rozdrażewska, mit Joseph Puchalski auf der einen und Stanisław Ścibor Chełmski mit einem Czajkowski auf der anderen Seite; beide Seiten klagen und sind zugleich geladen. Das Gericht hält eine Vernehmung beeideter Zeugen für nötig, lässt sie durchführen und die Aussagen verlesen. Danach hatte die Prusimska 1761 Pottaschebrenner mit Pottasche auf den Weg geschickt; Chełmski, der nach Posen reiste, traf sie bei Pyzdry, als sie nach Danzig zogen, ließ die Pottasche beschlagnahmen und in einem Wirtshaus in Pyzdry einlagern und legte beim Notar des Zollamts Arrest darauf. Die Brenner schafften sie trotz des Widerspruchs des Notars mit Hilfe der Adligen Wawrowski und Gotartowski fort und brachten sie nach Danzig. Weil zwischen den Parteien der Streit um die Grenze zwischen Trąbczyn und Łukom vor dem Krontribunal noch unentschieden ist und erst die Grenzziehung zeigen wird, auf wessen Grund die Pottasche hergestellt wurde, setzt das Gericht die Entscheidung aus und ordnet an, den Parteien die Zeugenaussagen aus der Kanzlei in verschlossener Rolle herauszugeben.',
     'A decree of the land court at Konin, of its sitting of 1763, in the dispute between the widow Katarzyna Prusimska, born Rozdrażewska, with Joseph Puchalski on one side, and Stanisław Ścibor Chełmski with one Czajkowski on the other; each side is plaintiff and at the same time summoned. The court holds that sworn witnesses must be examined, has it done and has the testimony read out. It showed that in 1761 Prusimska had sent potash-burners off with potash; Chełmski, travelling to Poznań, came upon them near Pyzdry as they were making for Gdańsk, had the potash sequestered and stored at an inn in Pyzdry, and laid an arrest on it with the notary of the customs house. The burners, helped by the noblemen Wawrowski and Gotartowski, took it away over the notary\'s objection and brought it to Gdańsk. Because the dispute over the boundary between Trąbczyn and Łukom is still undecided between the parties before the Crown Tribunal, and only the fixing of the boundary will show on whose ground the potash was made, the court suspends its decision and orders the testimony handed to the parties from the chancery in a closed roll.'),
}


def site_lines(name, lang_index):
    """Replace this holding's lines in a site summary file, keeping every other line as it is."""
    path = os.path.join(ROOT, 'site', '_data', name)
    lines = io.open(path, encoding='utf-8', newline='').read().split('\n')
    import re
    keep = [l for l in lines if not l.startswith(SLUG + '-')]
    new = []
    for n, pair in sorted(S.items()):
        new.append(yaml.safe_dump({'%s-%03d' % (SLUG, n): pair[lang_index]}, allow_unicode=True, width=10 ** 9).rstrip('\n'))
    assert all('\n' not in l for l in new)
    # before the first entry whose key sorts after this holding's (some entries run over two lines)
    at = next((i for i, l in enumerate(keep) if re.match(r'^[a-z0-9]+-\d+[a-z]?: ', l) and l.split('-', 1)[0] > SLUG), len(keep))
    keep[at:at] = new
    io.open(path, 'w', encoding='utf-8', newline='').write('\n'.join(keep))


def main():
    with open(os.path.join(UNIT_DIR, 'summaries_de.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# German summary of {REF}, written in the working session from the\n'
                '# corrected Latin (intake/summaries_draft.py, 2026-10-06).\n'
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
    site_lines('summaries_de.yml', 0)
    site_lines('summaries.yml', 1)
    print(len(S), 'summary written, German and English, and put into the site data')


if __name__ == '__main__':
    main()
