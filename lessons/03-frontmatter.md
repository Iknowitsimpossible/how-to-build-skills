# 3. Write the frontmatter

The frontmatter is the few lines of YAML at the top of `SKILL.md`. It's the most important part of the skill, because for most of a session it's the *only* part the agent sees ([lesson 1](01-what-is-a-skill.md)). The agent decides whether to load your skill by reading the `description`.

## The minimum

```yaml
---
name: commit-message
description: Writes a git commit message for the staged changes. Use when the user says "write a commit message" or "commit this".
---
```

That's enough to work. Everything else is optional.

## `name`

- 1 to 64 characters: lowercase letters, digits, and hyphens (kebab-case). No spaces, capitals, or underscores.
- Can't start or end with a hyphen or contain `--`.
- **Must match the folder name.** `name: commit-message` lives in `commit-message/`.
- For Claude compatibility, avoid reserved names containing `claude` or `anthropic`. This is a platform restriction, not a universal rule of the open format.

| Name | OK? |
|---|---|
| `commit-message` | Yes |
| `Commit-Message` | No: capitals |
| `commit_message` | No: underscore |
| `commit message` | No: space |
| `claude-helper` | Claude compatibility restriction |

## `description`: what + when + what not

The spec allows up to 1,024 characters; this is a limit, not a target. Use the shortest description that makes selection clear. A description can include:

1. **What it does**, starting with a verb, specific enough to tell it apart from other skills.
2. **When to use it**: the phrases a user would actually type, and file types if relevant.
3. **When not to use it** (negative triggers): nearby tasks that should go elsewhere.

```text
[What it does] + [Key capabilities] + Use when the user says "..." / "..." + Do NOT use for ...
```

### Bad vs. good

**Too vague.** Matches everything, so the agent can't tell when it's the right choice:

```yaml
description: Helps with studying.
```

**Missing triggers.** Says what it does, but never when, and uses no words a student would type:

```yaml
description: Generates spaced-repetition artifacts from instructional content.
```

**Good.** Specific output, real phrases, file types, and a boundary:

```yaml
description: Turns lecture notes, slides, or a textbook chapter into study flashcards and saves them as a file that Anki or Quizlet can import. Use when the user says "make flashcards", "turn my notes into cards", "Anki deck from this", or "help me memorize this". Do NOT use for practice exams, summaries, or study schedules.
```

(That's the description of [`flashcard-maker`](../examples/02-with-references/flashcard-maker/SKILL.md).)

### Negative triggers: powerful, and easy to overdo

"Do NOT use for..." stops your skill from loading for nearby tasks. Use it when testing shows the skill loading too often ([lesson 6](06-testing.md)). But test negative triggers as carefully as positive ones: the [case study](../examples/03-readme-organizer/) had "Do NOT use for README files of the skill itself", which silently blocked a perfectly reasonable "review this README" request.

### Description checklist

- [ ] Starts with what the skill does, using a verb
- [ ] Uses plain language that matches the task; add example phrases only when they improve discovery
- [ ] Mentions file types or tools if they matter (`.csv`, Anki, `package.json`)
- [ ] Says what it's *not* for, if there's a nearby task it could be confused with
- [ ] Checked against the target platform's restrictions (see below)

## Optional fields from the open spec

```yaml
---
name: flashcard-maker
description: ...
license: MIT
compatibility: Needs file read and write access. Python 3 is optional, for the bundled checker.
allowed-tools: Read Write Bash(python3:*)
metadata:
  author: your-github-username
  version: 1.0.0
---
```

| Field | Use it for |
|---|---|
| `license` | The license, if you share the skill (`MIT`, `Apache-2.0`) |
| `compatibility` | Up to 500 characters on what the skill needs: agent type, programs, network access. Most skills don't need it. |
| `metadata` | Anything else as key-value pairs: `author`, `version`, and so on |
| `allowed-tools` | Tools the skill may use without asking. Experimental; support varies by agent. |

Individual agents add their own fields too (Claude Code has `disable-model-invocation`, for example). They're covered on the [platform pages](../platforms/). Do not assume an unknown field will be honored or ignored consistently; check the target agent.

## Format requirements and platform restrictions

- **The `---` lines are required**, both of them.
- **Close your quotes.** `description: "Does things` (no closing quote) is invalid YAML.
- **Platform restrictions:** some platform guidance restricts angle brackets or reserves names. The open specification does not make these universal YAML restrictions. The validator reports compatibility warnings; consult the target platform before publishing.
- **Keep the description on one line** unless you know YAML block syntax well. It avoids most mistakes.

After installing the repository dependencies, run the validator for YAML and structural checks. It also reports compatibility and style warnings; it cannot prove runtime behavior:

```bash
python3 tools/validate_skill.py path/to/my-skill
```

## Exercise

Rewrite this description using the checklist: `description: Makes my code better.`

<details>
<summary>One possible answer</summary>

```yaml
description: Reviews a Python file for readability and suggests clearer names, shorter functions, and missing docstrings, without changing behavior. Use when the user says "clean up this code", "make this more readable", or "review my Python style". Do NOT use for fixing bugs, performance tuning, or other languages.
```

</details>

## Your deliverable

A valid name and concise description.

**Self-check:** Can a reader distinguish this task from a nearby task without a long keyword list?

**Next:** [4. Write the instructions](04-instructions.md)
