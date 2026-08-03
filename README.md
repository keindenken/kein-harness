# kein

Personal Claude Code harness. Greenfield scaffold — no content ported yet.

## Layout

```
.claude-plugin/
  plugin.json        manifest. `name` is the only required field; component
                     paths are omitted on purpose so the default directories
                     below are auto-discovered and the manifest never drifts
                     as components are added.
  marketplace.json   local marketplace entry, for installing by name
agents/              subagent markdown files      -> kein:<name>
skills/              <name>/SKILL.md              -> /kein:<name>
workflows/           workflow scripts
bin/                 ON the Bash tool's PATH while enabled. `kein` only.
libexec/             kein subcommands, OFF PATH. `kein-<name>` -> `kein <name>`
```

Default locations Claude Code also auto-discovers, absent until needed:
`hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `output-styles/`, `monitors/`,
`settings.json` (only the `agent` and `subagentStatusLine` keys are honored).

## How this is loaded

Three modes exist. They differ on one axis that matters during development:
**does Claude Code read the plugin in place, or copy it into the cache?**

| Mode | Load | Edits live? | Scope |
| :--- | :--- | :--- | :--- |
| **skills-dir** (active) | symlink at `~/.claude/skills/kein` | **yes, in place** | every session |
| `--plugin-dir <path>` | CLI flag | yes, in place | one session |
| marketplace install | `plugin marketplace add` + `install` | **no — copied to cache** | every session |

The active setup is a symlink:

```sh
ln -s /Users/kein/Documents/workspace/dev/kein ~/.claude/skills/kein
```

Any folder under a skills directory holding a `.claude-plugin/plugin.json` is
loaded as `<name>@skills-dir` on the next session, with no marketplace and no
install step, **discovered in place rather than copied into the plugin cache**.
The symlink keeps the repo here while satisfying that rule. Verify with
`claude plugin list` (expect `kein@skills-dir` / `Status: loaded`). Remove by
deleting the symlink — nothing else is registered anywhere.

`--plugin-dir` is still useful for loading a variant into one session without
disturbing the symlinked copy.

### The version trap (only in marketplace mode)

Marketplace installs are cache-copied and gated on the version string: with
`version` set in `plugin.json`, new commits alone do **not** reach an installed
user — the cached copy is kept until the version is bumped. `version` is
harmless here because skills-dir loads in place. If this ever ships through a
marketplace while under active development, either bump it every time or drop
the field so the git commit SHA is used instead.

### Validate

```sh
claude plugin validate /Users/kein/Documents/workspace/dev/kein --strict
```

### Turning it off for one project

Because skills-dir loads for every session, the harness is live everywhere,
including alongside omc. Disable it per project with `"kein@skills-dir": false`
in that project's `.claude/settings.json` `enabledPlugins`.

## The bridge CLI

`bin/kein` is the single entry point on PATH. Subcommands are executables at
`libexec/kein-<name>`; the first `#:` comment line in each is its summary in
`kein help`. Keeping them out of `bin/` stops every subcommand from also
becoming a bare shell command.

```sh
kein help
kein doctor
```

## Naming rule

While omc is still enabled anywhere, **do not reuse its component names.**
Agents and skills are namespaced (`kein:executor`), but the prose that drives
delegation is not — `repo/.claude/CLAUDE.md` says "Route code to `executor`",
and during a dual-run that bare name is ambiguous. Same lesson already recorded
in `descvi/docs/research.md` §7.
