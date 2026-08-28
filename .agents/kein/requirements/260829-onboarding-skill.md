# Onboarding skill — `/kein:onboard`

Status: Approved
Date: 2026-08-29

## Context

Three things have to be true before this harness is usable on a machine, and none of them is in version control. On the machine where the harness was built they were made by hand and live only in `~/.claude/`:

- `~/.claude/rules/wiki -> /Users/kein/Documents/wiki/_rules`, which is what puts `standing-prompt.md` in front of a session that opens a `SKILL.md` or a `CLAUDE.md`.
- `~/.claude/kein/orca-hud-wrapper/`, three shell files that render the `claude-hud` statusline in front of Orca's relay and re-apply themselves when Orca reverts them.
- A `UserPromptSubmit` hook in `~/.claude/settings.json` that runs the repair.

This is the state `docs/project/prompt-edit-rules/260810-prompt-revision/ratchet.md` names: a standing configuration outside version control, whose pre-edit form exists nowhere. A second machine reproduces none of it, and neither does anyone who installs the plugin.

The harness is otherwise built for distribution — `plugin/` is a source root that ships whole — so the gap is specifically the machine setup around it.

## Desired outcome

A person who has installed the `kein` plugin on a fresh machine runs one skill and ends with: the harness's rules loading globally, the HUD rendering in the statusline, and the HUD surviving an Orca restart without anyone touching it again.

Nothing the skill wrote requires a subsequent manual step, and nothing it wrote is irreversible.

## Scope

### In scope

- A skill, `/kein:onboard`, that brings a machine to the state above and reports what it did.
- The harness carrying its own rules, so that there is something for the symlink to point at on a machine that has never seen the author's wiki.
- A statusline HUD implemented inside the plugin.
- A hook that re-applies the statusline wrapper after Orca reverts it, carrying its own off-switch.
- A removal mode on the same skill, per step, that undoes what onboarding applied while the plugin stays enabled.
- The `docs/purpose.md` edits this work makes necessary. Its scope list and its hooks non-goal both predate this decision; the record is adjusted against the decision rather than the decision against the record.

### Out of scope

- Installing or depending on the third-party `claude-hud` plugin. It is read as a reference and not shipped, linked, or required at runtime.
- Installing the `kein` plugin itself. Onboarding runs as a kein skill, so the plugin is present before it starts.
- Vendor setup that is not the harness's: Codex authentication, Orca installation, `bun` or `node`.
- Per-project configuration. Everything here is machine-level.
- Uninstalling the `kein` plugin, and anything that requires disabling it. Removal runs with the plugin enabled, because keeping the harness while dropping the machine setup is the case removal exists for.
- Migrating an existing hand-made setup. On the machine that has one, the skill's result replaces it; recovering the old form is the backup's job, not a migration path's.

## Requirements

- The skill performs every step it can and asks the user to act only where a step cannot be scripted. As specified, no such step remains.
- Re-running the skill on a machine already onboarded changes nothing and says so. Each step is idempotent and reports `already` versus `applied`.
- A step whose precondition is absent is skipped with its reason named, and the remaining steps still run. A machine without Orca gets rules and HUD; a machine without a `~/.claude` gets told.
- No value specific to the author's machine is written by the skill. Paths that vary are resolved at run time or asked for; none is hardcoded.
- `standing-prompt.md` lives in the repository as the single copy, and `~/Documents/wiki/_rules` does not keep a second one.
- The symlink is placed at the home level, so the rules load in every project rather than only where the plugin is enabled.
- The HUD is implemented in the languages the harness already uses. It adds no runtime the harness does not already require.
- The HUD reads what Claude Code already hands a statusline command on stdin. It does not shell out to another program to obtain usage, context, or model facts.
- The repair hook ships in the plugin. The skill does not register it.
- The repair path reads its own off-switch before doing anything and exits silently when it is set. Disabling the plugin also stops it, but that is not the off-switch — it costs the whole harness, and the case removal exists for is keeping the harness.
- Removal is per step. A user who wants the HUD gone and the rules kept gets that, because "is the harness doing this?" is answered by removing one piece at a time.
- Removal sets the off-switch before restoring anything the hook would re-apply. Restoring first is defeated within one message.
- Removal reports the state of every step, including the steps it found already undone, because most of what onboarding applies comes undone on its own once the hook stops.
- Removal refuses to silently take away what onboarding did not create. The rules symlink is the case: onboarding moved `standing-prompt.md` out of the wiki, so removing the symlink leaves the user with no rules at all rather than with what they had before. Removal names this and stops, or asks where the rules should point instead.
- Before the statusline wrapper is applied, the file it modifies is backed up, and the skill names the backup's path in its report.
- The skill reports what it changed, what it skipped and why, and what the user should see next.

