# -*- coding: utf-8 -*-
"""Spanning-note repair pass (print-verified cases only).

Class (a) runover: the previous page's last note continues at the top of
the receiving page's note block; the parse left those lines in the body.
  0048 -> 0047, 0054 -> 0053, 0065 -> 0064, 0119 -> 0118, 0132 -> 0131

Class (b) missed note 1: the print's first note sits above the parsed
first note top and was absorbed into the body.
  0064 (Przywilej dla Ol. Karpicko ...), 0114 (Prawdopodobnie wyrokiem
  sądowym ...), 0133 (AW. Krosna ... crafted from the 3x print read),
  0035 (Zagadnienie etymologii ...), 0031 (the Wymysłowo sigla block,
  merged into the stored note 1 - 'I.' is the print's marker '1.')

Also: the running footer ('Prace Komisji Atlasu hist. Polski, z. 5')
had been absorbed into 7 note texts - stripped; 0114's body '1
serwitutów' -> 'i serwitutów' and note 'pod owa Bede' -> 'pod słowami
Bede' (both print-verified).

Edits BOTH structure2.json (raw record) and structure4.json (text of
record; new texts get note_apply's leading-junk strip). The per-note
crop files (notetexts/) are renamed to the new numbering so a future
note_polish re-run cannot overwrite a renumbered note with a stale
crop. note_apply/note_polish are NOT re-run (they would clobber); the
chain resumes at marked_lines.py.
"""
import json, os, re, shutil

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
STRIP_RE = re.compile(
    r'^[\d!%*+$§£|.,)»\-—–?\s]+(?=[A-ZĄĆĘŁŃÓŚŹŻ„"(])')
FOOTER_RE = re.compile(
    r'\s*Prace Komisji Atlasu hist\. Polski,? z\. \S+(?: \S+)?\s*$')

# receiving page: (lo, hi) line-top window moved into prev page's last note
MOVES = {
    '0048': (2600, 3522),
    '0054': (2900, 4209),
    '0065': (3450, 4133),
    '0119': (3100, 3541),
    '0132': (2750, 3216),
}
# page: (lo, hi) body lines promoted to a NEW first note
NEW_NOTE1 = {
    '0064': (2200, 3404),
    '0114': (3700, 4119),
    '0035': (2450, 2781),
}
CRAFTED = {
    '0133': ('AW. Krosna, A. 1: „Bakałarza dla nabożeństwa pozwala im '
             'się,... który bakałarz\nwięcej sobie postępować nie '
             'powinien, tylko jako bakałarzowi należy dyssydenckiemu, '
             'bez\nkazania i śpiewania”.', 3619, (3500, 3927)),
}


def last_note(page):
    return max(page['notes'], key=lambda x: x['top'])


def move_lines(page, lo, hi):
    moved = [l for l in page['lines'] if lo < l['top'] < hi]
    page['lines'] = [l for l in page['lines'] if not (lo < l['top'] < hi)]
    return moved


def renumber(page):
    page['notes'].sort(key=lambda x: x['top'])
    for i, note in enumerate(page['notes']):
        note['num'] = i + 1


