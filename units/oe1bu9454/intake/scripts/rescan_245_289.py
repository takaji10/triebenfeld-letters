# -*- coding: utf-8 -*-
"""Oe 1 Bü 9454, letters 245 and 289: the archive's new scans and the editor's new transcriptions (2026-10-07).

    python units/oe1bu9454/intake/scripts/rescan_245_289.py            # check only
    python units/oe1bu9454/intake/scripts/rescan_245_289.py --write    # once

The editor had asked the archive for better images of letter 245 (both pages)
and letter 289 (review/oe1bu9454/rescan_request_final.md). They came, with a
new machine reading of each page corrected by the editor, in
Downloads/"Oe 1_Bue 9454 Nr. 289, Nr. 245" (NEW). This script is the record
of what was done with them; it is not to be run again once written.

Images. Letter 245 keeps its page ids (0455_a, 0456_a): the new scans replace
the old files. Letter 289 was the right half of capture 0522 and the left
half of capture 0523 (pages 0522_a2, 0523_a1); the new scans show each page
whole and the editor names them 0522_b and 0522_c, so those are its page ids
now. The old processed images are moved to processed/_superseded/.

Text. Each page below is the text as it now stands in corpus.txt. It was made
line by line from three things: the text that stood in the corpus (which had
had every correcting pass of this holding: names, titles, expansions), the
editor's new transcription, and the new scan itself, enlarged and read
through. Where the two transcriptions differ, the scan decided; where the
scan did not let me decide, the reading both share stands, or the editor's
new one with its mark of doubt. Nothing was completed by guess.

Left as found, and logged in review/oe1bu9454/unresolved.md:
- 245: "praeciat" / "Praeciat" (the letters as read, twice; a term for the
  son's portion of 100,000 rt, perhaps Praecipuum); "Inträgen" on page 1,
  which page 2 writes "Intrigen"; the word after "Intresse" at the torn end
  of page 2, line 2; "aus der Casse" in an insertion above the line on page
  2, where one word between is struck out and not transcribed.
- 289: "zu bring" (perhaps "zu Brieg"); "bitte" in "so schrecklich bitte"
  (perhaps "litte"); "Circa 112/m" (perhaps "mit"); the name "Heneberg[?]".
The pencil date at the foot of 289's first page reads "5. Mai 1815."; the
editor's file had "3. Mai" and put it at the head.
"""
import io
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.dirname(os.path.dirname(UNIT))
NEW = r'C:\Users\Tersnaus\Downloads\Oe 1_Bue 9454 Nr. 289, Nr. 245'
RAW = r'J:\Documents\Archive\Genealogy\References\Hohenlohe-Zentralarchiv Neuenstein\Oe 1_Bü 9454\processed'

