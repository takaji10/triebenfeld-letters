# -*- coding: utf-8 -*-
"""One-off (2026-10-30): remove "Form and language" from the holdings' about
texts, keep the sentences that change how a document is read, and save the
whole old section in the holding's notes.md. Run once; the record is the
commit. Usage: python pipeline/review/drop_form_and_language.py [--apply]
"""
import re, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CTX = '<!-- context -->'
DATING = ('Dating.', 'Datierung.')
NOTES = ('Notes on the entries.', 'Anmerkungen zu den Einträgen.')


def sents(p):
    p = p.replace(CTX, '').strip()
    return [s for s in re.split(r'(?<=[.!?”"\)\]])\s+(?=[A-ZÄÖÜĄĆĘŁŃÓŚŹŻ"“\[*])', p) if s.strip()]


# unit -> list of groups (label, items). An item is an English sentence
# prefix, 'P<n>' for paragraph n whole, or (en_prefix, de_prefix) where the
# German splits differently.
SPEC = {
 'agad1169011745': [(('Sums.', 'Summen.'), ['In every line the men'])],
 'agad11740273': [(('The documents.', 'Die Dokumente.'), ['The three petitions are the originals', 'The resolution is the commission'])],
 'app53170koningr115': [(NOTES, [('Two of the notes of 1768', 'Zwei der Vermerke'), ("Chełmski's signature stands", 'Chełmskis Unterschrift'), ('Three entries stand under', 'Drei Einträge stehen')])],
 'app53170koningr116': [(NOTES, ['The signatures are autograph', "The clerk's Latin calls Kwilecki", 'Five of the twelve entries'])],
 'app53170koningr117': [(NOTES, ['Two reports give what the messenger saw', 'Antoni Prusimski here calls', "Chełmski's first protest has no heading", 'The note of the decree of remission', 'Six entries have no dated heading'])],
 'app53170koningr118': [(NOTES, ['Fifteen entries have no dated heading', 'One heading gives a weekday', 'One note is unfinished']), (None, ['P1'])],
 'app53170koningr119': [(DATING, ['Four entries have no dated heading'])],
 'app53170koningr120': [(DATING, ['The second entry has no dated heading'])],
 'app53170koningr121': [(None, ['The clerk describes the cart'])],
 'app53170koningr136': [(None, ['**Its middle is not transcribed', 'That part is in neither', 'The text takes up again'])],
 'app53170koningr153': [(('The acts.', 'Die Akte.'), ['Both acts are originals'])],
 'app534062': [(None, ['The entry has no date of its own', 'The year 1727 is assigned'])],
 'app536017': [(('Neighbouring entries.', 'Benachbarte Einträge.'), ['P1']), (DATING, ['P2'])],
 'app536036': [(DATING, ['P1'])],
 'app536045': [(DATING, ['P1'])],
 'app536046': [(DATING, ['P1']), (('Entry no. 17.', 'Eintrag Nr. 17.'), ['It names the Monday after Laetare', 'The citation to that hearing', 'The editor has looked at both pages'])],
 'app536047': [(DATING, ['P1'])],
 'app53640kalisztab21': [(None, ['A village that belonged to several owners'])],
 'app539680716': [(None, ['In the tables a figure such as'])],
 'app539680782': [(None, ['"pohl." after a sum'])],
 'app539680783': [(None, ['One summons was printed', 'On this copy he also', 'He struck out one name']), (None, ['P1'])],
 'ihagrrep7cnr1414': [(('The papers.', 'Die Schriftstücke.'), [('The first page is the department', 'Die erste Seite'), ('The extract is a clean copy', 'Der Auszug'), ("Schrötter's letter is the original", 'Schrötters Schreiben')])],
 'ihagrrep7cnr3570': [(None, ['The papers are drafts and copies', 'Registry notes at the front', 'Twelve pages, apparently'])],
 'ihagrrep7cnr3705': [(None, ['A fair copy in German', 'The letters A to H', 'The file contains no reply'])],
 'iiihamdaiiinr12366': [(('Originals and copies.', 'Originale und Abschriften.'), ['P0'])],
 'iiihamdaiiinr12367': [(('Originals and copies.', 'Originale und Abschriften.'), ['P0'])],
 'kdw': [(None, ["The editors' apparatus", 'Vertical strokes'])],
 'oe1bu14525': [(None, ['Because most documents are certified copies', 'Several charters appear more than once', 'The documents keep the archive'])],
 'oe1bu14526': [(None, ['Powers of attorney, royal confirmations', 'The documents keep the archive'])],
 'oe1bu9454': [(None, ['The file keeps the archive', 'Several numbers hold a letter', 'Four numbers are absent', 'Three documents are present']), (None, ['Triebenfeld wrote in haste'])],
}
# Hand-written kept text (label, EN, DE) where the old sentence mixed what
# goes with what stays. The German is the old German, cut the same way.
MANUAL = {
 'iharep162nr295': [(('The copies.', 'Die Abschriften.'),
   "All three pieces are copies in one clerk's hand, made for the treasury's file: every signature is preceded by \"gez.\" (signed), and the seals are given as \"L. S.\"",
   'Alle drei Stücke sind Abschriften von der Hand eines Schreibers, für die Akte der Staatsschatzverwaltung angefertigt: Vor jeder Unterschrift steht „gez.“, und die Siegel sind als „L. S.“ wiedergegeben.')],
 'app539680545': [(None,
   "Breyer's own spellings and slips are kept as written (Schultypußes, kulturtellen), and his Polish spellings vary from list to list (Bartmański and Barmański, Szulborski and Schulborski). No sheet is dated; the years they name – 1741, 1843, 1855 – are the dates of the material, not of the sheets. From the schools essay and from Breyer's work at Sompolno, which lies in the same country, the sheets are of the 1930s.",
   'Breyers eigene Schreibungen und Fehler sind wie geschrieben festgehalten (Schultypußes, kulturtellen), und seine polnischen Schreibungen wechseln von Liste zu Liste (Bartmański und Barmański, Szulborski und Schulborski). Kein Blatt ist datiert; die genannten Jahre – 1741, 1843, 1855 – sind Daten des Materials, nicht der Blätter. Aus dem Schulaufsatz und aus Breyers Wirken in Sompolno, das im selben Lande liegt, stammen die Blätter aus den dreißiger Jahren.')],
 'app539680801': [(('The copy.', 'Die Abschrift.'),
   "The copyist spells several places in his own way (Zagurowo, Trompczyn, Lond). He copied the list of the lessees' shares with corrections: two names are written in between the lines and the numbering is altered.",
   'Der Abschreiber schreibt mehrere Orte auf seine Weise (Zagurowo, Trompczyn, Lond). Die Liste der Anteile der Erbpächter hat er mit Verbesserungen abgeschrieben: Zwei Namen sind zwischen den Zeilen nachgetragen, und die Zählung ist geändert.')],
 'iiihamdaiiinr12765': [(None,
   'Twelve documents are drafts of outgoing letters, bearing the initials of the officials who approved them [[2, 5, 7, 9, 10, 16, 17, 21, 22, 24, 26, 29]]. Three drafts are written on the incoming letter to which they reply [[2, 9, 10]]. One reply to Hohenlohe-Ingelfingen exists as a cancelled draft and its fair copy, which was not sent [[11, 12]]. The initials are those of Hardenberg, the Councillor of State Stägemann, and the officials Hoffmann and Balan; they are expanded in square brackets [[5, 22, 29]].',
   'Zwölf Dokumente sind Entwürfe ausgehender Schreiben mit den Namenszeichen der Beamten, die sie genehmigten [[2, 5, 7, 9, 10, 16, 17, 21, 22, 24, 26, 29]]. Drei Entwürfe stehen auf dem eingegangenen Schreiben, das sie beantworten [[2, 9, 10]]. Eine Antwort an Hohenlohe-Ingelfingen liegt als kassierter Entwurf und als nicht abgesandte Reinschrift vor [[11, 12]]. Die Namenszeichen stammen von Hardenberg, dem Staatsrat Stägemann und den Beamten Hoffmann und Balan; sie sind in eckigen Klammern aufgelöst [[5, 22, 29]].')],
}


