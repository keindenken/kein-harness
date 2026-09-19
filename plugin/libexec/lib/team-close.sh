# `ocs team close <run-dir> [--discard]`, sourced by ocs-team.
#
# Removes a worktree that `ocs team --worktree new` created, and nothing else.
# `orca worktree rm` refuses a tree with uncommitted tracked changes but deletes the branch with it even when that branch holds commits merged nowhere, measured 2026-09-19 on orca 1.4.205: an unmerged commit was gone after a plain `rm` with no `--force`.
# So the check that makes removal safe is the merge, and it is made here because nothing downstream makes it.

run_dir=''
discard=0
while [ $# -gt 0 ]; do
  case "$1" in
    --discard) discard=1; shift ;;
    -h|--help) printf 'usage: ocs team close <run-dir> [--discard]\n' >&2; exit 0 ;;
    -*) printf "ocs team close: unknown option '%s'\n" "$1" >&2; exit 1 ;;
    *) [ -z "$run_dir" ] || { printf 'ocs team close: one run directory at a time\n' >&2; exit 1; }; run_dir=$1; shift ;;
  esac
done
[ -n "$run_dir" ] || { printf 'usage: ocs team close <run-dir> [--discard]\n' >&2; exit 1; }
[ -d "$run_dir" ] || { printf 'ocs team close: no run directory at %s\n' "$run_dir" >&2; exit 1; }
run_dir=$(cd "$run_dir" && pwd)
record="$run_dir/command.txt"
[ -r "$record" ] || { printf 'ocs team close: %s has no command.txt, so it is not an ocs team run\n' "$run_dir" >&2; exit 1; }

field() { sed -n "s/^$1=//p" "$record" | tail -1; }
lane_tree=$(field created_worktree)
lane_branch=$(field branch)
base=$(field base)
dispatch=$(field dispatch)
terminal=$(field terminal)

if [ -z "$lane_tree" ]; then
  printf 'ocs team close: this lane ran in an existing worktree (%s), which ocs team did not create and does not remove.\n' "$(field cwd)" >&2
  exit 1
fi
if [ ! -d "$lane_tree" ]; then
  printf 'ocs team close: %s is already gone.\n' "$lane_tree"
  exit 0
fi

# A worker still under way owns the tree; closing under it is the same accident as dispatching a second one onto it.
if [ -n "$dispatch" ]; then
  state=$(orca orchestration worker-show --dispatch "$dispatch" --json 2>/dev/null | python3 -c 'import json,sys
try: print(((json.load(sys.stdin).get("result") or {}).get("dispatch") or {}).get("status") or "")
except Exception: print("")' 2>/dev/null)
  case "$state" in
    ''|completed|failed) ;;
    *) printf 'ocs team close: dispatch %s is still %s in %s.\n' "$dispatch" "$state" "$lane_tree" >&2
       printf '  stop it first: orca orchestration worker-stop --dispatch %s\n' "$dispatch" >&2
       exit 1 ;;
  esac
fi

# The report and the run record live inside the lane tree, because that is the only place the worker's sandbox can write. They are kept by moving them to the caller's state directory before the tree goes.
keep_root=$("$KEIN_ROOT/libexec/ocs-state-dir")
case "$keep_root/" in
  "$lane_tree"/*) printf 'ocs team close: run this from outside %s; the lane record would be kept inside the tree being removed.\n' "$lane_tree" >&2; exit 1 ;;
esac
lane_state=$(KEIN_STATE_ROOT=$lane_tree "$KEIN_ROOT/libexec/ocs-state-dir")
run_name=${run_dir##*/}
report="$lane_state/reports/$run_name.md"

