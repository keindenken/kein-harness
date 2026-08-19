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
  "verdicts": {"architect@claude": null, "critic@claude": null},
  "findings": [],
  "next_action": "dispatch round 1 fresh reviewers"
}
```

The keys of `verdicts` are the run's lane roster, written once and fixed for the run: a lane that returned `MUST_FIX` cannot be dropped and the plan approved without it. Each key is `<role>@<vendor>`, with `:advisory` appended for a lane that reports without gating approval — `architect@claude`, `critic@codex`, `critic@codex:advisory`. A default run is `architect@claude` and `critic@claude`. Each role needs at least one lane that is not advisory, since a role served only by advisory lanes cannot block anything. A finding carries the same lane identifier as the verdict it came from.

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
    "architect@claude": {"lane": "architect@claude", "verdict": "PASS", "plan_sha256": "<review hash>", "reviewed_at": "2026-08-02T12:28:00+09:00"},
    "critic@claude": {"lane": "critic@claude", "verdict": "PASS", "plan_sha256": "<review hash>", "reviewed_at": "2026-08-02T12:29:00+09:00"}
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

## What a round checkpoints

Three states per blocked round, and a lane returning is not one of them:

1. the round opens — phase `reviewing`, fresh round number, empty verdicts;
2. the round is blocked — phase `revising`, consolidated findings persisted, every verdict cleared;
3. the revision landed — phase `drafted`, findings cleared, which the transition rules permit only once the review hash has moved.

`Status` stays `In Review` across all three: the run is open the whole time, and the artifact says so. Only `phase` moves.

A verdict arriving is not a state worth writing. The next checkpoint clears the map, so a checkpoint holding one incoming verdict is erased before anything reads it, and a blocked round records its review in `findings`, which carries the lane on each entry. Wait for every dispatched lane to return, then write the checkpoint that resolves the round.

Verdicts are recorded for their own sake only on the approving round, where they are the evidence that every fresh lane passed one hash and they survive into the receipt.

Delete the candidate file once the checkpoint succeeds. It is scratch for one transition; a long run otherwise leaves one per checkpoint behind in the run directory, and the durable record is `state.json` and the receipt.
