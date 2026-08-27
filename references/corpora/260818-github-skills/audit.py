#!/usr/bin/env python3
"""Stage 3: does what the corpus learned bear on what this harness commits to.

One call per matched commitment, and the control groups go through the same call
in the same shape. A model asked to find problems will find some; the rate it
finds them in pairs matched by shared vocabulary only means something next to the
rate it finds them in pairs that share no vocabulary at all. That is the lesson
of the null probe, where 91 flagged nulls yielded 15% and 45 unflagged ones
yielded 14%, and only the second number made the first readable.

The call cannot tell which kind it is looking at.

Usage: ./audit.py <match.json> <out.jsonl> [--model M] [--workers W]
"""
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL_NAME = "audit"
for _i, _a in enumerate(sys.argv):
    if _a == "--prompt":
        TPL_NAME = Path(sys.argv[_i + 1]).stem
TPL = (HERE / "prompt" / f"{TPL_NAME}.md").read_text()
QUOTES = {r["skill"]: r for r in json.loads((HERE / "runs" / "facet-records.json").read_text())}
sys.path.insert(0, str(HERE))
from practice import call, parse, norm  # noqa: E402


def one(args):
    gi, g, corpus, prac, model = args
    p = prac[g["practice"]]
    claims = []
    for i in g["claims"]:
        c = corpus[i]
        q = (QUOTES.get(c["skill"]) or {}).get("quote")
        if q:
            claims.append(json.dumps({"id": c["skill"], "about": c["about"], "quote": q},
                                     ensure_ascii=False))
    prompt = (TPL.replace("{{FILE}}", p["file"]).replace("{{KIND}}", p["kind"] or "")
                 .replace("{{COMMITMENT}}", p["quote"])
                 .replace("{{CLAIMS}}", "\n".join(claims)))
    out, err, usage = call(prompt, model)
    rec = parse(out, require="verdict")
    base = {"group": gi, "arm": g["kind"], "prompt": TPL_NAME, "file": p["file"], "about": p["about"],
            "commitment": p["quote"], "n_claims": len(claims),
            "top_score": g["scores"][0] if g["scores"] else 0.0,
            "cost_usd": usage.get("cost_usd")}
    if rec is None:
        return {**base, "ok": False, "error": (out or err)[-250:]}
    # Both halves must be locatable in what was actually shown, or the finding is
    # a paraphrase wearing quotation marks.
    cq, kq = rec.get("commitment_quote"), rec.get("claim_quote")
    fed = {c["skill"]: (QUOTES.get(c["skill"]) or {}).get("quote") or "" for c in
           (corpus[i] for i in g["claims"])}
    return {**base, "ok": True, **rec,
            "commitment_located": bool(cq) and norm(cq) in norm(p["quote"]),
            "claim_located": bool(kq) and any(norm(kq) in norm(v) for v in fed.values())}


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    model, w = "sonnet", 4
    for i, a in enumerate(sys.argv):
        if a == "--model": model = sys.argv[i + 1]
        if a == "--workers": w = int(sys.argv[i + 1])
    d = json.loads(src.read_text())
    done = ({json.loads(l)["group"] for l in out.read_text().splitlines()
             if json.loads(l).get("ok")} if out.exists() else set())
    todo = [(i, g, d["corpus"], d["practice"], model)
            for i, g in enumerate(d["groups"]) if i not in done]
    print(f"{len(d['groups'])} groups, {len(todo)} to judge", flush=True)
    t0, n, spend, hits = time.time(), 0, 0.0, 0
    with out.open("a") as fh, ThreadPoolExecutor(max_workers=w) as pool:
        for rec in pool.map(one, todo):
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            spend += rec.get("cost_usd") or 0
            n += 1
            v = rec.get("verdict", "FAIL")
            hits += v in ("conflict", "gap")
            print(f"  {n}/{len(todo)}  {v:8} [{rec['arm']}] {rec['about'][:34]:34}"
                  f"  {hits} hits  {int(time.time()-t0)}s  ${spend:.2f}", flush=True)


main()
