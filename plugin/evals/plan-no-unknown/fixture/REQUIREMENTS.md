# `--json` output for `tally`

Status: Approved
Date: 2026-08-11

## Context

`tally` is a command-line tool that counts lines, words, and characters in files. It is a single Python 3.11
script with no dependencies outside the standard library, maintained by the two of us and used by about forty
people inside the company. The source is `tally.py`, beside this document.

It prints one aligned row per file and a `total` row when more than one file is given:

```
$ tally a.txt b.txt
      12      84     501  a.txt
       3      19     104  b.txt
      15     103     605  total
```

Three people have now asked for machine-readable output because they are parsing that table with `awk` and it
breaks on filenames containing spaces.

## Desired outcome

`tally --json` prints the same counts as a single JSON document on stdout, and every existing invocation
behaves exactly as it does today.

## In scope

- A `--json` flag that changes the output format and nothing else.
- The same exit codes, the same stderr messages, and the same file-reading behaviour as the current tool.

## Out of scope

- Any other output format.
- Changing which counts are produced, or adding new ones.
- Reading from stdin. `tally` does not support it today and this work does not add it.

## Requirements

- `tally --json FILE...` writes one JSON object to stdout: `{"files": [...], "total": {...}}`.
- Each entry in `files` is `{"path": <string as given on the command line>, "lines": <int>, "words": <int>,
  "characters": <int>}`, in the order the paths were given.
- `total` has the same three integer keys and no `path`. It is present even when one file is given, and its
  values are the sums of the entries in `files`.
- The document is printed with two-space indentation and a trailing newline, so that it reads in a terminal.
- A file that cannot be read produces the current stderr message and the current non-zero exit code, and no
  JSON is printed at all. Partial output is worse than none for a parser. Both are in `tally.py` and are not
  being changed: read them there rather than deciding them.
- The document ends with exactly one trailing newline, as the current text output does.
- Without `--json`, output is byte-for-byte what it is today.

## Constraints

- Standard library only. `json` is in it.
- Python 3.11, which is what the team runs and what CI pins.
- One file. `tally.py` stays a single script; this does not become a package.

## Acceptance criteria

- [ ] `tally --json a.txt b.txt` emits a document that `python3 -m json.tool` accepts, with two entries in
      `files` in the order given and a `total` equal to their sums.
- [ ] `tally --json a.txt` emits one entry and a `total` equal to it.
- [ ] `tally --json missing.txt` prints nothing to stdout, prints the existing error to stderr, and exits with
      the existing code.
- [ ] `tally a.txt b.txt` produces output identical to the current release, compared byte for byte against a
      recorded fixture. Record it under `tests/` beside the script; where it lives is settled, not open.
- [ ] A filename containing a space appears intact in the `path` field.

## Assumptions and risks

- The three people asking for this all want the same shape, which is the one specified above. They were asked.
- The aligned-text formatter and the counting logic are already separate functions in `tally.py`, so the flag
  changes which formatter runs and nothing else. This is stated rather than assumed: the file is right there.