P245_1 = '''245
(des Fürsten Staats Kanzler v. Hardenberg)
Durchlauchtigster Fürst
Gnädigster Fürst und Herr
Ewr Hochfürstliche Durchlaucht soll ich beigebogenes Schreiben des Herrn Fürsten zu Hohenlohe allersubmiße[...]
überreichen, und Allerhöchst dieselben zugleich um die höchst gnädige Erlaubniß bitten, Euer Hochfürstliche
Durchlaucht die drükendeste Noth des Fürsten zu schildern und dabey einen Plan zur Rettung desselben
und zur Abhülfe seiner Leiden Ewer Durchlaucht zu Füßen zu legen.
Von jeher war der Fürst von Ingelfingen Ewr Hochfürstliche Durchlaucht treuester Anhänger und Verehrer
dieser, ohne eigene Schuld bloß durch Nachgiebigkeit gegen fremden Einfluß auf sein wohlwollendes Gemüth
unglücklich gewordene Mann, wirft sich Ewr Durchlaucht in die Arme, er bittet ihm vor der Chicane des Medi¬
zinalrathes Cosmar zu schüzzen, die weiter nichts beabsichtiget, als daß der gute Fürst in seinem Alter
hungern und im Elende umkommen soll.
Ein Vermögen von mehr als zwey Millionen Rttlr an Werth betragen die Schlawenschitzer, Lassowitzer und
Oppurger Güter, welche laut der Sub A in Abschrift, beigebogenen Urkunde von Sr Majestät 1799 als
Majorat bestättiget sind, und die heute in den bedrängtesten Zeiten, nach den sub B beigefügten Nach¬
weiß dennoch 79500 rttlr Ertrag gewähren. Von diesen nahmhaften Gütern, soll der Fürst als
Majorats Herr die Revenuen genießen. Allein durch die nur denklichsten Kunstgriffe hat sich der M R Cosmar
sowohl in die Majorats Güter als in den Nachlaß der verstorbenen Fürstin Sackin einzunisten gewußt, so daß er über
alles wie über sein Eigenthum gebietet alle Revenuen einzieht und Niemanden davon einen Heller giebt.
Er heißt Testa: Executor — was konte aber die Fürstin Sacken von Todes wegen verordnen? Sie war von diesen Gütern
und zwar nur Theilweise bloße Advitalitaets besizzerin. Die von Sr Maj[estät]. Sanct[ionirte] Acte A bestimt ja alles, der geschied[en?]
Fürstin jezt verehelich v Sacken gehört, die sämt. Güter. Nach ihrer Trennung cedirte sie all ihr Erbe gutwillig an ihren gekrän[...]
Eheherrn, dem Fürsten v Hohenlohe und der Fürst stiftete daraus das Fidei Commis welches Sr Maj Sanctionirten. Wie konte
also die Fürstin Sacken noch einen Executor Testamenti einsezzen, über ihren baaren Nachlaß konte Sie wohl testire
allein da sie gröst entheils alles ihren Lieblinge dem Prinzen Adolph vermacht hat, so verschwindet jeder Rechts Grund
aus welchem sie sich noch viel weniger ihr Busenfreund Cosmar in die Angelegenheiten der Majorats Güter mischen dürfte
um sich aber in diese Angelegenheiten, troz der entgegenstehenden rechtlichen Schrankken dennoch einzudringen, darin nach
Willkühr zu schalten, und über die Einkünfte ohne Verantwortung, wie über sein Eigenthum zu gebieten, hat der
M. Cosmar das verwegenste Wagestück eines entschloßenen Rabulisten unternommen. Er entwarf den hier sub C. beilie¬
gende, weit schichtigen Transact zu einer Zeit wo die Fürstin v. Sacken, wann sie ja noch lebte, den Inhalt und die folgen unmöglich
übersehen konte, da sie in den lezten Zügen lag, und in günstigsten Falle schon an Lebens Kräften so geschwächt war, daß sie
das weitschichtige Acten stück, statt der Unterschrift nur mit 3 Xen unterzeichnete.
Dieser Transact ist der Inbegrif aller Inträgen. Es sind darin so viel Schulden und Forderungen, welche die Fürstin Sackin zu fordern
hätte, aufgeführt, die alles übersteigen, und die in der Stiftungs Urkunde nie gedacht waren. Der Fürst hat darüber schon
wie die abschrift beilage sub D zeigt, bey dH. J[ustiz] M[inister] v Kircheisen Exc. Erwähnung gethan. In deßen Antwort sub E
wird aber darüber geschwiegen. Ferner besagt dieser Transact, daß Cosmar über alle Einkünfte der M Güter
gebieten kan, und Niemand Rechnung legen darff — Ob je ein zweiter Test: Executor von dieser Art in der
Geschichte aufzufinden ist, bezweifle ich, aber eben das wegen konte die Fürstin bey fertigung der 3 Xen, unmögl. mehr eines gesunden
Verstandes genießen, den der Transact geht darauf hinaus dem Monarchen und alle Gläubiger des Fürsten zu betrügen, dem Fürsten
aber besonders um Ehre und alles zu bringen, und dieses konte die verstor: Fürstin nicht wollen! Sie wüste zu gut was der Fürst um
ihrer Tochter willen gedultet hat. Es konte also diesen Machwerck, nur die unbegränzteste Bosheit zum Grunde liegen
zur Vollendung dieses, der Sanctionirten Acte von Jahr 1799 ganz widerstreitenden fameusen Transactes, wußte man sogar dem
Fürsten durch die schandlichsten Vorspiegelungen zur Genehmigung zu bewegen — Jezt hatte Cos[mar] seiner Meinung nach gewonnen Spiel
er sezte sogleich seinen unerfahrenen Minorennen Sohn zum Administrator der Güter ein. Bezog mit diesen alle Revenuen zahlte
weder Interesse noch Capital, und legte troz allen Anmahnungen des Brieger O[ber]. L[andes]. G[ericht]., welches er nur mit trozzigen sarkastischen
Antworten abwies, auch keine rechnung — Der Fürst soll jährl. nach das 1ste Abkommen 24/m rt. und deßen Sohn Aug: jezt F[ürst]. zu Öhringen
18000 rt. beziehen, auch solten lezten gleich nach dem Tode der Fürstin Sackin 100/m rt als ein praeciat zur Berichtigung auf seinen Schulden
ausgezahlt werden. Es sind aber 3 Jahre verfloßen, und der alte Herr hat mehr nicht als 2500 rt. der Sohn Fürst Aug: aber nicht
einen Groschen erhalten, wo bleiben also die Revenuen von jährl. 79500 rt. wo die Möglichkeit den Ersaz von Cos: zu erlangen?
Aber hier geht der Plan des Cosmars am Tage aus — Was ihm auch immer von dem Fürsten gesagt wird er leidet
alles ohne Erröthen — Das Schreiben des Fürsten an dH. Justiz Ministers Exc. [...] davon ein Beweis. Die Antwort Sr Exc. aber'''

