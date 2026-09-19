# Gate G1 — frontmatter hooks under a nested skill, probed 2026-09-19

This is the run U4 (`.agents/kein/plans/fsd.md`) calls Gate G1, plus the binding addition to it: whether a `hooks.json` `PostToolUse` `Skill` handler also fires, and what exact `skill` string a qualified and an unqualified Skill-tool call each leave in the hook input, from both the frontmatter placement and the `hooks.json` placement. `claude --version` was `2.1.276 (Claude Code)` throughout. Nothing here touches this repository; the probe plugin and every log live under a throwaway `mktemp -d` scratch directory outside it.

## Setup

A throwaway plugin `probeplug` was built at `$SCRATCH/probe-plugin` (`$SCRATCH` a fresh `mktemp -d`):

- `.claude-plugin/plugin.json` — a minimal valid manifest, `name: probeplug`.
- `scripts/log.py` — every hook target calls this with a label; it reads stdin as JSON, appends `{ts, label, extra_argv, input}` as one line to `$PROBE_LOG`, and always exits 0 so nothing the probe touches ever blocks anything.
- `skills/probe/SKILL.md` — the slash-only probe skill, `disable-model-invocation: true`, reachable only as `/probeplug:probe`. Its frontmatter declares all three hooks U4 needs measured: `Stop`, `PreToolUse` (matcher `Write`), `PostToolUse` (matcher `Skill`), each pointed at `scripts/log.py` through `${CLAUDE_PLUGIN_ROOT}`. Its body is a five-step directive: call the Skill tool for `probeplug:inner` (qualified), call it again for `inner` (bare), run `echo probe-bash-done` over Bash, write `probe-output-1.txt` with content `first`, then stop without asking anything.
- `skills/inner/SKILL.md` — the second, model-invocable skill the probe body calls into. It does nothing observable beyond replying one fixed line.
- `hooks/hooks.json` — the plugin-level placement being compared against the frontmatter one: `UserPromptSubmit` (logs the raw prompt), `PostToolUse` matcher `Bash`, and `PostToolUse` matcher `Skill` (the binding addition), all pointed at the same `log.py`.

`claude plugin validate probe-plugin --strict` passed both before and after the probe runs (`✔ Validation passed`), so this is also the record of that check.

Three headless processes were run, in this order, all with `PROBE_LOG` exported to a fixed path so every process appends to the same log:

```sh
cd "$SCRATCH"
claude -p '/probeplug:probe run the probe' --plugin-dir "$SCRATCH/probe-plugin" \
  --dangerously-skip-permissions --output-format json > run1.json
claude -c -p 'write another file' --plugin-dir "$SCRATCH/probe-plugin" \
  --dangerously-skip-permissions --output-format json > run2.json
# (probe/SKILL.md edited here to add the Bash step, then a fresh, non-continued process)
claude -p '/probeplug:probe run the probe' --plugin-dir "$SCRATCH/probe-plugin" \
  --dangerously-skip-permissions --output-format json > run3.json
```

`run1` was the first process: `claude -p '/probeplug:probe …'`, session `f42e1b54-27f8-45cc-bfe8-0d275c00917d`, with the probe body's original four steps (no Bash step yet). `run2` immediately continued that same process's session with `claude -c -p 'write another file'` — a genuinely new OS process, but `run2.json`'s own top-level `session_id` is the identical `f42e1b54-…`; this run produced no Bash-step evidence, since the probe body it continued from never had one. Only after `run2` finished was `probe/SKILL.md` edited to add the `echo probe-bash-done` step (covering `hooks.json`'s `PostToolUse Bash` handler, matching the 2026-09-19 shape exactly); `run3` then invoked `/probeplug:probe` fresh, `claude -p` without `-c`, which opened its own new session `66da9af9-197a-48e9-91ef-818712282bbf` — a process independent of `run1`/`run2`'s session, not a continuation of either. No `-c` continuation was ever run against `66da9af9-…`. `run1` and `run3` produced the same facts for every claim both cover; the quotes below are `run3`'s records, since only that run also carries the Bash-step evidence.

## Facts per claim

