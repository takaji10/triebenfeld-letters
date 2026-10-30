# -*- coding: utf-8 -*-
"""One-off (2026-10-30): give each holding a `prepared:` block (reference/
prepared.yml says what it may hold), save its old "How it was prepared" text
in notes.md, and remove process.md / process_de.md. Run once; the record is
the commit. Usage: python pipeline/review/write_prepared.py [--apply]
"""
import os, sys, io, re
import yaml
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def n(en, de):
    return {'en': en, 'de': de}


tE, tC, tA, tL = 't-editor', 't-claude-scans', 't-ai-supplied', 't-latin-expanded'
cCF, cCW, cEF, cEU = 'c-claude-full', 'c-claude-witness', 'c-editor-full', 'c-editor-uncertain'
l, lA, lE, lER, s = 'l-claude', 'l-auto-check', 'l-editor', 'l-editor-revised', 's-claude'

AS_PAGE = n('Spelling and abbreviations are given as the page has them.',
            'Schreibung und Abkürzungen stehen so, wie die Seite sie hat.')
TABLES = n('In the tables only the names and the words are translated, and every figure stands in the same cell as in the original. Russian names are transliterated letter by letter.',
           'In den Tabellen sind nur die Namen und die Wörter übersetzt, und jede Zahl steht in derselben Zelle wie im Original. Russische Namen sind Buchstabe für Buchstabe transliteriert.')

