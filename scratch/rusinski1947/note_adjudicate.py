# -*- coding: utf-8 -*-
"""The 38 rejected per-note cases, adjudicated BY READING (2026-11-05).

Each entry: (scan, note, verdict) where verdict is
  'adopt3x'    the 3x crop is the same note and better - adopt it;
  'keeppage'   the crop caught table debris / a wrong note - the page
               text stands;
  'spot'       the two witnesses genuinely diverge - the spot sheet
               decides with both crops shown.

The readings behind each verdict are in note_reject.csv (the record of
the disagreement); this file carries only the decisions.
"""

ADJUDICATED = {
    ('0024', 1): 'adopt3x',   # 'L Kremmer...' = page's 'Kremmer...' (artifact L)
    ('0026', 2): 'adopt3x',   # identical but the '?' artifact prefix
    ('0026', 3): 'keeppage',  # crop caught rule-line debris
    ('0032', 3): 'keeppage',  # crop caught debris
    ('0046', 2): 'adopt3x',   # same sentence, cleaner
    ('0050', 2): 'adopt3x',   # page text broken ('Wedlug s. czynscy.');
                              # 3x reads the note properly
    ('0050', 6): 'keeppage',  # crop caught debris
    ('0055', 4): 'keeppage',  # crop caught debris
    ('0059', 1): 'adopt3x',   # page glued the next note's tail ('10820...')
    ('0063', 2): 'adopt3x',   # ratio 0.83, same note
    ('0063', 3): 'adopt3x',   # page text broken; 3x proper
    ('0064', 2): 'keeppage',  # crop caught debris
    ('0067', 1): 'adopt3x',   # same text (ratio artifact of short text)
    ('0077', 1): 'keeppage',  # a TABELA row, not a note (page parse err)
    ('0077', 2): 'keeppage',  # as above
    ('0079', 1): 'keeppage',  # table row
    ('0079', 3): 'keeppage',  # table row
    ('0079', 4): 'keeppage',  # table row
    ('0084', 3): 'adopt3x',   # page dropped 'np. w'; 3x complete
    ('0091', 3): 'keeppage',  # crop empty
    ('0096', 4): 'adopt3x',   # same note, page mangled 'Huta'
    ('0096', 5): 'spot',      # divergent openings - decide on the crops
    ('0096', 10): 'keeppage', # crop caught debris
    ('0099', 5): 'spot',      # divergent content - decide on the crops
    ('0108', 1): 'keeppage',  # crop empty
    ('0108', 6): 'adopt3x',   # page glued the next note's tail
    ('0108', 7): 'adopt3x',   # page broken mid-citation; 3x proper
    ('0110', 4): 'keeppage',  # 3x more mangled than the page here
    ('0113', 4): 'adopt3x',   # same text, cleaner
    ('0113', 5): 'adopt3x',   # page broken; 3x proper ('W r. 1773
                              # Komisja...')
    ('0114', 7): 'keeppage',  # crop caught debris
    ('0122', 2): 'keeppage',  # crop caught debris
    ('0122', 5): 'adopt3x',   # same text, cleaner
    ('0127', 3): 'adopt3x',   # quote-variant only
    ('0130', 3): 'adopt3x',   # page dropped 's. '
    ('0131', 1): 'adopt3x',   # page broken ('47 a, Nie w (Szk.');
                              # 3x proper
    ('0131', 5): 'adopt3x',   # same text, cleaner
    ('0136', 1): 'adopt3x',   # page badly broken; 3x proper
}
