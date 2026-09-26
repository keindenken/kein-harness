#!/usr/bin/env python3
"""Fold results/<batch>/<id>.json into records.json, one record per agent cluster or skill, joined with its manifest entry."""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
manifest = {m["id"]: m for p in sorted((HERE / "batches").glob("*.json")) for m in json.loads(p.read_text())}
records, broken = [], []
for f in sorted((HERE / "results").glob("*/*.json")):
    try:
        r = json.loads(f.read_text())
    except json.JSONDecodeError:
        broken.append(str(f)); continue
    m = manifest.get(f.stem)
    if m:
        r.update({"id": m["id"], "kind": m["kind"], "file": m["file"], "stars": m["stars"], "copies_in_repos": m["copies_in_repos"], "batch": f.parent.name})
    records.append(r)
(HERE / "records.json").write_text(json.dumps(records, indent=1))
print(f"{len(records)} records, {sum(1 for r in records if r.get('design_role'))} design roles, {len(broken)} unreadable {broken[:3]}")
