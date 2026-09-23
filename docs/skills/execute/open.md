# `execute`: what is still open

## One worktree admits one run, and that was never a bar to parallelism

The sentence this section was written about is gone from `SKILL.md`, and so is the last prose that described the ledger as serial: 2da9b80 made disjoint scopes concurrent, and the 2026-09-23 run removed "Then advance serially." along with it. What the prose used to say badly, the mechanism says exactly, and the mechanism is what remains.

The rule that survives is about runs, not tasks: taking tasks out of *one* run's ledger and scattering them across worktrees is what nothing supports. N briefs producing N runs in N worktrees was always the shape it permitted.

The prose is one half of a mechanism. `scripts/state.py` takes an exclusive `flock` on `<tmp>/kein-execute-<uid>/<sha256 of the canonical worktree>.lock`, and `canonical_worktree()` computes that key from `git rev-parse --show-toplevel` — the worktree's own root. It also computes `--git-common-dir` and does **not** use it for the lock. So two worktrees of one repository take two different locks and their runs do not exclude each other.

That is the deliberate opposite of how Codex resolves project trust, which does follow the common dir and so makes a linked worktree inherit the main one. Two path-derived keys in the same neighbourhood, resolved on purpose to different things.

`worktree_fingerprint()` is the other half: HEAD plus staged, unstaged and untracked content, so a run notices the tree moving underneath it. Splitting lanes across worktrees makes that check stronger rather than weaker, because nothing else is writing in the tree it fingerprints.

**Nothing here needs changing.** It is recorded because the rule was read the wrong way round during the worktree work of 2026-08-19 and stated as a blocker, and because the next reader will parse the sentence the same way.

## Its reason is not in this repository

`04206fa` ported the loop wholesale from the Codex side on 2026-08-04, and the lock predates that: it arrived named `codex-orca-execute-<uid>` and was renamed to `kein-execute-<uid>` on both sides at once, because a rename on one side only "would silently break exclusion between the two vendors."

So the invariant the lock actually protects is **cross-vendor**: a Claude `execute` run and a Codex `execute` run must not both hold the same worktree. That is why it is a harness invariant rather than a Codex detail, and why the name is load-bearing in a way no test asserts.

If the rule is ever revisited, the argument for it is on the Codex side, from before this repository existed. Nothing here ever recorded why the ledger had to be serial *within* a run, as opposed to why a worktree admits only one run -- which is why the serial reading went, and the per-worktree one stayed.

## A completion condition's own wording cannot be corrected inside a run

`state.py` refuses any change to an existing task's `scope` or `completion_condition`, and `amend` moves only the plan. So when measurement falsifies the literal words a condition was ledgered with, the only exit is `blocked`, then abort and a new run. oh-my-claudecode 5.x gave ralph the opposite route: a criterion is replaced or superseded, the original kept verbatim with reason, evidence, authority and time, and every completion claim and approval bound to the criteria revision it was made under.

Deliberated on 2026-09-18 and not added. Every falsified ruling in the archived runs (`docs/artifacts/ledgers/260829-p47-run-state`, `260903-p48-run-state`: eight execute runs) was a plan clause, and the conditions defer to the plan ("DR47-6 lands", "the plan's §4 … text governs"), so `amend` carries the correction. The freeze is also what stops a lead fitting the condition to what got built; omc needed more than a dozen hardening commits to make its route safe.

**Reopen when** a run shows a condition written as literal values rather than a pointer — S48-1a's "20→8 / 80→16 clamped" is the shape — whose wording measurement refutes, and a lane's `blocks` cites that wording so the task cannot accept after the plan is amended.

The neighbouring question is in `docs/open-threads.md`, "A plan correction ends the run": whether an amendment that touches the condition an already accepted task passed under should unseat that acceptance. `amend` now keeps the run, so the acceptance stands; omc's revision binding is one answer to that thread, not to this one.

## Left open by the 2026-09-23 run

Carried in that run's receipt; the run record is `260923-audit-stopping-rule.md`.

- **No guard against a future time.** `observed_at` and `reviewed_at` accept any timezone-aware value, and that run's ledger carries invented future stamps because nothing refused them. Reopen when adding the guard: refuse a time later than the checkpoint's own clock read.
- **`reviewer_role` is matched as an exact string.** The final-audit coherence rule, and acceptance's before it, compares roles verbatim, and runs on disk already spell them both `kein:critic` and `critic`. A PASS under the other spelling passes silently over its own role's carried findings — the relabel the rule exists to stop. Normalise the role before comparing, or validate it against `agents.json`.
- **`check-execute-state` outlasts a tool call.** At about four and a half minutes it cannot finish inside one call, so a lane briefed to run it backgrounds it and returns early. Either the suite gets faster or briefs keep naming its runtime and leaving the full run to the lead.

