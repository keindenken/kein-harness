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
    "with-skill": {"plugin_dir": str(KEIN_ROOT), "invoke": "/kein:ralplan "},
    "without-skill": {"plugin_dir": None, "invoke": ""},
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


def prepare_config_home(path):
    """Build a config home that carries authentication and nothing else.

    Inheriting the operator's config home hands every arm their other plugins, and superpowers alone would put a second planning discipline in front of the control arm.
    Measured on this machine: inheriting gave 8 plugins, 13 MCP servers, and 54 skills; pinning gives 1 plugin, 0 MCP servers, and only Claude Code's own built-ins.

    Authentication does not survive the pin on its own, so two files are seeded.
    `.claude.json` gets the account and onboarding keys only — never `projects`, `mcpServers`, or any plugin key, which is what would smuggle the ambient environment back in.
    `.credentials.json` comes from the macOS Keychain, is written 0600, and is deleted when the run ends.
    """
    path.mkdir(parents=True, exist_ok=True)

    source = Path.home() / ".claude.json"
    if not source.exists():
        raise SystemExit(f"ocs eval: cannot seed a config home, {source} is missing")
    original = json.loads(source.read_text())
    keep = ("oauthAccount", "userID", "hasCompletedOnboarding", "lastOnboardingVersion", "firstStartTime", "installMethod")
    (path / ".claude.json").write_text(json.dumps({k: original[k] for k in keep if k in original}, indent=2))

    credentials = run(
        ["security", "find-generic-password", "-s", "Claude Code-credentials", "-w"], check=False,
    )
    if credentials.returncode != 0 or not credentials.stdout.strip():
        raise SystemExit(
            "ocs eval: no 'Claude Code-credentials' entry in the Keychain.\n"
            "  A pinned config home has no login of its own, and running without the pin would let the operator's\n"
            "  other plugins reach every arm, which silently invalidates the comparison."
        )
    target = path / ".credentials.json"
    target.write_bytes(credentials.stdout)
    target.chmod(0o600)
    return path


def discard_credentials(path):
    """Remove the copied secret as soon as the run no longer needs it."""
    secret = path / ".credentials.json"
    if secret.exists():
        secret.unlink()


def summarize_events(path):
    """Turn the event stream into what actually happened, rather than what the arm says happened.

    `system/init` is a complete inventory of what reached the session — plugins, skills, agents, tools, MCP servers — and it comes from configuration rather than from the model, so it settles every question about isolation without asking anyone.
    The tool-use events are the process record: which skill was invoked, which subagents were dispatched, and how many of them.
    This is also the honest way to read lane freshness, because a dispatch event is an observation while the `fresh` field in run state is a claim the arm writes about itself.
    """
    inventory, dispatched, skills_used, writes, turns = {}, [], [], [], 0
    result_text = ""
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind, subtype = event.get("type"), event.get("subtype")
        if kind == "system" and subtype == "init":
            inventory = {
                key: event.get(key) for key in
                ("model", "permissionMode", "plugins", "skills", "agents", "mcp_servers", "tools", "plugin_errors")
            }
        elif kind == "assistant":
            turns += 1
            for block in (event.get("message") or {}).get("content") or []:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                name, params = block.get("name"), block.get("input") or {}
                if name == "Task":
                    dispatched.append({"agent": params.get("subagent_type"), "description": params.get("description")})
                elif name == "Skill":
                    skills_used.append(params.get("skill"))
                elif name in ("Write", "Edit", "NotebookEdit"):
                    writes.append(params.get("file_path"))
        elif kind == "result":
            result_text = event.get("result") or ""
    return {
        "inventory": inventory,
        "subagents_dispatched": dispatched,
        "skills_invoked": skills_used,
        "files_written": writes,
        "assistant_turns": turns,
        "result": result_text,
    }


