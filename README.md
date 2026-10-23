# How to Build Skills

[![CI](https://github.com/Iknowitsimpossible/how-to-build-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/Iknowitsimpossible/how-to-build-skills/actions/workflows/ci.yml)

A hands-on course in writing **Agent Skills**: folders of instructions that teach an AI coding agent to do a task your way, every time. One skill works in Claude Code, Codex, claude.ai, and any other agent that supports the [open standard](https://agentskills.io).

You'll get eight short lessons, three working example skills (from one file to a real published skill), a template, and a validator that catches the mistakes that stop skills from loading.

## What is a skill?

A skill is a folder with a `SKILL.md` file in it:

```markdown
---
name: commit-message
description: Writes a git commit message for the staged changes. Use when the user says "write a commit message" or "commit this". Do NOT use for PR descriptions.
---

# Commit Message

## Instructions
1. Run `git diff --staged`.
2. Write a subject line of at most 50 characters, in the imperative mood...
```

The agent always sees every installed skill's `name` and `description`. When your request matches a description, it loads that skill's instructions and follows them. So you explain your process once, and the agent applies it whenever it's relevant.

## Quickstart: your first skill in 5 minutes

**1. Get this repo.**

```bash
git clone https://github.com/Iknowitsimpossible/how-to-build-skills.git
cd how-to-build-skills
```

**2. Copy the template into a new skill folder.** The folder name must match the `name` in the file.

```bash
mkdir -p my-skills/my-first-skill
cp templates/SKILL.template.md my-skills/my-first-skill/SKILL.md
```

**3. Edit `my-skills/my-first-skill/SKILL.md`.** Set `name: my-first-skill`, write a description that says what it does and when to use it ([lesson 3](lessons/03-frontmatter.md)), and replace the bracketed steps with your own.

**4. Check it.**

```bash
python3 tools/validate_skill.py my-skills/my-first-skill
```

Fix anything marked `error`, then run it again.

**5. Install it** in your agent's skills folder:

| Agent | All projects | One project | Call it by name |
|---|---|---|---|
| [Claude Code](platforms/claude-code.md) | `~/.claude/skills/` | `.claude/skills/` | `/my-first-skill` |
| [Codex](platforms/codex.md) | `~/.agents/skills/` | `.agents/skills/` | `$my-first-skill` |
| [claude.ai](platforms/claude-ai.md) | Upload a zip in Customize, Skills | | |

For Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -r my-skills/my-first-skill ~/.claude/skills/
```

**6. Try it.** Start a new session and type one of the phrases from your description. If the skill doesn't load, see [lesson 6](lessons/06-testing.md).

## Lessons

Read them in order; each takes about 10 minutes.

| # | Lesson | You'll learn |
|---|---|---|
| 1 | [What is a skill?](lessons/01-what-is-a-skill.md) | Folder anatomy, and the three levels of loading that keep skills cheap |
| 2 | [Plan your use cases](lessons/02-plan-use-cases.md) | Concrete use cases, three kinds of skills, defining success |
| 3 | [Write the frontmatter](lessons/03-frontmatter.md) | Naming rules, and descriptions that trigger at the right times |
| 4 | [Write the instructions](lessons/04-instructions.md) | `## Important`, specific steps, examples, troubleshooting |
| 5 | [Scripts and references](lessons/05-scripts-and-references.md) | When to bundle code, and loading docs only when needed |
| 6 | [Test your skill](lessons/06-testing.md) | Triggering, functional, and performance tests; iterating |
| 7 | [Patterns](lessons/07-patterns.md) | Five proven shapes for skill workflows |
| 8 | [Publish and share](lessons/08-publishing.md) | Repo layout, README, versioning, CI |

## Examples

Each example passes the validator and has a README explaining what to notice.

| Example | Shows |
|---|---|
| [1. Minimal: `commit-message`](examples/01-minimal/) | A complete skill in one file |
| [2. With references: `flashcard-maker`](examples/02-with-references/) | Reference files picked per task, and a checker script the skill runs on its own output |
| [3. Case study: `readme-organizer`](examples/03-readme-organizer/) | A real published skill, and the test-and-fix history that shaped it |

## Platforms

The lessons teach the open standard, which every agent below supports. These pages cover where each agent looks for skills, how to call one by name, and its extra features.

- [Claude Code](platforms/claude-code.md): `~/.claude/skills/`, `/skill-name`, extra fields like `disable-model-invocation`
- [Codex](platforms/codex.md): `~/.agents/skills/`, `$skill-name`, optional `agents/openai.yaml`
- [claude.ai and the Claude apps](platforms/claude-ai.md): zip upload, sandboxed scripts

## The validator

[`tools/validate_skill.py`](tools/validate_skill.py) checks one skill, or every skill in a folder, against the [Agent Skills spec](https://agentskills.io/specification) and Anthropic's published rules. It needs only Python 3 and no packages.

```bash
python3 tools/validate_skill.py path/to/skill-or-folder
```

**Errors** (the skill may not load): misspelled `SKILL.md`, missing `---` lines, unclosed quotes, a bad or mismatched `name`, a missing or too-long `description`, `<` or `>` in the frontmatter, a `README.md` inside the skill, or a mentioned `references/`/`scripts/` file that doesn't exist.

**Warnings** (it loads but may work worse): a description that never says when to use it, a `SKILL.md` over 500 lines, or fields outside the open spec.

Copy it into your own skill repo and run it in CI, like this repo does.

## Development

```bash
python3 tools/validate_skill.py examples    # validate the example skills
python3 -m unittest discover tests          # test the validator and the flashcard checker
```

CI runs both on every push.

## Sources and further reading

- [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) (Anthropic). Many ideas in these lessons come from it; the lessons explain them in their own words with new examples.
- [Agent Skills specification](https://agentskills.io/specification), the open standard
- [Claude Code skills docs](https://code.claude.com/docs/en/skills)
- [Codex skills docs](https://developers.openai.com/codex/skills)
- [anthropics/skills](https://github.com/anthropics/skills), Anthropic's public example skills

## License

[MIT](LICENSE)
