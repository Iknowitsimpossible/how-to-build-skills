---
name: commit-message
description: Writes a git commit message for the currently staged changes, with a short imperative subject line and a body that explains why. Use when the user says "write a commit message", "commit this", "what should I call this commit", or asks to describe their staged changes. Do NOT use for pull request descriptions, changelogs, or release notes.
---

# Commit Message

Write one commit message that a teammate could understand six months from now without opening the diff.

## Important

- Describe only what is **staged**. Unstaged changes are not part of the commit.
- Never run `git commit` yourself unless the user asked you to commit. Otherwise show the message and stop.

## Instructions

### Step 1: Read the staged changes

```bash
git diff --staged --stat
git diff --staged
git log --oneline -10
```

If nothing is staged, tell the user and ask whether to stage everything (`git add -A`) or stop. Use the log to match the repository's existing style (for example, whether it uses prefixes like `feat:` or `fix:`).

### Step 2: Write the message

- **Subject line:** imperative mood ("Add", "Fix", "Remove", not "Added" or "Adds"), at most 50 characters, no period at the end.
- **Blank line**, then a **body** wrapped at 72 characters that says *why* the change was made and anything surprising. Skip the body only for trivial changes such as fixing a typo.
- If the staged changes do two unrelated things, say so and suggest splitting them into two commits instead.

### Step 3: Show it

Show the message in a code block. If the user asked you to commit, run `git commit -F -` with the message on standard input so line breaks survive.

## Examples

**Example 1:** staged changes rename `calcTotal` to `calculateTotal` in 4 files and fix an off-by-one in its loop.

```text
Fix off-by-one in calculateTotal and rename it

The loop skipped the last item, so carts with one item totaled $0.
Renamed calcTotal to calculateTotal to match the other helpers.
```

**Example 2:** staged changes only fix a typo in the README.

```text
Fix typo in installation steps
```
