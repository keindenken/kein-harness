# Execute Task Ledger Contract

## Executability Gate

Input is executable when:

- the intended outcome and scope are bounded;
- work can be ordered without inventing a material architecture, product, scope, acceptance, or safety decision;
- each task has a completion condition;
- each task has at least one usable verification path.

Formal plan approval is not required. Record the declared plan status when known, but gate on the conditions above.

A factual correction or implementation-detail adjustment may update a task when it stays within the authorized outcome and scope and its rationale is recorded. Append a newly discovered necessary task only with its title, insertion position, scope, rationale, completion condition, and verification path. Otherwise checkpoint `blocked` with the missing decision and its impact.

## Normalized Task

```json
{
  "id": "task-001",
  "title": "Reject an empty collection size",
  "scope": ["src/math.py", "tests/test_math.py"],
  "completion_condition": "clamp_index raises ValueError when size is zero",
  "verification_path": ["python3 -m unittest tests.test_math.MathTests.test_empty_size_rejected -v"],
  "rationale": "Required by the bounded input contract",
  "status": "pending",
  "round": 0,
  "latest_verification": [],
  "unresolved_findings": [],
  "acceptance": null
}
```

Task statuses are `pending`, `implementing`, `verifying`, `reviewing`, `correcting`, and `accepted`. Only one task may be write-active. Every earlier task must be accepted before a later task becomes active.

## Evidence Gates

Run a load-bearing Evidence Gate before dependent production work. An expected result may select only a branch already authorized by the input. An unexpected result outside every authorized branch blocks the run; it does not authorize a new design or scope.