def repair(struct, is4):
    report = []
    # 0. footer strip
    for n in sorted(struct):
        for note in struct[n]['notes']:
            t = note['text']
            t2 = FOOTER_RE.sub('', t)
            if t2 != t:
                report.append('footer-strip %s #%s: ...%s' %
                              (n, note['num'], t2[-50:]))
                note['text'] = t2
    # 1. runover moves
    for recv, (lo, hi) in MOVES.items():
        prev = '%04d' % (int(recv) - 1)
        moved = move_lines(struct[recv], lo, hi)
        tgt = last_note(struct[prev])
        tgt['text'] = tgt['text'].rstrip() + '\n' + \
            '\n'.join(l['text'].strip() for l in moved)
        if is4:
            tgt['src'] = tgt.get('src', '') + '+span-repair'
        report.append('runover %s->%s: %d lines -> note %s (%d chars added)'
                      % (recv, prev, len(moved), tgt['num'],
                         sum(len(l['text']) for l in moved)))
    # 2. new first notes
    for n, (lo, hi) in NEW_NOTE1.items():
        page = struct[n]
        moved = move_lines(page, lo, hi)
        top = min(l['top'] for l in moved)
        raw = '\n'.join(l['text'].strip() for l in moved)
        text = raw if not is4 else STRIP_RE.sub('', raw).strip()
        page['notes'].insert(0, {'num': 1, 'top': top, 'num_read': 1,
                                 'text': text,
                                 **({'src': 'repair-note1'} if is4 else {})})
        renumber(page)
        report.append('new-note1 %s: %d lines (top %d), renumbered %d notes'
                      % (n, len(moved), top, len(page['notes'])))
    # 3. crafted note 1 (0133)
    n = '0133'
    text, top, (lo, hi) = CRAFTED[n]
    page = struct[n]
    moved = move_lines(page, lo, hi)
    text4 = STRIP_RE.sub('', text).strip()
    page['notes'].insert(0, {'num': 1, 'top': top, 'num_read': 1,
                             'text': text if not is4 else text4,
                             **({'src': 'repair-crafted'} if is4 else {})})
    renumber(page)
    report.append('crafted-note1 %s: %d lines replaced by print read, '
                  'renumbered %d notes' % (n, len(moved), len(page['notes'])))
    # 4. 0031 merge into note 1
    page = struct['0031']
    moved = move_lines(page, 2500, 3858)
    for l in moved:
        if l['top'] == 2585:
            l['text'] = l['text'].replace('I. Osada', '1. Osada', 1)
    note1 = min(page['notes'], key=lambda x: x['top'])
    head = '\n'.join(l['text'].strip() for l in moved)
    note1['text'] = head + '\n' + note1['text']
    note1['top'] = min(l['top'] for l in moved)
    if is4:
        note1['text'] = STRIP_RE.sub('', note1['text']).strip()
        note1['src'] = note1.get('src', '') + '+span-repair'
    report.append('merge-0031: %d lines prepended to note 1 '
                  '(top now %d)' % (len(moved), note1['top']))
    # 5. print-verified text fixes
    for l in struct['0114']['lines']:
        if l['top'] == 3409:
            if '1 serwitutów' in l['text']:
                l['text'] = l['text'].replace('1 serwitutów',
                                              'i serwitutów', 1)
                report.append('fix 0114 body: "i serwitutów"')
    for note in struct['0114']['notes']:
        if 'pod owa Bede' in note['text']:
            note['text'] = note['text'].replace('pod owa Bede',
                                                'pod słowami Bede', 1)
            report.append('fix 0114 note: "pod słowami Bede"')
    return report


def main():
    backs = []
    for name in ('structure2.json', 'structure4.json'):
        p = os.path.join(OCR, name)
        shutil.copy2(p, p + '.pre-span.bak')
        backs.append(name)
    print('backed up:', ', '.join(backs))
    reports = []
    structs = {}
    for name, is4 in (('structure2.json', False), ('structure4.json', True)):
        p = os.path.join(OCR, name)
        s = json.load(open(p, encoding='utf-8'))
        structs[name] = s
        r = repair(s, is4)
        reports.append((name, r))
        json.dump(s, open(p, 'w', encoding='utf-8', newline='\n'),
                  ensure_ascii=False)
    for name, r in reports:
        print('=====', name)
        for line in r:
            print('  ', line)
    # 6. notetexts renames (old num -> new num on renumbered pages)
    nt = os.path.join(OCR, 'notetexts')
    renames = [('0035', 5), ('0064', 3), ('0133', 4)]
    for n, k in renames:
        for old in range(k, 0, -1):
            src = os.path.join(nt, '%s_%d.json' % (n, old))
            if os.path.isfile(src):
                shutil.move(src, os.path.join(nt, '%s_%d.json' % (n, old + 1)))
        print('renamed notetexts %s: 1..%d -> 2..%d' % (n, k, k + 1))
    # 0114: its stored note count decides the rename range
    s4 = structs['structure4.json']
    k = len(s4['0114']['notes']) - 1  # after insert, old count = len-1
    for old in range(k, 0, -1):
        src = os.path.join(nt, '0114_%d.json' % old)
        if os.path.isfile(src):
            shutil.move(src, os.path.join(nt, '0114_%d.json' % (old + 1)))
    print('renamed notetexts 0114: 1..%d -> 2..%d' % (k, k + 1))
    # 0031: retire its note-1 crop (would clobber the merged note)
    src = os.path.join(nt, '0031_1.json')
    if os.path.isfile(src):
        shutil.move(src, src + '.pre-repair.bak')
        print('retired notetexts 0031_1.json -> .pre-repair.bak')


if __name__ == '__main__':
    main()