## Constraints

- POSIX `sh` and `python3` only. `node`, `bun`, and any package manager are excluded — this is the reason the HUD is reimplemented rather than vendored.
- `~/.claude/settings.json` is not written. The one file outside the repository that is modified in place is Orca's `~/.orca/agent-hooks/claude-statusline.sh`, which Orca itself rewrites at every launch.
- Orca reverts that file to its canonical copy whenever it starts, so nothing may assume the wrapper persists.
- The hook's output reaches the model context on `UserPromptSubmit`, so the repair path prints nothing on success or failure.
- `claude-hud` is MIT-licensed. A reimplementation informed by reading it carries an attribution note; copied source would carry the licence itself, which is a reason to keep the reimplementation genuine.
- A skill may not share a name with an `ocs` subcommand. `onboard` collides with none of `ask`, `team`, `state`, `state-dir`, `validate`, `doctor`.

## Decision boundaries

- Which segments the HUD renders, and their order and colours, bounded by the acceptance criterion below.
- Where inside `plugin/` the HUD renderer, the wrapper block, and the repair script sit, and what they are called.
- How the wrapper resolves the path to the HUD renderer from inside Orca's script, where `CLAUDE_PLUGIN_ROOT` is not set.
- How idempotence is detected for each step (marker string, symlink target comparison, or equivalent).
- The shape of the repair hook's off-switch: a sentinel file, an environment variable, or the absence of an install marker.
- How the removal mode is selected — a flag, a subcommand, or an argument — and what it is called.
- Whether removal defaults to reporting and requires a second word to act.
- Whether the backup of Orca's script is refreshed when Orca legitimately updates it, and where it is kept.
- The exact wording and shape of the `docs/purpose.md` edits.
- Whether `standing-prompt.md` is edited on the way in, or moved verbatim and revised separately.

## Acceptance criteria

- [ ] On a machine with none of the three in place, one invocation of `/kein:onboard` leaves all three in place, and the skill's report names each.
- [ ] A second invocation immediately afterwards changes no file and reports every step as already done.
- [ ] With Orca absent, the skill completes, applies the rules symlink and the HUD, and names Orca's absence as the reason the wrapper step was skipped.
- [ ] `~/.claude/settings.json` is byte-identical before and after every invocation.
- [ ] `git status` in the harness repository is clean after an invocation — the skill writes outside the repository only.
- [ ] The statusline the HUD renders is visually the same as the one the current hand-made setup produces: the same segments in the same order, with no effort symbols, `5h` and `wk` window labels, the context percentage labelled `ctx` and placed before the usage windows, and the skills count rendered as `<n> Skills:`.
- [ ] The rendered statusline is produced with no process outside `python3` and the shell.
- [ ] After Orca is restarted and one message is sent, the HUD is rendering again, and the transcript shows no output from the hook.
- [ ] With the plugin still enabled, running removal and then restarting Orca and sending one message leaves Orca's own statusline in place — the repair does not put the wrapper back.
- [ ] Removal run twice reports the second time that nothing was left to do, and changes no file.
- [ ] Removal of one step leaves the others in place: removing the HUD leaves the rules loading.
- [ ] Removal does not take the rules symlink away silently; it says what would be lost and requires the user to say so.
- [ ] Disabling the `kein` plugin also stops the repair from running, and Orca's next launch leaves its own statusline in place.
- [ ] With the harness's rules linked and the wiki copy gone, a session that opens a `SKILL.md` in an unrelated repository still loads `standing-prompt.md`.
- [ ] `docs/purpose.md` no longer contradicts what shipped: its skill list includes this skill, and its hooks non-goal accounts for the hook that now exists.

## Decisions and rationale