def span(text, heading_re):
    m = re.search(r'^### (?:%s)[ \t]*\n' % heading_re, text, re.M)
    if not m:
        return None
    n = re.search(r'^### ', text[m.end():], re.M)
    end = m.end() + n.start() if n else len(text)
    return m.start(), m.end(), end


def pick(paras_en, paras_de, items, lang):
    """The chosen sentences (or whole paragraphs), joined, in one language."""
    flat_en = [s for p in paras_en for s in sents(p)]
    flat_de = [s for p in paras_de for s in sents(p)]
    aligned = len(flat_en) == len(flat_de)
    out = []
    for it in items:
        pre = it[0] if isinstance(it, tuple) else it
        dpre = it[1] if isinstance(it, tuple) else None
        if re.fullmatch(r'P\d+', pre):
            out.append(' '.join(sents((paras_en if lang == 'en' else paras_de)[int(pre[1:])])))
            continue
        idx = [k for k, s in enumerate(flat_en) if s.startswith(pre)]
        if len(idx) != 1:
            raise SystemExit('English prefix not unique/found: %r %r' % (pre, idx))
        if lang == 'en':
            out.append(flat_en[idx[0]])
        elif dpre:
            hit = [s for s in flat_de if s.startswith(dpre)]
            if len(hit) != 1:
                raise SystemExit('German prefix not unique/found: %r' % dpre)
            out.append(hit[0])
        else:
            if not aligned:
                raise SystemExit('sentence counts differ, give German prefixes for %r' % pre)
            out.append(flat_de[idx[0]])
    return ' '.join(out)


