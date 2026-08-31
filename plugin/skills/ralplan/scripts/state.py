#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple


SCHEMA_VERSION = 1
PLAN_STATUSES = frozenset({"Draft", "In Review", "Approved"})
NONTERMINAL_LIFECYCLES = frozenset({"active", "blocked", "interrupted"})
TERMINAL_LIFECYCLES = frozenset({"completed", "aborted"})
PHASES = frozenset({
    "initializing",
    "drafting",
    "drafted",
    "reviewing",
    "revising",
    "gathering_evidence",
    "blocked",
    "interrupted",
})
# No `created_at` or `updated_at`.
# `reconcile` is the only authority on continuation and it reads no time, so a nonterminal timestamp had no consumer.
# `run_id` already carries the start to the second and is also the directory name; the file's mtime is the last write, and is more accurate than a value a model has to remember to refresh.
NONTERMINAL_FIELDS = frozenset({
    "schema_version",
    "workflow",
    "run_id",
    "lifecycle",
    "working_directory",
    "repository",
    "input",
    "plan",
    "phase",
    "round",
    "verdicts",
    "findings",
    "closure",
    "next_action",
})
COMPLETED_FIELDS = frozenset({
    "schema_version",
    "workflow",
    "run_id",
    "lifecycle",
    "completed_at",
    "plan",
    "approvals",
})
ABORTED_FIELDS = frozenset({
    "schema_version",
    "workflow",
    "run_id",
    "lifecycle",
    "aborted_at",
    "reason",
})
PLAN_FIELDS = frozenset({"path", "artifact_sha256", "review_sha256", "status"})
COMPLETED_PLAN_FIELDS = frozenset({"path", "artifact_sha256", "review_sha256"})
VERDICT_FIELDS = frozenset({"lane", "verdict", "plan_sha256", "reviewed_at"})
LANE_ROLES = ("architect", "critic")
LANE_PATTERN = re.compile(r"(architect|critic)@([a-z][a-z0-9-]*)(:advisory)?")
FINDING_FIELDS = frozenset({
    "lane",
    "claim",
    "evidence",
    "impact",
    "required_correction",
})
CLOSURE_FIELDS = frozenset({"lane", "finding", "disposition", "evidence"})
# `REWORDED-ONLY` is the whole reason a primed reader is worth asking: it is the one verdict a
# blind lane cannot reach, because reaching it means having seen the text the correction replaced.
CLOSURE_DISPOSITIONS = frozenset({"CLOSED", "PARTIAL", "NOT CLOSED", "REWORDED-ONLY"})


INPUT_FIELDS = frozenset({"reference", "summary", "sha256"})
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
STATUS_PATTERN = re.compile(r"^Status:\s*(.*?)\s*$", re.MULTILINE)
# One header line, `Status: <word> — <reason>`. Non-greedy up to the first em dash, so a reason
# may carry its own; the dash rather than a period because a reason is full of periods and the
# word has to stay recoverable from the left.
STATUS_LINE_PATTERN = re.compile(r"^(.*?)\s+—\s+(\S.*)$")
HEADING_PATTERN = re.compile(r"^#\s+\S", re.MULTILINE)
def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def review_text(text: str) -> str:
    lines = []
    for line in text.splitlines(keepends=True):
        if line.startswith("Status:"):
            continue
        lines.append(line)
    return "".join(lines)


def review_sha256(path: Path) -> str:
    return hashlib.sha256(review_text(path.read_text()).encode("utf-8")).hexdigest()


def parse_plan_text(text: str) -> Dict[str, str]:
    """The header's machine-read half. Empty for an absent or malformed line; `validate_plan_text` says which."""
    statuses = STATUS_PATTERN.findall(text)
    match = STATUS_LINE_PATTERN.match(statuses[0]) if len(statuses) == 1 else None
    return {"status": match.group(1).strip() if match else ""}


def validate_plan_text(text: str) -> List[str]:
    errors: List[str] = []
    if HEADING_PATTERN.search(text) is None:
        errors.append("Plan requires a level-one title")
    statuses = STATUS_PATTERN.findall(text)
    if len(statuses) != 1:
        errors.append("Plan requires exactly one Status line")
        return errors
    match = STATUS_LINE_PATTERN.match(statuses[0])
    if match is None or match.group(1).strip() not in PLAN_STATUSES:
        errors.append("Status must read `Draft`, `In Review` or `Approved`, an em dash, then a non-empty reason")
    return errors


