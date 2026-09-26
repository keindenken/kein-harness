#!/usr/bin/env python3
"""Refuse a subagent's attempt to start a worker of its own; leave the lead's session alone.

The lead holds the map of which worker owns which file, and a worker's own writer, reviewer or fan-out is invisible on it. A subagent has the spawn tool with no depth guard, and one has been seen invoking `/kein:execute` on its own task and putting its own work through review. A read-only lookup stays open, because a worker that must find something should not have to report back to ask.

Scope is `agent_id`, which a subagent's tool events carry and the lead's do not (measured for Agent and Skill calls on 2.1.283). `agent_type` is not enough: a main session started with `--agent` carries it too, and would lose all dispatch. What is refused:

- `Agent` or `Task` for any type but a lookup role. An omitted `subagent_type` is general-purpose, which writes.
- `Skill` for the kein skills that dispatch workers, spelled with or without the plugin prefix, since the hook sees the literal the model wrote. Other skills pass: a role such as `designer` loads skills as reference, which is why `disallowedTools: Skill` in role frontmatter was never an option.
- `Workflow`, which fans out by definition.
- `ocs team` and `ocs ask` in a Bash command, including inside `sh -c` and `eval`, which start another vendor's worker.

Not covered: `SendMessage` to a worker that already exists, which is also how siblings coordinate, and whatever a worker on another vendor does, since no Claude hook runs there.

Exit 2 blocks the call and hands the reason to the model that made it.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import sys

LOOKUP_TYPES = {"Explore", "kein:explore", "kein:document-specialist", "claude-code-guide"}
DISPATCHING_SKILLS = {"execute", "ralplan", "plan", "fsd", "research"}


SHELLS = {"sh", "bash", "zsh", "dash", "eval"}
# Not a here-string `<<<`, not a shift such as `$((1<<2))`: taking either for a heredoc would drop every later line from the scan.
HEREDOC = re.compile(r"(?<![<\d$(])<<-?(?!<)\s*(['\"]?)(\w+)\1")


def _without_heredoc_bodies(command: str) -> str:
    kept, terminator = [], None
    for line in command.split("\n"):
        if terminator is not None:
            if line.strip() == terminator:
                terminator = None
            continue
        kept.append(line)
        for match in HEREDOC.finditer(line):
            before = line[:match.start()]
            # Inside an open quote, `<<EOF` is text, not a heredoc.
            if before.count('"') % 2 == 0 and before.count("'") % 2 == 0:
                terminator = match.group(2)
                break
    return "\n".join(kept)


def _tokens(command: str) -> list[str]:
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:
        return command.split()


def _ocs_dispatches(command: str, depth: int = 0) -> list[str]:
    # Any position counts, not only a command's first word: `for ... do`, `timeout 600`, `xargs -n1` and the rest of shell grammar all put `ocs` somewhere else, and a false refusal costs a worker one reworded call where a missed one costs the rule. A quoted string stays one token and a heredoc body is dropped, so prose that names the command mostly passes.
    tokens = _tokens(_without_heredoc_bodies(command))
    hits = []
    for i, token in enumerate(tokens):
        name = os.path.basename(token)
        if name in ("ocs-team", "ocs-ask"):
            hits.append(name.replace("-", " "))
        elif name == "ocs" and i + 1 < len(tokens) and tokens[i + 1] in ("team", "ask"):
            hits.append(f"ocs {tokens[i + 1]}")
        elif depth < 2 and name in SHELLS:
            # The command string of `eval`, or of `sh -c` found by a short-option cluster so `--norc` is not taken for it, is a command too.
            for j in range(i + 1, len(tokens)):
                if name == "eval" or (tokens[j].startswith("-") and not tokens[j].startswith("--") and "c" in tokens[j][1:]):
                    target = j if name == "eval" else j + 1
                    if target < len(tokens):
                        hits += _ocs_dispatches(tokens[target], depth + 1)
                    break
    return list(dict.fromkeys(hits))


def refusal(tool: str, tool_input: dict) -> str | None:
    if tool in ("Agent", "Task"):
        kind = str(tool_input.get("subagent_type") or "general-purpose")
        # Compared without case: a live worker wrote `explore` for the built-in `Explore`.
        if kind.casefold() not in {t.casefold() for t in LOOKUP_TYPES}:
            return f"a {kind} subagent"
    elif tool == "Skill":
        name = str(tool_input.get("skill", "")).strip().lstrip("/").casefold()
        # A bare name is refused too: the model writes `execute` as often as `kein:execute`, and the hook sees the literal.
        if name.removeprefix("kein:") in DISPATCHING_SKILLS:
            return f"the {name} skill"
    elif tool == "Workflow":
        return "a workflow"
    elif tool == "Bash":
        hits = _ocs_dispatches(str(tool_input.get("command", "")))
        if hits:
            return ", ".join(hits)
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    if not isinstance(payload, dict) or not payload.get("agent_id"):
        return 0
    tool_input = payload.get("tool_input")
    what = refusal(str(payload.get("tool_name", "")), tool_input if isinstance(tool_input, dict) else {})
    if what is None:
        return 0
    print(
        f"Refused: you are a worker, and starting {what} would put a writer, reviewer or fan-out outside the lead's map of who owns what. "
        f"Do the work yourself, or stop and report what you would have dispatched and why. "
        f"A read-only lookup is fine: {', '.join(sorted(LOOKUP_TYPES))}.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
