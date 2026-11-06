# The HTML rendering of the review reports (the yml/txt files stay: they
# diff well in git; the pages are for reading and deciding).
#
#   Written by build.py alongside the other reports, into
#   review/genealogy/: index.html, excluded.html, privacy.html,
#   build_report.html. Same palette and habits as the project's other
#   review sheets (scan_review.html): the paper colours, a filter box per
#   table, pill badges, no external assets.

from __future__ import annotations

import html
from collections import Counter
from datetime import date


_CSS = """
:root{--ink:#1c1a17;--soft:#55504a;--faint:#857e75;--paper:#fbf9f5;--paper2:#f2eee6;
--rule:#ded7ca;--accent:#7a3b2e;--ok:#3f6b42;--warn:#8a4b1a;
--serif:Iowan Old Style,Palatino Linotype,Georgia,serif;
--sans:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:15px}
header{position:sticky;top:0;z-index:5;background:var(--paper2);border-bottom:1px solid var(--rule);
padding:.7rem 1rem;display:flex;flex-wrap:wrap;gap:.6rem 1.2rem;align-items:center}
h1{font-size:1rem;margin:0 1rem 0 0;font-family:var(--serif)}
nav a{font-size:.82rem;color:var(--accent);text-decoration:none;margin-right:.9rem}
nav a:hover{text-decoration:underline}
.stat{font-size:.8rem;color:var(--faint)}
.stat b{color:var(--ink)}
main{max-width:60rem;margin:0 auto;padding:1.2rem 1rem 3rem}
h2{font-family:var(--serif);font-size:1.05rem;margin:1.6rem 0 .4rem}
p.lead{color:var(--soft);font-size:.9rem;max-width:46rem}
input[type=search]{font:inherit;font-size:.85rem;padding:.35rem .6rem;border:1px solid var(--rule);
border-radius:3px;background:#fff;min-width:16rem}
table{border-collapse:collapse;width:100%;font-size:.85rem}
td,th{border-bottom:1px solid var(--rule);padding:.35rem .55rem;text-align:left;vertical-align:top}
th{font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--faint);font-weight:600}
tr:hover td{background:#f6f1e8}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.xref{color:var(--faint);font-size:.78rem;white-space:nowrap}
.pill{border:1px solid var(--rule);border-radius:999px;padding:.05rem .5rem;font-size:.72rem;
white-space:nowrap;display:inline-block}
.pill.warn{color:var(--warn);border-color:var(--warn)}
.pill.ok{color:var(--ok);border-color:var(--ok)}
.pill.acc{color:#fff;background:var(--accent);border-color:var(--accent)}
.pill.dim{color:var(--faint)}
.counts{display:flex;flex-wrap:wrap;gap:.5rem;margin:.6rem 0 1rem}
.count{border:1px solid var(--rule);border-radius:4px;background:#fff;padding:.5rem .8rem;min-width:9rem}
.count b{display:block;font-size:1.25rem;font-family:var(--serif)}
.count span{font-size:.72rem;color:var(--faint)}
.count.flag{border-color:var(--warn)}
.count.flag b{color:var(--warn)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(16rem,1fr));gap:1rem;margin-top:1rem}
.card{border:1px solid var(--rule);border-radius:4px;background:#fff;padding:1rem;display:block;
color:inherit;text-decoration:none}
.card:hover{border-color:var(--accent)}
.card h3{font-family:var(--serif);margin:.1rem 0 .3rem;font-size:1rem}
.card p{margin:0;font-size:.82rem;color:var(--soft)}
.card .big{font-size:1.6rem;font-family:var(--serif)}
pre{font-family:var(--serif);font-size:.88rem;white-space:pre-wrap;background:#fff;
border:1px solid var(--rule);padding:.8rem;border-radius:3px}
footer{max-width:60rem;margin:0 auto;padding:0 1rem 2rem;font-size:.75rem;color:var(--faint)}
"""


def _page(title: str, stats: str, body: str, active: str) -> str:
    def nav(href, label, key):
        cls = f' style="font-weight:700"' if key == active else ""
        return f'<a href="{href}"{cls}>{label}</a>'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} &middot; Triebenfeld genealogy</title>
<style>{_CSS}</style></head>
<body>
<header><h1>Genealogy build review</h1>
<nav>{nav("index.html", "Overview", "index")}{nav("excluded.html", "Excluded branch", "excluded")}{nav("privacy.html", "Living people", "privacy")}{nav("build_report.html", "Build report", "report")}</nav>
<span class="stat">{stats}</span></header>
<main>
{body}
</main>
<footer>Generated {date.today().isoformat()} by pipeline/genealogy/build.py. The yml and txt
reports beside this page are the diffable copies; nothing here is published.</footer>
</body></html>"""


def _esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def _table(id_: str, headers: list, rows: list, note: str = "") -> str:
    head = "".join(f"<th>{_esc(h)}</th>" for h in headers)
    filter_row = (f'<p><input type="search" placeholder="filter &hellip;" '
                  f'oninput="filterTable(\'{id_}\', this.value)"> '
                  f'<span class="stat">{note}</span></p>' if note != "nofilter" else "")
    body_rows = "".join(r for r in rows)
    script = ""
    if note != "nofilter":
        script = (f"<script>function filterTable(id,q){{q=q.toLowerCase();"
                  f"document.querySelectorAll('#'+id+' tbody tr').forEach("
                  f"tr=>{{tr.style.display=tr.textContent.toLowerCase()"
                  f".includes(q)?'':'none'}})}}</script>")
    return (f'{filter_row}<table id="{id_}"><thead><tr>{head}</tr></thead>'
            f"<tbody>{body_rows}</tbody></table>{script}")


# ---------------------------------------------------------------------------
# index.html

def write_index(directory, counts: dict, problems: int, bad_dates: int) -> None:
    flag = ' <span class="pill warn">review</span>' if problems or bad_dates else ""
    body = f"""
