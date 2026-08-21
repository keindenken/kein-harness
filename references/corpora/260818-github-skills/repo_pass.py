#!/usr/bin/env python3
"""Pass 1: one repository's whole skill collection per model call.

This runs after `extract.py`, not before it. Feeding a repository's raw files to
one call means the deciding read is the shallow one, and a 770 KB collection does
not fit in a call anyway; feeding it the per-file records instead costs a second
pass that is nearly free and gives this call a better input than the source.

What it reads is a slice, and the slice is not the collection. `shortlist.py`
deduped near-identical siblings and then capped each repository at twelve, so
745 of 846 repositories arrive here partly read — `garrytan/gstack` at nine files
of sixty-two. The count of what was read and what exists both go into the prompt
and into the record, because a `filler` list over nine of sixty-two is a claim
about nine files wearing a collection's name.

Usage: ./repo_pass.py <pass2.jsonl> <out.jsonl> [--model M] [--workers N]
                      [--only LIST] [--limit N] [--prompt P]
"""
import json, os, re, subprocess, sys, time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = json.loads((HERE / 'manifest.json').read_text())

FETCHED = defaultdict(int)
for _m in MANIFEST:
    FETCHED[_m['repo']] += 1

# Corrected dependency labels, where they exist. The first 150 repositories were
# fed `reach` and `cli` as `extract.py` wrote them, and `labels.py` was
# over-firing then: it matched a binary after any whitespace rather than in
# command position, so `go through` inside a fenced diagram scored `go`. Pass 1
# spent flags reporting that, which is how the bug was found — and would keep
# spending them on a bug that is now fixed.
FIXED = {}
_lv2 = HERE / 'runs' / 'labels-v2.jsonl'
if _lv2.exists():
    for _line in _lv2.read_text().splitlines():
        _r = json.loads(_line)
        FIXED[_r['skill']] = _r


def call(prompt, model):
    """Return (reply, stderr, usage) — the same envelope `extract.py` reads."""
    cmd = ['claude', '-p', '--model', model, '--output-format', 'json']
    p = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                       cwd='/tmp', timeout=900)
    try:
        env = json.loads(p.stdout)
    except Exception:
        return p.stdout, p.stderr, {}
    u = env.get('usage', {})
    return env.get('result', ''), p.stderr, {
        'cost_usd': env.get('total_cost_usd'),
        'in_new': u.get('cache_creation_input_tokens'),
        'in_cached': u.get('cache_read_input_tokens'),
        'out': u.get('output_tokens'),
        'thinking': (u.get('output_tokens_details') or {}).get('thinking_tokens'),
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


def one(args):
    repo, recs, model, tpl, tag = args
    body = []
    for r in recs:
        lab = FIXED.get(r['skill'], r)
        # `quote_file` is the field the pilot did not have. A claim quoted out of
        # `references/ERROR_PATTERNS.md` and one quoted out of `SKILL.md` are
        # different facts about how the collection is built, and only this pass
        # can see the pattern across siblings.
        body.append(json.dumps({
            'file': r['dir'] or r.get('loose_file') or '(repo root)',
            'summary': r.get('summary'),
            'reach': lab.get('reach'), 'mcp': lab.get('mcp'), 'cli': lab.get('cli'),
            'quote': r.get('quote'), 'quote_verified': r.get('quote_ok'),
            'quote_file': r.get('quote_file'),
            'prose_files': len(r.get('inlined') or []),
        }, ensure_ascii=False))
    n_read, n_total = len(recs), max(FETCHED.get(repo, 0), len(recs))
    relabelled = sum(1 for r in recs if r['skill'] in FIXED)
    prompt = (tpl.replace('{{REPO}}', repo)
                 .replace('{{N_READ}}', str(n_read))
                 .replace('{{N_TOTAL}}', str(n_total))
                 .replace('{{RECORDS}}', '\n'.join(body)))
    out, err, usage = call(prompt, model)
    prov = {'repo': repo, 'n_read': n_read, 'n_total': n_total,
            'relabelled': relabelled, 'model': model, 'prompt': tag, **usage}
    rec = parse(out)
    if rec is None:
        return {**prov, 'ok': False, 'error': (out or err)[-400:]}
    rec.pop('repo', None)
    return {**prov, 'ok': True, **rec}


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    model, w, only, limit, tag = 'sonnet', 3, None, None, 'repo'
    for i, a in enumerate(sys.argv):
        if a == '--model': model = sys.argv[i + 1]
        if a == '--workers': w = int(sys.argv[i + 1])
        if a == '--limit': limit = int(sys.argv[i + 1])
        if a == '--prompt': tag = Path(sys.argv[i + 1]).stem
        if a == '--only': only = set(Path(sys.argv[i + 1]).read_text().split())
    tpl = (HERE / 'prompt' / f'{tag}.md').read_text()
    by = defaultdict(list)
    for line in src.read_text().splitlines():
        r = json.loads(line)
        if r.get('ok'):
            by[r['repo']].append(r)
    done = ({json.loads(l)['repo'] for l in out.read_text().splitlines()}
            if out.exists() else set())
    todo = [(k, v, model, tpl, tag) for k, v in sorted(by.items())
            if k not in done and (only is None or k in only)][:limit]
    print(f'{len(by)} repos, {len(todo)} to run, model={model}, prompt={tag}', flush=True)
    t0, spend = time.time(), 0.0
    with out.open('a') as fh, ThreadPoolExecutor(max_workers=w) as pool:
        for rec in pool.map(one, todo):
            fh.write(json.dumps(rec, ensure_ascii=False) + '\n'); fh.flush()
            spend += rec.get('cost_usd') or 0
            print(f"  {rec['repo'][:38]:38} {'ok' if rec['ok'] else 'FAIL'}"
                  f"  {rec['n_read']}/{rec['n_total']}"
                  f"  {int(time.time()-t0)}s  ${spend:.2f}", flush=True)


main()
