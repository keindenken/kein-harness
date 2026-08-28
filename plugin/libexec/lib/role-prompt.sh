# Sourceable. No shebang and no `set` — the caller owns both.
#
# `agents/<role>.md` is the one copy of a role that ships. Claude Code reads it whole; a vendor CLI
# gets it with the frontmatter taken off, because that block is Claude's translation of the role
# (`model`, `disallowedTools`) and not the role. The vendor-neutral facts it was translated from are
# in `agents.json`, which is what `ocs` reads to pick a model and to refuse a write-capable role.
#
# There is no second rendered copy to keep in step, which is the point: the bodies were byte-identical
# for as long as both existed.

# Prefixed locals: this is sourced into someone else's shell, and POSIX sh has no `local`.
role_prompt_body() {
  _rpb_file=$1
  [ -f "$_rpb_file" ] || return 1
  # A file with no frontmatter prints whole, so this is safe against a hand-written role.
  awk '
    NR == 1 && $0 == "---" { infm = 1; next }
    infm && $0 == "---"    { infm = 0; skipblank = 1; next }
    infm                   { next }
    skipblank && $0 == ""  { next }
                           { skipblank = 0; print }
  ' "$_rpb_file"
}
