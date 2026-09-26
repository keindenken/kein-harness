# `execute`: what is still open

## A completion condition's own wording cannot be corrected inside a run

`state.py` refuses any change to an existing task's `scope` or `completion_condition`, and `amend` moves only the plan. So when measurement falsifies the literal words a condition was ledgered with, the only exit is `blocked`, then abort and a new run. oh-my-claudecode 5.x gave ralph the opposite route: a criterion is replaced or superseded, the original kept verbatim with reason, evidence, authority and time, and every completion claim and approval bound to the criteria revision it was made under.

Deliberated on 2026-09-18 and not added. Every falsified ruling in the archived runs (`docs/artifacts/ledgers/260829-p47-run-state`, `260903-p48-run-state`: eight execute runs) was a plan clause, and the conditions defer to the plan ("DR47-6 lands", "the plan's §4 … text governs"), so `amend` carries the correction. The freeze is also what stops a lead fitting the condition to what got built; omc needed more than a dozen hardening commits to make its route safe.

**Reopen when** a run shows a condition written as literal values rather than a pointer — S48-1a's "20→8 / 80→16 clamped" is the shape — whose wording measurement refutes, and a lane's `blocks` cites that wording so the task cannot accept after the plan is amended.

The neighbouring question is in `docs/closed-threads.md`, "A plan correction ends the run": whether an amendment that touches the condition an already accepted task passed under should unseat that acceptance. That thread closed 2026-09-26 (4a41c57): a task accepted under an earlier revision now keeps the run from completing until a fresh lane re-confirms it against the amended plan. This section's own question — correcting a condition's wording inside a run, rather than what an amendment does to an acceptance already made — is untouched by that closure.

## A dispatched worker sometimes invokes `/kein:execute` itself

Seen rarely, reported by the owner 2026-09-26: a subagent `execute` spawned — `executor` or another lane — called the `execute` skill on its own task and started putting its own work through review. The lead prompt's standing rule 9 ("workers do not spawn writers") says in its own words that nothing in the harness enforces it; the brief is the only place it exists, and a worker's skill listing still shows `kein:execute`, whose description ("a bounded code change … carried through implementation, verification, independent review") matches the task the worker was just handed.

No trace of an occurrence has been archived, so neither the frequency nor what in the brief preceded it is known. Candidates to weigh with `/kein:deliberate` once one is captured: a line in `execute`'s worker brief, a role-level refusal in `agents/*.md`, or a mechanism — a `PreToolUse` hook on `Skill` that refuses `kein:execute` (and the other orchestrating skills) outside the lead session. The hook is the only one that does not rely on the worker reading a sentence, which is the failure being described.
