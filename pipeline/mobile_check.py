"""The mobile-readiness check of the built site (2026-11-07).

    python pipeline/mobile_check.py --map <key> [...]
    python pipeline/mobile_check.py --pages /maps/lukom1766/,/de/karten/lukom1766/
    python pipeline/mobile_check.py --pages pages.txt
    python pipeline/mobile_check.py --all [--widths 390,360,320]

Measures every given page of the BUILT site (site/_site — run Jekyll first)
at phone widths in the machine's Edge (headless, puppeteer-core) and reports
horizontal overflow with the elements outside every clipping container that
extend it. Exits 1 on any overflow, 2 if the tooling is missing. Crawler
races are retried inside crawl.js; a page still unmeasured after that is
reported and listed but does not fail the run by itself — investigate it.

The map procedure (docs/ADDING_A_MAP.md, step 8) runs `--map <key>` after a
new map's pages are built: a map page that overflows on a phone is a build
defect, fixed and re-run before the map counts as in.

Requires node on PATH (puppeteer-core is installed into a persistent cache
under the system temp, never into the repository).
"""
import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site", "_site")
CRAWL_JS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "mobile_check", "crawl.js")
WORK = os.path.join(tempfile.gettempdir(), "opencode", "mobilecheck")
EDGE_PATHS = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]
EXCLUDE_DIRS = {"assets", "corpus", "feeds", "site_libs"}
EXCLUDE_SUBSTR = ("genealog",)   # the genealogy section (the editor's exception)


def die(msg, code=2):
    print("STOP: " + msg)
    sys.exit(code)


def enumerate_map(key):
    out = []
    for rel in (f"maps/{key}/index.html", f"de/karten/{key}/index.html"):
        if os.path.isfile(os.path.join(SITE, rel.replace("/", os.sep))):
            out.append("/" + rel[:-len("index.html")])
    if not out:
        die(f"no built pages for map {key!r} - build the site first "
            f"(map_pages.py, then Jekyll)")
    return out


def enumerate_all():
    out = []
    for dirpath, dirnames, filenames in os.walk(SITE):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        if "index.html" in filenames:
            rel = os.path.relpath(dirpath, SITE).replace(os.sep, "/")
            page = "/" if rel == "." else "/" + rel + "/"
            if not any(s in page for s in EXCLUDE_SUBSTR):
                out.append(page)
    return sorted(out)


def prepare_workdir():
    os.makedirs(WORK, exist_ok=True)
    # the crawler runs from WORK so require('puppeteer-core') resolves
    shutil.copy(CRAWL_JS, os.path.join(WORK, "crawl.js"))
    if not os.path.isfile(os.path.join(WORK, "node_modules",
                                       "puppeteer-core",
                                       "package.json")):
        if not shutil.which("node") or not shutil.which("npm"):
            die("node/npm not on PATH - the mobile check needs them "
                "(node >= 18)", 2)
        if not os.path.isfile(os.path.join(WORK, "package.json")):
            with open(os.path.join(WORK, "package.json"), "w",
                      encoding="utf-8", newline="\n") as f:
                json.dump({"name": "triebenfeld-mobilecheck",
                           "private": True}, f)
        r = subprocess.run(["npm", "install", "puppeteer-core",
                            "--no-audit", "--no-fund", "--silent"],
                           cwd=WORK, capture_output=True, text=True)
        if r.returncode:
            die("npm install puppeteer-core failed:\n" + (r.stderr or "")[-400:])


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):   # the request logs are noise
        pass


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--map", help="check one map's pages (en + de)")
    g.add_argument("--pages", help="comma-separated URL paths, or a file of them")
    g.add_argument("--all", action="store_true",
                   help="every built page (the genealogy section excluded)")
    ap.add_argument("--widths", default="390,360,320")
    ap.add_argument("--conc", type=int, default=6)
    a = ap.parse_args()

    if not os.path.isdir(SITE):
        die("no site/_site - build the site first (Jekyll)")
    if not any(os.path.isfile(p) for p in EDGE_PATHS):
        die("no msedge.exe found", 2)
    prepare_workdir()

    if a.map:
        pages = enumerate_map(a.map)
    elif a.all:
        pages = enumerate_all()
    else:
        if os.path.isfile(a.pages):
            with open(a.pages, encoding="utf-8") as f:
                pages = [s.strip() for s in f if s.strip()]
        else:
            pages = [s.strip() for s in a.pages.split(",") if s.strip()]

    server = ThreadingHTTPServer(("127.0.0.1", 0),
                                 partial(QuietHandler, directory=SITE))
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        pages_file = os.path.join(WORK, "pages_current.txt")
        with open(pages_file, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(pages))
        report = os.path.join(WORK, "report_current.json")
        r = subprocess.run(
            ["node", "crawl.js", "--base", f"http://127.0.0.1:{port}",
             "--pages", pages_file, "--out", report,
             "--widths", a.widths, "--conc", str(a.conc)],
            cwd=WORK, capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip())
        if r.returncode:
            die(f"the crawler failed (exit {r.returncode})")
        with open(report, encoding="utf-8") as f:
            res = json.load(f)
    finally:
        server.shutdown()

    for p in res["problems"]:
        print(f"\nOVERFLOW {p['page']} @{p['width']}: "
              f"{p['overflow']} px past the viewport")
        for o in p["offenders"]:
            print(f"  {o['sel']}  right {o['right']} w {o['width']}"
                  f"  \"{o['text']}\"")
    for u in res["unmeasured"]:
        print(f"\nUNMEASURED {u['page']} @{u['width']}: {u['error']}")

    if res["problems"]:
        print(f"\nFAILED - {len(res['problems'])} overflow(s)")
        sys.exit(1)
    print("\nALL PAGES FIT - no horizontal overflow at "
          + ", ".join(str(w) for w in
                      (int(x) for x in a.widths.split(","))))


main()
