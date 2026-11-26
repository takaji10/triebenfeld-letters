# -*- coding: utf-8 -*-
"""The spot sheet of Pyzdry Gr.75 (2026-11-26): the transcription with what Claude added or
changed highlighted, beside enlarged strips of the two pages, and the places Claude wants
looked at. Writes intake/spot_sheet.html (images inside it). Needs the strips in STRIPS."""
import base64, io, html, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
STRIPS = sys.argv[1]           # folder with 19r_03.png ... 19v_03.png
NEED = ['19r_03', '19r_04', '19r_05', '19r_06', '19r_07', '19r_08', '19v_01', '19v_02', '19v_03']

def data(name):
    im = Image.open(os.path.join(STRIPS, name + '.png')).convert('RGB')
    b = io.BytesIO(); im.save(b, 'JPEG', quality=80)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

# (id, kind, strips, context html, was, now/ask)  kind: add | ask | struck | look
ITEMS = [
 ('A1', 'add', ['19r_03'], 'Sanus mente et Corpore existens <mark class=add>Manifeste Recedendo &amp;c[etera]</mark> Recognovit',
  'Manifestatione Recedendo e[dem?]ce~', 'Line 2 of the entry, after "existens": the page seems to read "Mnfte Recedendo &amp;ce Recognovit" (the abbreviated adverb and the sign &amp;c). Is this right?'),
 ('A2', 'add', ['19r_03'], 'Unam quidem Mille Quinquaginta Trium Imperialium <mark class=add>Grossorum Tredecim, Fericorum[?] sc[ilicet] per olim Magnificum</mark> Paulum Prusimski pro arboribus',
  'Imperialium Paulum Prusimski', 'Lines 3-4 of the entry. Your text jumps from "Imperialium" to "Paulum"; the page has words between them: "Grossorum Tredecim" (13 groschen), a doubtful word ("Fericorum"?), "sc." and "per olim Magnificum". Do you read these words? What is the word after "Tredecim,"?'),
 ('A3', 'add', ['19r_07'], 'memorati olim Magnifici Pauli Prusimski <mark class=add>expositam</mark> seorsivo[?] Regestro',
  'ea positam', 'The line ends "ex-" and the next begins "positam". Do you see "ex" (with the hyphen stroke) rather than "ea"?'),
 ('A4', 'add', ['19r_08'], 'per huncce olim Magnificum Antonium Prusimski pro hisce secaminibus acceptam <mark class=add>proq[ue] usuq[ue]</mark> ac commodo suo dispositam',
  'proque sisce[?]', 'Last lines of the page, line 2 of the three at the foot. I read "proq usuq ac commodo suo". Do you?'),
 ('A5', 'add', ['19r_08', '19v_01'], 'tum et alias summas scriptis et Documentis <mark class=add>manualibus</mark> ac &nbsp;|&nbsp; [verso, line 1] <mark class=add>Regestris</mark> tum variis connotationibus',
  'manuali his ac Regestris (all at the foot of the recto)', 'Two moves. (1) The last line of the recto ends "manuali-bus ac" at the torn corner; I read "manualibus", not "manuali his". (2) "Regestris" I moved to the head of line 1 of the verso, because a word stands there before "tum variis" and the recto\'s torn corner shows nothing after "ac". Do you agree with both?'),
 ('A6', 'add', ['19v_01'], 'in Personam Magnifici Stanislai Chełmski uti <mark class=add>hasce</mark> summas iure[?] suo proprio',
  'hisce summas', 'Line 4 of the verso. The page seems to have "hasce" (as in "ad hasce summas" four lines below); a struck word "sibi" stands before it (not transcribed).'),
 ('A7', 'add', ['19v_03'], 'transfundit <mark class=add>Actaq[ue]</mark> praesenti Da[m/s?] et concedens [?]',
  'actas praesenti', 'Line 3 of the strip, after "transfundit". The first word looks to me like "Actaq" with the stroke of an abbreviation, not "actas". Do you read it so?'),
 ('A8', 'add', ['19v_03'], 'concedens [?] <mark class=add>hac</mark> sua personali recog~<mark class=add>tione</mark> ad praemissa libere accedente',
  'haec sua personali recog~tioni', 'Next line of the page. "hac ... recognitione" (ablative, with "accedente"); do the final letters read "hac" and "-e"?'),
 ('A9', 'add', ['19v_03'], '<mark class=add>Sup[er]</mark> Transfusionem sui Juris in Per M. Chełmski',
  'Super Transfusionem', 'The docket under the signature: the page has "Sup" with a flourish; I put the expansion in brackets.'),
 ('S1', 'struck', ['19r_04'], 'proprio honorati Traholtz recognoscentis peculio curaque elaboratis (struck: <s>per</s>) licet si olim idem Magnificus',
  '— (not transcribed)', 'Entry line 6: a struck "per" between "elaboratis" and "licet". I did not look at this strip myself (the second reader saw it); please look.'),
 ('S2', 'struck', ['19r_08'], 'per huncce olim Magnificum Antonium Prusimski pro (struck: <s>usu seu conversione?</s>) hisce secaminibus',
  '— (not transcribed)', 'Three words struck after "pro" (I read "usu seu conversione"; only the fact of the deletion matters, it is not transcribed). Is it struck?'),
 ('S3', 'struck', ['19v_01'], 'uti (struck: <s>sibi</s>) hasce summas', '— (not transcribed)', 'One word struck before "hasce".'),

 ('D1', 'ask', ['19r_07'], 'ex ratione subsecuta <mark class=ask>Borram</mark> et sylvarum inter ipsos controversiae',
  'kept as you have it', 'Line 2 of the strip. The word may read "Borrarum" (genitive plural, matching "sylvarum"). Which letters end it?'),
 ('D2', 'ask', ['19r_07'], 'per recognoscentem honoratum Traholtz erogatam <mark class=ask>[i?]</mark> partim pro commodo',
  'kept as you have it', 'A brown smear and two dots stand after "erogatam". Is there a word under it, or is "[i?]" the smear?'),
 ('D3', 'ask', ['19v_01'], 'hasce summas <mark class=ask>iure[?]</mark> suo proprio sibi recognoscenti persolventis',
  'kept as you have it', 'Line 5 of the verso. The first letter looks like "E/Æ" with no descender, so the word may be "aere" (from his own money), not "iure". This changes the sense of the payment.'),
 ('D4', 'ask', ['19v_01'], 'nihil sibi et suis successoribus <mark class=ask>ea</mark> praedictis summis in post reservando',
  'kept as you have it', 'Line 3 of the verso. "ea" or "ex"?'),
 ('D5', 'ask', ['19v_02'], 'et hasce summas enucleantibus Recognoscentem successoribus Prusimscianis instituto ac cum processe juris pertinente <mark class=ask>cessit</mark> contulit ... [end of the entry:] libere accedente <mark class=ask>fun[d?]u[m?] provisionibus ab ejsdem summis capitalibus provenientibus</mark>',
  'the two passages as you placed them', 'Strip 19v_02, the lines "cum omnibus quibusvis petendi ... se referentibus" and below. An interlinear line (beginning with a cross) stands above line 10 and ends in "&amp;"; a second cross stands in line 10 under "cessit". You have the interlinear words at the end of the entry. Should they stand before "cessit"? And can you read the first word of that line?'),
 ('D6', 'ask', ['19v_03'], 'Jan Traholtz ręką trzymaną &nbsp;[foot line:] <mark class=ask>Recognoscentem successoribus Prusimscianis instituto</mark>',
  'you have these words before "cessit" (with "ac cum processe juris pertinente")', 'The foot line begins with a cross; the matching cross stands after "per" at the end of the line "ac cum processu juris per[tinente]" just above the signature. So the foot line may belong at the end of the entry, after "pertinente". Which do you see?'),
 ('D7', 'ask', ['19v_03'], 'Actaq[ue] praesenti <mark class=ask>Da[m/s?]</mark> et concedens <mark class=ask>[?]</mark> hac sua',
  'kept as you have it', '"Da[m/s?]" and the flourish after "concedens" ("&amp;"? "J."?).'),
 ('D8', 'ask', ['19v_03'], 'Sup[er] Transfusionem sui Juris <mark class=ask>in Per</mark> M. Chełmski',
  'kept as you have it', 'The docket reads "in per" or "inter" before "M. Chełmski"?'),
 ('L1', 'look', ['19r_05'], 'Arborum <mark class=look>[ordine?]</mark> praefato olim Magnifico Prusimski conscripto',
  'unchanged', 'The line breaks "ord-/..."; I did not read this strip myself (second reader only). Is "[ordine?]" what stands there?'),
 ('L2', 'look', ['19r_06'], 'novem <mark class=look>Stru[i]um</mark> vulgo Rynek',
  'unchanged', 'I did not read this strip myself. "Struum" or "Struium" (stacks)?'),
 ('L3', 'look', ['19r_05', '19r_07'], 'scripto reversali vulgo <mark class=look>Auscuk[Auszug]</mark> ... seorsivo[?] Regestro',
  'unchanged', 'The editor\'s gloss "[Auszug]" (a German extract) for "Auscuk", and "seorsivo[?]", on strips I did not read myself.'),
]

