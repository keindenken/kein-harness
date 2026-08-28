# The vendor home a lane runs under is the operator's own unless `KEIN_CODEX_HOME` says otherwise,
# and a home carries more than credentials: the skills its installed plugins publish reach the
# worker's prompt.
#
# THIS DOES NOT CURRENTLY WORK, and it is kept anyway. Measured 2026-08-29 with
# `codex debug prompt-input`, which renders the model-visible prompt: passing
# `-c 'plugins."visualize@openai-bundled".enabled=false'` for a plugin that IS loaded leaves that
# prompt byte-identical, 12015 bytes either way, with `visualize` still in its skill list. The
# override is accepted and has no effect on this version of codex.
#
# Kept because it costs a dozen flags on a launch line and would start working if a later version
# honours the key. What actually isolates a lane is a home of the run's own, which needs a decision
# about how that home gets credentials -- see `docs/open-threads.md`. `KEIN_CODEX_PLUGINS=inherit`
# stops passing the flags.
#
# The incident that motivated this is also not what it looked like. The `superpowers` skills that
# Executor cited were never in its prompt: `config.toml` registers them under 6.2.0 and the disk
# holds 6.3.0, so nothing loaded, and that home's memories do not mention them either. The worker
# read them off disk or asserted them without a source; either way no loaded plugin was speaking.
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