def validate_plan(path: Path) -> List[str]:
    try:
        return validate_plan_text(path.read_text())
    except (OSError, UnicodeError) as error:
        return [str(error)]


def _valid_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        return datetime.fromisoformat(value).tzinfo is not None
    except ValueError:
        return False


def _valid_hash(value: Any) -> bool:
    return isinstance(value, str) and HEX_64.fullmatch(value) is not None


def _validate_verdict(value: Any, lane: str, expected_hash: str) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, dict) or set(value) != VERDICT_FIELDS:
        return [f"{lane} verdict must use the exact verdict field set"]
    errors: List[str] = []
    if value.get("lane") != lane:
        errors.append(f"{lane} verdict lane does not match")
    if value.get("verdict") not in {"PASS", "MUST_FIX"}:
        errors.append(f"{lane} verdict must be PASS or MUST_FIX")
    if value.get("plan_sha256") != expected_hash:
        errors.append(f"{lane} verdict does not match the current review hash")
    if not _valid_timestamp(value.get("reviewed_at")):
        errors.append(f"{lane} verdict requires a timezone-aware reviewed_at")
    return errors


def _parse_lane(key: Any) -> Optional[Tuple[str, str, bool]]:
    # A lane names its role, the vendor that ran it, and whether it gates approval.
    # `--critic claude,codex:advisory` becomes the keys `critic@claude` and `critic@codex:advisory`, so the roster reads straight off the state instead of being remembered.
    if not isinstance(key, str):
        return None
    match = LANE_PATTERN.fullmatch(key)
    if match is None:
        return None
    return match.group(1), match.group(2), match.group(3) is not None


def _validate_roster(verdicts: Any) -> List[str]:
    if not isinstance(verdicts, dict) or not verdicts:
        return ["Verdicts must be a non-empty lane roster"]
    errors: List[str] = []
    parsed: Dict[str, Tuple[str, str, bool]] = {}
    for key in verdicts:
        lane = _parse_lane(key)
        if lane is None:
            errors.append(f"Lane '{key}' is not <role>@<vendor> with an optional :advisory suffix")
            continue
        parsed[key] = lane
    for role in LANE_ROLES:
        lanes = [lane for lane in parsed.values() if lane[0] == role]
        if not lanes:
            errors.append(f"The roster requires at least one {role} lane")
        elif all(lane[2] for lane in lanes):
            # A role served only by advisory lanes cannot block anything, which silently removes half the consensus gate.
            errors.append(f"Every {role} lane is advisory, so nothing can block on {role} grounds")
    return errors


def _empty_roster(verdicts: Any) -> bool:
    return not _validate_roster(verdicts) and all(value is None for value in verdicts.values())


def _blocking_pass(verdicts: Any, digest: str) -> bool:
    # Advisory lanes are skipped here and nowhere else: their findings still reach Planner, and only the approval decision ignores them.
    if _validate_roster(verdicts):
        return False
    for key, value in verdicts.items():
        if _parse_lane(key)[2]:
            continue
        if not isinstance(value, dict):
            return False
        if value.get("lane") != key or value.get("verdict") != "PASS":
            return False
        if value.get("plan_sha256") != digest:
            return False
    return True


def _validate_plan_record(value: Any, completed: bool = False) -> List[str]:
    expected = COMPLETED_PLAN_FIELDS if completed else PLAN_FIELDS
    if not isinstance(value, dict) or set(value) != expected:
        return ["Plan state must use the exact plan field set"]
    errors: List[str] = []
    if not isinstance(value.get("path"), str) or not value["path"]:
        errors.append("Plan state requires a path")
    for key in ("artifact_sha256", "review_sha256"):
        if not _valid_hash(value.get(key)):
            errors.append(f"Plan state requires a valid {key}")
    if not completed and value.get("status") not in PLAN_STATUSES:
        errors.append("Plan state status is invalid")
    return errors


