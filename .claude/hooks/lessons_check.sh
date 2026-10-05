#!/bin/sh
# Finds a Python that runs (the desktop has "python", the cloud "python3") and
# hands lessons_check.py the hook's input. If there is none, Claude stops as usual.
here=$(dirname "$0")
for py in python3 python; do
    if "$py" -c "" </dev/null >/dev/null 2>&1; then
        exec "$py" "$here/lessons_check.py" "$@"
    fi
done
exit 0
