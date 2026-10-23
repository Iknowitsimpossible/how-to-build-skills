# Codex

OpenAI's [Codex](https://developers.openai.com/codex/skills) (CLI and IDE extension) reads the same `SKILL.md` format. A skill written to the open spec works without changes.

## Where to put skills

| Scope | Folder |
|---|---|
| User | `~/.agents/skills/<name>/SKILL.md` |
| Repository | `.agents/skills/<name>/SKILL.md`, in the current folder or any parent folder up to the repo root |
| Admin (whole machine) | `/etc/codex/skills/<name>/SKILL.md` |
| System | Built into Codex |

Note the folder is `.agents`, not `.codex`. Older third-party guides that say `~/.codex/skills` are out of date.

Install a skill from this repo:

```bash
mkdir -p ~/.agents/skills
cp -r examples/01-minimal/commit-message ~/.agents/skills/
```

Symlinks work too; Codex follows them:

```bash
ln -s "$PWD/examples/01-minimal/commit-message" ~/.agents/skills/commit-message
```

Codex usually notices new or changed skills by itself. If one doesn't show up, restart Codex.

## Using a skill

- **Automatically:** Codex picks a skill when your request matches its `description`.
- **By name:** type `$commit-message` in your message, or run `/skills` to browse and pick one.

## Frontmatter

Codex requires only `name` and `description`. Other spec fields are fine to include.

## Optional: `agents/openai.yaml`

Codex-specific settings go in a separate file inside the skill folder, so `SKILL.md` stays portable:

```text
commit-message/
├── SKILL.md
└── agents/
    └── openai.yaml
```

```yaml
interface:
  display_name: "Commit Message"
  short_description: "Write a commit message for staged changes"
policy:
  allow_implicit_invocation: false   # only run when called with $commit-message
```

| Section | What it controls |
|---|---|
| `interface` | How the skill appears in the app: `display_name`, `short_description`, icons, `brand_color`, `default_prompt` |
| `policy.allow_implicit_invocation` | `false` means Codex never picks the skill on its own; you must call it by name. Default `true`. |
| `dependencies.tools` | MCP servers the skill needs, so Codex can set them up |

This is the Codex counterpart of Claude Code's `disable-model-invocation`. Other agents ignore the file.

## Turning a skill off

Add an entry to `~/.codex/config.toml` and restart Codex:

```toml
[[skills.config]]
path = "/Users/you/.agents/skills/commit-message/SKILL.md"
enabled = false
```

## Built-in helpers

- `$skill-creator` asks what your skill should do and drafts it.
- `$skill-installer <name>` installs skills from a curated list or another repository.
