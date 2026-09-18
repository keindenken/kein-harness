#!/bin/sh
orca terminal create --command "codex -s read-only" --name worker
orca terminal wait --for tui-idle --terminal worker
orca terminal send --terminal worker --text "$TASK"
