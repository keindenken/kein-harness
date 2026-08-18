#!/usr/bin/env python3
"""Run one quote-extraction prompt variant over the fixture and score it.

The fixture is two labelled halves. Positives are files an earlier reading
named as carrying a claim someone had to do the work to write; negatives are
control-band files that scored zero on every specificity marker. A variant that
only maximises positives is indistinguishable from one that says yes to
everything, which is the failure the last round shipped.

Usage: ./run_variant.py <variant.md> [--effort E] [--workers N] [--window BYTES]
"""
import json, re, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / 'fixture'
RUNS = HERE / 'runs'
# The 260811 corpus is the fixture's source; the next harvest replaces this.
CORPUS = Path(os.environ.get('CORPUS', HERE.parent / '260811-github-skills' / 'corpus'))
sys.path.insert(0, str(HERE))
from verify import norm

def call(prompt, effort):
    p = subprocess.run(
        ['codex', 'exec', '--skip-git-repo-check', '--sandbox', 'read-only',
         '-m', 'gpt-5.6-luna', '-c', f'model_reasoning_effort={effort}',
         '-C', str(HERE), '-'],
        input=prompt, capture_output=True, text=True, timeout=600)
    return p.stdout

def parse(raw):
    m = re.findall(r'\{.*?\}(?=\s*$|\s*\n)', raw, re.S)
    for cand in reversed(re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', raw, re.S)):
        try: return json.loads(cand)
        except Exception: continue
    return None

def quotes_of(rec):
    if not rec: return []
    q = rec.get('quotes', rec.get('quote'))
    if q is None: return []
    return [x for x in (q if isinstance(q, list) else [q]) if x]

def one(job):
    label, file, tpl, effort, window = job
    text = (CORPUS / file).read_text(errors='replace')
    chunks = [text] if not window else [text[i:i+window] for i in range(0, len(text), window)]
    hits, invented, raws = [], [], []
    for ch in chunks:
        raw = call(tpl.replace('{{FILE}}', file).replace('{{BODY}}', ch), effort)
        raws.append(raw)
        rec = parse(raw)
        if rec is None:
            invented.append('__UNPARSED__'); continue
        src = norm(text)
        for q in quotes_of(rec):
            (hits if norm(q) in src else invented).append(q)
    return {'label': label, 'file': file, 'hits': hits, 'invented': invented,
            'n_chunks': len(chunks), 'raw': raws[-1][-400:]}

def main():
    tplpath = Path(sys.argv[1])
    effort = 'medium'; workers = 4; window = 0
    for i, a in enumerate(sys.argv):
        if a == '--effort': effort = sys.argv[i+1]
        if a == '--workers': workers = int(sys.argv[i+1])
        if a == '--window': window = int(sys.argv[i+1])
    tpl = tplpath.read_text()
    jobs = []
    halves = [('pos', 'positive.txt'), ('neg', 'negative.txt')]
    for i, a in enumerate(sys.argv):
        if a == '--fixture': halves = [(x.split('=')[0], x.split('=')[1]) for x in sys.argv[i+1].split(',')]
    for label, lst in halves:
        for f in (FIXTURE / lst).read_text().split():
            jobs.append((label, f, tpl, effort, window))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        res = list(pool.map(one, jobs))
    tagsfx = ''.join('-'+h[0] for h in halves if h[0] not in ('pos','neg'))
    RUNS.mkdir(exist_ok=True)
    out = RUNS / f'{tplpath.stem}-{effort}{tagsfx}{"-w"+str(window) if window else ""}.json'
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False))

    for label in [h[0] for h in halves]:
        rs = [r for r in res if r['label'] == label]
        withq = sum(1 for r in rs if r['hits'])
        inv = sum(len(r['invented']) for r in rs)
        print(f"  {label}: {withq}/{len(rs)} files yielded a verified quote"
              f"   ({sum(len(r['hits']) for r in rs)} quotes, {inv} unverified)")
    print(f"  -> {out.name}")

main()
