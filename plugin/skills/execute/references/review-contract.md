# Execute Review Contract

## Reviewer Selection

Choose lanes by the current evidence question. `kein:architect` normally evaluates boundaries and conformance; `kein:code-reviewer` normally evaluates correctness, regression, conventions, and maintainability. Use `kein:verifier` for proof adequacy, `kein:critic` for adversarial claims, `kein:tracer` or `kein:debugger` for causal uncertainty, `kein:test-engineer` for automated coverage and oracle quality, and `kein:qa-tester` for interactive runtime behavior.

This is neither a fixed reviewer matrix nor a fixed reviewer count. Every implementation or correction round requires at least one independent reviewer; complementary read-only lanes may run concurrently.

When the task's completion condition or verification path names a test or a gate, one of the round's lanes is `kein:test-engineer`, reading only, and its question is whether each named test can go RED against the defect it is there for. A lane that reads the code answers a different question, and two of them answer it twice; the holes that survived a review were oracles nobody read.

## Official Package

Supply the original bounded task, completion condition, repository instructions, relevant current code or diff, current fresh verification, selected rubric, task ID, round, and exact worktree fingerprint.

A new blind reviewer after correction receives no earlier finding, verdict, reviewer identity, correction note, claimed fix, closure result, or desired outcome. Wait for every selected lane, then consolidate the blocking findings before correction.

## Response

```markdown
VERDICT: PASS | REVISE | BLOCK
TASK_ID: task-001
ROUND: 1
WORKTREE_FINGERPRINT: <exact supplied fingerprint>

FINDINGS:
- Claim: <falsifiable defect or proof gap>
  Evidence: <precise location, observation, or contradiction>
  Impact: <realistic consequence>
  Required correction: <specific correction or missing proof>
  Severity: critical | important | minor
  Confidence: high | medium | low
  Blocks: <the clause of this task's completion condition it defeats, quoted — or `regression: <what>`, or `instruction: <which>` — or None>

UNCERTAINTY:
- <unresolved concern and discriminating evidence, or None>
```

The verdict follows the findings. `PASS` carries none; `REVISE` carries findings that all read `Blocks: None`; `BLOCK` carries at least one that cites something. The state refuses each way those can disagree, so the word is a summary of the findings rather than a second judgement about them. Every verdict binds to the supplied task, round, and fingerprint.

**`Severity` and `Blocks` answer different questions, and only the second decides acceptance.** Severity is how bad the defect is — the role's own calibration, kept. `Blocks` is whether *this task* is done, and it is a citation rather than a weight: quote the clause of the completion condition the finding defeats, verbatim, and the state checks that the clause is there. A `critical` defect outside this task's completion condition does not block this task; it becomes a task of its own. A `minor` one that defeats a clause blocks, because the task is not done.

`REVISE` accepts. Its findings are real, carried on the task and into the receipt, and none of them says the task is incomplete. That channel is why a lane never has to inflate a finding to keep it from evaporating — and why a `PASS` that lists findings in prose is a contradiction the state now refuses.

## Correction and Closure

Consolidate the `BLOCK` findings into one correction brief. After correction, require fresh `kein:executor` verification and at least one newly spawned, independent, new blind reviewer. A previous reviewer may run a primed closure check for a subtle or high-risk finding; its positive result cannot approve, while its negative result remains blocking and stays hidden from fresh reviewers.

## What acceptance carries

A task accepts over the findings a `REVISE` lane returned. Each is dispositioned once, at acceptance, and the disposition is one of three:

- **Fix it.** The executor corrects it within its `required_correction`, the task's verification path is re-run on the corrected tree, and the lead reads that diff. No fresh lane: the review that found it already happened, the finding never touched whether the task is done, and the final audit reads the whole change again. The acceptance records it under `fixed`, and it stands at the corrected fingerprint while the verdicts stand at the one they reviewed. A finding that cites the completion condition cannot take this route; that is a correction round.
- **Promote it.** Append a task whose rationale names the finding, and remove the finding from the task. The ledger already accepts an appended task at round zero; this is the existing mechanism, pointed at its intended input.
- **Carry it.** Leave it on the task; it projects into the receipt as `carried_findings`, which is the residual risk the final report names. Carrying costs the least now and the most later, so an `important` or `critical` carried this way must record `carried_because` — the state refuses acceptance without it — and a promotion that did not happen is a written decision rather than a silence. Severity prices the carry; it never gates the acceptance.

Nothing else is a disposition. A finding cannot be answered by deleting it from the list, because the receipt projects the list and a fresh audit reads the receipt.

## Final Audit

Final reviewers receive the complete post-simplification tree, all task completion conditions, repository instructions, final verification, and the exact final fingerprint. Any later mutation invalidates their verdicts.
