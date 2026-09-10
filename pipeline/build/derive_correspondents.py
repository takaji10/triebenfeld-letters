# -*- coding: utf-8 -*-
"""Derive sender and recipient for each letter from its salutation and signature.

    python derive_correspondents.py            # derive, write json + review sheet
    python derive_correspondents.py --report   # show what was found, write nothing

`sender` and `recipient` have been declared in the letters.json schema since the
database was first built, and empty in all 318 records ever since. They matter
for the translation because register is not decoration in this correspondence:
Triebenfeld writing up to his prince ("Durchlauchtigster Fürst ... unterthänigster
Diener") and the prince writing down to his agent ("Hochwohlgebohrner Herr ...
Hochzuehrender Herr Kriegs und Forst Rath") are different voices, and flattening
them into one polite English register loses the thing the letters are mostly about.

The derivation is deliberately conservative. It reads the opening salutation and
the closing signature, both of which are highly formulaic here, and matches them
against a table of known forms. Where either end is unrecognised the letter is
left blank and listed in correspondents_review.csv for a ruling, rather than
guessed at - the same discipline used for names and places.

Output:
    correspondents.json         letter_id -> {sender, recipient, basis, confidence}
    correspondents_review.csv   the residue, for your ruling
"""
import os as _os, sys as _sys
# pipeline scripts are run directly from two levels down; make the project
# root importable so `import unitlib` and the sibling modules resolve
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import io, os, sys, re, csv, json
import unitlib
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UNIT = unitlib.one_unit(unitlib.unit_arg())
OUT = os.path.join(UNIT.dir, 'correspondents.json')
SHEET = os.path.join(ROOT, 'review', UNIT.slug, 'correspondents_review.csv')

PRINCE = 'Friedrich Ludwig, Fürst zu Hohenlohe-Ingelfingen'
AGENT = 'von Triebenfeld'
KING = 'König Friedrich Wilhelm III. von Preußen'

# Signature -> sender. Order matters: first match wins, so put the specific
# forms above the general ones.
SIGNS = [
    (r'F\.?\s*L\.?\s*F\.?\s*zu\s*Hohenlohe|F(ü|ue)rst zu Hohenlohe', PRINCE),
    (r'Charlotte\s+von\s+Triebenfeld', 'Charlotte von Triebenfeld'),
    (r'(Kriegs\s*Rath\s+)?v\.?\s*Triebenfeld|von\s+Triebenfeld', AGENT),
    (r'\bA[:.]?\s*Hahn\b|\bHahn\b', 'Hahn'),
    (r'v\.?\s*Sanitz', 'von Sanitz'),
    (r'\bStubenrauch\b', 'Stubenrauch'),
    (r'\bGlenck\b', 'Glenck'),
    (r'\bBeyme?\b', 'Beyme'),
    (r'\bBequelin\b|\bBeugelin\b', 'Beugelin'),
    (r'\bGruemann\b', 'Gruemann[?]'),
    (r'\bGrewen', 'Grewen[z?]'),
    (r'\bHecker\b.*\bHonrichs\b|\bHonrichs\b.*\bHecker\b', 'Hecker and Honrichs'),
    (r'\bSmiedecki\b', 'Smiedecki'),
]

# Salutation -> recipient.
SALUTES = [
    (r'Euer\s+K(ö|oe)nigl\w*\.?\s+Majest', KING),
    (r'Allerdurchlauchtigster', KING),
    (r'Durchlauchtigster?\s+F(ü|ue)rst|Durchl(ä|eu)uchtigster', PRINCE),
    (r'Gn(ä|ae)digster\s+F(ü|ue)rst\s+und\s+Herr', PRINCE),
    (r'Hochf(ü|ue)rstliche\s+Durchlaucht', PRINCE),
    (r'Monseigneur', PRINCE),
    (r'Hochwohlgeb\w*\s+Herr', AGENT),
    (r'Hochzuehrender\s+Herr|Hochgeehrtester\s+Herr', AGENT),
    (r'Wohlgeborner\s+Herr', AGENT),
    (r'Gn(ä|ae)digster\s+Herr', PRINCE),
]

# The "Hochwohlgebohrner Herr" style is used for Triebenfeld by name often
# enough to confirm the reading; when the body names the office it is certain.
AGENT_OFFICE = re.compile(r'Kriegs?\s*(und)?\s*Forst\s*Ra(th|t)', re.I)

