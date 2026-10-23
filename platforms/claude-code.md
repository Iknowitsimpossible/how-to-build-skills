# Claude Code

[Claude Code](https://code.claude.com/docs/en/skills) supports the open Agent Skills format plus a few extra frontmatter fields of its own.

## Where to put skills

| Scope | Folder | Use for |
|---|---|---|
| Personal | `~/.claude/skills/<name>/SKILL.md` | Skills you want in every project |
| Project | `.claude/skills/<name>/SKILL.md` in the repo | Skills for one project, shared with everyone who clones it |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Skills distributed as part of a plugin |

If two skills have the same name, personal beats project.

Install a skill from this repo:

```bash
mkdir -p ~/.claude/skills
cp -r examples/01-minimal/commit-message ~/.claude/skills/
```

Or symlink it, so edits and `git pull` take effect without copying again:

```bash
ln -s "$PWD/examples/01-minimal/commit-message" ~/.claude/skills/commit-message
```

Claude Code watches these folders, so edits to an existing skill apply in the current session. If you created the `skills` folder itself during a session, run `/reload-skills` (or start a new session).

## Using a skill

- **Automatically:** Claude loads the skill when your request matches its `description`.
- **By name:** type `/commit-message` at the start of a message. Anything after the name is passed to the skill as arguments.

To test triggering, start a fresh session, send a should-trigger prompt, and watch for the skill being loaded in the transcript.

## Extra frontmatter fields

These work in Claude Code; other agents ignore them. The validator in this repo reports them as warnings, not errors, for that reason.

| Field | What it does |
|---|---|
| `disable-model-invocation: true` | Only you can run the skill (with `/name`). Good for things with side effects, like deploying. |
| `user-invocable: false` | Hidden from the `/` menu; only Claude can load it. Good for background knowledge. |
| `when_to_use` | Extra trigger text appended to the description. |
| `argument-hint` | Hint shown in autocomplete, such as `[issue-number]`. |
| `allowed-tools` | Tools the skill may use without asking each time, such as `Bash(git status *)`. |
| `model`, `effort` | Override the model or effort level while the skill runs. |
| `context: fork` | Run the skill in a separate subagent. |

The [Claude Code skills docs](https://code.claude.com/docs/en/skills) list every field.

## Arguments and live context

Claude Code fills in a few placeholders in the skill body before Claude reads it:

- `$ARGUMENTS` is everything typed after `/skill-name`; `$0`, `$1`, ... are individual arguments.
- `${CLAUDE_SKILL_DIR}` is the skill's own folder, handy for running bundled scripts from any directory.
- A line like `` !`git diff --staged --stat` `` runs the command first and puts its output into the skill.

These are Claude Code features. If you want your skill to work in other agents too, write plain instructions ("run `git diff --staged --stat`") instead.

## Skills vs. slash commands

Older Claude Code versions had custom commands in `.claude/commands/*.md`. They've been merged into skills: `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy`. Use a skill folder for anything new, since it can hold scripts and references.
