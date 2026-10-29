"""The spaced en dash in the site's own prose (the editor, 2026-10-20 and
2026-10-29; EDITORS_VOICE, "The editor's rulings on the pilot").

A hyphen standing for a dash (" - ") and an em dash ("—", spaced or not)
become the spaced en dash ( – ). Only the site's own prose is touched:

  units/*/about*.md, units/*/process*.md   the whole text but code spans,
                                           HTML comments and link targets
  literature/*/work.yml                    account_*, brief_*, summary_*
  newspapers/*/item.yml                    account_*, brief_*
  literature/links.yml                     en, de
  reference/people_bios.yml                bio, bio_de
  reference/genealogy.yml                  bio, bio_de, note, notes, notes_de
  reference/glossary.yml                   short_*, long_*

A quotation ("...", “...”, „...“, «...», ‚...‘) keeps its own dashes, as does
every other field (titles, citations). Never a transcription, reading copy or
translation. The document summaries are not here: a summary is kept in
several places and is changed with them (WORKING_NOTES, "Where one summary is
kept").

Usage: python pipeline/review/dash_fix.py [--dry]
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUOTE = re.compile(r'"[^"\n]*(?:\n[^"\n]*)*?"|“[^”]*”|„[^“”]*[“”]|«[^»]*»|‚[^‘]*‘')
PROTECT_MD = re.compile(r'`[^`]*`|<!--.*?-->|\]\([^)]*\)|\{\{[^}]*\}\}|\{%[^%]*%\}', re.S)
HYPHEN = re.compile(r'(?<=\S)([ \t]+|[ \t]*\n[ \t]*)-(?=[ \t]+\S|[ \t]*\n[ \t]*\S)')
EM_SPACED = re.compile(r'(?<=\s)—(?=\s)')
EM_TIGHT = re.compile(r'(?<=\w)—(?=\w)')

KEYS = {
    'work.yml': {'account_en', 'account_de', 'brief_en', 'brief_de', 'summary_en', 'summary_de'},
    'item.yml': {'account_en', 'account_de', 'brief_en', 'brief_de'},
    'links.yml': {'en', 'de'},
    'people_bios.yml': {'bio', 'bio_de'},
    'genealogy.yml': {'bio', 'bio_de', 'note', 'notes', 'notes_de'},
    'glossary.yml': {'short_en', 'short_de', 'long_en', 'long_de'},
}


def fix(text, protect):
    """The dashes of `text` outside quotations and the protected spans."""
    spans = [m.span() for m in protect.finditer(text)] + [m.span() for m in QUOTE.finditer(text)]
    def free(i):
        return not any(a <= i < b for a, b in spans)
    out, n = list(text), 0
    for m in HYPHEN.finditer(text):
        i = m.end() - 1
        if free(i):
            out[i] = '–'; n += 1
    for m in EM_SPACED.finditer(text):
        if free(m.start()):
            out[m.start()] = '–'; n += 1
    for m in EM_TIGHT.finditer(text):
        if free(m.start()):
            out[m.start()] = ' – '; n += 1
    return ''.join(out), n


def yaml_blocks(lines, keys):
    """(start, end) line ranges of the values of `keys` in a YAML file's text."""
    rx = re.compile(r'^(\s*)(?:-\s+)?([A-Za-z_]+):(.*)$')
    indent = lambda s: len(s) - len(s.lstrip())
    i = 0
    while i < len(lines):
        m = rx.match(lines[i])
        if m and m.group(2) in keys:
            ind = indent(lines[i])
            j = i + 1
            # the value runs on while the lines are blank or indented deeper
            while j < len(lines) and (not lines[j].strip() or indent(lines[j]) > ind):
                j += 1
            while j > i + 1 and not lines[j - 1].strip():
                j -= 1
            yield i, j
            i = j
        else:
            i += 1


def main():
    dry = '--dry' in sys.argv
    os.chdir(ROOT)
    total = 0
    md = sorted(glob.glob('units/*/about*.md') + glob.glob('units/*/process*.md'))
    for f in md:
        t = open(f, encoding='utf-8', newline='').read()
        t2, n = fix(t, PROTECT_MD)
        if n:
            total += n
            if not dry:
                open(f, 'w', encoding='utf-8', newline='').write(t2)
    ymls = (glob.glob('literature/*/work.yml') + glob.glob('newspapers/*/item.yml')
            + ['literature/links.yml', 'reference/people_bios.yml', 'reference/genealogy.yml', 'reference/glossary.yml'])
    for f in sorted(ymls):
        keys = KEYS[os.path.basename(f)]
        t = open(f, encoding='utf-8', newline='').read()
        lines = t.split('\n')
        n_file = 0
        for a, b in list(yaml_blocks(lines, keys)):
            block = '\n'.join(lines[a:b])
            head, sep, rest = block.partition(':')
            new, n = fix(rest, re.compile(r'(?!)'))
            if n:
                n_file += n
                lines[a:b] = (head + sep + new).split('\n')
        if n_file:
            total += n_file
            if not dry:
                open(f, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
    print(total, 'dashes made the spaced en dash', '(dry run)' if dry else '')


if __name__ == '__main__':
    main()
