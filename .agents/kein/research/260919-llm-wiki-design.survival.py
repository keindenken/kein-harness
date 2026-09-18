# Reproduce: gh search code '"] ingest |" filename:log.md' --limit 100 --json repository,path > hits.json; python3 survival.py
import subprocess,json,re,base64
from datetime import date
def gh(*a):
    r=subprocess.run(['gh','api',*a],capture_output=True,text=True); return r.stdout
hits=json.load(open('hits.json')); seen={}
for h in hits: seen.setdefault(h['repository']['nameWithOwner'],h['path'])
out=[]
for repo,p in seen.items():
    try: c=base64.b64decode(gh(f'repos/{repo}/contents/{p}','--jq','.content')).decode('utf8','replace')
    except Exception: c=''
    days=sorted(set(re.findall(r'^## \[(\d{4}-\d{2}-\d{2})\]',c,re.M)))
    meta=json.loads(gh(f'repos/{repo}','--jq','{l:.language,d:.description,s:.stargazers_count}') or '{}')
    d=p.rsplit('/',1)[0] if '/' in p else ''
    cm=json.loads(gh(f'repos/{repo}/commits?path={d or p}&per_page=100','--jq','[.[].commit.committer.date[:10]]') or '[]')
    out.append(dict(repo=repo,path=p,log_days=len(days),first=days[0] if days else None,last=days[-1] if days else None,
        nested='/' in p and not re.match(r'^(wiki|knowledge|vault)/',p,re.I),lang=meta.get('l'),
        commit_days=len(set(cm)),commit_first=min(cm) if cm else None,commit_last=max(cm) if cm else None))
json.dump(out,open('survival.json','w'),indent=1)
