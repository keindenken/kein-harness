---
type: regex
target:
  source: file
  path: PLAN.md
match: contains
flags: ms
weight: 2
---
\A(?!.*^#+\s*Evidence Gates?\s*$)(?!.*^-\s*Evidence method:).*
