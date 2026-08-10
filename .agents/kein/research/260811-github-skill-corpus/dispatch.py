#!/usr/bin/env python3
"""Send a stratified shortlist through codex-luna and collect one record per skill.

Division of labour. Shape — whether a file instructs, explains, or lists — is
structural and is computed here, because a regex counts imperatives more
cheaply and more consistently than a model does. The model is spent on the one
question nothing local can answer: what does this skill assert about its domain
that could not have been derived from knowing the domain exists.

Selection is stratified by domain and includes a control band drawn from below
the specificity median, so that the triage score can be checked against the
model's own judgement rather than assumed.

Usage:
  ./dispatch.py select              # writes shortlist.json
  ./dispatch.py run [--workers N]   # writes results/*.jsonl
  ./dispatch.py collect             # writes classified.json
"""

import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus"
RESULTS = HERE / "results"

PER_DOMAIN = 70      # top by specificity within each domain
CONTROLS = 80        # drawn from below the median, to test the triage score
BATCH = 6

FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.S)
IMPERATIVE = re.compile(
    r"^\s*(?:[-*]|\d+\.)?\s*(?:You MUST |ALWAYS |NEVER |Do not |Don't |"
    r"Use |Run |Read |Write |Check |Ensure |Verify |Create |Add |Set |Call |"
    r"Avoid |Prefer |Stop |Return |Report |Follow |Apply )", re.M)
HEADING = re.compile(r"^#{1,6} ", re.M)
FENCE = re.compile(r"^```", re.M)


def shape(text):
    """Instruction, guidebook, or reference — from form, not from meaning."""
    b = FRONTMATTER.sub("", text)
    lines = [l for l in b.splitlines() if l.strip()]
    if not lines:
        return "empty", {}
    imperatives = len(IMPERATIVE.findall(b))
    headings = len(HEADING.findall(b))
    fenced = len(FENCE.findall(b)) // 2
    bullets = sum(1 for l in lines if re.match(r"^\s*(?:[-*]|\d+\.)\s", l))
    sentences = len(re.findall(r"[.!?](?:\s|$)", b))
    sig = {
        "imperative_per_100_lines": round(100 * imperatives / len(lines), 1),
        "bullet_ratio": round(bullets / len(lines), 2),
        "headings": headings,
        "code_blocks": fenced,
        "sentences": sentences,
    }
    if sig["imperative_per_100_lines"] >= 12 and sig["bullet_ratio"] >= 0.3:
        return "instruction", sig
    if fenced >= 6 and sig["bullet_ratio"] < 0.45:
        return "reference", sig
    if sig["bullet_ratio"] < 0.3 and sentences > 25:
        return "guidebook", sig
    return "mixed", sig


PROMPT = """You are reading {n} Claude Code skill files collected from public GitHub repositories. \
They are at these paths, relative to the current working directory:

{paths}

Read each one in full.

For each file, decide the one thing that matters: does this skill assert anything about its \
domain that someone could NOT have produced by knowing only that the domain exists? A claim earns \
this if it names a specific failure, a threshold, a tool's actual behaviour, an ordering that \
matters, or a trade-off with a stated reason. It does not earn it by being well organised, by \
restating best practice, or by being confidently worded.

Most files will have nothing. Saying so is the correct answer and is more useful than a generous \
reading. Do not manufacture a claim to fill the field.

Output exactly {n} lines, one compact JSON object per line, no markdown fence, no commentary \
before or after. Each object has exactly these keys:

  "file"   the path as given above
  "domain" two or three words for what it is actually about
  "claim"  the strongest non-derivable claim, quoted or closely paraphrased, max 40 words. \
Empty string if there is none.
  "why"    max 25 words on what makes that claim non-derivable. Empty string if "claim" is empty.
  "note"   max 25 words for a later reader deciding whether to open this file. Be blunt; \
"generic, skip" is a useful note.
  "worth"  integer 0-3. 0 nothing here. 1 competent but derivable. 2 has one real claim. \
3 several, or one that would change how someone writes prompts.
"""


