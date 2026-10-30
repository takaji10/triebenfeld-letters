# -*- coding: utf-8 -*-
"""One-off (2026-10-30): a short title for each holding whose translated name
is long, for the browser tab and the search results (the editor: the page
titles of the archival units should be shortened versions of the unit's name).
`short_title` / `short_title_de` in unit.yml, placed after card_title_de;
unit_pages.page_title uses them before the card title. The page's heading
keeps the whole translated name. Run once; the record is the commit.
Usage: python pipeline/review/set_short_titles.py [--apply]
"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

S = {
 'agad1174016': ('Governing Commission: register of resolutions', 'Regierungskommission: Register der Beschlüsse'),
 'agad11740273': ('Governing Commission: records from Dresden', 'Regierungskommission: Akten aus Dresden'),
 'agad118501169': ('Jurisdictional dispute: Miączyńska v. Weigel', 'Zuständigkeitsstreit: Miączyńska gegen Weigel'),
 'apl399806603': ('Liquidation table of Łazińsk', 'Liquidationstabelle von Łazińsk'),
 'app5314550221': ('Privileges of the monastery of Ląd', 'Privilegien des Klosters Ląd'),
 'app534062': ('Kalisz Land Court: Relationes 1726-1727', 'Landgericht Kalisz: Relationes 1726-1727'),
 'app536017': ('Konin Land Court: Inscriptiones 1589', 'Landgericht Konin: Inscriptiones 1589'),
 'app53640kalisztab21': ('Hearth tax of the Kalisz voivodeship 1789', 'Rauchfangsteuer der Woiwodschaft Kalisch 1789'),
 'app5371057': ('Hereditary-lease contracts, Trąbczyn forest', 'Erbpachtverträge, Trąbczyner Wald'),
 'app539680545': ('Polonised names, Zagórów commune', 'Polonisierte Namen, Gmina Zagórów'),
 'app539680716': ('Łazińsk: notes and statistics 1937', 'Łazińsk: Notizen und Statistik 1937'),
 'app539680782': ('Agreement with the teacher Samuel Adolph 1820', 'Vertrag mit dem Lehrer Samuel Adolph 1820'),
 'app539680783': ('Summons of Karolina Fridenberg 1860', 'Ladung der Karolina Fridenberg 1860'),
 'app539680801': ('Copies on the parcelling of Zagórów and Trąbczyn', 'Abschriften zur Parzellierung von Zagórów und Trąbczyn'),
 'ihagrrep7cnr3570': ('Deed of gift to Prince Hohenlohe-Ingelfingen', 'Schenkungsurkunde für Fürst Hohenlohe-Ingelfingen'),
 'ihagrrep7cnr3705': ('Hereditary lease of Oleszinia', 'Vererbpachtung des Gutes Oleszinia'),
 'ihagrrep7cnr3709': ('Complaint of Michalina von Prusinska', 'Beschwerde der Michalina v. Prusinska'),
 'iharep162nr295': ("Triebenfeld's capital of 50,000 Reichstaler, Vol. 1", 'Triebenfelds Kapital von 50 000 Reichstalern, Bd. 1'),
 'iiihamdaiiinr12366': ('Suit of Michalina von Miaczynska, Vol. 1', 'Klage der Michalina von Miaczynska, Bd. 1'),
 'iiihamdaiiinr12367': ('Suit of Michalina von Miaczynska, Vol. 2', 'Klage der Michalina von Miaczynska, Bd. 2'),
 'oe1bu14525': ('Gift of South Prussian estates to Hohenlohe-Ingelfingen', 'Schenkung südpreußischer Güter an Hohenlohe-Ingelfingen'),
 'oe1bu14526': ('Sale of South Prussian estates by Hohenlohe-Ingelfingen', 'Verkauf südpreußischer Güter durch Hohenlohe-Ingelfingen'),
 'oe1bu9454': ('Correspondence of Hohenlohe-Ingelfingen and Triebenfeld', 'Korrespondenz Hohenlohe-Ingelfingens mit Triebenfeld'),
 'oe1u199': ("Confirmation of Hohenlohe-Ingelfingen's majorat", 'Bestätigung des Majorats Hohenlohe-Ingelfingens'),
}


def q(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main():
    apply = '--apply' in sys.argv
    for slug, (en, de) in S.items():
        p = os.path.join(ROOT, 'units', slug, 'unit.yml')
        t = open(p, encoding='utf-8').read()
        assert 'short_title:' not in t, slug
        m = re.search(r'^card_title_de:.*\n', t, re.M)
        assert m, slug
        t = (t[:m.end()] + '# The title in the browser tab and in search results: a short form of the\n'
             '# translated name (the page\'s heading keeps the whole name).\n'
             f'short_title: {q(en)}\nshort_title_de: {q(de)}\n' + t[m.end():])
        print(slug, len(en), len(de))
        if apply:
            with open(p, 'w', encoding='utf-8', newline='\n') as f:
                f.write(t)


main()
