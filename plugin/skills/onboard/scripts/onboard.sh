#!/bin/sh
#: Apply, report, or remove the machine setup the harness needs.
#
# Two steps, `rules` and `hud`, each idempotent and each reporting `applied`, `already`,
# `skipped` or `removed` with a reason. Not one transaction: a machine without Orca still
# gets its rules, and a user isolating a problem removes one step and keeps the other.
#
# Everything it writes lives in three places, none of them an edit that cannot be undone:
# a symlink under ~/.claude/rules, a state directory under ~/.claude/kein/onboard, and a
# block prepended to Orca's own statusline script, which Orca itself rewrites at every
# launch. ~/.claude/settings.json is never touched.
set -eu

usage() {
  cat <<'EOF'
usage: onboard.sh <status|apply|remove> [--step rules|hud] [--yes]

  status          what is in place, what is not, and what came undone on its own
  apply           put the missing pieces in place
  remove          take them out, with the plugin left enabled

  --step <name>   act on one step only. Default: every step
  --yes           consent to a removal that takes away more than onboarding added
EOF
}

command=${1:-status}
case "$command" in
  status | apply | remove) shift ;;
  -h | --help | help) usage; exit 0 ;;
  *) printf 'onboard: unknown command %s\n\n' "$command" >&2; usage >&2; exit 1 ;;
esac

step=all
consent=no
while [ $# -gt 0 ]; do
  case "$1" in
    --step) step=${2:-}; shift 2 || { printf 'onboard: --step wants a name\n' >&2; exit 1; } ;;
    --yes) consent=yes; shift ;;
    *) printf 'onboard: unknown option %s\n' "$1" >&2; exit 1 ;;
  esac
done
case "$step" in all | rules | hud) ;; *) printf "onboard: no step '%s'\n" "$step" >&2; exit 1 ;; esac

# CLAUDE_PLUGIN_ROOT is set when a session runs this. The fallback is for running it by hand
# from a clone, which is how it gets exercised without a session.
KEIN_ROOT=${CLAUDE_PLUGIN_ROOT:-$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)}
CONFIG_HOME=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
STATE="$CONFIG_HOME/kein/onboard"
RULES_LINK="$CONFIG_HOME/rules/kein"
# KEIN_ORCA_STATUSLINE points at another file, which is how this gets exercised without
# writing to the statusline the running session is using.
ORCA_STATUSLINE=${KEIN_ORCA_STATUSLINE:-$HOME/.orca/agent-hooks/claude-statusline.sh}
MARKER='# >>> kein hud wrapper'

say() { printf '  %-8s %-7s %s\n' "$1" "$2" "$3"; }

wants() { [ "$step" = all ] || [ "$step" = "$1" ]; }

# --- rules ---------------------------------------------------------------------------
# A symlink at the home level rather than inside the plugin, because these rules are meant
# to fire in every project and a plugin-scoped copy would only fire where kein is enabled.

rules_state() {
  if [ -L "$RULES_LINK" ]; then
    if [ "$(readlink "$RULES_LINK")" = "$KEIN_ROOT/rules" ]; then echo linked; else echo elsewhere; fi
  elif [ -e "$RULES_LINK" ]; then
    echo occupied
  else
    echo absent
  fi
}

rules_status() {
  case "$(rules_state)" in
    linked)    say rules already "$RULES_LINK -> $KEIN_ROOT/rules" ;;
    elsewhere) say rules other   "$RULES_LINK points at $(readlink "$RULES_LINK")" ;;
    occupied)  say rules blocked "$RULES_LINK exists and is not a symlink" ;;
    absent)    say rules absent  "no link at $RULES_LINK" ;;
  esac
}

rules_apply() {
  case "$(rules_state)" in
    linked)    say rules already "$RULES_LINK" ; return 0 ;;
    occupied)  say rules blocked "$RULES_LINK exists and is not a symlink; move it first"; return 1 ;;
    elsewhere) say rules blocked "$RULES_LINK points elsewhere; remove it first"; return 1 ;;
  esac
  mkdir -p "$CONFIG_HOME/rules"
  ln -s "$KEIN_ROOT/rules" "$RULES_LINK"
  say rules applied "$RULES_LINK -> $KEIN_ROOT/rules"
}

