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
    "review_sha256": "<hash excluding the Status line>",
    "status": "Draft"
  },
  "phase": "drafted",
  "round": 0,
  "verdicts": {"architect@claude": null, "critic@claude": null},
  "findings": [],
  "closure": [],
  "next_action": "dispatch round 1 fresh reviewers"
}
```

`input.summary` is required and is what reaches every lane in the review package; `input.reference` is optional and names the file `reconcile` re-hashes on resume. Name a file that already held the requirements — one written for the run records only that the lead's own text has not changed, and the lead is the one agent here no lane reviews.

The keys of `verdicts` are the run's lane roster, written once and fixed for the run: a lane that returned `MUST_FIX` cannot be dropped and the plan approved without it. Each key is `<role>@<vendor>`, with `:advisory` appended for a lane that reports without gating approval — `architect@claude`, `critic@codex`, `critic@codex:advisory`. A default run is `architect@claude` and `critic@claude`. Each role needs at least one lane that is not advisory, since a role served only by advisory lanes cannot block anything. A finding carries the same lane identifier as the verdict it came from.

Each verdict contains only `lane`, `verdict`, `plan_sha256`, and `reviewed_at`. Each persisted finding contains only `lane`, `claim`, `evidence`, `impact`, and `required_correction`. Each closure entry contains only `lane`, `finding`, `disposition`, and `evidence`, with the disposition one of `CLOSED`, `PARTIAL`, `NOT CLOSED`, `REWORDED-ONLY`.

`revised` is the only writer of `closure` and it writes on every call, so omitting `--closure` records that the revision was not checked rather than leaving an earlier disposition standing over text it never read. Nothing reads the field for approval except one refusal: an `Approved` state cannot retain a disposition other than `CLOSED`. That is the contract's two halves as a mechanism — a positive closure check cannot approve, because `_blocking_pass` never looks here, and a negative one blocks.

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

## Driving the run

One subcommand per transition. Each reads the saved state and the plan file, builds the next state, and promotes it through the same validation, so nothing is passed that the two of them already know — the round number, both hashes, and the artifact's own `Status` are read, never supplied.

```sh
ocs state ralplan start   --run-root <runs/ralplan> --slug <slug> --plan <path> --summary <text> --lanes architect@claude,critic@claude [--input <path>]
ocs state ralplan open    <state.json>                    # the next official round
ocs state ralplan block   <state.json> --findings <file>  # the round's consolidated findings
ocs state ralplan revised <state.json> [--closure <file>] # Planner's revision landed
ocs state ralplan approve <state.json>                    # every blocking lane passed this hash
ocs state ralplan complete <state.json>                   # compact to the receipt
ocs state ralplan abort   <state.json> --reason <text>
```

`start` names the run directory itself — `<run-root>/<YYMMDD-HHMMSS>-<slug>/state.json` — and prints the path it wrote, which is what every later command takes as its positional. Pass that path to `start` instead when a run directory already exists. Nothing needs creating first: a checkpoint makes its own parent directory.

`--next` overrides `next_action` on any of them; each carries a default. `--verdict <lane>=<verdict>` on `approve` names an advisory lane, which is otherwise left unset.

`--findings` takes a JSON array of findings, or an object carrying one under `findings`. It is the only content a transition cannot derive, and it is the round's review record rather than scratch — keep it beside the run.

`checkpoint <state.json> <candidate.json>` promotes a hand-authored state and remains for a shape no transition names — `blocked`, `interrupted`, `gathering_evidence`. Delete the candidate once it succeeds, since a long run otherwise leaves one per checkpoint behind in the run directory; the durable record is `state.json` and the receipt.

`validate-plan <plan.md>` checks the artifact's shape alone. `validate-state <state.json>` checks one state document's shape and no transition; every promoting command already runs it. `reconcile <state.json>` recomputes the plan and input hashes against the files on disk and returns the exact next action — run it before every resume and after compaction.

## What a round checkpoints

Three states per blocked round, and a lane returning is not one of them:

1. the round opens — phase `reviewing`, fresh round number, empty verdicts;
2. the round is blocked — phase `revising`, consolidated findings persisted, every verdict cleared;
3. the revision landed — phase `drafted`, findings cleared, which the transition rules permit only once the review hash has moved.

`Status` stays `In Review` across all three: the run is open the whole time, and the artifact says so. Only `phase` moves.

A verdict arriving is not a state worth writing. The next checkpoint clears the map, so a checkpoint holding one incoming verdict is erased before anything reads it, and a blocked round records its review in `findings`, which carries the lane on each entry. Wait for every dispatched lane to return, then write the checkpoint that resolves the round.

Verdicts are recorded for their own sake only on the approving round, where they are the evidence that every fresh lane passed one hash and they survive into the receipt.
