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
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

try:
    KEIN_ROOT = Path(os.environ["KEIN_ROOT"])
except KeyError:
    raise SystemExit("ocs eval: KEIN_ROOT environment variable is not set; run this command through 'ocs eval', which sets KEIN_ROOT")

# The plugin reaches an arm through --plugin-dir, which bypasses the enabledPlugins gate.
# That is what makes a genuinely skill-absent control arm possible: the ambient default is off everywhere, and only an injected arm has the harness.
# Ranking judges, pinned to one tier on purpose.
#
# A role's declared tier is set by the work that role normally does -- deep for the ones
# that design, standard for the one that checks evidence. As judges they are all doing the
# same job, so the tier that matters is the one the judging needs, not the one the role
# carries elsewhere.
#
# It has to be the same tier for all of them because the ranking sums their Borda points.
# Equal weight in the aggregate is a claim of equal capability, and a standard-tier judge
# sitting beside two deep ones gets an equal say it has not earned. The alternative is to
# stop aggregating and read the per-judge orders the report already prints; pinning is
# cheaper and keeps both readings available.
#
# Graders go the other way and stay at the role's tier: many narrow pass/fail calls, each
# read on its own, nothing summed across judges.
RANK_JUDGES = ["critic@codex:gpt-5.6-sol", "architect@codex:gpt-5.6-sol",
               "verifier@codex:gpt-5.6-sol"]

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


def prepare_plugin(path, model, source=None):
    """Copy the plugin for this run and re-render its agents onto one model.

    `source` defaults to the installed harness. A variant arm passes the `plugin/`
    directory of a worktree checked out at some other commit, which is what makes
    "this prompt against that prompt" an arm rather than a separate experiment.

    `--model` sets the lead only, and a subagent's `model:` frontmatter wins, so the deep-tier roles — planner, architect, critic — arrive as Opus under a Sonnet lead.
    That is expensive, and worse, it makes the arms differ by model as well as by skill: with-skill gets Opus lanes while the control improvises cheaper ones, and a difference between them can no longer be read as the skill's doing.
    Copying rather than rendering in place also keeps the installed harness untouched while a run is in flight.
    """
    # `evals` and the runner under `libexec/eval` are excluded whatever commit they come
    # from. Cases now live outside the plugin, but a `--variant` arm copies the plugin as
    # it existed at some older commit, where they did not, and the arm has no use for
    # either: the graders are what will judge it and `selftest/should-pass` is a worked
    # answer to the fixture it is planning for.
    shutil.copytree(source or KEIN_ROOT, path, symlinks=True,
                    ignore=shutil.ignore_patterns("evals", "eval"))
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


def evals_root():
    """Where the graded cases live: `evals/` in the harness repository, not in the plugin.

    They used to sit at `KEIN_ROOT/evals`, which is inside the plugin directory, which
    `prepare_plugin` copies wholesale and hands an arm as its `--plugin-dir`. Every arm
    therefore ran with the eleven graders that would judge it and with
    `selftest/should-pass/PLAN.md` -- a worked answer to the very fixture it was planning
    for -- readable on disk. No arm was found to have read either across six runs, and one
    did list the paths while looking for REQUIREMENTS.md, so it was an open channel rather
    than a used one. Cases are development assets and a plugin someone installs has no use
    for them.
    """
    found = run(["git", "rev-parse", "--show-toplevel"], cwd=KEIN_ROOT, check=False)
    if found.returncode != 0:
        raise SystemExit("ocs eval: graded cases live in the harness repository's `evals/`, "
                         f"and {KEIN_ROOT} is not inside one.")
    return Path(found.stdout.decode().strip()) / "evals"


def resolve_case(name):
    """A case name or a path, to the directory holding its `case.yaml`.

    Both entry points resolve it the same way and fail the same way. `--self-test` used to
    resolve without checking, so an unknown name reached `load_case` and came back as a
    FileNotFoundError traceback instead of the list of cases that do exist.
    """
    case_dir = Path(name)
    if not (case_dir / "case.yaml").is_file():
        case_dir = evals_root() / name
    if not (case_dir / "case.yaml").is_file():
        known = sorted(p.parent.name for p in evals_root().glob("*/case.yaml"))
        raise SystemExit(f"ocs eval: no case.yaml under {case_dir}. Known: {', '.join(known) or 'none'}")
    return case_dir


def prune_empty_dirs(root):
    """Remove the directories a finished run left holding nothing.

    A replicate's worktree goes as soon as its graders have read it, but the `worktrees/` tree that held it does not, and a pinned config home ends every replicate with half a dozen empty scaffolding directories of Claude's own.
    None of that is a finding, and all of it makes a spent run look like it still has something in it.
    `rmdir` refuses a directory with anything in it, so walking deepest-first removes exactly the empty ones and cannot reach a kept artifact.
    """
    for path in sorted((p for p in Path(root).rglob("*") if p.is_dir()),
                       key=lambda p: len(p.parts), reverse=True):
        try:
            path.rmdir()
        except OSError:
            pass


