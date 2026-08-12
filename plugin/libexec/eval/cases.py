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
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

# Read across arms, per assertion. The first is the finding; the second is the deletion
# evidence; the rest say the instrument or the expectation needs work before either.
DISCRIMINATES = "discriminates"        # every run with the skill, no run without it
STRENGTHENS = "strengthens"            # every run with the skill, some runs without it
INERT = "inert"                        # every run in both arms: this instruction does nothing here
HARMFUL = "harmful"                    # no run with the skill, at least one without it
UNREACHED = "unreached"                # no run in either arm: too hard, or the assertion is wrong
UNRELIABLE = "unreliable"              # the arm carrying the skill did it only sometimes


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
    path = grader.get("path") or grader.get("target", {}).get("path")
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
        produced = _produced(artifacts)
        if not produced.strip():
            return False, "the run produced no readable artifact to judge"
        prompt += ("=== WHAT THE RUN PRODUCED ===\n" + produced + "\n\n"
                   "=== FILES THE RUN WROTE, FROM ITS TOOL CALLS ===\n"
                   + "\n".join(record.get("files_written") or ["(none)"]) + "\n\n")
    prompt += "Reply with exactly one word: PASS or FAIL. Nothing else."

    out = run_cmd(["claude", "--model", model, "--strict-mcp-config", "-p", prompt],
                  check=False).stdout.decode("utf-8", "replace").strip()
    verdict = out.upper().split()[0] if out.split() else ""
    if verdict.startswith("PASS"):
        return True, out[:200]
    if verdict.startswith("FAIL"):
        return False, out[:200]
    return False, f"unreadable verdict: {out[:200]}"


PRODUCED_LIMIT = 40000


def _produced(artifacts):
    """Every text file the run produced, smallest name first, as one block.

    A criterion that names no path still has to be judged against something, and the
    something is the work product. Handing the judge a directory listing instead is how
    every llm verdict in this instrument was reached until 2026-08-12: the graders say
    "judge PLAN.md", the prompt showed them a list of filenames, and the verdicts were
    guesses that happened to look like judgements.
    """
    out, budget = [], PRODUCED_LIMIT
    for path in sorted(Path(artifacts).rglob("*")):
        if not path.is_file() or path.suffix not in (".md", ".txt", ".json", ".yaml", ".yml"):
            continue
        text = path.read_text(errors="replace")[:budget]
        budget -= len(text)
        out.append(f"--- {path.relative_to(artifacts)}\n{text}")
        if budget <= 0:
            break
    return "\n\n".join(out)


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


def classify(per_arm, roles=None):
    """One label per assertion, from its pass pattern across arms and replicates.

    Inconsistency is read asymmetrically, and deliberately. An inconsistent *treatment*
    arm means the skill does not reliably produce the behaviour, which is a defect in the
    skill or in the assertion. An inconsistent *control* arm is not a defect at all — it
    is the measurement, because a baseline that produces the behaviour one run in three is
    exactly what a skill that produces it three in three is worth. Collapsing both into one
    "flaky" label hid the most informative cell in the first real run of this instrument.
    """
    roles = roles or {"treatment": "with-skill", "control": "without-skill"}
    rates = {arm: (sum(results), len(results)) for arm, results in per_arm.items()}
    passed, total = rates.get(roles["treatment"], (0, 0))
    treatment = passed / total if total else 0.0
    passed, total = rates.get(roles["control"], (0, 0))
    control = passed / total if total else 0.0
    detail = {arm: f"{p}/{n}" for arm, (p, n) in rates.items()}

    if 0 < treatment < 1:
        return UNRELIABLE, detail
    if treatment == 1:
        if control == 0:
            return DISCRIMINATES, detail
        if control < 1:
            return STRENGTHENS, detail
        return INERT, detail
    return (HARMFUL if control > 0 else UNREACHED), detail


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


CODEX_SCHEMA = {
    "type": "object",
    "properties": {"winner": {"type": "string", "enum": ["A", "B", "TIE"]}, "why": {"type": "string"}},
    "required": ["winner", "why"],
    "additionalProperties": False,
}


