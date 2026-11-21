# -*- coding: utf-8 -*-
"""Systematic artifact scan of the composed draft: count and locate the
residual OCR artifact classes in the final text."""
import re, collections

T = open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\literature\rusinski1947\original.md',
         encoding='utf-8').read()
PATS = {
    'pct_art': r'\b\d{1,3}\s*[%9§]\s*/\s*[,.;:]?',
    'frac_art': r'\b\d{1,3}\s*/\s*[,gso0OrS]{1,2}\b',
    'slash_comma': r'/,',
    'dup_frag': r'\b([A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{4,})- \1',
    'dup_frag2': r'\b([A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{3,})- ([A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]*\1[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]*)',
    'lone_glyph': r'(?<![\w%])[§£@€](?![\w])',
    'double_qq': r'\?\?|\?\.',
    'OIL': r'\bO[I1l]L\b',
    'digit_in_word': r'[a-ząćęłńóśźż]1[a-ząćęłńóśźż]',
    'zero_in_word': r'[A-ZĄĆĘŁŃÓŚŹŻa-ząćęłńóśźż]0[a-ząćęłńóśźż]',
    'hyphen_space_midword': r'[a-ząćęłńóśźż]- [a-ząćęłńóśźż]',
    'quotes_glued': r'„"|"”',
    'tab_pipe_in_body': r'\|',
    'sentence_ends_comma': r',\s*\n',
}
counts = {}
for k, p in PATS.items():
    ms = list(re.finditer(p, T))
    counts[k] = len(ms)
    if ms and k in ('pct_art', 'frac_art', 'slash_comma', 'dup_frag',
                    'dup_frag2', 'OIL', 'lone_glyph'):
        print(f'=== {k}: {len(ms)}')
        shown = 0
        for m in ms:
            ctx = T[max(0, m.start() - 50):m.end() + 40].replace('\n', ' / ')
            print('   ', repr(ctx[:110]))
            shown += 1
            if shown >= 8:
                print('    ...')
                break
print()
for k in ('double_qq', 'digit_in_word', 'zero_in_word',
          'hyphen_space_midword', 'tab_pipe_in_body'):
    print(k, counts[k])
