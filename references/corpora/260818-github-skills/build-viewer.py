#!/usr/bin/env python3
"""Inline the reading pass into viewer.html.

The page is generated rather than committed: 3 MB that would change wholesale
on every run, and `runs/pass2.jsonl` rebuilds it exactly.

Usage: ./build-viewer.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
NUM = re.compile(r'\b(20\d\d-\d\d-\d\d|\d+%|\d+\s*(ms|s|MB|KB|GB|tokens?|lines?|results?)|\bv?\d+\.\d+)', re.I)


def main():
    # Last record wins: a skill re-run during a smoke test appears twice.
    rows = {}
    for line in (HERE / "runs" / "pass2.jsonl").read_text().splitlines():
        r = json.loads(line)
        rows[r["skill"]] = r
    rows = [r for r in rows.values() if r.get("ok")]

    stars = {r["full_name"]: r["stars"] for r in json.loads((HERE / "repos.json").read_text())}

    # `reach` and `cli` come from the corrected labels, not from the record. The
    # regex that produced the originals matched a binary after any whitespace
    # rather than in command position, so `go through` inside a fenced diagram
    # scored `go`; 216 records claimed to reach outside themselves and did not.
    fixed = {}
    lv2 = HERE / "runs" / "labels-v2.jsonl"
    for line in (lv2.read_text().splitlines() if lv2.exists() else []):
        r = json.loads(line)
        fixed[r["skill"]] = r

    # The repository pass has run on fifty of 846 repositories. Everything else
    # gets no verdict rather than a default one — `미분류` is a real answer here.
    repo1 = {}
    p1 = HERE / "runs" / "pass1-50-siblings.jsonl"
    for line in (p1.read_text().splitlines() if p1.exists() else []):
        r = json.loads(line)
        if r.get("ok"):
            repo1[r["repo"]] = r
    # The shortlist keys on (repo, dir, loose_file) and the reading pass never
    # carried `loose_file`, so a plain three-part join loses every AGENTS.md and
    # CLAUDE.md record — 450 of them. Key on what both sides actually share.
    spec = {}
    for s in json.loads((HERE / "shortlist.json").read_text()):
        spec[(s["repo"], s["dir"])] = s["specificity"]

    out = []
    for r in rows:
        q = r.get("quote")
        out.append({
            "k": r["skill"],
            "r": r.get("repo", ""),
            "su": r.get("summary", ""),
            "q": q,
            "qr": r.get("quote_reason"),
            "qf": r.get("quote_file"),
            "rc": (fixed.get(r["skill"], r).get("reach")) or [],
            "cl": (fixed.get(r["skill"], r).get("cli")) or [],
            "rl": (repo1.get(r.get("repo")) or {}).get("coherence"),
            "rf": ((repo1.get(r.get("repo")) or {}).get("field")
                   or (repo1.get(r.get("repo")) or {}).get("form")),
            "dr": (r.get("drives") or [])[:10],
            "m": "luna" if r.get("model") == "gpt-5.6-luna" else "haiku",
            "p": r.get("prompt") or "extract",
            "sp": spec.get((r.get("repo"), r.get("dir"))),
            "st": stars.get(r.get("repo")),
            "nf": len(r.get("unread_prose") or []),
            "il": len(r.get("inlined") or []),
            "n": bool(q and NUM.search(q)),
        })

    scored = [x["sp"] for x in out if x["sp"] is not None]
    scored.sort()
    cuts = [scored[len(scored) * i // 4] for i in (1, 2, 3)]
    blob = json.dumps({"rows": out, "cuts": cuts}, separators=(",", ":"), ensure_ascii=False)

    tpl = (HERE / "viewer-template.html").read_text()
    if "__DATA__" not in tpl:
        raise SystemExit("viewer-template.html has no __DATA__ placeholder")
    (HERE / "viewer.html").write_text(tpl.replace("__DATA__", blob))
    q = sum(1 for x in out if x["q"])
    print(f"  relabelled: {sum(1 for x in out if x['k'] in fixed)}, "
          f"repo verdict on {sum(1 for x in out if x['rl'])} rows "
          f"from {len(repo1)} repositories")
    print(f"viewer.html: {len(out)} rows ({q} with a quote), "
          f"specificity on {sum(1 for x in out if x['sp'] is not None)}, "
          f"{(HERE / 'viewer.html').stat().st_size / 1e6:.1f} MB")


main()