DATA = {
 'adwl85': ([tE, n("At the editor's request Claude transcribed from the scans the passages of the same pages that the editor's transcription had left out, and then read every page, the editor's text with it, against the scans word by word.",
                   'Auf Wunsch des Herausgebers transkribierte Claude die Stellen derselben Seiten, die die Transkription des Herausgebers ausgelassen hatte, nach den Scans und las dann jede Seite samt dem Text des Herausgebers Wort für Wort an den Scans nach.')],
            [l, s]),
 'agad1169011745': ([tC, cEF],
            [l, n('The English version of the table translates the heading and the kinds of place and leaves the names as the clerk wrote them.',
                  'Die englische Fassung der Tabelle übersetzt die Überschrift und die Ortsarten und lässt die Namen, wie der Schreiber sie schrieb.'), s]),
 'agad1174016': ([tE, cCF, AS_PAGE], [l, lA, s]),
 'agad11740273': ([tE, cCF, n('Spelling and abbreviations are given as the page has them; words the writers struck out are not transcribed.',
                              'Schreibung und Abkürzungen stehen so, wie die Seite sie hat; von den Schreibern gestrichene Wörter sind nicht transkribiert.')],
            [l, lA, s]),
 'agad118501169': ([n("The text is the archive's own transcript of the report, read against the scans.",
                      'Der Text ist die eigene Transkription des Berichts durch das Archiv, an den Scans nachgelesen.')],
            [n("The English is the archive's own translation, read against the French.",
               'Die englische Fassung ist die eigene Übersetzung des Archivs, am Französischen nachgelesen.'), s]),
 'apl399806603': ([tC, cEU], [l, TABLES, s]),
 'app5314550221': ([tC, tL], [l, s]),
 'app53150kaliszgr414': ([tE, tL, n("Claude then compared the transcription with the scans, except the middle of the recital of the Tribunal's decrees (about 200 words), and corrected it where the page is plain.",
                                    'Claude verglich die Transkription anschließend mit den Scans, außer der Mitte der Wiedergabe der Tribunalsdekrete (etwa 200 Wörter), und korrigierte sie, wo die Seite eindeutig ist.')],
            [lER, s]),
 'app53150kaliszgr424': ([tE, tL, cCF], [lER, s]),
 'app53150kaliszgr425': ([tE, n('Claude then compared the closing line, the signatures and the Latin record with the scans, but not the body of the adjournment (about 170 words of clear Polish), and corrected the transcription where the page is plain.',
                                'Claude verglich anschließend die Schlusszeile, die Unterschriften und den lateinischen Vermerk mit den Scans, nicht aber den Hauptteil der Vertagung (etwa 170 Wörter klares Polnisch), und korrigierte die Transkription, wo die Seite eindeutig ist.')],
            [lER, s]),
 'app53170koningr114': ([tE, tL, cCF], [lER, s]),
 'app53170koningr115': ([tE, tL, n('Claude then compared the transcription with the scans: every heading and date line, three of the longer entries whole, the second half of three more, and the notes of 1768. It corrected the transcription where the page is plain. Two notes of 1768 that the editor had given by their headings only were read from the scans as far as that could be done with confidence.',
                                   'Claude verglich die Transkription anschließend mit den Scans: alle Überschriften und Datumszeilen, drei der längeren Einträge ganz, die zweite Hälfte von drei weiteren und die Vermerke von 1768. Wo die Seite eindeutig ist, korrigierte Claude die Transkription. Zwei Vermerke von 1768, die der Herausgeber nur mit ihren Überschriften gegeben hatte, wurden an den Scans so weit gelesen, wie es mit Sicherheit möglich war.')],
            [lER, n("The three early notes had no English; Claude translated them in the editor's terms.",
                    'Für die drei frühen Vermerke gab es kein Englisch; Claude übersetzte sie in den Begriffen des Herausgebers.'), s]),
 'app53170koningr116': ([tE, tL, cCF], [lER, s]),
 'app53170koningr117': ([tE, tL, cCF], [lER, s]),
 'app53170koningr118': ([tE, tL, n("One note on a photographed page that the editor's text lacked was transcribed from the scan by Claude.",
                                   'Ein Vermerk auf einer fotografierten Seite, der im Text des Herausgebers fehlte, wurde von Claude nach dem Scan transkribiert.'), cCF],
            [lER, s]),
 'app53170koningr119': ([tE, tL, cCF], [lER, s]),
 'app53170koningr120': ([tE, tL, cCF], [lER, s]),
 'app53170koningr121': ([tE, tL, cCF], [lER, s]),
 'app53170koningr136': ([tE, n('Claude then compared the heading, the count of people and leaf 123 with the scans and corrected the transcription where the page is plain. The description of the manor buildings (about 540 words) was not compared.',
                               'Claude verglich anschließend die Überschrift, die Zählung der Personen und Blatt 123 mit den Scans und korrigierte die Transkription, wo die Seite eindeutig ist. Die Beschreibung der Herrenhausgebäude (etwa 540 Wörter) wurde nicht verglichen.')],
            [lER, s]),
 'app53170koningr145': ([tE, n("The Polish is given in modern spelling (i for the clerk's y, small letters for capitals, modern endings) and the Latin as written, with its abbreviations filled out.",
                               'Das Polnische steht in moderner Schreibung (i für das y des Schreibers, Kleinbuchstaben für Großbuchstaben, moderne Endungen), das Latein wie geschrieben, mit aufgelösten Abkürzungen.'),
                        n('Claude then compared all 122 pages with the scans and corrected the transcription, mostly misread words and words skipped between two occurrences of the same word.',
                          'Claude verglich anschließend alle 122 Seiten mit den Scans und korrigierte die Transkription, meist falsch gelesene Wörter und Wörter, die zwischen zwei gleichen Wörtern übersprungen worden waren.')],
            [lER, n('Claude translated one paragraph of about a hundred words at the head of leaf 680 that the translation lacked.',
                    'Claude übersetzte einen Absatz von etwa hundert Wörtern am Anfang von Blatt 680, der in der Übersetzung fehlte.'), s]),
 'app53170koningr153': ([tE, tL, cCF], [lER, s]),
 'app5320pozgr1181': ([tE], [l, s]),
 'app5321pyzdrygr115': ([tE], [l, s]),
 'app534062': ([tE, n('Two words were corrected at the editor\'s word: "Judicius" to "Judicio", and "Citti~" read as Citati.',
                      'Zwei Wörter wurden auf Wunsch des Herausgebers korrigiert: „Judicius“ zu „Judicio“, und „Citti~“ wurde als Citati gelesen.')],
            [l, s]),
 'app536017': ([tE, n("The editor's first reading left most words of the court's order in doubt. At the editor's request Claude read the entry again from the scans, reading each phrase in all the places it occurs in the neighbouring entries, which are orders of the same kind in the same set words. Its reading replaced the editor's text; five places remain marked as not fully read.",
                     'Die erste Lesung des Herausgebers ließ die meisten Wörter der gerichtlichen Anordnung im Zweifel. Auf Wunsch des Herausgebers las Claude den Eintrag noch einmal an den Scans und las jede Wendung an allen Stellen, an denen sie in den benachbarten Einträgen vorkommt; diese sind Anordnungen derselben Art in denselben festen Worten. Seine Lesung ersetzte den Text des Herausgebers; fünf Stellen bleiben als nicht vollständig gelesen gekennzeichnet.')],
            [n("The editor's English had been made from the first reading; Claude revised it throughout to follow the new reading, keeping the editor's terms.",
               'Das Englisch des Herausgebers war nach der ersten Lesung entstanden; Claude überarbeitete es durchgehend nach der neuen Lesung und behielt die Begriffe des Herausgebers bei.'), s]),
 'app536036': ([tE, n('Claude then read both entries against the scan word for word and corrected them, settling nearly every doubt from the other entries on the same pages, which are judgments of the same kind in the same words.',
                      'Claude las anschließend beide Einträge Wort für Wort am Scan nach und korrigierte sie; fast jeden Zweifel entschied es aus den anderen Einträgen auf denselben Seiten, die Urteile derselben Art in denselben Worten sind.')],
            [n("The editor's English had been made from the first reading; Claude revised it wherever the corrected Latin required it, which is in most sentences.",
               'Das Englisch des Herausgebers war nach der ersten Lesung entstanden; Claude überarbeitete es überall, wo das korrigierte Latein es verlangte, also in den meisten Sätzen.'), s]),
 'app536040': ([tE, tL, cCF], [lER, s]),
 'app536045': ([tE, tL, cCF], [lER, s]),
 'app536046': ([tE, n('Claude then read the whole of the first entry against the film, enlarged, and corrected it where the film is plain; the film shows the words but not every ending. Entry no. 17, which the editor had read only once, was transcribed again by Claude from the film, with the editor\'s reading beside it, and the editor settled two of its words against the page.',
                      'Claude las anschließend den ganzen ersten Eintrag vergrößert am Film nach und korrigierte ihn, wo der Film eindeutig ist; der Film zeigt die Wörter, aber nicht jede Endung. Eintrag Nr. 17, den der Herausgeber erst einmal gelesen hatte, transkribierte Claude am Film noch einmal, mit der Lesung des Herausgebers daneben; der Herausgeber entschied zwei Wörter an der Seite.')],
            [n("The editor's English had been made from the first reading; Claude revised it to follow the corrected reading and translated entry no. 17 in the editor's terms.",
               'Das Englisch des Herausgebers war nach der ersten Lesung entstanden; Claude überarbeitete es nach der korrigierten Lesung und übersetzte Eintrag Nr. 17 in den Begriffen des Herausgebers.'), s]),
 'app536047': ([tE, tL, cCF], [lER, s]),
 'app53640kalisztab21': ([tC, cEF],
            [l, n('The English version of the table translates the title, the heading and the common words (village, small town, demesne farm, mill, part of) and leaves the names as the clerk wrote them.',
                  'Die englische Fassung der Tabelle übersetzt den Titel, die Überschrift und die gewöhnlichen Wörter (Dorf, Städtchen, Vorwerk, Mühle, Teil von) und lässt die Namen, wie der Schreiber sie schrieb.'), s]),
 'app5371057': ([tA, cCW],
            [l, n('The English marks two garbled passages as uncertain.', 'Die englische Fassung kennzeichnet zwei verderbte Stellen als unsicher.'), s]),
 'app539680545': ([n('The five list sheets were read by Claude from enlarged bands of the images. The editor settled the doubtful readings, and their readings replaced most of them. The three prose sheets are the editor\'s own transcription, kept as typed.',
                     'Die fünf Listenblätter las Claude an vergrößerten Streifen der Aufnahmen. Der Herausgeber entschied die zweifelhaften Lesungen, und seine Lesungen ersetzten die meisten davon. Die drei Prosablätter sind die eigene Transkription des Herausgebers, so belassen, wie sie getippt war.')],
            [l, n('In the lists every name stays as written and only the headings and the common words are translated.',
                  'In den Listen bleibt jeder Name wie geschrieben, und nur die Überschriften und die gewöhnlichen Wörter sind übersetzt.'), s]),
 'app539680669': ([tC, cEU, n('The editor also read the English against the scans and corrected names, places and the order of some lines.',
                              'Der Herausgeber las außerdem das Englische an den Scans nach und korrigierte Namen, Orte und die Reihenfolge einiger Zeilen.')],
            [l, s]),
 'app539680716': ([tC, n("The editor checked the doubtful readings that a name, a place, a heading or the sense of a note rests on against the photographs, and a comparison with the original table of 1868 corrected figures and names misread in Breyer's copy of it. Where Breyer spells a name differently from the original table, the name is given as the original writes it, at the editor's word.",
                        'Der Herausgeber prüfte die zweifelhaften Lesungen, auf denen ein Name, ein Ort, eine Überschrift oder der Sinn einer Notiz beruht, an den Aufnahmen, und der Vergleich mit der Originaltabelle von 1868 korrigierte Zahlen und Namen, die in Breyers Abschrift falsch gelesen worden waren. Wo Breyer einen Namen anders schreibt als die Originaltabelle, steht der Name so, wie ihn das Original schreibt, auf Wunsch des Herausgebers.')],
            [l, TABLES, s]),
 'app539680782': ([tE, n('Claude laid out the lines against the images, and the editor ruled the doubtful line breaks.',
                         'Claude legte die Zeilen nach den Aufnahmen aus, und der Herausgeber entschied die zweifelhaften Zeilenumbrüche.')],
            [l, s]),
 'app539680783': ([tE, n("Claude then compared all five pages with the scans and corrected the transcription, adding the court messenger's handwritten lines. The editor read his pen alterations on the scan.",
                         'Claude verglich anschließend alle fünf Seiten mit den Scans und korrigierte die Transkription; dabei ergänzte es die handschriftlichen Zeilen des Gerichtsboten. Der Herausgeber las seine Federkorrekturen am Scan.')],
            [n("The editor's file had a machine translation, which was wrong in many places, some of them of substance. Claude wrote the English again from the corrected Polish, keeping the editor's wording where it was right.",
               'Die Datei des Herausgebers enthielt eine maschinelle Übersetzung, die an vielen Stellen falsch war, teils im Sachlichen. Claude schrieb das Englische nach dem korrigierten Polnisch neu und behielt die Formulierungen des Herausgebers, wo sie richtig waren.'), s]),
 'app539680801': ([tE, cCF], [l, s]),
 'ihagrrep7cnr1414': ([tE, cCF], [l, lA, s]),
 'ihagrrep7cnr3570': ([tA, cCW, n('Twelve pages repeating one form of charter for the other six recipients were left untranscribed at the editor\'s choice.',
                                  'Zwölf Seiten, die dieselbe Urkundenform für die übrigen sechs Empfänger wiederholen, blieben auf Wunsch des Herausgebers untranskribiert.')],
            [l, n("Corrections that Claude proposed during translation and that rested on sense alone were not applied, and the English marks those words as uncertain.",
                  'Korrekturen, die Claude während der Übersetzung vorschlug und die sich nur auf den Sinn stützten, wurden nicht übernommen; das Englische kennzeichnet diese Wörter als unsicher.'), s]),
 'ihagrrep7cnr3705': ([tA, cCW], [l, s]),
 'ihagrrep7cnr3709': ([n("The editor transcribed the file with a handwriting recognition model and read the French petition a second time. The transcription was then corrected where something proves the reading, such as the same sentence in the decree and in the drafts written from it, a fixed formula or a form that is no word. The signatures of the councillors at Poznań were read against the list of that court in the Prussian state handbook for 1800 and 1801.",
                      'Der Herausgeber transkribierte die Akte mit einem Handschriftenerkennungsmodell und las die französische Bittschrift ein zweites Mal. Die Transkription wurde danach korrigiert, wo etwas die Lesung beweist, etwa derselbe Satz im Urteil und in den daraus geschriebenen Entwürfen, eine feste Formel oder eine Form, die kein Wort ist. Die Unterschriften der Räte in Posen wurden mit dem Verzeichnis dieses Gerichts im preußischen Staatshandbuch für 1800 und 1801 gelesen.'),
                     n('The initials on the papers issued in the Grand Chancellor\'s name are one hand throughout and are given as "G[oldbeck]".',
                       'Die Namenszeichen auf den im Namen des Großkanzlers ausgefertigten Papieren stammen durchgehend von einer Hand und sind als „G[oldbeck]“ gegeben.')],
            [l, lA, s]),
 'iharep162nr295': ([tE, cCF], [l, lA, s]),
 'iiihamdaiiinr12366': ([tE, cCF], [l, lA, s]),
 'iiihamdaiiinr12367': ([tE, cCF], [l, lA, s]),
 'iiihamdaiiinr12765': ([tA, cCW, n('The editor checked a random twenty of the changes against the scans and found all twenty right.',
                                    'Der Herausgeber prüfte zwanzig zufällig gewählte Änderungen an den Scans und fand alle zwanzig richtig.'),
                         n('Claude cropped every set of initials from the scans and laid them side by side. They sort into four hands, which the editor confirmed as Hardenberg, Stägemann, Hoffmann and Balan; the names are filled out in square brackets.',
                           'Claude schnitt alle Namenszeichen aus den Scans aus und legte sie nebeneinander. Sie ordnen sich zu vier Händen, die der Herausgeber als Hardenberg, Stägemann, Hoffmann und Balan bestätigte; die Namen sind in eckigen Klammern aufgelöst.')],
            [l, lA, s]),
 'kdw': ([n('There are no page images. The text is copied from the electronic text of the Wielkopolska Digital Library, which the editor takes to be secure, and nothing in it is corrected.',
            'Es gibt keine Seitenbilder. Der Text ist aus dem elektronischen Text der Wielkopolska Digital Library kopiert, den der Herausgeber für gesichert hält, und nichts darin ist korrigiert.')],
            [n('Claude translated each entry into English, the editors\' parts as well as the document. Places are given in their modern Polish forms where the editors identify them, and the medieval spellings stand in the Latin.',
               'Claude übersetzte jeden Eintrag ins Englische, die Teile der Herausgeber ebenso wie die Urkunde. Orte stehen in ihren heutigen polnischen Formen, wo die Herausgeber sie bestimmen, und die mittelalterlichen Schreibungen stehen im Latein.'), s]),
 'oe1bu14525': ([tA, n("Claude went through the transcription in three passes, correcting misreadings and restoring the order of lines in places, and brought personal names and the King's titles to one spelling, on the editor's instruction. Place names stand in the German form the documents use; the lists and the English give the Polish name.",
                       'Claude ging die Transkription in drei Durchgängen durch, korrigierte Fehllesungen, stellte an einigen Stellen die Zeilenfolge wieder her und brachte auf Anweisung des Herausgebers Personennamen und Titel des Königs auf eine einheitliche Schreibung. Ortsnamen stehen in der deutschen Form der Dokumente; die Verzeichnisse und das Englische geben den polnischen Namen.'),
                 n('Catchwords at the foot of pages, which repeat the first word of the next page, were removed from the transcription at the editor\'s instruction.',
                   'Kustoden am Fuß der Seiten, die das erste Wort der nächsten Seite wiederholen, wurden auf Anweisung des Herausgebers aus der Transkription entfernt.')],
            [l, s]),
 'oe1bu14526': ([tA, n("The transcription's typical errors are a single wrong letter and, more seriously, a real word put in place of the right one without a mark of doubt. Claude settled most of the words marked as doubtful and corrected others it found wrong, usually from the same word written clearly elsewhere in the contract, a second copy of the contract or the standard wording of these contracts.",
                       'Die typischen Fehler der Transkription sind ein einzelner falscher Buchstabe und, schwerwiegender, ein echtes Wort anstelle des richtigen ohne Zweifelsmarkierung. Claude entschied die meisten der als zweifelhaft markierten Wörter und korrigierte weitere, die es für falsch hielt, meist nach demselben Wort an anderer Stelle des Vertrags deutlich geschrieben, nach einer zweiten Abschrift des Vertrags oder nach dem üblichen Wortlaut dieser Verträge.')],
            [l, s]),
 'oe1bu9454': ([n("Claude transcribed the letters from the German cursive handwriting; the present transcription is a second machine reading, made in September 2026, in which the editor corrected names and layout by hand. The machine's typical errors are a single misread letter and, more seriously, a real word put in place of the right one without a mark of doubt. The editor transcribed seventeen passages written sideways in the margins that the machine had missed.",
                'Claude transkribierte die Briefe nach der deutschen Kurrentschrift; die vorliegende Transkription ist eine zweite maschinelle Lesung vom September 2026, in der der Herausgeber Namen und Layout von Hand korrigierte. Die typischen Fehler der Maschine sind ein einzelner falsch gelesener Buchstabe und, schwerwiegender, ein echtes Wort anstelle des richtigen ohne Zweifelsmarkierung. Siebzehn quer an den Rand geschriebene Stellen, die die Maschine übersehen hatte, transkribierte der Herausgeber.'),
               n("Claude proposed corrections in several passes, with the editor setting the rule: a word is changed only where an independent witness supports the change and the new word is close in its letters to the old one. Accepted witnesses were a second copy of the same letter, the same word written correctly elsewhere in the letter, a word or name attested many times in the file, and fixed formulas of address and closing. Names, figures, abbreviations and passages in French, Polish or Latin were not changed on Claude's judgement. The editor checked samples of each batch against the scans.",
                 'Claude schlug in mehreren Durchgängen Korrekturen vor, wobei der Herausgeber die Regel setzte: Ein Wort wird nur geändert, wenn ein unabhängiger Beleg die Änderung stützt und das neue Wort dem alten in den Buchstaben nahe ist. Als Belege galten eine zweite Abschrift desselben Briefes, dasselbe Wort an anderer Stelle des Briefes richtig geschrieben, ein in der Akte vielfach belegtes Wort oder ein Name und feste Anrede- und Schlussformeln. Namen, Zahlen, Abkürzungen und Stellen auf Französisch, Polnisch oder Latein änderte Claude nicht nach eigenem Urteil. Der Herausgeber prüfte Stichproben jedes Durchgangs an den Scans.'),
               n('Personal names and titles were brought to one spelling on the editor\'s ruling. Where a letter gives no date, sender or recipient, the editor or Claude supplied it from the content, and the page of the document states the basis. Thirteen letters are largely uncorrected and marked as rough.',
                 'Personennamen und Titel wurden auf Entscheidung des Herausgebers auf eine Schreibung gebracht. Wo ein Brief kein Datum, keinen Absender oder Empfänger nennt, ergänzte ihn der Herausgeber oder Claude aus dem Inhalt, und die Seite des Dokuments nennt die Grundlage. Dreizehn Briefe sind weitgehend unkorrigiert und als grob gekennzeichnet.')],
            [l, lA, s]),
 'oe1u199': ([tA, cCW], [l, s]),
}


