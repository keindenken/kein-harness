#!/usr/bin/env python3
"""fsd's stage-transition hooks -- modes `stop`, `pre-write`, `post-skill`, `post-bash` -- for the placement Gate G1 selected (`docs/skills/fsd/260919-hook-probe.md`): declared in `fsd`'s own SKILL.md frontmatter, not in `plugin/hooks/hooks.json`. The probe found frontmatter Stop and PreToolUse still fire after the model invokes a nested, model-invocable skill, and that a frontmatter `PostToolUse` `Skill` hook's input reliably carries the exact `skill` string the model wrote -- verbatim, in both the qualified (`kein:<stage>`) and bare (`<stage>`) forms it can take -- so `post-skill` below reads that field directly rather than requiring the lead to run `ocs state fsd enter <stage>` unconditionally. A probe on 2026-09-19 further confirmed a frontmatter `PostToolUse` `Bash` hook receives `tool_input.command` (the exact shell text run) and `tool_response.stdout` (its captured stdout), which is what `post-bash` reads below.

Every mode allows by default and only ever acts on positive evidence. `stop` and `pre-write` act on `fsd`'s own `gap()`, imported here read-only exactly as `fsd/scripts/state.py` itself imports `execute`'s and `ralplan`'s internals -- nothing here re-derives what counts as a gap. `post-skill` and `post-bash` act on `fsd`'s own `enter`/`attach`, imported the same way -- nothing here re-derives what counts as a stage entry or a belonging association. Every path exits 0: `stop` blocks by printing `{"decision": "block", "reason": ...}`, `pre-write` denies by printing `hookSpecificOutput.permissionDecision: "deny"`, and every other outcome -- allow, an off-switch, no run, a corrupt or unreadable state, any exception -- is silent success. A block or deny reason that names `ocs state fsd closeout <state>` has `<state>` substituted with the resolved state.json path before it is printed, so the reason is a command the lead can run as-is rather than a template.

`post-bash` is what records a stage's association the moment its run is created, instead of `fsd`'s own state machine inferring it afterward from a directory listing or a worktree claim (see `state.py`'s "Stage association" section comment). It watches every Bash call for three commands: `ocs state ralplan start ...` and `ocs state execute start ...`, whose own stdout on success is exactly the new run's state.json path (`fsd/scripts/state.py`'s own `start` command prints the identical shape for itself); and `ocs validate interview ledger <path>`, since interview has no `start` builder of its own -- its ledger is written directly by the interview skill -- and this validator is the one command `interview/SKILL.md`'s own `<Ledger>` section says always runs against it, both before relying on an active ledger and before accepting a terminal receipt, so its own `<path>` argument stands in for a printed destination. The command text is tokenized with `shlex.split` and split again on the literal `&&`/`;` tokens that survive it, so a chained command (`checkpoint ... && ... start ...`, `state.py`'s own `_guard_action`) is matched segment by segment against each command's own leading tokens rather than a substring search of the whole line, and a quoted argument -- a ledger path holding a space -- comes back unquoted the way the shell itself would hand it to the underlying command. A relative argument is resolved against the cwd that Bash call actually ran in, falling back to the project root only when that cwd is unusable; a shell-substituted argument (`$(...)`, a backtick, `$VAR`/`${VAR}`) names its value only at the shell's own hands, never in the literal command text, so it cannot be resolved at all and the command yields no candidate. Each candidate is checked with `fsd`'s own strict belonging test (`_candidate_belongs`) before ever being attached; a candidate that fails it -- an unrelated run, a `--kind brief` stranger, a ralplan or interview run for a different document entirely -- is left exactly as unassociated as if `post-bash` had never run at all. `post-bash` never blocks and never raises.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

WRITE_TOOL_NAMES = frozenset({"Write", "Edit", "MultiEdit", "NotebookEdit"})

# Both forms a real Skill-tool call was measured to leave verbatim in `tool_input.skill` (docs/skills/fsd/260919-hook-probe.md, "binding addition"): qualified `kein:<stage>` and bare `<stage>`. Neither is normalized to the other by the runtime, so both map here; the same document records why the bare form stays despite the collision risk it carries.
_STAGE_BY_SKILL_NAME: Dict[str, str] = {}
for _stage in ("interview", "ralplan", "execute"):
    _STAGE_BY_SKILL_NAME[f"kein:{_stage}"] = _stage
    _STAGE_BY_SKILL_NAME[_stage] = _stage

# The Bash commands `post-bash` watches, as token sequences rather than a substring match. `ralplan start` and `execute start` each print their own new state.json path as their one line of stdout on success; a failed `start` prints nothing to stdout at all (its error goes to stderr instead), so a blank or unparsable stdout already yields no candidate for those two, with nothing further to check. Interview has no `start` of its own; its candidate is read from this command's own trailing argument, not from stdout, since a validation call prints nothing on success.
_START_TOKENS = {
    "ralplan": ("ocs", "state", "ralplan", "start"),
    "execute": ("ocs", "state", "execute", "start"),
}
_INTERVIEW_LEDGER_TOKENS = ("ocs", "validate", "interview", "ledger")

# A shell construct -- command substitution (`$(...)`, a backtick) or a variable expansion (`$VAR`, `${VAR}`) -- whose actual value is filled in by the shell that ran this command, never present in `tool_input.command`'s own literal text.
_SHELL_SUBSTITUTION = re.compile(r"\$\(|`|\$\{|\$[A-Za-z_][A-Za-z0-9_]*")


def _looks_shell_substituted(token: str) -> bool:
    """Whether `token` carries a shell construct whose value this function can never read from the literal command text alone. Such a token cannot be resolved at all, so the command it names a candidate for yields no candidate rather than a wrong one."""
    return bool(_SHELL_SUBSTITUTION.search(token))


def _chain_segments(tokens):
    """Splits one shlex-tokenized command line into its `&&`/`;`-separated segments, in execution order. Neither separator is special to `shlex.split` -- each survives as its own literal token, apart from its neighbours by whitespace the way a real chained command always writes it -- so this is a second, plain split over the already-tokenized list rather than a second shlex pass."""
    segments = [[]]
    for token in tokens:
        if token in ("&&", ";"):
            segments.append([])
        else:
            segments[-1].append(token)
    return [segment for segment in segments if segment]


def _segment_candidate(segment):
    """`(stage, ledger_path_token)` for a chain segment that names one of the three commands `post-bash` watches, matched by its own leading tokens rather than a substring search of the whole line -- `(None, None)` for every other segment. A `ralplan`/`execute` `start` segment's own candidate is read from `start`'s own stdout, never from here, so its own second element is always `None`; an interview-ledger segment's own candidate is its own trailing argument, since a successful validation prints nothing to stdout at all."""
    for stage, prefix in _START_TOKENS.items():
        if tuple(segment[: len(prefix)]) == prefix:
            return stage, None
    if (
        tuple(segment[: len(_INTERVIEW_LEDGER_TOKENS)]) == _INTERVIEW_LEDGER_TOKENS
        and len(segment) > len(_INTERVIEW_LEDGER_TOKENS)
    ):
        return "interview", segment[len(_INTERVIEW_LEDGER_TOKENS)]
    return None, None


