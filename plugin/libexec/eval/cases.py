#!/usr/bin/env python3
"""Run a graded eval case against both arms and classify each assertion.

`run.py` answers whether the plumbing held. This answers whether the skill changed the
outcome, which needs three things it does not have: expectations graded per run, more
than one run per arm, and a reading of each assertion across arms.

The case format is `claude plugin eval`'s — `case.yaml`, a `fixture/` directory, and one
grader per file under `graders/`. That command is gated behind early access on this
account, so this module exists to run the same files now. Anything it adds beyond that
format is a bug, not a feature: the point of borrowing the format is that a case outlives
whichever runner reaches it.

Every grader judges a produced file or a recorded tool call. A grader that reads the
assistant's reply passes a run that described the work without doing it, which
`trailofbits/skills` records as having been green for months.

The classification is the output that matters. An assertion passing in both arms is not a
pass — it is evidence that that part of the skill is doing nothing, which is the deletion
evidence `docs/prompt-revision.md` says nobody collects.
"""

import json
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path

import yaml

# Read across arms, per assertion. The first is the finding; the second is the deletion
# evidence; the rest say the instrument or the expectation needs work before either.
DISCRIMINATES = "discriminates"        # passes with the skill, fails without it
INERT = "inert"                        # passes in both arms: this instruction does nothing here
HARMFUL = "harmful"                    # passes without the skill, fails with it
UNREACHED = "unreached"                # fails in both arms: too hard, or the assertion is wrong
FLAKY = "flaky"                        # inconsistent inside at least one arm


def load_case(directory):
    directory = Path(directory)
    case = yaml.safe_load((directory / "case.yaml").read_text())
    graders = []
    for path in sorted((directory / "graders").glob("*.md")):
        text = path.read_text()
        match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", text, re.S)
        if not match:
            raise SystemExit(f"ocs eval: grader has no frontmatter: {path}")
        meta = yaml.safe_load(match.group(1)) or {}
        meta["name"] = path.stem
        meta["body"] = match.group(2).strip()
        graders.append(meta)
    if not graders:
        raise SystemExit(f"ocs eval: no graders under {directory / 'graders'}")
    return case, graders


def prepare_case_worktree(case_dir, destination, run_cmd):
    """A self-contained case has no upstream repository, so it gets a fresh one.

    The fixture is committed before the arm starts. That is what makes `git status`
    afterwards a list of exactly what the arm produced, which is how `collect` in run.py
    already reads a worktree — this keeps the two paths reading the same signal.
    """
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copytree(case_dir / "fixture", destination / "fixture", dirs_exist_ok=True)
    run_cmd(["git", "init", "--quiet", "--initial-branch", "eval"], cwd=destination)
    run_cmd(["git", "add", "-A"], cwd=destination)
    run_cmd(["git", "-c", "user.email=eval@kein", "-c", "user.name=eval",
             "commit", "--quiet", "-m", "fixture"], cwd=destination)
    return destination


def _artifact(artifacts, relative):
    candidate = Path(artifacts) / relative
    return candidate if candidate.is_file() else None


def _judge(grader, artifacts, record, model, run_cmd):
    """An LLM grader reads the artifact, never the reply.

    The verdict has to be one token because anything a judge can hedge in, it will.
    """
    path = grader.get("path") or grader.get("target", {}).get("path") or _default_artifact(grader)
    content = None
    if path:
        found = _artifact(artifacts, path)
        if found is None:
            return False, f"{path} was not produced"
        content = found.read_text(errors="replace")

    prompt = (
        "You are grading one artifact against one criterion. Apply the criterion exactly as written; "
        "do not add requirements it does not state, and do not withhold a pass for a shortcoming it "
        "does not name.\n\n"
        "=== CRITERION ===\n" + grader["body"] + "\n\n"
    )
    if content is not None:
        prompt += f"=== ARTIFACT ({path}) ===\n{content}\n\n"
    else:
        prompt += (
            "=== FILES THE RUN PRODUCED ===\n"
            + "\n".join(sorted(str(p.relative_to(artifacts)) for p in Path(artifacts).rglob("*") if p.is_file()))
            + "\n\n=== FILES THE RUN WROTE, FROM ITS TOOL CALLS ===\n"
            + "\n".join(record.get("files_written") or ["(none)"]) + "\n\n"
        )
    prompt += "Reply with exactly one word: PASS or FAIL. Nothing else."

    out = run_cmd(["claude", "--model", model, "--strict-mcp-config", "-p", prompt],
                  check=False).stdout.decode("utf-8", "replace").strip()
    verdict = out.upper().split()[0] if out.split() else ""
    if verdict.startswith("PASS"):
        return True, out[:200]
    if verdict.startswith("FAIL"):
        return False, out[:200]
    return False, f"unreadable verdict: {out[:200]}"