P245_2 = '''läßt die Entschuldigung des Cosmars vermuthen — In der That duldet dieser Mensch jede Erniedrigung, um nur seinen Plan nicht aufzugeben, ud seine Beute nicht,
laßen zu müßen. Die Grundlage des Cosmars Plans beruhet auf das Capital von 300/m rt. welches die Cur[ische] Erben am Fürsten zu fordern haben, und welches mit Inbegrif der Intresse v[?]
1805 — 426000 rt. beträgt. Des Königs Maj. haben die Schuldpost garantirt, und die ehemalige Fürstin Hohenlohe hat das Instrument als selbst schuldnerin, mit dem Fürsten zugl. unterschrieb[...]
In den mehrerwehnten Transact von 1811 hat aber der Fürst sich anheischig gemacht dieses Capi: nebst Zinsen aus seinen Mitteln zu bezahlen, und die vormahlige Fürstin jezt verehe¬
lichte F v Sakkin von der Bezahlung zu befreien — Ein doppelter Unsinn — erstens weil man den Fürsten eine so ansehnliche Zahlung zumuthet, der nicht zehn, geschweige den
hunderttausende zu bezahlen hat — zweitens, weil man die Rechte dritter intereßirender Personen, ohne ihre Einwilligung glaubte aufheben zu können, — die verstorbene
Fürstin dachte wohl zu edel, als daß sie am Rande des Grabes noch es darauf hatte anlegen sollen, ihren Souverain und mehr andere Menschen um viel hunderttausend rt zu
betrügen. Niemand kan hier das Getriebe eines eigennüzzigen Chicaneurs verkennen, dem bisher alles gelungen war — Cosmar wußte daß die Cur[ische] Erben schon ein Con¬
tumazial Urtheil für sich hatten, in welchem der Fürst diese nahmhafte Summa zu bezahlen verurtheilt war, er wußte daß bey dem Fürsten, den er schon 3 Jahre hatte hungern
laßen, kein Gegenſtand einer Execution aufzufinden ſey — Er ſchloß hieraus, daß der Monarch nun von den Curische Erben zur Bezahlung würde angegangen
werden; und so meinte er, daß des K[önigs]. Maj nach dieser metamorphose aufgebracht, sich von der Sache los sage, und aus Verdruß das 1799 gestiftete
fidei Commis. welches nur unbeschadet des allerhöchsten Interesse und jedes dritten sanctionirt wurde, gänzlich aufheben solte. Dann konte nach seiner Meinung die
ehemalige Fürstin jezzige Gr. Sakkin wieder auftreten, die Güter reclamiren, den armen Fürsten von allem austreiben und verhungern laßen — dann erst wäre
Cosmars Plan völlig gelungen, und sein Lohn würde gewiß Fürstlich gewesen sein —
Ewr Hochfürstl. Durch. nur können diesen Intrigen bald abhelfen und dem guten Fürsten aus den Klauen des Cosmars retten — Schon ist mit den Mandatarien
Der Cur[ische]. Erben ein Übereinkommen getroffen nach welchen diese für die ganze Forderung von 426000 rt. — 112000 nehmen, über alles quittiren, und sämtl.
Documente heraus geben wollen — Eben so ist auch schon mit allen andern Creditoren, ein Abkommen getroffen, daß sich diese mit einer jährl. abschl. Zahlung
von 12000 rt, welche der Fürst aus den ihm zustehenden Majorats Revenuen, angewiesen hat / die aber Cosmar troz allen Aufforderungen selbst vom
Brieger O[ber]. L[andes]. G[ericht]. nicht zahlen will / begnügen wollen —
Es kommt nur darauf an, daß Ewr Hochfürstl Durchlaucht einen Vorschuß von 112/m rt zur Bezahlung der Cur[ische] Erben, und wann auch nur auf eine kurze
Zeit gnädigst bewilligen, beſonders aber den von Cosmar ſo böslich geſchmiedet, Transact von 1811, der in der Art der Ausfertigung mehr als
verdächtig, dem von des K[önigs]. M[ajestät]. selbst Sanct[ionirten] Act von 1799 zuwider, mit den wohlerworbenen Rechten von dritten, unvereinbarlich kurz nichts
als ein vermessenes Attentat eines ränkevollen Fremden, gegen das Glück des Fürsten ist, verdienten maßen aufheben, dem
Cosmar aber von allem aus scheiden, und ihm zur strengsten Rechnungslegung anhalten laßen.
Der Vorschuß von 112000 rt kan, wofür auch ich, wann es verstattet wird, mit einer Caution von 60000 rt. hafte, in der kürzesten Zeit
Ja in mancherlei Art getilgt sey.
würde nicht eine Abschlagliche Zahlung, wie solche sub B aufgeführt mit 25000 rt. jährlich angenommen werden, so könte man einen Theil
von den 100000 die der Fürst August als Praeciat erhalten soll dazu vor der Hand Adhibiren. Nur muß vor allen der selbst dem Fürsten
so entehrende Transact von 1811 aufgehoben, sey und ein ehrlicher Sachkundiger Administrator, in Nahmen des K[önigs]. M[ajestät]. weil Allerhöchst
derselbe wegen der Garantie dabey interessirt ist angestellt werden. Dan steht der Tilgung des Vorschußes von 112/m nichts entgegen
Noch bemerke ich allsubmißest daß Cosmar über 43000 rt von den Geldern, welche der Fürst zu seinem Unterhalt beziehen, sollen
hinter sich hat, und welche der Fürst den Gemein Creditoren im Vergleich anwies — die aber Cosmar durchaus nicht zahlen will —
Noch gegen 60000 rt fabriq Waaren in den Magazinen voräthig — diese aber bleiben als ein Betriebs Capital anzusehen — indes
sind dies redende Beweise von der reichaltigkeit der Güter wovon ein Chicaneur alles zieht, hinter sich zur Ausführung
seines Plans behält, und inzwischen dem guten Fürsten mit seinen Umgebungen hungern läst —
Anführen muß ich hier noch daß ich die ehemals dem Fürsten aus der Casse vorgeschoßene 35000 rt zur Amortisirung mit aufgeführt habe.
Von Ewr Hochfürstl. Durch. stets gegen den H. Fürst zu Hohenlohe bewiesenes Wohlwollen hoffe ich die Erhöhrung meiner
submissesten bitte, wornach ich auf allergehorsamst flehe, über die Lage des Fürsten, über alle seine Leiden welche er durch
den p Cosmar dulden muß, ja daß alles hier wahr und gewiß geschildert ist, einen Bericht des Ober Land Gerichts zu Brieg
wohin dH. J[ustiz]. Minist. Excellenz dem Hrn Fürsten selbst gewiesen, zu erfordern, aus welchen sich mehr am Tag legen und
die drückende Noth des Fürsten bewiesen werden wird.
In tiefster Ehrfurcht ersterbe
E[wr]. H[ochfürstliche]. Durchl.
Wien den 20ten Octobr.
1814
treu unterthänigster Knecht
v Triebenfeld'''

