# gaduri

Personal Claude Code harness. Greenfield scaffold — no content ported yet.

## Layout

```
.claude-plugin/
  plugin.json        manifest. `name` is the only required field; component
                     paths are omitted on purpose so the default directories
                     below are auto-discovered and the manifest never drifts
                     as components are added.
  marketplace.json   local marketplace entry, for installing by name
agents/              subagent markdown files      -> gaduri:<name>
skills/              <name>/SKILL.md              -> /gaduri:<name>
workflows/           workflow scripts
bin/                 ON the Bash tool's PATH while enabled. `gdr` only.
libexec/             gdr subcommands, OFF PATH. `gdr-<name>` -> `gdr <name>`
```

Default locations Claude Code also auto-discovers, absent until needed:
`hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `output-styles/`, `monitors/`,
`settings.json` (only the `agent` and `subagentStatusLine` keys are honored).

## Dev loop

Load without installing — session-scoped, repeatable, survives edits:

```sh
claude --plugin-dir /Users/kein/Documents/workspace/dev/gaduri
```

Validate the manifest (`--strict` turns unrecognized-field warnings into errors):

```sh
claude plugin validate /Users/kein/Documents/workspace/dev/gaduri --strict
```

Once it earns a permanent slot, add the local marketplace and enable it per
project via `enabledPlugins` in that project's `.claude/settings.json`.

## The bridge CLI

`bin/gdr` is the single entry point on PATH. Subcommands are executables at
`libexec/gdr-<name>`; the first `#:` comment line in each is its summary in
`gdr help`. Keeping them out of `bin/` stops every subcommand from also
becoming a bare shell command.

```sh
gdr help
gdr doctor
```

## Naming rule

While omc is still enabled anywhere, **do not reuse its component names.**
Agents and skills are namespaced (`gaduri:executor`), but the prose that drives
delegation is not — `repo/.claude/CLAUDE.md` says "Route code to `executor`",
and during a dual-run that bare name is ambiguous. Same lesson already recorded
in `descvi/docs/research.md` §7.
