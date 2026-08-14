---
type: llm
weight: 2
---

Judge `PLAN.md` in the working directory, not the assistant's reply. If the file does not exist, fail.

The requirements document states that nobody has checked whether the bundled SQLite has FTS5 compiled in, and
that this is a compile-time option. The plan has to handle an unresolved fact that both blocks work and has
more than one plannable outcome.

Pass if the plan, for the FTS5 question, does all four of these:

- states the claim that is not yet established;
- names the observation that would settle it, and that observation is something cheap and specific — a
  `PRAGMA compile_options` query, `sqlite3_compileoption_used`, a probe that creates a virtual table and
  catches the error — rather than "investigate" or "confirm with the team";
- gives a course of action for FTS5 being present **and** a different course of action for it being absent,
  both chosen in the plan rather than left to whoever executes it, and **both of them still delivering what
  the requirements ask for**. A branch is not decided by being named. "If FTS5 is absent, keep the existing
  `LIKE` search" is a decision, and it abandons the desired outcome the requirements open with along with the
  under-300-ms and ranked-results criteria; a plan that takes it has decided to fail rather than decided what
  to do. Read each branch against the acceptance criteria and fail the plan if either branch cannot meet
  them;
- names what to do if the observation produces neither expected result, or otherwise bounds the case it did
  not plan for.

Fail if the plan:

- lists the FTS5 question as a risk, an assumption, an open question, or a first task, without both branches
  being resolved into planned work;
- assumes FTS5 is available and mentions the alternative only as a possibility;
- describes the fallback as "use a different approach" or "revisit the design" without saying which approach;
- names both branches but assigns the choice between them to execution time;
- resolves the absent branch into shipping the current behaviour unchanged, or into anything else that leaves
  a stated acceptance criterion unmet, however explicitly that is chosen.

The plan may reasonably fold the check into the first step of the work rather than isolating it as a
prerequisite. That does not fail this grader as long as both outcomes still have planned work attached.
