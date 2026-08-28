# kein-harness

The `kein` harness for Claude Code, driven by the `ocs` CLI.
Five skills, fourteen generated subagents, and a bridge CLI serving both vendors.

## Layout

```
.agents/kein/          run state and work products, resolved by `ocs state-dir`
agents/                the role library. Vendor-neutral prompt bodies; SOURCE
agents.json            the two facts about a role that are not about a vendor:
                       `tier` and `sandbox_mode`
docs/                  reference documentation
README.md
plugin/                everything Claude Code loads. The symlink points HERE,
                       not at the repository root.
  .claude-plugin/
    plugin.json        manifest. `name` is the only required field; component
                       paths are omitted on purpose so the default directories
                       below are auto-discovered and the manifest never drifts
                       as components are added.
    marketplace.json   local marketplace entry, for installing by name
  agents/              subagent markdown files      -> kein:<name>
  skills/              <name>/SKILL.md              -> /kein:<name>
  workflows/           workflow scripts
  hooks/hooks.json     one UserPromptSubmit hook, which keeps the HUD alive
  hud/                 the statusline renderer, the block that puts it in front
                       of Orca's, and the repair the hook runs
  rules/               rule files, linked into the config home by `onboard`
  bin/                 ON the Bash tool's PATH while enabled. `ocs` only.
  libexec/             ocs subcommands, OFF PATH. `ocs-<name>` -> `ocs <name>`
    lib/               sourceable shell shared by more than one subcommand
  agents.json          the role library's manifest, rendered alongside
```

`plugin/` is the source root, and everything above it is not shipped.
The split exists because a plugin folder is loaded whole: with the repository root serving as the plugin, `docs/`, `README.md`, and the entire `.agents/` state tree were part of what Claude Code loaded.
Artifacts still land at the repository root rather than inside `plugin/`, because `ocs state-dir` resolves through `git rev-parse --show-toplevel` and is unaffected by where the plugin sits.

The role library at `agents/` is the source, and `plugin/agents/` is `kein-dev render-agents`
rendering it under Claude's frontmatter — where `tier` becomes a `model:` and a `read-only`
`sandbox_mode` becomes `disallowedTools:`. Edit the library, not the render.

There is no second rendered copy for the other vendor. `ocs ask` and `ocs team` strip the
frontmatter at dispatch and hand the body over, because that block is Claude's translation of a
role rather than the role, and the two bodies were byte-identical for as long as both existed.
The facts the frontmatter was translated *from* are not recoverable from it, which is why
`agents.json` ships beside the render: `ocs` reads `sandbox_mode` to refuse a write-capable role
through a one-shot, and `tier` to pick a model.

Drift is therefore one question — does `plugin/agents/` still equal what the renderer produces —
and `kein-dev check-agents` answers it by re-rendering into a scratch directory and diffing. No
hash is recorded anywhere. One used to be, and `ocs ask` and `ocs team` checked it before spending
anything on inference, because the library lived in `~/.codex-orca` and a machine without that home
had no way to re-render. A hash answers "has this moved" where the source is out of reach; the
source is in the repository now, and a re-render says what moved and to what.

`rules/` is not auto-discovered — Claude Code reads rules from the config home, which is
why `/kein:onboard` links them there rather than the plugin shipping them into place. The
symlink sits at the home level on purpose: these rules are meant to fire in every project,
and a plugin-scoped copy would fire only where `kein` is enabled.

Default locations Claude Code also auto-discovers, absent until needed:
`.mcp.json`, `.lsp.json`, `output-styles/`, `monitors/`,
`settings.json` (only the `agent` and `subagentStatusLine` keys are honored).

## How this is loaded

Three modes exist. They differ on one axis that matters during development:
**does Claude Code read the plugin in place, or copy it into the cache?**

| Mode | Load | Edits live? | Scope |
| :--- | :--- | :--- | :--- |
| **skills-dir** (active) | symlink at `~/.claude/skills/kein` | **yes, in place** | discovered globally, enabled per project |
| `--plugin-dir <path>` | CLI flag | yes, in place | one session |
| marketplace install | `plugin marketplace add` + `install` | **no — copied to cache** | every session |

The active setup is a symlink:

```sh
ln -s /Users/kein/Documents/workspace/dev/kein-harness/plugin ~/.claude/skills/kein
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
claude plugin validate /Users/kein/Documents/workspace/dev/kein-harness/plugin --strict
```

### Scope: discovered globally, enabled per project

Discovery and activation are separate layers, and only the second one is per project.