- **The skill installs rather than diagnoses:** onboarding exists to remove the manual work, and a report of commands leaves that work where it was. Absorbing `claude-hud` removed the one step that could not be scripted, so nothing is left for the user to run.
- **Distribution is assumed:** the artifact is written for a machine that is not the author's, which is what forbids hardcoding the wiki path and the author's `bun` location. It is also why the rules have to come with the harness — a symlink with nothing behind it is a step that succeeds and does nothing.
- **The HUD is reimplemented in `python3`, not vendored:** vendoring `claude-hud`'s `dist/` is faster to working and brings `node` into a plugin that has no runtime dependency at all, plus several hundred KB of foreign code and an upstream to track. Reimplementation costs the most writing and is the only option that leaves the constraint intact. It also deletes the current `sed` cosmetic layer, which exists solely to reshape another program's output.
- **The harness ships the rules:** the alternative, plumbing that links whatever directory the user names, is empty on a machine that has no such directory — which is the machine onboarding is for. Moving `standing-prompt.md` in gives the step something to point at and closes the question of whether those rules belong to the plugin ecosystem.
- **One copy of the rules, in the repository:** the same duplication was just deleted for the role library, where a source outside the repository and a committed copy inside it had to be kept in step by a recorded hash. Repeating it for rules would repeat the machinery.
- **The symlink goes at the home level:** the rules currently fire in every project, and scoping them to the plugin would silently narrow that. Home-level placement keeps the present behaviour; the cost is that removing the symlink removes them everywhere, which is also how they work today.
- **The repair hook ships in `plugin/hooks/hooks.json`:** it removes the only irreversible edit the skill would have made. The cost is real and accepted: in a project where `kein` is not enabled, an Orca restart leaves the HUD stripped until a kein-enabled session runs.
- **The hook carries an off-switch of its own, and disabling the plugin is not it:** an earlier reading treated plugin-disable as sufficient, which substituted a larger switch for the one that was asked for. Wanting the harness and not the machine setup is a real position, and under plugin-disable it is unreachable. It is also what makes removal possible at all — with the hook running unguarded, restoring Orca's script is undone within one message, so removal would not fail, it would be actively defeated.
- **Removal is a mode on the same skill, per step, and its body lives in a reference:** a run that came to install does not read the removal procedure, so that text leaves the main file — the placement rule in `standing-prompt.md`, not a length judgement. Per step because all-or-nothing refuses the case that motivates it: isolating whether the harness is the cause of something.
- **Removal's real product is the report:** once the hook is guarded, the wrapper comes off by itself at Orca's next launch, so what removal mostly does is say what is left and what already came undone. Naming it after removal alone would oversell the acting half.
- **`docs/purpose.md` is amended, not obeyed:** its skill list and its zero-hooks non-goal both predate this work. The user's instruction is explicit that the document is a record rather than a rule. The hook's admission requirement is satisfiable on its own terms and is recorded below rather than waived.

## Relevant system evidence

