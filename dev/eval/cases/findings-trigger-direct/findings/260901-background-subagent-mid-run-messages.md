---
claim: Without agent teams, a message the lead sends to a running background subagent is not delivered; 0 of 40 sends arrived (probe FX-7Q).
measured: 2026-09-01
versions: claude-code 0.0.0-fixture
reproduce: the Probe section below
status: current
project: fixture
---
# Background subagents do not receive mid-run messages without agent teams

## Question

Can the lead correct a background subagent while it runs, when agent teams are off?

## Probe

Launch 40 background subagents that each loop reading for an instruction, then send each one a message naming a marker file to write. Count the marker files.

## Result

0 of 40 marker files were written. The sends returned without error, so the lead cannot tell from the call that nothing arrived. Probe id FX-7Q.
