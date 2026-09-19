#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
from contextlib import contextmanager
from datetime import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple


SCHEMA_VERSION = 1
TASK_STATUSES = frozenset({"pending", "implementing", "verifying", "reviewing", "correcting", "accepted", "parked"})
WRITE_ACTIVE_STATUSES = frozenset({"implementing", "verifying", "reviewing", "correcting"})
NONTERMINAL_LIFECYCLES = frozenset({"active", "blocked", "interrupted"})
TERMINAL_LIFECYCLES = frozenset({"completed", "aborted"})
PHASES = frozenset({"initializing", "task", "simplifying", "regression_verifying", "final_audit", "blocked", "interrupted"})
PHASE_TRANSITIONS = {
    "initializing": frozenset({"initializing", "task", "blocked", "interrupted"}),
    "task": frozenset({"task", "simplifying", "final_audit", "blocked", "interrupted"}),
    "simplifying": frozenset({"simplifying", "regression_verifying", "final_audit", "blocked", "interrupted"}),
    "regression_verifying": frozenset({"regression_verifying", "final_audit", "blocked", "interrupted"}),
    "final_audit": frozenset({"final_audit", "task", "regression_verifying", "blocked", "interrupted"}),
    "blocked": frozenset({"blocked", "task", "interrupted"}),
    "interrupted": frozenset({"interrupted", "task", "blocked"}),
}
# A parked task holds no writes: `pending` and a restored `implementing`/`correcting` may park, `verifying` and `reviewing` may not (their tree is between gates, not at a checked-in rest point), and `parked` only ever returns to `pending`, where the ordinary dispatch cycle picks it up again.
TASK_TRANSITIONS = {
    "pending": frozenset({"pending", "implementing", "parked"}),
    "implementing": frozenset({"implementing", "verifying", "parked"}),
    "verifying": frozenset({"verifying", "reviewing", "correcting"}),
    "reviewing": frozenset({"reviewing", "correcting", "accepted"}),
    "correcting": frozenset({"correcting", "verifying", "parked"}),
    "accepted": frozenset({"accepted", "correcting"}),
    "parked": frozenset({"parked", "pending"}),
}
HEX_64 = "0123456789abcdef"

# No `created_at` or `updated_at`.
# `reconcile` is the only authority on continuation and it reads no time, so a nonterminal timestamp had no consumer.
# `revision` already orders checkpoints, `run_id` carries the start to the second, and the file's mtime is the last write.
NONTERMINAL_FIELDS = frozenset({
    "schema_version", "revision", "workflow", "run_id", "lifecycle",
    "input", "worktree", "phase", "tasks", "current_task_id", "current_round",
    "latest_verification", "unresolved_findings", "final_audit", "next_action",
})
COMPLETED_FIELDS = frozenset({
    "schema_version", "revision", "workflow", "run_id", "lifecycle", "completed_at", "input",
    "worktree", "accepted_tasks", "final_verification", "final_audit", "carried_findings",
})
ABORTED_FIELDS = frozenset({
    "schema_version", "revision", "workflow", "run_id", "lifecycle", "aborted_at", "worktree_root", "reason",
})
INPUT_FIELDS = frozenset({"kind", "reference", "summary", "sha256", "declared_status"})
INPUT_OPTIONAL = frozenset({"amendments"})
AMENDMENT_FIELDS = frozenset({"at", "reason", "from", "to"})
WORKTREE_FIELDS = frozenset({"root", "git_common_dir", "baseline", "observed"})
FINGERPRINT_FIELDS = frozenset({"head", "index_sha256", "tracked_diff_sha256", "untracked_sha256", "fingerprint"})
TASK_FIELDS = frozenset({
    "id", "title", "scope", "completion_condition", "verification_path", "rationale",
    "status", "round", "latest_verification", "unresolved_findings", "acceptance",
})
# The fingerprint of the task's own scope on the observed tree, filled by `checkpoint` for every task not yet accepted and sealed on acceptance.
# A task's verification, verdicts and acceptance bind to this rather than to the whole tree, which is what lets two tasks with disjoint scopes be written at once: one's writes do not move the other's fingerprint. Optional so a state written before it existed still validates.
#
# `dispatch_scope_fingerprint` is a different shape, not this one: a map from a scope-relative path to the sha256 of that path's own content, read straight off the index and the worktree with no HEAD in it anywhere (`_scope_content_digest`). It is sealed once by `dispatch` on the `pending -> implementing` checkpoint that dispatches the task, before its executor is told to start, and never changed after that checkpoint while the task stays write-active.
# A task without it, or with one written in the pre-correction `worktree_fingerprint` shape (`_is_legacy_dispatch_seal`), cannot park from a write-active status.
# `parked` carries `question`, `from`, `decision_ref`, `at`: required exactly when `status` is `parked`, refused otherwise. Both optional so a state written before either existed still validates.
TASK_OPTIONAL = frozenset({"scope_fingerprint", "dispatch_scope_fingerprint", "parked"})
PARKED_FIELDS = frozenset({"question", "from", "decision_ref", "at"})
PARKED_FROM_VALUES = frozenset({"pending", "implementing", "correcting"})
VERIFICATION_FIELDS = frozenset({"command", "exit_code", "observed_at", "round", "worktree_fingerprint"})
VERDICT_FIELDS = frozenset({
    "reviewer_role", "verdict", "task_id", "round", "worktree_fingerprint",
    "reviewed_at", "fresh", "independent",
})
# `severity` and `confidence` are the reviewer role's own calibration (`agents/code-reviewer.md`, `agents/critic.md`), self-audited against inflation and minimisation there, and this workflow read neither: acceptance keyed on the verdict word alone, so a `minor` blocked exactly as a `critical` did. The phase-47 run's ten blind lanes returned some twenty findings that were real and not blocking, fourteen of them inside a `PASS`, and the state recorded none of them.
# `blocks` is the workflow's own question and is separate from severity on purpose: whether THIS task is done. It cites the clause of the task's completion condition the finding defeats, verbatim, or names a regression or a repository instruction with a prefix -- so a finding that cannot point at the condition is, by construction, not about whether this task is done, and goes to a new task or to the receipt instead of blocking this one.
VERDICT_VALUES = frozenset({"PASS", "REVISE", "BLOCK"})
FINDING_FIELDS = frozenset({
    "reviewer_role", "claim", "evidence", "impact", "required_correction", "severity", "confidence", "blocks",
})
# A `critical` that stays carried instead of becoming a task owes the receipt the reason, so a promotion that did not happen is a written decision rather than a silence.
FINDING_OPTIONAL = frozenset({"carried_because"})
BLOCKS_PREFIXES = ("regression: ", "instruction: ")
ACCEPTANCE_FIELDS = frozenset({"round", "worktree_fingerprint", "reviewers"})
ACCEPTANCE_OPTIONAL = frozenset({"fixed"})
COMPLETED_INPUT_FIELDS = frozenset({"reference", "sha256"})
COMPLETED_WORKTREE_FIELDS = frozenset({"root", "final_fingerprint"})
ACCEPTED_TASK_FIELDS = frozenset({"id", "title", "completion_condition", "carried_findings"})
ACCEPTED_TASK_OPTIONAL = frozenset({"fixed_findings"})