def _validate_input(value: Any) -> List[str]:
    if not isinstance(value, dict) or set(value) != INPUT_FIELDS:
        return ["Input state must use the exact input field set"]
    errors: List[str] = []
    reference = value.get("reference")
    summary = value.get("summary")
    if reference is not None and (not isinstance(reference, str) or not reference):
        errors.append("Input reference must be null or a non-empty path")
    if not isinstance(summary, str) or not summary:
        errors.append("Input summary must be non-empty")
    if not _valid_hash(value.get("sha256")):
        errors.append("Input requires a valid sha256")
    return errors


def _validate_findings(value: Any) -> List[str]:
    if not isinstance(value, list):
        return ["Findings must be a list"]
    errors: List[str] = []
    for index, finding in enumerate(value):
        if not isinstance(finding, dict) or set(finding) != FINDING_FIELDS:
            errors.append(f"Finding {index} must use the exact finding field set")
            continue
        if _parse_lane(finding.get("lane")) is None:
            errors.append(f"Finding {index} has an invalid lane")
        for key in FINDING_FIELDS - {"lane"}:
            if not isinstance(finding.get(key), str) or not finding[key].strip():
                errors.append(f"Finding {index} requires non-empty {key}")
    return errors


def _validate_closure(value: Any) -> List[str]:
    if not isinstance(value, list):
        return ["Closure must be a list"]
    errors: List[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict) or set(item) != CLOSURE_FIELDS:
            errors.append(f"Closure {index} must use the exact closure field set")
            continue
        if _parse_lane(item.get("lane")) is None:
            errors.append(f"Closure {index} has an invalid lane")
        if item.get("disposition") not in CLOSURE_DISPOSITIONS:
            errors.append(f"Closure {index} disposition must be one of {', '.join(sorted(CLOSURE_DISPOSITIONS))}")
        for key in ("finding", "evidence"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"Closure {index} requires non-empty {key}")
    return errors


