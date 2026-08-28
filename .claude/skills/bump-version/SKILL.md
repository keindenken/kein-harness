---
name: bump-version
description: Update this repo's plugin.json and marketplace.json versions together. Use when the user asks to bump, update, or release a new version of the kein plugin or marketplace manifest.
argument-hint: "New version, e.g. 0.0.2"
---

# Bump version

Run `./dev/kein-dev bump-version <new-version>` from the repository root, using the version the user gave. If they didn't give one, ask for it before running anything.

That command updates `plugin/.claude-plugin/plugin.json`'s `version` and `plugin/.claude-plugin/marketplace.json`'s top-level `version` and `plugins[0].version` together, and refuses to write anything if those three have already drifted apart.

It only edits files. It does not create a git tag, commit, or push — report the result and stop there unless the user separately asks for those.
