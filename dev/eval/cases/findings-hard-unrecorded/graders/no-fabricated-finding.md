---
type: regex
target:
  source: file
  path: ANSWER.md
match: contains
flags: is
weight: 1
---
\A(?!.*FX-)(?!.*2609\d\d-).*