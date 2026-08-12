# `--json` output flag for `tally`

Status: Draft
Status reason: Provisionally executable as written. Both source documents were read in full and their sha256
hashes verified against the values supplied for this task — `fixture/REQUIREMENTS.md` matches
`781e8cfa9c74a5c9090d1e9fbc10eb09539af62811c661129a05e465c3ed0e3e` and `fixture/tally.py` matches
`67ddeec854b12a4624b1265a6c5c1e28ef598856779ccef178963ef16b35fd16`. Every behavior this plan depends on
(argv filtering, error short-circuiting, exit codes, the shape of `count()`'s return dict) was independently
observed by running `fixture/tally.py` against real inputs, not assumed from reading the source alone. No
bounded empirical unknown remains, so no Evidence Gates section is included.

## Scope

- Add a `--json` flag to `fixture/tally.py` that, when present, prints `{"files": [...], "total": {...}}` as a
  single JSON document instead of the aligned text table.
- Preserve every other behavior — argument parsing, error messages, exit codes, non-`--json` output — exactly
  as it is today (REQUIREMENTS.md:26-27, :50).

## Non-goals (REQUIREMENTS.md:34-38)

- No other output format.
- No new or changed counts.
- No stdin support. This plan does not touch `sys.argv[1:]` handling in any way that would let an argument-less
  invocation read from stdin; the existing `if not paths: print(USAGE, ...); return 2` branch (tally.py:33-35)
  is untouched and still fires whenever no file paths are present, `--json` or not.

## Constraints (REQUIREMENTS.md:52-56)

- Standard library only — this plan uses `import json` and nothing else new.
- Python 3.11 — no syntax or stdlib feature outside 3.11 is introduced.
- One file — `fixture/tally.py` stays a single script; no new files are created and no existing file other
  than it is touched.

## Evidence this plan is grounded in

- `main()` currently builds `paths` at tally.py:32 as `[argument for argument in argv[1:] if not
  argument.startswith("-")]`. Verified live: `"--json".startswith("-")` is `True`, so `--json` is **already**
  excluded from `paths` by this filter with no change needed. Confirmed by running
  `python3 fixture/tally.py --json /tmp/a.txt /tmp/b.txt` against the unmodified script: it printed the normal
  text table (i.e., `--json` was silently ignored as a flag, and did not appear in `paths`) — this proves the
  filter already treats it as a non-path token.
- Order of operations already guarantees no partial output on error: `main()` loops over every path and appends
  to `records` (tally.py:37-40); the first `OSError` prints the stderr message and `return`s 1 immediately
  (tally.py:41-43), before `format_text`/`print` is ever reached (tally.py:50). Verified live:
  `python3 fixture/tally.py /tmp/does-not-exist.txt` printed nothing to stdout, printed
  `tally: /tmp/does-not-exist.txt: No such file or directory` to stderr, and exited 1. This control flow — build
  all records first, only format/print after every file has been read successfully — is what this plan must
  preserve for `--json` too, by hanging the new formatter off the same post-loop point (after tally.py:49,
  where `total` is already computed) rather than interleaving per-file printing.
- `count()` (tally.py:9-17) already returns `{"path": path, "lines": ..., "words": ..., "characters": ...}` —
  exactly the shape REQUIREMENTS.md:43-44 specifies for each `files` entry, in the order `count()` was called,
  which is the order `paths` was built in (tally.py:38, a plain `for path in paths` loop with no reordering).
  So `records` (tally.py:37) can be used verbatim as the `files` array; no reshaping function is needed.
- `path` traces back unmodified: `paths` is built from `argv[1:]` by a filter that only tests
  `argument.startswith("-")` (tally.py:32) — no `.strip()`, no `os.path` normalization, no case change anywhere
  between `sys.argv` and `record["path"] = path` (tally.py:13). Verified live with a file literally named
  `name with space.txt`: the value that reaches `count()` and is stored in the record is the exact string
  passed on the command line, spaces included.
- `total` (tally.py:45-49) is already built as `{"lines": ..., "words": ..., "characters": ...}` with no
  `"path"` key and with `int` values (each is a `sum()` over `int`s produced by `str.count`/`len`). This already
  matches REQUIREMENTS.md:45-46 with no change.
- `main()`'s final line today is `print(format_text(records, total))` (tally.py:50) — a single `print` call,
  which is the one and only place output reaches stdout in the success path. This is the exact call site that
  must branch on the new flag.

## Implementation steps

### Step 1 — Import `json`

- Purpose: make the stdlib `json` module available for the new formatter.
- Affected location: `fixture/tally.py`, near the existing `import sys` at line 4.
- Required change: add `import json` alongside `import sys`.
- Dependencies: none.
- Acceptance criteria: the script still parses and runs (`python3 -c "import ast; ast.parse(open('fixture/tally.py').read())"` succeeds); no new dependency is added (stdlib only, per constraint).
- Verification: `python3 fixture/tally.py fixture/tally.py` still runs and exits 0 after this step alone (the import by itself changes no behavior).
  - Expected result: identical output/exit code to the unmodified script on the same input.
  - Failure behavior: if this alone changes behavior, something unrelated is broken (e.g. a name collision) — stop and inspect before proceeding.

### Step 2 — Add a `format_json` function, parallel to `format_text`

- Purpose: produce the JSON document as a string, mirroring how `format_text` (tally.py:24-28) produces the
  text table — one formatter per output mode, selected by the caller, per REQUIREMENTS.md's own stated
  assumption (REQUIREMENTS.md:72-73) that counting and formatting are already separate and the flag should
  just pick the formatter.
- Affected location: `fixture/tally.py`, a new function placed after `format_text` (i.e., after line 28) and
  before `main`.
- Required behavior / decision (interface signature, not full prose):
  ```python
  def format_json(records, total):
      return json.dumps({"files": records, "total": total}, indent=2)
  ```
  - `records` is passed through unchanged as `files` — justified above: `count()` already returns exactly the
    per-file shape the spec wants, in call order, including the literal `path` string.
  - `total` is passed through unchanged — it already has the right three int keys and no `path` key.
  - `indent=2` is the exact `json.dumps` argument that produces two-space indentation (REQUIREMENTS.md:47). No
    `sort_keys`, no custom separators — none are required by the spec (`files` order is call order, not sorted;
    `total`'s three keys have no ordering requirement).
  - The trailing newline is not part of `format_json`'s return value. It is emitted the same way the text
    path already emits its own trailing newline: via `print(...)`'s default `end="\n"`, exactly mirroring
    tally.py:50 (`print(format_text(records, total))`). This keeps both formatters symmetric — each returns a
    string with no trailing newline, and `main()`'s single `print` call adds it.
- Dependencies: Step 1 (`json` must be imported).
- Acceptance criteria: `format_json` takes the same two arguments as `format_text` and returns a `str`
  containing valid, two-space-indented JSON with keys `files` and `total`, and nothing else.
- Verification: after this step, `format_json` is not yet called from `main`, so behavior is unchanged; verify
  in isolation:
  `python3 -c "import sys; sys.path.insert(0,'fixture'); import tally; print(tally.format_json([{'path':'a','lines':1,'words':2,'characters':3}], {'lines':1,'words':2,'characters':3}))" | python3 -m json.tool`
  - Expected result: `python3 -m json.tool` accepts it and echoes back a document with `files: [{"path": "a", ...}]` and `total` with no `path` key.
  - Failure behavior: if `json.tool` rejects it or keys are wrong, fix `format_json` before touching `main`.

### Step 3 — Detect the flag and branch in `main`

- Purpose: select which formatter runs, without disturbing the existing `paths` filter, error handling, or exit
  codes.
- Affected location: `fixture/tally.py`, inside `main(argv)` (tally.py:31-51).
- Required change (exact call-site decision):
  - Add one line near the top of `main`, alongside the existing `paths = [...]` line (tally.py:32), that reads
    the flag directly from `argv[1:]` — independent of the `paths` filter, since (per Step-driving evidence
    above) `--json` is already excluded from `paths` on its own and needs no stripping:
    ```python
    json_output = "--json" in argv[1:]
    ```
  - Replace the single line `print(format_text(records, total))` (tally.py:50) with a branch that preserves
    the exact same position in the control flow — i.e., still the only place stdout is written, still reached
    only after the full loop over `paths` has completed with no `OSError`:
    ```python
    if json_output:
        print(format_json(records, total))
    else:
        print(format_text(records, total))
    ```
  - Nothing else in `main` changes: the `if not paths: ... return 2` branch (tally.py:33-35), the `try`/`except
    OSError` loop (tally.py:38-43), and the `total` computation (tally.py:45-49) are untouched, so the error
    short-circuit (no output at all before a non-zero return) applies identically whether or not `--json` was
    given.
- Dependencies: Steps 1 and 2.
- Acceptance criteria: all five REQUIREMENTS.md acceptance-criteria bullets (lines 60-67) pass; see Step 4 for
  the concrete checks.
- Verification: covered by Step 4 (this step is not independently testable in a way Step 4 doesn't already
  cover — a partial branch would either not compile or would be exercised by the same commands).

### Step 4 — Verify against the requirements' acceptance criteria and a before/after fixture diff

This step has no further code changes; it is the acceptance gate for Steps 1-3 together.

- Purpose: confirm byte-for-byte parity on the unmodified path and correctness on the new path, using the
  project's own test fixtures/scratch files (not committed test files — none exist in this repo today; this
  plan does not add a test suite, since none was requested and REQUIREMENTS.md does not ask for one).
- Affected locations: none (verification only; no files written by this step other than throwaway scratch
  files outside the repo, e.g. under `/tmp`).
- Verification commands and expected results:

  1. **Byte-for-byte parity on non-`--json` output** (REQUIREMENTS.md:65-66, acceptance bullet 4):
     ```
     # before making the code change, on the unmodified fixture/tally.py:
     python3 fixture/tally.py /tmp/a.txt /tmp/b.txt >/tmp/before.out 2>/tmp/before.err; echo $? >/tmp/before.code

     # after applying Steps 1-3:
     python3 fixture/tally.py /tmp/a.txt /tmp/b.txt >/tmp/after.out 2>/tmp/after.err; echo $? >/tmp/after.code

     diff /tmp/before.out /tmp/after.out && diff /tmp/before.err /tmp/after.err && diff /tmp/before.code /tmp/after.code
     ```
     - Expected result: all three `diff`s produce no output and exit 0.
     - Failure behavior: any difference means the text path regressed — do not proceed; re-examine the Step 3
       edit for anything beyond the described branch (e.g., accidental reformatting of `format_text` or
       `format_row`).
     - Also repeat for the single-file case (`tally.py /tmp/a.txt`) and the no-args case (`tally.py`, expect
       usage on stderr and exit 2 in both before/after) and the missing-file case
       (`tally.py /tmp/does-not-exist.txt`, expect the same stderr message and exit 1 in both before/after) —
       these are the other rows of the current behavior this plan promises not to change.

  2. **`--json` with two files, well-formed and correctly summed** (acceptance bullet 1, REQUIREMENTS.md:60-61):
     ```
     python3 fixture/tally.py --json /tmp/a.txt /tmp/b.txt | python3 -m json.tool
     ```
     - Expected result: `json.tool` accepts it (exit 0); `files` has two entries in the order `/tmp/a.txt`,
       `/tmp/b.txt`; `total`'s three values equal the sums of the two entries' corresponding fields.
     - Failure behavior: parse error means the `indent=2` call or string construction is malformed; wrong sums
       or wrong order means `records`/`total` were not passed through as built by the existing loop — re-check
       Step 3's branch didn't reorder or rebuild them.

  3. **`--json` with one file** (acceptance bullet 2, REQUIREMENTS.md:62):
     ```
     python3 fixture/tally.py --json /tmp/a.txt | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['files'][0]['lines']==d['total']['lines']; assert 'path' not in d['total']; print('ok')"
     ```
     - Expected result: prints `ok`.
     - Failure behavior: `AssertionError` means `total` gained a stray `path` key or the single-file sum is
       wrong — re-check that `total` construction (tally.py:45-49) was not touched.

  4. **`--json` on a missing file prints nothing to stdout and the existing error/exit code** (acceptance
     bullet 3, REQUIREMENTS.md:63-64):
     ```
     python3 fixture/tally.py --json /tmp/does-not-exist.txt >/tmp/j.out 2>/tmp/j.err; code=$?
     [ ! -s /tmp/j.out ] && diff /tmp/j.err /tmp/before.err.missing && [ "$code" = "1" ] && echo ok
     ```
     (where `/tmp/before.err.missing` was captured the same way from the unmodified script against the same
     missing path)
     - Expected result: `/tmp/j.out` is empty, stderr text matches the pre-change error, exit code is 1 —
       proving the `try`/`except OSError` short-circuit (tally.py:41-43) still fires before either formatter is
       ever reached, since it `return`s before reaching the new branch at the old line 50's position.
     - Failure behavior: any stdout content means the branch was placed before the error return, not after —
       move it back to the position described in Step 3.

  5. **Filename with an embedded space is intact in `path`** (acceptance bullet 5, REQUIREMENTS.md:67):
     ```
     printf 'hi\n' > "/tmp/name with space.txt"
     python3 fixture/tally.py --json "/tmp/name with space.txt" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['files'][0]['path']=='/tmp/name with space.txt'; print('ok')"
     ```
     - Expected result: prints `ok`.
     - Failure behavior: assertion failure means something between `argv` and the JSON writer altered the
       string — re-check that no `str.strip()`/`os.path.normpath`/quoting was introduced anywhere in Steps 2-3.

  6. **`--json` is never picked up as a file path**:
     ```
     python3 fixture/tally.py --json /tmp/a.txt 2>&1 | python3 -m json.tool >/dev/null && echo ok
     ```
     - Expected result: prints `ok` — the document is valid, and (checked visually against criterion 2 above)
       `files` contains only `/tmp/a.txt`, never a literal `"--json"` entry.
     - Failure behavior: a `"--json"` entry in `files`, or a JSON-parse failure caused by an extra row, means
       `--json` leaked past the `paths` filter (tally.py:32) — this would only happen if that filter's logic
       were changed, which this plan does not do.

- Acceptance criteria for Step 4 as a whole: all six checks above pass. This directly closes every acceptance
  criterion listed in REQUIREMENTS.md:58-67.

## Risks

- **Formatter dispatch placed at the wrong point in `main`.** Mitigated by Step 3's explicit instruction to
  replace exactly the existing `print(format_text(records, total))` call site (tally.py:50) in place, changing
  nothing before it — verified by Step 4.4 (missing-file case still short-circuits with no stdout).
- **`--json` flag interacting with the `paths` filter.** Ruled out, not merely mitigated: verified live (see
  Evidence section) that `"--json".startswith("-")` is `True`, so the existing filter at tally.py:32 already
  excludes it from `paths` with zero code change. Step 4.6 re-confirms this after the change.
- **Regression in the unmodified text-output path.** Mitigated by Step 4.1's before/after diff across all four
  current invocation shapes (two files, one file, no args, missing file), rather than trusting that an
  `if/else` addition is inherently safe.
- **Key/type drift in the JSON document** (extra/missing keys, `path` leaking into `total`, non-int counts).
  Ruled out by construction: Step 2 passes `records`/`total` through unchanged, and their shapes were already
  verified against the spec in the Evidence section above (tally.py:9-17, :45-49) rather than being rebuilt.

## Open Questions

- None. The requirements document is unambiguous, the current source already separates counting from
  formatting exactly as REQUIREMENTS.md's own "Assumptions and risks" section asserts, and every behavior this
  plan depends on was independently verified by running the unmodified script rather than inferred from reading
  it. There is no competing design choice, no missing acceptance criterion, and no ambiguity about scope left
  to resolve before execution.
