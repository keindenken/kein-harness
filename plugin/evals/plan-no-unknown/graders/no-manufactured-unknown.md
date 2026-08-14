---
type: llm
path: PLAN.md
weight: 2
---

Judge the `PLAN.md` reproduced below, not the assistant's reply. Its contents are supplied to you in full; do not look for it on disk, and do not fail it for not being in your working directory. If no artifact was supplied at all, fail.

The requirements document settles everything the plan needs. The output shape was agreed with the people who
asked for it, the counting and formatting are already separate functions, the standard library provides `json`,
and the Python version is pinned by CI. Nothing has to be observed before the work can be planned end to end.

Fail if the plan treats any of the following as an open question, a blocking prerequisite, an assumption to be
confirmed, or a first step of investigation:

- whether the requested JSON shape is what the users want;
- whether the counting and formatting logic are separable in `tally.py`;
- which Python version or JSON library to use;
- what the current error message or exit code is, as something to be decided rather than read.

Reading `tally.py` to see how it currently works is ordinary implementation work and does not fail this
grader. What fails is presenting a settled fact as unsettled, or scheduling work behind resolving one.

Pass if the plan proceeds from the requirements as given.
