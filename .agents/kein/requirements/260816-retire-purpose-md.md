# Retire and rewrite `docs/purpose.md`

Status: Approved
Date: 2026-08-16

## Context

`docs/purpose.md` was written 2026-08-03 and is 246 lines. Nothing reads it automatically: this repository has no `CLAUDE.md` and no `AGENTS.md`, and nothing under `.claude/`, `plugin/skills/`, `plugin/prompts/` or `plugin/agents/` references it. Its force is conventional — an agent working here finds it and treats it as authority, and the user reports the same effect on themselves. That is what "it is acting as a second harness" names.

Two things make that harmful rather than merely unusual.

The first is a staleness mechanism written into the file. Line 4 says to revise it "when a decision here is overturned, not when work happens", and the file then carries `## Order` with per-item `Done.` markers and a `## v1 done` gate — sections that only stay true if they are updated as work happens. Nobody updated them, so they went stale: `Scope` enumerates eight skills where six exist, `ping` appears in neither list, and `ralph` and `autopilot` are listed as scope with `Order 7` unmarked.

The second is that authority does not stay inside the sentences that earn it. The document mixes commitments, conventions, rationale and history in one flat prose register, so a paragraph of reasoning is read with the same force as a rule. Removing stale rules does not fix this; the surviving description would keep being obeyed.

Meanwhile the document is not uniformly old. `## Naming and surfaces` was revised twice on 2026-08-16 against evidence (`93994a0`, `9ec1616`, `5f587ab`), and `## v1 done` was never wrong — it is unmet, and unmet because deploying an untested harness into a live project was judged risky, not because the harness is incapable. OMC porting is finished.

## Desired outcome

`docs/purpose.md` states what this harness is for, what it deliberately is not, and how to tell when it is done — and nothing else. Every sentence in it either constrains a future decision or is visibly marked as explaining one that was already made. No section in it needs editing because work progressed.

Material that is not a goal has left the file for a home that fits it, or has been dropped because git already holds it. Live open questions are in `docs/open-threads.md`.

## Scope

### In scope

- Rewriting `docs/purpose.md` in place, section by section, at its current path.
- Deleting `## Why build one`, `## Order` and `## Operating rules` from it.
- Reducing `## Naming and surfaces` to one rule and relocating that rule.
- Reducing `## Portability` to the fact that a Codex port is planned.
- Adding `research` to the `Scope` skills list.
- Moving `## Open`'s four items to `docs/open-threads.md`.
- Making the file distinguish what binds from what explains.

### Out of scope

- Writing the replacement for `## Operating rules`.
- Slimming `README.md` to its core.
- Deciding `ping`'s fate.
- Building anything named in `Scope`, including `research`.
- Adding a `CLAUDE.md` or `AGENTS.md` to this repository.
- Running the `v1 done` round.

## Requirements

- The file keeps its path, `docs/purpose.md`, so the three live citations continue to resolve.
- The file carries goals and the reasoning that fixes those goals. It carries no progress, no history, and no open questions.
- **The file states which of its own content binds and which explains.** A reader who finds it without being sent there must be able to tell a commitment from a rationale without judgement. This is the defect the rewrite exists to fix, and it is not satisfied by deleting rules alone.
- `## What this is, under the obsolescence lens` survives with its component classification table. The link to `~/Documents/wiki/harness/harness-obsolescence.md` is removed: the wiki is under reconstruction and the target does not resolve.
- `## Scope`'s skills list is the existing eight plus `research`. Unbuilt entries are not demoted for being unbuilt.
- The relationship between the new `research` entry and the existing `Not in v1: autoresearch` deferral is stated, so the two do not read as contradicting each other.
- `## Non-goals` survives.
- Of `## Naming and surfaces`, only "no skill may share a name with an `ocs` subcommand" survives, placed as a constraint on what gets built rather than as naming trivia. The `kein`/`ocs` rationale, the surface table, `gdr` and the `~/.codex-orca` surfaces are dropped.
- `## Portability` becomes the statement that a Codex port is planned for later. The `~/.codex-orca/foundation/prompts/` machinery goes. "Vendor-specific detail may differ" is reworded — as written it invites a reading the user does not intend.
- `## v1 done` is reproduced verbatim, including "Needing to re-enable OMC at any point means not done."
- `## Order` is deleted in full. Its argument for `ocs team` is not carried forward.
- `## Open`'s four items are moved to `docs/open-threads.md`. Item four is restated against the fact that `ocs ask` no longer requires the Codex home.

