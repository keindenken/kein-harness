# RALPLAN Review Contract

## Official package

Create a separate package for each lane containing only:

- the original task or prompt-safe task summary;
- the governing requirements and constraints;
- the complete current canonical plan, with its `Status` and `Status reason` lines removed;
- the current review-content plan hash;
- relevant repository evidence or exact locations;
- the lane rubric and response shape below.

Do not include state history. No lane receives another lane's response before returning its own. A fresh reviewer receives no previous finding, verdict, reviewer identity, revision note, change summary, claimed fix, closure result, or expected outcome.

The two removed lines are why. `Status reason` is required to say why approval is absent, which on any round after the first means naming the round, the verdicts it carried, and what the revision changed — four of the things in that list, arriving inside the artifact this package is required to carry whole. They are the same two lines the review hash already excludes, so removing them changes nothing a lane is being asked about.

## Architect lane

Apply the `kein:architect` role to architecture soundness, boundaries, interfaces, tradeoffs, reversibility, hidden dependencies, implementation readiness, and whether each Evidence Gate discriminates the decision it claims to gate.

## Critic lane

Apply the `kein:critic` role to requirement coverage, contradictions, missing failure behavior, unsupported assumptions, falsifiability, acceptance and verification adequacy, and whether the supplied gate could genuinely fail.

## Response

```markdown
VERDICT: PASS | MUST_FIX
PLAN_SHA256: <supplied review-content SHA-256>

MUST_FIX:
- Claim: <one falsifiable defect>
  Evidence: <source, contradiction, or missing proof>
  Impact: <why approval is unsafe>
  Required correction: <specific plan correction or missing evidence>

UNCERTAINTY:
- <unestablished concern and the proof needed, or None>
```

`PASS` contains no must-fix entry. `MUST_FIX` contains at least one complete finding. Any lane can block approval. A concern is blocking when it can materially change scope, architecture, acceptance semantics, safety, or the bounded paths of an Evidence Gate. Preferences and non-consequential suggestions do not block.

## Revision and closure

Consolidate all current must-fix findings into one correction brief for Planner. After any review-content change, clear every official verdict and send the complete revised plan to a new blind lane set.

A previous live reviewer may perform a primed closure check for a subtle, high-risk, partial, or reworded correction. A positive closure check cannot approve or replace a fresh lane. A negative closure check remains blocking evidence and stays hidden from fresh reviewers.
