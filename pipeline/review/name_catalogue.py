# -*- coding: utf-8 -*-
"""Exhaustive catalogue of every person and place name in the corpus, with the
variant spellings of each and a proposed canonical form.

Why this needs its own tool rather than the generic spelling audit: names break
every assumption that audit relies on. 527 of the 738 tokens that sit in name
position occur exactly once, so frequency proves nothing about them. A wrong
name is usually still a plausible name, so it never looks wrong. And plain edit
distance is the wrong metric -- `Köckritz` and `Koekritzsch` are four edits
apart but one misreading apart, while `Wien` and `Bier` are one edit apart and
unrelated.

So the method is anchored, not open-ended:

  1. SEED from what the project has already settled -- the canonical names in
     whos_who.md and CHANGELOG.md -- plus every token the corpus itself puts in
     an unambiguous name position ("Herr v. X", "nach X", "die X'schen Güter").
  2. STRIP German derivational morphology before comparing, so `Cosmarischen`,
     `Zagorower` and `Schlabrendorffschen` are recognised as inflections of a
     root rather than as rival spellings of it.
  3. MATCH the rest of the corpus against those roots with a Kurrent-weighted
     distance, where the confusions this hand actually produces are cheap and
     everything else is not.
  4. WITHHOLD anything that is also an ordinary German word, or that sits close
     to two different seeds -- those go to a separate review list rather than
     being proposed as fixes.

Output is a proposal. Nothing is applied.

    python name_catalogue.py
    python name_catalogue.py --max-dist 2.6      # widen the net
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, sys, os, re, csv, json, argparse, unicodedata
from collections import Counter, defaultdict
import unitlib
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UNIT = unitlib.one_unit(unitlib.unit_arg())
REPORT = os.path.join(ROOT, 'review', 'name_catalogue.md')
QUEUE = os.path.join(ROOT, 'review', 'name_catalogue.csv')

# ---------------------------------------------------------------- morphology

# German derivational and case endings that attach to a proper noun. Order
# matters: longest first, so `-ischen` is taken before `-en`.
SUFFIXES = ['ischen', 'ischer', 'isches', 'ische', 'schen', 'scher', 'sches',
            'sche', 'schi', 'isch', 'ern', 'ers', 'er', 'en', 'es', 'em', 'e',
            'n', 's']


def stem(w):
    """Strip one German ending, but never below a plausible name root."""
    for suf in SUFFIXES:
        if len(w) - len(suf) >= 4 and w.lower().endswith(suf):
            return w[:-len(suf)]
    return w


def fold(s):
    s = s.lower().replace('ſ', 's').replace('ß', 'ss')
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.replace('ł', 'l')


# ------------------------------------------------------- Kurrent distance

CHEAP = {frozenset(p) for p in [
    'nu', 'nm', 'um', 'ni', 'ur', 'nr', 'mw', 'ce', 'ea', 'ou', 'ao', 'bv',
    'bw', 'vw', 'bh', 'ck', 'kg', 'tl', 'td', 'fs', 'sf', 'ij', 'iy', 'jy',
    'pb', 'gq', 'kc', 'st', 'rn', 'ln', 'hk', 'dt', 'zs', 'cz', 'sz', 'ei',
    'oe', 'ae', 'ue', 'ya', 'ie', 'gj', 'lt', 'mn', 'vf', 'wv',
]}


def cost(a, b):
    return 0.4 if frozenset((a, b)) in CHEAP else 1.0


def dist(a, b, cap):
    if abs(len(a) - len(b)) > 3:
        return 99.0
    prev = [j * 0.8 for j in range(len(b) + 1)]
    for i in range(1, len(a) + 1):
        cur = [i * 0.8]
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            sub = prev[j - 1] + (0 if ai == b[j - 1] else cost(ai, b[j - 1]))
            cur.append(min(prev[j] + 0.8, cur[j - 1] + 0.8, sub))
        prev = cur
        if min(prev) > cap:
            return 99.0
    return prev[-1]


# ------------------------------------------------------------ seed harvest

PERSON_CUE = re.compile(
    r'(?:\bv\.?\s+|\bvon\s+|\bHerrn?\s+|\bH\.\s*|\bHl\.\s*|\bdH\.?\s*|\bdHl\.?\s*'
    r'|\bGraf(?:en)?\s+|\bGräfin\s+|\bFürst(?:in|en)?\s+|\bBaron\s+|\bFrau\s+'
    r'|\bMinister\s+|\bGeneral\s+|\bGen\.?\s+|\bObrist(?:en)?\s+|\bRath\s+'
    r'|\bJustiz\s+|\bDoctor\s+|\bDr\.\s*|\bProfessor\s+)'
    r'([A-ZÄÖÜ][^\W\d_]{2,})', re.UNICODE)

# "nach X" and "zu X" are strong place cues. "in X" / "von X" are not, because
# German capitalises every noun and those prepositions take ordinary nouns
# constantly ("in Ansehung", "von Geld"). The geography-marker form is the most
# reliable signal of all.
PLACE_CUE = re.compile(
    r'(?:\bnach\s+|\bzu\s+)([A-ZÄÖÜ][^\W\d_]{4,})'
    r'|([A-ZÄÖÜ][^\W\d_]{4,})(?=\s*(?:er\s+)?(?:Güter|Gütern|Kreis|Kreise|'
    r'Herrschaft|Vorwerk|Dominium|Starostey|Dorf|Stadt))', re.UNICODE)

# Articles, possessives and quantifiers. A German common noun takes these
# constantly; a place name essentially never does. Surnames in this register DO
# take them ("dem Hawich", "der Cosmar"), so a high rate can only veto a
# candidate, never nominate one -- which is why the settled canon is trusted
# outright rather than being put through this test.
ARTICLES = set('''der die das den dem des ein eine einen einem einer eines
mein meine meinen meinem meiner sein seine seinen seinem ihr ihre ihren ihrem
dieser diese dieses diesen diesem jener jene alle allen aller viele vieler
keine kein keinen unser unsere jeder jede jedes solche welche beide beiden
manche mancher'''.split())

WORD = re.compile(r'[^\W\d_]{3,}', re.UNICODE)

# Polish surname morphology. No German common noun ends this way, and these
# estates are in Posen and Kalisz, so a token of this shape is a person.
SLAVIC = re.compile(r'^[A-ZÄÖÜ][^\W\d_]*'
                    r'(?:ski|cki|wski|czyk|owicz|ewicz|icki|ynski|inski)$', re.UNICODE)

# Ordinary nouns that ride in on "zu X" / "nach X" -- German prepositional
# idiom, not place names ("zu Gunsten der Juden", "zu Füßen zu legen"). They
# have to be named because no statistic separates them: they are capitalised
# like every German noun and, inside a fixed phrase, take no article either.
NOT_NAMES = set('''Gunsten Rechts Rechte Füßen Fuße Wunsch Wünschen Stande
Grunde Ende Endes Theil Theile Folge Last Lasten Hause Hülfe Hilfe Zeiten Zeit
Sache Sachen Zwecke Zweck Kenntnis Kenntniß Protokoll Papier Papieren
Sicherheit Ansehung Erfüllung Bezahlung Zahlung Verfügung Rechenschaft Ordnung
Seite Seiten Ehren Willen Handen Händen Nutzen Nuzzen Schulden Kosten Gefallen
Tage Tagen Sinne Werke Ruhe Frieden Bette Tische Acten Akten Gelde Gelder
Geldern Hand Herzen Munde Statt Stelle Zufriedenheit Erkenntnis Vollmacht
Vollmachten Gericht Gerichte Casse Cassen Kasse Rath Rathe Rechnung Rechnungen
Antwort Bericht Berichte Schreiben Befehl Befehle Ordre Ordres Gnade Gnaden
Ehre Noth Nothdurft Zinsen Zinß Zins Güter Gütern Gut Gutes Herr Herrn Herren
Frau Fürst Fürsten König Königs Kayser Kaysers Majestät Durchlaucht Excellenz
Inspector Inspektor Ministerium Ministerin Gouvernement Gouverniment Prefect
Prefectur Praefectur Commission Comission Departement Collegium Regierung
Justiz Cammer Kammer Tribunal Senat Congress Congreß Bürgermeister
Burgemeister Kriegs Kriegen Krieg Kanzler Kanzlers Canzler Canzlers Minister
Ministers Gleich Gleiche Amtmann Oberamtmann Pächter Bauern Bauren
Staats Staat Kriegs Forst Hof Hofe Geheime Geheimen Ihren Ihnen Ihre Ihrem
Ihrer Euer Ewer Ewr Seiten Seite Dero Deren Denen Diener Knecht Bruder Vater
Mutter Sohn Tochter Schwester Gemahlin Wittwe Erben Erbe Herrschaft Hochwohl
Wohlgeboren Gnaden Excellenz Durchl Durchlauchtigster Gnädigster Gnädigſter
Gnädiger Hochzuverehrender Hochwohlgebohrner Lieut Lieutenant Capitain Major
Obrist Oberst Rittmeister Praesident President Referendarius Actuarius
Justizrath Kriegsrath Forstrath Hofrath Amtsrath Landrath Kreisrath
Waßer Wasser Abzug Boden Briefen Briefe Brief Wege Weges Werk Werth Werthes
Ufer Lande Landes Grenze Gränze Ansehen Stunde Stunden Mittag Abend Morgen
Nacht Jahre Jahren Monat Monate Woche Wochen Stück Stücke Summe Summen
Meliorationen Melioration Eingang Ausgang Anfang Ende Abschluß Vergleich
Verhandlung Verhandlungen Erklärung Erklärungen Bedingung Bedingungen
Hard Harde Graf Grafen Beym Beim Fond Fonds Halse Halsse Advocat Advocaten
Circa Moratorium Wuth Bureau Erer Finanz Gouverneur Jungen Sagen Banquier
Geheimer Hauses Haus Jemanden Staatskanzler Nachgiebigkeit Platz Schwammern
Korn Baum Baume Roth Koch Köch Kochen Pohle Pohlen Polen Advokat Notarius
Executor Sequester Sequestor Administrator Mandatarius Curator Vormund
Gläubiger Creditor Creditoren Debitor Schuldner Käufer Verkäufer Pächter
Arrende Arrenda Propination Revenue Revenuen Legat Testament Codicill'''.split())


def load_rulings():
    """Decisions already given, so a rebuild shows only outstanding work.

    Without this the catalogue re-proposes everything every time it runs, and
    the reviewer spends their attention re-reading conclusions they have
    already reached -- which is the fastest way to lose trust in the list.
    """
    p = os.path.join(ROOT, 'reference', 'name_rulings.json')
    if not os.path.isfile(p):
        return {}
    r = json.load(open(p, encoding='utf-8'))
    settled = {tuple(sorted(map(fold, pair)))
               for pair in r.get('settled_pairs', []) + r.get('locked_apart', [])}
    return {
        'suppress': {fold(t) for t in (r.get('applied', []) + r.get('rejected', [])
                                       + r.get('tracked_elsewhere', []))},
        'drop_seeds': {fold(t) for t in r.get('drop_seeds', [])
                       + r.get('tracked_elsewhere', [])},
        'settled_pairs': settled,
        'reclassify': r.get('reclassify', {}),
    }


def harvest_canon():
    """Canonical names the project has already settled."""
    seeds = set()
    p = os.path.join(ROOT, 'reference', 'whos_who.md')
    if os.path.isfile(p):
        for m in re.finditer(r'\*\*([^*]+)\*\*', open(p, encoding='utf-8').read()):
            for part in re.split(r'\s*/\s*|\s*,\s*', m.group(1)):
                part = re.sub(r'\([^)]*\)', '', part).strip()
                for tok in WORD.findall(part):
                    if tok[:1].isupper() and len(tok) >= 4:
                        seeds.add(tok)
    return seeds


# Places and names fixed in CHANGELOG.md / earlier phases that may not be
# bolded in whos_who.md.
EXTRA_SEEDS = """Triebenfeld Hohenlohe Ingelfingen Schlawenschitz Zagorowo
Trąbczyn Kopojno Krotoszyn Polajewo Kontopp Dyhrenfurth Warschau Königsberg
Berlin Breslau Wien Kalisch Posen Brieg Glogau Neuenstein Öhringen Sagan
Olesnica Swiątniki Radolin Lenschitz Konin Kaemen Oleśnica Brzechsta
Glenck Hawich Honrichs Cosmar Köckritz Schlabrendorff Stägemann Kircheisen
Hardenberg Metternich Talleyrand Scharnhorst Zerboni Massow Haugwitz Bülow
Höym Wedel Philippsborn Pochammer Chomanowski Urbanowski Plotow Schöler
Eberhard Goerne Blomberg Schenck Falkenhausen Kwilecki Grävenitz Knobelsdorff
Sobottendorff Rapacki Eysenhardt Prusimska Dąbska Moscinska Hecker Larisch
Amelang Sommer Voss Winzingerode Massenbach Hoym Sacken Bornstädt Stössel
Cabanis Prittwitz Zastrow Weigel Meyer Bernhard Kleist Radecki Michalski
Rembowski Lombardini Thiel Congress""".split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--max-dist', type=float, default=1.8)
    ap.add_argument('--cue-rate', type=float, default=0.15,
                    help='discovered seeds must sit in name position this often')
    ap.add_argument('--article-max', type=float, default=0.30,
                    help='reject anything preceded by an article this often')
    ap.add_argument('--min-seed', type=int, default=3,
                    help='a seed must occur at least this often to anchor a cluster')
    a = ap.parse_args()

    rulings = load_rulings()
    recs = json.load(open(os.path.join(ROOT, 'corpus', 'letters.json'), encoding='utf-8'))
    scans = {}
    mp = os.path.join(UNIT.dir, 'page_scan_map.csv')
    if os.path.isfile(mp):
        for r in csv.DictReader(open(mp, encoding='utf-8-sig')):
            scans[(r['letter'], r['page'])] = r.get('image', '')

    # ---- corpus index -----------------------------------------------------
    freq = Counter()
    lower_freq = Counter()
    where = defaultdict(list)
    cue_person, cue_place = Counter(), Counter()
    art = Counter()

    for r in recs:
        lid = str(r['letter_id'])
        for p in r['pages']:
            pg = str(p['page'])
            txt = p.get('transcription') or p['diplomatic']
            for ln_no, line in enumerate(txt.split('\n')):
                toks = WORD.findall(line)
                if toks and line.rstrip().endswith(('-', '¬')):
                    toks = toks[:-1]
                for i, t in enumerate(toks):
                    freq[t] += 1
                    if t[:1].isupper() and i:
                        if toks[i - 1].lower().rstrip('.') in ARTICLES:
                            art[t] += 1
                    if t[:1].islower():
                        lower_freq[fold(t)] += 1
                    if len(where[t]) < 6:
                        where[t].append((lid, pg, line.strip()[:70]))
                for m in PERSON_CUE.finditer(line):
                    cue_person[m.group(1)] += 1
                for m in PLACE_CUE.finditer(line):
                    cue_place[m.group(1) or m.group(2)] += 1

    caps = {t: n for t, n in freq.items() if t[:1].isupper() and len(t) >= 4}
    print(f'corpus: {len(freq):,} distinct tokens, {sum(freq.values()):,} total')
    print(f'        {len(caps):,} capitalised types >=4 chars')
    print(f'        {len(cue_person):,} in person position, {len(cue_place):,} in place position')

    # ---- seeds ------------------------------------------------------------
    def article_rate(t):
        return art.get(t, 0) / freq[t] if freq.get(t) else 0.0

    def cue_rate(t):
        return (cue_person.get(t, 0) + cue_place.get(t, 0)) / freq[t]             if freq.get(t) else 0.0

    # The canon is already adjudicated - accept it as given. It carries exactly
    # the names the statistics cannot see, such as Hawich and Honrichs, which
    # this register writes with an article and almost never with a title.
    canon = {s for s in harvest_canon() | set(EXTRA_SEEDS)
             if freq.get(s, 0) > 0 and s not in NOT_NAMES
             and stem(s) not in NOT_NAMES}

    # Everything else has to earn a place: cued as a name often enough, and not
    # behaving like an ordinary noun.
    # Polish surnames are the one case where morphology alone is decisive: no
    # German common noun ends in -ski/-cki/-owicz, and these estates sit in
    # Posen and Kalisz, so such a token is a person essentially without
    # exception. Requiring a title cue misses them, because the letters name
    # them bare - "Weder Trzcinski, Zerboni, noch Koenig". Trzcinski scored a
    # cue-rate of 0.14 against a 0.15 threshold and fell out by one hundredth,
    # while 68 of the 80 tokens of this shape were never seeded at all.
    # The article veto is deliberately NOT applied to the Slavic branch. This
    # register takes articles with surnames as a matter of course ("dem Hawich",
    # "der Cosmar"), so at two occurrences a single "der X" pushes the rate to
    # 50% and vetoes a perfectly good name -- which is how Smiedecki, Chwalowski,
    # Szczucki, Zglinski and others were being dropped. Where the suffix already
    # settles it, the veto has nothing left to protect against.
    discovered = {t for t in caps
                  if t not in canon
                  and t not in NOT_NAMES
                  and stem(t) not in NOT_NAMES
                  and ((SLAVIC.match(t) and freq[t] >= 2)
                       or (freq[t] >= a.min_seed and cue_rate(t) >= a.cue_rate
                           and article_rate(t) < a.article_max))}
    seeds = canon | discovered
    if rulings.get('drop_seeds'):
        before = len(seeds)
        seeds = {t for t in seeds if fold(t) not in rulings['drop_seeds']
                 and fold(stem(t)) not in rulings['drop_seeds']}
        print(f'        {before - len(seeds)} seeds dropped by name_rulings.json')
    print(f'        {len(canon)} from the settled canon, '
          f'{len(discovered)} discovered and vetted')
    # The place field is now derived from datelines and is reliable, so use it
    # to type seeds rather than relying on cue counts alone, which put Wien and
    # Krotoszyn under 'person' because "nach X" and "Herr v. X" both fire.
    # Estates and towns that appear in prose but never as a dateline, so the
    # derived place field never sees them. German "von X" is genuinely ambiguous
    # between "Herr von Triebenfeld" and "von Krotoszin", so these are named.
    known_places = set('''Krotoszyn Zagorowo Trąbczyn Kopojno Polajewo Swiątniki
Kaemen Kolno Konin Slupce Peisern Radolin Lenschitz Olesnica Oleśnica Dyhrenfurth
Kontopp Grüneberg Glogau Neisse Küstrin Kempen Militsch Medzibor Schwarzwald
Warschau Petersburg Paris Dresden Erfurt Prag Frankfurt Öhringen Ingelfingen
Neuenstein Sagan Bartenstein Blizanow Betsche Posen Brieg Breslau Berlin Wien
Kalisz Schlawenschitz Königsberg Neustadt Wrąbczyn Gostyszyn Miedzeritz
Preußen Preussen Sachsen Sachßen Würtemberg Wartemberg Italien Böhmen Hessen
Curland Kurland Thoren Oppeln Schlesien Pommern Rußland Russland Frankreich
Österreich Oesterreich Pohlen Polen Bayern Baiern Hannover Westphalen Holland
Szetlewek Swięcia Brzyze Kaemener Zagorower Trąbczyner'''.split())
    for r in recs:
        for part in re.split(r'\s+bey\s+|\s+a[.]?\s+d[.]?\s+', r.get('place') or ''):
            part = part.strip()
            if part:
                known_places.add(part)
                known_places.update(WORD.findall(part))

    kind = {}
    for s in seeds:
        if s in known_places:
            kind[s] = 'place'
            continue
        pc, lc = cue_person.get(s, 0), cue_place.get(s, 0)
        if pc == lc and SLAVIC.match(s):
            # named bare, so no cue either way - but the suffix settles it
            kind[s] = 'person'
            continue
        kind[s] = 'person' if pc > lc else ('place' if lc > pc else 'unknown')
    print(f'        {len(seeds):,} seed names '
          f'({sum(1 for v in kind.values() if v=="person")} person, '
          f'{sum(1 for v in kind.values() if v=="place")} place, '
          f'{sum(1 for v in kind.values() if v=="unknown")} unclassified)')

    # root -> the seed spelling(s) that share it
    for t, k in rulings.get('reclassify', {}).items():
        if t in kind:
            kind[t] = k

    seed_roots = defaultdict(set)
    for s in seeds:
        seed_roots[fold(stem(s))].add(s)

    # ---- match every capitalised token against the seed roots -------------
    clusters = defaultdict(list)      # seed -> [(token, n, dist)]
    ambiguous = []                    # token close to two different seeds
    seed_folded = {fold(stem(s)): s for s in seeds}

    suppress = rulings.get('suppress', set())
    n_suppressed = 0
    for tok, n in sorted(caps.items(), key=lambda x: -x[1]):
        if tok in seeds:
            continue
        if fold(tok) in suppress:
            n_suppressed += 1
            continue
        root = fold(stem(tok))
        if root in seed_folded:               # inflection of a seed, not a variant
            clusters[seed_folded[root]].append((tok, n, 0.0))
            continue
        if article_rate(tok) >= a.article_max:   # behaves like an ordinary noun
            continue
        hits = []
        for sroot, sname in seed_folded.items():
            if len(sroot) < 5:      # short names match everything; exact only
                continue
            # tolerance scales with length: two letters wrong in `Koekritzsch`
            # is one misreading, two letters wrong in `Wien` is a different word
            cap = min(a.max_dist, max(0.8, 0.18 * len(sroot)))
            d = dist(root, sroot, cap)
            if d <= cap:
                base = freq.get(sname, 0)
                if base >= max(a.min_seed, n * 3):
                    hits.append((d, sname))
        if not hits:
            continue
        hits.sort()
        if len(hits) > 1 and hits[1][0] - hits[0][0] < 0.5:
            ambiguous.append((tok, n, [(s, round(d, 1)) for d, s in hits[:3]]))
        else:
            clusters[hits[0][1]].append((tok, n, hits[0][0]))

    # Two established names a single misreading apart. Neither is rare, so the
    # rare-vs-common matching above never compares them -- which is exactly how
    # `Brzechsta` (36) and `Brzechta` (8) sat side by side unnoticed. These are
    # never auto-merged: the question "one person or two?" is the one the
    # project has already got wrong once, with Hawich and Honrichs.
    pairs = []
    slist = sorted(seeds)
    for i, s1 in enumerate(slist):
        r1 = fold(stem(s1))
        if len(r1) < 5:
            continue
        for s2 in slist[i + 1:]:
            r2 = fold(stem(s2))
            if len(r2) < 5 or abs(len(r1) - len(r2)) > 3:
                continue
            cap = min(a.max_dist, max(0.8, 0.18 * len(r1)))
            d = dist(r1, r2, cap)
            if d > cap:
                continue
            # One is the other plus a case ending (Amelung/Amelungs,
            # Betsch/Betschen). That is German grammar, not a rival spelling,
            # and putting it to the user as a decision wastes their attention.
            f1, f2 = fold(s1), fold(s2)
            if f1 == f2 or f1.startswith(f2) or f2.startswith(f1):
                continue
            if tuple(sorted((fold(s1), fold(s2)))) in rulings.get('settled_pairs', set()):
                continue
            pairs.append((d, s1, freq.get(s1, 0), s2, freq.get(s2, 0)))
    pairs.sort()
    if n_suppressed:
        print(f'        {n_suppressed} variants suppressed by name_rulings.json')

    # Export the vetted seeds so the website's people index is generated from
    # the same evidence rather than hand-curated. The hand list had 55 entries
    # and matched 54 of the 807 tokens sitting in person position -- Grotowski
    # (x15), Brzechsta (x29), Hardenberg (x24) and many others were simply
    # absent, so they were never highlighted anywhere on the site.
    export = []
    for s in sorted(seeds):
        n = freq.get(s, 0)
        if n < 2:
            continue
        infl = sorted({m[0] for m in clusters.get(s, []) if m[2] == 0})
        export.append({'name': s, 'kind': kind.get(s, 'unknown'), 'count': n,
                       'source': 'canon' if s in canon else 'discovered',
                       'inflections': infl[:12]})
    with open(os.path.join(ROOT, 'reference', 'name_seeds.json'), 'w',
              encoding='utf-8', newline='\n') as f:
        json.dump(export, f, ensure_ascii=False, indent=1)
    kinds = Counter(e['kind'] for e in export)
    print(f'        exported {len(export)} seeds to name_seeds.json  {dict(kinds)}')

    write_report(clusters, ambiguous, pairs, freq, kind, where, scans,
                 seeds, canon, a)


def write_report(clusters, ambiguous, pairs, freq, kind, where, scans,
                 seeds, canon, a):
    rows, L = [], []
    A = L.append
    live = {s: v for s, v in clusters.items() if any(d > 0 for _, _, d in v)}
    n_var = sum(1 for v in live.values() for _, _, d in v if d > 0)

    A('# Name catalogue\n')
    A('Every person and place name in the corpus, its variant spellings, and a '
      'proposed canonical form. **Nothing here has been applied.**\n')
    A(f'- **{len(seeds):,} names** anchored on the canon already settled in '
      f'`whos_who.md` and `CHANGELOG.md`, plus every token the corpus itself '
      f'puts in an unambiguous name position.\n'
      f'- **{n_var} variant spellings** proposed as transcription errors, across '
      f'**{len(live)} names**.\n'
      f'- **{len(pairs)} pairs of established names** that sit one misreading '
      f'apart and need a one-entity-or-two decision.\n'
      f'- **{len(ambiguous)} tokens withheld** as ambiguous — each sits equally '
      f'close to two different names, and merging on a coin-flip is how two real '
      f'people become one.\n')
    A('Inflected forms (`Cosmarischen`, `Zagorower`, `Schlabrendorffschen`) are '
      'listed under their root and marked `inflection` — they are correct German '
      'and must not be "fixed". Only rows marked **fix** are proposals.\n')
    A('The `Scan` column is the image behind that page, for checking in '
      '`scan_review.html`.\n')

    A('\n## Proposed corrections\n')
    order = sorted(live.items(), key=lambda kv: (-freq.get(kv[0], 0), kv[0]))
    for seed, members in order:
        variants = sorted([m for m in members if m[2] > 0], key=lambda m: -m[1])
        if not variants:
            continue
        infl = [m[0] for m in members if m[2] == 0]
        tier = 'A — settled canon' if seed in canon else 'B — discovered'
        A(f'\n### {seed}  ×{freq.get(seed, 0)}  ({kind.get(seed, "unknown")}, '
          f'tier {tier})\n')
        if infl:
            A(f'*Inflected forms present (correct, not to be changed):* '
              f'{", ".join("`"+i+"`" for i in sorted(infl)[:12])}\n')
        A('| Variant | × | Action | Distance | Where | Scan |')
        A('|---|---|---|---|---|---|')
        for tok, n, d in variants:
            w = where.get(tok, [])
            loc = ', '.join(f'L{l} p{p}' for l, p, _ in w[:3]) or '—'
            scan = scans.get((w[0][0], w[0][1]), '') if w else ''
            A(f'| `{tok}` | {n} | **fix → `{seed}`** | {d:.1f} | {loc} | '
              f'`{scan}` |')
            for l, p, ctx in w[:2]:
                rows.append({'canonical': seed, 'variant': tok, 'count': n,
                             'kind': kind.get(seed, 'unknown'),
                             'distance': round(d, 2), 'letter': l, 'page': p,
                             'scan': scans.get((l, p), ''), 'context': ctx})

    A('\n## Established names that may be the same person or place\n')
    A('Both spellings are common enough that neither looks like a slip, so the '
      'matching above never compares them — yet they are one misreading apart. '
      'Each needs a decision that only the manuscript and the context can '
      'settle: **one entity, or two?** Nothing here is proposed as a fix. This '
      'is the shape of the mistake the project nearly made once already, when '
      '`Hawich` and `Honrichs` were almost merged and turned out to be two '
      'different men.\n')
    if pairs:
        A('| Name A | × | Name B | × | Distance | Question |')
        A('|---|---|---|---|---|---|')
        for d, s1, n1, s2, n2 in pairs:
            hi, lo = (s1, s2) if n1 >= n2 else (s2, s1)
            A(f'| `{s1}` | {n1} | `{s2}` | {n2} | {d:.1f} | '
              f'same entity → `{hi}`, or genuinely distinct? |')
            rows.append({'canonical': '', 'variant': f'{s1} / {s2}',
                         'count': n1 + n2, 'kind': 'SEED-PAIR',
                         'distance': round(d, 2), 'letter': '', 'page': '',
                         'scan': '', 'context': f'{s1} x{n1} vs {s2} x{n2}'})
    else:
        A('*None.*\n')

    A('\n## Withheld — ambiguous between two names\n')
    A('Each of these is close to more than one established name. The project has '
      'already been burned once by nearly merging `Hawich` into `Honrichs`, so '
      'these are listed for your eye and the scan, not proposed.\n')
    if ambiguous:
        A('| Token | × | Candidates | Where | Scan |')
        A('|---|---|---|---|---|')
        for tok, n, cands in sorted(ambiguous, key=lambda x: -x[1]):
            w = where.get(tok, [])
            loc = ', '.join(f'L{l} p{p}' for l, p, _ in w[:2]) or '—'
            scan = scans.get((w[0][0], w[0][1]), '') if w else ''
            cs = ', '.join(f'`{s}` ({d})' for s, d in cands)
            A(f'| `{tok}` | {n} | {cs} | {loc} | `{scan}` |')
            rows.append({'canonical': '', 'variant': tok, 'count': n,
                         'kind': 'AMBIGUOUS',
                         'distance': cands[0][1] if cands else '',
                         'letter': w[0][0] if w else '', 'page': w[0][1] if w else '',
                         'scan': scan,
                         'context': f'candidates: {cs}'})
    else:
        A('*None.*\n')

    with open(REPORT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    with open(QUEUE, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, ['canonical', 'variant', 'count', 'kind',
                               'distance', 'letter', 'page', 'scan', 'context'])
        w.writeheader(); w.writerows(rows)
    print(f'\n{n_var} proposed fixes across {len(live)} names')
    print(f'{len(pairs)} seed pairs needing a one-entity-or-two decision')
    print(f'{len(ambiguous)} withheld as ambiguous')
    print(f'wrote {REPORT}')
    print(f'wrote {QUEUE}')


if __name__ == '__main__':
    main()
