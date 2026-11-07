# -*- coding: utf-8 -*-
"""Whole-book coverage + section stats of the finished transcription."""
import re

T = open(r'literature\rusinski1947\original.md', encoding='utf-8').read()
lines = T.splitlines()

# page markers present
labels = []
for ln in lines:
    m = re.match(r'^\[p\. (\w+)\]$', ln.strip())
    if m:
        labels.append(m.group(1))
nums = [int(l) for l in labels if l.isdigit()]
print('page labels: %d total; arabic %d (min %s max %s); roman %s'
      % (len(labels), len(nums), min(nums) if nums else '-',
         max(nums) if nums else '-', [l for l in labels if not l.isdigit()]))

# coverage gaps in the arabic run
missing = [n for n in range(min(nums), max(nums) + 1) if n not in set(nums)]
print('missing page labels in %d-%d: %s'
      % (min(nums), max(nums), missing if missing else 'none'))

# sheets in the annex zone
sheets = re.findall(r'<!-- annex sheet (\d+) -->', T)
print('annex sheet markers:', len(sheets), sheets[:5], '...')

# section sizes (words)
def words(s):
    return len(re.sub(r'\[\^\w+-\d+\]', ' ', s).split())

secs = [
    ('front matter', 0, T.find('[p. 1]')),
    ('body pp. 1-26 (ch. I-II + tables)', T.find('[p. 1]'), T.find('[p. 27]')),
    ('body pp. 27-54', T.find('[p. 27]'), T.find('[p. 55]')),
    ('body pp. 55-88', T.find('[p. 55]'), T.find('[p. 89]')),
    ('body pp. 89-122', T.find('[p. 89]'), T.find('[p. 123]')),
    ('ANEKS I pp. 123-144', T.find('[p. 123]'), T.find('[p. 145]')),
    ('ANEKS II-III pp. 145-150', T.find('[p. 145]'), T.find('[p. 157]')),
    ('plates', T.find('[p. 157]'), len(T)),
]
tot = 0
for name, a, b in secs:
    w = words(T[a:b])
    tot += w
    print('%-36s %7d words' % (name, w))
print('%-36s %7d words' % ('TOTAL', tot))
refs = len(re.findall(r'\[\^\w+-\d+\](?!:)', T))
defs = len(re.findall(r'\[\^\w+-\d+\]:', T))
print('refs: %d  defs: %d' % (refs, defs))
