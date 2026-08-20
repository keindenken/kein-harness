#!/usr/bin/env python3
"""Pass 2: one skill directory per model call.

The unit is the directory, not the file. 260811 read `SKILL.md` alone and then
concluded that prompts shrink by moving obligations down a level — a conclusion
about files it had never fetched. `n8n-agents` is 23 KB as a single file and
122 KB as a directory, and the eleven references hold most of it.

`assemble.py` builds the document: prose inlined under a path-carrying tag,
scripts and binaries listed by name and size and left on disk. The question this
pass asks is for a sentence, and a Python file does not answer it; what the
scripts contribute is the shape of the skill, which a file list carries.

Dependency labels are not asked of the model. `labels.py` derives them, because
the model reported `calls: ["none"]` for a file that says `uv run` forty-seven
times. It never reports absence, though — a quarter of one pilot disagreed with
the model and each side was right about something the other could not see.

Every quote is located in the assembled document before the record is written,
and the file it was found in is recorded. That last field is the measurement
260811 could not take: whether a skill's non-derivable claims sit in `SKILL.md`
or in the references they were moved to.

Usage:
  ./extract.py <manifest.json> <out.jsonl> [--prompt P] [--model M] [--workers N] [--effort E] [--limit N]
"""
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = Path(os.environ.get("CORPUS", HERE / "corpus"))
sys.path.insert(0, str(HERE))
from verify import norm          # noqa: E402
from labels import label         # noqa: E402
from assemble import assemble    # noqa: E402

DEFAULT_PROMPT = HERE / "prompt" / "extract.md"

# Haiku rather than luna, for a reason that is about the accounts and not the
# models: the ChatGPT plan is the $20 one and the cross-vendor audit lane already
# lives there, while the Claude plan has room three Opus sessions do not fill.
# Bulk corpus reading should not compete with the lane the harness reviews with.
#
# They measure the same on the fixture — 7/8 and 8/8 on the positives, 1/8 on
# the negatives for both, 10/15 and 9-15 unlabelled — which is inside the run to
# run spread. Haiku is the one that drifts mid-quote, though: on
# `mvanhorn/last30days-skill` it copied 105 characters exactly and then finished
# the sentence in its own words. The verbatim check caught it, and that is what
# the check is for, but a paraphrase that stops one clause earlier would pass.
DEFAULT_MODEL = "claude-haiku-4-5"

# Two vendors, one prompt. `codex exec` and `claude -p` both take a prompt on
# stdin and print the reply, so swapping the reader is a flag rather than a
# rewrite — and the fixture is what decides whether a swap is safe.
def call(prompt, model, effort):
    """Return (reply, stderr, usage). `usage` is empty for Codex.

    Claude's `--output-format json` wraps the reply in an envelope carrying cost
    and token counts. It is the only per-call gauge either vendor offers — Luna's
    `used_percent` moves in whole points and says nothing until it does — and a
    run without it can only be costed by extrapolating a one-off measurement,
    which is what the first 814 of this pass are stuck with.
    """
    if model.startswith("gpt-"):
        cmd = ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
               "-m", model, "-c", f"model_reasoning_effort={effort}", "-C", "/tmp", "-"]
        p = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                           cwd="/tmp", timeout=900)
        return p.stdout, p.stderr, {}
    cmd = ["claude", "-p", "--model", model, "--output-format", "json"]
    p = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                       cwd="/tmp", timeout=900)
    try:
        env = json.loads(p.stdout)
    except Exception:
        return p.stdout, p.stderr, {}          # fall back to the raw reply
    u = env.get("usage", {})
    return env.get("result", ""), p.stderr, {
        "cost_usd": env.get("total_cost_usd"),
        "in_new": u.get("cache_creation_input_tokens"),
        "in_cached": u.get("cache_read_input_tokens"),
        "out": u.get("output_tokens"),
        "thinking": (u.get("output_tokens_details") or {}).get("thinking_tokens"),
    }



