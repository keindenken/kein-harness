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
import random
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
        # Not `record["files_written"]`, which is read off the lead's event stream and so
        # contains nothing a subagent wrote. A run whose Planner wrote the artifact showed
        # the judge an empty list, and the judge concluded from it that no file was created
        # -- while the deterministic grader beside it confirmed the file was there.
        # `collect()` takes this from `git status` against a worktree committed before the
        # arm started, so it holds every file the run touched whoever touched it.
        prompt += ("=== WHAT THE RUN PRODUCED ===\n" + produced + "\n\n"
                   "=== EVERY FILE THE RUN CREATED OR CHANGED ===\n"
                   + "\n".join(_produced_paths(artifacts) or ["(none)"]) + "\n\n")
    prompt += ("Reply with exactly two lines and nothing else:\n"
               "VERDICT: PASS or FAIL\n"
               "WHY: one sentence naming the specific thing in the artifact that decided it.")

    out = run_cmd(["claude", "--model", model, "--strict-mcp-config", "-p", prompt],
                  check=False).stdout.decode("utf-8", "replace").strip()
    # The verdict is still one token and still the first thing parsed, because anything a
    # judge can hedge in it will. The reason is read from its own line and never consulted
    # for the decision -- it is there because a run of these is otherwise a column of bare
    # FAILs, and every time this programme learned something it was from a judge's wording.
    stated = re.search(r"^VERDICT:\s*(PASS|FAIL)", out, re.M | re.I)
    why = re.search(r"^WHY:\s*(.+)$", out, re.M | re.I)
    verdict = (stated.group(1) if stated else (out.split() or [""])[0]).upper()
    detail = (why.group(1).strip() if why else out.replace("\n", " "))[:300]
    if verdict.startswith("PASS"):
        return True, detail
    if verdict.startswith("FAIL"):
        return False, detail
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
        if path.name in HARNESS_FILES:
            continue
        text = path.read_text(errors="replace")[:budget]
        budget -= len(text)
        out.append(f"--- {path.relative_to(artifacts)}\n{text}")
        if budget <= 0:
            break
    return "\n\n".join(out)


HARNESS_FILES = {"_record.json"}


def _produced_paths(artifacts):
    """Every file the run created or changed, as paths, fixture copy excluded.

    `_record.json` is the self-test's own contract file and no run ever writes one.
    Listing it told a judge grading "is PLAN.md the only file written" that a second
    file had been written, and it failed the artifact built to pass it.
    """
    root = Path(artifacts)
    return sorted(str(p.relative_to(root)) for p in root.rglob("*")
                  if p.is_file() and p.name not in HARNESS_FILES
                  and not p.is_relative_to(root / "fixture"))


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


# Same criteria as JUDGE, asked of the whole field at once. Pairwise cost is quadratic in plans -- six per arm
# is 66 pairs and, at three judges and two orders, 396 calls -- while a judge that reads every plan in one
# sitting costs one call and still compares, which is what an isolated per-plan score would have thrown away.
RANKER = (
    "Several implementation plans were written from the same requirements document, by different processes. "
    "Rank them from best to worst for the person who has to build from them.\n\n"
    "Judge only against the requirements document below. Do not reward a plan for structure, for headings, "
    "for length, or for confident tone; a plan that carries a section is not thereby better than one that "
    "does the same work in prose. What matters is whether someone could execute it without having to make "
    "a decision the plan should have made for them.\n\n"
    "Pay particular attention to what each plan does with a fact the requirements say nobody has established "
    "yet. Naming it is easy. Deciding, now, what happens under each of its possible answers is the thing "
    "that costs something.\n\n"
    "=== REQUIREMENTS ===\n{requirements}\n\n"
    "{plans}\n\n"
    "Reply with exactly these lines and nothing else:\n"
    "RANKING: all {n} labels separated by commas, best first, each label exactly once\n"
    "WHY: one sentence naming the difference that separated the top of your ranking from the bottom.\n"
    "then one line per plan, in your ranked order:\n"
    "NOTE <label>: the specific thing about that plan that put it where you put it."
)

RANKING_SCHEMA = {
    "type": "object",
    "properties": {
        "ranking": {"type": "array", "items": {"type": "string"}},
        "why": {"type": "string"},
        "notes": {"type": "object", "additionalProperties": {"type": "string"}},
    },
    "required": ["ranking", "why"],
    "additionalProperties": False,
}


