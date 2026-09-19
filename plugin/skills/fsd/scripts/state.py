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
import shlex
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple


SCHEMA_VERSION = 1
LIFECYCLES = frozenset({"active", "paused", "completed", "halted", "aborted"})
NONTERMINAL_LIFECYCLES = frozenset({"active", "paused"})
TERMINAL_LIFECYCLES = frozenset({"completed", "halted", "aborted"})
STAGES = ("interview", "ralplan", "execute", "closeout")
STAGE_STATUSES = frozenset({"skipped", "pending", "entered"})
STAGE_FIELDS = frozenset({"status", "run"})
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


# fsd leans on the three workflows it chains rather than re-deriving their shapes: `guard`'s scope-collision reading, `execute`'s per-worktree claim reading (used only to word the entry-stage gap message when an occupant is in the way, never to establish an association), and the plan/requirements Status parsing all come from the sibling scripts by import, read-only, so nothing here can drift from what `execute` and `ralplan` actually enforce.
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
        run = entry.get("run")
        if run is not None and (not isinstance(run, str) or not run):
            errors.append(f"stage {stage} run must be null or a non-empty path")
        if stage == "closeout" and run is not None:
            errors.append("closeout has no stage run root, so its run stays empty")
        if entry.get("status") == "skipped" and run is not None:
            errors.append(f"a skipped stage {stage} cannot carry a run")
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
# Stage association: recorded when a stage's run is created, not inferred afterward.
#
# Earlier drafts of this file tried to decide which pre-existing run belongs to a stage after the fact -- a snapshot diff against the stage's run root, execute's own per-worktree claim read as a resume signal, a repository scan for `ralplan`/`interview`, a restart marker file for the window `guard`'s own recovery opens, and, in `attach` alone, a looser worktree-sharing fallback for a run the automatic path could not verify and a willingness to match a candidate that had already compacted to a terminal shape. Review kept finding another hole in each exception: a strict-only reading over a terminal receipt lost the flow's own completed `ralplan` in one pass and admitted a stranger in the next, and the loose fallback traded a confirmed mismatch for an unconfirmed guess by worktree alone.
# This round removes every exception rather than patching another one in. `stages.<stage>.run` -- the "kept link" -- is written only by `attach` (explicit, from the lead) or by the `post-bash` hook (automatic, from the very `ocs state ralplan start` / `ocs state execute start` / `ocs validate interview ledger` command that creates or first validates the run, read in `hook.py`), and only once that candidate has already passed the stage's own strict belonging test (`_candidate_belongs`) while it was still live -- nonterminal -- to check. Both callers apply the identical test; `attach` has no fallback left to reach for when the strict test refuses. Once written, a kept link is trusted outright and never re-verified or overridden -- not by a later read of the run's own current shape, not by whichever run currently holds execute's own worktree claim -- so every reader (`enter`, `gap`, `guard`, `close`, `status`, `resume`) sees the same association regardless of what has happened to the run's own file since, including its own compaction to a terminal receipt. A stage that never had a strictly-verified live candidate pinned to it simply has no association: `gap` and `guard` then treat it exactly as an unresolved stage, allowing by default, the same policy they already apply to any other missing evidence.


def _same_plan_reference(candidate_reference: Any, candidate_root: Any, expected_reference: Any, flow_worktree_root: Path) -> bool:
    """Whether two references name the same file, each resolved against its *own* root rather than both against the flow's, and whether the candidate's own root is genuinely this flow's canonical worktree rather than merely a path that happens to resolve to an equal-looking one. `candidate_root` is compared to `flow_worktree_root` by canonicalizing both through `_execute.canonical_worktree` -- the same git-toplevel resolution `execute start` already applies to its own `worktree.root` -- rather than a plain `Path.resolve()`: `ralplan start` stores `--repository`, or `Path.cwd()` when it is omitted, exactly as given, so a run started from a subdirectory of the repository carries that subdirectory as its own root, and only canonicalizing both sides lets it still match the flow's own (already-canonical) worktree.
    `candidate_root` must be present and must canonicalize to the same worktree as `flow_worktree_root`, or the candidate is refused outright -- there is no reading left in which a missing or non-canonicalizing root is treated as unconfirmed-but-acceptable evidence; a run that genuinely lives in a different repository, or whose own root cannot be read as a worktree at all, is refused even where a coincidental absolute-path collision of the reference alone might otherwise suggest a match.
    Once the root has cleared, each reference is resolved against its own root -- the candidate's own canonical root for `candidate_reference`, `flow_worktree_root` for `expected_reference` -- with a plain `Path.resolve()`, which handles `..`-bearing paths and an absolute spelling `os.path.realpath` has not touched (macOS's own `/var` -> `/private/var`, the same gap `_normalize_scope_entry` accounts for in `guard`) without requiring the file to exist. `resolve()` can raise for reasons that have nothing to do with a genuine mismatch -- a symlink loop raises `RuntimeError` on some Python versions, `OSError` on others -- so the catch here is broad by design: every caller reads its answer as ordinary evidence rather than expecting it to raise. Neither `candidate_reference` nor `expected_reference` may be `None`: two absent references are not treated as a match, since there would be nothing there to compare."""
    if not isinstance(candidate_reference, str) or not isinstance(expected_reference, str):
        return False
    if not isinstance(candidate_root, str) or not candidate_root or candidate_root == "none":
        return False
    try:
        resolved_candidate_root, _ = _execute.canonical_worktree(Path(candidate_root))
    except Exception:
        return False
    if resolved_candidate_root != flow_worktree_root.resolve():
        return False
    def _resolved(value: str, root: Path) -> Path:
        path = Path(value)
        if not path.is_absolute():
            path = root / path
        try:
            return path.resolve()
        except Exception:
            return path
    return _resolved(candidate_reference, resolved_candidate_root) == _resolved(expected_reference, flow_worktree_root)


