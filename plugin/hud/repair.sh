#!/bin/sh
# Put the HUD wrapper back into Orca's statusline script, and keep the path it reads fresh.
#
# Runs from the plugin's UserPromptSubmit hook. Orca reconciles
# ~/.orca/agent-hooks/claude-statusline.sh against its canonical copy at every app launch and
# reverts anything that differs, so without this the HUD survives exactly until the next
# Orca restart.
#
# The off-switch is the marker file, not the plugin's enabled state. Disabling the plugin
# stops this too, but that costs the whole harness, and wanting the harness without the
# machine setup is the case `kein-onboard remove` exists for.
#
# Silent on every path. UserPromptSubmit stdout is injected into the model's context, so a
# progress line here is a line in someone's prompt.
set -eu

STATE="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/kein/onboard"
MARKER='# >>> kein hud wrapper'
ORCA_STATUSLINE=${KEIN_ORCA_STATUSLINE:-$HOME/.orca/agent-hooks/claude-statusline.sh}

[ -f "$STATE/hud-enabled" ] || exit 0

root=${CLAUDE_PLUGIN_ROOT:-}
if [ -z "$root" ]; then
  root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd) || exit 0
fi
# Written on every run rather than at install: a marketplace upgrade moves the plugin, and
# the wrapper has no other way to find it. This is the line that makes that self-healing.
mkdir -p "$STATE" 2>/dev/null || exit 0
printf '%s\n' "$root" > "$STATE/plugin-root" 2>/dev/null || exit 0

[ -f "$ORCA_STATUSLINE" ] || exit 0
[ -r "$root/hud/wrapper-block.sh" ] || exit 0
grep -q "$MARKER" "$ORCA_STATUSLINE" && exit 0
# Someone else's wrapper is in there. Adding ours would render two statuslines, and this
# path has no way to say so -- it is required to be silent -- so it declines instead.
grep -q '>>> claude-hud wrapper' "$ORCA_STATUSLINE" && exit 0

# Unwrapped, so whatever is there now is Orca's current canonical version. Refresh the
# backup before prepending, or a legitimate Orca update would leave `remove` restoring a
# version that predates it.
cp "$ORCA_STATUSLINE" "$STATE/orca-statusline.original" 2>/dev/null || exit 0

tmp=$(mktemp) || exit 0
{
  head -1 "$ORCA_STATUSLINE"
  cat "$root/hud/wrapper-block.sh"
  tail -n +2 "$ORCA_STATUSLINE"
} > "$tmp" 2>/dev/null || { rm -f "$tmp"; exit 0; }

# Refuse to install a statusline that lost Orca's relay. A broken statusline is a blank line
# on every prompt with nothing saying why, so the failure to defend against is writing at
# all rather than writing something imperfect.
if [ "$(wc -c < "$tmp")" -gt "$(wc -c < "$ORCA_STATUSLINE")" ] && grep -q 'statusline/claude' "$tmp"; then
  cat "$tmp" > "$ORCA_STATUSLINE"
  chmod +x "$ORCA_STATUSLINE" 2>/dev/null || :
fi
rm -f "$tmp"
exit 0