<p class="lead">The three reports from this build of the genealogy database.
Read them before pushing anything: the exclusion page is the editor's
sign-off on the cut, the privacy page lists everyone redacted and why, and
the build report carries the counts and anything the checks flagged{flag}.</p>
<div class="cards">
<a class="card" href="excluded.html"><span class="big">{counts['people']}</span>
<h3>Excluded branch</h3><p>{counts['people']} people, {counts['media']} media files,
{counts['families']} families removed with Larry Charles Lacko's ancestors.</p></a>
<a class="card" href="privacy.html"><span class="big">{counts['living']}</span>
<h3>Living people</h3><p>{counts['living']} redacted, {counts['withheld']} media files
withheld. Grouped by the rule that decided each one.</p></a>
<a class="card" href="build_report.html"><span class="big">{problems or "&check;"}</span>
<h3>Build report</h3><p>{problems} consistency problems, {bad_dates} unparsed dates,
the full counts of the build.</p></a>
</div>"""
    (directory / "index.html").write_text(_page(
        "Overview", f"built {date.today().isoformat()}", body, "index"),
        encoding="utf-8")


# ---------------------------------------------------------------------------
# excluded.html


def write_excluded(directory, ex, model) -> None:
    rows = []
    for row in ex.report_rows:
        x = row["xref"]
        p = model.people.get(x)
        note = ""
        if p and p.famc:
            note = "parents cut; link cleared" if not p.famc else ""
        rows.append(
            f"<tr><td class='xref'>{_esc(x.strip('@'))}</td>"
            f"<td>{_esc(row['name'])}</td><td></td></tr>")
    people_table = _table("tpeople", ["Gramps id", "Name", ""], rows,
                          f"{len(rows)} people")

    # media grouped by top folder for a quicker read
    by_folder: dict = {}
    for path in sorted(ex.removed_media):
        parts = path.split("/")
        folder = " / ".join(parts[2:4]) if len(parts) > 3 else parts[0]
        by_folder.setdefault(folder, []).append("/".join(parts[2:]))
    media_rows = []
    for folder in sorted(by_folder):
        files = by_folder[folder]
        media_rows.append(
            f"<tr><td>{_esc(folder)}</td><td class='num'>{len(files)}</td>"
            f"<td>{'<br>'.join(_esc(f) for f in files)}</td></tr>")
    media_table = _table("tmedia", ["Folder", "Files", "Names"], media_rows,
                         f"{len(ex.removed_media)} files")

    fam_rows = [f"<tr><td class='xref'>{_esc(f.strip('@'))}</td></tr>"
                for f in sorted(ex.removed_families)]
    fam_table = _table("tfam", ["Family"], fam_rows, "nofilter")

    sanitised = "".join(f"<li>{_esc(s)}</li>" for s in ex.sanitized) or \
        "<li>none</li>"
    cut = "".join(f"<li><span class='xref'>{_esc(c['person'].strip('@'))}</span> "
                  f"lost the link to family "
                  f"<span class='xref'>{_esc(c['family'].strip('@'))}</span> "
                  f"(the parents left)</li>" for c in ex.cut_links) or "<li>none</li>"

    body = f"""
<p class="lead">Everyone removed under the exclusion ruling
(<code>config.yml</code>: root I0005, Larry Charles Lacko). The cut takes his
parents, their blood ancestors, his siblings through either parent, and
everyone attached only through them. Larry, his family and the Zelmer side
stay. Confirm each row before publishing; a correction is a config change,
not an edit here.</p>
<h2>People <span class="pill acc">{len(rows)}</span></h2>
{people_table}
<h2>Media <span class="pill acc">{len(ex.removed_media)}</span></h2>
{media_table}
<h2>Families <span class="pill acc">{len(ex.removed_families)}</span></h2>
{fam_table}
<h2>Cut links</h2><ul>{cut}</ul>
<h2>Sanitised references</h2>
<p class="lead">Kept records that pointed into the removed set; the link was
cleared so no page can dangle.</p><ul>{sanitised}</ul>"""
    (directory / "excluded.html").write_text(_page(
        "Excluded branch",
        f"<b>{len(rows)}</b> people &middot; <b>{len(ex.removed_media)}</b> media",
        body, "excluded"), encoding="utf-8")


# ---------------------------------------------------------------------------
# privacy.html


def write_privacy(directory, model, living, reasons, counts, withheld) -> None:
    grouped: dict = {}
    for x in living:
        grouped.setdefault(reasons.get(x, "undecided"), []).append(x)
    order = sorted(grouped, key=lambda k: -len(grouped[k]))
    blocks = []
    for reason in order:
        xs = grouped[reason]
        rows = "".join(
            f"<tr><td class='xref'>{_esc(x.strip('@'))}</td>"
            f"<td>{_esc(model.people[x].name.surname)}</td>"
            f"<td>{_esc(model.people[x].sex or '?')}</td></tr>"
            for x in sorted(xs))
        blocks.append(
            f"<h2>{_esc(reason[0].upper() + reason[1:])} "
            f"<span class='pill acc'>{len(xs)}</span></h2>"
            + _table(f"t{abs(hash(reason)) % 10**8}", ["Gramps id", "Surname", "Sex"],
                     rows, f"{len(xs)} people"))

    media_rows = "".join(f"<tr><td>{_esc(p)}</td></tr>" for p in sorted(withheld))
    media_table = _table("tmedia", ["Withheld media (living people)"], media_rows,
                         f"{len(withheld)} files")

    body = f"""