def validate_state(payload: Any) -> List[str]:
    if not isinstance(payload, dict):
        return ["State must be a JSON object"]
    errors: List[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        errors.append("State schema_version must be 1")
    if payload.get("workflow") != "ralplan":
        errors.append("State workflow must be ralplan")
    if not isinstance(payload.get("run_id"), str) or not payload["run_id"]:
        errors.append("State requires a run_id")
    lifecycle = payload.get("lifecycle")
    if lifecycle in NONTERMINAL_LIFECYCLES:
        if set(payload) != NONTERMINAL_FIELDS:
            errors.append("Nonterminal state must use the exact resumable field set")
            return errors
        for key in ("working_directory", "repository", "next_action"):
            if not isinstance(payload.get(key), str) or not payload[key]:
                errors.append(f"Nonterminal state requires non-empty {key}")
        if payload.get("phase") not in PHASES:
            errors.append("Nonterminal state phase is invalid")
        if type(payload.get("round")) is not int or payload["round"] < 0:
            errors.append("Nonterminal state round must be a non-negative integer")
        errors.extend(_validate_input(payload.get("input")))
        errors.extend(_validate_plan_record(payload.get("plan")))
        plan = payload.get("plan") if isinstance(payload.get("plan"), dict) else {}
        digest = plan.get("review_sha256", "")
        verdicts = payload.get("verdicts")
        roster_errors = _validate_roster(verdicts)
        errors.extend(roster_errors)
        if not roster_errors:
            for lane in verdicts:
                errors.extend(_validate_verdict(verdicts[lane], lane, digest))
        errors.extend(_validate_findings(payload.get("findings")))
        errors.extend(_validate_closure(payload.get("closure")))
        if plan.get("status") == "Approved":
            if not _blocking_pass(verdicts, digest):
                errors.append("Approved requires a fresh PASS from every blocking lane")
            if payload.get("findings"):
                errors.append("Approved state cannot retain unresolved findings")
            # A positive closure check cannot approve -- `_blocking_pass` never reads this field.
            # A negative one blocks, which is the half the contract had no way to record.
            closure = payload.get("closure")
            if isinstance(closure, list) and any(
                isinstance(item, dict) and item.get("disposition") != "CLOSED" for item in closure
            ):
                errors.append("Approved state cannot retain a closure disposition other than CLOSED")
    elif lifecycle == "completed":
        if set(payload) != COMPLETED_FIELDS:
            errors.append("Completed receipts must use the exact compact field set")
            return errors
        if not _valid_timestamp(payload.get("completed_at")):
            errors.append("Completed receipt requires timezone-aware completed_at")
        errors.extend(_validate_plan_record(payload.get("plan"), completed=True))
        plan = payload.get("plan") if isinstance(payload.get("plan"), dict) else {}
        digest = plan.get("review_sha256", "")
        approvals = payload.get("approvals")
        if not _blocking_pass(approvals, digest):
            errors.append("Completed receipt requires an exact-hash PASS from every blocking lane")
        elif isinstance(approvals, dict):
            for lane in approvals:
                errors.extend(_validate_verdict(approvals[lane], lane, digest))
    elif lifecycle == "aborted":
        if set(payload) != ABORTED_FIELDS:
            errors.append("Aborted receipts must use the exact compact field set")
            return errors
        if not _valid_timestamp(payload.get("aborted_at")):
            errors.append("Aborted receipt requires timezone-aware aborted_at")
        if not isinstance(payload.get("reason"), str) or not payload["reason"]:
            errors.append("Aborted receipt requires a reason")
    else:
        errors.append("State lifecycle is invalid")
    return errors


def validate_transition(previous: Optional[Dict[str, Any]], candidate: Dict[str, Any]) -> List[str]:
    errors = validate_state(candidate)
    if previous is None:
        is_initial = (
            candidate.get("lifecycle") == "active"
            and candidate.get("phase") == "drafted"
            and candidate.get("round") == 0
            and candidate.get("plan", {}).get("status") == "Draft"
            and _empty_roster(candidate.get("verdicts"))
            and candidate.get("findings") == []
        )
        if not is_initial:
            errors.append(
                "Initial checkpoint must be an active Draft in drafted phase at round 0"
            )
        return errors
    previous_errors = validate_state(previous)
    if previous_errors:
        return [f"Previous state is invalid: {error}" for error in previous_errors] + errors
    for key in ("schema_version", "workflow", "run_id"):
        if previous.get(key) != candidate.get(key):
            errors.append(f"Transition cannot change {key}")
    if previous.get("lifecycle") in TERMINAL_LIFECYCLES:
        errors.append("Terminal state cannot transition")
        return errors
    if candidate.get("lifecycle") in NONTERMINAL_LIFECYCLES:
        if previous.get("working_directory") != candidate.get("working_directory"):
            errors.append("Transition cannot change working_directory")
        if previous.get("repository") != candidate.get("repository"):
            errors.append("Transition cannot change repository")
        if previous.get("input") != candidate.get("input"):
            errors.append("Transition cannot change input identity")
        previous_plan = previous.get("plan", {})
        candidate_plan = candidate.get("plan", {})
        previous_status = previous_plan.get("status")
        candidate_status = candidate_plan.get("status")
        previous_verdicts = previous.get("verdicts", {})
        previous_has_must_fix = isinstance(previous_verdicts, dict) and any(
            isinstance(value, dict) and value.get("verdict") == "MUST_FIX"
            for value in previous_verdicts.values()
        )
        candidate_verdicts = candidate.get("verdicts")
        if isinstance(previous_verdicts, dict) and isinstance(candidate_verdicts, dict):
            if set(previous_verdicts) != set(candidate_verdicts):
                # Otherwise a lane that returned MUST_FIX could simply be removed from the roster and the plan approved without it.
                errors.append("The lane roster is fixed for the run and cannot change between checkpoints")
        previous_has_blocker = previous_has_must_fix or bool(previous.get("findings"))
        # Keyed on `phase` and not on `Status`. What must not happen is a plan reaching reviewers
        # while a finding against it is unresolved, and `phase` is the field that says whether
        # reviewers are reading. Keying it on `Status` also fixed the meaning of that field to
        # "did the last round block", which is not what a reader of the artifact needs from it.
        if candidate.get("phase") != "reviewing" and any(
            value is not None for value in (candidate.get("verdicts") or {}).values()
        ):
            # A verdict is a statement about a round under review. Recorded anywhere else it is a
            # `PASS` with no gate behind it, which `Status` being free text can no longer catch.
            errors.append("Verdicts can only be recorded in a reviewing phase")
        if previous_has_blocker and candidate.get("phase") == "reviewing":
            errors.append(
                "A recorded MUST_FIX or unresolved finding cannot enter a reviewing phase"
            )
        if (
            previous_has_blocker
            and previous_plan.get("review_sha256")
            == candidate_plan.get("review_sha256")
            and not candidate.get("findings")
        ):
            errors.append("Findings can only be cleared by a review-content change")
        if previous.get("phase") != "reviewing" and candidate.get("phase") == "reviewing":
            opens_fresh_round = (
                isinstance(previous.get("round"), int)
                and candidate.get("round") == previous.get("round") + 1
                and _empty_roster(candidate.get("verdicts"))
                and candidate.get("findings") == []
            )
            if not opens_fresh_round:
                errors.append(
                    "Entering a reviewing phase must advance to a fresh round with empty verdicts"
                )
        if candidate_status == "Approved":
            if previous_has_blocker:
                errors.append(
                    "Approval cannot overwrite a recorded MUST_FIX or unresolved finding"
                )
            if (
                previous.get("phase") != "reviewing"
                or candidate.get("phase") != "reviewing"
                or previous.get("round") != candidate.get("round")
                or not isinstance(candidate.get("round"), int)
                or candidate.get("round", 0) < 1
                or previous_plan.get("review_sha256")
                != candidate_plan.get("review_sha256")
            ):
                errors.append(
                    "Approval must transition from an official reviewing round"
                )
        if previous_plan.get("path") != candidate_plan.get("path"):
            errors.append("Transition cannot change the canonical plan path")
        previous_round = previous.get("round")
        candidate_round = candidate.get("round")
        if type(previous_round) is int and type(candidate_round) is int:
            if candidate_round < previous_round or candidate_round > previous_round + 1:
                errors.append("Round must remain stable or advance by one")
        if previous_plan.get("review_sha256") != candidate_plan.get("review_sha256"):
            verdicts = candidate.get("verdicts", {})
            if isinstance(verdicts, dict) and any(value is not None for value in verdicts.values()):
                errors.append("A changed plan hash must clear every previous verdict")
            if candidate_plan.get("status") == "Approved":
                errors.append("A changed plan hash cannot retain Approved status")
    if candidate.get("lifecycle") == "completed":
        previous_plan = previous.get("plan", {})
        if previous_plan.get("status") != "Approved":
            errors.append("Completion requires an Approved previous state")
        if candidate.get("plan", {}).get("review_sha256") != previous_plan.get("review_sha256"):
            errors.append("Completion receipt must retain the approved review hash")
    return errors


def _load_json(path: Path) -> Dict[str, Any]:
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        raise ValueError("State must be a JSON object")
    return payload


def reconcile(state_path: Path) -> Dict[str, Any]:
    payload = _load_json(state_path)
    errors = validate_state(payload)
    if errors:
        return {
            "valid": False,
            "errors": errors,
            "plan_hash_matches": False,
            "input_hash_matches": False,
            "required_action": "repair the invalid saved state before resuming",
        }
    if payload["lifecycle"] in TERMINAL_LIFECYCLES:
        return {
            "valid": True,
            "errors": [],
            "plan_hash_matches": True,
            "input_hash_matches": True,
            "required_action": "terminal receipt requires no resume action",
        }
    plan_path = Path(payload["plan"]["path"])
    plan_matches = (
        plan_path.is_file()
        and sha256_file(plan_path) == payload["plan"]["artifact_sha256"]
        and review_sha256(plan_path) == payload["plan"]["review_sha256"]
    )
    reference = payload["input"]["reference"]
    input_matches = True
    if reference is not None:
        input_path = Path(reference)
        input_matches = input_path.is_file() and sha256_file(input_path) == payload["input"]["sha256"]
    if not plan_matches:
        action = "invalidate current verdicts and reassess the exact next action"
    elif not input_matches:
        action = "block and reassess the changed input before resuming"
    else:
        action = payload["next_action"]
    return {
        "valid": True,
        "errors": [],
        "plan_hash_matches": plan_matches,
        "input_hash_matches": input_matches,
        "required_action": action,
    }


def checkpoint(destination: Path, candidate_path: Path) -> None:
    _commit(destination, _load_json(candidate_path))


def _commit(destination: Path, candidate: Dict[str, Any]) -> None:
    previous = _load_json(destination) if destination.exists() else None
    errors = validate_transition(previous, candidate)
    if errors:
        raise ValueError("; ".join(errors))
    if candidate["lifecycle"] in NONTERMINAL_LIFECYCLES | {"completed"}:
        plan_path = Path(candidate["plan"]["path"])
        plan_errors = validate_plan(plan_path)
        if plan_errors:
            raise ValueError("; ".join(plan_errors))
        if candidate["lifecycle"] in NONTERMINAL_LIFECYCLES:
            parsed = parse_plan_text(plan_path.read_text())
            if parsed["status"] != candidate["plan"]["status"]:
                raise ValueError("State plan status does not match the artifact")
        if sha256_file(plan_path) != candidate["plan"]["artifact_sha256"]:
            raise ValueError("State artifact_sha256 does not match the plan")
        if review_sha256(plan_path) != candidate["plan"]["review_sha256"]:
            raise ValueError("State review_sha256 does not match the plan")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=destination.parent,
            prefix=f".{destination.name}-",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(candidate, temporary_file, indent=2, sort_keys=True)
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, destination)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


