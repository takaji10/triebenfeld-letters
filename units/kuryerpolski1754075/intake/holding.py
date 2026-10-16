# -*- coding: utf-8 -*-
"""BK PAN Cz2271, Kuryer Polski 1754, nr 75: from the editor's image to the edition.

    python units/kuryerpolski1754075/intake/holding.py            # check only
    ... --crop        copy the page image into raw_dir/processed/ as 0002_a.jpg
    ... --write       page file and corpus.txt from TEXT
    ... --english     write translation/doc1.yml from ENGLISH
    ... --cache       put it into the translation cache
    ... --summaries   write the summaries S everywhere they are kept

This file is the record of what was done to this holding (2026-10-16). The
steps are those of courtbook.holding_main (pipeline/intake/courtbook.py).

The first holding from print and from a library. The editor gave the issue's
three images from the Wielkopolska Digital Library (openings of two pages)
and their own crop of the left page of the second, which carries the report
from Kalisz on the funeral of Paweł Prusimski: from "Z Kalißa die 5. Decemb:"
to the end of the report three lines into the next column, before "Z
Jarosławia d. 11 Decemb:" (the editor). Only that report is transcribed; the
page's other news is not.

There was no transcription. The report was read from the crop, enlarged three
and six times, line by line as printed. The printer's letters are kept: the
long s (ſ), the ligature ß in "Kalißa" (the italic ſz), æ in "Sæcularis",
accented á. A word broken at the line end is "¬". Italic (the dateline,
Latin words, "Rozdrażewſkich") is not marked. One word is mostly lost to
faint printing: a stroke at the start and an italic i at the end before
"Sæcularis"; it is given as "[Cleri?]", the usual formula ("Cleri
Saecularis", the secular clergy), read with doubt.

"Konwent Łędzki", "Opat Łędzki" are the Cistercian convent and abbot of Ląd on
the Warta (the editor, 2026-10-16: "Lęd is indeed Ląd"). The Polish keeps the
print's form; the English and the summaries say Ląd.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
import courtbook  # noqa: E402

SLUG = 'kuryerpolski1754075'
REF = 'BK PAN Cz2271, Kuryer Polski 1754, nr 75'
RAW = r"J:\Documents\Archive\Genealogy\References\Kuryer Polski 1754, nr. 75"

SCANS = [('cz_02271_1754_kuryer_075_0002_0001_crop.png', None, '0002_a', None)]
LEAF = {'0002_a': 'the left page of the second image'}
DOCS = [(1, ['0002_a'])]
ROWS = []

# The report, line by line as printed: lines 1-23 in the left column, 24-26 at
# the head of the right.
TEXT = [
    'Z Kalißa die 5. Decemb: W Trąb¬',
    'czynie pięć mil od Kaliſza w Dobrach',
    'Dziedzicznych Jchmćw Pańſtwa Pru¬',
    'ſińſkich, odprawił ſię Akt Pogrzebo¬',
    'wy ś. p. Jmći Pana Pawłá Pruſińſkie¬',
    'go Szambelana J. K. Mći, przy zná¬',
    'czney frekwencyi Domow zkolligo¬',
    'wanych, [Cleri?] Sæcularis; XX. Cy¬',
    'ſterſow z Konwentu Łędzkiego. Zá¬',
    'proſzony ná Summę Jmć X. Gło¬',
    'wiecki Opat Łędzki, lecz nieſpo¬',
    'dziany mroz zatamował przebycie',
    'przez rzekę Wartę. Kazanie miał',
    'X. Prefekt Szkoł Coll: Kaliſkiego',
    'Societatis Jeſu. Oracyą Pogrzebo¬',
    'wą po Kondukcie Jmć Pan Antoni',
    'Pruſińſki Synowiec Rodzony. W',
    'Klaſztorach zaś bliſkich, iako to: w',
    'Pyzdrach, Koninie, Kaźmierzu, zá',
    'dyſpozycyą Jeymći Pani Katarzyny',
    'z Rozdrażewſkich Pruſińſkiey, pozo¬',
    'ſtałey Małżonki, odprawiły ſię tegoż',
    'dnia Exekwie z Wigiliami y liczne¬',
    'mi Mſzami, dla ſczupłości mieyſca',
    'w Kościele Parafialnym Trąbczyń¬',
    'ſkim.',
]

ENGLISH = (
    "From Kalisz, 5 December. At Trąbczyn, five miles from Kalisz, on the hereditary estate of the "
    "Honourable Prusimski family, the funeral of the late Honourable Paweł Prusimski, Chamberlain of His "
    "Royal Majesty, was held, with a large attendance of related houses, of the secular [uncertain: clergy] "
    "and of the Cistercian Fathers of the convent of Ląd. The Reverend Głowiecki, Abbot of Ląd, had been "
    "invited to sing the High Mass, but an unexpected frost prevented his crossing the river Warta. The "
    "sermon was preached by the Reverend Prefect of the schools of the College of the Society of Jesus at "
    "Kalisz. The funeral oration after the procession was given by the Honourable Antoni Prusimski, his own "
    "nephew. In the monasteries nearby, namely at Pyzdry, Konin and Kaźmierz, at the order of Her Grace "
    "Katarzyna Prusimska, born Rozdrażewska, his widow, exequies were held on the same day, with vigils and "
    "many Masses, for lack of room in the parish church of Trąbczyn."
)


def read_source():
    return {(1, '0002_a'): TEXT}


def english():
    return {1: [ENGLISH]}


S = {
 1: ('Ein Bericht aus Kalisch vom 5. Dezember 1754 in der Warschauer Zeitung Kuryer Polski, Nr. 75 von 1754, auf Polnisch. In Trąbczyn, fünf Meilen von Kalisch, auf den Erbgütern der Familie Prusimski (im Druck „Prusiński“), wurde das Begräbnis des verstorbenen Paweł Prusimski, Kammerherrn Seiner Königlichen Majestät, gehalten, in Anwesenheit vieler verschwägerter Häuser und der Zisterzienser des Konvents von Ląd. Der Abt von Ląd, Głowiecki, war zum Hochamt eingeladen, doch ein unerwarteter Frost hinderte ihn, die Warthe zu überqueren. Die Predigt hielt der Präfekt der Schulen des Jesuitenkollegs in Kalisch, die Leichenrede nach dem Kondukt sein leiblicher Neffe Antoni Prusimski. Auf Anordnung der Witwe, Katarzyna Prusimska, geborene Rozdrażewska, wurden am selben Tag in den nahen Klöstern von Pyzdry, Konin und Kaźmierz Exequien mit Vigilien und vielen Messen gehalten, weil in der Pfarrkirche von Trąbczyn nicht genug Platz war.',
     'A report from Kalisz of 5 December 1754 in the Warsaw newspaper Kuryer Polski, no. 75 of 1754, in Polish. At Trąbczyn, five miles from Kalisz, on the hereditary estate of the Prusimski family (the print has "Prusiński"), the funeral of the late Paweł Prusimski, Chamberlain of His Royal Majesty, was held, with many related houses and the Cistercians of the convent of Ląd present. The Abbot of Ląd, Głowiecki, had been invited to sing the High Mass, but an unexpected frost prevented his crossing the Warta. The sermon was preached by the prefect of the schools of the Jesuit college at Kalisz, and the funeral oration after the procession was given by his own nephew, Antoni Prusimski. At the order of the widow, Katarzyna Prusimska, born Rozdrażewska, exequies with vigils and many Masses were held the same day in the monasteries nearby, at Pyzdry, Konin and Kaźmierz, as there was not room enough in the parish church of Trąbczyn.'),
}
HOW = ('written in the working session from the Polish as read from the image\n# (intake/holding.py, 2026-10-16).')

if __name__ == '__main__':
    courtbook.holding_main(globals())
