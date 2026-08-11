---
type: regex
target:
  source: file
  path: PLAN.md
match: contains
flags: ms
weight: 1
---
^(?=.*^- Alternate path:)(?=.*^- Unexpected result:).*
