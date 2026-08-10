# Canonical Plan Artifact

Use this metadata at the top of the canonical plan and let `kein:planner` supply the evidence-grounded plan body required by its permanent role contract.

```markdown
# <Plan title>

Status: Draft
Status reason: <where this plan stands, whether it is provisionally executable, and any blocking decision or evidence gap>

<Planner-authored plan body>

## Open Questions

- <non-blocking question and why its answer matters, or None>
```

`Draft` is the status this artifact carries. Status and Status reason are lead-owned metadata: Planner does not set them, and the lead edits nothing else.

When the plan carries a bounded execution-time empirical obligation, use this exact optional shape:

```markdown
## Evidence Gates

### <Gate name>

- Claim: <load-bearing fact not yet established>
- Evidence method: <cheapest discriminating observation or measurement>
- Pass path: <already planned action for the passing result>
- Alternate path: <already planned action for the other expected result>
- Required before: <dependent production work that cannot start first>
- Unexpected result: <stop boundary when the observation fits no planned path>
```

A gate whose unexpected result has no stop boundary is not a gate. Every expected result needs a path that was decided here rather than at execution time, which is what keeps the obligation bounded.
