# `execute`: what has closed

Items moved out of `docs/skills/execute/open.md` once closed, kept verbatim with a note on what closed them.

## One worktree admits one run, and that was never a bar to parallelism

Closed 2026-09-26: recorded as an explanatory record rather than open work — the section's own last line already says nothing here needs changing.

The sentence this section was written about is gone from `SKILL.md`, and so is the last prose that described the ledger as serial: 2da9b80 made disjoint scopes concurrent, and the 2026-09-23 run removed "Then advance serially." along with it. What the prose used to say badly, the mechanism says exactly, and the mechanism is what remains.

The rule that survives is about runs, not tasks: taking tasks out of *one* run's ledger and scattering them across worktrees is what nothing supports. N briefs producing N runs in N worktrees was always the shape it permitted.

The prose is one half of a mechanism. `scripts/state.py` takes an exclusive `flock` on `<tmp>/kein-execute-<uid>/<sha256 of the canonical worktree>.lock`, and `canonical_worktree()` computes that key from `git rev-parse --show-toplevel` — the worktree's own root. It also computes `--git-common-dir` and does **not** use it for the lock. So two worktrees of one repository take two different locks and their runs do not exclude each other.

That is the deliberate opposite of how Codex resolves project trust, which does follow the common dir and so makes a linked worktree inherit the main one. Two path-derived keys in the same neighbourhood, resolved on purpose to different things.

`worktree_fingerprint()` is the other half: HEAD plus staged, unstaged and untracked content, so a run notices the tree moving underneath it. Splitting lanes across worktrees makes that check stronger rather than weaker, because nothing else is writing in the tree it fingerprints.

**Nothing here needs changing.** It is recorded because the rule was read the wrong way round during the worktree work of 2026-08-19 and stated as a blocker, and because the next reader will parse the sentence the same way.

## Its reason is not in this repository

Closed 2026-09-26: recorded as an explanatory record rather than open work — it explains why the lock is named as it is and finds nothing to change here.

`04206fa` ported the loop wholesale from the Codex side on 2026-08-04, and the lock predates that: it arrived named `codex-orca-execute-<uid>` and was renamed to `kein-execute-<uid>` on both sides at once, because a rename on one side only "would silently break exclusion between the two vendors."

So the invariant the lock actually protects is **cross-vendor**: a Claude `execute` run and a Codex `execute` run must not both hold the same worktree. That is why it is a harness invariant rather than a Codex detail, and why the name is load-bearing in a way no test asserts.

If the rule is ever revisited, the argument for it is on the Codex side, from before this repository existed. Nothing here ever recorded why the ledger had to be serial *within* a run, as opposed to why a worktree admits only one run -- which is why the serial reading went, and the per-worktree one stayed.