P289_1 = '''289
Hochwohlgeborner Herr
Hochverehrter Herr Geheimer Cabinets Rath!
Euer Hochwohlgl. wird es gewiß nicht unbekannt seyn, daß die Churischen Erben
an den F. v. Hohenlohe eine Forderung von 300/m rt. haben, das Schuld Instrument
darüber ist vom Fürsten und deßen geschiedener Gemahlin ausgestellt und
von des höchst Seel. Königs Majestaet als selbst Schuldner unterschrieben, auch
sind aus den Königl. Cassen die Zinsen biß 1806 dafür bezahlt worden. Hier
auf glaubten die Curischen Erben ihr Recht zu gründen, um diese Summe
die heute mit den Intressen 426/m rt. beträgt vom fiscus fordern zu dürfen
und entamirten gegen diesen den Prozeß. Sr. Majestaet hatten hierauf vor
Jahr und Tag erklärt
"daß Sie mit der Sache nichts zu thun haben wollten, sondern
Sich gänzlich davon los sagten."
dies bewog den Fürsten / obgleich die Summe für des höchst Seel. Königs
Majestaet zuerst negozirt worden / mit den Cur. Erben einen
Vergleich einzuschreiten, nach welchen leztere Circa 112/m rt. zufrieden sein
und über die ganze Schuld Post quittiren wollten.
während Sr Majestaets Anwesenheit hierselbst, aber gaben allh. dieselben
ganz der erstern Erklärung entgegen, denen Erbinnen die Versicherung
daß allhst Sie Sich die Sache bey Höchst dero Rückkunft in Berlin würden
vorlegen laßen, und sich dann weiter erklären.
auf den Grund dieses Allerhöchsten Bescheids, hat der Justiz rath Heneberg[?]
in Berlin dem Curischen Mandatarius Eberhard zu bring angedeutet,
sofort alle Vergleichs Verhandlungen abzubrechen, weil fiscus nun die
ganze Bezahlung leisten würde und leisten müsse. Mich hatte der Fürst
hierher gesandt um die Sache zu beenden und einen Vorschuß
von 112/m rtl. gemäß Vergleich zu erbitten, der aus den Güter in
4 Jahren wieder remboursirt werden sollte. Da nun aber die
Curischen Erben ihr Wort auf die Ihnen gemachte Hoffnung zurück
gezogen, so bin ich außer Stande gesezt die Sache am erwünschten
Ziele zu bringen und Sr Majestaet ein Capital von 426/m rt. zu
erhalten. Ich würde auch Ehrfurchtsvoll verstummen, wenn
nicht mein Fürstl. Mandant so schrecklich bitte, denn auf den Grund
dieser Schuld administrirt der Medicinal Rath Cosmar die sämtl.
Majorats Güter und gibt keinem Menschen davon schon seit 4 Jahren
wenig oder nichts legt keine Rechnung und niemand weiß wo die
revenuen von diesen Nahmhaften Gütern bleiben. Ich muß daher
Nahmens meines H. Mandanten um allerhöchste Gnädigste Categorischen
Bescheid bitten.
welche an 80/m rt jährlich betragen
sollen den der Fürst hat seit
4 Jahren statt 96/m rt nur 2500 rt
überhaupt erhalten, und
hungert mit seinen Umge¬
bungen
+ ob Sr Majestaet würklich gemeint sind die Schuld von 426/m rt.
an die Curischen Erben zu bezahlen, oder ob der Fürst die Sache
abmachen und sich wie es jezt noch sein kann zu vergleichen
bemüht sein!
Im ersten Fall würde ich unterthänigst bitten, daß wenn Sr Majestaet
die Schuld bezahlen wollen, und sich als Selbst Schuldner dazu bekennen
ein allerhöchster Befehl gegeben würde,
"daß die Cosmarische Administration sofort aufgehoben und von
Ihm alle gelder Reponirt werden mögten"
5. Mai 1815.'''

