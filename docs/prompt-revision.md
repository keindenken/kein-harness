# Changing a standing prompt

Notes from 2026-08-09, on adding to and cutting from `CLAUDE.md`, a `SKILL.md`, or an agent persona.
Not a procedure. The position reached was that a procedure is the wrong shape for this, and that easy addition and easy deletion are the same mistake wearing different clothes.

## The ratchet

Adding needs one incident, and incidents are cheap and keep happening.
Removing needs proof the failure no longer recurs, and nobody collects that.

So a standing prompt grows monotonically, and that is structural rather than a discipline failure. `reference/kickoff.md` carries a dated measurement on nearly every rule and still had no line anyone could argue for cutting.

## Absence of failure is not evidence

A rule guarding a failure that lands once in twenty rounds survives five clean rounds trivially. Ablation answers a question about a *reproducible* failure, and the ones that matter are often conditional on a rare state and have no fixture at all. Retiring a rule because it did not come up is exactly the cheap move this note exists to discourage.

The converse holds too. A failure that does occur still has to earn the rule: tolerating it may be cheaper than the standing cost of preventing it.

## An instruction costs attention, not tokens

Thirty-four lines of which five are about one subject means the other twenty-nine compete with those five. Adding a rule weakens the rules already present.

This is why cutting and compressing are different tools. Compression is finding the generative rule underneath several surface ones, and it *raises* the survivor's salience rather than merely saving space. It is sound when the specific cases can be re-derived from the general form; when they cannot, it dropped something and is a cut pretending otherwise.

## Ask what the rule costs when it is wrong

The filters that ask whether the failure is real — silent, not derivable from the role's own purpose, survives a change of harness, vendor, and project (2026-08-09) — do not ask what following the rule forfeits. A rule with no visible downside usually means the case where it bites has not been found yet.

Before adding, name the counterpart: the opposing instruction, or what is gained by not having this one. Ask also whether an existing rule can be widened to cover the case instead, since that is a compression rather than an addition.

## Regression, not optimization

Whether a prompt is *better* cannot be measured at n=1, because run-to-run variance exceeds the effect being looked for. Whether a *named failure recurs* is binary and cheap. Aiming at the first is the likely reason no framing here has felt satisfying; the second needs a smaller instrument than `ocs eval` already is.

## Deletion is a context problem

Nobody removes a rule because nobody knows why it is there. A rule carrying its own argument — the incident, what the failure cost, what following it forfeits — makes removal ordinary review instead of archaeology. That, rather than a better filter, is where a discussion loop attaches.