<p class="lead">Everyone the build treats as living and therefore redacted:
their events, dates, places, notes, citations and media never reach the
site; the tree keeps the node as &ldquo;Living {'' }Surname&rdquo; so the
structure reads. The rule that decided each person is grouped below &mdash;
check the groups against Gramps' own privacy filter. Undated people inherit
the closest verdict among parents, spouses and children; anything still
open is redacted to be safe.</p>
{''.join(blocks)}
<h2>Media withheld <span class="pill acc">{len(withheld)}</span></h2>
{media_table}"""
    stats = (f"<b>{len(living)}</b> living &middot; "
             f"<b>{len(withheld)}</b> media withheld")
    (directory / "privacy.html").write_text(_page(
        "Living people", stats, body, "privacy"), encoding="utf-8")


# ---------------------------------------------------------------------------
# build_report.html


def write_build_report(directory, model, ex, living, counts, withheld,
                       unmatched, info, ged_path, checks, meta_counts) -> None:
    rows = [
        (len(model.people), "people kept", False),
        (len(ex.removed_people), "people excluded", False),
        (len(living), "living people (redacted)", False),
        (len(model.families) - len(ex.removed_families), "families kept", False),
        (meta_counts["media"], "media publishable", False),
        (len(ex.removed_media), "media excluded (branch)", False),
        (len(withheld), "media withheld (living)", False),
        (len(model.sources), "sources", False),
        (len(model.repos), "repositories", False),
        (info["stats"]["regions"], "focus regions joined", False),
        (unmatched, "media without a data.gramps match", unmatched > 0),
        (len(checks.get("bad_dates", [])), "dates that failed to parse",
         bool(checks.get("bad_dates"))),
        (len(checks.get("problems", [])), "consistency problems",
         bool(checks.get("problems"))),
    ]
    count_rows = "".join(
        f"<div class='count{' flag' if flag else ''}'><b>{n}</b>"
        f"<span>{_esc(label)}</span></div>"
        for n, label, flag in rows)

    bd = checks.get("bad_dates", [])
    bd_rows = []
    for d in bd:
        person, _, rest = d.partition("/")
        tag, _, raw = rest.partition(": ")
        bd_rows.append(
            f"<tr><td class='xref'>{_esc(person.strip('@'))}</td>"
            f"<td>{_esc(tag.strip())}</td>"
            f"<td><code>{_esc(raw or rest)}</code></td></tr>")
    bd_table = _table("tbd", ["Person", "Event", "Raw text"], bd_rows,
                      "the raw text is kept; only the sort key is missing") \
        if bd_rows else "<p class='lead'>none</p>"

    probs = checks.get("problems", [])
    prob_rows = "".join(
        f"<tr><td class='xref'>{_esc(p.split(':')[0].strip('@'))}</td>"
        f"<td>{_esc(p.split(':', 1)[1].strip() if ':' in p else p)}</td>"
        f"</tr>" for p in probs)
    prob_table = _table("tprob", ["Person", "Finding"], prob_rows,
                        "the editor's call: trim, keep, or leave") \
        if prob_rows else "<p class='lead'>none</p>"

    body = f"""
<p class="lead">Input {_esc(str(ged_path))}; database header
{_esc(model.header.get('SOUR', ''))} {_esc(model.header.get('DATE', ''))}.</p>
<div class="counts">{count_rows}</div>
<h2>Unparsed dates</h2>
{bd_table}
<h2>Consistency problems</h2>
{prob_table}
<h2>Checks run</h2>
<ul class="lead">
<li>every kept family link points at a kept person and family</li>
<li>every citation resolves to a real source</li>
<li>no excluded person's full name appears in a kept person's notes
(<code>[Living]</code> placeholders are skipped: removed and kept people
share them)</li>
<li>every media object resolves to a gpkg file (the count above)</li>
</ul>"""
    (directory / "build_report.html").write_text(_page(
        "Build report", f"built {date.today().isoformat()}", body, "report"),
        encoding="utf-8")