def _ask_judge(spec, prompt, run_cmd, scratch):
    """One judge, one verdict. `spec` is a Claude model, or `codex` / `codex:<model>`.

    A second vendor is not redundancy here. The skill's plans run about two and a half
    times the length of the control's, and a judge that prefers the longer document would
    produce this result without reading either. Two vendors share the task but not their
    error correlations, so agreement between them is the cheapest available control on
    that, and disagreement is itself the finding.
    """
    if spec.endswith("@codex"):
        role = spec[: -len("@codex")]
        out = run_cmd([str(Path(__import__("os").environ["KEIN_ROOT"]) / "libexec" / "ocs-ask"),
                       "codex", "--agent", role, "--model", "gpt-5.6-sol", "--effort", "medium", prompt],
                      check=False).stdout.decode("utf-8", "replace")
        winner = re.search(r"^WINNER:\s*(A|B|TIE)", out, re.M | re.I)
        why = re.search(r"^WHY:\s*(.+)$", out, re.M | re.I)
        return (winner.group(1).upper() if winner else "TIE"), (why.group(1).strip() if why else "")

    if spec.startswith("codex"):
        schema = scratch / "judge-schema.json"
        schema.write_text(json.dumps(CODEX_SCHEMA))
        command = ["codex", "exec", "--sandbox", "read-only", "--skip-git-repo-check",
                   "--ephemeral", "--output-schema", str(schema)]
        _, _, chosen = spec.partition(":")
        if chosen:
            command += ["-m", chosen]
        result = run_cmd(command + [prompt], check=False).stdout.decode("utf-8", "replace")
        # codex prints its hook and token lines around the answer, so the last JSON object wins.
        objects = re.findall(r'\{[^{}]*"winner"[^{}]*\}', result)
        if not objects:
            return "TIE", "unreadable codex output"
        parsed = json.loads(objects[-1])
        return parsed.get("winner", "TIE").upper(), parsed.get("why", "")

    out = run_cmd(["claude", "--model", spec, "--strict-mcp-config", "-p", prompt],
                  check=False).stdout.decode("utf-8", "replace")
    winner = re.search(r"^WINNER:\s*(A|B|TIE)", out, re.M | re.I)
    why = re.search(r"^WHY:\s*(.+)$", out, re.M | re.I)
    return (winner.group(1).upper() if winner else "TIE"), (why.group(1).strip() if why else "")