if [ "$discard" -eq 0 ]; then
  # Uncommitted work outside the lane's own record is work not yet landed.
  rel_runs=${lane_state#"$lane_tree"/}/runs/team/
  rel_reports=${lane_state#"$lane_tree"/}/reports/
  dirty=$(git -C "$lane_tree" status --porcelain --untracked-files=all | awk -v a="$rel_runs" -v b="$rel_reports" '{ p=substr($0,4); if (index(p,a)!=1 && index(p,b)!=1) print }')
  if [ -n "$dirty" ]; then
    printf 'ocs team close: %s has uncommitted changes:\n' "$lane_tree" >&2
    printf '%s\n' "$dirty" | sed 's/^/  /' | head -20 >&2
    printf '  commit them on %s and merge it, or pass --discard to lose them.\n' "${lane_branch:-the lane branch}" >&2
    exit 1
  fi
  [ -n "$base" ] || { printf 'ocs team close: the lane recorded no base branch (it was created from a detached HEAD), so nothing says where its branch should have landed.\n  pass --discard once you have checked by hand.\n' >&2; exit 1; }
  tip=$(git -C "$lane_tree" rev-parse HEAD)
  if ! git -C "$lane_tree" merge-base --is-ancestor "$tip" "refs/heads/$base" 2>/dev/null; then
    printf 'ocs team close: %s has commits not in %s:\n' "${lane_branch:-HEAD}" "$base" >&2
    git -C "$lane_tree" log --oneline "refs/heads/$base..$tip" 2>/dev/null | head -10 | sed 's/^/  /' >&2
    printf '  removing the worktree deletes the branch with them. Merge it into %s first, or pass --discard.\n' "$base" >&2
    exit 1
  fi
fi

mkdir -p "$keep_root/runs/team" "$keep_root/reports"
[ ! -e "$report" ] || cp "$report" "$keep_root/reports/$run_name.md"
cp -R "$run_dir" "$keep_root/runs/team/"

[ -z "$terminal" ] || orca terminal close --terminal "$terminal" --json >/dev/null 2>&1 || true

# Read before the tree goes, since the tree is how git is reached.
common_dir=$(git -C "$lane_tree" rev-parse --path-format=absolute --git-common-dir)

# `--force` because the lane's own record is untracked in the tree; the checks above are what stand in for the refusal it waives.
removed=$(orca worktree rm --worktree "path:$lane_tree" --force --json 2>/dev/null || true)
if ! printf '%s' "$removed" | python3 -c 'import json,sys; sys.exit(0 if json.load(sys.stdin).get("ok") else 1)' 2>/dev/null; then
  printf 'ocs team close: orca did not remove %s: %s\n' "$lane_tree" "$(printf '%s' "$removed" | python3 -c 'import json,sys
try: e=json.load(sys.stdin).get("error") or {}; print(e.get("code","?"), e.get("message",""))
except Exception: print("no response")' 2>/dev/null)" >&2
  exit 1
fi

# Whether Orca deletes the branch with the tree varies: it did for an unmerged commit without `--force` and did not for one with it (measured 2026-09-19). So the branch is settled here rather than left to it.
if [ -n "$lane_branch" ] && git --git-dir="$common_dir" show-ref --verify --quiet "refs/heads/$lane_branch"; then
  if [ "$discard" -eq 1 ]; then
    git --git-dir="$common_dir" branch -D "$lane_branch" >/dev/null
  else
    git --git-dir="$common_dir" branch -d "$lane_branch" >/dev/null 2>&1 || printf 'ocs team close: kept branch %s; git would not delete it as merged.\n' "$lane_branch" >&2
  fi
fi

if [ "$discard" -eq 1 ]; then
  printf 'closed %s and discarded %s.\n' "$lane_tree" "${lane_branch:-its branch}"
else
  printf 'closed %s; %s was merged into %s and is deleted.\n' "$lane_tree" "${lane_branch:-its branch}" "$base"
fi
[ ! -e "$keep_root/reports/$run_name.md" ] || printf 'report: %s\n' "$keep_root/reports/$run_name.md"
printf 'record: %s\n' "$keep_root/runs/team/$run_name"