def launch(arm, worktree, prompt, model, probe, timeout, events_path, config_home):
    # The event stream is the record. Plain text would give only the final message, which cannot show whether a lane was ever dispatched.
    command = [
        "claude", "--model", model,
        "--output-format", "stream-json", "--verbose",
        # Seeding the credential brings the account's own connectors with it — ten of them here, Gmail and Drive and Notion among them.
        # They are constant across arms and so do not break attribution, but a planning task should not have data connectors it never had in the original run.
        "--strict-mcp-config",
        "-p", prompt,
    ]
    plugin_dir = ARMS[arm]["plugin_dir"]
    if plugin_dir:
        command += ["--plugin-dir", plugin_dir]
    if not probe:
        # A real task writes files and dispatches lanes, which a headless run cannot stop to ask about.
        command += ["--permission-mode", "bypassPermissions"]

    # The config home is pinned rather than inherited, which is the same move `ocs ask` makes for the Codex side.
    # Inheriting it would hand every arm the user's other plugins — superpowers among them, whose planning skills would mask the variable under test far more thoroughly than the fixture's own contamination did.
    environment = dict(os.environ, CLAUDE_CONFIG_DIR=str(config_home))

    started = datetime.now(timezone.utc)
    with events_path.open("wb") as sink:
        process = subprocess.Popen(
            command, cwd=worktree, env=environment,
            stdin=subprocess.DEVNULL, stdout=sink, stderr=subprocess.PIPE,
        )
        try:
            _, errors = process.communicate(timeout=timeout)
            timed_out = False
        except subprocess.TimeoutExpired:
            process.kill()
            _, errors = process.communicate()
            timed_out = True

    outcome = {
        "command": command,
        "config_home": str(config_home),
        "prompt": prompt,
        "exit_code": process.returncode,
        "timed_out": timed_out,
        "stderr": (errors or b"").decode("utf-8", "replace")[-4000:],
        "seconds": round((datetime.now(timezone.utc) - started).total_seconds(), 1),
    }
    outcome.update(summarize_events(events_path))
    return outcome


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
        # Everything below reads the session's own init inventory, which comes from configuration rather than from the model.
        inventory = record["run"].get("inventory") or {}
        skills = inventory.get("skills") or []
        plugins = [p.get("name") for p in (inventory.get("plugins") or [])]
        expected_plugins = ["kein"] if ARMS[arm]["plugin_dir"] else []
        checks.append({
            "check": f"plugins loaded are exactly {expected_plugins or 'none'}",
            "arm": arm,
            "pass": sorted(plugins) == sorted(expected_plugins),
            "detail": f"plugins={plugins}",
        })
        checks.append({
            "check": "no inherited MCP servers",
            "arm": arm,
            "pass": not (inventory.get("mcp_servers") or []),
            "detail": f"count={len(inventory.get('mcp_servers') or [])}",
        })
        has_kein = any(str(s).startswith("kein:") for s in skills)
        checks.append({
            "check": f"kein skills {'present' if ARMS[arm]['plugin_dir'] else 'absent'}",
            "arm": arm,
            "pass": has_kein == bool(ARMS[arm]["plugin_dir"]),
            "detail": f"kein skills={[s for s in skills if str(s).startswith('kein:')]}",
        })
        # A rival planning harness is the failure this whole sanitize exists to prevent, so it is named rather than left to the plugin count.
        foreign = [s for s in skills if any(mark in str(s).lower() for mark in ("superpower", "omc", "oh-my-claudecode", "ralph-loop"))]
        checks.append({
            "check": "no foreign planning harness in scope",
            "arm": arm,
            "pass": not foreign,
            "detail": f"found={foreign}" if foreign else "none",
        })
        if not probe:
            checks.append({
                "check": "the skill was actually invoked" if ARMS[arm]["invoke"] else "no skill invoked (control)",
                "arm": arm,
                "pass": bool(record["run"].get("skills_invoked")) == bool(ARMS[arm]["invoke"]),
                "detail": f"skills_invoked={record['run'].get('skills_invoked')}, subagents={len(record['run'].get('subagents_dispatched') or [])}",
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

    # One pinned config home for the whole run, created empty, so no arm inherits the operator's plugins or MCP servers.
    config_home = prepare_config_home(run_dir / "config-home")

    try:
        records = {}

        for arm in ARMS:
            # The control arm receives the same task text without the invocation, so the only thing that differs is whether the workflow is entered.
            # Leaving the invocation out of both would measure whether the model reaches for the skill unprompted, which is a different question than whether the skill's process changes the result.
            prompt = PROBE_PROMPT if options.probe else ARMS[arm]["invoke"] + fixture["task"]
            worktree = run_dir / "worktrees" / arm
            print(f"[{arm}] preparing worktree at {fixture['commit'][:12]}", file=sys.stderr)
            wt = prepare_worktree(fixture["repo"], fixture["commit"], worktree)
            sanitized, touched = sanitize(worktree, contamination)
            loaded = plugin_status(worktree)
            print(f"[{arm}] launching ({model}, {'probe' if options.probe else 'task'})", file=sys.stderr)
            events = run_dir / f"events-{arm}.jsonl"
            outcome = launch(arm, worktree, prompt, model, options.probe, options.timeout, events, config_home)
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
            print(f"[{arm}] exit={outcome['exit_code']} {outcome['seconds']}s, {outcome['assistant_turns']} turns, {len(produced)} files", file=sys.stderr)

        checks = check_plumbing(records, options.probe, contamination)
        manifest = {
            "fixture": options.fixture,
            "fixture_config": fixture,
            "config_path": str(config_path),
            "mode": kind,
            "model": model,
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
    finally:
        # The copied secret goes away whether the run succeeded, failed, or was interrupted.
        discard_credentials(config_home)


if __name__ == "__main__":
    sys.exit(main())
