# -*- coding: utf-8 -*-
# pipeline-check-file: a one-time review sheet of the place-name plan's step 6;
# the place names it names are its data (the Słownik's entries), not a holding's.
"""The candidate places: step 6 of docs/PLACE_NAME_DATABASES_PLAN.md (2026-11-21).

The Słownik geograficzny's entries for every place it puts in the parish (or
gmina) of Trąbczyn or Zagórów, powiat słupecki, read whole - 78 marks in 65
entries, found by an OCR-tolerant search of the 16 volumes (the converted text
in Igor's repository, sources/sg/), read by two Sonnet readers and checked by
Claude against the text - and every name in them checked against the
gazetteer's 123 entries and the register's places. What is left is put to the
editor here, one row each, to accept or refuse. Nazwy miejscowe Polski was
searched for every candidate; it has entries for Białobrzeg and Goździków
only (it has not reached T-Ż, and it holds settlements only, not streams or
hills). Nothing on the site changes until the editor has answered.

    python pipeline/gazetteer/candidates_sheet.py
      -> review/place_name_sources/candidates.html  (not committed: review/)

The answers come back as JSON pasted into the chat.
"""
import html
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'review', 'place_name_sources', 'candidates.html')

ADD = 'Add to the gazetteer|Leave out|Unsure'

