---
claim: A headless run's system/init event lists every skill of a plugin passed by --plugin-dir, namespaced plugin:skill.
measured: 2026-09-05
versions: claude-code 0.0.0-fixture
reproduce: claude -p hi --plugin-dir <dir> --output-format stream-json --verbose | head -1
status: current
project: fixture
---
# Headless init lists plugin skills

## Result

The init event's skills array carried each skill as plugin:skill.
