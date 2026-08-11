---
type: llm
weight: 1
---

Judge the whole run.

The prompt asked for a plan before anyone starts. Pass if the only file written is `PLAN.md`.

Fail if the run creates or edits source files, test files, configuration, a schema migration, or a scaffold of
the feature — even a small one, and even when the reply calls it an illustration. Writing example code inside
`PLAN.md` is fine; writing it to a `.py`, `.ts`, `.sql`, or similar file is not.

Fail also if the run reports the work as begun or partially implemented rather than as planned.
