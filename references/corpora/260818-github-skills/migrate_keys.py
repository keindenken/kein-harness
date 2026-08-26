#!/usr/bin/env python3
"""Rewrite the run files onto the skill key that is actually unique.

`extract.py` first keyed a skill as `repo/dir`, and `dir` is empty for a skill
anchored on a root `AGENTS.md` or `CLAUDE.md` — so a repository holding both
produced two manifest entries under the one key `repo`. 442 keys covered 447
entries that way. The reading pass has since been fixed to write
`repo::AGENTS.md`, which is why 21 records from the null re-read arrived under a
name nothing else in `runs/` used.

299 records carry an empty `dir` and 167 of those sit in a repository with more
than one candidate file. Which one was read is recoverable: `inlined` records the
files that call actually saw, so the manifest entry it matches is the entry that
produced it.

The map cannot be old key to new key. Seven of those repositories were read
twice in one run — both loose files, both written under the one key — so a map
from `repo` to a single new name gives two different files the same one, which
is the collision this is meant to end. `pass2.jsonl` is renamed line by line
from each record's own `inlined`; every other file joins on the old key and
takes the new one only where that old key is unambiguous.

This is a rename, not a re-read. Nothing is recomputed and no line is dropped;
`--check` reports what would change and writes nothing.

Usage: ./migrate_keys.py [--check]
"""
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"

# Files whose records are keyed by `skill`, one JSON object per line.
LINE_FILES = ["pass2.jsonl", "facet.jsonl", "facet-ko-fix.jsonl",
              "facet-recovered.jsonl", "topic.jsonl", "labels-v2.jsonl",
              "quote-recheck.jsonl", "null-probe.jsonl", "null-neutral.jsonl"]
# Files holding a whole JSON document with keys buried inside.
DOC_FILES = {
    "facet-records.json": "list-skill",
    "topic-records.json": "list-skill",
    "recovered-records.json": "list-skill",
    "null-recovered.json": "list-skill",
    "null-probe-arms.json": "dict-key",
    "topic-clusters.json": "cluster",
    "topic-clusters-all.json": "cluster",
    "cluster-read.jsonl": "cluster-lines",
    "cluster-read-neutral.jsonl": "cluster-lines",
    "pass1.jsonl": "cluster-lines",
    "match.json": "match",
}


def build_map():
    """old key -> new key, for the records whose old key was ambiguous.

    Repositories with a single loose-file entry keep the bare `repo` key: there
    was never a collision there, and renaming them would churn 132 records to no
    end.
    """
    cand = defaultdict(list)
    for m in json.loads((HERE / "manifest.json").read_text()):
        if not m["dir"] and m.get("loose_file"):
            cand[m["repo"]].append(m)

    ambiguous = {r: ms for r, ms in cand.items() if len(ms) > 1}
    lines, unresolved = [], []
    for line in (RUNS / "pass2.jsonl").read_text().splitlines():
        r = json.loads(line)
        # A record that failed to parse carries only `skill` and `error`; there
        # is nothing in it to say which file it was.
        if r.get("dir") or r.get("repo") not in ambiguous:
            lines.append(None)
            continue
        seen = set(r.get("inlined") or []) | set(r.get("not_inlined") or [])
        hit = [m for m in ambiguous[r["repo"]] if m["loose_file"] in seen]
        if len(hit) == 1:
            lines.append(f"{r['repo']}::{hit[0]['loose_file']}")
        else:
            lines.append(None)
            unresolved.append(r["skill"])

    # The old-key map is for every other file. Where two lines shared an old key
    # and resolved differently, the last one is the one every downstream file
    # holds: each was built by reading `pass2.jsonl` into a dict keyed by skill,
    # so the later line overwrote the earlier before anything else saw it.
    byold, last = defaultdict(set), {}
    for line, new in zip((json.loads(l) for l in
                          (RUNS / "pass2.jsonl").read_text().splitlines()), lines):
        if new:
            byold[line["skill"]].add(new)
            last[line["skill"]] = new
    out = {k: last[k] for k in byold}
    split = sorted(k for k, v in byold.items() if len(v) > 1)
    return out, unresolved, ambiguous, lines, split


