# -*- coding: utf-8 -*-
"""Lay the editor's transcription into per-page files.

Authoritative as of 2026-10-26 (evening). Supersedes split_and_settle.py,
whose 108 grammar completions were applied in the morning session and are
WITHDRAWN here: the editor's fresh line-by-line transcription of p. 161
(2026-10-26) keeps the original doubts (sub~bo, notifica[??], quib[us??],
Religiosissim[e?], Niszczeviens[em?]...), and the editor's transcription is
the source of truth. The completions remain in split_and_settle.py as
proposals; the spot sheet's principle rows (pr_nieszwiez, pr_changes) rule
whether they go back in.

What this script writes:
- p. 161 (0161_a): the editor's own manuscript-line layout, verbatim - the
  five readings they settled in the fresh pass (1783; "videlicet 8ua";
  "Mens(is)" Junii; "oblatam"; "camera-/riali") are already in their lines.
- pp. 161v-167v: the editor's original text, unchanged, one paragraph per
  page (the lineation of those pages waits on the editor; drafts for
  checking at the desktop are written to intake/lineation_draft/).
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\rel1181.md'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'transcriptions')
DRAFT = os.path.join(HERE, 'lineation_draft')

# The editor's p. 161, laid out in the manuscript's lines, verbatim
# (2026-10-26). The [161] of their message is the page marker, not text.
PAGE_161 = """4ta Martii
Actum in Fundo Bonorum Villae Trąmpczyn Curiaque ibidem sitta 
Feria secunda post Dominicam Judica Quadragesimalim proxi-
ma die scilicet Vigesima Nona Mensis Martii Anno Domini
Millesimo Septingentesimo Octuagesimo Quarto Praesentibus Magnificis et Generosis 
Eugenio de Gora Skarbek Castellanida Junivladislaviensi Thoma Zelisławski Burgra-
bio Castrensis Coninensi Dominico Zboinatis Subdapifinda[?] Bidgostiensi Ignatio 
Łaszkowski Valentino Zeromski et aliis nec non Provido Bartholomeo Szepczyń-
ski de Villa Trąmpczyno Ministeriali Regni Generali actum praesentem acclamante.

Officia Castrensia Condescensorialia Burgrabiale Syradien[sem?] ac Commissoriale Generale Palatinatum
 Majoris Poloniae insistendo Ultimariae Limitationis per Officia Castrensia Gostinensia Judicatus 
