# The vendor home a lane runs under is the operator's own unless `KEIN_CODEX_HOME` says otherwise,
# and a home carries more than credentials: whatever plugins its `config.toml` registers arrive with
# it. The first measured cross-vendor Executor read a `superpowers` skill out of that home and cited
# its procedure back as authority for not waiting on approval -- a rule from a plugin nobody in this
# workflow chose, reaching a worker through a home pinned for its auth.
#
# So the plugins are turned off at the call rather than the home being replaced: the vendor's auth
# lives where its home does, and a separate home would have to be given credentials before it ran.
# `KEIN_CODEX_PLUGINS=inherit` leaves them on, which is what makes running without this rule a use
# rather than a violation.
codex_plugin_overrides() {
  [ "${KEIN_CODEX_PLUGINS:-off}" = "inherit" ] && return 0
  python3 - "$1/config.toml" <<'PY'
import re, sys
try:
    text = open(sys.argv[1], encoding="utf-8").read()
except OSError:
    raise SystemExit
for name in re.findall(r'^\[plugins\."([^"]+)"\]', text, re.MULTILINE):
    print(f'plugins."{name}".enabled=false')
PY
}
