# -*- coding: utf-8 -*-
"""The sheet of dropped phrases of APP 53/17/0/-/Konin Gr.145, for the editor.

    python units/app53170koningr145/intake/dropped_sheet.py

Writes review/app53170koningr145/dropped/index.html. The editor asked
(2026-10-06) for the phrases the transcription had dropped to be highlighted,
each with a word on whether it matters to the meaning. The sheet is made from
full_check_rows.py (what the full check found) and translation/fixes_full.py
(what was changed in the English), so it says what those files say.

Three parts: the dropped phrases, in the order of the text; the misread words
that changed what the court says; the other changes to the English.
"""
import difflib
import html
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'translation'))
import full_check_rows as F  # noqa: E402
from fixes_full import FIXES_FULL  # noqa: E402

OUT = os.path.join(ROOT, 'review', 'app53170koningr145', 'dropped')

VERDICT = {
    'court': ('Significant', 'It changes what the record says the court found or did.'),
    'fact': ('Adds a fact', 'It adds or corrects a fact (a name, a place, who did what). The outcome is the same.'),
    'formula': ('Not significant', 'Legal wording, or a repetition of what the sentence already says.'),
}
# Dropped phrases the editor's English already had right: nothing was changed.
ENGLISH_HAD_IT = {
    ('0675_a1', 'przed'): 'The English already had "Monday before Saint Hedwig". Not changed.',
    ('0677_a2', 'nie'): 'The English already had "heir not of all of Trąbczyn". Not changed.',
}
# The earlier, light check found one more.
EARLIER = dict(
    leaf='673 recto', page=38, weight='fact',
    pl='w lesie Lusnie ku mościskom ciągnących się na kilka staj <mark>las cały Lusnie zajmujących i zabierających</mark>',
    note='six words skipped between two words with the same ending: the eight mounds and forty-one blazes '
         'stretch toward the corduroy crossings for several staje, "occupying and taking in the whole Lusnia woodland". '
         'Found in the first, light check.',
    en='stretching toward the corduroy crossings for several staj<mark>, occupying and taking in the whole Lusnia woodland</mark>. And likewise he showed')


def ids():
    out = []
    for n in range(654, 716):
        for half in ('a1', 'a2'):
            pid = '%04d_%s' % (n, half)
            if pid not in ('0654_a1', '0655_a1'):
                out.append(pid)
    return out


def leaf(pid):
    n, half = int(pid[:4]), pid[5:]
    return '%d recto' % n if half == 'a2' else '%d verso' % (n - 1)


def note(t):
    """The working note, without its reminder to myself."""
    for tail in ('. Check the English', '; check the English'):
        if t.endswith(tail):
            t = t[:-len(tail)]
    return html.escape(t)


def marked(old, new):
    """`new`, with the words that are not in `old` highlighted."""
    a, b = old.split(), new.split()
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        seg = html.escape(' '.join(b[j1:j2]))
        if not seg:
            continue
        out.append(seg if tag == 'equal' else '<mark>%s</mark>' % seg)
    return ' '.join(out)


