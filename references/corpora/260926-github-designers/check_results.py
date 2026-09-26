#!/usr/bin/env python3
"""Validate <RESULTS>/<batch>/<id>.json: shape, ids against the manifest, and that every quote is verbatim in its file.

Whitespace and markdown emphasis are normalised before matching, since a quote that differs only in line wrapping or
`**` is still the author's sentence; anything else is reported.
"""
import json, os, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
FLAGS = {"inspects_existing_ui", "renders_and_looks", "follows_design_system", "anti_generic", "commits_to_direction",
         "multiple_variants", "user_context_first", "accessibility", "responsive", "states_coverage", "concrete_values",
         "references_named", "output_contract", "self_review_checklist", "asks_before_designing", "boundary_with_implementer"}
KEYS = {"id", "kind", "repo", "path", "design_role", "not_design_reason", "outputs", "modes", "surfaces", "flags",
        "instructions", "external_files", "specificity", "notes"}
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[*_`>#\\]", "", s)).strip().lower()
RES = HERE / (os.environ.get("RESULTS") or "results")
batches = sys.argv[1:] or sorted(p.name for p in RES.iterdir() if p.is_dir())
problems, bad, quotes, n, design = [], [], 0, 0, 0
for b in batches:
    manifest = {m["id"]: m for m in json.loads((HERE / "batches" / f"{b}.json").read_text())}
    got = {}
    for p in (RES / b).glob("*.json"):
        try:
            got[p.stem] = json.loads(p.read_text())
        except json.JSONDecodeError as e:
            problems.append(f"{b}/{p.name}: invalid JSON {e}")
    if set(got) != set(manifest):
        problems.append(f"{b}: missing {sorted(set(manifest) - set(got))} extra {sorted(set(got) - set(manifest))}")
    for i, r in got.items():
        n += 1
        m = manifest.get(i)
        if not m:
            continue
        if set(r) != KEYS:
            problems.append(f"{b}/{i}: keys differ {sorted(set(r) ^ KEYS)}")
        if set(r.get("flags", {})) != FLAGS:
            problems.append(f"{b}/{i}: flag keys differ {sorted(set(r.get('flags', {})) ^ FLAGS)}")
        design += bool(r.get("design_role"))
        src = norm((HERE / m["file"]).read_text())
        for q in r.get("instructions", []):
            quotes += 1
            parts = [norm(x) for x in re.split(r"\.\.\.|…", q["quote"]) if len(norm(x)) > 8] or [norm(q["quote"])]
            if not all(x in src for x in parts):
                bad.append(f"{b}/{i}: {q['quote'][:90]}")
print(f"{len(batches)} batches, {n} records, {design} design roles, {quotes} quotes, {len(bad)} not verbatim, {len(problems)} shape problems")
for x in problems[:20] + bad[:30]:
    print("  ", x)