SLUG_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")


def mint_run_dir(run_root: Path, slug: str) -> Path:
    """Build the run directory name so the caller does not have to read a clock.

    `run_id` is the directory name, so the lead was left assembling `<YYMMDD-HHMMSS>-<slug>` in
    the shell -- which is a compound command, and a worktree-isolated session refuses those.
    Both measured runs hit that refusal at this exact step and split it into three calls.
    """
    if not SLUG_PATTERN.match(slug):
        raise ValueError("Slug must start alphanumeric and hold only letters, digits, dot, dash, underscore")
    return run_root / f"{datetime.now().astimezone():%y%m%d-%H%M%S}-{slug}"


def _refresh(candidate: Dict[str, Any]) -> None:
    """The artifact is the authority on its own status and content.

    Every field here is readable from the plan file, so asking the caller for it only creates a
    way for the recorded state and the file to disagree -- which is exactly what the three checks
    in `_commit` existed to catch. Read them instead.
    """
    plan_path = Path(candidate["plan"]["path"])
    candidate["plan"]["status"] = parse_plan_text(plan_path.read_text())["status"]
    candidate["plan"]["artifact_sha256"] = sha256_file(plan_path)
    candidate["plan"]["review_sha256"] = review_sha256(plan_path)


def _advance(destination: Path, mutate, next_action: Optional[str], default_action: str) -> None:
    state = _load_json(destination)
    if state.get("lifecycle") in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    candidate = copy.deepcopy(state)
    _refresh(candidate)
    mutate(candidate)
    candidate["next_action"] = next_action or default_action
    _commit(destination, candidate)


