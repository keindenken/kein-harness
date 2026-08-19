#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
INPUT_FIELDS = frozenset({"reference", "summary", "sha256"})
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
STATUS_PATTERN = re.compile(r"^Status:\s*(.*?)\s*$", re.MULTILINE)
STATUS_REASON_PATTERN = re.compile(r"^Status reason:\s*(.*?)\s*$", re.MULTILINE)
HEADING_PATTERN = re.compile(r"^#\s+\S", re.MULTILINE)
EVIDENCE_GATE_LABELS = (
    "Claim",
    "Evidence method",
    "Pass path",
    "Alternate path",
    "Required before",
    "Unexpected result",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def review_text(text: str) -> str:
    lines = []
    for line in text.splitlines(keepends=True):
        if line.startswith("Status:") or line.startswith("Status reason:"):
            continue
        lines.append(line)
    return "".join(lines)


def review_sha256(path: Path) -> str:
    return hashlib.sha256(review_text(path.read_text()).encode("utf-8")).hexdigest()


def parse_plan_text(text: str) -> Dict[str, str]:
    statuses = STATUS_PATTERN.findall(text)
    reasons = STATUS_REASON_PATTERN.findall(text)
    return {
        "status": statuses[0].strip() if len(statuses) == 1 else "",
        "status_reason": reasons[0].strip() if len(reasons) == 1 else "",
    }


def _evidence_gate_errors(text: str) -> List[str]:
    marker = re.search(r"^## Evidence Gates\s*$", text, re.MULTILINE)
    if marker is None:
        return []
    remainder = text[marker.end():]
    next_h2 = re.search(r"^## (?!#)", remainder, re.MULTILINE)
    section = remainder[:next_h2.start()] if next_h2 else remainder
    headings = list(re.finditer(r"^###\s+(.+?)\s*$", section, re.MULTILINE))
    if not headings:
        return ["Evidence Gates requires at least one named gate"]
    errors: List[str] = []
    for index, heading in enumerate(headings):
        start = heading.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(section)
        body = section[start:end]
        name = heading.group(1).strip()
        for label in EVIDENCE_GATE_LABELS:
            if re.search(rf"^- {re.escape(label)}:\s*\S", body, re.MULTILINE) is None:
                errors.append(f"Evidence gate {name} is missing {label}")
    return errors


def validate_plan_text(text: str) -> List[str]:
    errors: List[str] = []
    if HEADING_PATTERN.search(text) is None:
        errors.append("Plan requires a level-one title")
    statuses = STATUS_PATTERN.findall(text)
    if len(statuses) != 1 or statuses[0].strip() not in PLAN_STATUSES:
        errors.append("Plan status must be Draft, In Review, or Approved")
    reasons = STATUS_REASON_PATTERN.findall(text)
    if len(reasons) != 1 or not reasons[0].strip():
        errors.append("Plan requires a non-empty Status reason")
    errors.extend(_evidence_gate_errors(text))
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
        if plan.get("status") == "Approved":
            if not _blocking_pass(verdicts, digest):
                errors.append("Approved requires a fresh PASS from every blocking lane")
            if payload.get("findings"):
                errors.append("Approved state cannot retain unresolved findings")
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
    candidate = _load_json(candidate_path)
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


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_plan_parser = subparsers.add_parser("validate-plan")
    validate_plan_parser.add_argument("path", type=Path)

    validate_state_parser = subparsers.add_parser("validate-state")
    validate_state_parser.add_argument("path", type=Path)

    reconcile_parser = subparsers.add_parser("reconcile")
    reconcile_parser.add_argument("path", type=Path)

    checkpoint_parser = subparsers.add_parser("checkpoint")
    checkpoint_parser.add_argument("destination", type=Path)
    checkpoint_parser.add_argument("candidate", type=Path)

    args = parser.parse_args()
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
