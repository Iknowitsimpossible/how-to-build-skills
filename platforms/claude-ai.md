# claude.ai and the Claude apps

The Claude web, desktop, and mobile apps can use custom skills too. Instead of putting a folder on disk, you upload it as a zip. See Anthropic's help article [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) for the latest steps.

## Requirements

- **Code execution** must be turned on in your settings. Skills run in Claude's sandbox.
- Some plans or organizations may restrict skills; check the help article if you don't see the option.

## Upload a skill

1. Zip the **skill folder itself**, so the folder is at the top of the archive:

   ```bash
   cd examples/02-with-references
   zip -r flashcard-maker.zip flashcard-maker
   ```

   Zipping the *contents* (so `SKILL.md` sits at the root of the zip) doesn't work.

2. In Claude, open **Customize, Skills**, click **+**, choose to create a skill, then **Upload a skill** and pick the zip.
3. Make sure the skill is toggled on.
4. Test it in a new chat: "make Anki flashcards from these notes" (and paste or attach some notes).

## What's different from coding agents

- **No access to your computer.** Skills that read your local git repo (like [readme-organizer](../examples/03-readme-organizer/)) can't do their job here. Say so in the `compatibility` field.
- **Scripts run in a sandbox.** Bundled Python scripts can run, but only on files you upload into the chat.
- **Updates mean re-uploading.** There's no `git pull`; upload the new zip after each change.

## Common upload errors

| Problem | Cause | Fix |
|---|---|---|
| "Could not find SKILL.md" | File named `skill.md`, or the zip has no top-level folder | Rename to `SKILL.md`; zip the folder, not its contents |
| Invalid skill name | Capitals, spaces, or underscores in `name`, or it doesn't match the folder | Use kebab-case that matches the folder name |
| Invalid frontmatter | Missing `---` line, unclosed quote, `<` or `>` | Run `python3 tools/validate_skill.py path/to/skill` |

## Using skills from the API

Developers can also attach skills to Claude API requests. That's outside the scope of these lessons; see the [Agent Skills API guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide).
