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
  ./extract.py <manifest.json> <out.jsonl> [--workers N] [--effort E] [--limit N]
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

TPL = (HERE / "prompt" / "extract.md").read_text()


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
    skill, effort = args
    key = f"{skill['repo']}/{skill['dir']}" if skill["dir"] else skill["repo"]
    try:
        doc, meta = assemble(skill, CORPUS)
    except OSError as e:
        return {"skill": key, "ok": False, "error": f"assemble: {e}"}
    p = subprocess.run(
        ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
         "-m", "gpt-5.6-luna", "-c", f"model_reasoning_effort={effort}", "-C", "/tmp", "-"],
        input=TPL.replace("{{FILE}}", key).replace("{{BODY}}", doc),
        capture_output=True, text=True, timeout=900)
    rec = parse(p.stdout)
    if rec is None:
        return {"skill": key, "ok": False, "error": (p.stdout or p.stderr)[-300:], **meta}
    q = rec.get("quote")
    where, found = _locate(q, doc)
    return {
        "skill": key, "repo": skill["repo"], "dir": skill["dir"], "ok": True,
        "summary": rec.get("summary", ""), "drives": rec.get("drives", []),
        "quote": q, "quote_reason": rec.get("quote_reason"),
        "quote_ok": found, "quote_file": where,
        **label(doc), **meta,
    }


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    w, effort, limit = 4, "medium", None
    for i, a in enumerate(sys.argv):
        if a == "--workers":
            w = int(sys.argv[i + 1])
        if a == "--effort":
            effort = sys.argv[i + 1]
        if a == "--limit":
            limit = int(sys.argv[i + 1])
    skills = json.loads(src.read_text())[:limit]
    done = ({json.loads(l)["skill"] for l in out.read_text().splitlines()}
            if out.exists() else set())
    todo = [s for s in skills
            if (f"{s['repo']}/{s['dir']}" if s["dir"] else s["repo"]) not in done]
    print(f"{len(skills)} skills, {len(done)} already done, {len(todo)} to run", flush=True)
    t0, n = time.time(), 0
    with out.open("a") as fh, ThreadPoolExecutor(max_workers=w) as pool:
        for rec in pool.map(one, ((s, effort) for s in todo)):
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            n += 1
            if n % 20 == 0 or n == len(todo):
                print(f"  {n}/{len(todo)}  {int(time.time()-t0)}s", flush=True)


main()
