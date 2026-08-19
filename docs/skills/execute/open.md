# `execute`: what is still open

## The serial-ledger sentence is a lock, and it permits what it was read as forbidding

`SKILL.md` step 1 says "Distinct worktrees host only genuinely distinct runs: every normalized task remains in this run's serial ledger through acceptance and cannot be extracted to another worktree for concurrency." Read quickly, that says worktrees cannot be used to parallelise `execute`. It says the opposite.

The first clause is a permission. What the second forbids is narrower: taking tasks out of *one* run's ledger and scattering them. N briefs producing N runs in N worktrees is the shape the sentence describes, not the shape it rules out.

The prose is one half of a mechanism. `scripts/state.py` takes an exclusive `flock` on `<tmp>/kein-execute-<uid>/<sha256 of the canonical worktree>.lock`, and `canonical_worktree()` computes that key from `git rev-parse --show-toplevel` — the worktree's own root. It also computes `--git-common-dir` and does **not** use it for the lock. So two worktrees of one repository take two different locks and their runs do not exclude each other.

That is the deliberate opposite of how Codex resolves project trust, which does follow the common dir and so makes a linked worktree inherit the main one. Two path-derived keys in the same neighbourhood, resolved on purpose to different things.

`worktree_fingerprint()` is the other half: HEAD plus staged, unstaged and untracked content, so a run notices the tree moving underneath it. Splitting lanes across worktrees makes that check stronger rather than weaker, because nothing else is writing in the tree it fingerprints.

**Nothing here needs changing.** It is recorded because the rule was read the wrong way round during the worktree work of 2026-08-19 and stated as a blocker, and because the next reader will parse the sentence the same way.

## Its reason is not in this repository

`04206fa` ported the loop wholesale from the Codex side on 2026-08-04, and the lock predates that: it arrived named `codex-orca-execute-<uid>` and was renamed to `kein-execute-<uid>` on both sides at once, because a rename on one side only "would silently break exclusion between the two vendors."

So the invariant the lock actually protects is **cross-vendor**: a Claude `execute` run and a Codex `execute` run must not both hold the same worktree. That is why it is a harness invariant rather than a Codex detail, and why the name is load-bearing in a way no test asserts.

If the rule is ever revisited, the argument for it is on the Codex side, from before this repository existed. Nothing here records why the ledger has to be serial *within* a run, as opposed to why a worktree admits only one run.