def parse(raw):
    """Pull the JSON object out of a reply.

    A brace-counting regex is not enough: a quote can carry braces of its own,
    and `{{ $json.output }}` inside one silently ends the object early. This
    scans with the string state that JSON actually has.
    """
    raw = raw.strip()
    try:
        return json.loads(raw)
    except Exception:
        pass
    for start in (m.start() for m in re.finditer(r"\{", raw)):
        depth, i, instr, esc = 0, start, False, False
        while i < len(raw):
            c = raw[i]
            if instr:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    instr = False
            elif c == '"':
                instr = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(raw[start:i + 1])
                    except Exception:
                        break
            i += 1
    return None


def _locate(quote, doc):
    """Which inlined file holds this quote, if any.

    Matching runs over the same normalisation `verify.py` uses, so a sentence
    lifted out of a wrapped `# ` comment or a `- **bold:**` bullet still lands.
    """
    if not quote:
        return None, False
    nq = norm(quote)
    for m in re.finditer(r'<file path="([^"]+)">\n(.*?)\n</file>', doc, re.S):
        if nq in norm(m.group(2)):
            return m.group(1), True
    return None, nq in norm(doc)


def one(args):
    skill, effort, model, tpl, tag = args
    key = f"{skill['repo']}/{skill['dir']}" if skill["dir"] else skill["repo"]
    try:
        doc, meta = assemble(skill, CORPUS)
    except OSError as e:
        return {"skill": key, "ok": False, "error": f"assemble: {e}"}
    out, err, usage = call(tpl.replace("{{FILE}}", key).replace("{{BODY}}", doc), model, effort)
    rec = parse(out)
    if rec is None:
        return {"skill": key, "ok": False, "error": (out or err)[-300:], "prompt": tag, "model": model, **usage, **meta}
    q = rec.get("quote")
    where, found = _locate(q, doc)
    # A null quote means one of two things and they are not the same event: the
    # skill holds no qualifying sentence, or the file holding it was never shown.
    # In the star-band run every record was anchors-only, so 80 of 150 were asked
    # about a skill with prose siblings the model could not see — and among eight
    # directories read at full depth, four of six quotes came from a sibling.
    unread_prose = [n for n in meta["not_inlined"]
                    if n.lower().endswith((".md", ".txt"))]
    return {
        "skill": key, "repo": skill["repo"], "dir": skill["dir"], "ok": True,
        "summary": rec.get("summary", ""), "drives": rec.get("drives", []),
        "quote": q, "quote_reason": rec.get("quote_reason"),
        "quote_ok": found, "quote_file": where,
        "partial": bool(unread_prose), "unread_prose": unread_prose, "prompt": tag, "model": model, **usage,
        **label(doc), **meta,
    }


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    w, effort, limit, model = 4, "medium", None, DEFAULT_MODEL
    prompt_path = DEFAULT_PROMPT
    for i, a in enumerate(sys.argv):
        if a == "--model":
            model = sys.argv[i + 1]
        if a == "--prompt":
            prompt_path = Path(sys.argv[i + 1])
        if a == "--workers":
            w = int(sys.argv[i + 1])
        if a == "--effort":
            effort = sys.argv[i + 1]
        if a == "--limit":
            limit = int(sys.argv[i + 1])
    # Which prompt produced a record belongs in the record. Swapping the file
    # under a fixed path is how the variants were first compared, and it leaves
    # the seam visible only in whoever remembers running it.
    tpl, tag = prompt_path.read_text(), prompt_path.stem
    skills = json.loads(src.read_text())[:limit]
    done = ({json.loads(l)["skill"] for l in out.read_text().splitlines()}
            if out.exists() else set())
    todo = [s for s in skills
            if (f"{s['repo']}/{s['dir']}" if s["dir"] else s["repo"]) not in done]
    print(f"{len(skills)} skills, {len(done)} already done, {len(todo)} to run, prompt={tag}", flush=True)
    t0, n = time.time(), 0
    with out.open("a") as fh, ThreadPoolExecutor(max_workers=w) as pool:
        for rec in pool.map(one, ((s, effort, model, tpl, tag) for s in todo)):
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            n += 1
            if n % 20 == 0 or n == len(todo):
                print(f"  {n}/{len(todo)}  {int(time.time()-t0)}s", flush=True)


main()