def _default_artifact(grader):
    """A criterion that judges the whole run names no path; one that judges a file does."""
    return None


def grade(grader, artifacts, record, judge_model, run_cmd):
    kind = grader.get("type")
    if kind == "file_exists":
        found = _artifact(artifacts, grader["path"]) is not None
        want = grader.get("exists", True)
        return found == want, f"{grader['path']} {'exists' if found else 'missing'}"

    if kind == "regex":
        target = grader.get("target") or {}
        if target.get("source") != "file":
            return False, f"unsupported regex target: {target.get('source')!r}"
        found = _artifact(artifacts, target["path"])
        if found is None:
            return False, f"{target['path']} was not produced"
        flags = 0
        for letter in grader.get("flags", ""):
            flags |= {"i": re.I, "m": re.M, "s": re.S}.get(letter, 0)
        hit = re.search(grader["body"], found.read_text(errors="replace"), flags)
        return hit is not None, ("matched" if hit else "no match")

    if kind == "tool_used":
        tool = grader["tool"]
        if tool in ("Skill",):
            used = record.get("skills_invoked") or []
        elif tool in ("Agent", "Task"):
            used = record.get("subagents_dispatched") or []
        elif tool in ("Write", "Edit", "NotebookEdit"):
            used = record.get("files_written") or []
        else:
            return False, f"unsupported tool for tool_used: {tool}"
        return len(used) >= grader.get("min", 1), f"{len(used)} {tool} call(s)"

    if kind == "llm":
        return _judge(grader, artifacts, record, judge_model, run_cmd)

    return False, f"unknown grader type: {kind!r}"


def classify(per_arm):
    """One label per assertion, from its pass pattern across arms and replicates."""
    consistent = {}
    for arm, results in per_arm.items():
        values = set(results)
        if len(values) != 1:
            return FLAKY, {arm: Counter(results) for arm in per_arm}
        consistent[arm] = values.pop()
    treatment = consistent.get("with-skill")
    control = consistent.get("without-skill")
    if treatment and not control:
        return DISCRIMINATES, consistent
    if treatment and control:
        return INERT, consistent
    if control and not treatment:
        return HARMFUL, consistent
    return UNREACHED, consistent


JUDGE = (
    "Two implementation plans were written from the same requirements document, by different processes. "
    "You are choosing which one better serves the person who has to build from it.\n\n"
    "Judge only against the requirements document below. Do not reward a plan for structure, for headings, "
    "for length, or for confident tone; a plan that carries a section is not thereby better than one that "
    "does the same work in prose. What matters is whether someone could execute it without having to make "
    "a decision the plan should have made for them.\n\n"
    "Pay particular attention to what each plan does with a fact the requirements say nobody has established "
    "yet. Naming it is easy. Deciding, now, what happens under each of its possible answers is the thing "
    "that costs something.\n\n"
    "=== REQUIREMENTS ===\n{requirements}\n\n"
    "=== PLAN A ===\n{a}\n\n=== PLAN B ===\n{b}\n\n"
    "Reply with exactly two lines and nothing else:\n"
    "WINNER: A or B or TIE\n"
    "WHY: one sentence naming the specific difference that decided it."
)


