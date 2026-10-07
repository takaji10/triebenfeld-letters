# -*- coding: utf-8 -*-
"""One page of what checking against the scans changed, across holdings.

    python pipeline/review/changes_page.py            # every holding that has a changes.yml
    python pipeline/review/changes_page.py --era prusimski-boundary

Writes review/changes/index.html. For the editor, who has written about
these documents outside the project from the earlier texts and needs to know
what to put right there (2026-10-07: "a page showing dropped phrases and
their importance, since I need to update some writing outside of the
project").

It reads units/<slug>/intake/changes.yml: a list of changes, each with an
importance (significant: changes what the record says happened or was
ordered; fact: adds or corrects a fact; wording: nothing to act on), what
changed in a sentence, and the words as they were and as they are. A holding
writes that file by hand when it is checked, or from its own record of the
check. Holdings are listed by the date of their documents.

The editor read the page on 2026-10-07 and keeps it to work from. A change
written after that carries `new: "<what it comes from>"` (the full check of a
holding, a text first transcribed here): it is marked NEW on the page and
counted at the top, so that the editor can find what they have not yet seen.
The mark stays until the editor says they have read those.
"""
import argparse
import html
import io
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
import unitlib  # noqa: E402

LABEL = {'significant': 'Significant', 'fact': 'A fact', 'wording': 'Wording only'}
SAY = {'significant': 'changes what the record says happened or was ordered',
       'fact': 'adds or corrects a fact; the outcome is the same',
       'wording': 'legal wording or a repetition; nothing to act on'}
ORDER = ['significant', 'fact', 'wording']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--era', default=None)
    a = ap.parse_args()
    unitlib.utf8_stdout()
    units = []
    for u in unitlib.load_units():
        p = os.path.join(ROOT, 'units', u.slug, 'intake', 'changes.yml')
        if not os.path.isfile(p) or (a.era and (u.get('era') or '') != a.era):
            continue
        d = yaml.safe_load(io.open(p, encoding='utf-8'))
        units.append((str(u.get('date_span') or ''), u.slug, d))
    units.sort()
    total = {k: 0 for k in ORDER}
    fresh = 0
    parts, toc = [], []
    for _span, slug, d in units:
        count = {k: sum(1 for c in d['changes'] if c['importance'] == k) for k in ORDER}
        for k in ORDER:
            total[k] += count[k]
        n_new = sum(1 for c in d['changes'] if c.get('new'))
        fresh += n_new
        toc.append('<li><a href="#%s">%s</a>: %d significant, %d facts, %d wording%s</li>'
                   % (slug, html.escape(d['unit']), count['significant'], count['fact'], count['wording'],
                      (' <span class="tag new">%d new</span>' % n_new) if n_new else ''))
        rows = []
        for k in ORDER:
            for c in [c for c in d['changes'] if c['importance'] == k]:
                bits = ['<p class="what"><span class="tag %s">%s</span>%s %s%s</p>'
                        % (k, LABEL[k],
                           ('<span class="tag new" title="%s">New</span>' % html.escape(str(c['new']))) if c.get('new') else '',
                           ('<span class="where">%s.</span> ' % html.escape(c['where'])) if c.get('where') else '',
                           html.escape(c['what']))]
                for key, name in (('was', 'Text as it was'), ('now', 'Text now'),
                                  ('english_was', 'English as it was'), ('english_now', 'English now')):
                    if c.get(key):
                        bits.append('<p class="q %s"><b>%s:</b> %s</p>'
                                    % ('old' if key.endswith('was') else 'new', name, html.escape(str(c[key]))))
                rows.append('<section class="%s">%s</section>' % (k, ''.join(bits)))
        parts.append('<h2 id="%s">%s</h2>%s' % (slug, html.escape(d['unit']), '\n'.join(rows)))
    css = ('body{font:17px/1.55 Georgia,serif;max-width:920px;margin:2em auto;padding:0 16px;background:#fbfaf7;color:#222}'
           'section{margin:1.1em 0;padding:.1em 1em;border-left:5px solid #bbb;background:#fff}'
           'section.significant{border-color:#b3261e}section.fact{border-color:#c98a00}section.wording{border-color:#9aa}'
           '.tag{font:bold 12px/1 Arial,sans-serif;text-transform:uppercase;padding:.25em .5em;border-radius:3px;color:#fff;'
           'margin-right:.5em}.tag.significant{background:#b3261e}.tag.fact{background:#c98a00}.tag.wording{background:#89a}'
           '.tag.new{background:#1a6b3c}'
           '.where{color:#555}.q{font-size:.93em;margin:.3em 0}.q.old{color:#777}.q.new{color:#123}'
           'h2{margin-top:2.4em;border-bottom:1px solid #ccc}.what{margin:.6em 0 .3em}')
    page = ('<!doctype html><html lang="en"><meta charset="utf-8"><title>What the check against the scans changed</title>'
            '<style>%s</style><h1>What the check against the scans changed</h1>'
            '<p>For putting right what you have written elsewhere from the earlier texts. %d holdings so far. Each change '
            'is graded: <b>significant</b> (%d), it %s; <b>a fact</b> (%d), it %s; <b>wording only</b> (%d), %s. '
            'Within a holding the significant ones come first.</p>'
            '<p>The texts in the edition are already corrected. This page is made again as each holding is checked.</p>'
            '%s<ul>%s</ul>%s</html>'
            % (css, len(units), total['significant'], SAY['significant'], total['fact'], SAY['fact'], total['wording'],
               SAY['wording'],
               ('<p><span class="tag new">New</span> %d changes were written after you read this page on 7 October 2026 '
                '(full checks, and texts first transcribed here). They carry this green mark, and the list below says '
                'which holdings have them.</p>' % fresh) if fresh else '',
               '\n'.join(toc), '\n'.join(parts)))
    out = os.path.join(ROOT, 'review', 'changes')
    os.makedirs(out, exist_ok=True)
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)
    print('wrote', os.path.join(out, 'index.html'), ':', len(units), 'holdings;', total, '; new:', fresh)


if __name__ == '__main__':
    main()
