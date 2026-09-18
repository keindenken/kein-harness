---
claim: SessionStart hook output reaches the main session's context only; dispatched subagents never see it (probe FX-3K, 0 of 12 subagents quoted the marker).
measured: 2026-09-12
versions: claude-code 0.0.0-fixture
reproduce: the Probe section below
status: current
project: fixture
---
# SessionStart hook output does not reach subagents

## Probe

A SessionStart hook printed a marker line. The lead quoted it; 12 dispatched subagents were each asked to quote any marker in their context.

## Result

0 of 12 subagents quoted it. Probe id FX-3K.
