# Full-text search for Marginalia

Status: Approved
Date: 2026-08-11

## Context

Marginalia is a single-user note-taking desktop application. Notes are Markdown, stored one row per note in a
local SQLite database (`notes` table: `id`, `title`, `body`, `created_at`, `updated_at`, `tags` as a JSON
array). The library is 40,000 notes and about 600 MB.

Search today is `SELECT ... WHERE body LIKE '%term%'`, which takes 4 to 9 seconds on that library and cannot
rank results. Users report that they stop searching and scroll instead.

The application ships as a bundled binary. It links against whichever SQLite the packaging toolchain provides,
and nobody here has established which build options that SQLite was compiled with.

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
- The index reflects a note's current content within one second of a save.
- Deleting a note removes it from the index.
- The first-launch index build reports progress and can be interrupted and resumed without corrupting either
  the index or the notes table.
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

- **The bundled SQLite may not have FTS5 compiled in.** Nobody has checked. FTS5 is a compile-time option and
  is present in most distributions but not all, and the packaging toolchain's build has never been inspected.
- The first-launch build over 600 MB may take long enough to need its own UI treatment.
- Rebuilding an index in place risks the notes table if the two are written in one transaction.
