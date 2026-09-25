#!/usr/bin/env python3
"""Validate results/*.json: shape, ids against the manifest, and that every quote is verbatim in its file.

Whitespace and markdown emphasis are normalised before matching, since a quote that differs only
in line wrapping or `**` is still the author's sentence; anything else is reported.
"""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
FLAGS = {"audience_first","verify_against_source","cite_sources","separate_fact_from_opinion","cut_or_concise","fixed_template",
         "names_style_guide","examples_in_prompt","output_contract","self_review_checklist","asks_before_writing",
         "research_before_writing","updates_existing_docs","reasoning_kept_out"}
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[*_`>#\\]", "", s)).strip().lower()
RES = HERE / (__import__("os").environ.get("RESULTS") or "results")
batches = sys.argv[1:] or sorted(p.stem for p in RES.glob("*.json"))
problems, quotes, bad_quotes, n, writing = [], 0, [], 0, 0
for b in batches:
    p = RES / f"{b}.json"
    if not p.exists():
        problems.append(f"{b}: missing"); continue
    try:
        data = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        problems.append(f"{b}: invalid JSON {e}"); continue
    manifest = {m["id"]: m for m in json.loads((HERE / "batches" / f"{b}.json").read_text())}
    got = {it.get("id") for it in data.get("items", [])}
    if got != set(manifest):
        problems.append(f"{b}: ids differ, missing {sorted(set(manifest) - got)} extra {sorted(got - set(manifest))}")
    for it in data.get("items", []):
        n += 1
        m = manifest.get(it.get("id"))
        if not m: continue
        if set(it.get("flags", {})) != FLAGS:
            problems.append(f"{b}/{it['id']}: flag keys differ")
        writing += bool(it.get("writing_role"))
        src = norm((HERE / m["file"]).read_text())
        for q in it.get("instructions", []):
            quotes += 1
            if norm(q["quote"].strip(".… ")) not in src and not all(norm(part) in src for part in re.split(r"\.\.\.|…", q["quote"]) if len(norm(part)) > 8):
                bad_quotes.append(f"{b}/{it['id']}: {q['quote'][:90]}")
print(f"{len(batches)} batches, {n} records, {writing} writing roles, {quotes} quotes, {len(bad_quotes)} not verbatim, {len(problems)} shape problems")
for x in problems[:20] + bad_quotes[:20]:
    print("  ", x)
