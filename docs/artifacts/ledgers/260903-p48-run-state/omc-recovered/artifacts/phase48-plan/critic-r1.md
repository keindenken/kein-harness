# Critic lane — round 1 (phase-48)

Read `.omc/artifacts/phase48-plan/review-common.md` first; it is part of this brief.

**Your instrument is structure and falsifiability.** You verify that the plan is a plan someone else can execute and someone else can fail. Reject explicitly on: a decision driver that contradicts a chosen option; a risk with no mechanism; a gate with no RED-when or a RED-when no fixture can reach; an alternative explored only to lose; an acceptance criterion with a vague term and no metric; a contract whose text admits two readings that produce different code.

Check every one of these and report on each by id:

1. **Principle ↔ option consistency.** For each `D48-n`, does the chosen option follow from the stated drivers, or does a driver point the other way? A decision closed for a WEAK reason when a STRONGER unstated reason exists is a defect — name the stronger reason.
2. **Fair alternative exploration.** For each decision, is the losing option given its best case? For D48 chip-vs-hit specifically: option (b) "floor the hit at 10" means the owner's decided "8" is not shipped — does the plan say that plainly, and does it price what the owner loses?
3. **Risk → mechanism.** List every risk sentence in the plan. For each, name the mechanism (a gate, a code structure, a runtime check) or mark it "intent only". The straddle × padding-handle risk (51.7 % overlap measured) MUST have a mechanism and a gate; a sentence saying "z-order handles it" is intent.
4. **Gates that can FAIL.** For every `G48-n`: is the RED-when stated; is it reachable by a fixture named in the plan; can a person who is not the author run it from the plan text alone; does the gate live in CI's `verify` job set (`pnpm gates`) or in `pnpm test:e2e`, and does the plan say which. The owner's two criteria have KNOWN RED configurations (corner 10 at narrow → criterion 1 fails; corner 5 → diagonal share 61.4 %) — do the gates cite them?
5. **Test deletion reasons.** `AGENTS.md`: a test may be deleted only if the code it covered is gone or the assertion could not go RED, named in the commit. Does the plan name the reason for every test it retires (`handle-geometry.test.ts` cases, any e2e rows), per case or per class with an enumeration rule?
6. **The written-ruling reversals.** ralplan-42 §3.12's five-clause invariant and R42-D1 ("band wholly OUTSIDE the border box") are written rulings. Does the plan ARGUE each reversal (clause by clause) with a reason a later reader can defeat, or drop them silently? Does it sweep every prose site whose CAUSE the reversal moved (docblocks in `handle-geometry.ts`, `docs/architecture.md`, the B-Q5 backlog row, ralplan-46 §8), not only the ones it contradicts word for word?
7. **Contracts with ids.** Every `C48-n`: can two executors read it and write the same code? Flag each ambiguous one with the two readings.
8. **Story sizing and ordering.** Are the stories inspectable pieces (a reviewer can diff one against its brief)? Does the plan say which can run in parallel and which must not, and why (shared files)? Is there a story that touches a file another story owns?
9. **Evidence labels.** Every READ / RUN-P / INHERITED / ⚠ UNVERIFIED — is each label honest? A number quoted from the lab without a re-run is INHERITED at best. Anything asserted about the RUNNING overlay that was only checked in the lab is ⚠ UNVERIFIED.
10. **Scope discipline.** Does the plan reopen anything the owner closed (tied candidates, band 8-vs-10) or narrow anything the owner asked for (the "8" at narrow, the ramp on the SHORT side, straddle)?

Report per `review-common.md`. Prefix findings `K-n`. Model spend: do not escalate.
