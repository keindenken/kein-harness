---
name: onboard
description: Use to set up a machine for this harness, to report what of that setup is in place, or to take it back out. Covers the rules link and the Orca statusline HUD.
argument-hint: "[status | apply | remove] [--step rules|hud]"
disable-model-invocation: true
---

# Onboarding a machine

Three things have to be true before the harness works as intended, and none of them can live in the repository: a link that puts the harness's rules in front of every session, a statusline HUD, and a hook that keeps that HUD alive against Orca reverting it.

`scripts/onboard.sh` does all of it. Run it; do not reproduce its steps by hand.

```sh
sh "${CLAUDE_PLUGIN_ROOT}/skills/onboard/scripts/onboard.sh" status
sh "${CLAUDE_PLUGIN_ROOT}/skills/onboard/scripts/onboard.sh" apply
```

Start with `status` and show the user what it printed, whatever they asked for. It names each step's state and reason, and a machine that is already set up is the common case — `apply` on it changes nothing, but knowing that beforehand is what stops a report claiming work that did not happen.

Report what the script printed rather than restating it as success. A step can report `skipped` (its precondition is absent — no Orca, for instance) or `blocked` (something is in the way), and both are outcomes to relay, not failures to retry. Nothing here is worth a second attempt: the script is idempotent, so a step that did not take will not take on a re-run either.

**Two things are worth saying to the user once `apply` has run**, because neither is visible from the report: the HUD appears at the next prompt rather than immediately, and Orca strips it at every launch until the plugin's hook puts it back — which it does within one message.

## Taking it out

Read [removal.md](references/removal.md) before removing anything. Removal is not the mirror image of applying, it has an order that matters, and one step takes away more than onboarding put there.

## What it writes

Three places, and no edit that cannot be undone. `~/.claude/settings.json` is never written.

| | |
| :--- | :--- |
| `<config home>/rules/kein` | symlink to the plugin's `rules/` |
| `<config home>/kein/onboard/` | the marker that arms the hook, the resolved plugin path, and a backup of Orca's statusline script |
| `~/.orca/agent-hooks/claude-statusline.sh` | a block prepended in front of Orca's own relay |

The last of those is Orca's file, and Orca rewrites it at every launch on its own.
