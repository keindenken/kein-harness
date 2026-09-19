#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
from datetime import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple


SCHEMA_VERSION = 1
LIFECYCLES = frozenset({"active", "paused", "completed", "halted", "aborted"})
NONTERMINAL_LIFECYCLES = frozenset({"active", "paused"})
TERMINAL_LIFECYCLES = frozenset({"completed", "halted", "aborted"})
STAGES = ("interview", "ralplan", "execute", "closeout")
STAGE_STATUSES = frozenset({"skipped", "pending", "entered"})
STAGE_FIELDS = frozenset({"status", "snapshot", "run"})
STAGE_STATUS_TRANSITIONS = {
    "skipped": frozenset({"skipped"}),
    "pending": frozenset({"pending", "entered"}),
    "entered": frozenset({"entered", "pending"}),
}
ENTRY_VALUES = frozenset({"interview", "ralplan", "execute"})
INPUT_FIELDS = frozenset({"kind", "reference", "summary"})
INPUT_KIND_VALUES = frozenset({"idea", "requirements", "plan"})
AGENTS_MD_SPAN_FIELDS = frozenset({"span_started_at", "sha256"})
HALT_FIELDS = frozenset({"reason"})
ASSUMPTION_FIELDS = frozenset({"id", "stage", "decision", "chosen", "alternatives", "reversal_cost", "where"})
QUESTION_FIELDS = frozenset({"id", "stage", "question", "options", "recommended", "why_irreversible", "parks", "answer"})
LESSON_FIELDS = frozenset({"id", "line", "why"})
FSD_FIELDS = frozenset({
    "schema_version", "workflow", "run_id", "lifecycle", "worktree", "entry", "input",
    "agents_md", "halt", "stages", "assumptions", "questions", "lessons",
    "retrospective", "next_action",
})
ID_PATTERNS = {
    "assumptions": re.compile(r"^A\d+$"),
    "questions": re.compile(r"^Q\d+$"),
    "lessons": re.compile(r"^L\d+$"),
}
HEX_64 = "0123456789abcdef"
STATUS_LINE = re.compile(r"^Status:\s*(\S.*?)\s*$", re.MULTILINE)


# fsd leans on the three workflows it chains rather than re-deriving their shapes: `guard`'s scope-collision reading, `enter`'s worktree-claim uniqueness test for a resumed execute run, and the plan/requirements Status parsing all come from the sibling scripts by import, read-only, so nothing here can drift from what `execute` and `ralplan` actually enforce.
# Interview has no importable state module -- its ledger is a hand-parsed YAML-ish frontmatter -- so only its artifact validator is imported and the ledger frontmatter is read locally.
_SKILLS_ROOT = Path(__file__).resolve().parents[2]


def _import_sibling(relative: str, name: str):
    path = _SKILLS_ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_execute = _import_sibling("execute/scripts/state.py", "_kein_fsd_execute_state")
_ralplan = _import_sibling("ralplan/scripts/state.py", "_kein_fsd_ralplan_state")
_interview_validate = _import_sibling("interview/scripts/validate_artifacts.py", "_kein_fsd_interview_validate")


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _valid_time(value: Any) -> bool:
    return _execute._valid_time(value)