def _ask_ranking(spec, prompt, run_cmd, scratch, labels):
    """One judge, one ordering of the whole field. Returns (ranking, why, notes) or (None, reason, {}).

    A reading is kept only when it is a permutation of the labels handed out. A judge that
    drops a plan or names one twice has not ranked the field, and averaging a partial order
    in with complete ones would quietly weight it.

    The per-plan notes are why this is worth more than a number. A ranking says the field
    was sorted; it does not say on what, and the axis the judges turned out to be sorting on
    was not the one the prompt under test was written to move. A note attached to a plan is
    where that shows up.
    """
    def check(order, why, notes):
        order = [item.strip().upper() for item in order if item.strip()]
        if sorted(order) != sorted(labels):
            return None, f"not a permutation of {''.join(labels)}: {','.join(order) or 'empty'}", {}
        return order, why, {k.strip().upper(): v.strip() for k, v in (notes or {}).items()}

    if spec.endswith("@codex") or not spec.startswith("codex"):
        if spec.endswith("@codex"):
            role = spec[: -len("@codex")]
            command = [str(Path(__import__("os").environ["KEIN_ROOT"]) / "libexec" / "ocs-ask"),
                       "codex", "--agent", role, "--model", "gpt-5.6-sol", "--effort", "medium", prompt]
        else:
            command = ["claude", "--model", spec, "--strict-mcp-config", "-p", prompt]
        out = run_cmd(command, check=False).stdout.decode("utf-8", "replace")
        ranking = re.search(r"^RANKING:\s*(.+)$", out, re.M | re.I)
        why = re.search(r"^WHY:\s*(.+)$", out, re.M | re.I)
        if not ranking:
            return None, "no RANKING line", {}
        notes = dict(re.findall(r"^NOTE\s+([A-Za-z]+)\s*:\s*(.+)$", out, re.M))
        return check(ranking.group(1).split(","), why.group(1).strip() if why else "", notes)

    schema = scratch / "rank-schema.json"
    schema.write_text(json.dumps(RANKING_SCHEMA))
    command = ["codex", "exec", "--sandbox", "read-only", "--skip-git-repo-check",
               "--ephemeral", "--output-schema", str(schema)]
    _, _, chosen = spec.partition(":")
    if chosen:
        command += ["-m", chosen]
    result = run_cmd(command + [prompt], check=False).stdout.decode("utf-8", "replace")
    objects = re.findall(r'\{.*?"ranking".*?\}\s*$', result, re.S | re.M)
    if not objects:
        return None, "unreadable codex output", {}
    parsed = json.loads(objects[-1])
    return check(parsed.get("ranking") or [], parsed.get("why", ""), parsed.get("notes"))


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


def _artifacts(run_dir, arm):
    """One arm's produced markdown, per replicate, with the copied fixture left out of it."""
    root = Path(run_dir) / "artifacts" / arm
    out = []
    for replicate in sorted(root.iterdir()) if root.is_dir() else []:
        files = sorted(p for p in replicate.rglob("*") if p.is_file() and p.suffix == ".md")
        files = [p for p in files if not p.is_relative_to(replicate / "fixture")]
        if files:
            out.append((replicate.name, "\n\n".join(p.read_text(errors="replace") for p in files)))
    return out


def _requirements(case_dir):
    return "\n\n".join(p.read_text(errors="replace")
                       for p in sorted((Path(case_dir) / "fixture").rglob("*.md")))


