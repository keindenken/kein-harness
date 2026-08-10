#!/usr/bin/env python3
"""Harvest SKILL.md files from GitHub into a local corpus.

Three stages, ordered by what they cost:

  repos   search/repositories, 30 requests/minute, so this is the throttled part
  trees   one core request per repo returns every path it holds; 5000/hour
  raw     raw.githubusercontent, not rate limited at all

Commit depth is deliberately not collected here. It costs one core request per
file and is only worth spending on a shortlist, so `history.py` does it after
classification has narrowed the set.

Usage:
  ./harvest.py repos          # stage 1, writes repos.json
  ./harvest.py trees          # stage 2, writes files.json
  ./harvest.py raw            # stage 3, writes corpus/ and index.json
  ./harvest.py all
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus"

# Two bands of query. The first finds skill collections as such; the second
# reaches the domains this harness has no skill for, which is where a
# non-derivable specialist claim would have to come from.
QUERIES = [
    "topic:claude-skills",
    "topic:claude-code-skills",
    "topic:agent-skills",
    "topic:claude-code",
    "topic:skills topic:ai",
    '"SKILL.md" in:readme',
    "claude skills in:name,description",
    "agent skills in:name,description",
    "skills writing in:name,description",
    "skills documentation in:name,description",
    "skills product management in:name,description",
    "skills research in:name,description",
    "prompts library in:name,description agent",
]

PER_QUERY = 60          # top N by stars from each query
MIN_STARS = 3           # below this a repo is one person's afternoon
MAX_SKILL_BYTES = 60000  # a SKILL.md larger than this is a book, fetch anyway but flag

# Skill count per repository is an inverted quality signal. The measured
# distribution over 434 repositories has a median of 9 and a maximum of 23,793;
# a person writes the first number and a generator writes the second. Repos at
# or under the cap are taken whole, and larger ones are sampled only far enough
# to tell what they are.
HUMAN_SCALE = 50
SAMPLE_FROM_LARGE = 12


def gh(path, paginate=False):
    cmd = ["gh", "api", path]
    if paginate:
        cmd.append("--paginate")
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        return None, out.stderr.strip()
    return json.loads(out.stdout), None


def stage_repos():
    seen = {}
    for i, q in enumerate(QUERIES):
        url = f"search/repositories?q={urllib.parse.quote(q)}&sort=stars&order=desc&per_page={PER_QUERY}"
        data, err = gh(url)
        if err:
            print(f"  ! {q}: {err}", file=sys.stderr)
            continue
        got = 0
        for r in data.get("items", []):
            if r["stargazers_count"] < MIN_STARS:
                continue
            if r["full_name"] in seen:
                seen[r["full_name"]]["queries"].append(q)
                continue
            seen[r["full_name"]] = {
                "full_name": r["full_name"],
                "stars": r["stargazers_count"],
                "description": r.get("description") or "",
                "pushed_at": r.get("pushed_at"),
                "created_at": r.get("created_at"),
                "default_branch": r.get("default_branch") or "main",
                "topics": r.get("topics", []),
                "archived": r.get("archived", False),
                "queries": [q],
            }
            got += 1
        print(f"  {q}: total {data.get('total_count')}, kept {got}, corpus {len(seen)}")
        if i < len(QUERIES) - 1:
            time.sleep(2.5)  # 30/min ceiling on the search endpoint

    repos = sorted(seen.values(), key=lambda r: -r["stars"])
    (HERE / "repos.json").write_text(json.dumps(repos, indent=1))
    print(f"stage repos: {len(repos)} repositories")


def _tree(repo):
    name, branch = repo["full_name"], repo["default_branch"]
    data, err = gh(f"repos/{name}/git/trees/{branch}?recursive=1")
    if err:
        return name, [], err
    hits = []
    for n in data.get("tree", []):
        if n["type"] != "blob":
            continue
        base = n["path"].rsplit("/", 1)[-1]
        if base in ("SKILL.md", "AGENTS.md", "CLAUDE.md"):
            hits.append({"repo": name, "branch": branch, "path": n["path"],
                         "size": n.get("size", 0), "kind": base})
    return name, hits, ("truncated" if data.get("truncated") else None)


def stage_trees():
    repos = json.loads((HERE / "repos.json").read_text())
    files, notes = [], {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        for name, hits, note in pool.map(_tree, repos):
            files.extend(hits)
            if note:
                notes[name] = note
    (HERE / "files.json").write_text(json.dumps(files, indent=1))
    skills = sum(1 for f in files if f["kind"] == "SKILL.md")
    print(f"stage trees: {len(files)} instruction files, {skills} of them SKILL.md")
    if notes:
        print(f"  notes: {json.dumps(notes)}")


FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)


def _frontmatter(text):
    m = FRONTMATTER.match(text)
    if not m:
        return {}
    out, key = {}, None
    for line in m.group(1).splitlines():
        fm = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if fm:
            key = fm.group(1)
            out[key] = fm.group(2).strip().strip("'\"")
        elif key and line.startswith((" ", "\t")):
            out[key] = (out[key] + " " + line.strip()).strip()
    return out


def _slug(repo, path):
    return (repo + "__" + path).replace("/", "_")


def _fetch(f):
    url = f"https://raw.githubusercontent.com/{f['repo']}/{f['branch']}/{urllib.parse.quote(f['path'])}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            text = r.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return None, f"{f['repo']}/{f['path']}: {e}"
    fm = _frontmatter(text)
    dest = CORPUS / _slug(f["repo"], f["path"])
    dest.write_text(text)
    return {
        **f,
        "file": dest.name,
        "words": len(text.split()),
        "name": fm.get("name", ""),
        "description": fm.get("description", ""),
        "has_frontmatter": bool(fm),
        "oversized": len(text.encode()) > MAX_SKILL_BYTES,
    }, None


def _select(files):
    """Take human-scale repositories whole; sample the generators."""
    by_repo = {}
    for f in files:
        by_repo.setdefault(f["repo"], []).append(f)
    picked, large = [], 0
    for repo, fs in by_repo.items():
        fs.sort(key=lambda f: f["path"])
        if len(fs) <= HUMAN_SCALE:
            picked.extend(fs)
        else:
            large += 1
            step = len(fs) / SAMPLE_FROM_LARGE
            picked.extend(fs[int(i * step)] for i in range(SAMPLE_FROM_LARGE))
    print(f"  {len(by_repo) - large} repos taken whole, {large} sampled -> {len(picked)} files")
    return picked


def stage_raw():
    files = json.loads((HERE / "files.json").read_text())
    files = _select([f for f in files if f["kind"] == "SKILL.md" and f["size"] > 0])
    CORPUS.mkdir(exist_ok=True)
    index, errs = [], []
    with ThreadPoolExecutor(max_workers=16) as pool:
        for rec, err in pool.map(_fetch, files):
            (index.append(rec) if rec else errs.append(err))
    index.sort(key=lambda r: (r["repo"], r["path"]))
    (HERE / "index.json").write_text(json.dumps(index, indent=1))
    print(f"stage raw: {len(index)} fetched, {len(errs)} failed")
    for e in errs[:5]:
        print(f"  ! {e}", file=sys.stderr)


if __name__ == "__main__":
    stages = {"repos": stage_repos, "trees": stage_trees, "raw": stage_raw}
    want = sys.argv[1:] or ["all"]
    for s in (list(stages) if want == ["all"] else want):
        print(f"== {s}")
        stages[s]()