def _matched_segment(command: str):
    """`(stage, ledger_path_token | None)` for the first chain segment of `command` that names one of the three commands `post-bash` watches, or `None` when no segment does. Tokenized with `shlex.split` first -- which un-quotes a quoted argument (a ledger path holding a space) back to its own literal text -- and split again on the literal `&&`/`;` tokens that survive it, so a chained command is checked segment by segment rather than as one line searched for a lookalike substring. Unbalanced quoting is not a command this function can ever match, so it reads as no match rather than raising."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        return None
    for segment in _chain_segments(tokens):
        stage, ledger_token = _segment_candidate(segment)
        if stage is not None:
            return stage, ledger_token
    return None


def _resolve_relative_argument(text: str, execute_module, payload: Dict[str, Any]) -> Path:
    """A relative argument named in the Bash command's own text or stdout -- the interview ledger path, or a `start` call's own printed destination when it too is relative -- resolved against the cwd that Bash call actually ran in (`payload["cwd"]`, the same directory its own relative shell arguments are relative to), falling back to the project root only when `cwd` itself is missing or unusable: a Bash call's own relative arguments are never relative to a git worktree root the lead never `cd`ed to."""
    candidate = Path(text)
    if candidate.is_absolute():
        return candidate
    cwd = payload.get("cwd")
    base = Path(cwd) if isinstance(cwd, str) and cwd else _canonical_worktree_root(execute_module, payload)
    return base / candidate


def _stdout_state_json_line(stdout: Optional[str], execute_module, payload: Dict[str, Any]) -> Optional[Path]:
    """The one line of a `start` call's own captured stdout that actually names an existing `state.json` file, scanned from the end -- not unconditionally the chain's last line, which a later command in the same chain (a chained recovery's own replacement `start`, or a lead's own `start && dispatch`) is not guaranteed to leave naming the run this call actually started. Scanning from the end, rather than the beginning, is what still picks the *replacement*'s own line over a chained recovery's own leading `checkpoint` line -- an aborted receipt's own printed destination, which also still exists and also still ends in `state.json` at the moment `post-bash` reads it."""
    for line in reversed((stdout or "").splitlines()):
        line = line.strip()
        if not line or _looks_shell_substituted(line):
            continue
        candidate = _resolve_relative_argument(line, execute_module, payload)
        if candidate.name == "state.json" and candidate.is_file():
            return candidate
    return None


