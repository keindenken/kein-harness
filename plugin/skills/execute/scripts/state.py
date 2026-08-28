#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
TASK_STATUSES = frozenset({"pending", "implementing", "verifying", "reviewing", "correcting", "accepted"})
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
TASK_TRANSITIONS = {
    "pending": frozenset({"pending", "implementing"}),
    "implementing": frozenset({"implementing", "verifying"}),
    "verifying": frozenset({"verifying", "reviewing", "correcting"}),
    "reviewing": frozenset({"reviewing", "correcting", "accepted"}),
    "correcting": frozenset({"correcting", "verifying"}),
    "accepted": frozenset({"accepted", "correcting"}),
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
    "worktree", "accepted_tasks", "final_verification", "final_audit",
})
ABORTED_FIELDS = frozenset({
    "schema_version", "revision", "workflow", "run_id", "lifecycle", "aborted_at", "worktree_root", "reason",
})
INPUT_FIELDS = frozenset({"kind", "reference", "summary", "sha256", "declared_status"})
WORKTREE_FIELDS = frozenset({"root", "git_common_dir", "baseline", "observed"})
FINGERPRINT_FIELDS = frozenset({"head", "index_sha256", "tracked_diff_sha256", "untracked_sha256", "fingerprint"})
TASK_FIELDS = frozenset({
    "id", "title", "scope", "completion_condition", "verification_path", "rationale",
    "status", "round", "latest_verification", "unresolved_findings", "acceptance",
})
VERIFICATION_FIELDS = frozenset({"command", "exit_code", "observed_at", "round", "worktree_fingerprint"})
VERDICT_FIELDS = frozenset({
    "reviewer_role", "verdict", "task_id", "round", "worktree_fingerprint",
    "reviewed_at", "fresh", "independent",
})
FINDING_FIELDS = frozenset({
    "reviewer_role", "claim", "evidence", "impact", "required_correction", "severity", "confidence",
})
ACCEPTANCE_FIELDS = frozenset({"round", "worktree_fingerprint", "reviewers"})
COMPLETED_INPUT_FIELDS = frozenset({"reference", "sha256"})
COMPLETED_WORKTREE_FIELDS = frozenset({"root", "final_fingerprint"})
ACCEPTED_TASK_FIELDS = frozenset({"id", "title", "completion_condition"})


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


def worktree_fingerprint(path: Path) -> Dict[str, str]:
    root, _ = canonical_worktree(path)
    head = _git_bytes(root, ["rev-parse", "HEAD"]).strip()
    index = _git_bytes(root, ["diff", "--cached", "--binary", "--no-ext-diff"])
    tracked = _git_bytes(root, ["diff", "--binary", "--no-ext-diff"])
    untracked_paths = [item for item in _git_bytes(root, ["ls-files", "--others", "--exclude-standard", "-z"]).split(b"\0") if item]
    untracked_parts: List[Tuple[bytes, bytes]] = []
    for relative_bytes in sorted(untracked_paths):
        relative = relative_bytes.decode("utf-8", "surrogateescape")
        if relative.startswith(LEDGER_PREFIX):
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
    if value.get("verdict") not in {"PASS", "MUST_FIX"}:
        errors.append("Review verdict must be PASS or MUST_FIX")
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


def _validate_findings(value: Any) -> List[str]:
    if not isinstance(value, list):
        return ["Findings must be a list"]
    errors: List[str] = []
    for index, finding in enumerate(value):
        if not isinstance(finding, dict) or set(finding) != FINDING_FIELDS:
            errors.append(f"Finding {index} must use the exact field set")
            continue
        for key in FINDING_FIELDS:
            if not isinstance(finding.get(key), str) or not finding[key].strip():
                errors.append(f"Finding {index} requires non-empty {key}")
        if finding.get("severity") not in {"critical", "important", "minor"}:
            errors.append(f"Finding {index} severity is invalid")
        if finding.get("confidence") not in {"high", "medium", "low"}:
            errors.append(f"Finding {index} confidence is invalid")
    return errors


def _validate_task(task: Any, current_fingerprint: str) -> List[str]:
    if not isinstance(task, dict) or set(task) != TASK_FIELDS:
        return ["Task must use the exact task field set"]
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
    verification = task.get("latest_verification")
    if not isinstance(verification, list):
        errors.append("Task latest_verification must be a list")
        verification = []
    else:
        for item in verification:
            errors.extend(_validate_verification(item))
    errors.extend(_validate_findings(task.get("unresolved_findings")))
    acceptance = task.get("acceptance")
    if acceptance is not None:
        if not isinstance(acceptance, dict) or set(acceptance) != ACCEPTANCE_FIELDS:
            errors.append("Task acceptance must use the exact field set")
        else:
            acceptance_fingerprint = acceptance.get("worktree_fingerprint", "")
            if not _valid_hash(acceptance_fingerprint):
                errors.append("Task acceptance requires a valid worktree fingerprint")
            reviewers = acceptance.get("reviewers")
            if not isinstance(reviewers, list):
                errors.append("Task acceptance reviewers must be a list")
                reviewers = []
            for reviewer in reviewers:
                errors.extend(_validate_verdict(reviewer, task.get("id", ""), task.get("round", -1), acceptance_fingerprint))
            current_verification = any(
                isinstance(item, dict) and item.get("exit_code") == 0
                and item.get("round") == task.get("round")
                and item.get("worktree_fingerprint") == acceptance_fingerprint
                for item in verification
            )
            if not current_verification:
                errors.append("Accepted task requires current-round verification")
            current_pass = any(
                isinstance(item, dict) and item.get("verdict") == "PASS"
                and item.get("fresh") is True and item.get("independent") is True
                and item.get("round") == task.get("round")
                and item.get("worktree_fingerprint") == acceptance_fingerprint
                for item in reviewers
            )
            if not current_pass:
                errors.append("Accepted task requires a fresh independent PASS")
            if any(isinstance(item, dict) and item.get("verdict") == "MUST_FIX" for item in reviewers):
                errors.append("Accepted task cannot retain a current MUST_FIX verdict")
            if acceptance.get("round") != task.get("round"):
                errors.append("Task acceptance does not match the current round")
    if task.get("status") == "accepted" and acceptance is None:
        errors.append("Accepted task requires acceptance facts")
    if task.get("status") == "accepted" and task.get("unresolved_findings"):
        errors.append("Accepted task cannot retain unresolved findings")
    if task.get("status") != "accepted" and acceptance is not None:
        errors.append("Only an accepted task may retain acceptance facts")
    return errors


