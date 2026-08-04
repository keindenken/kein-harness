#!/usr/bin/env python3
"""Run an A/B evaluation of skill variants against a pinned fixture.

Every arm and every replicate starts from a worktree detached at the same commit, so a difference in output cannot be attributed to a difference in starting state.
The harness prepares each worktree before an arm launches; an arm never creates its own, because a worktree made inside a session is a variable the harness does not control and would differ per arm.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

KEIN_ROOT = Path(os.environ["KEIN_ROOT"])

# The plugin reaches an arm through --plugin-dir, which bypasses the enabledPlugins gate.
# That is what makes a genuinely skill-absent control arm possible: the ambient default is off everywhere, and only an injected arm has the harness.
ARMS = {
    "with-skill": {"plugin_dir": str(KEIN_ROOT)},
    "without-skill": {"plugin_dir": None},
}

# A probe asks what reached the session instead of doing the task.
# The answer has to be machine-readable, because a prose answer would need a judge to interpret it and the point of a plumbing check is that it needs no judgement.
PROBE_PROMPT = (
    "Report only on capabilities available to you RIGHT NOW: skills you could invoke, plugins loaded into this session, agents you could dispatch.\n"
    "Do NOT count anything merely described, mentioned, or referenced in files, instructions, or documentation you can read.\n"
    "A name appearing in CLAUDE.md or in a directory name is NOT availability.\n"
    "\n"
    "Reply with exactly one line and nothing else, in this form:\n"
    "KEIN=<yes|no> OMC=<yes|no> CWD=<absolute path of your working directory>\n"
    "KEIN is yes only if a skill named kein:ping is invocable by you.\n"
    "OMC is yes only if a skill, plugin, or agent whose name contains 'omc' or 'oh-my-claudecode' is invocable by you.\n"
    "Do not explain."
)


def run(args, cwd=None, timeout=None, check=True):
    result = subprocess.run(
        args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=False,
    )
    if check and result.returncode != 0:
        raise SystemExit(
            f"ocs eval: command failed ({result.returncode}): {' '.join(map(str, args))}\n"
            + result.stderr.decode("utf-8", "replace")
        )
    return result


def state_dir(sub):
    out = run([str(KEIN_ROOT / "libexec" / "ocs-state-dir"), sub]).stdout
    return Path(out.decode().strip())


def load_config():
    path = state_dir("eval") / "fixtures.json"
    if not path.exists():
        raise SystemExit(f"ocs eval: no fixture definitions at {path}")
    return json.loads(path.read_text()), path


def prepare_worktree(repo, commit, destination):
    """Detach at the pinned commit so many worktrees can share one commit.

    Detached is not incidental. Git refuses two worktrees on the same branch, and every arm here starts at the same commit by design.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "worktree", "add", "--detach", "--quiet", str(destination), commit], cwd=repo)
    toplevel = run(["git", "rev-parse", "--show-toplevel"], cwd=destination).stdout.decode().strip()
    head = run(["git", "rev-parse", "HEAD"], cwd=destination).stdout.decode().strip()
    return {"toplevel": toplevel, "head": head}


def sanitize(worktree, contamination):
    """Strip a second harness out of the worktree, identically for every arm.

    The fixture repository tracks its own `.claude/settings.json` and its own project skills, so a worktree arrives carrying another harness's planning guidance.
    That guidance can mask the ablated rule and produce a null that reads as "the rule does not matter" when it means "something else already covered it".
    Applying the same strip to every arm keeps the starting state identical while removing the mask.
    """
    changes = []
    # Sanitizing dirties the worktree, so the paths it touches have to be remembered.
    # Otherwise `git status` reports them as work the arm produced, and the harness's own bookkeeping lands inside the artifact set being measured.
    touched = set()

    settings = worktree / ".claude" / "settings.json"
    disable = contamination.get("disable_plugins", [])
    if settings.exists() and disable:
        data = json.loads(settings.read_text())
        enabled = data.setdefault("enabledPlugins", {})
        for name in disable:
            if enabled.get(name) is not False:
                enabled[name] = False
                changes.append(f"disabled {name}")
        settings.write_text(json.dumps(data, indent=2) + "\n")
        touched.add(".claude/settings.json")

    for relative in contamination.get("remove_paths", []):
        target = worktree / relative
        if target.exists():
            shutil.rmtree(target) if target.is_dir() else target.unlink()
            changes.append(f"removed {relative}")
            touched.add(relative)

    # A delimited block is stripped rather than the whole file, because the same file also carries the project grounding the task legitimately needs.
    # Disabling the plugin is not enough on its own: its instructions can survive as prose inside the repository's own CLAUDE.md.
    for block in contamination.get("strip_blocks", []):
        target = worktree / block["path"]
        if not target.exists():
            continue
        text = target.read_text()
        start, end = text.find(block["start"]), text.find(block["end"])
        if start < 0 or end < 0 or end < start:
            continue
        stripped = text[:start] + text[end + len(block["end"]):]
        target.write_text(stripped.lstrip("\n"))
        removed = text[start:end].count("\n") + 1
        changes.append(f"stripped {removed} lines from {block['path']}")
        touched.add(block["path"])

    return changes, sorted(touched)


