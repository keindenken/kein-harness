import json, re, sys
from pathlib import Path
LEAD = re.compile(r'^[ \t]*(?:#{1,6}|//|>|\*|-|\d+\.)?[ \t]*', re.M)
EMPH = re.compile(r'[*_`]+')
# `[text](url)` keeps only the text: a model reading rendered Markdown quotes what
# it saw, and the source it is checked against still carries the URL.
LINK = re.compile(r'\[([^\]]*)\]\([^)]*\)')
# Typographic punctuation, mapped to the ASCII a source file is more likely to
# hold. A Chinese legal skill and its quote differed only in curly versus
# straight double quotes, and the pair scored 0.98 similar and 0 matches.
PUNCT = str.maketrans({
    '\u2018': "'", '\u2019': "'", '\u201a': "'", '\u201b': "'",
    '\u201c': '"', '\u201d': '"', '\u201e': '"', '\u201f': '"',
    '\u2032': "'", '\u2033': '"', '\u00b4': "'",   # not U+0060: EMPH strips backticks
    '\u2013': '-', '\u2014': '-', '\u2015': '-', '\u2212': '-',
    '\u2026': '...', '\u00a0': ' ', '\u200b': '', '\ufeff': '',
})
# Fullwidth forms, folded to the ASCII a model tends to answer in: a Chinese
# skill writes `，` and the reply comes back with `,`.
FULLWIDTH = {c: chr(c - 0xFEE0) for c in range(0xFF01, 0xFF5F)}
FULLWIDTH[0x3000] = ' '
# Whitespace between two CJK characters carries no meaning and models drop it.
# `v2 复盘` and `v2复盘` are the same sentence, and scored 0.99 similar with zero
# matches until this existed. The class is deliberately narrow — collapsing space
# everywhere would let an English paraphrase match by accident.
CJK = r'\u3000-\u303f\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef'
CJK_SP = re.compile(rf'(?<=[{CJK}])\s+|\s+(?=[{CJK}])')


def norm(s):
    """Strip per-line comment/list markers, inline emphasis and link syntax, fold
    typographic and fullwidth punctuation to ASCII, drop whitespace beside CJK,
    then collapse the rest. A quote lifted out of a wrapped `# ` comment, a
    `- **bold:**` bullet or a Markdown link still matches; an invented sentence
    still does not."""
    s = LINK.sub(r'\1', (s or '').translate(PUNCT).translate(FULLWIDTH))
    s = re.sub(r'\s+', ' ', EMPH.sub('', LEAD.sub(' ', s))).strip()
    return CJK_SP.sub('', s)
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
