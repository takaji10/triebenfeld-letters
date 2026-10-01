# -*- coding: utf-8 -*-
"""Draft German summaries, put where the paid claim check can read them.

    python units/iiihamdaiiinr12765/intake/summaries_draft.py --unit iiihamdaiiinr12765

read_letters.py --verify checks a summary and its statements against the
document, and may only cut or weaken. It reads both from
cache/reading-<slug>/<pad>.json, which the paid reading run normally writes.
This unit was read in the working session (reading_record.py), so this script
writes those cache records instead: the summary below, with the statements and
suspicions from reading.json. Nothing here calls the API.

The summaries follow summarise.py's German rules: 40 to 80 words, the substance
first, the edition's names (places now in Poland by their Polish name), Rthl for
rt, no em dashes. They are drafts until the check has run; only the checked
text goes into summaries_de.yml.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'review'))

S = {
1: "Triebenfeld erinnert Hardenberg daran, dass er ihm am 6. Mai in Paris ein Schreiben des Fürsten Hohenlohe an den russischen Kaiser übergeben hat. Er legt die darauf erteilte Resolution vom 14. Mai in Abschrift bei und bittet, die für den Fürsten wichtige Sache im jetzt entscheidenden Zeitpunkt wieder in Erinnerung bringen zu dürfen. Die Kanzlei vermerkt, das Gesuch sei am 20. November 1814 an Staatsrat Stägemann abgegeben worden.",
2: "Entwurf einer Antwort an Triebenfeld auf sein Gesuch vom 25. des Vormonats: Die Angelegenheit des Fürsten Hohenlohe wegen der Ansprüche auf Trąbczyn und Kamionna werde sich von selbst ausgleichen, sobald die allgemeine Auseinandersetzung und Übereinkunft wegen des Herzogtums Warschau zur Ausführung komme.",
3: "Abschrift eines Schreibens Hardenbergs an Triebenfeld: Die Ansprüche des Fürsten von Hohenlohe auf die ihm 1796 geschenkten südpreußischen Güter Trąbczyn und Kamionna könnten erst mit Aussicht auf Erfolg angeregt werden, wenn über die Warschauer Angelegenheiten definitive Bestimmungen erfolgt sind. Das sei noch nicht der Fall. Hardenberg hält deshalb das Schreiben des Fürsten an Kaiser Alexander zurück und bittet, dies dem Fürsten zu eröffnen.",
4: "Triebenfeld schildert Hardenberg den Fall: 1796 erhielt der Fürst Kamionna und Kolno, Trąbczyn mit Dörfern im Kreis Konin und Brzyce, die dem entwichenen Prusimski konfisziert waren. Kamionna und Kolno verkaufte er 1804 an Bankdirektor Leixner. 1807 nahm die polnische Verwaltungskommission alle Güter ohne Urteil und gab sie Prusimskis Tochter Miączyńska; das Tribunal zu Kalisz erklärte sich für nicht ermächtigt. Er bittet, Leixner seine Güter zurückzugeben und beim russischen Kaiser die Rückgabe der Trąbczyner Güter samt 36500 Rthl Revenuen zu erwirken.",
5: "Entwurf einer Antwort an Triebenfeld: Über die Entschädigung der Donatare südpreußischer Güter, denen der Besitz seit dem Frieden von Tilsit entzogen wurde, sei eine diplomatische Unterhandlung eingeleitet, deren Ergebnis dem Fürsten mitgeteilt werde. Leixner sei nicht durch den Verlust von Kolno und Kamionna in gerichtliche Untersuchung geraten, sondern durch die unregelmäßige Verwaltung seines Postens und die unerlaubte Beleihung eines dort für den Kaufmann Simon eingetragenen Aktivums.",
6: "Der Fürst bittet Stein auf Französisch, beim Kaiser eine Entschädigung für Kamionna und Trąbczyn zu erwirken, die ihm 1796 verliehen und 1807 vom polnischen Fiskus genommen und Prusimskis Tochter zugesprochen wurden. Um die verpfändeten Güter zu befreien, habe er 55000 écus zahlen müssen; seine Forderung in barem Geld betrage 85400 écus, sein Verlust insgesamt 325400 écus. Die Kanzlei vermerkt, es sei zu antworten, dass die Regelung der polnischen Angelegenheiten abzuwarten sei.",
7: "Entwurf einer französischen Antwort Hardenbergs an den Fürsten: Stein habe ihm dessen Schreiben vom 12. mitgeteilt. Der Fürst möge mit seiner Forderung auf Kamionna und Trąbczyn die endgültige Regelung der polnischen Angelegenheiten abwarten, die nicht fern scheine. Hardenberg werde dann alles tun, um das Gesuch beim König zu unterstützen.",
8: "Der Fürst schreibt Hardenberg, der Distrikt seiner Trąbczyner Güter falle unter russische Hoheit; da beide Souveräne die Handlungen der Kommission bestätigt hätten, seien sie für ihn verloren, und den Donataren solle eine Entschädigung durch andere Güter gegeben werden. Sein Verlust betrage über 261000 Rthl. Er wäre mit dem kleinen Amt Sokolnik zufrieden, das 8 bis 10000 Rthl Pacht gibt, und bittet Hardenberg, sich beim russischen Kaiser dafür zu verwenden.",
9: "Entwurf einer Antwort Hardenbergs an den Fürsten auf das Schreiben vom 12. des Vormonats wegen der Trąbczyner Güter. Minister vom Stein habe ihm auch das an ihn gerichtete Schreiben wegen Kamionna und Trąbczyn mitgeteilt. Hardenberg habe Zerboni ersucht, ihn über beide Güter in vollständige Kenntnis zu setzen, und behalte sich vor, dem Fürsten von seinen weiteren Schritten Nachricht zu geben.",
10: "Entwurf eines Schreibens an Zerboni in Poznań: Hardenberg übersendet urschriftlich zwei Schreiben des Fürsten, an ihn und an Stein, über die Ansprüche wegen der entzogenen Güter Kamionna und Trąbczyn und bittet um Mitteilung, welche Schritte zugunsten des Fürsten noch getan werden können. Kamionna habe der Fürst an Leixner verkauft; die 55000 Rthl und Zinsen habe die Bank zu fordern. Er erwartet Zerbonis Bericht so bald als möglich.",
11: "Kassierter Entwurf einer Antwort an den Fürsten: Die Territorialverhältnisse des Herzogtums Warschau seien für die an Preußen zurückfallenden Provinzen definitiv entschieden; die Entschädigung der Donatare sei einer besonderen Unterhandlung vorbehalten, zu der schon geschritten worden sei. Hardenberg werde darin Gelegenheit suchen, die Entschädigung für die entzogenen Trąbczyner Güter zu befördern. Der Entwurf verweist auf die anderweitige Verfügung vom 6. Juni 1815.",
12: "Reinschrift einer Antwort an den Fürsten: Die Territorialverhältnisse des Herzogtums Warschau seien für die an Preußen zurückfallenden Provinzen definitiv entschieden; die Entschädigung der Donatare sei einer besonderen Unterhandlung vorbehalten. Der Schreiber werde darin Gelegenheit suchen, die Entschädigung für die entzogenen Trąbczyner Güter zu befördern.",
13: "Reinschrift einer französischen Antwort an den Fürsten: Stein habe dessen Schreiben vom 12. des Vormonats mitgeteilt. Der Fürst möge mit seiner Forderung auf Kamionna und Trąbczyn die endgültige Regelung der polnischen Angelegenheiten abwarten; der Schreiber werde dann alles tun, um das Gesuch beim König zu unterstützen.",
14: "Zerboni berichtet Hardenberg: Kolno und Kamionna habe der Fürst vor 1806 an Leixner verkauft, Trąbczyn nicht; alle Güter gelangten 1806/7 an die Erben des vorigen Eigentümers zurück. Ein gewisser Schenk fordere als Mandatar 318500 Rthl Entschädigung, am besten durch das Amt Sokolnik. Zerboni hält die Berechnungen für Unsinn; der Fürst habe Trąbczyn deterioriert und mit Schulden überladen. Das Kabinett könne nur das russische Kabinett bewegen, den Fürsten zu entschädigen. Ein Randvermerk nennt Triebenfeld und Leixner verstorben.",
15: "Verfügung des Ministeriums: Schöler in St. Petersburg soll nach Zerbonis Antrag beauftragt werden, den Wunsch des Fürsten, da es eine reine Gnadensache sei, nur ganz im Allgemeinen zur Kenntnis des Kaisers zu bringen. Dem Fürsten soll namens Hardenbergs mitgeteilt werden, dass sein Entschädigungsgesuch durch die königliche Gesandtschaft zur Kenntnis des Kaisers gebracht werde.",
16: "Entwurf eines Schreibens an den Fürsten: Hardenberg habe heute den Gesandten in St. Petersburg, Generalmajor von Schöler, vom Entschädigungsgesuch für die Trąbczyner Güter unterrichtet und ihm aufgetragen, es dem Kaiser von Russland zur Kenntnis zu bringen. Er stellt dem Fürsten anheim, seine Angelegenheit nunmehr in St. Petersburg unmittelbar zu verfolgen, und wünscht ihm den günstigsten Erfolg.",
17: "Entwurf einer Weisung an Schöler: Der Fürst erhielt vom verstorbenen König die Trąbczyner Güter, früher Eigentum des Starosten Prusimski; sie gelangten 1806 und 1807 an dessen Tochter Miączyńska zurück, der der Kaiser von Russland den Besitz bestätigte. Da einige Donatare im Königreich Polen entschädigt worden sind, macht auch der Fürst Anspruch. Schöler soll den Antrag zur Kenntnis des Kaisers bringen, jedoch nur im Allgemeinen und ohne ihn dringend zu unterstützen, da es eine Gnadensache sei.",
18: "Registraturvermerk: Der Bericht ist unter Nr. 3278 C an die 3. Sektion des auswärtigen Departements abgegeben worden, gezeichnet Bever; er ist mit den Akten beigefügt, gezeichnet Strenger.",
19: "Die Witwe von Brehmer bittet Hardenberg um Hilfe: Ihr verstorbener Bruder, Major von Seehausen, lieh dem Fürsten 1803 ein Kapital von 5000 Rthl gegen Verpfändung des Gutes Szetlewek. Der Fürst zahlte weder Kapital noch Zinsen; 1807 wurde ihm das Gut abgenommen und der Erbin des früheren Besitzers zurückgegeben. Sie bittet um Befriedigung aus dem übrigen Vermögen des Fürsten. Ein Randvermerk Stägemanns: eine Entschädigung des russischen Kaisers müsse den auf die Güter ingrossierten Gläubigern zustattenkommen.",
20: "Zwei Verfügungen: Der Witwe von Brehmer ist zu eröffnen, sie müsse den Fürsten wegen ihres auf Szetlewek eingetragenen Kapitals von 5000 Rthl zuerst vor seiner Gerichtsbehörde belangen, damit der Anspruch rechtlich feststehe. Schöler ist mitzuteilen, dass die hypothekarischen Gläubiger Gefahr laufen, ihre Kapitalien zu verlieren, da der Fürst Trąbczyn deterioriert und mit Schulden belastet habe; er soll berichten, falls der Kaiser eine Entschädigung gewährt.",
21: "Entwurf einer Antwort an die Witwe von Brehmer: Ihre an Hardenberg gerichtete Vorstellung vom 26. April sei dem Ministerium zugefertigt worden. Wolle sie wegen des auf Szetlewek eingetragenen Kapitals von 5000 Rthl aus dem übrigen Vermögen des Fürsten Befriedigung suchen, so müsse sie ihn zuerst vor seiner Gerichtsbehörde belangen, um den Anspruch rechtlich festzustellen, falls der Kaiser von Russland dem Fürsten eine Entschädigung gewährt.",
22: "Entwurf eines Schreibens an Schöler: Mit Bezug auf das Schreiben vom 29. April teilt das Ministerium mit, dass die hypothekarischen Gläubiger Gefahr laufen, ihre Kapitalien zu verlieren, da der Fürst Trąbczyn deterioriert und mit Schulden belastet hat; Schöler möge dies zur Sprache bringen. Er soll Nachricht geben, falls der Kaiser dem Fürsten eine Entschädigung gewährt, damit die Gläubiger ihre Gerechtsame verfolgen können.",
23: "Die Witwe von Brehmer überreicht dem Ministerium ein rechtskräftiges Erkenntnis der ehemaligen südpreußischen Regierung zu Kalisz von 1806, wonach der Fürst zur Zahlung der 5000 Rthl nebst Zinsen verurteilt wurde, und das Testament ihres Bruders, des Majors von Seehausen. Sie bittet, sich wegen Kapital und Zinsen zu verwenden. Das Ministerium verfügt, ihr zu eröffnen, dass nach Lage der Umstände ein Mehreres nicht geschehen könne.",
24: "Entwurf einer Antwort an die Witwe von Brehmer: Das Ministerium habe der Gesandtschaft zu Petersburg bereits mitgeteilt, dass die hypothekarischen Gläubiger Gefahr laufen, ihre Kapitalien zu verlieren. Mehr könne es für sie nicht tun; sie müsse ihre Rechte selbst wahrnehmen, falls der Kaiser dem Fürsten eine Entschädigung gewährt. Die am 25. Juli eingereichten Anlagen gehen zurück.",
25: "Schöler berichtet dem Ministerium aus St. Petersburg, er habe am 17. Mai dem Grafen Nesselrode eine Note in der Angelegenheit des Fürsten übergeben und in einer späteren Note vom 1. August den im Erlass vom 29. Juni berührten Umstand zur Sprache gebracht. Die erst gestern erteilte Antwort sei abschlägig ausgefallen. Das Ministerium verfügt, dem Fürsten Abschrift der Anlage zu senden.",
26: "Entwurf eines Schreibens an den Fürsten: Das Ministerium übersendet Abschrift der Note, mit der das russische Ministerium die Verwendung der Gesandtschaft zu Petersburg wegen der Entschädigung für Kamionna und Trąbczyn beantwortet hat, und bedauert, dass es trotz der gesandtschaftlichen Bemühung nicht gelungen ist, einen günstigen Erfolg herbeizuführen.",
27: "Note des russischen Gesandten Alopeus an Ancillon: Herzog Eugen von Württemberg empfahl die Forderungen der Erben des Fürsten von Hohenlohe-Ingelfingen und des Grafen Bethusy an das Königreich Polen. Die Erben berufen sich auf die Generale von Zastrow und von Sanitz; die Sache wurde schon 1816 mit Schöler verhandelt und abgelehnt. Bethusys Antrag nach Artikel 18 des Wiener Vertrags lehnte die polnische Regierung ab. Der Kaiser bedauert, der Empfehlung nicht folgen zu können.",
28: "Abschrift eines Berichts des Fürsten Zajączek an den Kaiser: Graf Ernst Bethusy bat, mit seinen drei Söhnen zu den Vergünstigungen des Artikels 18 des Wiener Vertrags zugelassen zu werden. Der Artikel gelte nur für Besitzungen, die von der Grenze zwischen dem Königreich Polen und dem Großherzogtum Posen durchschnitten werden. Bethusy wolle offenbar nur Eisenerz für seine Hütten in Schlesien ausführen, was die Zollvorschriften verbieten.",
29: "Entwurf eines Schreibens an Minister von Schuckmann: Die Erben des verstorbenen Fürsten von Hohenlohe-Ingelfingen und Graf Bethusy ließen sich bei der russischen Regierung durch Prinz Eugen von Württemberg vertreten; nach der Note des russischen Gesandten hat der Kaiser beide Gesuche abgelehnt. Für die Erben könne, als in einer bloßen Gnadensache, keine Verwendung stattfinden. Bethusys Antrag sei unzulässig, da seine Besitzungen nicht von der neuen Grenze durchschnitten werden. Die weitere Verfügung wird dem Minister anheimgestellt.",
30: "Schuckmann antwortet dem Ministerium der auswärtigen Angelegenheiten: Er stimme zu, dass der Anspruch des Grafen Bethusy auf freien Verkehr zwischen seinen Besitzungen in Schlesien und dem Königreich Polen auch nach dem Traktat unzulässig sei. Er habe dies Bethusy unter Verweis auf Artikel 18 eröffnet, mit der Bemerkung, dass die preußische Regierung Einspruch erhoben hätte, wenn die russische dem Gesuch stattgegeben hätte.",
}


def main():
    import unitlib
    import read_letters as RL              # also sets stdout to UTF-8
    unit = unitlib.one_unit('iiihamdaiiinr12765')
    corpus = RL.Corpus(unit)
    reading = json.load(open(os.path.join(UNIT_DIR, 'reading.json'), encoding='utf-8'))
    os.makedirs(RL.out_dir(unit), exist_ok=True)
    for lid, text in sorted(S.items()):
        n = len(text.split())
        if not 25 <= n <= 80:
            sys.exit(f'document {lid}: {n} words')
        if '—' in text or '–' in text:
            sys.exit(f'document {lid}: a dash')
        r = reading[unit.pad(str(lid))]
        RL.save(unit, corpus, str(lid), {
            'reading_notes': r['notes'], 'legibility': r['legibility'],
            'summary_de': text, 'claims': r['claims'], 'fixes': [],
            'suspicions': r['doubtful_words']},
            {'input': 0, 'output': 0, 'cache_read': 0, 'cache_write': 0},
            {'model': 'in-session reading, no API call (2026-10-01)'})
    print(len(S), 'draft summaries written to', RL.out_dir(unit))
    print('words:', min(len(t.split()) for t in S.values()), 'to',
          max(len(t.split()) for t in S.values()))


if __name__ == '__main__':
    main()
