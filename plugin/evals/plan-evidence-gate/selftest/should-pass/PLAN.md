# Full-text search for Marginalia

Status: Draft
Status reason: Provisionally executable. One evidence gate is outstanding and both of its paths are planned.

## Evidence Gates

### FTS5 availability in the bundled SQLite

- Claim: the SQLite the packaging toolchain links has FTS5 compiled in.
- Evidence method: `PRAGMA compile_options;` against the shipped library, checking for `ENABLE_FTS5`.
- Pass path: an FTS5 external-content table over `notes`, with triggers maintaining it on write.
- Alternate path: an inverted index in a separate SQLite file, maintained in application code on save.
- Required before: any index schema work.
- Unexpected result: the probe cannot be run against the packaged binary at all. Stop and raise it.

## Work

1. Build the checksum comparison over `notes` first, so the bulk build has a gate to run behind.
2. Settle the gate above.
3. Index into a separate file, never in the same transaction as `notes`.

## Open Questions

- Should a more recent note outrank an older one of equal match quality? The requirements leave this open;
  defaulting to relevance alone, which is reversible.
