# -*- coding: utf-8 -*-
"""The farm-labels working page's server: static files from the repository
root, plus the POST endpoints the page saves its state to.

    python scratch/map4456/save_server.py              # port 8779
    python scratch/map4456/save_server.py --port 8780  # a test instance

POST /__save/farm_labels  body: [{n, x, y}, ...]  (the working page's whole
label set, in the mosaic's pixels) -> written atomically to
scratch/map4456/farm_labels_latest.json, the file pipeline/maps/import_farms.py
reads. POST /__save/red_labels takes the red readings the same way, to
red_labels_latest.json. Every save replaces the file whole, so the page's
full state is always what is on disk.

Single-writer guard: each file has a version (farm_labels_latest.meta.json).
A save carrying header X-State-Version that does not match the current
version is refused with 409 - a second window of the page (or a stale tab)
must not silently overwrite the newer state; the page says so loudly.
A save with no version header (the tab-close beacon, which cannot carry
headers) is accepted as before.

Out-of-band edits (import_farms.py writing the yml targets, or a manual
restore of the json) are detected by the file being newer than the meta
record; the version bumps so the open windows stop saving stale state.

Every successful save also drops a timestamped snapshot into
scratch/map4456/history/<file>/ (the last 50 are kept): the working state
survives an accidental deletion of the latest file.
GET /__save/version?name=<file> returns the current version, for the
windows to compare against.
Bound to 127.0.0.1 only.
"""
import glob
import json
import os
import shutil
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KEEP = 50
PORT = 8779
STATE_DIR = None
if '--port' in sys.argv:
    PORT = int(sys.argv[sys.argv.index('--port') + 1])
if '--state-dir' in sys.argv:
    # a test instance keeps EVERYTHING it writes - state files, version
    # records, history - under its own directory: the editor's working
    # state must never be touched by a test run (the shared state file
    # once had a battery's 73-label states stomping the editor's 79)
    STATE_DIR = os.path.abspath(
        sys.argv[sys.argv.index('--state-dir') + 1])
    os.makedirs(STATE_DIR, exist_ok=True)
# the editor's server (the default port) keeps the history of the working
# state; a sandboxed or test instance keeps its churn under its own
# history/ directory
HISTORY = (os.path.join(STATE_DIR, 'history') if STATE_DIR is not None
           else os.path.join(HERE, 'history' if PORT == 8779
                             else 'history-test'))


def _target(name):
    return (os.path.join(STATE_DIR, name) if STATE_DIR is not None
            else os.path.join(HERE, name))


TARGET = _target('farm_labels_latest.json')
REDS_TARGET = _target('red_labels_latest.json')


def meta_of(target):
    return target.replace('.json', '.meta.json')


