#!/usr/bin/env python3
"""Reduce the harvested corpus to what is worth a model's attention.

Two reductions, in this order:

  dedupe       Convergence in this corpus is copying, so a family of near
               identical files carries one file's worth of information. Each
               cluster keeps its longest member and records the rest.

  specificity  A skill that has met reality names things: a version, a
               threshold, an error string, a reason, a thing not to do. A skill
               derived from the idea of the domain does not. This is a cheap
               proxy computed here so that the model is spent on ranking within
               the plausible set rather than discarding the obvious.

Neither reduction decides anything. Both are recorded per file so a later pass
can disagree with them.

Usage: ./triage.py            # writes triage.json and prints the distribution
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus"

FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.S)
SHINGLE = 9  # words per shingle; long enough that shared boilerplate lines do not match by luck

# Each pattern is a way a document shows it was corrected by something outside
# the author's imagination. Weights are ordinal, not calibrated.
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

# Rough domain buckets. Deliberately coarse: this only stratifies the shortlist
# so that one crowded domain cannot starve the others.
DOMAINS = {
    "process": r"\b(workflow|orchestrat|pipeline|loop|iterat|subagent|delegat|dispatch|plan(ning)?|review|critique|verify|checkpoint|handoff)\b",
    "research": r"\b(research|investigat|literature|citation|survey|synthesis|evidence|hypothes)\b",
    "writing": r"\b(writ(ing|e)|prose|style guide|editing|copy|narrative|tone|voice)\b",
    "documentation": r"\b(documentation|docs|readme|changelog|api reference|tutorial|runbook)\b",
    "product": r"\b(product manage|roadmap|okr|stakeholder|user stor|backlog|prd|requirements doc|prioriti)\b",
    "meta": r"\b(skill|prompt|claude\.md|agents\.md|context window|instruction)\b",
    "code": r"\b(refactor|test|debug|typescript|python|react|database|migration|deploy|lint)\b",
}
DOMAIN_RE = {k: re.compile(v, re.I) for k, v in DOMAINS.items()}


def body(text):
    return FRONTMATTER.sub("", text)


def shingles(text):
    words = re.findall(r"\w+", text.lower())
    return {hash(tuple(words[i:i + SHINGLE])) for i in range(0, max(0, len(words) - SHINGLE), 3)}


def cluster(records):
    """Group by shingle overlap. Union-find over an inverted index, so a file is
    only compared against files it actually shares a shingle with."""
    parent = list(range(len(records)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    posting = defaultdict(list)
    for i, r in enumerate(records):
        for s in r["_shingles"]:
            posting[s].append(i)

    overlap = Counter()
    for members in posting.values():
        if len(members) > 40:
            continue  # boilerplate shingle, tells us nothing about any pair
        for a in members:
            for b in members:
                if a < b:
                    overlap[(a, b)] += 1

    for (a, b), n in overlap.items():
        sa, sb = records[a]["_shingles"], records[b]["_shingles"]
        smaller = min(len(sa), len(sb)) or 1
        if n / smaller >= 0.6:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

    groups = defaultdict(list)
    for i in range(len(records)):
        groups[find(i)].append(i)
    return list(groups.values())


def main():
    index = json.loads((HERE / "index.json").read_text())
    records = []
    for rec in index:
        text = (CORPUS / rec["file"]).read_text(errors="replace")
        b = body(text)
        rec = dict(rec)
        rec["_shingles"] = shingles(b)
        hits, score = {}, 0
        for label, weight, pat in SPECIFICITY:
            n = len(pat.findall(b))
            if n:
                hits[label] = n
                score += weight * min(n, 6)
        rec["specificity"] = score
        rec["markers"] = hits
        blob = f"{rec['name']} {rec['description']} {b[:4000]}"
        rec["domains"] = [d for d, p in DOMAIN_RE.items() if p.search(blob)]
        records.append(rec)

    clusters = cluster(records)
    kept = []
    for members in clusters:
        members.sort(key=lambda i: -records[i]["words"])
        head = records[members[0]]
        head["cluster_size"] = len(members)
        head["cluster_repos"] = sorted({records[i]["repo"] for i in members})[:8]
        kept.append(head)

    for r in kept:
        r.pop("_shingles", None)
    kept.sort(key=lambda r: -r["specificity"])
    (HERE / "triage.json").write_text(json.dumps(kept, indent=1))

    print(f"{len(records)} files -> {len(kept)} after dedupe")
    dup = sorted((r for r in kept if r["cluster_size"] > 1), key=lambda r: -r["cluster_size"])
    print(f"{len(dup)} clusters hold more than one file; largest {dup[0]['cluster_size'] if dup else 0}")
    print("\ncopied across the most repositories:")
    for r in sorted(dup, key=lambda r: -len(r["cluster_repos"]))[:8]:
        print(f"  x{r['cluster_size']:<4} {len(r['cluster_repos'])} repos  {r['name'][:34]:34} {r['repo'][:30]}")

    print("\nspecificity deciles:")
    s = [r["specificity"] for r in kept]
    for q in range(0, 101, 10):
        print(f"  p{q:<3} {s[min(len(s) - 1, int(len(s) * (100 - q) / 100))]}")

    print("\ndomain coverage (deduped):")
    c = Counter(d for r in kept for d in r["domains"])
    for d, n in c.most_common():
        top = sorted((x for x in kept if d in x["domains"]), key=lambda x: -x["specificity"])[:1]
        print(f"  {d:14} {n:5}   top: {top[0]['name'][:30] if top else '-'}")
    print(f"  {'(none)':14} {sum(1 for r in kept if not r['domains']):5}")


if __name__ == "__main__":
    main()