## Constraints

- **No `CLAUDE.md` and no `AGENTS.md` in this repository, now or later.** The harness is built and measured against a maximally vanilla agent, and this repository is that test environment. Every fix available for the over-trust problem therefore acts on document content, never on injection or discovery.
- The rewrite may add to `README.md` where that is the right home. It must not treat `README.md` as a dumping ground, since `README.md` independently needs slimming.
- `~/Documents/wiki/` is under reconstruction. No requirement may depend on a wiki path resolving.

## Decision boundaries

- The exact prose of every surviving section.
- The mechanism that separates binding content from explanatory content — a framing sentence, a section split, a heading convention, or another device — provided a reader can apply it without judgement.
- Where within the file the surviving naming rule sits.
- Whether any dropped material is restated in `README.md` or simply dropped, judged per item against whether `README.md` is that item's right home.
- The wording that relates `research` to the `autoresearch` deferral.
- The wording of the reduced `Portability` statement.
- Section order and heading names.

## Acceptance criteria

- [ ] `docs/project/prompt-edit-rules/prompt-revision.md`, `docs/project/prompt-edit-rules/rule-md-distillation.md` and `docs/research/260811-planning-skill-references.md` still resolve their references to `docs/purpose.md`.
- [ ] No section of `docs/purpose.md` requires editing as a consequence of work progressing. Specifically: no `Done` marker, no per-item completion status, no progress table.
- [ ] No sentence claims a skill exists that is absent from `plugin/skills/`, and no sentence claims a skill is finished.
- [ ] Reading only `docs/purpose.md`, a first-time reader can state which of its sentences they are expected to comply with.
- [ ] `## v1 done` is byte-identical to its previous text.
- [ ] `docs/purpose.md` contains no path under `~/Documents/wiki/` and no `gdr`.
- [ ] `docs/open-threads.md` carries the four items formerly under `## Open`, and `docs/purpose.md` carries none.
- [ ] `kein-dev check-prompts` and `ocs help` are unaffected — this change touches documentation only.

## Decisions and rationale

- **Rewritten in place, not split out and not deleted:** the file's three live citations keep resolving, and a single entry point for "what is this for" is worth keeping. A separate decisions document was considered and rejected — one more discovered document is one more thing to be over-trusted, and the commit-message convention settled earlier already owns provenance.
- **The file stays a goals document rather than becoming a decision record:** the user's judgement. Consequence: material that is a convention rather than a goal has to leave, which is what disqualified the naming rationale and the surface table.
- **`## Order` deleted:** its `Done.` markers are not merely redundant with `ls plugin/skills/` — they are wrong. Existing is not finished: `interview` has had no A/B run of the kind `plan` received, and `ocs ask` is deliberately open to vendors beyond codex. A marker that is both restated elsewhere and false has no defence.
- **`Order 6`'s `ocs team` argument dropped rather than relocated:** git holds it, in its commit and in `.agents/kein/requirements/260806-ocs-team-bridge.md`. This follows the convention settled earlier the same day, that provenance goes in the commit rather than beside the rule.
- **`## Why build one` deleted whole, Keep list included:** OMC porting is finished, so the keep/replace analysis is history. The Keep list is also a stance rather than a goal, and one of its three items is already falsified — of "keep the skill names", only `plan` and `ralplan` came from OMC.
- **The obsolescence lens kept:** it produces the component classification table, which produces `Scope`. Without it `Scope` is a list with no warrant, and a list with no warrant is exactly what invites nearest-match compliance.
- **`Scope` keeps its unbuilt entries:** once `Order` is gone, `Scope` no longer implies progress, so an unbuilt entry sitting in scope is accurate rather than contradictory.
- **`## v1 done` kept verbatim:** it was never stale. It is unmet because deployment risk was unresolved, and the resolution is to run the round inside a worktree — containing the blast radius rather than softening the gate. A gate that punishes falling back to OMC was considered for relaxation and rejected on the user's judgement.
- **`## Operating rules` deleted now rather than rewritten now:** the replacement is gated on `standing-prompt`, which is still being settled. Deleting first is safe because the conventions the rules described are implemented and documented elsewhere — state under `.agents/kein/` is enforced by `ocs state-dir` and described in `README.md`.
- **Authority separation treated as a requirement, not a risk:** deleting stale rules leaves the surviving description carrying the same prescriptive force. The user named this as the thing to be careful about, so it is the criterion the rewrite is judged on rather than a caveat attached to it.