def select():
    triage = json.loads((HERE / "triage.json").read_text())
    scores = sorted(r["specificity"] for r in triage)
    median = scores[len(scores) // 2]

    picked, seen = [], set()
    by_domain = defaultdict(list)
    for r in triage:
        for d in r["domains"] or ["(none)"]:
            by_domain[d].append(r)
    for d, rs in sorted(by_domain.items()):
        rs.sort(key=lambda r: -r["specificity"])
        taken = 0
        for r in rs:
            if taken >= PER_DOMAIN:
                break
            if r["file"] in seen:
                continue
            seen.add(r["file"])
            r = dict(r, band="top", stratum=d)
            picked.append(r)
            taken += 1

    low = [r for r in triage if r["specificity"] < median and r["file"] not in seen]
    step = max(1, len(low) // CONTROLS)
    for r in low[::step][:CONTROLS]:
        seen.add(r["file"])
        picked.append(dict(r, band="control", stratum="control"))

    for r in picked:
        text = (CORPUS / r["file"]).read_text(errors="replace")
        r["shape"], r["shape_signals"] = shape(text)

    (HERE / "shortlist.json").write_text(json.dumps(picked, indent=1))
    print(f"shortlist {len(picked)} files (median specificity {median})")
    print("  by stratum: " + ", ".join(f"{k}={v}" for k, v in Counter(r["stratum"] for r in picked).items()))
    print("  by shape:   " + ", ".join(f"{k}={v}" for k, v in Counter(r["shape"] for r in picked).most_common()))
    print(f"  batches of {BATCH}: {(len(picked) + BATCH - 1) // BATCH}")


def _one(batch):
    i, files = batch
    out = RESULTS / f"batch-{i:03d}.jsonl"
    if out.exists() and out.stat().st_size > 0:
        return i, "cached"
    paths = "\n".join(f"  corpus/{f}" for f in files)
    prompt = PROMPT.format(n=len(files), paths=paths)
    p = subprocess.run(
        ["ocs", "ask", "codex", "--agent", "explore",
         "--model", "gpt-5.6-luna", "--effort", "low", prompt],
        capture_output=True, text=True, cwd=HERE, timeout=900)
    if p.returncode != 0:
        return i, f"exit {p.returncode}: {p.stderr.strip()[:160]}"
    lines = [l for l in p.stdout.splitlines() if l.strip().startswith("{")]
    if not lines:
        return i, f"no json: {p.stdout.strip()[:160]}"
    out.write_text("\n".join(lines) + "\n")
    return i, f"{len(lines)}/{len(files)}"


def run(workers=6):
    shortlist = json.loads((HERE / "shortlist.json").read_text())
    RESULTS.mkdir(exist_ok=True)
    files = [r["file"] for r in shortlist]
    batches = [(i, files[i * BATCH:(i + 1) * BATCH])
               for i in range((len(files) + BATCH - 1) // BATCH)]
    batches = [b for b in batches if b[1]]
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for i, status in pool.map(_one, batches):
            done += 1
            if status != "cached":
                print(f"[{done}/{len(batches)}] batch {i}: {status}", flush=True)
    print(f"run: {done} batches")


def collect():
    shortlist = {r["file"]: r for r in json.loads((HERE / "shortlist.json").read_text())}
    got, bad = {}, 0
    for f in sorted(RESULTS.glob("batch-*.jsonl")):
        for line in f.read_text().splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                bad += 1
                continue
            key = rec.get("file", "").replace("corpus/", "").strip()
            if key in shortlist:
                got[key] = rec
            else:
                bad += 1

    merged = []
    for key, r in shortlist.items():
        rec = got.get(key)
        merged.append({
            "file": key, "repo": r["repo"], "path": r["path"], "name": r["name"],
            "stars": None, "words": r["words"], "specificity": r["specificity"],
            "markers": r["markers"], "shape": r["shape"], "band": r["band"],
            "stratum": r["stratum"], "cluster_size": r["cluster_size"],
            "domain": (rec or {}).get("domain", ""),
            "claim": (rec or {}).get("claim", ""),
            "why": (rec or {}).get("why", ""),
            "note": (rec or {}).get("note", ""),
            "worth": (rec or {}).get("worth"),
            "read": rec is not None,
        })
    repos = {r["full_name"]: r for r in json.loads((HERE / "repos.json").read_text())}
    for m in merged:
        m["stars"] = repos.get(m["repo"], {}).get("stars")
    merged.sort(key=lambda m: (-(m["worth"] or -1), -m["specificity"]))
    (HERE / "classified.json").write_text(json.dumps(merged, indent=1))

    read = [m for m in merged if m["read"]]
    print(f"collect: {len(read)}/{len(merged)} classified, {bad} unusable lines")
    print("  worth: " + ", ".join(f"{k}={v}" for k, v in sorted(Counter(m["worth"] for m in read).items(), key=lambda x: str(x[0]))))
    for band in ("top", "control"):
        b = [m for m in read if m["band"] == band]
        if b:
            hi = sum(1 for m in b if (m["worth"] or 0) >= 2)
            print(f"  {band}: {hi}/{len(b)} scored 2+")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "select"
    if cmd == "run":
        w = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 6
        run(w)
    else:
        {"select": select, "collect": collect}[cmd]()
