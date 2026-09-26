#!/usr/bin/env python3
"""Count what design roles are told, over records.json, split by kind (agent, skill). One record is one cluster, so a prompt copied into many repositories counts once."""
import json, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
recs = [r for r in json.loads((HERE / "records.json").read_text()) if r.get("design_role")]
FLAGS = ["inspects_existing_ui", "follows_design_system", "renders_and_looks", "user_context_first", "commits_to_direction", "anti_generic",
         "multiple_variants", "accessibility", "responsive", "states_coverage", "concrete_values", "references_named", "output_contract",
         "self_review_checklist", "asks_before_designing", "boundary_with_implementer"]
pct = lambda n, d: f"{n}/{d} ({100*n/d:.0f}%)" if d else "0/0"
owner = lambda r: r["repo"].split("/")[0]
kinds = {"all": recs, "agent": [r for r in recs if r["kind"] == "agent"], "skill": [r for r in recs if r["kind"] == "skill"]}
print("design roles: " + ", ".join(f"{k} {len(v)} records / {len({owner(r) for r in v})} owners" for k, v in kinds.items()))
print("specificity:", {k: dict(sorted(collections.Counter(r.get('specificity') for r in v).items(), key=lambda x: (x[0] is None, x[0]))) for k, v in kinds.items()})
print("external_files:", {k: pct(sum(bool(r.get('external_files')) for r in v), len(v)) for k, v in kinds.items()})
for field in ("outputs", "modes", "surfaces"):
    print(f"\n{field}:")
    for k, v in kinds.items():
        c = collections.Counter(x for r in v for x in r.get(field, []))
        print(f"  {k:6s} " + ", ".join(f"{x} {n} ({100*n/len(v):.0f}%)" for x, n in c.most_common()))
print(f"\n{'flag':28s} {'all':16s} {'agent':16s} {'skill':16s}")
for f in FLAGS:
    print(f"  {f:26s} " + " ".join(f"{pct(sum(r['flags'].get(f, False) for r in v), len(v)):16s}" for v in kinds.values()))
print("\nflag rate by mode (all kinds):")
for m in ("create", "revise-existing", "review"):
    v = [r for r in recs if m in r.get("modes", [])]
    print(f"  {m:16s} n={len(v):3d} " + " ".join(f"{f[:10]}={100*sum(r['flags'][f] for r in v)/len(v):.0f}" for f in FLAGS[:8]) if v else f"  {m}: none")
print("\nnot design roles:", collections.Counter((r.get("not_design_reason") or "")[:60] for r in json.loads((HERE / "records.json").read_text()) if not r.get("design_role")).most_common(12))