def main():
    order = ids()
    dropped = [r for r in F.ROWS if r['kind'] == 'dropped']
    en_dropped = [x for x in FIXES_FULL if x[3].startswith('dropped') or x[3].startswith('a paragraph')]
    en_other = [x for x in FIXES_FULL if x not in en_dropped]
    need = [r for r in dropped if not any(r['page'] == k[0] and r['new'].split().count(k[1]) for k in ENGLISH_HAD_IT)]
    had = [r for r in dropped if r not in need]
    assert len(had) == len(ENGLISH_HAD_IT) and len(need) == len(en_dropped), (len(had), len(need), len(en_dropped))
    fix_of = {id(r): x for r, x in zip(need, en_dropped)}

    items = []

    def item(n, where, weight, pl, note_text, en_html):
        head, say = VERDICT[weight]
        items.append('<section class="%s"><h3>%d. Leaf %s <span class="v">%s</span></h3>'
                     '<p class="pl">%s</p><p>%s</p><p class="say"><b>%s.</b> %s</p>%s</section>'
                     % (weight, n, where, head, pl, html.escape(note_text), head, say, en_html))

    n = 0
    put_earlier = False
    for r in dropped:
        if not put_earlier and r['page'] > '0673_a2':
            n += 1
            item(n, '%s (page %d of 122)' % (EARLIER['leaf'], EARLIER['page']), EARLIER['weight'], EARLIER['pl'],
                 EARLIER['note'], '<p class="en"><b>English now:</b> %s</p>' % EARLIER['en'])
            put_earlier = True
        n += 1
        where = '%s (page %d of 122)' % (leaf(r['page']), order.index(r['page']) + 1)
        x = fix_of.get(id(r))
        if x is None:
            key = [k for k in ENGLISH_HAD_IT if k[0] == r['page'] and k[1] in r['new'].split()][0]
            en = '<p class="en">%s</p>' % html.escape(ENGLISH_HAD_IT[key])
        elif x[3].startswith('a paragraph'):
            new_par = x[1].split('\n\n')[2]
            en = ('<p class="en"><b>English:</b> the translation had no paragraph for this passage at all (about a hundred '
                  'Polish words at the start of your section 5). I translated it from the Polish, in your terms: '
                  '<mark>%s</mark></p>' % html.escape(new_par))
        else:
            en = '<p class="en"><b>English now:</b> %s</p>' % marked(x[0], x[1])
        item(n, where, r['weight'], marked(r['old'], r['new']), html.unescape(note(r['note'])), en)

    sense = []
    for r in F.ROWS:
        if r['kind'] == 'misread' and r['weight'] == 'court':
            sense.append('<section class="court"><h3>Leaf %s (page %d of 122)</h3><p class="pl"><s>%s</s><br>%s</p><p>%s</p></section>'
                         % (leaf(r['page']), order.index(r['page']) + 1, html.escape(r['old']), marked(r['old'], r['new']),
                            note(r['note'])))
    other = []
    for old, new, lf, why in en_other:
        other.append('<section><h3>Leaf %s</h3><p class="en"><s>%s</s><br>%s</p><p>%s</p></section>'
                     % (html.escape(lf), html.escape(old), marked(old, new), html.escape(why)))

    count = {w: sum(1 for r in dropped if r['weight'] == w) for w in VERDICT}
    count[EARLIER['weight']] += 1
    css = ('body{font:17px/1.55 Georgia,serif;max-width:900px;margin:2em auto;padding:0 16px;background:#fbfaf7;color:#222}'
           'section{margin:1.6em 0;padding:.2em 1em;border-left:5px solid #bbb;background:#fff}'
           'section.court{border-color:#b3261e}section.fact{border-color:#c98a00}section.formula{border-color:#9aa}'
           'h3{margin:.6em 0 .2em;font-size:1.05em}.v{font-weight:normal;font-size:.85em;color:#555;margin-left:.6em}'
           '.pl{font-style:italic}.en{color:#123}.say{color:#444}mark{background:#ffe58a}s{color:#999}'
           'h2{margin-top:2.5em;border-bottom:1px solid #ccc}')
    page = ('<!doctype html><html lang="en"><meta charset="utf-8"><title>Dropped phrases: APP 53/17/0/-/Konin Gr.145</title>'
            '<style>%s</style><h1>Dropped phrases: APP 53/17/0/-/Konin Gr.145</h1>'
            '<p>All 122 pages were read against the scans. The transcription lacked words in %d places. They are listed '
            'here in the order of the text, the restored words highlighted in the Polish (in italics) and in the English. '
            '<b>%d are significant</b> (red): they change what the record says the court found or did. %d add or correct a '
            'fact (amber). %d are legal wording or repetition (grey).</p>'
            '<p>The Polish and the English on the site are already corrected. If a reading looks wrong to you, tell me the '
            'number.</p><h2>1. The dropped phrases</h2>%s'
            '<h2>2. Misread words that changed what the court says</h2>'
            '<p>Not dropped, but read wrongly, in the court\'s own rulings. The English already had the right sense in '
            'each, except where part 3 says otherwise.</p>%s'
            '<h2>3. Other changes to the English</h2>'
            '<p>Places where the English had followed a misread word, and one where I read the Polish differently from '
            'the translation (the tower). Struck through is the English as it stood.</p>%s</html>'
            % (css, len(items), count['court'], count['fact'], count['formula'], '\n'.join(items), '\n'.join(sense),
               '\n'.join(other)))
    os.makedirs(OUT, exist_ok=True)
    io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)
    print('wrote', os.path.join(OUT, 'index.html'), ':', len(items), 'dropped phrases', count, ';', len(sense),
          'sense-changing misreadings;', len(other), 'other English changes')


if __name__ == '__main__':
    main()
