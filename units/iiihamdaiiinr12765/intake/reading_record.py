# -*- coding: utf-8 -*-
"""The reading of every document of this file, written down as reading.json.

    python units/iiihamdaiiinr12765/intake/reading_record.py

The other units' readings came from a paid run of pipeline/review/read_letters.py.
This one was made in the working session of 2026-10-01, at no API cost, by the
same reader who had just compared all thirty documents with their scans,
corrected them and identified their signatures. It has the same shape: notes on
who writes to whom about what, legibility, statements with the lines that
support them, and words still suspected of being misread. It has NOT had the
second, independent call that checks each statement; every statement was
re-read against its lines here instead.

Lines below are corpus lines (units/<slug>/corpus.txt), as (first, last) ranges;
the script converts them to the document's own line numbers, which is what
reading.json holds and what the site shows.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'review'))
S, P, G = 'sound', 'partly garbled', 'largely garbled'

# doc: (legibility, notes, [(statement, [(first, last), ...])], [(line, word, note)])
R = {
1: (S,
 "Triebenfeld to the State Chancellor Hardenberg, Vienna, 25 Oct 1814. He reminds him that on 6 May in Paris he handed over a letter from Prince Hohenlohe to the Russian Emperor, encloses a copy of Hardenberg's answer of 14 May (document 3), and asks leave to bring the matter up again now that the moment is decisive. The chancery noted that the petition was handed to Staatsrath Stägemann on 20 Nov 1814 (Küster).",
 [("Triebenfeld übergab am 6. Mai 1814 in Paris ein Schreiben des Fürsten Hohenlohe an den russischen Kaiser", [(13, 14)]),
  ("Er legt Hardenbergs Resolution vom 14. Mai in Abschrift bei und bittet, die Sache im jetzt entscheidenden Zeitpunkt wieder in Erinnerung bringen zu dürfen, und um Hilfe", [(15, 19)]),
  ("Kanzleivermerk: am 20. November 1814 in Wien an Staatsrat Stägemann abgegeben, gezeichnet Küster", [(25, 27)])],
 []),
2: (P,
 "Draft of the reply to Triebenfeld, Vienna, 25 Nov 1814, written beneath his letter and approved by Stägemann and Hardenberg. The Prince's claims to Trąbczyn and Kaemen will settle themselves once the general settlement over the Duchy of Warsaw, now in progress, is carried out.",
 [("Die Ansprüche des Fürsten auf Trąbczyn und Kaemen würden sich von selbst ausgleichen, sobald die allgemeine Auseinandersetzung und Übereinkunft wegen des Herzogtums Warschau zur Ausführung komme", [(35, 39)])],
 [(37, 'Wort', "probably 'Werk' ('im Werk begriffene'); the editor could not tell on the scan"),
  (38, 'Auseinändersezung', "Auseinandersezung; the ä is a slip")]),
3: (S,
 "Copy of Hardenberg's letter to Triebenfeld, Paris, 14 May 1814, enclosed in document 1. The Prince's claims to the South Prussian estates given him in 1796, Trąbczyn and Kaemen, can only be raised with any prospect once the Warsaw affairs are settled. That is not yet so, and he is therefore holding back the Prince's letter to Emperor Alexander that Triebenfeld handed him on the 6th; Triebenfeld is to tell the Prince.",
 [("Die Ansprüche des Fürsten auf die 1796 geschenkten südpreußischen Güter Trąbczyn und Kaemen könnten erst nach definitiven Bestimmungen über die Warschauer Angelegenheiten mit Aussicht auf Erfolg angeregt werden", [(46, 49)]),
  ("Hardenberg hält deshalb das am 6. Mai übergebene Schreiben des Fürsten an Kaiser Alexander zurück und bittet Triebenfeld, dies dem Fürsten zu eröffnen", [(50, 53)])],
 []),
4: (S,
 "Triebenfeld to Hardenberg, Vienna, 2 March 1815: the fullest statement of the case. In 1796 the late King gave the Prince Kaemen and Kulm in the Posen department, the villages Trąbczyn, Szettleweck, Nowawies, Lazy, Laske, Osziny and Trąbczyner Hauland in Konin district, and Brzyze in Cujavia, confiscated from a von Prusimski after his flight. The Prince held them over eleven years, except Brzyze, which Prusimski's daughter (now married von Miączyńska) recovered as her mother's inheritance. In 1804 he sold Kaemen and Kulm to the bank director Leixner of Frankfurt an der Oder. In 1807, fourteen weeks after the peace of Tilsit, the Polish administrative commission took all the estates without any judgment and gave them to Miączyńska. The Prince sued at the peace court at Konin and then before the tribunal at Kalisz, which after more than a year declared itself not empowered to undo the commission's order: she keeps the estates and the Prince pays the costs. She draws all the revenues and has paid no interest since 1806; Leixner lost his fortune, his living and his freedom. Triebenfeld asks Hardenberg to have Kulm and Kaemen returned to Leixner, so that the Royal Bank can be satisfied, and to intercede with the Russian Emperor so that the Trąbczyn estates beyond the Prosna are returned to the Prince with nine years' revenues, 36500 rt. The chancery marked it to be laid before Stägemann; Hardenberg's paraph of 14 March.",
 [("1796 verlieh der König dem Fürsten die Güter Kaemen und Kulm im Posener Departement, die Dörfer Trąbczyn, Szettleweck, Nowawies, Lazy, Laske, Osziny und Trąbczyner Hauland im Kreis Konin sowie Brzyze in Cujawien, die dem entwichenen von Prusimski konfisziert worden waren", [(65, 70)]),
  ("Der Fürst besaß die Güter über 11 Jahre, außer Brzyze, das Prusimskis Tochter, verehelichte von Miączyńska, als mütterliches Erbteil vindizierte", [(71, 72)]),
  ("1804 verkaufte er Kaemen und Kulm an den Bankdirektor Leixner zu Frankfurt an der Oder, der sie 3 Jahre ungestört besaß", [(72, 74)]),
  ("1807, 14 Wochen nach dem Tilsiter Frieden, nahm die polnische Verwaltungskommission dem Fürsten und Leixner sämtliche Güter ohne richterliches Erkenntnis weg und gab sie der Miączyńska", [(75, 77)]),
  ("Der Fürst klagte beim Friedensgericht zu Konin und dann beim Tribunal zu Kalisz; dieses erklärte nach über einem Jahr, es sei nicht ermächtigt, die Verfügung der Verwaltungskommission aufzuheben, die Miączyńska bleibe in den Gütern, der Fürst trage die Kosten", [(78, 88)]),
  ("Die Miączyńska zieht sämtliche Revenuen ein und zahlt seit 1806 keine Zinsen", [(89, 90)]),
  ("Leixner verlor dadurch sein Vermögen, sein Brot und seine Freiheit", [(90, 92)]),
  ("Triebenfeld bittet, Leixner Kulm und Kaemen zurückgeben zu lassen, damit die Königliche Bank befriedigt werden kann, und beim russischen Kaiser zu erwirken, dass der Fürst die Trąbczyner Güter jenseits der Prosna mit den seit 9 Jahren bezogenen Revenuen von 36500 Rthl zurückerhält", [(93, 99)]),
  ("Kanzleivermerk: Staatsrat Stägemann vorzulegen, Paraphe Hardenbergs vom 14. März", [(108, 110)])],
 [(80, 'Submissiert', "probably 'submissest' (most humbly)"),
  (83, 'nicht nicht', "a word doubled; perhaps 'auch noch nicht'")]),
5: (P,
 "Draft of the reply to Triebenfeld, Vienna, 17 March 1815, issued in Hardenberg's name; much of it is badly read. The enclosures are returned. A diplomatic negotiation has been opened on compensating those donees of South Prussian estates who lost possession after the peace of Tilsit, and its result will be communicated to the Prince in due course. As for Leixner of the Frankfurt bank: it was not his loss of the Kolno and Kähmen estates that brought him under judicial investigation, but the irregular conduct of his post, and in particular that he borrowed on the asset registered on Kolno and Kähmen for the merchant Simon at its full value when he already knew Miączyńska had taken the estates.",
 [("Über die Entschädigung der Donatare südpreußischer Güter, denen der Besitz seit dem Frieden von Tilsit entzogen wurde, sei eine diplomatische Unterhandlung eingeleitet, deren Ergebnis dem Fürsten zu seiner Zeit mitgeteilt werde", [(121, 126)]),
  ("Leixner sei nicht durch den Verlust der Güter Kolno und Kähmen in die gerichtliche Untersuchung geraten, sondern durch die unregelmäßige Verwaltung seines Postens und die unerlaubte Beleihung des auf Kolno und Kähmen für den Kaufmann Simon eingetragenen Aktivums, als ihm die Besitznahme durch die Miączyńska bereits bekannt war", [(127, 140)])],
 [(119, 'wieder ich auch', "probably 'erwiedere ich auf'"),
  (120, 'Zurückbegabe der Weiligen', "probably 'Zurückgabe der Beilagen'"),
  (125, 'des Kosten Fürsten', "probably 'dem Herrn Fürsten'"),
  (127, 'Bedeuten', "probably 'Rendanten'"),
  (132, 'Vorzug', "probably 'Verhaft' or 'Arrest'"),
  (137, 'bauen Beständen der Buch[?] noch zu mir', "an insertion in the margin, garbled"),
  (138, 'Fsez[?]nahme', "probably 'Besitznahme'"),
  (139, 'End', "probably 'Frau'")]),
6: (P,
 "The Prince to Baron vom Stein, Sławięcice, 12 April 1815, in French. In 1796 the King conferred on him the lands of Kaemen and Trąpczin, forfeited by the flight of the Starost Prussiemski. In 1807, fourteen weeks after Tilsit, the Polish treasury seized them and they were adjudged to Prusimski's daughter, now married to M. de Mięczynsky; all his steps since have failed, and he now hears the Emperor has confirmed those decrees. He asks Stein to obtain an indemnity from the Emperor and sets out the figures: Prusimski had mortgaged the lands for 80,000 écus and 36,000 ducats, and after an eight-year suit and 6,000 écus in costs the Prince had to pay 55,000 écus to free them; interest on the two sums (61,000) since 1807 comes to 24,400 écus, making 85,400 in cash; the Kalisz government valued the lands at 316,000 écus, against 76,000 of debts he had contracted, leaving 240,000; his loss in all 325,400 écus. The receiving office wrote the direction for the reply on it: wait for the final settlement of Polish affairs, when the Prince (Hardenberg) will do all he can to support the claim.",
 [("Der König verlieh ihm 1796 die Güter Kaemen und Trąbczyn, die durch die Flucht des Starosten Prusimski heimgefallen waren", [(148, 148)]),
  ("1807, vierzehn Wochen nach dem Frieden von Tilsit, bemächtigte sich der polnische Fiskus der Güter; sie wurden Prusimskis Tochter, verheiratet mit Herrn von Miączyński, zugesprochen", [(149, 149)]),
  ("Alle Schritte blieben erfolglos; der Kaiser habe die Dekrete zugunsten der Frau Miączyńska bestätigt", [(150, 150)]),
  ("Er bittet Stein, beim Kaiser eine angemessene Entschädigung zu erwirken", [(151, 151), (154, 154)]),
  ("Prusimski hatte die Güter für 80000 écus und 36000 Dukaten verpfändet; nach einem achtjährigen Prozess und 6000 écus Kosten musste der Fürst 55000 écus zahlen, um sie zu befreien", [(155, 155)]),
  ("Er beziffert seine Forderung in barem Geld auf 85400 écus, darunter 24400 écus Zinsen für 1807 bis 1815", [(155, 155)]),
  ("Die Regierung zu Kalisz schätzte die Güter auf 316000 écus, worauf er 76000 écus Schulden aufgenommen hatte; sein Verlust betrage insgesamt 325400 écus", [(156, 158)]),
  ("Vermerk der Kanzlei: zu antworten, dass die endgültige Regelung der polnischen Angelegenheiten abzuwarten sei, die nicht fern scheine; der Fürst werde dann alles tun, um die Forderung zu unterstützen", [(152, 152)])],
 [(148, 'Miedzeris', "the circle of Meseritz (Międzyrzecz)"),
  (150, 'croijés', "probably 'croyois'"),
  (158, 'a ce qui', "the opening 'a' is probably a catchword from the page before")]),
7: (P,
 "Draft in French of Hardenberg's reply to the Prince, Vienna, May 1815 (day left open; his paraph of 30 April). Stein has passed on the letter the Prince wrote him on the 12th. Hardenberg knows the claim on Kaemen and Trąbczyn, asks him to await the final settlement of Polish affairs, which seems near, and promises then to do everything he can to support the request with the King. Document 13 is the fair copy.",
 [("Stein habe ihm das Schreiben des Fürsten vom 12. mitgeteilt", [(173, 173)]),
  ("Der Fürst möge mit seiner Forderung auf Kaemen und Trąbczyn die endgültige Regelung der polnischen Angelegenheiten abwarten, die nicht fern scheine; Hardenberg werde dann alles tun, um das Gesuch beim König zu unterstützen", [(175, 175)])],
 [(173, 'en[?]ire', "a word struck out in the draft; the fair copy has 'du mois passé'. The editor could not tell"),
  (175, 'pour les faire valoir', "the draft as transcribed lacks 'mais je l'engage à attendre', which the fair copy has before these words")]),
8: (S,
 "The Prince to Hardenberg, Sławięcice, 12 May 1815. Poland's fate is decided: the district of his Trąbczyn estates falls under Russian sovereignty, and since both sovereigns have confirmed what the commission did, the estates are lost to him for ever; his one comfort is that the donees are to be compensated with other estates. He expects his compensation from the Russian Emperor and has already written to Stein, but knows Hardenberg's word with the Emperor would help at once. His loss is over 261,000 rt. He would be content with the small Amt Sokolnik near Boleslawice, which yields 8 to 10,000 rt in rent, and asks Hardenberg to obtain it for him, the more so as he is the only one whose estates were taken.",
 [("Der Distrikt der ihm von der polnischen Verwaltungskommission genommenen Trąbczyner Güter falle unter russische Hoheit", [(181, 184)]),
  ("Da beide Souveräne die Handlungen der Kommission bestätigt hätten, seien die Güter für ihn verloren; den Donataren solle eine Entschädigung durch andere Güter gegeben werden", [(185, 191)]),
  ("Er erwarte sein Dedommagement vom russischen Kaiser und habe sich schon an Stein gewandt; durch Hardenbergs Vorwort wäre ihm sogleich geholfen", [(192, 200)]),
  ("Sein Verlust betrage über 261000 Rthl; er wäre mit dem kleinen Amt Sokolnik unweit Boleslawice zufrieden, das 8 bis 10000 Rthl Pacht gibt", [(202, 207)]),
  ("Er bittet Hardenberg, sich beim russischen Kaiser dafür zu verwenden, dass ihm das Sokolniker Amt als Entschädigung verliehen werde", [(207, 213)])],
 [(186, 'Preußl.', "the sense wants the Polish commission of line 183 ('Pohlnl'), not a Prussian one")]),
9: (G,
 "Draft of the reply to the Prince, Vienna, 6 June 1815, in Hardenberg's name; it replaced the cancelled draft 11. Badly read throughout, but the sense holds: he acknowledges the Prince's letter of 12 May on the Trąbczyn claim and says Minister vom Stein has passed on the Prince's letter of April about Kaemen and Trąbczyn. He has asked Zerboni to inform him fully on the present state of both estates, and will tell the Prince what further steps he is able to take once that report is in. He assures him of his sincere sympathy.",
 [("Hardenberg bestätigt den Empfang des Schreibens vom 12. Mai wegen der Trąbczyner Güter; Minister vom Stein habe ihm das an ihn gerichtete Schreiben des Fürsten vom April wegen Kaemen und Trąbczyn mitgeteilt", [(230, 237)]),
  ("Er habe Zerboni ersucht, ihn über die gegenwärtigen Verhältnisse beider Güter in vollständige Kenntnis zu setzen, und behalte sich vor, dem Fürsten danach von seinen weiteren Schritten Nachricht zu geben", [(238, 245)]),
  ("Er versichert seine aufrichtige Teilnahme", [(246, 250)])],
 [(230, 'geringsten', "probably 'geehrtesten'"),
  (232, 'gesorgtniß melden, bisher ich', "garbled; probably 'gehorsamst melde, beehre ich'"),
  (233, 'bemüchtigen', "probably 'benachrichtigen'"),
  (234, '< April.', "the day is not read; the letter to Stein is of 12 April"),
  (240, 'entreten', "garbled; probably 'eintreten'"),
  (241, 'gegenmüßigen Verzichtnißen', "probably 'gegenwärtigen Verhältnißen'"),
  (243, 'behabt', "probably 'behalte'"),
  (243, 'Ausbunden', "probably 'Auskunft'"),
  (246, 'trauesten', "garbled"),
  (247, 'Vorhaus', "garbled")]),
10: (P,
 "Draft to Zerboni di Sposetti at Poznań, Vienna, 6 June 1815, signed in the fair copy by Hardenberg himself. It sends him in the original the Prince's two letters, to Hardenberg of 12 May and to Stein of 12 April, on the estates Kämen and Trąbczyn taken from him. As Zerboni knows the matter fully, he is asked to say what steps could still be taken in the Prince's favour. Kämen is beyond dispute the estate the Prince sold to the bank official Leixner of Frankfurt, so the 55,000 rt and interest are the Bank's to claim and the Prince has long been satisfied; Zerboni's investigation and report are awaited as soon as possible.",
 [("Hardenberg übersendet Zerboni urschriftlich zwei Schreiben des Fürsten, an ihn und an Stein vom 12. April, über die Ansprüche wegen der entzogenen Güter Kämen und Trąbczyn", [(258, 263)]),
  ("Zerboni soll mitteilen, welche Schritte zugunsten des Fürsten noch getan werden können", [(264, 267)]),
  ("Kämen seien unstreitig die Güter, die der Fürst an den Banco-Rendanten Leixner zu Frankfurt verkauft hat; die 55000 Rthl und Zinsen habe die Bank zu fordern, der Fürst sei längst befriedigt", [(269, 273)]),
  ("Hardenberg erwartet Zerbonis Untersuchung und Bericht so bald als möglich", [(273, 275)]),
  ("Die Reinschrift wurde von Hardenberg selbst vollzogen", [(278, 278)])],
 [(256, 'dringl.[?]', "address line, garbled"),
  (257, 'Zahlrungen[?]', "address line, garbled; Zerboni's title"),
  (258, 'Hochwolz überstande', "probably 'Hochwohlg. übersende'"),
  (259, 'von 12 rt.', "probably 'vom 12. v. M.', the letter of 12 May"),
  (270, 'Fürsten von', "probably 'Fürst dem'"),
  (271, 'Magistel', "possibly 'Kaufgeld'; the editor could not tell")]),
11: (P,
 "The first draft of a reply to the Prince's letter of 12 May, Vienna, May 1815, approved by Hardenberg on 21 May and then cancelled in favour of the reply of 6 June (document 9); document 12 is its fair copy. The territorial questions of the Duchy of Warsaw, as far as the provinces returning to Prussia are concerned, are settled; the compensation of the donees in the Duchy is left to a separate negotiation, already begun, in which he will gladly look for a chance to further the Prince's wish to be compensated for Trąbczyn.",
 [("Die Territorialverhältnisse des Herzogtums Warschau seien für die an Preußen zurückfallenden Provinzen definitiv entschieden; die Entschädigung der Donatare sei einer besonderen Unterhandlung vorbehalten, zu der schon geschritten worden sei", [(290, 303)]),
  ("Hardenberg werde im Lauf dieser Unterhandlung Gelegenheit suchen, die Entschädigung für die entzogenen Trąbczyner Güter zu befördern", [(303, 313)]),
  ("Der Entwurf ist kassiert, mit Verweis auf die Verfügung vom 6. Juni 1815", [(288, 289)])],
 [(287, 'R. 28/5 nach Rthl 28/5.', "registry marks, garbled; probably 'mund.' and 'abg.' with the date")]),
12: (S,
 "Fair copy of the cancelled reply of May 1815 (document 11), in a clerk's hand, engrossed and not sent. The same text.",
 [("Die Territorialverhältnisse des Herzogtums Warschau seien für die an Preußen zurückfallenden Provinzen definitiv entschieden; die Entschädigung der Donatare sei einer besonderen Unterhandlung vorbehalten", [(324, 331)]),
  ("Hardenberg werde darin Gelegenheit suchen, die Entschädigung für die entzogenen Trąbczyner Güter zu befördern", [(331, 335)])],
 []),
13: (S,
 "Fair copy in French of Hardenberg's reply to the Prince, Vienna, May 1815 (document 7). Stein has passed on the Prince's letter of the 12th; Hardenberg knows the claim on Kaemen and Trąbczyn, asks him to await the final settlement of Polish affairs, and will then do all he can to support the request with the King.",
 [("Hardenberg bittet den Fürsten, mit der Forderung auf Kaemen und Trąbczyn die endgültige Regelung der polnischen Angelegenheiten abzuwarten, und will das Gesuch dann beim König unterstützen", [(345, 345)])],
 []),
14: (P,
 "Zerboni di Sposetti's report to Hardenberg (then at Paris), Poznań, 2 Nov 1815, answering the order of 6 June. The Prince received Kolno and Kaemen in the Posen country and Trąbczyn in the Kalisz department, both confiscated from the Starost Prusimski after the insurrection of 1794. He sold Kolno and Kaemen to Leixner before 1806, but not Trąbczyn. All the estates went back to the former owner's heirs in 1806-07 and stay with them under the Vienna treaty of 3 May, while His Majesty is inclined to compensate the donees. After empty letters and talks through Triebenfeld, a certain Schenk appeared as the Prince's agent and argued from a volume of accounts that 318,500 rt are due for Trąbczyn, best met by the domain Amt Sokolnik close to the border, which pays 15,000 rt a year; the Prince asks for it as a hereditary grant from the Tsar. Zerboni finds the accounts full of nonsense: Trąbczyn was never worth a third of Sokolnik, and the Prince ran it down and loaded it with debt; he hardly believes any compensation is still due. All the cabinet can do without compromising itself is to move the Russian cabinet to decide to compensate the Prince for Trąbczyn, and leave it to him to settle with the Russian authorities for what and how. In the margin an opinion of 13 April (1816), signed by Stägemann: Kolno and Kaemen are no longer the Prince's, sold in 1805 for 142,000 rt to Leixner; the Prince's agent, the late von Triebenfeld, seems to have taken that up out of pity for Leixner, who has also since died; the ministry should intercede for the Prince over Trąbczyn only. The passage implies Triebenfeld was dead by April 1816.",
 [("Hardenberg hatte Zerboni mit Erlass vom 6. Juni zwei Schreiben des Fürsten zugefertigt, mit dem Befehl, sich über die beim russischen Kabinett zu machenden Schritte zu äußern", [(353, 360)]),
  ("Der Fürst erhielt Kolno und Kaemen im Posenschen und Trąbczyn im Kalischer Departement zum Geschenk; beide waren Eigentum des in die Insurrektion von 1794 verwickelten Starosten Prusimski und konfisziert", [(361, 368)]),
  ("Kolno und Kaemen verkaufte der Fürst vor 1806 an den Banco-Rendanten Leixner, die Trąbczyner Güter nicht", [(369, 371)]),
  ("Sämtliche Güter gelangten 1806/7 an die Erben des vorigen Eigentümers zurück und verbleiben ihnen nach dem Wiener Traktat vom 3. Mai; Seine Majestät sei geneigt, die Donatare zu entschädigen", [(372, 378)]),
  ("Ein gewisser Schenk trat als Mandatar des Fürsten auf und leitete aus einem Band Rechnungen ab, dem Fürsten gebühre für Trąbczyn eine Entschädigung von 318500 Rthl, am besten durch das Domänenamt Sokolnik, das jährlich 15000 Rthl Pacht zahle", [(379, 380), (406, 420)]),
  ("Für Kolno und Kaemen habe nach dem Mandatar zunächst Leixner als Eigentümer die Entschädigung zu fordern", [(421, 424)]),
  ("Zerboni hält die Berechnungen für voll Unsinn; Trąbczyn habe ursprünglich kaum ein Drittel des Wertes von Sokolnik gehabt, sei vom Fürsten deterioriert und mit Schulden überladen; er glaube kaum, dass dieser noch eine Entschädigung zu fordern habe", [(425, 432)]),
  ("Das Kabinett könne nur das russische Kabinett zu dem Entschluss bewegen, den Fürsten für den Verlust von Trąbczyn zu entschädigen, und es ihm überlassen, das Wofür und Wie mit den russischen Behörden selbst zu regeln", [(433, 448)]),
  ("Randvermerk: Kolno und Kaemen gehörten dem Fürsten nicht mehr, da er sie 1805 für 142000 Rthl an Leixner verkauft habe", [(383, 390)]),
  ("Randvermerk: der Mandatar des Fürsten, der verstorbene von Triebenfeld, scheine sich aus Mitleid für den inzwischen ebenfalls verstorbenen Leixner dafür interessiert zu haben", [(390, 396)]),
  ("Randvermerk vom 13. April, gezeichnet Stägemann: es komme nur darauf an, dass sich das Ministerium der auswärtigen Angelegenheiten für den Fürsten wegen der Trąbczyner Güter verwende", [(399, 404)])],
 [(356, 'vom 12ten May', "the letter to Stein is of 12 April (document 6); the one to Hardenberg of 12 May"),
  (393, 'Mandatoris', "'Mandatarius'"),
  (397, 'HauptAmt, als Inselung', "garbled; probably the Hauptbank as holder"),
  (398, 'intalulirten Capitulien', "probably 'intabulirten Capitalien'"),
  (402, 'für vielen Fürsten', "probably 'für den Fürsten'"),
  (403, 'kein zusch[?]. Meisten[?]. Hofe werden', "garbled; the sense is intercession at the Russian court"),
  (404, 'Gericht Jordan widerum erfolgen', "probably 'G. L. R. v. Jordan wiederum vorlegen'")]),
15: (G,
 "Decree of 20 April 1816 on Zerboni's report, by the official Balan; badly read. 1. Schöler at St Petersburg is to be instructed as Zerboni proposed, with the remark that since the Prince's request is purely a matter of grace, his wish is to be brought to the Emperor's knowledge only in general terms and without direct support. 2. The Prince is to be told in Hardenberg's name that his request for compensation will be brought to the Emperor's knowledge through the royal legation.",
 [("Schöler in St. Petersburg soll nach Zerbonis Antrag beauftragt werden, den Wunsch des Fürsten, da es eine reine Gnadensache sei, nur ganz im Allgemeinen zur Kenntnis des Kaisers zu bringen, ohne direkte Unterstützung", [(462, 469)]),
  ("Dem Fürsten soll namens Hardenbergs mitgeteilt werden, dass sein Entschädigungsgesuch durch die königliche Gesandtschaft zur Kenntnis des Kaisers gebracht werde", [(470, 475)])],
 [(462, 'Committat', "'Committatur'"),
  (464, 'Eröhnen[?]', "probably 'Eröfnen'"),
  (467, 'S. Lieut[?].', "probably 'S. Kaiserl.'"),
  (468, 'lecter[?]', "garbled; with the next line probably 'Unterstützung'"),
  (474, 'v. dH[?]. werde gebruesst', "garbled; probably 'von Rußland werde gebracht'"),
  (475, 'andere[?].', "probably 'werden'")]),
16: (P,
 "Draft to the Prince, Berlin, 20 April 1816 (posted on the 30th), in Hardenberg's name with his paraph of 28 April. Following his letter of 6 June last year he reports that he has today informed the envoy at St Petersburg, Major General von Schöler, of the Prince's request for compensation for the Trąbczyn estates and instructed him to bring it to the Emperor's knowledge and to support it. The Prince may now pursue the matter directly in St Petersburg; he wishes him success.",
 [("Hardenberg habe heute den Gesandten in St. Petersburg, Generalmajor von Schöler, vom Entschädigungsgesuch des Fürsten für die Trąbczyner Güter unterrichtet und ihm aufgetragen, es dem Kaiser von Russland zur Kenntnis zu bringen", [(486, 503)]),
  ("Er stellt dem Fürsten anheim, seine Angelegenheit nunmehr in St. Petersburg unmittelbar zu verfolgen, und wünscht ihm den günstigsten Erfolg", [(507, 512)])],
 [(489, 'Beklag[?]', "garbled"),
  (504, 'Ihre[?] des ſtelsagen', "garbled; the line says the envoy is to support the request, while the decree and the instruction to Schöler say without urging it"),
  (515, 'einem', "the closing runs on garbled into the next page"),
  (520, 'vermögte', "garbled")]),
17: (P,
 "Draft instruction to Major General von Schöler, envoy at St Petersburg, Berlin, 29 April 1816, from the third section of the foreign ministry, with Hardenberg's paraph of 28 April. It recites the case in Zerboni's words: the King gave the Prince the Trąbczyn estates, formerly the Starost Prusimsky's; in 1806-07 they went back to the former owner's daughter, Frau von Miączyńska, and the Prince's attempts to recover them failed because the Russian Emperor confirmed her in possession. As some donees in the Kingdom of Poland have since been compensated, the Prince now claims the same. Schöler is to bring the request to the Emperor's knowledge and decision, but only in general terms and without pressing it, since the matter is purely one of grace.",
 [("Der Fürst erhielt vom verstorbenen König die Trąbczyner Güter im Kalischer Departement, Kreis Konin, früher Eigentum des Starosten Prusimsky und durch Konfiskation an den Staat gefallen", [(539, 552)]),
  ("Die Güter gelangten 1806 und 1807 an die Tochter des vorigen Eigentümers, Frau von Miączyńska, zurück; die Versuche des Fürsten, wieder in den Besitz zu kommen, waren vergeblich, da der Kaiser von Russland ihr den Besitz bestätigte", [(553, 570)]),
  ("Da inzwischen einige Donatare im Königreich Polen entschädigt worden sind, macht auch der Fürst darauf Anspruch", [(571, 577)]),
  ("Schöler soll den Antrag zur Kenntnis und Entscheidung des Kaisers bringen, jedoch nur ganz im Allgemeinen und ohne das Gesuch dringend zu unterstützen, da es lediglich eine Gnadensache sei", [(578, 590)])],
 [(573, 'geworden wer¬', "probably 'gewährt worden'"),
  (578, 'Indem ich dann', "garbled opening of the request"),
  (582, 'gefall ist', "probably 'gefälligst'"),
  (590, 'betrachten muss.', "after this the scan has a passage about Sokolnik, struck out; it is not in the transcription")]),
18: (S,
 "Registry note of 3 and 5 May 1816: the report (Zerboni's) has been handed to the third section of the foreign department under no. 3278 C, signed Bever; it is attached with the file, signed Strenger.",
 [("Der Bericht wurde unter Nr. 3278 C an die 3. Sektion des auswärtigen Departements abgegeben (Bever, 3. Mai)", [(598, 602)]),
  ("Er ist mit den Akten beigefügt (Strenger, 5. Mai 1816)", [(603, 605)])],
 []),
19: (P,
 "The widow of Colonel von Brehmer to Hardenberg, Sommerfeld, 26 April 1816. Her late brother, the Prussian Major Johann Friedrich von Seehausen, whose sole heir she is, lent the Prince 5,000 rt on a bond of 26 March 1803, secured on his estate Szettlewek in Konin district, with a promise to satisfy him otherwise if the estate did not cover it. The Prince paid neither capital nor interest while he held the estate, and after South Prussia was ceded it was taken from him by the commission's decision of 21 July 1807 and returned to the former owner's heiress, Prusimska, married von Dąbska. She has no hope of payment from the estate and cannot pursue the Prince; she has no means but this capital and a pension of 120 rt. She asks Hardenberg to help her to payment from the Prince's other property. The office assigned it to Balan and attached Zerboni's report; Stägemann's opinion of 7 May 1816 in the margin: Szettlewek belongs to Trąbczyn, and since the Prince ran the estates down and loaded them with debt, any compensation the Tsar grants must go not to the Prince but to the creditors registered on the estates.",
 [("Ihr verstorbener Bruder, Major Johann Friedrich von Seehausen, dessen Universalerbin sie ist, lieh dem Fürsten auf Obligation vom 26. März 1803 ein Kapital von 5000 Rthl, wofür dieser sein Gut Szettlewek im Koniner Kreis verpfändete", [(610, 618), (643, 645)]),
  ("Solange der Fürst im Besitz war, zahlte er weder Kapital noch Zinsen", [(645, 647)]),
  ("Nach der Abtretung Südpreußens wurde ihm Szettlewek durch Erkenntnis der Kommission vom 21. Juli 1807 abgenommen und der Erbin des früheren Besitzers, der Prusimska verm. von Dąbska, zurückgegeben", [(648, 655)]),
  ("Sie lebt von einer Pension von 120 Rthl und hat außer diesem Kapital kein Vermögen", [(659, 661)]),
  ("Sie bittet Hardenberg, sich zu verwenden, dass sie an Kapital und Zinsen aus dem übrigen Vermögen des Fürsten befriedigt werde", [(662, 667)]),
  ("Kanzleivermerke: präsentiert im Mai 1816, Dezernent Legationsrat Balan, Zerbonis Bericht beizufügen, dem Herrn von Jordan vorzulegen", [(619, 630)]),
  ("Randvermerk Stägemanns vom 7. Mai 1816: Szettlewek gehöre zu Trąbczyn; da der Fürst die Güter deterioriert und mit Schulden beladen habe, müsse eine Entschädigung des russischen Kaisers nicht dem Fürsten, sondern den auf die Güter ingrossierten Gläubigern zustattenkommen", [(631, 641)])],
 [(614, 'und Obligation', "probably 'auf Obligation'"),
  (616, 'Caier[?]:', "probably 'Cour:' (Courant)"),
  (634, '[h?] erbladen', "garbled; probably 'erklären'"),
  (651, 'Beschr.', "garbled; a place and date formula, perhaps 'Warschau'"),
  (667, 'ſulte', "garbled; with 'an¬' probably a verb such as 'erhalte'")]),
20: (P,
 "Minute of two decisions by Balan, Berlin, 15 and 18 June 1816; badly read in places. 1. A resolution for the widow von Brehmer: her petition was passed by Hardenberg to the section chief; to be paid her 5,000 rt, once registered on Szettlewek, from the Prince's other property she must first sue him before his own court, so that the claim is legally established and can be considered if the Russian Emperor grants the Prince compensation for Szettlewek and Trąbczyn. 2. Schöler is to be told, with reference to the letter of 29 April, that since the Prince ran Trąbczyn down and loaded it with debt the mortgage creditors risk losing their capital; he may raise this when supporting the Prince's request, and is asked to report at once if the Emperor grants compensation, so that the creditors can pursue their rights.",
 [("Die Vorstellung der Witwe von Brehmer vom 26. April sei von Hardenberg dem Sektionschef zugefertigt worden", [(677, 681)]),
  ("Um wegen ihres auf Szettlewek eingetragenen Kapitals von 5000 Rthl aus dem übrigen Vermögen des Fürsten befriedigt zu werden, müsse sie ihn zuerst vor seiner Gerichtsbehörde belangen, damit der Anspruch rechtlich feststehe", [(682, 691)]),
  ("Schöler soll eröffnet werden, dass die hypothekarischen Gläubiger durch die Einziehung des Gutes 1807 Gefahr laufen, ihre Kapitalien zu verlieren, da der Fürst Trąbczyn deterioriert und mit Schulden belastet habe; er möge dies zur Sprache bringen", [(699, 711)]),
  ("Schöler wird ersucht, den Sektionschef unverzüglich zu unterrichten, falls der Kaiser dem Fürsten eine Entschädigung gewährt, damit die Gläubiger ihre Gerechtsame verfolgen können", [(712, 718)])],
 [(688, 'Inverderst[?]', "probably 'Zuvörderst'"),
  (690, 'berüber.', "garbled; with the next line probably 'berücksichtigt'"),
  (696, 'Ingenähmen[?]', "probably 'zu gewähren'"),
  (714, 'In genähmen geraten', "probably 'zu gewähren geruhen'")]),
21: (P,
 "Draft to the widow von Brehmer at Sommerfeld, Berlin, dated 22 June 1816 (headed 29 June; fair copy 3 July, posted 6 July). Her petition of 26 April to Hardenberg has been passed on. If she means to seek payment from the Prince's other property for the 5,000 rt her late brother lent him, registered on Szettlewek, she must first sue him before his own court to establish the claim, in case she wants it considered should the Emperor of Russia grant the Prince compensation for Szettlewek and Trąbczyn.",
 [("Ihre an Hardenberg gerichtete Vorstellung vom 26. April ist dem Ministerium zugefertigt worden", [(733, 737)]),
  ("Will sie wegen des auf Szettlewek eingetragenen Kapitals von 5000 Rthl aus dem übrigen Vermögen des Fürsten Befriedigung suchen, so müsse sie ihn zuerst vor seiner Gerichtsbehörde belangen, um den Anspruch rechtlich festzustellen", [(737, 748)]),
  ("Dies gelte für den Fall, dass der Kaiser von Russland dem Fürsten wegen Szettlewek und Trąbczyn eine Entschädigung gewährt", [(749, 755)])],
 [(737, 'Ewohnfrau', "garbled; a form of address"),
  (744, 'Beständigung in', "probably 'Befriedigung zu'"),
  (754, 'hier,', "garbled through the next line; probably 'hierbei verlangen'")]),
22: (P,
 "Draft to Schöler at St Petersburg, Berlin, 22 June 1816, from the third section; fair copy 3 July; paraphs of Hoffmann and Balan, 1 July. Following the letter of 29 April on interceding for the Prince, it passes on the later information that, as the Prince ran Trąbczyn down and loaded it with debt, the mortgage creditors risk losing their capital; Schöler may mention this when supporting the request. He is also asked to report if the Emperor grants the Prince any compensation, so that the creditors can pursue their rights.",
 [("Mit Bezug auf das Schreiben vom 29. April teilt das Ministerium Schöler mit, dass die hypothekarischen Gläubiger Gefahr laufen, ihre Kapitalien zu verlieren, da der Fürst Trąbczyn deterioriert und mit Schulden belastet hat; er möge dies zur Sprache bringen", [(766, 785)]),
  ("Schöler soll Nachricht geben, falls der Kaiser dem Fürsten eine Entschädigung gewährt, damit die Gläubiger ihre Gerechtsame verfolgen können", [(786, 793)])],
 [(774, 'so', "garbled; probably 'sehe'"),
  (776, 'Nachm[?]¬', "garbled; probably 'Nachricht'"),
  (777, 'den Fürst', "'der Fürst'"),
  (786, 'Einehml[?].', "garbled; a form of address")]),
23: (P,
 "The widow von Brehmer to the foreign ministry, Sommerfeld, 25 July 1816. In answer to the resolution of 29 June she sends a final judgment of the former South Prussian government at Kalisz, published 24 May 1806, condemning the Prince to pay the 5,000 rt with interest, and a copy of her late brother Major von Seehausen's will, which shows her to be his sole heir and that much of the capital is left in legacies to people as needy as she is. She asks the ministry to intercede for the capital and interest. The office's direction, Berlin, 3 August 1816 (Balan): she is to be told what was sent to the legation on 22 June, and that in the circumstances nothing more can be done.",
 [("Sie überreicht ein rechtskräftiges Erkenntnis der ehemaligen südpreußischen Regierung zu Kalisch, publiziert am 24. Mai 1806, wonach der Fürst zur Zahlung der 5000 Rthl nebst Zinsen verurteilt wurde", [(801, 809)]),
  ("Sie legitimiert sich durch das Testament ihres verstorbenen Bruders, des Majors von Seehausen, als dessen einzige Universalerbin", [(809, 813)]),
  ("Ein großer Teil des Kapitals sei zu Legaten bestimmt; sie bittet das Ministerium, sich wegen Kapital und Zinsen zu verwenden", [(813, 819)]),
  ("Verfügung vom 3. August 1816: die Bittstellerin sei mit dem bekannt zu machen, was unter dem 22. Juni an die Gesandtschaft erlassen wurde, und ihr zu eröffnen, dass nach Lage der Umstände ein Mehreres nicht geschehen könne", [(823, 842)])],
 [(801, 'hoher Ministerio', "'hohen Ministerio'"),
  (828, 'was an dic[h?]', "garbled through line 830; probably 'was an die königl. Gesandschaft'"),
  (832, 'erlagen werden', "probably 'erlaßen worden'"),
  (835, 'der zu röhen', "probably 'dabei zu eröfnen'"),
  (841, 'tione[?]', "probably 'könne'")]),
24: (P,
 "Draft to the widow von Brehmer, Berlin, 10 August 1816 (posted on the 13th), from the third section; paraphs of Hoffmann (12 August) and Balan. Already on her letter of 26 April the ministry told the legation at Petersburg that the mortgage creditors risk losing their capital, for use when supporting the Prince's request. As the ministry can do no more for her, and she must herself look to her rights if the Emperor grants the Prince compensation, the papers she sent on 25 July are returned.",
 [("Das Ministerium hat der Gesandtschaft zu Petersburg bereits mitgeteilt, dass die hypothekarischen Gläubiger Gefahr laufen, ihre Kapitalien zu verlieren, um davon bei der Unterstützung des Gesuchs Gebrauch zu machen", [(852, 865)]),
  ("Mehr könne das Ministerium für sie nicht tun; sie müsse ihre Rechte selbst wahrnehmen, falls der Kaiser dem Fürsten eine Entschädigung gewährt; die am 25. Juli eingereichten Anlagen gehen zurück", [(865, 875)])],
 [(863, 'das Für¬', "'des Fürsten'")]),
25: (S,
 "Schöler to the third section of the foreign ministry, St Petersburg, 23 November 1816 (11 November old style). As instructed on 29 April he handed Count Nesselrode a note on the Prince's matter on 17 May, and in a later note of 1 August raised the circumstance mentioned in the order of 29 June. Only yesterday did he receive an answer, enclosed in copy: a refusal. The office (Balan, received 8 December 1816) ordered a copy of the enclosure sent to the Prince.",
 [("Schöler übergab am 17. Mai dem Grafen Nesselrode eine Note in der Angelegenheit des Fürsten und brachte in einer späteren Note vom 1. August den im Erlass vom 29. Juni berührten Umstand zur Sprache", [(882, 886)]),
  ("Die erst gestern erteilte Antwort ist abschlägig ausgefallen", [(887, 889)]),
  ("Verfügung: dem Fürsten zu Hohenlohe Abschrift der Anlage (Berlin, 9. Dezember 1816)", [(894, 899)])],
 [(886, 'Erlasse vom 29sten Juny', "the draft of that order is dated 22 June and headed 29 June (documents 21 and 22)")]),
26: (P,
 "Draft to the Prince at Sławięcice, Berlin, 22 December 1816 (posted on the 24th), with Hardenberg's and Balan's paraphs of 21 December. It sends a copy of the note with which the Russian ministry answered the legation's intercession over the compensation he sought for Kamen and Trąbczyn, and regrets that the legation's effort brought no favourable result.",
 [("Das Ministerium übersendet dem Fürsten Abschrift der Note, mit der das russische Ministerium die Verwendung der Gesandtschaft wegen der Entschädigung für Kamen und Trąbczyn beantwortet hat", [(908, 917)]),
  ("Es bedauert, dass es trotz der gesandtschaftlichen Bemühung nicht gelungen ist, einen günstigen Erfolg herbeizuführen", [(917, 921)])],
 [(906, 'c. alleg: Spost.', "dispatch note, garbled"),
  (908, 'S. Durchl.', "'E. Durchl.'"),
  (914, 'damahl', "garbled")]),
27: (S,
 "Note in French from the Russian envoy at Berlin, Alopeus, to Ancillon of the Prussian foreign ministry, Berlin, 31 January 1820 (received 5 February, assigned to Balan). Duke Eugen of Württemberg had recommended to the Russian ministry the claims on the Kingdom of Poland of the heirs of Prince Friedrich Ludwig of Hohenlohe-Ingelfingen and of Count Bethusy; the Emperor had both examined. The Prince received in 1796 part of the lands confiscated from the Starost Prusimski; the events of 1807 deprived him of them, and they were restored to the former owner's successors. His heirs now claim an indemnity, citing the generals Zastrow and Sanitz, who were compensated at the Prussian government's expense. The matter was already discussed in 1816 with General von Schöler and refused by the note of 10 November 1816; the case of Zastrow and Sanitz is explained by a report of Prince Zajączek, and the Polish minister Count Sobolewski has confirmed the arguments. Count Ernst Bethusy, with property in Poland and Prussian Silesia, claimed the benefits of article 18 of the Vienna treaty for owners on both sides; the Polish government refused, since the article concerns only properties cut by the new frontier with the Grand Duchy of Posen, and his aim seems only to ease an export harmful to the Kingdom. The Emperor regrets he cannot follow Duke Eugen's recommendation; the envoy asks the King's ministry to tell the petitioners.",
 [("Herzog Eugen von Württemberg empfahl dem kaiserlichen Ministerium die Forderungen der Erben des Fürsten Friedrich Ludwig von Hohenlohe-Ingelfingen und des Grafen Bethusy an das Königreich Polen; der Kaiser ließ beide prüfen", [(927, 927)]),
  ("Der Fürst erhielt 1796 einen Teil der dem Starosten Prusimski konfiszierten Güter; die Ereignisse von 1807 nahmen sie ihm, und sie wurden den Nachfolgern des früheren Eigentümers zurückgegeben", [(928, 932)]),
  ("Die Erben fordern eine Entschädigung vom Königreich Polen und berufen sich auf die Generale von Zastrow und von Sanitz, die auf Kosten der preußischen Regierung entschädigt wurden", [(933, 933)]),
  ("Die Sache wurde schon 1816 mit General von Schöler verhandelt und vom Kaiser abgelehnt (Note vom 10. November 1816)", [(934, 934)]),
  ("Der Fall Zastrow und Sanitz sei durch einen Bericht des Fürsten Zajączek aufgeklärt; die Antwort des Grafen Sobolewski bestätige die Gründe", [(935, 938)]),
  ("Graf Ernst Bethusy verlangte die Vergünstigungen des Artikels 18 des Wiener Vertrags für gemischte Eigentümer; die polnische Regierung lehnte ab, weil der Artikel nur von der Grenze durchschnittene Besitzungen betreffe", [(939, 942)]),
  ("Der Kaiser bedauert, der Empfehlung des Herzogs Eugen nicht folgen zu können, ; der Gesandte bittet das Ministerium des Königs, den Bittstellern die Entscheidungen bekannt zu machen", [(943, 945)])],
 []),
28: (S,
 "Copy in French of the report of Prince Zajączek, the Tsar's viceroy in Poland, to the Emperor, Warsaw, 4 June 1819 (23 May old style), enclosed with document 27. Count Ernst Bethusy asked to be admitted with his three sons to the benefits of article 18 of the Vienna treaty for owners on both sides. Zajączek reports that the article applies only to properties cut by the frontier between the Kingdom and the Grand Duchy of Posen, so it cannot be read in Bethusy's favour; and that Bethusy seems to want only the freedom to carry iron ore from the Kingdom to his forges in Silesia, which he had under Prussian rule but which the customs rules now forbid as harmful to the country's works.",
 [("Graf Ernst Bethusy bat, mit seinen drei Söhnen zu den Vergünstigungen des Artikels 18 des Wiener Vertrags für gemischte Eigentümer zugelassen zu werden", [(953, 953)]),
  ("Der Artikel gelte nur für Besitzungen, die von der Grenze zwischen dem Königreich Polen und dem Großherzogtum Posen durchschnitten werden, und könne nicht zugunsten des Bittstellers ausgelegt werden", [(954, 957)]),
  ("Bethusy wolle offenbar nur Eisenerz aus dem Königreich für seine Hütten in Schlesien ausführen, was die Zollvorschriften verbieten", [(958, 958)])],
 []),
29: (P,
 "Draft to the minister of the interior von Schuckmann, Berlin, 13 May 1820, with the paraphs of Hoffmann and Balan of 12 May; badly read in places. The heirs of the late Prince of Hohenlohe-Ingelfingen, who lived at Sławięcice, and Count Bethusy had their requests put to the Russian government by Prince Eugen of Württemberg: the heirs for compensation for Kaemen and Trąbczyn, Bethusy for free traffic between his properties in Silesia and Poland under the treaty of 3 May 1815. The Russian envoy's note, enclosed in copy, refuses both. For the heirs, as a pure matter of grace, no intercession is possible; the envoy's intercession in the Prince's lifetime was also unheeded. Bethusy's request is inadmissible, since article 18 favours only owners whose land the new frontier cuts, while his properties lie far apart in different provinces; had Russia granted it, this government would have had to object. As the petitioners' whereabouts are not known (their properties lie in the Oppeln district), the minister is left to deal with them.",
 [("Die Erben des verstorbenen Fürsten von Hohenlohe-Ingelfingen und Graf Bethusy ließen sich bei der russischen Regierung durch Prinz Eugen von Württemberg vertreten, die Erben wegen einer Entschädigung für Kaemen und Trąbczyn, Bethusy wegen freien Verkehrs zwischen seinen Besitzungen in Schlesien und Polen", [(965, 979)]),
  ("Nach der in Abschrift mitgeteilten Note des russischen Gesandten hat der Kaiser beide Gesuche abgelehnt", [(979, 986)]),
  ("In der Sache der Erben könne, als einer bloßen Gnadensache, keine Verwendung stattfinden; auch die Verwendung des Gesandten zu Petersburg bei Lebzeiten des Fürsten blieb unberücksichtigt", [(987, 995)]),
  ("Bethusys Antrag sei unzulässig, da Artikel 18 des Traktats vom 3. Mai 1815 nur Gutsbesitzer begünstige, deren Besitzungen die neue Grenze durchschneidet; seine liegen weit getrennt in verschiedenen Provinzen", [(999, 1008)]),
  ("Hätte die russische Regierung dem Gesuch stattgegeben, hätte die preußische dagegen Einspruch tun müssen", [(1009, 1014)]),
  ("Da der Aufenthalt der Bittsteller nicht näher bekannt ist, stellt das Ministerium dem Minister die weitere Verfügung anheim", [(1018, 1024)])],
 [(972, 'Das leztere', "'der letztere'"),
  (974, 'von zwischen', "word order garbled; with line 975 'aus dem Vertrage zwischen Preußen und Rußland vom'"),
  (983, 'ganzen ergebenst mitgetheilen', "probably 'ganz ergebenst mitzutheilen'"),
  (985, 'des Gesuch', "'das Gesuch'"),
  (986, 'bei der', "probably 'beider'"),
  (992, 'Sachschlung', "garbled; probably 'Unterstützung' or 'Empfehlung'"),
  (997, 'und gar nicht erst', "an insertion from the margin, which belongs to the passage on Bethusy's properties"),
  (1009, 'unses[?]', "probably 'nichts' ('nichts desto weniger')"),
  (1016, 'behörigkeit', "with 'Un¬': the impropriety of the request; the exact word is unsure"),
  (1017, 'nicht meine [...] Signe[?] EE.', "garbled"),
  (1025, 'Blin', "probably 'Berlin'"),
  (1026, 'In Alu[?]s.', "garbled")]),
30: (S,
 "The minister of the interior von Schuckmann to the foreign ministry, Berlin, 19 May 1820 (received 28 May; filed with Hoffmann's and Balan's marks). He has learned from the letter of the 13th of the requests the late Prince's heirs and Count Bethusy made to the Russian government through Prince Eugen of Württemberg, and of the refusal. He agrees that Bethusy's claim to free traffic between his properties in Silesia and the Kingdom of Poland is inadmissible even under the treaty of 3 May 1815, and has told Bethusy so, pointing to article 18 and adding that had Russia granted it, this government would have objected.",
 [("Schuckmann ist durch das Schreiben vom 13. von den Anträgen der Erben des verstorbenen Fürsten und des Grafen Bethusy und der ablehnenden Antwort der russischen Regierung unterrichtet", [(1030, 1035)]),
  ("Er stimmt zu, dass Bethusys Anspruch auf freien Verkehr zwischen seinen Besitzungen in Schlesien und dem Königreich Polen auch nach dem Traktat unzulässig ist", [(1035, 1040)]),
  ("Er hat dies Bethusy unter Verweis auf Artikel 18 eröffnet, mit der Bemerkung, dass die preußische Regierung Einspruch erhoben hätte, wenn Russland stattgegeben hätte", [(1040, 1044)]),
  ("Das Schreiben wurde zu den Akten genommen", [(1052, 1057)])],
 [(1035, 'Was der war dem', "probably 'Was den von dem'"),
  (1052, 'R[...] Balan', "the docket naming Balan; the title before the name is lost")]),
}


def main():
    import unitlib
    import read_letters as RL              # also sets stdout to UTF-8
    unit = unitlib.one_unit('iiihamdaiiinr12765')
    corpus_lines = open(os.path.join(UNIT_DIR, 'corpus.txt'), encoding='utf-8').read().split('\n')
    # corpus line -> the line number the document page shows (markers skipped)
    shown, doc_of, cur, k = {}, {}, None, 0
    for i, l in enumerate(corpus_lines, 1):
        if l.startswith('[DOC '):
            cur, k = l[5:-1], 0
        elif l.strip() and not l.startswith('[PAGE '):
            k += 1
            shown[i] = k
        doc_of[i] = cur

    corpus = RL.Corpus(unit) if hasattr(RL, 'Corpus') else None
    out, problems = {}, []
    for lid, (leg, notes, claims, doubtful) in sorted(R.items()):
        lid = str(lid)
        cl = []
        for st, ranges in claims:
            ls = []
            for a, b in ranges:
                for n in range(a, b + 1):
                    if n in shown:
                        if doc_of[n] != lid:
                            problems.append(f'doc {lid}: line {n} belongs to doc {doc_of[n]}')
                        ls.append(shown[n])
            if not ls:
                problems.append(f'doc {lid}: claim with no lines: {st[:40]}')
            cl.append({'statement': st, 'lines': ls})
        dw = []
        for n, word, note in doubtful:
            if doc_of.get(n) != lid:
                problems.append(f'doc {lid}: doubtful line {n} is in doc {doc_of.get(n)}')
            elif word not in corpus_lines[n - 1] and not any(
                    w in corpus_lines[n - 1] for w in word.split()[:1]):
                problems.append(f'doc {lid}: "{word}" is not on line {n}: {corpus_lines[n - 1][:60]}')
            dw.append({'line': shown.get(n, 0), 'word': word, 'note': note})
        # The paid claim check (read_letters.py --verify, run 2026-10-01): where
        # it found a statement overstated or unsupported, the verdict and its
        # reason travel with the statement, as in the other units' readings.
        vf = os.path.join(ROOT, 'cache', f'reading-{unit.slug}', unit.pad(lid) + '.json')
        if os.path.isfile(vf):
            verdicts = {c.get('statement'): c for c in
                        ((json.load(open(vf, encoding='utf-8')).get('verify') or {})
                         .get('claims') or [])}
            for c in cl:
                v = verdicts.get(c['statement'])
                if v and v.get('verdict') != 'supported':
                    c['check'], c['why'] = v['verdict'], v.get('reason', '')
        rec = {'letter': lid, 'legibility': leg, 'notes': notes, 'claims': cl,
               'doubtful_words': dw}
        if corpus is not None:
            rec['read_against'] = RL.source_hash(corpus, lid)
        out[unit.pad(lid)] = rec
    if problems:
        sys.exit('NOT WRITTEN\n' + '\n'.join(problems))
    with open(os.path.join(UNIT_DIR, 'reading.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(len(out), 'documents ->', os.path.join(UNIT_DIR, 'reading.json'),
          '| claims', sum(len(v['claims']) for v in out.values()),
          '| doubtful words', sum(len(v['doubtful_words']) for v in out.values()),
          '| hashed' if corpus is not None else '| NOT hashed')


if __name__ == '__main__':
    main()
