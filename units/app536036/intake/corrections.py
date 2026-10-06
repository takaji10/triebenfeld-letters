# -*- coding: utf-8 -*-
"""The readings of APP 53/6/0/-/36 corrected against the scan, 2026-10-06.

    python units/app536036/intake/corrections.py            # check only
    python units/app536036/intake/corrections.py --write    # once

Run once, after build_pages.py --write. A record: do not run it again, and do
not run build_pages.py --write after it.

The holding is one opening, so both entries were read word for word against
the scan, enlarged. The editor's transcription had eighteen marks of doubt in
317 words. Nearly all are settled by the entry above ours on the same page
and the two below it, which are default judgments in the same set words:
"citatione de praemissis latiori existente. Per Ministerialem Regni
Generalem ... juridice clamatos et non comparentes in termino primo in poena
contumaciae admittente judicio eodem judicialiter condemnaverunt. Hicque
personaliter stans Ministerialis ... recognovit se citationem ratione
praemissorum editam feria secunda proxime praeterita in curia citatorum ...
praesente familia domus posuisse." Their headings are "Contumax"; ours, for
several defendants, "Contumaces".

Left as the editor has them: "filiis" (the scan may have "filios"); the name
"Koelmarek" (the scan may have "Kaczmarek"); "tanq[uam]"; and one doubt kept,
"a[ssignatis?]", where the scan has "ass" with a mark of abbreviation.

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
    # -- leaf 641 verso: the first entry
    ('0642_a1', 'Trąmpczynscy Conces[sionis]', 'Trąmpczynscy Con[tuma]ces',
     'the heading is "Con ces" with marks of abbreviation over it: Contumaces, in default. The two entries below ours on '
     'the opening are headed "Con x", Contumax, and each ends "in poena contumaciae ... condemnavit". It is not "concessio"'),
    ('0642_a1', 'Annam de Słończyc eandem olim Stanislai Trąmpczyński Consorte[m] relict[am] bonorumq[ue] more[?] eiusdem '
                'derelictorum Dominam Reform[atricem] et Aduct[ricem]',
     'Annam de Słończyce eiusdem olim Stanislai Trąmpczyński Consorte[m] relict[am] bonorumq[ue] morte eiusdem '
     'derelictorum Dominam Reform[atoriam] et Advit[alem]',
     'the scan has "de Słonczyce eiusd", "morte eiusd derelictorum" and "Reformrem et Advitlem" with marks of '
     'abbreviation: widow of the same Stanisław, and of the goods left by his death "domina reformatoria et advitalis", '
     'holder of her dower and of a life interest'),
    ('0642_a1', 'de bonis ipsorum gnatorum omnibus', 'de bonis ipsorum generaliter omnibus',
     'the scan has "gnalr" with a mark of abbreviation: the set phrase "de bonis ipsorum generaliter omnibus"'),
    ('0642_a1', 'Minorennes si que sunt cum Tutori[ssa] ipsorum a[ssignata?] Citatos',
     'Minorennes si qui sunt cum Tutoribus ipsorum a[ssignatis?] Citatos',
     'the scan has "si qui sunt cum Tutorib" with a mark of abbreviation: with their guardians. The word after is still in doubt'),
    ('0642_a1', 'per immissionem Subactorum ipsorum eidem Actori in borra eiusdem Actori propria',
     'per immissionem Subditorum ipsorum eidem Actori in borra eiusdem Actoris propria',
     'the scan has "Subditorum": by sending in their subjects, the peasants of their estate'),
    ('0642_a1', 'prioribus incurijs damnis', 'prioribus iniurijs damnis', 'the scan has "iniurijs", injuries'),
    ('0642_a1', 'volentes euismodi facto', 'volentes eiusmodi facto', 'a slip of typing'),
    ('0642_a1', 'in grave[?] damnum Actoris praemissa faciendo eundem siti Contra ipsos fundo in [t?]acto pensat',
     'in grave damnum Actoris praemissa faciendo Quod sibi Contra ipsos fundo intacto pensat',
     'the scan has "Quod sibi ... fundo intacto pensat": the harm, "which he reckons for himself against them, the ground '
     'left untouched", that is, apart from the land itself'),
    ('0642_a1', 'damnique totidem vel pnr~ Judicium decernet Ac nihilominusque [edu?]cto officio Succameratis eadem signa '
                'huius[?] paenis[?] annihilent. Citons[?] de praemissis latiori existente',
     'damnique totidem vel prout Judicium decernet Ac nihilominus educto officio Succamerali eadem signa luitis paenis '
     'annihilent. Citatione de praemissis latiori existente',
     'the scan has "vel prout Judicium decernet Ac Nihilominus educto Officio Succamerali eadem signa luitis poenis '
     'annihilent. Citatione de Praemissis latiori existente": the sub-chamberlain\'s court being brought out, they are to '
     'annul the marks, the penalties paid; the citation says more'),
    ('0642_a1', 'Per Ministerialem Regni Generalis Honestum Nicolaus Jaworowski de Karmin Jur~ce clamant et non Comparendum '
                'in Termino primo in paena contumaciae Admittendam Judicio eodem Jud[icatum?] Cond[o]navit',
     'Per Ministerialem Regni Generalem Honestum Nicolaum Jaworowski de Karmin Juridice clamatos et non Comparentes '
     'in Termino primo in paena contumaciae Admittente Judicio eodem Judicialiter Condemnavit',
     'the set words of a default judgment, as in the entry above on the same page: the defendants, "lawfully called and '
     'not appearing at the first term", the plaintiff "judicially condemned in the penalty of contumacy, the same court '
     'admitting it"'),
    ('0642_a1', 'Hicque per[o?]t~ stans Ministerialis Regni Generalis Providens Bartholomaeus Koelmarek de Łukom '
                'tanq[uam] [?]ula[?] Recognovit se Citationem remissam[?] praemissorum elatam[?] Feria secunda pre praeterita[?]',
     'Hicque personaliter stans Ministerialis Regni Generalis Providus Bartholomaeus Koelmarek de Łukom '
     'tanq[uam] palam Recognovit se Citationem ratione praemissorum editam Feria secunda proxime praeterita',
     'the scan has "personlr stans ... Providus ... palam Recognt se Citonem roe Pmissorum editam feria secunda pxe ptita" '
     'with marks of abbreviation: standing here in person, he openly acknowledged that he had laid the citation issued on '
     'this account, on the Monday last past'),
    # -- leaf 642: the end of the first entry
    ('0642_a2', 'in Curia Citationis Villae Trampczyno praesens familia domus posuisse.',
     'in Curia Citatorum Villae Trampczyno praesente familia domus posuisse.',
     'the scan has "Citator" and "pnte" with marks of abbreviation: at the manor of the cited, in the presence of the household'),
    # -- leaf 642: the second entry
    ('0642_a2', 'arbores variis generis pro aedificiis valentes praecipu[ae?] pinaticos Circiter Centum pro foco vero '
                'Trecentus Currus Circa vel Ulera exciderunt',
     'arbores varii generis pro aedificiis valentes praecipue pinaticas Circiter Centum pro foco vero '
     'Trecentos Currus Citra vel Ultra exciderunt',
     'the scan has "varij generis", "Praecipue pinaticas", "Trecentos Currus Citra vel Ultra"'),
    ('0642_a2', 'In grave[?] damnum Actoris praemissa faciendo eundem siti Contra Ipsos pensat fundo in tacto[?] ad',
     'In grave damnum Actoris praemissa faciendo Quod sibi Contra Ipsos pensat fundo intacto ad',
     'as in the first entry: "Quod sibi ... pensat fundo intacto"'),
]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    courtbook.correct(UNIT_DIR, B.SLUG, B.DOCS, ROWS, '--write' in sys.argv)


if __name__ == '__main__':
    main()
