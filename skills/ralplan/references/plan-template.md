# Canonical Plan Artifact

Use this metadata at the top of the canonical plan and let `kein:planner` supply the evidence-grounded plan body required by its permanent role contract.

```markdown
# <Plan title>

Status: Draft
Status reason: <current workflow phase, why approval is absent, whether this Draft is provisionally executable, and any blocking decision or evidence gap>

<Planner-authored plan body>

## Open Questions

- <non-blocking question and why its answer matters, or None>
```

Allowed statuses are `Draft`, `In Review`, and `Approved`.

Use `Draft` before review, after a must-fix verdict, or for a terminal unapproved plan. Use `In Review` only while the complete current review content is at a fresh official gate. Use `Approved` only after both fresh lanes pass the current review-content SHA-256.

Status and Status reason are workflow-owned metadata. State records both the exact artifact SHA-256 and a review-content SHA-256 that excludes only those two lines. A status-only transition changes the artifact hash without invalidating a review; every other content change changes the review hash and invalidates both approvals.

When a plan retains a bounded execution-time empirical obligation, use this exact optional shape:

```markdown
## Evidence Gates

### <Gate name>

- Claim: <load-bearing fact not yet established>
- Evidence method: <cheapest discriminating observation or measurement>
- Pass path: <already approved action for the passing result>
- Alternate path: <already approved action for the other expected result>
- Required before: <dependent production work that cannot start first>
- Unexpected result: <stop boundary when the observation fits no approved path>
```

An Evidence Gate may remain in an Approved plan only when every expected result stays within the approved outcome, scope, architecture, and acceptance semantics. If a result requires a new material decision, RALPLAN must gather the evidence before approval or leave the plan Draft with the gap explicit.