## Relevant system evidence

- `docs/purpose.md`: 246 lines. Line 4 states the revision rule that `## Order` and `## v1 done` contradict.
- No `CLAUDE.md`, no `AGENTS.md` at any level of this repository. `grep` over `.claude/`, `plugin/skills/`, `plugin/prompts/`, `plugin/agents/` finds no reference to `purpose.md`.
- 17 files cite `purpose.md`. Live: `docs/project/prompt-edit-rules/prompt-revision.md`, `docs/project/prompt-edit-rules/rule-md-distillation.md`, `docs/research/260811-planning-skill-references.md`. The remainder are records under `.agents/kein/{research,requirements,plans,handoff}/`.
- `plugin/skills/` holds `execute handoff interview ping plan ralplan`. `Scope` lists `interview plan ralplan execute handoff ralph autopilot` plus orca orchestration.
- `docs/open-threads.md` is 19 lines and already holds live threads; one of its three closed on 2026-08-16.
- Commits `93994a0`, `9ec1616` and `5f587ab` revised `## Naming and surfaces` on 2026-08-16, so the document is not uniformly stale.
- `9ec1616` removed `ocs ask`'s dependency on the Codex home, which is the gate named by `## Open`'s fourth item.

## Assumptions and risks

- **The over-trust may relocate rather than end.** With no `CLAUDE.md` by design, whatever reads as most authoritative under `docs/` becomes the de facto harness. `README.md` is longer than `purpose.md` and reads prescriptively. The user raised `README.md` slimming independently, which is the same observation from the other side; it is deferred, so this risk is accepted for now and is the reason the authority-separation requirement is worth applying to `purpose.md` first as a trial.
- Goals change, and changed during this interview. The document's revision rule survives that: a changed goal is a decision overturned, not work happening.
- Deleting `## Operating rules` assumes rules 1, 2 and 5 are adequately carried by `README.md` and by the code that implements them. If a convention turns out to exist only in those sentences, it is lost until the replacement lands.
- The expansion beyond engineering is a direction the user holds but has not made concrete, so nothing in this document is sized for it.

## Deferred items

- **Replacement for `## Operating rules`.** Gated on `standing-prompt`. It may land as a repository-local skill rather than as prose in a document, which the user raised as the likelier shape. Boundary that stays fixed: nothing restores rules to `docs/purpose.md` without going through that gate.
- **Slimming `README.md` to its core, moving detail out.** Boundary that stays fixed: this work does not enlarge `README.md` beyond what is genuinely its right home. Later gate: a separate pass with `README.md`'s audience question answered first.
- **`ping`'s fate.** It exists only to confirm the plugin loaded, which it no longer needs to do. Options are deletion or repurposing it as a skill that exercises other skill mechanics — scripts, progressive disclosure. Boundary that stays fixed: it is not added to `Scope` and is not treated as one of the harness's skills. Later gate: the choice between those two.
- **Expansion beyond engineering** into documentation, writing, design and planning. Stated as a direction and deliberately not concrete. Boundary that stays fixed: `Scope` commits to no non-engineering skill and nothing is built for it. Later gate: when one such use is concrete enough to name its own outcome.
- **Restating `## Open`'s fourth item** — extracting the canonical prompt library from `~/.codex-orca` — against what `9ec1616` settled. Boundary that stays fixed: it moves to `docs/open-threads.md` as-is if the restatement is not done at move time.