def _valid_hash(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(character in HEX_64 for character in value)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _read_agents_md_hash(root: Path) -> Optional[str]:
    path = Path(root) / "AGENTS.md"
    if not path.is_file():
        return None
    return _sha256_bytes(path.read_bytes())


def _field_set_error(label: str, actual: Any, expected: frozenset) -> str:
    keys = set(actual) if isinstance(actual, dict) else set()
    missing = sorted(expected - keys)
    unexpected = sorted(keys - expected)
    return (label
            + (f"; missing {missing}" if missing else "")
            + (f"; unexpected {unexpected}" if unexpected else ""))


def _mint_id(existing_ids: List[str], prefix: str) -> str:
    pattern = re.compile(rf"^{prefix}(\d+)$")
    numbers = []
    for item in existing_ids:
        match = pattern.match(item)
        if match:
            numbers.append(int(match.group(1)))
    return f"{prefix}{(max(numbers) + 1) if numbers else 1}"


# ---------------------------------------------------------------------------
# Reading the two workflows this script chains, and interview's ledger, without editing any of them.


def _load(path: Path) -> Dict[str, Any]:
    value = json.loads(Path(path).read_text())
    if not isinstance(value, dict):
        raise ValueError("State must be a JSON object")
    return value


def _parse_ledger(text: str) -> Dict[str, str]:
    """The active ledger's own frontmatter, read the way `validate_artifacts.py` reads it: `key: value` lines between two `---` markers. Read-only; nothing here writes a ledger."""
    if not text.startswith("---\n"):
        return {}
    match = re.match(r"\A---\n(?P<raw>.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if match is None:
        return {}
    values: Dict[str, str] = {}
    for line in match.group("raw").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if key:
            values[key] = value
    return values


def _requirements_status(path: Path) -> Optional[str]:
    matches = STATUS_LINE.findall(Path(path).read_text())
    return matches[0] if len(matches) == 1 else None


def classify_input(raw_input: str, root: Path) -> Dict[str, Any]:
    """Mechanical classification, in the order U3 fixes: requirements shape first, then plan shape, else an idea.
    A relative `raw_input` is joined onto `root` -- the canonical worktree, not the process's current working directory, which `start --worktree` may point somewhere else entirely -- with a plain `Path` join and no further `.resolve()` call; that joined path, exactly as constructed, is what a matching classification stores as `reference`.
    A file is read as a requirements document when it passes interview's own artifact validator regardless of its declared status; only then does the Status line decide whether the entry is `ralplan` (Approved) or `interview` (still Draft).
    Failing that, the same two-step test runs against ralplan's own plan-text validator.
    Anything else -- free text, or a path that is neither shape -- is an idea and starts at `interview`."""
    candidate = Path(raw_input)
    if not candidate.is_absolute():
        candidate = root / candidate
    if candidate.is_file():
        text = candidate.read_text()
        if not _interview_validate.validate_requirements(candidate):
            status = _requirements_status(candidate)
            entry = "ralplan" if status == "Approved" else "interview"
            return {"kind": "requirements", "reference": str(candidate), "summary": raw_input, "entry": entry}
        if not _ralplan.validate_plan_text(text):
            parsed = _ralplan.parse_plan_text(text)
            entry = "execute" if parsed["status"] == "Approved" else "ralplan"
            return {"kind": "plan", "reference": str(candidate), "summary": raw_input, "entry": entry}
    return {"kind": "idea", "reference": None, "summary": raw_input, "entry": "interview"}


# ---------------------------------------------------------------------------
# Validation


def _validate_input(value: Any) -> List[str]:
    if not isinstance(value, dict) or set(value) != INPUT_FIELDS:
        return [_field_set_error("Input must use the exact field set", value, INPUT_FIELDS)]
    errors: List[str] = []
    kind = value.get("kind")
    if kind not in INPUT_KIND_VALUES:
        errors.append("Input kind must be idea, requirements, or plan")
    reference = value.get("reference")
    if reference is not None and (not isinstance(reference, str) or not reference):
        errors.append("Input reference must be null or a non-empty path")
    if kind == "idea" and reference is not None:
        errors.append("An idea input carries no reference")
    if kind in {"requirements", "plan"} and reference is None:
        errors.append(f"A {kind} input requires a reference")
    if not isinstance(value.get("summary"), str) or not value["summary"]:
        errors.append("Input requires a non-empty summary")
    return errors


def _validate_agents_md(value: Any) -> List[str]:
    if not isinstance(value, list) or not value:
        return ["agents_md requires at least one span"]
    errors: List[str] = []
    for index, span in enumerate(value):
        if not isinstance(span, dict) or set(span) != AGENTS_MD_SPAN_FIELDS:
            errors.append(_field_set_error(f"agents_md span {index} must use the exact field set", span, AGENTS_MD_SPAN_FIELDS))
            continue
        if not _valid_time(span.get("span_started_at")):
            errors.append(f"agents_md span {index} requires a timezone-aware span_started_at")
        sha = span.get("sha256")
        if sha is not None and not _valid_hash(sha):
            errors.append(f"agents_md span {index} sha256 must be null or a valid hash")
    return errors


def _validate_halt(value: Any, lifecycle: Any) -> List[str]:
    if value is None:
        return ["Halted state requires halt facts"] if lifecycle == "halted" else []
    if lifecycle != "halted":
        return ["Only a halted state may carry halt facts"]
    if not isinstance(value, dict) or set(value) != HALT_FIELDS:
        return [_field_set_error("halt must use the exact field set", value, HALT_FIELDS)]
    if not isinstance(value.get("reason"), str) or not value["reason"].strip():
        return ["halt requires a non-empty reason"]
    return []


def _validate_stages(value: Any) -> List[str]:
    if not isinstance(value, dict) or set(value) != set(STAGES):
        return [_field_set_error("stages must name exactly interview, ralplan, execute, closeout", value, frozenset(STAGES))]
    errors: List[str] = []
    for stage in STAGES:
        entry = value[stage]
        if not isinstance(entry, dict) or set(entry) != STAGE_FIELDS:
            errors.append(_field_set_error(f"stage {stage} must use the exact field set", entry, STAGE_FIELDS))
            continue
        if entry.get("status") not in STAGE_STATUSES:
            errors.append(f"stage {stage} status is invalid")
        snapshot = entry.get("snapshot")
        if not isinstance(snapshot, list) or not all(isinstance(item, str) for item in snapshot):
            errors.append(f"stage {stage} snapshot must be a list of strings")
            snapshot = []
        run = entry.get("run")
        if run is not None and (not isinstance(run, str) or not run):
            errors.append(f"stage {stage} run must be null or a non-empty path")
        if stage == "closeout" and (run is not None or snapshot):
            errors.append("closeout has no stage run root, so its run and snapshot stay empty")
        if entry.get("status") == "skipped" and (run is not None or snapshot):
            errors.append(f"a skipped stage {stage} cannot carry a run or snapshot")
    return errors


def _validate_list(value: Any, fields: frozenset, label: str, id_key: str = "id") -> List[str]:
    if not isinstance(value, list):
        return [f"{label} must be a list"]
    errors: List[str] = []
    pattern = ID_PATTERNS[label]
    seen: set = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict) or set(item) != fields:
            errors.append(_field_set_error(f"{label[:-1]} {index} must use the exact field set", item, fields))
            continue
        identifier = item.get(id_key, "")
        if not pattern.match(identifier):
            errors.append(f"{label[:-1]} {index} id must match {pattern.pattern}")
        elif identifier in seen:
            errors.append(f"{label[:-1]} {index} id is reused")
        else:
            seen.add(identifier)
    return errors


def _validate_assumptions(value: Any) -> List[str]:
    errors = _validate_list(value, ASSUMPTION_FIELDS, "assumptions")
    if not isinstance(value, list):
        return errors
    for index, item in enumerate(value):
        if not isinstance(item, dict) or set(item) != ASSUMPTION_FIELDS:
            continue
        for key in ("stage", "decision", "chosen", "reversal_cost", "where"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"assumption {index} requires non-empty {key}")
        alternatives = item.get("alternatives")
        if not isinstance(alternatives, list) or not all(isinstance(a, str) and a for a in alternatives):
            errors.append(f"assumption {index} alternatives must be a list of non-empty strings")
    return errors


def _validate_questions(value: Any) -> List[str]:
    errors = _validate_list(value, QUESTION_FIELDS, "questions")
    if not isinstance(value, list):
        return errors
    for index, item in enumerate(value):
        if not isinstance(item, dict) or set(item) != QUESTION_FIELDS:
            continue
        for key in ("stage", "question", "recommended", "why_irreversible", "parks"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"question {index} requires non-empty {key}")
        options = item.get("options")
        if not isinstance(options, list) or not all(isinstance(o, str) and o for o in options):
            errors.append(f"question {index} options must be a list of non-empty strings")
        answer = item.get("answer")
        if answer is not None and (not isinstance(answer, str) or not answer.strip()):
            errors.append(f"question {index} answer must be null or non-empty text")
    return errors


def _validate_lessons(value: Any) -> List[str]:
    errors = _validate_list(value, LESSON_FIELDS, "lessons")
    if not isinstance(value, list):
        return errors
    for index, item in enumerate(value):
        if not isinstance(item, dict) or set(item) != LESSON_FIELDS:
            continue
        for key in ("line", "why"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"lesson {index} requires non-empty {key}")
    return errors


def validate_state(payload: Any) -> List[str]:
    if not isinstance(payload, dict):
        return ["State must be a JSON object"]
    if set(payload) != FSD_FIELDS:
        return [_field_set_error("State must use the exact fsd field set", payload, FSD_FIELDS)]
    errors: List[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        errors.append("State schema_version must be 1")
    if payload.get("workflow") != "fsd":
        errors.append("State workflow must be fsd")
    if not isinstance(payload.get("run_id"), str) or not payload["run_id"]:
        errors.append("State requires a run_id")
    lifecycle = payload.get("lifecycle")
    if lifecycle not in LIFECYCLES:
        errors.append("State lifecycle is invalid")
        return errors
    if not isinstance(payload.get("worktree"), str) or not payload["worktree"]:
        errors.append("State requires a non-empty worktree")
    if payload.get("entry") not in ENTRY_VALUES:
        errors.append("State entry must be interview, ralplan, or execute")
    errors.extend(_validate_input(payload.get("input")))
    errors.extend(_validate_agents_md(payload.get("agents_md")))
    errors.extend(_validate_halt(payload.get("halt"), lifecycle))
    errors.extend(_validate_stages(payload.get("stages")))
    errors.extend(_validate_assumptions(payload.get("assumptions")))
    errors.extend(_validate_questions(payload.get("questions")))
    errors.extend(_validate_lessons(payload.get("lessons")))
    retrospective = payload.get("retrospective")
    if retrospective is not None and (not isinstance(retrospective, str) or not retrospective):
        errors.append("State retrospective must be null or a non-empty path")
    if not isinstance(payload.get("next_action"), str) or not payload["next_action"]:
        errors.append("State requires the exact next action")
    return errors


def _validate_stage_transition(previous: Any, candidate: Any) -> List[str]:
    errors: List[str] = []
    for stage in STAGES:
        prev_entry = (previous or {}).get(stage, {}) if isinstance(previous, dict) else {}
        cand_entry = (candidate or {}).get(stage, {}) if isinstance(candidate, dict) else {}
        prev_status = prev_entry.get("status")
        cand_status = cand_entry.get("status")
        if cand_status not in STAGE_STATUS_TRANSITIONS.get(prev_status, frozenset()):
            errors.append(f"stage {stage} status transition {prev_status} -> {cand_status} is not allowed")
    return errors


def _validate_append_only(previous_list: Any, candidate_list: Any, label: str) -> List[str]:
    previous_list = previous_list or []
    candidate_list = candidate_list or []
    if candidate_list[: len(previous_list)] != previous_list:
        return [f"{label} entries cannot change or be removed, only appended"]
    return []


def _validate_questions_transition(previous_list: Any, candidate_list: Any) -> List[str]:
    previous_list = previous_list or []
    candidate_list = candidate_list or []
    if len(candidate_list) < len(previous_list):
        return ["questions cannot be removed"]
    errors: List[str] = []
    for index, prev_item in enumerate(previous_list):
        cand_item = candidate_list[index]
        if cand_item == prev_item:
            continue
        diff_keys = {key for key in QUESTION_FIELDS if cand_item.get(key) != prev_item.get(key)}
        if diff_keys != {"answer"} or prev_item.get("answer") is not None or cand_item.get("answer") is None:
            errors.append(f"question {prev_item.get('id')} can only move from an unanswered to an answered state")
    return errors


LIFECYCLE_TRANSITIONS = {
    "active": frozenset({"active", "paused", "completed", "halted", "aborted"}),
    "paused": frozenset({"paused", "active", "aborted"}),
}


def validate_transition(previous: Optional[Dict[str, Any]], candidate: Dict[str, Any]) -> List[str]:
    errors = validate_state(candidate)
    if previous is None:
        if candidate.get("lifecycle") != "active":
            errors.append("Initial checkpoint must be active")
        if len(candidate.get("agents_md") or []) != 1:
            errors.append("Initial checkpoint opens exactly one agents_md span")
        return errors
    previous_errors = validate_state(previous)
    if previous_errors:
        return [f"Previous state is invalid: {error}" for error in previous_errors] + errors
    for key in ("schema_version", "workflow", "run_id", "worktree", "entry"):
        if previous.get(key) != candidate.get(key):
            errors.append(f"Transition cannot change {key}")
    if previous.get("input") != candidate.get("input"):
        errors.append("Transition cannot change input identity")
    if previous.get("lifecycle") in TERMINAL_LIFECYCLES:
        errors.append("Terminal state cannot transition")
        return errors
    allowed = LIFECYCLE_TRANSITIONS.get(previous.get("lifecycle"), frozenset())
    if candidate.get("lifecycle") not in allowed:
        errors.append(f"Lifecycle transition {previous.get('lifecycle')} -> {candidate.get('lifecycle')} is not allowed")
    previous_spans = previous.get("agents_md") or []
    candidate_spans = candidate.get("agents_md") or []
    if candidate_spans[: len(previous_spans)] != previous_spans:
        errors.append("agents_md spans cannot change or be removed, only appended")
    if previous.get("halt") is not None and candidate.get("halt") != previous.get("halt"):
        errors.append("halt facts cannot change once recorded")
    if candidate.get("lifecycle") == "halted" and candidate.get("halt") is None:
        errors.append("Entering halted requires halt facts")
    errors.extend(_validate_stage_transition(previous.get("stages"), candidate.get("stages")))
    errors.extend(_validate_append_only(previous.get("assumptions"), candidate.get("assumptions"), "assumptions"))
    errors.extend(_validate_append_only(previous.get("lessons"), candidate.get("lessons"), "lessons"))
    errors.extend(_validate_questions_transition(previous.get("questions"), candidate.get("questions")))
    return errors


def _commit(destination: Path, candidate: Dict[str, Any]) -> None:
    previous = _load(destination) if destination.exists() else None
    errors = validate_transition(previous, candidate)
    if errors:
        raise ValueError("; ".join(errors))
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


def checkpoint(destination: Path, candidate_path: Path) -> None:
    _commit(destination, _load(candidate_path))


# ---------------------------------------------------------------------------
# Stage association: `enter` records it, directly when a stage run is resumed rather than created, or by snapshot otherwise.
# Every reader that needs it resolves it the same way, live, from `run` or from the snapshot diff, so `gap`, `status`, `close`, and `guard` never disagree with each other.


def _stage_run_root(worktree_root: Path, stage: str) -> Path:
    return worktree_root / ".agents" / "kein" / "runs" / stage


def _list_run_dirs(run_root: Path) -> List[str]:
    if not run_root.exists():
        return []
    return sorted(child.name for child in run_root.iterdir() if child.is_dir())


def _find_unique_nonterminal_stage_run(stage: str, run_root: Path, worktree_root: Path) -> Optional[Path]:
    """A stage run that already exists, nonterminal, for this worktree -- a run being resumed rather than created.
    For execute this reuses `_execute.find_occupying_run`, whose own per-worktree claim file already makes it unique by construction.
    For ralplan and interview, which carry no such claim, uniqueness is scanned for directly, and an ambiguous match (more than one) is treated the same as none: `attach` is the explicit way past that."""
    if not run_root.exists():
        return None
    if stage == "execute":
        return _execute.find_occupying_run(worktree_root / ".agents" / "kein" / "runs", worktree_root)
    matches: List[Path] = []
    if stage == "ralplan":
        for state_path in sorted(run_root.glob("*/state.json")):
            try:
                payload = _load(state_path)
            except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
                continue
            if payload.get("lifecycle") not in _ralplan.NONTERMINAL_LIFECYCLES:
                continue
            repository = payload.get("repository")
            if isinstance(repository, str) and repository != "none" and Path(repository).resolve() == worktree_root.resolve():
                matches.append(state_path)
    else:
        for ledger_path in sorted(run_root.glob("*/ledger.md")):
            try:
                frontmatter = _parse_ledger(ledger_path.read_text())
            except (OSError, UnicodeError):
                continue
            if frontmatter.get("status") != "active":
                continue
            repository = frontmatter.get("repository")
            if repository and repository != "none" and Path(repository).resolve() == worktree_root.resolve():
                matches.append(ledger_path)
    return matches[0] if len(matches) == 1 else None


def _stage_association_detail(state: Dict[str, Any], stage: str) -> Tuple[Optional[Path], str]:
    stage_state = state["stages"][stage]
    if stage_state.get("run"):
        return Path(stage_state["run"]), "kept"
    if stage == "closeout":
        return None, "not applicable"
    if stage_state.get("status") != "entered":
        return None, "not entered"
    root = Path(state["worktree"])
    run_root = _stage_run_root(root, stage)
    current = set(_list_run_dirs(run_root))
    snapshot = set(stage_state.get("snapshot") or [])
    new = sorted(current - snapshot)
    if len(new) != 1:
        return None, "none" if not new else "ambiguous"
    child = run_root / new[0]
    candidate_file = child / ("ledger.md" if stage == "interview" else "state.json")
    if not candidate_file.is_file():
        return None, "none"
    return candidate_file, "resolved"


def _resolve_association(state: Dict[str, Any], stage: str) -> Optional[Path]:
    path, _ = _stage_association_detail(state, stage)
    return path


def _run_belongs_to_worktree(stage: str, run_path: Path, worktree_root: Path) -> bool:
    """Interview's compact completed/aborted ledger and ralplan's completed/aborted receipt carry no repository field at all -- there is nothing in either compact shape to check a path against.
    An absent field is trusted rather than refused, since `attach` exists precisely for the cases the automatic association cannot resolve on its own; a present field is still checked."""
    try:
        if stage == "interview":
            repository = _parse_ledger(run_path.read_text()).get("repository")
        elif stage == "execute":
            repository = _load(run_path).get("worktree", {}).get("root")
        else:
            repository = _load(run_path).get("repository")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
        return False
    if repository is None:
        return True
    return isinstance(repository, str) and repository != "none" and Path(repository).resolve() == worktree_root.resolve()


def _expected_execute_plan_reference(state: Dict[str, Any]) -> Optional[str]:
    """The plan path this flow is driving `execute` against, established without reading the occupying run's own file at all: the fsd input's own `reference` when `execute` is the entry stage -- the only classification that reaches `execute` directly, and one that always carries a plan reference (`classify_input`'s plan branch) -- or, when `ralplan` led here instead, the plan path recorded on `ralplan`'s own completed receipt (`plan.path`, the same field `gap` reads for its ralplan-completed row). `None` when neither can be read: too little evidence to call any occupant a match, so `enter` treats that the same as a mismatch rather than guessing either way."""
    if state["entry"] == "execute":
        return state["input"].get("reference")
    run_path = _resolve_association(state, "ralplan")
    if run_path is None:
        return None
    try:
        payload = _load(run_path)
    except Exception:
        return None
    if payload.get("lifecycle") != "completed":
        return None
    return payload.get("plan", {}).get("path")


def _same_plan_reference(candidate_reference: Any, expected_reference: Any, worktree_root: Path) -> bool:
    """Whether two plan references name the same file, compared as paths rather than as the raw strings each side happened to store: `execute start` and `ralplan start` keep an `--input`/`--plan` reference exactly as given, relative or absolute, and `classify_input` joins a relative one onto the worktree root without ever calling `.resolve()` on the result, so the same plan can be spelled two different ways -- relative here, absolute there, a `..`-bearing path, or an absolute spelling `os.path.realpath` has not touched (macOS's own `/var` -> `/private/var`, the same gap `_normalize_scope_entry` accounts for in `guard`). A relative side is joined onto `worktree_root` before both sides are run through `Path.resolve()`, which does not require the file to exist. `resolve()` can also raise for reasons that have nothing to do with a genuine mismatch -- a symlink loop raises `RuntimeError` on some Python versions, `OSError` on others -- so the catch here is broad by design: every caller of this function, directly or through `_occupying_execute_run`, reads its answer as ordinary evidence rather than expecting it to raise, `guard_check` among them, and a caller left to catch a resolution failure itself would refuse to run at all rather than simply not calling this pair a match. Neither side may be `None`: two absent references are not treated as a match, since there would be nothing there to compare."""
    if not isinstance(candidate_reference, str) or not isinstance(expected_reference, str):
        return False
    def _resolved(value: str) -> Path:
        path = Path(value)
        if not path.is_absolute():
            path = worktree_root / path
        try:
            return path.resolve()
        except Exception:
            return path
    return _resolved(candidate_reference) == _resolved(expected_reference)


def _occupying_execute_run(state: Dict[str, Any], exclude: Optional[Path]) -> Optional[Path]:
    """The nonterminal execute run currently occupying the worktree, other than `exclude`, whose own `input.reference` names the same plan this flow is executing (`_expected_execute_plan_reference`, compared with `_same_plan_reference`) -- reusing execute's own per-worktree claim (`find_occupying_run`) to find the occupant, but never treating a merely-different one as this flow's own replacement. That match is what keeps an operator's unrelated `/kein:execute` run from ever being read by `guard`, or from ever standing in for a finished `execute` stage in `gap` or `close`: only a run that is actually this flow's own continuation does that, the same run `enter` would adopt directly were it not already occupying the worktree when `enter` first ran. It is also what keeps this reading correct through the window `_guard_action`'s abort-then-restart recovery opens: the replacement execute run holds the claim from the moment `execute start` returns, before `attach` repoints `stages.execute.run` at it, so for exactly that long the kept association still names the just-aborted run while a different, live, matching one actually occupies the worktree. A read failure, or no expected reference to compare against, reads as no matching occupant, the same as everywhere else here that treats an unreadable or absent file as no evidence rather than raising."""
    root = Path(state["worktree"])
    runs_dir = root / ".agents" / "kein" / "runs"
    try:
        occupant = _execute.find_occupying_run(runs_dir, root, exclude=exclude)
    except Exception:
        return None
    if occupant is None:
        return None
    expected = _expected_execute_plan_reference(state)
    if expected is None:
        return None
    try:
        occupant_reference = _load(occupant).get("input", {}).get("reference")
    except Exception:
        return None
    return occupant if _same_plan_reference(occupant_reference, expected, root) else None


def enter(destination: Path, stage: str) -> bool:
    """Marks `stage` entered. Idempotent once entered; keeps a resume-kept association untouched.
    Otherwise either directly associates a uniquely resumed pre-existing run, or snapshots the stage's run root for a later reader to diff.
    For `execute`, a uniquely resumed run is adopted only when its own `input.reference` names the same plan this flow is executing (`_expected_execute_plan_reference`, compared as a resolved path by `_same_plan_reference` rather than as the raw string each side happened to store); an occupant that does not match -- someone else's `/kein:execute` run left occupying the same worktree -- is refused by name and lifecycle, the same way `start` refuses an occupying fsd run, rather than silently claimed as this flow's own or silently stepped around (a snapshot would still hit the same run when `execute start` itself refuses the still-occupied worktree, but only later and less clearly than naming it here). The refusal is worded differently for the two ways a match can fail to be established: when the plan this flow executes cannot even be read yet -- `ralplan` has not completed, or its receipt is unreadable -- the refusal says so and names `attach` as the way past a false negative, for the case the occupant genuinely is this flow's own run; when both references are known and simply differ, the refusal names both and tells the lead to finish or abort the occupying run before rerunning `enter`, without suggesting `attach` -- a confirmed mismatch is not a spelling the comparison merely failed to resolve.
    Returns whether it wrote anything."""
    if stage not in ("interview", "ralplan", "execute"):
        raise ValueError("enter names interview, ralplan, or execute; use `closeout` for the closeout stage")
    state = _load(destination)
    if state.get("lifecycle") in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    stage_state = state["stages"][stage]
    if stage_state["status"] == "skipped":
        raise ValueError(f"{stage} is skipped for this run")
    if stage_state["status"] == "entered":
        return False
    candidate = copy.deepcopy(state)
    candidate_stage = candidate["stages"][stage]
    if candidate_stage.get("run") is None:
        root = Path(candidate["worktree"])
        run_root = _stage_run_root(root, stage)
        resumed = _find_unique_nonterminal_stage_run(stage, run_root, root)
        if resumed is not None and stage == "execute":
            expected_reference = _expected_execute_plan_reference(candidate)
            try:
                occupant_payload = _load(resumed)
            except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
                occupant_payload = {}
            occupant_reference = occupant_payload.get("input", {}).get("reference")
            occupant_lifecycle = occupant_payload.get("lifecycle", "?")
            if expected_reference is None:
                raise ValueError(
                    "a nonterminal execute run already occupies the worktree at "
                    f"{resumed} ({occupant_lifecycle}), but the plan this flow executes could not be "
                    "established -- ralplan has not completed yet, or its receipt could not be read; wait "
                    "for ralplan to complete, or if this occupant genuinely is the flow's own run, pin it "
                    f"with `ocs state fsd attach {destination} execute {resumed}`"
                )
            if not _same_plan_reference(occupant_reference, expected_reference, root):
                raise ValueError(
                    "a nonterminal execute run already occupies the worktree at "
                    f"{resumed} ({occupant_lifecycle}), but its own input.reference ({occupant_reference!r}) "
                    f"does not match the plan this flow executes ({expected_reference!r}); finish or abort "
                    f"{resumed} before rerunning enter"
                )
        if resumed is not None:
            candidate_stage["run"] = str(resumed)
        else:
            candidate_stage["snapshot"] = _list_run_dirs(run_root)
    candidate_stage["status"] = "entered"
    _commit(destination, candidate)
    return True


def closeout(destination: Path) -> bool:
    state = _load(destination)
    if state.get("lifecycle") in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    if state["stages"]["closeout"]["status"] == "entered":
        return False
    candidate = copy.deepcopy(state)
    candidate["stages"]["closeout"]["status"] = "entered"
    _commit(destination, candidate)
    return True


def attach(destination: Path, stage: str, run_path: Path) -> None:
    if stage not in ("interview", "ralplan", "execute"):
        raise ValueError("attach names interview, ralplan, or execute")
    state = _load(destination)
    if state.get("lifecycle") in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    if not run_path.is_file():
        raise ValueError(f"{run_path} does not exist")
    root = Path(state["worktree"])
    if not _run_belongs_to_worktree(stage, run_path, root):
        raise ValueError(f"{run_path} does not belong to this worktree's {stage} run")
    stage_state = state["stages"][stage]
    if stage_state["status"] == "skipped":
        raise ValueError(f"{stage} is skipped for this run")
    candidate = copy.deepcopy(state)
    candidate_stage = candidate["stages"][stage]
    candidate_stage["run"] = str(run_path)
    if candidate_stage["status"] == "pending":
        candidate_stage["status"] = "entered"
    _commit(destination, candidate)


# ---------------------------------------------------------------------------
# gap


def _question_by_id(state: Dict[str, Any], question_id: Optional[str]) -> Optional[Dict[str, Any]]:
    if not question_id:
        return None
    for item in state.get("questions", []):
        if item.get("id") == question_id:
            return item
    return None


def _parked_question_unanswered(state: Dict[str, Any], task: Dict[str, Any]) -> bool:
    ref = (task.get("parked") or {}).get("decision_ref")
    question = _question_by_id(state, ref)
    return question is not None and question.get("answer") is None


def gap(state: Dict[str, Any]) -> Dict[str, Any]:
    """`{gap, completed, next, action}`. Rows are evaluated in the table's own order and the first satisfied row wins.
    A nonterminal fsd lifecycle is checked before any stage row, so a paused, completed, halted, or aborted run always reports no gap regardless of what the underlying stage evidence would otherwise read -- this is what keeps the last row and the execute-derived row mutually exclusive once `close` has paused.
    Every row past the first reads a file this script did not just write -- an associated run's state or ledger, or the requirements document it names -- so each row's read is wrapped, and any failure (missing, unreadable, malformed) is treated the same as "an unfinished or unreadable stage gives no row": that row does not fire, and evaluation continues to the next one, rather than the whole check raising.
    The execute-derived closeout row also does not fire while a different nonterminal execute run occupies the worktree than the one `stages.execute.run` names (`_occupying_execute_run`): between `_guard_action`'s own `checkpoint ... aborted` and the `attach` that repoints the kept association at the replacement, the kept link still names the just-aborted run while the replacement already holds the claim, and reading the stale link as if execute's side of the flow had ended would open a false closeout window for exactly that long."""
    if state["lifecycle"] != "active":
        return {"gap": False, "completed": None, "next": None, "action": "no gap"}
    stages = state["stages"]
    entry = state["entry"]
    if stages[entry]["status"] == "pending":
        target = state["input"].get("reference") or state["input"].get("summary")
        return {"gap": True, "completed": None, "next": entry, "action": f"invoke /kein:{entry} {target}"}
    if stages["ralplan"]["status"] == "pending":
        try:
            run_path = _resolve_association(state, "interview")
            if run_path is not None:
                payload = _parse_ledger(run_path.read_text())
                if payload.get("status") == "completed":
                    requirements_path = payload.get("requirements_path")
                    if requirements_path and _requirements_status(Path(requirements_path)) == "Approved":
                        return {"gap": True, "completed": "interview", "next": "ralplan",
                                "action": f"invoke /kein:ralplan {requirements_path}"}
        except Exception:
            pass
    if stages["execute"]["status"] == "pending":
        try:
            run_path = _resolve_association(state, "ralplan")
            if run_path is not None:
                payload = _load(run_path)
                if payload.get("lifecycle") == "completed":
                    plan_path = payload.get("plan", {}).get("path")
                    return {"gap": True, "completed": "ralplan", "next": "execute",
                            "action": f"invoke /kein:execute {plan_path}"}
        except Exception:
            pass
    if stages["closeout"]["status"] == "pending":
        for stage in ("interview", "ralplan"):
            try:
                run_path = _resolve_association(state, stage)
                if run_path is None:
                    continue
                payload = _parse_ledger(run_path.read_text()) if stage == "interview" else _load(run_path)
                key = "status" if stage == "interview" else "lifecycle"
                if payload.get(key) == "aborted":
                    return {"gap": True, "completed": stage, "next": "closeout", "action": "run ocs state fsd closeout <state>"}
            except Exception:
                continue
        try:
            execute_run = _resolve_association(state, "execute")
            if execute_run is not None and _occupying_execute_run(state, execute_run) is None:
                payload = _load(execute_run)
                lifecycle = payload.get("lifecycle")
                if lifecycle in {"completed", "aborted"}:
                    return {"gap": True, "completed": "execute", "next": "closeout", "action": "run ocs state fsd closeout <state>"}
                if lifecycle == "blocked":
                    tasks = payload.get("tasks", [])
                    write_active = any(task.get("status") in _execute.WRITE_ACTIVE_STATUSES for task in tasks)
                    parked = [task for task in tasks if task.get("status") == "parked"]
                    if not write_active and parked and all(_parked_question_unanswered(state, task) for task in parked):
                        return {"gap": True, "completed": "execute", "next": "closeout", "action": "run ocs state fsd closeout <state>"}
                    if not write_active and not parked:
                        whole_run = [q for q in state["questions"] if q.get("parks") == "whole run" and q.get("answer") is None]
                        if whole_run:
                            return {"gap": True, "completed": "execute", "next": "closeout", "action": "run ocs state fsd closeout <state>"}
        except Exception:
            pass
    return {"gap": False, "completed": None, "next": None, "action": "no gap"}


def status(state: Dict[str, Any]) -> Dict[str, Any]:
    stage_report = {}
    for stage in STAGES:
        path, detail = _stage_association_detail(state, stage)
        stage_report[stage] = {"status": state["stages"][stage]["status"], "run": str(path) if path else None, "association": detail}
    result: Dict[str, Any] = {"lifecycle": state["lifecycle"], "entry": state["entry"], "stages": stage_report}
    result.update(gap(state))
    return result


# ---------------------------------------------------------------------------
# guard


def _normalize_scope_entry(entry: str, worktree_root: Path) -> str:
    """`execute start` accepts an absolute path or a relative one carrying `..`, as long as it still resolves inside the repository, and the scope it records is exactly whatever text the ledger wrote -- not a canonical form.
    `_scopes_collide` reads scope entries as literal repo-relative text, so an absolute or `..`-bearing entry has to be resolved against the worktree root and re-expressed relative to it before that reading (or `_covers_agents_md`'s own root check) can see what it actually names.
    `state["worktree"]` is itself a resolved path (`canonical_worktree` calls `.resolve()`), but an absolute scope entry the ledger recorded need not be: on macOS a temp directory under `/var/...` is itself a symlink to `/private/var/...`, and `execute start` accepts and stores an absolute scope entry in whichever spelling it was given, unresolved.
    An absolute entry's *parent* is therefore run through `os.path.realpath` -- which does touch the filesystem, unlike the pure `os.path.normpath`/`os.path.relpath` string math that follows -- so it lands in the same resolved form as the worktree root before the two are compared; the entry's own final component is left exactly as named, deliberately not resolved, since `os.path.realpath` on the whole entry would also follow a symlinked leaf: an absolute path to AGENTS.md would resolve to whatever AGENTS.md itself points at if it happens to be a symlink, rather than staying "AGENTS.md" relative to the worktree. A relative entry never introduces a symlink of its own in its directory prefix (the worktree root it is joined to is already resolved) and is left to plain string math."""
    candidate = Path(entry)
    if candidate.is_absolute():
        resolved = Path(os.path.realpath(str(candidate.parent))) / candidate.name
    else:
        resolved = worktree_root / candidate
    normalized = os.path.normpath(str(resolved))
    try:
        return os.path.relpath(normalized, str(worktree_root))
    except ValueError:
        return normalized


def _covers_agents_md(entry: str, worktree_root: Path) -> bool:
    """A root-covers-everything reading this keeps for itself rather than delegating: a scope entry that normalizes to the repository root has no path parts at all, and is treated as covering AGENTS.md unconditionally, before `_scopes_collide` is ever asked about it -- so this does not depend on how `_scopes_collide` happens to read an empty-parts entry on either side of it, only on what `_scope_parts` reports.
    Everything with at least one path part defers to execute's own reading, over the entry normalized relative to the worktree root, folded to lowercase before the comparison: `agents.md`, `Agents.MD`, and every other case variant name the same file AGENTS.md does on the case-insensitive filesystems this repository already has to account for elsewhere (macOS's own `/var` -> `/private/var` symlink, handled just above), so the comparison is case-insensitive unconditionally rather than only where the host filesystem happens to require it."""
    normalized = _normalize_scope_entry(entry, worktree_root)
    if not _execute._scope_parts(normalized):
        return True
    return _execute._scopes_collide(normalized.lower(), "AGENTS.md".lower())


def _guard_action(state: Dict[str, Any]) -> str:
    """The recovery `guard` names when it finds a violation, naming the actual plan this flow is executing (`_expected_execute_plan_reference`) as the restart's `--input` rather than a `<plan|brief>` placeholder: this flow always executes a plan, and a `--kind brief` replacement stores `input.reference: null`, which `_same_plan_reference` can never call a match against that plan -- exactly the gap that would reopen the false-closeout and vacuous-guard windows `_occupying_execute_run` exists to close, between this abort and the `attach` the same recovery ends with. When the plan cannot be read (should not happen once `guard` has already read a real ledger, but guarded against regardless), a placeholder names what the lead must supply instead of a guess. `--worktree` is likewise the run's own actual worktree rather than a placeholder: `execute start` requires it, so the printed command would fail as given without it."""
    plan_reference = _expected_execute_plan_reference(state)
    plan_argument = plan_reference if plan_reference is not None else "<the plan this flow executes>"
    return (
        "an existing task's scope cannot change and tasks cannot be removed, and parking the task does "
        "not clear this: its scope is unchanged while parked, so guard keeps failing and close keeps "
        "refusing. The fix is to abort the execute run (ocs state execute checkpoint <state.json> "
        "<aborted-candidate.json>) and start a new one without the task (ocs state execute start "
        f"--run-root <runs/execute> --slug <s> --kind plan --input {plan_argument} --worktree "
        f"{state['worktree']} --tasks <ledger without it>), then ocs state fsd attach <state.json> "
        "execute <new-state.json> and rerun guard. If the run cannot be restarted, close will keep "
        "refusing and the run ends halted"
    )


GUARD_NO_ASSOCIATION = (
    "execute is entered but its association is {detail}; guard cannot read a run it cannot find, so "
    "run `ocs state fsd attach <state.json> execute <path>` (or `enter`, if the ambiguity was a "
    "passing snapshot race) before guard can check it"
)


def _guard_failure_message(guard_result: Dict[str, Any]) -> str:
    if "reason" in guard_result:
        return guard_result["reason"]
    names = ", ".join(sorted({violation["task"] for violation in guard_result["violations"]}))
    return f"guard failed: task(s) {names} scope AGENTS.md"


def guard_check(state: Dict[str, Any]) -> Dict[str, Any]:
    """Clean when execute is not yet entered, or entered but has no run there yet (`none`) -- the ordinary transient window between `enter execute` and the skill's own `execute start`, where there is genuinely nothing to check.
    Once execute is entered, an `ambiguous` association (more than one candidate, so no read is safe) or an associated run this cannot actually read is *not* silently clean: it is a check that could not run, and says so, pointing at `attach`, rather than letting the absence of evidence read as the absence of a problem.
    Before reading tasks, the kept association is checked against `_occupying_execute_run`: while `_guard_action`'s own abort-then-restart recovery is between its `checkpoint ... aborted` and its `attach`, the kept link still names the just-aborted run, but a different, live replacement already holds the worktree's claim -- `guard` reads that live run's own tasks instead, so a task the lead already restarted without is never the reason a still-stale link fails it."""
    stage_state = state["stages"]["execute"]
    if stage_state["status"] != "entered":
        return {"clean": True, "violations": []}
    execute_run, detail = _stage_association_detail(state, "execute")
    if execute_run is None:
        if detail == "ambiguous":
            return {"clean": False, "violations": [], "reason": GUARD_NO_ASSOCIATION.format(detail=detail)}
        return {"clean": True, "violations": []}
    live_run = _occupying_execute_run(state, execute_run)
    if live_run is not None:
        execute_run = live_run
    try:
        payload = _load(execute_run)
    except Exception:
        return {"clean": False, "violations": [], "reason": GUARD_NO_ASSOCIATION.format(detail=f"unreadable at {execute_run}")}
    worktree_root = Path(state["worktree"])
    violations = []
    for task in payload.get("tasks", []):
        for entry in task.get("scope") or []:
            if _covers_agents_md(entry, worktree_root):
                violations.append({"task": task.get("id"), "scope_entry": entry})
    result: Dict[str, Any] = {"clean": not violations, "violations": violations}
    if violations:
        result["action"] = _guard_action(state)
    return result


# ---------------------------------------------------------------------------
# close / halt / resume, and the retrospective's location while execute is still nonterminal.
#
# A retrospective written directly under `ocs state-dir retros/` while execute has not yet reached a completed receipt is an untracked file outside `.agents/kein/runs/`, which is the only prefix execute's own fingerprint excludes -- so it would count as drift on the very next `execute reconcile`.
# `close` refuses a `--retro` outside `.agents/kein/runs/` on the `paused` outcome while execute's own run is still nonterminal (this fsd run's own `runs/fsd/<run>/` directory, itself excluded from every workflow's fingerprint the same way, is the natural place to point it); once execute reaches a terminal lifecycle, or was never started, the check no longer applies.
# `close` only relocates the file, to the durable `retros/<YYMMDD>-<slug>.md` path, on the `completed` outcome; a `paused` outcome or a refusal leaves the file exactly where it was handed to it.


def _run_slug(run_id: str) -> str:
    parts = run_id.split("-", 2)
    return parts[2] if len(parts) == 3 else run_id


def _durable_retro_path(state: Dict[str, Any]) -> Path:
    root = Path(state["worktree"])
    slug = _run_slug(state["run_id"])
    today = datetime.now().astimezone().strftime("%y%m%d")
    return root / ".agents" / "kein" / "retros" / f"{today}-{slug}.md"


def _retro_missing_ids(text: str, state: Dict[str, Any]) -> List[str]:
    """The retrospective is the durable copy of every assumption, question, and lesson this run recorded, so it has to cite all of them, not merely one -- a retro that names only the first of three parked questions would silently drop the other two from the record the next reader inherits.
    Returns the ids it does not cite, in minting order, so a refusal can name exactly what is missing."""
    ids = ([item["id"] for item in state["assumptions"]]
           + [item["id"] for item in state["questions"]]
           + [item["id"] for item in state["lessons"]])
    return [identifier for identifier in ids if not re.search(rf"\b{re.escape(identifier)}\b", text)]


def _execute_stage_reachable(state: Dict[str, Any]) -> bool:
    """False once interview or ralplan has aborted: the flow ends at closeout without execute ever running (gap's own row for it), so there is nothing there for `close` to wait on."""
    for stage in ("interview", "ralplan"):
        try:
            run_path = _resolve_association(state, stage)
            if run_path is None:
                continue
            payload = _parse_ledger(run_path.read_text()) if stage == "interview" else _load(run_path)
            key = "status" if stage == "interview" else "lifecycle"
            if payload.get(key) == "aborted":
                return False
        except Exception:
            continue
    return True


def _execute_side_done(state: Dict[str, Any]) -> bool:
    """Whether `execute`'s side of the flow is done for `close`'s purposes: either its associated run is a completed receipt, or it never started at all because interview or ralplan aborted first, so the flow was never going to reach it.
    An `execute` run that itself aborted, or one that is simply absent while nothing upstream aborted (execute has not been reached yet), is not done. Nor is it done while a different nonterminal execute run occupies the worktree than the one associated (`_occupying_execute_run`) -- the same abort-then-restart window `gap`'s execute-derived closeout row guards against, so `close` cannot read a stale kept link as a finished execute stage while its replacement is still live."""
    execute_run = _resolve_association(state, "execute")
    if execute_run is None:
        return not _execute_stage_reachable(state)
    if _occupying_execute_run(state, execute_run) is not None:
        return False
    try:
        payload = _load(execute_run)
    except Exception:
        return False
    return payload.get("lifecycle") == "completed"


def _close_execute_run(state: Dict[str, Any]) -> Optional[Path]:
    """The execute run `close` and `halt` should actually read: the live, matching occupant `_occupying_execute_run` finds in place of a stale kept link -- the same substitution `guard` makes -- or the kept association itself when there is no such occupant. Preferring the live run here is what keeps the retrospective-location rule below applying correctly while a matching replacement is genuinely still nonterminal, even though the kept link it has not yet been `attach`ed over reads as an already-terminal receipt."""
    execute_run = _resolve_association(state, "execute")
    if execute_run is None:
        return None
    live_run = _occupying_execute_run(state, execute_run)
    return live_run if live_run is not None else execute_run


def _execute_lifecycle_or_none(state: Dict[str, Any]) -> Optional[str]:
    execute_run = _close_execute_run(state)
    if execute_run is None:
        return None
    try:
        return _load(execute_run).get("lifecycle")
    except Exception:
        return None


def _execute_not_done_message(state: Dict[str, Any]) -> str:
    """`close`'s and `halt`'s refusal text naming execute's current status. The status itself is read the way `_execute_lifecycle_or_none` reads it -- off the live, matching occupant in place of a stale kept link when `_occupying_execute_run` finds one -- and the message is extended with that run's own path and an `attach` pointer exactly when such a substitution happened, so the refusal also names what to do about it rather than only a lifecycle word that, on its own, would describe a run the flow has already moved past."""
    kept_run = _resolve_association(state, "execute")
    live_run = _occupying_execute_run(state, kept_run) if kept_run is not None else None
    read_run = live_run if live_run is not None else kept_run
    try:
        status = (_load(read_run).get("lifecycle") if read_run is not None else None) or "not started"
    except Exception:
        status = "not started"
    message = f"execute is {status}, not completed"
    if live_run is not None:
        message += (
            f"; a matching execute run is live at {live_run}, but fsd's own association still names "
            f"{kept_run} -- run `ocs state fsd attach <state.json> execute {live_run}` and retry"
        )
    return message


def close(destination: Path, retro_path: Path, next_action: Optional[str]) -> None:
    """Three outcomes, checked in this order.
    `paused`, when some fsd question is unanswered, regardless of execute's own state -- a question can exist with execute already completed or never started at all (before a ralplan/interview abort, or an AGENTS.md story turned into a whole-run question), and a paused run must still be reachable then, not carried past the open question into `completed`.
    Failing that, `completed`, when execute's side of the flow is done -- either a completed receipt, or never reached at all because interview or ralplan aborted first.
    Failing both, close refuses and names the unfinished stage.
    This ordering is what keeps 'execute completed with a leftover unanswered question' (pauses) distinct from 'execute still has work to do and nothing is unanswered' (refuses, once the only question was answered and nothing else remains but execute itself).

    While execute is still nonterminal (its own run exists and has not reached a terminal lifecycle) and the outcome here is `paused`, the retrospective must live under this worktree's `.agents/kein/runs/` -- the one prefix every workflow's fingerprint excludes -- so it cannot register as drift on `execute reconcile` while execute is still live.
    On `completed`, the file is moved to its durable path before the checkpoint that names that path is committed (unless `--retro` already names the durable path, in which case nothing moves): if the commit is then refused, the move is undone and the run stays `active`, exactly as `close` found it, so the caller can retry; if the move itself fails, its OSError propagates before anything is committed, and the run is likewise untouched."""
    state = _load(destination)
    if state["lifecycle"] != "active":
        raise ValueError(f"close requires an active run; lifecycle is {state['lifecycle']}")
    root = Path(state["worktree"])
    current_hash = _read_agents_md_hash(root)
    if state["agents_md"][-1].get("sha256") != current_hash:
        raise ValueError("AGENTS.md changed since the current span began")
    guard_result = guard_check(state)
    if not guard_result["clean"]:
        raise ValueError(_guard_failure_message(guard_result))
    if not retro_path.is_file():
        raise ValueError(f"{retro_path} does not exist")
    retro_text = retro_path.read_text()
    missing_ids = _retro_missing_ids(retro_text, state)
    if missing_ids:
        raise ValueError(f"retrospective does not cite every assumption, question, and lesson id; missing {', '.join(missing_ids)}")
    unanswered = [item for item in state["questions"] if item.get("answer") is None]
    candidate = copy.deepcopy(state)
    if unanswered:
        execute_lifecycle = _execute_lifecycle_or_none(state)
        if execute_lifecycle is not None and execute_lifecycle not in _execute.TERMINAL_LIFECYCLES:
            runs_prefix = (root / ".agents" / "kein" / "runs").resolve()
            try:
                retro_path.resolve().relative_to(runs_prefix)
            except ValueError:
                raise ValueError(
                    f"while execute is still {execute_lifecycle}, --retro must be a path under {runs_prefix} "
                    f"(this fsd run's own directory is a safe choice), so it cannot register as drift on "
                    f"execute's own worktree fingerprint before execute reaches a terminal receipt; got {retro_path}"
                )
        candidate["lifecycle"] = "paused"
        candidate["retrospective"] = str(retro_path)
        candidate["next_action"] = next_action or ("paused: answer " + ", ".join(item["id"] for item in unanswered) + ", then resume")
        _commit(destination, candidate)
    elif _execute_side_done(state):
        durable = _durable_retro_path(state)
        already_durable = retro_path.resolve() == durable.resolve()
        if not already_durable and durable.exists():
            raise ValueError(f"a retrospective already exists at {durable}; move or rename it before closing")
        candidate["lifecycle"] = "completed"
        candidate["retrospective"] = str(durable)
        candidate["next_action"] = next_action or "completed"
        if not already_durable:
            durable.parent.mkdir(parents=True, exist_ok=True)
            retro_path.replace(durable)
        try:
            _commit(destination, candidate)
        except Exception:
            # The move (if any) already landed, but the checkpoint it was moved for did not: put the file back where `close` found it, so the run -- still `active`, since nothing committed -- can be retried exactly as it stood before this call.
            if not already_durable:
                durable.replace(retro_path)
            raise
    else:
        raise ValueError(_execute_not_done_message(state))


def _structural_close_blocker(state: Dict[str, Any]) -> Optional[str]:
    """The part of `close`'s refusal surface that does not depend on the retrospective file it is handed: AGENTS.md drift, a guard violation, or execute genuinely unfinished with nothing left unanswered.
    When none of these hold, close would succeed given any valid retrospective, so halting would be premature."""
    root = Path(state["worktree"])
    current_hash = _read_agents_md_hash(root)
    if state["agents_md"][-1].get("sha256") != current_hash:
        return "AGENTS.md changed since the current span began"
    guard_result = guard_check(state)
    if not guard_result["clean"]:
        return _guard_failure_message(guard_result)
    unanswered = any(item.get("answer") is None for item in state["questions"])
    if _execute_side_done(state) or unanswered:
        return None
    return _execute_not_done_message(state)


def halt(destination: Path, reason: str, next_action: Optional[str]) -> None:
    state = _load(destination)
    if state["lifecycle"] != "active":
        raise ValueError(f"halt requires an active run; lifecycle is {state['lifecycle']}")
    if not reason or not reason.strip():
        raise ValueError("halt needs --reason <text>")
    blocker = _structural_close_blocker(state)
    if blocker is None:
        raise ValueError("halt is refused: close would succeed")
    candidate = copy.deepcopy(state)
    candidate["lifecycle"] = "halted"
    candidate["halt"] = {"reason": reason.strip()}
    candidate["next_action"] = next_action or f"halted: {reason.strip()}"
    _commit(destination, candidate)


def resume(destination: Path, next_action: Optional[str]) -> None:
    """Refuses while any question is unanswered.
    It also refuses, rather than guessing, if execute's associated run exists but cannot actually be read (corrupt or otherwise unparseable): the load is not wrapped, so that error surfaces the same way any other refusal does.
    Otherwise it moves `paused -> active`, opens a new `agents_md` span over AGENTS.md's current bytes (keeping earlier spans), and always resets `closeout` to `pending`.
    Whether it also resets `execute` to `pending` (pinning its `run` to the same association, so `enter execute` keeps it rather than re-snapshotting) depends on whether `execute`'s associated run is present and nonterminal at that moment -- the one case this resets.
    In every other case, `execute`'s own stage is left exactly as it was, and only `closeout` resets, so the next `gap` decides where the run goes from what it finds rather than from anything `resume` assumed. Four situations route through that one "leave it alone" branch:
    `execute`'s associated run is present and already terminal (a completed or aborted receipt), in which case `gap` reports the same execute-derived row again and the next action is `closeout`;
    upstream (`interview` or `ralplan`) aborted before `execute` was ever going to run, in which case `gap` reports the same aborted-stage row again and the next action is `closeout`;
    `ralplan` completed but `execute` was never entered (a question paused the run before the lead invoked it), in which case `gap` reports the ralplan-completed row again and the next action is to invoke `execute`;
    or `execute` was entered but never got an association at all (no run created, or an ambiguous one), in which case `gap` finds no evidence either way and reports no gap until `attach` or a fresh `execute start` resolves it."""
    state = _load(destination)
    if state["lifecycle"] != "paused":
        raise ValueError(f"resume requires a paused run; lifecycle is {state['lifecycle']}")
    unanswered = [item for item in state["questions"] if item.get("answer") is None]
    if unanswered:
        raise ValueError("cannot resume while a question is unanswered: " + ", ".join(item["id"] for item in unanswered))
    candidate = copy.deepcopy(state)
    root = Path(candidate["worktree"])
    execute_run = _resolve_association(state, "execute")
    execute_payload = _load(execute_run) if execute_run is not None else None
    execute_terminal_or_absent = execute_run is None or (execute_payload is not None and execute_payload.get("lifecycle") in _execute.TERMINAL_LIFECYCLES)
    if not execute_terminal_or_absent:
        candidate["stages"]["execute"]["status"] = "pending"
        candidate["stages"]["execute"]["run"] = str(execute_run)
    candidate["stages"]["closeout"] = {"status": "pending", "snapshot": [], "run": None}
    candidate["agents_md"] = list(candidate["agents_md"]) + [{"span_started_at": _now(), "sha256": _read_agents_md_hash(root)}]
    candidate["lifecycle"] = "active"
    candidate["next_action"] = next_action or "reassess the current stage's gap"
    _commit(destination, candidate)


def abort(destination: Path, reason: str, next_action: Optional[str]) -> None:
    state = _load(destination)
    if state["lifecycle"] in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    if not reason or not reason.strip():
        raise ValueError("abort needs --reason <text>")
    candidate = copy.deepcopy(state)
    candidate["lifecycle"] = "aborted"
    candidate["next_action"] = next_action or f"aborted: {reason.strip()}"
    _commit(destination, candidate)


# ---------------------------------------------------------------------------
# report


def report(state: Dict[str, Any]) -> str:
    lines: List[str] = []
    if state["lifecycle"] == "halted":
        lines += ["## Halted", "", (state.get("halt") or {}).get("reason", ""), ""]
    lines += ["## Assumptions", ""]
    if state["assumptions"]:
        for item in state["assumptions"]:
            lines.append(f"- {item['id']} ({item['stage']}): {item['decision']} -- chose {item['chosen']}; "
                         f"reversal cost: {item['reversal_cost']} ({item['where']})")
    else:
        lines.append("None.")
    lines += ["", "## Parked questions", ""]
    if state["questions"]:
        for item in state["questions"]:
            state_word = f"answered: {item['answer']}" if item.get("answer") else "unanswered"
            lines.append(f"- {item['id']} ({item['stage']}): {item['question']} -- {state_word}; parks {item['parks']}. "
                         "Answer by re-invoking /kein:fsd with the answers.")
    else:
        lines.append("None.")
    lines += ["", "## Lesson proposals", ""]
    if state["lessons"]:
        for index, lesson_item in enumerate(state["lessons"], start=1):
            lines.append(f"{index}. {lesson_item['id']}: {lesson_item['line']} -- {lesson_item['why']} (vetoable)")
    else:
        lines.append("None.")
    lines += ["", "## Retrospective", ""]
    lines.append(state.get("retrospective") or "None.")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# assume / question / answer / lesson


def assume(destination: Path, stage: str, decision: str, chosen: str, alternatives: List[str],
           reversal_cost: str, where: str, next_action: Optional[str]) -> str:
    state = _load(destination)
    if state["lifecycle"] in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    candidate = copy.deepcopy(state)
    new_id = _mint_id([item["id"] for item in candidate["assumptions"]], "A")
    candidate["assumptions"].append({
        "id": new_id, "stage": stage, "decision": decision, "chosen": chosen,
        "alternatives": alternatives, "reversal_cost": reversal_cost, "where": where,
    })
    if next_action:
        candidate["next_action"] = next_action
    _commit(destination, candidate)
    return new_id


def question(destination: Path, stage: str, question_text: str, options: List[str], recommended: str,
             why_irreversible: str, parks: str, next_action: Optional[str]) -> str:
    state = _load(destination)
    if state["lifecycle"] in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    candidate = copy.deepcopy(state)
    new_id = _mint_id([item["id"] for item in candidate["questions"]], "Q")
    candidate["questions"].append({
        "id": new_id, "stage": stage, "question": question_text, "options": options,
        "recommended": recommended, "why_irreversible": why_irreversible, "parks": parks, "answer": None,
    })
    if next_action:
        candidate["next_action"] = next_action
    _commit(destination, candidate)
    return new_id


def answer(destination: Path, question_id: str, text: str, next_action: Optional[str]) -> None:
    state = _load(destination)
    if state["lifecycle"] in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    if not text or not text.strip():
        raise ValueError("answer needs --text <text>")
    candidate = copy.deepcopy(state)
    target = next((item for item in candidate["questions"] if item["id"] == question_id), None)
    if target is None:
        raise ValueError(f"no such question: {question_id}")
    if target.get("answer") is not None:
        raise ValueError(f"{question_id} is already answered")
    target["answer"] = text.strip()
    if next_action:
        candidate["next_action"] = next_action
    _commit(destination, candidate)


def lesson(destination: Path, line: str, why: str, next_action: Optional[str]) -> str:
    state = _load(destination)
    if state["lifecycle"] in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    candidate = copy.deepcopy(state)
    new_id = _mint_id([item["id"] for item in candidate["lessons"]], "L")
    candidate["lessons"].append({"id": new_id, "line": line, "why": why})
    if next_action:
        candidate["next_action"] = next_action
    _commit(destination, candidate)
    return new_id


# ---------------------------------------------------------------------------
# start


def _find_nonterminal_fsd_run(run_root: Path, worktree_root: Path, exclude: Optional[Path] = None) -> Optional[Path]:
    if not run_root.exists():
        return None
    excluded = exclude.resolve() if exclude is not None else None
    for state_path in sorted(run_root.glob("*/state.json")):
        if excluded is not None and state_path.resolve() == excluded:
            continue
        try:
            payload = _load(state_path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
            continue
        if payload.get("lifecycle") in NONTERMINAL_LIFECYCLES and Path(payload.get("worktree", "")).resolve() == worktree_root.resolve():
            return state_path
    return None


def start(destination: Path, input_text: str, worktree_path: Path, next_action: Optional[str]) -> None:
    if destination.exists():
        raise ValueError(f"{destination} already exists; a run is started once")
    root, _ = _execute.canonical_worktree(worktree_path)
    run_root = destination.parent.parent
    occupant = _find_nonterminal_fsd_run(run_root, root, exclude=destination)
    if occupant is not None:
        payload = _load(occupant)
        raise ValueError(f"a nonterminal fsd run already exists for this worktree: {occupant} ({payload.get('lifecycle')})")
    classification = classify_input(input_text, root)
    entry = classification["entry"]
    order = ("interview", "ralplan", "execute")
    entry_index = order.index(entry)
    stages = {stage: {"status": "skipped" if index < entry_index else "pending", "snapshot": [], "run": None}
              for index, stage in enumerate(order)}
    stages["closeout"] = {"status": "pending", "snapshot": [], "run": None}
    span = {"span_started_at": _now(), "sha256": _read_agents_md_hash(root)}
    target = classification["reference"] or classification["summary"]
    candidate = {
        "schema_version": SCHEMA_VERSION, "workflow": "fsd", "run_id": destination.parent.name,
        "lifecycle": "active", "worktree": str(root), "entry": entry,
        "input": {"kind": classification["kind"], "reference": classification["reference"], "summary": classification["summary"]},
        "agents_md": [span], "halt": None, "stages": stages,
        "assumptions": [], "questions": [], "lessons": [],
        "retrospective": None,
        "next_action": next_action or f"invoke /kein:{entry} {target}",
    }
    _commit(destination, candidate)


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
    return _execute.mint_run_dir(args.run_root, args.slug) / "state.json"


# ---------------------------------------------------------------------------
# CLI


def _split_csv(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)

    validate_parser = commands.add_parser("validate")
    validate_parser.add_argument("state", type=Path)

    checkpoint_parser = commands.add_parser("checkpoint", help="promote a hand-authored candidate; the escape hatch for a state no transition names")
    checkpoint_parser.add_argument("destination", type=Path)
    checkpoint_parser.add_argument("candidate", type=Path)

    start_parser = commands.add_parser("start", help="classify the input mechanically and open the first checkpoint")
    start_parser.add_argument("destination", type=Path, nargs="?",
                              help="state.json path; omit and pass --run-root with --slug to have one named for you")
    start_parser.add_argument("--run-root", type=Path, default=None, help="mint <run-root>/<YYMMDD-HHMMSS>-<slug>/state.json instead of naming it")
    start_parser.add_argument("--slug", default=None, help="run slug, used with --run-root")
    start_parser.add_argument("--input", required=True, dest="input_text", help="a path to requirements or a plan, or free idea text")
    start_parser.add_argument("--worktree", type=Path, default=None, help="any path inside the canonical worktree; defaults to cwd")
    start_parser.add_argument("--next", dest="next_action", default=None)

    enter_parser = commands.add_parser("enter", help="mark a stage entered; idempotent, keeps a resume-kept association")
    enter_parser.add_argument("state", type=Path)
    enter_parser.add_argument("stage", choices=("interview", "ralplan", "execute"))

    attach_parser = commands.add_parser("attach", help="pin a stage's run explicitly, past the snapshot-diff heuristic")
    attach_parser.add_argument("state", type=Path)
    attach_parser.add_argument("stage", choices=("interview", "ralplan", "execute"))
    attach_parser.add_argument("path", type=Path)

    gap_parser = commands.add_parser("gap", help="print {gap, completed, next, action}")
    gap_parser.add_argument("state", type=Path)

    status_parser = commands.add_parser("status", help="lifecycle, per-stage association, and gap, all live-resolved")
    status_parser.add_argument("state", type=Path)

    assume_parser = commands.add_parser("assume", help="record a reversible decision taken on its recommended option")
    assume_parser.add_argument("state", type=Path)
    assume_parser.add_argument("--stage", required=True)
    assume_parser.add_argument("--decision", required=True)
    assume_parser.add_argument("--chosen", required=True)
    assume_parser.add_argument("--alternatives", default="", help="comma-separated")
    assume_parser.add_argument("--reversal-cost", required=True, dest="reversal_cost")
    assume_parser.add_argument("--where", required=True)
    assume_parser.add_argument("--next", dest="next_action", default=None)

    question_parser = commands.add_parser("question", help="record an irreversible decision that parks the tasks or stories depending on it")
    question_parser.add_argument("state", type=Path)
    question_parser.add_argument("--stage", required=True)
    question_parser.add_argument("--question", required=True, dest="question_text")
    question_parser.add_argument("--options", default="", help="comma-separated")
    question_parser.add_argument("--recommended", required=True)
    question_parser.add_argument("--why-irreversible", required=True, dest="why_irreversible")
    question_parser.add_argument("--parks", required=True, help="task or story ids this question parks, or 'whole run'")
    question_parser.add_argument("--next", dest="next_action", default=None)

    answer_parser = commands.add_parser("answer", help="fill a question's answer once, from unanswered to answered")
    answer_parser.add_argument("state", type=Path)
    answer_parser.add_argument("question_id")
    answer_parser.add_argument("--text", required=True)
    answer_parser.add_argument("--next", dest="next_action", default=None)

    lesson_parser = commands.add_parser("lesson", help="propose an AGENTS.md line, never applying it")
    lesson_parser.add_argument("state", type=Path)
    lesson_parser.add_argument("--line", required=True)
    lesson_parser.add_argument("--why", required=True)
    lesson_parser.add_argument("--next", dest="next_action", default=None)

    guard_parser = commands.add_parser("guard", help="list every execute task whose scope meets AGENTS.md; exits nonzero if any do")
    guard_parser.add_argument("state", type=Path)

    closeout_parser = commands.add_parser("closeout", help="enter the closeout stage")
    closeout_parser.add_argument("state", type=Path)

    close_parser = commands.add_parser("close", help="paused when a question is unanswered; else completed when execute is a completed receipt; else refuses")
    close_parser.add_argument("state", type=Path)
    close_parser.add_argument("--retro", required=True, type=Path, dest="retro_path")
    close_parser.add_argument("--next", dest="next_action", default=None)

    halt_parser = commands.add_parser("halt", help="the end state for a run close refused; refused when close would succeed")
    halt_parser.add_argument("state", type=Path)
    halt_parser.add_argument("--reason", required=True)
    halt_parser.add_argument("--next", dest="next_action", default=None)

    report_parser = commands.add_parser("report", help="the final report, in every lifecycle")
    report_parser.add_argument("state", type=Path)

    resume_parser = commands.add_parser("resume", help="paused -> active; refuses while a question is unanswered")
    resume_parser.add_argument("state", type=Path)
    resume_parser.add_argument("--next", dest="next_action", default=None)

    abort_parser = commands.add_parser("abort", help="set the terminal aborted lifecycle")
    abort_parser.add_argument("state", type=Path)
    abort_parser.add_argument("--reason", required=True)
    abort_parser.add_argument("--next", dest="next_action", default=None)

    args = parser.parse_args()
    try:
        if args.command == "validate":
            errors = validate_state(_load(args.state))
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            return 0
        if args.command == "checkpoint":
            checkpoint(args.destination, args.candidate)
            print(args.destination)
            return 0
        if args.command == "start":
            destination = _resolve_start_destination(args)
            worktree = args.worktree or Path.cwd()
            start(destination, args.input_text, worktree, args.next_action)
            print(destination)
            return 0
        if args.command == "enter":
            enter(args.state, args.stage)
            print(args.state)
            return 0
        if args.command == "attach":
            attach(args.state, args.stage, args.path)
            print(args.state)
            return 0
        if args.command == "gap":
            print(json.dumps(gap(_load(args.state)), indent=2, sort_keys=True))
            return 0
        if args.command == "status":
            print(json.dumps(status(_load(args.state)), indent=2, sort_keys=True))
            return 0
        if args.command == "assume":
            new_id = assume(args.state, args.stage, args.decision, args.chosen, _split_csv(args.alternatives),
                            args.reversal_cost, args.where, args.next_action)
            print(new_id)
            return 0
        if args.command == "question":
            new_id = question(args.state, args.stage, args.question_text, _split_csv(args.options),
                              args.recommended, args.why_irreversible, args.parks, args.next_action)
            print(new_id)
            return 0
        if args.command == "answer":
            answer(args.state, args.question_id, args.text, args.next_action)
            print(args.state)
            return 0
        if args.command == "lesson":
            new_id = lesson(args.state, args.line, args.why, args.next_action)
            print(new_id)
            return 0
        if args.command == "guard":
            result = guard_check(_load(args.state))
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0 if result["clean"] else 1
        if args.command == "closeout":
            closeout(args.state)
            print(args.state)
            return 0
        if args.command == "close":
            close(args.state, args.retro_path, args.next_action)
            print(args.state)
            return 0
        if args.command == "halt":
            halt(args.state, args.reason, args.next_action)
            print(args.state)
            return 0
        if args.command == "report":
            print(report(_load(args.state)), end="")
            return 0
        if args.command == "resume":
            resume(args.state, args.next_action)
            print(args.state)
            return 0
        if args.command == "abort":
            abort(args.state, args.reason, args.next_action)
            print(args.state)
            return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
