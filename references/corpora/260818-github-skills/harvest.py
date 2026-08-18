#!/usr/bin/env python3
"""Harvest skill directories from GitHub, whole rather than one file each.

What changed from 260811, and why.

**A skill is a directory, not a file.** That harvest kept three basenames and
threw the rest of every tree away, so no `references/` or `scripts/` file was
ever fetched. Its own strongest finding was that prompts shrink by *relocation* —
the obligation moves down a level and the run still reads it — measured entirely
on files that do not contain the level it moves to. A survey of 2,239 skill
directories found 51% hold something besides `SKILL.md`, and only 47% of those
siblings are Markdown: `.py` is 32%, and there are fonts, spreadsheets and
images that no text corpus can carry at all.

**The tree is mirrored, not flattened.** 260811 stored `owner_repo__a_b_c.md` in
one directory, which cannot represent `references/` at all once it exists. Paths
here mirror upstream, so a skill's siblings sit where the author put them and the
level a sentence lives at is still readable.

**Every file records the commit it came from.** 260811 states plainly that
re-running it will not reproduce its corpus. With a SHA per file the next round
diffs instead of re-harvesting, and a claim can be traced to the bytes it was
read from.

Binaries are recorded and not downloaded. Their existence is the signal — a
skill that ships a `.ttf` is doing something a skill that ships prose is not —
and their bytes answer no question here.

Usage:
  ./harvest.py repos                 # search, writes repos.json
  ./harvest.py trees                 # one request per repo, writes skills.json
  ./harvest.py fetch [--workers N]   # writes corpus/ and manifest.json
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus"

# 260811 took the top 60 of each query by stars, which set every floor at a
# different height: `"SKILL.md" in:readme` was cut at 27,275 stars and
# `skills product management` exhausted itself at 51 results. The first number
# means a whole band of large repositories was never seen; the second means the
# vocabulary, not the depth, is what limits the specialist end. Both are
# addressed here — deeper pages, and more ways to ask.
QUERIES = [
    # collections as such
    "topic:claude-skills", "topic:claude-code-skills", "topic:agent-skills",
    "topic:claude-code", "topic:skills topic:ai", "topic:ai-agents topic:skills",
    '"SKILL.md" in:readme', '"AGENTS.md" in:readme',
    "claude skills in:name,description", "agent skills in:name,description",
    "skill library in:name,description", "prompts library in:name,description agent",
    # domains this harness has no skill for, where a non-derivable claim would
    # have to come from someone who does the work
    "skills writing in:name,description", "skills documentation in:name,description",
    "skills product management in:name,description", "skills research in:name,description",
    "skills design in:name,description", "skills marketing in:name,description",
    "skills legal in:name,description", "skills medical in:name,description",
    "skills finance in:name,description", "skills data analysis in:name,description",
    "skills security in:name,description", "skills devops in:name,description",
    "skills education in:name,description", "skills science in:name,description",
]

PAGES = 3            # 100 per page; GitHub caps any query at 1000 results
MIN_STARS = 3
HUMAN_SCALE = 60     # skills per repo above which a generator, not a person, wrote them
SAMPLE_FROM_LARGE = 15
LOOSE_SCALE = 15     # `AGENTS.md` files per repo past which it is one convention repeated
SAMPLE_FROM_LOOSE = 8

# Downloaded when a skill directory holds them. Everything else is recorded in
# the manifest by path and size and left upstream.
TEXT_EXT = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".sh", ".bash", ".zsh",
            ".py", ".ts", ".js", ".mjs", ".cjs", ".rb", ".go", ".rs", ".sql",
            ".xml", ".xsd", ".csv", ".tsv", ".html", ".css", ".env.example"}
MAX_FILE_BYTES = 250_000   # one sibling above this is a data dump, not an instruction
# Only `SKILL.md` marks a directory. `AGENTS.md` and `CLAUDE.md` are instructions
# scoped to a subtree, not bundles that own it: `langgenius/dify` carries
# `web/AGENTS.md`, and treating that as a skill handed one record 7,428 source
# files. Both are still collected, one file each, wherever they sit.
DIR_ANCHOR = "SKILL.md"
LOOSE_ANCHORS = ("AGENTS.md", "CLAUDE.md")
# A skill directory above this is not a bundled skill; it is a project that
# happens to hold one. Recorded rather than dropped, so the shape stays visible.
MAX_SKILL_FILES = 250
# Directory names that are never part of a skill, however deep inside one they sit.
NOT_SOURCE = {"node_modules", ".git", "vendor", "dist", "build", "__pycache__",
              ".venv", "venv", "target", ".next", "coverage"}


_LIMIT_LOCK = __import__("threading").Lock()


def _wait_for_core():
    """Block until the core quota is usable again.

    5,065 repositories is one tree request each against a 5,000/hour ceiling, so
    a run that does not wait fails on its last sixty and loses the other five
    thousand with it.
    """
    with _LIMIT_LOCK:
        out = subprocess.run(["gh", "api", "rate_limit"], capture_output=True, text=True)
        if out.returncode != 0:
            time.sleep(60)
            return
        core = json.loads(out.stdout)["resources"]["core"]
        if core["remaining"] > 20:
            return
        nap = max(30, core["reset"] - int(time.time()) + 5)
        print(f"  core exhausted, sleeping {nap // 60}m{nap % 60}s", flush=True)
        time.sleep(nap)


def gh(path, retries=3):
    for attempt in range(retries):
        out = subprocess.run(["gh", "api", path], capture_output=True, text=True)
        if out.returncode == 0:
            return json.loads(out.stdout), None
        err = out.stderr.strip()
        if "rate limit" in err.lower() or "API rate limit" in err:
            _wait_for_core()
            continue
        if attempt < retries - 1 and ("timeout" in err.lower() or "connection" in err.lower()):
            time.sleep(2 * (attempt + 1))
            continue
        return None, err[:200]
    return None, "rate limited after retries"


def stage_repos():
    seen = {}
    for i, q in enumerate(QUERIES):
        kept_before, total = len(seen), "?"
        for page in range(1, PAGES + 1):
            url = (f"search/repositories?q={urllib.parse.quote(q)}"
                   f"&sort=stars&order=desc&per_page=100&page={page}")
            data, err = gh(url)
            if err:
                print(f"  ! {q} p{page}: {err}", file=sys.stderr)
                break
            items = data.get("items", [])
            total = data.get("total_count", "?")
            for r in items:
                if r["stargazers_count"] < MIN_STARS:
                    continue
                fn = r["full_name"]
                if fn in seen:
                    seen[fn]["queries"].append(q)
                    continue
                seen[fn] = {
                    "full_name": fn, "stars": r["stargazers_count"],
                    "description": r.get("description") or "",
                    "pushed_at": r.get("pushed_at"), "created_at": r.get("created_at"),
                    "default_branch": r.get("default_branch") or "main",
                    "topics": r.get("topics", []), "archived": r.get("archived", False),
                    "queries": [q],
                }
            if len(items) < 100:
                break
            time.sleep(2.2)   # 30/min ceiling on the search endpoint
        print(f"  {q[:46]:46} total {total:>7}  new {len(seen)-kept_before:4}  corpus {len(seen)}", flush=True)
        time.sleep(2.2)
    repos = sorted(seen.values(), key=lambda r: -r["stars"])
    (HERE / "repos.json").write_text(json.dumps(repos, indent=1))
    print(f"stage repos: {len(repos)} repositories")


def _tree(repo):
    """Return every skill directory in one repository, with all of its files.

    The tree call already returns the whole repository; 260811 discarded all but
    three basenames from the same response.
    """
    name, branch = repo["full_name"], repo["default_branch"]
    data, err = gh(f"repos/{name}/git/trees/{branch}?recursive=1")
    if err:
        return name, [], err
    blobs = [n for n in data.get("tree", []) if n["type"] == "blob"]
    anchors = [n["path"] for n in blobs
               if n["path"].rsplit("/", 1)[-1] == DIR_ANCHOR and "/" in n["path"]]
    # A skill directory is one holding an anchor file. Nested anchors mean the
    # inner one owns its subtree, so the outer does not claim it.
    #
    # The repository root is never a skill directory even when a `CLAUDE.md`
    # sits there. A root anchor is a repository-level instruction file, and
    # treating it as a skill hands it every path no inner skill claimed:
    # `trailofbits/skills` gave the root 570 files, `.github/` and all.
    dirs = sorted({p.rsplit("/", 1)[0] for p in anchors})
    owned, oversized = {}, []
    for d in dirs:
        prefix = d + "/"
        inner = [x for x in dirs if x != d and (x + "/").startswith(prefix)]
        files = []
        for n in blobs:
            p = n["path"]
            if not p.startswith(prefix):
                continue
            if any(p.startswith(x + "/") for x in inner):
                continue
            if any(seg in NOT_SOURCE for seg in p[len(prefix):].split("/")[:-1]):
                continue
            files.append({"path": p, "size": n.get("size", 0), "sha": n["sha"]})
        if len(files) > MAX_SKILL_FILES:
            keep = [f for f in files
                    if f["path"].rsplit("/", 1)[-1] == DIR_ANCHOR
                    or f["path"].lower().endswith((".md", ".txt"))][:MAX_SKILL_FILES]
            owned[d] = keep or files[:MAX_SKILL_FILES]
            oversized.append((d, len(files)))
            continue
        if files:
            owned[d] = files
    skills = [{"repo": name, "branch": branch, "dir": d, "files": f,
               **({"trimmed_from": dict(oversized)[d]} if d in dict(oversized) else {})}
              for d, f in owned.items()]
    # Directory-scoped instruction files are kept as themselves, one file each,
    # at whatever depth they sit. They are the subject, not their neighbours.
    for n in blobs:
        base = n["path"].rsplit("/", 1)[-1]
        if base in LOOSE_ANCHORS and not any(seg in NOT_SOURCE for seg in n["path"].split("/")[:-1]):
            skills.append({"repo": name, "branch": branch, "dir": n["path"].rsplit("/", 1)[0] if "/" in n["path"] else "",
                           "loose_file": base,
                           "files": [{"path": n["path"], "size": n.get("size", 0), "sha": n["sha"]}]})
    return name, skills, ("truncated" if data.get("truncated") else None)


def stage_trees():
    """Walk every repository's tree, appending as it goes so a stop is resumable."""
    repos = json.loads((HERE / "repos.json").read_text())
    raw = HERE / "trees.jsonl"
    seen = set()
    if raw.exists():
        for line in raw.read_text().splitlines():
            try:
                seen.add(json.loads(line)["repo"])
            except Exception:
                pass
    todo = [r for r in repos if r["full_name"] not in seen]
    print(f"{len(repos)} repositories, {len(seen)} already walked, {len(todo)} to go", flush=True)
    notes = {}
    with raw.open("a") as fh, ThreadPoolExecutor(max_workers=8) as pool:
        for i, (name, skills, note) in enumerate(pool.map(_tree, todo), 1):
            fh.write(json.dumps({"repo": name, "skills": skills, "note": note}) + "\n")
            fh.flush()
            if note and note != "truncated":
                notes[name] = note
            if i % 200 == 0:
                print(f"  {i}/{len(todo)} repos", flush=True)
    out = []
    for line in raw.read_text().splitlines():
        rec = json.loads(line)
        out.extend(rec["skills"])
    # A repository holding hundreds of skills was generated, and 260811 measured
    # the count itself as an inverted quality signal: median 9, maximum 23,793.
    by_repo = defaultdict(lambda: ([], []))
    for s in out:
        by_repo[s["repo"]][1 if s.get("loose_file") else 0].append(s)

    def sample(ss, cap, take):
        ss.sort(key=lambda s: s["dir"])
        if len(ss) <= cap:
            return ss, False
        step = len(ss) / take
        return [ss[int(i * step)] for i in range(take)], True

    picked, sampled, loose_sampled = [], 0, 0
    for repo, (dirs, loose) in by_repo.items():
        got, cut = sample(dirs, HUMAN_SCALE, SAMPLE_FROM_LARGE)
        picked.extend(got)
        sampled += cut
        # A monorepo puts an `AGENTS.md` in every package: `elizaOS/eliza` has
        # 312. Past a point those are one convention repeated, not 312 readings.
        got, cut = sample(loose, LOOSE_SCALE, SAMPLE_FROM_LOOSE)
        picked.extend(got)
        loose_sampled += cut
    (HERE / "skills.json").write_text(json.dumps(picked, indent=1))
    files = sum(len(s["files"]) for s in picked)
    print(f"stage trees: {len(picked)} skills over {len(by_repo)} repositories, {files} files")
    d = sum(1 for s in picked if not s.get("loose_file"))
    print(f"  {d} skill directories, {len(picked)-d} loose instruction files")
    print(f"  sampled down: {sampled} repositories above {HUMAN_SCALE} skills, "
          f"{loose_sampled} above {LOOSE_SCALE} loose files")
    if notes:
        print(f"  truncated trees: {len(notes)}")


