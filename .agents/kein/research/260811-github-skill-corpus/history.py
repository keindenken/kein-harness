#!/usr/bin/env python3
"""Rank skill files by how much they have been revised, and extract the diffs.

The premise, which this repository arrived at by accident: the most useful
thing found in an external corpus this year came from diffing three cached
releases of one vendor's prompts, not from reading any file in them. A file
committed once is its author's first draft and contains only what they could
derive. A file revised twenty times was corrected by something, and the
correction is in the diff rather than in the current text.

Commit depth per path is expensive over the API — one request per file — and
free from a blobless clone, which fetches every commit and tree but no file
contents. So this clones, counts locally, and then fetches the blobs only for
the paths that turned out to be worth reading.

Usage:
  ./history.py clone [--workers N]   # blobless clones into .cache/
  ./history.py rank                  # writes history.json
  ./history.py diffs [--top N]       # writes diffs/<slug>.diff for the top N
"""

import json
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / ".cache"
DIFFS = HERE / "diffs"

CLONE_TIMEOUT = 300
# A blobless clone still carries every tree object, so a repository with a long
# history of a large working set is slow for no benefit here. Anything past this
# is skipped and recorded as skipped rather than silently dropped.
MAX_CLONE_MB = 400


def _repos():
    shortlist = json.loads((HERE / "shortlist.json").read_text())
    return sorted({r["repo"] for r in shortlist})


def _slug(repo):
    return repo.replace("/", "__")


def _clone(repo):
    dest = CACHE / _slug(repo)
    if (dest / "HEAD").exists():
        return repo, "cached"
    tmp = CACHE / (_slug(repo) + ".tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    p = subprocess.run(
        ["git", "clone", "--filter=blob:none", "--bare", "--single-branch",
         f"https://github.com/{repo}.git", str(tmp)],
        capture_output=True, text=True, timeout=CLONE_TIMEOUT)
    if p.returncode != 0:
        shutil.rmtree(tmp, ignore_errors=True)
        return repo, f"failed: {p.stderr.strip().splitlines()[-1][:100] if p.stderr.strip() else '?'}"
    mb = sum(f.stat().st_size for f in tmp.rglob("*") if f.is_file()) / 1e6
    if mb > MAX_CLONE_MB:
        shutil.rmtree(tmp, ignore_errors=True)
        return repo, f"skipped: {mb:.0f}MB"
    tmp.rename(dest)
    return repo, f"ok {mb:.1f}MB"


def clone(workers=6):
    CACHE.mkdir(exist_ok=True)
    repos = _repos()
    counts = defaultdict(int)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for i, (repo, status) in enumerate(pool.map(_clone, repos), 1):
            counts[status.split(":")[0].split()[0]] += 1
            if not status.startswith(("ok", "cached")):
                print(f"  ! {repo}: {status}", flush=True)
            if i % 40 == 0:
                print(f"[{i}/{len(repos)}] {dict(counts)}", flush=True)
    print(f"clone: {dict(counts)}")


LOGSEP = "\x01"


def _walk(repo):
    """Per-path commit count, author spread, and lifespan, from one git log."""
    d = CACHE / _slug(repo)
    if not (d / "HEAD").exists():
        return repo, {}
    p = subprocess.run(
        ["git", "-C", str(d), "log", "--no-merges", "--name-only",
         f"--format={LOGSEP}%H %at %ae"],
        capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        return repo, {}
    stats = defaultdict(lambda: {"commits": 0, "authors": set(), "first": None, "last": None})
    ts = email = None
    for line in p.stdout.splitlines():
        if line.startswith(LOGSEP):
            parts = line[1:].split()
            if len(parts) >= 3:
                _, ts, email = parts[0], int(parts[1]), parts[2]
            continue
        path = line.strip()
        if not path.endswith("SKILL.md") or ts is None:
            continue
        s = stats[path]
        s["commits"] += 1
        s["authors"].add(email)
        s["last"] = ts if s["last"] is None else max(s["last"], ts)
        s["first"] = ts if s["first"] is None else min(s["first"], ts)
    return repo, {k: {"commits": v["commits"], "authors": len(v["authors"]),
                      "first": v["first"], "last": v["last"],
                      "span_days": round((v["last"] - v["first"]) / 86400, 1)}
                  for k, v in stats.items()}


def rank():
    shortlist = json.loads((HERE / "shortlist.json").read_text())
    repos = _repos()
    hist = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        for repo, stats in pool.map(_walk, repos):
            hist[repo] = stats

    out, missing = [], 0
    for r in shortlist:
        s = hist.get(r["repo"], {}).get(r["path"])
        if s is None:
            missing += 1
        out.append({**{k: r[k] for k in ("file", "repo", "path", "name", "words",
                                         "specificity", "shape", "band", "stratum")},
                    "commits": (s or {}).get("commits", 0),
                    "authors": (s or {}).get("authors", 0),
                    "span_days": (s or {}).get("span_days", 0),
                    "in_clone": s is not None})
    out.sort(key=lambda r: (-r["commits"], -r["specificity"]))
    (HERE / "history.json").write_text(json.dumps(out, indent=1))

    seen = [r for r in out if r["in_clone"]]
    print(f"rank: {len(seen)}/{len(out)} resolved, {missing} not in a clone")
    if seen:
        c = [r["commits"] for r in seen]
        c.sort()
        print(f"  commits per file: median {c[len(c)//2]}, p90 {c[int(len(c)*.9)]}, max {c[-1]}")
        print(f"  revised more than once: {sum(1 for x in c if x > 1)}/{len(c)}")
        print("\n  most revised:")
        for r in seen[:15]:
            print(f"    {r['commits']:4d}c {r['authors']:3d}a {r['span_days']:7.0f}d  "
                  f"{r['name'][:28]:28} {r['repo'][:34]}")


def diffs(top=60):
    hist = json.loads((HERE / "history.json").read_text())
    DIFFS.mkdir(exist_ok=True)
    picked = [r for r in hist if r["in_clone"] and r["commits"] >= 3][:top]
    for r in picked:
        d = CACHE / _slug(r["repo"])
        p = subprocess.run(
            ["git", "-C", str(d), "log", "--no-merges", "--reverse", "-p",
             "--format=%n=== %h %ad %an%n%s%n", "--date=short", "--", r["path"]],
            capture_output=True, text=True, errors="replace", timeout=300)
        if p.returncode == 0 and p.stdout.strip():
            (DIFFS / (r["file"].replace(".md", "") + ".diff")).write_text(p.stdout)
    print(f"diffs: wrote {len(picked)} histories to diffs/")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "rank"
    n = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 6
    t = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 60
    {"clone": lambda: clone(n), "rank": rank, "diffs": lambda: diffs(t)}[cmd]()
