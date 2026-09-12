# Authoring a Task in Another Worktree

Read this only when the lead means to have more than one task authored at once. A run that goes task by task in one worktree needs nothing here.

## What the ledger holds, and what it does not

The ledger is serial in its worktree: one task is write-active, tasks are accepted in order, and a task can neither leave the ledger nor move within it. That is what lets every verdict bind to one fingerprint of one tree. It says nothing about other worktrees. A second worktree is a second tree with its own run, and a task of this run may be *authored* there while this run works on the tasks before it.

Whether to do that is not the harness's call. A project whose stories share files has no candidates; a project whose tests hold a machine-global port can author in parallel and still verify one tree at a time; a lead with a large story and three small independent ones behind it has a reason to split and a reason not to. The harness makes the shape available and measures the one thing the ledger can measure.

## The measurement

```sh
ocs state execute split-check <state.json> <task-id>...
```

It answers whether the named pending tasks write where each other writes, or where any task still to be done in this run writes, on the `scope` lists the ledger holds. A directory names everything under it. Exit 0 with `disjoint: true` means the scopes do not meet; exit 1 lists each colliding pair and the paths. Accepted tasks are not counted: the side worktree branches from a tree that already has them.

The answer is about scopes as written. A scope that was written too narrowly passes here and collides in the merge, so the merge below is a real step rather than a formality.

## The shape

1. Run `split-check` for the tasks that would go out. A collision is a reason to keep them here, or to re-cut the scopes before the run opens — an existing task's scope cannot change once the run is under way.
2. Make the worktree from the current tree. `orca worktree create` gives one Orca manages from birth, runs the project's setup hook, and inherits the provider's trust record; `Agent(isolation: "worktree")` and `EnterWorktree` are the native forms. Which one is the project's choice.
3. Open a run there with a brief holding exactly the tasks going out, and run it as any run: its own ledger, its own reviews, its own acceptance at its own fingerprints. `ocs team --worktree <path>` sends a vendor lane into it.
4. In this run, those tasks stay `pending` in their places. When one's turn comes, its implementation round is the merge: bring the side branch into this tree, run the task's verification path here, and review here. Acceptance binds to this tree's fingerprint, as for any task. The side run's ledger is the record of how the change was authored; this run's ledger is the record that it landed.
5. The final audit reads this tree, whole, as always.

What the side run may not do is verify against a resource the main run is also using. Which resources those are is a fact about the project, and the project is where it is written down.