def compare(run_dir, case_dir, model, run_cmd):
    """Blind pairwise reading of the two arms' artifacts.

    A per-assertion grader answers whether a plan carried a field. It cannot answer whether
    the plan is better, and that is the question a skill exists to move. This asks a
    stronger model directly, against a fixed reference, as a forced choice — so the reading
    is scoreable rather than an essay — and runs every pair in both orders, because a judge
    handed two documents has a position preference that would otherwise be read as a result.

    Arm labels never reach the judge. That is the whole point: told which plan came from the
    skill, a judge grades the label.
    """
    run_dir, case_dir = Path(run_dir), Path(case_dir)
    requirements = "\n\n".join(
        p.read_text(errors="replace") for p in sorted((case_dir / "fixture").rglob("*.md"))
    )

    def artifacts(arm):
        root = run_dir / "artifacts" / arm
        out = []
        for replicate in sorted(root.iterdir()) if root.is_dir() else []:
            files = sorted(p for p in replicate.rglob("*") if p.is_file() and p.suffix == ".md")
            files = [p for p in files if not p.is_relative_to(replicate / "fixture")]
            if files:
                out.append((replicate.name, "\n\n".join(p.read_text(errors="replace") for p in files)))
        return out

    treatment, control = artifacts("with-skill"), artifacts("without-skill")
    if not treatment or not control:
        raise SystemExit(f"ocs eval: need artifacts from both arms under {run_dir / 'artifacts'}")

    tally = Counter()
    reasons = []
    for index in range(min(len(treatment), len(control))):
        t_name, t_text = treatment[index]
        c_name, c_text = control[index]
        # Both orders. A judge that answers "A" to both is expressing a position preference,
        # not a verdict, and that pair is recorded as a tie rather than as one win each.
        verdicts = []
        for first, second, treatment_is in ((t_text, c_text, "A"), (c_text, t_text, "B")):
            out = run_cmd(["claude", "--model", model, "--strict-mcp-config", "-p",
                           JUDGE.format(requirements=requirements, a=first, b=second)],
                          check=False).stdout.decode("utf-8", "replace")
            winner = re.search(r"^WINNER:\s*(A|B|TIE)", out, re.M | re.I)
            why = re.search(r"^WHY:\s*(.+)$", out, re.M | re.I)
            choice = (winner.group(1).upper() if winner else "TIE")
            verdicts.append(("with-skill" if choice == treatment_is else
                             "tie" if choice == "TIE" else "without-skill"))
            reasons.append((f"{t_name}v{c_name}", verdicts[-1], (why.group(1).strip() if why else "")[:220]))
        result = verdicts[0] if verdicts[0] == verdicts[1] else "tie"
        tally[result] += 1

    lines = [f"blind pairwise, {model} judge, both orders per pair:"]
    for arm in ("with-skill", "without-skill", "tie"):
        lines.append(f"  {arm:15} {tally[arm]}")
    lines.append("")
    lines.append("  reasons given (one per judged order):")
    for pair, winner, why in reasons:
        lines.append(f"    {pair}  {winner:14} {why}")
    if tally["with-skill"] == tally["without-skill"]:
        lines.append("\n  No preference. Read this beside the assertion classification: if the graders "
                     "separated the arms and this did not, the skill moved the form and not the plan.")
    return "\n".join(lines), dict(tally)