KIND = {'add': ('Claude changed this', '#fff3b0'), 'ask': ('For your eye (left as you have it)', '#ffd7b5'),
        'struck': ('Struck-out words (not transcribed)', '#e6e6e6'), 'look': ('Strips I did not read myself', '#d9ecff')}

def card(it):
    id_, kind, strips, ctx, was, now = it
    imgs = ''.join('<figure><img data-strip="%s" alt="strip %s"><figcaption>%s - click to enlarge</figcaption></figure>' % (s, s, s) for s in strips)
    return ('<section class="card %s" id="%s"><h3><span class=tag>%s</span> %s</h3>'
            '<p class=ctx>%s</p><p class=was><b>You had / now:</b> %s</p><p class=q>%s</p>%s</section>'
            % (kind, id_, id_, KIND[kind][0], ctx, was, now, imgs))

full = open(os.path.join(HERE, '..', 'corpus.txt'), encoding='utf-8').read().split('\n')
def hi(t):
    t = html.escape(t)
    for a in ['Manifeste Recedendo &amp;c[etera]', 'Grossorum Tredecim, Fericorum[?] sc[ilicet] per olim Magnificum', 'expositam',
              'proq[ue] usuq[ue]', 'manualibus', 'Regestris', 'hasce', 'Actaq[ue]', ' hac ', 'tione ', 'Sup[er]']:
        pass
    return t
