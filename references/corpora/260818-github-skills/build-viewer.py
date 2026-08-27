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

    # 170 records the reading pass called null hold a quote after all. Its prompt
    # ended the copying rule with "null is the right answer for most files", and
    # deleting those forty-five characters more than doubled the yield on a
    # controlled re-read — 15% to 35% on 135 records, with the control arm rising
    # too. Every recovered quote is located in its source like the rest.
    rf = HERE / "runs" / "null-recovered.json"
    for r in (json.loads(rf.read_text()) if rf.exists() else []):
        base = next((x for x in rows if x["skill"] == r["skill"]), None)
        if base is not None:
            base.update({k: r[k] for k in ("quote", "quote_reason", "quote_file")
                         if k in r})
            base["quote_ok"] = True

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
    # `specificity.json` is the one column of `shortlist.json` this reads, at 0.2 MB
    # against 6. The shortlist is rebuilt from the manifest and stays out of the
    # repository; this is checked in so the page can be rebuilt from a clone.
    # It keys on (repo, dir): the shortlist also carries `loose_file` and the
    # reading pass did not, and a three-part join lost 450 AGENTS.md records.
    spec = {}
    for k, v in json.loads((HERE / "specificity.json").read_text()).items():
        repo, _, d = k.partition("\t")
        spec[(repo, d)] = v

    # Pass 3: how far the claim travels, and the Korean. Later files win, so the
    # re-translation of the 61 quotes that came back in their own language
    # overrides the echo. `untranslated` and `lost_quote` ride along: a
    # translation that altered a token or never happened is still shown, because
    # the English beside it is what was verified, but it is not shown silently.
    facet = {}
    for name in ("facet.jsonl", "facet-ko-fix.jsonl", "facet-recovered.jsonl"):
        f = HERE / "runs" / name
        for line in (f.read_text().splitlines() if f.exists() else []):
            fr = json.loads(line)
            if fr.get("ok"):
                facet[fr["skill"]] = fr

    # What each claim is about, named without a category list to choose from and
    # checked by re-running the naming with the claims regrouped: 81% agree,
    # against 0.3% for randomly paired claims. It is the only judgement here whose
    # reproducibility was measured, which is why it carries the search.
    about = {}
    tf = HERE / "runs" / "topic.jsonl"
    for line in (tf.read_text().splitlines() if tf.exists() else []):
        a = json.loads(line)
        if a.get("ok") and a.get("seed", 0) == 0:
            about[a["skill"]] = a["about"]

    # The clusters that survived being read — 6 of 23 came back "not a subject",
    # grouped on a shared word and nothing else, and those are not shown.
    cl = {}
    cf = HERE / "runs" / "cluster-read.jsonl"
    for line in (cf.read_text().splitlines() if cf.exists() else []):
        c = json.loads(line)
        if c.get("ok") and c.get("coherent"):
            for s in c["skills"]:
                cl[s] = c["subject"]

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
            "ab": about.get(r["skill"]),
            "cs": cl.get(r["skill"]),
            **(lambda f: {
                "tr": f.get("transfer"),
                "tw": f.get("transfer_why"),
                "kq": f.get("ko_quote"),
                "kr": f.get("ko_reason"),
                "ks": f.get("ko_summary"),
                # 6 quotes came back in their own language and 6 lost a token
                # in translation; both are marked rather than hidden or dropped.
                "kbad": bool(f.get("untranslated")) or bool(f.get("lost_quote")),
            })(facet.get(r["skill"], {})),
        })

    scored = [x["sp"] for x in out if x["sp"] is not None]
    scored.sort()
    cuts = [scored[len(scored) * i // 4] for i in (1, 2, 3)]
    blob = json.dumps({"rows": out, "cuts": cuts}, separators=(",", ":"), ensure_ascii=False)

    tpl = (HERE / "viewer-template.html").read_text()
    if "__DATA__" not in tpl:
        raise SystemExit("viewer-template.html has no __DATA__ placeholder")
    (HERE / "viewer.html").write_text(tpl.replace("__DATA__", blob))
    print(f"  about: {sum(1 for x in out if x.get('ab'))} named, "
          f"{len(set(x['ab'] for x in out if x.get('ab')))} distinct, "
          f"{sum(1 for x in out if x.get('cs'))} in a read cluster")
    print(f"  facet: {sum(1 for x in out if x.get('tr'))} rated, "
          f"{sum(1 for x in out if x.get('ks'))} translated, "
          f"{sum(1 for x in out if x.get('kbad'))} flagged")
    q = sum(1 for x in out if x["q"])
    print(f"  relabelled: {sum(1 for x in out if x['k'] in fixed)}, "
          f"repo verdict on {sum(1 for x in out if x['rl'])} rows "
          f"from {len(repo1)} repositories")
    print(f"viewer.html: {len(out)} rows ({q} with a quote), "
          f"specificity on {sum(1 for x in out if x['sp'] is not None)}, "
          f"{(HERE / 'viewer.html').stat().st_size / 1e6:.1f} MB")


main()
