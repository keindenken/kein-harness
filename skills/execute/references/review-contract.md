# Execute Review Contract

## Reviewer Selection

Choose lanes by the current evidence question. `kein:architect` normally evaluates boundaries and conformance; `kein:code-reviewer` normally evaluates correctness, regression, conventions, and maintainability. Use `kein:verifier` for proof adequacy, `kein:critic` for adversarial claims, `kein:tracer` or `kein:debugger` for causal uncertainty, `kein:test-engineer` for automated coverage and oracle quality, and `kein:qa-tester` for interactive runtime behavior.

This is neither a fixed reviewer matrix nor a fixed reviewer count. Every implementation or correction round requires at least one independent reviewer; complementary read-only lanes may run concurrently.

## Official Package

Supply the original bounded task, completion condition, repository instructions, relevant current code or diff, current fresh verification, selected rubric, task ID, round, and exact worktree fingerprint.

A new blind reviewer after correction receives no earlier finding, verdict, reviewer identity, correction note, claimed fix, closure result, or desired outcome. Wait for every selected lane, then consolidate current `MUST_FIX` findings before correction.

## Response

```markdown
VERDICT: PASS | MUST_FIX
TASK_ID: task-001
ROUND: 1
WORKTREE_FINGERPRINT: <exact supplied fingerprint>

MUST_FIX:
- Claim: <falsifiable defect or proof gap>
  Evidence: <precise location, observation, or contradiction>
  Impact: <realistic consequence>
  Required correction: <specific correction or missing proof>
  Severity: critical | important | minor
  Confidence: high | medium | low

UNCERTAINTY:
- <unresolved concern and discriminating evidence, or None>
```

`PASS` contains no must-fix entry and binds to the supplied task, round, and fingerprint. A `MUST_FIX` from any lane blocks acceptance.

## Correction and Closure

Consolidate all blocking findings into one correction brief. After correction, require fresh `kein:executor` verification and at least one newly spawned, independent, new blind reviewer. A previous reviewer may run a primed closure check for a subtle or high-risk finding; its positive result cannot approve, while its negative result remains blocking and stays hidden from fresh reviewers.

## Final Audit

Final reviewers receive the complete post-simplification tree, all task completion conditions, repository instructions, final verification, and the exact final fingerprint. Any later mutation invalidates their verdicts.
