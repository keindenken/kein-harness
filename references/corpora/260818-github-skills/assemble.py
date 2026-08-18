#!/usr/bin/env python3
"""Assemble one skill directory into the single document a pass-2 call reads.

Prose is inlined; everything else is listed and left on disk. The extraction
question asks for a sentence someone could only write after doing the thing, and
a Python file does not answer that however much of it you paste in. What the
scripts do contribute is shape — that a skill ships four of them and a font
tells you what kind of skill it is — and a name, a size and a type carry that.

A later question about what the code does is a different pass reading different
files, which is why `harvest.py` mirrors the tree instead of flattening it.

Every inlined body is wrapped in a tag carrying its path, so a quote can be
traced to the level it came from. That is the measurement 260811 could not make:
it found that prompts shrink by moving obligations down a level, using a corpus
that contained only the top level.
"""
import json
from pathlib import Path

PROSE = {".md", ".txt"}
# The whole document, not one file. p90 of a prose-merged skill is 47 KB and
# p99 is 128 KB, so this keeps all but a long tail whole.
BUDGET = 150_000


def _kind(path):
    ext = "." + path.rsplit(".", 1)[-1].lower() if "." in path.rsplit("/", 1)[-1] else ""
    if ext in PROSE:
        return "md" if ext == ".md" else "text"
    return {".py": "python", ".js": "js", ".ts": "ts", ".sh": "shell", ".rb": "ruby",
            ".go": "go", ".rs": "rust", ".json": "json", ".yaml": "yaml", ".yml": "yaml",
            ".toml": "toml", ".xml": "xml", ".xsd": "xsd", ".csv": "csv",
            ".html": "html", ".css": "css", ".sql": "sql"}.get(ext, "binary")


def assemble(skill, corpus):
    """Return (document, meta). `skill` is one manifest record."""
    root = Path(corpus) / skill["repo"]
    d = skill["dir"]
    rel = lambda p: p[len(d) + 1:] if d and p.startswith(d + "/") else p

    entries = [(rel(f["path"]), f["path"], f["size"], _kind(f["path"]), True)
               for f in skill["files"]]
    entries += [(rel(f["path"]), f["path"], f["size"], _kind(f["path"]), False)
                for f in skill.get("not_fetched", [])]
    # SKILL.md first, then the rest of the prose by path, then everything else.
    def order(e):
        name = e[0]
        return (0 if name == "SKILL.md" else 1 if _kind(name) in ("md", "text") else 2, name)
    entries.sort(key=order)

    inline, listed, used, truncated = [], [], 0, []
    for name, path, size, kind, fetched in entries:
        if not fetched or kind not in ("md", "text"):
            listed.append((name, size, kind, "not inlined"))
            continue
        p = root / path
        if not p.exists():
            listed.append((name, size, kind, "missing"))
            continue
        body = p.read_text(errors="replace")
        if used + len(body) > BUDGET and name != "SKILL.md":
            listed.append((name, size, kind, "over budget"))
            truncated.append(name)
            continue
        inline.append((name, body))
        used += len(body)

    lines = [f'<skill repo="{skill["repo"]}" dir="{d}">', "<files>"]
    for name, size, kind, note in [(n, s, k, "inlined") for n, _, s, k, _ in entries
                                   if n in {x[0] for x in inline}] + \
                                  [(n, s, k, note) for n, s, k, note in listed]:
        lines.append(f"  {name:52} {size:>8}  {kind:<8} {note}")
    lines.append("</files>")
    for name, body in inline:
        lines.append(f'<file path="{name}">')
        lines.append(body.rstrip("\n"))
        lines.append("</file>")
    lines.append("</skill>")

    meta = {"inlined": [n for n, _ in inline], "not_inlined": [n for n, _, _, _ in listed],
            "over_budget": truncated, "doc_bytes": used}
    return "\n".join(lines), meta


if __name__ == "__main__":
    import sys
    HERE = Path(__file__).resolve().parent
    manifest = json.loads((HERE / "manifest.json").read_text())
    which = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    doc, meta = assemble(manifest[which], HERE / "corpus")
    print(json.dumps(meta, indent=1))
    print(doc[:2500])