def compare(run_dir, case_dir, judges, run_cmd, repeats=2, roles=None):
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

    named = roles or {"treatment": "with-skill", "control": "without-skill"}
    treatment, control = artifacts(named["treatment"]), artifacts(named["control"])
    if not treatment or not control:
        raise SystemExit(
            f"ocs eval: need artifacts from both arms under {run_dir / 'artifacts'}; "
            f"looked for {named['treatment']!r} and {named['control']!r}")

    scratch = Path(run_dir) / "compare"
    scratch.mkdir(exist_ok=True)

    # Replicate index carries no correspondence between arms - run 0 of one is not the
    # partner of run 0 of the other - so pairing by index both invented a relationship and
    # threw away two thirds of the available comparisons. Every cross-arm pair is judged.
    #
    # The within-arm pairs are the control. If a judge separates two plans from the same
    # arm as readily as it separates plans from different arms, the arm is not the variable
    # and a cross-arm win rate means nothing.
    pairs = [("cross", i, j) for i in range(len(treatment)) for j in range(len(control))]
    pairs += [("within-treatment", i, j) for i in range(len(treatment)) for j in range(i + 1, len(treatment))]
    pairs += [("within-control", i, j) for i in range(len(control)) for j in range(i + 1, len(control))]

    def texts(kind, i, j):
        if kind == "within-treatment":
            return treatment[i][1], treatment[j][1]
        if kind == "within-control":
            return control[i][1], control[j][1]
        return treatment[i][1], control[j][1]

    calls = [(judge, pair, order, repeat)
             for judge in judges for pair in pairs
             for order in ("treatment-first", "control-first") for repeat in range(repeats)]

    def one(call):
        judge, pair, order, repeat = call
        kind, i, j = pair
        t_text, c_text = texts(kind, i, j)
        first, second, treatment_is = ((t_text, c_text, "A") if order == "treatment-first"
                                       else (c_text, t_text, "B"))
        choice, why = _ask_judge(judge, JUDGE.format(requirements=requirements, a=first, b=second),
                                 run_cmd, scratch)
        if kind == "cross":
            winner = (named["treatment"] if choice == treatment_is else
                      "tie" if choice == "TIE" else named["control"])
        else:
            # Within an arm there is no arm to win; what is recorded is whether the judge
            # expressed any preference between two plans the same prompt produced.
            winner = "tie" if choice == "TIE" else "decided"
        return call, winner, why

    with ThreadPoolExecutor(max_workers=min(8, len(calls))) as pool:
        verdicts = list(pool.map(one, calls))

    by_judge, reasons, per_pair = {}, [], {}
    for (judge, pair, order, repeat), winner, why in verdicts:
        per_pair.setdefault((judge, pair), {}).setdefault(order, []).append(winner)
        reasons.append((judge, pair, f"{order}#{repeat}", winner, why[:200]))

    def verdict(judge, pair):
        """One judge's reading of one pair, after both orders and every repeat.

        Anything short of unanimity is a tie: a judge that names the same position in both
        orders is stating a position preference, and one that changes its mind between
        identical calls has not stated a preference at all.
        """
        orders = per_pair.get((judge, pair), {})
        seen = {w for winners in orders.values() for w in winners}
        return seen.pop() if len(seen) == 1 else "tie"

    cross = [p for p in pairs if p[0] == "cross"]
    within = [p for p in pairs if p[0] != "cross"]
    for judge in judges:
        by_judge[judge] = Counter(verdict(judge, p) for p in cross)

    lines = [f"blind pairwise over every cross-arm pair ({len(cross)}), both orders "
             f"x{repeats} repeat(s), arm labels withheld from every judge:"]
    for judge, tally in by_judge.items():
        lines.append(f"  {judge:24} {named['treatment']}={tally[named['treatment']]}  "
                     f"{named['control']}={tally[named['control']]}  tie={tally['tie']}")

    if within:
        lines.append("")
        lines.append(f"  control - the same judges on {len(within)} pairs drawn from inside one arm, where")
        lines.append("  there is no arm to win. A separation rate here as high as the cross-arm rate means")
        lines.append("  the judges are separating plans rather than arms:")
        for judge in judges:
            w = Counter(verdict(judge, p) for p in within)
            lines.append(f"    {judge:24} within: decided={w['decided']} tie={w['tie']}"
                         f"   cross: decided={len(cross) - by_judge[judge]['tie']} tie={by_judge[judge]['tie']}")

    if len(judges) > 1:
        agreed = sum(1 for p in cross if len({verdict(j, p) for j in judges}) == 1)
        lines.append("")
        lines.append(f"  judges agreed on {agreed}/{len(cross)} cross-arm pairs. Agreement across judges is a")
        lines.append("  control on any one of them simply preferring the longer document; disagreement is a")
        lines.append("  finding of its own.")

    lines.append("")
    lines.append("  reasons given:")
    for judge, pair, order, winner, why in reasons:
        kind, i, j = pair
        lines.append(f"    [{judge}] {kind}:{i}v{j} {order:15} {winner:14} {why}")

    flat = Counter()
    for tally in by_judge.values():
        flat.update(tally)
    if flat[named["treatment"]] == flat[named["control"]]:
        lines.append("\n  No preference overall. Read this beside the assertion classification: if the graders "
                     "separated\n  the arms and this did not, the skill moved the form and not the plan.")
    return "\n".join(lines), {j: dict(t) for j, t in by_judge.items()}


