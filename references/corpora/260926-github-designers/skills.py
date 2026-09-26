#!/usr/bin/env python3
"""Pull UI design skills out of the 260818 skill corpus's provenance and fetch them.

Design craft turned out to live in skills as much as in agents, so the SKILL.md files whose directory name reads as
UI work are fetched alongside the agents. The name filter here is wide on purpose; pick.py narrows it.

Files are fetched from each repository's current HEAD, not the commit the skill corpus saw, because the provenance
records blob hashes rather than commits. So a rerun can see newer text, and only SKILL.md is taken: a skill's
references/ directory, where several keep most of their substance, is not.

Usage: ./skills.py select fetch
"""
import csv, hashlib, json, re, ssl, sys, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HERE = Path(__file__).resolve().parent
TLS = ssl.create_default_context(cafile="/etc/ssl/cert.pem")
UI = re.compile(r"(frontend|front-end|(?:^|[-_/])ui(?:[-_/]|$)|(?:^|[-_/])ux(?:[-_/]|$)|ui-?ux|web-?design|design-?system|design-?eng|a11y|"
                r"accessib|figma|tailwind|taste|brand|(?:^|[-_/])css|landing|interface|typograph|colou?r|motion|animation|prototyp|"
                r"mockup|wirefram|canvas-design|visual-design|shadcn|component)", re.I)
NOT = re.compile(r"(api|database|schema|distributed|experiment|eval|metric|protocol|research|graphviz|video|test|backend|sprite|email|"
                 r"advocacy|category|agent-team)", re.I)


def stage_select():
    rows = csv.DictReader(open(HERE.parent / "260818-github-skills" / "provenance.tsv"), delimiter="\t")
    picked = [r for r in rows if r["path"].lower().endswith("skill.md") and "/" in r["path"]
              and UI.search(r["path"].rsplit("/", 2)[-2]) and not NOT.search(r["path"].rsplit("/", 2)[-2])]
    (HERE / "skills-selected.json").write_text(json.dumps(picked, indent=1))
    print(f"select: {len(picked)} skills")


def _get(r):
    url = f"https://raw.githubusercontent.com/{r['repo']}/HEAD/{urllib.parse.quote(r['path'])}"
    try:
        with urllib.request.urlopen(url, timeout=30, context=TLS) as f:
            text = f.read().decode("utf-8", "replace")
    except Exception:
        return None
    slug = (r["repo"] + "__" + r["path"]).replace("/", "_")
    (HERE / "corpus-skills" / slug).write_text(text)
    return dict(repo=r["repo"], path=r["path"], file=slug, words=len(text.split()), sha=hashlib.sha256(text.encode()).hexdigest())


def stage_fetch():
    (HERE / "corpus-skills").mkdir(exist_ok=True)
    selected = json.loads((HERE / "skills-selected.json").read_text())
    with ThreadPoolExecutor(16) as pool:
        got = [x for x in pool.map(_get, selected) if x]
    distinct = {}
    for x in got:
        distinct.setdefault(x["sha"], x)
    (HERE / "skills-index.json").write_text(json.dumps(list(distinct.values()), indent=1))
    print(f"fetch: {len(got)} of {len(selected)} fetched, {len(distinct)} distinct")


if __name__ == "__main__":
    stages = {"select": stage_select, "fetch": stage_fetch}
    for s in sys.argv[1:] or list(stages):
        stages[s]()