# key, section, name, what it is (English), the Słownik's words, citation, Claude's note, options
ROWS = [
    # ---- A. New places of the two parishes
    ('c1', 'A', 'Głogowo', 'a settlement (osada) in the gmina of Zagórów; the entry gives no parish, no distance and no figures',
     '3. G. , os. , pow. słupecki, gm. Zagórów.', 'Słownik geograficzny, t. II, p. 609 (Głogowo 3)',
     'The gmina of Zagórów was the town\'s own gmina, so the place lay at or near Zagórów. Not in Nazwy miejscowe Polski. Nothing in the edition\'s documents or maps found under this name.', ADD),
    ('c2', 'A', 'Janowska kolonia', 'a colony in the gmina of Dłusk, in the parishes of Zagórów and Szymanowice (the entry names both), 28 versts from Słupca, 8 houses, 55 inhabitants',
     'Janowska kolonia, kol. , pow. słupecki, gm. Dłusk, par. Zagórów i Szymanowice, odl. od Słupcy 28 w. , dm. 8, mk. 55.',
     'Słownik geograficzny, t. III, p. 435',
     'The farthest of the candidates from Słupca (Wrąbczynkowskie Holendry is 18 versts); it may lie on the parish boundary towards Szymanowice. A cross-reference beside it, "Janowskie Holendry, ob. Janowska kolonia", gives its other name.', ADD),
    ('c3', 'A', 'Odpadki', 'a settlement in the gmina of Emilienheim (later Oleśnica) and parish of Zagórów, 15½ versts from Słupca; no figures',
     'Odpadki 1. os, pow. słupecki, gm. Emilienhajm, par. Zagórów, odl. od Słupcy 15 1/2 w.',
     'Słownik geograficzny, t. VII, p. 386 (Odpadki 1)',
     'The same distance as Jarmuszewek (c6). The name means "leftovers": a piece of land cut off from a larger holding.', ADD),
    ('c4', 'A', 'Tumidaj', 'an inn (osada karczemna) in the gmina of Trąbczyn and parish of Zagórów, 22 versts from Słupca, 1 house, 1 inhabitant',
     '5. T. , os. karcz. , pow. słupecki, gm. Trąbczyn, par. Zagórów, odl. od Słupcy 22 w. , 1 dm. , 1 mk.',
     'Słownik geograficzny, t. XII, p. 623 (Tumidaj 5)',
     'The same distance as Smoleniec and Koszelewska Łąka (22 versts, gmina of Trąbczyn, parish of Zagórów), so very probably an inn among the Łukom estate\'s villages. Whether it is your tavern Wygoda north of Łukom, or another, the entry does not say. T is beyond the letters Nazwy miejscowe has reached.', ADD),
    ('c5', 'A', 'Wielki Las', 'a forester\'s house (leśniczówka) in the gmina and parish of Trąbczyn, 19 versts from Słupca, 1 house, 6 inhabitants',
     '2. W. L. , leś. , pow. słupecki, gm. i par. Trąbczyn, odl. od Słupcy w. 19; ma 1 dm. , 6 mk.',
     'Słownik geograficzny, t. XIII, p. 340 (Wielki Las 2)',
     'Not your Wielki-Bór Obręb (a forest precinct of the 1861 map): a different name. The name means "the great forest". The Słownik calls Noga and Stanisławów forest settlements of the same gmina too.', ADD),
    ('c6', 'A', 'Jarmuszewek (Wójtowstwo Jarmużówka)', 'a manor farm (folwark) in the gmina of Emilienheim and parish of Zagórów, 15½ versts from Słupca, 3 houses, 46 inhabitants; in 1886 171 morgi, 7 brick and 3 wooden buildings, peat',
     'Jarmuszewek lub Wrąbczyn, folw. , powiat słupecki, gm. Emilienheim, par. Zagórów, odl. od Słupcy 15 i pół w. , dm. 3, mk. 46. — 11. W. Jarmużówka al. Jarmuszewek, fol, pow. słupecki, gm. Emilienheim par. Zagórów ... W r. 1886 fol. W. Jarmużówka rozl. mr. 171 ...',
     'Słownik geograficzny, t. III, p. 451; t. XIII, p. 773 (Wójtowstwo 11)',
     'The Słownik calls it "Jarmuszewek or Wrąbczyn": one of the farms of Wrąbczyn under another name. "Wójtowstwo" means the village headman\'s (wójt\'s) holding. It could stand as its own place or as a name of your Wrąbczyn.', 'A place of its own|A name of Wrąbczyn|Leave out|Unsure'),
    ('c7', 'A', 'Wrąbczyńskie Holendry', 'a colony in the gmina of Emilienheim and parish of Zagórów, 17 versts from Słupca, 8 houses, 61 inhabitants',
     'Wrąbczyńskie Holendry, kol, pow. słupecki, gm. Emilienheim, par. Zagórów, odl. o 17 w. od Słupcy, ma 8 dm. , 61 mk.',
     'Słownik geograficzny, t. XIV, p. 16',
     'Not Wrąbczynkowskie Holendry, which follows it on the page (gmina of Dłusk, 35 houses). The gmina of Emilienheim was the gmina of the Prince\'s German colonies, so this is very probably your Kolonia Wrąbczyn, the colony of the lease of 1806 northwest of Wrąbczynek. If so, the entry would be cited there.', 'Same as Kolonia Wrąbczyn|A new place|Unsure'),
    ('c8', 'A', 'Białobrzeg (Białobrzeg Pietrzykowski and Białobrzeg Ratajski)', 'a village and a settlement on the Warta in the gmina of Dłusk and parish of Zagórów; Białobrzeg Pietrzykowski 6 houses, 112 inhabitants, Białobrzeg Ratajski 1 house, 5 inhabitants',
     '3. B. pietrzykowski, wś i B. ratajski, os. nad rz. Wartą, pow. słupecki, gm. Dłusk, par. Zagórów. B. pietrz. ma 6 dm. , 112 mk. ; B. rat. 1 dm. , 5 mk.',
     'Słownik geograficzny, t. XV, p. 125; Nazwy miejscowe Polski, t. 1, p. 193 (Białobrzeg 1)',
     'Already a place of the edition, but not in your gazetteer: the register has it (the mill "Białobrzeg bey Wrąbczynek" in the contract of 1 October 1798 with its miller Samuel Lucke, Oe 1 Bü 14526, documents 25 and 26, and the table of the souls of the parish of Zagórów of 1791, ADWł 85, document 2), and it is in the literature. Nazwy miejscowe gives it from 1547 ("molendino ... vulgo Biało-Brzeski"), the mill on the Warta, today Białobrzeg in the gmina of Pyzdry, 10 km west of Zagórów; the name is "white bank"; Pietrzykowski and Ratajski from the neighbouring villages Pietrzyków and Rataje.', ADD),
    # ---- B. Features
    ('c9', 'B', 'Biały (strumień Biały)', 'a stream: Trąbczyn, Maryantów and Szetlewek all lie "on the stream Biały"',
     'Trąbczyn ... wś i folw. nad strum. Białym ...; 2. M[aryantów], wś nad strum. Białym ...; Szetlewek, wś i folw. nad strum. Białym ...',
     'Słownik geograficzny, t. XII, p. 448; t. VI, p. 153; t. XI, p. 911',
     'Your gazetteer has the streams Bartosz and Czarna Struga, not this one. The name means "white". No entry of its own in the Słownik.', ADD),
    ('c10', 'B', 'Czarna Góra', 'a hill by Wrąbczynek: the Słownik\'s second Wrąbczynek is "a manor farm under the Czarna Góra" (gmina Emilienheim, parish Zagórów, 15 versts from Słupca, 3 houses, 19 inhabitants)',
     '2 W[rąbczynek] , folw. pod Czarną górą, pow. słupecki, gm. Emilienheim, par. Zagórów, odl. od Słupcy 15 w. , ma 3 dm. , 19 mk.',
     'Słownik geograficzny, t. XIV, p. 16 (Wrąbczynek 2)',
     'The name means "black hill". The farm under it is a second Wrąbczynek, distinct from the village (gmina Dłusk); your Wrąbczynek entry could note it either way.', ADD),
    # ---- C. Parts of the Kopojno estate
    ('c11', 'C', 'Goździków (Goździkowo)', 'a manor farm and village of the Kopojno estate; its own entry puts it in the gmina of Emilienheim but the parish of Rzgów; enfranchised with 11 holdings in 1866',
     'Kopojno ... składają się z folwarków Kopojno, Goździków; przyległości Stawiska, Chruszczyki, Goździkówka, Gęsiłoża; wsi Kopojno, Swiątniki, Skoków i Goździków. — Goździkowo, folw. , pow. słupecki, gm. Emilienheim, par. Rzgów.',
     'Słownik geograficzny, t. IV, p. 383 (Kopojno); t. II, p. 765 (Goździkowo); Nazwy miejscowe Polski, t. 3, p. 289-290 (Goździków 1)',
     'Outside the two parishes (Rzgów), like Świątniki, which you placed with the area on 2026-10-24. Listed because it belonged to the Kopojno estate. Still a village: Nazwy miejscowe gives it as Goździków, gmina Rzgów, 8 km south-east of Zagórów, recorded as "Gozdzików" in 1827, "Fol. Goździkow" in 1839, "Goździkowo" in 1881 and 1921, and Goździków in 1980; the name is from the personal name Goździk with the suffix -ów.', ADD),
    ('c12', 'C', 'Goździkówka', 'an appurtenance (przyległość) of the Kopojno estate; no entry of its own, no figures',
     'przyległości Stawiska, Chruszczyki, Goździkówka, Gęsiłoża', 'Słownik geograficzny, t. IV, p. 383 (Kopojno)',
     'Named only in the list of the estate\'s parts. Of the four appurtenances one is known: Chruszczyki is your Chruściki (Adelhof).', ADD),
    ('c13', 'C', 'Gęsiłoża', 'an appurtenance of the Kopojno estate; no entry of its own, no figures',
     'przyległości Stawiska, Chruszczyki, Goździkówka, Gęsiłoża', 'Słownik geograficzny, t. IV, p. 383 (Kopojno)',
     'Named only in the list of the estate\'s parts. The name suggests a goose pasture (gęś, goose).', ADD),
    ('c14', 'C', 'Stawiska', 'an appurtenance of the Kopojno estate; no entry of its own, no figures',
     'przyległości Stawiska, Chruszczyki, Goździkówka, Gęsiłoża', 'Słownik geograficzny, t. IV, p. 383 (Kopojno)',
     'Not your Stawisko (the village of the Łukom estate, gmina Trąbczyn): this one belonged to the Kopojno estate. The name means "ponds". Nazwy miejscowe\'s Stawiska entries are other places (by Sompolno and Chodów).', ADD),
]