**(a) — frontmatter Stop and PreToolUse still fire after the model invokes a second, model-invocable skill with the Skill tool.** Holds. Within one process (`run3`, session `66da9af9…`), after both Skill-tool calls into `inner`, the log carries a `frontmatter-pre-write` record for the `Write` call:

```json
{"hook_event_name": "PreToolUse", "tool_name": "Write",
 "tool_input": {"file_path": ".../probe-output-1.txt", "content": "first"},
 "session_id": "66da9af9-197a-48e9-91ef-818712282bbf"}
```

and a `frontmatter-stop` record closing the same turn:

```json
{"hook_event_name": "Stop", "stop_hook_active": false,
 "last_assistant_message": "probe inner ok",
 "session_id": "66da9af9-197a-48e9-91ef-818712282bbf"}
```

Both fired after two intervening `Skill` tool calls in the same turn, so a nested skill invocation does not disarm the outer skill's frontmatter hooks within a process.

**(b) — a frontmatter `PostToolUse` hook with matcher `Skill` fires, and its input carries the invoked skill's name.** Holds. Two `frontmatter-post-skill` records appear per run, one per Skill-tool call:

```json
{"tool_name": "Skill", "tool_input": {"skill": "probeplug:inner"}, "tool_response": {"commandName": "probeplug:inner", "success": true}}
{"tool_name": "Skill", "tool_input": {"skill": "inner"},           "tool_response": {"commandName": "inner", "success": true}}
```

**(c) — `${CLAUDE_PLUGIN_ROOT}` expands in a frontmatter hook command.** Holds. The frontmatter `Stop` command was written `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/log.py" frontmatter-stop "${CLAUDE_PLUGIN_ROOT}"`, passing the same placeholder a second time as a literal argument so `log.py` could record it. Both runs' `frontmatter-stop` records carry `"extra_argv": ["/tmp/kein-fsd-g1-probe.RREtbs/probe-plugin"]` — the real path handed to `--plugin-dir`, not the placeholder text — and `log.py` only ran at all (rather than failing to find itself) because the command's own `"${CLAUDE_PLUGIN_ROOT}/scripts/log.py"` segment resolved the same way.

**(d) — the `session_id` a hook sees before and after a `claude -c` continuation in a new process.** The continuation keeps the same `session_id`. `run1.json`'s top-level `session_id` and `run2.json`'s (a fully separate `claude` process, `-c -p`) are both `f42e1b54-27f8-45cc-bfe8-0d275c00917d`; every hook record inside `run2` (the `hooksjson-user-prompt-submit` record for `"write another file"`) carries that identical id. This matters only to the alternate path's arming scheme (U4's `hooks.json` fallback would stay armed across such a continuation, which that path already treats as harmless); it does not change which path this probe selects.

`run2`'s turn carries exactly one log record: `hooksjson-user-prompt-submit`. No `frontmatter-*` record appeared for it at all — neither `frontmatter-pre-write` nor `frontmatter-stop` — although the model did perform a Write tool call in that turn (`run2.json`'s own result text names the file it wrote, `probe-output-2.txt`). This was read directly from the full log dump captured at the time (not a gap in the record): the frontmatter `PreToolUse`/`Stop` hooks declared in `probe/SKILL.md` simply did not fire for that Write call or for that turn's stop, which is the direct evidence behind "frontmatter hooks do not survive a `claude -c` continuation in a new process" rather than an inference from (d)'s `session_id` fact alone.

**(e) — whether a plugin `hooks.json` `UserPromptSubmit` handler receives the raw `/<plugin>:<skill> …` text as its `prompt`.** Holds. `run1`'s first log record:

```json
{"hook_event_name": "UserPromptSubmit", "prompt": "/probeplug:probe run the probe", "session_id": "f42e1b54-..."}
```

`prompt` is the literal slash-command line, unexpanded. This also only matters to the alternate path, not taken here.

**Binding addition — the `hooks.json` `PostToolUse` `Skill` handler, and the exact `skill` string for a qualified and an unqualified call, from both placements.** The `hooks.json` handler fires, alongside the frontmatter one, for both forms:

