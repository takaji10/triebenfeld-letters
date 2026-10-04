# -*- coding: utf-8 -*-
"""Corrections to the Polish judgment (document 6) and the ministry's draft
(document 3) of III. HA MdA, III. Nr. 12366, 2026-10-04.

    python units/iiihamdaiiinr12366/intake/polish_corrections.py            # check only
    python units/iiihamdaiiinr12366/intake/polish_corrections.py --write    # once

The editor asked for the Polish and the rest of the text to be gone through.
Every page was read against its scan. A row is here only where the scan is
plain and the corrected form is a word of the Polish (or French) of the time
that fits its sentence: both, not one. The scribe's own spelling is kept (y
for j, "Osmsetnego", "Xięciu", missing accents), and so are the words the scan
does not settle; those are in unresolved.md.

Rows: (text as transcribed, text as on the scan, what it means or why). Each
`old` must stand exactly once in its document. Most rows change more than one
word, so they are applied here and logged in transcription_decisions.csv by
this script, not through the single-word tool.

In this hand k is written like "li" or "lu" and R like "K": that is behind
"litore" (ktore), "politadanych" (pokładanych), "kządu" (Rządu).
"""
import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
SLUG = 'iiihamdaiiinr12366'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROWS = {
 '6': [
  ('Obani', 'Obecni', '"Present": the heading over the list of judges'),
  ('PProkurator', 'Prokurator', 'a flourished P, not two'),
  ('przy Ulicey Jozefi nie odbywaiącego', 'przy Ulicy Jozefinie odbywaiącego', 'the street name, broken over a line: "Jozefi-nie"; the court sits there, it does not "not sit"'),
  ('Tysiącnego Osmsetnego dwiedziestego', 'Tysiącznego Osmsetnego dwudziestego', 'the year 1827 written out'),
  ('zamieszkałemi Powodaniu', 'zamięszkałemi Powodami', '"plaintiffs"; the catchword on 0017 is "zamię"'),
  ('Hypoteki Dobr Trąbczyna i przy', 'Hypoteki Dobr Trąpczyna i przy', 'the scribe writes p here as everywhere in this document'),
  ('Czterdziestu dwuch Tysiący Talarów w Kurantu Patrona', 'Czterdziestu dwuch Tysięcy Talarow w Kurant u Patrona', '"42,000 thalers in currency, at the advocate ...": "u Patrona", with whom they chose their domicile'),
  ('Chrystowskiego Ptron Trybunału zdnegiey strony', 'Chrystowskiego Patrona Trybunału z drugiey strony', '"of the second part"'),
  ('dwanastego Roku', 'dwunastego Roku', 'the year 1812 written out'),
  ('pozostałego w do zakypotekowaney', 'pozostałego co do zahypotekowaney', '"as to the sum mortgaged"'),
  ('summy stu Dwadziesta Tysięcy', 'summy stu Dwudziestu Tysięcy', '120,000 written out'),
  ('podobniez a Patrona', 'podobniez u Patrona', '"likewise at the advocate"'),
  ('ztrzeciey strony', 'z trzeciey strony', '"of the third part"'),
  ('Excesscyą niewaznosci', 'Excepcyą niewaznosci', '"the objection of nullity"; "Excepcyą" twice more on the page'),
  ('Z powodka nie mogła w Pozwic', 'Ze Powodka nie mogła w Pozwie', '"That the plaintiff could not, in the summons"'),
  ('naznacać im zamięszkania, iak to litore sobie', 'naznaczać im zamięszkania, iak to ktore sobie', '"than that which they chose"'),
  ('na tey zasadzic Excepcyą te iaku beż zawadną oddala iąc w Rozpoznancie', 'na tey zasadzie Excepcyą te iako bez zasadną oddalaiąc w Rozpoznaniu', '"on that ground dismissing this objection as unfounded; in considering"'),
  ('wiarogrodnym abłem', 'wiarogodnym aktem', '"by no credible document"'),
  ('bo pokłtadane', 'bo pokładane', '"the certificate produced"'),
  ('nie przynosć dowodu, gdy z nie tylko', 'nie przynosi dowodu, gdyz nie tylko', '"brings no proof, since not only"'),
  ('udowodnieby się dato', 'udowodnicby się dało', '"could be proved"'),
  ('roztrząsnieniu politadanych', 'roztrząsnieniu pokładanych', '"the documents produced"'),
  ('własniscią niegdy', 'własnoscią niegdy', '"property"'),
  ('za nalizenie do Powstania pozia dane były', 'za nalezenie do Powstania posiadane były', '"for belonging to the uprising, were possessed"'),
  ('z dały dzewiątego sierpnia', 'z daty dziewiątego sierpnia', '"dated the ninth of August"'),
  ('dziewiącdziesiątego', 'dziewięcdziesiątego', 'the year 1796 written out'),
  ('i ż takiego to', 'i z takiego to', '"and from such a deed"'),
  ('zmianie kządu, Kommissya Kządząca', 'zmianie Rządu, Kommissya Rządząca', '"change of government, the Governing Commission"; "Rządu" is so read lower on 0021'),
  ('dwudziesto pierwszego', 'dwudziestego pierwszego', 'the 21st written out'),
  ('zamęscia Dąbska,', 'zamęscia Dąbską,', 'the accusative, as "Miączyńską" beside it'),
  ('Czynownie inne', 'Czynow nie inne', '"from all these acts no other consequence follows"'),
  ('Darowizny Zięciu Hohenlohe', 'Darowizny Xięciu Hohenlohe', '"to Prince Hohenlohe"; Zięciu would be "to the son-in-law"'),
  ('Okolicznisci będący do tąd tylko', 'Okolicznosci będący dotąd tylko', '"circumstances ... only so long"'),
  ('do poliąd taz', 'dopokąd taz', '"as long as the same state of things lasted"'),
  ('owcza sowey', 'owczasowey', '"the then (Dąbska)"'),
  ('iaku istniał, w czadzie', 'iaki istniał, w czasie', '"as it existed at the time"'),
  ('warankowego', 'warunkowego', '"conditional (possessor)"'),
  ('Tytulu iego, rownic i Długi przez niego zawągnione', 'Tytułu iego, rownie i Długi przez niego zaciągnione', '"his title, likewise the debts he contracted"'),
  ('obowięzywać', 'obowiązywać', '"to bind"'),
  ('z Blacho Grotowska', 'z Blachow Grotowska', 'her maiden name, as on 0018 and 0019'),
  ('zastaniac się w zaden spodob', 'zasłaniać się w zaden sposob', '"can in no way shield themselves"; the page turn follows'),
  ('Biorąc na Uwagą:', 'Biorąc na Uwagę:', '"Taking into consideration"'),
  ('własnosci nic da się', 'własnosci nie da się', '"cannot"'),
  ('obciązać niały gdyzby', 'obciązać miały, gdyzby', '"were to burden, since otherwise"'),
  ('w stanie opłacie przez obią i trzecią osobę zaciągnątych', 'w stanie opłacić przez obcą i trzecią osobę zaciągniętych', '"able to pay the debts contracted by a stranger and third person"'),
  ('przy własnosci przywłasnosci przywroconych', 'przy własnosci przy własnosci przywroconych', 'the scribe wrote "przy własnosci" twice and underlined the second to cancel it'),
  ('mianowiać Artykuł', 'mianowicie Artykuł', '"namely article"'),
  ('gdyz takowey do Dobr', 'gdyz takowy do Dobr', '"since it (the treaty)"'),
  ('i na powrotim zwroconych', 'i napowrot im zwroconych', '"and returned to them again"'),
  ('zastosować się nic da', 'zastosować się nie da', '"cannot be applied"'),
  ('piątnym Pazdziernika', 'piątym Pazdziernika', '"the fifth of October"'),
  ('Z Rzesza zwazaiąc', 'Z Resztą zwazaiąc', '"Considering, moreover"'),
  ('Krot Jegomość Pruski ustaki raczył', 'Krol Jegomość Pruski ustalić raczył', '"His Majesty the King of Prussia was pleased to establish"'),
  ('do swey własnisci', 'do swey własnosci', '"to his property"'),
  ('nie ma bydz nic ma bydz', 'nie ma bydz nie ma bydz', 'written twice; the scribe underlined the second to cancel it'),
  ('od powiedzialnym', 'odpowiedzialnym', '"answerable"'),
  ('wedle politadanego', 'wedle pokładanego', '"according to the charter produced"'),
  ('wypadgrodzenie', 'wynadgrodzenie', '"in compensation"'),
  ('na tych samych za sadach oparte', 'na tych samych zasadach oparte', '"resting on the same principles"'),
  ('Obecnym prypadku przyiąwszy rownic tez', 'Obecnym przypadku przyiąwszy rownie tez', '"in the present case, adopting likewise"'),
  ('1. Czterdziesci', 'a Czterdziesci', 'the scan letters the two sums a and b'),
  ('2. Dwadziescia Tysiący Talarow, czyli Sto dwadziescia Tysiący', 'b Dwadziescia Tysięcy Talarow, czyli Sto dwadziescia Tysięcy', 'the scan letters the two sums a and b; "Tysięcy"'),
  ('sponądzonym przy wyciśnienciu', 'sporządzonym przy wycisnieniu', '"drawn up, with the impression (of the seal)"'),
  ('pieczęci Swiadczą', 'pieczęci Swiadczę', '"I certify": one clerk signs'),
 ],
 # the ministry's draft of 11 May 1819: a German writer's French hand, read on
 # enlarged crops. The names stay as the editor wrote them (the scan has
 # "Myaczynska").
 '3': [
  ('Envoyé extraordinaire de Ministre Plénipotentiare de Russie', 'Envoyé extraordinaire et Ministre Plénipotentiaire de Russie', 'the address in the left margin'),
  ('qui M. d’Alopeus Envoyé Extraordinaire de Ministre Plénipotentiare de Sa Majesté', 'que M. d’Alopeus Envoyé Extraordinaire et Ministre Plénipotentiaire de Sa Majesté', '"the note and the memorandum which M. d\'Alopeus, envoy extraordinary and minister plenipotentiary"'),
  ('La soussignée qui croit devrir retracer', 'Le soussigné croit devoir retracer', 'the insertion in the left margin: "The undersigned thinks he should first retrace"'),
  ('la fuite, sur biens furent', 'la fuite, ses biens furent', '"his estates were confiscated"'),
  ('empruntèrent sur en biens fonds', 'empruntèrent sur ces biens fonds', '"borrowed on these lands"'),
  ('en paix d’étranger', 'en pais étranger', '"in a foreign country"'),
  ('elle fute remise', 'elle fut remise', '"she was put back"'),
  ('le Gouvernement de Grand Duché', 'le Gouvernement du Grand Duché', '"du", with "grand" written in above'),
  ('lui on garanti', 'lui a garanti', '"has guaranteed her"'),
  ('n’est pas satisfacte d’avoir recouvri sa terre dans l’état où la donataires la une laissées. Elle demande qui la dettes', 'n’est pas satisfaite d’avoir recouvré ses terres dans l’état où les donataires les ont laissées. Elle demande que les dettes', '"is not satisfied to have recovered her lands in the state in which the donees left them. She asks that the debts"; this writer\'s "les" looks like "ly"'),
  ('qu’elle posside dans la royaume', 'qu’elle possède dans le royaume', '"which she possesses in the kingdom"'),
  ('d’equité ce voient fait rejetter', 'd’equité avoient fait rejetter', '"had caused her request to be rejected"'),
  ('Les raisons sont toujours', 'Ces raisons sont toujours', '"These reasons are still the same"'),
  ('a présantés avec', 'a présentés avec', '"has presented"'),
  ('et sa fonde encore', 'et se fonde encore', '"and still rests"'),
  ('dans toute leus force et avec a la plus grande évidence dans la mémoire, que la soussigné a l’honneur', 'dans toute leur force et avec la plus grande évidence dans le mémoire, que le soussigné a l’honneur', '"in all their force and with the greatest clearness in the memorandum which the undersigned has the honour"'),
  ('qu[?], lecture faite, ca ministre ne prouve que', 'que, lecture faite, ce ministre ne trouve que', '"that, having read it, this minister will find that"'),
  ('La recommendation de Cabinet', 'La recommendation du Cabinet', '"of the Cabinet of Petersburg"'),
  ('autout de soin que d’impartiabilité après s’être acquitté de ce devoir fait regrette à la vérité, que la résultat de cet examen en soit pas', 'autant de soin que d’impartialité. Après s’être acquitté de ce devoir il regrette à la vérité, que le résultat de cet examen ne soit pas', '"as much care as impartiality. Having done this duty he regrets, in truth, that the result of this examination is not"'),
  ('en faveur de ce Comtesse', 'en faveur de la Comtesse', '"in favour of the Countess"'),
  ('Gouvernement Russs', 'Gouvernement Russe', '"the Russian government"'),
 ],
}