def _expected_execute_plan_reference(state: Dict[str, Any]) -> Optional[str]:
    """The plan path this flow is driving `execute` against, established without reading any candidate execute run's own file at all: the fsd input's own `reference` when `execute` is the entry stage -- the only classification that reaches `execute` directly, and one that always carries a plan reference (`classify_input`'s plan branch) -- or, when `ralplan` led here instead, the plan path recorded on `ralplan`'s own completed receipt (`plan.path`, the same field `gap` reads for its ralplan-completed row), read through `_resolve_association` like every other reader of ralplan's own stage. `None` when neither can be read: too little evidence to call any candidate a match, so it reads as a mismatch rather than a guess in either direction."""
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


def _expected_ralplan_reference(state: Dict[str, Any]) -> Optional[str]:
    """The reference this flow's own `ralplan` stage has to match, established the same way `_expected_execute_plan_reference` establishes execute's: the fsd input's own `reference` when `ralplan` is the entry stage -- carrying either a requirements path or a not-yet-approved plan path, `classify_input`'s two ways to reach `ralplan` directly -- or, when `interview` led here instead, the requirements path on interview's own completed ledger (`requirements_path`), read through `_resolve_association` like every other reader of interview's own stage. `None` when neither can be read."""
    if state["entry"] == "ralplan":
        return state["input"].get("reference")
    if state["entry"] != "interview":
        return None
    run_path = _resolve_association(state, "interview")
    if run_path is None:
        return None
    try:
        payload = _parse_ledger(run_path.read_text())
    except (OSError, UnicodeError):
        return None
    if payload.get("status") != "completed":
        return None
    return payload.get("requirements_path") or None


def _expected_ralplan_field(state: Dict[str, Any]) -> str:
    """Which of a candidate ralplan run's own fields `_expected_ralplan_reference` has to be checked against: `plan.path` when this flow's own reference names a plan document -- `ralplan` is the entry stage and the fsd input's own `kind` is `plan`, `classify_input`'s other way to reach `ralplan` directly, over an unapproved plan rather than a requirements document -- and `input.reference` for every other case, since interview only ever hands `ralplan` a requirements path and `classify_input`'s other `ralplan` branch is a requirements document too. Comparing `plan.path` against a requirements path (or the reverse) would never match by construction -- they name two different documents entirely -- so which field is checked has to follow what kind of document `expected` actually names, not both fields against the one value."""
    if state["entry"] == "ralplan" and state["input"].get("kind") == "plan":
        return "plan"
    return "input"


def _ralplan_candidate_reference(state: Dict[str, Any], payload: Dict[str, Any]) -> Any:
    field = _expected_ralplan_field(state)
    if field == "plan":
        return payload.get("plan", {}).get("path")
    return payload.get("input", {}).get("reference")


def _execute_candidate_reference(payload: Dict[str, Any]) -> Any:
    """`input.reference` from a candidate's own nonterminal shape, the only shape `_execute_candidate_belongs` ever reads this from -- present, though possibly `null` for a `--kind brief` run's own copy. `None` either way, since neither an absent nor a `null` reference ever compares equal to a real one."""
    input_field = payload.get("input")
    return input_field.get("reference") if isinstance(input_field, dict) else None


def _execute_candidate_root(payload: Dict[str, Any]) -> Optional[str]:
    """The candidate's own idea of where it lives, read from `worktree.root` -- present on every nonterminal execute run, the only shape `_execute_candidate_belongs` ever reads this from."""
    worktree = payload.get("worktree")
    if isinstance(worktree, dict) and isinstance(worktree.get("root"), str):
        return worktree["root"]
    root = payload.get("worktree_root")
    return root if isinstance(root, str) else None


def _execute_candidate_belongs(state: Dict[str, Any], run_path: Path) -> bool:
    """Strict, and the only belonging test ever applied to an `execute` candidate: it must be live -- nonterminal -- with its own `input.reference` known and matching this flow's own expected reference by resolved path, each side resolved against its own canonical root (`_same_plan_reference`). A terminal receipt, completed or aborted, never belongs here, however faithfully its own surviving fields might still match: `post-bash` links a run at creation, while it is still live, so there is nothing left for a terminal reading to rescue. A `None` reference -- a `--kind brief` run, which this flow, always executing a plan, never starts as its own -- is likewise a non-match, not merely unconfirmed evidence: refusing it is what keeps an operator's own unrelated execute run from ever being read as this flow's own."""
    expected = _expected_execute_plan_reference(state)
    if expected is None:
        return False
    try:
        payload = _load(run_path)
    except Exception:
        return False
    if payload.get("lifecycle") not in _execute.NONTERMINAL_LIFECYCLES:
        return False
    return _same_plan_reference(_execute_candidate_reference(payload), _execute_candidate_root(payload), expected, Path(state["worktree"]))


