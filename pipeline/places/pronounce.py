# -*- coding: utf-8 -*-
"""
IPA pronunciations of Polish place names, made from the spelling by rule
(the editor, 2026-11-24: "phonetic pronunciations of place names ... in small
text after the main representation of the name"; their choice: generated for
Polish names, each checked by Claude, a sample shown to them first).

Polish spelling is close to phonemic, so a short set of rules gives the
standard pronunciation: digraphs (ch, cz, dz, dź, dż, rz, sz) and the
softening i (si, ci, zi, ni, dzi before a vowel); nasal vowels; word-final
devoicing; w and rz unvoiced after a voiceless consonant; stress on the
second-to-last syllable. The output is a proposal: reference/pronunciations.yml
holds what was checked (`checked: true`), and only checked entries are shown.

    python pipeline/places/pronounce.py "Świątniki"     # one name
    python pipeline/places/pronounce.py --places        # every Polish place
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

VOWELS = 'aąeęioóuy'
# (spelling, sound) in the order they must be tried: longest first
SOFT = [('dzi', 'dʑ'), ('si', 'ɕ'), ('ci', 'tɕ'), ('zi', 'ʑ'), ('ni', 'ɲ')]
DIGRAPHS = [('au', 'aw'), ('dź', 'dʑ'), ('dż', 'dʐ'), ('dz', 'dz'), ('ch', 'x'), ('cz', 'tʂ'),
            ('rz', 'ʐ'), ('sz', 'ʂ')]
SINGLE = {'a': 'a', 'ą': 'ɔ̃', 'b': 'b', 'c': 'ts', 'ć': 'tɕ', 'd': 'd', 'e': 'ɛ',
          'ę': 'ɛ̃', 'f': 'f', 'g': 'ɡ', 'h': 'x', 'i': 'i', 'j': 'j', 'k': 'k',
          'l': 'l', 'ł': 'w', 'm': 'm', 'n': 'n', 'ń': 'ɲ', 'o': 'ɔ', 'ó': 'u',
          'p': 'p', 'r': 'r', 's': 's', 'ś': 'ɕ', 't': 't', 'u': 'u', 'w': 'v',
          'y': 'ɨ', 'z': 'z', 'ź': 'ʑ', 'ż': 'ʐ', 'x': 'ks', 'q': 'k', 'v': 'v'}
VOICELESS = {'p', 't', 'k', 'f', 's', 'ɕ', 'ʂ', 'x', 'ts', 'tɕ', 'tʂ'}
DEVOICE = {'b': 'p', 'd': 't', 'ɡ': 'k', 'v': 'f', 'z': 's', 'ʐ': 'ʂ', 'ʑ': 'ɕ',
           'dz': 'ts', 'dʑ': 'tɕ', 'dʐ': 'tʂ'}
VOWEL_SOUNDS = {'a', 'ɔ̃', 'ɛ', 'ɛ̃', 'i', 'ɔ', 'u', 'ɨ'}


def segments(word):
    """The word as a list of sounds, each marked vowel or consonant."""
    w = word.lower()
    out, i = [], 0
    while i < len(w):
        ch = w[i]
        if not ch.isalpha():
            i += 1
            continue
        done = False
        for sp, snd in SOFT:
            if w.startswith(sp, i):
                nxt = w[i + len(sp)] if i + len(sp) < len(w) else ''
                out.append(snd)
                if nxt and nxt in VOWELS:   # the i only softens
                    i += len(sp)
                else:                       # the i is a vowel too
                    out.append('i')
                    i += len(sp)
                done = True
                break
        if done:
            continue
        for sp, snd in DIGRAPHS:
            if w.startswith(sp, i):
                out.append(snd)
                i += len(sp)
                done = True
                break
        if done:
            continue
        # i between a consonant and a vowel is a glide (Pierwszy, Mariantów)
        if (ch == 'i' and out and out[-1] not in VOWEL_SOUNDS
                and i + 1 < len(w) and w[i + 1] in VOWELS):
            out.append('j')
            i += 1
            continue
        out.append(SINGLE.get(ch, ch))
        i += 1
    # rz and w after a voiceless consonant are voiceless (trzy, Świątniki)
    for k in range(1, len(out)):
        if out[k] in ('ʐ', 'v') and out[k - 1] in VOICELESS:
            out[k] = 'ʂ' if out[k] == 'ʐ' else 'f'
    # voicing assimilates backwards through a consonant cluster before a
    # voiceless consonant, and at the end of the word
    for k in range(len(out) - 1, -1, -1):
        nxt = out[k + 1] if k + 1 < len(out) else None
        if out[k] in DEVOICE and (nxt is None or nxt in VOICELESS):
            out[k] = DEVOICE[out[k]]
    # nasal vowels: before a stop or affricate they are a vowel and a nasal;
    # ę at the end of a word is a plain e
    for k, s in enumerate(out):
        if s in ('ɔ̃', 'ɛ̃'):
            nxt = out[k + 1] if k + 1 < len(out) else None
            base = 'ɔ' if s == 'ɔ̃' else 'ɛ'
            if nxt in ('p', 'b'):
                out[k] = base + 'm'
            elif nxt in ('t', 'd', 'ts', 'dz', 'tʂ', 'dʐ'):
                out[k] = base + 'n'
            elif nxt in ('tɕ', 'dʑ'):
                out[k] = base + 'ɲ'
            elif nxt in ('k', 'ɡ'):
                out[k] = base + 'ŋ'
            elif nxt is None and s == 'ɛ̃':
                out[k] = 'ɛ'
    return out


def word_ipa(word):
    segs = segments(word)
    vix = [k for k, s in enumerate(segs) if s[0] in 'aɔɛiuɨ']
    if len(vix) >= 2:
        # stress the second-to-last syllable: mark before its onset
        v = vix[-2]
        start = v
        prev_v = vix[-3] if len(vix) >= 3 else -1
        # the onset: the consonants before the vowel, leaving one for the
        # syllable before where there are two or more
        cons = list(range(prev_v + 1, v))
        if len(cons) >= 2:
            start = cons[1] if prev_v >= 0 else cons[0]
            # a consonant and the glide j, or an obstruent and r, l, ł,
            # start the syllable together (maˈrjantuf, xaˈɡrɔvɔ)
            if prev_v >= 0 and (segs[cons[-1]] == 'j' or (
                    segs[cons[-1]] in ('r', 'l', 'w')
                    and segs[cons[-2]] not in ('r', 'l', 'w', 'm', 'n', 'ɲ', 'j'))):
                start = cons[-2]
        elif cons:
            start = cons[0]
        segs = segs[:start] + ['ˈ'] + segs[start:]
    return ''.join(segs)


NOT_POLISH = {'river'}


def ipa(name):
    words = [w for w in name.replace('-', ' ').replace(',', ' ').split()
             if len(w) > 1 and w.lower() not in NOT_POLISH]
    return ' '.join(word_ipa(w) for w in words)


def main(argv):
    if argv and argv[0] != '--places':
        print(ipa(' '.join(argv)))
        return 0
    import yaml
    with open(os.path.join(ROOT, 'site', '_data', 'places_index.yml'), encoding='utf-8') as fh:
        idx = yaml.safe_load(fh)
    for r in idx['tier1']:
        if r.get('see'):
            continue
        print(f"{r['slug']}\t{r['name']}\t/{ipa(r['name'])}/")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
