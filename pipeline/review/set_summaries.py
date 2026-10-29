"""Carry a changed document summary into every place it is kept (WORKING_NOTES,
"Where one summary is kept"; the voice review, docs/VOICE_REVIEW_PLAN.md).

The batch file (YAML) maps a pad (oe1bu14525-021) to `en` and/or `de`, each
with `text:`, the whole new summary. For each it rewrites:

  site/_data/summaries.yml / summaries_de.yml   the site's copies, one line each
  units/<slug>/summaries_de.yml                 the holding's German, if it has the pad
  cache/summaries-raw[-de]/<pad>.json           the cache (`summary`), if present
  units/<slug>/intake/summaries_draft.py and    the drafting record: the old text is
  units/<slug>/intake/english*.py               replaced only where it stands as one
                                                string; otherwise reported

Then run pipeline/build/build_dataset.py and build_site_data.py, which copy the
site's summaries into dataset/ and the pages. The claim checks
(intake/claim_check.yml) hold statements, not the wording, and are left.

Usage: python pipeline/review/set_summaries.py <batch.yml> [--dry]
"""
import glob, json, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def one_line(pad, text):
    return yaml.safe_dump({pad: text}, allow_unicode=True, width=10 ** 9, sort_keys=False).rstrip('\n')


def set_yaml_line(path, pad, text):
    """Replace the entry `pad:` of a flat YAML map; True if it was there."""
    lines = open(path, encoding='utf-8', newline='').read().split('\n')
    for i, ln in enumerate(lines):
        if ln.startswith(pad + ':'):
            j = i + 1
            while j < len(lines) and lines[j].startswith((' ', '\t')):
                j += 1
            lines[i:j] = one_line(pad, text).split('\n')
            new = '\n'.join(lines)
            assert yaml.safe_load(new)[pad] == text, path
            return new
    return None


def main():
    batch = yaml.safe_load(open(sys.argv[1], encoding='utf-8'))
    dry = '--dry' in sys.argv
    os.chdir(ROOT)
    site = {'en': 'site/_data/summaries.yml', 'de': 'site/_data/summaries_de.yml'}
    cache = {'en': 'cache/summaries-raw', 'de': 'cache/summaries-raw-de'}
    old_site = {l: yaml.safe_load(open(p, encoding='utf-8')) for l, p in site.items()}
    writes, report = {}, []
    def text_of(p):
        return writes.get(p) or open(p, encoding='utf-8', newline='').read()
    for pad, langs in batch.items():
        slug = pad.rsplit('-', 1)[0]
        for lang, v in langs.items():
            new = ' '.join(str(v['text']).split())
            old = old_site[lang].get(pad)
            if old is None:
                raise SystemExit(f'{pad} {lang}: not in {site[lang]}')
            if new == old:
                continue
            got = set_yaml_line(site[lang], pad, new) if site[lang] not in writes else None
            if site[lang] in writes:
                tmp = site[lang] + '.tmp'
                open(tmp, 'w', encoding='utf-8', newline='').write(writes[site[lang]])
                got = set_yaml_line(tmp, pad, new); os.remove(tmp)
            writes[site[lang]] = got
            places = ['site']
            if lang == 'de':
                u = f'units/{slug}/summaries_de.yml'
                if os.path.exists(u):
                    tmp = u + '.tmp'
                    open(tmp, 'w', encoding='utf-8', newline='').write(text_of(u))
                    got = set_yaml_line(tmp, pad, new); os.remove(tmp)
                    if got is not None:
                        writes[u] = got; places.append('unit')
            c = os.path.join(cache[lang], pad + '.json')
            if os.path.exists(c):
                d = json.load(open(c, encoding='utf-8'))
                if d.get('summary') is not None:
                    d['summary'] = new
                    writes[c] = json.dumps(d, ensure_ascii=False, indent=2) + '\n'
                    places.append('cache')
            drafts = glob.glob(f'units/{slug}/intake/summaries_draft.py') + glob.glob(f'units/{slug}/intake/english*.py')
            hit = False
            for dp in drafts:
                t = text_of(dp)
                for q in ("'", '"'):
                    lit = q + old.replace('\\', '\\\\').replace(q, '\\' + q) + q
                    if lit in t:
                        t = t.replace(lit, q + new.replace('\\', '\\\\').replace(q, '\\' + q) + q)
                        writes[dp] = t; hit = True
            places.append('draft' if hit else 'draft not found' if drafts else 'no draft')
            report.append(f'{pad} {lang}: ' + ', '.join(places))
    if not dry:
        for p, t in writes.items():
            open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('\n'.join(report))
    print(len(report), 'summaries set', '(dry run)' if dry else '')


if __name__ == '__main__':
    main()
