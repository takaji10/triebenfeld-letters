# -*- coding: utf-8 -*-
"""The summaries of I. HA Rep. 162, Nr. 295, written in the working session.

    python units/iharep162nr295/intake/summaries_draft.py

Each document was read whole against its page images on 2026-10-05 and
summarised in German; the English is a translation of the German. They were
claim-checked in the same session (claim_check.yml beside this file), as
read_letters.py --verify checks, not by the paid run. This script writes the
records summarise.py would have written (units/<slug>/summaries_de.yml,
cache/summaries-raw-de/, cache/summaries-raw/). Follows
units/app539680801/intake/summaries_draft.py.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
SLUG = 'iharep162nr295'
REF = 'I. HA Rep. 162, Nr. 295'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

S = {
 1: ('Abschrift der Schuldverschreibung des Kriegs- und Forstrats Peter Friedrich August von Triebenfeld, Berlin, 28. Januar 1805. Das dritte Departement des Ober-Kriegs-Kollegiums hat ihm aus der General-Invalidenkasse ein Darlehen von 50.000 Talern Courant bewilligt und in Seehandlungs-Obligationen ausgezahlt. Er verspricht, es nach sechsmonatiger, beiden Teilen freistehender Kündigung zurückzuzahlen und bis dahin mit 5 Prozent in halbjährlichen Raten in Berlin zu verzinsen. Zur Sicherheit verpfändet er sein ganzes Vermögen und besonders die Obligation des Fürsten zu Hohenlohe-Ingelfingen vom 1. Juni 1804 über 250.000 Taler, die auf dessen südpreußische Güter Zagórów, Drzewce, Kopojno, Świątniki, Skokum, Oleśnica, Wrąbczyn und Grądzyń eingetragen ist. Für den Fall der Nichtzahlung tritt er der Kasse 50.000 Taler davon ab, mit Vorrang vor den ihm verbleibenden 200.000. Am selben Tag erkennt er die Urkunde vor dem ersten Kurmärkischen Justizamt in Berlin an.',
     "A copy of the bond of the Councillor of War and Forests Peter Friedrich August von Triebenfeld, Berlin, 28 January 1805. The third department of the Supreme War College has granted him a loan of 50,000 Thaler Courant out of the General Invalids' Fund and paid it out in Seehandlung bonds. He promises to repay it after six months' notice, which either side may give, and until then to pay 5 per cent interest in half-yearly instalments at Berlin. As security he pledges his whole property and, specially, the bond of the Prince of Hohenlohe-Ingelfingen of 1 June 1804 for 250,000 Thaler, which is registered on the Prince's South Prussian estates of Zagórów, Drzewce, Kopojno, Świątniki, Skokum, Oleśnica, Wrąbczyn and Grądzyń. In case of non-payment he cedes 50,000 Thaler of it to the fund, with priority over the 200,000 that remain his. The same day he acknowledges the deed before the first Kurmark justice office at Berlin."),
 2: ('Abschrift einer Urkunde der Südpreußischen Regierung in Kalisch vom 5. März 1805, im Namen des Königs ausgestellt. Vor dem Regierungsrat Stosch als Kommissar ist Triebenfeld am 27. Februar 1805 in Kalisch erschienen und hat seine Schuld- und Verpfändungsurkunde vom 28. Januar über 50.000 Taler aus der General-Invalidenkasse nochmals anerkannt, ebenso das unter der Obligation stehende Anerkennungsprotokoll; der Regierungsrat von Lichnowski bezeugte seine Identität. Darunter steht der Vermerk des Ingrossators Beda vom 13. März 1805: Aufgrund eines Dekrets vom 5. des Monats sind die 50.000 Taler, zu 5 Prozent verzinslich und nach sechsmonatiger Kündigung zahlbar, im Hypothekenbuch des Koniner Kreises auf Zagórów, Drzewce und Kopojno für die Invalidenkasse eingetragen worden.',
     "A copy of a certificate of the South Prussian Government at Kalisz of 5 March 1805, issued in the King's name. Before the Government Councillor Stosch as commissary, Triebenfeld appeared at Kalisz on 27 February 1805 and once more acknowledged his deed of debt and pledge of 28 January for 50,000 Thaler from the General Invalids' Fund, and likewise the protocol of acknowledgement standing under the bond; the Government Councillor von Lichnowski vouched for his identity. Below it stands the note of the Ingrossator Beda of 13 March 1805: on the ground of a decree of the 5th of the month the 50,000 Thaler, bearing 5 per cent interest and payable after six months' notice, have been entered for the Invalids' Fund in the mortgage book of the Konin district upon Zagórów, Drzewce and Kopojno."),
 3: ('Abschrift des Hypothekenscheins über die Stadt Zagórów im Koniner Kreis, den die Südpreußische Regierung in Kalisch am 13. März 1805 der General-Invalidenkasse erteilt (Nr. 1179). Der Fürst zu Hohenlohe-Ingelfingen besitzt das Gut durch die Verleihungsurkunde König Friedrich Wilhelms II. vom 19. Juni 1797; sein Besitztitel ist durch Dekret vom 31. Juli 1801 eingetragen. Als dauernde Lasten stehen darauf: eine jährliche Abgabe von 88 Reichstalern 5 Groschen 9 Pfennig an die Kalischer Kriegs- und Domänenkasse; ein Vorbehalt des Fiskus wegen Bau- und Brennholz aus den Forsten des Gutes nach der Einziehung der geistlichen Güter; und ein Vorbehalt für Johann Giese, Johann Bagans und Friedrich Gietzinger wegen der Holz- und Weiderechte, die ihnen ihr Erbpachtvertrag über Oleśnica vom 22. Februar 1804 in den Zagórówer Forsten gibt. Als Schulden stehen darauf: ein Vorbehalt für den Landesältesten von Lichnowski in Brieg wegen einer schon auf Trąbczyn eingetragenen Forderung von 32.300 Reichstalern; 250.000 Reichstaler für Triebenfeld aus der Schuldverschreibung des Fürsten vom 1. Juni 1804; und davon 50.000 Reichstaler, die Triebenfeld der Invalidenkasse verpfändet und abgetreten hat, mit Vorrang vor dem Rest. Die letzte Zeile beginnt wie dieser Schein und bricht ab.',
     "A copy of the mortgage certificate for the town of Zagórów in the Konin district, which the South Prussian Government at Kalisz issues to the General Invalids' Fund on 13 March 1805 (No. 1179). The Prince of Hohenlohe-Ingelfingen holds the estate by the deed of grant of King Friedrich Wilhelm II of 19 June 1797; his title of possession was registered by a decree of 31 July 1801. As perpetual charges there stand on it: a yearly due of 88 Reichsthaler 5 Groschen 9 Pfennig to the Kalisz Treasury of War and Domains; a caveat of the Treasury for building timber and firewood from the estate's forests, after the confiscation of the ecclesiastical estates; and a caveat for Johann Giese, Johann Bagans and Friedrich Gietzinger for the rights of wood and pasture that their hereditary lease of Oleśnica of 22 February 1804 gives them in the Zagórów forests. As debts there stand on it: a caveat for the Provincial Elder von Lichnowski at Brzeg for a claim of 32,300 Reichsthaler already registered on Trąbczyn; 250,000 Reichsthaler for Triebenfeld under the Prince's bond of 1 June 1804; and 50,000 Reichsthaler of these which Triebenfeld has pledged and ceded to the Invalids' Fund, with priority over the remainder. The last line opens like this certificate and breaks off."),
}


def main():
    with open(os.path.join(UNIT_DIR, 'summaries_de.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# German summaries of {REF}, written in the working session from a\n'
                '# reading of each document against its page images (intake/summaries_draft.py, 2026-10-05).\n'
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
