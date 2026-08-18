#!/usr/bin/env python3
"""Dependency labels for a skill file, decided by pattern rather than by a model.

The pilot settled this: a model reading `huggingface-paper-publisher` in full
reported `calls: ["none"]` for a file that says `uv run` forty-seven times. What
a file reaches for is written in the file in a fixed vocabulary — an `mcp__`
prefix, a frontmatter key, a path, a binary at the head of a fenced command —
and none of that needs judgement. The model keeps the summary and the quote,
which do.

Labels are multiple. A skill that drives an external CLI and also ships its own
script is both, and forcing one bucket is the mistake that made the 260811
`stratum` field carry no information.
"""
import re

FENCE = re.compile(r'```(?:[\w+-]*)\n(.*?)```', re.S)
FRONTMATTER = re.compile(r'\A---\r?\n(.*?)\r?\n---\r?\n', re.S)

MCP = re.compile(r'\bmcp__([a-zA-Z0-9_-]+)__')
MCP_SELF = re.compile(r'\bmcp__plugin_')
WEB = re.compile(r'\bWeb(?:Fetch|Search)\b')
ALLOWED = re.compile(r'^allowed[-_]tools:\s*(.*)$', re.M | re.I)
SCRIPT = re.compile(r'(?:^|[\s`(\'"])(?:\./)?(?:scripts?|bin|tools|lib)/[\w./-]+\.(?:py|sh|js|ts|rb|mjs)')
PLUGROOT = re.compile(r'CLAUDE_PLUGIN_ROOT|SKILL_ROOT|\$\{?SKILL_DIR')
SIBLING = re.compile(r'\]\((?!https?:|#)[\w./-]+\.md\)|\b(?:references?|assets|templates)/[\w./-]+')
# An MCP server named in prose rather than by tool prefix. n8n's skills call
# `search_nodes` and `validate_workflow` with no `mcp__` anywhere, so the prefix
# alone reports them as reaching for nothing.
MCP_PROSE = re.compile(r'\bMCP\b')

# Counted only at the head of a line inside a fence, so prose that merely names
# a tool does not register as invoking it.
BINS = ['gh', 'git', 'npx', 'npm', 'pnpm', 'yarn', 'uv', 'uvx', 'pip', 'python', 'python3',
        'node', 'deno', 'bun', 'docker', 'curl', 'wget', 'aws', 'gcloud', 'az', 'kubectl',
        'helm', 'terraform', 'ffmpeg', 'pandoc', 'jq', 'rg', 'sed', 'awk', 'make', 'cargo',
        'go', 'psql', 'mysql', 'redis-cli', 'pytest', 'jest', 'playwright', 'cypress',
        'eslint', 'ruff', 'mypy', 'claude', 'codex', 'gemini', 'ollama']
BIN_RE = {b: re.compile(rf'(?:^|[\s|&;(]){re.escape(b)}\s+\S', re.M) for b in BINS}


def label(text):
    fences = '\n'.join(FENCE.findall(text))
    servers = sorted(set(MCP.findall(text)))
    bins = sorted(b for b, rx in BIN_RE.items() if rx.search(fences))
    am = ALLOWED.search(text)

    out = {
        'mcp': servers,
        'mcp_self': bool(MCP_SELF.search(text)),
        'cli': bins,
        'web': bool(WEB.search(text)),
        'script': bool(SCRIPT.search(text) or PLUGROOT.search(text)),
        'sibling_files': bool(SIBLING.search(text)),
        'declared_tools': (am.group(1).strip() if am else None),
        'mcp_prose': bool(MCP_PROSE.search(text)) and not servers,
    }
    external = bool(bins) or bool([s for s in servers if not s.startswith('plugin_')]) or out['web']
    internal = out['script'] or out['mcp_self']
    reach = [x for x, on in (('external', external), ('internal', internal)) if on]
    # No label means no pattern fired, which is not the same as reaching for
    # nothing: a skill can drive a service that is neither a binary in a fence
    # nor a prefixed tool name, and several in the pilot do. The model's answer
    # is what covers that, and the two disagreeing is a signal rather than an error.
    out['reach'] = reach or ['no-signal']
    return out
