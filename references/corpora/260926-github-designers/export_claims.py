#!/usr/bin/env python3
"""Write claims/<dimension>.jsonl: every specific, verbatim-checked instruction quote from a design role, with its source's metadata."""
import json, re, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[*_`>#\\]", "", s)).strip().lower()
out = collections.defaultdict(list); dropped = 0
for r in json.loads((HERE / "records.json").read_text()):
    if not r.get("design_role"): continue
    src = norm((HERE / r["file"]).read_text())
    for q in r.get("instructions", []):
        if not q.get("specific"): continue
        parts = [norm(p) for p in re.split(r"\.\.\.|…", q["quote"]) if len(norm(p)) > 8] or [norm(q["quote"])]
        if not all(p in src for p in parts):
            dropped += 1; continue
        out[q.get("dimension", "other")].append({"id": r["id"], "kind": r["kind"], "repo": r["repo"], "stars": r.get("stars", 0),
                                                 "copies_in_repos": r.get("copies_in_repos", 1), "outputs": r.get("outputs", []),
                                                 "modes": r.get("modes", []), "quote": q["quote"]})
d = HERE / "claims"; d.mkdir(exist_ok=True)
for dim, rows in out.items():
    (d / f"{dim}.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n")
print({k: len(v) for k, v in sorted(out.items(), key=lambda kv: -len(kv[1]))}, "dropped non-verbatim:", dropped)
