# 1. What is a skill?

A **skill** is a folder of instructions an AI agent can pick up when a task calls for it. Think of it as a recipe card you write once: instead of explaining your process in every conversation ("check the staged diff, keep the subject under 50 characters, explain *why* in the body..."), you put it in a skill, and the agent follows it whenever the task comes up.

Skills follow an open format, [Agent Skills](https://agentskills.io/specification), so the same folder works in Claude Code, Codex, claude.ai, and other agents that support the standard.

## Anatomy of a skill folder

```text
my-skill/
├── SKILL.md          # required: frontmatter + instructions
├── scripts/          # optional: code the agent runs
├── references/       # optional: extra docs the agent reads when needed
└── assets/           # optional: templates, images, data used in the output
```

Only `SKILL.md` is required. Its exact spelling matters: `skill.md` or `Skill.md` won't be found.

`SKILL.md` has two parts:

```markdown
---
name: commit-message
description: Writes a git commit message for the staged changes. Use when the user says "write a commit message" or "commit this".
---

# Commit Message

Step-by-step instructions go here, in plain Markdown.
```

- The **frontmatter** (between the `---` lines) is YAML. `name` and `description` are required.
- The **body** is Markdown: whatever instructions help the agent do the task well.

## Progressive disclosure: three levels of loading

An agent might have dozens of skills installed. If it read all of them into its context for every message, it would waste space and get confused. So skills load in three levels, each only when needed:

| Level | What loads | When | Rough size |
|---|---|---|---|
| 1. Metadata | `name` + `description` of **every** installed skill | Always, at the start of each session | ~100 tokens per skill |
| 2. Instructions | The body of **one** `SKILL.md` | When the agent decides that skill fits the task | Keep it under ~5,000 words |
| 3. Resources | Specific files in `references/`, `scripts/`, `assets/` | Only when a step in `SKILL.md` points to them | As large as needed |

An analogy: level 1 is the table of contents of a cookbook, level 2 is the recipe you turned to, level 3 is the appendix on how to temper chocolate, which you only read if this recipe needs it.

This shapes how you write skills:

- **The description decides everything.** At level 1 it's the *only* thing the agent sees. A great skill with a vague description never runs. ([Lesson 3](03-frontmatter.md).)
- **The body should be focused.** Every word is loaded each time the skill runs.
- **Detail goes in reference files** that the body points to, so the agent reads only what this particular task needs. ([Lesson 5](05-scripts-and-references.md).)

## What a skill is not

- **Not a tool or an API.** A skill doesn't give the agent new abilities like "call the Linear API". That's what tools and [MCP servers](https://modelcontextprotocol.io) do. A skill teaches the agent *how* to use the abilities it has. An MCP server is the kitchen; a skill is the recipe.
- **Not a project memory file.** `CLAUDE.md` or `AGENTS.md` is always loaded for one project. A skill loads only when a task matches, and works in any project.
- **Not the only skill running.** Several skills can be active at once, so don't write yours as if it controls the whole conversation.

## Check your understanding

1. You install 30 skills. How much of each one does the agent read when you send "hello"?
2. Your skill has a 40-page style guide. Where should it go, and why?
3. Why would a skill named `Commit Message` with a file called `skill.md` not work?

<details>
<summary>Answers</summary>

1. Only the `name` and `description` of each (level 1).
2. In `references/`, with a line in `SKILL.md` saying when to read it. Then it's only loaded for tasks that need it (level 3).
3. Two problems: names must be lowercase with hyphens (`commit-message`), and the file must be named exactly `SKILL.md`.

</details>

**Next:** [2. Plan your use cases](02-plan-use-cases.md)
