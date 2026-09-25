#!/usr/bin/env python3
"""Group near-duplicate agent texts, so a prompt copied into fifty repositories counts once.

Exact dedupe (harvest.py) leaves every lightly edited copy standing, and a claim that "recurs"
across copies of one ancestor is one source, not fifty. Word 5-shingles, MinHash with 128
permutations, LSH in 32 bands of 4 rows, then a union over pairs whose estimated Jaccard is at
least THRESHOLD. Each cluster keeps its most-starred member as the one agents read.
"""
import hashlib, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
THRESHOLD = 0.6
PERMS, BANDS = 128, 32
ROWS = PERMS // BANDS
MIN_WORDS = 40

def shingles(text, k=5):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {" ".join(words[i:i + k]) for i in range(max(1, len(words) - k + 1))}

def minhash(sh):
    hs = [int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), "big") for s in sh]
    M = (1 << 61) - 1
    return [min(((a * h + b) % M) for h in hs) for a, b in ((2 * i + 1, 7919 * i + 13) for i in range(PERMS))]

unique = json.loads((HERE / "unique.json").read_text())
docs = []
for r in unique:
    text = (HERE / "corpus" / r["file"]).read_text()
    if len(text.split()) < MIN_WORDS:
        continue
    docs.append((r, minhash(shingles(text))))
parent = list(range(len(docs)))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
buckets = {}
for i, (_, sig) in enumerate(docs):
    for b in range(BANDS):
        buckets.setdefault((b, tuple(sig[b * ROWS:(b + 1) * ROWS])), []).append(i)
for members in buckets.values():
    for j in members[1:]:
        a, b = members[0], j
        if find(a) != find(b):
            sa, sb = docs[a][1], docs[b][1]
            if sum(x == y for x, y in zip(sa, sb)) / PERMS >= THRESHOLD:
                parent[find(a)] = find(b)
clusters = {}
for i in range(len(docs)):
    clusters.setdefault(find(i), []).append(docs[i][0])
out = []
for members in clusters.values():
    members.sort(key=lambda r: -r.get("stars", 0))
    head = members[0]
    repos = sorted({m["repo"] for m in members} | {c.split("/", 2)[0] + "/" + c.split("/", 2)[1] for m in members for c in m.get("copies", [])})
    out.append({"file": head["file"], "repo": head["repo"], "path": head["path"], "stars": head.get("stars", 0),
                "words": head["words"], "members": len(members), "repos": len(repos),
                "sample_repos": repos[:8]})
out.sort(key=lambda c: (-c["repos"], -c["stars"]))
(HERE / "clusters.json").write_text(json.dumps(out, indent=1))
print(f"{len(unique)} distinct texts, {len(docs)} at or over {MIN_WORDS} words -> {len(out)} clusters; "
      f"{sum(1 for c in out if c['members'] > 1)} with more than one member, largest spans {out[0]['repos']} repositories")
