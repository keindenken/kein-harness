#!/usr/bin/env python3
"""Pass 3: how far each claim travels, and what it says in Korean.

The unit is the record, not the skill directory. Everything this pass needs was
already written by pass 2 — `summary`, the verbatim `quote`, `quote_reason`, and
`drives`, which names tools the summary never mentions in 85% of cases and
*only* names them in half of all records. Re-reading the files would cost 3,957
calls to recover context already on disk; batching forty records costs a hundred.

Translation rides along rather than taking a pass of its own, because it reads
the same fields and its output sits beside them. The English is never replaced:
a located quote is the one guarantee this corpus makes, and a translation cannot
carry it. `check()` enforces the part of that which is mechanical — code, flags,
identifiers and numbers must survive into the Korean unaltered.

Usage:
  ./facet.py <records.json> <out.jsonl> [--model M] [--batch N] [--workers W]
"""
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = (HERE / "prompt" / "facet.md").read_text()

# What must come through translation untouched. Backticked spans are the
# author's own marking of "this is a token, not prose"; the rest catches what a
# writer left bare.
TICK = re.compile(r"`[^`\n]+`")
FLAG = re.compile(r"(?<![\w-])--?[A-Za-z][\w-]{1,}")
# A path needs a dot-extension or a `./` on the front. Anything looser matches
# prose: `access/deletion`, `web/CLI/TUI`, `verified/unsupported/needs-human` are
# all slash-separated word lists, and every one of them made a correct Korean
# translation look like a violation. Bare `plugins/foo/bar` is given up with it.
PATH = re.compile(r"\.{1,2}/[\w.-]+(?:/[\w.-]+)*"
                  r"|\b[\w./-]*[\w-]+\.(?:md|py|json|ya?ml|ts|tsx|js|sh|toml|txt|csv)\b")
# Bare numbers only. Protecting `5s` as a unit made `약 5초` a violation, and
# `5초` is the better translation — a unit outside backticks is prose.
NUM = re.compile(r"\b\d+(?:[.,]\d+)*\b")


def fields(s):
    """Tokens a translation is not allowed to alter."""
    if not s:
        return set()
    out = set()
    for rx in (TICK, FLAG, PATH):
        out |= {m.group(0).strip("`") for m in rx.finditer(s)}
    out |= {m.group(0).replace(" ", "") for m in NUM.finditer(s) if any(c.isdigit() for c in m.group(0))}
    return {t for t in out if len(t) > 1}


def check(src, ko):
    """Which protected tokens the Korean dropped."""
    if not src or not ko:
        return []
    flat = ko.replace(" ", "")
    return sorted(t for t in fields(src) if t not in ko and t.replace(" ", "") not in flat)


def call(prompt, model):
    p = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json"],
                       input=prompt, capture_output=True, text=True, cwd="/tmp", timeout=1200)
    try:
        env = json.loads(p.stdout)
    except Exception:
        return p.stdout, p.stderr, {}
    u = env.get("usage", {})
    return env.get("result", ""), p.stderr, {
        "cost_usd": env.get("total_cost_usd"),
        "in_new": u.get("cache_creation_input_tokens"),
        "in_cached": u.get("cache_read_input_tokens"),
        "out": u.get("output_tokens"),
    }


def parse(raw):
    """Pull the JSON array out of a reply, brace-aware inside strings."""
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


def payload(r):
    return {
        "id": r["skill"],
        "summary": r.get("summary"),
        "quote": r.get("quote"),
        "quote_reason": r.get("quote_reason"),
        "quote_file": r.get("quote_file"),
        "drives": (r.get("drives") or [])[:12],
        "cli": r.get("cli") or [],
        "mcp": r.get("mcp") or [],
        "reach": r.get("reach") or [],
    }


def one(args):
    batch, model = args
    body = "\n".join(json.dumps(payload(r), ensure_ascii=False) for r in batch)
    out, err, usage = call(TPL.replace("{{RECORDS}}", body), model)
    arr = parse(out)
    if arr is None:
        return [{"skill": r["skill"], "ok": False, "error": (out or err)[-300:]} for r in batch]
    by = {a.get("id"): a for a in arr if isinstance(a, dict)}
    recs = []
    for r in batch:
        a = by.get(r["skill"])
        if a is None:
            recs.append({"skill": r["skill"], "ok": False, "error": "absent from reply"})
            continue
        recs.append({
            "skill": r["skill"], "ok": True, "model": model,
            "transfer": a.get("transfer"), "transfer_why": a.get("transfer_why"),
            "needs_source": bool(a.get("needs_source")),
            "ko_quote": a.get("ko_quote"), "ko_reason": a.get("ko_reason"),
            "ko_summary": a.get("ko_summary"),
            # Recorded, not enforced: a dropped token is a fact about the
            # translation, and the English it sits beside is untouched either way.
            "lost_quote": check(r.get("quote"), a.get("ko_quote")),
            "lost_summary": check(r.get("summary"), a.get("ko_summary")),
            "batch_cost": (usage.get("cost_usd") or 0) / len(batch),
        })
    return recs


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    model, size, w = "sonnet", 40, 3
    for i, a in enumerate(sys.argv):
        if a == "--model": model = sys.argv[i + 1]
        if a == "--batch": size = int(sys.argv[i + 1])
        if a == "--workers": w = int(sys.argv[i + 1])
    recs = json.loads(src.read_text())
    # Only a successful record counts as done. A batch dies whole — one reply
    # that will not parse, or one record that trips a safeguard, takes its
    # twenty-nine neighbours with it — and those neighbours have to come back on
    # a resume. Counting every line written would bury them as already-read.
    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            r = json.loads(line)
            if r.get("ok"):
                done.add(r["skill"])
    todo = [r for r in recs if r["skill"] not in done]
    batches = [todo[i:i + size] for i in range(0, len(todo), size)]
    print(f"{len(recs)} records, {len(done)} done, {len(batches)} batches of {size}, model={model}", flush=True)
    t0, n, spend = time.time(), 0, 0.0
    with out.open("a") as fh, ThreadPoolExecutor(max_workers=w) as pool:
        for got in pool.map(one, ((b, model) for b in batches)):
            for rec in got:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                spend += rec.get("batch_cost") or 0
            fh.flush()
            n += 1
            ok = sum(1 for r in got if r.get("ok"))
            print(f"  batch {n}/{len(batches)}  {ok}/{len(got)} ok  "
                  f"{int(time.time()-t0)}s  ${spend:.2f}", flush=True)


main()
