#!/usr/bin/env python3
"""Hand the lead prompt to an interactive main session, and the worker prompt to its subagents, and nothing to anything else.

Run as `prompt-layers.py lead` from SessionStart and `prompt-layers.py worker` from SubagentStart. The two events already separate the roles: a subagent never runs SessionStart, and a main session never runs SubagentStart.

The lead prompt used to arrive through a launcher, `claude-kein`, running `--append-system-prompt-file`. Orca restarts a session with the command its settings name, so a launcher only held until the first restart. A hook runs whatever the launch command was.

A headless `claude -p` runs both events, and a layer's language rule would land on output a script reads; its `CLAUDE_CODE_ENTRYPOINT` is `sdk-cli` where an interactive session's is `cli` (measured on 2.1.280, and in a SubagentStart hook on 2.1.283), so only `cli` gets a prompt. That also keeps eval arms and their subagents bare unless `--lead-prompt` appends the lead's on purpose. Anything else, including an entrypoint no one has measured, gets nothing.

SessionStart fires again on resume, clear and compact, and the lead prompt goes in each time: after clear and compact it is gone otherwise, and after resume it is in the transcript twice, which costs less than a lead that lost it.

The plugin's `prompts/<role>.md` is the core, and two optional layers follow it: the user's `~/.agents/kein/prompts/<role>.md`, then the project's `.agents/kein/prompts/<role>.md`, the project resolved in `ocs state-dir`'s order, minus its config-home fallback and with git asked from the hook input's `cwd`. They sit under `.agents/` rather than `.claude/` because the text is vendor-neutral and another vendor's harness can read the same files. A layer that does not exist is skipped silently; that is the ordinary case. Each layer arrives under a comment naming its path, so the reader can find the file it came from.

`KEIN_LEAD_PROMPT` and `KEIN_WORKER_PROMPT` pin a different core file, or `none` turns that role's prompt off, layers included. A missing core file is reported to the user rather than skipped, because a session without the prompt looks exactly like one with it.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

PROMPTS = Path(__file__).resolve().parent.parent / "prompts"
ROLES = {"lead": ("SessionStart", "KEIN_LEAD_PROMPT"), "worker": ("SubagentStart", "KEIN_WORKER_PROMPT")}


def project_root(cwd: str) -> Path | None:
    for var in ("KEIN_STATE_ROOT", "CLAUDE_PROJECT_DIR"):
        if os.environ.get(var):
            return Path(os.environ[var])
    try:
        out = subprocess.run(["git", "-C", cwd or ".", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    return Path(out.stdout.strip()) if out.returncode == 0 and out.stdout.strip() else None


def layers(role: str, cwd: str) -> tuple[list[str], list[str]]:
    layer = Path(".agents") / "kein" / "prompts" / f"{role}.md"
    texts, errors, seen = [], [], set()
    root = project_root(cwd)
    for path in [Path.home() / layer] + ([root / layer] if root else []):
        # Everything that touches the file sits inside the try: a layer is hand-written, and no fault in one may cost the core.
        try:
            path.stat()
            # A project rooted at the home directory would otherwise hand the user layer in twice.
            key = path.resolve()
            if key in seen:
                continue
            seen.add(key)
            texts.append(f"<!-- kein {role} layer: {path} -->\n{path.read_text(encoding='utf-8')}")
        except (FileNotFoundError, NotADirectoryError):
            continue
        except (OSError, RuntimeError, ValueError) as exc:
            errors.append(f"kein: {role} layer {path} is unreadable ({getattr(exc, 'strerror', None) or exc}); skipped.")
    return texts, errors


def main() -> int:
    role = sys.argv[1] if len(sys.argv) > 1 else "lead"
    if role not in ROLES or os.environ.get("CLAUDE_CODE_ENTRYPOINT") != "cli":
        return 0
    event, variable = ROLES[role]
    choice = os.environ.get(variable, "")
    if choice == "none":
        return 0
    try:
        cwd = json.loads(sys.stdin.read() or "{}").get("cwd", "")
    except (ValueError, AttributeError):
        cwd = ""
    if not isinstance(cwd, str):
        cwd = ""
    path = Path(choice).expanduser() if choice else PROMPTS / f"{role}.md"
    parts, notices = [], []
    try:
        parts.append(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        notices.append(f"kein: no {role} prompt at {path}; this session runs without it.")
    texts, errors = layers(role, cwd)
    parts += texts
    notices += errors
    # The lead prompt says a message lands at the worker's next tool round, which is false under agent teams, and a hook cannot unset the variable the way the launcher did.
    if role == "lead" and parts and os.environ.get("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS", "") not in ("", "0", "false"):
        notices.append("kein: CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS is on, so worker messages queue until the turn ends, not at the next tool round as the lead prompt assumes.")
    out = {}
    if notices:
        out["systemMessage"] = " ".join(notices)
    if parts:
        out["hookSpecificOutput"] = {"hookEventName": event, "additionalContext": "\n\n".join(parts)}
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
