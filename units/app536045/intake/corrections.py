# -*- coding: utf-8 -*-
"""The readings of APP 53/6/0/-/45 corrected against the scan, 2026-10-06.

    python units/app536045/intake/corrections.py            # check only
    python units/app536045/intake/corrections.py --write    # once

Run once, after build_pages.py --write. A record: do not run it again, and do
not run build_pages.py --write after it.

The holding is one opening, so all of it was read word for word against the
scan, enlarged. The editor's transcription fills out the clerk's
abbreviations without marking them; that is kept. What is corrected is where
the scan has another word. Several were settled by the entry before on the
same page (no. 16), which has the same formulas written a little more
fully: "addit eisdem partibus Ministerialem ad pronuntiandam super
incorporationem eorum testium juramenti rotham ... quoniam per partes ...
mutuo est indultum".

Left as the editor has them, where the scan does not decide: the endings of
"deducendum" and "deducendo", both written "deduc" with a mark of
abbreviation; "Rozdrazewska", where the scan may have "Rozdrazewskie";
"post hac". Words the clerk struck out are not transcribed.

ROWS: (page, text as transcribed, text as on the scan, why).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
sys.path.insert(0, HERE)
import courtbook  # noqa: E402
import build_pages as B  # noqa: E402

ROWS = [
    # -- leaf 653 verso
    ('0673_a1', 'actricem et citatum tum', 'actricem et citatam tum',
     'written above the line, "Actt et Citt": both words belong to Prusimska, plaintiff and summoned'),
    ('0673_a1', 'earumque plurimum actoralibus et reatibus', 'earumque plurium actoratibus et reatibus',
     'the scan has "plurium Actoratibus": the claims and charges of the several parties'),
    ('0673_a1', 'per partes expedientes censet', 'per partes expediendam censet',
     'the scan has "expediendam": an inquiry "to be carried out by the parties"'),
    ('0673_a1', 'decernendo quatenque partes', 'decernendo quatenus partes', 'the scan has "quatenus"'),
    ('0673_a1', 'testibus juratus super contenta praeteritorum', 'testibus juratis super contenta protestationum',
     'the scan has "juratis" and "pttonum" with a mark of abbreviation, protestationum: the contents of the protestations'),
    # -- leaf 654
    ('0673_a2', 'et addant praesentibus eisdem [Ill___?] ad [pro___?] super incorporationem earundem tertium juramenti rotham',
     'et addit praesentibus eisdem Ministerialem ad pronuntiandam super incorporationem eorum testium juramenti rotham',
     'the scan has "addit pntibus eisd Mlm ad pronuntian sup Incorpnem eorum testium jurti rotham", as in entry 16 above '
     'it: the court assigns the parties its summoner (Ministerialis) to pronounce the formula of the oath for swearing in '
     'their witnesses'),
    ('0673_a2', 'per partes sibi resoluo est indultum', 'per partes sibi mutuo est indultum',
     'the scan has "mutuo": conceded by the parties to each other'),
    ('0673_a2', 'et inquisitionis pro parte sui expediverunt ad quartam sectionem hoc idem judicium accessit',
     'et inquisitiones pro parte sui expediverunt ad quarum lectionem hoc idem judicium accessit',
     'the scan has "Inquones ... ad quarum Lectionem": the court went on to the reading of the inquiries'),
    ('0673_a2', 'opponente se Magnifico Thelonei', 'opponente se Notario Thelonei',
     'the scan has "Nrio" with a mark of abbreviation, as "Notarium Thelonei" two lines above: the notary of the customs house'),
    ('0673_a2', 'Generossorum Wawrowski', 'Generosorum Wawrowski', 'a slip of typing'),
    ('0673_a2', 'quando quiae inter has partes', 'quandoquidem inter has partes', 'the scan has "quandoqdem" with a mark of abbreviation'),
    ('0673_a2', 'et Łukom ac acta in Judicio Tribunalio Regni ventilatur indecisia',
     'et Łukom ac alia in Judicio Tribunalis Regni ventilatur indecisa',
     'the scan has "ac alia in Judo Trblis Rni ventilatur indecisa": the boundary case "and others" are before the Crown Tribunal'),
    ('0673_a2', 'in occluso rothulo excdendum debere jubet', 'in occluso rothulo extradendas debere jubet',
     'the scan has "extra|den" over the line end, with a mark of abbreviation: the inquiries are to be handed out'),
]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    courtbook.correct(UNIT_DIR, B.SLUG, B.DOCS, ROWS, '--write' in sys.argv)


if __name__ == '__main__':
    main()
