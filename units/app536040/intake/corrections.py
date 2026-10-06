# -*- coding: utf-8 -*-
"""The readings of APP 53/6/0/-/40 corrected against the scans, 2026-10-07.

    python units/app536040/intake/corrections.py            # check only
    python units/app536040/intake/corrections.py --write    # once

Run once, after build_pages.py --write. A record: do not run it again, and do
not run build_pages.py --write after it.

All five pages were read word for word against the scans, enlarged. The hand
is a clear one of 1728 and the editor's transcription was close: of its eleven
marks of doubt ten are settled here and one is kept ("devehi[?]"). The
transcription fills out the clerk's abbreviations without marks; that is
kept. Small differences of spelling and of case endings that change nothing
are left as the editor has them.

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
    # -- leaf 368: the heading of the sitting
    ('0368_a2', 'in diem hodiernam incedentibus', 'in diem hodiernam incidentibus', 'the scan has "incidentibus"'),
    # -- leaf 372
    ('0372_a2', 'Inter G. Generosus Chełmskię et Generosus Prusimski Decretum Locationis.',
     'Inter Generosos Chełmskie et Generosum Prusimski Decretum Locationis.',
     'the heading has "Inr GG. Chełmskie et G. Prusimski": between the Chełmskis, more than one, and Prusimski'),
    ('0372_a2', 'feria secunda post terminum[?] Sanctissimae', 'feria secunda post Festum Sanctissimae',
     'the scan has "pt Fm" with marks of abbreviation: after the feast of the Trinity'),
    ('0372_a2', 'parti infrascriptae citae per', 'parti infrascriptae citatae per', 'the scan has "Cittae" with a mark: citatae'),
    ('0372_a2', 'instigator judicii praesentes ejusdem delatores G Generosi Franciscus',
     'instigator judicii praesentis ejusque delatores Generosi Franciscus',
     'the scan has "Instigator Judij pntis ejusq Delatores GG.": the instigator of the present court and his informants'),
    ('0372_a2', 'et aliorum et pertinentium haereditates et possessores actores',
     'et aliorum eo pertinentium haeredes et possessores actores',
     'the scan has "eo pertinen Haeredes": heirs and possessors of Łukom, Łomowo and the others belonging to them'),
    ('0372_a2', 'in judicium praesens terre Calissiensis ternosque terrestres partes decretos Coninenses filiis quibus cum '
                'parentis famulis et subditis cum decreto ipsos ad inhaerendum protestationi suae con[tra] eisdem factae',
     'in judicium praesens terrestre Calissiense terminosque terrestres particulares districtus Coninensis filiis quibus cum '
     'parentibus famulis et subditis cum dominis ipsorum ad inhaerendum protestationi suae contra eosdem factae',
     'the scan has "Terrosq Terres Parles Dctus Coninen" (terminos terrestres particulares districtus Coninensis, as in the '
     'heading of the sitting) and "cum Parentibus Famulis et Subditis cum Dnis ipsorum": the sons with their parents, the '
     'servants and subjects with their lords. There is no decree here and no "three"'),
    ('0372_a2', 'non contentibus anterioribus immunis[?] violentiis', 'non contentus anterioribus damnis violentiis',
     'the scan has "non Contentus anterioribus Damnis"'),
    # -- leaf 372 verso
    ('0373_a1', 'in virtute vicinae cum manifestationis amicitiam', 'in virtute vicinae commansionis amicitiam',
     'the scan has "vicinae Commansionis amicitiam": the friendship that goes with living as neighbours'),
    ('0373_a1', 'quo tempore certo in tertio termino exprimens tegulas alias Szkudeł et centum sexagenas',
     'quo tempore certo in termino termini exprimendo tegulas alias Szkudeł centum sexagenas',
     'the scan has "in Terno Terni exprimen": at a certain time "to be stated at the hearing", the phrase used twice on the '
     'page before. "Centum sexagenas" follows without "et": a hundred sixties (kopy) of shingles, six thousand'),
    ('0373_a1', 'circa violentam ejusdem armatum et turmatim [super/supra] invasionem',
     'circa violentam ejus armatim et turmatim super invasionem', 'the scan has "ejus armatim et turmatim sup invasionem"'),
    ('0373_a1', 'tribunalibus Regni Petricoviensis causa requisitionum suorum',
     'tribunalis Regni Petricoviensis causa negotiorum suorum',
     'the scan has "Trblis Rni Petricovien Causa Negotiorum suorum": at the Crown Tribunal at Piotrków on their business'),
    ('0373_a1', 'ut supponatur[?] sibi usurpando', 'ut supponitur sibi usurpando', 'the scan has "ut supponitur"'),
    ('0373_a1', 'in non postrema quam testate currium intercipere', 'in non postrema quantitate curruum intercipere',
     'the scan has "in non postrema quantitate Curruum": in no small number of cartloads'),
    ('0373_a1', 'ad bona Trąpczyn seveti[?] curare et per inde decessum[?] inventarii causae aliasque',
     'ad bona Trąpczyn devehi[?] curare et per inde decessum inventarii causare aliasque',
     'the scan has "decessum Inventarij causare": to cause the loss of livestock (for want of the hay). The word before '
     '"curare" must be "devehi", carried off, but its first letter is not the clerk\'s usual d, so the doubt stays'),
    ('0373_a1', 'particularibus decretis Coninensibus controversiis', 'particularibus districtus Coninensis controversiis',
     'the scan has "Dctus Coninen": of the district of Konin'),
    ('0373_a1', 'actoreae quidem Generosus Hełmskich et per Generosum Josephum Chełmski',
     'actoreae quidem Generosorum Chełmskich per Generosum Josephum Chełmski',
     'the scan has "Gnosorum Chełmskich per G. Josephum Chełmski"'),
    ('0373_a1', 'Generosorum Prusimskich et conjugum', 'Generosorum Prusimskich conjugum',
     'no "et" on the scan: the Prusimskis, husband and wife'),
    # -- leaf 373
    ('0373_a2', 'et judicio controvertentes in praemissis judicii factis exauditis decidendum et ter[mi?]num partis actoreae',
     'et judicialiter controvertentium in praemissis judicialiter factis exauditis decidendo terminum partis actoreae',
     'the scan has "Decidendo Ternum Partis Actoreae": the court, deciding the plaintiffs\' cause, finds an inspection needed. '
     'It does not say that a decision must be reached'),
    ('0373_a2', 'ex quo certa controversia', 'ex quo orta controversia', 'the scan has "orta": the ground from which the dispute arose'),
    ('0373_a2', 'sittum mutuo suo sumptum conducant qui Generosi Commissarii ac amici',
     'situm mutuo suo sumptu conducant qui Generosus Commissarius ac amici',
     'the scan has "Sumptu" and "G. Commissarius": one commissioner, at the parties\' common cost'),
    ('0373_a2', 'super contenta protestationem partium', 'super contenta protestationum partium', 'the scan has "protestationum"'),
    ('0373_a2', 'et quid quid ac eisdem compertum', 'et quid quid ex eisdem compertum', 'the scan has "ex eisdem"'),
    ('0373_a2', 'non nisi t[amen?] a definitiva', 'non nisi tantum a definitiva', 'the scan has "tm" with a mark: tantum'),
    ('0373_a2', 'de Regni Poloniae Dominiis [quibus] illi annexis proscriptionis quae jam',
     'de Regno Poloniae Dominiisque illi annexis proscriptionis quae jam', 'the scan has "de Rno Poloniae Dnijsq illi annexis"'),
    ('0373_a2', 'supra parte decreto praesenti contravenientem per judicium praesens decernitur ipsique irrogatu[r?]',
     'super parte decreto praesenti contraveniente per judicium praesens decernitur ipsique irrogatur',
     'the scan has "sup Parte ... Contraveniente ... irrogatur"'),
    ('0373_a2', 'ad publicanda et more solito proclamandam paenam eadem bannitionis',
     'ad publicandam et more solito proclamandam paenam eandem bannitionis', 'the scan has "publicandam ... eandem"'),
    ('0373_a2', 'deputatur et ad aliam pro qua publicata', 'deputatur et additur pro qua publicata',
     'the scan has "deputatur et additur": the messenger is deputed and assigned'),
    ('0373_a2', 'cum [???]o suo effectu', 'cum toto suo effectu', 'the scan has "cum toto suo effectu"'),
]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    courtbook.correct(UNIT_DIR, B.SLUG, B.DOCS, ROWS, '--write' in sys.argv)


if __name__ == '__main__':
    main()