Discovery is global and has no project-level equivalent.
A folder under a *user* skills directory is what gets registered; the same folder under a project's `.claude/skills/` is **not** discovered as a plugin.
That was measured — a probe plugin planted at `<project>/.claude/skills/probe/.claude-plugin/plugin.json` never appeared in `claude plugin list`.

Activation is where projects differ, through `enabledPlugins`.
The default is inverted deliberately: `~/.claude/settings.json` carries `"kein@skills-dir": false`, so the harness is off everywhere, and each project that wants it opts in.
This repository opts itself in through `.claude/settings.json`.

```json
{ "enabledPlugins": { "kein@skills-dir": true } }
```

Opting in is one line, so any other project can take the harness by adding the same file.
The reason for opt-in over opt-out is that a globally live harness reaches projects that never asked for it: `kein:` subagents were dispatched inside an unrelated project simply because the plugin was loaded there.
Off-by-default also makes a skill-absent control arm possible, which an always-loaded plugin would quietly contaminate.

## The bridge CLI

`bin/ocs` is the single entry point on PATH. Subcommands are executables at
`libexec/ocs-<name>`; the first `#:` comment line in each is its summary in
`ocs help`. Keeping them out of `bin/` stops every subcommand from also
becoming a bare shell command.

```sh
ocs help
ocs doctor
ocs state-dir runs/interview   # where this project's run state lives
ocs validate <workflow> ...    # check an artifact's shape
ocs state <workflow> ...       # the workflow's durable run state
```

The commands that build and gate the harness answer to `dev/kein-dev` instead, from
`dev/libexec/<name>`. They are split off by audience: `ocs help` is a surface an agent
reads mid-task, and `render-agents` overwrites generated artifacts.
The whole tree sits outside `plugin/` because a plugin folder is installed wholesale, and
anything under `plugin/bin/` would additionally become a bare command wherever the plugin
is enabled — putting them back in front of every agent by another route. Nothing under
`ocs` reaches into `dev/`, and nothing under `ocs` needs the role library either: a dispatch
reads the render it ships with.

`kein-dev` exports three roots. `KEIN_ROOT` is the plugin these commands read and write;
`KEIN_REPO_ROOT` holds what is not shipped, including the role library they render from;
`KEIN_DEV_ROOT` is `dev/` itself, and is how a subcommand reaches a sibling without
assuming it was copied along with the plugin — `eval` builds a variant arm out of an
arbitrary older commit, whose `plugin/` has no development tooling in it at all.

```sh
kein-dev help
kein-dev render-agents    # agents/ + agents.json -> plugin/agents/
kein-dev check-agents     # fail if the render has drifted
kein-dev eval <fixture>   # A/B a skill variant against a pinned fixture
```

### Where state goes

`ocs state-dir [<sub>]` resolves `<repo>/.agents/kein/<sub>`, falling back to the config
home when no repository is in scope.

In the repository rather than a vendor's config home, because a run started from Claude
should be resumable from Codex — a ledger parked under `~/.claude` is invisible to half
the harness. Under `.agents/` rather than a `.kein/` of its own, because that is already
the vendor-neutral namespace at both the project and home level.

Not `docs/`: that tree is for reference documentation, not the output of a work session.

The harness writes nothing the user did not ask for. `runs/` is transient and worth
adding to a project's `.gitignore`; `requirements/`, `plans/`, `handoff/` and other
deliverables are records and worth keeping.

### Asking another vendor

```sh
ocs ask codex --agent critic "<task>"       # one-shot, advisory
```

`ask` assembles exactly the role prompt, a blank line, and the task. It injects no
repository instructions — it cannot know whether a repository's conventions bear on a
given question, and the caller can, so put them in the brief.

Only the nine read-only roles are available. A write-capable role reached through a bare
one-shot would let a remote vendor edit the worktree with no workflow around it.

### Adding a teammate from another vendor

```sh
ocs team codex --agent executor "<task>"   # supervised, write-capable
```

`team` is the other half of the same bridge, and covers exactly the five write-capable
roles `ask` refuses. It composes a vendor terminal carrying the harness's own launch
arguments, hands it to Orca as a supervised worker, and blocks until Orca's completion
signal arrives. Orca owns the run, task, dispatch, completion, and recovery; none of that
is reimplemented.

What the command owns is the execution environment, because Orca's own agent launch takes
one global command per vendor and so cannot vary it per lane: the model comes from the
role's tier, the vendor home is the pinned vanilla one, and the sandbox is the narrowest
setting that can both write in the worktree and reach Orca to report. It refuses before
creating anything when the project has no trust record in that home, since an untrusted
directory stops the agent at a prompt the brief would be typed into.

