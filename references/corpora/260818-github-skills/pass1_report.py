#!/usr/bin/env python3
"""Score a pass-1 run against the pass-2 records it read.

Three things are checkable without a second opinion, and they are the three that
matter. Schema discipline: `field` is meant to be set only for `one-field` and
`form` only for `unified-by-form`, so a leak is a model answering a question it
was told not to answer. Provenance: `best_claim` is supposed to be copied from a
quote that was itself located in the source, which makes the chain source -> quote
-> claim checkable end to end rather than trusted at the last step. And the flags:
a `recheck` that restates a boolean already in the input costs a re-read and buys
nothing, so they are sorted by whether pass 1 was the only pass that could see it.

Usage: ./pass1_report.py <pass1.jsonl> [pass1-other.jsonl ...] [--pass2 F]
"""
import json, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify import norm  # noqa: E402


def load2(path):
    by_repo, by_file = {}, {}
    for line in Path(path).read_text().splitlines():
        r = json.loads(line)
        if not r.get('ok'):
            continue
        by_repo.setdefault(r['repo'], []).append(r)
        by_file[(r['repo'], r['dir'])] = r
    return by_repo, by_file


def classify(flag, rec):
    """Which pass could have raised this flag.

    `no-signal` is the one that needs saying: `labels.py` reports a pattern it
    found and never reports absence, so a `no-signal` record whose summary
    describes calling a service is that field working as designed. Twenty of the
    first run's fifty flags were exactly that.
    """
    why = (flag.get('why') or '').lower()
    reach = (rec or {}).get('reach') or []
    if 'reach' in why or 'no-signal' in why:
        return 'reach: no-signal (not a defect)' if reach == ['no-signal'] else 'reach: labelled external'
    if 'quote_verified' in why or 'verbatim check' in why:
        return 'restates quote_verified (a field it was handed)'
    if rec is not None and not rec.get('quote'):
        return 'null quote vs specific summary'
    if any(w in why for w in ('identical', 'same ', 'every other', 'rest of', 'nothing else')):
        return 'cross-file (only pass 1 can see)'
    return 'other'


def report(path, by_repo, by_file):
    rows = [json.loads(l) for l in Path(path).read_text().splitlines()]
    ok = [r for r in rows if r.get('ok')]
    print(f"\n=== {Path(path).name}  {len(ok)}/{len(rows)} ok  "
          f"${sum(r.get('cost_usd') or 0 for r in rows):.2f}  "
          f"prompt={ok[0].get('prompt')}  model={ok[0].get('model')}")
    print('  coherence:', dict(Counter(r.get('coherence') for r in ok)))
    leak = sum(1 for r in ok if (r.get('coherence') != 'one-field' and r.get('field'))
               or (r.get('coherence') != 'unified-by-form' and r.get('form')))
    print(f'  schema leaks: {leak}')

    exact = sub = none = broken = 0
    for r in ok:
        bc = norm(r.get('best_claim') or '')
        quotes = [(x, norm(x.get('quote') or '')) for x in by_repo.get(r['repo'], []) if x.get('quote')]
        if not bc:
            none += 1
            continue
        if any(bc == q for _, q in quotes):
            exact += 1
        elif any(bc in q for _, q in quotes):
            sub += 1
        else:
            none += 1
        src = next((x for x, q in quotes if bc in q), None)
        if src is not None and not src.get('quote_ok'):
            broken += 1
    print(f'  best_claim: {exact} verbatim, {sub} trimmed, {none} untraceable; '
          f'{broken} resting on an unverified quote')

    flags = [(r['repo'], f) for r in ok for f in (r.get('recheck') or [])]
    n_rec = sum(r['n_read'] for r in ok)
    kinds = Counter(classify(f, by_file.get((repo, f.get('file', '')))) for repo, f in flags)
    print(f'  recheck: {len(flags)} flags over {n_rec} records ({len(flags)/n_rec:.0%})')
    for k, v in kinds.most_common():
        print(f'      {v:3}  {k}')
    novel = kinds['cross-file (only pass 1 can see)'] + kinds['null quote vs specific summary']
    print(f'      -> {novel} that no cheaper pass produces')
    return {r['repo']: r for r in ok}


def main():
    p2 = 'runs/pass2.jsonl'
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    for i, a in enumerate(sys.argv):
        if a == '--pass2':
            p2 = sys.argv[i + 1]
    by_repo, by_file = load2(HERE / p2)
    runs = [report(a, by_repo, by_file) for a in args]
    if len(runs) == 2:
        shared = set(runs[0]) & set(runs[1])
        same = sum(1 for k in shared if runs[0][k].get('coherence') == runs[1][k].get('coherence'))
        print(f'\ncoherence agreement between the two runs: {same}/{len(shared)}')
        for k in sorted(shared):
            a, b = runs[0][k].get('coherence'), runs[1][k].get('coherence')
            if a != b:
                print(f'    {k[:40]:40} {a:16} vs {b}')


main()
