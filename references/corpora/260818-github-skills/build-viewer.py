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

    # Four quotes the checker had rejected are real: `norm` did not fold curly
    # quotes to straight ones, and did not reduce `[text](url)` to its text.
    # 89 of the 93 rejections survive the fix, which is the answer to whether
    # the check was too strict — it was not, it was slightly wrong.
    requote = {}
    rq = HERE / "runs" / "quote-recheck.jsonl"
    for line in (rq.read_text().splitlines() if rq.exists() else []):
        r = json.loads(line)
        if r["quote_ok"]:
            requote[r["skill"]] = r

    # The repository pass runs in chunks, highest-value repositories first, and
    # everything it has not reached gets no verdict rather than a default one —
    # `미판정` is a real answer, and its count is the honest size of the gap.
    repo1 = {}
    p1 = HERE / "runs" / "pass1.jsonl"
    for line in (p1.read_text().splitlines() if p1.exists() else []):
        r = json.loads(line)
        # A verdict reached from one skill directory is not a verdict. Asked what
        # a collection's files share, a reader shown one file has no siblings to
        # compare, and 100% of those came back `one-field` at every coverage band
        # but the lowest — one skill has one subject. The model said as much in
        # `house_style` ("cannot be determined from a single file"); the
        # `coherence` field had no way to say it.
        if r.get("ok") and r["n_read"] >= 2:
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
            # A sentence the checker could not find in the source is kept and
            # shown, but it is not a quote: the page's one guarantee is that a
            # quote was located in the file it claims to come from. 93 of these
            # read as the model drifting into paraphrase mid-sentence.
            "qv": bool(r.get("quote_ok") or r["skill"] in requote),
            "qr": r.get("quote_reason"),
            "qf": (requote.get(r["skill"]) or r).get("quote_file"),
            "rc": (fixed.get(r["skill"], r).get("reach")) or [],
            "cl": (fixed.get(r["skill"], r).get("cli")) or [],
            "rl": (repo1.get(r.get("repo")) or {}).get("coherence"),
            # How much of the repository the verdict was reached from. It belongs
            # next to the verdict because it changes what the verdict means:
            # holding repository size fixed, reading less of one pushes it toward
            # `grab-bag`, so part of that label is the reader's uncertainty.
            "rv": (lambda x: round(100 * x["n_read"] / x["n_total"]) if x else None)(repo1.get(r.get("repo"))),
            "rf": ((repo1.get(r.get("repo")) or {}).get("field")
                   or (repo1.get(r.get("repo")) or {}).get("form")),
            "dr": (r.get("drives") or [])[:10],
            "m": "luna" if r.get("model") == "gpt-5.6-luna" else "haiku",
            "p": r.get("prompt") or "extract",
            "sp": spec.get((r.get("repo"), r.get("dir"))),
            "st": stars.get(r.get("repo")),
            # Whether this skill has a `SKILL.md` at all. 408 records are anchored
            # on a root `AGENTS.md` or `CLAUDE.md` and have none, so `quote_file
            # != SKILL.md` marked them as a claim that had moved down a level
            # when there was no level above it to move from.
            "hm": "SKILL.md" in (r.get("inlined") or []),
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