# Many letters open mid-flow with no salutation at all. The recipient is still
# recoverable from the form of address used throughout the body - a letter that
# says "Ewr Durchlaucht" twenty times is written to the prince whether or not it
# bothered to say so at the top. This is evidence, not assumption, so it is
# used - but only for the recipient. Nothing in the address form identifies the
# SENDER, so an unsigned letter is left unsigned rather than guessed at, even
# where one correspondent would be overwhelmingly likely.
BODY_PRINCE = re.compile(
    r'(Ewr|Ewer|Euer|Ew\.?)\s+(Hochf(ü|ue)rstliche\s+)?Durchlaucht|Höchstdieselben', re.I)
BODY_AGENT = re.compile(r'(Ew|Ewr|Euer)\.?\s+Hochwohlgeb|Hochzuehrender', re.I)


def head_tail(text, n_head=6, n_tail=8):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return '\n'.join(lines[:n_head]), '\n'.join(lines[-n_tail:])


def match(table, blob):
    for pat, who in table:
        if re.search(pat, blob, re.I):
            return who, pat
    return '', ''


def derive(rec):
    text = rec.get('text') or ''
    if not text.strip():
        return {'sender': '', 'recipient': '', 'basis': 'no text', 'confidence': 'none'}
    head, tail = head_tail(text)
    sender, s_pat = match(SIGNS, tail)
    recipient, r_pat = match(SALUTES, head)

    # A letter addressed to the Kriegs- und Forstrath is addressed to Triebenfeld,
    # which also means he is not the one signing it.
    if recipient == AGENT and AGENT_OFFICE.search(head):
        basis_extra = ' +office named'
    else:
        basis_extra = ''

    # No salutation: fall back to the address form used in the body.
    from_body = False
    if not recipient:
        p, a = len(BODY_PRINCE.findall(text)), len(BODY_AGENT.findall(text))
        if p > a:
            recipient, from_body = PRINCE, True
        elif a > p:
            recipient, from_body = AGENT, True

    # Guard against reading the same person as both ends: the salutation table
    # keys on style, and a copy of a document can carry someone else's greeting.
    if sender and sender == recipient:
        sender = ''

    if sender and recipient:
        conf = 'body' if from_body else 'high'
    elif sender or recipient:
        conf = 'partial'
    else:
        conf = 'none'
    sal = 'body address form' if from_body else f'sal:{r_pat[:24]}'
    basis = f'sig:{s_pat[:24]}|{sal}{basis_extra}' if conf != 'none' else 'unmatched'
    return {'sender': sender, 'recipient': recipient, 'basis': basis, 'confidence': conf}


def main():
    recs = unitlib.load_documents(ROOT)
    # Scoped to this unit: the merged file holds every holding, and `out` is
    # keyed by a bare archival number, so without this one unit's correspondents
    # land in another's file and documents sharing an id overwrite each other.
    recs = [r for r in recs if r['unit'] == UNIT.slug]
    print(f'{UNIT.slug}: {len(recs)} document(s)')
    out, residue = {}, []
    tally = {'high': 0, 'body': 0, 'partial': 0, 'none': 0}
    for r in recs:
        lid = str(r['letter_id'])
        d = derive(r)
        out[lid] = d
        tally[d['confidence']] += 1
        if d['confidence'] not in ('high', 'body'):
            head, tail = head_tail(r.get('text') or '', 3, 4)
            residue.append({
                'letter_id': lid,
                'date': r.get('date_display', ''),
                'sender': d['sender'], 'recipient': d['recipient'],
                'opens': head.replace('\n', ' / ')[:70],
                'closes': tail.replace('\n', ' / ')[:70],
                'ruling_sender': '', 'ruling_recipient': '',
            })

    print(f'{len(recs)} letters: ' + ', '.join(f'{k} {v}' for k, v in tally.items()))
    pairs = {}
    for d in out.values():
        if d['confidence'] in ('high', 'body'):
            pairs[(d['sender'], d['recipient'])] = pairs.get((d['sender'], d['recipient']), 0) + 1
    print('\nconfident pairings:')
    for (s, rc), n in sorted(pairs.items(), key=lambda x: -x[1]):
        print(f'  {n:>4}  {s}  ->  {rc}')

    if '--report' in sys.argv:
        print('\n(report only - nothing written)')
        return

    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
    with open(SHEET, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, ['letter_id', 'date', 'sender', 'recipient',
                               'opens', 'closes', 'ruling_sender', 'ruling_recipient'])
        w.writeheader()
        w.writerows(residue)
    print(f'\nwrote {OUT}')
    print(f'wrote {SHEET}  -  {len(residue)} letter(s) needing a ruling')


if __name__ == '__main__':
    main()