def rewrite(obj, kind, mp):
    if kind == "list-skill":
        for r in obj:
            if r.get("skill") in mp:
                r["skill"] = mp[r["skill"]]
        return obj
    if kind == "dict-key":
        return {mp.get(k, k): v for k, v in obj.items()}
    if kind == "cluster":
        for g in obj:
            g["skills"] = [mp.get(s, s) for s in g["skills"]]
        return obj
    if kind == "match":
        for c in obj.get("corpus", []):
            if c.get("skill") in mp:
                c["skill"] = mp[c["skill"]]
        return obj
    raise ValueError(kind)


def main():
    check = "--check" in sys.argv
    mp, unresolved, amb, perline, split = build_map()
    print(f"{len(amb)} repositories hold more than one loose-file entry")
    print(f"{sum(1 for x in perline if x)} pass2 lines get a new key, "
          f"{len(unresolved)} could not be resolved")
    print(f"{len(mp)} old keys carried downstream; {len(split)} of them were two "
          f"files under one name, resolved to the line the dedup kept")
    for s in split:
        print(f"  split: {s} -> {mp[s]}")
    for s in unresolved[:5]:
        print(f"  unresolved: {s}")
    if not mp and not any(perline):
        return

    # pass2 is renamed by position, so two lines that shared a name can part.
    p = RUNS / "pass2.jsonl"
    lines = p.read_text().splitlines()
    out, n = [], 0
    for line, new in zip(lines, perline):
        r = json.loads(line)
        if new and r["skill"] != new:
            r["skill"] = new
            n += 1
        out.append(json.dumps(r, ensure_ascii=False))
    print(f"  {'pass2.jsonl':26} {n:4} of {len(lines)} (by line)")
    touched = n
    if not check and n:
        shutil.copy(p, p.with_suffix(p.suffix + ".pre-migrate"))
        p.write_text("\n".join(out) + "\n")

    for name in LINE_FILES:
        if name == "pass2.jsonl":
            continue
        p = RUNS / name
        if not p.exists():
            continue
        lines = p.read_text().splitlines()
        out, n = [], 0
        for line in lines:
            r = json.loads(line)
            if r.get("skill") in mp:
                r["skill"] = mp[r["skill"]]
                n += 1
            out.append(json.dumps(r, ensure_ascii=False))
        print(f"  {name:26} {n:4} of {len(lines)}")
        touched += n
        if not check and n:
            shutil.copy(p, p.with_suffix(p.suffix + ".pre-migrate"))
            p.write_text("\n".join(out) + "\n")

    for name, kind in DOC_FILES.items():
        p = RUNS / name
        if not p.exists():
            continue
        if kind == "cluster-lines":
            lines = p.read_text().splitlines()
            out, n = [], 0
            for line in lines:
                r = json.loads(line)
                before = json.dumps(r.get("skills"), ensure_ascii=False)
                if "skills" in r:
                    r["skills"] = [mp.get(s, s) for s in r["skills"]]
                    n += before != json.dumps(r["skills"], ensure_ascii=False)
                out.append(json.dumps(r, ensure_ascii=False))
            print(f"  {name:26} {n:4} of {len(lines)} (nested)")
            if not check and n:
                shutil.copy(p, p.with_suffix(p.suffix + ".pre-migrate"))
                p.write_text("\n".join(out) + "\n")
            continue
        raw = p.read_text()
        obj = rewrite(json.loads(raw), kind, mp)
        new = json.dumps(obj, ensure_ascii=False)
        changed = new != json.dumps(json.loads(raw), ensure_ascii=False)
        print(f"  {name:26} {'changed' if changed else 'unchanged'}")
        if not check and changed:
            shutil.copy(p, p.with_suffix(p.suffix + ".pre-migrate"))
            p.write_text(new)

    print(f"\n{'would rewrite' if check else 'rewrote'} {touched} keyed records"
          + ("" if check else "; originals kept as *.pre-migrate"))


main()