def validate_state(payload: Any, state_path: Path) -> List[str]:
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
            errors.append("Nonterminal state must use the exact resumable field set")
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
        if not isinstance(input_value, dict) or set(input_value) != INPUT_FIELDS:
            errors.append("Input must use the exact field set")
        else:
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
            errors.append("Worktree must use the exact field set")
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
            errors.extend(_validate_task(task, current_fingerprint))
            if isinstance(task, dict):
                identifiers.append(task.get("id"))
                if task.get("status") in WRITE_ACTIVE_STATUSES:
                    active_indexes.append(index)
        if len(identifiers) != len(set(identifiers)):
            errors.append("Task ids must be unique")
        if len(active_indexes) > 1:
            errors.append("Only one task may be write-active")
        if active_indexes and any(tasks[index].get("status") != "accepted" for index in range(active_indexes[0])):
            errors.append("Every earlier task must be accepted before a later task becomes active")
        if payload.get("current_task_id") is not None and payload.get("current_task_id") not in identifiers:
            errors.append("current_task_id must identify a task")
        for task in tasks:
            if (
                isinstance(task, dict)
                and task.get("id") == payload.get("current_task_id")
                and task.get("status") == "accepted"
                and isinstance(task.get("acceptance"), dict)
                and task["acceptance"].get("worktree_fingerprint") != current_fingerprint
            ):
                errors.append("Current task acceptance must match the observed worktree fingerprint")
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
        errors.extend(_validate_findings(payload.get("unresolved_findings")))
        if payload.get("phase") == "final_audit" and payload.get("unresolved_findings"):
            errors.append("Final audit cannot retain unresolved findings")
    elif lifecycle == "completed":
        if set(payload) != COMPLETED_FIELDS:
            errors.append("Completed receipt must use the exact compact field set")
            return errors
        if not _valid_time(payload.get("completed_at")):
            errors.append("Completed receipt requires timezone-aware completed_at")
        compact_input = payload.get("input")
        if not isinstance(compact_input, dict) or set(compact_input) != COMPLETED_INPUT_FIELDS:
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
                if not isinstance(task, dict) or set(task) != ACCEPTED_TASK_FIELDS:
                    errors.append("Accepted task summary must use the exact compact field set")
                    continue
                accepted_ids.append(task.get("id"))
                for key in ACCEPTED_TASK_FIELDS:
                    if not isinstance(task.get(key), str) or not task[key].strip():
                        errors.append(f"Accepted task summary requires non-empty {key}")
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
            errors.append("Aborted receipt must use the exact compact field set")
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
    errors = validate_state(candidate, Path("state.json"))
    if previous is None:
        if candidate.get("revision") != 0:
            errors.append("Initial state revision must be zero")
        if candidate.get("lifecycle") not in NONTERMINAL_LIFECYCLES:
            errors.append("Initial checkpoint must be nonterminal")
        return errors
    previous_errors = validate_state(previous, Path("state.json"))
    if candidate.get("lifecycle") == "completed" and previous.get("unresolved_findings"):
        errors.append("Completion cannot retain unresolved findings")
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
            errors.append("Transition cannot change input identity")
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
            {key: task.get(key) for key in ACCEPTED_TASK_FIELDS}
            for task in previous.get("tasks", [])
        ]
        if candidate.get("accepted_tasks") != expected_tasks:
            errors.append("Completed task summaries must exactly project accepted tasks")
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
    errors = validate_state(payload, state_path)
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
        action = "block and reassess the changed input before resuming"
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
    def fill(node: Any) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key in {"worktree_fingerprint", "final_fingerprint"} and value == AUTO:
                    node[key] = combined
                else:
                    fill(value)
        elif isinstance(node, list):
            for item in node:
                fill(item)

    fill(candidate)


def checkpoint(destination: Path, candidate_path: Path) -> None:
    _promote(destination, _load(candidate_path))


def _promote(destination: Path, candidate: Dict[str, Any]) -> None:
    _root_value = candidate.get("worktree", {}).get("root") if isinstance(candidate.get("worktree"), dict) else candidate.get("worktree_root")
    _autofill(candidate, destination, Path(_root_value) if isinstance(_root_value, str) else None)
    candidate_errors = validate_state(candidate, destination)
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
                      "latest_verification": [], "unresolved_findings": [], "acceptance": None})
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

    checkpoint_parser = commands.add_parser("checkpoint")
    checkpoint_parser.add_argument("destination", type=Path)
    checkpoint_parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            errors = validate_state(_load(args.state), args.state)
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            return 0
        if args.command == "reconcile":
            result = reconcile(args.state)
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0 if result["valid"] and result["input_matches"] and result["worktree_matches"] else 1
        if args.command == "check-worktree":
            occupant = find_occupying_run(args.run_root, args.worktree)
            print(json.dumps({"occupying_state": str(occupant) if occupant else None}, indent=2))
            return 1 if occupant else 0
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
