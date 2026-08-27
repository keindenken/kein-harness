#!/usr/bin/env python3
"""Join what the corpus knows to what this harness commits to, without a model.

Both sides were read the same way — a verbatim quote plus a three-to-six word
subject — so the join is between two sets of subjects and can be arithmetic. That
matters more here than anywhere else in this pipeline: asked which corpus claims
bear on our practice, a model will find some, and there would be no way to tell a
real bearing from a helpful one.

Words are weighted by rarity across both sides together, so a subject sharing
only `file` or `context` scores near nothing while one sharing `judge ordering`
scores high. Same measure `cluster.py` uses.

`--control N` emits N pairs drawn at random from subjects that share no words at
all. Those go through the judging pass mixed in with the real ones, and the rate
of conflicts found in them is what says whether the rate found in the real pairs
means anything.

Usage: ./match.py <topic.jsonl> <practice.jsonl> <out.json> [--th 0.30] [--control 25]
"""
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cluster import words  # noqa: E402  — same stopwords, same tokenisation


def main():
    tf, pf, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    th, ncontrol = 0.30, 25
    for i, a in enumerate(sys.argv):
        if a == "--th": th = float(sys.argv[i + 1])
        if a == "--control": ncontrol = int(sys.argv[i + 1])

    corpus = [json.loads(l) for l in tf.read_text().splitlines()]
    corpus = [r for r in corpus if r.get("ok") and r.get("seed", 0) == 0]
    prac = [json.loads(l) for l in pf.read_text().splitlines()]
    prac = [r for r in prac if r.get("ok") and r.get("quote_ok")]

    A = [words(r["about"]) for r in corpus]
    B = [words(r["about"]) for r in prac]
    df = Counter()
    for s in A + B:
        df.update(s)
    n = len(A) + len(B)
    idf = {w: math.log(n / df[w]) for w in df}
    na = [math.sqrt(sum(idf[w] for w in s)) or 1.0 for s in A]
    nb = [math.sqrt(sum(idf[w] for w in s)) or 1.0 for s in B]

    inv = defaultdict(list)
    for i, s in enumerate(A):
        for w in s:
            inv[w].append(i)

    # For each harness commitment, the corpus claims whose subject it shares
    # rare words with. A commitment can match many claims; a claim can match
    # many commitments. Grouped by commitment, because the question is asked of
    # our practice.
    groups = []
    for j, sb in enumerate(B):
        cand = {i for w in sb for i in inv.get(w, []) if len(inv[w]) <= 300}
        hits = []
        for i in cand:
            sh = A[i] & sb
            if not sh:
                continue
            s = sum(idf[w] for w in sh) / (na[i] * nb[j])
            if s >= th:
                hits.append((round(s, 3), i))
        if hits:
            hits.sort(reverse=True)
            groups.append({"kind": "real", "practice": j,
                           "claims": [i for _, i in hits[:12]],
                           "scores": [s for s, _ in hits[:12]]})

    rng = random.Random(826)
    used = {g["practice"] for g in groups}
    pool = [j for j in range(len(B)) if j in used] or list(range(len(B)))
    for _ in range(ncontrol):
        j = rng.choice(pool)
        far = [i for i in rng.sample(range(len(A)), 60) if not (A[i] & B[j])][:4]
        if far:
            groups.append({"kind": "control", "practice": j, "claims": far,
                           "scores": [0.0] * len(far)})

    payload = {
        "corpus": [{"skill": r["skill"], "about": r["about"]} for r in corpus],
        "practice": [{"file": r["file"], "quote": r["quote"], "about": r["about"],
                      "kind": r["kind"]} for r in prac],
        "groups": groups,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False))
    real = [g for g in groups if g["kind"] == "real"]
    print(f"{len(prac)} commitments, {len(corpus)} claims")
    print(f"  {len(real)} commitments matched at th={th} "
          f"({len(real)/len(prac):.0%}), {sum(len(g['claims']) for g in real)} pairs")
    print(f"  {ncontrol} control groups, sharing no subject words at all")
    for g in sorted(real, key=lambda g: -g["scores"][0])[:8]:
        print(f"    {g['scores'][0]:.2f}  {prac[g['practice']]['about'][:34]:34} "
              f"← {corpus[g['claims'][0]]['about'][:38]}")


main()
