#!/usr/bin/env python3
"""Render the harness's statusline from the payload Claude Code writes to stdin.

Informed by reading claude-hud (MIT, Jarrod Watts) — its element order, colours and
thresholds are what this reproduces. No code was copied: claude-hud is TypeScript on Node,
and taking it would put a runtime in a plugin that has none.

What it renders, left to right:

    [<model> <effort>] | <project> git:(<branch>*) | ctx <n>% | 5h <n>% (<reset>) | wk <n>% (<reset>)

A segment whose data is absent is dropped, separators included. The whole line is one line:
Claude Code will render more, but every additional element claude-hud offers is off in its
own defaults, and the setup this replaces ran on those defaults.

Failure is silent and total. A statusline that raises prints a Python traceback into the
user's prompt line, which is worse than no statusline, so `main` returns empty on anything
unexpected.
"""

import json
import os
import subprocess
import sys

RESET = "\x1b[0m"
DIM = "\x1b[2m"
RED = "\x1b[31m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
MAGENTA = "\x1b[35m"
CYAN = "\x1b[36m"
BRIGHT_BLUE = "\x1b[94m"
BRIGHT_MAGENTA = "\x1b[95m"


def paint(text, colour):
    return f"{colour}{text}{RESET}"


def context_colour(percent):
    # 85 / 70 are claude-hud's defaults for critical and warning.
    if percent >= 85:
        return RED
    if percent >= 70:
        return YELLOW
    return GREEN


def quota_colour(percent):
    if percent >= 90:
        return RED
    if percent >= 75:
        return BRIGHT_MAGENTA
    return BRIGHT_BLUE


def format_reset(resets_at):
    """Time until a usage window resets, as `45m`, `2h 30m`, `5d 10h`, or `3d`.

    Empty when the reset is unknown or already past, which is what drops the parenthetical
    rather than printing an empty one.
    """
    if resets_at is None:
        return ""
    try:
        import time

        remaining_ms = float(resets_at) * 1000 - time.time() * 1000
    except (TypeError, ValueError):
        return ""
    if remaining_ms <= 0:
        return ""
    # Ceiling, so a window with thirty seconds left reads `1m` rather than `0m`.
    minutes = int(-(-remaining_ms // 60000))
    if minutes < 60:
        return f"{minutes}m"
    hours, minutes = divmod(minutes, 60)
    if hours >= 24:
        days, hours = divmod(hours, 24)
        return f"{days}d {hours}h" if hours else f"{days}d"
    return f"{hours}h {minutes}m" if minutes else f"{hours}h"


def git_segment(cwd):
    """`git:(branch*)`, or empty outside a repository.

    Two cheap commands with a short timeout. The statusline runs on every render, and a git
    call that blocks is a prompt line that stops updating, so a slow or wedged repository
    costs the segment rather than the line.
    """
    def git(*args):
        return subprocess.run(
            ["git", "--no-optional-locks", *args],
            cwd=cwd, capture_output=True, text=True, timeout=1.5,
        )

    try:
        head = git("rev-parse", "--abbrev-ref", "HEAD")
        if head.returncode != 0:
            return ""
        branch = head.stdout.strip()
        if not branch:
            return ""
        if branch == "HEAD":
            short = git("rev-parse", "--short", "HEAD")
            branch = short.stdout.strip()
            if not branch:
                return ""
        status = git("-c", "core.quotePath=false", "status", "--porcelain")
        if status.returncode == 0 and status.stdout.strip():
            branch += "*"
    except (OSError, subprocess.SubprocessError):
        return ""
    return paint("git:(", MAGENTA) + paint(branch, CYAN) + paint(")", MAGENTA)


def effort_level(raw):
    """The effort level as a word. claude-hud also prints a symbol; this never does.

    The setup this replaces stripped those symbols back out with `sed`, so rendering them
    in order to remove them is work with no reader.
    """
    if isinstance(raw, str):
        return raw.strip().lower() or None
    if isinstance(raw, dict):
        level = raw.get("level")
        if isinstance(level, str) and level.strip():
            return level.strip().lower()
    return None


def context_percent(window):
    if not isinstance(window, dict):
        return None
    native = window.get("used_percentage")
    if isinstance(native, (int, float)):
        return int(round(native))
    size = window.get("context_window_size")
    usage = window.get("current_usage")
    if not isinstance(size, (int, float)) or not size or not isinstance(usage, dict):
        return None
    used = sum(
        value for key, value in usage.items()
        if key.endswith("input_tokens") and isinstance(value, (int, float))
    )
    return int(round(used / size * 100))


def window_segment(label, window):
    if not isinstance(window, dict):
        return None
    percent = window.get("used_percentage")
    if not isinstance(percent, (int, float)):
        return None
    percent = int(round(percent))
    part = paint(label, DIM) + " " + paint(f"{percent}%", quota_colour(percent))
    reset = format_reset(window.get("resets_at"))
    if reset:
        part += " " + paint(f"({reset})", DIM)
    return part


def render(data):
    segments = []

    model = (data.get("model") or {}).get("display_name") or "Claude"
    effort = effort_level(data.get("effort"))
    segments.append(paint(f"[{model} {effort}]" if effort else f"[{model}]", CYAN))

    workspace = data.get("workspace") or {}
    cwd = workspace.get("current_dir") or data.get("cwd") or os.getcwd()
    project = paint(os.path.basename(os.path.normpath(cwd)), YELLOW)
    git = git_segment(cwd)
    segments.append(f"{project} {git}" if git else project)

    percent = context_percent(data.get("context_window"))
    if percent is not None:
        segments.append("ctx " + paint(f"{percent}%", context_colour(percent)))

    limits = data.get("rate_limits") or {}
    for label, key in (("5h", "five_hour"), ("wk", "seven_day")):
        segment = window_segment(label, limits.get(key))
        if segment:
            segments.append(segment)

    return RESET + " | ".join(segments)


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return ""
        return render(json.loads(raw))
    except Exception:
        return ""


if __name__ == "__main__":
    line = main()
    if line:
        sys.stdout.write(line + "\n")