def start(destination: Path, plan: Path, summary: str, lanes: List[str],
          reference: Optional[Path], working_directory: Path, repository: Path,
          next_action: Optional[str]) -> None:
    if destination.exists():
        raise ValueError(f"{destination} already exists; a run is started once")
    digest = sha256_file(reference) if reference is not None else hashlib.sha256(summary.encode("utf-8")).hexdigest()
    candidate = {
        "schema_version": SCHEMA_VERSION,
        "workflow": "ralplan",
        "run_id": destination.parent.name,
        "lifecycle": "active",
        "working_directory": str(working_directory),
        "repository": str(repository),
        "input": {
            "reference": str(reference) if reference is not None else None,
            "summary": summary,
            "sha256": digest,
        },
        "plan": {"path": str(plan), "status": "", "artifact_sha256": "", "review_sha256": ""},
        "phase": "drafted",
        "round": 0,
        "verdicts": {lane: None for lane in lanes},
        "findings": [],
        "closure": [],
        "next_action": next_action or "dispatch round 1 fresh reviewers",
    }
    _refresh(candidate)
    _commit(destination, candidate)


def open_round(destination: Path, next_action: Optional[str]) -> None:
    state = _load_json(destination)
    upcoming = state.get("round", 0) + 1 if isinstance(state.get("round"), int) else 1

    def mutate(candidate: Dict[str, Any]) -> None:
        candidate["phase"] = "reviewing"
        candidate["round"] = upcoming
        candidate["verdicts"] = {lane: None for lane in candidate["verdicts"]}
        candidate["findings"] = []

    _advance(destination, mutate, next_action, f"await round {upcoming} lane verdicts")


def block(destination: Path, findings_path: Path, next_action: Optional[str]) -> None:
    findings = _load_findings(findings_path)

    def mutate(candidate: Dict[str, Any]) -> None:
        candidate["phase"] = "revising"
        candidate["findings"] = findings
        candidate["verdicts"] = {lane: None for lane in candidate["verdicts"]}

    _advance(destination, mutate, next_action, "ask Planner to revise the same artifact")