def kept_for(unit, paras_en, paras_de):
    res = {'en': [], 'de': []}
    for label, en, de in MANUAL.get(unit, []):
        res['en'].append((label[0] if label else None, en))
        res['de'].append((label[1] if label else None, de))
    for label, items in SPEC.get(unit, []):
        for k, lang in enumerate(('en', 'de')):
            res[lang].append((label[k] if label else None, pick(paras_en, paras_de, items, lang)))
    return res


def fmt(label, text):
    body = (('**%s** ' % label) if label else '') + text
    return body + ('' if re.search(r'\[\[\s*\d', text) else ' ' + CTX)


def rebuilt(unit, lang, kept):
    path = os.path.join(ROOT, 'units', unit, 'about%s.md' % ('_de' if lang == 'de' else ''))
    text = open(path, encoding='utf-8').read()
    fl = span(text, 'Form and language' if lang == 'en' else 'Form und Sprache')
    text2 = text[:fl[0]] + text[fl[2]:]
    if lang == 'en':
        target = 'The entry' if unit == 'app534062' else 'Contents'
    else:
        target = 'Der Eintrag' if unit == 'app534062' else 'Inhalt'
    new = text2
    if kept:
        tsp = span(text2, re.escape(target))
        if not tsp:
            raise SystemExit('%s %s: no target section %r' % (unit, lang, target))
        body = text2[tsp[1]:tsp[2]].rstrip()
        add = '\n\n'.join(fmt(l, t) for l, t in kept)
        new = text2[:tsp[1]] + body + '\n\n' + add + '\n\n' + text2[tsp[2]:]
    new = re.sub(r'\n{3,}', '\n\n', new).rstrip() + '\n'
    return new, path


def main():
    apply = '--apply' in sys.argv
    base = os.path.join(ROOT, 'units')
    for u in sorted(os.listdir(base)):
        pe = os.path.join(base, u, 'about.md')
        if not os.path.exists(pe):
            continue
        te = open(pe, encoding='utf-8').read()
        fe = span(te, 'Form and language')
        if not fe:
            continue
        td = open(os.path.join(base, u, 'about_de.md'), encoding='utf-8').read()
        fd = span(td, 'Form und Sprache')
        if not fd:
            raise SystemExit('%s: no German section' % u)
        paras_en = te[fe[1]:fe[2]].strip().split('\n\n')
        paras_de = td[fd[1]:fd[2]].strip().split('\n\n')
        kept = kept_for(u, paras_en, paras_de)
        print('===', u)
        for lang in ('en', 'de'):
            for l, t in kept[lang]:
                print('  %s | %s' % (lang, fmt(l, t)[:240]))
        if apply:
            for lang in ('en', 'de'):
                new, path = rebuilt(u, lang, kept[lang])
                with open(path, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(new)
            np_ = os.path.join(base, u, 'notes.md')
            notes = open(np_, encoding='utf-8').read() if os.path.exists(np_) else ''
            add = ('\n\n## Form and language (taken off the public page, 2026-10-30)\n\n'
                   'The editor ruled the section too descriptive: the languages went to the header, '
                   'and what changes how a document is read stays in "Contents". The old text:\n\n'
                   + te[fe[1]:fe[2]].replace(CTX, '').strip() + '\n')
            with open(np_, 'w', encoding='utf-8', newline='\n') as f:
                f.write(notes.rstrip() + add)


main()
