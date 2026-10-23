# Example 1: a minimal skill

[`commit-message/`](commit-message/) is the smallest useful skill: one folder, one `SKILL.md`, no scripts or reference files. Start here.

```text
commit-message/
└── SKILL.md
```

## What to notice

- **The description does three jobs.** It says what the skill does, lists phrases a user would actually type, and names the nearby tasks it should *not* take over (PR descriptions, changelogs). See [lesson 3](../../lessons/03-frontmatter.md).
- **`## Important` comes first.** The two rules that matter most (only staged changes; don't commit unless asked) sit above the steps, where an agent reads them before anything else. See [lesson 4](../../lessons/04-instructions.md).
- **Steps name exact commands.** "Run `git diff --staged`" leaves less room for guessing than "look at the changes".
- **Examples show the output format.** Two short examples teach the style faster than a paragraph of rules.
- **No scripts.** Nothing here needs a deterministic check, so the skill stays a single file. Example 2 shows when that changes.

## Try it

```bash
mkdir -p ~/.claude/skills
cp -r examples/01-minimal/commit-message ~/.claude/skills/
```

For Codex, copy it to `~/.agents/skills/` instead. Then stage a change in any repo and ask your agent: "write a commit message".
