# -*- coding: utf-8 -*-
"""The spot sheet "Readings in Breyer's second notebook" (2026-10-14).

    python units/app539680669/intake/spot_sheet4.py
    python pipeline/review/queries.py --unit app539680669 --sheet readings4.csv

The readings of document 2 (notebook2.py) that a name, a place or the sense
of a note rests on, each with a picture of its line. Made with the machinery
of spot_sheet2.py; the pictures come from the page images in processed/,
which for this document are cut from the editor's photos.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spot_sheet2  # noqa: E402
from notebook2 import TEXT2  # noqa: E402

ROWS = [
    ('u01', '5194_a1', '[Verwand.?]', '[Verwand.?]', '[Verwand.?]|Verwand.',
     'The people who went to Russia "cleared the forest there, the ... then ...": read Verwand. (relatives) with doubt; the next two words were not read.'),
    ('u02', '5194_a1', '[katen?]', '[katen?]', '[katen?]|katen',
     '"Łazinsker Lehm-...": the end of the word on the next line, read katen (clay cottages) with doubt.'),
    ('u03', '5196_a2', '[Retzr.?]', '[Retzr.?]', '[Retzr.?]|Retzr.',
     'The settlers of the new settlement on forest land: "Bochenski 20 M., Kinast, Winterfeld, ..." A name written at the end of the line, read Retzr. with doubt; Retzläff follows on the next line.'),
    ('u04', '5197_a1', '[Kirschkacker?]', '[Kirschkacker?]', '[Kirschkacker?]|Kirschknacker',
     'A nickname after "Oberscher": read Kirschkacker with doubt. The other notebook has "Oborscher Kirschknacker".'),
    ('u05', '5197_a2', '[Birtz?]', '[Birtz?]', '[Birtz?]|Birtz',
     '"Herzfeld near Berlin: Robert ..., married there." A surname, read Birtz with doubt, with a word below it not read.'),
    ('u06', '5197_a2', '[Brudzyn?]', '[Brudzyn?]', '[Brudzyn?]|Brudzyń',
     'G. Merk sold 10 Morgen here and "bought in ... near Strzałkowo": a place, read Brudzyn with doubt.'),
    ('u07', '5198_a2', '[Rheinwochenmarkt?]', '[Rheinwochenmarkt?]', '[Rheinwochenmarkt?]',
     'In the old German script: "Es gibt auf ... im Dorfe?" Read Rheinwochenmarkt with doubt; the reading is not certain.'),
    ('u08', '5199_a1', '[Frucht?]sucht', '[Frucht?]', '[Frucht?]',
     'The whole page is in the old German script, after "Uneheliche Kinder viel." The second line: read "[Frucht?]sucht auf [Wanderschaft?]". The page is the hardest of the notebook.'),
    ('u09', '5199_a1', '[Sachsengänger?]', '[Sachsengänger?]', '[Sachsengänger?]|Sachsengänger',
     'The same page: "Die [Holländer?] ... gehen, die Mädchen bringen sehr oft Kinder mit." Read Sachsengänger (seasonal workers who went to Saxony) with doubt.'),
    ('u10', '5199_a1', '[Kosmatki?]', '[Kosmatki?]', '[Kosmatki?]|Kosmatki',
     'The same page, its last line: "Aus ... 50 Personen." A place, read Kosmatki with doubt.'),
    ('u11', '5199_a2', '[Sprachweizen?]', '[Sprachweizen?]', '[Sprachweizen?]',
     '"Otherwise even the ... perishes": a crop, read Sprachweizen with doubt (the first letters are unclear).'),
    ('u12', '5199_a2', '[Swirkhaber?]', '[Swirkhaber?]', '[Swirkhaber?]|Swirkhaber',
     '"The people of Łazinsk bought forest from Trompczyn C": its name in quotation marks, read Swirkhaber with doubt. Your English notes have "Swirkhaber".'),
    ('u13', '5200_a1', '[Servitut?]', '[Servitut?]', '[Servitut?]|Servitut',
     '"10 years ago Białobłoty and Orlin got ... of 4 Morgen": read Servitut with doubt.'),
    ('u14', '5202_a2', '[Koście…?]', '[Koście…?]', '[Koście…?]|Kościelec',
     '"Near Józefów a New World, a village, towards ...": a place, only "Koście" read.'),
    ('u15', '5203_a1', '[Siebzigjährige?]', '[Siebzigjährige?]', '[Siebzigjährige?]',
     'In the old German script, among sketches of grave boards: read Siebzigjährige with doubt, and the next line Dreissigjährige.'),
]
SHIFT = {'u02': 2, 'u06': -4, 'u10': 3, 'u11': 1, 'u12': 2.7, 'u13': 1.5, 'u14': 3, 'u15': 7.5}

if __name__ == '__main__':
    assert all(r[1] in TEXT2 for r in ROWS)
    spot_sheet2.TEXT.update(TEXT2)
    spot_sheet2.main(ROWS, SHIFT, 'readings4.csv')