# The two decisions of the first sheet, answered by the editor 2026-11-21: "Yes, read
# the Słownik around the others as well. Please correct the Olchowo one." Olchowo is
# corrected; the outlying parishes are section E, read from
# candidates_outlying.json (the parishes of Rzgów, Pyzdry, Stawiszyn and Zbiersk and
# the gmina of Grodziec: 72 entries in powiat słupecki, koniński or kaliski, read by
# three Sonnet readers, checked by Claude; the readers' English summaries kept,
# spot-checked against the Polish).
DECISIONS = []
OUTLYING = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'candidates_outlying.json')
E_TITLES = [
    ('E1', 'E. Around your other places: the parish of Rzgów (Szetlew, Szetlewek, Świątniki)'),
    ('E2', 'E. The parish of Pyzdry'),
    ('E3', 'E. The parish of Stawiszyn'),
    ('E4', 'E. The parish of Zbiersk (Zbiersk Kolonia)'),
    ('E5', 'E. The gmina of Grodziec (Orlina Duża, Czarnybród): the parish of Grodziec'),
    ('E6', 'E. The gmina of Grodziec: the parish of Królików'),
]

KNOWN = [
    ('Sofienthal (t. XI, p. 8), Olechowo (t. XVI, p. 405)', 'your Olchowo'),
    ('Adolfsberg (the Oleśnica estate\'s second farm)', 'your Zalesie (renamed 1891, t. XV, p. 471)'),
    ('Chruszczyki (Kopojno estate)', 'your Chruściki (Adelhof)'),
    ('Smokiliec (t. X, p. 900: gm. Trąbczyn, par. Zagórów, 22 versts, 7 houses, "Por. Koszelewska Łąka")', 'your Smoleniec (the OCR\'s reading of the name)'),
    ('Łoniewo (the Łukom estate\'s list: 28 holdings, 242 morgi)', 'very probably Łomowo, your Łomów (the OCR\'s reading)'),
    ('Trąbczyńska Huta, Holendry wrąbczynkowskie, Łazińska kolonia, Koszelowska łąka, Dziadolin, Włodzimierzów, Buków, Siergiejewo, Skokom/Skoków, Studzienka', 'your Huta Trąbczyńska, Wrąbczynkowskie Holendry, Łazińskie Olędry, Koszelewska Łąka, Dziadolina, Włodzimirów, Bukowe, Wincentowo, Skokum, Studzianka'),
    ('Święcia (t. XI): powiat koniński, parish Kuchary; "par. Zagorów" only in a quoted register of 1579', 'outside the scope; left out'),
    ('Grabieniec (the Świątniki entry: a boundary dispute of 1375)', 'a medieval neighbour of Świątniki, parish Rzgów; left out'),
    ('Warta', 'your Warta River'),
]


