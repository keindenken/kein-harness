#!/usr/bin/env python3
"""Count what writing-role agents are told, over records.json. One record is one cluster, so a prompt copied into many repositories counts once."""
import json, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
recs = [r for r in json.loads((HERE / "records.json").read_text()) if r.get("writing_role")]
FLAGS = ["audience_first","verify_against_source","cite_sources","separate_fact_from_opinion","cut_or_concise","reasoning_kept_out",
         "research_before_writing","updates_existing_docs","fixed_template","names_style_guide","examples_in_prompt","output_contract",
         "self_review_checklist","asks_before_writing"]
def pct(n, d): return f"{n}/{d} ({100*n/d:.0f}%)" if d else "0/0"
out = {}
N = len(recs)
spec = collections.Counter(r.get("specificity") for r in recs)
hi = [r for r in recs if (r.get("specificity") or 0) >= 4]
print(f"writing roles: {N}; specificity {dict(sorted(spec.items(), key=lambda x: (x[0] is None, x[0])))}; >=4: {len(hi)}")
scope = collections.Counter(r.get("scope") for r in recs)
print("scope:", dict(scope), " | among >=4:", dict(collections.Counter(r.get("scope") for r in hi)))
dt = collections.Counter(t for r in recs for t in r.get("doc_types", []))
print("doc types:", dt.most_common())
print("\nflag                          all            specificity>=4")
for f in FLAGS:
    a = sum(r["flags"].get(f, False) for r in recs); h = sum(r["flags"].get(f, False) for r in hi)
    print(f"  {f:28s} {pct(a, N):16s} {pct(h, len(hi))}")
core = ["audience_first", "verify_against_source", "cut_or_concise"]
allcore = sum(all(r["flags"][f] for f in core) for r in recs); allcore_hi = sum(all(r["flags"][f] for f in core) for r in hi)
print(f"\nall three core (audience, verify, cut): {pct(allcore, N)}; among >=4: {pct(allcore_hi, len(hi))}")
print("\nflag rate by primary doc type (types with >=40 roles):")
for t, n in dt.most_common():
    if n < 40: break
    rs = [r for r in recs if t in r.get("doc_types", [])]
    print(f"  {t:18s} n={n:4d} " + " ".join(f"{f[:8]}={100*sum(r['flags'][f] for r in rs)/len(rs):.0f}" for f in core + ["separate_fact_from_opinion", "cite_sources", "fixed_template"]))
by_repo = collections.defaultdict(list)
for r in recs: by_repo[r["repo"]].append(r)
multi = {k: v for k, v in by_repo.items() if len(v) >= 3}
print(f"\nrepos with >=3 distinct writing roles: {len(multi)}")
for k, v in sorted(multi.items(), key=lambda kv: -len(kv[1]))[:12]:
    print(f"  {k} ({len(v)}): " + ", ".join(sorted({r['path'].rsplit('/',1)[-1].rsplit('.',1)[0] for r in v}))[:150])
