#!/usr/bin/env python3
"""Hand the lead prompt to an interactive main session, and to nothing else.

The prompt used to arrive through a launcher, `claude-kein`, running `--append-system-prompt-file`. Orca restarts a session with the command its settings name, so a launcher only held until the first restart. A SessionStart hook runs whatever the launch command was.

Three kinds of session must not get it, and each is kept out by something different. A subagent never runs SessionStart; it gets SubagentStart instead, so nothing here has to tell one apart. A headless `claude -p` does run it, and the prompt's Korean rule would land on output a script reads; its `CLAUDE_CODE_ENTRYPOINT` is `sdk-cli` where an interactive session's is `cli` (both measured on 2.1.280), so only `cli` gets the prompt. That also keeps eval arms bare unless `--lead-prompt` appends it on purpose. Anything else, including an entrypoint no one has measured, gets nothing.

SessionStart fires again on resume, clear and compact, and the prompt goes in each time: after clear and compact it is gone otherwise, and after resume it is in the transcript twice, which costs less than a lead that lost it.

The plugin's prompt is the core, and two optional layers follow it: the user's `~/.agents/kein/prompts/lead.md`, then the project's `.agents/kein/prompts/lead.md`, the project resolved in `ocs state-dir`'s order, minus its config-home fallback and with git asked from the hook input's `cwd`. They sit under `.agents/` rather than `.claude/` because the text is vendor-neutral and another vendor's harness can read the same files. A layer that does not exist is skipped silently; that is the ordinary case. Each layer arrives under a comment naming its path, so the lead can find the file it came from.

`KEIN_LEAD_PROMPT` pins a different core file, or `none` turns the prompt off, layers included. A missing core file is reported to the user rather than skipped, because a session without the prompt looks exactly like one with it.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent.parent / "prompts" / "lead.md"
LAYER = Path(".agents") / "kein" / "prompts" / "lead.md"


def project_root(cwd: str) -> Path | None:
    for var in ("KEIN_STATE_ROOT", "CLAUDE_PROJECT_DIR"):
        if os.environ.get(var):
            return Path(os.environ[var])
    try:
        out = subprocess.run(["git", "-C", cwd or ".", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    return Path(out.stdout.strip()) if out.returncode == 0 and out.stdout.strip() else None


def layers(cwd: str) -> tuple[list[str], list[str]]:
    texts, errors, seen = [], [], set()
    root = project_root(cwd)
    for path in [Path.home() / LAYER] + ([root / LAYER] if root else []):
        # Everything that touches the file sits inside the try: a layer is hand-written, and no fault in one may cost the core.
        try:
            path.stat()
            # A project rooted at the home directory would otherwise hand the user layer in twice.
            key = path.resolve()
            if key in seen:
                continue
            seen.add(key)
            texts.append(f"<!-- kein lead layer: {path} -->\n{path.read_text(encoding='utf-8')}")
        except (FileNotFoundError, NotADirectoryError):
            continue
        except (OSError, RuntimeError, ValueError) as exc:
            errors.append(f"kein: lead layer {path} is unreadable ({getattr(exc, 'strerror', None) or exc}); skipped.")
    return texts, errors


def main() -> int:
    if os.environ.get("CLAUDE_CODE_ENTRYPOINT") != "cli":
        return 0
    choice = os.environ.get("KEIN_LEAD_PROMPT", "")
    if choice == "none":
        return 0
    try:
        cwd = json.loads(sys.stdin.read() or "{}").get("cwd", "")
    except (ValueError, AttributeError):
        cwd = ""
    if not isinstance(cwd, str):
        cwd = ""
    path = Path(choice).expanduser() if choice else DEFAULT
    parts, notices = [], []
    try:
        parts.append(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        notices.append(f"kein: no lead prompt at {path}; this session runs without it.")
    texts, errors = layers(cwd)
    parts += texts
    notices += errors
    # The prompt says a message lands at the worker's next tool round, which is false under agent teams, and a hook cannot unset the variable the way the launcher did.
    if parts and os.environ.get("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS", "") not in ("", "0", "false"):
        notices.append("kein: CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS is on, so worker messages queue until the turn ends, not at the next tool round as the lead prompt assumes.")
    out = {}
    if notices:
        out["systemMessage"] = " ".join(notices)
    if parts:
        out["hookSpecificOutput"] = {"hookEventName": "SessionStart", "additionalContext": "\n\n".join(parts)}
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