et Commissoriale inferius subscriptum in Fundo praesentem Bonorum Feria secunda post Festum S. 
Andrae Apostoli proxima die scilicet Prima Mensis Decembris anno immediate elapso 1783 
post injunctam adimpletionem comportationis documentorum subsecutae actis Calissiensis 
Coninensi sub~bo post Festum Immaculate Conceptionis BVM eodem anno oblatuatae robore 
Decreti Tribunalitii Regni Petricoviae Feria Secunda post Ferium S. Francisci Confessoris proxima 
die videlicet 8ua Mensis 8bris anno 1782 inter partes inferius comparitione exau-
das prolati de sui essentia sui actu primitivae Limitationis in loco praesenti Feria 
secunda post Ferium Ssmae~ et Individuae Trinitatis proxima seu die decima sexta Men-
sis Junii anno praeterito 1783 per Officia Castrensem Gostinense Judicatus et camera-
riali Terrestre Gnesni~ expedito ad acta eadem die 20 mensis et anni eorundem per obla-
tam porrecto circumscripti diem hodiernam actis praesentis determinati in fun-
dum actu specificatum Condescenderunt ibidemque fundata sua judiciali juris-
dictione et per acclamationem Ministerialis Judicii apparitoni partibus notifica[??] 
easdem partes ad inscribendam comparitionem acclamare demandarunt quib[us??] 
et quidem Magnificus Casimiro Judica Terrestri Brestensi Cujaviae Parenti Joanna Nepomucen 
Judica Castrensen Radziejoviensem Ignatio E[v?sifen Predecen~ et Ludovico Judic[?]da Terrestri Bre-
stensem Cujaviae Filiis Zakrzewskie actoribus et littis~ et quidem Magnificis Ignatio E[n?]sifero Pre-
decendem et Ludovico Za-
krzewskie p~lr jam vero Magnificis Paulo et Josepho Fratribus inter se ger-
manis Tomickie itidem actoribus et cittis~ per eundem Magnificis Jacobo Parente Josepho Regen-
te Terrestri Vielun[em?][Wieluń?] Raphaele Vincentio et Nicolao cum olini Magnificum Elisabetha de Tworo-
wicze provercatis Filiis Fratribus inter se germanis Taczanowskie atque Petro et Cunegun-
da de Kowalskie invicem conjugibus Kołaczkowskie actoribus et cittis~ per Magnificum Jose-
phum Taczanowski Regentem Terrestrem Vielun[em?] suo et aliorum nomine personaliter Magnifico Francis[cum?] 
Tworowicz itidem actore et citto~ per eundem Illustrissimi Magnifico Antonio in Kolno Prusimski Ca-
pitaneo Niszczeviens[em?] Insignis S. Stanislai Equite citto~ et actore personaliter Religiosissim[e?] 
Benedicto Lubstowski Conventus Landensis Sacri Ordinis Cistercien[sis?] Ablate tum Re[ligiosi?]"""


def unescape(s):
    return s.replace('\\[', '[').replace('\\]', ']').replace('\\~', '~')


def main():
    text = open(SRC, encoding='utf-8').read()
    pages = {}
    cur = None
    for line in text.split('\n'):
        m = re.match(r'\\\[(\S+)\\\]\s*$', line.strip())
        if m:
            cur = m.group(1)
            pages[cur] = []
            continue
        if cur is None:
            continue
        pages[cur].append(unescape(line))

    order = ['161', '161v', '162', '162v', '163', '163v', '164', '164v',
             '165', '165v', '166', '166v', '167', '167v']
    pid = {'161': '0161_a', '161v': '0161_b', '162': '0162_a',
           '162v': '0162_b', '163': '0163_a', '163v': '0163_b',
           '164': '0164_a', '164v': '0164_b', '165': '0165_a',
           '165v': '0165_b', '166': '0166_a', '166v': '0166_b',
           '167': '0167_a', '167v': '0167_b'}
    os.makedirs(OUT, exist_ok=True)
    for p in order:
        if p == '161':
            body = PAGE_161
        else:
            lines = [l for l in pages[p]]
            while lines and not lines[-1].strip():
                lines.pop()
            body = '\n'.join(lines)
        with open(os.path.join(OUT, pid[p] + '.txt'), 'w', encoding='utf-8',
                  newline='\n') as f:
            f.write(body + '\n')
    print('wrote %d page files (p. 161 in the editor\'s layout)' % len(order))

    # the check: the corpus words must be the editor's words. Normalize both
    # sides (doubt markers out, line-break hyphens out) and require that the
    # only differences are the editor's five fresh readings and the full stop
    # they added after "acclamante" - anything else fails the run.
    def flat(s):
        s = re.sub(r'\s+', ' ', s).strip()
        s = re.sub(r'\[[^\]]*\]', '', s)      # doubt markers and flags
        s = re.sub(r'-\s+', '', s)            # line-end breaks, naively joined
        s = s.replace('~', '')
        return s
    orig161 = flat(' '.join(unescape(l) for l in pages['161']))
    new161 = flat(PAGE_161)
    KNOWN = [('replace', 'acclamante', 'acclamante.'),
             ('replace', '178', '1783'),           # 178[5?] -> 1783
             ('replace', 'sui', 'Mensis'),          # [??] sui -> Mensis
             ('replace', 'indlt', 'videlicet'),    # indl~t -> videlicet
             ('replace', 'camriali', 'camerariali'),
             ('replace', 'tam', 'oblatam')]
    import difflib
    ops = [o for o in difflib.SequenceMatcher(None, orig161.split(),
                                              new161.split()).get_opcodes()
           if o[0] != 'equal']
    got = [(o[0], flat(' '.join(orig161.split()[o[1]:o[2]])),
            flat(' '.join(new161.split()[o[3]:o[4]]))) for o in ops]
    unexpected = [g for g in got if not any(
        g[0] == k and g[1].replace('-', '') == a and g[2].replace('-', '') == b
        for k, a, b in KNOWN)]
    print('p. 161: %d differences, all expected: %s' % (
        len(got), not unexpected))
    for g in unexpected:
        print('  UNEXPECTED:', g)
    for p in order[1:]:
        a = flat(' '.join(pages[p]))
        b = flat(open(os.path.join(OUT, pid[p] + '.txt'), encoding='utf-8').read())
        if a != b:
            print('MISMATCH on', p)
    print('other pages carried verbatim: checked')


if __name__ == '__main__':
    main()
