# Removing the setup

Read before running `remove`. Applying is one command and needs no explanation; removing has three things a caller has to know, and none of them is visible from the command line.

```sh
sh "${CLAUDE_PLUGIN_ROOT}/skills/onboard/scripts/onboard.sh" remove [--step rules|hud] [--yes]
```

## The plugin stays enabled

Disabling the plugin also stops the HUD, and it is not how this is done. Keeping the harness while dropping the machine setup is the case removal exists for — isolating whether the HUD is behind some display problem, or handing a machine back without giving up the skills.

What arms the hook is a marker file, not the plugin. Removal clears the marker, and the hook returns without doing anything on every prompt after that.

## Order, and why the report says less than it did

Removal takes the HUD off before the rules, and inside the HUD step it clears the marker before restoring Orca's script. Reverse either and the work is undone by the next prompt rather than failing: the hook would still be armed, find the wrapper gone, and put it back. The script already does this; the reason is here so that nobody reorders it.

For the same reason a removal often has little to do. Orca reverts its statusline at every launch, so on a machine that has restarted since the wrapper went on, clearing the marker is the whole job and the report says the wrapper was not there. That is the normal case, not a sign that something went wrong earlier.

## The rules step takes away more than onboarding added

`apply` links `<config home>/rules/kein` at the home level, and the rules behind that link ship with the harness. Whatever rules the machine had before onboarding are not restored by removing the link — they were never displaced, they were simply not what the link points at.

So `remove --step rules` refuses without `--yes` and says what would be lost. Two ways forward, and the second is usually the better one:

- `--yes`, if the intent really is to have no rules loading.
- Leave the link alone and repoint it at a directory of the user's own. That keeps rules loading and is not a thing this script does — it is one `ln -sfn`.

Relay the refusal to the user rather than re-running with `--yes` on their behalf. It is a question about what they want loading in every project, and the script has no way to know the answer.

## What removal cannot do

Nothing here uninstalls the plugin, and nothing restores a hand-made setup that onboarding replaced. Orca's statusline script comes back from the backup under `<config home>/kein/onboard/`, and that backup is Orca's own version — refreshed whenever the hook found the file unwrapped, so it tracks Orca's updates rather than freezing at first install.
