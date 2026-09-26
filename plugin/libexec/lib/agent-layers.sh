# Sourceable. No shebang and no `set` — the caller owns both.
#
# The user's and the project's prompt layers for a role, the same files `hooks/prompt-layers.py` appends on the Claude side: `~/.agents/kein/prompts/<role>.md`, then `<project>/.agents/kein/prompts/<role>.md`, the project resolved in `ocs state-dir`'s order without its config-home fallback.
# The plugin's own `prompts/<role>.md` is not among them. It carries what the Claude runtime and the plugin's hooks make true, which a vendor lane does not run under; the layers live under `.agents/` because they are meant to be vendor-neutral.
# Prints nothing when neither exists. An unreadable layer is reported on stderr and skipped.

# Prefixed locals: this is sourced into someone else's shell, and POSIX sh has no `local`.
agent_layers() {
  _al_role=$1
  _al_rel=".agents/kein/prompts/$_al_role.md"
  if [ -n "${KEIN_STATE_ROOT:-}" ]; then _al_root=$KEIN_STATE_ROOT
  elif [ -n "${CLAUDE_PROJECT_DIR:-}" ]; then _al_root=$CLAUDE_PROJECT_DIR
  else _al_root=$(git rev-parse --show-toplevel 2>/dev/null) || _al_root=''
  fi
  _al_seen=''
  for _al_path in "$HOME/$_al_rel" ${_al_root:+"$_al_root/$_al_rel"}; do
    if [ ! -e "$_al_path" ]; then
      # A directory on the way that cannot be entered hides the file rather than proving it absent; the Claude-side hook reports that case too.
      _al_dir=$(dirname "$_al_path")
      while [ ! -e "$_al_dir" ] && [ "$_al_dir" != / ]; do _al_dir=$(dirname "$_al_dir"); done
      [ -d "$_al_dir" ] && [ ! -x "$_al_dir" ] && printf 'ocs: %s layer %s is unreadable; skipped.\n' "$_al_role" "$_al_path" >&2
      continue
    fi
    # A project rooted at the home directory would otherwise hand the user layer in twice.
    _al_key=$(cd "$(dirname "$_al_path")" 2>/dev/null && pwd -P)/$(basename "$_al_path")
    [ "$_al_key" != "$_al_seen" ] || continue
    _al_seen=$_al_key
    if [ -r "$_al_path" ] && [ -f "$_al_path" ]; then
      printf '<!-- kein %s layer: %s -->\n' "$_al_role" "$_al_path"
      cat "$_al_path"
      printf '\n'
    else
      printf 'ocs: %s layer %s is unreadable; skipped.\n' "$_al_role" "$_al_path" >&2
    fi
  done
}
