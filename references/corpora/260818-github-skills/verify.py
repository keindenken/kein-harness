import json, re, sys
from pathlib import Path
LEAD = re.compile(r'^[ \t]*(?:#{1,6}|//|>|\*|-|\d+\.)?[ \t]*', re.M)
EMPH = re.compile(r'[*_`]+')
def norm(s):
    """Strip per-line comment/list markers and inline emphasis, then collapse
    whitespace. A quote lifted out of a wrapped `# ` comment or a `- **bold:**`
    bullet still matches; an invented sentence still does not."""
    return re.sub(r'\s+', ' ', EMPH.sub('', LEAD.sub(' ', s or ''))).strip()
def check(quote, source):
    if not quote: return 'none'
    return 'verbatim' if norm(quote) in norm(source) else 'not-found'
if __name__ == '__main__':
    outdir, listfile, corpus = map(Path, sys.argv[1:4])
    files = [l for l in listfile.read_text().split('\n') if l]
    tally = {}
    for i, f in enumerate(files, 1):
        p = outdir / f'{i:02d}.txt'
        m = re.search(r'\{.*\}', p.read_text(), re.S) if p.exists() else None
        if not m: tally['unparsed']=tally.get('unparsed',0)+1; print(f'{i:2} UNPARSED'); continue
        try: rec = json.loads(m.group(0))
        except Exception: tally['badjson']=tally.get('badjson',0)+1; print(f'{i:2} BADJSON'); continue
        v = check(rec.get('quote'), (corpus/f).read_text(errors='replace'))
        tally[v]=tally.get(v,0)+1
        tag=f.split('__')[0][:24]
        print(f'{i:2} {v.upper():10} {str(rec.get("calls")):34} {tag}')
        if rec.get('quote'): print(f'       "{re.sub(chr(10)," ",rec["quote"])[:150]}"')
    print('  ->', tally)