def _ralplan_candidate_root(payload: Dict[str, Any]) -> Optional[str]:
    """`repository`, present on every nonterminal ralplan run -- the only shape `_ralplan_candidate_belongs` ever reads this from."""
    repository = payload.get("repository")
    return repository if isinstance(repository, str) else None


def _ralplan_candidate_belongs(state: Dict[str, Any], run_path: Path) -> bool:
    """Strict, over whichever of a candidate's own fields `_expected_ralplan_field` names, and live -- nonterminal -- only, the same reasoning `_execute_candidate_belongs` applies. `ralplan`'s own completed and aborted receipts never belong here, whatever they still carry: `post-bash` links a ralplan run at creation, while it is still live, so there is nothing left for a terminal reading to rescue."""
    expected = _expected_ralplan_reference(state)
    if expected is None:
        return False
    try:
        payload = _load(run_path)
    except Exception:
        return False
    if payload.get("lifecycle") not in _ralplan.NONTERMINAL_LIFECYCLES:
        return False
    return _same_plan_reference(_ralplan_candidate_reference(state, payload), _ralplan_candidate_root(payload), expected, Path(state["worktree"]))


def _interview_candidate_belongs(state: Dict[str, Any], run_path: Path) -> bool:
    """Interview carries fsd no reference of its own to check a candidate against -- an idea input, the only one that ever leads here, has a `null` `input.reference` -- so there is no expected value to match, only whether this ledger is genuinely this flow's own: `active` (live; a `completed` ledger is terminal and never belongs here, whatever `requirements_path` it still carries -- the same live-only rule execute's and ralplan's own candidates follow), its own `repository` canonicalizing to this flow's canonical worktree (`_execute.canonical_worktree`, the same root check `_same_plan_reference` applies elsewhere, since a hand-authored `repository` line is not guaranteed to already be canonical), and its own `output_path` resolving to a path inside that same worktree. The expected reference for an interview is simply "none yet", so the first ledger to clear all three checks is accepted -- there is nothing further to rank candidates by."""
    try:
        ledger = _parse_ledger(run_path.read_text())
    except (OSError, UnicodeError):
        return False
    if ledger.get("status") != "active":
        return False
    repository = ledger.get("repository")
    if not isinstance(repository, str) or not repository or repository == "none":
        return False
    try:
        candidate_root, _ = _execute.canonical_worktree(Path(repository))
    except Exception:
        return False
    flow_root = Path(state["worktree"]).resolve()
    if candidate_root != flow_root:
        return False
    output_path = ledger.get("output_path")
    if not isinstance(output_path, str) or not output_path:
        return False
    candidate_output = Path(output_path)
    if not candidate_output.is_absolute():
        candidate_output = candidate_root / candidate_output
    try:
        resolved_output = candidate_output.resolve()
    except Exception:
        return False
    try:
        resolved_output.relative_to(flow_root)
    except ValueError:
        return False
    return True


def _candidate_belongs(state: Dict[str, Any], stage: str, run_path: Path) -> bool:
    """The strict belonging test: what `post-bash` checks before ever attaching a run it watched a Bash command create, and the only test `attach` applies -- there is no looser fallback left to reach for. A candidate that fails it is not this flow's, full stop, regardless of who is asking or what else is true about it."""
    if stage == "execute":
        return _execute_candidate_belongs(state, run_path)
    if stage == "ralplan":
        return _ralplan_candidate_belongs(state, run_path)
    return _interview_candidate_belongs(state, run_path)


def _execute_occupant(worktree_root: Path) -> Optional[Path]:
    """Whichever nonterminal execute run currently holds this worktree's own per-worktree claim, regardless of which flow started it or whether it belongs to this one. Used only to word the entry-stage gap message when an occupant is in the way of `/kein:execute` (`_execute_occupant_block`, below) -- never to establish or override an association; `_flow_stage_run` reads only the kept link. A read failure reads as no occupant, the same as everywhere else here that treats an unreadable file as no evidence rather than raising."""
    runs_dir = worktree_root / ".agents" / "kein" / "runs"
    try:
        return _execute.find_occupying_run(runs_dir, worktree_root)
    except Exception:
        return None


def _flow_stage_run(state: Dict[str, Any], stage: str) -> Tuple[Optional[Path], str]:
    """The one resolver every reader of a stage's run goes through -- `enter`, `gap`, `guard`, `close`, `status`, and `resume` -- and it reads exactly one thing: the kept link `stages.<stage>.run` names, written only by `attach` or by the `post-bash` hook, each only once a candidate has already passed the stage's own strict belonging test while it was still live (see the section comment above). Nothing here re-derives or re-verifies that association from the run's own current content, and nothing here ever substitutes a different, currently-live run in its place -- not a snapshot of the stage's run root, not whichever run currently holds `execute`'s own worktree claim. A kept link is trusted outright for exactly the same reason a completed receipt with no `input` field left to check is still trusted once pinned: the belonging test that mattered already ran, while the evidence for it still existed.
    Returns `(None, "not entered")` before the stage has any run at all to speak of, `(None, "not applicable")` for `closeout`, `(None, "none")` once the stage is entered but has no kept link yet, or `(path, "kept")` naming the kept link."""
    if stage == "closeout":
        return None, "not applicable"
    stage_state = state["stages"][stage]
    kept = stage_state.get("run")
    if kept:
        return Path(kept), "kept"
    if stage_state.get("status") == "entered":
        return None, "none"
    return None, "not entered"


