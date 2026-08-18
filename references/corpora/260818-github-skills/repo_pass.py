#!/usr/bin/env python3
"""Pass 1: one repository's whole skill collection per model call.

This runs after `extract.py`, not before it. Feeding a repository's raw files to
one call means the deciding read is the shallow one, and a 770 KB collection does
not fit in a call anyway; feeding it the per-file records instead costs a second
pass that is nearly free and gives this call a better input than the source.

Usage: ./repo_pass.py <pass2.jsonl> <out.jsonl> [--model M] [--workers N]
"""
import json, re, subprocess, sys, time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = (HERE / 'prompt' / 'repo.md').read_text()
INDEX = json.loads((HERE.parent / '260811-github-skills' / 'index.json').read_text())
PATH_OF = {r['file']: (r['repo'], r['path']) for r in INDEX}

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

def one(args):
    repo, recs, model = args
    body = []
    for r in recs:
        _, path = PATH_OF.get(r['file'], ('', r['file']))
        body.append(json.dumps({
            'file': path, 'summary': r.get('summary'),
            'reach': r.get('reach'), 'mcp': r.get('mcp'), 'cli': r.get('cli'),
            'quote': r.get('quote'), 'quote_verified': r.get('quote_ok'),
        }, ensure_ascii=False))
    p = subprocess.run(
        ['claude', '-p', '--model', model],
        input=TPL.replace('{{REPO}}', repo).replace('{{RECORDS}}', '\n'.join(body)),
        capture_output=True, text=True, cwd='/tmp', timeout=900)
    rec = parse(p.stdout)
    if rec is None:
        return {'repo': repo, 'ok': False, 'error': (p.stdout or p.stderr)[-400:]}
    return {'repo': repo, 'ok': True, 'n_files': len(recs), **rec}

def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    model = 'sonnet'; w = 3
    for i, a in enumerate(sys.argv):
        if a == '--model': model = sys.argv[i+1]
        if a == '--workers': w = int(sys.argv[i+1])
    by = defaultdict(list)
    for line in src.read_text().splitlines():
        r = json.loads(line)
        if r.get('ok'): by[PATH_OF.get(r['file'], ('?',))[0]].append(r)
    done = {json.loads(l)['repo'] for l in out.read_text().splitlines()} if out.exists() else set()
    todo = [(k, v, model) for k, v in sorted(by.items()) if k not in done]
    print(f"{len(by)} repos, {len(todo)} to run, model={model}", flush=True)
    t0 = time.time()
    with out.open('a') as fh, ThreadPoolExecutor(max_workers=w) as pool:
        for rec in pool.map(one, todo):
            fh.write(json.dumps(rec, ensure_ascii=False) + '\n'); fh.flush()
            print(f"  {rec['repo']:34} {'ok' if rec['ok'] else 'FAIL'}"
                  f"  {int(time.time()-t0)}s", flush=True)

main()
