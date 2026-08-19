#!/usr/bin/env python3
"""Choose which skills the reading pass spends a call on.

Named `shortlist` and not `select`: this directory goes on `sys.path` for the
other scripts here, and a `select.py` beside them shadows the standard library
module that `subprocess` imports. Everything that shells out breaks, and the
traceback blames `msvcrt`.

37,276 skills is more than any pass will read, so something has to rank them.
This uses `specificity` — a weighted count of the ways a document shows it was
corrected by something outside its author's imagination — and it uses it because
it was checked rather than assumed. A stratified 500 through the reading pass
yielded verified quotes at 24%, 40%, 64% and 74% across its quartiles: monotonic,
threefold, and measured against an output a grep can confirm.

That check matters because the same proxy looked dead a round earlier. 260811
drew a control band from below the median and the model scored it 85% against
the top band's 91%, which reads as a proxy that separates nothing. What it
actually showed was a *score* that separated nothing; the proxy was fine.

Three reductions, in order:

  dedupe    Convergence here is copying. A cluster of near-identical files is
            one file's worth of information, so each keeps its longest member.
  cap       One repository holding sixty high-scoring skills would otherwise
            take sixty of the slots. The cap is per repository, not per domain:
            260811 stratified by seven domain regexes, and because a file was
            assigned to whichever matched first alphabetically, every bucket
            after `code` held leftovers. A repository is a fact; a domain
            assigned by regex was not.
  rank      Take the top N by specificity from what survives.

Usage: ./shortlist.py [--top N] [--per-repo K] [--out shortlist.json]
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus"

# Each pattern is a way a document shows it met something it did not predict.
# Weights are ordinal and inherited from 260811 unchanged, so the quartile
# yields measured there still describe this scale.
SPECIFICITY = [
    ("version_pin", 3, re.compile(r"\b\d+\.\d+(\.\d+)?\b")),
    ("threshold", 3, re.compile(r"\b\d+\s*(ms|s|kb|mb|gb|tokens?|lines?|chars?|characters|seconds|minutes)\b", re.I)),
    ("error_string", 4, re.compile(r"\b(error|exception|errno|E[A-Z]{4,}|traceback|panic|fatal):", re.I)),
    ("reason", 2, re.compile(r"\b(because|since it|the reason|which is why|otherwise)\b", re.I)),
    ("negative", 2, re.compile(r"\b(do not|don't|never|avoid|instead of|rather than)\b", re.I)),
    ("failure_report", 5, re.compile(r"\b(in practice|we found|turned out|fails when|breaks when|silently|gotcha|footgun|pitfall|caveat)\b", re.I)),
    ("dated", 5, re.compile(r"\b(20\d\d-\d\d-\d\d|measured|observed|verified on)\b", re.I)),
    ("command", 2, re.compile(r"^\s*(\$|>)\s*\S+|`[a-z-]+ (--?\w|\w+ --)", re.M)),
]
FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.S)
SHINGLE = 9   # long enough that a shared boilerplate line does not match by luck


def score(text):
    body = FRONTMATTER.sub("", text)
    hits, total = {}, 0
    for label, weight, pat in SPECIFICITY:
        n = len(pat.findall(body))
        if n:
            hits[label] = n
            total += weight * min(n, 6)
    return total, hits


def shingles(text):
    words = re.findall(r"\w+", text.lower())
    return {hash(tuple(words[i:i + SHINGLE])) for i in range(0, max(0, len(words) - SHINGLE), 3)}


def cluster(records):
    """Union-find over an inverted index, so a file is only compared against
    files it actually shares a shingle with."""
    parent = list(range(len(records)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    posting = defaultdict(list)
    for i, r in enumerate(records):
        for s in r["_sh"]:
            posting[s].append(i)

    overlap = Counter()
    for members in posting.values():
        if len(members) > 40:
            continue          # boilerplate shingle, says nothing about any pair
        for a in members:
            for b in members:
                if a < b:
                    overlap[(a, b)] += 1

    for (a, b), n in overlap.items():
        sa, sb = records[a]["_sh"], records[b]["_sh"]
        if n / (min(len(sa), len(sb)) or 1) >= 0.6:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

    groups = defaultdict(list)
    for i in range(len(records)):
        groups[find(i)].append(i)
    return list(groups.values())


def main():
    top, per_repo, out = 4000, 12, HERE / "shortlist.json"
    for i, a in enumerate(sys.argv):
        if a == "--top":
            top = int(sys.argv[i + 1])
        if a == "--per-repo":
            per_repo = int(sys.argv[i + 1])
        if a == "--out":
            out = Path(sys.argv[i + 1])

    manifest = json.loads((HERE / "manifest.json").read_text())
    stars = {r["full_name"]: r["stars"] for r in json.loads((HERE / "repos.json").read_text())}

    records = []
    for m in manifest:
        anchor = next((f for f in m["files"]
                       if f["path"].rsplit("/", 1)[-1] in ("SKILL.md", "AGENTS.md", "CLAUDE.md")), None)
        if not anchor:
            continue
        p = CORPUS / m["repo"] / anchor["path"]
        if not p.exists():
            continue
        text = p.read_text(errors="replace")
        s, hits = score(text)
        records.append({**m, "specificity": s, "markers": hits,
                        "words": len(text.split()), "stars": stars.get(m["repo"], 0),
                        "_sh": shingles(FRONTMATTER.sub("", text))})
    print(f"{len(records)} skills scored")

    groups = cluster(records)
    kept = []
    for members in groups:
        members.sort(key=lambda i: -records[i]["words"])
        head = records[members[0]]
        head["cluster_size"] = len(members)
        head["cluster_repos"] = sorted({records[i]["repo"] for i in members})[:8]
        kept.append(head)
    for r in kept:
        r.pop("_sh", None)
    dup = [r for r in kept if r["cluster_size"] > 1]
    print(f"dedupe: {len(records)} -> {len(kept)}  ({len(dup)} clusters hold more than one, "
          f"largest {max((r['cluster_size'] for r in dup), default=0)})")

    kept.sort(key=lambda r: -r["specificity"])
    picked, taken = [], Counter()
    overflow = 0
    for r in kept:
        if len(picked) >= top:
            break
        if taken[r["repo"]] >= per_repo:
            overflow += 1
            continue
        taken[r["repo"]] += 1
        picked.append(r)

    out.write_text(json.dumps(picked, indent=1))
    s = [r["specificity"] for r in picked]
    st = sorted(r["stars"] for r in picked)
    print(f"selected {len(picked)} over {len(taken)} repositories "
          f"(cap {per_repo}/repo held back {overflow} higher-scoring skills)")
    print(f"  specificity: cut {s[-1]}, median {s[len(s)//2]}, max {s[0]}")
    print(f"  stars:       floor {st[0]}, median {st[len(st)//2]}, top {st[-1]:,}")
    print(f"  with prose siblings not yet fetched: "
          f"{sum(1 for r in picked if any(f['path'].lower().endswith(('.md','.txt')) for f in r.get('not_fetched', [])))}")
    print(f"  -> {out.name}")


main()
