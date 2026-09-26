#!/usr/bin/env python3
"""Pick the clusters and skills the extraction reads: popular, and named for UI/UX design.

Popular is the writer corpus's lesson: the tail read as domain content, not craft. Here that means copied into
more than one repository, or 100 stars and up. The name filter is an allowlist of design terms minus a denylist of
the other things "design" names (APIs, games, systems, experiments, curricula). Accessibility auditors,
frontend implementers and UX researchers are left out on purpose: each is its own specialist, and designer
roles that cover those concerns will say so in their own text.
"""
import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent

ALLOW = re.compile(r"(?:^|[-_.])(?:ui|ux|uiux|ux-ui|ui-ux)(?:[-_.]|$)|design|prototyp|mockup|wirefram|figma|brand-(?:designer|guardian)", re.I)
DENY = re.compile(
    r"api|game|level|sound|economy|narrative|character|plot|experiment|chaos|workflow|schema|architect(?!ure-?ui)|arch-|"
    r"system-?design|systems-designer|technical-designer|spec-design|acp|task-\d|milestone|yaml|learning|training|"
    r"curriculum|course|instructional|prompt|agent-design|self-distillation|resource|garden|title|profile|art-designer|"
    r"roblox|godot|unity|ba-designer|feature-designer|voice|benchmark|acceptance|sc2data|content-designer|ux-writer|"
    r"researcher|research|accessib|a11y|wcag|frontend-(?:dev|engineer|specialist|build|fix|implement)|"
    r"latex|pdf|word|excel|epub|powerpoint|markdown|document|dashboard-designer|live-ops|interactive-agent|plan-design|"
    r"yaml|parser|\.backup|template$|reference-system|design-reference|design-create|code-design|cross-reference",
    re.I,
)

# Read by name and description, then dropped: tool operation (Figma API, UI libraries' install-and-use guides),
# other meanings of the word (TypeScript types, API interfaces, prototype pollution, image colour grading, poster
# art), and one codebase's internals. What stays is craft a designer role could carry or point at.
DROP = re.compile(
    r"figma|shadcn|nuxt-ui|expo-ui$|compose-ui|swiftui-ui-patterns|react-ui-patterns|taro-ui|tailwind-4|ui-widget-developer|"
    r"json-ui|graph-colorize|top-value-coloring|color-correction|prototype-pollution|structs-interfaces|fix-interface|"
    r"validate-interface|design-an-interface|asc-app-create-ui|ux-writing|canvas-design|mockup-device|gui-settings-ui|"
    r"verify-ui-change|type-design-analyzer|ui-programmer|imports-design-system|maintainer-orchestrator|topics-ux-v2",
    re.I,
)


def stem(path):
    return re.sub(r"\.(agent|chatmode|spec|reference)$", "", path.rsplit("/", 1)[-1].rsplit(".", 1)[0].lower())

def is_design(name):
    return bool(ALLOW.search(name)) and not DENY.search(name) and not DROP.search(name)

if __name__ == "__main__":
    clusters = json.loads((HERE / "clusters.json").read_text())
    agents = []
    for i, c in enumerate(clusters):
        if (c["repos"] > 1 or c["stars"] >= 100) and is_design(stem(c["path"])):
            agents.append(dict(c, id=f"c{i:05d}", kind="agent"))
    skills = []
    for s in json.loads((HERE / "skills-index.json").read_text()):
        name = s["path"].rsplit("/", 2)[-2].lower()
        if is_design(name) or re.search(r"frontend-design|taste|tailwind|shadcn|css|typograph|colou?r|motion-design|interface|landing-page|visual-design", name):
            if not DROP.search(name) and (not DENY.search(name.replace("frontend-design", "")) or "frontend-design" in name):
                skills.append(dict(s, kind="skill", name=name))
    # Skills were never near-duplicate clustered in their own corpus: twelve copies of one frontend-design skill arrive as twelve texts.
    # Same rule as cluster.py (5-word shingles, Jaccard 0.6), exact here because 141 texts make the pairwise pass cheap; the longest copy is kept.
    shingles = []
    for s in skills:
        w = re.sub(r"\s+", " ", (HERE / "corpus-skills" / s["file"]).read_text().lower()).split()
        shingles.append({" ".join(w[i:i + 5]) for i in range(len(w) - 4)})
    parent = list(range(len(skills)))
    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i in range(len(skills)):
        for j in range(i + 1, len(skills)):
            a, b = shingles[i], shingles[j]
            if a and b and len(a & b) / len(a | b) >= 0.6:
                parent[root(i)] = root(j)
    groups = {}
    for i in range(len(skills)):
        groups.setdefault(root(i), []).append(i)
    kept = []
    for g in groups.values():
        g.sort(key=lambda i: -skills[i]["words"])
        kept.append(dict(skills[g[0]], copies=[skills[i]["repo"] + "/" + skills[i]["path"] for i in g[1:]]))
    skills = sorted(kept, key=lambda x: (-len(x["copies"]), x["repo"]))
    (HERE / "selection.json").write_text(json.dumps({"agents": agents, "skills": skills}, indent=1))
    print(f"agents {len(agents)} ({sum(a['words'] for a in agents)} words), skills {len(skills)} ({sum(s['words'] for s in skills)} words)")

    # Batches of ten, agents first. Skill stars come from the skill corpus's repository list.
    stars = {r["full_name"]: r["stars"] for r in json.loads((HERE.parent / "260818-github-skills" / "repos.json").read_text())}
    items = [dict(id=a["id"], kind="agent", file="corpus/" + a["file"], repo=a["repo"], path=a["path"], stars=a["stars"], copies_in_repos=a["repos"]) for a in agents]
    items += [dict(id=f"s{i:04d}", kind="skill", file="corpus-skills/" + k["file"], repo=k["repo"], path=k["path"], stars=stars.get(k["repo"], 0),
                   copies_in_repos=1 + len(k["copies"])) for i, k in enumerate(skills)]
    (HERE / "batches").mkdir(exist_ok=True)
    for b in range(0, len(items), 10):
        (HERE / "batches" / f"{b // 10:04d}.json").write_text(json.dumps(items[b:b + 10], indent=1))
    print(f"{len(items)} items in {(len(items) + 9) // 10} batches")
