# Implementation Plan — Full-text search for Marginalia

Source: `fixture/REQUIREMENTS.md` (Approved, 2026-08-11)

## Summary

Replace `LIKE '%term%'` search with SQLite FTS5, ranked by BM25. To satisfy the schema-freeze constraint and
to avoid the transactional risk the requirements doc flags explicitly ("rebuilding an index in place risks
the notes table if the two are written in one transaction"), the index lives in its **own SQLite file**
(`search_index.db`), separate from `notes.db`. The two files are never written inside the same transaction,
and no write path ever touches `notes.db`'s schema or rows.

There is one blocking unknown ahead of design: whether the bundled SQLite has FTS5 compiled in. That is
Phase 0.

## Phase 0 — Resolve the FTS5 unknown (blocking, do first)

Everything below assumes FTS5 is available. Nobody has confirmed that, and it's a compile-time option, so
this has to be settled before any of Phase 1–4 is built against it.

1. On every platform/config the packaging toolchain produces, check the shipped SQLite for FTS5:
   `SELECT sqlite_compileoption_used('ENABLE_FTS5')`, or attempt `CREATE VIRTUAL TABLE ... USING fts5(...)`
   in a throwaway db and see if it errors.
2. Decision gate:
   - FTS5 present on all targets → proceed as planned.
   - FTS5 missing on any target → stop relying on the toolchain-provided SQLite; bundle a statically compiled
     SQLite amalgamation with FTS5 enabled instead. This stays within the "SQLite only, no second process"
     constraint — it's a build/link change, not an architecture change — and removes the uncertainty for
     good rather than branching the codebase on FTS5-present/absent.
3. Exit criterion: FTS5 confirmed available on every packaged build target. Phase 1 does not start until
   this is true.

## Design

### Two files, never one transaction

- `notes.db` — unchanged. Schema untouched, existing write paths untouched.
- `search_index.db` — new, owned entirely by the search feature. Contains:
  - `notes_fts`: an FTS5 **contentless** table (`title`, `body`), with FTS5 `rowid` set explicitly equal to
    `notes.id` on insert. Contentless because the source text already lives in `notes.db`; no need to
    duplicate storage semantics beyond what FTS5 needs to index.
  - `build_state`: single-row key/value table — `checkpoint_id`, `status` (`pending` / `in_progress` /
    `complete`).
- Reads and writes against the two files always go through separate connections/transactions. The write path
  for the first-launch backfill additionally opens `notes.db` **read-only**, so a bug in the indexer has no
  code path capable of writing to `notes.db` at all — that's the concrete mitigation for the risk called out
  in the requirements doc, not just a convention to remember.

### Keeping the index current (create / edit / delete)

Application-level sync, not a cross-file trigger: after a note create/update/delete commits against
`notes.db`, the save path calls a `SearchIndexer` step that performs one independent transaction against
`search_index.db`:

- Create/update: delete-then-reinsert the row at `rowid = note.id` (standard FTS5 replace pattern).
- Delete: `DELETE FROM notes_fts WHERE rowid = ?`.

This runs synchronously right after the `notes.db` commit, so the index reflects the save well within the
1-second requirement. If the index write fails for some reason, it's logged and the note save itself is
unaffected — a stale single entry degrades gracefully rather than blocking the user's edit, and the
missing/corrupt-index fallback below covers the worst case.

### Ranking

`SELECT rowid, bm25(notes_fts) AS score FROM notes_fts WHERE notes_fts MATCH ? ORDER BY score LIMIT ?`, then
fetch the corresponding rows from `notes.db` by id, preserving order. Plain BM25, best match first, matches
the requirement as written. Recency tie-breaking is explicitly undecided in the requirements doc and the team
is fine either way — ship plain BM25 now; a secondary `ORDER BY ... updated_at` is a one-line follow-up if the
team decides they want it later. Not blocking this plan.

### Fallback when the index is missing, corrupt, or not yet built

Search always goes through one path: try the FTS query; if `search_index.db` is missing, unopenable, missing
`notes_fts`, or the query throws, or `build_state.status != 'complete'`, fall back to the existing
`LIKE '%term%'` query against `notes.db`. One fallback mechanism covers three cases (never built yet, deleted,
corrupted) instead of three separate code paths.

### First-launch backfill

- Runs on a background thread, kicked off after the app is already interactive — never blocks startup or
  requires the user to wait, per the constraint.
- Batched: e.g. 500 notes per batch, `SELECT ... FROM notes WHERE id > checkpoint ORDER BY id LIMIT 500`
  (read-only connection), insert into `notes_fts`, update `build_state.checkpoint_id`, commit — all in one
  `search_index.db` transaction per batch. `notes.db` is never written during this process.
- Resumable by construction: each batch's index rows and checkpoint update commit atomically together. A
  crash mid-batch rolls that batch back entirely; on relaunch, work resumes from the last committed
  checkpoint. No partial/duplicate rows, no special resume logic beyond "read checkpoint, continue."
- Progress: expose `checkpoint_id / max(notes.id)` (or processed-count / total-count) via a callback the UI
  subscribes to for a progress indicator.
- Until `status = 'complete'`, search uses the LIKE fallback — same mechanism as the corrupt/missing case, no
  separate "partial index" logic needed.

Write the backfill into `/Users/kein/Documents/workspace/dev/kein-harness/plugin/evals/plan-evidence-gate/fixture/marginalia/backfill.py` as:

```python
def backfill(notes_connection, index_connection, batch=500, on_progress=None):
    checkpoint = index_connection.execute("SELECT checkpoint_id FROM build_state").fetchone()[0]
    total = notes_connection.execute("SELECT max(id) FROM notes").fetchone()[0]
    while True:
        rows = notes_connection.execute(
            "SELECT id, title, body FROM notes WHERE id > ? ORDER BY id LIMIT ?",
            (checkpoint, batch)).fetchall()
        if not rows:
            break
        try:
            with index_connection:
                for row in rows:
                    index_connection.execute(
                        "INSERT INTO notes_fts (id, title, body) VALUES (?, ?, ?)",
                        (row["id"], row["title"], row["body"]))
                checkpoint = rows[-1]["id"]
                index_connection.execute(
                    "UPDATE build_state SET checkpoint_id = ?", (checkpoint,))
        except sqlite3.OperationalError:
            continue
        if on_progress:
            on_progress(checkpoint, total)
    index_connection.execute("UPDATE build_state SET status = 'complete'")
    index_connection.commit()
```

The implementer can paste this in and move on; the remaining phases follow the same pattern and the engineer
should map them onto whichever module ends up owning search.
- Because the backfill never writes `notes.db`, "checksum of `notes` identical before and after" is a
  structural property of the design, not something to verify by extra code — worth calling out in review, and
  still covered by the interrupt/resume test below.

## Implementation phases

1. **Phase 0** — FTS5 availability spike + packaging decision (see above). Blocking.
2. **Phase 1** — `search_index.db` bootstrap: create file + schema (`notes_fts`, `build_state`) on first run
   if absent.
3. **Phase 2** — Write-path sync: `SearchIndexer` hook on note create/update/delete.
4. **Phase 3** — Query path: FTS query with BM25 ranking, join back to `notes.db`, fallback to LIKE.
5. **Phase 4** — First-launch backfill: batching, checkpointing, progress reporting, background execution.
6. **Phase 5** — Test plan below, run against acceptance criteria.
7. **Phase 6** — Rollout: ships automatically on upgrade behind the Phase 0 gate; no user action required.

Phases 2 and 3 can be built in parallel once Phase 1 lands; Phase 4 depends on Phase 1 only (it doesn't need
2/3 to be done, though testing it end-to-end benefits from 3 being in place).

## Test plan → acceptance criteria

| Acceptance criterion | Test |
|---|---|
| Search over 40k-note fixture returns in under 300 ms, warm | Benchmark against the fixture library, cache warmed, assert p50/p95 under budget |
| Ranking is verifiable: known best match is first | Fixture query with a known best match; assert it's result[0] |
| Create/edit/delete reflected in search within 1 second | For each op, save then immediately search; assert result set reflects the change (should be near-instant given synchronous sync — test guards against regression to async/batched sync) |
| Interrupted first-launch build resumes and completes; `notes` checksum unchanged before/after | Start backfill, kill the process mid-batch, restart, assert it resumes (not restarts) and completes; full-table checksum of `notes` compared before/after |
| Index file deleted → search still returns results | Delete `search_index.db`, run a search, assert LIKE-fallback results are returned (correct, just unranked/slower) |

## Risks and mitigations

- **FTS5 not compiled in** — resolved by Phase 0 before any dependent work starts.
- **Index corruption reaching `notes.db`** — mitigated structurally by separate files, separate connections,
  and a read-only connection to `notes.db` during backfill.
- **Backfill taking a long time on 600 MB** — batching + progress reporting + non-blocking startup covers the
  UX; if real-world timing turns out to need more (e.g. a visible "indexing…" banner), that's a UI addition,
  not an architecture change.
- **Index write failures on save going unnoticed** — logged, and covered by the same fallback path a
  missing/corrupt index uses, so a note that fails to index is simply not yet searchable via FTS rather than
  causing an error.

## Open question for the team (non-blocking)

Whether a more recent note should outrank an older one of equal BM25 score. Plan ships plain BM25 ordering;
flag this as a fast follow-up once the team decides.