def _wanted(f):
    base = f["path"].rsplit("/", 1)[-1]
    ext = "." + base.rsplit(".", 1)[-1].lower() if "." in base else ""
    return ext in TEXT_EXT and f["size"] <= MAX_FILE_BYTES


def _fetch_skill(skill):
    got, skipped = [], []
    for f in skill["files"]:
        if not _wanted(f):
            skipped.append({**f, "reason": "binary" if f["size"] <= MAX_FILE_BYTES else "oversize"})
            continue
        url = (f"https://raw.githubusercontent.com/{skill['repo']}/"
               f"{skill['branch']}/{urllib.parse.quote(f['path'])}")
        dest = CORPUS / skill["repo"] / f["path"]
        if dest.exists() and dest.stat().st_size == f["size"]:
            got.append(f)
            continue
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                body = r.read()
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            skipped.append({**f, "reason": f"fetch: {e}"})
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        got.append(f)
    return {"repo": skill["repo"], "branch": skill["branch"], "dir": skill["dir"],
            "files": got, "not_fetched": skipped}


def stage_fetch(workers=12):
    skills = json.loads((HERE / "skills.json").read_text())
    CORPUS.mkdir(exist_ok=True)
    manifest, done = [], 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for rec in pool.map(_fetch_skill, skills):
            manifest.append(rec)
            done += 1
            if done % 200 == 0:
                print(f"  {done}/{len(skills)} skills", flush=True)
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=1))
    fetched = sum(len(m["files"]) for m in manifest)
    left = sum(len(m["not_fetched"]) for m in manifest)
    byte = sum(f["size"] for m in manifest for f in m["files"])
    print(f"stage fetch: {len(manifest)} skills, {fetched} files ({byte/1e6:.0f} MB), "
          f"{left} recorded but not downloaded")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "repos"
    w = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 12
    {"repos": stage_repos, "trees": stage_trees,
     "fetch": lambda: stage_fetch(w)}[cmd]()