def _import_sibling(relative: str, name: str):
    path = Path(__file__).resolve().parents[2] / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _config_dir() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or (Path.home() / ".claude"))


def _off_switch_present() -> bool:
    return (_config_dir() / "kein" / "fsd" / "hooks-off").is_file()


def _reference_dir(payload: Dict[str, Any]) -> Path:
    """The directory a resolution step runs from: `$CLAUDE_PROJECT_DIR` when set, else the hook input's own `cwd`, else this process's cwd -- the same order a hook subprocess can actually observe, since it has no guarantee `CLAUDE_PROJECT_DIR` is exported into its environment."""
    hint = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    return Path(hint)


def _state_dir_root(payload: Dict[str, Any]) -> Path:
    """Mirrors `plugin/libexec/ocs-state-dir`'s own resolution order exactly, since the constraint is 'found the way `ocs state-dir` resolves' and a hook has no PATH guarantee that binary is reachable to shell out to: `KEIN_STATE_ROOT`, then `$CLAUDE_PROJECT_DIR`, then the nearest git worktree from the reference directory, then the vendor config home with no project in scope."""
    if os.environ.get("KEIN_STATE_ROOT"):
        return Path(os.environ["KEIN_STATE_ROOT"]) / ".agents" / "kein"
    if os.environ.get("CLAUDE_PROJECT_DIR"):
        return Path(os.environ["CLAUDE_PROJECT_DIR"]) / ".agents" / "kein"
    reference = _reference_dir(payload)
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], cwd=str(reference),
            capture_output=True, text=True, timeout=5,
        )
        top = result.stdout.strip()
        if result.returncode == 0 and top:
            return Path(top) / ".agents" / "kein"
    except (OSError, subprocess.SubprocessError):
        pass
    return _config_dir() / "kein"


def _load_fsd_and_execute():
    fsd_module = _import_sibling("fsd/scripts/state.py", "_kein_hook_fsd_state")
    return fsd_module, fsd_module._execute


def _canonical_worktree_root(execute_module, payload: Dict[str, Any]) -> Path:
    reference = _reference_dir(payload)
    try:
        root, _ = execute_module.canonical_worktree(reference)
        return root
    except Exception:
        return reference.resolve()


def _find_active_state_path(fsd_module, execute_module, payload: Dict[str, Any]) -> Optional[Path]:
    run_root = _state_dir_root(payload) / "runs" / "fsd"
    worktree_root = _canonical_worktree_root(execute_module, payload)
    return fsd_module._find_nonterminal_fsd_run(run_root, worktree_root)


def _gap_action(fsd_module, state_path: Path, state: Dict[str, Any]) -> Optional[str]:
    """The reason text a block or deny prints, with `<state>` -- the literal placeholder `fsd`'s own `gap()` writes into a closeout-row action -- replaced by the resolved state.json path, `shlex.quote`d so the printed reason still runs as one valid argument when the state.json path itself sits under a repository path holding a space, so the printed reason is a command the lead can run directly rather than a template they still have to fill in."""
    result = fsd_module.gap(state)
    if result.get("gap"):
        action = result.get("action") or "advance the next stage"
        return action.replace("<state>", shlex.quote(str(state_path)))
    return None


def _read_stdin_payload() -> Optional[Dict[str, Any]]:
    """The parsed JSON object, or `None` for anything that is not one: unreadable stdin, unparseable text, or JSON that parses to something other than an object -- an array, a string, a number, `null`. `None` is not coerced to an empty `{}` stand-in, because an empty dict still has every field a mode reads come back `None`/missing and so would still run the ordinary gap check and could still block or deny on whatever state happens to be on disk; `main` allows outright on `None` instead, before any mode runs at all."""
    try:
        raw = sys.stdin.read()
        parsed = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
        return None
    return parsed if isinstance(parsed, dict) else None


def _allow() -> None:
    sys.exit(0)


def _block_stop(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": f"fsd: {reason}"}))
    sys.exit(0)


def _deny_pretool(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"fsd: {reason}",
        },
    }))
    sys.exit(0)