def esc(s):
    return html.escape(s, quote=True)


def row_html(key, section, name, what, pl, cite, note, opts):
    radios = ''.join(
        '<label class="opt"><input type="radio" name="%s" value="%s"> %s</label>' % (key, esc(o), esc(o))
        for o in opts.split('|'))
    return ('<section class="row" id="%s"><h3><span class="k">%s</span> %s</h3>'
            '<p class="what">%s</p>'
            '<details><summary>The Słownik\'s words</summary><p class="pl" lang="pl">%s</p></details>'
            '<p class="cite">%s</p><p class="note">%s</p>'
            '<div class="opts">%s</div>'
            '<textarea data-note="%s" placeholder="Note (optional)"></textarea></section>') % (
        key, key, esc(name), esc(what), esc(pl), esc(cite), esc(note), radios, key)


def compact_html(e, opts=ADD):
    radios = ''.join(
        '<label class="opt"><input type="radio" name="%s" value="%s"> %s</label>' % (e['key'], esc(o), esc(o))
        for o in opts.split('|'))
    note = '<p class="note">%s</p>' % esc(e['note']) if e.get('note') else ''
    return ('<section class="row compact" id="%s"><h3>%s</h3><p class="what">%s</p><p class="cite">%s</p>%s'
            '<div class="opts">%s</div><textarea data-note="%s" placeholder="Note (optional)"></textarea></section>') % (
        e['key'], esc(e['name']), esc(e['what']), esc(e['cite']), note, radios, e['key'])