P289_2 = '''Im 2ten Falle aber würde ich allergehorsamst bitten, daß
Sr Majestaet Sich sogleich von der ganzen Sache gemäß Ihres
erst gegebenen Wortes, welches doch stets heillig bleiben muß,
los sagten, wornach ich dann den Vergleich mit zuversicht
Obzuschliesen hoffen dürfte. Mein H. Mandant verliert
zwar im leztern falle. Er will aber nicht seinen Monarchen
erzürnt wissen, den 426/m rt ist eine Bedeutende Summa
die Sr. Majestaet erhalten wird, und daher rechnet der
Fürst drauf, daß Sr Majestaet um die Summa, um welche
sich mit den Curischen Erben verglichen werden wird,
allergnädigst vorzuschießen, befehlen mögten, die aber
nach dem beigebogenen Plan in wenig Jahren gewiß
wenn besonders die
Güter für Königl.
Rechnung sogleich in
Administration
genommen werden.
u. reel zurückgezahlt werden kann, nach welchen
dann des Königs Majestaet auch nicht einen Groschen Verlieren
sondern nach meinem Plan selbst eine alte Schuld
von 35000 rt. retten und sich in allen 461000 rt erhalten.
"Ewr Hochwohlg. geruhen diese Sache zu beherzigen stellen
solche Sr Majestaet vor ud bewürken für mich die Cate¬
gorische Erklärung des Monarchen, damit jeder
daß seine erhält und der Fürst vom Untergang
den ihm Cosmar bereiten würde gerettet
werde."
bemerken muß ich hier noch ganz gehorsamst daß das
Brieger Ober Landes Gericht alles was ich gesagt, schon in
einem Von dem Fürsten Staats Kanzler erforderten
Bericht bethätiget hat, worüber sämtl. Acten
Sr Durchl. vorliegen.
Die gröste Verehrung ist es in welcher ich verharre
Ew Hochwohlgeboren
Wien d 5ten May 1815
ganz gehorsamster
v Triebenfeld
an des Hr. Cabinets Rath Albrecht'''

