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
    "with-skill": {"inject": True, "invoke": "/kein:ralplan "},
    "without-skill": {"inject": False, "invoke": ""},
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


def run(args, cwd=None, timeout=None, check=True, env=None):
    result = subprocess.run(
        args, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=False,
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


def prepare_plugin(path, model):
    """Copy the plugin for this run and re-render its agents onto one model.

    `--model` sets the lead only, and a subagent's `model:` frontmatter wins, so the deep-tier roles — planner, architect, critic — arrive as Opus under a Sonnet lead.
    That is expensive, and worse, it makes the arms differ by model as well as by skill: with-skill gets Opus lanes while the control improvises cheaper ones, and a difference between them can no longer be read as the skill's doing.
    Copying rather than rendering in place also keeps the installed harness untouched while a run is in flight.
    """
    shutil.copytree(KEIN_ROOT, path, symlinks=True)
    run(
        [str(path / "libexec" / "ocs-render-agents"), str(path / "agents")],
        env=dict(os.environ, KEIN_ROOT=str(path), KEIN_TIER_MODEL=model),
    )
    models = sorted({
        line.split(":", 1)[1].strip()
        for agent in (path / "agents").glob("*.md")
        for line in agent.read_text().splitlines()[:8]
        if line.startswith("model:")
    })
    if models != [model]:
        raise SystemExit(f"ocs eval: agent models did not collapse to {model}: {models}")
    return path


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


def sessions_outside(config_home, allowed):
    """Name every working directory this run opened a session in, minus the ones it was supposed to.

    Claude Code encodes the working directory into a project directory name under the config home, so a pinned config home records where every lead and lane actually ran.
    A first run left a directory for the origin fixture repository, meaning a lane had been pointed at live work rather than at its detached copy.
    """
    projects = config_home / "projects"
    if not projects.is_dir():
        return []
    permitted = {str(Path(a).resolve()).replace("/", "-").replace(".", "-") for a in allowed}
    return sorted(d.name for d in projects.iterdir() if d.is_dir() and d.name not in permitted)


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
                # The dispatch tool is `Agent`; `Task` is accepted too so a rename upstream does not silently zero this out.
                if name in ("Agent", "Task"):
                    dispatched.append({
                        "agent": params.get("subagent_type"),
                        "description": params.get("description"),
                        "background": params.get("run_in_background"),
                    })
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


def ask_traces(worktree):
    """Every `ocs ask` call the lead made, read from the traces it left rather than from the event stream.

    A bridge lane is a shell call, so nothing about it appears as a tool the parser can recognize.
    `--trace` is what makes the lane observable at all, which is why the lane reference requires it.
    """
    root = Path(worktree) / ".agents" / "kein" / "runs" / "ask"
    traces = []
    for directory in sorted(root.glob("*")) if root.is_dir() else []:
        prompt = directory / "prompt.txt"
        command = directory / "command.txt"
        traces.append({
            "dir": directory.name,
            "role": directory.name.split("-", 3)[-1],
            "prompt": prompt.read_text(errors="replace") if prompt.is_file() else "",
            "command": command.read_text(errors="replace") if command.is_file() else "",
            "answered": (directory / "response.txt").is_file(),
        })
    return traces


def ralplan_lanes(worktree):
    """The verdict keys the workflow actually wrote, which is where a lane roster becomes visible."""
    root = Path(worktree) / ".agents" / "kein" / "runs" / "ralplan"
    lanes = []
    for state in sorted(root.rglob("state.json")) if root.is_dir() else []:
        try:
            payload = json.loads(state.read_text())
        except (OSError, ValueError):
            continue
        for key in payload.get("verdicts", {}) or payload.get("approvals", {}) or {}:
            if key not in lanes:
                lanes.append(key)
    return lanes


def repository_instruction_lines(worktree):
    """Long lines from the repository's own instruction files, used to tell whether a brief carried them.

    `ocs ask` deliberately injects no repository instructions, so a bridge lane that received none was briefed incompletely.
    Matching on the longest lines keeps a coincidental one-word overlap from counting as a match.
    """
    lines = []
    for name in (".claude/CLAUDE.md", "CLAUDE.md", "AGENTS.md"):
        path = Path(worktree) / name
        if path.is_file():
            lines += [line.strip() for line in path.read_text(errors="replace").splitlines()]
    return sorted({line for line in lines if len(line) > 60}, key=len, reverse=True)[:40]


def launch(arm, worktree, prompt, model, probe, timeout, events_path, config_home, plugin_dir, max_turns):
    # The event stream is the record. Plain text would give only the final message, which cannot show whether a lane was ever dispatched.
    command = [
        "claude", "--model", model,
        "--output-format", "stream-json", "--verbose",
        # Seeding the credential brings the account's own connectors with it — ten of them here, Gmail and Drive and Notion among them.
        # They are constant across arms and so do not break attribution, but a planning task should not have data connectors it never had in the original run.
        "--strict-mcp-config",
        "-p", prompt,
    ]
    if ARMS[arm]["inject"]:
        command += ["--plugin-dir", str(plugin_dir)]
    if max_turns:
        # A backstop against a runaway loop, not a round limiter: a run that produced a plan took 135 assistant turns, so the ceiling is set far above any honest run.
        # It also cannot reach a subagent's own turns, so the real cost lever is the pinned model, not this.
        command += ["--max-turns", str(max_turns)]
    if not probe:
        # A real task writes files and dispatches lanes, which a headless run cannot stop to ask about.
        command += ["--permission-mode", "bypassPermissions"]

    # The config home is pinned rather than inherited, which is the same move `ocs ask` makes for the Codex side.
    # Inheriting it would hand every arm the user's other plugins — superpowers among them, whose planning skills would mask the variable under test far more thoroughly than the fixture's own contamination did.
    # KEIN_STATE_ROOT pins the arm's run ledger to its own worktree.
    # Without it a lead that steps into the plugin directory to read a reference makes `ocs state-dir` resolve to the harness repository, and the ledger escapes the arm entirely.
    environment = dict(os.environ, CLAUDE_CONFIG_DIR=str(config_home), KEIN_STATE_ROOT=str(worktree))

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
        expected_plugins = ["kein"] if ARMS[arm]["inject"] else []
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
            "check": f"kein skills {'present' if ARMS[arm]['inject'] else 'absent'}",
            "arm": arm,
            "pass": has_kein == bool(ARMS[arm]["inject"]),
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
            # A slash invocation does not emit a Skill tool_use — the CLI expands it directly — so entry is read from the lanes it dispatches instead.
            # Dispatching a kein: role is specific to this workflow and cannot happen by accident in the control arm.
            dispatched = record["run"].get("subagents_dispatched") or []
            lanes = [d.get("agent") for d in dispatched if str(d.get("agent") or "").startswith("kein:")]
            checks.append({
                "check": "the workflow dispatched its own lanes" if ARMS[arm]["invoke"] else "no kein lane dispatched (control)",
                "arm": arm,
                "pass": bool(lanes) == bool(ARMS[arm]["invoke"]),
                "detail": f"kein lanes={lanes}, all subagents={[d.get('agent') for d in dispatched]}",
            })
            # Dispatching into the background and then waiting is the known way for a lane's report to be lost.
            # Only the workflow promises to avoid it, so only the workflow can fail here; for the control this is an observation, and an interesting one, since a bare lead does the risky thing the rule exists to prevent.
            backgrounded = [d.get("agent") for d in dispatched if d.get("background") is not False]
            checks.append({
                "check": "no lane left to report through a background notification"
                         if ARMS[arm]["invoke"] else "background dispatch by a lead with no such rule (observation)",
                "arm": arm,
                "pass": (not backgrounded) or not ARMS[arm]["invoke"],
                "detail": f"backgrounded={backgrounded}" if backgrounded else "all synchronous",
            })
            # A cross-vendor lane is a shell call, so none of the event-stream checks above can see it.
            # These run only when the invocation asked for one; a native run has nothing here to assert.
            if "codex" in record.get("invoke", ""):
                traces = record.get("ask_traces") or []
                review_traces = [trace for trace in traces if trace["role"] in ("architect", "critic")]
                checks.append({
                    "check": "the codex lane actually ran",
                    "arm": arm,
                    "pass": bool(review_traces),
                    "detail": f"traces={[trace['dir'] for trace in traces]}" if traces else "no ocs ask trace",
                })
                checks.append({
                    "check": "the lane carried the canonical role prompt",
                    "arm": arm,
                    "pass": bool(review_traces) and all("<Agent_Prompt>" in trace["prompt"] for trace in review_traces),
                    "detail": f"{sum('<Agent_Prompt>' in trace['prompt'] for trace in review_traces)}/{len(review_traces)} carried it",
                })
                # The bridge runs against the pristine Codex home on purpose, so the plugin's role prompt is what shapes the reply.
                # A lane that picked up ~/.codex-orca would be answering as the operator's tuned lead as well.
                homes = [line for trace in review_traces for line in trace["command"].splitlines() if line.startswith("CODEX_HOME=")]
                checks.append({
                    "check": "the lane ran against the vanilla codex home",
                    "arm": arm,
                    "pass": bool(homes) and all(home.endswith("/.codex") for home in homes),
                    "detail": f"homes={sorted(set(homes))}" if homes else "no CODEX_HOME recorded",
                })
                instructions = repository_instruction_lines(record["path"])
                briefed = [
                    trace for trace in review_traces
                    if any(line in trace["prompt"] for line in instructions)
                ]
                checks.append({
                    "check": "the brief carried repository instructions",
                    "arm": arm,
                    "pass": bool(review_traces) and len(briefed) == len(review_traces),
                    "detail": f"{len(briefed)}/{len(review_traces)} briefed against {len(instructions)} candidate lines",
                })
                lanes = record.get("ralplan_lanes") or []
                checks.append({
                    "check": "verdicts are keyed by lane, including the codex lane",
                    "arm": arm,
                    "pass": any(lane.startswith(("architect@codex", "critic@codex")) for lane in lanes),
                    "detail": f"lanes={lanes}" if lanes else "no ralplan state written",
                })
            checks.append({
                "check": "produced at least one file",
                "arm": arm,
                "pass": bool(record["produced"]),
                "detail": f"{len(record['produced'])} files",
            })
            # Claude Code names a project directory after the working directory it ran in, so the config home doubles as a record of everywhere this run went.
            # A directory for anything other than the two arm worktrees means a lane escaped its isolation — the origin fixture repository being the one that matters, since an arm reaching it can read, and in principle write, live work.
            strayed = record.get("visited_outside") or []
            checks.append({
                "check": "no session ran outside an arm worktree",
                "arm": arm,
                "pass": not strayed,
                "detail": f"strayed={strayed}" if strayed else "none",
            })
    return checks


def main():
    parser = argparse.ArgumentParser(prog="ocs eval")
    parser.add_argument("fixture", help="fixture name defined in .agents/kein/eval/fixtures.json")
    parser.add_argument("--probe", action="store_true", help="ask each arm what reached it instead of running the task")
    parser.add_argument("--timeout", type=int, default=1800, help="per-arm timeout in seconds")
    parser.add_argument("--keep", action="store_true", help="leave worktrees on disk for inspection")
    parser.add_argument("--arm", action="append", choices=sorted(ARMS), help="run only these arms; repeatable. A conformance run needs one arm, not a comparison.")
    parser.add_argument("--invoke", help="override the injected arm's invocation, e.g. '/kein:ralplan --critic claude,codex '. The trailing space matters.")
    parser.add_argument("--max-turns", type=int, default=500, help="runaway backstop for the lead; not a round limiter")
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
    plugin_dir = prepare_plugin(run_dir / "plugin", model)

    try:
        records = {}

        selected = options.arm or list(ARMS)
        for arm in selected:
            # The control arm receives the same task text without the invocation, so the only thing that differs is whether the workflow is entered.
            # Leaving the invocation out of both would measure whether the model reaches for the skill unprompted, which is a different question than whether the skill's process changes the result.
            invoke = ARMS[arm]["invoke"]
            if options.invoke is not None and ARMS[arm]["inject"]:
                invoke = options.invoke
            prompt = PROBE_PROMPT if options.probe else invoke + fixture["task"]
            worktree = run_dir / "worktrees" / arm
            print(f"[{arm}] preparing worktree at {fixture['commit'][:12]}", file=sys.stderr)
            wt = prepare_worktree(fixture["repo"], fixture["commit"], worktree)
            sanitized, touched = sanitize(worktree, contamination)
            loaded = plugin_status(worktree)
            print(f"[{arm}] launching ({model}, {'probe' if options.probe else 'task'})", file=sys.stderr)
            events = run_dir / f"events-{arm}.jsonl"
            outcome = launch(arm, worktree, prompt, model, options.probe, options.timeout, events, config_home, plugin_dir, options.max_turns)
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
                "invoke": invoke,
                "ask_traces": ask_traces(worktree),
                "ralplan_lanes": ralplan_lanes(worktree),
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