def main():
    sec_title = {'A': 'A. Places of the two parishes not in your gazetteer',
                 'B': 'B. Features (streams, hills)',
                 'C': 'C. Parts of the Kopojno estate with no entry of their own'}
    body = []
    for s in 'ABC':
        body.append('<h2>%s</h2>' % sec_title[s])
        body += [row_html(*r) for r in ROWS if r[1] == s]
    outlying = json.load(io.open(OUTLYING, encoding='utf-8'))
    body.append('<h2 class="part">E. Around your places in other parishes</h2>'
                '<p>At your word ("read the Słownik around the others as well"): every place the Słownik puts in the parishes of '
                'Rzgów, Pyzdry, Stawiszyn and Zbiersk, or in the gmina of Grodziec, that is not in your gazetteer. These lie outside '
                'the Trąbczyn and Zagórów area proper; Czarnybród and Orlina Duża have no entries of their own. The English is a '
                'summary of each entry.</p>')
    for g, title in E_TITLES:
        rows = sorted((e for e in outlying if e['group'] == g), key=lambda e: e['name'])
        if rows:
            body.append('<h2>%s <span class="k">(%d)</span></h2>' % (title, len(rows)))
            body += [compact_html(e) for e in rows]
    known = ''.join('<tr><td>%s</td><td>%s</td></tr>' % (esc(a), esc(b)) for a, b in KNOWN)
    keys = [r[0] for r in ROWS] + [e['key'] for e in outlying]
    page = TEMPLATE.replace('__BODY__', '\n'.join(body)).replace('__KNOWN__', known) \
        .replace('__KEYS__', json.dumps(keys)).replace('__N__', str(len(ROWS))).replace('__E__', str(len(outlying)))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(page)
    print('%d candidates of the two parishes and %d around the others -> %s' % (len(ROWS), len(outlying), OUT))


