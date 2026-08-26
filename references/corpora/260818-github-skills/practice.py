#!/usr/bin/env python3
"""Extract what this harness commits to, so it can be checked against the corpus.

Both sides get the same treatment. The corpus was read by quoting a sentence and
locating it in the source; the harness is read the same way, because a rule
paraphrased into a summary cannot be checked against the file it came from, and
because the comparison that follows is between two sets of quotes rather than
between a corpus and somebody's impression of how we work.

`plugin/agents/*.md` is generated from `plugin/prompts/*.md` and differs only in
frontmatter, so only the canonical prompt is read.

Usage: ./practice.py <root> <out.jsonl> [--model M] [--workers W]
"""
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = (HERE / "prompt" / "practice.md").read_text()


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


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[*_`]+", "", s or "")).strip()


def one(args):
    root, rel, model = args
    body = (root / rel).read_text(errors="replace")
    out, err, usage = call(TPL.replace("{{PATH}}", rel).replace("{{BODY}}", body), model)
    rec = parse(out, require="commitments")
    if rec is None:
        return [{"file": rel, "ok": False, "error": (out or err)[-250:]}]
    src = norm(body)
    recs = []
    for c in rec["commitments"]:
        q = c.get("quote")
        recs.append({
            "file": rel, "ok": True, "quote": q, "about": c.get("about"),
            "kind": c.get("kind"),
            # Located in the file, the same check the corpus quotes get.
            "quote_ok": bool(q) and norm(q) in src,
            "cost_usd": (usage.get("cost_usd") or 0) / max(len(rec["commitments"]), 1),
        })
    return recs or [{"file": rel, "ok": True, "quote": None, "about": None,
                     "kind": None, "quote_ok": False, "cost_usd": usage.get("cost_usd")}]


def main():
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    model, w = "sonnet", 4
    for i, a in enumerate(sys.argv):
        if a == "--model": model = sys.argv[i + 1]
        if a == "--workers": w = int(sys.argv[i + 1])
    files = ["prompts/lead.md", "prompts/lead-omc.md"]
    files += [str(p.relative_to(root)) for p in sorted((root / "plugin/skills").rglob("*.md"))]
    files += [str(p.relative_to(root)) for p in sorted((root / "plugin/prompts").glob("*.md"))]
    done = ({json.loads(l)["file"] for l in out.read_text().splitlines()
             if json.loads(l).get("ok")} if out.exists() else set())
    todo = [(root, f, model) for f in files if f not in done]
    print(f"{len(files)} files, {len(todo)} to read", flush=True)
    t0, n, spend = time.time(), 0, 0.0
    with out.open("a") as fh, ThreadPoolExecutor(max_workers=w) as pool:
        for got in pool.map(one, todo):
            for rec in got:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                spend += rec.get("cost_usd") or 0
            fh.flush()
            n += 1
            ok = sum(1 for r in got if r.get("quote_ok"))
            print(f"  {n}/{len(todo)}  {got[0]['file'][:44]:44} {ok}/{len(got)} located"
                  f"  {int(time.time()-t0)}s  ${spend:.2f}", flush=True)


if __name__ == "__main__":
    main()
