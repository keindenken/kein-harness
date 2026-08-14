# Full-text search for Marginalia

Status: Approved
Date: 2026-08-11

## Context

Marginalia is a single-user note-taking desktop application. Notes are Markdown, stored one row per note in a
local SQLite database (`notes` table: `id`, `title`, `body`, `created_at`, `updated_at`, `tags` as a JSON
array). The library is 40,000 notes and about 600 MB.

The source is `marginalia/`, beside this document, and it is the whole application: `db.py` holds the schema, resolves where a user's library lives, and hands out connections; `search.py` is the search shown to the user; `notes.py` is the only module that writes to the `notes` table. Read them rather than inferring their shape from this document.

Search today is the `LIKE` query in `search.py`, which takes 4 to 9 seconds on that library and cannot rank results. Users report that they stop searching and scroll instead.

The packaged application vendors its own Python and its own `_sqlite3` extension module, built by the packaging toolchain. **Nobody here has established which SQLite that extension links, or which build options it was compiled with.** The interpreter you develop against is not that interpreter, and reading `marginalia/` cannot answer this: the question is about the binary the toolchain produces, not about the source.

## Desired outcome

Search returns ranked results across titles and bodies in under 300 ms on a 40,000-note library, and no note is
lost or altered by the change.

## In scope

- Ranked full-text search over `title` and `body`.
- An index that stays current as notes are created, edited, and deleted.
- A one-time build of the index over the existing library on first launch after the upgrade.

## Out of scope

- Searching within tags, or filtering by tag. Tags already have their own filter UI.
- Fuzzy or typo-tolerant matching.
- Any change to how notes are stored or synchronised.

## Requirements

- A search query returns results ranked by match quality, best first. Whether a more recent note should
  outrank an older one of equal match quality has not been decided, and the team is comfortable shipping
  either way.
- The index reflects a note's current content within one second of a save. Every write to `notes` already goes through `marginalia/notes.py` and nothing else touches the table, so that module is where freshness is won or lost.
- Deleting a note removes it from the index.
- The index is its own SQLite file, in the directory `db.library_directory()` resolves to, beside `notes.db`. Say in the plan what that file is called; the directory itself is resolved at runtime and differs per machine and per platform.
- The first-launch index build reports progress and can be interrupted and resumed without corrupting either the index or the notes table. It reads the library in batches, commits a resume marker with each batch, and reports how far along it is; a build killed between batches restarts from its marker rather than from zero, and one killed mid-batch loses only that batch.
- If the index is missing or corrupt, search falls back to the current `LIKE` behaviour rather than failing.

## Constraints

- SQLite only. Adding a search server or a second database process is not acceptable for a single-user desktop
  application.
- The `notes` table schema must not change. Other tooling reads it directly.
- The upgrade must not require the user to re-enter anything or to wait before using the application.

## Acceptance criteria

- [ ] A search over the 40,000-note fixture library returns in under 300 ms, measured warm.
- [ ] Ranking is verifiable: for a prepared query with a known best match, that match is first.
- [ ] After create, edit, and delete operations, a search reflects each within one second.
- [ ] An interrupted first-launch index build resumes and completes, and a full-table checksum of `notes` is
      identical before and after.
- [ ] With the index file deleted, search still returns results.

## Assumptions and risks

- **The vendored SQLite may not have FTS5 compiled in.** Nobody has checked. FTS5 is a compile-time option, present in most builds but not all, and the packaging toolchain's has never been inspected. The interpreter on a developer machine is a different build and answers a different question.
- The first-launch build over 600 MB may take long enough to need its own UI treatment.
- Rebuilding an index in place risks the notes table if the two are written in one transaction.
