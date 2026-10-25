# -*- coding: utf-8 -*-
"""Update the edition guide's hand counts and the Poznań bullet for
APP 53/968/0/-/545, English and German. Run once, 2026-10-25.
"""
import io

p = 'site/reading-this-edition.md'
s = io.open(p, encoding='utf-8').read()
s = s.replace('The edition holds 619 documents on 2,011 pages, dated from 1173 to 1936.',
              'The edition holds 626 documents on 2,021 pages, dated from 1173 to 1936.')
old = ("a printed summons of 1860 in a lawsuit between the owner of\n"
       "  Trąbczyn and its colonists; and two notebooks of 1936 in which the historian Albert Breyer\n"
       "  wrote down what the German settlers of")
new = ("a printed summons of 1860 in a lawsuit between the owner of\n"
       "  Trąbczyn and its colonists; ten research sheets in which the historian Albert Breyer\n"
       "  collected the Polonised German surnames of the gmina Zagórów, with his excerpt of a\n"
       "  Breslau print of 1741 and his notes on how and why the names were changed; and two\n"
       "  notebooks of 1936 in which the historian Albert Breyer\n"
       "  wrote down what the German settlers of")
if old in s:
    s = s.replace(old, new)
    print('en bullet updated')
else:
    print('en bullet already updated or not found')
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

p = 'site/de/ueber-diese-edition.md'
s = io.open(p, encoding='utf-8').read()
s = s.replace('Die Edition enthält 619 Dokumente auf 2.011 Seiten aus den Jahren 1173 bis 1936.',
              'Die Edition enthält 626 Dokumente auf 2.021 Seiten aus den Jahren 1173 bis 1936.')
old = ("Vorladung von 1860 in einem Prozess zwischen dem Besitzer von Trąbczyn und dessen\n"
       "  Kolonisten, zwei Notizheften von 1936, in die der Historiker Albert Breyer")
new = ("Vorladung von 1860 in einem Prozess zwischen dem Besitzer von Trąbczyn und dessen\n"
       "  Kolonisten, zehn Arbeitsblättern, auf denen der Historiker Albert Breyer die\n"
       "  polonisierten deutschen Familiennamen der Gemeinde Zagórów sammelte, mit seinem\n"
       "  Auszug aus einem Breslauer Druck von 1741 und seinen Notizen, wie und warum die\n"
       "  Namen geändert wurden; zwei Notizheften von 1936, in die der Historiker Albert Breyer")
if old in s:
    s = s.replace(old, new)
    print('de bullet updated')
else:
    print('de bullet already updated or not found')
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
