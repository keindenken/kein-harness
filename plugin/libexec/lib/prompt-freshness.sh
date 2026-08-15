# Sourceable. No shebang and no `set` — the caller owns both.
#
# `prompts/` is what `ocs ask` and `ocs team` hand a vendor CLI, so a hand-edit there would
# answer as a role that no longer exists as written. This is the half of the freshness
# question a dispatch can settle by itself: does the rendered copy still match the hashes
# recorded when it was rendered.
#
# It deliberately does NOT compare against the canonical source. That comparison needs
# `~/.codex-orca` present, and a dispatch that depends on it contradicts the reason
# `prompts/` is committed at all — the harness is meant to work without the Codex home.
# It used to: `ocs ask` called the full `check-prompts`, which reported every role as
# `missing(canonical)` and exited 1 on any machine without that directory.
#
# Whether canonical itself has moved, and whether `agents/` still matches `prompts/`, are
# maintenance questions that `kein-dev check-prompts` owns. Neither can change the answer a
# dispatch is about to produce, and the second costs a renderer fork over fourteen files.

# Prefixed locals: this is sourced into someone else's shell, and POSIX sh has no `local`.
prompt_library_fresh() {
  _plf_prompts=${1:-$KEIN_ROOT/prompts}
  _plf_record="$_plf_prompts/canonical.sha256"

  if [ ! -f "$_plf_record" ]; then
    printf 'prompt library: no rendered copy at %s. Run `kein-dev sync-prompts`.\n' \
      "$_plf_prompts" >&2
    return 1
  fi

  _plf_bad=''
  # A redirect rather than a pipe, so the accumulator survives the loop.
  while read -r _plf_expected _plf_name; do
    [ -n "$_plf_name" ] || continue
    _plf_file="$_plf_prompts/$_plf_name"
    if [ ! -f "$_plf_file" ]; then
      _plf_bad="$_plf_bad $_plf_name(missing)"
      continue
    fi
    [ "$(shasum -a 256 "$_plf_file" | cut -d' ' -f1)" = "$_plf_expected" ] \
      || _plf_bad="$_plf_bad $_plf_name"
  done < "$_plf_record"

  if [ -n "$_plf_bad" ]; then
    printf 'prompt library has been edited since it was rendered:%s\n' "$_plf_bad" >&2
    printf '  prompts/ is generated — change the canonical prompt and run `kein-dev sync-prompts`\n' >&2
    return 1
  fi
  return 0
}
