#!/usr/bin/env python3
"""Pass 2: one skill file per model call. Produces the per-file record the repo
pass reads, and is the half that needs no sibling context.

Dependency labels are not asked of the model; `labels.py` derives them from the
file. The model is spent only on the summary and the quote.

Every quote is located in its source before the record is written, so a row that
survives to disk is one a grep can reproduce. `quote_ok: false` means the model
returned prose that is not in the file; the quote is kept for inspection and the
row is marked rather than dropped.

Usage: ./extract.py <list.txt> <out.jsonl> [--workers N] [--effort E] [--limit N]
"""
import json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = Path(os.environ.get('CORPUS', HERE.parent / '260811-github-skills' / 'corpus'))
sys.path.insert(0, str(HERE))
from verify import norm
from labels import label

TPL = (HERE / 'prompt' / 'extract.md').read_text()

def parse(raw):
    for cand in reversed(re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', raw, re.S)):
        try: return json.loads(cand)
        except Exception: continue
    return None

def one(args):
    f, effort = args
    src = (CORPUS / f).read_text(errors='replace')
    p = subprocess.run(
        ['codex', 'exec', '--skip-git-repo-check', '--sandbox', 'read-only',
         '-m', 'gpt-5.6-luna', '-c', f'model_reasoning_effort={effort}', '-C', '/tmp', '-'],
        input=TPL.replace('{{FILE}}', f).replace('{{BODY}}', src),
        capture_output=True, text=True, timeout=900)
    rec = parse(p.stdout)
    if rec is None:
        return {'file': f, 'ok': False, 'error': p.stdout[-300:] or p.stderr[-300:]}
    q = rec.get('quote')
    return {'file': f, 'ok': True,
            'summary': rec.get('summary', ''), 'drives': rec.get('drives', []),
            'quote': q, 'quote_reason': rec.get('quote_reason'),
            'quote_ok': bool(q) and norm(q) in norm(src),
            **label(src)}

def main():
    lst, out = Path(sys.argv[1]), Path(sys.argv[2])
    w = 4; effort = 'medium'; limit = None
    for i, a in enumerate(sys.argv):
        if a == '--workers': w = int(sys.argv[i+1])
        if a == '--effort': effort = sys.argv[i+1]
        if a == '--limit': limit = int(sys.argv[i+1])
    files = lst.read_text().split()[:limit]
    done = {json.loads(l)['file'] for l in out.read_text().splitlines()} if out.exists() else set()
    todo = [f for f in files if f not in done]
    print(f"{len(files)} files, {len(done)} already done, {len(todo)} to run", flush=True)
    t0 = time.time(); n = 0
    with out.open('a') as fh, ThreadPoolExecutor(max_workers=w) as pool:
        for rec in pool.map(one, ((f, effort) for f in todo)):
            fh.write(json.dumps(rec, ensure_ascii=False) + '\n'); fh.flush()
            n += 1
            if n % 10 == 0 or n == len(todo):
                print(f"  {n}/{len(todo)}  {int(time.time()-t0)}s", flush=True)

main()
