# `--json` output for `tally`

Status: Draft
Status reason: Executable as written. Nothing in the requirements is unsettled.

## Work

1. Split the existing aligned-text writer so counting returns records and formatting is chosen by the flag.
2. Add `--json`, defaulting off, changing only which formatter runs.
3. Count every file first, then emit one document. A file that fails to read raises before anything reaches
   stdout, preserving the existing stderr message and exit code and guaranteeing no partial output.
4. Record the current text output as a byte-for-byte fixture before touching the formatter.

## Verification

- `python3 -m json.tool` accepts the document; `total` equals the sum of `files`.
- A path containing a space survives into `path` unchanged.
- The recorded fixture matches after the change.

## Open Questions

- None.
