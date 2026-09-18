# Repository instructions skill — `/kein:instructions`

Status: Approved
Date: 2026-09-18

## Context

oh-my-claudecode 5.x ships `drydock`, a per-repository scaffold that writes CLAUDE.md and a dozen empty surfaces and audits them with `--check`. Reviewing it against this harness surfaced three complaints about `/kein:onboard`: it does nothing after a machine's first setup, nothing in the harness writes a repository's agent instructions, and the HUD's shape is fixed. A `--project` flag on `onboard` was considered and rejected, because `onboard` is machine-scoped and reversible by contract while repository instructions are committed files.

Separately, `onboard` is a run-once skill whose description sits in every session's model context. The user considers that standing cost too high for what it does.

## Desired outcome

A repository gains, from one skill, an AGENTS.md that holds only what inspection of the repository cannot reveal and a CLAUDE.md that is the single line `@AGENTS.md`. The same skill reviews an existing agent instruction file against the `standing-prompt` rule and reports what it finds without editing. `onboard` no longer appears in the model's skill list.

## Scope

### In scope

- `onboard` declares `disable-model-invocation: true`.
- A new skill, `/kein:instructions`, with an authoring mode and a review mode (`--check`).
- Moving an existing CLAUDE.md's content into AGENTS.md and replacing CLAUDE.md with the `@AGENTS.md` anchor.

### Out of scope

- drydock's empty surfaces: `docs/standards/`, `docs/business/`, `docs/adr/`, `design-system/`, `.mcp.json`, `scripts/`, `.gitattributes`. No flow in this harness fills them.
- drydock's document-language contract. The file's existing language governs.
- `CLAUDE.local.md`.
- HUD configurability.

## Requirements

- `onboard`'s description does not reach the model context; `/kein:onboard` remains invocable by the user.
- Authoring inspects the repository before asking anything, and asks the user only what inspection cannot establish: gotchas, constraints whose reason is invisible, conventions that live in someone's head. Answers are written into AGENTS.md in the form `standing-prompt` prescribes.
- A short or empty AGENTS.md is a valid authoring result when nothing needs asking.
- CLAUDE.md, after authoring, contains only the line `@AGENTS.md`.
- When only a populated CLAUDE.md exists, its content is moved verbatim into AGENTS.md and CLAUDE.md becomes the anchor. The move changes no text; anything worth changing in the moved content is reported as a review finding.
- When only AGENTS.md exists, authoring creates the CLAUDE.md anchor and extends AGENTS.md in place. Existing content is never overwritten.
- When both AGENTS.md and CLAUDE.md already carry content, the skill reports the situation and asks instead of merging.
- Review with no argument covers the repository's AGENTS.md and CLAUDE.md. Review with a path covers that file when it is one `standing-prompt` governs (CLAUDE.md, AGENTS.md, SKILL.md, `.claude/rules/**`, `prompts/**`).
- Review reads `standing-prompt` as its criterion, reports findings, and edits nothing in that run. Each finding names the `standing-prompt` clause it rests on. An edit happens only after the user approves, typically as the next turn's instruction.
- The new skill is model-invocable.

## Constraints

- For this change, `standing-prompt` stays a `paths:` rule in `plugin/rules/` and stays the single copy; the skill reads it rather than restating it.
- The skill name must not collide with an `ocs` subcommand (`ask`, `doctor`, `state`, `state-dir`, `team`, `validate`) or a native Claude Code command.
- Prompt prose names no model; tier comes from `agents.json` if any agent is involved.
- `plugin/` is what ships; anything the skill runs lives under `plugin/`.

## Decision boundaries

- The syntax that selects authoring versus review.
- Whether review also runs cheap mechanical checks, such as paths and commands AGENTS.md names that do not exist.
- The order and wording of authoring questions, within "ask only what inspection cannot reveal".
- The shape of a review finding, provided it names its `standing-prompt` clause.

## Acceptance criteria

