# Canonical Plan Artifact

Written to whoever writes the plan. It fixes the artifact's form and nothing about its content — what the body argues is your role contract's, not this file's.

```markdown
# <Plan title>

Status: Draft — <where this plan stands, whether it is provisionally executable, and any blocking decision or evidence gap>

<the plan body>

## Open Questions

- <non-blocking question and why its answer matters, or None>
```

You write `Draft`, and the reason after the em dash is yours. It is where a plan that is not ready for execution says so and says what would make it ready — **the marking your role contract asks for lives here, and this line is the only place that gives it a shape.** The em dash separates the machine-read word from the prose after it, and a period would not: a reason is full of them.

`In Review` and `Approved` also exist and neither is yours to write. A consensus workflow sets them while it runs, and it edits this line and nothing else in the artifact.

When the plan carries a bounded execution-time empirical obligation, use this exact optional shape:

```markdown
## Evidence Gates

### <Gate name>

- Claim: <load-bearing fact not yet established>
- Evidence method: <cheapest discriminating observation or measurement>
- Pass path: <already planned action for the passing result>
- Alternate path: <already planned action for the other expected result>
- Required before: <dependent production work that cannot start first>
- Unexpected result: <stop boundary when the observation fits no planned path>
```

A gate whose unexpected result has no stop boundary is not a gate. Every expected result needs a path that was decided here rather than at execution time, which is what keeps the obligation bounded.

When your role contract calls for a pre-mortem, use this exact optional shape. Whether one is called for is that contract's decision and not this file's:

```markdown
## Pre-mortem

### S<n>: <how this ships wrong>

- Caught by: <the acceptance criterion or gate that surfaces it>
- Prevented by: <the mechanism that stops it, or None>
- Acts on: <what that mechanism reads, writes, removes or attaches, and how it resolves that target>
- Residual: <what is accepted because nothing catches it, or None>
```

A scenario with no `Caught by` is a worry rather than a pre-mortem entry: it names a fear without saying which check would have to fail for it to happen. `Residual: None` and a missing `Residual` line say different things — the first is a claim that the scenario is covered, the second is silence about whether anyone looked.

`Acts on` describes the preventer rather than the scenario, because the preventer is the one element of the entry no earlier review has seen: the scenario has just been argued at length, and the mechanism guarding it is new here. It has no `None` — while `Prevented by` names a mechanism, an entry that cannot say how that mechanism reaches what it touches is showing a gap rather than reporting an absence.

The numbering is what lets the rest of the plan cite a scenario instead of restating it; the shape is otherwise free, and the section is the plan's own record of what it expects to survive.
