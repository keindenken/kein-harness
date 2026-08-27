#!/usr/bin/env python3
"""Stage C: one call per cluster, reading the claims rather than their subjects.

`cluster.py` groups on shared vocabulary and that is sometimes all a group has:
five claims once landed together because every subject ended in "false
positives", covering A/B testing, HLA typing, cloud storage and subdomain
takeover. So the first thing this asks is whether the group is a subject at all,
and a `false` there is a finding rather than a failure — it is the same discipline
as `coherence` in the repository pass, where the model is allowed to say the
collection has no thread.

What it is for is `read_first`. The corpus is an index and not a replacement:
someone about to write a skill will open the original, and the useful output is
which original and why.

Usage: ./cluster_read.py <clusters.json> <out.jsonl> [--model M] [--min 2] [--workers W]
"""
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL_NAME = "cluster"
for _i, _a in enumerate(sys.argv):
    if _a == "--prompt":
        TPL_NAME = Path(sys.argv[_i + 1]).stem
TPL = (HERE / "prompt" / f"{TPL_NAME}.md").read_text()


def call(prompt, model):
    p = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json"],
                       input=prompt, capture_output=True, text=True, cwd="/tmp", timeout=900)
    try:
        env = json.loads(p.stdout)
    except Exception:
        return p.stdout, p.stderr, {}
    return env.get("result", ""), p.stderr, {"cost_usd": env.get("total_cost_usd")}


def parse(raw, require=None):
    raw = raw.strip()
    try:
        v = json.loads(raw)
        if isinstance(v, dict) and (require is None or require in v):
            return v
    except Exception:
        pass
    for start in (m.start() for m in re.finditer(r"\{", raw)):
        depth, i, instr, esc = 0, start, False, False
        while i < len(raw):
            c = raw[i]
            if instr:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    instr = False
            elif c == '"':
                instr = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        v = json.loads(raw[start:i + 1])
                    except Exception:
                        break
                    if isinstance(v, dict) and (require is None or require in v):
                        return v
                    break
            i += 1
    return None


def one(args):
    idx, group, byskill, model = args
    body = "\n".join(json.dumps({
        "id": s,
        "quote": byskill[s].get("quote"),
        "named_subject": None,
        "skill_summary": (byskill[s].get("summary") or "")[:200],
    }, ensure_ascii=False) for s in group["skills"] if s in byskill)
    out, err, usage = call(TPL.replace("{{CLAIMS}}", body), model)
    rec = parse(out, require="coherent")
    base = {"cluster": idx, "n": group["n"], "abouts": group["abouts"],
            "skills": group["skills"], "model": model, "prompt": TPL_NAME,
            "cost_usd": usage.get("cost_usd")}
    if rec is None:
        return {**base, "ok": False, "error": (out or err)[-250:]}
    return {**base, "ok": True, **rec}


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    model, mn, w = "sonnet", 2, 4
    for i, a in enumerate(sys.argv):
        if a == "--model": model = sys.argv[i + 1]
        if a == "--min": mn = int(sys.argv[i + 1])
        if a == "--workers": w = int(sys.argv[i + 1])
    groups = [g for g in json.loads(src.read_text()) if g["n"] >= mn]
    byskill = {r["skill"]: r for r in json.loads((HERE / "runs" / "topic-records.json").read_text())}
    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            r = json.loads(line)
            if r.get("ok"):
                done.add(r["cluster"])
    todo = [(i, g, byskill, model) for i, g in enumerate(groups) if i not in done]
    print(f"{len(groups)} clusters, {len(todo)} to read, model={model}", flush=True)
    t0, n, spend = time.time(), 0, 0.0
    with out.open("a") as fh, ThreadPoolExecutor(max_workers=w) as pool:
        for rec in pool.map(one, todo):
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            spend += rec.get("cost_usd") or 0
            n += 1
            tag = "FAIL" if not rec.get("ok") else ("not-a-subject" if not rec.get("coherent")
                                                    else (rec.get("subject") or "")[:38])
            print(f"  {n}/{len(todo)}  [{rec['n']}] {tag}  {int(time.time()-t0)}s  ${spend:.2f}", flush=True)


main()