```json
{"label": "hooksjson-post-skill", "tool_input": {"skill": "probeplug:inner"}}
{"label": "hooksjson-post-skill", "tool_input": {"skill": "inner"}}
{"label": "frontmatter-post-skill", "tool_input": {"skill": "probeplug:inner"}}
{"label": "frontmatter-post-skill", "tool_input": {"skill": "inner"}}
```

Both placements see the exact same, unnormalized literal the model wrote into the Skill tool's `skill` parameter — the qualified call reads `"probeplug:inner"` in the hook input on both placements, and the bare call reads `"inner"` on both, never coerced to the other form. `tool_response.commandName` mirrors whichever form was passed, so it carries no more information than `tool_input.skill` itself. The skill name is therefore reliably available to a `PostToolUse` `Skill` hook, in exactly the two forms U4 names, from either placement — this is the fact `hook.py`'s `post-skill` mode is built against: it accepts both `kein:<stage>` and bare `<stage>`, matching the literal string a real Skill-tool call carries under either spelling, rather than falling back to the lead-runs-`enter` path.

**Also recorded, not required by any path — the `hooks.json` `PostToolUse` `Bash` handler.** Fired once, matching `echo probe-bash-done` verbatim in `tool_input.command`, confirming the `hooks.json` placement functions for a plain non-Skill matcher too, as a sanity check on the plugin's `hooks.json` loading at all.

**Not measured — frontmatter hooks on a subagent's tool calls.** The probe never dispatched a subagent (`probeplug:inner` is a plain skill invocation, not an `Agent` dispatch), so this fact from U4's list is left unmeasured here, as the plan itself says no decided path depends on it.

## Cross-check against the shipped binary

A parallel read of the installed `claude` CLI's own bundled schemas (not documentation — the binary's own Zod definitions, extracted via `grep` over the compiled JS) independently confirms every shape used above before this probe ran: `PostToolUse` for a Skill-tool call carries `tool_input = {skill, args?}`, `"Skill"` is an ordinary registered tool name with no exclusion from `PostToolUse` matching, a frontmatter `hooks:` block is documented in-schema as "Hooks registered while this skill is active" (consistent with (a) holding inside a process and the established fact that it does not survive a new one), and `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_CONFIG_DIR}` are the path placeholders substituted per-element into a hook command. The binary's own schema comments do not state whether frontmatter hooks survive `claude -c`; that half is settled only by the measurement above and by the 2026-09-19 probe this one repeats the shape of.

## Risk: `post-skill` accepts the bare stage name too

`hook.py`'s `post-skill` mode maps both `kein:interview`/`kein:ralplan`/`kein:execute` and the bare `interview`/`ralplan`/`execute` to a stage, because the measurement above shows a real Skill-tool call can carry either form verbatim, with no normalization the hook can rely on. This means a different plugin's skill, or a user's own project skill, literally named `interview`, `ralplan`, or `execute` and invoked by its bare name would also be read by this hook as a stage transition. What the probe actually measured for the bare form was a *directed* call: the probe body explicitly instructed the model to invoke the Skill tool a second time "with the skill parameter set to the exact literal string `inner`", and the log shows that instruction produces `"tool_input": {"skill": "inner"}` verbatim, unnormalized, on both placements. That proves the mechanism — a bare Skill-tool call is not coerced to the qualified form before a hook sees it — but it does not show a model spontaneously dropping the `kein:` prefix on its own initiative in ordinary use; no such unprompted case was observed. The bare form is kept anyway, for two reasons that do not depend on how often it occurs in practice: first, since the mechanism proves a bare call is a real, valid way to invoke a stage skill (nothing rules it out or normalizes it away), rejecting it would risk a missed real transition on the strength of an assumption about how often it happens, which was not measured; second, the blast radius of a false match from an unrelated same-named skill is small and bounded, not a silent state-machine corruption. `enter()` is idempotent; its only effect is to set that one stage's `status` to `entered`, and, for `execute` alone, to pin a nonterminal occupant of the worktree's own per-worktree claim as the stage's kept link — but only once that occupant has already passed the identical strict belonging test `attach` and `post-bash` apply. It never fabricates a completed run, and it links nothing at all for `interview` or `ralplan`. `gap()` and every other reader read only that kept link — `stages.<stage>.run`, written solely by `attach`, `post-bash`, or this one case in `enter` — and treat a stage with no kept link exactly as unresolved, allowing by default; there is no separate "resolved" association left to confuse with a genuine kept link. A stray `enter` from an unrelated same-named skill therefore cannot manufacture a false "stage complete" signal on its own: for `interview` and `ralplan` it does nothing beyond marking the stage entered, and for `execute` it can only pin an occupant that already independently passes the strict test, the same test a confirmed real transition would also have to pass — at worst it marks a stage entered slightly early, which costs one missed or mistimed nudge, the same low severity `post-skill`'s "never blocks" design already accepts elsewhere. Both forms stay accepted on that basis.

