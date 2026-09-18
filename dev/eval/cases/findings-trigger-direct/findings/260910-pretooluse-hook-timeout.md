---
claim: A PreToolUse hook that exceeds its timeout lets the tool call proceed rather than blocking it.
measured: 2026-09-10
versions: claude-code 0.0.0-fixture
reproduce: unrecorded
status: current
project: fixture
---
# A timed-out PreToolUse hook does not block

## Result

The hook slept past its timeout and the Bash call ran.
