# RALPLAN Review Contract

## Official package

Create a separate package for each lane containing only:

- the original task or prompt-safe task summary;
- the governing requirements and constraints;
- the complete current canonical plan;
- the current review-content plan hash;
- relevant repository evidence or exact locations;
- the lane rubric and response shape below.

Do not include state history. Neither lane receives the other lane's response before returning its own. A fresh reviewer receives no previous finding, verdict, reviewer identity, revision note, change summary, claimed fix, closure result, or expected outcome.

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

`PASS` contains no must-fix entry. `MUST_FIX` contains at least one complete finding. Either lane can block approval. A concern is blocking when it can materially change scope, architecture, acceptance semantics, safety, or the bounded paths of an Evidence Gate. Preferences and non-consequential suggestions do not block.

## Revision and closure

Consolidate all current must-fix findings into one correction brief for Planner. After any review-content change, clear both official verdicts and send the complete revised plan to two new blind reviewers.

A previous live reviewer may perform a primed closure check for a subtle, high-risk, partial, or reworded correction. A positive closure check cannot approve or replace either fresh lane. A negative closure check remains blocking evidence and stays hidden from fresh reviewers.
