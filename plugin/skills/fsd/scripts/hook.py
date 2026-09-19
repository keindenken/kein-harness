#!/usr/bin/env python3
"""fsd's stage-transition hooks -- modes `stop`, `pre-write`, `post-skill` -- for the placement Gate G1 selected (`docs/skills/fsd/260919-hook-probe.md`): declared in `fsd`'s own SKILL.md frontmatter, not in `plugin/hooks/hooks.json`. The probe found frontmatter Stop and PreToolUse still fire after the model invokes a nested, model-invocable skill, and that a frontmatter `PostToolUse` `Skill` hook's input reliably carries the exact `skill` string the model wrote -- verbatim, in both the qualified (`kein:<stage>`) and bare (`<stage>`) forms it can take -- so `post-skill` below reads that field directly rather than requiring the lead to run `ocs state fsd enter <stage>` unconditionally. The probe document also records why accepting the bare form is kept despite the (low, bounded) risk of a same-named third-party skill.

Every mode allows by default and only ever acts on positive gap evidence read from `fsd`'s own `gap()`, imported here read-only exactly as `fsd/scripts/state.py` itself imports `execute`'s and `ralplan`'s internals -- nothing here re-derives what counts as a gap. Every path exits 0: `stop` blocks by printing `{"decision": "block", "reason": ...}`, `pre-write` denies by printing `hookSpecificOutput.permissionDecision: "deny"`, and every other outcome -- allow, an off-switch, no run, a corrupt or unreadable state, any exception -- is silent success. A block or deny reason that names `ocs state fsd closeout <state>` has `<state>` substituted with the resolved state.json path before it is printed, so the reason is a command the lead can run as-is rather than a template.
"""
from __future__ import annotations

import importlib.util
import json
import os
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
    """The reason text a block or deny prints, with `<state>` -- the literal placeholder `fsd`'s own `gap()` writes into a closeout-row action -- replaced by the resolved state.json path, so the printed reason is a command the lead can run directly rather than a template they still have to fill in."""
    result = fsd_module.gap(state)
    if result.get("gap"):
        action = result.get("action") or "advance the next stage"
        return action.replace("<state>", str(state_path))
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
    # Never blocks, so every branch below still falls through to `_allow()` at the end; the only question is whether `enter` gets a chance to run first. The off-switch check happens here too, ahead of every other read, so a marker present makes this mode a pure no-op -- no stage's status, snapshot, or association is touched -- rather than merely suppressing the (nonexistent) block.
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
        else:
            _allow()
    except SystemExit:
        raise
    except Exception:
        _allow()


if __name__ == "__main__":
    main()
