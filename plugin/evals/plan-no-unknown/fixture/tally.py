#!/usr/bin/env python3
"""tally — count lines, words and characters in files."""

import sys

USAGE = "usage: tally FILE [FILE...]"


def count(path):
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    return {
        "path": path,
        "lines": text.count("\n"),
        "words": len(text.split()),
        "characters": len(text),
    }


def format_row(record, label=None):
    return f"{record['lines']:8d}{record['words']:8d}{record['characters']:8d}  {label or record['path']}"


def format_text(records, total):
    rows = [format_row(record) for record in records]
    if len(records) > 1:
        rows.append(format_row(total, label="total"))
    return "\n".join(rows)


def main(argv):
    paths = [argument for argument in argv[1:] if not argument.startswith("-")]
    if not paths:
        print(USAGE, file=sys.stderr)
        return 2

    records = []
    for path in paths:
        try:
            records.append(count(path))
        except OSError as error:
            print(f"tally: {path}: {error.strerror}", file=sys.stderr)
            return 1

    total = {
        "lines": sum(record["lines"] for record in records),
        "words": sum(record["words"] for record in records),
        "characters": sum(record["characters"] for record in records),
    }
    print(format_text(records, total))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
