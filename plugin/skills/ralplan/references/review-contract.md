# RALPLAN Review Contract

## Official package

Create a separate package for each lane containing only:

- the original task or prompt-safe task summary;
- the governing requirements and constraints;
- the complete current canonical plan, with its `Status` line removed;
- the current review-content plan hash;
- relevant repository evidence or exact locations;
- the lane rubric and response shape below.

Do not include state history. No lane receives another lane's response before returning its own. A fresh reviewer receives no previous finding, verdict, reviewer identity, revision note, change summary, claimed fix, closure result, or expected outcome.

The removed line is why. Its reason half is required to say why approval is absent, which on any round after the first means naming the round, the verdicts it carried, and what the revision changed — four of the things in that list, arriving inside the artifact this package is required to carry whole. It is the same line the review hash already excludes, so removing it changes nothing a lane is being asked about.

## Architect lane

Apply the `kein:architect` role to architecture soundness, boundaries, interfaces, tradeoffs, reversibility, hidden dependencies, implementation readiness, and whether each Evidence Gate discriminates the decision it claims to gate.

## Critic lane

Apply the `kein:critic` role to requirement coverage, contradictions, missing failure behavior, unsupported assumptions, falsifiability, acceptance and verification adequacy, and whether the supplied gate could genuinely fail.

## Response

```markdown
VERDICT: PASS | REVISE | BLOCK
PLAN_SHA256: <supplied review-content SHA-256>

FINDINGS:
- Claim: <one falsifiable defect>
  Evidence: <source, contradiction, or missing proof>
  Impact: <what goes wrong if the plan ships as written>
  Required correction: <specific plan correction or missing evidence>
  Blocking: <scope | architecture | acceptance semantics | safety | evidence gate paths, or None>

UNCERTAINTY:
- <unestablished concern and the proof needed, or None>
```

The verdict follows the findings rather than being decided beside them. `PASS` carries none; `REVISE` carries findings that all read `Blocking: None`; `BLOCK` carries at least one that names a ground. Those are the only three shapes, and the state refuses each way they can disagree — a `BLOCK` with nothing blocking behind it, a `PASS` standing over the lane's own finding — so the verdict word is a summary of the findings rather than a second judgement about them.

**`Blocking` is the whole of the severity decision, and it is a claim rather than a weight.** Name the one ground the finding moves, or write `None`. Naming a ground is falsifiable and the lead reads it as such: a finding that concerns a gate is not the same as one that moves an Evidence Gate's bounded paths, and only the second is a ground. Preferences and non-consequential suggestions are not findings at all.

**`REVISE` is for a defect that is real and does not make execution unsafe.** It reaches approval carried rather than costing a round, and it carries the full finding shape while it does. That channel is the reason a lane never has to inflate a finding to keep it from evaporating.

`UNCERTAINTY` is not the middle of that scale and never became it. It holds what the lane could not establish, which is a different thing from a defect it could.

## Deferral

A `BLOCK` is answered by a revision or by a deferral, and a deferral is the lead overruling the ground the lane named — not the finding, and not on any other ground. It is recorded with the finding:

```markdown
- Finding: <the claim>
  Blocking claimed: <the ground the lane named>
  Disposition: DEFERRED
  Why the ground does not hold: <argued against that ground, not against the finding>
  Caught by: <the story, gate, or execution round that surfaces it instead>
```

`Caught by` is what keeps this from being a word. It is the plan template's own field, so a deferral that cannot name a catcher is a `Residual`, which the pre-mortem already requires writing down in a section every later lane reads. **The escape hatch costs a line in the artifact rather than a line in the ledger.**

What it is for: a defect the plan cannot settle and execution can, because the evidence does not exist until the code does. What it is not for: a round the lead would rather not run. The distinction is testable at the point of writing — if the required correction is something Planner could do now, deferring it defers work rather than evidence.

## Revision and closure

Consolidate the round's findings into one correction brief for Planner, and ask it for the corrected fact rather than a record of the correction — the revision's two readers are a fresh lane the contract forbids seeing it and an implementer who cannot act on it. After any review-content change, clear every official verdict and send the complete revised plan to a new blind lane set.

A previous live reviewer of either role may perform a primed closure check for a subtle, high-risk, partial, or reworded correction. A positive closure check cannot approve or replace a fresh lane. A negative closure check remains blocking evidence and stays hidden from fresh reviewers.

Its answer is one disposition per finding it was handed, recorded with `revised --closure`:

```markdown
- Finding: <the claim it answers>
  Disposition: CLOSED | PARTIAL | NOT CLOSED | REWORDED-ONLY
  Evidence: <what in the current text settles it>
```

`REWORDED-ONLY` is why the reader has to be primed. A blind lane can judge whether the current text is right; only a reader holding the text the correction replaced can see that it was restated rather than fixed. The run ledger's `round-N-plan.md` and `round-N-findings.json` are that priming, so a fresh agent given both is as capable here as a continued one — which is what makes the check available after a resume, and to a vendor lane that cannot be continued at all.
