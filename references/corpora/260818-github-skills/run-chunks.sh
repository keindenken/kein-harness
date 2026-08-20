#!/usr/bin/env bash
# Run the reading pass in chunks, stopping if the weekly quota climbs unexpectedly.
# 496 calls moved it 2 points, so a chunk that costs much more than that is a
# reason to look before spending the next one.
set -u
W=/Users/kein/Documents/workspace/dev/worktree/kein-harness/corpus/references/corpora/260818-github-skills
CHUNK=${1:-500}
CEILING=${2:-40}

pct() { python3 -c "
import glob,os,re
fs=sorted(glob.glob(os.path.expanduser('~/.codex/sessions/2026/*/*/*.jsonl')),key=os.path.getmtime)
for f in reversed(fs[-8:]):
    m=re.findall(r'\"used_percent\":([0-9.]+)',open(f,errors='replace').read())
    if m: print(m[-1]); break
else: print('0')"; }

cd "$W"
while :; do
  n=$(wc -l < runs/pass2.jsonl)
  total=$(python3 -c "import json;print(len(json.load(open('run-manifest.json'))))")
  [ "$n" -ge "$total" ] && { echo "ALLDONE $n/$total"; break; }
  q=$(pct)
  echo "--- chunk from $n/$total, quota ${q}% ---"
  if python3 -c "import sys;sys.exit(0 if float('$q')>=$CEILING else 1)"; then
    echo "STOPPED: quota ${q}% reached the ${CEILING}% ceiling"; break
  fi
  python3 extract.py run-manifest.json runs/pass2.jsonl \
    --prompt prompt/extract-nonum.md --model gpt-5.6-luna \
    --workers 6 --limit $((n+CHUNK)) 2>&1 | tail -1
  after=$(wc -l < runs/pass2.jsonl)
  [ "$after" -le "$n" ] && { echo "STOPPED: no progress"; break; }
done
echo "final: $(wc -l < runs/pass2.jsonl) records, quota $(pct)%"