def _resolve(payload: Dict[str, Any]) -> Optional[Tuple[Any, Path, Dict[str, Any]]]:
    """`None` on anything that is not a live gap check: off-switch, no importable state machine, no associated nonterminal run, or a state file that does not load. Every caller treats `None` as allow, so a resolution failure of any kind is indistinguishable here from there being no gap."""
    if _off_switch_present():
        return None
    fsd_module, execute_module = _load_fsd_and_execute()
    state_path = _find_active_state_path(fsd_module, execute_module, payload)
    if state_path is None:
        return None
    state = fsd_module._load(state_path)
    return fsd_module, state_path, state


def mode_stop(payload: Dict[str, Any]) -> None:
    if payload.get("stop_hook_active") is True:
        _allow()
    resolved = _resolve(payload)
    if resolved is None:
        _allow()
    fsd_module, state_path, state = resolved
    action = _gap_action(fsd_module, state_path, state)
    if action:
        _block_stop(action)
    _allow()


def mode_pre_write(payload: Dict[str, Any]) -> None:
    if payload.get("tool_name") not in WRITE_TOOL_NAMES:
        _allow()
    resolved = _resolve(payload)
    if resolved is None:
        _allow()
    fsd_module, state_path, state = resolved
    action = _gap_action(fsd_module, state_path, state)
    if action:
        _deny_pretool(action)
    _allow()


def mode_post_skill(payload: Dict[str, Any]) -> None:
    # Never blocks, so every branch below still falls through to `_allow()` at the end; the only question is whether `enter` gets a chance to run first. The off-switch check happens here too, ahead of every other read, so a marker present makes this mode a pure no-op -- no stage's status or association is touched -- rather than merely suppressing the (nonexistent) block.
    if _off_switch_present():
        _allow()
    skill_name = (payload.get("tool_input") or {}).get("skill")
    stage = _STAGE_BY_SKILL_NAME.get(skill_name) if isinstance(skill_name, str) else None
    if stage is not None:
        try:
            fsd_module, execute_module = _load_fsd_and_execute()
            state_path = _find_active_state_path(fsd_module, execute_module, payload)
            if state_path is not None:
                fsd_module.enter(state_path, stage)
        except Exception:
            # `enter`'s own refusal -- the stage is `skipped` for this run, among other reasons -- lands here too, and stays swallowed on purpose: the stage's own status is simply left exactly as it was, no different from `enter` never having been tried at all.
            pass
    _allow()


def mode_post_bash(payload: Dict[str, Any]) -> None:
    # Never blocks; every branch falls through to `_allow()`. The off-switch check happens ahead of every other read, so a marker present makes this mode a pure no-op.
    if _off_switch_present():
        _allow()
    command = (payload.get("tool_input") or {}).get("command")
    if not isinstance(command, str):
        _allow()
    matched = _matched_segment(command)
    if matched is None:
        _allow()
    stage, ledger_token = matched
    tool_response = payload.get("tool_response") or {}
    stdout = tool_response.get("stdout")
    stdout = stdout if isinstance(stdout, str) else None
    try:
        fsd_module, execute_module = _load_fsd_and_execute()
        candidate_path: Optional[Path] = None
        if ledger_token is not None:
            if not _looks_shell_substituted(ledger_token):
                candidate_path = _resolve_relative_argument(ledger_token, execute_module, payload)
        else:
            candidate_path = _stdout_state_json_line(stdout, execute_module, payload)
        if candidate_path is not None:
            state_path = _find_active_state_path(fsd_module, execute_module, payload)
            if state_path is not None:
                state = fsd_module._load(state_path)
                # The strict belonging test runs here, before `attach` is ever called, so a non-belonging candidate -- an unrelated run, a `--kind brief` stranger, a ralplan or interview run for a different document -- is never attached; `attach` applies the identical test to a lead's own explicit call, with no looser fallback of its own to reach for either.
                if candidate_path.is_file() and fsd_module._candidate_belongs(state, stage, candidate_path):
                    fsd_module.attach(state_path, stage, candidate_path)
    except Exception:
        # A refusal from `attach` (the stage is skipped, or the state is terminal) lands here too, and stays swallowed on purpose, the same as `post-skill`'s own `enter` refusal: the stage's association is simply left exactly as it was.
        pass
    _allow()


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    payload = _read_stdin_payload()
    try:
        if payload is None:
            _allow()
        elif mode == "stop":
            mode_stop(payload)
        elif mode == "pre-write":
            mode_pre_write(payload)
        elif mode == "post-skill":
            mode_post_skill(payload)
        elif mode == "post-bash":
            mode_post_bash(payload)
        else:
            _allow()
    except SystemExit:
        raise
    except Exception:
        _allow()


if __name__ == "__main__":
    main()
