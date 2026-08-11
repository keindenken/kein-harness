---
type: llm
weight: 1
---

Judge `PLAN.md`, not the reply. If the file does not exist, fail.

One requirement is easy to skip because it is about what must *not* happen: a file that cannot be read
produces the existing stderr message and exit code, and **no JSON at all** — partial output is worse than none
for a parser.

Pass if the plan accounts for this: that counting happens before anything is written to stdout, or that the
document is assembled in full and emitted once, or any other arrangement that makes partial output impossible,
and that the existing error behaviour is preserved rather than replaced.

Fail if the plan describes the JSON output without addressing the failure case, or if it emits per file as it
goes with no statement of what happens when a later file fails.

This grader is present so the case is not scored purely on what the plan omits.