def self_test(case_dir, run_cmd):
    """Prove the deterministic graders still detect their target before spending a run on them.

    Three assertions, and the count of them is itself asserted, because a self-test that
    silently ran nothing would be the exact failure it exists to catch: a checker that
    inspects zero items and reports success.

    `llm` graders are out of scope here — checking them costs a judge call each and their
    behaviour is not deterministic, so what this establishes is that everything which
    *can* be settled without a model is settled correctly.
    """
    case, graders = load_case(case_dir)
    free = [g for g in graders if g.get("type") != "llm"]
    if not free:
        raise SystemExit(f"ocs eval: {case['name']} has no deterministic grader to self-test")

    checks, failures = 0, []

    def probe(artifacts, record):
        return {g["name"]: grade(g, artifacts, record, None, run_cmd)[0] for g in free}

    # 1. Every file-judging grader fails when the run produced nothing. A grader that
    #    passes an absent artifact makes a skipped run look like a successful one.
    empty = Path(case_dir) / "selftest" / ".empty"
    empty.mkdir(parents=True, exist_ok=True)
    for name, passed in probe(empty, {"skills_invoked": [], "files_written": []}).items():
        checks += 1
        if passed:
            failures.append(f"{name} passed against an empty artifact directory")
    empty.rmdir()

    # 2. The known-good and known-bad artifacts, when the case supplies them.
    for expectation, directory in (("pass", "should-pass"), ("fail", "should-fail")):
        root = Path(case_dir) / "selftest" / directory
        if not root.is_dir():
            continue
        record_path = root / "_record.json"
        record = json.loads(record_path.read_text()) if record_path.is_file() else {}
        results = probe(root, record)
        checks += len(results)
        if expectation == "pass":
            failures += [f"{n} failed against the known-good artifact" for n, ok in results.items() if not ok]
        elif all(results.values()):
            failures.append("every grader passed the known-bad artifact, so none of them discriminates")

    # 3. The classification, which is where a per-assertion result becomes a finding.
    for per_arm, want in (
        ({"with-skill": [True] * 3, "without-skill": [False] * 3}, DISCRIMINATES),
        ({"with-skill": [True] * 3, "without-skill": [True] * 3}, INERT),
        ({"with-skill": [False] * 3, "without-skill": [True] * 3}, HARMFUL),
        ({"with-skill": [False] * 3, "without-skill": [False] * 3}, UNREACHED),
        ({"with-skill": [True, False, True], "without-skill": [False] * 3}, FLAKY),
    ):
        checks += 1
        got, _ = classify(per_arm)
        if got != want:
            failures.append(f"classify returned {got} where {want} was expected")

    minimum = len(free) + 5
    if checks < minimum:
        failures.append(f"self-test ran {checks} assertions, fewer than the {minimum} it must run")

    for line in failures:
        print(f"  FAIL {line}")
    print(f"\n{checks - len(failures)}/{checks} self-test assertions passed"
          f" ({len(free)} deterministic grader(s), {len(graders) - len(free)} llm grader(s) not covered)")
    return 1 if failures else 0


def report(case, graders, records):
    """`records` is {arm: [ {grader_name: bool} per replicate ]}."""
    lines = [f"case: {case['name']}  ({case.get('runs', 1)} run(s) per arm)"]
    tally = Counter()
    rows = []
    for grader in graders:
        name = grader["name"]
        per_arm = {arm: [r["graders"][name]["passed"] for r in runs] for arm, runs in records.items()}
        label, detail = classify(per_arm)
        tally[label] += 1
        scores = "  ".join(
            f"{arm}={sum(v for v in vals)}/{len(vals)}" for arm, vals in sorted(per_arm.items())
        )
        rows.append((label, name, grader.get("type"), grader.get("weight", 1), scores))

    width = max(len(r[1]) for r in rows)
    for label, name, kind, weight, scores in sorted(rows, key=lambda r: (r[0] != DISCRIMINATES, r[1])):
        lines.append(f"  {label:14} {name:{width}}  {kind:11} w{weight}  {scores}")

    lines.append("")
    if not tally[DISCRIMINATES]:
        lines.append(
            "  No assertion discriminated. Report this as an insensitive instrument or an insensitive\n"
            "  expectation set, not as a successful measurement."
        )
    if tally[INERT]:
        lines.append(
            f"  {tally[INERT]} assertion(s) passed in both arms. That part of the skill is doing nothing here,\n"
            "  which is deletion evidence rather than a pass."
        )
    if tally[FLAKY]:
        lines.append(f"  {tally[FLAKY]} assertion(s) were inconsistent within an arm; more replicates before reading them.")
    return "\n".join(lines), dict(tally)
