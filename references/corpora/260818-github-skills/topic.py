#!/usr/bin/env python3
"""Stage A: what each claim is knowledge about, named without a list to choose from.

No taxonomy is supplied, on purpose. 260811 handed a model seven `DOMAINS`
regexes and assigned by first alphabetical match, so `meta` fired on 66% of files
and every bucket after `code` held leftovers — a category list is a hypothesis,
and offering one gets it confirmed rather than tested. Here the subjects come out
of the claims and the clustering happens afterwards, in `cluster.py`, where it can
be inspected.

The one thing this cannot rule out on its own is a batch agreeing with itself:
thirty claims read together may converge on shared wording that thirty other
claims would not have produced. `--seed` reshuffles the grouping so the same run
can be repeated with different neighbours, and the agreement between two seeds is
the measurement that says whether the subjects are in the corpus or in the call.

Usage: ./topic.py <records.json> <out.jsonl> [--model M] [--batch N]
                  [--workers W] [--seed S]
"""
import json
import random
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = (HERE / "prompt" / "topic.md").read_text()


def call(prompt, model):
    p = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json"],
                       input=prompt, capture_output=True, text=True, cwd="/tmp", timeout=900)
    try:
        env = json.loads(p.stdout)
    except Exception:
        return p.stdout, p.stderr, {}
    return env.get("result", ""), p.stderr, {"cost_usd": env.get("total_cost_usd")}


def parse(raw):
    raw = raw.strip()
    try:
        v = json.loads(raw)
        if isinstance(v, list):
            return v
    except Exception:
        pass
    for start in (m.start() for m in re.finditer(r"\[", raw)):
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
            elif c in "[{":
                depth += 1
            elif c in "]}":
                depth -= 1
                if depth == 0:
                    try:
                        v = json.loads(raw[start:i + 1])
                        if isinstance(v, list):
                            return v
                    except Exception:
                        pass
                    break
            i += 1
    return None


def one(args):
    batch, model, seed = args
    body = "\n".join(json.dumps(
        {"id": r["skill"], "quote": r["quote"], "skill_summary": (r.get("summary") or "")[:220]},
        ensure_ascii=False) for r in batch)
    out, err, usage = call(TPL.replace("{{RECORDS}}", body), model)
    arr = parse(out)
    if arr is None:
        return [{"skill": r["skill"], "ok": False, "seed": seed,
                 "error": (out or err)[-250:]} for r in batch]
    by = {a.get("id"): a for a in arr if isinstance(a, dict)}
    recs = []
    for r in batch:
        a = by.get(r["skill"])
        if a is None or not a.get("about"):
            recs.append({"skill": r["skill"], "ok": False, "seed": seed,
                         "error": "absent from reply"})
            continue
        recs.append({"skill": r["skill"], "ok": True, "seed": seed,
                     "about": a["about"].strip(),
                     "batch_cost": (usage.get("cost_usd") or 0) / len(batch)})
    return recs


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    model, size, w, seed = "sonnet", 30, 4, 0
    for i, a in enumerate(sys.argv):
        if a == "--model": model = sys.argv[i + 1]
        if a == "--batch": size = int(sys.argv[i + 1])
        if a == "--workers": w = int(sys.argv[i + 1])
        if a == "--seed": seed = int(sys.argv[i + 1])
    recs = json.loads(src.read_text())
    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            r = json.loads(line)
            if r.get("ok") and r.get("seed") == seed:
                done.add(r["skill"])
    todo = [r for r in recs if r["skill"] not in done]
    if seed:
        random.Random(seed).shuffle(todo)
    batches = [todo[i:i + size] for i in range(0, len(todo), size)]
    print(f"{len(recs)} claims, {len(done)} done at seed {seed}, "
          f"{len(batches)} batches of {size}", flush=True)
    t0, n, spend = time.time(), 0, 0.0
    with out.open("a") as fh, ThreadPoolExecutor(max_workers=w) as pool:
        for got in pool.map(one, ((b, model, seed) for b in batches)):
            for rec in got:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                spend += rec.get("batch_cost") or 0
            fh.flush()
            n += 1
            print(f"  batch {n}/{len(batches)}  {sum(1 for r in got if r.get('ok'))}/{len(got)} ok"
                  f"  {int(time.time()-t0)}s  ${spend:.2f}", flush=True)


main()