def self_test(case_dir, run_cmd, judge_model=None):
    """Prove the deterministic graders still detect their target before spending a run on them.

    Three assertions, and the count of them is itself asserted, because a self-test that
    silently ran nothing would be the exact failure it exists to catch: a checker that
    inspects zero items and reports success.

    `llm` graders are covered too when `judge_model` is given, against the same known-good
    and known-bad artifacts. That is not redundant with the deterministic checks: a judge
    that fails an artifact satisfying its own criterion is a false negative, and a false
    negative is indistinguishable from a real regression once a run is under way. Two of
    them landed in the 2026-08-12 before/after comparison and were read as a regression
    until the artifacts were opened. A handful of judge calls is nothing beside the agent
    runs they precede.
    """
    case, graders = load_case(case_dir)
    free = [g for g in graders if g.get("type") != "llm"]
    if not free:
        raise SystemExit(f"ocs eval: {case['name']} has no deterministic grader to self-test")

    checks, failures = 0, []

    judged = [g for g in graders if g.get("type") == "llm"] if judge_model else []

    def probe(artifacts, record, include_judged=False):
        pool = free + (judged if include_judged else [])
        return {g["name"]: grade(g, artifacts, record, judge_model, run_cmd)[0] for g in pool}

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
        results = probe(root, record, include_judged=True)
        checks += len(results)
        if expectation == "pass":
            failures += [f"{n} failed against the known-good artifact"
                         + (" (a judge that fails its own criterion is a false negative)"
                            if n in {g["name"] for g in judged} else "")
                         for n, ok in results.items() if not ok]
        elif all(results.values()):
            failures.append("every grader passed the known-bad artifact, so none of them discriminates")

    # 3. The classification, which is where a per-assertion result becomes a finding.
    for per_arm, want in (
        ({"with-skill": [True] * 3, "without-skill": [False] * 3}, DISCRIMINATES),
        ({"with-skill": [True] * 3, "without-skill": [True] * 3}, INERT),
        ({"with-skill": [False] * 3, "without-skill": [True] * 3}, HARMFUL),
        ({"with-skill": [False] * 3, "without-skill": [False] * 3}, UNREACHED),
        ({"with-skill": [True, False, True], "without-skill": [False] * 3}, UNRELIABLE),
        ({"with-skill": [True] * 3, "without-skill": [True, False, False]}, STRENGTHENS),
    ):
        checks += 1
        got, _ = classify(per_arm)
        if got != want:
            failures.append(f"classify returned {got} where {want} was expected")

    minimum = len(free) + 6
    if checks < minimum:
        failures.append(f"self-test ran {checks} assertions, fewer than the {minimum} it must run")

    for line in failures:
        print(f"  FAIL {line}")
    covered = f"{len(free)} deterministic" + (f" + {len(judged)} llm" if judged else "")
    uncovered = "" if judged else f", {len(graders) - len(free)} llm grader(s) NOT covered — pass --judge-model to include them"
    print(f"\n{checks - len(failures)}/{checks} self-test assertions passed ({covered} grader(s){uncovered})")
    return 1 if failures else 0


def report(case, graders, records, roles=None):
    """`records` is {arm: [ {grader_name: bool} per replicate ]}."""
    named = roles or {"treatment": "with-skill", "control": "without-skill"}
    # The replicate count comes from what ran, not from what the case file asks for:
    # --runs overrides it, and a header that reports the intention misdescribes the run.
    replicates = min((len(runs) for runs in records.values()), default=0)
    lines = [f"case: {case['name']}  ({replicates} run(s) per arm; "
             f"treatment={named['treatment']}, control={named['control']})"]
    tally = Counter()
    rows = []
    for grader in graders:
        name = grader["name"]
        per_arm = {arm: [r["graders"][name]["passed"] for r in runs] for arm, runs in records.items()}
        label, detail = classify(per_arm, roles)
        tally[label] += 1
        scores = "  ".join(
            f"{arm}={sum(v for v in vals)}/{len(vals)}" for arm, vals in sorted(per_arm.items())
        )
        rows.append((label, name, grader.get("type"), grader.get("weight", 1), scores))

    width = max(len(r[1]) for r in rows)
    order = [DISCRIMINATES, STRENGTHENS, UNRELIABLE, INERT, HARMFUL, UNREACHED]
    for label, name, kind, weight, scores in sorted(rows, key=lambda r: (order.index(r[0]), r[1])):
        lines.append(f"  {label:14} {name:{width}}  {kind:11} w{weight}  {scores}")

    lines.append("")
    if not tally[DISCRIMINATES] and not tally[STRENGTHENS]:
        lines.append(
            "  No assertion discriminated. Report this as an insensitive instrument or an insensitive\n"
            "  expectation set, not as a successful measurement."
        )
    if tally[INERT]:
        lines.append(
            f"  {tally[INERT]} assertion(s) passed in both arms. That part of the skill is doing nothing here,\n"
            "  which is deletion evidence rather than a pass."
        )
    if tally[STRENGTHENS]:
        lines.append(
            f"  {tally[STRENGTHENS]} assertion(s) the control produced sometimes and the skill produced every\n"
            "  time. This is a real effect and the replicate count is what bounds it, so read the ratio rather\n"
            "  than the label.")
    if tally[UNRELIABLE]:
        lines.append(
            f"  {tally[UNRELIABLE]} assertion(s) the skill itself produced only sometimes. That is the skill or\n"
            "  the assertion being unreliable, not the baseline, and it needs more replicates before it is read.")
    return "\n".join(lines), dict(tally)