def main():
    write = '--write' in sys.argv
    cp = os.path.join(UNIT_DIR, 'corpus.txt')
    L = io.open(cp, encoding='utf-8').read().split('\n')
    doc = page = None
    pno = 0
    where = {}
    for i, l in enumerate(L):
        m = re.match(r'\[DOC (\S+)\]', l)
        if m:
            doc, pno = m.group(1), 0
            continue
        m = re.match(r'\[PAGE (\S+)\]', l)
        if m:
            page, pno = m.group(1), pno + 1
            continue
        where[i] = (doc, page, pno)
    log, bad = [], []
    for d, rows in ROWS.items():
        for old, new, why in rows:
            hits = [i for i in where if where[i][0] == d and old in L[i]]
            n = sum(L[i].count(old) for i in hits)
            if n != 1:
                bad.append(f'[{d}] {old!r}: found {n} time(s)')
                continue
            i = hits[0]
            L[i] = L[i].replace(old, new)
            key = hashlib.md5(f'{d}|{i + 1}|{old}|{new}'.encode()).hexdigest()[:8]
            log.append((key, f'{SLUG}-{int(d):03d}', where[i][2], where[i][1], old, new,
                        f'@{i + 1} {old} -> {new}', 'read on the scan: ' + why))
    if bad:
        sys.exit('NOT WRITTEN\n' + '\n'.join(bad))
    print(len(log), 'corrections')
    if not write:
        return
    with io.open(cp, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L))
    for _, _, _, pid, old, new, _, _ in log:
        tp = os.path.join(UNIT_DIR, 'transcriptions', pid + '.txt')
        t = io.open(tp, encoding='utf-8').read()
        if t.count(old) != 1:
            sys.exit(f'{pid}.txt: {old!r} found {t.count(old)} time(s)')
        io.open(tp, 'w', encoding='utf-8', newline='\n').write(t.replace(old, new))
    import csv
    dp = os.path.join(UNIT_DIR, 'transcription_decisions.csv')
    with io.open(dp, 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        for key, pad, pno, _pid, old, new, dec, why in log:
            w.writerow([key, pad, pno, old, new, dec, why])
    print('written and logged')


if __name__ == '__main__':
    main()
