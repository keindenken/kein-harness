#!/usr/bin/env python3
"""Harvest UI/UX designer agent definitions from GitHub into a local corpus.

A sibling of 260926-github-agents, which harvested writing roles. This one looks for
agent definitions whose name says the agent designs interfaces: UI/UX designer,
design system, visual or brand designer, accessibility, interaction, prototyping,
and the design reviewers too, since a designer's output can be a written critique.
The writer harvest's repositories seed the repo list, so the same collections are
walked again with a different filename filter.

Two ways in, because agent files live in two kinds of repository:

  repos   search/repositories for agent collections (30 requests/minute), then
          one tree request per repository (core, 5000/hour) to list its files
  code    search/code for writing-role filenames under agent directories
          (10 requests/minute), which reaches repositories no topic names

Then `raw` fetches every candidate from raw.githubusercontent (not rate limited),
and `dedupe` collapses byte-identical copies, which collections copy freely.

Usage:
  ./harvest.py repos trees code raw dedupe
"""

import hashlib
import json
import re
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus"
# The python.org build ships without a CA bundle wired in, so every raw fetch failed certificate checks; the system bundle is the fix.
TLS = ssl.create_default_context(cafile="/etc/ssl/cert.pem")

REPO_QUERIES = [
    "topic:claude-code-subagents",
    "topic:claude-subagents",
    "topic:subagents",
    "topic:claude-code-agents",
    "topic:claude-agents",
    "topic:ai-agents claude",
    "topic:claude-code",
    "topic:opencode",
    "topic:codex-cli",
    "topic:github-copilot agents",
    "subagents in:name,description",
    "claude code agents in:name,description",
    "custom agents in:name,description copilot",
    "codex agents in:name,description",
    "opencode agents in:name,description",
    "agent prompts in:name,description",
    "writing agents in:name,description",
    "ui ux agent in:name,description",
    "design agent claude in:name,description",
    "designer agent in:name,description",
    "design system agent in:name,description",
    "frontend design claude in:name,description",
    "topic:design-systems claude",
    "topic:ui-design ai-agents",
]
PER_QUERY = 60
MIN_STARS = 3

# Filenames that say the agent's job is design. Deliberately wide; the reading pass decides.
WRITING = re.compile(
    r"(design|(?:^|[-_.])ui(?:[-_.]|$)|(?:^|[-_.])ux(?:[-_.]|$)|uiux|ui-ux|visual|brand|style-?guide|"
    r"tailwind|css|figma|a11y|accessib|interaction|motion|animat|typograph|colou?r|layout|"
    r"prototyp|mockup|wirefram|frontend|front-end|landing|component|design-?tokens?|(?:^|[-_])tokens?(?:[-_.]|$)|theme|usability|polish)",
    re.I,
)
NOT_WRITING = re.compile(r"(code-?review|test|lint|debug|security|deploy|infra|sql|database|backend|devops|pentest)", re.I)

# Where runtimes look for agent definitions.
AGENT_DIR = re.compile(
    r"(^|/)(\.claude/agents|agents|agent|subagents|sub-agents|\.opencode/agents?|\.github/agents|"
    r"\.codex/agents|\.factory/droids|droids|\.cursor/agents|\.gemini/agents|\.kiro/agents)(/|$)",
    re.I,
)
AGENT_EXT = (".md", ".toml", ".yaml", ".yml")

CODE_QUERIES = [
    f"filename:{name} path:{d}"
    for d in ("agents", ".claude/agents", ".github/agents", ".opencode/agent", ".codex/agents")
    for name in ("designer", "ui-designer", "ux-designer", "ui-ux", "design-system", "frontend-design", "accessibility", "ux")
] + [
    'path:.claude/agents "UI/UX"',
    'path:.claude/agents "you are a designer"',
    'path:.claude/agents "design system" "you are"',
    'path:.github/agents "UI/UX"',
    'path:agents "UX designer"',
    'path:agents "visual design" "you are"',
    'path:agents "design tokens"',
    'path:agents "WCAG" "you are" designer',
]

MAX_PER_REPO = 40  # a collection with hundreds of writer files is a generator, sample it


def gh(path):
    out = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if out.returncode != 0:
        return None, out.stderr.strip()[:200]
    return json.loads(out.stdout), None


def is_candidate(path):
    base = path.rsplit("/", 1)[-1]
    stem = base.rsplit(".", 1)[0]
    if not base.lower().endswith(AGENT_EXT) or base.upper() in ("README.MD", "AGENTS.MD", "CLAUDE.MD", "INDEX.MD"):
        return False
    if not AGENT_DIR.search(path.rsplit("/", 1)[0] + "/"):
        return False
    return bool(WRITING.search(stem)) and not NOT_WRITING.search(stem)


def stage_repos():
    seed = HERE.parent / "260926-github-agents" / "repos.json"
    seen = {r["full_name"]: r for r in json.loads(seed.read_text())} if seed.exists() else {}
    for i, q in enumerate(REPO_QUERIES):
        data, err = gh(f"search/repositories?q={urllib.parse.quote(q)}&sort=stars&order=desc&per_page={PER_QUERY}")
        if err:
            print(f"  ! {q}: {err}", file=sys.stderr)
        else:
            got = 0
            for r in data.get("items", []):
                if r["stargazers_count"] < MIN_STARS:
                    continue
                if r["full_name"] in seen:
                    seen[r["full_name"]]["queries"].append(q)
                    continue
                seen[r["full_name"]] = {"full_name": r["full_name"], "stars": r["stargazers_count"],
                                        "description": r.get("description") or "", "pushed_at": r.get("pushed_at"),
                                        "default_branch": r.get("default_branch") or "main", "queries": [q]}
                got += 1
            print(f"  {q}: total {data.get('total_count')}, new {got}, corpus {len(seen)}")
        time.sleep(2.5)
    repos = sorted(seen.values(), key=lambda r: -r["stars"])
    (HERE / "repos.json").write_text(json.dumps(repos, indent=1))
    print(f"stage repos: {len(repos)} repositories")


