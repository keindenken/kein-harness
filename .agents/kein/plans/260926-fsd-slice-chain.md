# fsd slice chain: `ocs state fsd continue`, chained states, and a shorter Stop-hook reason

Status: Approved — architect and critic (round 2, 2026-09-26)

## Source and scope

Requirements: `.agents/kein/requirements/260926-fsd-slice-chain.md` (Approved), including the later-added Stop-hook reason item.

Classification: a feature (the chain) plus one bounded correction (the Stop-hook no-gap reason). It adds one CLI subcommand, two optional state fields, chain-aware output to `gap`/`status`/`report`, one hook reason rewrite, oracle sections, and reference prose.

Outcome: one `/fsd` invocation can run `interview → ralplan 1 → execute 1 → ralplan 2 → execute 2 → … → closeout`, each `ralplan → execute` pair held in its own fsd state and linked to its predecessor, with one retrospective and one report written by the last state's closeout.

Non-goals, all from the requirements: a live chained run (deferred and recorded in `docs/skills/fsd/open.md` by U6), a slice count or cap, a gate on the final `close` requiring every criterion covered, numbering criteria in the interview template, a prose rule on when to split.

Where the work happens: a separate git worktree on its own branch. Every path in this plan is relative to the repository root. The main checkout's `plugin/` runs the hooks of live fsd sessions through `~/.claude/skills/kein`; worktree edits do not reach them before merge, so task order is not constrained by the running flow. Merging replaces the code under any fsd run still live on main, which is why backward compatibility (below) is a hard constraint of every task.

Throughout, "verified" means read in this repository at d92ba33.

## Repository facts this plan stands on

- `plugin/skills/fsd/scripts/state.py` `validate_state` requires `set(payload) == FSD_FIELDS` exactly (15 keys) and `schema_version == 1`; `validate_transition` refuses any change to `schema_version`, `workflow`, `run_id`, `worktree`, `entry`, `input`. (verified)
- `plugin/skills/execute/scripts/state.py` already carries the precedent for growing a schema without moving its version: `*_OPTIONAL` frozensets checked as `REQUIRED <= keys <= REQUIRED | OPTIONAL`, "so a state written before either existed still validates", with a `_field_set_error(label, actual, expected, optional)` that reports optional keys. (verified, lines 60–122 and 952–978)
- `start` refuses while `_find_nonterminal_fsd_run(run_root, worktree)` finds another nonterminal state; `hook.py` `_find_active_state_path` resolves the flow's state with that same function over `<state-dir>/runs/fsd`, first nonterminal match in sorted order. (verified)
- A state whose `entry` is `ralplan` and whose `input.kind` is `requirements` already drives the whole machinery from its own `input.reference`: `_expected_ralplan_reference` returns it, `_expected_ralplan_field` compares ralplan candidates' `input.reference`, and `_expected_execute_plan_reference` then reads the linked ralplan's `resolved_reference`. (verified)
- `gap`'s entry row is `invoke /kein:{entry} {shlex.quote(target)}` while the entry stage is `pending`; `status` is the stage table merged with `gap()`; `report` prints `## Halted` (halted only), `## Assumptions`, `## Parked questions`, `## Lesson proposals`, `## Retrospective`, and `check-fsd-state` scenario1 asserts exactly four `None.` on a fresh run. (verified)
- `_mint_id` numbers from the maximum id already in the list it is given; `_retro_missing_ids` and `report` read only the state's own `assumptions`, `questions`, `lessons`. (verified)
- `close`'s pause outcome sets `retrospective` to the draft path it was handed, and `resume` copies the state without touching `retrospective`, so a slice that paused and resumed carries a non-null `retrospective` while active. (verified, `close` and `resume`)
- `hook.py` `_gap_action` replaces every literal `<state>` in `gap`'s action with the quoted state path before printing it, and `_block_stop` prefixes the printed reason with `fsd: `. (verified)
- `classify_input` joins a relative input onto the canonical worktree root with a plain `Path` join and no `.resolve()`, and stores that joined path as `input.reference`. (verified)
- `close` shows the house pattern for a two-part write: do the reversible side effect (moving the retrospective), commit, and undo the side effect if the commit is refused. (verified, `close` lines 1432–1448)
- `_execute.mint_run_dir(run_root, slug)` names `<run-root>/<YYMMDD-HHMMSS>-<slug>` without checking existence; `_run_slug` recovers the slug from a run id; `_durable_retro_path` names `retros/<today>-<slug>.md` from the state's own run id. (verified)
- `plugin/skills/interview/scripts/validate_artifacts.py` `_section_body(text, heading)` returns a heading's body up to the next `#`/`##`/`###` heading; fsd already imports that module as `_interview_validate`. The requirements template writes criteria as `- [ ] <criterion>` under `## Acceptance criteria`. (verified)
- `ralplan start` does not refuse an existing plan file, so a later slice's ralplan pointed at an earlier slice's plan path would overwrite a document an execute receipt already hashed. (verified, `ralplan/scripts/state.py` `start`)
- `hook.py` `_active_no_gap_reason` builds today's long reason (next_action, diagnosis, pause/end procedure); `check-fsd-hooks` pins it exactly through `_expected_active_no_gap_closing` / `_expected_active_no_gap_reason` and by substrings in sections `execute-blocked-parked`, `postskill-ralplan-forms`, `live-running-stages`, `closeout-path-end-to-end`, `active-no-gap-block`. (verified)
- Both oracles take `--list` and `--only <name>[,<name>...]` and register sections in a `SECTIONS` list; they do not import each other and keep fixture helpers local. `check-fsd-state`'s `write_requirements` writes `- item` under every heading, so no existing fixture has checkbox criteria. (verified)
- Runtimes: `check-fsd-hooks` full run measured at 36 s; `check-fsd-state` full run is about a minute or more; `check-execute-state` about four and a half minutes; `check-ralplan-state` unmeasured. `.agents/kein/runs/` is gitignored, so a fresh worktree has no live run state. (measured / verified)

## Principles