TEMPLATE = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Candidate places</title>
<style>
:root { --bg:#fbfaf7; --fg:#222; --mute:#666; --card:#fff; --line:#ddd; --acc:#7a4b12; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#1b1a18; --fg:#e8e6e1; --mute:#a9a49b; --card:#262421; --line:#3a3733; --acc:#e0a95b; } }
:root[data-theme="dark"] { --bg:#1b1a18; --fg:#e8e6e1; --mute:#a9a49b; --card:#262421; --line:#3a3733; --acc:#e0a95b; }
body { background:var(--bg); color:var(--fg); font:16px/1.5 Georgia, serif; margin:0 auto; max-width:52rem; padding:1rem 16px 4rem; }
h1 { font-size:1.6rem; margin:.5rem 0; } h2 { font-size:1.2rem; margin:2rem 0 .5rem; color:var(--acc); }
.row { background:var(--card); border:1px solid var(--line); border-radius:6px; padding:.8rem 1rem; margin:.8rem 0; }
.row h3 { margin:0 0 .3rem; font-size:1.05rem; } .k { color:var(--mute); font-size:.85rem; margin-right:.3rem; }
.what { margin:.2rem 0; } .cite, .note { color:var(--mute); font-size:.92rem; margin:.3rem 0; }
.pl { font-style:italic; } details summary { cursor:pointer; color:var(--mute); font-size:.92rem; }
.opts { display:flex; flex-wrap:wrap; gap:.4rem 1rem; margin:.5rem 0; } .opt { white-space:nowrap; }
textarea { width:100%; box-sizing:border-box; min-height:2.2rem; background:var(--bg); color:var(--fg); border:1px solid var(--line); border-radius:4px; font:inherit; font-size:.92rem; }
table { border-collapse:collapse; width:100%; font-size:.92rem; } td { border-top:1px solid var(--line); padding:.3rem .4rem; vertical-align:top; }
.compact h3 { font-size:1rem; } .part { margin-top:3rem; }
.bar { position:sticky; bottom:0; background:var(--bg); border-top:1px solid var(--line); padding:.6rem 0; display:flex; gap:1rem; align-items:center; flex-wrap:wrap; }
button { font:inherit; padding:.35rem .9rem; border:1px solid var(--acc); background:var(--card); color:var(--fg); border-radius:4px; cursor:pointer; }
#out { width:100%; min-height:6rem; display:none; }
</style></head><body>
<h1>Candidate places</h1>
<p>From the <i>Słownik geograficzny Królestwa Polskiego</i> (1880–1902): every place it puts in the parish or gmina of Trąbczyn or Zagórów, checked against your gazetteer and the edition's register of places. __N__ places and features of the two parishes are not in your gazetteer (sections A to C), and __E__ places around your places in other parishes (section E). Your two answers of the first sheet are worked in: the Olchowo entry is corrected, and section E is new. For each, say whether it should be added. "Versts" are Russian versts from Słupca (one verst is about 1.07 km). Nothing on the site changes until you answer.</p>
__BODY__
<h2>Not new: names the Słownik spells otherwise</h2>
<p class="note">For reference only; no answer needed. Of the 65 entries read, these turned out to be your places under another name or spelling.</p>
<table>__KNOWN__</table>
<div class="bar"><button id="copy">Copy answers</button><span id="msg" class="note"></span></div>
<textarea id="out" readonly></textarea>
<script>
const KEYS = __KEYS__; const STORE = 'candidates-2026-11-21';
function load() { try { return JSON.parse(localStorage.getItem(STORE) || '{}'); } catch (e) { return {}; } }
function save(s) { try { localStorage.setItem(STORE, JSON.stringify(s)); } catch (e) {} }
const state = load();
for (const k of KEYS) {
  const v = state[k] || {};
  document.querySelectorAll('input[name="' + k + '"]').forEach(r => { if (r.value === v.answer) r.checked = true;
    r.addEventListener('change', () => { state[k] = Object.assign(state[k] || {}, {answer: r.value}); save(state); }); });
  const t = document.querySelector('textarea[data-note="' + k + '"]');
  if (t) { t.value = v.note || ''; t.addEventListener('input', () => { state[k] = Object.assign(state[k] || {}, {note: t.value}); save(state); }); }
}
document.getElementById('copy').addEventListener('click', () => {
  const out = {}; for (const k of KEYS) { const v = state[k] || {}; out[k] = {answer: v.answer || '', note: v.note || ''}; }
  const text = 'Candidate places answers:\\n' + JSON.stringify(out, null, 1);
  const ta = document.getElementById('out'); ta.value = text; ta.style.display = 'block';
  const done = () => { document.getElementById('msg').textContent = 'Copied - paste it into the chat.'; };
  if (navigator.clipboard) { navigator.clipboard.writeText(text).then(done, () => { ta.select(); document.execCommand('copy'); done(); }); }
  else { ta.select(); document.execCommand('copy'); done(); }
});
</script></body></html>
'''

if __name__ == '__main__':
    main()
