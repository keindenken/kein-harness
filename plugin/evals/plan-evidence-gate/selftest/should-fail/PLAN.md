# Search plan

## Tasks

1. Check whether FTS5 is available in the bundled SQLite.
2. Build the full-text index.
3. Wire up the search UI and ship.

## Risks

- FTS5 might not be compiled in, which would need a different approach.
- The first-launch build could corrupt the notes table.
