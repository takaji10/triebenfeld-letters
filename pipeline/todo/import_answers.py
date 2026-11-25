# -*- coding: utf-8 -*-
"""Apply the editor's exported answers from the to-do page ("Apply my to-do answers").

    python pipeline/todo/import_answers.py todo_answers_<date>.json           # check: list, change nothing
    python pipeline/todo/import_answers.py todo_answers_<date>.json --write   # record them

A final answer (an option, "Something else" with its text, Done, Not needed / Drop it, Go ahead, Now)
moves the item from `items:` to `done:` in reference/todo.yml with the answer and the note, and the
page data and docs/TODO.md are rebuilt. "Later" and "Can't tell", and a note with no answer, keep the
item open and put the editor's words on it (`editor_note`). Ids no longer in the list are refused
(the item was changed or removed since), and an answer given to an item whose text has since changed
is listed for a second look, not applied.

The answer to a question is only recorded here. Claude then writes it where it belongs (the holding's
rulings.yml or notes.md, NEEDS_CONFIRMATION, the changelog), as for any ruling from the editor.
"""
import os, sys, json, datetime, hashlib
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'reference', 'todo.yml')
LABEL = {'__done__': 'Done', '__drop__': 'Not needed', '__go__': 'Go ahead', '__now__': 'Now',
         '__later__': 'Later', '__unsure__': "Can't tell"}
FINAL = {'__done__', '__drop__', '__go__', '__now__', '__other__'}


def card_hash(it):
    return hashlib.sha1((it['text'] + '|'.join(it.get('options') or [])).encode('utf-8')).hexdigest()[:8]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    write = '--write' in sys.argv
    data = json.load(open(sys.argv[1], encoding='utf-8'))
    answers = data.get('answers') or {}
    raw = open(SRC, encoding='utf-8').read()
    hdr = raw.split('items:')[0]
    src = yaml.safe_load(raw)
    by_id = {it['id']: it for it in src['items']}
    today = datetime.date.today().isoformat()
    closed, kept, refused, changed = [], [], [], []
    for i, a in answers.items():
        it = by_id.get(i)
        if not it:
            refused.append((i, a.get('title', '?'))); continue
        if a.get('h') and a['h'] != card_hash(it):
            changed.append((i, it['title'])); continue
        v = a.get('v') or ''
        text = (a.get('other') or '').strip() if v == '__other__' else LABEL.get(v, v)
        note = (a.get('note') or '').strip()
        if v in FINAL or (v and v not in LABEL):
            closed.append((it, text or '(no text)', note))
        elif v or note:
            kept.append((it, text, note))
    print(f'{len(answers)} answers in the file: {len(closed)} final, {len(kept)} left open with a note, '
          f'{len(refused)} refused (id gone), {len(changed)} for a second look (the item changed).\n')
    for it, text, note in closed:
        print(f'FINAL  {it["id"]} [{it["kind"]}] {it["title"]}\n       answer: {text}' + (f'\n       note: {note}' if note else ''))
    for it, text, note in kept:
        print(f'OPEN   {it["id"]} {it["title"]}: {text}' + (f' / {note}' if note else ''))
    for i, t in refused:
        print(f'REFUSED {i}: {t}')
    for i, t in changed:
        print(f'CHANGED {i}: {t}')
    if not write:
        print('\n(check only; add --write to record)'); return
    done = src.get('done') or []
    gone = {it['id'] for it, _, _ in closed}
    for it, text, note in closed:
        done.append({'id': it['id'], 'title': it['title'], 'date': today, 'answer': text, 'note': note})
    for it, text, note in kept:
        it['editor_note'] = ' / '.join(x for x in (text, note) if x)
    src['items'] = [it for it in src['items'] if it['id'] not in gone]
    src['done'] = done
    open(SRC, 'w', encoding='utf-8', newline='\n').write(
        hdr + yaml.safe_dump({'items': src['items'], 'done': done}, allow_unicode=True, sort_keys=False, width=100))
    os.system(f'"{sys.executable}" "{os.path.join(ROOT, "pipeline", "todo", "build_todo.py")}"')


if __name__ == '__main__':
    main()
