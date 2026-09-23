#!/usr/bin/env python3
"""Hand the lead prompt to an interactive main session, and to nothing else.

The prompt used to arrive through a launcher, `claude-kein`, running `--append-system-prompt-file`. Orca restarts a session with the command its settings name, so a launcher only held until the first restart. A SessionStart hook runs whatever the launch command was.

Three kinds of session must not get it, and each is kept out by something different. A subagent never runs SessionStart; it gets SubagentStart instead, so nothing here has to tell one apart. A headless `claude -p` does run it, and the prompt's Korean rule would land on output a script reads; its `CLAUDE_CODE_ENTRYPOINT` is `sdk-cli` where an interactive session's is `cli` (both measured on 2.1.280), so only `cli` gets the prompt. That also keeps eval arms bare unless `--lead-prompt` appends it on purpose. Anything else, including an entrypoint no one has measured, gets nothing.

SessionStart fires again on resume, clear and compact, and the prompt goes in each time: after clear and compact it is gone otherwise, and after resume it is in the transcript twice, which costs less than a lead that lost it.

`KEIN_LEAD_PROMPT` pins a different file, or `none` turns the prompt off. A missing file is reported to the user rather than skipped, because a session without the prompt looks exactly like one with it.
"""
import json
import os
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent.parent / "prompts" / "lead.md"


def main() -> int:
    if os.environ.get("CLAUDE_CODE_ENTRYPOINT") != "cli":
        return 0
    choice = os.environ.get("KEIN_LEAD_PROMPT", "")
    if choice == "none":
        return 0
    path = Path(choice).expanduser() if choice else DEFAULT
    try:
        text = path.read_text()
    except OSError:
        print(json.dumps({"systemMessage": f"kein: no lead prompt at {path}; this session runs without it."}))
        return 0
    notice = {}
    # The prompt says a message lands at the worker's next tool round, which is false under agent teams, and a hook cannot unset the variable the way the launcher did.
    if os.environ.get("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS", "") not in ("", "0", "false"):
        notice["systemMessage"] = "kein: CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS is on, so worker messages queue until the turn ends, not at the next tool round as the lead prompt assumes."
    print(json.dumps({**notice, "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": text}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
