#!/usr/bin/env python3
"""Refuse git state changes from a subagent's Bash call; leave the lead's session alone.

Every worker brief says the same thing in prose: no git mutations, read-only git is fine, git state belongs to the lead. It failed on first contact when an executor ran `git stash push` on an untracked file (nothing captured) and then `git stash pop`, unpacking another session's June stash into a live worktree -- the stash stack is shared by every worktree of a repository, which is the reason the rule exists. This is that sentence as a mechanism.

Scope is the one thing that separates a worker's call from the lead's: a subagent's tool events carry `agent_id` and `agent_type`, the lead's do not. The lead keeps its own prose rule. A worker's git call passes only when every `git` invocation in the command is read-only -- an allowlist of reading subcommands, plus the reading forms of the ones that go both ways (`branch`, `tag`, `config`, `remote`, `worktree`, `stash`, `reflog`, `notes`, `apply --check`). Anything else exits 2, which blocks the call and hands the reason back to the model.
"""
import json
import shlex
import sys

GLOBAL_OPTIONS_WITH_ARG = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path", "--super-prefix", "--config-env"}

READ_ONLY = {
    "status", "log", "diff", "show", "ls-files", "ls-tree", "rev-parse", "rev-list", "blame", "grep", "cat-file",
    "describe", "shortlog", "name-rev", "merge-base", "check-ignore", "check-attr", "check-ref-format", "for-each-ref",
    "count-objects", "fsck", "whatchanged", "range-diff", "diff-tree", "diff-index", "diff-files", "ls-remote", "var",
    "version", "help", "archive", "show-ref", "verify-pack", "verify-commit", "verify-tag", "show-branch", "cherry",
    "format-patch", "annotate", "get-tar-commit-id", "rev-parse", "mailinfo", "column", "stripspace", "hash-object",
}

BRANCH_MUTATING = {"-d", "-D", "-m", "-M", "-c", "-C", "-f", "--force", "--delete", "--move", "--copy", "-u",
                   "--set-upstream-to", "--unset-upstream", "--edit-description", "-t", "--track"}
BRANCH_READ_FLAGS = {"--list", "-l", "-a", "-r", "-v", "-vv", "--show-current", "--contains", "--no-contains",
                     "--merged", "--no-merged", "--points-at"}
TAG_MUTATING = {"-d", "-a", "-s", "-u", "-f", "-m", "-F", "--delete", "--force", "--annotate", "--sign", "--edit"}
TAG_READ_FLAGS = {"-l", "--list", "--contains", "--no-contains", "--points-at", "--merged", "--no-merged"}
CONFIG_READ_FLAGS = {"--get", "--get-all", "--get-regexp", "--list", "-l", "--get-color", "--get-colorbool", "get", "list"}
APPLY_READ_FLAGS = {"--check", "--stat", "--numstat", "--summary"}


def _tokens(command: str):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:
        return command.split()


def _invocations(tokens):
    """Yield (subcommand, args) for every `git ...` in the command, args cut at the next shell operator."""
    operators = {";", "&&", "||", "|", "&", "(", ")", "<", ">", ">>", "<<"}
    for index, token in enumerate(tokens):
        if token != "git":
            continue
        cursor = index + 1
        while cursor < len(tokens) and tokens[cursor].startswith("-"):
            cursor += 2 if tokens[cursor] in GLOBAL_OPTIONS_WITH_ARG else 1
        if cursor >= len(tokens) or tokens[cursor] in operators:
            continue
        sub = tokens[cursor]
        args = []
        for item in tokens[cursor + 1:]:
            if item in operators:
                break
            args.append(item)
        yield sub, args


def _flags(args):
    return {a.split("=", 1)[0] for a in args if a.startswith("-")}


def _positionals(args):
    return [a for a in args if not a.startswith("-")]


def _reads_only(sub, args) -> bool:
    flags = _flags(args)
    if sub in READ_ONLY:
        return True
    if sub == "stash":
        return bool(args) and args[0] in {"list", "show"}
    if sub == "branch":
        if flags & BRANCH_MUTATING:
            return False
        return not _positionals(args) or bool(flags & BRANCH_READ_FLAGS)
    if sub == "tag":
        if flags & TAG_MUTATING:
            return False
        return not _positionals(args) or bool(flags & TAG_READ_FLAGS)
    if sub == "config":
        return bool(flags & CONFIG_READ_FLAGS) or (bool(args) and args[0] in CONFIG_READ_FLAGS)
    if sub == "remote":
        return not _positionals(args) or _positionals(args)[0] in {"show", "get-url"}
    if sub == "worktree":
        return bool(args) and args[0] == "list"
    if sub == "reflog":
        return not _positionals(args) or _positionals(args)[0] == "show"
    if sub == "notes":
        return bool(args) and args[0] in {"show", "list"}
    if sub == "symbolic-ref":
        return "-d" not in flags and "--delete" not in flags and len(_positionals(args)) <= 1
    if sub == "apply":
        return bool(flags & APPLY_READ_FLAGS)
    return False


def mutations(command: str):
    return [f"git {sub} {' '.join(args)}".strip() for sub, args in _invocations(_tokens(command)) if not _reads_only(sub, args)]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if not isinstance(payload, dict) or payload.get("tool_name") != "Bash":
        return 0
    if not (payload.get("agent_id") or payload.get("agent_type")):
        return 0
    command = (payload.get("tool_input") or {}).get("command", "")
    if not isinstance(command, str):
        return 0
    hits = mutations(command)
    if not hits:
        return 0
    print(
        "Refused: this git call changes repository state, and a worker leaves git state to the lead -- report what you would have done instead. "
        "Read-only git is fine (status, log, diff, show, ls-files, blame, grep, rev-parse, stash list, branch --show-current, apply --check ...). "
        "The stash stack is shared by every worktree of this repository, so a stash or pop here reaches other sessions' work; set a file aside under the scratch directory instead. "
        "Matched: " + "; ".join(hits),
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
