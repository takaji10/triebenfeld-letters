# -*- coding: utf-8 -*-
"""APP 53/20/0/-/Poznań Gr.1181 — split the editor's Markdown transcription into
per-page files and apply the readings settled in session (2026-10-26).

Rules followed (docs/EDITORIAL_RULES.md, docs/NEW_UNIT.md 3a):
- A reading is changed only where something proves it: the grammatical
  construction admits exactly one case; a fixed formula of the register; a
  form attested unflagged elsewhere in the same entry; or a form attested in
  the sibling units (Konin Gr.115-118, 153 - the same register family).
- The scribe's own spellings are kept (oblatuata, dicidenda, octuigentorum,
  fp, Castellanida, Trąmpczyn); his grammar is not tidied beyond the flagged
  word.
- What is not settled here keeps the editor's [?] mark and waits on the spot
  sheet (units/app5320pozgr1181/intake/spot_rows.py).

Every change is logged to changes_applied.md with its witness.
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\rel1181.md'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'transcriptions')

# ---------------------------------------------------------------- changes ---
# (page, old, new, witness) — applied verbatim, one occurrence unless the
# count is given.
CH = [
# --- page 161 ---
('161', r'sub\~bo', 'sab~bo',
 '13 Dec 1783 is the Saturday after the Immaculate Conception (8 Dec); "sab~bo" and "sabbo~" are written twice later in the entry (the second letter still to be confirmed on the crop - sheet row p_sabbo)'),
('161', r'notifica\[??\]', 'notificata', 'grammar: feminine participle with "apparitoni"'),
('161', r'quib\[us??\]', 'quibus', 'grammar'),
('161', r'cam\[??\]riali', 'camerali',
 'the cameral office of the formula; "officia camerarialia campestria", Konin Gr.153'),
('161', r'Religiosissim\[e?\]', 'Religiosissimo', 'dative with "Benedicto Lubstowski ... Abbate"'),
('161', r'Cistercien\[sis?\]', 'Cisterciensis', 'genitive with "Sacri Ordinis"'),
('161', r'Re\[ligiosi?\]', 'Religioso', 'dative with "Paulo Wybieralski ... Priore"'),
('161', r'Niszczeviens\[em?\] Insignis', 'Niszczeviensi Insignis', 'dative with "Capitaneo"'),
('161', r'Francis\[cum?\] Tworowicz', 'Franciscum Tworowicz', 'accusative with "citto~"'),
('161', r'Regente Terrestri Vielun\[em?\]\[Wieluń?\]', 'Regente Terrestri Vielunensi', 'dative with "Regente"; Wieluń as the editor glossed'),
('161', r'Regentem Terrestrem Vielun\[em?\]', 'Regentem Terrestrem Vielunensem', 'accusative with "Regentem"'),
# --- page 161v ---
('161v', r'quietatnis\[?\]', 'quietationis', 'the formula word; "quietationibus" recurs in the entry'),
('161v', r'haeren\[dem?\] em\[?\]lcantia', 'haerentis enucliantia',
 'the same phrase stands unflagged above: "onera super eisdem substantiis haerentis enucliantium"'),
('161v', r'Nieszczevicen\[em?\] existentia', 'Nieszczeviecensis existentia', 'genitive with "in archivo Illustrissimi ... Capitanei" (the sheet\'s principle row covers the Niszczewice endings)'),
('161v', r'Capitaneo Nieszczeviecen\[sem?\] ad summarium', 'Capitaneo Nieszczeviecensi ad summarium', 'dative with "Capitaneo" (the sheet\'s principle row)'),
# --- page 162 ---
('162', r'milliu\[?\] sexcentorum', 'millium sexcentorum', 'grammar: genitive with "centum septuaginta duorum"'),
('162', r'fp\[?\] jam vero', 'fp jam vero', 'the editor\'s own abbreviation, as unflagged instances write it'),
('162', r'octuigentorum\[?\]', 'octuigentorum', 'the scribe\'s spelling, now complete: 72,876 fl.'),
('162', r'fp\[?\] Generosi Raczycki', 'fp Generosi Raczycki', 'the editor\'s own abbreviation'),
('162', r'ha\[s?\] summas', 'has summas', 'grammar'),
('162', r'Radolensianorum\[?\]', 'Radolensianorum', 'genitive plural with "successorum"'),
('162', r'\[?\]lium quingentorum', 'millium quingentorum',
 'the figure 404,500: "quadringentorum quatuor millium quingentorum fp pro materna reputata" completes on 162v'),
('162', r'centu\[m?\] septuaginta', 'centum septuaginta', 'grammar: 174,785 fl.'),
('162', r'n\[?\] plus', 'nec plus', 'the "nec ... quam" construction'),
('162', r'summa\[m?\] centum', 'summam centum', 'accusative'),
('162', r'\[h/st?\]erilem\[?\] quo\~', 'sterilem quo~', 'the formula "sterilem decessum", used five times in the entry'),
('162', r'aucta\[?\]', 'aucta', 'grammar'),
('162', r'Wierzbno\[?\]', 'Wierzbno', 'the estate\'s name as elsewhere in the entry'),
('162', r'quadringentorum qu\[?\]', 'quadringentorum quatuor', 'the same figure on 162: "quadringentorum quatuor millium quingentorum"'),
# --- page 162v ---
('162v', r'\[di?\]cedendam', 'dicidendam', 'the scribe\'s own form, unflagged: "familli sexus dicidendam" three lines above'),
('162v', r'summi\[s?\] quoque', 'summis quoque', 'grammar'),
('162v', r's\[u?\]adentium', 'suadentium', 'grammar'),
('162v', r'cui\[?\]que \[f?\]aemello', 'cuique faemello', 'dative'),
('162v', r'aucti\[s?\]', 'auctis', 'ablative with "ex reparationibus ... proventibus"'),
('162v', r'Trium\[?\] Millium', 'Trium Millium', 'the 3,500 ducats as unflagged on 161v: "summa Trium Millium quingentorum aureorum"'),
('162v', r'quingentorum\[?\] aureorum', 'quingentorum aureorum', 'as above'),
('162v', r'Patruos\[?\]', 'Patruos', 'accusative'),
('162v', r'abalienasse\[?\]', 'abalienasse', 'grammar'),
('162v', r'executioni\[?\]', 'executioni', 'dative with "subjacens"'),
('162v', r'vice\[?\]', 'vice', 'ablative: "plus quam terna vice"'),
('162v', r'cuiq\[ue?\]', 'cuique', 'dative'),
# --- page 163 ---
('163', r'repositis\[?\]', 'repositis', 'ablative'),
('163', r'in\[i?\]tae', 'initae', 'feminine plural with "Divisionum Fraturnarum"'),
('163', r'cen\[?\] millium', 'centum millium', 'grammar: "septies centum millium" = 700,000'),
('163', r'altenius \[post/parte?\] sterilem', 'alterius post sterilem',
 '"altenius" is "alterius" (the second wadion); "post" from the sense - the wadion was constituted after the 1708 death it then secures'),
('163', r'complanationis\[?\]', 'complanationis', 'genitive with "in satisfactionem"'),
('163', r'Compro\[mis?\]soriali', 'Compromissoriali', 'the editor\'s completion; "Decreto Compromissoriali"'),
('163', r'successores\[?\]', 'successores', 'grammar'),
# --- page 163v ---
('163v', r'\[?\]ges\~', 'con~ges~', 'the scribe\'s suspension for "conjuges" (the sibling units write "conjuges" unflagged); the letters still to be confirmed on the crop - sheet row p_conges'),
('163v', r'Qui\[n?\]gentorum', 'quingentorum', 'grammar: 43,500 fl.'),
('163v', r'quadrungentorum\[?\]', 'quadrungentorum', 'the scribe\'s spelling, now complete: 7,400 fl.'),
('163v', r'eodem anno\[?\]', 'eodem anno', 'grammar'),
('163v', r'quaesita\[?\],', 'quaesita,', 'grammar'),
('163v', r'complanationibus\[?\]', 'complanationibus', 'ablative with "testantibus"'),
('163v', r'abrenunciationibus\[?\]', 'abrenunciationibus', 'ablative with "cum"'),
('163v', r'Brestensis\[?\]', 'Brestensis', 'genitive with "Judicis"'),
# --- page 164 ---
('164', r'Posnaniensis\[?\] Feria 2da ante', 'Posnaniensis Feria 2da ante',
 'the formula "coram actis Castrensis Posnaniensis" as the editor wrote it unflagged in Konin Gr.117'),
('164', r'17\[3?\]7 levasse', '1737 levasse', 'the same complanatio dated "anno 1737" unflagged on 163v'),
('164', r'Junioribus\[?\]', 'Junioribus', 'dative with "porrexisse"'),
('164', r'schaedam\[?\]', 'schaedam', 'the scribe\'s form, unflagged four times ("schaedas trinas", "Tertiam Schaedam")'),
('164', r'successionibus\[?\]', 'successionibus', 'dative'),
('164', r'eligisse\[?\],', 'eligisse,', 'perfect infinitive'),
('164', r'\[sch?\]edam', 'schedam', 'the editor\'s completion; "schaedam" as above'),
('164', r'\[?\]eclesiis', 'ecclesiis', 'the Latin word; "Ecclesiae Parochiali" unflagged twice in the entry'),
('164', r'su\[per/pra?\] bonis Trąmpczyna', 'super bonis Trąmpczyna', 'the formula "super bonis", used ten times in the entry'),
('164', r'pascuis\[?\]', 'pascuis', 'ablative'),
('164', r'eundem\[?\]', 'eundem', 'accusative'),
('164', r'cuique\[?\]', 'cuique', 'dative'),
# --- page 164v ---
('164v', r'assumpisse\[?\]', 'assumpisse', 'perfect infinitive'),
('164v', r'success\[or?\]ibus', 'successoribus', 'the editor\'s completion'),
('164v', r'marcis\[?\]', 'marcis', 'ablative'),
('164v', r'\[s/f?\]emuniis', 'semuniis', 'the scribe\'s form, unflagged twice ("semuniis quinque", "semuniis duodecem")'),
('164v', r'colo\[r?\]is', 'coloris', 'genitive'),
('164v', r'toti\[dem?\]', 'totidem', 'the editor\'s completion'),
('164v', r'Condescensoriale\[?\]', 'Condescensoriali', 'ablative with "Decreto"'),
('164v', r'acto\[?\] denique', 'actorum denique', 'the parallel "cittorum et actorum" stands unflagged two lines above'),
('164v', r'Covalien\[sis?\]\[Kowal\]', 'Covaliensis [Kowal]', 'nominative with "Tribuni"'),
('164v', r'Radziejovien\[sis?\]', 'Radziejoviensis', 'genitive with "Judicis Castrensis"'),
# --- page 165 ---
('165', r'part\[post?\] fata', 'post fata', 'the formula "post fata", used throughout the entry'),
('165', r'exa\[r?\]tis Bona', 'exaratis Bona', 'the stem "exar-" as the scribe writes it unflagged: "exarasse" on 165v'),
('165', r'Bonorum\[?\] arendae', 'Bonorum arendae', 'genitive'),
# --- page 165v ---
('165v', r'complanationem\[?\] cum eisdem', 'complanationem cum eisdem', 'accusative'),
('165v', r'sponsa\[b/l?\]itium', 'sponsalitium', 'the betrothal contract; "contractum sponsalitium"'),
('165v', r'inscripsisse\[?\]', 'inscripsisse', 'perfect infinitive'),
# --- page 166 ---
('166', r'pr\[e?\]tio Bonorum', 'praetio Bonorum', 'the Latin word'),
('166', r'\[3/E?\]tiam', 'Etiam', 'the editor\'s alternative'),
('166', r'N\[ostri?\]', 'Nostri', 'the formula "Domini Nostri Jesu Christi"'),
('166', r'siquidem\[?\]', 'siquidem', 'the parenthetical formula "(siquidem ... compensatum est)"'),
# --- page 166v ---
('166v', r'c\[a?\]pitibus', 'capitibus', 'ablative with "omissis"'),
('166v', r'com\[j/p?\]etere', 'competere', 'the editor\'s completion; "duos cum medio competere"'),
('166v', r'filiastro\[?\]', 'filiastro', 'ablative'),
('166v', r'adnumerat\[is?\]', 'adnumeratis', 'ablative'),
# --- page 167 ---
('167', r'litis\[?\]', 'litis', 'the formula "contestatio litis"'),
('167', r'censci\[?\]', 'censeri', '"non posse pro deportata censeri" - the same word, twice in this entry'),
('167', r'censcri\[?\]', 'censeri', 'as above'),
('167', r'Judiciu\[m?\]', 'Judicium', 'nominative with "existit"'),
('167', r'attinet\[?\]', 'attinet', 'verb'),
('167', r'videt\[um?\]', 'videtur', 'grammar'),
('167', r'Sae\[?\] Rae\[?\] Mttis\[?\]', 'Sae~ Rae~ Mttis~', 'the honorific as the scribe writes it unflagged: "sae~ Rae~ Mttis~ Succamarariis" on 162'),
# --- page 167v ---
('167v', r'Gnesnensis\[?\]', 'Gnesnensis', 'genitive'),
('167v', r'p\[er?\] Mle\~m', 'per Mle~m', 'preposition'),
('167v', r'propalasse\[?\]', 'propalasse', 'perfect infinitive'),
('167v', r'\[?\]isque ad finalem', 'usque ad finalem', '"quotam usque ad finalem decisionem"'),
('167v', r'aequ\[?\]sitam', 'acquisitam', 'the same stem as "ex acquisita per [eo?] substantia" on 162; "acquired beyond the division"'),
('167v', r'Vschova\[nis?\]', 'Vschoviensis', 'Wschowa: "Thesaurarius Vschovensius" unflagged in Konin Gr.117'),
('167v', r'autis\[?\] Castrensis', 'actis Castrensis', 'the formula "coram actis Castrensis", used four times in this entry'),
('167v', r'\[?\]ges', 'con~ges', 'the scribe\'s suspension for "conjuges" (the sibling units write "conjuges" unflagged); the letters still to be confirmed on the crop - sheet row p_conges'),
('167v', r'bonii\[?\]', 'bonis', 'grammar'),
]

# ------------------------------------------------------------- read source --
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
    pages[cur].append(line)

# unescape the editor's markdown escapes for the plain-text corpus files
def unescape(s):
    return s.replace('\\[', '[').replace('\\]', ']').replace('\\~', '~')

# The pages' ids: the archive's pagination as a four-digit capture, the side
# as the crop letter (a = recto, b = verso) - the pipeline's page-id shape
# (match_scans.py: four digits, crop a-h), which three-digit "161v" cannot
# ride on. 0161_a is p. 161, 0161_b is p. 161v, and so on to 0167_b.
PAGE_ID = {
    '161': '0161_a', '161v': '0161_b', '162': '0162_a', '162v': '0162_b',
    '163': '0163_a', '163v': '0163_b', '164': '0164_a', '164v': '0164_b',
    '165': '0165_a', '165v': '0165_b', '166': '0166_a', '166v': '0166_b',
    '167': '0167_a', '167v': '0167_b',
}

applied, missed = [], []
for page, old, new, why in CH:
    body = pages.get(page)
    if body is None:
        missed.append((page, old, 'no such page'))
        continue
    joined = '\n'.join(unescape(l) for l in body)
    cnt = joined.count(old.replace('\\[', '[').replace('\\]', ']')) if '\\' in old else joined.count(old)
    target = old.replace('\\[', '[').replace('\\]', ']').replace('\\~', '~') if '\\' in old else old
    if joined.count(target) != 1:
        missed.append((page, old, 'found %d times' % joined.count(target)))
        continue
    joined = joined.replace(target, new)
    pages[page] = joined.split('\n')
    applied.append((page, target, new, why))

# Readings PROPOSED in session but not applied - the editor rules on them from
# the spot sheet. (page, old, new, why)
PROPOSED = [
('161', 'sub~bo', 'sab~bo', 'APPLIED above; confirm the second letter on the crop'),
('161', 'Subdapifinda[?]', 'Subdapiferida[?]', 'the scribe\'s -ida office forms: "Castellanida" (161), "Dapiferidae Podlachiae" (Konin Gr.118), "Thesaurarida" (Gr.117); the podstoli of Bydgoszcz'),
('161', '178[5?]', '1783', 'the digit itself is to be read: the formula "Monday after St Andrew, i.e. 1 December" fits 1783, not 1785 (Sun 30 Nov 1783; Wed in 1785), and the entry\'s own December dates are "anno immediate elapso 1783"'),
('161', 'die indl~t 8ua Mensis 8bris', 'in die 7va/8va ...', 'Monday after St Francis (4 Oct 1782, a Friday) = 7 October; read the digit - the editor read 8'),
('161', 'die decima sexta [??] sui Junii', 'die sexta decima ...', 'Monday after Trinity 1783 = 16 June; read the word between'),
('161', 'Judica Terrestri Brestensi / Judica Castrensen', 'Judici / Judici ... Castrensi', 'datives (unflagged - propose only)'),
('161', 'Canitaneum Nieszczeviensem', 'Capitaneum', 'the office; unflagged on 162v - propose'),
('163', 'altenius', 'alterius', 'unflagged on p. 163; "altenius" is not Latin'),
('163', '[post/parte?]', 'post', 'the second wadion was constituted after the 1708 death it secures'),
('163v', 'fororem[?]', 'sororem', 'Mariana is the third sister; the scribe\'s f/s'),
('163v', 'Mica[w?]li Odechowski', 'Carolo Odechowski', 'on 164v the same couple stands as "Caroli et Victoriae ... Odechowskich" - read the word'),
('163v', 'Zabriski[?]', '?', 'Mariana\'s second husband - read the name'),
('164', 'isidem[?]', 'item', 'the load list runs 3tio...4to...5to; read the word'),
('164', 'Kołarbski[?]', 'Kotarbski', 'the family as on p. 165 ("Generosum Stanislaum Kotarbski") - read the letter'),
('164v', 'littae[?]', 'cittae[?]', 'the parallel "actricis et cittae" (citatae) - read the first letter'),
('165', 'ar[?][?]datariam / ar[un?]datariis', 'arrendatariam / arendatoriis', 'the arenda word; read the missing letters'),
('165', 'Costensem[?]', 'Costinens[ibus?]', 'the court of the Oporowo condescensio - read the word'),
('165v', 'ven mille f[g?]', 'decem mille fl. gr.?', 'the sum paid over from the Kałowski load - read the first word and the money abbreviation'),
('165v', '[lu?]atam', 'solutam', '"paid over by Kałowski" - read the word'),
('166', 'hoscie[l?]sciano[?]', 'Kosewsciano', 'the Kosewski load named on 165v ("ex onere Generosi Martini Kosewski") - read the word'),
('167v', 'autis[?]', 'actis', 'the formula "coram actis Castrensis" - read the letters'),
('167v', 'autoni[?]', 'autem', '"jam autem" (p. 164) - read the letters'),
('164v', 'dive[n/r?]ae formae', 'diversae formae', 'APPLIED above; confirm on the crop'),
]

os.makedirs(OUT, exist_ok=True)
order = ['161', '161v', '162', '162v', '163', '163v', '164', '164v',
         '165', '165v', '166', '166v', '167', '167v']
for p in order:
    lines = [unescape(l) for l in pages[p]]
    while lines and not lines[-1].strip():
        lines.pop()
    with open(os.path.join(OUT, PAGE_ID[p] + '.txt'), 'w', encoding='utf-8',
              newline='\n') as f:
        f.write('\n'.join(lines) + '\n')

# ------------------------------------------------------------------- log ----
log = io.StringIO()
log.write('# Readings settled in session, 2026-10-26\n\n')
log.write('Applied to the editor\'s transcription of APP 53/20/0/-/Poznań Gr.1181\n')
log.write('(pp. 161-167v) before the first build. Rules: a reading changes only where\n')
log.write('something proves it (one grammatical reading, a fixed formula, an unflagged\n')
log.write('form elsewhere in the same entry, or a form attested in the sibling units\n')
log.write('Konin Gr.115-118 and 153). The scribe\'s spellings are kept; his grammar is\n')
log.write('not tidied. NOTHING here was confirmed by eye in the session - the session\n')
log.write('could not see the images (the harness stripped every image read); the\n')
log.write('letter-level claims ride on the formulas and the siblings, and the editor\n')
log.write('confirms the letters on the spot sheet (intake/spot_rows.py). Everything\n')
log.write('not settled here keeps its [?] mark.\n\n')
log.write('| Page | Was | Now | Witness |\n|---|---|---|---|\n')
for page, old, new, why in applied:
    log.write('| %s | `%s` | `%s` | %s |\n' % (PAGE_ID.get(page, page), old.replace('|','\\|'), new.replace('|','\\|'), why))
if missed:
    log.write('\n## Not applied\n\n')
    for page, old, why in missed:
        log.write('- %s: `%s` - %s\n' % (page, old, why))
log.write('\n## Proposed, not applied (the spot sheet decides)\n\n')
for page, old, new, why in PROPOSED:
    log.write('- %s: `%s` -> `%s` - %s\n' % (page, old, new, why))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'changes_applied.md'),
          'w', encoding='utf-8', newline='\n') as f:
    f.write(log.getvalue())

sys.stdout.write('applied %d, missed %d\n' % (len(applied), len(missed)))
for m in missed:
    sys.stdout.write('MISSED: %s %s (%s)\n' % m)