def rank(run_dir, case_dir, judges, run_cmd, shuffles=3, roles=None):
    """Every plan ranked in one sitting, by each judge, over several presentation orders.

    This answers the same question `compare` does and replaces it above about four plans a
    side, where the pairwise cost stops being worth paying: pairs grow as the square of the
    field, so six a side is 66 pairs and 396 calls at three judges and two orders, while
    this is one call per judge per shuffle.

    What the shuffles buy is what both orders bought pairwise. A judge handed a list has a
    position preference, and re-presenting the same field in a different order is the only
    thing that separates that preference from a reading of the plans.

    The within-arm control does not survive as its own number, and does not need to: the
    ranking already carries it. If plans from the two arms interleave, whatever the judges
    are sorting on is not the arm -- which is the same reading the control was there to
    license, taken off the ranking instead of off a separate set of pairs.
    """
    run_dir, case_dir = Path(run_dir), Path(case_dir)
    requirements = _requirements(case_dir)
    named = roles or {"treatment": "with-skill", "control": "without-skill"}
    field = ([(f"{named['treatment']}/{name}", text) for name, text in _artifacts(run_dir, named["treatment"])] +
             [(f"{named['control']}/{name}", text) for name, text in _artifacts(run_dir, named["control"])])
    if len(field) < 3:
        raise SystemExit(f"ocs eval: need at least three plans under {run_dir / 'artifacts'}; found {len(field)}")

    scratch = run_dir / "rank"
    scratch.mkdir(exist_ok=True)
    labels = [chr(ord("A") + i) for i in range(len(field))]

    # Seeded from the shuffle index alone, so the same run ranked twice presents the same
    # orders twice and a difference between the readings is the judges, not the deal.
    orders = []
    for index in range(shuffles):
        order = list(range(len(field)))
        random.Random(9000 + index).shuffle(order)
        orders.append(order)

    def one(call):
        judge, index = call
        order = orders[index]
        plans = "\n\n".join(f"=== PLAN {labels[seat]} ===\n{field[plan][1]}"
                            for seat, plan in enumerate(order))
        ranking, why, notes = _ask_ranking(
            judge, RANKER.format(requirements=requirements, plans=plans, n=len(field)),
            run_cmd, scratch, labels)
        if ranking is None:
            return call, None, why, {}
        # The judge names seats; the seat's occupant is what gets the points, and what the
        # note is about. A note filed under a seat is meaningless one deal later.
        seated = {label: field[order[labels.index(label)]][0] for label in labels}
        return (call, [seated[label] for label in ranking], why,
                {seated[label]: text for label, text in notes.items() if label in seated})

    calls = [(judge, index) for judge in judges for index in range(shuffles)]
    with ThreadPoolExecutor(max_workers=min(8, len(calls))) as pool:
        readings = list(pool.map(one, calls))

    points, per_judge, discarded, said = Counter(), {}, [], {}
    for (judge, index), ranking, why, notes in readings:
        if ranking is None:
            discarded.append((judge, index, why))
            continue
        per_judge.setdefault(judge, Counter())
        for position, plan in enumerate(ranking):
            gained = len(field) - 1 - position
            points[plan] += gained
            per_judge[judge][plan] += gained
        for plan, text in notes.items():
            said.setdefault(plan, []).append((judge, index, text))
    for plan, _ in field:
        points.setdefault(plan, 0)

    kept = len(readings) - len(discarded)
    lines = [f"every plan ranked in one sitting, {len(field)} plans x {len(judges)} judge(s) "
             f"x {shuffles} presentation order(s), arm labels withheld:"]
    lines.append(f"  {kept}/{len(readings)} reading(s) usable; a reading that is not a permutation "
                 f"of the field is dropped rather than partially counted.")
    lines.append("")
    lines.append(f"  points (a plan placed first in a reading takes {len(field) - 1}, last takes 0):")
    standing = sorted(points.items(), key=lambda kv: -kv[1])
    for plan, score in standing:
        lines.append(f"    {score:4d}  {plan}")
    lines.append(f"    order by arm: {' '.join(plan.split('/')[0] for plan, _ in standing)}")
    lines.append("    Arms interleaved here means the arm is not what the ranking is ranking.")
    lines.append("    This line is the control: within-arm spread showing up as interleaving is the same")
    lines.append("    finding the separate within-arm pairs used to report.")

    if len(per_judge) > 1:
        lines.append("")
        lines.append("  each judge's own order, so a single judge driving the aggregate is visible:")
        for judge, tally in per_judge.items():
            order = [plan for plan, _ in sorted(tally.items(), key=lambda kv: -kv[1])]
            lines.append(f"    {judge:24} {' > '.join(order)}")

    if discarded:
        lines.append("")
        lines.append("  dropped readings:")
        for judge, index, why in discarded:
            lines.append(f"    [{judge}] order#{index}  {why}")

    lines.append("")
    lines.append("  each reading, and the axis it says it sorted on:")
    for (judge, index), ranking, why, _ in readings:
        if ranking is not None:
            lines.append(f"    [{judge}] order#{index}  {' > '.join(ranking)}")
            lines.append(f"      {why[:220]}")

    if said:
        lines.append("")
        lines.append("  what the judges said about each plan, in finishing order. A ranking says the field was")
        lines.append("  sorted and not on what; this is where a judge sorting on something the prompt under")
        lines.append("  test was never written to move becomes visible:")
        for plan, _ in standing:
            if plan in said:
                lines.append(f"    {plan}")
                for judge, index, text in said[plan]:
                    lines.append(f"      [{judge}#{index}] {text[:200]}")

    return "\n".join(lines), {plan: score for plan, score in standing}


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

    named = roles or {"treatment": "with-skill", "control": "without-skill"}
    treatment, control = _artifacts(run_dir, named["treatment"]), _artifacts(run_dir, named["control"])
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
        left = f"{named['treatment']}/{i}" if kind != "within-control" else f"{named['control']}/{i}"
        right = (f"{named['control']}/{j}" if kind == "cross"
                 else f"{named['treatment']}/{j}" if kind == "within-treatment"
                 else f"{named['control']}/{j}")
        winner = "tie" if choice == "TIE" else (left if choice == treatment_is else right)
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

    def arm_of(plan):
        return plan.split("/")[0]

    for judge in judges:
        tally = Counter()
        for p in cross:
            v = verdict(judge, p)
            tally[v if v == "tie" else arm_of(v)] += 1
        by_judge[judge] = tally

    # 15 pairs over 6 plans is every pair, so wins across all of them is a ranking.
    standings = Counter()
    for judge in judges:
        for p in pairs:
            v = verdict(judge, p)
            if v != "tie":
                standings[v] += 1
    everyone = [f"{named['treatment']}/{i}" for i in range(len(treatment))] + \
               [f"{named['control']}/{i}" for i in range(len(control))]
    for plan in everyone:
        standings.setdefault(plan, 0)

    lines = [f"blind pairwise over every cross-arm pair ({len(cross)}), both orders "
             f"x{repeats} repeat(s), arm labels withheld from every judge:"]
    for judge, tally in by_judge.items():
        lines.append(f"  {judge:24} {named['treatment']}={tally[named['treatment']]}  "
                     f"{named['control']}={tally[named['control']]}  tie={tally['tie']}")

    lines.append("")
    lines.append(f"  every plan ranked, wins over all {len(pairs)} pairs x {len(judges)} judge(s) x 2 orders:")
    for plan, wins in sorted(standings.items(), key=lambda kv: -kv[1]):
        lines.append(f"    {wins:3d}  {plan}")
    arms_in_order = [arm_of(plan) for plan, _ in sorted(standings.items(), key=lambda kv: -kv[1])]
    lines.append(f"    order by arm: {' '.join(arms_in_order)}")
    lines.append("    Arms interleaved here means the arm is not what the ranking is ranking.")

    if within:
        lines.append("")
        lines.append(f"  control - the same judges on {len(within)} pairs drawn from inside one arm, where")
        lines.append("  there is no arm to win. A separation rate here as high as the cross-arm rate means")
        lines.append("  the judges are separating plans rather than arms:")
        for judge in judges:
            w = Counter("tie" if verdict(judge, p) == "tie" else "decided" for p in within)
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
    # `--arm` can leave one side out, and a run of one arm has no comparison to name. It
    # still has results worth printing -- filling a gap in an interrupted run is exactly
    # when one gets used -- so say which arm ran instead of failing on the missing role.
    if len(records) < 2:
        only = next(iter(records), "none")
        lines = [f"case: {case['name']}  ({replicates} run(s); {only} only, no comparison)"]
    else:
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
    if tally[HARMFUL]:
        lines.append(
            f"  {tally[HARMFUL]} assertion(s) the control produced and the skill did not. Read it as written\n"
            "  before softening it: the arm carrying the skill is the one that failed.")
    if tally[UNREACHED]:
        lines.append(
            f"  {tally[UNREACHED]} assertion(s) neither arm produced. The word is not `unreachable` and does not\n"
            "  mean the run fell short of them — both arms finished and both failed. It is a rule the skill\n"
            "  states and does not get followed, or an assertion no plan can satisfy as written, and the two\n"
            "  are different findings this label does not separate. Read the artifact before choosing.")
    return "\n".join(lines), dict(tally)