def _tree(repo):
    data, err = gh(f"repos/{repo['full_name']}/git/trees/{repo['default_branch']}?recursive=1")
    if err:
        return repo, [], err
    hits = [{"repo": repo["full_name"], "ref": repo["default_branch"], "path": n["path"], "size": n.get("size", 0),
             "stars": repo["stars"], "via": "tree"}
            for n in data.get("tree", []) if n["type"] == "blob" and is_candidate(n["path"])]
    return repo, hits, ("truncated" if data.get("truncated") else None)


def stage_trees():
    repos = json.loads((HERE / "repos.json").read_text())
    files, notes = [], {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        for repo, hits, note in pool.map(_tree, repos):
            files.extend(hits)
            if note:
                notes[repo["full_name"]] = note
    (HERE / "files-tree.json").write_text(json.dumps(files, indent=1))
    print(f"stage trees: {len(files)} candidates from {len({f['repo'] for f in files})} repositories; notes {len(notes)}")


def stage_code():
    found, stars = {}, {}
    for i, q in enumerate(CODE_QUERIES):
        for page in (1, 2, 3):
            data, err = gh(f"search/code?q={urllib.parse.quote(q)}&per_page=100&page={page}")
            time.sleep(6.5)  # 10/minute on code search
            if err:
                print(f"  ! {q} p{page}: {err}", file=sys.stderr)
                break
            items = data.get("items", [])
            for it in items:
                repo, path = it["repository"]["full_name"], it["path"]
                if not is_candidate(path):
                    continue
                ref = it["html_url"].split("/blob/", 1)[1].split("/", 1)[0]
                found[(repo, path)] = {"repo": repo, "ref": ref, "path": path, "size": 0, "via": "code"}
            if len(items) < 100:
                break
        print(f"  {q}: corpus {len(found)}")
    # The writer harvest looked these up one at a time and spent most of the stage here.
    def _stars(repo):
        data, _ = gh(f"repos/{repo}")
        return repo, (data or {}).get("stargazers_count", 0)
    with ThreadPoolExecutor(max_workers=8) as pool:
        stars = dict(pool.map(_stars, {r for r, _ in found}))
    files = [dict(f, stars=stars.get(f["repo"], 0)) for f in found.values()]
    (HERE / "files-code.json").write_text(json.dumps(files, indent=1))
    print(f"stage code: {len(files)} candidates from {len(stars)} repositories")


def _fetch(f):
    url = f"https://raw.githubusercontent.com/{f['repo']}/{f['ref']}/{urllib.parse.quote(f['path'])}"
    try:
        with urllib.request.urlopen(url, timeout=30, context=TLS) as r:
            text = r.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return None, f"{f['repo']}/{f['path']}: {e}"
    slug = (f["repo"] + "__" + f["path"]).replace("/", "_")
    (CORPUS / slug).write_text(text)
    return dict(f, file=slug, words=len(text.split()), sha=hashlib.sha256(text.encode()).hexdigest()), None


def stage_raw():
    merged = {}
    for name in ("files-tree.json", "files-code.json"):
        p = HERE / name
        if p.exists():
            for f in json.loads(p.read_text()):
                merged.setdefault((f["repo"], f["path"]), f)
    by_repo = {}
    for f in merged.values():
        by_repo.setdefault(f["repo"], []).append(f)
    picked = []
    for fs in by_repo.values():
        fs.sort(key=lambda f: f["path"])
        step = max(1, len(fs) / MAX_PER_REPO)
        picked.extend(fs[int(i * step)] for i in range(min(len(fs), MAX_PER_REPO)))
    CORPUS.mkdir(exist_ok=True)
    index, errs = [], []
    with ThreadPoolExecutor(max_workers=16) as pool:
        for rec, err in pool.map(_fetch, picked):
            (index.append(rec) if rec else errs.append(err))
    (HERE / "index.json").write_text(json.dumps(sorted(index, key=lambda r: (r["repo"], r["path"])), indent=1))
    print(f"stage raw: {len(index)} fetched from {len(by_repo)} repositories, {len(errs)} failed")


def stage_dedupe():
    index = json.loads((HERE / "index.json").read_text())
    groups = {}
    for r in index:
        norm = hashlib.sha256(re.sub(r"\s+", " ", (CORPUS / r["file"]).read_text()).strip().lower().encode()).hexdigest()
        groups.setdefault(norm, []).append(r)
    unique = []
    for members in groups.values():
        members.sort(key=lambda r: -r.get("stars", 0))
        head = dict(members[0], copies=[f"{m['repo']}/{m['path']}" for m in members[1:]])
        unique.append(head)
    unique.sort(key=lambda r: -r.get("stars", 0))
    (HERE / "unique.json").write_text(json.dumps(unique, indent=1))
    print(f"stage dedupe: {len(index)} files -> {len(unique)} distinct texts")


if __name__ == "__main__":
    stages = {"repos": stage_repos, "trees": stage_trees, "code": stage_code, "raw": stage_raw, "dedupe": stage_dedupe}
    for s in sys.argv[1:] or list(stages):
        print(f"== {s}")
        stages[s]()
