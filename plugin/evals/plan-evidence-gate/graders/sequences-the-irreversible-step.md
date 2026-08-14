---
type: llm
path: PLAN.md
weight: 1
---

Judge `PLAN.md`, not the reply. If the file does not exist, fail.

The fixture pairs a first-launch index build over an existing 600 MB library with an acceptance criterion that
a checksum of the `notes` table is identical before and after, and warns that writing the index and the notes
table in one transaction risks the notes.

Pass if the plan orders the work so that the guarantee protecting `notes` exists before anything writes at
scale — separating the index write from the notes table, building into a separate file or a separate
transaction, or establishing the checksum comparison as a gate the bulk build runs behind.

Fail if the plan schedules the bulk index build before any protection for `notes` is in place, or treats the
corruption hazard only as a risk to be aware of with no ordering consequence.

Mentioning the hazard is not enough on its own. The plan has to place a step because of it.
