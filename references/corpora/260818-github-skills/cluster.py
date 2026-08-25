#!/usr/bin/env python3
"""Stage B: group the claims by the subjects `topic.py` named, without a model.

The subjects come out almost all distinct — 867 strings for 881 claims, 853 of
them used once — so exact matching groups nothing and the join has to be on
shared words. Shared words alone over-merge: the commonest, `file`, appears in
31 subjects that have nothing else in common. Each word is therefore weighted by
how rare it is across the set, and two subjects are neighbours when the rare
words they share outweigh the ones they do not.

Linkage is average, not single. Single linkage is what a union-find gives you and
it chains: `concurrent plan file writes` joins `file read context size` joins
`subagent dispatch context size`, and a cluster of fourteen forms that is about
nothing. A claim joins a cluster here only if it is close to the cluster on
average, which leaves the chain as several smaller true groups.

Nothing here decides what the clusters mean. That is `prompt/cluster.md`, one
call per cluster, reading the claims themselves.

Usage: ./cluster.py <topic.jsonl> <out.json> [--th 0.35] [--seed 0]
"""
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

STOP = set("""a an the of in for to and or on at with by from is are be as it its this
that when using use vs across between into over under after before during not no non""".split())


def words(s):
    return {w for w in re.findall(r"[a-z0-9.+-]+", s.lower()) if w not in STOP and len(w) > 1}


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    th, seed = 0.35, 0
    for i, a in enumerate(sys.argv):
        if a == "--th": th = float(sys.argv[i + 1])
        if a == "--seed": seed = int(sys.argv[i + 1])

    rows = [json.loads(l) for l in src.read_text().splitlines()]
    rows = [r for r in rows if r.get("ok") and r.get("seed", 0) == seed]
    W = [words(r["about"]) for r in rows]
    n = len(W)
    df = Counter()
    for s in W:
        df.update(s)
    idf = {w: math.log(n / df[w]) for w in df}
    norm = [math.sqrt(sum(idf[w] for w in s)) or 1.0 for s in W]

    def sim(i, j):
        sh = W[i] & W[j]
        return sum(idf[w] for w in sh) / (norm[i] * norm[j]) if sh else 0.0

    # Only pairs sharing a word can score above zero, so the candidate set comes
    # from an inverted index rather than from all n^2 pairs.
    inv = defaultdict(list)
    for i, s in enumerate(W):
        for w in s:
            inv[w].append(i)
    pairs = {}
    for w, ids in inv.items():
        if len(ids) > 150:          # a word this common carries no signal
            continue
        for a in range(len(ids)):
            for b in range(a + 1, len(ids)):
                p = (ids[a], ids[b])
                if p not in pairs:
                    pairs[p] = sim(*p)
    ranked = sorted((v, k) for k, v in pairs.items() if v >= th)
    ranked.reverse()

    # Greedy average linkage: merge the closest pair whose two clusters are still
    # close on average once joined.
    cl = {i: [i] for i in range(n)}
    of = list(range(n))
    for s, (i, j) in ranked:
        a, b = of[i], of[j]
        if a == b:
            continue
        ga, gb = cl[a], cl[b]
        avg = sum(pairs.get((min(x, y), max(x, y)), 0.0) for x in ga for y in gb) / (len(ga) * len(gb))
        if avg < th:
            continue
        for x in gb:
            of[x] = a
        cl[a] = ga + gb
        del cl[b]

    groups = sorted((g for g in cl.values() if len(g) > 1), key=len, reverse=True)
    payload = [{"n": len(g),
                "abouts": sorted({rows[i]["about"] for i in g}),
                "skills": [rows[i]["skill"] for i in g]} for g in groups]
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1))
    covered = sum(len(g) for g in groups)
    print(f"{n} claims, {len(groups)} clusters of 2+, {covered} covered ({covered/n:.0%}), "
          f"largest {len(groups[0])}, {n - covered} singletons")
    for g in groups[:10]:
        print(f"  [{len(g)}] " + " · ".join(sorted({rows[i]['about'] for i in g})[:5]))


main()
