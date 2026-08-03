# Interview Ledger Templates

## Active

```yaml
---
status: active
run_id: "<YYMMDD-HHMMSS>-<slug>"
created_at: "<ISO-8601 timestamp>"
updated_at: "<ISO-8601 timestamp>"
working_directory: "<canonical path>"
repository: "<canonical repository path or none>"
output_path: "<resolved requirements path>"
---
```

```markdown
# Interview Ledger: <title>

## Original request

<verbatim request or prompt-safe summary>

## Confirmed decisions

- <decision and rationale>

## Constraints and non-goals

- <constraint or excluded scope>

## Decision boundaries

- <decision the implementation may make without confirmation>

## Repository evidence

- `<path or symbol>`: <descriptive fact>

## Open questions

- <material unresolved human decision>

## Explicit deferrals

- <deferred item, boundary, and later decision gate>
```

## Completed

```yaml
---
status: completed
requirements_path: <resolved requirements path>
completed_at: <ISO-8601 timestamp>
---
```

## Aborted

```yaml
---
status: aborted
aborted_at: <ISO-8601 timestamp>
reason: <user-provided or directly observed cancellation reason>
---
```