# (document, old page id, new page id, text, old transcription file, new transcription file, new scan, old processed image, new processed image)
PAGES = [
    ('245', '0455_a', '0455_a', P245_1, '0722_Oe 1_Bue 9454_0455_a.txt', '0722_Oe 1_Bue 9454_0455_a.txt',
     r'Oe 1_Bü 9454 Nr. 245\Oe 1_Bü 9454_0455_a.jpg', 'Oe 1_Bü 9454_0455_a.jpg', 'Oe 1_Bü 9454_0455_a.jpg'),
    ('245', '0456_a', '0456_a', P245_2, '0723_Oe 1_Bue 9454_0456_a.txt', '0723_Oe 1_Bue 9454_0456_a.txt',
     r'Oe 1_Bü 9454 Nr. 245\Oe 1_Bü 9454_0456_a.jpg', 'Oe 1_Bü 9454_0456_a.jpg', 'Oe 1_Bü 9454_0456_a.jpg'),
    ('289', '0522_a2', '0522_b', P289_1, '0828_Oe 1_Bue 9454_0522_a2.txt', '0828_Oe 1_Bue 9454_0522_b.txt',
     r'Oe 1_Bü 9454 Nr. 289\Oe 1_Bü 9454_0522_b.jpg', 'Oe 1_Bü 9454_0522_a2.jpg', 'Oe 1_Bü 9454_0522_b.jpg'),
    ('289', '0523_a1', '0522_c', P289_2, '0829_Oe 1_Bue 9454_0523_a1.txt', '0829_Oe 1_Bue 9454_0522_c.txt',
     r'Oe 1_Bü 9454 Nr. 289\Oe 1_Bü 9454_0522_c.jpg', 'Oe 1_Bü 9454_0523_a1.jpg', 'Oe 1_Bü 9454_0522_c.jpg'),
]