- [ ] In a new session with the plugin enabled, the model-visible skill list contains no `kein:onboard`, and `/kein:onboard status` still runs.
- [ ] Authoring in this repository leaves AGENTS.md byte-identical to the CLAUDE.md content before the run and CLAUDE.md equal to `@AGENTS.md` plus a newline.
- [ ] Authoring in a repository with only AGENTS.md creates the CLAUDE.md anchor and leaves AGENTS.md's prior content intact.
- [ ] Authoring in a repository where both files carry content changes neither file and asks the user.
- [ ] In a fresh repository, none of the questions authoring asks can be answered by reading the repository.
- [ ] Review leaves `git status` unchanged, and every finding it reports names a `standing-prompt` clause.
- [ ] Review given a path `standing-prompt` does not govern says so rather than reviewing it.
- [ ] `claude plugin validate plugin --strict` passes.

## Decisions and rationale

- **A separate skill, not `onboard --project`:** `onboard` writes only outside the repository and is undone per step by `removal.md`; committed repository documents break both properties.
- **`standing-prompt` stays a path rule for this change:** it is the one copy, and the skill reading it adds an entry point without a second copy. Moving it into the skill would stop it loading on hand edits; moving it into `deliberate` would give a verdict-only skill the writing rules and load them only when deliberating. Where it finally lives is deferred, not settled.
- **Review reports, the user approves next:** this matches how `deliberate` is used in practice, a report followed by "fix it", so the skill needs no approval step of its own.
- **Review defaults to AGENTS.md and CLAUDE.md, with a path argument:** keeps the skill repository-scoped while leaving a route to any file the rule governs.
- **Authoring asks rather than infers:** a draft inferred from README, configuration, and history fills the file with what looking already shows, which is what `standing-prompt` forbids and what drydock's CLAUDE.md seed produces.
- **Existing CLAUDE.md content moves to AGENTS.md:** the user prefers CLAUDE.md as an anchor, and AGENTS.md is what other vendors such as Codex read. The move is verbatim so that moving and judging stay separate.
- **Both files populated means ask:** merging two authored documents is a judgement about which text governs, which is the user's.
- **The new skill is model-invocable:** the user chose reachability from requests like "tidy AGENTS.md" over removing its description cost. Only `onboard` loses model invocation.
- **Named `instructions`:** literal, and wide enough to cover path-argument review of agent-followed documents in general.

## Relevant system evidence

- `plugin/skills/handoff/SKILL.md`: declares `disable-model-invocation: true`; `kein:handoff` is absent from the model-visible skill list in the session that produced this document while the other kein skills are listed.
- `plugin/skills/onboard/SKILL.md`: machine-only, writes `<config home>/rules/kein`, `<config home>/kein/onboard/`, and Orca's statusline script, "no edit that cannot be undone".
- `plugin/rules/standing-prompt.md`: `paths:` frontmatter over CLAUDE.md, CLAUDE.local.md, AGENTS.md, SKILL.md, `.claude/rules/**`, `prompts/**`, `prompt/**`; the only file in `plugin/rules/`.
- `deliberate` SKILL.md: "It produces a verdict, not an edit" and defers writing to `standing-prompt`.
- `plugin/libexec/`: `ocs-ask`, `ocs-doctor`, `ocs-state`, `ocs-state-dir`, `ocs-team`, `ocs-validate`.
- oh-my-claudecode v5.4.0 `skills/drydock/SKILL.md`: detect first, never clobber, one real file plus a one-line pointer; its CLAUDE.md seed lists language, framework, and package manager, which its own `agent-doc-discipline` forbids.

## Assumptions and risks

- `disable-model-invocation` removing a skill from the model's list is observed for `handoff` in one session, not documented here; the first acceptance criterion re-checks it for `onboard`.
- "Answerable by reading the repository" is a judgement, so the fresh-repository criterion is checked by reading the questions, not mechanically.
- The model-invocable description may trigger on edits where the `standing-prompt` rule alone was enough.

## Deferred items

- HUD configurability: a separate `onboard` change with its own plan.
- Where `standing-prompt` lives, and its loading condition (once per session, on first read of a matching file): unchanged here and not settled. The gate is after `/kein:instructions` ships, when the user reconsiders moving it into the skill or elsewhere with the skill in hand; a hand edit of an agent prompt observed without the rule loaded is evidence for that decision.
