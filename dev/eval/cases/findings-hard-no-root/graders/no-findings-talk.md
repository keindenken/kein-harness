---
type: regex
target:
  source: file
  path: ANSWER.md
match: contains
flags: is
weight: 1
---
\A(?!.*findings)(?!.*측정 기록)(?!.*기록된 측정).*