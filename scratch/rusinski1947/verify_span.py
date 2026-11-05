# -*- coding: utf-8 -*-
"""Verify the spanning-note repairs in the recomposed draft."""
import re

t = open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
         r'\rusinski1947\literature\rusinski1947\original.md',
         encoding='utf-8').read()


def page(label):
    i = t.find('[p. %s]' % label)
    j = t.find('\n[p. ', i + 1)
    return t[i:j if j > 0 else len(t)]


print('--- footer junk remaining:', len(re.findall(
    r'Prace Komisji Atlasu hist\. Polski', t)))

p49 = page('49')
print('--- p. 49 defs:')
for m in re.finditer(r'\[\^49-\d\]: .{0,90}', p49):
    print('   ', m.group(0).replace('\n', ' / '))
print('   body has quotation?', 'równo należeć maią' in p49)

p50 = page('50')
print('--- p. 50 body starts:', p50.split('\n', 1)[1][:100].replace('\n', ' / '))

print('--- p. 32 tail / p. 33 head (Daleszyno join):')
print('   32:', p49[-0:0] or '')
p32 = page('32')
print('   32 note tail: ...', re.search(
    r'\[\^32-3\]: .{0,4000}', p32, re.S).group(0)[-160:].replace('\n', ' / '))
p33 = page('33')
print('   33 body head:', p33.split('\n', 2)[2][:80] if p33.count('\n') > 2 else '')

p39 = page('39')
m = re.search(r'\[\^39-3\]: .{0,4000}', p39, re.S)
print('--- p. 39 note 3 tail: ...', m.group(0)[-170:].replace('\n', ' / '))
p40 = page('40')
print('    p. 40 body has "sprzedali, inwentarz"?',
      'sprzedali, inwentarz' in p40)

p103 = page('103')
m = re.search(r'\[\^103-3\]: .{0,4000}', p103, re.S)
print('--- p. 103 note 3 tail: ...', m.group(0)[-140:].replace('\n', ' / '))
p104 = page('104')
print('    p. 104 body has "dass wir"?', 'dass wir' in p104)

p116 = page('116')
m = re.search(r'\[\^116-5\]: .{0,4000}', p116, re.S)
print('--- p. 116 note 5 tail: ...', m.group(0)[-150:].replace('\n', ' / '))
p117 = page('117')
print('    p. 117 body has "metryki protestanckie"?',
      'metryki protestanckie' in p117)

print('--- p. 49 note 1 (new):')
m = re.search(r'\[\^49-1\]: .{0,200}', p49, re.S)
print('   ', m.group(0)[:180].replace('\n', ' / '))

p14 = page('14')
m = re.search(r'\[\^14-1\]: .{0,180}', p14, re.S)
print('--- p. 14 note 1 (merged sigla):')
print('   ', m.group(0)[:180].replace('\n', ' / '))
print('    p. 14 body still has "Tp. 75"?', 'Tp. 75' in p14)

p99 = page('99')
m = re.search(r'\[\^99-1\]: .{0,160}', p99, re.S)
print('--- p. 99 note 1 (new):')
print('   ', m.group(0)[:170].replace('\n', ' / '))
print('    "i serwitutów" in body?', 'i serwitutów' in p99)
print('    Grimm note: ', re.search(r'\[\^99-2\]: .{0,110}', p99, re.S)
      .group(0).replace('\n', ' / '))

p20 = page('20')
m = re.search(r'\[\^20-1\]: .{0,120}', p20, re.S)
print('--- p. 20 note 1 (new):')
print('   ', m.group(0)[:130].replace('\n', ' / '))

p118 = page('118')
m = re.search(r'\[\^118-1\]: .{0,140}', p118, re.S)
print('--- p. 118 note 1 (crafted):')
print('   ', m.group(0)[:150].replace('\n', ' / '))