rules_remove() {
  if [ "$(rules_state)" != linked ]; then say rules already "nothing of ours at $RULES_LINK"; return 0; fi
  if [ "$consent" != yes ]; then
    say rules held "removing this leaves no rules at all, not the ones you had before"
    printf '\n  The harness carries the rules it links here, so this is not the inverse of\n'
    printf '  applying it: before onboarding they came from wherever you kept them, and that\n'
    printf '  copy is not restored by taking the link away. Re-run with --yes, or point\n'
    printf '  %s somewhere of your own instead.\n\n' "$RULES_LINK"
    return 1
  fi
  rm "$RULES_LINK"
  say rules removed "$RULES_LINK"
}

# --- hud -----------------------------------------------------------------------------
# The marker file is the hook's off-switch. With it absent the repair hook returns before
# doing anything, which is what lets the wrapper stay off while the plugin stays enabled.

hud_wrapped() { [ -f "$ORCA_STATUSLINE" ] && grep -q "$MARKER" "$ORCA_STATUSLINE"; }

hud_status() {
  if [ ! -f "$ORCA_STATUSLINE" ]; then say hud skipped "no Orca statusline at $ORCA_STATUSLINE"; return 0; fi
  if [ -f "$STATE/hud-enabled" ]; then
    if hud_wrapped; then say hud already "rendering, and the hook will keep it that way"
    else say hud pending "enabled; the wrapper goes back on the next prompt"; fi
  else
    if hud_wrapped; then say hud stale "wrapper present but disabled; Orca strips it at its next launch"
    else say hud absent "not enabled"; fi
  fi
}

hud_apply() {
  if [ ! -f "$ORCA_STATUSLINE" ]; then say hud skipped "no Orca statusline at $ORCA_STATUSLINE"; return 0; fi
  # Another wrapper in the same file renders its own line and ours, which reads as the HUD
  # having duplicated rather than as two programs both being installed.
  if grep -q '>>> claude-hud wrapper' "$ORCA_STATUSLINE" 2>/dev/null; then
    say hud blocked "$ORCA_STATUSLINE already carries a claude-hud wrapper; remove that first"
    return 1
  fi
  if [ -f "$STATE/hud-enabled" ] && hud_wrapped; then say hud already "rendering"; return 0; fi
  mkdir -p "$STATE"
  : > "$STATE/hud-enabled"
  # The same code path the hook runs, so applying and self-healing cannot drift apart.
  sh "$KEIN_ROOT/hud/repair.sh" || :
  if hud_wrapped; then
    say hud applied "wrapper on; backup at $STATE/orca-statusline.original"
  else
    say hud pending "enabled; the wrapper goes on at the next prompt"
  fi
}

hud_remove() {
  removed=no
  if [ -f "$STATE/hud-enabled" ]; then rm -f "$STATE/hud-enabled"; removed=yes; fi
  # Order matters: the marker goes first. Restoring the script while the hook is still armed
  # is undone by the next prompt.
  if hud_wrapped; then
    if [ -f "$STATE/orca-statusline.original" ]; then
      cat "$STATE/orca-statusline.original" > "$ORCA_STATUSLINE"
      chmod +x "$ORCA_STATUSLINE" 2>/dev/null || :
      say hud removed "wrapper off, Orca's own statusline restored"
    else
      say hud partial "hook disarmed, but no backup to restore; Orca reverts its own script at its next launch"
    fi
    return 0
  fi
  if [ "$removed" = yes ]; then say hud removed "hook disarmed; the wrapper was not on"
  else say hud already "nothing of ours in place"; fi
}

# --- run -----------------------------------------------------------------------------

printf 'kein onboard: %s\n' "$command"
printf '  plugin   %s\n\n' "$KEIN_ROOT"

failed=0
case "$command" in
  status)
    wants rules && rules_status
    wants hud   && hud_status
    ;;
  apply)
    wants rules && { rules_apply || failed=1; }
    wants hud   && { hud_apply   || failed=1; }
    ;;
  remove)
    # Reverse order, so the piece with a live mechanism behind it comes off first.
    wants hud   && { hud_remove   || failed=1; }
    wants rules && { rules_remove || failed=1; }
    ;;
esac

printf '\n'
exit "$failed"
