# -*- coding: utf-8 -*-
"""The correction pass on III. HA MdA, III. Nr. 12366 (NEW_UNIT.md 3a), 2026-10-04.

    python units/iiihamdaiiinr12366/intake/rulings_corrections.py            # writes rulings_corrections.tsv
    python units/iiihamdaiiinr12366/intake/rulings_corrections.py --direct   # once: words that stand twice in a paragraph

The French of documents 1, 2, 4 and 5 is written in clean copy hands, and
every row here was read on the scan of its page: a typing slip in the
transcription, corrected to what the page has. Nothing was changed because
another word would make better sense. The writers' own spelling stays
(rénouveller, apartiennent, compromittre, tems, argumens), as do the Polish
names the editor wrote in their Polish form where the scribe did not
(Trąpczyn for "Trapczin", Dąbski for "Dobsky"). The editor's doubt mark is
dropped where the page is plain. Document 3, the ministry's draft, and
document 6, the Polish judgment, were not corrected: see unresolved.md.

Rows: (text that finds the line, old token, new token, reason). The lines are
paragraphs, so a word that stands twice in one is changed under DIRECT.
Five rows the applying tool refused (a word twice in its paragraph, a doubt
mark after a semicolon, two rows keyed to the wrong half of a paragraph cut
by a page) were made by hand on the same day; all are in
transcription_decisions.csv.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
CORPUS = os.path.join(os.path.dirname(HERE), 'corpus.txt')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

S = 'read on the scan'
ROWS = [
 # -- document 1: Alopeus to Bernstorff (0002)
 ('à Son Excellence Mnosieur', 'Mnosieur', 'Monsieur', 'a typing slip; "Monsieur" on the scan'),
 ('Le soussigné Envoyé Extraordinaire et Ministre Plénipotentiare de Sa Majesté L', 'Plénipotentiare', 'Plénipotentiaire', S),
 ('a en ordre de communique', 'communique', 'communiquer', S + ': "a eu ordre de communiquer"'),
 ('a en ordre de communique', 'se', 'le', S + ': "le rapport ci-joint"'),
 ('a en ordre de communique', 'rélatif[?]', 'rélatif', 'plain on the scan'),
 ('Ce rapport renferme', 'ayany', 'ayant', S),
 ('Ce rapport renferme', 'récuilli[?]', 'récueilli', S),
 # -- document 2: the Warsaw report (0003-0009)
 ('Les Commissaires Plénipotentiares', 'acif', 'actif', S + ': "la liquidation de l\'actif et du passif"'),
 ('L’objet de ces réclamations', 'Varovie', 'Varsovie', S),
 ('L’objet de ces réclamations', 'pr', 'par', S + ': "contractées par les donnataires"'),
 ('L’objet de ces réclamations', 'soix', 'soit', S),
 ('L’objet de ces réclamations', 'supputé[?]', 'supputé', 'plain on the scan'),
 ('L’objet de ces réclamations', 'chargé', 'charge', S + ': "à la charge du Gouvernement Prussien"'),
 ('Le mauvais état de sa santé', 'l’obligea[?]', 'l’obligea', 'plain on the scan'),
 ('maladie et de la mort de sa femme', 'désai[?]', 'délai', S + ': "proroger le délai fixé"'),
 ('maladie et de la mort de sa femme', 'mis', 'mais', S + ': "mais avant qu\'il ai pû"'),
 ('maladie et de la mort de sa femme', 'succomber', 'succomba', S),
 ('maladie et de la mort de sa femme', 'cherchez', 'chercher', S),
 ('Lors des changemens politiques', 'survinrent[?]', 'survinrent', 'plain on the scan'),
 ('Le Général Niemojewski et Wichrowsky', 'teurs[?]', 'leurs', S + ': "dans leurs propriétés respectives"'),
 ('Il résulte de là', 'en[?]', 'eu', S + ': "elle n\'aurait eu aucun sujet"'),
 ('disposa des susdit biens', 'néanmoins[?]', 'néanmoins', 'plain on the scan; the n is written in above'),
 ('disposa des susdit biens', 'ressortaient;[?]', 'ressortaient;', 'plain on the scan'),
 ('avait été fait, si', 'astreins[?]', 'astreins', 'plain on the scan'),
 ('3. Les droits de Mme.', 'Wichnowski', 'Wichrowski', S + '; the same man is "Wichrowsky" on 0006'),
 ('Wichnowski rentra en possession', 'Wichnowski', 'Wichrowski', S),
 ('jugea[?] convenable', 'jugea[?]', 'jugea', 'plain on the scan'),
 ('Que puisque le Gouvernement du çi-devant', 's’étair', 's’était', S),
 ('Que puisque le Gouvernement du çi-devant', 'reconnut[?]', 'reconnut', 'plain on the scan'),
 ('Que puisque le Gouvernement du çi-devant', 'néanmoins[?]', 'néanmoins', 'plain on the scan; the n is written in above'),
 ('Que puisque le Gouvernement du çi-devant', 'st', 'est', S + ': "il est hors de doute"'),
 ('les créanciers régleront', 'indeminté', 'indemnité', S),
 ('1. Que le dit Gouvernement dans attendre', 'dans', 'sans', S + ': "sans attendre que le Staroste"'),
 ('1. Que le dit Gouvernement dans attendre', 'prouse', 'prouve', S),
 ('2. Mme. Miączyńska en bus âge', 'bus', 'bas', S + '; "en bas âge" also on 0005'),
 ('de la tutelle de Mme.', 'redressant[?]', 'redressant', 'plain on the scan'),
 # -- document 4: Tarczewski (0012)
 ('Pour l’instruction, je me sens', 'sens', 'sers', S + ': "je me sers de copies simples"'),
 ('Pour l’instruction, je me sens', 'plaiser', 'plaider', S),
 ('Pour l’instruction, je me sens', 'indispensible', 'indispensable', S),
 # -- document 5: Schöler to Nesselrode (0013-0016)
 ('C’est bien à regret', 'acquiescen', 'acquiescer', S),
 ('C’est bien à regret', 'sacrificer', 'sacrifier', S),
 ('En se référant aux Notes', 'en', 'eu', S + ': "a eu l\'honneur d\'adresser"'),
 ('Le Staroste de Prusimski ayant pris part', 'furient', 'furent', S),
 ('Les intérêts de cette créances', 'créances', 'créance', S + ': "cette créance hypothécaire"'),
 ('Les intérêts de cette créances', 'hypothécaise', 'hypothécaire', S),
 ('1. Que l’arrêt de la Commission', 'servit', 'servir', S),
 ('2. Que, quand même il ne soit pas dit', 'constractées', 'contractées', S),
 ('2. Que, quand même il ne soit pas dit', 'c’acte', 'l’acte', S),
 ('3. Que les actes de donation', 'Gouvernment', 'Gouvernement', S),
 ('Le Négociant Weigel, après avoir interjeté', 'en', 'eu', S + ': "a eu l\'honneur de s\'adresser"'),
 ('Neuf mois s’étant', 'écoutés', 'écoulés', S),
 ('Neuf mois s’étant', 'expépiée', 'expédiée', S),
 ('Neuf mois s’étant', 'demura', 'demeura', S),
 ('Bienque le Soussigné', 'supèrier', 'supérieur', S),
 ('Il menerait trop loin', 'argument', 'argumens', S + ': "les argumens allégués"'),
 ('tenir aux lois', 'étrance', 'étrange', S),
 ('En attribuant un effet rétroactif', 'arisés', 'avisés', S),
 ('Non seulement ces tribuneaux', 'one', 'ont', S + ': "ont excédé les bornes"'),
 ('Non seulement ces tribuneaux', 'exiédé', 'excédé', S),
 ('Non seulement ces tribuneaux', 'quit', 'qui', S),
 ('Non seulement ces tribuneaux', 'em', 'en', S + ': "déjà en 1819"'),
 ('La paix de Tilsit', 'quit', 'qui', S + ': "ce qui suit"'),
 ('Kalisz, soit annulé', 'légitement', 'légitimement', S),
 ('Dans la ferme convistion', 'convistion', 'conviction', S),
 ('Dans la ferme convistion', 'rclamation', 'réclamation', S),
 ('Dans la ferme convistion', 'Gouvernmenet', 'Gouvernement', S),
 ('Dans la ferme convistion', 'se', 'ce', S + ': "ce qui paroit être le dessein"'),
]

# A word that stands more than once in its paragraph: (line key, old text with
# enough round it to be unique, new text, reason). Logged in notes.md.
DIRECT = [
 ('Que puisque le Gouvernement du çi-devant', 'équitable d’indeminser', 'équitable d’indemniser', S),
 ('Que puisque le Gouvernement du çi-devant', 'déterminés à indeminser', 'déterminés à indemniser', S),
 ('Le Soussigné, chargé par sa Cour', 'aussitôt qui possible', 'aussitôt que possible', S),
 ('En se référant aux Notes', 'Roi a en l’honneur', 'Roi a eu l’honneur', S),
 ('Dans la ferme convistion', 'créance, se qui', 'créance, ce qui', S),
 ('a en ordre de communique', 'a en ordre', 'a eu ordre', S),
]


def find(L, key):
    hits = [i for i, l in enumerate(L, 1) if key in l]
    if len(hits) != 1:
        sys.exit(f'{key!r}: found on {len(hits)} lines')
    return hits[0]


def main():
    L = open(CORPUS, encoding='utf-8').read().split('\n')
    if '--direct' in sys.argv:
        for key, old, new, _ in DIRECT:
            i = find(L, key)
            if L[i - 1].count(old) != 1:
                sys.exit(f'{old!r}: {L[i - 1].count(old)} times on line {i}')
            L[i - 1] = L[i - 1].replace(old, new)
            print(i, old, '->', new)
        with open(CORPUS, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(L))
        return
    rows = sorted((find(L, key), old, new, why) for key, old, new, why in ROWS)
    with open(os.path.join(HERE, 'rulings_corrections.tsv'), 'w', encoding='utf-8',
              newline='\n') as f:
        for r in rows:
            f.write('\t'.join(map(str, r)) + '\n')
    print(len(rows), 'rows')


if __name__ == '__main__':
    main()