- `~/.claude/rules/`: contains one entry, `wiki -> /Users/kein/Documents/wiki/_rules`. The harness repository contains no rules of its own.
- `~/Documents/wiki/_rules/standing-prompt.md`: 4,943 bytes, with `paths:` frontmatter claiming `**/CLAUDE.md`, `**/CLAUDE.local.md`, `**/AGENTS.md`, `**/SKILL.md`, `**/.claude/rules/**`, `**/prompts/**/*.md`, `**/prompt/**/*.md`.
- `~/.claude/kein/orca-hud-wrapper/wrapper-block.sh`: renders `claude-hud` under `/Users/kein/.bun/bin/bun`, globs the newest version directory under `plugins/cache/*/claude-hud/*/`, and post-processes the rendered line with `sed` — removing the effort symbols `○◔◑◕●`, shortening `5h:`/`7d:` to `5h`/`wk`, moving the context percentage in front of the usage windows and labelling it `ctx`, and rewriting `✓ Skills (n):` as `n Skills:`. It re-runs the original script under `CLAUDE_HUD_WRAPPED=1` so the payload still reaches Orca.
- `~/.claude/kein/orca-hud-wrapper/repair.sh`: prepends the wrapper block to `~/.orca/agent-hooks/claude-statusline.sh` when a marker comment is absent, refreshes the pristine copy first, and writes only if the rebuilt file is larger than the original and still contains Orca's `statusline/claude` relay call. Its header records the failure it exists for: *"Orca reconciles ~/.orca/agent-hooks/claude-statusline.sh against its canonical copy at every app launch and reverts anything that differs, which strips the wrapper."* Its comments also record that it must stay silent because `UserPromptSubmit` stdout is injected into the model context.
- `~/.claude/settings.json`: `statusLine.command` is Orca's relay script. Eleven hook events are registered, all Orca's, plus one `UserPromptSubmit` entry that runs `repair.sh`.
- `~/.claude/plugins/cache/claude-hud/claude-hud/0.6.0/`: `package.json` declares `"engines": { "node": ">=18.0.0" }` and TypeScript sources; the directory is 43 MB with `node_modules`. Segments are separated under `src/render/` (`model-display`, `project-path`, `vcs-status`, `session-line`, `skills-mcp-line`, `todos-line`, `tools-line`, `agents-line`). `src/types.ts` shows `StdinData` already carrying `context_window` and `rate_limits`, which is what makes a reimplementation possible without a second data source.
- `README.md`: lists `hooks/hooks.json` among the default locations Claude Code auto-discovers inside a plugin, absent until needed.
- `docs/purpose.md`, Scope: names `interview`, `plan`, `ralplan`, `execute`, `handoff`, `ralph`, `autopilot`, orca orchestration, and after v1 `research` and `deliberate`. Onboarding is not among them.
- `docs/purpose.md`, Non-goals: *"Hooks. Start at zero. Adding one requires naming the failure it prevents and how its misfire would be detected."*
- `docs/purpose.md`, Portability: a Codex port is planned, and detail may differ where a platform forces it.
- `plugin/skills/`: seven skills at present.

## Assumptions and risks

- **The HUD's segment set is assumed recoverable from the running statusline.** It has not been captured; the acceptance criterion pins the result to what the current setup renders, so the assumption is checked at implementation rather than carried.
- **Reimplementing the usage segments is the largest unknown.** `rate_limits` arrives on stdin, but how `claude-hud` derives its windows and percentages from it has not been read in detail. If a segment turns out to need a source outside the payload, it is the first candidate to drop rather than a reason to add a dependency.
- **Resolving the plugin's own path from inside Orca's script is unsolved.** `CLAUDE_PLUGIN_ROOT` is not set there. The existing wrapper solves the equivalent problem by globbing the plugin cache, which is available but ties the wrapper to an installation layout.
- **A marketplace install pins a version directory, and a `skills-dir` symlink does not.** Whatever path the wrapper records is right for one of those and possibly stale for the other after an upgrade.
- **This is Claude-only.** The statusline, the hook, and the rules directory are all Claude Code surfaces with no Codex equivalent, so the planned port gets no onboarding from this work. `purpose.md` permits a platform-forced difference; it does not exempt anyone from noticing that the whole skill is one.
- **Moving `standing-prompt.md` out of the wiki changes what an unrelated session loads,** since it will then load through the harness's symlink instead of the wiki's. If the symlink is absent the rules are absent, where previously the wiki entry stood on its own.
- **The hook does not run where the plugin is disabled.** On a machine that works in projects without `kein`, an Orca restart can leave the HUD stripped for an arbitrarily long time. This was chosen knowingly over writing to `settings.json`.
- **Removal rests on onboarding writing three things, none of them irreversibly.** That is true as specified and is what makes the inverse small enough to be worth having. A fourth write, or one that cannot be undone, invalidates the removal mode's design rather than merely extending it.
- **Removal is expected to be rare.** Its standing cost is one routing line in the skill body, which is why rarity does not argue against it; but a rarely run path is also a rarely tested one, and nothing here proposes a fixture for it.

## Deferred items

- **The HUD's exact segment set, order, and colouring.** Gate: implementation, by capturing the current statusline output and matching it. The boundary is fixed by the acceptance criterion — visually the same as today — so the deferral cannot expand into a redesign.
- **Whether `standing-prompt.md` is revised while it moves.** Gate: a separate pass. `docs/open-threads.md` already carries "The ported skills have never been read against `standing-prompt.md`", and revising the rule and reading the skills against it are the same work; neither belongs in onboarding.
- **A Codex-side equivalent.** Gate: the Codex port. Recorded here so that the port does not discover the absence as a surprise.
