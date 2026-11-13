# -*- coding: utf-8 -*-
"""Write intake/index.csv from the settled reading of the index (review/apl399801333/final.json).

Run once (2026-11-13); kept as the record of how index.csv was made. index.csv
is the source from then on: correct it there, not here. The conversions:
doubt marks from "word[?]" to the edition's "[word?]"; the English of the
entries whose doubt marks or names were settled after the review sheet
(Hohm, from the colonists' petition of 1867 signed "Daniel Hohm"; the
edition's forms Nowawies and Commissioner).
"""
import csv, io, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
rows = json.load(io.open(os.path.join(ROOT, 'review', 'apl399801333', 'final.json'), encoding='utf-8'))

def doubt(s):
    s = s.replace('Секретарь Бер[?]', 'Секретарь [Бер…?]')
    return re.sub(r'([^\s\[\]]+?)\s?\[\?\]', r'[\1?]', s)

E = {'45': 'Draft of an outgoing letter to the Commissioner of the [бер.?] district, [Vladimirov?], 23 May 1867, no. 1748',
     '47': 'Valuation table of the house of the [former?] servants in the village of Marianton',
     '48': 'Two plans: of the village of Marianton and of the house of the [former?] servants',
     '68': "Petition of the peasant Ferdinand [Werding?], with a [certificate?] of the gmina's wójt, 24 Nov/6 Dec 1864",
     '72': 'Petition of Jasińska and [Rymarska?], 1/13 August 1865',
     '89': 'Petition of Zelmer and Hohm, 10 September 1868',
     '90': 'Petition of Gośka and Hohm, 21 September/3 October 1868',
     '91': 'Petition of Wilhelm Hohm, 15/27 January 1868, with documents',
     '102': 'Petition of the colonists of the village of [Łazińsk?], with a postal receipt, 6/18 December 1867',
     '106': 'Petition of Ferd. Werdin, 18/30 June 1868, with an endorsement, no. 3912',
     '118': 'Draft of an outgoing letter to the Upr. [Kom.?], 30 April 1869, no. 2731',
     '126': 'Draft of an outgoing letter to the [Upr.?] Kom., 24 July 1869, no. 4380',
     '': 'Secretary [Ber…?]'}
N = {'90': "first surname Госьки or Госки; Гома is Hohm (the colonists' petition of 1867, folio 163, is signed Daniel Hohm)"}

out = io.open(os.path.join(HERE, 'index.csv'), 'w', encoding='utf-8', newline='')
w = csv.writer(out, lineterminator='\n')
w.writerow(['page', 'no', 'russian', 'leaves', 'folio', 'english', 'reading', 'note'])
for e in rows:
    no = e['no']
    en = E.get(no, doubt(e['english'])).replace('Nowa Wieś', 'Nowawies').replace('Commissar of', 'Commissioner of')
    w.writerow(['%04d_a' % int(e['image'][-7:-4]), no, doubt(e['russian']), e['leaves'], e['folio'], en,
                e['status'], N.get(no, e['note'])])
out.close()
print(len(rows), 'rows')