## Which placement holds, and why

**Frontmatter.** (a) and (c) both hold, so U4's Gate G1 "If (a) or (c) fails" branch is not taken and the flow does not fall back to `hooks.json`. (b) also holds — the binding addition even establishes it holds *stronger* than U4's own alternate-path text worried about ("if only (b) fails"): the exact skill string is available on the frontmatter `PostToolUse` `Skill` hook in both the qualified and bare forms, verbatim, so `hook.py`'s `post-skill` mode is built to accept both directly from `tool_input.skill` rather than requiring the lead to run `ocs state fsd enter <stage>` unconditionally before every stage invocation. This matches Decision 1 in `fsd.md` (one session, hooks in `fsd`'s own frontmatter) and needs no revision from this gate. `claude plugin validate probe-plugin --strict` passing (`✔ Validation passed`) is evidence that this exact `hooks:` shape is one `claude plugin validate --strict` accepts, not yet the plugin-wide check U4 asks this gate to also produce: `claude plugin validate plugin --strict` against this repository's own `plugin/` is unaffected either way right now, since `plugin/skills/fsd/SKILL.md` does not exist yet (U5's file), and that check must be re-run once U5 writes it with this frontmatter block in place.

No result here falls into G1's "Unexpected result" branch: frontmatter hooks did fire after invocation, consistent with the 2026-09-19 probe, and `--strict` accepted the plugin. U4 and `hook.py` proceed on the frontmatter placement.

## `post-bash`'s own measurement — a frontmatter `PostToolUse` `Bash` hook, probed 2026-09-19

`post-bash` is built on one further claim: a frontmatter `PostToolUse` hook with matcher `Bash` receives the exact command text a Bash tool call ran, as `tool_input.command`, and that command's own captured stdout, as `tool_response.stdout` — the two fields `post-bash` reads to find and confirm a stage's run. This was probed the same way as the rest of this file: a throwaway plugin declared a frontmatter `PostToolUse` hook, matcher `Bash`, pointed at a logging script, and the model was directed to run exactly one Bash command, `echo /tmp/fake-run/state.json`, and nothing else. `claude --version` was `2.1.278 (Claude Code)` for this run.

The hook fired once, and its own logged input carried exactly these fields (session id and every path stripped out below; nothing else was trimmed):

```json
{
  "hook_event_name": "PostToolUse",
  "tool_name": "Bash",
  "tool_input": {"command": "echo /tmp/fake-run/state.json", "description": "Print a file path"},
  "tool_response": {"stdout": "/tmp/fake-run/state.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
}
```

`tool_input.command` is the literal shell text the model ran, unexpanded and unquoted-by-the-hook — exactly the string `post-bash` tokenizes to find a watched command. `tool_response.stdout` is that command's own real captured stdout, with the trailing newline `echo` itself writes already stripped, which is what lets `post-bash` read a `start` call's own printed state.json path straight off it without any further trimming of its own. Both fields land on the same top-level shape every other frontmatter hook in this file already uses — `hook_event_name`, `tool_name`, `tool_input`, alongside `tool_response` — so `post-bash` needs no handling beyond what `mode_stop`/`mode_pre_write`/`mode_post_skill` already establish for reading a frontmatter hook's own JSON stdin.
