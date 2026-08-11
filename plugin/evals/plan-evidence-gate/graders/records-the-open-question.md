---
type: llm
weight: 1
---

Judge `PLAN.md`, not the reply. If the file does not exist, fail.

The requirements document leaves one thing genuinely undecided and says the team is comfortable either way:
whether a more recent note should outrank an older one of equal match quality. This does not block the plan —
the work is the same under either answer — so the right handling is to carry it as a question rather than to
stop for it or to silently choose.

Pass if the plan records the recency-versus-relevance tie-break as an open, non-blocking question, and the
plan's work does not depend on which way it goes.

Fail if the plan:

- treats it as blocking, or asks the user to resolve it before planning can continue;
- picks one behaviour and states it as settled without marking that the requirements left it open;
- omits it entirely.

Choosing a default is fine, and is the better answer, provided the plan says the requirements left it open and
that the default is reversible.
