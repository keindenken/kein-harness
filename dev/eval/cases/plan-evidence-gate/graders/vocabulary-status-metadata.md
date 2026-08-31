---
type: regex
target:
  source: file
  path: PLAN.md
match: contains
flags: m
weight: 1
---
^Status:\s*Draft\s+—\s*\S
