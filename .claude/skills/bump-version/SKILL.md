---
name: bump-version
description: Update this repo's plugin.json and marketplace.json versions together, commit, and push. Use when the user asks to bump, update, or release a new version of the kein plugin or marketplace manifest.
argument-hint: "New version, e.g. 0.0.2"
---

# Bump version

Run `./dev/kein-dev bump-version <new-version>` from the repository root, using the version the user gave. If they didn't give one, ask for it before running anything.

That command updates `plugin/.claude-plugin/plugin.json`'s `version` and `plugin/.claude-plugin/marketplace.json`'s top-level `version` and `plugins[0].version` together, and refuses to write anything if those three have already drifted apart.

It only edits files. Then commit the two manifests as `chore: <new-version>` and push the current branch; this is the only place this repository pushes, so push whatever local commits are ahead along with it. No tag is created unless the user asks for one.