def _git_bytes(path: Path, args: List[str]) -> bytes:
    result = subprocess.run(
        ["git", *args], cwd=str(path), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", "replace").strip()
        raise ValueError(message or f"git {' '.join(args)} failed")
    return result.stdout


def _hash_parts(parts: List[Tuple[bytes, bytes]]) -> str:
    digest = hashlib.sha256()
    for name, value in parts:
        digest.update(len(name).to_bytes(8, "big"))
        digest.update(name)
        digest.update(len(value).to_bytes(8, "big"))
        digest.update(value)
    return digest.hexdigest()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_worktree(path: Path) -> Tuple[Path, Path]:
    root_text = _git_bytes(path, ["rev-parse", "--show-toplevel"]).decode().strip()
    root = Path(root_text).resolve()
    common_text = _git_bytes(root, ["rev-parse", "--git-common-dir"]).decode().strip()
    common = Path(common_text)
    if not common.is_absolute():
        common = root / common
    return root, common.resolve()


# The run ledger is the harness's own live scratch, and it changes on every checkpoint by definition:
# `ocs state-dir` resolves inside the worktree, so writing `state.json` alters the very untracked set
# the fingerprint just recorded. Left in, the first `reconcile` after a clean checkpoint reports drift
# with no work done at all, and a gate that is always RED buys what a gate that is always GREEN buys.
#
# This repository hides the bug from itself. Its own `.gitignore` carries exactly this path with the
# note "Transient run state. Deliverables under `.agents/kein/` are tracked." -- so the exclusion is a
# decision already made here by hand, and the only thing wrong was that it lived in one repository's
# ignore file instead of in the code, leaving the behaviour to depend on whether a target repository
# happened to repeat it. Measured 2026-08-20: identical checkpoints reconcile clean under the ignore
# and dirty without it.
#
# Only `runs/`. Plans and other deliverables under `.agents/kein/` stay in the fingerprint, because a
# plan changing under an executing round is drift that matters -- and is the case `input.sha256`
# answers for the current input but not for anything else in the tree.
LEDGER_PREFIX = ".agents/kein/runs/"


def worktree_fingerprint(path: Path, scope: Optional[List[str]] = None) -> Dict[str, str]:
    """The tree's fingerprint, or with `scope` the fingerprint of those paths alone.

    A scoped fingerprint reads the same four components over the scope's pathspec: HEAD, the staged and unstaged diffs limited to the scope, and the untracked files under it. `:(literal)` keeps the pathspec from globbing, so a scope entry means exactly the path it names and, for a directory, everything under it -- the same reading `_scopes_collide` gives it.
    """
    root, _ = canonical_worktree(path)
    head = _git_bytes(root, ["rev-parse", "HEAD"]).strip()
    pathspec = ["--"] + [f":(literal){entry}" for entry in scope] if scope else []
    index = _git_bytes(root, ["diff", "--cached", "--binary", "--no-ext-diff", *pathspec])
    tracked = _git_bytes(root, ["diff", "--binary", "--no-ext-diff", *pathspec])
    untracked_paths = [item for item in _git_bytes(root, ["ls-files", "--others", "--exclude-standard", "-z"]).split(b"\0") if item]
    untracked_parts: List[Tuple[bytes, bytes]] = []
    for relative_bytes in sorted(untracked_paths):
        relative = relative_bytes.decode("utf-8", "surrogateescape")
        if relative.startswith(LEDGER_PREFIX):
            continue
        if scope is not None and not any(_scopes_collide(entry, relative) for entry in scope):
            continue
        candidate = root / relative
        if candidate.is_symlink():
            value = b"symlink\0" + os.fsencode(os.readlink(candidate))
        elif candidate.is_file():
            value = b"file\0" + candidate.read_bytes()
        else:
            value = b"other\0"
        untracked_parts.append((relative_bytes, value))
    untracked_hash = _hash_parts(untracked_parts)
    components = {
        "head": head.decode("ascii"),
        "index_sha256": _sha256_bytes(index),
        "tracked_diff_sha256": _sha256_bytes(tracked),
        "untracked_sha256": untracked_hash,
    }
    components["fingerprint"] = _hash_parts([
        (key.encode(), value.encode()) for key, value in sorted(components.items())
    ])
    return components


def _scope_pathspec(scope: List[str]) -> List[str]:
    """The `git` pathspec argument list for a scope, matched the same way `worktree_fingerprint` matches its own scoped calls.

    A scope entry with no path parts -- `.`, `./`, `""` -- names the whole tree and needs no restriction to say so: an unscoped call already reads as "no restriction" elsewhere in this file, and `_scopes_collide` reads the same entries as meeting every other scope, so this keeps that same reading rather than routing it through a pathspec that would say the same thing more roundabout. Every other scope is restricted to its own `:(literal)` entries as before.
    """
    if any(not _scope_parts(entry) for entry in scope):
        return []
    return ["--"] + [f":(literal){entry}" for entry in scope]


_CHUNK_SIZE = 1 << 20


def _hash_scope_path(candidate: Path) -> Optional[str]:
    """A symlink's target, or a regular file's bytes read in chunks rather than loaded whole, so a large file under a scope does not have to fit in memory at once; `None` for a path that is neither -- deleted, or never a regular file to begin with."""
    if candidate.is_symlink():
        return _sha256_bytes(b"symlink\0" + os.fsencode(os.readlink(candidate)))
    if not candidate.is_file():
        return None
    digest = hashlib.sha256()
    digest.update(b"file\0")
    with candidate.open("rb") as handle:
        for chunk in iter(lambda: handle.read(_CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _scope_content_digest(path: Path, scope: List[str]) -> Dict[str, str]:
    """The scope's actual content right now, one hash per path, read from the index and the worktree with no reference to HEAD at all.

    This is not `worktree_fingerprint`: that reads `git diff` output, which is a delta against HEAD, so it moves whenever HEAD moves even where the bytes a task actually wrote have not changed -- a commit elsewhere sweeps a task's own draft into HEAD and the diff goes quiet over it, and a commit of an earlier, overlapping task's already-accepted work moves the index's blob id for paths this task never touched. Content this function reads is the current tracked-or-visibly-untracked path list under the scope's own `git` pathspec (`git ls-files` and `git ls-files --others --exclude-standard`, restricted the way `_scope_pathspec` builds it, ignored paths and the run ledger excluded exactly as `worktree_fingerprint` excludes them) and, per path, the literal bytes on disk right now -- a symlink's target, a regular file's content, nothing else. No blob id from the index is read: a path's index entry can change across an `add`+`commit` even while its worktree bytes do not move, and that would make a genuinely restored path fail this comparison for a reason that has nothing to do with restoration. A path absent from the returned map does not currently exist under the scope, whether it never did or was deleted; that absence is itself part of what two digests are compared for.
    """
    root, _ = canonical_worktree(path)
    pathspec = _scope_pathspec(scope)
    tracked_paths = [item for item in _git_bytes(root, ["ls-files", "-z", *pathspec]).split(b"\0") if item]
    untracked_paths = [item for item in _git_bytes(root, ["ls-files", "--others", "--exclude-standard", "-z", *pathspec]).split(b"\0") if item]
    digest: Dict[str, str] = {}
    for relative_bytes in sorted(set(tracked_paths) | set(untracked_paths)):
        relative = relative_bytes.decode("utf-8", "surrogateescape")
        if relative.startswith(LEDGER_PREFIX):
            continue
        value_hash = _hash_scope_path(root / relative)
        if value_hash is None:
            continue
        digest[relative] = value_hash
    return digest


def _scope_digest_diff(current: Any, dispatched: Any) -> List[str]:
    """The scope paths whose content differs between two digests, sorted; empty when they agree everywhere `_scope_content_digest` could report a difference (a changed path, an added one, or a removed one)."""
    if not isinstance(current, dict) or not isinstance(dispatched, dict):
        return sorted(set(current) | set(dispatched)) if isinstance(current, dict) or isinstance(dispatched, dict) else ["<unreadable>"]
    return sorted(path for path in set(current) | set(dispatched) if current.get(path) != dispatched.get(path))


def _scope_parts(entry: str) -> Tuple[str, ...]:
    return tuple(part for part in entry.strip().replace("\\", "/").split("/") if part not in ("", "."))


def _scopes_collide(left: str, right: str) -> bool:
    """Two scope entries name the same place when one is the other or contains it.

    Scope is a list of paths a task may write, and a task that names a directory names everything under it, so `src/b/` and `src/b/x.py` collide while `src/b/` and `src/bx.py` do not. An entry with no path parts -- `.`, `./`, an empty string -- names the whole tree rather than nothing, the same reading `_scope_pathspec` gives it for a content digest, so it collides with every other entry, including another one shaped the same way: a root-scoped task must not dispatch alongside a write-active sibling, must wait behind an earlier pending or parked one, and must hold a later one back exactly as any other scope does. Nothing here reads the filesystem: this measures what the ledger says, which is what the lead wrote and can be held to.
    """
    a, b = _scope_parts(left), _scope_parts(right)
    if not a or not b:
        return True
    shorter, longer = (a, b) if len(a) <= len(b) else (b, a)
    return longer[:len(shorter)] == shorter


def _scope_collisions(tasks: List[Dict[str, Any]], candidates: List[str]) -> List[Dict[str, Any]]:
    """Where the named tasks would write over each other, over a task already being written, or over an earlier task not yet done.

    Scope is what the ledger says a task may write, a directory naming everything under it. Two tasks may be written at once only when their scopes do not meet; a task may not start ahead of an earlier task whose scope meets its own, because the ledger's order is the plan's dependency order and an overlap is where that order is load-bearing. Accepted tasks are already in the tree and do not count. A parked task collides exactly as a pending one does: it occupies its scope only against tasks listed after it, so an earlier independent task is never starved by a question that parked something later. Nothing here reads the filesystem.
    """
    by_id = {task["id"]: task for task in tasks if isinstance(task, dict) and "id" in task}
    order = [task["id"] for task in tasks if isinstance(task, dict) and "id" in task]
    def shared(left_id: str, right_id: str) -> List[str]:
        return sorted({" ~ ".join(sorted((l, r))) if l != r else l
                       for l in by_id[left_id].get("scope", []) for r in by_id[right_id].get("scope", [])
                       if isinstance(l, str) and isinstance(r, str) and _scopes_collide(l, r)})
    collisions: List[Dict[str, Any]] = []
    seen = set()
    for index, left_id in enumerate(candidates):
        others = list(candidates[index + 1:])
        others += [task_id for task_id in order if task_id not in candidates and by_id[task_id].get("status") in WRITE_ACTIVE_STATUSES]
        others += [task_id for task_id in order[:order.index(left_id)] if task_id not in candidates and by_id[task_id].get("status") in {"pending", "parked"}]
        for right_id in others:
            pair = tuple(sorted((left_id, right_id)))
            if pair in seen:
                continue
            seen.add(pair)
            paths = shared(left_id, right_id)
            if paths:
                collisions.append({"tasks": [left_id, right_id], "paths": paths})
    return collisions


def split_check(payload: Dict[str, Any], task_ids: List[str]) -> Dict[str, Any]:
    """Whether the named pending tasks could be dispatched now, together, measured on the ledger's own scopes.

    The same rule `checkpoint` enforces when a task becomes write-active, answered before anything is dispatched. It reports; whether two disjoint tasks should be written at once is the lead's call, and a project whose tests hold a machine-global port has a reason no scope list shows.
    """
    tasks = payload.get("tasks", [])
    by_id = {task["id"]: task for task in tasks if isinstance(task, dict) and "id" in task}
    unknown = [task_id for task_id in task_ids if task_id not in by_id]
    if unknown:
        raise ValueError(f"no such task: {', '.join(unknown)}")
    if len(set(task_ids)) != len(task_ids):
        raise ValueError("a task is named twice")
    for task_id in task_ids:
        if by_id[task_id].get("status") != "pending":
            raise ValueError(f"{task_id} is {by_id[task_id].get('status')}; only a pending task can be dispatched")
    collisions = _scope_collisions(tasks, task_ids)
    return {
        "dispatch": task_ids,
        "active": [task_id for task_id, task in by_id.items() if task.get("status") in WRITE_ACTIVE_STATUSES],
        "disjoint": not collisions,
        "collisions": collisions,
    }


def _valid_hash(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(character in HEX_64 for character in value)


def _valid_oid(value: Any) -> bool:
    return isinstance(value, str) and len(value) in {40, 64} and all(character in HEX_64 for character in value)


def _valid_time(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        return datetime.fromisoformat(value).tzinfo is not None
    except ValueError:
        return False


def _validate_fingerprint(value: Any, label: str) -> List[str]:
    if not isinstance(value, dict) or set(value) != FINGERPRINT_FIELDS:
        return [f"{label} must use the exact fingerprint field set"]
    errors = [f"{label} requires a valid head"] if not _valid_oid(value.get("head")) else []
    errors.extend(
        f"{label} requires a valid {key}"
        for key in FINGERPRINT_FIELDS - {"head"}
        if not _valid_hash(value.get(key))
    )
    if not errors:
        expected = _hash_parts([
            (key.encode(), value[key].encode())
            for key in sorted(FINGERPRINT_FIELDS - {"fingerprint"})
        ])
        if value["fingerprint"] != expected:
            errors.append(f"{label} combined fingerprint is inconsistent")
    return errors


def _validate_verification(value: Any, expected_round: Optional[int] = None, expected_fingerprint: Optional[str] = None) -> List[str]:
    if not isinstance(value, dict) or set(value) != VERIFICATION_FIELDS:
        return ["Verification must use the exact field set"]
    errors: List[str] = []
    if not isinstance(value.get("command"), str) or not value["command"]:
        errors.append("Verification requires a command")
    if type(value.get("exit_code")) is not int:
        errors.append("Verification requires an integer exit_code")
    if not _valid_time(value.get("observed_at")):
        errors.append("Verification requires a timezone-aware observed_at")
    if type(value.get("round")) is not int or value["round"] < 0:
        errors.append("Verification round must be non-negative")
    if not _valid_hash(value.get("worktree_fingerprint")):
        errors.append("Verification requires a worktree fingerprint")
    if expected_round is not None and value.get("round") != expected_round:
        errors.append("Verification does not match the current round")
    if expected_fingerprint is not None and value.get("worktree_fingerprint") != expected_fingerprint:
        errors.append("Verification does not match the current worktree fingerprint")
    return errors


def _validate_verdict(value: Any, task_id: str, round_number: int, fingerprint: str) -> List[str]:
    if not isinstance(value, dict) or set(value) != VERDICT_FIELDS:
        return ["Review verdict must use the exact field set"]
    errors: List[str] = []
    if not isinstance(value.get("reviewer_role"), str) or not value["reviewer_role"]:
        errors.append("Review verdict requires a reviewer_role")
    if value.get("verdict") not in VERDICT_VALUES:
        errors.append(f"Review verdict must be one of {', '.join(sorted(VERDICT_VALUES))}")
    if value.get("task_id") != task_id:
        errors.append("Review verdict task_id does not match")
    if value.get("round") != round_number:
        errors.append("Review verdict round does not match")
    if value.get("worktree_fingerprint") != fingerprint:
        errors.append("Review verdict fingerprint does not match")
    if not _valid_time(value.get("reviewed_at")):
        errors.append("Review verdict requires a timezone-aware reviewed_at")
    if type(value.get("fresh")) is not bool or type(value.get("independent")) is not bool:
        errors.append("Review verdict freshness and independence must be booleans")
    return errors


def _normalized(text: Any) -> str:
    return " ".join(str(text).split()).lower()


def _canonical(finding: Any) -> str:
    return json.dumps(finding, sort_keys=True, ensure_ascii=False)


def _legacy_findings(payload: Any) -> frozenset:
    """The findings a state recorded before `blocks` existed.

    The field landed while a run was live, and that run's predecessor is validated on every checkpoint; refusing it would wedge the run over a shape it had no way to write. So a finding in the older shape stands where it stood, unchanged, until something is accepted over it -- acceptance, the final audit and the receipt still require the field, because that is where it decides -- and anything written new must carry it.
    """
    legacy = set()
    lists: List[Any] = []
    if isinstance(payload, dict):
        tasks = payload.get("tasks")
        for task in tasks if isinstance(tasks, list) else []:
            if isinstance(task, dict):
                lists.append(task.get("unresolved_findings"))
        lists.append(payload.get("unresolved_findings"))
    for findings in lists:
        for finding in findings if isinstance(findings, list) else []:
            if isinstance(finding, dict) and set(finding) == FINDING_FIELDS - {"blocks"}:
                legacy.add(_canonical(finding))
    return frozenset(legacy)


def _validate_findings(value: Any, completion_condition: Optional[str] = None, inherited: frozenset = frozenset()) -> List[str]:
    if not isinstance(value, list):
        return ["Findings must be a list"]
    errors: List[str] = []
    for index, finding in enumerate(value):
        if not isinstance(finding, dict):
            errors.append(f"Finding {index} must be an object")
            continue
        if _canonical(finding) in inherited:
            continue
        if set(finding) - FINDING_OPTIONAL != FINDING_FIELDS:
            errors.append(_field_set_error(f"Finding {index} must use the exact field set", finding, FINDING_FIELDS, FINDING_OPTIONAL))
            continue
        for key in FINDING_FIELDS - {"blocks"}:
            if not isinstance(finding.get(key), str) or not finding[key].strip():
                errors.append(f"Finding {index} requires non-empty {key}")
        if finding.get("severity") not in {"critical", "important", "minor"}:
            errors.append(f"Finding {index} severity is invalid")
        if finding.get("confidence") not in {"high", "medium", "low"}:
            errors.append(f"Finding {index} confidence is invalid")
        errors.extend(_validate_blocks(finding.get("blocks"), completion_condition, index))
        reason = finding.get("carried_because")
        if reason is not None and (not isinstance(reason, str) or not reason.strip()):
            errors.append(f"Finding {index} carried_because must be non-empty text when present")
        if reason is not None and finding.get("blocks") is not None:
            errors.append(f"Finding {index} cannot be carried and blocking at once")
    return errors


def _validate_blocks(value: Any, completion_condition: Optional[str], index: int) -> List[str]:
    """`blocks` is a citation, not a word: the clause has to be in the condition the lane was handed.

    Whitespace and case are the author's; the check folds both. A finding about a regression or a repository instruction has no clause to cite and says which with a prefix instead.
    """
    if value is None:
        return []
    if not isinstance(value, str) or not value.strip():
        return [f"Finding {index} blocks must be null or non-empty text"]
    if value.startswith(BLOCKS_PREFIXES):
        if not value.split(":", 1)[1].strip():
            return [f"Finding {index} blocks names a prefix and nothing after it"]
        return []
    if completion_condition is not None and _normalized(value) not in _normalized(completion_condition):
        return [f"Finding {index} blocks cites a clause that is not in this task's completion condition"]
    return []


def _blocking(findings: Any) -> bool:
    return isinstance(findings, list) and any(
        isinstance(finding, dict) and finding.get("blocks") is not None for finding in findings
    )


def _verdict_coherence(reviewers: Any, findings: Any) -> List[str]:
    """A verdict is a summary of the role's own findings, and the state can re-derive that summary.

    `BLOCK` with nothing of that role blocking, `REVISE` with nothing of that role at all or with something blocking, `PASS` over a finding the same role wrote -- each is a disagreement between two things one lane produced, and the one place severity was ever adjudicated by anything but the lane.
    """
    if not isinstance(reviewers, list) or not isinstance(findings, list):
        return []
    errors: List[str] = []
    for reviewer in reviewers:
        if not isinstance(reviewer, dict):
            continue
        role = reviewer.get("reviewer_role")
        mine = [f for f in findings if isinstance(f, dict) and f.get("reviewer_role") == role]
        blocking = [f for f in mine if f.get("blocks") is not None]
        verdict = reviewer.get("verdict")
        if verdict == "BLOCK" and not blocking:
            errors.append(f"{role} returned BLOCK with no finding of its own citing what it blocks")
        elif verdict == "REVISE" and blocking:
            errors.append(f"{role} returned REVISE over its own blocking finding")
        elif verdict == "REVISE" and not mine:
            errors.append(f"{role} returned REVISE with no finding of its own")
        elif verdict == "PASS" and mine:
            errors.append(f"{role} returned PASS over its own recorded finding")
    return errors


def _field_set_error(label: str, actual: Any, expected: frozenset, optional: frozenset = frozenset()) -> str:
    """Name the difference rather than the set the caller then has to go find.

    Every state in this workflow is hand-authored -- there are no transitions that build one -- so a
    field-set mismatch is the first thing a run hits. The first measured run hit it and answered by
    writing a script to read the constant out of this file.
    """
    keys = set(actual) if isinstance(actual, dict) else set()
    missing = sorted(expected - keys)
    unexpected = sorted(keys - expected - optional)
    return (label
            + (f"; missing {missing}" if missing else "")
            + (f"; unexpected {unexpected}" if unexpected else ""))


def _validate_scope_digest(value: Any, label: str) -> List[str]:
    """`dispatch_scope_fingerprint`'s shape: a map from a scope-relative path to the sha256 of that path's content, exactly what `_scope_content_digest` returns. An empty object is valid -- it means the scope covered nothing that existed yet at dispatch."""
    if not isinstance(value, dict):
        return [f"{label} must be an object mapping paths to content hashes"]
    errors: List[str] = []
    for path, value_hash in value.items():
        if not isinstance(path, str) or not path:
            errors.append(f"{label} requires a non-empty string for every key")
        if not _valid_hash(value_hash):
            errors.append(f"{label} requires a valid content hash for {path if isinstance(path, str) else '?'}")
    return errors


def _is_legacy_dispatch_seal(value: Any) -> bool:
    """A `dispatch_scope_fingerprint` written before this correction, in `worktree_fingerprint`'s field shape (`head` plus three diff hashes plus the combined one) rather than the per-path content digest.

    It is a valid seal in the sense that it once satisfied `_validate_fingerprint`, and a state holding it still validates -- refusing it would wedge a run this correction lands under mid-flight, exactly the failure `TASK_OPTIONAL` exists to rule out elsewhere in this file. It cannot answer the restored-scope question the new shape exists for, because it is a diff against HEAD rather than per-path content read straight off the tree, so a task holding one is treated exactly as a task with no seal at all: it cannot park from a write-active status.
    """
    return isinstance(value, dict) and set(value) == FINGERPRINT_FIELDS


def _validate_task(task: Any, current_fingerprint: str, inherited: frozenset = frozenset()) -> List[str]:
    if not isinstance(task, dict) or set(task) - TASK_OPTIONAL != TASK_FIELDS:
        return [_field_set_error("Task must use the exact task field set", task, TASK_FIELDS, TASK_OPTIONAL)]
    if task.get("scope_fingerprint") is not None:
        errors_scope = _validate_fingerprint(task["scope_fingerprint"], f"Task {task.get('id', '?')} scope_fingerprint")
        if errors_scope:
            return errors_scope
    if task.get("dispatch_scope_fingerprint") is not None:
        seal = task["dispatch_scope_fingerprint"]
        label = f"Task {task.get('id', '?')} dispatch_scope_fingerprint"
        errors_dispatch = _validate_fingerprint(seal, label) if _is_legacy_dispatch_seal(seal) else _validate_scope_digest(seal, label)
        if errors_dispatch:
            return errors_dispatch
    errors: List[str] = []
    for key in ("id", "title", "completion_condition", "rationale"):
        if not isinstance(task.get(key), str) or not task[key].strip():
            errors.append(f"Task requires non-empty {key}")
    for key in ("scope", "verification_path"):
        value = task.get(key)
        if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
            errors.append(f"Task requires non-empty {key}")
    if task.get("status") not in TASK_STATUSES:
        errors.append("Task status is invalid")
    if type(task.get("round")) is not int or task["round"] < 0:
        errors.append("Task round must be non-negative")
    parked = task.get("parked")
    if task.get("status") == "parked":
        if not isinstance(parked, dict) or set(parked) != PARKED_FIELDS:
            errors.append(_field_set_error(f"Task {task.get('id', '?')} parked must use the exact field set", parked, PARKED_FIELDS))
        else:
            if not isinstance(parked.get("question"), str) or not parked["question"].strip():
                errors.append("Task parked requires a non-empty question")
            if parked.get("from") not in PARKED_FROM_VALUES:
                errors.append(f"Task parked.from must be one of {', '.join(sorted(PARKED_FROM_VALUES))}")
            decision_ref = parked.get("decision_ref")
            if decision_ref is not None and (not isinstance(decision_ref, str) or not decision_ref.strip()):
                errors.append("Task parked.decision_ref must be null or non-empty text")
            if not _valid_time(parked.get("at")):
                errors.append("Task parked requires a timezone-aware at")
    elif parked is not None:
        errors.append("Only a parked task may carry parked facts")
    verification = task.get("latest_verification")
    if not isinstance(verification, list):
        errors.append("Task latest_verification must be a list")
        verification = []
    else:
        for item in verification:
            errors.extend(_validate_verification(item))
    findings = task.get("unresolved_findings")
    errors.extend(_validate_findings(findings, task.get("completion_condition") if isinstance(task.get("completion_condition"), str) else None,
                                     inherited if task.get("status") != "accepted" else frozenset()))
    acceptance = task.get("acceptance")
    if acceptance is not None:
        if not isinstance(acceptance, dict) or set(acceptance) - ACCEPTANCE_OPTIONAL != ACCEPTANCE_FIELDS:
            errors.append(_field_set_error("Task acceptance must use the exact field set", acceptance, ACCEPTANCE_FIELDS, ACCEPTANCE_OPTIONAL))
        else:
            acceptance_fingerprint = acceptance.get("worktree_fingerprint", "")
            if not _valid_hash(acceptance_fingerprint):
                errors.append("Task acceptance requires a valid worktree fingerprint")
            reviewers = acceptance.get("reviewers")
            if not isinstance(reviewers, list):
                errors.append("Task acceptance reviewers must be a list")
                reviewers = []
            # The third disposition. A non-blocking finding may be fixed before acceptance: the executor corrects within its required_correction, the task's verification path is re-run on the corrected tree, and the lead reads that diff. No fresh lane -- the review that found it already happened, the finding does not touch whether the task is done, and the final audit reads the whole change again. So the verdicts stand at the fingerprint they reviewed, and the acceptance stands at the corrected one.
            fixed = acceptance.get("fixed")
            if fixed is None:
                fixed = []
            elif not isinstance(fixed, list):
                errors.append("Task acceptance fixed must be a list of findings")
                fixed = []
            else:
                errors.extend(_validate_findings(fixed, task.get("completion_condition") if isinstance(task.get("completion_condition"), str) else None))
                if _blocking(fixed):
                    errors.append("A finding that cites the completion condition cannot be fixed under the same review; it needs a correction round")
                if any(isinstance(f, dict) and f.get("carried_because") for f in fixed):
                    errors.append("A fixed finding carries no carried_because")
            reviewed = {r.get("worktree_fingerprint") for r in reviewers if isinstance(r, dict)}
            reviewed_fingerprint = next(iter(reviewed)) if len(reviewed) == 1 else acceptance_fingerprint
            if len(reviewed) > 1:
                errors.append("Task acceptance reviewers must all have read one fingerprint")
            if fixed and reviewed_fingerprint == acceptance_fingerprint:
                errors.append("Task acceptance records fixed findings but the tree the reviewers read is the tree accepted; nothing was fixed")
            if not fixed:
                reviewed_fingerprint = acceptance_fingerprint
            for reviewer in reviewers:
                errors.extend(_validate_verdict(reviewer, task.get("id", ""), task.get("round", -1), reviewed_fingerprint))
            current_verification = any(
                isinstance(item, dict) and item.get("exit_code") == 0
                and item.get("round") == task.get("round")
                and item.get("worktree_fingerprint") == acceptance_fingerprint
                for item in verification
            )
            if not current_verification:
                errors.append("Accepted task requires current-round verification")
            # `REVISE` accepts: its findings are real, carried on the task, and not about whether the task is done. Only `BLOCK` says that.
            current_pass = any(
                isinstance(item, dict) and item.get("verdict") in {"PASS", "REVISE"}
                and item.get("fresh") is True and item.get("independent") is True
                and item.get("round") == task.get("round")
                and item.get("worktree_fingerprint") == reviewed_fingerprint
                for item in reviewers
            )
            if not current_pass:
                errors.append("Accepted task requires a fresh independent PASS or REVISE")
            if any(isinstance(item, dict) and item.get("verdict") == "BLOCK" for item in reviewers):
                errors.append("Accepted task cannot retain a current BLOCK verdict")
            if acceptance.get("round") != task.get("round"):
                errors.append("Task acceptance does not match the current round")
            errors.extend(_verdict_coherence(reviewers, (findings if isinstance(findings, list) else []) + fixed))
    if task.get("status") == "accepted" and acceptance is None:
        errors.append("Accepted task requires acceptance facts")
    if task.get("status") == "accepted":
        if _blocking(findings):
            errors.append("Accepted task cannot retain a finding that blocks its completion condition")
        # Carrying is the disposition that costs the least now and the most later, so it is the one that owes a reason once the finding is above minor. The severity the role assigned finally has a consumer: it prices the carry, and it never gates the acceptance.
        if isinstance(findings, list) and any(
            isinstance(f, dict) and f.get("severity") in {"critical", "important"} and f.get("blocks") is None
            and not f.get("carried_because")
            for f in findings
        ):
            errors.append("Accepted task carrying an important or critical finding must record carried_because, fix it before acceptance, or promote it to a task")
    if task.get("status") != "accepted" and acceptance is not None:
        errors.append("Only an accepted task may retain acceptance facts")
    return errors


def _validate_amendments(input_value: Dict[str, Any]) -> List[str]:
    amendments = input_value.get("amendments")
    if amendments is None:
        return []
    if not isinstance(amendments, list):
        return ["Input amendments must be a list"]
    errors: List[str] = []
    previous_hash: Optional[str] = None
    for index, entry in enumerate(amendments):
        if not isinstance(entry, dict) or set(entry) != AMENDMENT_FIELDS:
            errors.append(_field_set_error(f"Amendment {index} must use the exact field set", entry, AMENDMENT_FIELDS))
            continue
        if not isinstance(entry.get("reason"), str) or not entry["reason"].strip():
            errors.append(f"Amendment {index} requires a non-empty reason")
        if not _valid_time(entry.get("at")):
            errors.append(f"Amendment {index} requires a timezone-aware at")
        if not _valid_hash(entry.get("from")) or not _valid_hash(entry.get("to")) or entry.get("from") == entry.get("to"):
            errors.append(f"Amendment {index} must move from one input hash to a different one")
        if previous_hash is not None and entry.get("from") != previous_hash:
            errors.append(f"Amendment {index} does not continue from the previous amendment")
        previous_hash = entry.get("to")
    if amendments and previous_hash != input_value.get("sha256"):
        errors.append("The last amendment must end at the input's current sha256; an input that moved again needs another `amend --reason`")
    return errors


def _amendment_transition_errors(previous: Any, candidate: Any) -> List[str]:
    """The input may move under a run, and only through an amendment that says why.

    A plan is edited while its run is live whenever an owner ruling or a factual correction lands in it, and refusing the run at that point restarts it for a ledger's worth of nothing: three phase-48 and phase-49 runs were aborted and reopened on the same tree for exactly this. The identity rule stays -- a candidate that moves the hash without the entry is still refused -- and the entry is what the receipt carries, so the reader who inherits the tree sees what the plan was approved as and what it became.
    """
    refusal = ["Transition cannot change input identity; `amend --reason` records why the input moved"]
    if not isinstance(previous, dict) or not isinstance(candidate, dict):
        return refusal
    for key in ("kind", "reference"):
        if previous.get(key) != candidate.get(key):
            return refusal
    before = previous.get("amendments") or []
    after = candidate.get("amendments") or []
    if len(after) != len(before) + 1 or after[:len(before)] != before:
        return refusal
    entry = after[-1]
    if not isinstance(entry, dict) or entry.get("from") != previous.get("sha256") or entry.get("to") != candidate.get("sha256"):
        return refusal
    return []


def validate_state(payload: Any, state_path: Path, inherited: frozenset = frozenset()) -> List[str]:
    del state_path
    if not isinstance(payload, dict):
        return ["State must be a JSON object"]
    errors: List[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        errors.append("State schema_version must be 1")
    if type(payload.get("revision")) is not int or payload["revision"] < 0:
        errors.append("State revision must be a non-negative integer")
    if payload.get("workflow") != "execute":
        errors.append("State workflow must be execute")
    if not isinstance(payload.get("run_id"), str) or not payload["run_id"]:
        errors.append("State requires a run_id")
    lifecycle = payload.get("lifecycle")
    if lifecycle in NONTERMINAL_LIFECYCLES:
        if set(payload) != NONTERMINAL_FIELDS:
            errors.append(_field_set_error("Nonterminal state must use the exact resumable field set", payload, NONTERMINAL_FIELDS))
            return errors
        if payload.get("phase") not in PHASES:
            errors.append("Nonterminal phase is invalid")
        if lifecycle == "blocked" and payload.get("phase") != "blocked":
            errors.append("Blocked lifecycle requires blocked phase")
        if lifecycle == "interrupted" and payload.get("phase") != "interrupted":
            errors.append("Interrupted lifecycle requires interrupted phase")
        if lifecycle == "active" and payload.get("phase") in {"blocked", "interrupted"}:
            errors.append("Active lifecycle cannot use blocked or interrupted phase")
        if not isinstance(payload.get("next_action"), str) or not payload["next_action"]:
            errors.append("Nonterminal state requires the exact next action")
        input_value = payload.get("input")
        if not isinstance(input_value, dict) or set(input_value) - INPUT_OPTIONAL != INPUT_FIELDS:
            errors.append(_field_set_error("Input must use the exact field set", input_value, INPUT_FIELDS, INPUT_OPTIONAL))
        else:
            errors.extend(_validate_amendments(input_value))
            if input_value.get("kind") not in {"plan", "brief"}:
                errors.append("Input kind must be plan or brief")
            if input_value.get("reference") is not None and not isinstance(input_value["reference"], str):
                errors.append("Input reference must be null or a path")
            if input_value.get("summary") is not None and not isinstance(input_value["summary"], str):
                errors.append("Input summary must be null or text")
            if not _valid_hash(input_value.get("sha256")):
                errors.append("Input requires a valid sha256")
            if input_value.get("kind") == "brief":
                if input_value.get("reference") is not None or not isinstance(input_value.get("summary"), str) or not input_value["summary"]:
                    errors.append("Brief input requires null reference and non-empty summary")
                elif _sha256_bytes(input_value["summary"].encode("utf-8")) != input_value.get("sha256"):
                    errors.append("Brief input sha256 must match the normalized summary")
            if input_value.get("kind") == "plan":
                if not isinstance(input_value.get("reference"), str) or not input_value["reference"] or input_value.get("summary") is not None:
                    errors.append("Plan input requires a reference and null summary")
        worktree = payload.get("worktree")
        current_fingerprint = ""
        if not isinstance(worktree, dict) or set(worktree) != WORKTREE_FIELDS:
            errors.append(_field_set_error("Worktree must use the exact field set", worktree, WORKTREE_FIELDS))
        else:
            for key in ("root", "git_common_dir"):
                if not isinstance(worktree.get(key), str) or not worktree[key]:
                    errors.append(f"Worktree requires non-empty {key}")
            errors.extend(_validate_fingerprint(worktree.get("baseline"), "Worktree baseline"))
            errors.extend(_validate_fingerprint(worktree.get("observed"), "Worktree observed"))
            if isinstance(worktree.get("observed"), dict):
                current_fingerprint = worktree["observed"].get("fingerprint", "")
        tasks = payload.get("tasks")
        if not isinstance(tasks, list) or not tasks:
            errors.append("Nonterminal state requires at least one task")
            tasks = []
        identifiers = []
        active_indexes = []
        for index, task in enumerate(tasks):
            errors.extend(_validate_task(task, current_fingerprint, inherited))
            if isinstance(task, dict):
                identifiers.append(task.get("id"))
                if task.get("status") in WRITE_ACTIVE_STATUSES:
                    active_indexes.append(index)
        if len(identifiers) != len(set(identifiers)):
            errors.append("Task ids must be unique")
        # Tasks are written at once only where their scopes do not meet, and never ahead of an earlier task whose scope meets theirs. Everything else about order is the plan's to say.
        if active_indexes and len(identifiers) == len(set(identifiers)):
            active_ids = [tasks[index]["id"] for index in active_indexes]
            for collision in _scope_collisions(tasks, active_ids):
                left, right = collision["tasks"]
                errors.append(f"{left} and {right} cannot both be under way: their scopes meet at {', '.join(collision['paths'])}")
        if payload.get("current_task_id") is not None and payload.get("current_task_id") not in identifiers:
            errors.append("current_task_id must identify a task")
        if type(payload.get("current_round")) is not int or payload["current_round"] < 0:
            errors.append("current_round must be non-negative")
        latest_verification = payload.get("latest_verification")
        if not isinstance(latest_verification, list):
            errors.append("latest_verification must be a list")
            latest_verification = []
        else:
            for item in latest_verification:
                errors.extend(_validate_verification(item, expected_fingerprint=current_fingerprint))
        final_audit = payload.get("final_audit")
        if not isinstance(final_audit, list):
            errors.append("final_audit must be a list")
            final_audit = []
        else:
            for verdict in final_audit:
                errors.extend(_validate_verdict(verdict, "whole-change", payload.get("current_round", -1), current_fingerprint))
        if payload.get("phase") == "regression_verifying" and latest_verification:
            if any(item.get("exit_code") != 0 for item in latest_verification if isinstance(item, dict)):
                errors.append("Regression verification evidence must pass")
        errors.extend(_validate_findings(payload.get("unresolved_findings"), inherited=inherited if payload.get("phase") != "final_audit" else frozenset()))
        if payload.get("phase") == "final_audit" and _blocking(payload.get("unresolved_findings")):
            errors.append("Final audit cannot retain a blocking finding")
    elif lifecycle == "completed":
        if set(payload) != COMPLETED_FIELDS:
            errors.append(_field_set_error("Completed receipt must use the exact compact field set", payload, COMPLETED_FIELDS))
            return errors
        if not _valid_time(payload.get("completed_at")):
            errors.append("Completed receipt requires timezone-aware completed_at")
        compact_input = payload.get("input")
        if not isinstance(compact_input, dict) or set(compact_input) - INPUT_OPTIONAL != COMPLETED_INPUT_FIELDS:
            errors.append("Completed input must use the exact compact field set")
        elif not _valid_hash(compact_input.get("sha256")):
            errors.append("Completed input requires a valid sha256")
        compact_worktree = payload.get("worktree")
        fingerprint = ""
        if not isinstance(compact_worktree, dict) or set(compact_worktree) != COMPLETED_WORKTREE_FIELDS:
            errors.append("Completed worktree must use the exact compact field set")
        else:
            fingerprint = compact_worktree.get("final_fingerprint", "")
            if not _valid_hash(fingerprint):
                errors.append("Completed worktree requires a final fingerprint")
        accepted_tasks = payload.get("accepted_tasks")
        if not isinstance(accepted_tasks, list) or not accepted_tasks:
            errors.append("Completed receipt requires accepted task summaries")
        else:
            accepted_ids = []
            for task in accepted_tasks:
                if not isinstance(task, dict) or set(task) - ACCEPTED_TASK_OPTIONAL != ACCEPTED_TASK_FIELDS:
                    errors.append("Accepted task summary must use the exact compact field set")
                    continue
                accepted_ids.append(task.get("id"))
                for key in ACCEPTED_TASK_FIELDS - {"carried_findings"}:
                    if not isinstance(task.get(key), str) or not task[key].strip():
                        errors.append(f"Accepted task summary requires non-empty {key}")
                errors.extend(_validate_findings(task.get("carried_findings"), task.get("completion_condition")))
                if task.get("fixed_findings") is not None:
                    errors.extend(_validate_findings(task.get("fixed_findings"), task.get("completion_condition")))
                if _blocking(task.get("carried_findings")):
                    errors.append("Accepted task summary cannot carry a blocking finding")
            if len(accepted_ids) != len(set(accepted_ids)):
                errors.append("Accepted task summary ids must be unique")
        final_verification = payload.get("final_verification")
        if not isinstance(final_verification, list) or not final_verification:
            errors.append("Completed receipt requires final verification")
        else:
            for item in final_verification:
                errors.extend(_validate_verification(item, expected_fingerprint=fingerprint))
            if any(not isinstance(item, dict) or item.get("exit_code") != 0 for item in final_verification):
                errors.append("Completed receipt requires passing final verification")
        errors.extend(_validate_findings(payload.get("carried_findings")))
        if _blocking(payload.get("carried_findings")):
            errors.append("Completed receipt cannot carry a blocking finding")
        final_audit = payload.get("final_audit")
        if not isinstance(final_audit, list) or not final_audit:
            errors.append("Completed receipt requires final audit PASS facts")
        else:
            for verdict in final_audit:
                round_number = verdict.get("round", -1) if isinstance(verdict, dict) else -1
                errors.extend(_validate_verdict(verdict, "whole-change", round_number, fingerprint))
                if isinstance(verdict, dict) and not (
                    verdict.get("verdict") == "PASS" and verdict.get("fresh") is True and verdict.get("independent") is True
                ):
                    errors.append("Final audit requires fresh independent PASS verdicts")
    elif lifecycle == "aborted":
        if set(payload) != ABORTED_FIELDS:
            errors.append(_field_set_error("Aborted receipt must use the exact compact field set", payload, ABORTED_FIELDS))
            return errors
        if not _valid_time(payload.get("aborted_at")):
            errors.append("Aborted receipt requires timezone-aware aborted_at")
        for key in ("worktree_root", "reason"):
            if not isinstance(payload.get(key), str) or not payload[key]:
                errors.append(f"Aborted receipt requires non-empty {key}")
    else:
        errors.append("State lifecycle is invalid")
    return errors


def validate_transition(previous: Optional[Dict[str, Any]], candidate: Dict[str, Any]) -> List[str]:
    inherited = _legacy_findings(previous) if previous is not None else frozenset()
    errors = validate_state(candidate, Path("state.json"), inherited)
    if previous is None:
        if candidate.get("revision") != 0:
            errors.append("Initial state revision must be zero")
        if candidate.get("lifecycle") not in NONTERMINAL_LIFECYCLES:
            errors.append("Initial checkpoint must be nonterminal")
        # There is no predecessor for the per-task loop below to read, so nothing there ever runs against an initial checkpoint; a hand-authored one could otherwise declare a task already `implementing` with a forged seal, or already `parked` from a write-active status that never happened, since neither `dispatch` nor a restored scope can have occurred before the first checkpoint exists. So here, directly: no task may carry `dispatch_scope_fingerprint`, and a `parked` task's `parked.from` must equal `pending`.
        for task in candidate.get("tasks", []) if isinstance(candidate.get("tasks"), list) else []:
            if not isinstance(task, dict):
                continue
            task_id = task.get("id", "?")
            if task.get("dispatch_scope_fingerprint") is not None:
                errors.append(f"{task_id} cannot carry a seal on the initial checkpoint; nothing has dispatched it yet")
            if task.get("status") == "parked":
                parked_info = task.get("parked")
                from_status = parked_info.get("from") if isinstance(parked_info, dict) else None
                if from_status != "pending":
                    errors.append(f"{task_id} cannot park from {from_status} on the initial checkpoint; nothing has dispatched it yet")
        return errors
    previous_errors = validate_state(previous, Path("state.json"), inherited)
    if candidate.get("lifecycle") == "completed" and _blocking(previous.get("unresolved_findings")):
        errors.append("Completion cannot retain a blocking finding")
    if previous_errors:
        return [f"Previous state is invalid: {error}" for error in previous_errors] + errors
    for key in ("schema_version", "workflow", "run_id"):
        if previous.get(key) != candidate.get(key):
            errors.append(f"Transition cannot change {key}")
    if candidate.get("revision") != previous.get("revision", -1) + 1:
        errors.append("Candidate revision does not match the current predecessor")
    if previous.get("lifecycle") in TERMINAL_LIFECYCLES:
        errors.append("Terminal state cannot transition")
        return errors
    if candidate.get("lifecycle") in NONTERMINAL_LIFECYCLES:
        if previous.get("input") != candidate.get("input"):
            errors.extend(_amendment_transition_errors(previous.get("input"), candidate.get("input")))
        if previous.get("worktree", {}).get("root") != candidate.get("worktree", {}).get("root"):
            errors.append("Transition cannot change canonical worktree")
        previous_phase = previous.get("phase")
        candidate_phase = candidate.get("phase")
        if candidate_phase not in PHASE_TRANSITIONS.get(previous_phase, frozenset()):
            errors.append(f"Phase transition {previous_phase} -> {candidate_phase} is not allowed")
        previous_task_list = previous.get("tasks", [])
        candidate_task_list = candidate.get("tasks", [])
        previous_ids = [task.get("id") for task in previous_task_list if isinstance(task, dict)]
        candidate_ids = [task.get("id") for task in candidate_task_list if isinstance(task, dict)]
        if candidate_ids[:len(previous_ids)] != previous_ids:
            errors.append("Existing tasks cannot be removed or reordered")
        for appended in candidate_task_list[len(previous_ids):]:
            if not isinstance(appended, dict) or appended.get("status") != "pending" or appended.get("round") != 0:
                errors.append("Newly appended tasks must begin pending at round zero")
        previous_tasks = {task["id"]: task for task in previous_task_list if isinstance(task, dict) and "id" in task}
        for task in candidate.get("tasks", []):
            if not isinstance(task, dict) or task.get("id") not in previous_tasks:
                continue
            old = previous_tasks[task["id"]]
            old_status = old.get("status")
            new_status = task.get("status")
            if new_status not in TASK_TRANSITIONS.get(old_status, frozenset()):
                errors.append(f"Task status transition {old_status} -> {new_status} is not allowed")
            old_round = old.get("round", 0)
            new_round = task.get("round", 0)
            entering_correction = new_status == "correcting" and old_status != "correcting"
            initial_dispatch = old_status == "pending" and new_status == "implementing"
            allowed_rounds = {old_round, old_round + 1} if initial_dispatch else ({old_round + 1} if entering_correction else {old_round})
            if new_round not in allowed_rounds:
                errors.append("Task round does not match its status transition")
            if entering_correction:
                if task.get("acceptance") is not None:
                    errors.append("Correction must clear previous acceptance")
                if task.get("latest_verification"):
                    errors.append("Correction must clear previous verification")
            if old.get("scope") != task.get("scope") or old.get("completion_condition") != task.get("completion_condition"):
                errors.append("Existing task scope and completion condition cannot change during execution")
            if new_status == "accepted" and old_status != "accepted":
                scoped = task.get("scope_fingerprint")
                expected = scoped.get("fingerprint") if isinstance(scoped, dict) else None
                if expected is not None and isinstance(task.get("acceptance"), dict) and task["acceptance"].get("worktree_fingerprint") != expected:
                    errors.append(f"{task['id']} acceptance must match its scope fingerprint at this checkpoint; the scope moved after review")
            # `dispatch_scope_fingerprint` may change on exactly two transitions: `pending -> implementing`, where `dispatch` (or `_autofill`, for any candidate that leaves it unfilled) seals it fresh, and `parked -> pending`, where `unpark` drops it so the next dispatch seals again. Every other transition must carry it forward unchanged -- explicitly including `accepted -> correcting`, which is not a write-active status and so was once missed here, the gap a forged seal could pass through unchecked.
            seal_may_change = (old_status == "pending" and new_status == "implementing") or (old_status == "parked" and new_status == "pending")
            if not seal_may_change and old.get("dispatch_scope_fingerprint") != task.get("dispatch_scope_fingerprint"):
                errors.append(f"{task['id']} dispatch_scope_fingerprint cannot change except when dispatched or unparked")
            if new_status == "parked" and old_status != "parked":
                parked_info = task.get("parked")
                if isinstance(parked_info, dict) and parked_info.get("from") != old_status:
                    errors.append(f"{task['id']} parked.from must record the status it parked from ({old_status})")
                # Parking clears the task's own review state: the round is unchanged, but nothing it carried from before is still current once the tree it was measured against is gone.
                if task.get("latest_verification"):
                    errors.append(f"{task['id']} parking must clear previous verification")
                # `pending -> parked` needs no restored-scope check: a pending task was never dispatched and holds no writes by construction. `implementing | correcting -> parked` is the one that can hold a partial write, and whether its content is actually restored needs the live worktree, which this function does not read -- `validate_external_state` makes that comparison and raises there. A task with no seal at all, or with one written before this correction (`worktree_fingerprint`'s diff-shaped fields rather than the per-path content digest, which cannot answer the restored-scope question either), is refused here instead; it never restores from a write-active status at all.
                old_seal = old.get("dispatch_scope_fingerprint")
                if old_status in {"implementing", "correcting"} and (not isinstance(old_seal, dict) or _is_legacy_dispatch_seal(old_seal)):
                    errors.append(f"{task['id']} cannot park from {old_status}: it was dispatched without a seal")
        if candidate_phase in {"simplifying", "regression_verifying", "final_audit"} and any(
            isinstance(task, dict) and task.get("status") == "parked" for task in candidate_task_list
        ):
            errors.append(f"Cannot enter {candidate_phase} while a task is parked")
        previous_fingerprint = previous.get("worktree", {}).get("observed", {}).get("fingerprint")
        candidate_fingerprint = candidate.get("worktree", {}).get("observed", {}).get("fingerprint")
        fingerprint_changed = previous_fingerprint != candidate_fingerprint
        if previous_phase == "simplifying" and fingerprint_changed and candidate_phase != "regression_verifying":
            errors.append("Simplifier mutation must enter regression_verifying")
        if previous_phase == "final_audit" and fingerprint_changed:
            if candidate.get("final_audit"):
                errors.append("Post-audit mutation must clear final audit verdicts")
            if candidate_phase not in {"task", "regression_verifying"}:
                errors.append("Post-audit mutation must return to verification")
    if candidate.get("lifecycle") == "completed":
        if any(task.get("status") != "accepted" for task in previous.get("tasks", [])):
            errors.append("Completion requires every task accepted")
        final_fingerprint = candidate.get("worktree", {}).get("final_fingerprint")
        expected_input = {
            "reference": previous.get("input", {}).get("reference"),
            "sha256": previous.get("input", {}).get("sha256"),
        }
        if previous.get("input", {}).get("amendments"):
            expected_input["amendments"] = previous["input"]["amendments"]
        if candidate.get("input") != expected_input:
            errors.append("Completed input must exactly project checkpointed input identity")
        if candidate.get("worktree", {}).get("root") != previous.get("worktree", {}).get("root"):
            errors.append("Completed worktree root must match the checkpointed canonical worktree")
        if final_fingerprint != previous.get("worktree", {}).get("observed", {}).get("fingerprint"):
            errors.append("Completion must retain the final audited fingerprint")
        if previous.get("phase") != "final_audit":
            errors.append("Completion requires a checkpointed final_audit phase")
        previous_verification = previous.get("latest_verification", [])
        if not any(
            isinstance(item, dict) and item.get("exit_code") == 0
            and item.get("worktree_fingerprint") == final_fingerprint
            for item in previous_verification
        ):
            errors.append("Completion requires checkpointed final verification")
        previous_audit = previous.get("final_audit", [])
        if not previous_audit or any(
            not isinstance(item, dict) or item.get("verdict") != "PASS"
            or item.get("fresh") is not True or item.get("independent") is not True
            or item.get("worktree_fingerprint") != final_fingerprint
            for item in previous_audit
        ):
            errors.append("Completion requires checkpointed final audit PASS")
        expected_tasks = [
            {**{key: task.get(key) for key in ACCEPTED_TASK_FIELDS - {"carried_findings"}},
             "carried_findings": task.get("unresolved_findings", []),
             **({"fixed_findings": task["acceptance"]["fixed"]} if isinstance(task.get("acceptance"), dict) and task["acceptance"].get("fixed") else {})}
            for task in previous.get("tasks", [])
        ]
        if candidate.get("accepted_tasks") != expected_tasks:
            errors.append("Completed task summaries must exactly project accepted tasks and what each carries")
        if candidate.get("carried_findings") != previous.get("unresolved_findings", []):
            errors.append("Completed carried findings must exactly project the checkpointed whole-change findings")
        if candidate.get("final_verification") != previous_verification:
            errors.append("Completed verification must exactly match checkpointed final verification")
        if candidate.get("final_audit") != previous_audit:
            errors.append("Completed audit must exactly match checkpointed final audit")
    return errors


def _load(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError("State must be a JSON object")
    return value


def find_occupying_run(run_root: Path, worktree: Path, exclude: Optional[Path] = None) -> Optional[Path]:
    canonical, _ = canonical_worktree(worktree)
    excluded = exclude.resolve() if exclude is not None else None
    claim_path = _global_claim_path(canonical)
    try:
        recorded_path = Path(claim_path.read_text().strip()).resolve()
        if recorded_path != excluded:
            payload = _load(recorded_path)
            if payload.get("lifecycle") in NONTERMINAL_LIFECYCLES and Path(payload.get("worktree", {}).get("root", "")).resolve() == canonical:
                return recorded_path
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
        pass
    for state_path in sorted(run_root.glob("execute/*/state.json")):
        if excluded is not None and state_path.resolve() == excluded:
            continue
        try:
            payload = _load(state_path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
            continue
        if payload.get("lifecycle") in NONTERMINAL_LIFECYCLES:
            recorded = payload.get("worktree", {}).get("root")
            if isinstance(recorded, str) and Path(recorded).resolve() == canonical:
                return state_path
    return None


@contextmanager
def _worktree_claim(run_root: Path, worktree: Path):
    del run_root
    canonical, _ = canonical_worktree(worktree)
    lock_root = Path(tempfile.gettempdir()) / f"kein-execute-{os.getuid()}"
    lock_root.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(_global_claim_path(canonical), os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield descriptor
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _global_claim_path(canonical: Path) -> Path:
    lock_root = Path(tempfile.gettempdir()) / f"kein-execute-{os.getuid()}"
    lock_root.mkdir(parents=True, exist_ok=True)
    return lock_root / (hashlib.sha256(str(canonical).encode("utf-8")).hexdigest() + ".lock")


def _record_claim(descriptor: int, state_path: Optional[Path]) -> None:
    value = b"" if state_path is None else str(state_path.resolve()).encode("utf-8") + b"\n"
    os.lseek(descriptor, 0, os.SEEK_SET)
    os.ftruncate(descriptor, 0)
    if value:
        os.write(descriptor, value)
    os.fsync(descriptor)


def _claimed_state(descriptor: int) -> Optional[Path]:
    os.lseek(descriptor, 0, os.SEEK_SET)
    value = os.read(descriptor, 65536).decode("utf-8").strip()
    return Path(value).resolve() if value else None


def reconcile(state_path: Path) -> Dict[str, Any]:
    payload = _load(state_path)
    errors = validate_state(payload, state_path, _legacy_findings(payload))
    if errors:
        return {"valid": False, "errors": errors, "input_matches": False, "worktree_matches": False, "required_action": "repair invalid state before resuming"}
    if payload["lifecycle"] in TERMINAL_LIFECYCLES:
        return {"valid": True, "errors": [], "input_matches": True, "worktree_matches": True, "required_action": "terminal receipt requires no resume action"}
    input_value = payload["input"]
    input_matches = True
    if input_value["reference"] is not None:
        input_path = Path(input_value["reference"])
        input_matches = input_path.is_file() and _sha256_bytes(input_path.read_bytes()) == input_value["sha256"]
    try:
        observed = worktree_fingerprint(Path(payload["worktree"]["root"]))
        worktree_matches = observed["fingerprint"] == payload["worktree"]["observed"]["fingerprint"]
    except (OSError, ValueError):
        worktree_matches = False
    if not input_matches:
        action = "the input changed under the run: `amend --reason` it if the change was authorized, otherwise block"
    elif not worktree_matches:
        action = "inspect and verify partial worktree changes before choosing a safe continuation"
    else:
        action = payload["next_action"]
    return {"valid": True, "errors": [], "input_matches": input_matches, "worktree_matches": worktree_matches, "required_action": action}


AUTO = "auto"


def _autofill(candidate: Dict[str, Any], destination: Path, root: Optional[Path]) -> None:
    """Fill in the parts of a candidate that are derived rather than decided.

    Every value here is already computable from the predecessor and the worktree, and the checkpoint
    recomputes all of them to check the candidate anyway. Asking the author for them creates one way
    to be wrong per field and no way to be right that the file does not already determine -- and the
    combined fingerprint alone is repeated in the observed fingerprint, the latest verification, each
    task's verification and acceptance, every verdict, and the final audit.

    `revision` is filled from an unlocked read on purpose. If another run checkpoints before the lock
    is taken, the filled number is stale and `validate_transition` refuses it, which is exactly what
    the counter exists for. Re-deriving it under the lock would let content authored against an older
    state overwrite a newer one, which is the failure the counter was added to prevent.
    """
    if candidate.get("revision") == AUTO or "revision" not in candidate:
        previous = _load(destination) if destination.exists() else None
        candidate["revision"] = 0 if previous is None else previous.get("revision", -1) + 1
    if root is None:
        return
    prints = worktree_fingerprint(root)
    worktree = candidate.get("worktree")
    if isinstance(worktree, dict):
        if worktree.get("observed") == AUTO:
            worktree["observed"] = prints
        # The baseline is what the run started against and must not move, so it fills only where there
        # is nothing to move away from. `"auto"` on any later checkpoint is refused rather than
        # silently re-derived, which would erase the drift the baseline exists to expose.
        if worktree.get("baseline") == AUTO and not destination.exists():
            worktree["baseline"] = prints
    combined = prints["fingerprint"]

    # A walk rather than a list of the places it appears: the set of sites grew with the schema and
    # would have to be maintained alongside it, and a site the list forgot fails as a bad candidate
    # rather than as a missing case.
    def fill(node: Any, value_for_auto: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key in {"worktree_fingerprint", "final_fingerprint"} and value == AUTO:
                    node[key] = value_for_auto
                else:
                    fill(value, value_for_auto)
        elif isinstance(node, list):
            for item in node:
                fill(item, value_for_auto)

    # Inside a task, "auto" is the task's scope fingerprint: recomputed at every checkpoint while the task is open, sealed once it is accepted, and absent only on a task recorded before the field existed, where the whole tree stands in as it always did.
    tasks = candidate.get("tasks")
    if isinstance(tasks, list):
        previous_state = _load(destination) if destination.exists() else None
        previous_tasks = (previous_state or {}).get("tasks", [])
        sealed = {task.get("id") for task in previous_tasks
                  if isinstance(task, dict) and task.get("status") == "accepted"}
        previous_status = {task.get("id"): task.get("status") for task in previous_tasks
                            if isinstance(task, dict) and "id" in task}
        for task in tasks:
            if not isinstance(task, dict):
                continue
            scope = task.get("scope")
            scoped_ok = isinstance(scope, list) and scope and all(isinstance(entry, str) and entry for entry in scope)
            # Recomputed for every task the previous checkpoint had not accepted, which includes the one being accepted now: the acceptance binds to the scope as it is at this checkpoint, not as it was when the reviewer read it, and the two differing is the refusal.
            if task.get("id") not in sealed or task.get("scope_fingerprint") == AUTO:
                if scoped_ok:
                    task["scope_fingerprint"] = worktree_fingerprint(root, list(scope))
            # `dispatch_scope_fingerprint` fills from `_scope_content_digest`, read fresh from the worktree right now -- not from `scope_fingerprint`, which is a diff against HEAD and moves for reasons that have nothing to do with this task's own content. This is what makes `dispatch` a seal that happens before any executor is dispatched: the CLI command reads the worktree, writes the checkpoint, and only then is the executor told to start, so the value captured here is the task's content at that moment. `validate_external_state` re-derives it the same way at every `pending -> implementing` checkpoint and refuses a candidate whose literal value does not match, and `validate_transition` refuses any later candidate that tries to change it while the task stays write-active, so a stale `"auto"` re-derivation on an already-sealed task fails as a changed field rather than silently re-sealing over a partial write. It also fills a `pending -> implementing` candidate that never mentioned the field at all: Decision 2 means every fresh dispatch to seal, and `dispatch` is the documented route to it, but a hand-authored `checkpoint` reaching the same transition must not quietly produce a task that can never park -- only a task already `implementing` before this checkpoint, or one carrying a seal in the pre-correction shape, is treated as dispatched without a seal.
            seal = task.get("dispatch_scope_fingerprint")
            freshly_dispatched = previous_status.get(task.get("id")) == "pending" and task.get("status") == "implementing"
            if scoped_ok and (seal == AUTO or (freshly_dispatched and not isinstance(seal, dict))):
                task["dispatch_scope_fingerprint"] = _scope_content_digest(root, list(scope))
            scoped = task.get("scope_fingerprint")
            fill(task, scoped["fingerprint"] if isinstance(scoped, dict) and _valid_hash(scoped.get("fingerprint")) else combined)
    fill(candidate, combined)


def checkpoint(destination: Path, candidate_path: Path) -> None:
    _promote(destination, _load(candidate_path))


def _promote(destination: Path, candidate: Dict[str, Any]) -> None:
    _root_value = candidate.get("worktree", {}).get("root") if isinstance(candidate.get("worktree"), dict) else candidate.get("worktree_root")
    _autofill(candidate, destination, Path(_root_value) if isinstance(_root_value, str) else None)
    candidate_errors = validate_state(candidate, destination, _legacy_findings(_load(destination)) if destination.exists() else frozenset())
    if candidate_errors:
        raise ValueError("; ".join(candidate_errors))
    lifecycle = candidate["lifecycle"]
    root_value = candidate.get("worktree", {}).get("root") if isinstance(candidate.get("worktree"), dict) else candidate.get("worktree_root")
    root = Path(root_value) if isinstance(root_value, str) else None
    run_root = destination.parent.parent.parent if destination.parent.parent.name == "execute" else destination.parent

    def validate_external_state() -> None:
        if lifecycle in NONTERMINAL_LIFECYCLES:
            assert root is not None
            actual_root, actual_common = canonical_worktree(root)
            if str(actual_root) != candidate["worktree"]["root"] or str(actual_common) != candidate["worktree"]["git_common_dir"]:
                raise ValueError("Candidate does not match the canonical worktree")
            actual = worktree_fingerprint(root)
            if actual != candidate["worktree"]["observed"]:
                raise ValueError("Candidate observed fingerprint does not match the worktree")
            reference = candidate["input"]["reference"]
            if reference is not None:
                path = Path(reference)
                if not path.is_file() or _sha256_bytes(path.read_bytes()) != candidate["input"]["sha256"]:
                    raise ValueError("Candidate input hash does not match")
            occupant = find_occupying_run(run_root, root, exclude=destination)
            if occupant is not None:
                raise ValueError(f"Canonical worktree is occupied by {occupant}")
            # Two checks that need the live worktree, which `validate_transition` never reads because it is a pure function over two JSON payloads. Both re-derive `_scope_content_digest` the same way `_autofill` does, so a legitimate candidate (built through `dispatch` or `park`, or copied forward unchanged) always agrees with what is read here, and only a hand-authored value that does not match the actual tree is refused.
            previous_for_scope = _load(destination) if destination.exists() else None
            previous_tasks_by_id = {t["id"]: t for t in (previous_for_scope or {}).get("tasks", []) if isinstance(t, dict) and "id" in t}
            for task in candidate.get("tasks", []):
                if not isinstance(task, dict):
                    continue
                old_task = previous_tasks_by_id.get(task.get("id"))
                if old_task is None:
                    continue
                old_status, new_status, scope = old_task.get("status"), task.get("status"), task.get("scope")
                if not isinstance(scope, list):
                    continue
                # A `pending -> implementing` checkpoint may carry a `dispatch_scope_fingerprint` that is absent (the legacy path, case (c)) or exactly what this checkpoint computes; nothing else, so a candidate cannot forge a seal or carry one held over from a stale read.
                if old_status == "pending" and new_status == "implementing" and task.get("dispatch_scope_fingerprint") is not None:
                    fresh = _scope_content_digest(root, scope)
                    if fresh != task["dispatch_scope_fingerprint"]:
                        raise ValueError(f"{task['id']} dispatch_scope_fingerprint does not match the scope's content at this checkpoint")
                # `implementing | correcting -> parked` may leave only once the scope's actual content is back at what `dispatch` sealed; `validate_transition` already refused a task with no seal, or a legacy-shaped one, to compare against.
                if new_status == "parked" and old_status in {"implementing", "correcting"}:
                    dispatched_scope = old_task.get("dispatch_scope_fingerprint")
                    if isinstance(dispatched_scope, dict) and not _is_legacy_dispatch_seal(dispatched_scope):
                        differing = _scope_digest_diff(_scope_content_digest(root, scope), dispatched_scope)
                        if differing:
                            raise ValueError(f"{task['id']} cannot park from {old_status}: {', '.join(differing)} still differs from its dispatch content")
        elif lifecycle == "completed":
            assert root is not None
            actual = worktree_fingerprint(root)["fingerprint"]
            if actual != candidate["worktree"]["final_fingerprint"]:
                raise ValueError("Completed fingerprint does not match the worktree")

    def atomic_write() -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary_path: Optional[Path] = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", dir=destination.parent, prefix=f".{destination.name}-", suffix=".tmp", delete=False) as temporary:
                temporary_path = Path(temporary.name)
                json.dump(candidate, temporary, indent=2, sort_keys=True)
                temporary.write("\n")
                temporary.flush()
                os.fsync(temporary.fileno())
            os.replace(temporary_path, destination)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()

    def validate_current_transition() -> None:
        previous = _load(destination) if destination.exists() else None
        errors = validate_transition(previous, candidate)
        if errors:
            raise ValueError("; ".join(errors))

    if root is not None:
        with _worktree_claim(run_root, root) as claim:
            claimed = _claimed_state(claim)
            if claimed is not None and claimed != destination.resolve():
                try:
                    claimed_payload = _load(claimed)
                    claimed_active = claimed_payload.get("lifecycle") in NONTERMINAL_LIFECYCLES
                except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
                    claimed_active = False
                if claimed_active:
                    raise ValueError(f"Canonical worktree is occupied by {claimed}")
            validate_current_transition()
            validate_external_state()
            atomic_write()
            _record_claim(claim, destination if lifecycle in NONTERMINAL_LIFECYCLES else None)
    else:
        validate_current_transition()
        validate_external_state()
        atomic_write()


SLUG_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")


def mint_run_dir(run_root: Path, slug: str) -> Path:
    """Build the run directory name so the caller does not have to read a clock.

    `run_id` is the directory name, so the lead was left assembling `<YYMMDD-HHMMSS>-<slug>` in
    the shell -- which is a compound command, and a worktree-isolated session refuses those.
    """
    if not SLUG_PATTERN.match(slug):
        raise ValueError("Slug must start alphanumeric and hold only letters, digits, dot, dash, underscore")
    return run_root / f"{datetime.now().astimezone():%y%m%d-%H%M%S}-{slug}"


def _resolve_start_destination(args: Any) -> Path:
    minted = args.run_root is not None or args.slug is not None
    if args.destination is not None and minted:
        raise ValueError("Pass a state.json path or --run-root with --slug, not both")
    if not minted:
        if args.destination is None:
            raise ValueError("start needs a state.json path, or --run-root with --slug")
        return args.destination
    if args.run_root is None or args.slug is None:
        raise ValueError("--run-root and --slug are used together")
    return mint_run_dir(args.run_root, args.slug) / "state.json"


TASK_AUTHORED_FIELDS = frozenset({
    "id", "title", "scope", "completion_condition", "verification_path", "rationale",
})


def _load_tasks(path: Path) -> List[Dict[str, Any]]:
    """The ledger the lead writes, and the five fields per task it does not.

    `task-ledger-template.md` shows an eleven-field task, six of which are the lead's and five of
    which are a run's opening position -- pending, round zero, no verification, no findings, no
    acceptance. Copying those five per task was the shape a first checkpoint had to get exactly
    right before anything else could happen.
    """
    payload = json.loads(path.read_text())
    if isinstance(payload, dict) and "tasks" in payload:
        payload = payload["tasks"]
    if not isinstance(payload, list) or not payload:
        raise ValueError("Tasks must be a non-empty JSON array, or an object carrying one under `tasks`")
    tasks: List[Dict[str, Any]] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValueError(f"Task {index} must be an object")
        missing = sorted(TASK_AUTHORED_FIELDS - set(item))
        unexpected = sorted(set(item) - TASK_AUTHORED_FIELDS)
        if missing or unexpected:
            raise ValueError(
                f"Task {item.get('id', index)} must carry exactly {sorted(TASK_AUTHORED_FIELDS)}"
                + (f"; missing {missing}" if missing else "")
                + (f"; unexpected {unexpected}" if unexpected else "")
            )
        tasks.append({**item, "status": "pending", "round": 0,
                      "latest_verification": [], "unresolved_findings": [], "acceptance": None,
                      "scope_fingerprint": AUTO})
    return tasks


def start(destination: Path, kind: str, reference: Optional[Path], summary: Optional[str],
          declared_status: Optional[str], worktree: Path, tasks_path: Path,
          next_action: Optional[str]) -> None:
    if destination.exists():
        raise ValueError(f"{destination} already exists; a run is started once")
    root, common = canonical_worktree(worktree)
    if kind == "plan":
        if reference is None:
            raise ValueError("A plan input needs --input <path>")
        if summary is not None:
            raise ValueError("A plan input carries no --summary; the reference is the input")
        digest = _sha256_bytes(reference.read_bytes())
        reference_value: Optional[str] = str(reference)
        summary_value: Optional[str] = None
    else:
        if summary is None:
            raise ValueError("A brief input needs --summary <text>")
        if reference is not None:
            raise ValueError("A brief input carries no --input; the summary is the input")
        digest = _sha256_bytes(summary.encode("utf-8"))
        reference_value, summary_value = None, summary
    tasks = _load_tasks(tasks_path)
    _promote(destination, {
        "schema_version": SCHEMA_VERSION,
        "revision": AUTO,
        "workflow": "execute",
        "run_id": destination.parent.name,
        "lifecycle": "active",
        "input": {"kind": kind, "reference": reference_value, "summary": summary_value,
                  "sha256": digest, "declared_status": declared_status},
        "worktree": {"root": str(root), "git_common_dir": str(common),
                     "baseline": AUTO, "observed": AUTO},
        "phase": "initializing",
        "tasks": tasks,
        "current_task_id": tasks[0]["id"],
        "current_round": 0,
        "latest_verification": [],
        "unresolved_findings": [],
        "final_audit": [],
        "next_action": next_action or f"dispatch {tasks[0]['id']} to an Executor",
    })


def amend(destination: Path, reason: str, summary: Optional[str], next_action: Optional[str]) -> None:
    from datetime import datetime
    state = _load(destination)
    if state.get("lifecycle") in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    if not reason.strip():
        raise ValueError("An amendment needs a reason")
    input_value = state.get("input", {})
    candidate = copy.deepcopy(state)
    if input_value.get("kind") == "plan":
        if summary is not None:
            raise ValueError("A plan input is amended by editing the plan; there is no --summary")
        reference = Path(input_value["reference"])
        if not reference.is_file():
            raise ValueError(f"Plan input {reference} is not a file")
        digest = _sha256_bytes(reference.read_bytes())
    else:
        if summary is None:
            raise ValueError("A brief input is amended with --summary <new text>")
        digest = _sha256_bytes(summary.encode("utf-8"))
        candidate["input"]["summary"] = summary
    if digest == input_value.get("sha256"):
        raise ValueError("Input is unchanged; nothing to amend")
    candidate["revision"] = AUTO
    candidate["worktree"]["observed"] = AUTO
    candidate["input"]["sha256"] = digest
    candidate["input"]["amendments"] = list(input_value.get("amendments") or []) + [{
        "at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "reason": reason.strip(),
        "from": input_value.get("sha256"),
        "to": digest,
    }]
    candidate["next_action"] = next_action or "reassess the remaining tasks against the amended input, then continue"
    _promote(destination, candidate)


def _named_tasks(state: Dict[str, Any], task_ids: List[str]) -> Dict[str, Dict[str, Any]]:
    by_id = {task["id"]: task for task in state.get("tasks", []) if isinstance(task, dict) and "id" in task}
    unknown = [task_id for task_id in task_ids if task_id not in by_id]
    if unknown:
        raise ValueError(f"no such task: {', '.join(unknown)}")
    if len(set(task_ids)) != len(task_ids):
        raise ValueError("a task is named twice")
    return by_id


def dispatch(destination: Path, task_ids: List[str], next_action: Optional[str]) -> None:
    """`pending -> implementing`, sealing `dispatch_scope_fingerprint` before any executor is dispatched.

    This command is the seal: it reads the worktree and writes the checkpoint synchronously, and only once it has returned does the lead tell an executor to start writing that task's scope. Nothing else orders those two events, so a lead that dispatches the executor first and runs this afterward has already broken the guarantee -- the ledger contract states the order because the state machine cannot enforce it from here.
    """
    state = _load(destination)
    if state.get("lifecycle") in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    by_id = _named_tasks(state, task_ids)
    for task_id in task_ids:
        status = by_id[task_id].get("status")
        if status != "pending":
            raise ValueError(f"{task_id} is {status}; only a pending task can be dispatched")
    candidate = copy.deepcopy(state)
    candidate["revision"] = AUTO
    candidate["worktree"]["observed"] = AUTO
    if candidate.get("phase") == "initializing":
        candidate["phase"] = "task"
    for task in candidate["tasks"]:
        if task.get("id") in task_ids:
            task["status"] = "implementing"
            task["dispatch_scope_fingerprint"] = AUTO
    candidate["next_action"] = next_action or f"await verification for {', '.join(task_ids)}"
    _promote(destination, candidate)


def park(destination: Path, task_ids: List[str], question: str, ref: Optional[str], next_action: Optional[str]) -> None:
    """`pending | implementing | correcting -> parked`. A write-active task parks only once its scope is restored to its dispatch content; `checkpoint`'s transition check names the scope paths still differing when it is not."""
    state = _load(destination)
    if state.get("lifecycle") in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    if not question.strip():
        raise ValueError("park needs --question <text>")
    by_id = _named_tasks(state, task_ids)
    for task_id in task_ids:
        status = by_id[task_id].get("status")
        if status not in {"pending", "implementing", "correcting"}:
            raise ValueError(f"{task_id} is {status}; only a pending, implementing, or correcting task can park")
    at = datetime.now().astimezone().isoformat(timespec="seconds")
    candidate = copy.deepcopy(state)
    candidate["revision"] = AUTO
    candidate["worktree"]["observed"] = AUTO
    for task in candidate["tasks"]:
        if task.get("id") in task_ids:
            from_status = by_id[task["id"]]["status"]
            task["status"] = "parked"
            task["parked"] = {"question": question.strip(), "from": from_status, "decision_ref": ref, "at": at}
            task["latest_verification"] = []
            task["acceptance"] = None
    candidate["next_action"] = next_action or f"blocked on {ref or question.strip()}: {', '.join(task_ids)} parked"
    _promote(destination, candidate)


def unpark(destination: Path, task_ids: List[str], next_action: Optional[str]) -> None:
    """`parked -> pending`. Drops `parked` and the stale `dispatch_scope_fingerprint`; the task is dispatched again in the ordinary way, so no verification or review is skipped, and its next `dispatch` seals a fresh value rather than carrying one held over from before it parked."""
    state = _load(destination)
    if state.get("lifecycle") in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    by_id = _named_tasks(state, task_ids)
    for task_id in task_ids:
        status = by_id[task_id].get("status")
        if status != "parked":
            raise ValueError(f"{task_id} is {status}; only a parked task can be unparked")
    candidate = copy.deepcopy(state)
    candidate["revision"] = AUTO
    candidate["worktree"]["observed"] = AUTO
    for task in candidate["tasks"]:
        if task.get("id") in task_ids:
            task["status"] = "pending"
            task.pop("parked", None)
            task.pop("dispatch_scope_fingerprint", None)
    candidate["next_action"] = next_action or f"dispatch {', '.join(task_ids)}"
    _promote(destination, candidate)


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    validate_parser = commands.add_parser("validate")
    validate_parser.add_argument("state", type=Path)
    reconcile_parser = commands.add_parser("reconcile")
    reconcile_parser.add_argument("state", type=Path)
    worktree_parser = commands.add_parser("check-worktree")
    worktree_parser.add_argument("run_root", type=Path)
    worktree_parser.add_argument("worktree", type=Path)
    split_parser = commands.add_parser("split-check", help="whether the named pending tasks can be dispatched now, together: their scopes must not meet each other's, a task already under way, or an earlier task still pending")
    split_parser.add_argument("state", type=Path)
    split_parser.add_argument("task_ids", nargs="+", metavar="task-id")
    start_parser = commands.add_parser("start", help="first checkpoint of a run; builds the state from its parts")
    start_parser.add_argument("destination", type=Path, nargs="?",
                              help="state.json path; omit and pass --run-root with --slug to have one named for you")
    start_parser.add_argument("--run-root", type=Path, default=None,
                              help="mint <run-root>/<YYMMDD-HHMMSS>-<slug>/state.json instead of naming it")
    start_parser.add_argument("--slug", default=None, help="run slug, used with --run-root")
    start_parser.add_argument("--kind", choices=("plan", "brief"), required=True)
    start_parser.add_argument("--input", type=Path, default=None, dest="reference", help="plan path")
    start_parser.add_argument("--summary", default=None, help="brief text")
    start_parser.add_argument("--declared-status", default=None, help="the plan's own status, when it has one")
    start_parser.add_argument("--worktree", type=Path, required=True, help="any path inside the canonical worktree")
    start_parser.add_argument("--tasks", type=Path, required=True, dest="tasks_path",
                              help="JSON array of tasks, each with id, title, scope, completion_condition, verification_path, rationale")
    start_parser.add_argument("--next", dest="next_action", default=None)

    amend_parser = commands.add_parser("amend", help="the input changed under the run: re-hash it and record why, in place")
    amend_parser.add_argument("destination", type=Path)
    amend_parser.add_argument("--reason", required=True, help="what changed and who ruled it")
    amend_parser.add_argument("--summary", default=None, help="the new text, for a brief input; a plan input is re-read from its path")
    amend_parser.add_argument("--next", dest="next_action", default=None)

    dispatch_parser = commands.add_parser("dispatch", help="pending -> implementing, sealing dispatch_scope_fingerprint before any executor is dispatched; run this before telling an executor to start, never after")
    dispatch_parser.add_argument("destination", type=Path)
    dispatch_parser.add_argument("task_ids", nargs="+", metavar="task-id")
    dispatch_parser.add_argument("--next", dest="next_action", default=None)

    park_parser = commands.add_parser("park", help="pending|implementing|correcting -> parked; refuses a write-active task whose scope is not yet restored to its dispatch content")
    park_parser.add_argument("destination", type=Path)
    park_parser.add_argument("task_ids", nargs="+", metavar="task-id")
    park_parser.add_argument("--question", required=True, help="the decision, as asked")
    park_parser.add_argument("--ref", default=None, help="the caller's id for the decision, e.g. Q1")
    park_parser.add_argument("--next", dest="next_action", default=None)

    unpark_parser = commands.add_parser("unpark", help="parked -> pending; drops the parked record so the task is dispatched again in the ordinary way")
    unpark_parser.add_argument("destination", type=Path)
    unpark_parser.add_argument("task_ids", nargs="+", metavar="task-id")
    unpark_parser.add_argument("--next", dest="next_action", default=None)

    checkpoint_parser = commands.add_parser("checkpoint")
    checkpoint_parser.add_argument("destination", type=Path)
    checkpoint_parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            payload = _load(args.state)
            errors = validate_state(payload, args.state, _legacy_findings(payload))
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            return 0
        if args.command == "reconcile":
            result = reconcile(args.state)
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0 if result["valid"] and result["input_matches"] and result["worktree_matches"] else 1
        if args.command == "split-check":
            payload = _load(args.state)
            errors = validate_state(payload, args.state, _legacy_findings(payload))
            if errors:
                raise ValueError("; ".join(errors))
            result = split_check(payload, args.task_ids)
            print(json.dumps(result, indent=2))
            return 0 if result["disjoint"] else 1
        if args.command == "check-worktree":
            occupant = find_occupying_run(args.run_root, args.worktree)
            print(json.dumps({"occupying_state": str(occupant) if occupant else None}, indent=2))
            return 1 if occupant else 0
        if args.command == "amend":
            amend(args.destination, args.reason, args.summary, args.next_action)
            print(args.destination)
            return 0
        if args.command == "dispatch":
            dispatch(args.destination, args.task_ids, args.next_action)
            print(args.destination)
            return 0
        if args.command == "park":
            park(args.destination, args.task_ids, args.question, args.ref, args.next_action)
            print(args.destination)
            return 0
        if args.command == "unpark":
            unpark(args.destination, args.task_ids, args.next_action)
            print(args.destination)
            return 0
        if args.command == "start":
            destination = _resolve_start_destination(args)
            start(destination, args.kind, args.reference, args.summary, args.declared_status,
                  args.worktree, args.tasks_path, args.next_action)
            print(destination)
            return 0
        checkpoint(args.destination, args.candidate)
        print(args.destination)
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