def prepare_config_home(path):
    """Build a config home that carries authentication and nothing else.

    Inheriting the operator's config home hands every arm their other plugins, and superpowers alone would put a second planning discipline in front of the control arm.
    Measured on this machine: inheriting gave 8 plugins, 13 MCP servers, and 54 skills; pinning gives 1 plugin, 0 MCP servers, and only Claude Code's own built-ins.

    Authentication does not survive the pin on its own, so two files are seeded.
    `.claude.json` gets the account and onboarding keys only — never `projects`, `mcpServers`, or any plugin key, which is what would smuggle the ambient environment back in.
    `.credentials.json` comes from the macOS Keychain, is written 0600, and is deleted when the run ends.

    The pin covers plugins and MCP servers, not `~/.claude/CLAUDE.md`, which reaches every Claude agent by design and is why lead-only guidance has to arrive some other way.
    Confirmed for this config home rather than assumed: a run under it still quoted that file back.
    Attribution survives, since every arm gets the same file, but a planning rule added there reaches the control arm too and would move the comparison without the fixture or the skill moving.
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


def _argv_value(command, flag):
    """The value that followed `flag` in a recorded argv, one token per line."""
    lines = command.splitlines()
    for index, line in enumerate(lines[:-1]):
        if line == flag:
            return lines[index + 1]
    return ""


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


def team_traces(worktree):
    """Every `ocs team` worker the lead started, read from its trace directory.

    A team lane leaves more behind than an ask lane because it has to: the launch path that gives
    the worker a per-lane model and sandbox is the one Orca cannot produce a hook transcript for,
    so the trace and the worker's own report are the entire record of what ran.
    """
    root = Path(worktree) / ".agents" / "kein" / "runs" / "team"
    traces = []
    for directory in sorted(root.glob("*")) if root.is_dir() else []:
        def read(name):
            path = directory / name
            return path.read_text(errors="replace") if path.is_file() else ""

        # The trace records one `key=value` header line per fact and then the launch as its last line,
        # because a launch is a single shell string rather than the one-token-per-line argv an ask lane records.
        # Splitting on the last line rather than on whitespace keeps a path containing a space from being read as a launch.
        lines = read("command.txt").splitlines()
        launch = lines[-1] if lines else ""
        header = dict(line.partition("=")[::2] for line in lines[:-1] if "=" in line)
        traces.append({
            "dir": directory.name,
            "role": directory.name.split("-", 2)[-1],
            "role_prompt": read("role.md"),
            "spec": read("spec.txt"),
            "report": read("report.md"),
            "header": header,
            "launch": launch,
        })
    return traces


def _launch_value(launch, flag):
    """The token that followed `flag` in a recorded shell launch string."""
    tokens = launch.split()
    for index, token in enumerate(tokens[:-1]):
        if token == flag:
            return tokens[index + 1]
    return ""


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


WORKTREE_INSTRUCTION_NAMES = (".claude/CLAUDE.md", "CLAUDE.md", "AGENTS.md")


def binding_instruction_lines(worktree):
    """Long lines from the worktree's own instruction files, used to tell whether a brief carried them.

    `ocs ask` and `ocs team` inject no instructions by design, so a bridge lane that received none was briefed incompletely.
    Matching on the longest lines keeps a coincidental one-word overlap from counting as a match.

    The operator's `~/.claude/CLAUDE.md` is deliberately out of scope, and it is the more interesting omission.
    It reaches the lead and every native lane automatically while reaching no Codex lane at all, so a cross-vendor brief does have to carry it by hand, and the first observed team run carried it faithfully.
    It was carried as a paraphrase, which is what a lead should do, and neither escape this check offers survives that: substring matching reads a paraphrase as an omission, and naming the file instead points a worktree-sandboxed lane at something it cannot open.
    Including it therefore converts a correct pass into a false failure. Whether the standing conventions reached a lane is not a thing this instrument can measure; pretending otherwise costs more than the silence does.
    """
    lines = []
    for name in WORKTREE_INSTRUCTION_NAMES:
        path = Path(worktree) / name
        if path.is_file():
            lines += [line.strip() for line in path.read_text(errors="replace").splitlines()]
    return sorted({line for line in lines if len(line) > 60}, key=len, reverse=True)[:40]


def worktree_instruction_names(worktree):
    """The instruction files a lane could open for itself, which is what makes naming one an acceptable substitute for quoting it."""
    return [Path(name).name for name in WORKTREE_INSTRUCTION_NAMES if (Path(worktree) / name).is_file()]


def launch(arm, worktree, prompt, model, probe, timeout, events_path, config_home, plugin_dir, max_turns, denied=()):
    """`plugin_dir` is None for an arm that runs without the harness."""
    # The event stream is the record. Plain text would give only the final message, which cannot show whether a lane was ever dispatched.
    command = [
        "claude", "--model", model,
        "--output-format", "stream-json", "--verbose",
        # Seeding the credential brings the account's own connectors with it — ten of them here, Gmail and Drive and Notion among them.
        # They are constant across arms and so do not break attribution, but a planning task should not have data connectors it never had in the original run.
        "--strict-mcp-config",
        "-p", prompt,
    ]
    if plugin_dir is not None:
        command += ["--plugin-dir", str(plugin_dir)]
    if max_turns:
        # A backstop against a runaway loop, not a round limiter: a run that produced a plan took 135 assistant turns, so the ceiling is set far above any honest run.
        # It also cannot reach a subagent's own turns, so the real cost lever is the pinned model, not this.
        command += ["--max-turns", str(max_turns)]
    if not probe:
        # A real task writes files and dispatches lanes, which a headless run cannot stop to ask about.
        command += ["--permission-mode", "bypassPermissions"]
    if denied:
        # `bypassPermissions` approves every tool, so an allow-list is a no-op here and only a deny-list restricts anything; checked against a live session rather than assumed.
        # A case denies a tool when having it would let the arm settle the very fact the case is built around — `plan-evidence-gate` is the one, where the local `sqlite3` is not the bundled one the requirements ask about.
        command += ["--disallowedTools", *denied]

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


def arm_spec(name):
    """The built-in arms by name; a variant arm is injected and carries no invocation."""
    return ARMS.get(name, {"inject": True, "invoke": ""})


def resolve_arms(options, run_dir, model):
    """Build this run's arms, each with the plugin directory it launches under.

    Without `--variant` the arms are the built-in pair: the harness present, and the
    harness absent. With it, every arm carries the harness as it existed at some commit,
    and the comparison moves from "does the skill do anything" to "did this edit change
    what it does". The second question is the one a prompt revision has to answer, and
    nothing in the paired-arm shape had to change to ask it.
    """
    if not options.variant:
        plugin = prepare_plugin(run_dir / "plugin", model)
        return {
            name: {**spec, "plugin": plugin if spec["inject"] else None,
                   "role": "treatment" if spec["inject"] else "control"}
            for name, spec in ARMS.items()
            if not options.arm or name in options.arm
        }

    repo = run(["git", "rev-parse", "--show-toplevel"], cwd=KEIN_ROOT).stdout.decode().strip()
    arms = {}
    for spec in options.variant:
        name, _, ref = spec.partition("=")
        if not ref:
            raise SystemExit(f"ocs eval: --variant wants name=gitref, got {spec!r}")
        resolved = run(["git", "rev-parse", "--verify", f"{ref}^{{commit}}"], cwd=repo, check=False)
        if resolved.returncode != 0:
            raise SystemExit(f"ocs eval: --variant {name}: no such commit {ref!r} in {repo}")
        commit = resolved.stdout.decode().strip()
        checkout = run_dir / "refs" / name
        prepare_worktree(repo, commit, checkout)
        arms[name] = {
            "inject": True, "invoke": "", "ref": ref, "commit": commit,
            "role": "control" if not arms else "treatment",
            "plugin": prepare_plugin(run_dir / "plugins" / name, model, source=checkout / "plugin"),
        }
        print(f"[{name}] harness at {ref} ({commit[:12]})", file=sys.stderr)
    return arms


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


def lane_checks(record, arm):
    """Checks for lanes that ran as a separate process rather than as an Agent-tool subagent.

    A cross-vendor lane leaves nothing in the event stream, so every assertion here reads the trace
    the lane was required to write. That is also why `--trace` is mandatory in both lane references
    rather than merely recommended: without it there is no evidence the lane ran at all.

    Split out of `check_plumbing` so a live run can be verified with `--verify`. The eval harness
    builds a throwaway git worktree, which Orca does not know and Codex does not trust, so a
    write-capable lane cannot run inside it and has to be checked where it actually ran.
    """
    checks = []
    # A read-only cross-vendor lane runs only when the invocation asked for one; a native run has nothing here to assert.
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
        # A brief satisfies this by quoting the instructions or by naming the file that holds them.
        # The first observed run did the second — a digest of the conventions plus "also read .claude/CLAUDE.md" — and the lane is sandboxed with the worktree as its cwd, so the pointer resolves.
        # Requiring verbatim lines would have failed a brief that was better than the one the check imagined.
        instructions = binding_instruction_lines(record["path"])
        names = worktree_instruction_names(record["path"])
        briefed = [
            trace for trace in review_traces
            if any(line in trace["prompt"] for line in instructions)
            or any(name in trace["prompt"] for name in names)
        ]
        checks.append({
            "check": "the brief carried the instructions that bind here",
            "arm": arm,
            "pass": bool(review_traces) and (len(briefed) == len(review_traces) or not instructions),
            "detail": f"{len(briefed)}/{len(review_traces)} briefed against {len(instructions)} candidate lines" if instructions else "nothing binds here to carry",
        })
        # The lane's model must come from the role's tier, not from whatever the operator has set in their own Codex config.
        # This was invisible until an operator noticed the reported model matched their personal default, which it did by coincidence.
        pinned = [_argv_value(trace["command"], "-m") for trace in review_traces]
        checks.append({
            "check": "the lane pinned its tier's model rather than inheriting a default",
            "arm": arm,
            "pass": bool(pinned) and all(model for model in pinned),
            "detail": f"models={sorted(set(pinned))}" if any(pinned) else "no -m on the command line",
        })
        lanes = record.get("ralplan_lanes") or []
        checks.append({
            "check": "verdicts are keyed by lane, including the codex lane",
            "arm": arm,
            "pass": any(lane.startswith(("architect@codex", "critic@codex")) for lane in lanes),
            "detail": f"lanes={lanes}" if lanes else "no ralplan state written",
        })
    # A write-capable lane is gated on its traces rather than on the invocation, because `ocs team`
    # can be reached from more than one flag and an execute run that used one must be checked wherever it came from.
    for trace in record.get("team_traces") or []:
        label = f"{arm}:{trace['dir']}"
        # The single most regressible thing here. The role belongs in the launch, not in the task
        # spec, and putting it back in the spec would still produce a working worker — one that reads
        # its own identity as part of the job it was handed. Only the absence proves the layering held.
        checks.append({
            "check": "the role prompt reached the worker as a launch field, not as part of its task",
            "arm": label,
            "pass": "<Agent_Prompt>" in trace["role_prompt"] and "<Agent_Prompt>" not in trace["spec"],
            "detail": f"role.md={'yes' if '<Agent_Prompt>' in trace['role_prompt'] else 'NO'}, spec={'LEAKED' if '<Agent_Prompt>' in trace['spec'] else 'clean'}",
        })
        # An unrecognized Codex config field is ignored rather than refused, so a build that stopped
        # honouring this would run roleless workers and report nothing. `ocs team` pre-flights it; this
        # asserts the pre-flight's subject is still on the command that actually ran.
        checks.append({
            "check": "the launch carried the role through developer_instructions",
            "arm": label,
            "pass": "developer_instructions=" in trace["launch"],
            "detail": "present" if "developer_instructions=" in trace["launch"] else "absent from the launch",
        })
        # The home must travel with the worker, not merely with the trust pre-flight that resolved it.
        # It read correctly for a whole session while being inherited, because the tuned home is reached
        # through a shell function rather than an exported variable.
        launched = trace["launch"].startswith("CODEX_HOME=")
        home = trace["launch"].split(" ", 1)[0].partition("=")[2] if launched else ""
        checks.append({
            "check": "the worker's launch pinned the vanilla codex home",
            "arm": label,
            "pass": launched and home.endswith("/.codex"),
            "detail": f"launch home={home}" if launched else "CODEX_HOME recorded in the trace but absent from the launch",
        })
        model = _launch_value(trace["launch"], "-m")
        checks.append({
            "check": "the worker pinned its tier's model rather than inheriting a default",
            "arm": label,
            "pass": bool(model),
            "detail": f"model={model}" if model else "no -m on the launch",
        })
        # Measured 2026-08-06: a plain workspace-write worker can write files but cannot reach the Orca
        # app to report completion, and one without writable_roots cannot write its own ledger.
        # Both failures look like a worker that simply did not finish.
        sandbox = _launch_value(trace["launch"], "-s")
        reachable = "network_access=true" in trace["launch"]
        writable = "writable_roots=" in trace["launch"]
        checks.append({
            "check": "the sandbox let the worker both write and report completion",
            "arm": label,
            "pass": sandbox == "workspace-write" and reachable and writable,
            "detail": f"sandbox={sandbox or 'none'}, network={reachable}, writable_roots={writable}",
        })
        # The terminal is created by worktree selector while the sandbox roots are built from the caller's
        # cwd, so a mismatch would sandbox one directory and run the worker in another.
        checks.append({
            "check": "the worker ran in the worktree its sandbox describes",
            "arm": label,
            "pass": bool(trace["header"].get("cwd")) and f'"{trace["header"]["cwd"]}/.agents"' in trace["launch"],
            "detail": f"cwd={trace['header'].get('cwd') or 'unrecorded'}",
        })
        # `ocs team` assembles the role and nothing else, exactly as `ocs ask` does.
        # Nothing to carry is a pass rather than a failure, because the check would otherwise be asking for
        # something that does not exist — the same false negative the ask lane's version produced once, by
        # demanding verbatim lines from a brief that named the file instead.
        # "Nothing to carry" can also mean the check is looking in too few places: the first observed team run
        # passed that way while the lead had in fact carried the operator's standing conventions, which no file
        # in the worktree holds. See `binding_instruction_lines` for why widening it made the check worse.
        instructions = binding_instruction_lines(record["path"])
        briefed = any(line in trace["spec"] for line in instructions) or any(
            name in trace["spec"] for name in worktree_instruction_names(record["path"])
        )
        checks.append({
            "check": "the task package carried the instructions that bind here",
            "arm": label,
            "pass": briefed or not instructions,
            "detail": f"against {len(instructions)} candidate lines" if instructions else "nothing binds here to carry",
        })
        # This launch path cannot produce a hook transcript. The report is what was accepted in exchange,
        # so an empty one means the run bought control and paid for it with nothing.
        checks.append({
            "check": "the worker wrote the report that replaces its missing transcript",
            "arm": label,
            "pass": bool(trace["report"].strip()),
            "detail": f"{len(trace['report'])} bytes",
        })
    return checks


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
        expected_plugins = ["kein"] if arm_spec(arm)["inject"] else []
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
            "check": f"kein skills {'present' if arm_spec(arm)['inject'] else 'absent'}",
            "arm": arm,
            "pass": has_kein == bool(arm_spec(arm)["inject"]),
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
                "check": "the workflow dispatched its own lanes" if arm_spec(arm)['invoke'] else "no kein lane dispatched (control)",
                "arm": arm,
                "pass": bool(lanes) == bool(arm_spec(arm)["invoke"]),
                "detail": f"kein lanes={lanes}, all subagents={[d.get('agent') for d in dispatched]}",
            })
            # Dispatching into the background and then waiting is the known way for a lane's report to be lost.
            # Only the workflow promises to avoid it, so only the workflow can fail here; for the control this is an observation, and an interesting one, since a bare lead does the risky thing the rule exists to prevent.
            backgrounded = [d.get("agent") for d in dispatched if d.get("background") is not False]
            checks.append({
                "check": "no lane left to report through a background notification"
                         if arm_spec(arm)["invoke"] else "background dispatch by a lead with no such rule (observation)",
                "arm": arm,
                "pass": (not backgrounded) or not arm_spec(arm)["invoke"],
                "detail": f"backgrounded={backgrounded}" if backgrounded else "all synchronous",
            })
            checks += lane_checks(record, arm)
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


def run_case_mode(options, model, config_home_root):
    """Run a graded case: every arm, every replicate, then one label per assertion.

    The case prompt goes to both arms verbatim, and the harness prefixes nothing to either. Whether entry is pinned is the case's own decision, written into its prompt, and `--invoke` does not reach here.

    Both settings are worth measuring and conflating them would leave a null unattributable between routing and content, so a case picks one and says which. A case comparing two versions of the harness can pin, since both arms carry the skill; a case comparing presence against absence cannot, because a slash command reaching the arm without the plugin is an unexpanded string rather than a fair prompt. `plan-no-unknown` is the first, `plan-evidence-gate` the second, and each says so in its own file.
    """
    import cases as case_runner

    case_dir = resolve_case(options.case)

    case, graders = case_runner.load_case(case_dir)
    execution = case.get("execution") or {}
    prompt = execution.get("prompt")
    if not prompt:
        raise SystemExit(f"ocs eval: {case_dir}/case.yaml has no execution.prompt")
    replicates = options.runs or case.get("runs", 3)
    timeout = options.timeout if options.timeout != 1800 else execution.get("timeout_seconds", 1800)
    max_turns = options.max_turns if options.max_turns != 500 else execution.get("max_turns", 500)
    # Named for what it does. The field this replaces was `allowed_tools`, which is `claude plugin eval`'s
    # and which nothing here read, so every case ran with every tool while its own file said otherwise.
    denied = list(execution.get("denied_tools") or [])

    stamp = datetime.now().strftime("%y%m%d-%H%M%S")
    run_dir = state_dir("runs/eval") / f"{stamp}-case-{case['name']}"
    run_dir.mkdir(parents=True)
    arms = resolve_arms(options, run_dir, model)

    # A replicate is independent of every other one by construction — its own worktree, its
    # own event stream, its own artifacts — so the only thing forcing them into a queue was
    # a single shared config home. Each gets its own instead, which costs two small files
    # and a keychain read, and the wall clock becomes the slowest replicate rather than the
    # sum of all of them.
    jobs = [(arm, index) for arm in arms for index in range(replicates)]
    homes = {job: prepare_config_home(run_dir / "config-homes" / f"{job[0]}-{job[1]}") for job in jobs}

    def one(job):
        arm, index = job
        worktree = run_dir / "worktrees" / arm / str(index)
        case_runner.prepare_case_worktree(case_dir, worktree, run)
        events = run_dir / f"events-{arm}-{index}.jsonl"
        print(f"[{arm}] run {index + 1}/{replicates} started ({model})", file=sys.stderr)
        outcome = launch(arm, worktree, prompt, model, False, timeout, events,
                         homes[job], arms[arm]["plugin"], max_turns, denied)
        artifacts = run_dir / "artifacts" / arm / str(index)
        produced = collect(worktree, artifacts)
        with ThreadPoolExecutor(max_workers=len(graders)) as pool:
            results = pool.map(
                lambda g: (g["name"], case_runner.grade(g, artifacts, outcome, options.judge_model, run)),
                graders)
            graded = {name: {"passed": bool(passed), "detail": detail} for name, (passed, detail) in results}
        marks = "".join("." if graded[g["name"]]["passed"] else "x" for g in graders)
        print(f"[{arm}] run {index + 1}/{replicates} exit={outcome['exit_code']} {outcome['seconds']}s "
              f"{outcome['assistant_turns']} turns  graders {marks}", file=sys.stderr)
        if not options.keep:
            shutil.rmtree(worktree, ignore_errors=True)
        return job, {"run": outcome, "produced": produced, "graders": graded, "artifacts": str(artifacts)}

    try:
        records = {arm: [None] * replicates for arm, _ in jobs}
        with ThreadPoolExecutor(max_workers=max(1, options.jobs)) as pool:
            for (arm, index), record in pool.map(one, jobs):
                records[arm][index] = record

        roles = {spec.get("role", "treatment"): name for name, spec in arms.items()}
        text, tally = case_runner.report(case, graders, records, roles)
        (run_dir / "manifest.json").write_text(json.dumps({
            "case": case["name"], "case_dir": str(case_dir), "model": model,
            "judge_model": options.judge_model, "runs_per_arm": replicates, "jobs": options.jobs,
            "arms_spec": {a: {k: str(v) for k, v in spec.items()} for a, spec in arms.items()},
            "roles": {spec.get("role", "treatment"): name for name, spec in arms.items()},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "denied_tools": denied,
            "arms": records, "classification": tally,
        }, indent=2) + "\n")
        if not options.keep:
            prune_empty_dirs(run_dir)

        print(f"\nrun: {run_dir}")
        print(text)
        # Both arms' artifacts are kept whatever the outcome. A blind pairwise reading of
        # the two plans answers what a per-assertion grader cannot — whether the artifact
        # is better, rather than whether it carried the fields — and it needs them on disk.
        print(f"\nartifacts kept at {run_dir / 'artifacts'}")
        return 0 if tally.get(case_runner.DISCRIMINATES) else 1
    finally:
        for home in homes.values():
            discard_credentials(home)


def main():
    parser = argparse.ArgumentParser(prog="ocs eval")
    parser.add_argument("fixture", nargs="?", help="fixture name defined in .agents/kein/eval/fixtures.json")
    parser.add_argument("--case", help="run a graded case from the repository's evals/<name>/ (or a path) instead of a fixture: every arm, every replicate, one label per assertion")
    parser.add_argument("--runs", type=int, help="replicates per arm; overrides the case's own `runs`")
    parser.add_argument("--judge-model", default="verifier@codex", help="judge for `llm` graders, at whatever tier the role declares -- standard, for `verifier`. The fast tier was tried first, since a grader is one narrow pass/fail and there are many of them, and it is not usable here: on `gate-decides-both-paths` it hallucinated a missing PLAN.md that both higher tiers read, and passed a plan they agreed to fail. Standard and deep returned the same verdicts as each other. Takes the same specs --compare-judge does. Defaults to the Codex side because `~/.claude/CLAUDE.md` reaches every Claude agent, is not covered by the pinned config home, and broke a verdict here by being obeyed over the reply format; a harness that never reads it cannot be contaminated by it and cannot be forgotten about. haiku also answered the same artifact three different ways, one of them a hallucinated missing file, where the Codex role returned the same verdict three times.")
    parser.add_argument("--judge", action="store_true", help="with --self-test: also check the llm graders against the case's known-good and known-bad artifacts. Costs one judge call per grader per fixture, and catches a judge that fails its own criterion.")
    parser.add_argument("--self-test", action="store_true", help="with --case: prove the deterministic graders still detect their target, without launching an arm")
    parser.add_argument("--variant", action="append", metavar="NAME=GITREF", help="define an arm as the harness at a commit; repeatable. `--variant before=HEAD~1 --variant after=HEAD` compares two versions of a prompt instead of comparing presence against absence. Replaces the built-in arm pair for this run.")
    parser.add_argument("--jobs", type=int, default=3, help="replicates to run concurrently with --case. Each gets its own worktree and config home, so the ceiling is the account's tolerance for concurrent sessions rather than anything in the harness.")
    parser.add_argument("--reclassify", metavar="RUN_DIR", help="re-read a finished case run's stored grader results under the current classifier, without launching anything. The labels are a reading of the data, so they change when the reading does.")
    parser.add_argument("--compare-runs", type=int, default=2, help="times to repeat the whole comparison. A single run of a pairwise judge is one draw: the first comparison here returned 3-0 and the second, on identical input, contradicted it. Order control does not cover run-to-run variance.")
    parser.add_argument("--compare-judge", action="append", metavar="JUDGE", help="judge for --rank and --compare; repeatable. Defaults to the three Codex role lenses pinned to the deep tier, because the ranking sums Borda points across judges and equal weight in a sum is a claim of equal capability. Pass your own and keep them on one tier, or read the per-judge orders the report prints instead of the aggregate. A Claude model name, or `codex` / `codex:<model>`. Two vendors share the task but not their error correlations, so their agreement is the control on a judge simply preferring the longer document. Defaults to --judge-model.")
    parser.add_argument("--compare", metavar="RUN_DIR", help="read the two arms' artifacts from a finished case run as a blind pairwise choice, which answers whether the plan is better rather than whether it carried the fields")
    parser.add_argument("--regrade-all", action="store_true", help="with --regrade: re-ask every `llm` verdict, not only the ones that were never reached. For when the grader files changed and the stored verdicts answer a question no grader asks any more. It does replace results that were honestly obtained, which is why it is not the default.")
    parser.add_argument("--regrade", metavar="RUN_DIR", help="re-ask only the graders whose verdict was never reached, against artifacts already on disk. A judge stopped by a rate limit records `unreadable verdict`, which counts as a failure and is not one; this repairs those and leaves every honestly-obtained verdict alone.")
    parser.add_argument("--rank", metavar="RUN_DIR", help="the same question as --compare, asked of the whole field at once. Pairs grow as the square of the plans -- six an arm is 66 pairs, 396 calls at three judges and two orders -- so past about four a side this is the one to reach for: one call per judge per presentation order, and the judge still compares rather than scoring a plan alone.")
    parser.add_argument("--rank-orders", type=int, default=3, help="presentation orders for --rank. These do for a list what judging both orders did for a pair: a judge handed a list has a position preference, and re-dealing the same field is what separates it from a reading.")
    parser.add_argument("--verify", metavar="WORKTREE", help="check the lane traces already in a worktree instead of running a fixture. A write-capable lane cannot run inside a throwaway eval worktree, so this is how one is checked where it actually ran.")
    parser.add_argument("--probe", action="store_true", help="ask each arm what reached it instead of running the task")
    parser.add_argument("--timeout", type=int, default=1800, help="per-arm timeout in seconds")
    parser.add_argument("--keep", action="store_true", help="leave worktrees on disk for inspection")
    parser.add_argument("--arm", action="append", choices=sorted(ARMS), help="run only these arms; repeatable. A conformance run needs one arm, not a comparison.")
    parser.add_argument("--invoke", help="override the injected arm's invocation, e.g. '/kein:ralplan --critic claude,codex '. The trailing space matters.")
    parser.add_argument("--max-turns", type=int, default=500, help="runaway backstop for the lead; not a round limiter")
    options = parser.parse_args()

    if options.verify:
        target = Path(options.verify).resolve()
        if not target.is_dir():
            raise SystemExit(f"ocs eval: {target} is not a directory")
        # A worktree accumulates every lane it has ever run, and a trace written before a fix stays wrong
        # forever, so checking the whole worktree reports history rather than the state of the build.
        # Pointing at one trace directory is how a single run is gated; pointing at the worktree is how the history is read.
        # A trace lives at <worktree>/.agents/kein/runs/<kind>/<stamp>-<role>, so the worktree is four levels up.
        single = (target / "command.txt").is_file()
        worktree = target.parents[4] if single else target
        traces = {"ask_traces": ask_traces(worktree), "team_traces": team_traces(worktree)}
        if single:
            for kind in traces:
                traces[kind] = [trace for trace in traces[kind] if trace["dir"] == target.name]
        # The ask checks are gated on the invocation because a run's own transcript is what says a vendor
        # lane was asked for. Verifying after the fact there is no such transcript, so presence stands in.
        record = {
            "path": str(worktree),
            "invoke": "codex" if traces["ask_traces"] else "",
            "ralplan_lanes": ralplan_lanes(worktree),
            **traces,
        }
        checks = lane_checks(record, worktree.name)
        if not checks:
            raise SystemExit(f"ocs eval: no lane traces under {worktree}/.agents/kein/runs. A lane must be run with --trace to be checkable.")
        failed = sum(not check["pass"] for check in checks)
        for check in checks:
            print(f"  {'ok  ' if check['pass'] else 'FAIL'} [{check['arm']}] {check['check']} — {check['detail']}")
        print(f"\n{len(checks) - failed}/{len(checks)} checks passed")
        raise SystemExit(1 if failed else 0)

    if options.reclassify:
        import cases as case_runner
        target = Path(options.reclassify)
        manifest = json.loads((target / "manifest.json").read_text())
        case, graders = case_runner.load_case(manifest["case_dir"])
        text, tally = case_runner.report(case, graders, manifest["arms"], manifest.get("roles"))
        print(text)
        return 0 if (tally.get(case_runner.DISCRIMINATES) or tally.get(case_runner.STRENGTHENS)) else 1

    if options.regrade:
        # A judge that could not answer is not a grader that answered no. When the account's
        # session limit landed mid-run, six llm graders on two replicates came back
        # "unreadable verdict: You've hit your session limit", and both plans were complete
        # and on disk. Without this the whole run is thrown away to re-earn verdicts on
        # artifacts that never changed.
        import cases as case_runner
        target = Path(options.regrade)
        manifest = json.loads((target / "manifest.json").read_text())
        _, graders = case_runner.load_case(manifest["case_dir"])
        by_name = {g["name"]: g for g in graders}
        redone = 0
        for arm, records in manifest["arms"].items():
            for index, record in enumerate(records):
                for name, result in (record or {}).get("graders", {}).items():
                    detail = str(result.get("detail") or "")
                    # Only verdicts that were never reached. Re-rolling a verdict that was
                    # honestly obtained would quietly replace a result with a fresh sample.
                    # --regrade-all lifts that, and is for one situation: the grader files
                    # themselves changed, so the stored verdicts answer a question no
                    # grader asks any more. Every llm verdict is then re-asked and the run
                    # is a reading under the current graders, which is what --reclassify is
                    # for the classifier one level up.
                    if not options.regrade_all and (
                            result.get("passed") or not detail.startswith("unreadable verdict")):
                        continue
                    if options.regrade_all and by_name[name].get("type") != "llm":
                        continue
                    passed, why = case_runner.grade(
                        by_name[name], Path(record["artifacts"]), record["run"],
                        options.judge_model, run)
                    record["graders"][name] = {"passed": bool(passed), "detail": why}
                    redone += 1
                    print(f"  [{arm}/{index}] {name}: {'pass' if passed else 'fail'}", file=sys.stderr)
        if not redone:
            print("no unreached verdicts to regrade")
            return 0
        case, graders = case_runner.load_case(manifest["case_dir"])
        text, tally = case_runner.report(case, graders, manifest["arms"], manifest.get("roles"))
        manifest["classification"] = tally
        (target / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        print(f"\nregraded {redone} verdict(s)\n")
        print(text)
        return 0

    if options.rank:
        import cases as case_runner
        target = Path(options.rank)
        manifest = json.loads((target / "manifest.json").read_text())
        judges = options.compare_judge or RANK_JUDGES
        text, _ = case_runner.rank(target, manifest["case_dir"], judges, run,
                                   options.rank_orders, manifest.get("roles"))
        print(text)
        return 0

    if options.compare:
        import cases as case_runner
        target = Path(options.compare)
        manifest = json.loads((target / "manifest.json").read_text())
        judges = options.compare_judge or [options.judge_model]
        text, tally = case_runner.compare(target, manifest["case_dir"], judges, run,
                                          options.compare_runs, manifest.get("roles"))
        print(text)
        return 0

    if options.case:
        if options.self_test:
            import cases as case_runner
            return case_runner.self_test(resolve_case(options.case), run, options.judge_model if options.judge else None)
        config, _ = load_config()
        return run_case_mode(options, config.get("models", {}).get("arm", "sonnet"), None)

    if not options.fixture:
        raise SystemExit("ocs eval: a fixture name is required unless --case or --verify is given")

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
    arms = resolve_arms(options, run_dir, model)

    try:
        records = {}

        for arm in arms:
            # The control arm receives the same task text without the invocation, so the only thing that differs is whether the workflow is entered.
            # Leaving the invocation out of both would measure whether the model reaches for the skill unprompted, which is a different question than whether the skill's process changes the result.
            invoke = arms[arm]["invoke"]
            if options.invoke is not None and arms[arm]["inject"]:
                invoke = options.invoke
            prompt = PROBE_PROMPT if options.probe else invoke + fixture["task"]
            worktree = run_dir / "worktrees" / arm
            print(f"[{arm}] preparing worktree at {fixture['commit'][:12]}", file=sys.stderr)
            wt = prepare_worktree(fixture["repo"], fixture["commit"], worktree)
            sanitized, touched = sanitize(worktree, contamination)
            loaded = plugin_status(worktree)
            print(f"[{arm}] launching ({model}, {'probe' if options.probe else 'task'})", file=sys.stderr)
            events = run_dir / f"events-{arm}.jsonl"
            outcome = launch(arm, worktree, prompt, model, options.probe, options.timeout, events, config_home, arms[arm]["plugin"], options.max_turns)
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
                "team_traces": team_traces(worktree),
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
