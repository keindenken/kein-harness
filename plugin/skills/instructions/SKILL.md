---
name: instructions
description: Use to write a repository's agent instructions into AGENTS.md, or with --check to review an agent instruction file against the standing-prompt rule. Review reports findings and edits nothing.
argument-hint: "[--check [path]]"
---

# A repository's agent instructions

Without `--check` this authors; with it, it reviews. Both judge against `${CLAUDE_PLUGIN_ROOT}/rules/standing-prompt.md`, so read that file whole before either, even if it loaded earlier in the session: it loads once, on the first file it matches, which may have been long ago.

The content lives in AGENTS.md, and CLAUDE.md is the single line `@AGENTS.md`. Claude Code reads CLAUDE.md and imports AGENTS.md through that line, while Codex and other vendors read AGENTS.md directly, so one file serves every agent working in the repository.

## Authoring

**1. Settle the two files at the repository root.** A CLAUDE.md whose only non-blank line is `@AGENTS.md` counts as empty.

| State | Action |
| :--- | :--- |
| neither has content | AGENTS.md is written from step 3; CLAUDE.md becomes the anchor |
| only CLAUDE.md has content | `git mv CLAUDE.md AGENTS.md` (plain `mv` when untracked), then write the anchor as a new CLAUDE.md |
| only AGENTS.md has content | write the anchor; AGENTS.md is extended in place |
| both have content | change neither; report what each holds and ask the user which governs |

The move changes no byte of the moved text. Whatever in it deserves changing becomes a review finding in the report, because moving and judging in one pass leaves no point where the user saw the text before it changed.

**2. Inspect before asking.** Read what an agent in this repository would find on its own: README, manifests and their scripts, CI configuration, existing docs, recent history. This rules questions out; nothing found here is written into AGENTS.md, since the agent will find it the same way.

**3. Ask one question at a time about what inspection could not establish** — the gotcha, the constraint whose reason is invisible, the convention that lives only in someone's head, which of two conflicting sources governs. Stop when the next answer would not change what an agent does. Ending with nothing to ask, and AGENTS.md short or empty, is a result, not a failure.

**4. Write the answers into AGENTS.md** under the standing-prompt rule, leaving existing lines as they are. Keep the file's language; a new file takes the user's.

**5. Report** what was moved, created, and added. When content was moved, run the review below over the moved text and include its findings, unapplied.

## Review (`--check`)

With no path, the targets are AGENTS.md and CLAUDE.md at the repository root. With a path, review it only if it matches the `paths:` frontmatter of the standing-prompt rule; otherwise say so and stop, because the rule was written for those files and holding other text to it produces findings nobody should act on.

Read each target whole. For every line that fails the rule, report where it is, the clause it fails (by the clause's bold lead), why it fails, and the change you would make, deletion included. A finding that the repository already shows something must name where it shows it. Paths and commands the target names are checked for existence too, since a dead one is a mechanical failure no reading catches. No findings is a valid result.

Where the question is whether a rule should exist at all rather than how it is written, the finding names `/kein:deliberate` instead of proposing an edit; that decision is not this skill's.

Edit nothing during review. The user approves findings afterwards and the edit follows then, so every change is read by someone before it lands.
