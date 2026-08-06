# RALPLAN State Schema

Store state under `<run-root>/<YYMMDD-HHMMSS>-<slug>/state.json`, where the run root is `ocs state-dir runs/ralplan`.

## Nonterminal state

Active, blocked, and interrupted state uses exactly these top-level fields:

```json
{
  "schema_version": 1,
  "workflow": "ralplan",
  "run_id": "260802-120000-boundary",
  "lifecycle": "active",
  "working_directory": "/absolute/target",
  "repository": "/absolute/repository",
  "input": {
    "reference": "/absolute/requirements.md",
    "summary": "Implement the bounded boundary behavior.",
    "sha256": "<64 lowercase hex characters>"
  },
  "plan": {
    "path": "/absolute/target/.agents/kein/plans/boundary.md",
    "artifact_sha256": "<exact file hash>",
    "review_sha256": "<hash excluding Status and Status reason lines>",
    "status": "Draft"
  },
  "phase": "drafted",
  "round": 0,
  "verdicts": {"architect": null, "critic": null},
  "findings": [],
  "next_action": "dispatch round 1 fresh reviewers"
}
```

Nonterminal state carries no timestamp. `reconcile` decides continuation and reads no time, `run_id` already carries the start to the second, and the file's own mtime is the last write. Do not reintroduce one without a reader that branches on it.

Each verdict contains only `lane`, `verdict`, `plan_sha256`, and `reviewed_at`. Each persisted finding contains only `lane`, `claim`, `evidence`, `impact`, and `required_correction`.

Allowed nonterminal phases are `initializing`, `drafting`, `drafted`, `reviewing`, `revising`, `gathering_evidence`, `blocked`, and `interrupted`. Use the closest current activity; put the operationally exact continuation in `next_action`.

The first durable checkpoint is the validated Planner-authored Draft: lifecycle `active`, phase `drafted`, round `0`, both verdicts null, and no findings. A completed receipt, Approved artifact, review round, or revision state cannot be introduced as the first checkpoint.

## Completed receipt

```json
{
  "schema_version": 1,
  "workflow": "ralplan",
  "run_id": "260802-120000-boundary",
  "lifecycle": "completed",
  "completed_at": "2026-08-02T12:30:00+09:00",
  "plan": {
    "path": "/absolute/target/.agents/kein/plans/boundary.md",
    "artifact_sha256": "<exact approved artifact hash>",
    "review_sha256": "<fresh dual-approved review hash>"
  },
  "approvals": {
    "architect": {"lane": "architect", "verdict": "PASS", "plan_sha256": "<review hash>", "reviewed_at": "2026-08-02T12:28:00+09:00"},
    "critic": {"lane": "critic", "verdict": "PASS", "plan_sha256": "<review hash>", "reviewed_at": "2026-08-02T12:29:00+09:00"}
  }
}
```

## Aborted receipt

```json
{
  "schema_version": 1,
  "workflow": "ralplan",
  "run_id": "260802-120000-boundary",
  "lifecycle": "aborted",
  "aborted_at": "2026-08-02T12:15:00+09:00",
  "reason": "The user cancelled planning."
}
```

Create a candidate JSON file, then run `ocs state ralplan checkpoint <state.json> <candidate.json>` from the skill directory. The command validates the plan, transition, hashes, and compact terminal shape before atomically replacing state. Run `reconcile` before every resume and after compaction.