The worker writes its report to a file and the command prints that path. That file is the
deliverable — this launch path gets no transcript hook, so a report the worker wrote on
purpose replaces one the tooling would have scraped.

One invocation is one worker, and it blocks. Several lanes come from backgrounding several
invocations; `--trace` persists everything, so nothing is lost when no one is waiting.

`--worktree` decides where the worker writes, and defaults to here. Backgrounded lanes sharing one
worktree share every file in it, so each lane wants `--worktree new` unless they are meant to
collide: that creates an Orca-managed worktree through `orca worktree create`, which runs the
project's setup hook and so leaves the worker able to run gates rather than landing in a tree with
no dependencies. An absolute path reuses an existing worktree instead. The run directory follows the
worker, because `workspace-write` is scoped to the tree it holds and a report path outside that tree
is one it cannot write.

The provider runs with `CODEX_HOME` pinned to the vanilla Codex home, never inherited: a
one-shot advisory call must not pick up the lead tuning in `~/.codex-orca`. `KEIN_CODEX_HOME`
overrides it. Nothing about the role library depends on that home any more — it was where the
library lived, which was an accident of where it was first written.

`--trace` writes the assembled prompt, the invocation, and the response under
`$(ocs state-dir runs/ask)/`. On `ocs ask` it is the only persistence there is — without it nothing
is written anywhere — which is why RALPLAN and `execute` both require it on every cross-vendor lane:
the trace is what makes that lane's verdict recoverable after the fact. Treat it as required wherever
a verdict has to outlive the session, rather than as a debug flag.

`ocs team` has no such flag. It creates its run directory and copies the role prompt whether or not
anyone asked, so the marginal cost of also recording the spec, the launch environment and the Orca
handles is two small files, and what they hold is the only record of which home, model and sandbox a
lane actually received. `execute`'s lane reference already deletes a requirement on the strength of
that record existing, and a record that depends on remembering a flag is precisely the failure that
argument names. The material is written as each piece becomes known rather than once the lane
succeeds, so a lane that dies early still leaves what it got that far with.

Requirements: [.agents/kein/requirements/260803-kein-ask-bridge.md](.agents/kein/requirements/260803-kein-ask-bridge.md)

## Claude subagents

`kein-dev render-agents` turns each role into a subagent under its canonical name, so
`kein:critic` and `kein:executor` exist alongside the rest. `sandbox_mode` from the
canonical manifest becomes the tool restriction:

| canonical | Claude frontmatter |
| :--- | :--- |
| `read-only` (9 roles) | `disallowedTools: Write, Edit, NotebookEdit` |
| `workspace-write` (5 roles) | no restriction |

A denylist rather than a `tools:` allowlist, because the constraint is "must not
mutate" and an allowlist would need re-enumerating every time a read-only tool is
added — the kind of rule that quietly goes stale.

**The translation is not exact.** Codex enforces read-only in its sandbox; Claude has
no subagent equivalent, so only the mutating tools are removed. Bash stays, because
these roles are required to run diagnostics, tests, and history inspection and taking
that away would break the role rather than bound it. Shell-level read-only is therefore
prompt-enforced here, not tool-enforced.

### Model routing

The canonical manifest carries a vendor-neutral `tier`, which each renderer maps onto its
own lineup. Tiers follow omc 4.15.7's per-role model choice rather than a fresh judgement.

| tier | roles | Claude | Codex |
| :--- | ---: | :--- | :--- |
| `deep` | 6 | `opus` | `gpt-5.6-sol` |
| `standard` | 7 | `sonnet` | `gpt-5.6-terra` |
| `fast` | 1 | `haiku` | `gpt-5.6-luna` |

Routing lives in configuration, which is what the normalization policy means by
"configure runtime model, effort, and sandbox separately". What it excludes is a model
named inside prompt prose.

The Codex half carries a wrinkle this side does not: those models default to `low`,
`medium`, and `medium` reasoning effort respectively, so `deep` would arrive at the
*lowest* effort unless the Codex renderer sets effort explicitly. Claude has no
per-agent effort field; effort comes from the session. The Codex renderer does not
consume `tier` yet.

### Sharing names with omc

These are omc's agent names too. Namespacing separates `kein:executor` from
`omc:executor`, but the prose that drives delegation is not namespaced — a repository
instruction saying "route code to `executor`" is ambiguous while both are enabled
(`descvi/docs/research.md` §7). Keep them apart per project with `enabledPlugins` in
that project's `.claude/settings.json` rather than relying on the namespace.
