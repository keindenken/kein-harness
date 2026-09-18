---
claim: `orca terminal wait --for tui-idle` never returns for a codex TUI showing the update prompt; 9 of 9 waits hung past 300s (probe FX-9Z).
measured: 2026-09-15
versions: orca 0.0.0-fixture; codex 0.0.0-fixture
reproduce: the Probe section below
status: current
project: fixture
---
# tui-idle wait hangs on the codex update prompt

## Probe

Start codex in an Orca terminal on a machine where an update is available, then `orca terminal wait --for tui-idle`.

## Result

9 of 9 waits hung past 300s. Probe id FX-9Z.
