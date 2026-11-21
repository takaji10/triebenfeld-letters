# -*- coding: utf-8 -*-
"""Cross-check the TOC: find each heading's actual [p. N] in the draft
body (the print's own pagination) and print it next to the TOC's
candidate number reads."""
import re

t = open(r'literature\rusinski1947\original.md', encoding='utf-8').read()

HEADS = [
    ('Wykaz skrótów', ['V?']),
    ('Wiadomości wstępne', ['1', '?']),
    ('A. Temat, zakres pracy', ['1', '?']),
    ('B. Geneza', ['6', '3?']),
    ('C. Charakterystyka osad', ['12', '?']),
    ('Rozdział I', ['17', '?']),
    ('Rozdział II', ['27', '22?']),
    ('Stosunki demograficzne', ['27', '22?']),
    ('Rozdział III', ['31', '37?']),
    ('Stosunki prawne osad', ['31', '?']),
    ('1. Stosunek prawny do pana', ['40', '?']),
    ('2. Prawo rzeczowe', ['43', '?']),
    ('3. Prawo spadkowe', ['49', '?']),
    ('4. Samorząd gminny', ['50', '?']),
    ('Rozdział IV', ['55', '?']),
    ('A. Topografia osad', ['55', '?']),
    ('1. Topografia osad', ['55', '?']),
    ('2. Formy osadnictwa', ['56', '?']),
    ('3. Budownictwo', ['57', '?']),
    ('B. Skład zawodowy', ['58', '?']),
    ('1. Skład zawodowy', ['58', '?']),
    ('2. Skład społeczny', ['60', '?']),
    ('C. Poszczególne działy gospodarstwa', ['65', '?']),
    ('1. Rolnictwo', ['65', '?']),
    ('4. Przemysł', ['76', '?']),
    ('5. Handel', ['79', '?']),
    ('6. Inne zawody', ['80', '?']),
    ('D. Prawa użytkowe', ['80', '?']),
    ('E. Niestałe świadczenia', ['83', '?']),
    ('F. Powinności dworskie', ['84', '?']),
    ('1. Czynsze', ['84', '?']),
    ('a. Czynsze pieniężne', ['91', '?']),
    ('4. Inne obciążenia na rzecz dworu', ['93', '?']),
    ('a. Przymus propinacyjny', ['94', '?']),
    ('b. Przymus mlewa', ['95', '?']),
    ('5. Służebności dworskie', ['95', '?']),
    ('G. Powinności kościelne', ['104', '?']),
    ('H. Powinności publiczne', ['107', '?']),
    ('I. Ogólna sytuacja gospodarcza', ['109', '?']),
    ('Rozdział V', ['110', '?']),
    ('Kultura duchowa', ['111', '?']),
    ('A. Typ psychiczny', ['112', '?']),
    ('B. Szkolnictwo', ['113', '?']),
    ('C. Kult religijny', ['117', '?']),
    ('Uwagi końcowe', ['121', '?']),
    ('Aneksy', ['123', '?']),
    ('Plany osad', ['157', '?']),
    ('Mapa', ['?', '?']),
]

pages = [(m.start(), int(m.group(1)))
         for m in re.finditer(r'\[p\. (\d+)\]', t)]
toc_i = t.find('[p. 1]')  # the body starts after the front matter


def page_of(pos):
    best = None
    for start, num in pages:
        if start <= pos:
            best = num
        else:
            break
    return best


for head, cands in HEADS:
    # search only in the body (after [p. 1])
    i = t.find('\n' + head, toc_i)
    if i < 0:
        i = t.find(head, toc_i)
    pg = page_of(i) if i > 0 else None
    print('%-38s body p.%-4s toc-cands %s' % (head[:38], pg, cands))