def main():
    write = '--write' in sys.argv
    sys.stdout.reconfigure(encoding='utf-8')
    cp = os.path.join(UNIT, 'corpus.txt')
    lines = io.open(cp, encoding='utf-8').read().split('\n')
    rename = json.load(io.open(os.path.join(UNIT, 'scan_rename_map.json'), encoding='utf-8'))
    decisions_p = os.path.join(UNIT, 'scan_decisions.json')
    decisions = io.open(decisions_p, encoding='utf-8').read()
    for doc, old_id, new_id, text, old_txt, new_txt, scan, old_img, new_img in PAGES:
        new = text.split('\n')
        i = lines.index('[PAGE %s]' % old_id)
        j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith(('[PAGE ', '[DOC ')))
        d = max(k for k in range(i) if lines[k].startswith('[DOC '))
        assert lines[d] == '[DOC %s]' % doc, (lines[d], doc)
        old = lines[i + 1:j]
        same = sum(1 for a in new if a in old)
        print('letter %s, page %s -> %s: %d lines were there, %d now; %d lines unchanged' % (doc, old_id, new_id, len(old), len(new), same))
        assert os.path.isfile(os.path.join(NEW, scan)), scan
        staged_old = rename[old_img]
        staged_new = staged_old.replace(old_id, new_id)
        if write:
            lines[i:j] = ['[PAGE %s]' % new_id] + new
            t = os.path.join(UNIT, 'transcriptions')
            if old_txt != new_txt:
                os.remove(os.path.join(t, old_txt))
            io.open(os.path.join(t, new_txt), 'w', encoding='utf-8', newline='\n').write(text + '\n')
            # the images: the archive's processed folder, then pages/ under the staged name
            sup = os.path.join(RAW, '_superseded')
            os.makedirs(sup, exist_ok=True)
            if os.path.isfile(os.path.join(RAW, old_img)):
                shutil.move(os.path.join(RAW, old_img), os.path.join(sup, old_img))
            shutil.copyfile(os.path.join(NEW, scan), os.path.join(RAW, new_img))
            pages = os.path.join(ROOT, 'pages')
            if os.path.isfile(os.path.join(pages, staged_old)):
                os.remove(os.path.join(pages, staged_old))
            shutil.copyfile(os.path.join(NEW, scan), os.path.join(pages, staged_new))
            web = os.path.join(ROOT, 'site', 'assets', 'scans', staged_old)
            if os.path.isfile(web):
                os.remove(web)                      # made again by make_scan_derivatives.py
            rename = {(new_img if k == old_img else k): (staged_new if k == old_img else v) for k, v in rename.items()}
            assert decisions.count('"%s"' % staged_old) == 1, staged_old
            decisions = decisions.replace('"%s"' % staged_old, '"%s"' % staged_new)
    if write:
        io.open(cp, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
        # scan_rename_map.json and scan_decisions.json are CRLF and in the archive's order: the two names of
        # letter 289 were changed in place by hand (the first run of this script sorted and rewrote them,
        # and they were restored from git).
        io.open(decisions_p, 'w', encoding='utf-8', newline='\n').write(decisions)
        print('written')


if __name__ == '__main__':
    main()