def main():
    apply = '--apply' in sys.argv
    base = os.path.join(ROOT, 'units')
    slugs = sorted(d for d in os.listdir(base) if os.path.exists(os.path.join(base, d, 'unit.yml')))
    missing = [x for x in slugs if x not in DATA]
    extra = [x for x in DATA if x not in slugs]
    if missing or extra:
        raise SystemExit('missing %r extra %r' % (missing, extra))
    lib = yaml.safe_load(open(os.path.join(ROOT, 'reference', 'prepared.yml'), encoding='utf-8'))['sentences']
    for t, ltr in DATA.values():
        for it in t + ltr:
            if isinstance(it, str) and it not in lib:
                raise SystemExit('unknown key %r' % it)
    print(len(DATA), 'holdings')
    if not apply:
        return
    for slug, (t, ltr) in DATA.items():
        d = os.path.join(base, slug)
        up = os.path.join(d, 'unit.yml')
        txt = open(up, encoding='utf-8').read()
        if re.search(r'^prepared:', txt, re.M):
            raise SystemExit('%s already has prepared:' % slug)
        block = yaml.safe_dump({'prepared': {'transcription': t, 'translation': ltr}},
                               allow_unicode=True, sort_keys=False, width=100000,
                               default_flow_style=False)
        txt = txt.rstrip() + ('\n\n# What the "How it was prepared" tab says (reference/prepared.yml; the old text is in notes.md).\n'
                              + block)
        with open(up, 'w', encoding='utf-8', newline='\n') as f:
            f.write(txt)
        # the old public text goes to the notes
        pp = os.path.join(d, 'process.md')
        old = open(pp, encoding='utf-8').read().strip() if os.path.exists(pp) else ''
        if old:
            npth = os.path.join(d, 'notes.md')
            notes = open(npth, encoding='utf-8').read() if os.path.exists(npth) else ''
            with open(npth, 'w', encoding='utf-8', newline='\n') as f:
                f.write(notes.rstrip() + '\n\n## How it was prepared (the public text before 2026-10-30)\n\n'
                        'The editor ruled the tab too detailed: it now tells only what an AI decided that '
                        'affected the text (`prepared:` in unit.yml). The full account, kept here:\n\n'
                        + old + '\n')
        for fn in ('process.md', 'process_de.md'):
            fp = os.path.join(d, fn)
            if os.path.exists(fp):
                os.remove(fp)


main()