def plugin_status(worktree):
    """Ask the CLI what is loaded, rather than asking the model.

    The model reports what it believes, and a first probe showed it will answer "yes" for a harness that is only named in the instructions it read.
    `claude plugin list` answers from configuration, so it is the authority for whether a plugin actually reached the session.
    """
    result = run(["claude", "plugin", "list"], cwd=worktree, check=False)
    statuses = {}
    name = None
    for line in result.stdout.decode("utf-8", "replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("❯"):
            name = stripped.lstrip("❯ ").strip()
        elif stripped.startswith("Status:") and name:
            statuses.setdefault(name, []).append("enabled" if "enabled" in stripped or "loaded" in stripped else "disabled")
    return statuses


def launch(arm, worktree, prompt, model, probe, timeout):
    command = ["claude", "--model", model, "-p", prompt]
    plugin_dir = ARMS[arm]["plugin_dir"]
    if plugin_dir:
        command += ["--plugin-dir", plugin_dir]
    if not probe:
        # A real task writes files and dispatches lanes, which a headless run cannot stop to ask about.
        command += ["--permission-mode", "bypassPermissions"]

    started = datetime.now(timezone.utc)
    try:
        result = run(command, cwd=worktree, timeout=timeout, check=False)
        timed_out = False
    except subprocess.TimeoutExpired:
        return {
            "command": command, "exit_code": None, "timed_out": True,
            "stdout": "", "stderr": f"timed out after {timeout}s",
            "seconds": timeout,
        }
    return {
        "command": command,
        "exit_code": result.returncode,
        "timed_out": timed_out,
        "stdout": result.stdout.decode("utf-8", "replace"),
        "stderr": result.stderr.decode("utf-8", "replace"),
        "seconds": round((datetime.now(timezone.utc) - started).total_seconds(), 1),
    }


def collect(worktree, destination, exclude=()):
    """Capture what the arm actually produced, separately from what it said.

    A work product that is a file survives regardless of what the final message contained, so the files are the record and stdout is corroboration.
    """
    porcelain = run(["git", "status", "--porcelain"], cwd=worktree).stdout.decode()
    produced = []
    destination.mkdir(parents=True, exist_ok=True)
    for line in porcelain.splitlines():
        if not line.strip():
            continue
        relative = line[3:].strip().strip('"')
        if relative in exclude:
            continue
        source = worktree / relative
        if not source.is_file():
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        produced.append({"path": relative, "bytes": source.stat().st_size})
    return produced


def check_plumbing(records, probe, contamination):
    """Report the plumbing assertions rather than assuming them.

    A run whose isolation silently failed is worse than one that failed loudly, because its numbers still look like numbers.
    """
    checks = []
    for arm, record in records.items():
        wt = record["worktree"]
        checks.append({
            "check": "worktree owns its git root",
            "arm": arm,
            "pass": wt["toplevel"] == record["path"],
            "detail": f"toplevel={wt['toplevel']}",
        })
        checks.append({
            "check": "detached at the pinned commit",
            "arm": arm,
            "pass": wt["head"] == record["expected_commit"],
            "detail": f"head={wt['head'][:12]}",
        })
        checks.append({
            "check": "contamination stripped",
            "arm": arm,
            "pass": bool(record["sanitized"]),
            "detail": ", ".join(record["sanitized"]) or "nothing changed",
        })
        for name in contamination.get("disable_plugins", []):
            seen = record["plugins"].get(name, [])
            checks.append({
                "check": f"{name} not loaded (from the CLI, not the model)",
                "arm": arm,
                "pass": bool(seen) and all(state == "disabled" for state in seen),
                "detail": f"status={seen or 'not listed'}",
            })
        if probe:
            answer = record["run"]["stdout"].strip().splitlines()
            line = answer[-1] if answer else ""
            expect_kein = "yes" if ARMS[arm]["plugin_dir"] else "no"
            checks.append({
                "check": f"kein presence is {expect_kein}",
                "arm": arm,
                "pass": f"KEIN={expect_kein}" in line,
                "detail": line,
            })
            checks.append({
                "check": "omc absent",
                "arm": arm,
                "pass": "OMC=no" in line,
                "detail": line,
            })
    return checks


def main():
    parser = argparse.ArgumentParser(prog="ocs eval")
    parser.add_argument("fixture", help="fixture name defined in .agents/kein/eval/fixtures.json")
    parser.add_argument("--probe", action="store_true", help="ask each arm what reached it instead of running the task")
    parser.add_argument("--timeout", type=int, default=1800, help="per-arm timeout in seconds")
    parser.add_argument("--keep", action="store_true", help="leave worktrees on disk for inspection")
    options = parser.parse_args()

    config, config_path = load_config()
    fixtures = config["fixtures"]
    if options.fixture not in fixtures:
        raise SystemExit(f"ocs eval: unknown fixture '{options.fixture}'. Known: {', '.join(sorted(fixtures))}")
    fixture = fixtures[options.fixture]
    contamination = config.get("contamination", {})
    model = config.get("models", {}).get("arm", "sonnet")

    stamp = datetime.now().strftime("%y%m%d-%H%M%S")
    kind = "probe" if options.probe else "task"
    run_dir = state_dir("runs/eval") / f"{stamp}-{options.fixture}-{kind}"
    run_dir.mkdir(parents=True)

    prompt = PROBE_PROMPT if options.probe else fixture["task"]
    records = {}

    for arm in ARMS:
        worktree = run_dir / "worktrees" / arm
        print(f"[{arm}] preparing worktree at {fixture['commit'][:12]}", file=sys.stderr)
        wt = prepare_worktree(fixture["repo"], fixture["commit"], worktree)
        sanitized, touched = sanitize(worktree, contamination)
        loaded = plugin_status(worktree)
        print(f"[{arm}] launching ({model}, {'probe' if options.probe else 'task'})", file=sys.stderr)
        outcome = launch(arm, worktree, prompt, model, options.probe, options.timeout)
        produced = collect(worktree, run_dir / "artifacts" / arm, exclude=set(touched))
        records[arm] = {
            "path": str(worktree),
            "expected_commit": fixture["commit"],
            "worktree": wt,
            "sanitized": sanitized,
            "sanitized_paths": touched,
            "plugins": loaded,
            "run": outcome,
            "produced": produced,
        }
        print(f"[{arm}] exit={outcome['exit_code']} {outcome['seconds']}s, {len(produced)} files", file=sys.stderr)

    checks = check_plumbing(records, options.probe, contamination)
    manifest = {
        "fixture": options.fixture,
        "fixture_config": fixture,
        "config_path": str(config_path),
        "mode": kind,
        "model": model,
        "prompt": prompt,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "arms": records,
        "plumbing_checks": checks,
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    print(f"\nrun: {run_dir}")
    failed = 0
    for check in checks:
        mark = "ok  " if check["pass"] else "FAIL"
        failed += 0 if check["pass"] else 1
        print(f"  {mark} [{check['arm']}] {check['check']} — {check['detail']}")

    if not options.keep:
        for arm in records:
            run(["git", "worktree", "remove", "--force", records[arm]["path"]], cwd=fixture["repo"], check=False)
        print("  worktrees removed (pass --keep to inspect them)")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
