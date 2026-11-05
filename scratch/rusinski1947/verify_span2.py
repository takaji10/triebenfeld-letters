# -*- coding: utf-8 -*-
"""Final verification of the spanning-note repairs in the draft."""
import re

t = open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
         r'\rusinski1947\literature\rusinski1947\original.md',
         encoding='utf-8').read()


def deftext(label):
    m = re.search(r'\[\^%s\]: (.*?)(?=\n\[\^|\n\n\[p\. |\Z)' % label,
                  t, re.S)
    return m.group(1) if m else None


def body(label):
    i = t.find('[p. %s]' % label)
    j = t.find('\n[^', i)
    return t[i:j if j > 0 else i + 3000]


ok = True


def check(name, cond, detail=''):
    global ok
    print('%s %s %s' % ('PASS' if cond else 'FAIL', name, detail))
    if not cond:
        ok = False


# runovers: the continuation lives in the prev page's note, not in the
# receiving page's body
check('49-4 ends with the p.50 quotation',
      'równo należeć maią' in (deftext('49-4') or ''))
check('p.50 body free of the quotation',
      'równo należeć maią' not in body('50'))
check('32-3 ends "(Por. spis z T. 1921, s. 80)."',
      (deftext('32-3') or '').rstrip().endswith('(Por. spis z T. 1921, s. 80).'))
check('p.33 body free of "t. nr 55"',
      't. nr 55' not in body('33'))
check('38-3 ends "...dochowały się."',
      'dochowały się' in (deftext('38-3') or ''))
check('p.40 body free of "sprzedali, inwentarz"',
      'sprzedali, inwentarz' not in body('40'))
check('103-3 ends the German quote',
      'zu gestatten”' in (deftext('103-3') or ''))
check('p.104 body free of "dass wir"',
      'dass wir' not in body('104'))
check('116-5 ends "umieli się podpisać."',
      'umieli się podpisać' in (deftext('116-5') or ''))
check('p.117 body free of "metryki protestanckie"',
      'metryki protestanckie' not in body('117'))
# new note 1s
check('49-1 = Przywilej Karpicko',
      (deftext('49-1') or '').startswith('Przywilej dla Ol. Karpicko'))
check('16-1 = merged sigla block',
      (deftext('16-1') or '').startswith('Osada Wymysłowo'))
check('16-1 contains "Dalszy przykład:"',
      'Dalszy przykład' in (deftext('16-1') or ''))
check('16-2 = Burzykowo',
      (deftext('16-2') or '').startswith('Burzykowo'))
check('99-1 = Prawdopodobnie wyrokiem',
      (deftext('99-1') or '').startswith('Prawdopodobnie wyrokiem'))
check('99-2 Grimm "pod słowami"',
      'pod słowami Bede' in (deftext('99-2') or ''))
check('p.99 body "i serwitutów"', 'i serwitutów' in body('99'))
check('20-1 = Zagadnienie etymologii',
      (deftext('20-1') or '').startswith('Zagadnienie etymologii'))
check('118-1 = AW. Krosna',
      (deftext('118-1') or '').startswith('AW. Krosna'))
# no footer junk in the notes (the title page's imprint line is the
# book's own colophon, not note junk)
notes_junk = len(re.findall(r'\[\^[^\]]+\]:[^\n]*Prace Komisji', t))
check('no footer junk in notes', notes_junk == 0, '(%d)' % notes_junk)
# def numbering on the renumbered pages
for lbl, want in (('49', 4), ('16', 2), ('99', 5), ('20', 6), ('118', 5)):
    got = len(re.findall(r'\[\^%s-\d\]:' % lbl, t))
    check('p. %s def count' % lbl, got == want, '(%d/%d)' % (got, want))
print()
print('ALL PASS' if ok else 'FAILURES PRESENT')
