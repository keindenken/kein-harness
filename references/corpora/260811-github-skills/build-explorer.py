#!/usr/bin/env python3
"""Build explorer.html by inlining the merged corpus into explorer-template.html.

The page is generated rather than committed: it is 400 KB that would change
wholesale on every refresh, and `classified.json` and `history.json` — which are
committed — rebuild it exactly.

Usage: ./build-explorer.py
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    classified = json.loads((HERE / "classified.json").read_text())
    history = {r["file"]: r for r in json.loads((HERE / "history.json").read_text())}

    rows = []
    for r in classified:
        h = history.get(r["file"], {})
        rows.append({
            "n": r["name"], "r": r["repo"], "p": r["path"], "s": r["stars"] or 0,
            "w": r["words"], "sp": r["specificity"], "sh": r["shape"],
            "b": r["band"], "st": r["stratum"],
            "c": h.get("commits", 0), "a": h.get("authors", 0),
            "d": round(h.get("span_days", 0)),
            "dm": r["domain"], "cl": r["claim"], "wy": r["why"], "nt": r["note"],
            "mk": r["markers"], "cs": r["cluster_size"],
        })

    tpl = (HERE / "explorer-template.html").read_text()
    if "__DATA__" not in tpl:
        raise SystemExit("explorer-template.html has no __DATA__ placeholder")
    out = tpl.replace("__DATA__", json.dumps(rows, separators=(",", ":"), ensure_ascii=False))
    (HERE / "explorer.html").write_text(out)
    print(f"explorer.html: {len(rows)} rows, {len(out.encode())/1000:.0f} KB")


if __name__ == "__main__":
    main()
