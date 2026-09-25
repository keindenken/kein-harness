#!/usr/bin/env python3
"""Fold results-sonnet/<batch>/<id>.json into records.json, one record per cluster, joined with the cluster's metadata."""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
clusters = {f"c{i:05d}": c for i, c in enumerate(json.loads((HERE / "clusters.json").read_text()))}
records, broken = [], []
for f in sorted((HERE / "results-sonnet").glob("*/*.json")):
    try:
        r = json.loads(f.read_text())
    except json.JSONDecodeError:
        broken.append(str(f)); continue
    c = clusters.get(r.get("id"))
    if c:
        r.update({"stars": c["stars"], "copies_in_repos": c["repos"], "members": c["members"], "words": c["words"], "batch": f.parent.name})
    records.append(r)
(HERE / "records.json").write_text(json.dumps(records, indent=1))
print(f"{len(records)} records, {sum(1 for r in records if r.get('writing_role'))} writing roles, {len(broken)} unreadable {broken[:3]}")
