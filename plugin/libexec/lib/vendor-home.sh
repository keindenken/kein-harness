# A lane runs under the operator's own Codex home unless `KEIN_CODEX_HOME` says otherwise, because that is where the credentials are. The home carries much more than credentials, and all of it reaches the worker unless the launch line turns it off. These are the arguments that do, each measured on codex-cli 0.156.1 (2026-09-26) against an empty `CODEX_HOME` as the vanilla baseline:
#
# - `--disable plugins` and `--disable apps` remove the plugin skills, the plugin and app instructions and the recommended-plugins list, and the MCP servers plugins bring (`context7`, `codex_apps`). The earlier `-c 'plugins."<name>".enabled=false'` per plugin was measured inert (2026-08-29) and is gone.
# - `-c mcp_servers.<name>.enabled=false` for every server `config.toml` declares. Without it a read-only `ocs ask` lane had the operator's `filesystem` server over all of `$HOME`, which runs outside the sandbox; a lane asked to list its MCP servers named `exa`, `filesystem`, `context7` and `codex_apps` before, and none after.
# - `--disable memories` with `memories.use_memories=false` and `memories.generate_memories=false`. A lane asked what memory it was given quoted the home's memory summary with `use_memories=true`, and answered NONE with these added after it. The memory folder holds summaries of other runs (`rollout_summaries/`) and a skill memories wrote, none of which a lane should see. The owner traced workers citing `superpowers` and answering in Korean to memories; the folder on 2026-09-26 mentions neither, so that attribution is unconfirmed.
# - `notify=[]`, so a lane's turns do not fire the operator's own notifier.
#
# Two things stay on purpose. `hooks.json` still runs, because Orca's agent hooks are how it tells a worker is idle or done. The home `AGENTS.md` still reaches the worker merged into the repository's, because no config key separates the two; it holds the operator's cross-project writing rules.
#
# `KEIN_CODEX_VANILLA=off` passes none of this.
#
# One argument per line, so a caller reads them with `while IFS= read -r` and a server name with spaces stays one argument. Names come from a TOML parse, because a header can carry a trailing comment or a quoted key; the regex fallback is for a Python older than 3.11. A name goes into the `-c` path raw: codex splits that path on dots and takes quotes literally, so `mcp_servers."my server"` names a new server while `mcp_servers.my server` names the right one. A name with a dot in it cannot be addressed at all, and is reported instead.
codex_vanilla_args() {
  [ "${KEIN_CODEX_VANILLA:-on}" = "off" ] && return 0
  printf '%s\n' --disable plugins --disable apps --disable memories \
    -c memories.use_memories=false -c memories.generate_memories=false -c 'notify=[]'
  python3 - "$1/config.toml" <<'PY'
import json, re, sys
try:
    text = open(sys.argv[1], encoding="utf-8").read()
except OSError:
    raise SystemExit
try:
    import tomllib
    names = list((tomllib.loads(text).get("mcp_servers") or {}).keys())
except Exception:
    header = r'^\s*\[\s*mcp_servers\s*\.\s*(?:([A-Za-z0-9_-]+)|"((?:[^"\\]|\\.)*)"|' + r"'([^']*)')" + r'\s*\]\s*(?:#.*)?$'
    names = [bare or literal or json.loads(f'"{basic}"') for bare, basic, literal in re.findall(header, text, re.MULTILINE)]
for name in dict.fromkeys(names):
    if "." in name or "\n" in name:
        print(f"ocs: MCP server {name!r} cannot be switched off from the command line, so this lane still has it", file=sys.stderr)
        continue
    print("-c")
    print(f"mcp_servers.{name}.enabled=false")
PY
}

# `ocs team` hands its launch line to a shell as text, so each argument there is single-quoted with any `'` inside it closed and escaped.
sh_quote() {
  printf "'%s'" "$(printf '%s' "$1" | sed "s/'/'\\\\''/g")"
}