def _resolve_association(state: Dict[str, Any], stage: str) -> Optional[Path]:
    path, _ = _flow_stage_run(state, stage)
    return path


def _occupant_is_kept_link(state: Dict[str, Any], occupant: Path) -> bool:
    """Whether `occupant` -- whichever nonterminal execute run currently holds the worktree's own per-worktree claim -- is the very run `stages.execute.run` already keeps. A resumed run's own kept association is trusted outright wherever this is asked, the same as everywhere else a kept link is read, without ever re-running the strict belonging test on it: a paused-then-resumed run's own still-live occupant must never read as a stranger merely because that test happens to be momentarily unable to confirm it (a transient read failure, or evidence the run's own file no longer carries)."""
    kept = state["stages"]["execute"].get("run")
    if not kept:
        return False
    try:
        return Path(kept).resolve() == occupant.resolve()
    except Exception:
        return False


def enter(destination: Path, stage: str) -> bool:
    """Marks `stage` entered. Idempotent once entered -- a second call changes nothing.
    `enter` no longer discovers or adopts a pre-existing run of its own: under the recorded-at-creation design, a stage's association is written only by `attach` (explicit, from the lead) or by the `post-bash` hook (automatic, watching the very `ocs state ralplan start` / `ocs state execute start` / `ocs validate interview ledger` command that creates or first validates the run), never inferred afterward from what the stage's run root or the worktree's own claim happen to hold at the moment of entry. Any existing association -- kept by a prior `resume`, or by an `attach`/`post-bash` call that landed before this call -- is left exactly as it is; there is nothing here to adopt, snapshot, or associate.
    `execute` alone still checks one thing before marking itself entered: whether a nonterminal execute run already occupies the worktree and does not belong to this flow. An occupant equal to the kept link belongs without re-running the strict test at all -- a resumed run's own kept association is trusted outright here exactly as everywhere else a kept link is read, which is what keeps a paused-then-resumed run's own still-live occupant from ever being read as a stranger merely because the strict test happens to be momentarily unable to confirm it. Failing that shortcut, the strict test (`_execute_candidate_belongs`) still runs. This is not an association check -- `run` is never touched here, whichever way it comes out -- it exists only so a non-belonging occupant keeps `stages.execute.status` at `pending`, which is what keeps `gap`'s own occupant-aware message (`_execute_occupant_block`) reachable at all: that message only ever fires from the entry-stage row, which requires `pending`. Marking `execute` entered over a non-belonging occupant would silently retire that row -- and the binding single-invocation-clears-it requirement with it -- the moment `post-skill` calls `enter` for a model-invoked `kein:execute`, regardless of whether the occupant ever gets cleared. An occupant that already belongs, or no occupant at all, does not block entry; `ralplan` and `interview` carry no worktree claim of their own and so have nothing to check here.
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
    if stage == "execute":
        occupant = _execute_occupant(Path(state["worktree"]))
        if occupant is not None:
            if not _occupant_is_kept_link(state, occupant) and not _execute_candidate_belongs(state, occupant):
                raise ValueError(
                    f"a nonterminal execute run already occupies the worktree at {occupant} and does not "
                    "execute this flow's own plan; finish or abort it before entering execute"
                )
    candidate = copy.deepcopy(state)
    candidate["stages"][stage]["status"] = "entered"
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


def _kept_link_still_live(stage: str, kept_path: Path) -> bool:
    """Whether the run currently sitting behind a stage's own kept link is still live -- nonterminal -- which is what `attach` treats as the one thing worth protecting a kept link against being swapped out from under: a candidate genuinely competing with one this flow is still actively relying on. Read fresh, not from any cached belonging result, since this asks a different question than `_candidate_belongs` does -- not "does this run belong to this flow," which a kept link answers once and for all at the moment it is written, but "is the run this flow already trusts still going," which can only be answered by reading it again. `False` -- meaning nothing left here to protect -- once that run has compacted to a terminal shape (`ralplan`'s and `execute`'s own `lifecycle`, `interview`'s own ledger `status`) or cannot be read at all, the same "absence of evidence is not evidence of a problem" reading every other unreadable-file case here takes; this is what reopens the guard-recovery window (`_guard_action`) to a genuine replacement once the violating run has been aborted, and what lets an unreadable kept association (`GUARD_NO_ASSOCIATION`'s own case) be repaired with a plain `attach` rather than staying stuck forever pointing at a file nothing can read any more."""
    try:
        if stage == "interview":
            return _parse_ledger(kept_path.read_text()).get("status") == "active"
        payload = _load(kept_path)
        nonterminal = _execute.NONTERMINAL_LIFECYCLES if stage == "execute" else _ralplan.NONTERMINAL_LIFECYCLES
        return payload.get("lifecycle") in nonterminal
    except Exception:
        return False


def attach(destination: Path, stage: str, run_path: Path) -> None:
    """Pins a stage's association explicitly. This is the only writer of a kept link besides the `post-bash` hook, which calls this same function once it has already run the identical strict check on its own (see `hook.py`); the lead uses it directly whenever no bash command the hook watches produced the run.
    Applies the same strict belonging test `post-bash` applies, and no other (`_candidate_belongs`): the candidate must be live -- nonterminal -- its own identifying field known, and it must match this flow's own expected reference by resolved path, each side resolved against its own canonical worktree. A candidate that fails it is refused outright, by name -- there is no looser fallback left to reach for; a run this cannot verify, whether because it has already gone terminal or because it is genuinely not this flow's own, has nothing left here to rescue it.
    A kept link is never replaced while its own referent is still live: once `stages.<stage>.run` is set, a call naming a different path is refused as long as the run currently sitting there is still nonterminal (`_kept_link_still_live`) -- protecting a kept link the flow is still actively relying on from being silently swapped out, which is exactly what a same-repository second interview ledger, still active, would otherwise do. A call naming the exact same path -- resolved, so an equivalent relative and absolute spelling both count -- is always a no-op that writes nothing, live or not. Once the currently kept run has itself gone terminal (or can no longer be read at all), a call naming a different, live, correctly-belonging path is accepted, moving the kept link there instead: this is what lets `guard`'s own abort-then-restart recovery -- which necessarily starts its replacement at a new path, since `execute start` refuses to reuse an existing one -- reach the replacement at all, and what lets an unreadable kept association (`GUARD_NO_ASSOCIATION`) be repaired with a plain `attach` rather than staying stuck forever."""
    if stage not in ("interview", "ralplan", "execute"):
        raise ValueError("attach names interview, ralplan, or execute")
    state = _load(destination)
    if state.get("lifecycle") in TERMINAL_LIFECYCLES:
        raise ValueError("Terminal state cannot transition")
    if not run_path.is_file():
        raise ValueError(f"{run_path} does not exist")
    if not _candidate_belongs(state, stage, run_path):
        raise ValueError(
            f"{run_path} does not belong to this flow's {stage} stage: it must be a live run of this flow "
            "whose own reference matches this flow's by resolved path, in this flow's own canonical worktree"
        )
    stage_state = state["stages"][stage]
    if stage_state["status"] == "skipped":
        raise ValueError(f"{stage} is skipped for this run")
    kept = stage_state.get("run")
    if kept:
        try:
            same_path = Path(kept).resolve() == run_path.resolve()
        except Exception:
            same_path = kept == str(run_path)
        if same_path:
            return
        if _kept_link_still_live(stage, Path(kept)):
            raise ValueError(f"{stage} already has a kept link at {kept}, still live; a kept link is never replaced while it is still live")
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


def _execute_occupant_abort_command(occupant: Path) -> str:
    """The single Bash command `_execute_occupant_block` prints for aborting an occupant: one `python3 -c` call that reads the occupant's own state (always still live here -- `_execute_occupant` only ever returns a nonterminal run -- so its own `worktree.root` is always present), builds its aborted candidate, writes it under the occupant's own run directory (itself under `.agents/kein/runs/`, the one prefix every workflow's own fingerprint excludes, so writing it there registers as no drift), and checkpoints it -- all inside the one Bash tool call, so nothing here ever calls the Write tool at all. That is what lets this run as printed while `pre-write` is still denying Write/Edit/MultiEdit/NotebookEdit over this very gap: the candidate file that `ocs state execute checkpoint` needs cannot be produced by a tool `pre-write` would deny, so this produces it from inside the one tool call `pre-write` never gates.
    The inline script is passed as one `shlex.quote`d argument rather than wrapped in bare double quotes, and `occupant`/`candidate_path` are each `shlex.quote`d again in the trailing `checkpoint` call, so the whole line still runs as printed when a repository path holds a space or another shell-special character; the script's own two path literals are built with Python's `!r`, which is a separate, always-valid escaping for the Python source itself, not a substitute for the outer shell quoting."""
    candidate_path = occupant.parent / "fsd-occupant-abort-candidate.json"
    script = (
        "import json, pathlib, datetime; "
        f"p = pathlib.Path({str(occupant)!r}); "
        "s = json.loads(p.read_text()); "
        "c = {'schema_version': 1, 'revision': 'auto', 'workflow': 'execute', 'run_id': s['run_id'], "
        "'lifecycle': 'aborted', 'aborted_at': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), "
        "'worktree_root': s['worktree']['root'], 'reason': 'occupies the worktree without executing this flow'}; "
        f"pathlib.Path({str(candidate_path)!r}).write_text(json.dumps(c))"
    )
    return (
        f"python3 -c {shlex.quote(script)} && ocs state execute checkpoint "
        f"{shlex.quote(str(occupant))} {shlex.quote(str(candidate_path))}"
    )


def _execute_occupant_block(state: Dict[str, Any]) -> Optional[str]:
    """The reason a `gap` row that would otherwise say `invoke /kein:execute ...` must say instead, when a nonterminal execute run already occupies the worktree and does not execute this flow's own plan: invoking `/kein:execute` again would only be refused a second time by execute's own per-worktree claim, and a binding requirement (`.agents/kein/requirements/260918-unattended-flow.md` Constraints: "A block's reason names an action whose single invocation clears the condition") rules out naming an action whose one invocation cannot clear what is actually blocking. This is worded as a decision about someone else's run, not this flow's own: the occupant is not this flow's, and finishing it or aborting it -- outside this flow's own judgment either way -- are the two options; aborting is the one this names an actual command for, since it is the one that clears this row (it releases the claim `/kein:execute` needs, after which the ordinary row resolves again on its own), and that command is the single chained Bash call `_execute_occupant_abort_command` builds, runnable as printed even while `pre-write` is denying every Write-tool call over this same row (see that function's own docstring for why a separate Write step would deadlock here). `None` when no occupant is in the way, or the occupant already belongs to this flow -- an occupant equal to the kept link belongs without re-running the strict test at all, the identical shortcut `enter` takes (`_occupant_is_kept_link`), which is what keeps a resumed, pending, still-live kept run from reading as a stranger to abort merely because the strict test happens to be momentarily unable to confirm it -- the ordinary case, where naming `/kein:execute` is exactly the action that clears the row. Only `execute` ever needs this: neither `ralplan` nor `interview` refuses to start on an occupied worktree, so their own pending-entry rows never open the gap this closes. This is the one place `_execute_occupant` is read for anything other than association -- purely to word this message, never to attach or substitute a run."""
    occupant = _execute_occupant(Path(state["worktree"]))
    if occupant is None or _occupant_is_kept_link(state, occupant) or _execute_candidate_belongs(state, occupant):
        return None
    try:
        lifecycle = _load(occupant).get("lifecycle", "?")
    except Exception:
        lifecycle = "?"
    return (
        f"a nonterminal execute run already occupies the worktree at {occupant} ({lifecycle}); it is not this "
        "flow's own run, so invoking /kein:execute would only be refused again by execute's own per-worktree "
        "claim, and finishing it or aborting it are decisions for whoever owns that occupant, not for this "
        "flow. To abort it, run this single Bash command, which builds the aborted candidate and checkpoints "
        f"it in one call: {_execute_occupant_abort_command(occupant)}"
    )


def gap(state: Dict[str, Any]) -> Dict[str, Any]:
    """`{gap, completed, next, action}`. Rows are evaluated in the table's own order and the first satisfied row wins.
    A nonterminal fsd lifecycle is checked before any stage row, so a paused, completed, halted, or aborted run always reports no gap regardless of what the underlying stage evidence would otherwise read.
    Every row past the first reads a file this script did not just write -- an associated run's state or ledger, or the requirements document it names -- so each row's read is wrapped, and any failure (missing, unreadable, malformed) is treated the same as "an unfinished or unreadable stage gives no row": that row does not fire, and evaluation continues to the next one, rather than the whole check raising.
    Neither row that would otherwise say `invoke /kein:execute ...` -- the entry-stage row and the ralplan-completed row -- fires that action while a nonterminal execute run already occupies the worktree without belonging to this flow: invoking `/kein:execute` again would only be refused by execute's own per-worktree claim, which a single invocation of that action could never clear, so `_execute_occupant_block` names the occupant and the command that does clear it instead (`.agents/kein/requirements/260918-unattended-flow.md` Constraints).
    The execute-derived closeout row fires only for a `completed` execute lifecycle, never for `aborted`. This is a deliberate narrowing, not an oversight: once `guard`'s own recovery can abort a violating execute run and start its replacement (see `_guard_action`), an aborted receipt with nothing live yet to replace it is inherently ambiguous between "a restart is about to start" and "the lead has given up on execute altogether" -- both leave the exact same tasks-less aborted receipt behind, with nothing left in fsd's own recorded-at-creation state to tell them apart without reintroducing some form of inference. Rather than guess, `gap` simply does not treat an aborted execute, by itself, as evidence of a stage-to-stage gap; this is also what keeps the guard-recovery window (between the abort and the replacement's `start`) from ever producing a false closeout push, since the very same reading covers both cases uniformly. A genuine give-up still reaches a terminal outcome through the ordinary path: the lead (or fsd's own orchestrating skill, watching for it) invokes `ocs state fsd closeout <state>` on its own judgment once it decides execute will not be restarted; `close` then refuses correctly -- `_execute_side_done` requires a `completed` lifecycle, never `aborted` -- naming execute as aborted, not completed, and the lead calls `halt`."""
    if state["lifecycle"] != "active":
        return {"gap": False, "completed": None, "next": None, "action": "no gap"}
    stages = state["stages"]
    entry = state["entry"]
    if stages[entry]["status"] == "pending":
        if entry == "execute":
            blocked = _execute_occupant_block(state)
            if blocked is not None:
                return {"gap": True, "completed": None, "next": entry, "action": blocked}
        target = state["input"].get("reference") or state["input"].get("summary")
        return {"gap": True, "completed": None, "next": entry, "action": f"invoke /kein:{entry} {shlex.quote(target)}"}
    if stages["ralplan"]["status"] == "pending":
        try:
            run_path = _resolve_association(state, "interview")
            if run_path is not None:
                payload = _parse_ledger(run_path.read_text())
                if payload.get("status") == "completed":
                    requirements_path = payload.get("requirements_path")
                    if requirements_path and _requirements_status(Path(requirements_path)) == "Approved":
                        return {"gap": True, "completed": "interview", "next": "ralplan",
                                "action": f"invoke /kein:ralplan {shlex.quote(requirements_path)}"}
        except Exception:
            pass
    if stages["execute"]["status"] == "pending":
        try:
            run_path = _resolve_association(state, "ralplan")
            if run_path is not None:
                payload = _load(run_path)
                if payload.get("lifecycle") == "completed":
                    plan_path = payload.get("plan", {}).get("path")
                    blocked = _execute_occupant_block(state)
                    if blocked is not None:
                        return {"gap": True, "completed": "ralplan", "next": "execute", "action": blocked}
                    return {"gap": True, "completed": "ralplan", "next": "execute",
                            "action": f"invoke /kein:execute {shlex.quote(plan_path)}"}
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
            if execute_run is not None:
                payload = _load(execute_run)
                lifecycle = payload.get("lifecycle")
                if lifecycle == "completed":
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


def _none_association_reason(state: Dict[str, Any], stage: str) -> str:
    """What `status` reports alongside a stage whose association is `"none"` -- entered, or `pending` with no kept link at all, but with no run linked yet. This is the one thing status can actually tell a lead who has no memory of what already happened to this run (a fresh session after compaction, say): the command that links this stage automatically the moment it creates or first validates a matching run, with the specific argument this flow's own strict test actually reads -- for `ralplan`, `--plan <plan-path>` when this flow's own reference is a plan document, `--input <requirements-path>` when it is a requirements document (`_expected_ralplan_field`) -- and that `attach` pins nothing this same test would refuse: it works only on a live run of this flow, never a terminal one and never a stranger, so a run whose own reference genuinely contradicts this flow's is refused by `attach` too, exactly as it is by `post-bash`."""
    if stage == "interview":
        command = ("ocs validate interview ledger <path>, run against an active ledger whose own "
                   "repository is this flow's canonical worktree and whose output_path resolves inside it")
    elif stage == "ralplan":
        flag = "--plan <plan-path>" if _expected_ralplan_field(state) == "plan" else "--input <requirements-path>"
        command = f"ocs state ralplan start ... {flag}, matching this flow's own reference by resolved path"
    else:
        command = "ocs state execute start ... --input <plan-path>, matching this flow's own reference by resolved path"
    return (
        f"no run linked yet; {command} links it automatically. attach works only on a live run of this "
        f"flow, by the identical test: ocs state fsd attach <state> {stage} <path>"
    )


def status(state: Dict[str, Any]) -> Dict[str, Any]:
    stage_report = {}
    for stage in STAGES:
        path, detail = _flow_stage_run(state, stage)
        entry = {"status": state["stages"][stage]["status"], "run": str(path) if path else None, "association": detail}
        if detail == "none":
            entry["association_reason"] = _none_association_reason(state, stage)
        stage_report[stage] = entry
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


def _guard_action(state: Dict[str, Any], execute_run: Path) -> str:
    """The recovery `guard` names when it finds a violation in `execute_run`'s own tasks: abort this run and start its replacement, without the offending task, joined into one Bash call with `&&` so no hook ever observes the run aborted with no replacement yet -- the `post-bash` hook attaches the replacement automatically, once it strictly belongs, from that same `execute start` call's own printed stdout, so no separate `attach` step is named here at all. Chaining the two commands into a single tool call is what actually closes the abort-to-replacement window this action opens: `PostToolUse`/`PreToolUse`/`Stop` fire around whole tool calls, never in the middle of one shell line, so nothing reads fsd's own state between the abort landing and the replacement's association being attached.
    The `--input` names the actual plan this flow is executing (`_expected_execute_plan_reference`) rather than a `<plan|brief>` placeholder: this flow always executes a plan, and a `--kind brief` replacement would store a `null` `input.reference`, which `_same_plan_reference` can never call a match -- exactly the gap this design closes. When the plan cannot be read (should not happen once `guard` has already read a real ledger, but guarded against regardless), a placeholder names what the lead must supply instead of a guess. `--worktree` is likewise the run's own actual worktree rather than a placeholder: `execute start` requires it, so the printed command would fail as given without it. Both real, substituted values -- the plan reference and the worktree -- are `shlex.quote`d so the line still runs as printed when either path holds a space; the angle-bracket placeholders the lead still has to fill in (`<state.json>`, `<s>`, and the rest) are left bare, since they are not values this substitutes at all."""
    plan_reference = _expected_execute_plan_reference(state)
    plan_argument = shlex.quote(plan_reference) if plan_reference is not None else "<the plan this flow executes>"
    return (
        "an existing task's scope cannot change and tasks cannot be removed, and parking the task does "
        "not clear this: its scope is unchanged while parked, so guard keeps failing and close keeps "
        "refusing. The fix is to abort this execute run and start its replacement, without the offending "
        "task, in the same Bash tool call, joined with && so no hook ever observes the run aborted with "
        "no replacement yet: ocs state execute checkpoint <state.json> <aborted-candidate.json> && "
        "ocs state execute start --run-root <runs/execute> --slug <s> --kind plan --input "
        f"{plan_argument} --worktree {shlex.quote(state['worktree'])} --tasks <replacement-tasks-ledger.json, "
        "without the offending task>. The post-bash hook attaches the replacement automatically once it "
        "strictly belongs -- no attach step is needed. If the run cannot be restarted, close will keep "
        "refusing and the run ends halted"
    )


GUARD_NO_ASSOCIATION = (
    "execute is entered but its association at {detail} could not be read; guard cannot check a run it "
    "cannot read, so run `ocs state fsd attach <state.json> execute <path>` with a readable path before "
    "guard can check it"
)


def _guard_failure_message(guard_result: Dict[str, Any]) -> str:
    if "reason" in guard_result:
        return guard_result["reason"]
    names = ", ".join(sorted({violation["task"] for violation in guard_result["violations"]}))
    return f"guard failed: task(s) {names} scope AGENTS.md"


def guard_check(state: Dict[str, Any]) -> Dict[str, Any]:
    """Checks the kept execute link whenever one exists, whatever the stage's own status -- not only while it reads `entered`. A `pending` stage can still carry a kept link: `resume` pins one back onto a stage it resets to `pending` when a parked task's own run is still nonterminal, and that run's tasks are exactly what still needs checking across the pause. Clean whenever there is no kept link to check at all -- before the stage has any run, entered with none yet (`none`), a skipped stage (which the schema forbids from ever carrying a run), or a `pending` stage `resume` never touched.
    Once a kept link exists, a run this cannot actually read is *not* silently clean: it is a check that could not run, and says so, pointing at `attach`, rather than letting the absence of evidence read as the absence of a problem."""
    execute_run, _ = _flow_stage_run(state, "execute")
    if execute_run is None:
        return {"clean": True, "violations": []}
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
        result["action"] = _guard_action(state, execute_run)
    return result


def guard(destination: Path) -> Dict[str, Any]:
    """The CLI's own entry point for `guard`, distinct from `guard_check` (the pure read `close` and `halt` also call internally)."""
    state = _load(destination)
    return guard_check(state)


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
    """Whether `execute`'s side of the flow is done for `close`'s purposes: either its associated run is a completed receipt, or it never started at all because interview or ralplan aborted first, so the flow was never going to reach it. An `execute` run that itself aborted, or one that is simply absent while nothing upstream aborted (execute has not been reached yet), is not done."""
    execute_run = _resolve_association(state, "execute")
    if execute_run is None:
        return not _execute_stage_reachable(state)
    try:
        payload = _load(execute_run)
    except Exception:
        return False
    return payload.get("lifecycle") == "completed"


def _execute_lifecycle_or_none(state: Dict[str, Any]) -> Optional[str]:
    execute_run = _resolve_association(state, "execute")
    if execute_run is None:
        return None
    try:
        return _load(execute_run).get("lifecycle")
    except Exception:
        return None


def _execute_not_done_message(state: Dict[str, Any]) -> str:
    """`close`'s and `halt`'s refusal text naming execute's current status, read through `_resolve_association` like every other reader -- the same kept link, nothing more."""
    read_run = _resolve_association(state, "execute")
    try:
        status = (_load(read_run).get("lifecycle") if read_run is not None else None) or "not started"
    except Exception:
        status = "not started"
    return f"execute is {status}, not completed"


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
    Whether it also resets `execute` to `pending` (pinning its `run` to the same association, so `enter execute` keeps it rather than leaving it unresolved) depends on whether `execute`'s associated run is present and nonterminal at that moment -- the one case this resets.
    In every other case, `execute`'s own stage is left exactly as it was, and only `closeout` resets, so the next `gap` decides where the run goes from what it finds rather than from anything `resume` assumed. Four situations route through that one "leave it alone" branch:
    `execute`'s associated run is present and already terminal (a completed or aborted receipt), in which case `gap` reports the same execute-derived row again and the next action is `closeout`;
    upstream (`interview` or `ralplan`) aborted before `execute` was ever going to run, in which case `gap` reports the same aborted-stage row again and the next action is `closeout`;
    `ralplan` completed but `execute` was never entered (a question paused the run before the lead invoked it), in which case `gap` reports the ralplan-completed row again and the next action is to invoke `execute`;
    or `execute` was entered but never got an association at all, in which case `gap` finds no evidence either way and reports no gap until `attach` or the `post-bash` hook resolves it."""
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
    candidate["stages"]["closeout"] = {"status": "pending", "run": None}
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
    stages = {stage: {"status": "skipped" if index < entry_index else "pending", "run": None}
              for index, stage in enumerate(order)}
    stages["closeout"] = {"status": "pending", "run": None}
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

    enter_parser = commands.add_parser("enter", help="mark a stage entered; idempotent, leaves any existing association untouched")
    enter_parser.add_argument("state", type=Path)
    enter_parser.add_argument("stage", choices=("interview", "ralplan", "execute"))

    attach_parser = commands.add_parser("attach", help="pin a stage's run explicitly")
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
            result = guard(args.state)
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
