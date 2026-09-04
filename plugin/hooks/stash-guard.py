#!/usr/bin/env python3
"""Refuse `git stash` from a subagent's Bash call; leave the lead's session alone.

The stash stack is shared by every worktree of a repository, and an executor that ran `git stash push` on an untracked file (nothing captured) and then `git stash pop` unpacked another session's June stash into a live tree. The brief had forbidden git mutations in prose; this is that sentence as a mechanism, scoped to the workers the brief addresses. A subagent's tool events carry `agent_id` and `agent_type`; the lead's do not, and the lead keeps its own rule (`push -u -m <tag>`, `apply <sha>`, never a bare `stash` or a `pop`).

`list` and `show` read; everything else moves the stack and is refused. Exit 2 blocks the call and hands the reason back to the model.
"""
import json
import shlex
import sys

READ_ONLY = {"list", "show"}
OPTIONS_WITH_ARG = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path", "--super-prefix"}


def stash_mutations(command: str):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        tokens = list(lexer)
    except ValueError:
        tokens = command.split()
    found = []
    for index, token in enumerate(tokens):
        if token != "git":
            continue
        cursor = index + 1
        while cursor < len(tokens) and tokens[cursor].startswith("-"):
            skip = 2 if tokens[cursor] in OPTIONS_WITH_ARG else 1
            cursor += skip
        if cursor < len(tokens) and tokens[cursor] == "stash":
            sub = tokens[cursor + 1] if cursor + 1 < len(tokens) else ""
            if sub.startswith("-") or sub not in READ_ONLY:
                found.append(" ".join(tokens[index:cursor + 2]).strip())
    return found


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if not isinstance(payload, dict) or payload.get("tool_name") != "Bash":
        return 0
    if not (payload.get("agent_id") or payload.get("agent_type")):
        return 0
    command = (payload.get("tool_input") or {}).get("command", "")
    if not isinstance(command, str):
        return 0
    hits = stash_mutations(command)
    if not hits:
        return 0
    print(
        "Refused: `git stash` is not available to a worker. The stash stack is shared by every worktree of this repository, and a pop here unpacks another session's work into this tree. "
        "Set a file aside under the scratch directory instead, and leave git state to the lead. Matched: " + "; ".join(hits),
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
