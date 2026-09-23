# Execute Task Ledger Contract

## Executability Gate

Input is executable when:

- the intended outcome and scope are bounded;
- work can be ordered without inventing a material architecture, product, scope, acceptance, or safety decision;
- each task has a completion condition;
- each task has at least one usable verification path.

Formal plan approval is not required. Record the declared plan status when known, but gate on the conditions above.

A factual correction or implementation-detail adjustment that stays within the authorized outcome and scope may change a task's title, verification path, or rationale, with its reason recorded. A task's scope and completion condition are fixed once it is in the ledger, and `checkpoint` refuses a change to either. Append a newly discovered necessary task at the end of the ledger only with its title, scope, rationale, completion condition, and verification path. When the correction or the ruling lands in the plan itself, `amend` the run with the reason; the input moves and the ledger stays, so a completion condition that points at the plan's text follows the correction there. A correction that falsifies a completion condition's own ledgered wording has no route inside the run. Otherwise checkpoint `blocked` with the missing decision and its impact.

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

Task statuses are `pending`, `implementing`, `verifying`, `reviewing`, `correcting`, `accepted`, and `parked`. Tasks are under way at once only where their scopes do not meet, a directory naming everything under it, and a task does not start ahead of an earlier pending task whose scope meets its own; a parked task collides exactly as a pending one does. A scope entry with no path parts — `.`, `./`, an empty string — names the whole tree, so it meets every other task's scope: a task scoped that way cannot dispatch alongside a write-active sibling, waits behind an earlier pending or parked task the same as any narrower scope would, and holds a later task back in turn. `split-check` answers the same question before a dispatch, and refuses a parked task the same way it refuses any non-pending one.

Each open task carries a `scope_fingerprint`, the fingerprint of its scope on the observed tree, filled at every checkpoint and sealed at acceptance. Its verification, verdicts and acceptance bind to that, so a write elsewhere does not unseat its review and a write inside its scope does.

`ocs state execute dispatch <state.json> <task-id>...` moves a task from `pending` to `implementing` and, in the same checkpoint, seals its `dispatch_scope_fingerprint`: one sha256 per path the scope's `git` pathspec matches, read against the index (`git ls-files`) and the visibly untracked files under it (`git ls-files --others --exclude-standard`) — ignored paths and the run ledger under `.agents/kein/runs/` excluded, and a scope entry with no path parts, such as `.` or `./`, covering the whole tree rather than nothing. What is hashed per path is the actual bytes on disk right now — a symlink's target, or a regular file's content, read in chunks — never `git diff` output and never an index blob id, both of which move for reasons that have nothing to do with what this task actually wrote. Sealing happens before any executor is told to start, which is why the seal is the task's content at dispatch and not whatever a partial write leaves behind. `checkpoint` fills the same seal for any `pending -> implementing` candidate that leaves it unset, so `dispatch` is the documented route to it but not the only way the transition seals; run `dispatch` first and only then dispatch the executor regardless, since nothing else orders the two. `checkpoint` refuses a `pending -> implementing` candidate whose literal seal does not match what it computes itself, and refuses a change to an already-sealed `dispatch_scope_fingerprint` on every other transition except `parked -> pending`. The run's first checkpoint has no predecessor to check that against, so it is held to the same outcome directly instead: no task may carry `dispatch_scope_fingerprint`, and a `parked` task's `parked.from` must equal `pending`. A hand-authored candidate can neither forge a seal nor move one that already exists, on the first checkpoint or any later one.

`unresolved_findings` is empty at the opening position and, on an accepted task, holds what the task carries: the findings a `REVISE` lane returned that do not cite its completion condition and were not promoted to a task of their own. Their shape is in the review contract.

A decision only some tasks depend on parks those tasks while the rest continue: `ocs state execute park <state.json> <task-id>... --question <text> [--ref <id>]` moves a `pending`, `implementing`, or `correcting` task to `parked`, and clears `latest_verification`. A task already under way parks once every path in its scope clears one of two routes, asked per path rather than of the whole scope at once. The first: the path is restored to its dispatch content, read as the actual content at that path, not a diff against HEAD, so a commit made elsewhere while the task is under way (this repository commits each verified unit) does not stand in the way once the task's own bytes there are back. The second, asked only of a path that fails the first: the path carries no staged or unstaged modification against HEAD and is not visibly untracked either -- so a commit that instead carries the task's own undone write on that path, rather than reverting it, still clears it, because a rebase moves a path's content for reasons that have nothing to do with unfinished writes and this route answers the same question the seal does for that path (does this task still hold a write nobody has accepted here) just as directly. A path that fails both is evidence of unaccepted work and blocks the park; an untracked path the seal already holds unchanged clears on the first route alone and is never asked the second question, so it never blocks and is never named as a reason one did. `park`'s own `parked` record names which route was needed and every path the seal comparison found diverging, when the second route was needed for any of them; an executor stops before any decision-dependent write regardless of which route parked it. When some path clears neither route, `park`'s refusal names only the paths actually blocking: which still differ from the dispatch seal, and that HEAD does not clear them either. When nothing is dispatchable and a task is parked, the run checkpoints `blocked` and names each parked question. Once the decision is made, `ocs state execute unpark <state.json> <task-id>...` returns the task to `pending` and drops the stale seal along with the `parked` record, so the next `dispatch` seals fresh; a ruling that changes the plan lands there through `amend`. Finalization does not start while a task is parked.

## Evidence Gates

Run a load-bearing Evidence Gate before dependent production work. An expected result may select only a branch already authorized by the input. An unexpected result outside every authorized branch blocks the run; it does not authorize a new design or scope.
