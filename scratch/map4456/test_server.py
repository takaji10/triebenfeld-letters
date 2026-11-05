# -*- coding: utf-8 -*-
"""A private save-server instance for the tests, on port 8780.

The editor's own server runs on 8779; the tests must never touch it - a
test that killed the shared server once left the editor saving into the
void. Every test suite starts its own instance here and stops it after.
"""
import os
import subprocess
import sys
import time

import requests

PORT = 8780
URL = 'http://127.0.0.1:%d/scratch/map4456/farm_labels.html' % PORT
# the sandbox: everything the test server writes - state files, version
# records, history - lives here, and the editor's working state on 8779
# is never touched by a test run (the shared state file once had a
# battery's 73-label states stomping the editor's 79)
STATE = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test-state'))
FARMS_STATE = os.path.join(STATE, 'farm_labels_latest.json')
REDS_STATE = os.path.join(STATE, 'red_labels_latest.json')
_proc = [None]


def _port_serving():
    try:
        requests.get('http://127.0.0.1:%d/__save/version?name=x' % PORT,
                     timeout=1)
        return True
    except Exception:
        return False


def start():
    if _port_serving():
        # already up - adopt it (a leftover from a crashed earlier run is
        # the same server pointed at the same files; two binds on one port
        # once split the requests and broke the server-down scene)
        _proc[0] = None
        return
    _proc[0] = subprocess.Popen(
        [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      'save_server.py'), '--port', str(PORT),
         '--state-dir', STATE],
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    for _ in range(40):
        try:
            requests.get(URL, timeout=1)
            return
        except Exception:
            time.sleep(0.25)
    stop()
    raise RuntimeError('the test server on %d did not come up' % PORT)


def stop():
    # by port, so an adopted stray is cleaned up as well - the editor's
    # own server on 8779 is a different port and is never touched
    _proc[0] = None
    subprocess.run(['powershell', '-Command',
                    '$c = Get-NetTCPConnection -LocalPort %d -State Listen '
                    '-ErrorAction SilentlyContinue; '
                    'if ($c) { $c | Select-Object -Unique OwningProcess | '
                    'ForEach-Object { Stop-Process -Id $_.OwningProcess '
                    '-Force } }' % PORT],
                   capture_output=True)


def kill():   # for the server-down test: kill EVERY listener on the port
    stop()
    time.sleep(0.5)
    if _port_serving():
        raise RuntimeError('port %d is still serving after the kill' % PORT)
