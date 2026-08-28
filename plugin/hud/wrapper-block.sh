# >>> kein hud wrapper >>>
# Prepended to Orca's ~/.orca/agent-hooks/claude-statusline.sh by `kein-onboard`.
#
# Orca owns the statusline command in ~/.claude/settings.json and relays the payload to its
# own UI. Claude Code gives that command to one program, so rendering anything else means
# going in front of Orca rather than beside it: this reads the payload once, renders the
# harness HUD from it, and then re-runs the original script with the payload on stdin and a
# guard set, so Orca still receives everything it did before.
#
# Orca reverts this file to its canonical copy at every launch, which strips this block.
# That is not a failure mode to defend against — it is the removal path, and the plugin's
# UserPromptSubmit hook is what puts the block back while the HUD is meant to be on.
#
# The marker line above is what `repair.sh` greps for. Do not reword it in one place only.
if [ -z "${KEIN_HUD_WRAPPED:-}" ]; then
  kein_hud_payload=$(cat)
  kein_hud_state="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/kein/onboard"
  # The plugin's location is not knowable from here: Orca's script runs outside the plugin,
  # so CLAUDE_PLUGIN_ROOT is unset, and a marketplace install moves on every upgrade. The
  # repair hook runs inside the plugin and rewrites this file on every prompt, so the path
  # is refreshed by the same mechanism that keeps the block in place.
  if [ -r "$kein_hud_state/plugin-root" ]; then
    kein_hud_root=$(cat "$kein_hud_state/plugin-root")
    if [ -r "$kein_hud_root/hud/statusline.py" ]; then
      # COLUMNS less the frame Orca draws around the line. Rendering into the full width
      # wraps, and a wrapped statusline costs a row on every prompt.
      kein_hud_cols=${COLUMNS:-}
      case "$kein_hud_cols" in ''|*[!0-9]*) kein_hud_cols=120 ;; esac
      [ "$kein_hud_cols" -gt 4 ] && kein_hud_cols=$((kein_hud_cols - 4)) || kein_hud_cols=1
      printf '%s' "$kein_hud_payload" \
        | COLUMNS="$kein_hud_cols" python3 "$kein_hud_root/hud/statusline.py" || :
    fi
  fi
  printf '%s' "$kein_hud_payload" | KEIN_HUD_WRAPPED=1 /bin/sh "$0"
  exit 0
fi
# <<< kein hud wrapper end <<<
