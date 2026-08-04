#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


REQUIREMENTS_HEADINGS = (
    "## Context",
    "## Desired outcome",
    "## Scope",
    "### In scope",
    "### Out of scope",
    "## Requirements",
    "## Constraints",
    "## Decision boundaries",
    "## Acceptance criteria",
    "## Decisions and rationale",
    "## Relevant system evidence",
    "## Assumptions and risks",
    "## Deferred items",
)

ACTIVE_LEDGER_HEADINGS = (
    "## Original request",
    "## Confirmed decisions",
    "## Constraints and non-goals",
    "## Decision boundaries",
    "## Repository evidence",
    "## Open questions",
    "## Explicit deferrals",
)

ACTIVE_LEDGER_KEYS = {
    "status",
    "run_id",
    "created_at",
    "updated_at",
    "working_directory",
    "repository",
    "output_path",
}

TERMINAL_LEDGER_KEYS = {
    "completed": {"status", "requirements_path", "completed_at"},
    "aborted": {"status", "aborted_at", "reason"},
}

ROUND_PATTERN = re.compile(r"\bRound\s+\d+\b", re.IGNORECASE)


def _has_forbidden_history(text: str) -> bool:
    return "## Transcript" in text or ROUND_PATTERN.search(text) is not None


def _section_body(text: str, heading: str) -> str | None:
    marker = f"{heading}\n"
    start = text.find(marker)
    if start < 0:
        return None
    body_start = start + len(marker)
    next_heading = re.search(r"^#{1,3} ", text[body_start:], re.MULTILINE)
    body_end = body_start + next_heading.start() if next_heading else len(text)
    return text[body_start:body_end].strip()


def _frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    if not text.startswith("---\n"):
        return {}, text, ["Ledger must start with frontmatter"]
    match = re.match(r"\A---\n(?P<raw>.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if match is None:
        return {}, text, ["Ledger frontmatter is not closed"]
    raw = match.group("raw")
    body = text[match.end():].strip()
    values: dict[str, str] = {}
    errors: list[str] = []
    for line in raw.splitlines():
        if ":" not in line:
            errors.append(f"Invalid ledger frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if not key or not value:
            errors.append(f"Ledger frontmatter requires a value for {key or '<empty>'}")
            continue
        if key in values:
            errors.append(f"Duplicate ledger frontmatter key: {key}")
            continue
        values[key] = value
    return values, body, errors


def validate_requirements(path: Path) -> list[str]:
    text = path.read_text()
    errors: list[str] = []
    status_match = re.search(r"^Status:\s*(\S.*?)\s*$", text, re.MULTILINE)
    status = status_match.group(1) if status_match else None
    if status not in {"Approved", "Draft"}:
        errors.append("Requirements status must be Approved or Draft")
    for heading in REQUIREMENTS_HEADINGS:
        if _section_body(text, heading) is None:
            errors.append(f"Missing requirements heading: {heading}")
    blocking_body = _section_body(text, "## Blocking gaps")
    if status == "Approved" and blocking_body is not None:
        errors.append("Approved artifacts cannot contain blocking gaps")
    if status == "Draft" and not blocking_body:
        errors.append("Draft artifacts require non-empty blocking gaps")
    if _has_forbidden_history(text):
        errors.append("Requirements artifacts cannot contain transcripts or numbered rounds")
    return errors


def validate_ledger(path: Path) -> list[str]:
    text = path.read_text()
    frontmatter, body, errors = _frontmatter(text)
    status = frontmatter.get("status")
    if status == "active":
        missing_keys = ACTIVE_LEDGER_KEYS - set(frontmatter)
        extra_keys = set(frontmatter) - ACTIVE_LEDGER_KEYS
        for key in sorted(missing_keys):
            errors.append(f"Missing active ledger key: {key}")
        for key in sorted(extra_keys):
            errors.append(f"Unexpected active ledger key: {key}")
        for heading in ACTIVE_LEDGER_HEADINGS:
            if _section_body(body, heading) is None:
                errors.append(f"Missing active ledger heading: {heading}")
    elif status in TERMINAL_LEDGER_KEYS:
        allowed = TERMINAL_LEDGER_KEYS[status]
        if set(frontmatter) != allowed or body:
            errors.append(
                f"{status.capitalize()} ledgers must be compact receipts with exact frontmatter keys"
            )
    else:
        errors.append("Ledger status must be active, completed, or aborted")
    if _has_forbidden_history(body):
        errors.append("Ledgers cannot contain transcripts or numbered rounds")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=("requirements", "ledger"))
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    validator = validate_requirements if args.kind == "requirements" else validate_ledger
    try:
        errors = validator(args.path)
    except (OSError, UnicodeError) as error:
        print(error, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
