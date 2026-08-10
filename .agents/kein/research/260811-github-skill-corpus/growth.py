#!/usr/bin/env python3
"""Measure whether standing prompts grow monotonically, over the revised corpus.

`docs/prompt-revision.md` rests on a premise it never tested: that a standing
prompt grows because adding needs one incident and removing needs proof a
failure no longer recurs. The corpus of most-revised public skills can answer
this directly, since every commit that touched a SKILL.md is a prompt edit with
its own message.

Reported per commit and per file:

  net             added minus removed lines, excluding diff headers
  shrinking       commits whose net is negative
  intent vs act   commits whose message claims simplification, against what
                  their diff actually did. This is the interesting cell: a
                  release titled "simpler prompts" was +163/-0 in one file.

Usage: ./growth.py
"""

import json
import re
import statistics
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIFFS = HERE / "diffs"

HEADER = re.compile(r"^(=== [0-9a-f]{7,40} |diff --git |index |--- |\+\+\+ |@@ )")
SIMPLIFY = re.compile(
    r"\b(simplif|simpler|shrink|trim|slim|condens|compress|concise|terse|"
    r"remove|delet|drop|cut|prune|dedup|consolidat|reduce|streamlin|clean ?up|refactor)\b", re.I)


def commits(text):
    out, cur = [], None
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("=== ") and re.match(r"=== [0-9a-f]{7,40} \d{4}-\d\d-\d\d ", line):
            if cur:
                out.append(cur)
            parts = line[4:].split(" ", 2)
            cur = {"sha": parts[0], "date": parts[1], "author": parts[2] if len(parts) > 2 else "",
                   "subject": lines[i + 1].strip() if i + 1 < len(lines) else "",
                   "add": 0, "rem": 0}
        elif cur is not None and not HEADER.match(line):
            if line.startswith("+"):
                cur["add"] += 1
            elif line.startswith("-"):
                cur["rem"] += 1
    if cur:
        out.append(cur)
    return out


def main():
    files = sorted(DIFFS.glob("*.diff"))
    per_file, all_commits = [], []
    for f in files:
        cs = commits(f.read_text(errors="replace"))
        if not cs:
            continue
        for c in cs:
            c["file"] = f.stem
        all_commits.extend(cs)
        per_file.append({
            "file": f.stem,
            "commits": len(cs),
            "add": sum(c["add"] for c in cs),
            "rem": sum(c["rem"] for c in cs),
            "net": sum(c["add"] - c["rem"] for c in cs),
        })

    edits = [c for c in all_commits if c["add"] or c["rem"]]
    nets = [c["add"] - c["rem"] for c in edits]
    shrink = [c for c in edits if c["add"] - c["rem"] < 0]
    grow = [c for c in edits if c["add"] - c["rem"] > 0]

    print(f"{len(files)} files, {len(all_commits)} commits, {len(edits)} that changed a line")
    print(f"  net positive: {len(grow)}  net negative: {len(shrink)}  net zero: {len(edits)-len(grow)-len(shrink)}")
    print(f"  median net per commit: {statistics.median(nets):.0f}")
    print(f"  total added {sum(c['add'] for c in edits)}, removed {sum(c['rem'] for c in edits)}")
    print()

    print("per file, net line change over its whole history:")
    per_file.sort(key=lambda r: -r["commits"])
    shrank = [r for r in per_file if r["net"] < 0]
    print(f"  files that ended smaller than they started: {len(shrank)}/{len(per_file)}")
    for r in per_file[:12]:
        print(f"    {r['commits']:4d}c  +{r['add']:<5d} -{r['rem']:<5d} net {r['net']:+6d}  {r['file'][:52]}")
    print()

    claims = [c for c in edits if SIMPLIFY.search(c["subject"])]
    honest = [c for c in claims if c["add"] - c["rem"] < 0]
    print(f"commits whose message claims a cut or a simplification: {len(claims)}")
    print(f"  of those, actually net negative: {len(honest)} ({100*len(honest)//max(1,len(claims))}%)")
    print(f"  net positive anyway: {sum(1 for c in claims if c['add'] - c['rem'] > 0)}")
    print()
    print("  the largest additions made under a subject that claims subtraction:")
    for c in sorted(claims, key=lambda c: -(c["add"] - c["rem"]))[:10]:
        print(f"    {c['add']-c['rem']:+5d}  {c['date']}  {c['subject'][:78]}")
    print()
    print("  the real cuts:")
    for c in sorted(honest, key=lambda c: c["add"] - c["rem"])[:10]:
        print(f"    {c['add']-c['rem']:+5d}  {c['date']}  {c['subject'][:78]}")

    (HERE / "growth.json").write_text(json.dumps(
        {"per_file": per_file, "commits": all_commits}, indent=1))

    print()
    print("author concentration over the revised set:")
    a = Counter(c["author"] for c in edits)
    print(f"  {len(a)} distinct authors; top 5 hold "
          f"{100*sum(n for _, n in a.most_common(5))//len(edits)}% of edits")


if __name__ == "__main__":
    main()