def revised(destination: Path, closure_path: Optional[Path], next_action: Optional[str]) -> None:
    """`revised` is the only writer of `closure`, and it writes on every call.

    The check judges one revision against the findings it answered, so a later revision makes an
    earlier disposition stale for the same reason a content change clears every verdict. Calling
    without `--closure` therefore records that this revision was not checked, rather than leaving
    the previous one standing over text it never read.
    """
    state = _load_json(destination)
    upcoming = state.get("round", 0) + 1 if isinstance(state.get("round"), int) else 1
    closure = _load_findings(closure_path, "closure") if closure_path is not None else []

    def mutate(candidate: Dict[str, Any]) -> None:
        candidate["phase"] = "drafted"
        candidate["findings"] = []
        candidate["closure"] = closure

    # This transition is where the round's findings leave the state, and the fresh lanes about to be
    # dispatched are forbidden from seeing them, so it is the last point anything can say they exist.
    # The file beside the run is the only surviving copy and nothing reads it back; a lead who does
    # not open it has no way to tell a finding's second appearance from its first.
    _advance(destination, mutate, next_action,
             f"dispatch round {upcoming} fresh reviewers; every earlier round's findings stay beside the run, so read them before treating a finding as new, and `revised --closure` records a primed reader's per-item disposition of them")


def approve(destination: Path, overrides: Dict[str, str], next_action: Optional[str]) -> None:
    state = _load_json(destination)
    if state.get("phase") != "reviewing" or not isinstance(state.get("round"), int) or state["round"] < 1:
        raise ValueError("Approval must transition from an official reviewing round")

    def mutate(candidate: Dict[str, Any]) -> None:
        digest = candidate["plan"]["review_sha256"]
        stamped = _now()
        for lane in candidate["verdicts"]:
            parsed = _parse_lane(lane)
            if parsed is not None and parsed[2] and lane not in overrides:
                continue
            candidate["verdicts"][lane] = {
                "lane": lane,
                "verdict": overrides.get(lane, "PASS"),
                "plan_sha256": digest,
                "reviewed_at": stamped,
            }

    _advance(destination, mutate, next_action, "compact to the completed receipt")


def complete(destination: Path) -> None:
    state = _load_json(destination)
    plan = state.get("plan", {})
    _commit(destination, {
        "schema_version": SCHEMA_VERSION,
        "workflow": "ralplan",
        "run_id": state.get("run_id"),
        "lifecycle": "completed",
        "completed_at": _now(),
        "plan": {key: plan.get(key) for key in ("path", "artifact_sha256", "review_sha256")},
        "approvals": copy.deepcopy(state.get("verdicts", {})),
    })


def abort(destination: Path, reason: str) -> None:
    state = _load_json(destination)
    _commit(destination, {
        "schema_version": SCHEMA_VERSION,
        "workflow": "ralplan",
        "run_id": state.get("run_id"),
        "lifecycle": "aborted",
        "aborted_at": _now(),
        "reason": reason,
    })


