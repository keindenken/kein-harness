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
            "rc": r.get("reach") or [],
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
    print(f"viewer.html: {len(out)} rows ({q} with a quote), "
          f"specificity on {sum(1 for x in out if x['sp'] is not None)}, "
          f"{(HERE / 'viewer.html').stat().st_size / 1e6:.1f} MB")


main()