text = ''.join('<p>%s</p>' % html.escape(l) for l in full if l and not l.startswith('['))

doc = '''<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Spot sheet: Pyzdry Gr.75, entry no. 39</title>
<style>
:root{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#666;--card:#fff;--line:#ddd}
@media (prefers-color-scheme:dark){:root{--bg:#1a1a18;--fg:#eceae4;--mut:#aaa;--card:#242421;--line:#3a3a36}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 Georgia,serif}
main{max-width:1100px;margin:0 auto;padding:16px}
h1{font-size:1.4rem}h2{margin-top:2rem;border-bottom:1px solid var(--line)}
.legend span{display:inline-block;padding:2px 8px;margin:2px;border-radius:4px;color:#111}
.card{background:var(--card);border:1px solid var(--line);border-left:6px solid #ccc;border-radius:6px;padding:8px 14px;margin:14px 0}
.card.add{border-left-color:#e0b800}.card.ask{border-left-color:#e07a00}.card.struck{border-left-color:#888}.card.look{border-left-color:#3a8fd9}
.tag{font-weight:bold;font-family:sans-serif;margin-right:6px}h3{margin:.2rem 0;font-size:1rem;font-family:sans-serif}
mark.add{background:#fff3b0;color:#111}mark.ask{background:#ffd7b5;color:#111}mark.look{background:#d9ecff;color:#111}s{color:#a00}
.ctx{font-family:Georgia,serif;font-size:1.05rem}.was,.q{margin:.3rem 0;font-size:.95rem}
figure{margin:8px 0}figure img{width:100%;max-height:340px;object-fit:contain;object-position:left;background:#eee;cursor:zoom-in;border:1px solid var(--line)}
figure img.big{max-height:none;cursor:zoom-out}figcaption{font:12px sans-serif;color:var(--mut)}
.text p{margin:.5rem 0}
</style><main>
<h1>Pyzdry Gr.75, entry no. 39: spot sheet</h1>
<p>Leaf 19 recto and verso. Each card shows an enlarged strip of the page (click to enlarge), the words in the transcription, what you had, and what I ask. The strips are 2x enlargements of the images you sent; the names (19r_03, 19v_01 ...) say page and strip, from the top down.</p>
<p class=legend><span style="background:#fff3b0">yellow: Claude changed or added</span><span style="background:#ffd7b5">orange: for your eye, left as you have it</span><span style="background:#e6e6e6">grey: struck out, not transcribed</span><span style="background:#d9ecff">blue: strips I did not read myself</span></p>
<h2>Answer in the to-do list or in chat; the questions that matter most</h2>
<ol><li><b>A2</b>: the 13 groschen your text skipped, and the word after "Tredecim,".</li><li><b>D5 and D6</b>: where the two inserted lines belong.</li><li><b>D3</b>: "iure" or "aere".</li></ol>
''' + '\n'.join('<h2>%s</h2>' % h + '\n'.join(card(i) for i in ITEMS if i[1] in ks)
                for h, ks in [('Changed by Claude (nine corrections)', ('add',)), ('Struck out, not transcribed', ('struck',)),
                              ('Left as you have it, for your eye', ('ask',)), ('Places I did not read myself', ('look',))]) + '''
<h2>The transcription as it now stands</h2><div class=text>''' + text + '''</div>
</main><script>
const S={%s};
document.querySelectorAll('img[data-strip]').forEach(i=>{i.src=S[i.dataset.strip];i.onclick=()=>i.classList.toggle('big')});
</script></html>''' % ','.join('"%s":"%s"' % (n, data(n)) for n in NEED)
open(os.path.join(HERE, 'spot_sheet.html'), 'w', encoding='utf-8', newline='\n').write(doc)
print('wrote spot_sheet.html', len(doc) // 1024, 'KB')