def read_meta(target):
    try:
        with open(meta_of(target), encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {'v': 0}


def current_version(target):
    """The file's version, bumping past out-of-band edits: if the file was
    written by anything but this server since the last save (an import, a
    manual restore), the version moves so open windows stop saving stale
    state over it."""
    m = read_meta(target)
    try:
        fmtime = os.path.getmtime(target)
    except OSError:
        fmtime = 0
    if fmtime > m.get('m', 0):
        m['v'] = m.get('v', 0) + 1
        m['m'] = fmtime
        try:
            with open(meta_of(target), 'w', encoding='utf-8') as f:
                json.dump(m, f)
        except Exception:
            pass
    return m['v']


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def _snapshot(self, target):
        # a timestamped copy of every successful save: the working state
        # survives an accidental deletion, and yesterday's positions can
        # always be dug out
        name = os.path.basename(target).replace('.json', '')
        hdir = os.path.join(HISTORY, name)
        os.makedirs(hdir, exist_ok=True)
        stamp = time.strftime('%Y%m%d-%H%M%S')
        path = os.path.join(hdir, stamp + '.json')
        shutil.copy(target, path)
        old = sorted(glob.glob(os.path.join(hdir, '*.json')))[:-KEEP]
        for p in old:
            os.remove(p)

    def _save_json(self, target, want):
        # want 'int': the farm labels' n is a farm number, unique per label.
        # want 'str': the reds' n is a reading as written - the same row
        # number recurs on every parcel of its farm, so the position is the
        # identity, not the value; a repeated x,y is the only duplicate.
        try:
            length = int(self.headers.get('Content-Length', 0))
            payload = json.loads(self.rfile.read(length))
            # the reds arrive either as a bare list (the old page) or as
            # {marks, deleted} - the deletions are the baked positions of
            # the marks the editor removed, which the import takes out of
            # reds.yml
            dels = []
            if isinstance(payload, dict):
                dels = payload.get('deleted') or []
                payload = payload.get('marks') or []
            clean = []
            seen = set()
            for x in payload:
                key = int(x['n']) if want == 'int' else str(x['n'])
                pos = (int(x['x']), int(x['y']))
                # a farm number may repeat - a farmer can hold several
                # farmsteads, each with its own label - so the (n, x, y)
                # triple is the identity. An exact triple twice is a
                # double-click, not a second farmstead: collapse it
                # silently (a 400 here once bricked every save of a tab
                # that held stacked duplicates, banner re-appearing on
                # every retry)
                trip = (key, pos[0], pos[1])
                if trip in seen:
                    continue
                seen.add(trip)
                entry = {'n': key, 'x': pos[0], 'y': pos[1]}
                if want == 'str':
                    # a moved red keeps the position it was baked at
                    # (ox,oy) beside its new one; a hand-added red keeps
                    # its (negative) id until the import turns it into a
                    # real mark
                    if x.get('ox') is not None:
                        entry['ox'] = int(x['ox'])
                    if x.get('oy') is not None:
                        entry['oy'] = int(x['oy'])
                    if x.get('id') is not None:
                        entry['id'] = int(x['id'])
                clean.append(entry)
            dl = []
            dseen = set()
            for x in dels:
                k = (int(x['x']), int(x['y']))
                if k in dseen:
                    continue
                dseen.add(k)
                dl.append({'x': k[0], 'y': k[1]})
        except Exception as e:
            self.send_error(400, 'bad payload: %s' % e)
            return
        # the single-writer guard: a window holding an older version than
        # the file's must not overwrite what it has not seen
        v = current_version(target)
        sent = self.headers.get('X-State-Version')
        if sent is not None:
            try:
                sent = int(sent)
            except ValueError:
                sent = None
            if sent is not None and sent != v:
                data = json.dumps(
                    {'error': 'changed elsewhere', 'v': v}).encode('utf-8')
                self.send_response(409)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
        tmp = target + '.tmp'
        with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
            if want == 'str':
                # the reds' file carries the marks and the deletion ledger
                json.dump({'marks': clean, 'deleted': dl}, f,
                          ensure_ascii=False, indent=1)
            else:
                json.dump(clean, f, ensure_ascii=False, indent=1)
        os.replace(tmp, target)
        nv = v + 1
        try:
            with open(meta_of(target), 'w', encoding='utf-8') as f:
                json.dump({'v': nv, 'm': os.path.getmtime(target)}, f)
        except Exception:
            pass
        try:
            self._snapshot(target)
        except Exception:
            pass  # a failed snapshot must not fail the save itself
        data = json.dumps({'saved': len(clean), 'deleted': len(dl),
                           'v': nv}).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split('?')[0].rstrip('/')
        if path == '/__save/version':
            name = self.path.split('name=')[-1].split('&')[0]
            target = (REDS_TARGET if 'red' in name else TARGET)
            data = json.dumps({'v': current_version(target)}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data)))
            # the version is asked to decide a save: a cached answer would
            # teach a window a version the file has long outgrown (the
            # browser heuristically caches a Last-Modified response - a
            # battery run once failed on exactly that)
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)
            return
        if path == '/__save/state':
            # the working state the page restores from: THIS server's own
            # file, whatever directory it keeps - a test instance serves
            # its sandbox and the editor's server serves the working file
            name = self.path.split('name=')[-1].split('&')[0]
            target = (REDS_TARGET if 'red' in name else TARGET)
            try:
                with open(target, 'rb') as f:
                    body = f.read()
                lm = self.date_time_string(os.path.getmtime(target))
            except OSError:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Last-Modified', lm)
            # no-store: the state the page restores from must be read
            # again at every load - a heuristically cached answer (the
            # browser reuses a Last-Modified response for a tenth of the
            # file's age) once served the pre-save state after a save,
            # and a test window then restored what it had just erased
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        path = self.path.split('?')[0].rstrip('/')
        if path == '/__save/farm_labels':
            self._save_json(TARGET, 'int')
            return
        if path == '/__save/red_labels':
            self._save_json(REDS_TARGET, 'str')
            return
        self.send_error(404)

    def log_message(self, *a):
        pass


if __name__ == '__main__':
    print('serving %s at http://127.0.0.1:%d '
          '(POST /__save/farm_labels -> %s)' % (ROOT, PORT, TARGET))
    ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