1. A state written by the current schema validates, reads and prints exactly as before: every addition is an optional key, and every new output appears only on a state that carries one.
2. The per-state machinery (attach, belonging tests, hooks, park, close) is reused unchanged; the chain lives in the link between whole states.
3. One writer per new fact: `chain` is written only when `continue` creates a state, `continued` only by `continue` closing one, and `checkpoint` cannot forge either.
4. Refuse before writing: `continue` validates both states it will write before touching disk, and a failure part-way leaves slice k exactly as it was found.

## Decision drivers

1. Backward compatibility with current-schema state files, including runs live on main at merge.
2. Atomicity of `continue`: never two nonterminal fsd states for a worktree, never zero between slices.
3. Oracle-falsifiable behavior with the fewest new code paths through existing readers.

## Decisions on the requirements' decision boundaries

Each is settled here; U1–U6 build on these names and none is reopened in a task.

- **D1 — Criterion identity: order.** Criteria are the `- [ ]` / `- [x]` lines in the requirements' `## Acceptance criteria` body (read with `_interview_validate._section_body`, which stops at the next heading, so `## Deferred items` is never read), numbered `AC1`, `AC2`, … in document order. Why: the template has no ids and numbering them is out of scope; order is the only identity the document already carries, and `AC` cannot collide with the retrospective's `\bA<n>\b` id match. A requirements document with no checkbox criteria has no `AC` ids, so every `--covered` names a nonexistent criterion and is refused (the requirements' accepted risk).
- **D2 — No schema version move; two optional fields.** `SCHEMA_VERSION` stays 1 and `FSD_OPTIONAL = {"chain", "continued"}` joins `FSD_FIELDS` the way execute's `*_OPTIONAL` sets do. Why: `validate_transition` refuses a `schema_version` change, so a version-2 design could not continue a slice written as version 1 (every slice 1, and every run live at merge); the optional-set precedent keeps current files valid with no migration.
- **D3 — Where each fact lives.** The next state carries its predecessor link; the closed state carries what it covered and why it continued:

  ```json
  "chain":     {"previous": "<absolute path of slice k's state.json>", "slice": 2},
  "continued": {"covered": ["AC1", "AC3"], "reason": "<why these criteria are left to the next slice>", "next": "<absolute path of slice k+1's state.json>"}
  ```

  Rules: `chain` exact field set; `previous` a non-empty absolute path; `slice` an integer (not a bool) of at least 2; a state with `chain` has `entry` `ralplan`, `input.kind` `requirements` and `stages.interview.status` `skipped`. `continued` exact field set; `covered` a non-empty list of distinct ids matching `^AC[1-9][0-9]*$`, in ascending number order; `reason` non-empty; `next` a non-empty absolute path; only on `lifecycle` `completed` with `retrospective` null. `continue` writes `retrospective: null` on the slice it closes: a slice that paused carries the draft path `close` stored, and on a mid-chain slice that path would read as the chain's retrospective, which only the last state's `close` writes; the draft file itself stays where it is, under the run's own directory. Transitions: `chain` never changes, appears or disappears; `continued` may appear only on an `active → completed` transition. `checkpoint` refuses a candidate whose `continued` differs from the stored one. Why: coverage is recorded once, at the end of the slice it describes, on the state it describes; a slice's successor is found from `continued.next`, its predecessor from `chain.previous`, with no forward write into an already-terminal state.
- **D4 — Mid-chain terminal lifecycle is `completed` with `continued`.** No new lifecycle. Why: `TERMINAL_LIFECYCLES`, `_find_nonterminal_fsd_run` and the hooks already treat `completed` as done, so nothing that finds "the flow's state" needs to learn a new value; `continued` plus a null `retrospective` distinguishes a mid-chain close from a final one.
- **D5 — Copy forward, not read through.** The next state starts with slice k's `assumptions`, `questions` and `lessons` copied verbatim. Why: `_mint_id` then continues numbering past every earlier id (uniqueness across the chain for free), and `_retro_missing_ids`, `report` and the append-only transition rules keep reading one state's own lists unchanged; read-through would add a chain walk to `assume`, `question`, `lesson`, `close` and `report`, each a new failure mode on an unreadable predecessor. `continue` refuses on an unanswered question, so copied questions are all answered.
- **D6 — CLI spelling: a subcommand of its own.** `ocs state fsd continue <state.json> --covered <AC ids, comma-separated> --reason <text>`; repeated ids in `--covered` are collapsed to one and stored in ascending number order; on success it prints the next state's absolute path, as `start` does. Why: `close` requires `--retro` and all three of its outcomes are about a retrospective, while continue takes none and has two required arguments of its own; every other lifecycle move (`halt`, `resume`, `abort`) is its own subcommand; a separate parser leaves `close`'s argparse and behavior byte-for-byte unchanged.
- **D7 — Handing the remaining criteria and earlier receipts to ralplan: `gap`'s entry-row action.** On a chained state whose `ralplan` is pending, the action is the ordinary `invoke /kein:ralplan <quoted requirements path>`, then `CHAIN_SUFFIX_SEPARATOR` (a newline, a module constant in `state.py`), then one suffix naming the slice number, each remaining criterion as `AC<n>` with its text, the instruction to write this slice's plan to a path of its own, and, for every earlier slice, its plan path, ralplan receipt path, execute receipt path and continue reason. `continue` sets the next state's `next_action` to that same text. Covered criteria are not named in the action. Criterion text and continue reasons reach the lead verbatim: `hook.py` `_gap_action` substitutes `<state>` only in the part of the action before the first `CHAIN_SUFFIX_SEPARATOR`, so a criterion that itself contains `<state>` is not rewritten; an action without the separator (every unchained row) is substituted exactly as before. Why: the lead invokes the stage `gap` names, the Stop and pre-write hooks already print `gap`'s action, and `ralplan`'s argument is free text, so the planner receives this without any change to ralplan; `ocs state ralplan start --input` stays the requirements path because the state's own `input.reference` is that path.
- **D8 — AGENTS.md drift check carried over from `close`.** `continue` also refuses when AGENTS.md's bytes no longer hash to the current span, with `close`'s own message. Why: the final `close` checks only the last state's span, so without this a slice could end with AGENTS.md changed and no check would ever see it; this keeps an existing invariant rather than adding a product rule. `close`'s guard check is not carried over: once row 5 has required a completed execute receipt, `guard_check` reads that receipt's absent `tasks` and is always clean (the accepted risk `docs/skills/fsd/open.md` already records), so the check would be dead code.
- **D9 — Slug and location.** The next state is minted with `_execute.mint_run_dir(<slice k's run root>, _run_slug(<slice k run_id>))`, so every slice shares slice 1's slug and run root. Because the slug is shared, a mint in the same wall-clock second as slice k's own directory names that directory; when the minted directory already exists, `continue` waits for the next second and mints once more, and refuses (row 13) only if that name exists too. The wait measures the second with the same clock `mint_run_dir` reads (the `datetime` in `_execute`'s module namespace), so one patched clock drives both the mint and the wait. Why: the hooks find the flow's state only under that run root, and the final `close` names the durable retrospective `retros/<today>-<slug>.md` after the chain's own name.
- **D10 — The Stop-hook rest procedure's home.** It moves to a new section `## Bringing the run to rest` in `plugin/skills/fsd/references/closeout.md`, and its presence is pinned by a docs-check section in `check-fsd-hooks` rather than in `check-fsd-state`. Why: the hooks oracle already knows the heading the reason names, so one section checks both the pointer and its target, and keeping it out of `check-fsd-state` keeps U4 disjoint from U1–U3.

## Interfaces fixed here

`continue` checks, in this order, and each refusal leaves the state file's bytes and the run root's listing exactly as they were. The oracle asserts each phrase as a substring (property), not the full message:

| # | Refused when | Message contains |
|---|---|---|
| 1 | lifecycle is not `active` | `continue requires an active run` |
| 2 | `--reason` empty after strip | `continue needs --reason` |
| 3 | no chain requirements path, or its `Status` is not `Approved` | `no approved requirements document` |
| 4 | a question is unanswered | `cannot continue while a question is unanswered` |
| 5 | the execute kept link is not a `completed` receipt | `not completed` (from `_execute_not_done_message`) |
| 6 | AGENTS.md drifted since the current span | `AGENTS.md changed since the current span began` |
| 7 | an earlier slice cannot be read | `earlier slice could not be read` |
| 8 | `--covered` names nothing | `names no acceptance criterion` |
| 9 | a named id is not a criterion of the requirements | `no such acceptance criterion` |
| 10 | every named id is already covered by an earlier slice | `adds no acceptance criterion not already covered` |
| 11 | nothing would remain | `no acceptance criterion would remain` |
| 12 | `_find_nonterminal_fsd_run(<slice k's run root>, <worktree>, exclude=<slice k's path>)` finds another nonterminal state | `a nonterminal fsd run already exists` (naming that state's path) |
| 13 | both minted destinations already exist (D9) | `already exists` |

The chain's requirements path: `input.reference` when `input.kind` is `requirements`; else, when `entry` is `interview`, `stages.interview.resolved_reference` or the completed ledger's `requirements_path` (the reading `gap`'s interview row already uses); else none (an execute-entry run, or a ralplan-entry run over a plan). `_chain_requirements_path` always returns an absolute path: a relative value is joined onto `state["worktree"]` with the plain join `classify_input` applies, and no further resolve. `continue` stores exactly that value as the next state's `input.reference`, which `_expected_ralplan_reference` then compares by resolved path.

`status` on a state with `chain` gains one key, and on any other state its key set is unchanged:

```json
"chain": {"slice": 2, "previous": "<path>", "requirements": "<path>", "covered_by_earlier_slices": ["AC1"],
          "remaining": [{"id": "AC2", "text": "<criterion text>"}, {"id": "AC3", "text": "<criterion text>"}],
          "earlier_slices": [{"slice": 1, "state": "<path>", "plan": "<path> | null", "ralplan": "<path> | null", "execute": "<path> | null", "covered": ["AC1"], "reason": "<text>"}]}
```

`status` carries the criteria text and earlier receipts because `gap` stops naming them once `ralplan` is entered, and `status` is what a lead reads after a compaction.

or `"chain": {"slice": 2, "previous": "<path>", "error": "<text>"}` when an earlier slice cannot be read.

`report` on a state with `chain` prints `## Slices` right after `## Halted` (when present) and before `## Assumptions`: one line per earlier slice in order (slice number, plan path, ralplan receipt path, execute receipt path, covered ids, continue reason), then one line for the state itself marked as the current slice (its plan, ralplan receipt, execute receipt, each or `none linked`). A state without `chain` prints no such section.

The Stop hook's no-gap reason: `_active_no_gap_reason` returns exactly this text, without a leading `fsd: `, and the printed `reason` field is `_block_stop`'s `fsd: ` followed by it. `quoted_state = shlex.quote(str(state_path))`; `closeout_md` is the resolved absolute path of `plugin/skills/fsd/references/closeout.md` computed from `hook.py`'s own location:

```python
f"this run ({quoted_state}) is active and {running_stage} is the stage running. "
f"If you are waiting on another lane, confirm it is still alive; ending this turn to wait for its notification is then fine. "
f"Otherwise keep {running_stage} moving: `ocs state fsd gap {quoted_state}` says why it is stuck. "
f"To pause or end the run instead, follow \"Bringing the run to rest\" in {closeout_md}."
```

## Order

| Story | Scope | After | Runs beside |
|---|---|---|---|
| U1 schema | `plugin/skills/fsd/scripts/state.py`, `dev/libexec/check-fsd-state` | U4 | — |
| U2 continue | same as U1 | U1 | — |
| U3 chained readers | same as U1 | U2 | — |
| U4 Stop reason | `plugin/skills/fsd/scripts/hook.py`, `dev/libexec/check-fsd-hooks`, `plugin/skills/fsd/references/closeout.md` | — | — |
| U5 chained hooks | `dev/libexec/check-fsd-hooks`, `plugin/skills/fsd/scripts/hook.py` (`_gap_action`, and the state lookup only through its gate) | U3 | — |
| U6 documentation | `plugin/skills/fsd/SKILL.md`, `plugin/skills/fsd/references/closeout.md`, `plugin/skills/fsd/references/state-schema.md`, `plugin/skills/fsd/references/decision-policy.md`, `docs/skills/fsd/open.md` | U5 | — |

The stories run one at a time, in the order U4, U1, U2, U3, U5, U6. Each story's verification executes files another story edits (`check-fsd-hooks` drives and imports `state.py`; U6 runs `check-fsd-hooks`), so no two stories run side by side. U4 goes first because its checks run against the `state.py` U1–U3 have not yet touched, and nothing U1–U3 verify with executes `hook.py` or `check-fsd-hooks`. No story has `AGENTS.md` or `CLAUDE.md` in scope. Each story commits after its own verification passes (`feat(fsd): …` or `test(fsd): …`), per `AGENTS.md`.

How each story keeps a current-schema state file behaving as before is stated inside it; the full existing suites at the end are the backstop.

## Stories

### U1 — chain fields in the fsd schema

Purpose: make `chain` and `continued` (D2, D3) valid, validated and unforgeable, with no behavior change for a state that carries neither.

Scope: `plugin/skills/fsd/scripts/state.py` (`FSD_OPTIONAL`, `_field_set_error`, `validate_state`, `validate_transition`, `checkpoint`), `dev/libexec/check-fsd-state` (new section `chain-schema`).

Required behavior: the D3 shapes and rules, and `_field_set_error` naming optional keys the way execute's does. Nothing else in the module reads the new keys yet.

Compatibility: the required set is unchanged and the new keys are optional, so a file with exactly `FSD_FIELDS` takes the same path through every check it took before.

Completion conditions, all in section `chain-schema`:

1. A hand-written current-schema state (exactly the 15 `FSD_FIELDS` keys, shaped like a live run's file: entry `ralplan`, input kind `requirements`, ralplan pending) passes `validate` (exit 0); its `status` key set is exactly `{lifecycle, entry, stages, gap, completed, next, action, diagnosis}` [exact]; its `gap` action equals `invoke /kein:ralplan <shlex.quote(requirements path)>` [exact]; its `report` has no `## Slices` [property].
2. A state from `start` (approved requirements) with `chain = {"previous": <absolute path>, "slice": 2}` written into the file validates (exit 0).
3. `validate` exits nonzero with stderr naming `chain` for each of: `chain` missing `slice`; `slice` 1; `slice` `true`; relative `previous`; `chain` on an execute-entry state. [property]
4. `validate` exits nonzero with stderr naming `continued` for each of: `continued` on an `active` state; on a completed state with a non-null `retrospective`; with empty `covered`; with `covered` holding `X1`; with a duplicate id. [property]
5. `validate` exits nonzero with stderr containing `unexpected` for an unknown top-level key such as `chains`. [property]
6. `checkpoint` refuses a candidate that moves an active state to `completed` with `continued` added (stderr contains `continued`), and a candidate that adds, changes or removes `chain` (stderr contains `Transition cannot change chain`); the state file's bytes are unchanged after each. [property, exact bytes]

Verification: `dev/kein-dev check-fsd-state --only chain-schema,scenario1-input-classification,scenario2-full-drive-lifecycle,scenario37-checkpoint-refuses-run-change,scenario38-checkpoint-refuses-added-span-not-paused-to-active,scenario41-checkpoint-refuses-new-destination-with-run` exits 0 and prints `ran …` (under a minute). A nonzero exit on any existing section means the optional-set change altered current-schema behavior: stop and fix U1 before U2. Optional extra evidence: `python3 plugin/skills/fsd/scripts/state.py validate <main checkout>/.agents/kein/runs/fsd/260926-214639-fsd-slice-chain/state.json` exits 0 when the main checkout is reachable.

### U2 — `ocs state fsd continue`

Purpose: end slice k and start slice k+1 in one command (D4–D6, D8, D9), with every requirements refusal and the failure rule.

Scope: `plugin/skills/fsd/scripts/state.py` (new helpers, `continue_chain`, a `continue` subparser beside `close`), `dev/libexec/check-fsd-state` (a local `write_requirements_with_criteria(path, status, criteria, deferred=())` helper, a slice-driving helper built from scenario2's ralplan and execute steps, sections `chain-continue`, `chain-continue-from-interview`, `chain-continue-after-pause`, `chain-refusals`, `chain-create-failure`).

Required behavior:

- Helpers, named so U3 reuses them: `_chain_requirements_path(state) -> Optional[Path]` (the reading in "Interfaces fixed here"); `_acceptance_criteria(path) -> List[Tuple[str, str]]` (D1); `_chain_predecessors(state) -> List[Tuple[Path, Dict]]` walking `chain.previous` from slice 1 to slice k-1 of the given state, raising `ValueError` on an unreadable or invalid predecessor, one without `continued`, a slice number that does not step by one, or a repeated path.
- `continue_chain(destination, covered, reason) -> Path` collapses repeated `--covered` ids, runs the table's checks in order, then builds both candidates in memory and runs `validate_transition(None, next)` and `validate_transition(current, closed)` before any write. Next state: fields as `start` builds for an approved-requirements input (entry `ralplan`, interview `skipped`, other stages `pending` with null links), `input = {"kind": "requirements", "reference": <chain requirements path>, "summary": <slice k's input.summary>}`, one fresh `agents_md` span over AGENTS.md's current bytes, slice k's `assumptions`/`questions`/`lessons` copied, `chain = {"previous": <slice k path, resolved>, "slice": <k's slice or 1, plus 1>}`, `next_action` `invoke /kein:ralplan <quoted path>` (U3 replaces this with D7's text). Closed state: `lifecycle` `completed`, `continued` as D3, `retrospective` null, `next_action` `continued in <next path>`, everything else unchanged.
- Write order: mint the destination with D9's one re-mint, refusing with row 13 when both names exist; `_commit` the next state (creating its directory); then `_commit` slice k; if that second commit raises, remove the next state's file and the directory `continue` created, then re-raise. If the first write fails, nothing was written.
- CLI: `continue` with positional `state`, required `--covered` (split like `--alternatives`), required `--reason`; prints the next state's path; refusals exit 1 through `main`'s existing handler. `close`'s parser is untouched.

Compatibility: no existing function changes behavior; a current-schema state is exactly what slice 1 is, and `continue` reads it without migrating it.

Completion conditions:

1. `chain-continue`: requirements with three checkbox criteria and a `## Deferred items` checkbox; slice 1 entered at `ralplan`, driven to a completed execute receipt with A1 and L1 recorded. `continue --covered AC1,AC1 --reason <R>` runs in process: a wrapper imports `plugin/skills/fsd/scripts/state.py` from `KEIN_ROOT`, replaces the `datetime` in its `_execute` module's namespace with a `datetime` subclass whose `now` returns a fixed time t0 on its first call and t0 plus one second on every later call, pre-creates `<run root>/<t0 as %y%m%d-%H%M%S>-<slug>`, sets `sys.argv`, and calls `main()`. It returns 0 and prints one absolute path under the same run root whose run id is `<t0 plus one second as %y%m%d-%H%M%S>-<slug>`, and the pre-created directory is left untouched and empty. Slice 1 afterwards: `lifecycle` `completed`, `retrospective` null, `continued` equals `{"covered": ["AC1"], "reason": R, "next": <printed path>}`, `next_action` equals `continued in <printed path>`, and every key other than `lifecycle`, `retrospective`, `continued` and `next_action` equals its value before the call. [exact]
2. The next state: `lifecycle` `active`, `entry` `ralplan`, `input` as above, `chain` equals `{"previous": <slice 1 path>, "slice": 2}`, stages as `start` builds for a ralplan entry, lists equal slice 1's, one span, `halt` and `retrospective` null; `validate` exits 0 on both files. [exact]
3. After continuing, `start` for the same worktree is refused with `a nonterminal fsd run already exists` naming the next state's path, `assume` on the next state prints `A2` and `lesson` prints `L2`. [property, exact ids]
4. `chain-continue-from-interview`: slice 1 starts from an idea, its interview ledger linked while active and completed onto approved checkbox requirements whose ledger `requirements_path` is relative to the worktree (the route scenario2 drives), then ralplan and execute driven to a completed execute receipt. `continue --covered AC1 --reason <R>` exits 0; the next state's `input.reference` is absolute and equals slice 1's `stages.interview.resolved_reference` [exact]; with that `resolved_reference` set to null in slice 1's file before a second, otherwise identical fixture's `continue`, the next state's `input.reference` equals the worktree root joined with the ledger's relative `requirements_path` [exact]; its `gap` action's part before the first newline equals `invoke /kein:ralplan ` followed by `shlex.quote(<that path>)` [exact].
5. `chain-continue-after-pause`: a slice driven to a completed execute receipt records a question; `continue` is refused with row 4's phrase and unchanged bytes; `closeout`, then `close` with a retrospective under the run's directory citing the question pauses the run with `retrospective` set; `answer`, `resume`, `closeout`; `continue --covered AC1 --reason <R>` then exits 0, the closed slice has `lifecycle` `completed`, `retrospective` null and `continued` as D3 [exact], the draft retrospective file still exists [property], and `validate` exits 0 on both states.
6. `chain-refusals`: each of rows 1–13 is triggered by a fixture where only that condition fails (row 12 by writing a second active state by hand into a new directory of the run root, a copy of slice 1's file with its own `run_id`, and removing it after the call; row 13 through condition 1's in-process wrapper with both the t0 and the t0-plus-one-second directories pre-created; row 1 on a paused state; row 2 with `--reason ' '`; row 3 on an execute-entry run whose execute completed; row 4 by recording a question, then answering it before the next row; row 5 before execute is started and again while it is active; row 6 by editing AGENTS.md and restoring its bytes afterwards; row 9 with `AC4` where the fourth checkbox is under `## Deferred items`, and with `X1`; row 10 on slice 2, driven to its own completed execute receipt, with `--covered AC1`; row 7 on that same slice 2 with slice 1's file moved away for the call and restored after it; row 11 with `--covered AC1,AC2,AC3`). For each: nonzero exit, stderr contains the table's phrase, the state file's bytes are identical before and after, and the run root's directory listing is identical. [property, exact bytes, exact listing]
7. `chain-create-failure`, injection A: the run root made read-only (mode 0o555) before `continue`; the call exits nonzero, slice 1's bytes are unchanged and its lifecycle is `active`, and no new directory exists. Injection B: slice 1's own run directory made read-only; the call exits nonzero, slice 1's bytes are unchanged, and the run root's listing equals its listing before the call (the next state was removed). After permissions are restored, the same `continue` succeeds. Before each injection the section proves it takes effect (creating a probe entry there raises `PermissionError`) and records a failure, never a skip, when it does not, since a root user would pass vacuously. [exact bytes, exact listing]

Verification: `dev/kein-dev check-fsd-state --only chain-schema,chain-continue,chain-continue-from-interview,chain-continue-after-pause,chain-refusals,chain-create-failure,scenario1-input-classification` exits 0 (one to two minutes; the chain sections drive real ralplan and execute runs). A refusal that changes bytes, or an injection that leaves a second nonterminal state, is a stop: fix U2 before U3.

### U3 — `gap`, `status`, `report` and the final `close` on a chained state

Purpose: make a chained state name the next ralplan with what remains (D7), show the chain in `status` and `report`, and prove the last state's `close` covers every slice's ids.

Scope: `plugin/skills/fsd/scripts/state.py` (`gap`'s entry row, `status`, `report`, `continue_chain`'s `next_action`), `dev/libexec/check-fsd-state` (sections `chain-gap-status`, `chain-final-close-report`).

Required behavior: a shared read of the chain built on U2's helpers (slice number, requirements path, criteria, ids covered by earlier slices, remaining ids, and per earlier slice its state path, plan path from `stages.ralplan.resolved_reference` or the ralplan receipt's `plan.path`, ralplan receipt path, execute receipt path, covered ids and reason). `gap`'s entry row on a state with `chain` appends D7's suffix; when the chain read raises, the row still fires with the ordinary prefix plus a clause containing `could not be read`. `status` adds the `chain` key from "Interfaces fixed here" (criteria text and earlier receipts included) only when the state has `chain`. `report` adds `## Slices` only when the state has `chain`, and tolerates a broken chain with a line containing `could not be read`. `continue_chain` sets the next state's `next_action` to D7's action for the next state, computed before either write: the chain read and the action builder take an optional in-memory override mapping slice k's resolved path to its closed candidate (the one carrying `continued`), so the walk from the next state reads slice k from memory rather than from a file that does not yet carry `continued`; `gap` itself keeps its one-argument signature and passes no override. U2's write order and rollback are unchanged. Every other `gap` row, and every output of a state without `chain`, is unchanged.

Compatibility: every addition is inside a branch taken only when `chain` is present.

Completion conditions:

1. `chain-gap-status`, slice 2 of a three-criterion chain where slice 1 covered AC1: `gap` returns `gap` true, `next` `ralplan`, `completed` and `diagnosis` null [exact]; the part of `action` before the first newline equals `invoke /kein:ralplan ` followed by `shlex.quote(<requirements path>)` [exact]; it contains `AC2` and `AC3` with each criterion's text, slice 1's plan path, ralplan receipt path, execute receipt path and continue reason, and the phrase `a path of its own` [property]; `\bAC1\b` does not match it and AC1's text is absent [property]; the state's `next_action` equals the action [exact].
2. Continuing slice 2 with `--covered AC2` makes slice 3's `gap` action name AC3 only (neither `\bAC1\b` nor `\bAC2\b` matches) and both earlier slices' receipt paths and reasons. [property]
3. `status` on slice 2 has `chain` equal to the "Interfaces fixed here" shape with `slice` 2, slice 1's path, the requirements path, `covered_by_earlier_slices` `["AC1"]`, `remaining` AC2 and AC3 with their criterion text, and one `earlier_slices` entry carrying slice 1's plan, ralplan receipt, execute receipt, `["AC1"]` and its reason [exact]; the same `status` after `enter ralplan` still carries that `chain` [exact]; `status` on slice 1 before continuing has no `chain` key [exact key set].
4. With slice 1's state file moved away, `gap`, `status` and `report` on slice 2 each exit 0; `gap` still fires the ralplan row, its part before the first newline equal to the ordinary prefix, and contains `could not be read`; `status.chain` has an `error` key; `report` contains `could not be read` under `## Slices`. [property]
5. `chain-final-close-report`: slice 2 is driven to a completed execute receipt with A2 recorded; a retrospective citing A2 and L1 but not A1 makes `close` exit nonzero with stderr containing `missing A1` [property]; a retrospective citing A1, A2 and L1 completes the run and moves it to `.agents/kein/retros/<today>-<slice 1's slug>.md` [exact path].
6. `report` on the completed slice 2 contains `## Slices` before `## Assumptions`, one line for slice 1 with its plan path, execute receipt path and reason, and one current-slice line with slice 2's plan path and execute receipt path; it also contains A1, A2 and L1 [property]. `report` on an unchained state contains no `## Slices` [property].

Verification: `dev/kein-dev check-fsd-state --only chain-continue,chain-gap-status,chain-final-close-report,scenario1-input-classification,scenario2-full-drive-lifecycle,gap` exits 0 (about a minute). A change in any existing section's output is a stop: the branch leaked into the unchained path.

### U4 — a shorter Stop-hook reason and the rest procedure in closeout.md

Purpose: the requirements' Stop-hook item. The no-gap block says only the run and its running stage, the lane allowance, `ocs state fsd gap <state>`, and where the rest procedure lives; that procedure moves intact to `closeout.md`.

Scope: `plugin/skills/fsd/scripts/hook.py` (`_active_no_gap_reason` and its call in `mode_stop`, their docstring and comments), `dev/libexec/check-fsd-hooks` (the expected-reason helpers, the assertions in `execute-blocked-parked`, `postskill-ralplan-forms`, `live-running-stages`, `closeout-path-end-to-end`, `active-no-gap-block`, the closing summary print, and a new section `rest-procedure-in-closeout`), `plugin/skills/fsd/references/closeout.md` (new section `## Bringing the run to rest`).

Required behavior: `_active_no_gap_reason` returns the text fixed in "Interfaces fixed here" and no longer reads `next_action` or `gap()`'s diagnosis; `mode_stop`'s other paths are unchanged. The new closeout.md section carries what the reason carries today, as steps: pausing (`ocs state fsd question <state> --stage <running stage> --question <text> --recommended <text> --why-irreversible <text> --parks 'whole run'`, unless a question parking the whole run is already unanswered) or ending outright (skip the question); then, either way, `ocs state fsd closeout <state>` unless closeout is already the running stage, and `ocs state fsd close <state> --retro <path>` with the retrospective under this run's own directory citing every assumption, question and lesson id; if close refuses, `ocs state fsd halt <state> --reason <close's refusal>`; if halt answers that close would succeed, fix what close named and close again; ending changes only this run's state, a stage run still live underneath stays active and keeps occupying the worktree, so prefer pausing while one is live.

Compatibility: no state is read differently; only the text of one block reason changes, which is the requirement.

Completion conditions:

1. With the running stage `execute` (`active-no-gap-block`, repository path containing a space) and `closeout` (`closeout-path-end-to-end`), the printed `reason` field equals `fsd: ` followed by the fixed text exactly, `closeout_md` computed in the oracle as `(ROOT / "skills" / "fsd" / "references" / "closeout.md").resolve()`. [exact]
2. In those sections and in `live-running-stages` (ralplan and execute): the reason contains `ocs ` exactly once, as `ocs state fsd gap <quoted state>`; it contains neither the fixture's `next_action` nor `no run linked yet`. [property]
3. `execute-blocked-parked` and `postskill-ralplan-forms` assert the running-stage sentence for their stage instead of `next_action`; the close/halt walks in `active-no-gap-block` are unchanged and pass. [property]
4. `rest-procedure-in-closeout`: `plugin/skills/fsd/references/closeout.md` has the line `## Bringing the run to rest` [exact], and that section's body contains `ocs state fsd question`, `--stage`, `--why-irreversible`, `--parks 'whole run'`, `already unanswered`, `ocs state fsd closeout`, `ocs state fsd close <state> --retro`, `under this run's own directory`, `every assumption, question, and lesson id`, `ocs state fsd halt`, `close would succeed`, and `stays active`. [property]
5. `grep -nE "last recorded intent|Do not end this turn here|two exits that" plugin/skills/fsd/scripts/hook.py dev/libexec/check-fsd-hooks` prints nothing. [exact: empty]

Verification: `dev/kein-dev check-fsd-hooks --only execute-blocked-parked,postskill-ralplan-forms,live-running-stages,closeout-path-end-to-end,active-no-gap-block,rest-procedure-in-closeout` exits 0 (about 15 s), then the grep in condition 5.

### U5 — the hooks on a chained state

Purpose: prove the requirement that the hooks work on slice k+1 as on any other state.

Scope: `dev/libexec/check-fsd-hooks` (a local checkbox-requirements helper and section `chain-hooks`); `plugin/skills/fsd/scripts/hook.py` (`_gap_action` substituting `<state>` only before the first `fsd_module.CHAIN_SUFFIX_SEPARATOR`, per D7, with its docstring; the state lookup only through the gate below).

**Gate — hook.py's state lookup needs no change for a chained state.**

- Claim: with slice k `completed` and slice k+1 `active` under the same run root, `_find_active_state_path` returns slice k+1, and `post-skill` / `post-bash` enter and link on it through the unchanged belonging tests, because slice k+1's own `input.reference` is the requirements path.
- Evidence method: `chain-hooks` run against `hook.py` as U4 left it, opening with a discriminating probe before any hook call: slice k's `lifecycle` is `completed`, and `ocs state fsd start` for the worktree is refused with a message naming slice k+1's path.
- Alternate path: only when the probe names slice k+1 and a block, entry or link still lands on slice k or is missing, the fix is confined to `hook.py`'s state lookup (`_find_active_state_path`), then `chain-hooks` and U4's section list run again.
- Unexpected result: a probe that names slice k, or finds slice k not `completed`, puts the cause in `state.py`; the story stops and is reported against U2. Any other failure whose cause is in `state.py` (a belonging test or `gap`) stops it too, reported against U2 or U3 rather than patched from here.

Completion conditions, all in `chain-hooks` (slice 1 linked through `post-bash` from real `ralplan start` and `execute start` stdout, driven to a completed execute receipt, then `continue`):

1. Stop blocks on slice 2 with a reason containing `invoke /kein:ralplan`, `shlex.quote(<requirements path>)` and each remaining id; pre-write denies `Write` with the same three substrings. [property]
2. One remaining criterion's text contains a literal `<state>`; the Stop reason and the pre-write reason each contain that criterion's text verbatim, `<state>` included [exact substring]. `closeout-path-end-to-end` and `execute-blocked-parked` still pass, proving an unchained closeout action is still substituted.
3. `post-skill` for `kein:ralplan` marks slice 2's `ralplan` `entered`, and slice 1's file bytes are unchanged. [exact]
4. `post-bash` fed a real `ocs state ralplan start --input <requirements path> --plan <slice 2 plan>` command and its real stdout sets slice 2's `stages.ralplan.run` to that run's path. [exact]
5. With that ralplan run completed, Stop blocks naming `invoke /kein:execute` and slice 2's plan path; `post-bash` fed a real `ocs state execute start --input <slice 2 plan>` and its stdout sets slice 2's `stages.execute.run`. [property, exact]
6. With execute running and linked, Stop blocks with `fsd: ` followed by U4's fixed text for slice 2's own state path. [exact]
7. Slice 1's file bytes are unchanged from just after `continue` to the end of the section. [exact bytes]

Verification: `dev/kein-dev check-fsd-hooks --only chain-hooks,closeout-path-end-to-end,execute-blocked-parked` exits 0 (about 20 s); if the gate's alternate path edited the state lookup, also U4's `--only` list.

### U6 — the chain in the skill and its references

Purpose: the requirements' documentation item, plus the deferred live-run record.

Scope: `plugin/skills/fsd/SKILL.md`, `plugin/skills/fsd/references/closeout.md`, `plugin/skills/fsd/references/state-schema.md`, `plugin/skills/fsd/references/decision-policy.md`, `docs/skills/fsd/open.md`.

Required behavior:

- `SKILL.md`: one conditional line under "Between stages": when `execute` completes and acceptance criteria remain that this slice could not take, because their plan needed what this slice revealed or because decision-policy's split route removed their story from this slice's plan, closeout's continue branch starts the next slice instead of ending the run, and the next slice's state is the path `continue` prints.
- `closeout.md`: a continue branch under "After `execute` ends", after step 1, taken instead of steps 2–5 when acceptance criteria remain that this slice could not take, for either reason in the `SKILL.md` line: `ocs state fsd continue <state> --covered <AC ids> --reason <what the next slice needs that could not be planned before, or which split story it carries and why it was split>`; `AC<n>` is the n-th checkbox of the requirements' `## Acceptance criteria`; use the printed path from then on and invoke the stage its `gap` names exactly as printed; give that slice's plan a path of its own; when `continue` refuses on an unanswered question, `close` as below (the run pauses, and the chain continues after the answer and `resume`). Step 3's retrospective gains a **Slices** bullet: every slice's plan, receipts and continue reason, from `report`'s `## Slices`. The U4 section stays as U4 left it.
- `state-schema.md`: the schema block shows the optional `chain` and `continued`; the command list gains `ocs state fsd continue <state.json> --covered <AC ids> --reason <text>`; a section on chained slices covers D1–D9, the refusal table, the write order and its rollback, the `status` `chain` key and the `report` `## Slices` section; the `## report` paragraph names `## Slices`.
- `decision-policy.md`: the sentence "The split story goes back through its own requirements-and-plan pass after this run rather than holding the settled ones behind it." becomes: the split story's criteria stay uncovered by this slice, so closeout's continue branch carries them into the next slice's `ralplan` rather than a separate pass after the run.
- `docs/skills/fsd/open.md`: an entry for the deferred live chained run: what the next real use should measure (whether the lead continues rather than closes when criteria remain, whether ralplan's planner uses the remaining criteria and earlier receipts from `gap`'s action, whether a later slice's plan kept a path of its own, whether ralplan's review lanes approve a slice plan that deliberately covers only part of the acceptance criteria (slice 1's action carries no remaining-criteria suffix to say so), and whether the lead passes `gap`'s multi-line action as the whole `/kein:ralplan` argument rather than its first line, and which `--input` value it then gives `ocs state ralplan start`).
- All prose: English, one line per sentence or paragraph, no model names.

Completion conditions:

1. `grep -c "ocs state fsd continue" plugin/skills/fsd/SKILL.md` prints 1, and `grep -n "state fsd continue" plugin/skills/fsd/references/closeout.md plugin/skills/fsd/references/state-schema.md` finds each file. [exact count, property]
2. `grep -n "after this run rather than holding the settled ones" plugin/skills/fsd/references/decision-policy.md` prints nothing, and `grep -n "next slice" plugin/skills/fsd/references/decision-policy.md` finds the replacement. [property]
3. `grep -nE '"chain"|"continued"' plugin/skills/fsd/references/state-schema.md` finds the schema block, and `grep -n "## Slices" plugin/skills/fsd/references/state-schema.md` finds the report description. [property]
4. `grep -n "chained run" docs/skills/fsd/open.md` finds the deferred entry. [property]
5. `git diff -U0 -- plugin/skills/fsd docs/skills/fsd | grep '^+' | grep -niE 'opus|sonnet|haiku|fable|gpt-'` prints nothing. [exact: empty]
6. `dev/kein-dev check-fsd-hooks --only rest-procedure-in-closeout` still exits 0.

Verification: the commands in conditions 1–6, then `claude plugin validate plugin --strict` exits 0.

## Final verification

After U1–U6, in this order, each waited on to completion (none may be treated as passed while still running in the background):

1. `dev/kein-dev check-fsd-state` — full, about a minute or more with the new sections.
2. `dev/kein-dev check-fsd-hooks` — full, about 40 s.
3. `dev/kein-dev check-ralplan-state` — full, runtime unmeasured.
4. `dev/kein-dev check-execute-state` — full, about four and a half minutes; give it a timeout of at least ten minutes.
5. `claude plugin validate plugin --strict`.

Each exits 0. These are the acceptance criterion "a state file written by the current schema behaves as before" in its broad form: every existing section builds its states with the unchanged `start` and exercises the unchained path.

## Risks

- **A later slice's plan written over an earlier slice's plan.** `ralplan start` does not refuse an existing plan path. Mitigation: D7's action and closeout's continue branch both tell the lead to give each slice's plan a path of its own; the earlier plan path is in the action, so a collision is visible. Residual: nothing refuses it mechanically.
- **Coverage is the lead's claim.** The progress guard (row 10) catches a slice claiming nothing new, not a false claim. Accepted by the requirements.
- **Requirements edited mid-chain.** Criteria are identified by order, so inserting a checkbox above a covered one shifts ids. The document is Approved and the chain treats it as fixed; nothing detects an edit. Accepted; the live-run entry in `open.md` names it as something to watch.
- **Rollback itself failing.** If removing the next state after a failed commit of slice k also fails, two nonterminal states exist; the raised error names the orphan path so it can be aborted by hand. Accepted.

## Pre-mortem

- **S1: A current-schema state stops validating, or prints differently, after merge.** Caught by: U1 condition 1, U3 condition 6, and the full `check-fsd-state` / `check-fsd-hooks` runs · Prevented by: D2's optional-key check and output additions gated on `chain` · Acts on: `validate_state` reads the payload's key set against `FSD_FIELDS` and `FSD_FIELDS | FSD_OPTIONAL`; `gap`/`status`/`report` test `"chain" in state` before adding anything · Residual: None
- **S2: `continue` half-applies, leaving two nonterminal states or none.** Caught by: U2 condition 7 (both injections) · Prevented by: validating both candidates before writing, writing slice k+1 first, and removing it when slice k's commit fails · Acts on: removes the `state.json` and run directory `continue` itself minted, resolved from the destination it computed in the same call · Residual: a rollback that itself fails leaves an orphan the error names
- **S3: The rest procedure loses a branch on its way from the hook into `closeout.md`, and a lead that must pause or end has nowhere complete to read it.** Caught by: U4 condition 4 · Prevented by: U4 moving the procedure as steps carrying every clause the reason had · Acts on: the oracle reads `plugin/skills/fsd/references/closeout.md` from `KEIN_ROOT` and checks the section the reason names · Residual: wording drift inside a clause the phrase list does not pin

## ADR

- Decision: chain whole fsd states through `ocs state fsd continue`, with `chain` on the new state, `continued` on the closed one, criteria identified by order as `AC<n>`, earlier A/Q/L copied forward, and remaining criteria and earlier receipts handed to ralplan through `gap`'s entry-row action; shorten the Stop-hook no-gap reason and move its procedure to `closeout.md`.
- Drivers: backward compatibility of current-schema state files; atomic slice handover; reuse of the per-state machinery unchanged.
- Alternatives considered: a schema version 2 (refused by `validate_transition` for any slice written as version 1); a new `continued` lifecycle (every reader of terminal lifecycles would need to learn it); reading A/Q/L through the link (a chain walk in five commands); `close --continue` (changes `close`'s required arguments and folds a no-retrospective outcome into a retrospective command); a separate field or file for ralplan's input (ralplan would need to read it, where `gap`'s action already reaches the lead and the hooks).
- Why chosen: each choice reuses a mechanism the code already has (optional-set validation, `completed` as terminal, `_mint_id`, `gap` as the one source of the next action, `close`'s undo-on-refusal write) instead of adding a reader.
- Consequences: a mid-chain state is `completed` with no retrospective; the final report and retrospective carry every slice through `## Slices` and the copied lists; the Stop reason no longer prints `next_action` or the diagnosis, which `gap` still does.
- Follow-ups: the live chained run in `docs/skills/fsd/open.md`.

## Open Questions

- None.