def _load_findings(path: Path, key: str = "findings") -> List[Dict[str, Any]]:
    payload = json.loads(path.read_text())
    if isinstance(payload, dict) and key in payload:
        payload = payload[key]
    if not isinstance(payload, list):
        raise ValueError("Findings must be a JSON array, or an object carrying one under `findings`")
    return payload


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


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_plan_parser = subparsers.add_parser("validate-plan")
    validate_plan_parser.add_argument("path", type=Path)

    validate_state_parser = subparsers.add_parser("validate-state")
    validate_state_parser.add_argument("path", type=Path)

    reconcile_parser = subparsers.add_parser("reconcile")
    reconcile_parser.add_argument("path", type=Path)

    checkpoint_parser = subparsers.add_parser(
        "checkpoint", help="promote a hand-authored candidate; the escape hatch for a state no transition names"
    )
    checkpoint_parser.add_argument("destination", type=Path)
    checkpoint_parser.add_argument("candidate", type=Path)

    # One subcommand per transition the workflow actually makes.
    # Each builds the candidate from the saved state and the plan file and promotes it through the
    # same validation, so the caller supplies only what cannot be derived: the findings of a round,
    # and the free text of `next_action`.
    start_parser = subparsers.add_parser("start", help="first checkpoint of a run")
    start_parser.add_argument("destination", type=Path, nargs="?",
                              help="state.json path; omit and pass --run-root with --slug to have one named for you")
    start_parser.add_argument("--run-root", type=Path, default=None,
                              help="mint <run-root>/<YYMMDD-HHMMSS>-<slug>/state.json instead of naming it")
    start_parser.add_argument("--slug", default=None, help="run slug, used with --run-root")
    start_parser.add_argument("--plan", type=Path, required=True)
    start_parser.add_argument("--summary", required=True, help="prompt-safe task summary")
    start_parser.add_argument("--lanes", required=True, help="comma-separated roster, e.g. architect@claude,critic@claude")
    start_parser.add_argument("--input", type=Path, default=None, dest="reference", help="requirements path; omit to hash the summary instead")
    start_parser.add_argument("--working-directory", type=Path, default=None)
    start_parser.add_argument("--repository", type=Path, default=None)
    start_parser.add_argument("--next", dest="next_action", default=None)

    open_parser = subparsers.add_parser("open", help="open the next official round")
    open_parser.add_argument("destination", type=Path)
    open_parser.add_argument("--next", dest="next_action", default=None)

    block_parser = subparsers.add_parser("block", help="record the round's consolidated findings and return to Planner")
    block_parser.add_argument("destination", type=Path)
    block_parser.add_argument("--findings", type=Path, required=True, help="JSON array of findings")
    block_parser.add_argument("--next", dest="next_action", default=None)

    revised_parser = subparsers.add_parser("revised", help="Planner's revision has landed; clears the findings")
    revised_parser.add_argument("destination", type=Path)
    revised_parser.add_argument("--closure", type=Path, default=None, dest="closure",
                                help="JSON array of per-item closure dispositions from a primed reader; omit to record none")
    revised_parser.add_argument("--next", dest="next_action", default=None)

    approve_parser = subparsers.add_parser("approve", help="record every blocking lane's PASS at the current review hash")
    approve_parser.add_argument("destination", type=Path)
    approve_parser.add_argument("--verdict", action="append", default=[], metavar="LANE=VERDICT",
                                help="override one lane; repeatable. Advisory lanes stay unset unless named here")
    approve_parser.add_argument("--next", dest="next_action", default=None)

    complete_parser = subparsers.add_parser("complete", help="compact an approved run to its receipt")
    complete_parser.add_argument("destination", type=Path)

    abort_parser = subparsers.add_parser("abort", help="compact to an aborted receipt")
    abort_parser.add_argument("destination", type=Path)
    abort_parser.add_argument("--reason", required=True)

    args = parser.parse_args()
    builders = {"start", "open", "block", "revised", "approve", "complete", "abort"}
    if args.command in builders:
        try:
            if args.command == "start":
                here = Path.cwd()
                destination = _resolve_start_destination(args)
                start(destination, args.plan, args.summary,
                      [lane.strip() for lane in args.lanes.split(",") if lane.strip()],
                      args.reference, args.working_directory or here, args.repository or here,
                      args.next_action)
                print(destination)
            elif args.command == "open":
                open_round(args.destination, args.next_action)
            elif args.command == "block":
                block(args.destination, args.findings, args.next_action)
            elif args.command == "revised":
                revised(args.destination, args.closure, args.next_action)
            elif args.command == "approve":
                overrides = dict(item.split("=", 1) for item in args.verdict)
                approve(args.destination, overrides, args.next_action)
            elif args.command == "complete":
                complete(args.destination)
            else:
                abort(args.destination, args.reason)
            return 0
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
            print(error, file=sys.stderr)
            return 1

    if args.command == "validate-plan":
        errors = validate_plan(args.path)
    elif args.command == "validate-state":
        try:
            errors = validate_state(_load_json(args.path))
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
            errors = [str(error)]
    elif args.command == "reconcile":
        try:
            result = reconcile(args.path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
            result = {"valid": False, "errors": [str(error)]}
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result.get("valid") and result.get("plan_hash_matches") and result.get("input_hash_matches") else 1
    else:
        try:
            checkpoint(args.destination, args.candidate)
            return 0
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
            print(error, file=sys.stderr)
            return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
