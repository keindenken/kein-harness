---
name: dispatch
description: Fan a task out to background worker subagents and collect their results.
---

# Dispatch

1. Split the task into independent pieces, one per worker.
2. Launch each worker as a background subagent with its piece and the path it writes its result to.
3. Wait for every worker to finish, then read the result files and merge them.
4. Report which pieces succeeded and which failed.

Workers do not talk to each other. Each one owns exactly one result file, and the lead is the only reader of all of them.
