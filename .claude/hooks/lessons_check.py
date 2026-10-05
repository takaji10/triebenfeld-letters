# -*- coding: utf-8 -*-
"""The check behind the rule on lessons (CLAUDE.md, "Lessons go into the repository").

Run by Claude Code itself, through .claude/settings.json, in desktop and cloud
sessions alike:

    SessionStart  ->  lessons_check.py start    notes where the session began
    Stop          ->  lessons_check.py          each time Claude is about to stop

The rule: work that is committed ends with the question whether it taught
anything a later session will need, and the answer is written down. Either
docs/WORKING_NOTES.md (or another document) gains the lesson in those commits,
or the report to the editor ends with a line that begins "Lessons:".

What this script does when Claude is about to stop: if commits were made in
this session since it last looked, and none of them changed
docs/WORKING_NOTES.md, and the closing message has no "Lessons:" line, it stops
Claude from finishing once and tells it to answer the question. It asks once
for each batch of commits, never twice, and it never blocks on a failure of its
own: any error here lets Claude stop as usual.

It cannot know whether a lesson was learned. It makes sure the question is
asked and answered where the editor can see the answer.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time

NOTES = 'docs/WORKING_NOTES.md'
ASK = (
    "Project rule (CLAUDE.md, \"Lessons go into the repository\"): work was committed in this "
    "session and docs/WORKING_NOTES.md was not changed by it. Before stopping, ask whether this "
    "work taught anything a later session will need: a correction or ruling from the editor, a "
    "mistake made, a trap in a tool, a method that worked. If it did, write it into "
    "docs/WORKING_NOTES.md (or the document it belongs to: EDITORIAL_RULES, HOUSE_STYLE, NEW_UNIT, "
    "the holding's notes.md) and commit it; a desktop session saves it to memory as well. Then "
    "end your reply to the editor with one line beginning \"Lessons:\" that says what was written "
    "down, or \"Lessons: none.\" Do not push for this alone unless the editor has asked for the "
    "work to be published."
)


def git(root, *args):
    r = subprocess.run(['git', '-C', root] + list(args), capture_output=True, text=True,
                       encoding='utf-8', errors='replace', timeout=20)
    return r.stdout.strip() if r.returncode == 0 else ''


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    root = os.environ.get('CLAUDE_PROJECT_DIR') or data.get('cwd') or os.getcwd()
    session = re.sub(r'[^A-Za-z0-9_-]', '', str(data.get('session_id') or 'nosession'))
    where = data.get('scratchpad_dir')
    if not (where and os.path.isdir(where)):
        where = tempfile.gettempdir()
    state_path = os.path.join(where, 'lessons_check_%s.json' % session)
    try:
        state = json.load(open(state_path, encoding='utf-8'))
    except Exception:
        state = None
    head = git(root, 'rev-parse', 'HEAD')
    if not head:
        return 0

    def save(asked):
        st = {'began': (state or {}).get('began', time.time()), 'asked': asked}
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(st, f)

    if 'start' in sys.argv[1:] or state is None:
        # Where the session began. Commits older than this are someone else's.
        if state is None:
            save(head)
        return 0
    if data.get('stop_hook_active') or head == state.get('asked'):
        return 0
    asked = state.get('asked') or head
    # Only commits made since the session began count: a pull brings in older ones.
    times = git(root, 'log', '--format=%ct', '%s..%s' % (asked, head)).split()
    mine = [t for t in times if t.isdigit() and int(t) >= int(state.get('began', 0)) - 60]
    save(head)
    if not mine:
        return 0
    changed = git(root, 'diff', '--name-only', asked, head).splitlines()
    if NOTES in [c.strip() for c in changed]:
        return 0
    last = str(data.get('last_assistant_message') or '')
    if re.search(r'(?mi)^\W*Lessons\s*:', last):
        return 0
    print(json.dumps({'decision': 'block', 'reason': ASK}))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
